# Task Tracking: Estate Consolidation, Governance Distillation & Promotion Architecture

## Task Identity
- **Task ID:** TASK-20260905-ESTATE-DISTILLATION
- **Owner:** Antigravity (Pair Programming with Mike)
- **Workspace:** `/Users/man/agents` (fork `redtrades/agents`)
- **Status:** IN_PROGRESS

## Goal
Finalize `/Users/man/agents` as the sovereign, unified multi-agent operating engine. Selectively distill and extract high-leverage assets from historic `agent-*` archives, move unneeded legacy repos into cold archive (`~/archive/`), and establish a fully working autonomous SDLC for the swarm. (GovCon Proposal Factory is parked until swarm SDLC and archive extraction are fully complete).

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
13. Finalize `AGENTS.md` with inlined communication grammar, SDLC worktree/queue invariants, and dual-mission intent while maintaining <=150 lines. [COMPLETED]
14. Codify Mandatory A Priori Research & Counter-Points invariant into `AGENTS.md` and author canonical SOTA Swarm SDLC and Extraction Architecture plan (`docs/plans/20260905-sota-swarm-sdlc-and-extraction-architecture.md`). [COMPLETED]
15. Implement native worktree lifecycle recipes and zero-loss backup automation (`tools/worktree_manager.py`, `Makefile`, `tools/tests/test_worktree_manager.py`). Closed Issue #1. [COMPLETED]
16. Historic estate triage: selectively distill candidate tools/skills, pack unneeded `agent-*` to `~/archive/`, and verify swarm SDLC. [IN_PROGRESS]

## Active Phase
Phase 12: Historic Estate Extraction, Cold Archiving & Swarm SDLC Hardening

## Evidence & Verification
- `Decision Ratification`: All key governance decisions ratified with Mike (`DEC-18` sovereign split, `DEC-19` estate namespace rejected, `DEC-20` advisory balance precedence, `DEC-14` adaptive hybrid execution, `DEC-21` cost-optimized compute & swarm routing, `DEC-22` streamlined AGENTS.md constitution, `DEC-23` unified estate dual mission).
- `Worktree Lifecycle Operational (Issue #1 Closed)`: Implemented `tools/worktree_manager.py` and `Makefile` recipes (`make worktree-spawn`, `make worktree-clean`, `make worktree-list`). Enforces concurrency limit (<=2) and zero-loss backup branch snapshots (`backup/worktrees/<task-id>`). Unit tested in `tools/tests/test_worktree_manager.py` (582 passed).
- `GitHub Project 13 Created`: Project 13 ("Agents Sovereign Engine") created and synced with issues #1-#4.
- `Mandatory Research Invariant`: Codified directly into `AGENTS.md` (52 lines, cap <=150) as a Non-Negotiable Hard Gate requiring automatic internal research, SOTA GitHub benchmarking, and counter-points (`CP1..CPN`) before engineering work.
- `SOTA Swarm Architecture Authored`: `docs/plans/20260905-sota-swarm-sdlc-and-extraction-architecture.md` documents research protocol, Git worktree mechanics, Jules cloud offloading, cross-model review, and archive distillation pipeline.
- `Skills Consolidation`: Distilled 104 raw skills into 6 first-class native plugins (41 curated skills). Total skills: 225 across 100 plugins.
- `Skills MOC Integrity`: All skills verified <=8 KB. Automated MOC generator (`tools/generate_catalog.py`) built `docs/skills-moc.md`.
- `Zero Em Dashes`: Full codebase and markdown docs verified 100% clean of em/en dashes.
- `Quality Gates`: `make validate STRICT=1` (OK across 5 harnesses), `make garden` (0 errors), `npm test` (16 passed), `make test` (582 passed).
- `Upstream Detachment`: Active git remote removed; read-only innovation check available via `make check-upstream`.

## Parked Backlog (On The Board / Tracked on GitHub redtrades/agents)
- **Issue #1** (`sdlc:done`): Implement native worktree lifecycle recipes and session backup automation. [CLOSED]
- **Issue #2** (`sdlc:backlog`): Distill candidate evaluation harnesses from `agent-mesh` and hooks from `agent-configs`.
- **Issue #3** (`sdlc:backlog`): Package unneeded legacy `agent-*` repositories to `~/archive/` and prune filesystem.
- **Issue #4** (`sdlc:backlog`): Wire Garry Tan GBrain PGLite WASM MCP server for cross-session recall.
- **Parked (P0)**: GovCon Proposal Factory pipeline (Parked until swarm SDLC is hardened and historic archives extracted).
- **Parked (P2)**: Configure Hermes progressive disclosure in `~/.hermes/config.yaml`.
- **Parked (P3)**: Set up Jules GitHub App issue automation on `redtrades/agents`.

## Next Immediate Action
Claim Issue #2: Inspect `agent-mesh` evals via triage manifest and distill into `plugins/plugin-eval/` and `tools/tests/`.
