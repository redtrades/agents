---
name: operational-decision-log
status: active
tier: standard
date: 2026-09-05
---

# Operational Decision Log (Level B Ledger)

Lightweight chronological ledger for operational, tactical, and micro-decisions that do not require a full MADR architectural document.
Every decision is classified under the 5-state lifecycle: `PROPOSED`, `RATIFIED`, `SUPERSEDED`, `STALE`, or `REJECTED`. Only `RATIFIED` decisions explicitly confirmed by Mike govern agent execution. Unconfirmed proposals and historical notes remain `PROPOSED` and carry no governing authority.

| Decision ID | Date | Level | Category | Decision Statement | Rationale / Tradeoff | Status | Successor / Notes |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **DEC-20260905-01** | 2026-09-05 | L4 (Constitution) | Governance | Center single source of truth in `/Users/man/agents`. | Eliminates fragmentation across 5 legacy repos. | **RATIFIED** | Authoritative repo root |
| **DEC-20260905-02** | 2026-09-05 | L2 (Living Rule) | Runtime | Prune custom Python wrappers in `src/adapters/`. | Native CLI harnesses (`claude`, `codex`, `opencode`) run directly. | **RATIFIED** | -2,761 lines pruned |
| **DEC-20260905-03** | 2026-09-05 | L2 (Living Rule) | State | Use Git commits as immutable ledger; drop parallel JSONL. | YAGNI; eliminates JSON parsing errors and token bloat. | **RATIFIED** | `git log -n 5 --oneline` |
| **DEC-20260905-04** | 2026-09-05 | L2 (Living Rule) | Execution | Complexity-tiered turn budgets (5 to 100 turns) as adaptive guidance. | Provides headroom for `/goal` workflows while preventing runaway loops. | **PROPOSED** | Guidance ceiling, not rigid dogma |
| **DEC-20260905-05** | 2026-09-05 | L2 (Living Rule) | Tooling | Automated self-healing catalog generator (`tools/generate_catalog.py`). | Prevents manual documentation drift across 184 skills. | **RATIFIED** | Wired to `make catalog` |
| **DEC-20260905-06** | 2026-09-05 | L4 (Constitution) | Architecture | 3-Tier Map of Content (MOC) progressive disclosure for all skills. | Keeps resident prompt <300 tokens; prevents 27k token context blowout. | **RATIFIED** | Spec compliant |
| **DEC-20260905-07** | 2026-09-05 | L4 (Constitution) | Governance | Hardcode Disler anti-fancy laws in `AGENTS.md`. | Replaced by distilled operational guidance to avoid over-prescription. | **SUPERSEDED** | Superseded by distilled `AGENTS.md` |
| **DEC-20260905-08** | 2026-09-05 | L2 (Living Rule) | Orchestration | Complexity-adaptive hybrid skill intent inference ladder. | T1 skips skills, T2 checks domain triggers, T3/T4 activates MOC. | **PROPOSED** | Under evaluation |
| **DEC-20260905-09** | 2026-09-05 | L4 (Constitution) | Governance | Automatic research and pushback invariant (Never wait to be asked). | Automatically executes research and tags CPs on user proposals. | **RATIFIED** | Codified in `AGENTS.md` |
| **DEC-20260905-10** | 2026-09-05 | L3 (Estate Brain) | Knowledge | Adopt Karpathy Wiki-LLM + Garry Tan GBrain MCP memory pattern. | Markdown MOC on disk + PGLite WASM MCP; preserves prompt cache. | **PROPOSED** | Long-term vision (P4 backlog) |
| **DEC-20260905-11** | 2026-09-05 | L3 (Estate Brain) | Verification | Blind cross-model council review for Tier 3/4 architectural changes. | Eliminates self-judgment bias across heterogeneous model families. | **PROPOSED** | Exploration (P1 backlog) |
| **DEC-20260905-12** | 2026-09-05 | L4 (Constitution) | Autonomy | Codify Risk-Tiered Autonomy Ladder (L1-L4) into `AGENTS.md`. | Replaces rigid thread caps with dynamic risk-based gates. | **RATIFIED** | Codified in `AGENTS.md` |
| **DEC-20260905-13** | 2026-09-05 | L4 (Constitution) | Governance | Codify Anti-Wholesale Ingestion Law into `AGENTS.md`. | Forbids bulk copying of legacy dirs; enforces selective distillation. | **RATIFIED** | Codified in `AGENTS.md` |
| **DEC-20260905-14** | 2026-09-05 | L4 (Constitution) | Architecture | Adaptive Hybrid Execution: Combine Ponytail mechanical recipes and deterministic checks with lean agent prompts, refining variants as swarm final state matures. | Avoids premature lock-in to rigid daemons while preventing worktree sprawl; adapts to estate scale. | **RATIFIED** | Adaptive hybrid ratified by Mike |
| **DEC-20260905-15** | 2026-09-05 | L1 (Task Queue) | SDLC | Park triage asset harvesting to SDLC review queue before execution. | Enforces disciplined review-first lifecycle for historic code. | **RATIFIED** | Parked backlog P1 |
| **DEC-20260905-16** | 2026-09-05 | L2 (Living Rule) | Taxonomy | Establish canonical estate glossary (`docs/GLOSSARY.md`). | Eliminates terminology drift and cognitive confusion across harnesses. | **RATIFIED** | In `docs/GLOSSARY.md` |
| **DEC-20260905-17** | 2026-09-05 | L2 (Living Rule) | Governance | Establish Side-Inquiry & Parked Backlog Protocol in `TASK.md`. | Captures operator side thoughts to backlog without derailing in-flight focus. | **RATIFIED** | In `TASK.md` |
| **DEC-20260905-18** | 2026-09-05 | L4 (Constitution) | Architecture | Clean split: Standalone sovereign repo (`redtrades/agents`) with quarterly read-only check. | Detach upstream git tracking to prevent merge pollution; review upstream innovations quarterly. | **RATIFIED** | Clean split ratified by Mike |
| **DEC-20260905-19** | 2026-09-05 | L3 (Estate Brain) | Architecture | Dedicated estate namespace for proprietary tools (`plugins/estate-*` or other). | Isolate proprietary GovCon & estate assets from generic upstream tools. | **REJECTED** | Mike: 'Our agent repo is ours. There's no estate plugins.' Native plugins live directly under `plugins/`. |
| **DEC-20260905-20** | 2026-09-05 | L4 (Constitution) | Governance | Advisory Balance: Treat historical documents, brain notes, and current chat instructions as co-equal advisory inputs. | Preserves deep context from brain notes and archives while reconciling discrepancies dynamically. | **RATIFIED** | Advisory balance ratified by Mike |
| **DEC-20260905-21** | 2026-09-05 | L4 (Constitution) | Compute & Models | Selective Swarm & Cost-Optimized Routing: Maximize free-tier cloud (Gemini Flash, Groq) and Jules async cloud; reserve frontier subscriptions (Claude Max, Codex CLI) for interactive synthesis; local M16 models for non-time-bound long runs. | Conserves expensive subscription quotas; offloads async runs to cloud; avoids tying up local hardware. | **RATIFIED** | Ratified by Mike (adaptive refinement) |
| **DEC-20260905-22** | 2026-09-05 | L4 (Constitution) | Governance | Streamlined AGENTS.md Constitution: Surface Dual Mission, Non-Negotiable Invariants, and How-to-Work first; prune upstream links, transpilation mechanics, and doc lists. Capped at 51 lines. | Eliminates cold-start distraction; makes communication rules and SDLC invariants inescapable on turn 1. | **RATIFIED** | Ratified by Mike (Commit `110e99b`) |
| **DEC-20260905-23** | 2026-09-05 | L4 (Constitution) | Strategy | Unified Estate Dual Mission: (1) GovCon RFP Proposal Starter Factory ($8k-$10k/mo revenue); (2) Sovereign, vendor-agnostic resilient multi-agent foundation. | Anchors commercial revenue deliverable and engineering swarm in root constitution. | **RATIFIED** | Ratified by Mike |
