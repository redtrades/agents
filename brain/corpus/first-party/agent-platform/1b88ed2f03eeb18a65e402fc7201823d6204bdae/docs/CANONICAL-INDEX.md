# Canonical Reference — Index & Modular Navigation

Companion to [`CANONICAL-REFERENCE.md`](CANONICAL-REFERENCE.md). This file is the table of contents / quick-jump map. Read CANONICAL-REFERENCE.md §1 (Navigation root) for the why.

## 0. How to use this index

- Pick the role or phase in column 1.
- Jump to the file/module in column 2 (all in `agent-platform/` unless marked otherwise).
- Then cross-reference column 3 if your work extends into `agent-mesh`, `agent-configs`, or legacy evidence.
- For history / open-claw heritage, go directly to §4.

## 1. By role (who am I in this architecture?)

| Role | Primary docs / modules | Cross-repo |
|---|---|---|
| Cold-start agent (new session) | `docs/START-HERE.md` (cold resume procedure) → this index → `AGENTS.md` | `agent-mesh/HANDOFF.md` → `WORKLOG.md` last 40 lines |
| Dispatcher (capacity / eligibility) | `docs/DISPATCH-LOOP.md` + `tools/controller/dispatcher.mjs` + `dispatch_eligibility.mjs` + `capacity_policy.mjs` | `.agent/prompts/council-review.md` for the analogous role (non-monotonic) |
| Implementer / builder (bounded worker) | `docs/CONTROLLER.md` §Principals (Worker row) + `docs/COMMIT-IDENTITY.md` + `tools/identity/configure_git_identity.py` | `.agent/agents/forge.md` (or operator.md) for persona body |
| Reviewer / verifier (read-only) | `docs/CONTROLLER.md` §Principals (Reviewer row) + `docs/OPERATING-MODEL.md` | `.agent/protocols/` (generator ≠ judge rule) |
| Promoter (expected-head merge) | `docs/CONTROLLER.md` §Principals (Promoter row) + `docs/OPERATING-MODEL.md` §Principal separation | n/a — software principal, not LLM role |
| Projector (derives issue/Project state from receipts) | `docs/CONTROLLER.md` §Principals (Projector row) + `tools/controller/terminal_projection_parity.mjs` | n/a |
| Architect / owner of effects | `docs/OPERATING-MODEL.md` (approval schema) + `docs/MASTER-PLAN.md` §North star | n/a |
| Memory / knowledge maintainer | `.agent/memory/ARCHITECTURE.md` + `agent-mesh/research/INDEX.md` | `vault/` Obsidian taxonomy + auto-sort tools |
| Model / harness evaluator | `evals/` (YAML golden cases) + `agent-mesh/HANDOFF.md` | `agent-mesh/hermes/` model routing policy |
| Researcher / SOTA intake | `agent-mesh/research/` (12 digests) + `agent-mesh/.agent/agents/scout.md` persona | `pipelines/intake/` normalizer |

## 2. By phase of the delivery loop (start with the one you are in)

| Phase | Canonical doc | Module / evidence |
|---|---|---|
| Intake (issue + subissues) | `docs/START-HERE.md` §What we are building | Issue #1, GitHub Project 12 (projection only) |
| Admission (dependency-clear, input-complete) | `docs/CONTROLLER.md` §Required input + §Owned state #1 | `tools/controller/github_task_admission.mjs` |
| Atomic claim (CAS + lease + generation) | `docs/CONTROLLER.md` §Principals + §Receipts | `tools/controller/github_contents_authority.mjs` (640 lines) |
| Isolated workspace (exact revision) | `docs/CONTROLLER.md` §Owned state #3 | `run_gate_c.mjs`; PR #110 worktree record |
| Dispatch (capacity / eligibility) | `docs/DISPATCH-LOOP.md` | `tools/controller/dispatcher.mjs`; `four_worker_dispatch.test.mjs` |
| Bounded role phase | `docs/CONTROLLER.md` §Owned state #4 + `.agent/agents/*.md` | persona files + skill bodies |
| Checkpoint / resume | `docs/CONTROLLER.md` §Owned state #5 | `tools/controller/work_item_contract.mjs` |
| Candidate binding (exact inputs) | `docs/COMMIT-IDENTITY.md` + `docs/CONTROLLER.md` §Owned state #6 | `tools/identity/*` |
| Deterministic gates (CI) | `docs/CI-GATES.md` | `tools/ci/run_gates.py`; runs 33281620826 / 33281657677 |
| Independent review (read-only) | `docs/CONTROLLER.md` §Owned state #8 + §Principals (Reviewer row) | Reviewer App; review `5059477980` |
| Effect classification | `docs/OPERATING-MODEL.md` (4 outcomes) | n/a (policy layer) |
| Expected-head promotion | `docs/CONTROLLER.md` §Owned state #10 + §Principals (Promoter row) | Promoter App; merge `19246a5...` |
| Projection (issue + Project) | `docs/CONTROLLER.md` §Owned state #11 | Projector PAT (separate from 3 Apps) |
| Teardown / transfer | `docs/CONTROLLER.md` §Owned state #12 | Receipt `gate-c-receipt-33281620826-1` |

