# Unified Multi-Agent Swarm Architecture Specification (2026)

## Executive Summary

This document establishes the canonical, end-to-end systems architecture for the autonomous multi-agent engineering swarm. It synthesizes all historical estate lessons, first-principles systems engineering decompositions, and the 2026 state of the art across nine decoupled layers:

1. Estate Governance & Canonical Authority
2. Visual Cockpit & Token Telemetry
3. Durable State & Concurrency Engine
4. Inter-Agent Communication & Protocols
5. Inference Gateway & 4-Tier Cost Routing
6. Execution Harnesses & Ephemeral Sandboxes
7. Memory, Context Management & Knowledge
8. Skills, Plugins & Self-Compounding Loop
9. Autonomous Proactive SDLC Pipeline

---

## Layer 1: Estate Governance & Canonical Authority

- **Canonical Source of Truth:** GitHub (`https://github.com/redtrades/*`) is the absolute master authority for all code, pull requests, issues, and releases.
- **Human Chair (Solo Operator):** Mike directs high-level intent, approves budgets, and maintains ultimate administrative control.
- **Autonomous Merge Policy:** To eliminate the human bottleneck, any pull request that passes deterministic verification (`npm test`, `pytest`, static linters) and receives an adversarial `APPROVE` verdict from an independent peer model family (e.g., Claude Code reviewed by Codex/Grok) merges directly to `main` without manual intervention.

---

## Layer 2: Visual Cockpit & Token Telemetry

- **Primary Interface:** Runfusion / Fusion web application active on port 4040 (`http://localhost:4040`).
- **Live Board Tracking:** Displays tasks moving across four standard columns: `Backlog`, `In Progress`, `Review`, and `Done`.
- **Milestone & DAG Drill-Down:** Provides visual inspection into multi-step task dependencies, subagent handoffs, and execution logs.
- **Real-Time Token & Cost Accounting:** Tracks prompt tokens, completion tokens, and cached tokens in real time, broken down by model provider (Anthropic, OpenAI, FreeLLMAPI, local inference).

---

## Layer 3: Durable State & Concurrency Engine

- **State Engine:** Hatchet durable workflow engine (`hatchet.run`) backed by PostgreSQL.
- **Crash Resilience & Replay:** Every agent step is an idempotent activity. If a machine reboots or an API hits rate limits (HTTP 429), the workflow resumes from the latest checkpoint without re-spending tokens on past steps.
- **Concurrency & WIP Limits:** Enforced via Hatchet Common Expression Language (CEL) concurrency keys:
  - `WIP = 1` per individual git repository.
  - Global `WIP <= 3` active workers across the entire estate.
- **Two-Try Circuit Breaker:** If an action or test fails twice in succession, the task immediately halts and flags for review, preventing infinite recursive failure loops.

---

## Layer 4: Inter-Agent Communication & Protocols

- **Agent Client Protocol (ACP):** Universal open standard for orchestrator-to-agent communication over stdio and WebSockets, allowing any compatible harness to be invoked interchangeably.
- **Model Context Protocol (MCP):** Universal standard connecting agents to local tools, databases, and filesystem resources.
- **Decentralized Agent Relay (Buzz):** Built on Nostr protocols (`~/.buzz`), giving agents cryptographic keypairs (`nsec`/`npub`), inter-agent channels (NIP-01/02), collaborative markdown canvases for co-authoring specifications, and decentralized git collaboration (NIP-34).
- **Structured Artifact Handoffs:** Agents do not engage in unstructured chatroom banter. Communication between stages occurs via typed files (plans, diffs, review verdicts) written to disk.

---

## Layer 5: Inference Gateway & 4-Tier Cost Routing

- **Gateway Engine:** LiteLLM Proxy running on port 3100. Unifies all upstream providers behind a standard OpenAI-compatible `/v1/chat/completions` endpoint with automated fallbacks, virtual keys, and prompt caching.
- **Tier 0: Local Apple Silicon Inference ($0.00)**
  - Engine: oMLX (`jundot/omlx`) running Qwen 2.5 Coder 32B or Llama 3.3 70B on port 8300.
  - Advantage: Paged SSD KV caching enables instantaneous prompt resumption at zero marginal cost. Used for continuous formatting, test analysis, and offline tasks.
- **Tier 1: Cloud Free Tiers ($0.00)**
  - Google Gemini 2.5 Flash: 1M token context for massive repository ingestion and RFP analysis.
  - Groq LPU: High-speed inference (300 to 800 tok/s) for sub-300ms AST verification and JSON extraction.
  - Cloudflare Workers AI: 10k neurons/day for edge webhooks and BAAI BGE embeddings.
  - FreeLLMAPI: Fallback quota harvester across 30+ free providers.
- **Tier 2: Asynchronous Cloud PR Workers ($20.00/month flat)**
  - GitHub Jules (Google AI Pro): 100 autonomous sessions/day in secure cloud VMs for routine bug fixes, test generation, and documentation.
- **Tier 3: Frontier Subscriptions (Protected)**
  - Claude Code (Max Subscription) and OpenAI Codex CLI (o3) reserved strictly for complex architectural design and security reviews.

