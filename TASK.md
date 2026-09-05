# Task Tracking: Estate Consolidation, Governance Distillation & Promotion Architecture

## Task Identity
- **Task ID:** TASK-20260905-ESTATE-DISTILLATION
- **Owner:** Antigravity (Pair Programming with Mike)
- **Workspace:** `/Users/man/agents` (fork `redtrades/agents`)
- **Status:** IN_PROGRESS

## Goal
Establish a zero-bloat, unified multi-agent engineering foundation centered on `/Users/man/agents`. Codify Mike's instructions into a living decision and promotion registry (`docs/decisions/` and `rules/`), eliminate custom Python adapter wrappers (`src/adapters/`), distill core operating rules into 4 clean files, and prevent agent amnesia and recursive meta-work loops.

## Acceptance Criteria
1. Full scan of Sep 4 and Sep 5 documentation synthesized into root causes and actionable plan. [COMPLETED]
2. SOTA decision and instruction promotion pipeline codified (`docs/decisions/` + 5-state lifecycle). [COMPLETED]
3. 25 untracked legacy rule files pruned and replaced by 4 distilled living rules with zero dead links. [COMPLETED]
4. Redundant Python wrappers in `src/adapters/` and `tests/adapters/` pruned. [COMPLETED]
5. Tiered hybrid decision tracking implemented (ADR 0001 + `docs/decisions/DECISION_LOG.md`). [COMPLETED]
6. Declarative catalog generation tool implemented (`tools/generate_catalog.py`) and wired to Makefile. [COMPLETED]
7. All repository quality gates pass (`make validate STRICT=1`, `make garden`, `make test`, `npm test`). [COMPLETED]
8. `CONTINUATION.md` maintained after every atomic step. [COMPLETED]
9. SOTA Patterns & Anti-Patterns catalog authored (`docs/research/20260905-sota-patterns-and-anti-patterns.md`). [COMPLETED]
10. All 9 oversize skills refactored into MOC + references/details.md (0 skill warnings in make garden). [COMPLETED]
11. One-at-a-time decision ratification protocol active with Mike. [IN_PROGRESS]
12. Consolidate native skills & research from agent-configs into agents (Phases 1-4). [IN_PROGRESS]

## Active Phase
Phase 8: Native Skills & Research Consolidation (Distillation, MECE Dedup, MOC Generator, Multi-Harness Sync)

## Evidence & Verification
- `Skills MOC Integrity`: Refactored all 9 oversize skills (>8 KB) into `references/details.md`. `make garden` reports 0 `SKILL_OVER_CODEX_CAP` warnings.
- `Quality Gates`: `make validate STRICT=1` (OK across 5 harnesses), `make garden` (0 errors), `npm test` (16 passed), `make test` (568 passed).
- `Decision Rollback`: Re-classified DEC-14 (SSSF), DEC-18 (fork split), DEC-19 (estate namespace), and DEC-20 (conflict policy) as `PROPOSED` pending explicit one-at-a-time ratification.
- `AGENTS.md`: Distilled SOTA operating constitution (111 lines, commands first, MOC pointers, zero em dashes).

## Parked Backlog (On The Board / Side Inquiries)
- P1: Review candidate tool clusters (`agent-mesh/evals`, `agent-configs/hooks`) following SDLC gates.
- P2: Configure Hermes progressive disclosure in `~/.hermes/config.yaml`.
- P3: Set up Jules GitHub App issue automation on `redtrades/agents`.
- P4: Wire Garry Tan GBrain MCP memory server.
- P5: Package historic `agent-*` folders to `~/archive/` and clean up `~` and iCloud Drive.

## Next Immediate Action
Execute Phase 1: Transfer and normalize research docs from agent-configs to docs/research/.
