---
name: operational-decision-log
status: active
tier: standard
date: 2026-09-05
---

# Operational Decision Log (Level B Ledger)

Lightweight chronological ledger for operational, tactical, and micro-decisions that do not require a full MADR architectural document.

| Decision ID | Date | Category | Decision Statement | Rationale / Tradeoff | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **DEC-20260905-01** | 2026-09-05 | Governance | Center single source of truth in `/Users/man/agents`. | Eliminates fragmentation across 5 repos. | **ACTIVE** |
| **DEC-20260905-02** | 2026-09-05 | Runtime | Prune custom Python wrappers in `src/adapters/`. | Native CLI harnesses (`claude`, `codex`, `opencode`) run directly. | **ACTIVE** |
| **DEC-20260905-03** | 2026-09-05 | State | Use Git commits as immutable ledger; drop parallel JSONL. | YAGNI; eliminates JSON parsing errors and token bloat. | **ACTIVE** |
| **DEC-20260905-04** | 2026-09-05 | Execution | Complexity-tiered turn budgets (5 to 100 turns). | Gives headroom for `/goal` workflows with 25-turn checkpoints. | **ACTIVE** |
| **DEC-20260905-05** | 2026-09-05 | Tooling | Automated self-healing catalog generator (`tools/generate_catalog.py`). | Prevents manual documentation drift across 184 skills. | **ACTIVE** |
