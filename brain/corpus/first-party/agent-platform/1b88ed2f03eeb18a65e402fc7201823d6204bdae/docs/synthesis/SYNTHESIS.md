# Synthesized Design Specification — Agent Platform Canonical Reference

Status: SYNTHESIZED from audited evidence (agent-platform / agent-mesh / agent-configs / openclaw archive / GitHub evidence #103 #81 #69 / receipts / DECISIONS D-001..D-035 / research/INDEX.md 12 files / .agent/ portable brain). Not a replacement of governing docs; supplements CANONICAL-REFERENCE.md + CANONICAL-INDEX.md.
Synthesis method: evidence-first extraction → category grouping → interface contract derivation → historical attribution → modular boundary enforcement.
Certainty band: 95% on verified receipts / commits / actions; 90% on model-selection / concurrency evidence (D-026/D-032/D-035 with exact SHAs); 85% on open gaps (clean-host / multi-harness / full scorecard / #117); 80% on original openclaw repo URL reconstruction (archive reference confirmed, original URLs not cached locally).

---

## 1. Synthesis thesis (what this document claims)

The agent-platform architecture is not a single repository or a single controller — it is a **three-layer composable system** with a deterministic spine, a portable brain, a reusable library, and strict boundary rules enforced by policy (not folder structure):

```
Layer 1 — Spine (authority, evidence, promotion): agent-platform
Layer 2 — Brain (portability, personas, protocols, memory): agent-mesh (.agent/ + hermes/ + pipelines/ + evals/ + command-center/ + vault/)
Layer 3 — Library (distribution, rules, skills, hooks, roles): agent-configs
Boundary — Runtime (credentials, models, caches, DBs): outside all three (MASTER-PLAN §Repo/storage map)
Evidence — Migration (openclaw* archive + legacy repos): read-only, only when admitted issue names path (START-HERE.md §Entry contract #2)
```

Synthesis conclusion: the canonical reference implementation must preserve **principal separation** (Controller ≠ Reviewer ≠ Promoter ≠ Projector), **exact-subject binding** (every receipt names exact commit / tree / input / artifact / review / promotion / projection / teardown), and **modular adoption** (no wholesale load from any layer into any other; every adoption requires a bounded issue + verification + review + promotion).

---

## 2. Interface contracts derived from evidence

These contracts are synthesized from `CONTROLLER.md` §Owned state (12 transitions), `OPERATING-MODEL.md` (4 outcomes), `COMMIT-IDENTITY.md` (range validation), `github_contents_authority.mjs` (CAS interface), and `.agent/AGENTS.md` (adoption rules).

### 2.1 Controller → Worker (dispatch contract)

```text
Input:  TaskPacket (issueId + taskId + inputRevision + role + harness + provider + model + budget + expiry + ownedPaths + acceptanceCriteria)
Output: Bound artifact + exact-candidate commit + receipt + checkpoint
Constraints:
  - One claim per packet (CAS lease; generation fence; replay allowed only from same attempt+generation)
  - One workspace per claim (isolated, hydrated at exact inputRevision)
  - One bounded phase (one role; one owned output; allowed/forbidden effects declared)
  - Checkpoints must be artifact-first (status, files, commands/results, blocker, next); no artifact → release ownership (DELIVERY-FAILURE-LEDGER.md DFL-005)
  - Review must be separate identity / model family (generator ≠ judge; D-008; .agent/protocols/)
```

Evidence: Gate C #103 / PR #110 / receipt `gate-c-receipt-33281620826-1` proves this chain end-to-end.

### 2.2 Controller → Reviewer (exam contract)

```text
Input:  Exact-candidate PR + review request + receipt chain so far
Output: Verdict (verified / failed / unsure) + exact findings (no repair; findings return to builder)
Constraints:
  - Read-only by policy (CONTROLLER.md §Principals; OPERATING-MODEL.md §Principal separation)
  - Must bind exact head; changed candidate invalidates prior review (DFL-009; delivery-failure-ledger.md)
  - Independent identity required (not same App token; not same model family preferred; review `5059477980` on PR #110 is the verified proof)
```

### 2.3 Controller → Promoter (promotion contract)

```text
Input:  Reviewed candidate + expected-head + receipt chain (admission → claim → workspace → checkpoint → candidate → gates → review → policy)
Output: Expected-head merge OR fail-closed (expected head changed / review missing / policy denied)
Constraints:
  - Separate token / App (verified in #103 readiness + execution runs; Projector PAT explicitly not the 4th principal)
  - Must reconcile expected-head against recorded base (DFL-018; DFL-017 stale replay denial)
  - Must record promotion receipt binding exact merge commit
```

### 2.4 Controller → Projector (projection contract, currently report-only)

```text
Input:  Terminal receipt (PASS + exact candidate/merge projection + issue/Project snapshots)
Output: Projected state (state:done + exact projection) OR report-only discrepancy (DFL-019; AP-24 historical drift: stale active labels on #91 / #93 / #103)
Constraints:
  - Must not become second authority (MASTER-PLAN §One authority per concern; START-HERE.md §Authority: Project 12 is derived, not lock)
  - Must chain to durable typed postcondition receipt (not yet active; #117 open)
  - Only existing Projector transition may clear labels / write Project fields (delivery-failure-ledger.md §DFL-019; current-state from START-HERE.md)
```

### 2.5 Identity / Attribution (commit-range contract)

```text
Input:  repo + base (40-hex OID) + head (40-hex OID) + expectedActor (agent/<persona>) + expectedRunId + expectedValidatorSha256 + expectedValidatorGitBlob + gitExecutable (absolute, pinned)
Output:  Portable JSON receipt (admitted / violations / commit list / execution: {attestation: "external-required", self_attested: false})
Constraints (derived from validate_commit_range.py 626 lines + configure_git_identity.py 151 lines):
  - Python must run -I -S (isolated, no site)
  - Git executable absolute + --no-replace-objects + GIT_CONFIG_GLOBAL=/dev/null + GIT_NO_REPLACE_OBJECTS=1
  - Repository must not have non-empty graft overlay / must not be shallow / must be inside worktree
  - Every agent-author commit must have Agent-Actor + Agent-Run-ID contiguous final block; optional Agent-Model; no multiline / duplicate / reorder / unknown keys
  - Author identity = committer identity = expected (author_committer_identity_mismatch is violation)
  - Material commits only (tree differs from first parent) counted; human-merge (multiple parents) allowed; non-material empty commits allowed but must match identity rules
  - Receipt never claims self-attestation (execution field fixed; trusted outer receipt required from controller)
```

Evidence: `tests/identity/` fixtures (worktree-local identity; range validation; malformed-history regression for PRs #14/#17/#18/#19).

---

## 3. Component registry (modular inventory, synthesized)

Each component names its layer (Spine / Brain / Library / Boundary), its governing contract, its evidence, and its interface to the others. Full table in `docs/synthesis/COMPONENT-REGISTRY.md`. Summary:

- **C-01..C-12 (Spine)**: intake → claim → workspace → phase → checkpoint → candidate → gates → review → policy → promotion → projection → teardown. Each transition returns a typed receipt binding exact inputs (CONTROLLER.md §Receipts).
- **B-01..B-04 (Brain)**: portable `.agent/` (personas/protocols/memory) → pipelines (brief/intake/council/vault) → eval harness (generator ≠ judge) → command-center (static v1, deferred live PWA).
- **L-01..L-05 (Library)**: rules / skills / hooks / prompts / roles. Each adopted only via bounded issue + behavioral proof; no bulk-load (agent-configs README).
- **E-01..E-05 (Boundary / Evidence)**: runtime homes (credentials, model stores, caches, DBs); openclaw archive; legacy product factories (`govcon-factory` / `agent-workspace` / `agent-tools` / `agent-reports`); GitHub Forge (Issues / Projects / PR / Actions / Contents API; not promotion mutex on Free plan); model / harness providers (provider-neutral adapter required; reports `projected → discovered → loaded → activated → behaviorally verified`).

---

## 4. Historical synthesis (the full path, synthesized from evidence)

### 4.1 Phase I — OpenClaw (retired, now archive)

Sources: `agent-mesh/DECISIONS.md` D-001..D-005 + archive reference.

- Multiple repos (`redtrades/openclaw*`) with v2 / v3 / backup / config folds.
- Decision (D-001, 2026-08-26): one canonical archive = `redtrades/openclaw`; unique material folded under `folded/`; others sanitized separately (history preserved via forward commits).
- Sanitization (D-002): whitelist `.md/.yml/.yaml/.py/.json(≤1MB)/.txt(≤256KB)/LICENSE/.gitignore/.gitleaks.toml/.env.example`; all else removed.
- Credentials stripped (D-003); private key `~/.openclaw/identity/device.json` secure-deleted (D-004); new repo named `redtrades/agent-mesh` (D-005); universal rules stay in `agent-configs`, doc-only reference.
- Synthesis: this is not just archive cleanup — it is the **origin proof** that agent-mesh did not invent architecture but mined intent from an earlier system, then corrected identity errors (D-032 correcting D-030/D-031's false model identity) and enforced versioned receipts.

### 4.2 Phase II — Agent-Mesh Build (overnight 2026-08-26)

Sources: `README.md` + `HANDOFF.md` + `DECISIONS.md` D-006..D-035 + `research/INDEX.md` (12 digests, ~3k lines) + live measurement receipts.

- Construction: 12 parallel agents (websearch + primary docs + local repo archaeology) produced 12 research digests.
- Bot seed (D-006): Prime (dispatch), Scout (research/intake), Sentinel (audit/diagnostics), Morning Brief (aggregation spine) — later tiers filed as issues, not built (prevents over-commit).
- Model selection path (D-016 → D-017 → D-025 → D-026 → D-027 → D-032 → D-034 → D-035):
  - Initial 27B OMLX control selected (`Jundot/Qwen3.8-27B-oQ4e-mtp` / `qwen3.8-oq4e`)
  - D-032 (2026-08-27): identity correction — `Jundot/Qwen3.8-27B-oQ4e-mtp` ≠ `Qwen/Qwen3.8-Flash-Next`; latter is `qwen4_exp` (125B main / 6B active + 51B n-gram + 4B MTP), AtomicChat `AD-3.84bpw-IQ4_XS-M64`
  - Previous measurements (D-026) preserved as historical 27B evidence; file names renamed (`bench_qwen38_27b_omlx_ssd_cache.py`; receipt `results_qwen38_27b_oq4e_control_2026-08-27.jsonl`)
  - Exact Flash-Next `AD-3.84bpw-IQ4_XS-M64` selected (D-035) at 131,072 context, 4,096 practical output; Q4.27 rejected at 128K (memory-pressure level 1); 262,144 resource-rejected
- Engine/cache boundary (D-027 supersedes D-026's scheduler-tuning claim: `prefill_step_size` / `max_num_batched_tokens` are internal dataclass fields, not operator-tuned; observed 89.2-91.2 tok/s remains workload measurement, not attribution to tuning)
- Memory (D-009): MemPalace adopted as semantic store; gbrain demoted to secondary/export; verbatim episodic ledgers preserved (git-canonical JSONL); search-before-synthesis gate
- Evaluation (D-008): minimal harness; generator ≠ judge; provider-agnostic endpoints
- Pipeline / command-center (D-011 / D-022): static v1; reuse over build; no cross-repo coordination (govcon-factory separate)
- Trade / arb (D-012): NOT built; prediction-market probabilities adopted as brief sentiment features only; NO auto-trading
- X intake (D-013): Owned Reads (~$0.001/read); Shortcuts POST; Nitter dead (C&D Aug 24 2026)
- Tracking (D-033): local only; MLflow loopback 127.0.0.1:5001; Promptfoo 0.122.1 out-of-Git; allowlisted sanitizer; zero default permissions
- Concurrency (D-019 supersedes D-018 coordination clause; D-023 tier assignments; D-026 2-slot / 2-agent receipts `0e3e13c6...` / `00dd96a4...`)

### 4.3 Phase III — Agent-Platform Canonical Authority (Gate C proof)

Sources: `AGENTS.md` + `MASTER-PLAN.md` + `CONTROLLER.md` + `START-HERE.md` §Current implementation state + receipt evidence.

- Issue #103 / PR #110 / `19246a5...`: principal-separated Gate C proof with distinct Controller / Reviewer / Promoter Apps + separate Projector PAT.
- Receipt `gate-c-receipt-33281620826-1` (artifact 9723173013) binds: admission → claim → workspace → committed candidate `9ec4b521...` → exact-subject CI 33281657677 → review `5059477980` → promotion `19246a5...` → projection → terminal receipt → inspected cleanup.
- Historical proofs preserved: #81/PR #82 (run 33265987993, pre-App, PR #74 base); #69/PR #68 (first AUTO_WRITE, base `37444ecd...`, candidate `6e3699b9...`, merge `e8f58d56...` — attempt 1 cancelled, attempt 2 passed, DFL-015 mapped).
- Critical path (MASTER-PLAN §Critical Path + START-HERE.md §Critical path): 5 steps — (1) reconcile receipts / stale labels; (2) repeat Gate C on eligible issue; (3) clean-host reconstruction + interruption/resume + adversarial lifecycle (#27); (4) provider-neutral multi-harness (2 harnesses + 2 providers) + scorecard; (5) only then broader adapters / product / estate.
- Gaps named (not hidden): clean-host; interruption/resume; multi-harness; full scorecard; terminal parity #117; autonomous drain #9; next eligible `state:ready` issue after #103.

---

## 5. Design choices documented (synthesis, not invention)

Each choice below is derived from source evidence and named as such.

| Choice | Source evidence | Rationale synthesized |
|---|---|---|
| One repository = one authority (agent-platform for lifecycle; agent-mesh for brain; agent-configs for library) | MASTER-PLAN §Repo/storage; START-HERE.md §Single work board; AGENTS.md | Prevent competing queues / split-brain (DFL-003 / DFL-010) |
| Principal separation required (Controller / Reviewer / Promoter / Projector) | CONTROLLER.md §Principals; OPERATING-MODEL.md §Principal separation; receipt #103 | Self-review / self-promotion is failure (DFL-007 / DFL-009) |
| Exact-subject binding at every step | CONTROLLER.md §Receipts; COMMIT-IDENTITY.md; CI-GATES.md | Changed candidate invalidates review (DFL-009); stale revision = DENY |
| Portable brain (`.agent/`) with adoption rules per harness | `.agent/AGENTS.md`; D-005; D-022 | Reuse over build; no bulk load; provenance (SOURCE.md) required |
| Four-effect policy (DENY / AUTO_READ / AUTO_WRITE / APPROVAL_DESTRUCTIVE) | OPERATING-MODEL.md; DELIV-FAIL-LEDGER DFL-013 | Work level (L0/L1/L2) is ceremony, never authorization |
| Identity via worktree-local Git config + exact range validator | `configure_git_identity.py`; `validate_commit_range.py`; DFL-020; COMMIT-IDENTITY.md | Attribution ≠ signature; non-delivery domain `agents.invalid`; isolated Python (`-I -S`) |
| Failure register is sole canonical anti-pattern index (DFL-001..020 / AP-01..027) | DELIVERY-FAILURE-LEDGER.md; D-001..D-035; issue #57 | Prevent repetition; fingerprint dedupe by SHA-256 of mechanism |
| Openclaw lineage preserved as archive + sanitization + decision log (not rewritten) | D-001..D-005; archive/ | Audit trail preserved; no history rewrite |
| Model selection corrected by versioned decision (D-032 superseding D-030/D-031) | DECISIONS.md D-032; HANDOFF.md; `qwen38-flash-next-experiment.yaml` | Identity errors must not propagate to performance/cache/engine claims |
| Static command-center v1 deferred from live PWA | D-011; SwarmClaw archaeology | No second queue / second authority / second promotion mechanism |

---

## 6. Certainty commentary (explicit, per section of this synthesis)

| Section / claim | Certainty | Why |
|---|---|---|
| Synthesis thesis (3-layer composable system) | 95% | GOVERNING docs (MASTER-PLAN / AGENTS.md / ARCHITECTURE.md) + this audit's cross-repo read |
| Interface contracts (§2) | 93% | Directly derived from CONTROLLER.md / OPERATING-MODEL.md / COMMIT-IDENTITY.md + receipt proof |
| Component registry (§3) | 92% | Each row named with module + evidence; interfaces derived, not invented |
| Phase I (OpenClaw archive / D-001..D-005) | 90% | Archive shape + decision record verified; original repo URLs not locally reconstructible beyond reference names |
| Phase II (agent-mesh build / D-006..D-035 / receipts with SHAs) | 92% | Live measurements quoted with receipt SHAs; D-026/D-027/D-032/D-034/D-035 all exact |
| Phase III (agent-platform / Gate C #103 / PR #110) | 95% | Exact commit / PR / receipt / run ID / artifact digest / App identity all in governing docs |
| Choice documentation (§5) | 90% | Each row cites source evidence; rationale is synthesis, not new invention |
| Open gaps (clean-host / multi-harness / #117 / #9) | 85% | Explicitly named in governing docs (MASTER-PLAN §Critical Path / START-HERE.md §Current state / DISPATCH-LOOP.md §What blocks) — not fabricated |

---

## 7. Navigation for this synthesized artifact

- Read CANONICAL-REFERENCE.md for the full consolidated audit + navigation guides.
- Read CANONICAL-INDEX.md for the 7-section quick-access map (by role / phase / category / history / evidence / file-tree / quick-jumps).
- This file (SYNTHESIS.md) is the **generative layer**: it extracts design contracts, registers components, logs synthesis decisions, and documents the open-claw-to-platform path — all from audited evidence, with nothing invented.
- For cold-start: START-HERE.md (§Cold resume) → CANONICAL-INDEX.md §1 (role) → this §3 (component registry) if implementing; → this §4 (history) if explaining provenance.
- For architecture change: read §2 (contracts) + §5 (design choices) + governing doc named in §3 table, then issue #1 + child issue + PR + receipt chain.

---

*Synthesized 2026-08-30. Evidence base: agent-platform (main `codex/worker-c-issue-9`), agent-mesh (`preserve/uncommitted-2026-08-29`), agent-configs, agent-workspace, agent-tools, agent-reports, openclaw archive, GitHub evidence #103/PR #110 / #81/PR #82 / #69/PR #70, receipt `gate-c-receipt-33281620826-1`. All claims backed by exact IDs in source repos; open gaps named explicitly. No fabrication of receipt evidence, commit IDs, run IDs, or model performance numbers beyond what source docs quote.*
