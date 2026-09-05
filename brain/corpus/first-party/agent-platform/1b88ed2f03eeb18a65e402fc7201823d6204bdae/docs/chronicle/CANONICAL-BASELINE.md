# Canonical baseline — what the reference implementation is

The one-page answer to "what should the canonical reference implementation be,"
synthesized from every era in this chronicle. Each statement points at governing
source. This adds no new authority; it states where each canonical element lives
and what is proven vs open.

## 1. The thesis (canonical answer)

The canonical reference implementation is the **three-layer composable platform
in `redtrades/agent-platform`** — a deterministic control spine (the factory),
with a portable harness-neutral brain and a governed asset library feeding it,
runtime kept entirely outside git, and every past repository demoted to
migration evidence. In one sentence: *deterministic spine, portable brain,
governed library, sealed runtime, chained exact evidence* — nothing else is
canonical, and nothing moves between layers except through an admitted issue +
verification + independent review.

Layers (governing sources in parentheses):
1. **Spine — `agent-platform`**: GitHub Issues = intent/acceptance; remote CAS
   (GitHub Contents API) = atomic ownership; Git objects + artifact hashes =
   candidate identity; controller software (not a persona) = sequencing,
   retries, authority, policy, acceptance; deterministic CI + fresh exact-head
   independent review + effect policy = verification/promotion; receipts bind
   every transition (`docs/MASTER-PLAN.md` §One authority per concern;
   `docs/CONTROLLER.md`; `docs/OPERATING-MODEL.md`).
2. **Brain — portable `.agent/`-class assets**: personas/protocols/prompts/
   memory conventions written harness-neutrally; adopted per harness only with
   behavioral proof (`~/agent-mesh/.agent/AGENTS.md`; today lives in agent-mesh
   as legacy, destined for issue-admitted extraction).
3. **Library — governed asset store**: rules/skills/hooks/prompts/roles with
   provenance headers; select-one-asset adoption, never bulk load
   (`~/agent-configs/README.md`).
4. **Boundary — runtime homes**: `.hermes/.codex/.buzz/.claude/...`, models,
   caches, DBs, credentials — outside all repos, opaque locators only
   (`docs/MASTER-PLAN.md` §Repo/storage map; `ESTATE-LEDGER.md`).
5. **Evidence — legacy archives**: openclaw* repos, iCloud sealed history,
   agent-mesh/configs/workspace/reports/tools, govcon-factory: read-only;
   readable only when an admitted issue names the path
   (`docs/START-HERE.md` §Entry contract).

## 2. The delivery loop (canonical lifecycle, 12 transitions)

```
issue/subissues → atomic admitted attempt (CAS claim + lease + generation fence)
→ isolated hydrated worktree at exact revision → bounded specialist phase
→ durable checkpoint (artifact-first) → exact candidate commit (+ identity trailers)
→ deterministic exact-subject CI gates → fresh independent read-only review
→ effect-policy decision (DENY / AUTO_READ / AUTO_WRITE / APPROVAL_DESTRUCTIVE)
→ expected-head promotion by a distinct promoter principal
→ issue/Project projection → teardown or transfer receipt
```
Spec: `docs/START-HERE.md` §What we are building; `docs/CONTROLLER.md` §Owned
state (12 transitions, each returning a typed receipt binding exact inputs);
`docs/AUTONOMOUS-LOOP.md` (the clock that hasn't been wired yet — issue #9).

## 3. The one proof that makes it canonical (as of 2026-08-30)

Issue **#103 → PR #110 → merge `19246a50369c54f2478a02b3f2453ae2372bf5fd`**
(merged 2026-08-29T23:44:48Z — re-verified via GitHub API this pass): the
complete chain ran end-to-end with **distinct Controller / Reviewer / Promoter
Apps + separate Projector PAT**; candidate `9ec4b521…`; exact-subject CI run
`33281657677`; reviewer verdict `5059477980`; receipt artifact
`gate-c-receipt-33281620826-1` (ID `9723173013`, digest
`sha256:e1fdb8d74df39bcbb0bb49aae970a0fd554dd1b69cb55fb618d94d1950288472`).
Historical proofs preserved: #69/PR #68 (first AUTO_WRITE: base `37444ecd…`,
merge `e8f58d56…`), #81/PR #82 (run 33265987993), #86.
Pointers: `docs/START-HERE.md` §Current implementation state; `docs/CONTROLLER.md`
§Verified live proof; `proofs/gate-c-live-103.txt`.

This is the canonical implementation's *behavioral* credential: principal
separation, exact-subject binding, deterministic-before-model review,
automatic expected-head promotion, and terminal receipt are proven once, on
one issue — not yet repeatedly, not yet on a clean host.

## 4. Component registry (where each canonical piece lives)