---

## Layer 6: Execution Harnesses & Ephemeral Sandboxes

- **Interchangeable Harness Roster:**
  - **Goose (`block/goose`):** Primary on-machine ACP execution harness for local tool use, builds, and native diff reviews (`goose review`).
  - **Hermes Agent (`NousResearch/hermes-agent`):** Persistent background reasoning harness providing Mixture-of-Agents (MoA) parallel exploration and self-improving skill discovery.
  - **Aider (`paul-gauthier/aider`):** Specialized repo mapper using tree-sitter and PageRank to supply compact structural context to other agents.
  - **Claude Code & Codex CLI:** Frontier interactive reasoning CLIs driven via headless non-interactive commands.
- **Ephemeral Git Worktrees:**
  - Every task executes in an isolated worktree at `.worktrees/issue-<number>`.
  - Protected by POSIX atomic lockfiles (`.claim.lock`).
  - A 10-minute launchd reaper daemon kills orphaned processes and unlinks clean worktrees older than 120 minutes.

---

## Layer 7: Memory, Context Management & Knowledge

- **Garry Tan's GBrain (`garrytan/gbrain`):** Embedded PostgreSQL database (PGlite WASM) with `pgvector` stored at `~/.gbrain/brain.pglite`. Automatically extracts typed knowledge graphs and serves hybrid vector + BM25 search via MCP.
- **Karpathy Wiki-LLM:** Obsidian markdown vault in `Brain/` with bi-directional `[[wikilinks]]` and Map of Content (MOC) index tables. Progressive disclosure ensures agents only load relevant nodes.
- **Context Hygiene & Caveman Minimalism:**
  - Resident system prompts are strictly capped under 800 tokens.
  - JuliusBrussee Caveman syntax strips conversational filler from agent-to-agent exchanges, saving 65% to 75% of context window space.
  - DietrichGebert Ponytail YAGNI ladder prioritizes native Unix commands and stdlib utilities over custom code.

---

## Layer 8: Skills, Plugins & Self-Compounding Loop

- **Cross-Harness Skill Foundation:** 183 skills and 92 plugins maintained in `plugins/` and automatically compiled across Claude Code, Codex, OpenCode, Cursor, and Antigravity via `make generate-all`.
- **Compound Engineering Loop (`EveryInc/compound-engineering-plugin`):**
  - Standard development cycle: Brainstorm -> Plan -> Work -> Review -> Compound.
  - The `/ce-compound` command captures post-task learnings, root-cause fixes, and edge cases, permanently committing them into repository rules to prevent regression loops.
- **Declarative Optimization (Stanford DSPy):** Replaces brittle manual prompt engineering with typed `dspy.Signature` modules compiled against deterministic test suites.

---

## Layer 9: Autonomous Proactive SDLC Pipeline

```
┌───────────────────────────────────────────────────────────────────────────┐
│                     STEP 1: PROACTIVE SENSOR (Scout)                      │
│ - Continuous git commit hooks, test regression checks, and security scans │
│ - Automatically creates a structured ticket on the Fusion Board           │
└─────────────────────────────────────┬─────────────────────────────────────┘
                                      │
                                      ▼
┌───────────────────────────────────────────────────────────────────────────┐
│                     STEP 2: AUTOMATED LOE TRIAGE GATE                     │
│ - Sizes task: Small (S), Medium (M), Large (L), or Extra Large (XL)       │
│ - Binds S to local/free models, M to Jules cloud, L/XL to Claude/Codex    │
└─────────────────────────────────────┬─────────────────────────────────────┘
                                      │
                                      ▼
┌───────────────────────────────────────────────────────────────────────────┐
│                     STEP 3: ISOLATED WORKTREE EXECUTION                   │
│ - Spins up ephemeral worktree: .worktrees/issue-<id>                      │
│ - Generator agent (Goose / Hermes / Claude) writes code and tests         │
└─────────────────────────────────────┬─────────────────────────────────────┘
                                      │
                                      ▼
┌───────────────────────────────────────────────────────────────────────────┐
│                     STEP 4: DETERMINISTIC VERIFICATION                    │
│ - Executes test suites (npm test, pytest, cargo test, typecheck, lint)    │
│ - Two-try circuit breaker halts immediately on repeated failures          │
└─────────────────────────────────────┬─────────────────────────────────────┘
                                      │
                                      ▼
┌───────────────────────────────────────────────────────────────────────────┐
│                     STEP 5: ADVERSARIAL PEER CODE REVIEW                  │
│ - Opposing model family audits diff against issue acceptance criteria     │
│ - Must emit an unambiguous APPROVE verdict before merge                   │
└─────────────────────────────────────┬─────────────────────────────────────┘
                                      │
                                      ▼
┌───────────────────────────────────────────────────────────────────────────┐
│                     STEP 6: ZERO-BOTTLENECK AUTO-MERGE                    │
│ - Merges directly to main branch without human bottleneck                 │
│ - Prunes ephemeral worktree and closes issue on Fusion board              │
│ - Executes /ce-compound to update persistent project memory               │
└───────────────────────────────────────────────────────────────────────────┘
```
