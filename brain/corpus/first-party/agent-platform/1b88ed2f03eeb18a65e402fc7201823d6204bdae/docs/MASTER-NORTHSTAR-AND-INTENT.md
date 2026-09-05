# Master North Star & Intent Synthesis — The Software Agent Factory

Date: 2026-08-30
Author: Synthesized across 5 months of historical archives (`OpenClaw` v1–v3, `agent-mesh`, `agent-configs`, `agent-workspace`, `govcon-factory`, and `agent-platform`).

---

## 1. Executive Summary & Founding Intent

Across five months of continuous iteration, the underlying north star has remained fixed:

> *"I still want to have the agnostic, genetic harness and plug-in-play brain and body so that any model can be implemented into the baseline or any of the other agents... Think of composable modular architecture, but for agentic swarms."* — Mike (Founding Directive, April 2026)

The vision is a **solo-operator enterprise** driven by a continuously operating, provider-neutral agent workforce producing reviewed software and revenue-generating business deliverables with **95% autonomy**.

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│ THE DUAL ENGINE OF THE OPERATING INTENT                                                          │
├──────────────────────────────────────────────────┬───────────────────────────────────────────────┤
│ 1. THE PRODUCTION REVENUE ENGINE                 │ 2. THE AUTONOMOUS SOFTWARE AGENT FACTORY      │
│    (govcon-factory / Business Deliverables)       │    (The System That Builds The System)        │
│                                                  │                                               │
│ - Eliminates federal contracting capture tedium: │ - Mind / Body / Brain composability:          │
│   FAR/DFARS compliance matrices, Section L/M     │   Harness-neutral roles in Git; swappable     │
│   rubric extraction, past performance matching.  │   harnesses; multi-tier inference routing.    │
│ - Public data -> computed high-intent hooks      │ - Crash-proof durable execution: work         │
│   -> submission-ready starters ($699–$5,000).    │   survives rate limits, context windows,      │
│ - Target: $8K–$10K/mo net profit with <= 40 hrs/ │   agent crashes, and machine reboots.         │
│   week of human strategic oversight.             │ - "Generator != Judge": multi-principal       │
│                                                  │   verification and deterministic gating.      │
└──────────────────────────────────────────────────┴───────────────────────────────────────────────┘
```

---

## 2. Historical Lineage & Lessons Learned

| Era | Timeline | Core Implementation | Failure Mode / Why It Stalled |
|---|---|---|---|
| **Era 1: OpenClaw v1** | Apr 2026 – May 2026 | 138 Markdown Decision Rules (`CLAUDE.md`), Slack `#prime`, JSONL ledgers, SwarmClaw PWA. | Aspirational rules: markdown prose without automated gating led to prompt drift and unenforced constraints. |
| **Era 2: OpenClaw v2–v3** | May 2026 – June 2026 | `gbrain` canonical tools, commit transaction primitives, courtroom topology. | Tool bloat (gbrain reached 124 tools / 28K tokens), exhausting LLM context windows. |
| **Era 3: Pre-Wipe Reset & SSSF** | July 2026 – Aug 2026 | Super Simple Software Factory (SSSF), launchd daemons, local MLX benchmarks. | Fragile Python loops; local GPU contention (1500s hangs); sessions dying silently at context limits. |
| **Era 4: Agent-Mesh & Configs** | Aug 2026 | Consolidated `.agent/` portable brain, 12 research digests, separated library configs. | Model configuration fragmentation across Hermes, Buzz, Pi, and OpenCode; lack of unified routing. |
| **Era 5: Agent-Platform Gate C** | Late Aug 2026 | GitHub Contents CAS authority, isolated worktrees, multi-App verification (`#103`). | High ceremony around manual issue promotion; need for a self-healing durable execution substrate. |

---

## 3. First-Principles Architecture of the Agent Factory

The architecture decouples **Task State**, **Execution Context**, **Inference Routing**, and **Verification**.

```
                                  ┌────────────────────────────────────────────────────────┐
                                  │      GitHub Issues / Project 12 (Intent & Mutex)       │
                                  └───────────────────────────┬────────────────────────────┘
                                                              │ Webhook / CAS Lease
                                                              ▼
┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ 1. DURABLE ORCHESTRATION SPINE (Temporal.io OSS / Hatchet.run)                                                           │
│    - Deterministic state machine surviving process deaths, context limits, and machine reboots.                          │
│    - Lifecycle: TASK_INTAKE -> CAS_LEASE -> HYDRATE_WORKTREE -> DISPATCH -> DETERMINISTIC_GATES -> VERIFY -> PROMOTE     │
└───────┬──────────────────────────────────────────────┬──────────────────────────────────────────┬────────────────────────┘
        │ Hydrates                                     │ Routes Inference                         │ Verifies
        ▼                                              ▼                                          ▼
┌───────────────────────────────┐     ┌─────────────────────────────────┐        ┌─────────────────────────────────┐
│ 2. ISOLATED WORKSPACE RUNNER  │     │ 3. UNIFIED INFERENCE (:3100)    │        │ 4. DUAL-GATE VERIFICATION       │
│                               │     │                                 │        │                                 │
│ - Ephemeral Git Worktrees     │     │ - LiteLLM Proxy (Port 3100)     │        │ - Gate 1: Deterministic CI      │
│ - macOS Seatbelt sandbox      │     │ - Tier 1: Local MLX (Qwen 3.8)  │        │   (Pytest, AST, Ruff, schemas)  │
│ - Pydantic V2 JSON envelopes  │     │ - Tier 2: Gemini Flash (Free 1M)│        │ - Gate 2: Independent Review    │
│ - Grammar-constrained decode  │     │ - Tier 3: Groq Cloud (Free JSON)│        │   (Read-only Reviewer App)      │
│   (xgrammar / GBNF schemas)   │     │ - Auto-fallback & rate limits   │        │ - Gate 3: Promoter App Merge    │
└───────────────────────────────┘     └─────────────────────────────────┘        └─────────────────────────────────┘
                                                       │                                          │
                                                       ▼                                          ▼
                                      ┌─────────────────────────────────┐        ┌─────────────────────────────────┐
                                      │ 5. OBSERVABILITY (Langfuse OSS) │        │ 6. PERSISTENCE (Litestream + R2)│
                                      │ - Tracing, tokens, latency, eval│        │ - Zero-egress SQLite replication│
                                      └─────────────────────────────────┘        └─────────────────────────────────┘
```

