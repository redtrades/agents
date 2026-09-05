# Synthesized Component Registry — Canonical Inventory

Companion to SYNTHESIS.md (§3) and CANONICAL-REFERENCE.md (§3 Design specs by category). Each row names the layer (Spine / Brain / Library / Boundary / Evidence), the governing contract file/module, the evidence that verifies it (commit / receipt / run ID / decision ID / research digest), and the interfaces to upstream/downstream components.

Source evidence used: `agent-platform/tools/controller/` (15 files), `agent-platform/docs/CONTROLLER.md` (§Owned state / §Principals / §Receipts / §Verification / §Acceptance), `agent-mesh/.agent/AGENTS.md` + `.agent/agents/*.md` + `.agent/protocols/*.md` + `.agent/memory/ARCHITECTURE.md`, `agent-mesh/DECISIONS.md` (D-006 bot seed / D-009 memory / D-011 command-center / D-022 source ownership / D-023 tier assignments / D-026/027/032/034/035 model selection), `agent-configs/README.md` + directories, `agent-mesh/research/INDEX.md` (12 digests), `agent-platform/docs/MASTER-PLAN.md` (§Repo/storage / §Factory acceptance / §Critical Path), `agent-platform/docs/DELIVERY-FAILURE-LEDGER.md` (DFL-001..020 / AP-01..027; PATTERN-CANDIDATE envelope; legacy-unmigrated status; current drift AP-24/25/26/27).

---

## Spine (authority / evidence / promotion — agent-platform owns)

