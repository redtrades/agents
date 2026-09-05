# Council Brief: Improve/Enhance/Optimize Agnostic Agentic Swarm Pipelines & Workflows

**Date:** 2026-08-25  
**Council ID:** 2026-08-25-swarm-optimization  
**Brief Type:** Strategy Attack + Enhancement Proposals  

## Current State Summary

**Repository:** `govcon-factory` (agentic swarm for govcon opportunity packets + industry reports)  
**Pipeline Architecture:** SSSF (Synchronous Stage-Specific Fail-closed)  
- 3 pipelines: `govcon-sources-sought-packet` (9 stages), `govcon-industry-report` (8 stages), `govcon-market-snapshot` (8 stages)  
- 9 gates: schema, inputs_present, provenance, count_recomputation, freshness, single_writer, compliance, format, value  
- SQLite trace, fail-closed on any gate failure  

**Agent Infrastructure:**  
- 252 Hermes skills available (5 agent-config types: rules, hooks, prompts, roles, library — all v2 enhanced)  
- Local MLX (Qwen3.6-35B-A3B-8bit @ :8080) + Frontier (claude -p)  
- Agent-council and lane swarm patterns documented  

**Human Gates (blocking):**  
- TASK-0018: Matcher gold-set ≥80% precision (counsel ruling)  
- TASK-0015: Sending domain + DNS (SPF/DKIM/DMARC)  
- TASK-0013/0014: COI policy, terms/E&O/refund policy  

---

## Your Task

Each persona: Write a research file `research/council/2026-08-25-<role>-<model>.md` with:
1. **Diagnosis** — What's weak, missing, or risky in current pipelines/workflows?
2. **Proposals** — Concrete improvements (code, architecture, process, tooling)
3. **Prioritization** — Rank by impact/effort (P0/P1/P2)
4. **Risks/Dependencies** — What could block or break

---

## Personas & Roles

| Persona | Focus | Model Slot |
|---------|-------|------------|
| **Architect** | Pipeline architecture, data flow, scalability, SSSF framework | |
| **Operator** | Day-to-day running, monitoring, debugging, human-in-loop | |
| **Quality Engineer** | Gate coverage, test strategy, CI/CD, fail-closed guarantees | |
| **Security/Compliance** | Data handling, secrets, audit trail, SOP adherence | |
| **Product/Business** | Throughput, cost, time-to-value, human gates, pricing | |

---

## Constraints

- No new PLAN-V8. Proposals only.
- Cite repo paths (e.g., `factory/gates/registry.py`, `factory/runner.py`).
- Label guesses explicitly.
- No credentials in briefs.
- Write to `research/council/2026-08-25-<role>-<model>.md`