---

## 4. Modern Stack Selection: Open-Source, Free-Tier & Low-Cost

| Layer | Recommended SOTA Component | Cost / License | Solves What Failed Historically |
|---|---|---|---|
| **Durable Task Spine** | **Temporal (OSS)** or **Hatchet.run (OSS)** | Apache 2.0 / $0 | Eliminates fragile background cron loops. Resumes interrupted agent sessions automatically upon reboot. |
| **Inference Router** | **LiteLLM Proxy (Port :3100)** | MIT / $0 | Unifies Hermes, Buzz, Pi, and OpenCode under one OpenAI-compatible endpoint with automatic fallback. |
| **Local Coding Engine** | **MLX-LM (`omlx`) on M1 Max** | Open Source / $0 | Private, fast iterative code generation and AST fixing with zero per-token cost. |
| **Large-Context Intake** | **Google Gemini 1.5/2.0 Flash (AI Studio)** | Free Tier (15 RPM / 1M ctx) | Ingests 100+ page FAR/DFARS solicitations and RFP PDFs without local RAM saturation. |
| **Fast JSON Extraction** | **Groq Cloud API (Llama 3.3 70B)** | Free Tier (30 RPM) | Ultra-fast (<1s) Pydantic JSON handoff envelope generation and intent classification. |
| **Workspace Sandboxing** | **Ephemeral `git worktree` + `sandbox-exec`** | macOS Built-in / $0 | Isolates each sub-agent in a throwaway branch directory, preventing file-write collisions. |
| **Verification & Evals** | **DSPy + GEPA (Genetic-Pareto Optimizer)** | Open Source / $0 | Continuously optimizes system prompts and few-shot examples from historical failure traces. |
| **Telemetry & Evals** | **Langfuse (Self-Hosted Docker)** | Open Source / Free Cloud | Provides deep trace visibility, token tracking, and evaluation scoring across all harnesses. |
| **Durable Database Backup** | **Litestream + Cloudflare R2** | Free Tier (<10GB storage) | Real-time continuous streaming replication of SQLite task databases to cloud storage with zero egress fees. |

---

## 5. Canonical Directory & Reference Map

To prevent future sessions from re-researching settled ground, all previous repositories and reports are mapped:

1. **`agent-platform` (This Repository - Canonical Authority):**
   - `docs/START-HERE.md`: Cold-start handoff contract.
   - `docs/MASTER-PLAN.md`: Delivery sequence and scorecard.
   - `docs/CONTROLLER.md`: Deterministic Gate C controller contract and principal separation.
   - `docs/OPERATING-MODEL.md`: Effect policy (`DENY`, `AUTO_READ`, `AUTO_WRITE`, `APPROVAL_DESTRUCTIVE`).
   - `docs/chronicle/`: Exhaustive repository lineage, timeline, and research catalog.
   - `docs/MASTER-NORTHSTAR-AND-INTENT.md`: This comprehensive synthesis.

2. **`govcon-factory` (Production Business Deliverables):**
   - `sop/PLAN-V5.md`: End-to-end RFP ingestion, compliance matrix, and proposal generation workflows.
   - `factory/`: Pipelines for SAM.gov notices, Section L/M extraction, and DOCX/PDF rendering.

3. **`agent-mesh` (Legacy Research & Portable Brain - Read-Only):**
   - `.agent/`: Harness-neutral personas (`prime`, `forge`, `scout`, `sentinel`, `operator`), prompts, and protocols.
   - `research/INDEX.md`: 12 peer-reviewed digests covering memory, inference, caching, and harnesses.

4. **`agent-configs` (Universal Config & Skill Library - Read-Only):**
   - `rules/`, `skills/`, `hooks/`, `roles/`: Tested modular skills and behavioral enforcers.
   - `knowledge/MIKE-INTENT-DEBRIEF-2026-08-28.md`: Complete context debrief across 70+ sessions.

5. **`~/agent-reports` (Historical Execution & Benchmark Archive - Read-Only):**
   - 66 dated experiment folders containing Apple Silicon benchmark data, runbooks, and inventory reports.