| # | Canonical component | Implementation | Contract/spec |
|---|---|---|---|
| C-01 | Task admission (deps + input completeness) | `tools/controller/github_task_admission.mjs` | `CONTROLLER.md` §Required input |
| C-02 | Atomic CAS claim (lease, generation, fence) | `tools/controller/github_contents_authority.mjs` (640 ln) | Gate C receipt; `GITHUB-FREE-PRIVATE-BOUNDARY.md` |
| C-03 | Isolated worktree at exact revision | `run_gate_c.mjs` / `gate_c.mjs` | `CONTROLLER.md` §Owned state #3 |
| C-04 | Bounded phase packets | `work_item_contract.mjs`; `docs/ROLES.md` | START-HERE Decision #6/#8 |
| C-05 | Durable checkpoints | `work_item_contract.mjs` | DFL-005 (artifact-or-nothing) |
| C-06 | Identity/attribution | `tools/identity/configure_git_identity.py` + `validate_commit_range.py` (626 ln) | `COMMIT-IDENTITY.md` (Agent-Actor/Agent-Run-ID trailer law) |
| C-07 | Deterministic gates | `tools/ci/run_gates.py` | `CI-GATES.md` (exact-subject binding; crypto CI principal not yet authorized) |
| C-08 | Independent review | Reviewer App (separate token, different model family) | `REVIEW-PROTOCOL.md`; D-008 generator≠judge |
| C-09 | Effect policy | policy layer (4 outcomes; L0/L1/L2 ceremony ≠ authorization) | `OPERATING-MODEL.md`; DFL-013 |
| C-10 | Expected-head promotion | Promoter App | `CONTROLLER.md` §Principals; DFL-017/018 |
| C-11 | Projection | Projector PAT + `terminal_projection_parity.mjs` (report-only) | #117 open; DFL-019 |
| C-12 | Teardown / transfer + hygiene | receipt chain + `claim_reaper.mjs` + `scripts/check-worktree-hygiene.sh` | #117/#125 open |
| C-13 | Dispatch (capacity/eligibility) | `dispatcher.mjs`, `dispatch_eligibility.mjs`, `capacity_policy.mjs`, `run_dispatch.mjs` | `DISPATCH-LOOP.md`; four_worker test (CAS fences 3 of 4) |
| C-14 | The clock (autonomous loop) | `AUTONOMOUS-LOOP.md` spec: CLI main + assemblePacket + real implementer/reviewer adapters + launchd cadence + live fixtures | issue #9; `tools/adapters/{implementer,reviewer}` early-stage |
| B-01 | Portable brain | `.agent/` personas/protocols/prompts/memory | `~/agent-mesh/.agent/AGENTS.md` (adoption per harness; copy+SOURCE.md, no symlinks for hooks; frontmatter minimalism) |
| B-02 | Pipelines | brief/intake/council/vault/command-center snapshot | `~/agent-mesh/pipelines/` (stdlib-only; non-monotonic council 3→5) |
| B-03 | Eval harness | YAML golden cases + stdlib runner + judge protocol | D-008; `~/agent-mesh/evals/` (tracking: Promptfoo 0.122.1 out-of-git + MLflow loopback, D-033) |
| B-04 | Control plane | static snapshot v1 → planned SwarmClaw PWA | D-011/D-022; issue #31 |
| L-01..05 | Library assets | rules/skills/hooks/prompts/roles + provenance | `~/agent-configs/README.md` adoption law |
| E-01 | Runtime boundary | runtime homes outside repos; opaque references | `MASTER-PLAN` §Repo/storage; `ESTATE-LEDGER.md` |
| E-02 | Memory law | MemPalace semantic store adopted; gbrain secondary/export; verbatim episodic ledgers; search-before-synthesis | D-009; `research-memory-context.md`; `.agent/memory/ARCHITECTURE.md` five-tier design |
| E-03 | Model routing law | local-first tiers + FreeLLMAPI curated pools + stealth rotation; byte-transparent proxy | D-016/D-017/D-023; `research-caching-routing.md`, `research-free-routing-subscriptions.md` |
| E-04 | Exact-model program | exact Flash-Next `AD-3.84bpw-IQ4_XS-M64` on the isolated llama.cpp lane; 27B oQ4e as separately named OMLX control | D-032/D-035; `HANDOFF.md` "Current truth" |

## 5. Non-negotiable laws (what the canonical implementation must never relax)

