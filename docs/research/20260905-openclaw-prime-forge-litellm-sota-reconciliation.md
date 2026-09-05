# OpenClaw Baseline 5, LiteLLM Routing, and SOTA Enterprise Swarm Reconciliation

**Date:** 2026-09-05  
**Context:** Deep grounding across OpenClaw architecture v2, Baseline 5 roster (Prime, Forge, Scout, Sentinel, Operator), 17 ephemeral blueprints, LiteLLM gateway, Nix/Kubernetes infrastructure, and SOTA multi-agent enterprise engineering.  
**Author:** AI Pair Programmer with Mike  

---

## 1. The Original OpenClaw Workforce Architecture

From `openclaw-INTENT.md`, `openclaw-first-principles-architecture-v2.md`, and `pipelines/ideas/README.md`, Mike designed a structured division of labor:

```
┌───────────────────────────────────────────────────────────────────────────┐
│                          MIKE (Human Chairman)                            │
│           Final merge authority, budget approvals, strategic veto        │
└─────────────────────────────────────┬─────────────────────────────────────┘
                                      │ directs
                                      ▼
┌───────────────────────────────────────────────────────────────────────────┐
│                        PRIME (Executive Orchestrator)                     │
│         - High-judgment planning (Claude Opus 4.8 / Sonnet 3.7)           │
│         - Evaluates Scout's research; selects weekly business initiatives │
│         - Sets task scopes and reviews Forge's delivered PRs              │
└───────────────────┬───────────────────────────────────┬───────────────────┘
                    │ assigns implementation            │ assigns research
                    ▼                                   ▼
┌───────────────────────────────────┐   ┌───────────────────────────────────┐
│    FORGE (The Code Builder)       │   │   SCOUT (The Research Sensor)     │
│ - Bounded code engineering        │   │ - Nightly X intake ($0.001)       │
│ - Codex CLI / Claude Code / Jules │   │ - trafilatura + r.jina.ai scrape  │
│ - Ephemeral worktrees, unit tests │   │ - Local Qwen omlx topic clusters  │
│ - Strictly forbidden to self-judge│   │ - Feeds Karpathy Wiki in `Brain`  │
└───────────────────┬───────────────┘   └───────────────────┬───────────────┘
                    │                                       │
                    └───────────────────┬───────────────────┘
                                        ▼
┌───────────────────────────────────────────────────────────────────────────┐
│                       SENTINEL (The Watchdog & Auditor)                   │
│         - Enforces 2-try circuit breaker (kills loops after 2 fails)      │
│         - DLP (Data Loss Prevention) & credential pre-flight checks       │
│         - Hard budget limits ($10/session, $1,000/mo cap)                 │
│         - Deterministic test verification (npm test, pytest exit 0)       │
└─────────────────────────────────────┬─────────────────────────────────────┘
                                      │ protects
                                      ▼
┌───────────────────────────────────────────────────────────────────────────┐
│                       OPERATOR (System Admin & GitOps)                    │
│         - Git worktree lifecycle & 10-minute launchd reaper daemon        │
│         - LiteLLM gateway configuration & health monitoring               │
│         - Environment bootstrap (Nix / bootstrap.sh reproducibility)      │
└───────────────────────────────────────────────────────────────────────────┘
```

### The 17 Ephemeral Blueprints (Not 22 Running Pods)
A critical insight recovered from the OpenClaw decisions:
- Flat always-on swarms collapse past 8-10 agents due to message storms and token starvation.
- Mike's model is **Baseline 5 (always-on coordination) + Ephemeral N (on-demand execution)**.
- The 17 specialist blueprints (FAR shredder, pricing analyst, security auditor, test synthesizer) spin up dynamically as ephemeral tasks in isolated worktrees, execute their payload, push their branch, and scale to zero.

---

## 2. The Universal Inference Gateway: LiteLLM Proxy

From `personal-agent-sota.md` and `Agent SDLC.md`:
- Hand-built routing scripts and multi-provider failover wrappers were identified as a primary source of fragility.
- **The Solution**: Self-hosted **LiteLLM Proxy** (running on port 3100 or 4000).
  - Single standard OpenAI-compatible `/v1` endpoint.
  - Multi-provider fallback: if Anthropic or OpenAI returns HTTP 429 or quota exhaustion, LiteLLM automatically fails over to secondary routes without task disruption.
  - Free-tier first: Routes high-volume classification to local Apple Silicon OMLX (:8300), FreeLLMAPI free tiers, or Gemini 2.5 Flash (1M free context).
  - Frontier reserved: Claude Opus 4.8 and OpenAI o1 are guarded by Sentinel for high-judgment gates only.
  - Hard spend ceilings and token tracking per virtual API key.

---

## 3. Declarative Portability: Nix & Ephemeral Cloud Containers

To satisfy the requirement that the entire swarm can be stood up on any machine, laptop, or remote cloud instance in a few commands:
- **Nix / Nix Flakes (`flake.nix`)**:
  - Provides a bit-for-bit reproducible development environment across macOS (Apple Silicon) and Linux (cloud VMs).
  - Pinning `python 3.12`, `uv`, `ruff`, `ty`, `nodejs 22`, and `git` eliminates "works on my machine" drift.
- **Ephemeral Cloud Workers (Jules)**:
  - Offloads routine Tier 2/3 tasks to GitHub Jules cloud instances (100 free sessions/day).
  - Jules spins up in isolated cloud containers, executes against GitHub issues, and opens pull requests.
  - Zero local CPU/RAM footprint and zero local worktree residue.

---

## 4. First-Principles Reconciliation: What to Keep vs What to Adopt

| OpenClaw Concept | Historic Implementation | Modern SOTA Adopt-First Solution | Status |
|---|---|---|---|
| **Role Separation** | Complex custom agent loops | Baseline 5 roles (Prime, Forge, Scout, Sentinel, Operator) codified in `agents/docs/roles/` | **Keep & Formalize** |
| **Inference Router** | Hand-rolled Python routing | Self-hosted **LiteLLM Proxy** / FreeLLMAPI on port 3100 with fallback configs | **Adopt Maintained OSS** |
| **Ephemeral Runners** | Heavy Kubernetes cluster | Ephemeral Git worktrees with 10-min launchd reaper + GitHub Jules for cloud | **Radical Simplification** |
| **Knowledge Vault** | Complex custom database | **Karpathy Wiki-LLM** (Obsidian Markdown vault with wikilinks in `Brain`) | **Adopt SOTA Pattern** |
| **Agent Memory** | Monolithic prompt injection | **Garry Tan GBrain** (PGLite WASM vector + BM25 via MCP at `~/.gbrain/`) | **Adopt Maintained OSS** |
| **Task State Machine** | Custom SQLite queues | **GitHub Issues** as authoritative state machine + Fusion port 4040 for visual DAG | **Adopt Proven Tools** |
| **Declarative Bootstrap** | Custom multi-repo setup | Single declarative repository (`/Users/man/agents`) + Nix / `bootstrap.sh` | **Zero Overhead** |
