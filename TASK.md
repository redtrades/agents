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
11. One-at-a-time decision ratification protocol active with Mike. [COMPLETED]
12. Consolidate native skills & research from agent-configs into agents (Phases 1-4). [COMPLETED]

## Active Phase
Phase 10: Estate Handoff & Session Seal (Cold-Start Ready for New Session)

## Evidence & Verification
- `Decision Ratification`: All key governance decisions ratified with Mike (`DEC-18` sovereign split, `DEC-19` estate namespace rejected, `DEC-20` advisory balance precedence, `DEC-14` adaptive hybrid execution, `DEC-21` cost-optimized compute & swarm routing).
- `Skills Consolidation`: Distilled 104 raw skills into 6 first-class native plugins (41 curated skills). Total skills: 225 across 100 plugins.
- `Skills MOC Integrity`: All skills verified <=8 KB. Automated MOC generator (`tools/generate_catalog.py`) built `docs/skills-moc.md`.
- `Zero Em Dashes`: Full codebase and markdown docs verified 100% clean of em/en dashes.
- `Quality Gates`: `make validate STRICT=1` (OK across 5 harnesses), `make garden` (0 errors), `npm test` (16 passed), `make test` (580 passed).
- `AGENTS.md & rules/`: Hardened with ratified policies (112 lines, commands first, MOC pointers, zero em dashes).
- `Upstream Detachment`: Active git remote removed; read-only innovation check available via `make check-upstream`.

## Parked Backlog (On The Board / Side Inquiries)
- P1: Review candidate tool clusters (`agent-mesh/evals`, `agent-configs/hooks`) following SDLC gates.
- P2: Configure Hermes progressive disclosure in `~/.hermes/config.yaml`.
- P3: Set up Jules GitHub App issue automation on `redtrades/agents`.
- P4: Wire Garry Tan GBrain MCP memory server.
- P5: Package historic `agent-*` folders to `~/archive/` and clean up `~` and iCloud Drive.

## Next Immediate Action
Clean handoff to Mike; all foundations solidified, verified, and cold-start resume ready for new session.
