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
16. Historic estate triage: selectively distill candidate tools/skills, pack unneeded `agent-*` to `~/archive/`, and verify swarm SDLC. [COMPLETED]
17. Brain knowledge archive hygiene & 8-digit date-prefix versioning: moved/renamed 83 files across numbered folders and reports in `/Users/man/Brain`; authored Canonical Definitive Estate Plan (`docs/plans/20260905-canonical-definitive-estate-plan.md`). [COMPLETED]
18. Historical estate excavation from May OpenClaw to now: salvaged 50 root receipts and 91 Claude scratchpad files from `/private/tmp/` into `~/agent-reports/tmp-historical-salvage-2026-09-05/`; promoted 9 platform rules to `Brain/100-governance-safety-and-evidence/` and 3 deep research docs to `agents/docs/research/`. [COMPLETED]
19. Brain consolidation & zero dangling documents: consolidated `/Users/man/Brain` directly into `/Users/man/agents/brain/`, created backward-compatible symlinks (`/Users/man/Brain` and `/Users/man/agent-knowledge-archive`), organized 5 loose market reports and 2 loose audits/tasks into dated brain folders, archived all remaining backups into `~/archive/`. [COMPLETED]
20. Implement GitHub Jules App cloud task dispatch and validation workflow (`tools/jules_dispatch.py`, `.github/workflows/jules-dispatch.yml`, `tools/tests/test_jules_dispatch.py`). Closed Issue #5. [COMPLETED]
21. Multi-Harness Canary Verification runner and smoke suite implemented (`tools/canary_runner.py`, `tools/tests/test_canary_runner.py`, `tools/tests/test_cli_smoke.py`, `make canary`). Verified across all 5 installed CLIs. Closed Issue #7. [COMPLETED]

## Active Phase
Phase 12: Historic Estate Extraction, Cold Archiving & Swarm SDLC Hardening

