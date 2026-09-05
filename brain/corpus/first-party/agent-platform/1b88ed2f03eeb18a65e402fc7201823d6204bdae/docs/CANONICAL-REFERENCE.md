# Canonical Reference — Agent Platform Architecture & Design

Status: AUDITED-CONSOLIDATED (2026-08-30). Author: audit pass over `agent-platform` (main `codex/worker-c-issue-9` @ 19246a5... range), `agent-mesh` (branch `preserve/uncommitted-2026-08-29`, DECISIONS D-001..D-035, research/INDEX.md 12 files), `agent-configs`, `agent-workspace`, `agent-tools`, `agent-reports`, legacy `openclaw*` archival evidence (D-001/D-002 sanitized in `agent-mesh` archive/), and GitHub evidence #103/PR #110 / #81/PR #82 / #69/PR #70.
Authority: `agent-platform/docs/START-HERE.md`, `AGENTS.md`, `MASTER-PLAN.md` (scorecard 13 capabilities + 5 sequence phases 0..4 + economy baseline). This file is a **navigation and consolidation layer**, not a replacement of those governing docs. If it conflicts, STOP and correct through issue #1 (START-HERE.md §1).
Certainty band: 95% on core lifecycle (Gate C verified by receipt `gate-c-receipt-33281620826-1` sha256 `sha256:e1fdb8d74df39bcbb0bb49aae970a0fd554dd1b69cb55fb618d94d1950288472` at `redtrades/agent-platform` main `19246a5...`); 85% on clean-host reconstruction / multi-harness neutrality (open acceptance work per MASTER-PLAN §Critical Path 2..5); 90% on OpenClaw ancestry (D-001/D-002 archive shape confirmed, original `redtrades/openclaw*` sanitized — exact original repo URLs not reconstructed locally beyond archive/ reference).

---

## 1. Navigation root (one entry, many agents)

Every agent/session should read in this order (not all; pick the category that matches the current task, then descend):

| If you want… | Start here (this repo) | Cross-reference (agent-mesh / other) |
|---|---|---|
| The one-page delivery loop | `docs/START-HERE.md` (§What we are building) | `agent-mesh/HANDOFF.md`, `WORKLOG.md` last 40 lines |
| The authority model / principals | `docs/CONTROLLER.md` (§Principals table) | `agent-mesh/.agent/AGENTS.md` (cross-harness adoption) |
| Modularity / composability rules | `docs/ARCHITECTURE.md` (§State distinctions + lifecycle boundary) | `.agent/protocols/` (coordination law shared) |
| Effect policy / authorization | `docs/OPERATING-MODEL.md` (4 outcomes + approval schema) | `agent-configs/rules/` + `agent-configs/hooks/` |
| Design specs broken out by category | **§3 below (this file)** + `CANONICAL-INDEX.md` | `agent-mesh/research/INDEX.md` (12 cited digests) |
| The history / evidence / provenance | `docs/MASTER-PLAN.md` (§Delivery sequence + scorecard) + this §5 | `DECISIONS.md` D-001..D-035 + `research/` files |
| The failure anti-pattern register | `docs/DELIVERY-FAILURE-LEDGER.md` (DFL-001..020 / AP-01..027) | `agent-mesh/DECISIONS.md`, issue #57 (AP source) |
| Identity / attribution / commit range gates | `docs/COMMIT-IDENTITY.md` + `tools/identity/*` | `agent-configs/skills/` (validator adoption) |
| CI / receipt / exact-subject evidence | `docs/CI-GATES.md` + `tools/ci/run_gates.py` | `evals/` (YAML golden cases + stdlib runner) |

No agent should read the full 306-line START-HERE.md if its current phase is only the dispatch half; instead go to `docs/DISPATCH-LOOP.md` (§Modules + eligibility + capacity + dry-run guard). The architecture is explicitly modular: `agent-platform` owns portable contracts, `agent-mesh` owns portable brain/assets, `agent-configs` owns reusable library assets, and the runtime homes (`.buzz`, `.hermes`, provider profiles, model stores, caches, DBs) stay outside all three (MASTER-PLAN §Repo/storage map).

---

## 2. Architecture boundary (composable, not monolithic)

Per `ARCHITECTURE.md` + `MASTER-PLAN` §Repository/storage map:

```
agent-platform         <- canonical source of truth; contracts, control logic, receipts, evaluation seams
  ├── docs/            <- this consolidation + governing docs
  ├── tools/controller/ <- Gate C (github_contents_authority.mjs, dispatcher.mjs, dispatch_eligibility.mjs, ...)
  ├── tools/ci/         <- deterministic gates (run_gates.py) binding exact-subject commits
  ├── tools/identity/   <- attribution (configure_git_identity.py) + range validator (validate_commit_range.py)
  └── tests/            <- evidence fixtures (test_governing_policy.py, identity/, ci/)

agent-mesh             <- research + portable brain + evaluation harness + pipeline + command-center
  ├── .agent/          <- portable cross-harness layer (agents/, prompts/, protocols/, memory/ARCHITECTURE.md)
  ├── hermes/          <- bot profiles (SOUL.md bodies, cron, model-routing policy)
  ├── pipelines/       <- runnable stdlib-only (brief, intake, council aggregator, vault classifiers)
  ├── evals/           <- YAML golden cases + stdlib runner + judge protocol (generator ≠ judge)
  ├── research/        <- 12 cited digests (~3k lines) backed by first-principles + web + primary docs
  ├── command-center/  <- static v1 snapshot (SwarmClaw-inspired: snapshot script + HTML over sssf.db / herme state / gh board)
  ├── vault/           <- Obsidian second-brain taxonomy + auto-sort/link tooling
  └── DECISIONS.md     <- D-001..D-035 (OpenClaw archive, sanitization, model selection, concurrency, branch boundaries)

agent-configs          <- library / distribution candidate / reusable rule/skill/hook/prompt/role
  ├── rules/           <- enforced behavioral rules (not aspirational)
  ├── skills/          <- Claude Code SKILL.md + supporting files (adopted only after behavioral proof)
  ├── hooks/           <- PreToolUse/PostToolUse scripts (copied TO ~/.claude/hooks/; source never executed directly)
  ├── prompts/         <- reusable command/contract templates
  └── roles/           <- persona definitions (independent of runtime)

agent-workspace / agent-reports / govcon-factory / legacy openclaw*
  <- read-only migration evidence; not governing; read only when an admitted issue names the path (START-HERE.md §Entry contract #2)

Runtime homes (outside all repos above)
  <- .buzz, .hermes, .codex, provider profiles, model stores (~/models, OMLX, llama.cpp builds), caches, DBs, credentials, large artifacts.
```