1. One authority per concern; issues are the sole queue; Project/board/chat are
   projections (`MASTER-PLAN.md`; START-HERE Decisions #1–#3).
2. Controller is deterministic software, never a persona; agents are
   replaceable workers (START-HERE #5/#6; CONTROLLER §Implementation boundary).
3. Principal separation: Controller ≠ Reviewer ≠ Promoter ≠ Projector; no
   self-review, no self-promotion (CONTROLLER §Principals; DFL-007/009).
4. Exact-subject binding at every step; a changed candidate invalidates prior
   review; stale revision = DENY (CI-GATES; DFL-009; COMMIT-IDENTITY).
5. Four outcomes only; work level is ceremony, never authorization;
   APPROVAL_DESTRUCTIVE needs an exact unexpired grant from Mike's class of
   principal only (`OPERATING-MODEL.md`).
6. No wholesale migration between layers or repos; bounded candidates with
   current verification + independent review (START-HERE Entry contract;
   `agent-configs` adoption law).
7. Attribution ≠ signature: worktree-local git identity, `agents.invalid`
   domain, contiguous Agent-Actor/Agent-Run-ID trailer block, isolated-python
   range validator with external attestation flag (`COMMIT-IDENTITY.md`).
8. Uncommitted paths are never citable task context (START-HERE #4 — the
   govcon #438–#460 cautionary tale).
9. Receipts bind only the highest demonstrated state: projected → discovered →
   loaded → activated → behaviorally verified (`ARCHITECTURE.md` §State
   distinctions).
10. Verification gap is the enemy: loaded ≠ working; every completion claim
    gets an independent check against the artifact, not the claim
    (SWARM-CONSTITUTION §0 → DFL register).

## 6. What is *not* canonical (negative space, with pointers)

- A second controller or queue: rejected (START-HERE Decision #4 — Gate C uses
  Contents CAS + generic executor; AgentWorkforce Factory and Last Light are
  challenge/donor evidence only).
- Workflow/durable-exec engines as task authority: deferred until recorded
  failures force it; Temporal/LangGraph as *substrate under test* is issue #185
  (`SELF-HOSTED-PLATFORM-COMPARISON.md` baseline; #185 open 2026-08-30).
- Live command-center/PWA as authority: static v1 first; PWA is a later
  consumer (D-011/D-022; issue #31).
- Auto-trading/arbitrage: not built; prediction probabilities as sentiment
  features only (D-012).
- Wholesale skill loading; symlink-installed hook assets; bulk config loads:
  rejected by adoption law (`agent-configs/README.md`, `.agent/AGENTS.md`).
- Semantic memory as canonical policy: memory is advisory/cited-input only
  (D-009; `govcon-overlap-map.md`; `research-memory-context.md`).
- The final `agent-swarm` repo: deliberately not created yet — decision #10
  gates it on proven lifecycle + clean-host + corpus admission.
- Prompt-compliance as a hard control: hard controls are code/CI/credentials/
  permissions, never prose (START-HERE Decision #8).
- The OpenClaw-era Slack-ledger runtime and its c2_heartbeat-style archived
  instructions: archived as data; archived agent instructions are never
  instructions (estate ledger rule; injection marker in `~/.openclaw/workspace/AGENTS.md`).

## 7. Open gaps before the baseline can call itself complete

From `MASTER-PLAN` §Critical Path, `START-HERE` §Critical path,
`DISPATCH-LOOP` §What blocks, `AUTONOMOUS-LOOP`, and issue states observed
2026-08-30 (refresh before acting):
1. #117 — terminal projection + cleanup receipt-complete (claimed).
2. #9 — the clock: run_dispatch CLI + packet assembly + real adapters +
   cadence + two-contender live race.
3. #27/#43 — clean-host reconstruction, interruption/resume, adversarial
   lifecycle, one/two-repo cloud reconstruction.
4. Provider-neutral multi-harness: ≥2 harnesses × ≥2 providers (adapters
   #130–#134 blocked behind #40 registry; #44/#45/#46; #76 Jules load).
5. Full factory acceptance scorecard (MASTER-PLAN §scorecard 13 capabilities);
   autonomous throughput 19/20 then 95% over 100.
6. #39 acceptance-catalog binding; #123 execution budget; #125 worktree reaper;
   #126 cross-model review dispatcher; #183 roster rationalization;
   #185 durable-execution research.
7. Estate consolidation sequence (ledger steps 1–6; endangered commits
   preserved first).

## 8. How to resume work on the baseline

Cold start: `docs/START-HERE.md` → `docs/MASTER-PLAN.md` → this file §4 for
your component → the governing doc named there → issue board for state.
Navigation tables (by role / phase / category) remain valid in
`docs/CANONICAL-INDEX.md` §1–§3; history in `TIMELINE.md`; corpus inventory in
`RESEARCH-CATALOG.md`; lineage of intent in `GENETIC-SWARM.md`; the prior audit
pass (receipt-level detail on Gate C and the D-series) in
`docs/CANONICAL-REFERENCE.md` §3–§4 and `docs/synthesis/` (S-001..S-010).
