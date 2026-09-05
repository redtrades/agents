# System Disaster Recovery & Persistence Ledger (Disaster Recovery Blueprint)

Date: 2026-08-30
Machine: `m64` (Apple M1 Max, 64GB Unified Memory)
Purpose: Complete disaster recovery, persistence, and service manifest to reconstruct the entire AI agent stack, inference infrastructure, and Tailscale topology from scratch after a machine reset, macOS wipe, or hardware restore.

## 0. Current runtime qualification (observed 2026-08-31)

The manifest below is a reconstruction record, not proof of current model
residency. At observation time OMLX `:8300` was healthy with one model catalogued
but `loaded_count: 0`; llama.cpp `:8318` was healthy with its model loaded and zero
active requests. Both services were running independently. This is a resource
arbitration conflict, not a successful dual-engine configuration. The required
single-GPU lease, status, and recovery contract is in
[`LOCAL-INFERENCE-RESOURCE-ARBITER.md`](LOCAL-INFERENCE-RESOURCE-ARBITER.md).

Until that arbiter is deployed and its status endpoint is verified, do not claim
that both local engines are simultaneously available or safe to switch.

---

## 1. System-Level Boot Daemons & Hardware Limits

| Setting / Daemon | Path | Type | Value / Function |
|---|---|---|---|
| **GPU Wired Memory Limit** | `/Library/LaunchDaemons/com.mike.iogpu-wired-limit.plist` | Root LaunchDaemon (Runs at raw boot) | Sets `sysctl iogpu.wired_limit_mb=61440` (60GB dedicated to Metal GPU, leaving 4GB for macOS WindowServer). |
| **Tailscale Daemon** | `/Library/LaunchDaemons/com.tailscale.tailscaled.plist` | Root LaunchDaemon | Tailscale mesh networking daemon. |

---

## 2. Active LaunchAgents & Persistent Services (`~/Library/LaunchAgents/`)

Every persistent daemon is configured with `RunAtLoad: true` and `KeepAlive: true` to survive logout, login, and reboot:

| Service Label | Plist Path | Port | Command / Binary | Function |
|---|---|---|---|---|
| `com.mike.omlx-server` | `~/Library/LaunchAgents/com.mike.omlx-server.plist` | **8300** | `/Users/man/.venv-omlx/bin/omlx serve --host 127.0.0.1 --port 8300 --hf-cache --memory-guard-gb 59` | OMLX service; model residency is lazy and must be admitted by the GPU arbiter. |
| `com.hermes.free-llm-proxy` | `~/Library/LaunchAgents/com.hermes.free-llm-proxy.plist` | **4000** | `/Users/man/.hermes/scripts/run_free_llm_proxy.sh` (`litellm --config ~/.hermes/litellm_config.yaml`) | Unified LiteLLM proxy routing Hermes, Buzz, and OpenCode across Gemini Flash, Mistral, and OpenRouter free tiers. |
| `com.hermes.webui` | `~/Library/LaunchAgents/com.hermes.webui.plist` | **8787** | `~/.hermes/webui/launchd-start.sh` | Hermes WebUI interactive chat front-end. |
| `com.mike.status-dashboard` | `~/Library/LaunchAgents/com.mike.status-dashboard.plist` | **8901** | Python static HTTP server | Glance real-time dashboard displaying GPU/Metal utilization, RAM/swap, and active requests. |
| `com.macmon` | `~/Library/LaunchAgents/com.macmon.plist` | **9090** | `/usr/local/bin/macmon` (or local binary) | Sudoless real-time Metal / IOReport GPU utilization JSON stream. |
| `com.mike.sssf-visualizer` | `~/Library/LaunchAgents/com.mike.sssf-visualizer.plist` | **4600** | `bun run server/index.ts` | Super Simple Software Factory trace visualizer and session database UI. |
| `com.mike.freellmapi-server` | `~/Library/LaunchAgents/com.mike.freellmapi-server.plist` | **3101** | `sandbox-exec -f freellmapi.sb node server/dist/index.js` | FreeLLMAPI router backend under Seatbelt sandbox. |
| `com.mike.hermes-free-models-sync` | `~/Library/LaunchAgents/com.mike.hermes-free-models-sync.plist` | Scheduled | `~/.hermes/scripts/sync_free_models.sh` | Periodic probe syncing healthy free tier models into the proxy config. |