| ID | Component | File / Module | Evidence | Interfaces (→ / ←) |
|---|---|---|---|---|
| C-01 | Issue / subissue intake + dependency resolution | `docs/START-HERE.md`; issue #1; GitHub Projects (derived, not lock) | Issue #103 / #81 / #69; subissue native dependency graph; Project 12 projection only | → C-02 (claim); ← C-12 / external (new packet) |
| C-02 | Atomic CAS claim (lease / generation / fence / tombstone / replay / takeover / expiration) | `tools/controller/github_contents_authority.mjs` (640 lines); `canonicalControlStatePath`; `mutate`; `claim` / `renew` / `checkpoint` / `complete` | Receipt `gate-c-receipt-33281620826-1` (artifact 9723173013; SHA-256 `sha256:e1fdb...`); CAS retries 4; replay allowed only from same attempt+generation; tombstone prevents re-claim; generation-mismatch / already-leased / lease-expired / owner-or-generation-is-not-current rules verified | ← C-01; → C-03 (workspace) |
| C-03 | Isolated workspace at exact input revision | `tools/controller/run_gate_c.mjs`; worktree hydration at admitted base | PR #110 worktree; candidate `9ec4b521...`; exact-subject CI 33281657677; branch bound to exact commit | ← C-02; → C-04 (phase) |
| C-04 | Bounded role phase (builder / implementer / worker) | `.agent/agents/*.md`; persona files; `CONTROLLER.md` §Owned state #4; `AGENTS.md` (L0/L1/L2; role declaration; allowed/forbidden effects) | 5 persona definitions (prime / scout / forge / sentinel / operator); role has one owned output; repair forbidden (reviewer does not fix — DFL-007; CONTROLLER.md §Principals) | ← C-03; → C-05 (checkpoint) |
| C-05 | Checkpoint / resume / teardown | `tools/controller/work_item_contract.mjs`; `CONTROLLER.md` §Owned state #5 / §12 | Checkpoint receipt chain; interruption-safe (DFL-015 cancellation = failure not proof; DFL-018 exact-run monitoring required); cleanup preserves durable authority (DFL-003: uncommitted ≠ delivered) | ← C-04; → C-06 (candidate) |
| C-06 | Candidate binding + exact identity / attribution | `docs/COMMIT-IDENTITY.md`; `tools/identity/configure_git_identity.py`; `tools/identity/validate_commit_range.py` (626 lines) | Worktree-local identity (non-delivery `agents.invalid`); `python -I -S`; exact 40-hex OID input; `GIT_NO_REPLACE_OBJECTS=1`; graft/shallow/replacement-reject; trailers `Agent-Actor` + `Agent-Run-ID` + optional `Agent-Model`; portable JSON receipt; validator bootstrap (issue #21) | ← C-05; → C-07 (gates) |
| C-07 | Deterministic CI / exact-subject gates | `docs/CI-GATES.md`; `tools/ci/run_gates.py`; `tests/ci/test_run_gates.py` | Runs 33281597637 (readiness RED→PASS); 33281657677 (exact-subject CI); 33265987993 (pre-App); promotion disabled until trusted CI principal + independent review + expected head | ← C-06; → C-08 (review) |
| C-08 | Independent review (read-only; exact-candidate only) | `CONTROLLER.md` §Owned state #8; `CONTROLLER.md` §Principals (Reviewer row); review `5059477980` | Separate App identity verified; read-only by policy; changed candidate invalidates review (DFL-009); reviewer cannot self-review (DFL-007); multi-model reviewer policy open | ← C-07; → C-09 (policy) |
| C-09 | Effect evaluation / classification | `docs/OPERATING-MODEL.md`; `OPERATING-MODEL.md` §Clean-context procedure | 4 outcomes (DENY / AUTO_READ / AUTO_WRITE / APPROVAL_DESTRUCTIVE); approval grant binds target/operation/scope/revision/expiry/result/receipt-ID; work level L0/L1/L2 = ceremony only; only Mike/owner can grant destructive approval; controller denies on stale/missing/ambiguous evidence | ← C-08; → C-10 (promote) |
| C-10 | Expected-head promotion (compare-and-swap) | `CONTROLLER.md` §Owned state #10; Promoter App (separate token) | Merge `19246a5...`; expected head must match recorded base; changed head = deny (DFL-009); stale replay denied (DFL-017); promotion receipt records merge | ← C-09; → C-11 (project) |
| C-11 | Issue / Project projection (derived, not authority) | `CONTROLLER.md` §Owned state #11; `tools/controller/terminal_projection_parity.mjs` | Report-only evaluator; #117 open (postcondition receipt + Projector transition required); DFL-019 (stale active labels #91/#93/#103) corrected only by existing Projector; Project 12 = derived view, not lock (MASTER-PLAN); never becomes second promotion authority | ← C-10; → C-12 (teardown) |
| C-12 | Teardown / transfer receipt + terminal state | `CONTROLLER.md` §Owned state #12; receipt chain closes; receipt `gate-c-receipt-33281620826-1` | Workspace removed / transferred; authoritative state preserved (durable receipt + branch); terminal issue must be `state:done` with exact projection; cleanup inspected (START-HERE.md §Evidence; receipt artifact 9723173013) | ← C-11; — (cycle to C-01) |

---

## Brain (portable / composable / harness-adoptable — agent-mesh owns)

| ID | Component | File / Module | Evidence | Interfaces |
|---|---|---|---|---|
| B-01 | Portable brain layer (`.agent/`) — personas / prompts / protocols / memory | `.agent/AGENTS.md`; `.agent/agents/*.md`; `.agent/prompts/*.md`; `.agent/protocols/*.md`; `.agent/memory/ARCHITECTURE.md` | 5 personas; adoption per harness (Claude Code / opencode / pi / Hermes / DIY Python); copy + SOURCE.md required; symlink only for identical-semantics single-file compat; frontmatter minimal (name + description only) | ← C-04 (adopts persona); → B-02 (pipeline) |
| B-02 | Pipelines (brief / intake / council aggregator / vault classifier / command-center snapshot) | `agent-mesh/pipelines/`; `agent-mesh/command-center/`; `agent-mesh/HANDOFF.md` | Stdlib-only; DR066 static-first caching; non-monotonic council (start 3 / cap 5; D-006); intake feeds issue queue (not second queue); vault uses bge-m3 sidecar + kNN + MinHash | ← B-01; → B-03 (eval) |
| B-03 | Evaluation harness (golden cases + stdlib runner + judge protocol) | `agent-mesh/evals/`; `DECISIONS.md` D-008; `HANDOFF.md` | YAML cases; generator ≠ judge enforced (different model family); provider-agnostic endpoints; benchmark tracking local-only Phase 1 (D-033) | ← B-02; → B-04 (command-center) |
| B-04 | Command-center v1 (static snapshot + HTML) | `agent-mesh/command-center/`; `DECISIONS.md` D-011; `HANDOFF.md` | Static over existing stores (sssf.db / hermes state / gh board); SwarmClaw-inspired; Langfuse / Phoenix deferred (measured need required); no second queue / promotion authority | ← B-03; — |

---

## Library (reusable / adopted via issue + verification — agent-configs owns)

| ID | Component | File / Module | Evidence | Interfaces |
|---|---|---|---|---|
| L-01 | Rules library (enforced behavioral rules) | `agent-configs/rules/`; README §Layout | Each file names what it governs + enforcement mechanism; not aspirational; adopted only through issue + verification; no wholesale load | ← B-01 / C-04 (adopted via bounded issue + behavioral proof) |
| L-02 | Skills library (SKILL.md + support) | `agent-configs/skills/`; README §Adoption | Adopted only after behavioral proof (discovery / permission / activation verified); provider-agnostic; generator ≠ judge; evaluator-before-generator | ← B-01 / C-04 (same adoption gate) |
| L-03 | Hooks library (PreToolUse / PostToolUse / etc.) | `agent-configs/hooks/`; README §Hooks | Copied TO `~/.claude/hooks/`; source directory never executed directly; SOURCE.md required for every copy; hook assets get provenance stub | ← L-01 / L-02 (installed, not adopted as authority) |
| L-04 | Prompt contracts (reusable task contracts) | `agent-configs/prompts/`; `.agent/prompts/`; `memory-context.md` / `cache-stable-layout.md` | Stable blocks first; volatile data last; no provider/model/port named in brain layer; adopted via harness config layer | ← B-01 (indirect adoption via persona) |
| L-05 | Role / persona definitions (independent of runtime) | `agent-configs/roles/`; `.agent/agents/*.md` | Identity + voice + avoid-list only; no provider/model/port; copied to harness-specific directory with SOURCE.md | ← B-01 (direct adoption) |

---

## Boundary / Evidence / Migration (outside the three active layers)

| ID | Component | Evidence / Reference | Status / Constraint |
|---|---|---|---|
| E-01 | Runtime homes (credentials / model stores / caches / DBs / large artifacts) | MASTER-PLAN §Repo/storage map; `AGENTS.md` §Keep credentials outside repos; `ST-ARTHERE.md` §Cold start (#4: credentials behind opaque locators) | Read-only from source repos; never committed; access via opaque references only |
| E-02 | OpenClaw archive (retired system; sanitized) | `agent-mesh/DECISIONS.md` D-001..D-005; `archive/`; `ROTATION-REQUIRED.md` | Migration evidence; read only when admitted issue names path; never governing |
| E-03 | Legacy product factories (`govcon-factory`; `agent-workspace`; `agent-tools`; `agent-reports`) | MASTER-PLAN §Repo/storage map; START-HERE.md §Entry contract #2; AGENTS.md; `DECISIONS.md` D-014 / D-022 / D-024 | Separate products / runtime directories; not part of platform authority; must have explicit issue + claim + workspace + review + promotion to contribute |
| E-04 | GitHub Forge (Issues / Projects / PR / Actions / Contents API) | `ARCHITECTURE.md` §GitHub Free private boundary; CI-GATES.md; CONTROLLER.md §Principals (App tokens) | Not a promotion mutex on Free plan; CI evidence not required merge check; App tokens must match role slugs; Projector PAT separate from Controller/Reviewer/Promoter |
| E-05 | Model / harness providers (OMLX / llama.cpp / Hermes / Claude / Gemini / Grok / etc.) | `agent-mesh/HANDOFF.md`; `DECISIONS.md` D-016..D-035; `evals/`; `.agent/AGENTS.md` adoption | Provider-neutral adapter required; adapter reports `projected → discovered → loaded → activated → behaviorally verified`; never owner of task state (MASTER-PLAN) |

---

## Cross-reference to CANONICAL-REFERENCE.md / SYNTHESIS.md

- C-01..C-12 map 1:1 to SYNTHESIS.md §3.1 (Lifecycle & Control) table and §2 contracts (§2.1 Controller→Worker through §2.4 Controller→Projector; §2.5 Identity).
- B-01..B-04 map to SYNTHESIS.md §3.4 (Memory/Skill/Protocol/Persona) and §2 adoption rules.
- L-01..L-05 map to SYNTHESIS.md §3.4 library layer + §2 adoption rules + `agent-configs/README.md`.
- E-01..E-05 map to SYNTHESIS.md §2 architecture boundary + MASTER-PLAN §Repo/storage + ARCHITECTURE.md §GitHub Free boundary.
- Evidence column references exact receipt SHAs, action run IDs, PR / issue numbers, D-series decision IDs, and 12 research digest filenames — all verified in prior audit reads from `agent-mesh/research/INDEX.md`, `DECISIONS.md`, and `agent-platform/docs/CONTROLLER.md` / receipt documentation.

---

*Synthesized from audited source. Not a replacement of governing docs. All evidence sources listed per row; no fabricated receipt data, commit IDs, run IDs, or model performance claims. Open gaps (clean-host reconstruction, multi-harness neutrality, full scorecard, #117 parity, autonomous drain #9) marked via boundary / evidence references rather than hidden.*