## Evidence & Verification
- `Jules Cloud Task Dispatch (Issue #5 Closed)`: Implemented issue dispatch parser and validator in `tools/jules_dispatch.py` and GitHub Actions workflow `.github/workflows/jules-dispatch.yml` triggered on labels (`jules`, `jules:cloud`) and comments. Added 12 deterministic unit tests in `tools/tests/test_jules_dispatch.py`. Verified `make jules-validate ISSUE=5` outputs valid structured dispatch packet. All 625 pytest tests passing, `make lint` clean, and `make gbrain-check` verified (286 tokens). Closed Issue #5 on GitHub and updated Project 13 to Done.
- `Evals & Safety Hooks Distillation (Issue #2 Closed)`: Extracted root write-blocking hook to `tools/hooks/block-home-root-writes.sh` and wired `make install-hooks` for pre-commit mechanical enforcement. Extracted Apple Silicon M1 Max roofline benchmark to `tools/bench/m1_roofline.py` with unit tests (`tools/tests/test_bench_roofline.py`) and `make bench` recipe. All 589 tests passing cleanly. Closed Issue #2 on GitHub `redtrades/agents` and updated Project 13 to Done.
- `Legacy Estate Cold Archiving (Issue #3 Closed)`: Relocated all 6 legacy repositories (`agent-mesh`, `agent-configs`, `agent-platform`, `agent-workspace`, `agent-sdlc`, `agent-tools`) into `/Users/man/archive/` without redundant backup bloat. Authored canonical archive inventory in `/Users/man/archive/README.md` with standard YAML frontmatter. Verified `/Users/man/agents` is the sole active repo in `~`. Closed Issue #3 on GitHub `redtrades/agents` and updated Project 13 to Done.
- `Brain Consolidation & Zero Dangling Documents`: Consolidated `/Users/man/Brain` directly into `/Users/man/agents/brain/` (tracked natively under `redtrades/agents`), backed up previous git history to `~/archive/Brain-git-history-20260905.tar.gz`, created symlinks `/Users/man/Brain -> /Users/man/agents/brain` and `/Users/man/agent-knowledge-archive -> /Users/man/agents/brain`. Swept all loose files from `~`: moved 5 market/competitive reports into `brain/120-market-and-open-source-research/` with 8-digit date prefixes, moved 2 platform audits/tasks into `brain/110-failures-postmortems-and-lessons/`, and moved 4 backup archives into `~/archive/`. All 4 quality gates pass cleanly.
- `Historical Estate Excavation & Scratchpad Salvage`: Salvaged 50 root session receipts and 91 Claude scratchpad files from `/private/tmp` into `~/agent-reports/tmp-historical-salvage-2026-09-05/` preventing reboot data loss; promoted 9 extracted platform rules into `Brain/100-governance-safety-and-evidence/`, second-brain architecture to `Brain/70-knowledge-context-and-memory/`, issue 106/117 handovers to `Brain/110-failures-postmortems-and-lessons/`, and 3 deep research docs into `agents/docs/research/`.
- `Brain Knowledge Archive Hygiene`: Migrated 83 files across `/Users/man/Brain` to enforce 8-digit date prefixes (`YYYYMMDD-<name>.md`), versioned domain syntheses (`20260831-current-historical-synthesis.md`), updated 36 internal markdown link references, and committed cleanly to git (`2f5bc9b`).
- `Canonical Definitive Estate Plan Authored`: Authored `docs/plans/20260905-canonical-definitive-estate-plan.md` in `agents` and mirrored in `Brain/10-intent-and-north-star/`, consolidating Decisions 1-58, estate decisions DEC-01 to DEC-23, and Phase 1 contradiction resolutions D1-D6.
- `Decision Ratification`: All key governance decisions ratified with Mike (`DEC-18` sovereign split, `DEC-19` estate namespace rejected, `DEC-20` advisory balance precedence, `DEC-14` adaptive hybrid execution, `DEC-21` cost-optimized compute & swarm routing, `DEC-22` streamlined AGENTS.md constitution, `DEC-23` unified estate dual mission).
- `Worktree Lifecycle Operational (Issue #1 Closed)`: Implemented `tools/worktree_manager.py` and `Makefile` recipes (`make worktree-spawn`, `make worktree-clean`, `make worktree-list`). Enforces concurrency limit (<=2) and zero-loss backup branch snapshots (`backup/worktrees/<task-id>`). Unit tested in `tools/tests/test_worktree_manager.py` (582 passed).
- `GitHub Project 13 Created`: Project 13 ("Agents Sovereign Engine") created and synced with issues #1-#5.
- `Mandatory Research Invariant`: Codified directly into `AGENTS.md` (52 lines, cap <=150) as a Non-Negotiable Hard Gate requiring automatic internal research, SOTA GitHub benchmarking, and counter-points (`CP1..CPN`) before engineering work.
- `SOTA Swarm Architecture Authored`: `docs/plans/20260905-sota-swarm-sdlc-and-extraction-architecture.md` documents research protocol, Git worktree mechanics, Jules cloud offloading, cross-model review, and archive distillation pipeline.
- `Skills Consolidation`: Distilled 104 raw skills into 6 first-class native plugins (41 curated skills). Total skills: 225 across 100 plugins.
- `Skills MOC Integrity`: All skills verified <=8 KB. Automated MOC generator (`tools/generate_catalog.py`) built `docs/skills-moc.md`.
- `Zero Em Dashes`: Full codebase and markdown docs verified 100% clean of em/en dashes.
- `Quality Gates`: `make validate STRICT=1` (OK across 5 harnesses), `make garden` (0 errors), `npm test` (16 passed), `make test` (625 passed).
- `GBrain PGLite WASM MCP Memory (Issue #4 Closed)`: Wired Garry Tan GBrain PGLite memory (`~/.gbrain/brain.pglite`) into `redtrades/agents` via lean MCP proxy (`tools/gbrain_mcp.py`). Indexed 373 brain markdown files (2,162 chunks), verified 64.6ms warm query latency, capped token overhead at 286 tokens (well below 800-token limit), added 5 unit tests (`tools/tests/test_gbrain_mcp.py`), and configured multi-harness entries across `.mcp.json`, `~/.claude/settings.json`, `~/.claude.json`, and `~/.codex/config.toml`. Closed Issue #4 on GitHub and updated Project 13 to Done.
- `GBrain Rules & Skills Codified`: Added Mandatory GBrain Knowledge Grounding invariant to `AGENTS.md` (Section 1). Created `rules/memory.md` (`v1.0.0`) specifying when and how to query/persist memory. Created native `gbrain-memory` skill in `plugins/context-management/skills/gbrain-memory/SKILL.md`. Integrated GBrain checks into `research` and `investigate-first` skills. Synchronized all 5 harnesses via `make generate-all` and regenerated `docs/skills-moc.md` (226 skills). All quality gates verified.
- `Multi-Harness Canary Suite (Issue #7 Closed)`: Built `tools/canary_runner.py` probing all 5 installed harness CLIs on PATH (`claude`, `codex`, `agy`, `opencode`, `hermes`). Added `TestHermesSmoke` in `tools/tests/test_cli_smoke.py` and unit tests in `tools/tests/test_canary_runner.py`. Added `make canary` recipe. All 5 CLIs pass in <600ms total. 640 unit tests passing cleanly. Closed Issue #7 on GitHub and marked Done in Project 13.
- `Upstream Detachment`: Active git remote removed, read-only innovation check available via `make check-upstream`.

## Parked Backlog (On The Board / Tracked on GitHub redtrades/agents)
- **Issue #1** (`sdlc:done`): Implement native worktree lifecycle recipes and session backup automation. [CLOSED]
- **Issue #2** (`sdlc:done`): Distill candidate evaluation harnesses from `agent-mesh` and hooks from `agent-configs`. [CLOSED]
- **Issue #3** (`sdlc:done`): Package unneeded legacy `agent-*` repositories to `~/archive/` and prune filesystem. [CLOSED]
- **Issue #4** (`sdlc:done`): Wire Garry Tan GBrain PGLite WASM MCP server for cross-session recall. [CLOSED]
- **Issue #5** (`sdlc:done`): Wire GitHub Jules App and cloud task dispatch workflow. [CLOSED]
- **Issue #7** (`sdlc:done`): Multi-harness canary verification runner and smoke suite. [CLOSED]
- **Hermes Integration** (`sdlc:done`): Configure Hermes progressive disclosure and GBrain MCP in `~/.hermes/config.yaml`. [COMPLETED]
- **Cross-Model Review Engine** (`sdlc:done`): Build autonomous peer review engine in `tools/cross_model_review.py` enforcing author/reviewer separation and diff slop audits. [COMPLETED]
- **Parked (P0)**: GovCon Proposal Factory pipeline (Parked until swarm SDLC is hardened and historic archives extracted).

## Next Immediate Action
Execute 5-part GBrain grounding and context compilation plan:
1. Codify GBrain grounding directives into key planning, research, and debugging skills.
2. Build deterministic context compilation pipeline (make context-compile, make context-check).
3. Connect autonomous cross-model review engine to GBrain memory logging.
4. Add deterministic governance test suite (test_gbrain_governance.py).
5. Ratify ADR in DECISION_LOG.md and regenerate multi-harness catalog.