## 3. By design category (the "broken out" layer)

| Category | Spec / source | Key principle |
|---|---|---|
| **3.1 Lifecycle & Control** | CANONICAL-REFERENCE.md §3.1 + `docs/CONTROLLER.md` | Deterministic software, not LLM; principal separation |
| **3.2 Identity & Range** | CANONICAL-REFERENCE.md §3.2 + `docs/COMMIT-IDENTITY.md` + `tools/identity/*` | Attribution ≠ signature; range requires trusted outer receipt |
| **3.3 Effect Policy** | CANONICAL-REFERENCE.md §3.3 + `docs/OPERATING-MODEL.md` | 4 outcomes; work level = ceremony only |
| **3.4 Memory / Skill / Protocol / Persona** | CANONICAL-REFERENCE.md §3.4 + `.agent/AGENTS.md` | Portable brain; adopt-per-harness with behavioral proof |
| **3.5 Pipelines & Command Center** | CANONICAL-REFERENCE.md §3.5 + `agent-mesh/pipelines/` + `command-center/` | Reuse over build; no parallel infra |
| **3.6 Failure Anti-patterns** | `docs/DELIVERY-FAILURE-LEDGER.md` (DFL-001..020 / AP-01..027) | Sole canonical register; PATTERN-CANDIDATE envelope |
| **3.7 History / Provenance** | CANONICAL-REFERENCE.md §4 + `agent-mesh/DECISIONS.md` (D-001..D-035) | Append-only; never rewrite; supersede explicitly |

## 4. By history / repository (the open-claw → agent-mesh → agent-platform path)

| Era | Repo | Reference (in this audit) |
|---|---|---|
| Original (retired) | `redtrades/openclaw*` (v1 / v2 / v3 / backup / config) | `agent-mesh/DECISIONS.md` D-001..D-005; sanitized archive in `agent-mesh/archive/` |
| Consolidation 1 | `redtrades/agent-mesh` (overnight 2026-08-26) | `agent-mesh/README.md`; `HANDOFF.md`; `WORKLOG.md`; `research/INDEX.md` (12 digests) |
| Library extraction | `redtrades/agent-configs` (2026-08-24) | `agent-configs/README.md`; `rules/`, `skills/`, `hooks/`, `prompts/`, `roles/` |
| Canonical authority | `redtrades/agent-platform` (live Gate C proof) | `agent-platform/docs/START-HERE.md`; `MASTER-PLAN.md`; `CONTROLLER.md`; issue #103/PR #110; `19246a5...` |
| Migration evidence (read-only) | `govcon-factory`, `agent-workspace`, `agent-tools`, `agent-reports` | Listed in MASTER-PLAN §Repo/storage map; not authoritative |
| Runtime (outside repos) | `.buzz`, `.hermes`, `.codex`, provider profiles, model stores, caches, DBs | MASTER-PLAN §Repo/storage map; opaque locators only |

## 5. By evidence / proof (what currently passes vs what is open)

