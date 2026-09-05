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
10. Unified Intent & North Star ratified in Brain vault (`/Users/man/Brain/10-intent-and-north-star/`). [COMPLETED]

## Active Phase
Phase 7: Horizon 2 Estate Consolidation & Asset Extraction

## Evidence & Verification
- `Origin Sync`: Pushed commits up to `546d8e2` to `git@github.com:redtrades/agents.git`.
- `Brain Established`: Renamed `/Users/man/agent-knowledge-archive` to `/Users/man/Brain` cleanly; committed `20260905-unified-intent-and-north-star.md`.
- `SOTA Catalog`: Authored `docs/research/20260905-sota-patterns-and-anti-patterns.md` synthesizing 13 research reports and benchmarks across 8 operational domains.
- `AGENTS.md`: Full operating constitution with L1-L4 Autonomy, Anti-Wholesale Ingestion Law, and Distilled Operational Guidance (107 lines, <=150 cap, zero em dashes).
- `rules/`: 4 distilled living rule files (`communication.md`, `task-tracking.md`, `hygiene.md`, `verification.md`).
- `docs/GLOSSARY.md`: Authoritative estate glossary and taxonomy.
- `docs/decisions/`: ADR 0001 (MADR) + `DECISION_LOG.md` with 5-state lifecycle (`PROPOSED`, `RATIFIED`, `SUPERSEDED`, `STALE`, `REJECTED`) recording DEC-01 through DEC-19.
- `Quality Gates`: `make garden` (0 errors), `make validate STRICT=1` (OK), `npm test` (16 passed), `make test` (568 passed).

## Parked Backlog (On The Board / Side Inquiries)
- P1: Review and selectively harvest candidate tool clusters (`agent-mesh/evals`, `agent-configs/hooks`) following SDLC gates.
- P2: Configure Hermes progressive disclosure in `~/.hermes/config.yaml`.
- P3: Set up Jules GitHub App issue automation on `redtrades/agents`.
- P4: Wire Garry Tan GBrain MCP memory server.
- P5: Separate proprietary estate skills into dedicated namespaces (`plugins/estate-orchestration/`, `plugins/govcon-deliverables/`).
- P6: Package historic `agent-*` folders to `~/archive/` and clean up `~` and iCloud Drive.

## Next Immediate Action
Execute automated skill metadata backfill across plugins/*/skills/ and split 9 oversize skills into references/details.md to bring make garden warnings to 0.
