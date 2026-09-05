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
2. SOTA decision and instruction promotion pipeline codified (`docs/decisions/` + promotion lifecycle). [COMPLETED]
3. 25 untracked legacy rule files pruned and replaced by 4 distilled living rules with zero dead links. [COMPLETED]
4. Redundant Python wrappers in `src/adapters/` and `tests/adapters/` pruned. [COMPLETED]
5. Tiered hybrid decision tracking implemented (ADR 0001 + `docs/decisions/DECISION_LOG.md`). [COMPLETED]
6. Declarative catalog generation tool implemented (`tools/generate_catalog.py`) and wired to Makefile. [COMPLETED]
7. All repository quality gates pass (`make validate STRICT=1`, `make garden`, `make test`, `npm test`). [COMPLETED]
8. `CONTINUATION.md` maintained after every atomic step. [COMPLETED]

## Active Phase
Phase 7: Horizon 2 Estate Consolidation & Asset Extraction

## Evidence & Verification
- `Origin Sync`: Pushed commits up to `dabb303` to `git@github.com:redtrades/agents.git`.
- `Brain Established`: Renamed `/Users/man/agent-knowledge-archive` to `/Users/man/Brain` cleanly (no symlink).
- `Task Ledger`: Created `docs/tasks/README.md` for completed task lifecycle and GitHub commit binding.
- `Mechanical Triage`: Built and ran `tools/triage_historic_estate.py` (scanned 8,731 files across 5 historic repos with zero LLM tokens).
- `AGENTS.md`: Full operating constitution with L1-L4 Autonomy, Anti-Wholesale Ingestion Law, Disler SSSF principles, and Scope Containment (107 lines, <=150 cap).
- `rules/`: 4 distilled living rule files (`communication.md`, `task-tracking.md`, `hygiene.md`, `verification.md`).
- `docs/decisions/`: ADR 0001 (MADR) + `DECISION_LOG.md` (Level B ledger DEC-01 through DEC-15).
- `Quality Gates`: `make garden` (0 errors), `make validate STRICT=1` (OK), `npm test` (16 passed), `make test` (568 passed).

## Parked Backlog (On The Board / Review Queue)
- P1: Review and selectively harvest candidate tool clusters (`agent-mesh/evals`, `agent-configs/hooks`) following SDLC gates.
- P2: Configure Hermes progressive disclosure in `~/.hermes/config.yaml`.
- P3: Set up Jules GitHub App issue automation on `redtrades/agents`.
- P4: Wire Garry Tan GBrain MCP memory server.

## Next Immediate Action
Execute automated skill metadata backfill across plugins/*/skills/ to ensure spec compliance.