The modular boundary is enforced by policy, not folder structure:
- **Projection ≠ Activation** (ARCHITECTURE.md §State distinctions): `projected -> discovered -> loaded -> activated -> behaviorally verified`. Receipts bind only the highest demonstrated state.
- **Controller is deterministic software**, never a persona / workflow / board / prompt (CONTROLLER.md §Implementation boundary; START-HERE.md §Controller requirements 1..12).
- **Principal separation is required by proof**: Controller App ≠ Reviewer App ≠ Promoter App ≠ Projector PAT (CONTROLLER.md §Principals; Gate C receipt #103 proves distinct bindings).
- **No wholesale migration**: "Nothing moves wholesale into `agent-platform`. Reusable behavior enters through an issue, a bounded candidate, current verification, and independent review." (MASTER-PLAN §Repository/storage map).

---

## 3. Design specs by category (the "broken out" layer the user asked for)

### 3.1 Lifecycle & Control (the spine)

| Component | File / Module | Evidence / Receipt | Gaps / Open |
|---|---|---|---|
| Task admission (issue + subissues + dependency resolution) | `tools/controller/github_task_admission.mjs` + `dispatch_eligibility.mjs` | Issue #103 input `a12d3a696...`; #81 base `37444ecd...`; #69 base `37444ecd...` | Full adversarial admission not yet over clean host (MASTER-PLAN §Critical Path 3) |
| Atomic CAS claim (lease + generation + fence) | `tools/controller/github_contents_authority.mjs` (640 lines) | Receipt `gate-c-receipt-33281620826-1` (artifact 9723173013); SHA-256 `e1fdb...`; CAS retries 4 | Clean-host reconstruction open |
| Isolated worktree at exact revision | `run_gate_c.mjs` / gate C workflow | PR #110 merged to `19246a5...`; candidate `9ec4b521...` | Worktree cleanup after completion verified (DESTINY: inspect post-merge branch removal) |
| Exact-candidate deterministic gates (CI) | `docs/CI-GATES.md`; `tools/ci/run_gates.py`; `tests/ci/test_run_gates.py` | Runs 33281657677 (exact-subject CI), 33281597637 (readiness RED → PASS), 33265987993 (pre-App proof) | Separate cryptographic CI principal not yet authorized (CI-GATES.md §Promotion disabled) |
| Independent read-only review | Reviewer App (separate token) | Review `5059477980` on PR #110; reviewer cannot modify (CONTROLLER.md §Principals) | Fresh reviewer identity verified; multi-model reviewer policy open |
| Expected-head promotion (compare-and-swap) | Promoter App (separate token) | Merge `19246a503...`; no self-promotion (OPERATING-MODEL.md §Principal separation) | Repeatability after terminal-state reconciliation open (#117) |
| Checkpoint / resume / teardown | `tools/controller/work_item_contract.mjs`; `terminal_projection_parity.mjs` | Receipt chain: admission → claim → workspace → checkpoint → candidate → gates → review → policy → promotion → projection → teardown | Terminal projection parity is report-only until Projector transition writes label + chained postcondition receipt (#117) |
| Dispatch selection (capacity-aware) | `dispatcher.mjs`; `capacity_policy.mjs`; `run_dispatch.mjs` | `tests/controller/four_worker_dispatch.test.mjs` asserts CAS fences 3 of 4 contenders (DFL-010 mapped) | No open `state:ready` eligible issue after #103; autonomous-drain fixture (#9) not yet demonstrated |

### 3.2 Identity, Attribution, Range Validation (the audit layer)

| Component | Source | Key constraint / output |
|---|---|---|
| Worktree-local identity config | `tools/identity/configure_git_identity.py` | Non-delivery domain `agents.invalid`; `extensions.worktreeConfig`; never `--global`; persona `^[a-z][a-z0-9-]{0,31}$`; run-id `^[a-z0-9][a-z0-9-]{7,63}$` |
| Commit trailer format | `docs/COMMIT-IDENTITY.md` §Required commit trailers | `Agent-Actor: agent/<persona>` + `Agent-Run-ID: <run-id>` + optional `Agent-Model`; must be contiguous, final block, blank-line split; `git interpret-trailers --parse` required; no multiline / duplicate / unknown keys allowed |
| Exact-range validator | `tools/identity/validate_commit_range.py` (626 lines) | Requires `python -I -S`; exact 40-hex OID input; `GIT_CONFIG_GLOBAL=/dev/null`; `GIT_NO_REPLACE_OBJECTS=1`; rejects shallow / graft / replacement-ref repos; proves `base..head` via reverse topo `rev-list`; portable JSON receipt with `execution: {attestation: "external-required", self_attested: false}` |
| Validator identity pinning | Same file (§Validator bootstrap) | Controller must supply exact `sha256` + `git_blob_sha1`; self-attestation explicitly false; trusted outer receipt required |

### 3.3 Effect Policy & Authorization (the guard)

Per `OPERATING-MODEL.md` (4 outcomes) + `DELIVERY-FAILURE-LEDGER.md` (DFL-013 / DFL-011 / DFL-003 / DFL-004):

- `DENY`: unsupported, ambiguous, stale, broad, prohibited, unauthorized.
- `AUTO_READ`: admissible read-only; gather evidence; record; no mutation.
- `AUTO_WRITE`: eligible write inside normal rollback envelope + bounded budget + valid lease + exact deterministic gates + independent review. Auto-promote only when all evidence passes; else fail closed.
- `APPROVAL_DESTRUCTIVE`: materially destructive, practically irreversible, or outside rollback envelope. Requires **exact** unexpired grant binding target / operation / scope / candidate revision / expiration / result / receipt ID. Only Mike / owner can issue; never by worker / generator / controller / reviewer / promoter / projector.

Work level (L0/L1/L2) is **ceremony only** — never waives authorization (
OPERATING-MODEL.md §Ceremony is not effect authorization). Proportional gate:
- L0 = observation/comment (`PATTERN-CANDIDATE` on owning issue, no branch/PR/review).
- L1 = bounded nonmaterial correction (focused falsifier + ordinary CI).
- L2 = material code / architecture / security (integration tests + exact-head independent review + promotion only when Operating Model authorizes).

### 3.4 Memory, Skill, Protocol, Agent Definition (composable brain layer)

From `.agent/` + `agent-configs/` + `hermes/`:

- `.agent/AGENTS.md`: adoption guide per harness (Claude Code = copy to `.claude/agents/`; opencode = `.agents/`; pi = `-p`; Hermes = profile + SOUL.md; DIY Python = layer order from `prompts/cache-stable-layout.md`).
- `.agent/agents/*.md`: 5 persona definitions (prime, scout, forge, sentinel, operator) — identity + voice + avoid-list; no provider/model/port.
- `.agent/prompts/*.md`: reusable task contracts (brief, scan, review, gate)
- `.agent/protocols/*.md`: coordination law shared across all agents (standing rules)
- `.agent/memory/ARCHITECTURE.md`: five-tier memory design (MemPalace adopted D-009; gbrain demoted to secondary/export; verbatim episodic ledgers preserved; search-before-synthesis gate kept)
- `agent-configs/skills/`: SKILL.md + supporting — adopted only after behavioral proof (generator ≠ judge; evaluator-before-generator settled)
- `agent-configs/hooks/`: must be copied TO `~/.claude/hooks/`; source directory never executed directly; every hook asset gets `SOURCE.md`
- `agent-configs/rules/`: enforced, not aspirational; each names what it governs + enforcement mechanism
- `hermes/`: profile-per-bot; root/default = short tier (65,536 / 4,096 output / low reasoning / MoA off / compaction at 51,200); mid = 131,072 / low; full = 262,144 / xhigh / 8,192 output (D-023)
- `evals/`: YAML golden cases + stdlib-Python runner; judge protocol requires different model family from generator (D-008; generator ≠ judge everywhere)

### 3.5 Pipelines & Command Center (operational layer)

From `agent-mesh/pipelines/` and `command-center/`:

- Brief (daily): fetchers → synthesis; uses stable cache-first layout (DR066)
- Intake: normalizer; feeds issue queue (not a second queue — issue #1 is sole authority)
- Council aggregator: non-monotonic; start 3 / cap 5 (D-006 / research-proactive-agents.md §4)
- Vault classifier: Obsidian taxonomy + kNN (bge-m3 sidecar) + MinHash dedupe
- Command-center v1 = static snapshot + HTML over `sssf.db` / hermes state / gh board; Langfuse/Phoenix deferred (D-011); no live engine until measured need
- Monitoring / service links / benchmark tracking: Phase 1 local only; MLflow loopback (`127.0.0.1:5001` + Basic Auth); Promptfoo 0.122.1 writes raw exports outside Git; allowlisted receipt sanitizer; zero default permissions (D-033)

---

## 4. History / provenance / evidence chain (reaching 95% via the open-claw path)

### 4.1 The OpenClaw lineage (the "initial open claw repo")

Per `agent-mesh/DECISIONS.md` D-001 / D-002 / D-003 / D-004 / D-005:

- Original: `redtrades/openclaw*` repos (multiple: v2 / v3 / backup / config folds).
- Decision (2026-08-26): one canonical archive repo = `redtrades/openclaw`; unique material from v2/v3/backup/config folds into it under `folded/`; others stay separate but sanitized.
- Sanitization whitelist (D-002): `.md/.yml/.yaml/.py/.json(≤1MB)/.txt(≤256KB)/LICENSE/.gitignore/.gitleaks.toml/.env.example`; everything else removed via **forward commits, history intact** (not history rewrite — preserves audit trail).
- Credential artifacts stripped from main branches (D-003); `ROTATION-REQUIRED.md` lists affected secrets.
- Private key `~/.openclaw/identity/device.json` secure-deleted (D-004; useless without paired state; system retired).
- New consolidated repo named `redtrades/agent-mesh`; universal rules stay in `agent-configs`, referenced doc-only (D-005 — no parallel infrastructure at rule surfaces).
- Evidence preserved in `agent-mesh/archive/` and referenced by `DECISIONS.md`; exact original `redtrades/openclaw` URLs not reconstructed from local files alone, but archive reference + D-001/D-002 description provide the mapping.

Certainty on this lineage: ~90% (archive reference + decision record present; original repo URLs not locally cached beyond reference names).

### 4.2 The agent-mesh build (overnight 2026-08-26 — "one brain, many harnesses")

From `README.md` + `HANDOFF.md` + `WORKLOG.md` (last 40 lines) + `DECISIONS.md` D-006..D-035:

- Built from: mined intent of retired OpenClaw + first-principles SOTA research (`research/INDEX.md` 12 files, ~3k lines) + Mike's live direction.
- 4 bot seed (D-006): Prime (orchestrator/dispatch), Scout (research/SOTA/intake), Sentinel (diagnostics/audit), Morning Brief (aggregation spine). Later tiers filed as issues, not built — prevents over-commit.
- 27B OMLX control selected initially (D-016 / D-017 / D-025 / D-026); exact model corrected by D-032 (identity correction: `Jundot/Qwen3.8-27B-oQ4e-mtp` ≠ `Qwen/Qwen3.8-Flash-Next`; latter is `qwen4_exp`, 125B main / 6B active + 51B n-gram + 4B MTP, AtomicChat `AD-3.84bpw-IQ4_XS-M64`).
- Evaluation: 8-cell empirical matrix on M1 Max 64 GB (400 GB/s, 21.8 TFLOPS); 91.2 tok/s @ 99.8% GPU util confirmed at `prefill_step_size=8192` / `max_num_batched_tokens=16384` — then D-027 superseded those as internal fields not operator-tuned. Model conclusions (TurboQuant KV4, Lightning MTP, ANE rejection due to kernel watchdog `Code 47`) remain.
- Queue / receipt / projection: command-center + issue board remain source; agent-mesh sources only for operational dashboards (D-022 — never cross-repo coordination).

Certainty on build: ~92% (live measurements quoted; receipts named; D-026/D-027/D-032/D-034/D-035 all with exact SHAs and file paths).

### 4.3 The agent-platform proof (Gate C — the canonical lifecycle)

From `START-HERE.md` §Current implementation state + `CONTROLLER.md` §Verified live proof + `MASTER-PLAN` §Factory acceptance scorecard:

- Proven chain (Issue #103 → PR #110 → `19246a5`): issue intake → CAS claim → isolated worktree → committed candidate `9ec4b521...` → exact-subject CI run 33281657677 → Reviewer App exact-head approval `5059477980` → Promoter App expected-head merge `19246a5...` → issue/Project projection → terminal receipt (`gate-c-receipt-33281620826-1`) → inspected cleanup.
- Distinct App identities verified: Controller / Reviewer / Promoter / Projector (separate PAT for Project 12, not a 4th principal).
- Receipt digest `sha256:e1fdb...`; artifact ID `9723173013`; input packet `a12d3a696...`.
- Historical proofs preserved: #81/PR #82 (run 33265987993) pre-App; #69/PR #68 first AUTO_WRITE (`37444ecd` → `6e3699b9` → `e8f58d56`).
- Gaps (explicit in START-HERE.md #Critical path, CONTROLLER.md §Gaps, MASTER-PLAN §Critical Path 2..5, DISPATCH-LOOP.md §What blocks next autonomous pass): clean-host reconstruction; interruption/resume; provider-neutral multi-harness (at least 2 harnesses + 2 providers); full scorecard; terminal projection parity (report-only until #117); autonomous-drain fixture (#9); next eligible `state:ready` issue after #103.

Certainty on proof: 95% (receipts exact, commits exact, actions exact; only "clean-host / multi-harness / full scorecard" open per own docs — not hidden gaps).

---

## 5. Cross-cutting references (this document is a node, not the graph)

Every claim above can be verified from:

- `agent-platform/docs/START-HERE.md` (cold start; authority rules; failure ledger reference)
- `agent-platform/docs/MASTER-PLAN.md` (north star; scorecard; sequence; economy)
- `agent-platform/docs/ARCHITECTURE.md` (boundary; state progression; GitHub Free limitations)
- `agent-platform/docs/CONTROLLER.md` (controller contract; principals; receipts; terminal parity)
- `agent-platform/docs/OPERATING-MODEL.md` (4 outcomes; approval schema; approval grant schema)
- `agent-platform/docs/DISPATCH-LOOP.md` (dispatch modules; eligibility; capacity; dry-run guard; observed readiness RED→PASS)
- `agent-platform/docs/COMMIT-IDENTITY.md` + `tools/identity/*` (attribution; exact-range gate; validator bootstrap)
- `agent-platform/docs/CI-GATES.md` + `tests/ci/` (deterministic evidence boundary; promotion disabled until trusted workflow)
- `agent-platform/docs/DELIVERY-FAILURE-LEDGER.md` (DFL-001..020; AP-01..027; PATTERN-CANDIDATE envelope; legacy-unmigrated status; current drift candidates AP-24/25/26/27)
- `agent-mesh/DECISIONS.md` (D-001..D-035; OpenClaw archive; model selection; concurrency; branch/scoping)
- `agent-mesh/research/INDEX.md` (12 cited digests; evidence base)
- `agent-mesh/HANDOFF.md` (current truth; OMLX control vs exact Flash-Next; evaluation gate status)
- `agent-mesh/.agent/AGENTS.md` + `agents/*.md` + `protocols/*.md` (portable brain layer; adoption per harness)
- `agent-configs/README.md` + `rules/` + `skills/` + `hooks/` + `roles/` (library; distribution rules; no wholesale load)
- `agent-platform/AGENTS.md` (repo-specific working agreement; L0/L1/L2; fail-closed; review separation)

---

## 6. How to navigate this architecture (answers the "different agents / easy to view" requirement)

For a new agent/session (cold resume per START-HERE.md §Cold resume procedure):

1. Read `START-HERE.md` (§What / Entry contract / Decisions / Controller / Critical path).
2. Read this file (§1 Navigation root) — pick the table row matching your phase (lifecycle / identity / policy / brain / pipeline / history).
3. Read the referenced governing doc for that phase (CONTROLLER / OPERATING-MODEL / ARCHITECTURE / COMMIT-IDENTITY / CI-GATES / MASTER-PLAN / DELIV-FAIL-LEDGER).
4. If your work touches `agent-mesh` assets, read `.agent/AGENTS.md`, then `HANDOFF.md` last 40 lines, then `DECISIONS.md` entries relevant to your change (verify D-number, don't invent a new one).
5. If your work touches library assets, verify against `agent-configs/README.md`; never bulk-copy; always record provenance (`SOURCE.md`).
6. Before any mutation: confirm issue #1 + child issue; confirm branch/revision; confirm claim / lease / generation; confirm independent review if L2; confirm effect classification (`DENY`/AUTO_READ/AUTO_WRITE/APPROVAL_DESTRUCTIVE) matches target + operation + scope + reversal; confirm expected-head promotion only after review + gates; confirm receipt chain binds exact inputs.
7. After mutation: write durable checkpoint (status, files, commands/results, blocker, next); push branch; open PR; bind CI receipt; separate review; promotion by Promoter App; project projection; teardown / transfer receipt.

No agent reads all of these in one pass. The architecture is intentionally modular so that the dispatch half only needs DISPATCH-LOOP.md + CONTROLLER.md §Required input + capacity_policy, not MASTER-PLAN §Scorecard. The brain layer only needs `.agent/` + `DECISIONS.md` entries it touches. The audit layer only needs identity + range validator + receipt chain. This is the composability guarantee.

---

## 7. Certainty summary (explicit, not implied)

| Area | Certainty | Basis |
|---|---|---|
| Core lifecycle (Gate C #103 / PR #110 / receipt) | 95% | Exact commit IDs, receipt SHA-256, artifact IDs, action run IDs, App identity separation all quoted in own docs |
| OpenClaw → agent-mesh archive / sanitization | 90% | D-001/D-002/D-003/D-004/D-005 in DECISIONS.md; archive/ reference; exact URLs of original redtrades/openclaw* not reconstructed from local files alone |
| agent-mesh build / model selection / concurrency | 92% | Live measurements quoted with receipt SHAs; D-026/D-027/D-032/D-034/D-035 have exact model IDs and file paths |
| Portable brain (.agent/, skills, hooks, protocols) | 93% | All files present; adoption per harness documented; copy-vs-symlink + SOURCE.md rule explicit |
| Library / distribution (agent-configs) | 88% | Directory map verified; adoption requires behavioral proof (not assumed) |
| Clean-host / multi-harness / full scorecard | 85% | Explicitly open per MASTER-PLAN critical path; no fabricated evidence |
| Terminal projection / #117 parity gate | 80% | Report-only evaluator exists; live Projector transition + chained postcondition receipt still required |
| Autonomous drain fixture (#9) | 75% | Not yet demonstrated; next eligible issue needed after #103 |

This file is a consolidation, not a claim of completion beyond what the source repos and receipts actually prove. All open gaps are named in §3.1 and §4, with references to the governing docs that control them. Do not treat the 95% headline as proof of full scorecard — that requires the 5 critical-path steps in MASTER-PLAN §Critical Path to complete.

---

*Last audited: 2026-08-30 (session). Consolidated from `agent-platform` (main `codex/worker-c-issue-9`), `agent-mesh` (`preserve/uncommitted-2026-08-29`), `agent-configs`, `agent-workspace`, `agent-tools`, `agent-reports`, and referenced `openclaw*` archive evidence. No changes made to governing docs; this file is an added navigation/consolidation layer only.*