---

## 3. Dedicated Python Virtual Environments (`~/.venv-*`)

| Virtual Environment | Location | Key Packages | Purpose |
|---|---|---|---|
| **`omlx`** | `/Users/man/.venv-omlx` | `omlx`, `mlx`, `mlx-lm`, `transformers` | Local MLX Apple Silicon inference server with custom kernel optimizations. |
| **`litellm` (Hermes)** | `/Users/man/.hermes/hermes-agent/venv` | `litellm[proxy]`, `httpx`, `pydantic` | Running the live LiteLLM proxy on port 4000. |
| **`litellm` (Global)** | `/Users/man/.venv-litellm` | `litellm[proxy]`, `fastapi`, `uvicorn` | Standalone unified gateway runtime. |
| **`vllm-metal`** | `/Users/man/.venv-vllm-metal` | `vllm`, `torch` | Benchmark engine for Metal kernel evaluations. |

---

## 4. Tailscale Serve Network Topology & Service Aliases (`m64.tailfb03be.ts.net`)

Live verified from `tailscale serve status`. All internal loopback services are securely exposed to authenticated devices on the personal Tailscale tailnet (`m64`, `iphone181`, `m16`):

### 4.1 Root Port 443 Path Mappings (`https://m64.tailfb03be.ts.net`)
| External Path | Loopback Target | Service Description |
|---|---|---|
| `https://m64.tailfb03be.ts.net/` | `127.0.0.1:8902` | Landing Page & Service Portal |
| `https://m64.tailfb03be.ts.net/status` | `127.0.0.1:8901` | Live Glance GPU / Memory / Request Status Dashboard |
| `https://m64.tailfb03be.ts.net/admin` | `127.0.0.1:8300/admin` | omlx Server Admin & Model Management Panel |
| `https://m64.tailfb03be.ts.net/gpu` | `127.0.0.1:9090` | Macmon raw GPU telemetry JSON feed |
| `https://m64.tailfb03be.ts.net/proxy` | `127.0.0.1:4000` | LiteLLM Unified Free Proxy Endpoint |
| `https://m64.tailfb03be.ts.net/llama` | `127.0.0.1:8318` | llama.cpp / Flash-Next Local Backend Endpoint |
| `https://m64.tailfb03be.ts.net/benchmarks-live` | `127.0.0.1:8903` | Live Benchmark Dashboard |

### 4.2 Dedicated HTTPS Port Mappings
| External Tailnet URL | Loopback Target | Service Description |
|---|---|---|
| `https://m64.tailfb03be.ts.net:8443` | `127.0.0.1:4600` | SSSF Workflow Visualizer & Trace UI (`/sssf/` alias) |
| `https://m64.tailfb03be.ts.net:8444` | `127.0.0.1:3100` | FreeLLMAPI Enforcement Gateway (`/freellmapi/` alias) |
| `https://m64.tailfb03be.ts.net:8445` | `127.0.0.1:8787` | Hermes WebUI (`/hermes/` alias) |
| `https://m64.tailfb03be.ts.net:8446` | `127.0.0.1:5001` | MLflow Experiment Tracking Server (`/mlflow/` alias) |

---

## 5. Model Assets on Disk

| Storage Path | Approx Size | Key Models | Notes |
|---|---|---|---|
| `~/.cache/huggingface/hub/` | ~34 GB | `mlx-community/Qwen3.8-27B-8bit`<br>`Qwen3-32B`<br>`Qwen3.5-4B-MLX-8bit` | Main weight storage for omlx. Served directly out of HF cache. |
| `~/.omlx/models/` | ~4.8 GB | `mlx-community/Qwen3.5-4B-MLX-8bit` | Dedicated omlx storage directory. |
| `~/.buzz/models/` | ~300 MB | `pocket-tts`, `parakeet-tdt-ctc-110m-en` | ASR & TTS voice models for Buzz desktop app. |

---

## 6. Verification Script After Reboot

To instantly verify that all LaunchAgents, sysctl limits, ports, and Tailscale endpoints survived a reboot or wipe, run:

```bash
bash ~/agent-reports/verify-persistence.sh
```
Expectation: **22 OK, 0 FAIL**.
