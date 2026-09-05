---
name: operational-decision-log
status: active
tier: standard
date: 2026-09-05
---

# Operational Decision Log (Level B Ledger)

Lightweight chronological ledger for operational, tactical, and micro-decisions that do not require a full MADR architectural document.

| Decision ID | Date | Level | Category | Decision Statement | Rationale / Tradeoff | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **DEC-20260905-01** | 2026-09-05 | L4 (Constitution) | Governance | Center single source of truth in `/Users/man/agents`. | Eliminates fragmentation across 5 repos. | **ACTIVE** |
| **DEC-20260905-02** | 2026-09-05 | L2 (Living Rule) | Runtime | Prune custom Python wrappers in `src/adapters/`. | Native CLI harnesses (`claude`, `codex`, `opencode`) run directly. | **ACTIVE** |
| **DEC-20260905-03** | 2026-09-05 | L2 (Living Rule) | State | Use Git commits as immutable ledger; drop parallel JSONL. | YAGNI; eliminates JSON parsing errors and token bloat. | **ACTIVE** |
| **DEC-20260905-04** | 2026-09-05 | L2 (Living Rule) | Execution | Complexity-tiered turn budgets (5 to 100 turns). | Gives headroom for `/goal` workflows with 25-turn checkpoints. | **ACTIVE** |
| **DEC-20260905-05** | 2026-09-05 | L2 (Living Rule) | Tooling | Automated self-healing catalog generator (`tools/generate_catalog.py`). | Prevents manual documentation drift across 184 skills. | **ACTIVE** |
| **DEC-20260905-06** | 2026-09-05 | L4 (Constitution) | Architecture | 3-Tier Map of Content (MOC) progressive disclosure for all skills. | Keeps resident prompt <300 tokens; prevents 27k token context blowout. | **ACTIVE** |
| **DEC-20260905-07** | 2026-09-05 | L4 (Constitution) | Governance | Hardcode Disler anti-fancy laws and CP counter-points in `AGENTS.md`. | Enforces strict scope containment, YAGNI, and exit code 0 proof. | **ACTIVE** |
| **DEC-20260905-08** | 2026-09-05 | L2 (Living Rule) | Orchestration | Complexity-adaptive hybrid skill intent inference ladder. | T1 skips skills, T2 checks domain triggers, T3/T4 activates MOC. | **ACTIVE** |
| **DEC-20260905-09** | 2026-09-05 | L4 (Constitution) | Governance | Automatic research and pushback invariant (Never wait to be asked). | Automatically executes research and tags CPs on user proposals. | **ACTIVE** |
| **DEC-20260905-10** | 2026-09-05 | L3 (Estate Brain) | Knowledge | Adopt Karpathy Wiki-LLM + Garry Tan GBrain MCP memory pattern. | Markdown MOC on disk + PGLite WASM MCP; preserves prompt cache. | **ACTIVE** |
| **DEC-20260905-11** | 2026-09-05 | L3 (Estate Brain) | Verification | Blind cross-model council review for Tier 3/4 architectural changes. | Eliminates self-judgment bias across heterogeneous model families. | **ACTIVE** |
| **DEC-20260905-12** | 2026-09-05 | L4 (Constitution) | Autonomy | Codify Risk-Tiered Autonomy Ladder (L1-L4) into `AGENTS.md`. | Replaces rigid thread caps with dynamic risk-based gates. | **ACTIVE** |
| **DEC-20260905-13** | 2026-09-05 | L4 (Constitution) | Governance | Codify Anti-Wholesale Ingestion Law into `AGENTS.md`. | Forbids bulk copying of legacy dirs; enforces selective distillation. | **ACTIVE** |
| **DEC-20260905-14** | 2026-09-05 | L4 (Constitution) | Architecture | Adopt Disler SSSF principles: Thin agents, fat Makefile recipes. | Keeps agents focused on judgment; mechanical logic stays in recipes. | **ACTIVE** |
| **DEC-20260905-15** | 2026-09-05 | L1 (Task Queue) | SDLC | Park triage asset harvesting to SDLC review queue before execution. | Enforces disciplined review-first lifecycle for historic code. | **ACTIVE** |
| **DEC-20260905-16** | 2026-09-05 | L2 (Living Rule) | Taxonomy | Establish canonical estate glossary (`docs/GLOSSARY.md`). | Eliminates terminology drift and cognitive confusion across harnesses. | **ACTIVE** |
| **DEC-20260905-17** | 2026-09-05 | L2 (Living Rule) | Governance | Establish Side-Inquiry & Parked Backlog Protocol. | Captures operator side thoughts to backlog without derailing in-flight focus. | **ACTIVE** |