| Capability (from MASTER-PLAN §Factory acceptance scorecard) | Current proof | Open work |
|---|---|---|
| Autonomous throughput (19/20 then 95% over 100) | Bounded Gate C fixture only (#103 / PR #110) | Full drain; #9; #27 |
| Atomic dispatch | `four_worker_dispatch.test.mjs` + Gate C claim (DFL-010) | Clean-host reconstruction |
| Queue draining | DFL-019 partial (stale labels #91/#93/#103) | #117 Projector transition + postcondition receipt |
| Continuity | Bounded checkpoint receipts | Interruption / quota exhaustion / handoff across clean host |
| Exact verification | `validate_commit_range.py` + `tools/ci/run_gates.py` | Independent cryptographic CI principal (CI-GATES.md) |
| Independent challenge | Reviewer App + review `5059477980` | Multi-model reviewer policy |
| Provider neutrality | 1 harness, 1 model | At least 2 harnesses + 2 providers |
| Controlled improvement | Eval harness; D-008 | Fixed baseline + held-out gates + regression |
| Proactivity | D-006 bots; morning brief pipeline | Drift / cost / regression automated detection |
| Economy | Zero-cost baseline (D-033, MASTER-PLAN §Economical baseline) | Cost / quota / retry instrumentation |
| Security & control | OPERATING-MODEL 4 outcomes; non-delivery domain `agents.invalid` | `APPROVAL_DESTRUCTIVE` audit trail enrichment |
| Estate clarity | MASTER-PLAN §Repo/storage map; this file | Drop-ship discipline at the repo level |
| Product proof | `govcon-factory` separate | One real product-factory slice through the platform |

## 6. File-tree navigation (literal)

```
agent-platform/
├── AGENTS.md                                  <- repo working agreement (L0/L1/L2; fail-closed; review separation)
├── docs/
│   ├── START-HERE.md                          <- cold-start handoff
│   ├── MASTER-PLAN.md                         <- north star; scorecard; sequence 0..4
│   ├── ARCHITECTURE.md                        <- boundary; state progression; GitHub Free limitations
│   ├── OPERATING-MODEL.md                     <- 4 outcomes; approval schema
│   ├── CONTROLLER.md                          <- controller contract; principals; receipts; Gate C proof
│   ├── DISPATCH-LOOP.md                       <- dispatch half; capacity; dry-run guard
│   ├── GOAL.md                                <- concise outcome
│   ├── COMMIT-IDENTITY.md                     <- attribution; range gate
│   ├── CI-GATES.md                            <- deterministic evidence boundary
│   ├── DELIVERY-FAILURE-LEDGER.md             <- DFL-001..020; AP-01..027; PATTERN-CANDIDATE envelope
│   ├── CANONICAL-REFERENCE.md                 <- this consolidation (NEW; 2026-08-30)
│   └── CANONICAL-INDEX.md                     <- this file (NEW; 2026-08-30)
├── tools/
│   ├── controller/                            <- Gate C, dispatcher, parity, claims
│   ├── ci/                                    <- deterministic gates
│   └── identity/                              <- attribution + range validator
├── tests/                                     <- evidence fixtures
└── ... (other repo content)

agent-mesh/
├── AGENTS.md                                  <- repo working agreement
├── README.md                                  <- one-brain-many-harnesses map
├── HANDOFF.md                                 <- current truth; OMLX vs exact Flash-Next
├── WORKLOG.md                                 <- append-only log
├── DECISIONS.md                               <- D-001..D-035 (OpenClaw archive; model; concurrency)
├── research/INDEX.md                          <- 12 cited digests
├── .agent/                                    <- portable cross-harness layer
├── hermes/                                    <- bot profiles; SOUL.md; cron; model-routing
├── pipelines/                                 <- runnable stdlib-only
├── evals/                                     <- YAML golden cases + stdlib runner
├── command-center/                            <- static v1
├── vault/                                     <- Obsidian taxonomy
└── ... (other repo content)

agent-configs/
├── README.md
├── rules/                                     <- enforced behavioral rules
├── skills/                                    <- SKILL.md (adopt after behavioral proof)
├── hooks/                                     <- copied to ~/.claude/hooks/
├── prompts/                                   <- reusable command/contract templates
└── roles/                                     <- persona definitions (independent of runtime)
```

## 7. Quick jumps (the 12 most-clicked references in this audit)

1. `agent-platform/docs/START-HERE.md`
2. `agent-platform/docs/MASTER-PLAN.md`
3. `agent-platform/docs/CONTROLLER.md`
4. `agent-platform/docs/OPERATING-MODEL.md`
5. `agent-platform/docs/DELIVERY-FAILURE-LEDGER.md`
6. `agent-platform/docs/COMMIT-IDENTITY.md`
7. `agent-platform/docs/CI-GATES.md`
8. `agent-platform/docs/DISPATCH-LOOP.md`
9. `agent-platform/docs/ARCHITECTURE.md`
10. `agent-mesh/HANDOFF.md`
11. `agent-mesh/DECISIONS.md`
12. `agent-mesh/research/INDEX.md`

All 12 are also referenced from CANONICAL-REFERENCE.md §1 with task→doc mapping.

---

*Companion file to CANONICAL-REFERENCE.md. Generated 2026-08-30 by audit consolidation over `agent-platform`, `agent-mesh`, `agent-configs`, and referenced OpenClaw archival evidence. No changes made to governing docs.*
