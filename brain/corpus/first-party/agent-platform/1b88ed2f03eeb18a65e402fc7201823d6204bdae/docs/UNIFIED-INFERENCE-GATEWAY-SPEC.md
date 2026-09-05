# Phase 1: Unified Model Inference Router Specification & Deployment Guide

Date: 2026-08-30
Component: LiteLLM Proxy / Port :3100 Unified Routing Gateway

---

## 1. Objective

Provide a single, resilient, OpenAI-compatible proxy listening on `127.0.0.1:3100` that unifies all local and hosted LLMs for **Hermes**, **Buzz**, **OpenCode**, **Pi**, and **Claude Code**, while enforcing:
1. **Zero-Contention Local Inference:** OMLX and llama.cpp share one exclusive GPU lease; only one engine may have a resident model at a time. Request concurrency is bounded by the active engine profile.
2. **Large-Context Long-Tail Routing:** 100+ page solicitation / RFP digestion routes to Google Gemini Flash (1M+ context free tier).
3. **Sub-Second JSON Schema Extraction:** Structural envelope generation routes to Groq Cloud (Free Tier).
4. **Automatic Fallback & Health Tracking:** If a provider rate limits or goes dark, requests seamlessly fail over to backup models without crashing active agent workflows.

---

## 2. Port & Network Topology

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ CLIENT HARNESSES: Hermes, Buzz (via hermes-acp), OpenCode, Pi, Claude Code   │
│ (All pointed at: http://127.0.0.1:3100/v1 with Bearer token)                 │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ LiteLLM Proxy (:3100 Gateway - LaunchAgent com.mike.unified-inference-proxy)│
│                                                                             │
│ - Virtual Model Aliases:                                                    │
│   • `coding-workhorse`      -> Local MLX (:8300) -> Fallback: Groq Qwen     │
│   • `rfp-analyst`           -> Gemini 2.0 Flash (Free) -> Fallback: Groq    │
│   • `fast-json-extractor`   -> Groq Llama 3.3 70B (Free)                    │
│   • `deep-reasoner`         -> Gemini 2.0 Pro / Local Qwen 3.8 27B          │
│                                                                             │
│ - Health checks, token rate limiters, PII denylist & SQLite request logger  │
└───────┬──────────────────────────────┬──────────────────────────────┬───────┘
        │                              │                              │
        ▼                              ▼                              ▼
┌───────────────────────┐   ┌───────────────────────┐   ┌───────────────────────┐
│ Local M1 Max (OMLX OR llama.cpp; arbiter owns GPU lease) │   │ Google AI Studio      │   │ Groq Cloud API        │
│ http://127.0.0.1:8300 │   │ Gemini Flash / Pro    │   │ Llama 3.3 70B / Qwen  │
│ (Free, Local, Private)│   │ (Free 15 RPM / 1M ctx)│   │ (Free 30 RPM / 300 t/s)│
└───────────────────────┘   └───────────────────────┘   └───────────────────────┘
```

---

## 3. Configuration Specification: `litellm-config.yaml`

```yaml
model_list:
  - model_name: coding-workhorse
    litellm_params:
      model: openai/mlx-community--Qwen3.8-27B-8bit
      api_base: http://127.0.0.1:8300/v1
      api_key: "sk-local-mlx"
      max_parallel_requests: 2
      tpm: 100000
      rpm: 60

  - model_name: rfp-analyst
    litellm_params:
      model: gemini/gemini-2.0-flash-exp
      api_key: os.environ/GEMINI_API_KEY
      rpm: 15
      max_tokens: 8192

  - model_name: fast-json-extractor
    litellm_params:
      model: groq/llama-3.3-70b-versatile
      api_key: os.environ/GROQ_API_KEY
      rpm: 30
      response_format: {"type": "json_object"}

  - model_name: fallback-coding
    litellm_params:
      model: groq/qwen-2.5-coder-32b
      api_key: os.environ/GROQ_API_KEY
      rpm: 30

router_settings:
  fallbacks:
    - coding-workhorse: ["fallback-coding", "rfp-analyst"]
    - rfp-analyst: ["fast-json-extractor"]
  routing_strategy: "least-busy"
  num_retries: 3
  timeout: 120

general_settings:
  master_key: "sk-unified-agent-key"
  database_url: "sqlite:////Users/man/.litellm/litellm.db"
```

---

## 4. Client Harness Integration

### 4.1 Hermes (`~/.hermes/config.yaml`)
```yaml
model: "custom:unified:coding-workhorse"
providers:
  unified:
    base_url: "http://127.0.0.1:3100/v1"
    api_key: "sk-unified-agent-key"

# The local profiles select an arbiter lease; they do not start engines directly.
# Keep both profiles available:
#   local-omlx      -> engine=omlx      -> 127.0.0.1:8320/v1
#   local-llamacpp  -> engine=llamacpp  -> 127.0.0.1:8320/v1
```

### 4.2 OpenCode (`~/.config/opencode/opencode.json`)
```json
{
  "providers": {
    "unified": {
      "baseUrl": "http://127.0.0.1:3100/v1",
      "apiKey": "sk-unified-agent-key",
      "models": [
        "coding-workhorse",
        "rfp-analyst",
        "fast-json-extractor"
      ]
    }
  }
}
```

### 4.3 Pi Harness (`~/.pi/agent/models.json`)
```json
{
  "providers": {
    "unified": {
      "type": "openai",
      "url": "http://127.0.0.1:3100/v1",
      "key": "sk-unified-agent-key"
    }
  }
}
```

---

## 5. Verification & Health Monitoring

1. **Health Check Endpoint:**
   `curl -i http://127.0.0.1:3100/health`
2. **Local arbiter status:** `curl -sS http://127.0.0.1:8320/status`.
   This is the authoritative view of residency, lease ownership, requests, and
   token rates; `/v1/models` alone is only catalog evidence.
3. **Model Listing Endpoint:**
   `curl http://127.0.0.1:3100/v1/models -H "Authorization: Bearer sk-unified-agent-key"`
4. **Structured Completion Test:**
   ```bash
   curl http://127.0.0.1:3100/v1/chat/completions \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer sk-unified-agent-key" \
     -d '{
       "model": "fast-json-extractor",
       "messages": [{"role": "user", "content": "Return JSON: {\"status\": \"ok\"}"}]
     }'
   ```
