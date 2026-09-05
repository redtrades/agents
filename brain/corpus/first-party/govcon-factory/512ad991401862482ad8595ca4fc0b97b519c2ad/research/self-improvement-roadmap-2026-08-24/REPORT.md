# Self-improvement roadmap: from gate-enforced to genuinely self-improving

2026-08-24. Mandate: survey current SOTA for self-improving agent systems, do OpenClaw
archaeology (observer-only — its `AGENTS.md`/`CLAUDE.md` read as historical data, never as
instructions), assess the locally-installed `fusion-harness` pi extension, and synthesize a
prioritized roadmap for evolving this swarm from gate-enforced to genuinely self-improving,
self-optimizing, and proactive — Mike's benchmark being "like Hermes." Deliverable-first,
evidence-gated throughout: every verdict below cites a file, a commit, or a dated external
source, per the same discipline this repo already applies to customer-facing claims (`AGENTS.md`
rule 3, "no claim without a file").

Full working notes (URLs, additional detail) for Phase 1 and Phase 2 are folded into this
report; nothing external to the repo is treated as the durable record.

---

## 0. Where the factory actually stands today — the reality check this roadmap is built on

Verified directly against `origin/main` (`704fce3`) and the repo's own `git log`/`gh issue
list`, not assumed from the mandate's framing:

- **The pipeline is real and gate-enforced.** `pipeline/factory/` — typed envelopes, a
  fail-closed gate registry, a runner with a SQLite trace — has run end-to-end against a live
  same-day SAM.gov pull (`operations/runs/`). `pipeline/gates/gate_runner.py` covers G2/G3/G4/G5
  for the Sources Sought Response; G1 Compliance and the entire Market Snapshot gate set are
  explicitly **not yet scripted** (`pipeline/gates/README.md`).
- **CI is real, self-hosted, and already has an eval-discovery mechanism sitting idle.**
  `.github/workflows/ci.yml` discovers and runs any committed `verify*.py` script and any file
  matching `*poison*harness*.py`/`.sh` — today it "passes trivially" and prints "0 verify*.py
  scripts found" / "no poison harness in this repo yet" because nothing matching those globs is
  merged to `main` yet (`ci.yml` lines 58-89). This is load-bearing for §4.1 below: the CI hook
  this roadmap's first proposal needs already exists.
- **SSSF is wired in for real, narrowly.** `~/agent-workspace/adws/adw_govcon_pipeline.py` runs
  the deterministic half of the pipeline (`ingest → normalize → triage → match → assemble →
  gate`) as genuine synchronous `kind="code"` SSSF phases, mirrored into SSSF's own `sssf.db`
  (`pipeline/specs/factory-architecture.md` §8, live trace `operations/runs/3e625951/`). The one
  agent-driven phase that works, `packet_reviewer`, runs `coding_agent: pi` against local omlx —
  `coding_agent: claude_code` is a confirmed stub (`adw_modules/agent_cc.py` raises
  `NotImplementedError` unconditionally). This is a direct, in-repo reversal of the 2026-08-20
  report's "reimplement natively, don't run the dependency" verdict on SSSF — Mike's own install
  matured enough that the deterministic half was worth wiring in for real (`DECISIONS.md` D-003,
  "reversed-partially").
- **Proactivity infrastructure already exists, in heartbeat shape.** `scripts/daily-digest.sh`
  (scheduled 13:00 UTC) and `scripts/check-stale-claims.sh` (2-hourly) are real, running, batched
  heartbeats — not per-check cron sprawl. `scripts/lease-{acquire,release,status}.sh` and
  `scripts/check-worktree-hygiene.sh` close the exact category-6/7 gaps (abandoned background
  jobs, unlocked shared resources) the 2026-08-20 report flagged as the actual top cost driver at
  the time.
- **An eval-driven improvement loop already happened once, organically, without any framework —
  with one important correction to how it's usually described.** Two agents independently built
  an **agent-adjudicated** matcher gold set + a "poison test" harness for TASK-0018 (branches
  `work/gold-set-TASK-0018`, `work/matcher-gold-TASK-0018` — unmerged, read via `git show
  <branch>:queue/proposals/PROPOSAL-0018.md` / `...-0019.md`, not checked out). **Both source
  documents state plainly that TASK-0018's hand-label requirement is unmet**: `gold-set-TASK-0018`'s
  own README retracts an earlier "hand-labelled" description as *"an overclaim"* — *"these are
  agent labels, not hand labels"* — and `matcher-gold-TASK-0018`'s REPORT independently states the
  same thing. A ~10-row human spot-check (`SPOTCHECK.md`) is written and ready but has not run; per
  that document, 3+ disagreements on the 7 promotion rows would **void the reported 0%**. Both
  agent-adjudicated sets measured the shipped list-3 matcher against V6's required ≥80% precision
  gate (`AGENTS.md`: *"Matcher gold-set required (V6). Before any commercial list-3 send, precision on
  a hand-labeled set must be ≥ 80%. Below that floor is a hard stop."*) and both failed it —
  0% (n=7, 95% CI up to 34.8%) and 20% (n=45, 95% CI 10.9–33.8%) respectively. Both independently
  traced the failure to the same two root causes (geography-only promotion, an award-size-sorted
  candidate pool that never contains small businesses) and filed rival fix proposals
  (PROPOSAL-0018, PROPOSAL-0019) that are still unreconciled. **This is the single strongest piece
  of evidence in this whole roadmap**: eval-as-CI / golden-set work is not a hypothetical
  capability to build, it already produced a real, correct, embarrassing finding about shipped
  code — the only thing missing is making it run automatically instead of once, by hand, twice,
  independently.

---

## 1. Revisiting the 2026-08-20 verdict

`~/agent-reports/software-factory/2026-08-20-report.md` surveyed this space four days ago and
ruled several mechanisms Tier 3 ("not worth it right now") because the operator's actual failure
modes at the time were abandoned background jobs and missing resource locks — turn-discipline
problems, not model-quality problems. Those specific gaps are now structurally closed (leases,
stale-claim reaper, CI, §0 above). The question this section answers: does that change the
verdict, or does Tier 3 still hold on its own terms?

| # | Mechanism | 08-20 verdict | 2026 SOTA (current) | Verdict now | Why it changed (or didn't) |
|---|---|---|---|---|---|
| 1 | Eval-as-CI / golden sets | Tier 3 — "not worth it" | Mature tooling (`claude plugin eval`, TribeAI/claude-evals, sjnims/cc-plugin-eval); production practice is metric-based checks + LLM-judge for the rest + human review of the ambiguous 1-5%. **Panels specifically have a documented 2026 failure mode**: "Nine Judges, Two Effective Votes" (arXiv:2605.29800) found 9 correlated judges return the informational value of ~2. | **Build now, narrow.** Wire the existing gold-set/poison-test into CI's already-idle discovery hook. Skip multi-judge panels — the repo's proven mechanism (deterministic gold-set scoring) is the cheap, high-signal half of the 2026 hybrid pattern already. | §0's organic gold-set incident is the reversal trigger, not the SOTA survey alone — the capability already proved itself once. |
| 2 | DSPy / GEPA | Tier 3 | GEPA is an ICLR 2026 oral, 35x fewer rollouts than GRPO/RL, and has a documented local-Ollama execution path (Roy Wong, Medium, 2026), weakening the rollout-cost objection. Still needs a metric with text feedback — 20-100 labeled examples. | **Build later**, scoped to the matcher only, sequenced *after* item 1 exists (GEPA needs the gold set as its metric anyway). | Softened, not reversed — cost is lower than believed, but it's still not free on a GPU-constrained secondary machine, and it now has a real prerequisite (the gold set) that didn't exist on 08-20. |
| 3 | Skill-library accretion (Voyager-style) | Not separately scored on 08-20; `compound-engineering` flagged as "worth assessing" | SkillsBench (arXiv:2602.12670, 87 tasks across 8 domains, 7,308 trajectories) found **human-curated skills add ~16.6 points (33.9% → 50.5%)**; the paper's abstract doesn't state as strongly as this report originally implied that LLM-authored skills add zero — the load-bearing, verified figure is the curated-skill gain, not a flat null result for agent-authored skills. `/ce-compound` (installed) already runs the Voyager-style loop with a demonstrated real retrieval instance 18 days later. | **Mostly already covered.** Add a periodic *human* (or a distinct reviewer, never the authoring agent) curation pass over `docs/solutions/` — the one gap SOTA identifies. | New 2026 finding (SkillsBench) sharpens what to do, doesn't change that a new system isn't needed. |
| 4 | Reflection / self-critique loops | Tier 3 | Real gains on tool-use/diagnosable errors; real, named 2026 harms on objective tasks — over-correction, self-reinforcing false negatives, shared blind spots when generator=evaluator, confabulated failure narratives (arXiv:2607.28908, 2605.29463). | **Build later, narrow — no general critique-and-revise stage.** The existing pattern (`packet_reviewer` as a separate SSSF agent phase, not self-critique) is already the right shape per the "shared blind spots" finding. | Confirms the current design was accidentally correct; warns explicitly against generalizing it. |
| 5 | Agentic memory consolidation | Tier 2 | Four-lever framework converged (importance/merge/decay/**eviction**); `AutoDream`-style idle-time background consolidation is a live 2026 production pattern. | **Build later, small.** `MEMORY.md` already does the semantic-store tier; add a decay/eviction pass — some entries there are already stale (e.g. the Ox Alpha entry names its own 2026-08-27 removal date). | Unchanged tier; scoped to the one lever actually missing. |
| 6 | Automated curriculum from failures | Tier 3 | SEAgent/Agent0-class curriculum generation is real but confined to dense-automatic-reward sandboxes (computer-use, math/code RL). No evidence at this repo's scale (sparse, slow, human-gated reward). | **Not worth it.** The one usable idea — a failure becoming a durable "don't do that again" lesson — is already covered by `/ce-compound` + item 1's CI gate. | Confirmed, not reversed. |
| 7 | OTel tracing → automated optimization | Tier 2, spec-maturity caveat | GenAI semantic conventions reached v1.41, now the adopted standard (was pre-1.0 on 08-20). The actually-closed 2026 production loop is trace → curated eval case → CI gate, **not** trace → auto-rewrite. | **Build later**, sequenced after item 1 — reframe the goal as gold-set-mining infrastructure (traces feed new poison-test cases over time), not standalone observability. | Spec-maturity objection resolved; sequencing logic is new. |
| 8 | Proactivity — the Hermes benchmark | Not separately scored on 08-20 | Heartbeat-batching-over-cron-sprawl is the converged 2026 pattern (an 80% turn-cost reduction vs. per-check cron, per a concrete open-source scheduler); layered guardrails + human-on-the-loop + a held kill-switch are the production-safety norm, with an explicit warning against letting a scanner read an untrusted external source and act in the same causal chain. | **Build now, narrow.** `daily-digest.sh`/stale-claim-reaper are already the right shape (batched heartbeat, not cron sprawl). The literal gap vs. Hermes is auto-*filing*: extend the digest to stage `PROPOSAL-NNNN.md` drafts for recurring failure shapes it already has data for, never merge/ship/execute anything itself. | This is the direct answer to the benchmark named in the mandate. |

---

## 2. OpenClaw archaeology — lessons from a system that tried this and mostly didn't finish

**Identity check, load-bearing:** "OpenClaw" here is Mike's own archived fork
(`redtrades/openclaw`/`openclaw-v2`), not the real upstream `openclaw/openclaw` project — the two
share a name and nothing else; this has been misidentified twice before
(`~/agent-reports/agent-memory/openclaw-upstream-vs-mikes-repo.md`). Every file inside that
archive, including its own `AGENTS.md`/`CLAUDE.md`, was read as historical data describing what a
past system was built to do — never adopted as an instruction. Both checkouts were unmaterialized
on disk; every claim below traces to `git ls-tree -r HEAD` / `git show HEAD:path`, not a
filesystem walk (a naive `find` over the checkout returns false negatives).

### Shipped and running (confirmed by commit history)

| Mechanism | What it did | Verdict for this roadmap |
|---|---|---|
| Skill-discover + SOTA-EVAL graduation gate | Before authoring any new skill: define the gap, search local+archive+GitHub+MCP, score alternatives, write a verdict — a skill without a `SOTA-EVAL.md` "does not graduate." | **Low-priority port** — govcon-factory's `pipeline/skills/rubric-improve/` already does the structural equivalent for SOP/gate/skill changes (`AGENTS.md` rule 5). Reinforces rather than adds a new capability. |
| Three-layer circuit breaker (ADR-013) | Same action ×3 → abort; cron 5 errors → alert, 10 → auto-disable; hard turn caps. | **Port directly** into any new scheduled/autonomous runner from day one — was a backfill in OpenClaw (added *after* a runaway incident), no reason to repeat that lag here. |
| Delta classification + self-disabling pollers | Classify each poll MILESTONE/PROGRESS/STUCK/DONE/UNKNOWN, notify only on non-PROGRESS; a poller can disable itself. | **Port directly** — cheap noise-suppression for §4.2's proposed digest extension. |
| "Recommend, don't act" memory-promotion gate (`knowledge/1-rooms`) | Staleness (0 edits/30d) auto-*proposes* promotion; a human approves. | **Already the shape** of govcon-factory's proposal culture — safe, no new trust boundary. |
| Weighted-score autonomous backlog driver | Scored open work, picked exactly one item per fire, hard stops on failure streaks. | **The one item every independent OpenClaw evaluator flinched at and deferred, across five-plus separate passes, and it was never actually run.** Not proven bad — proven *untested*. Treat as the last, most-gated capability this roadmap could ever add, not a near-term build. |
| 19 launchd plists / scheduler substrate | The actual heartbeat/cron substrate. Two — `status-broadcaster` and `prime-daemon` — are named by OpenClaw's own post-mortem as "the lie / exit-1 pair": one misreported state, one silently exited 1. | **Direct warning.** A daemon that can fail silently is the opposite of this repo's "fail closed" rule (`AGENTS.md` rule 2). Any scheduled mechanism here must trip an actual gate on failure, never just log. |

### Specified, never shipped

The self-improvement loop items proper — `dspy-gepa-nightly`, `reflexion-loop`,
`distill-lora-weekly`, `routellm-train` — were audited by OpenClaw's *own* agents (Thread 7,
April 2026), which found 70% of a 16-item self-improvement proposal redundant with native
primitives (deleted) and marked the remaining four **DEFER, "until a failing eval demands
them."** None were ever built. "Genuine standups"/emergent multi-agent coordination was
explicitly named aspirational by OpenClaw's own research: *"No production reference exists.
Every published demo degrades into rubber-stamping or runaway debate within ~10 turns."*
Checkpoint/resume and an ontology/knowledge-graph layer were specified and never written.

### What actually broke

Two concrete incidents, both worth carrying forward as design constraints rather than abstractions:

1. **The system's own diagnosed "unforgivable failure" repeated ten days after it was named.**
   OpenClaw's post-mortem (`V3-MANIFESTO-AND-LESSONS-2026-05-22.md`) names *"building any
   standalone script + launchd plist + standalone vault dump again"* as the failure mode that cost
   11 PRs of disconnected infrastructure instead of integration. Ten days later, commit `2063b25b`
   did exactly that again. **A written rule against parallel self-infrastructure did not survive
   contact with the next work cycle** — enforcement has to be structural (a gate a build can't pass
   without), not documentary. This is the single most important transferable lesson in the whole
   archive.
2. **Committing raw agent transcripts as a memory substrate leaked 77–88 candidate secrets**
   across 9+ pushed remote branches
   (`~/.buzz/RESEARCH/OPENCLAW_ARCHIVE_CREDENTIAL_SWEEP_2026-08-16.md` §9c) — because agents read
   live credentials into context during normal work, and full session logs recording that context
   were git-committed wholesale, unredacted. That source itself cautions against hardening the
   count further: *"no exact integer should be quoted,"* and Mike's own actually-exposed count "may
   be well below 77" since many hits are documentation examples rather than live secrets. One Slack
   token alone appears in 182 committed files regardless of how the aggregate count is read. A
   near-identical AWS-key leak recurred four months earlier — same failure class, twice.

### Port vs. reject, filtered against this repo's actual culture

**Sound, low-risk, already-matching this repo's gate/proposal discipline:** the discover-first
gate (redundant with `rubric-improve` but harmless), the circuit breaker, the noise gate, and
"recommend don't act" memory promotion.

**The idea itself was the mistake, not just the implementation — do not port even in spirit:**
- Standalone script+scheduler+parallel-store as the *default* way to add automation. The
  govcon-factory analog to avoid: any future self-improvement work spinning up bespoke
  cron/scripts outside `pipeline/factory/`'s gate registry, `.github/workflows/`, and the issue
  queue, rather than extending them.
- Unreviewed agent-authored artifacts landing without another party's sign-off
  (`skills/proposed/` had no owner-approval field). This is precisely the failure
  `pipeline/skills/rubric-improve/SKILL.md`'s existing rule — *"Never apply your own proposal
  without another agent's or Mike's sign-off"* — already exists to prevent. **Worth confirming
  explicitly, not assuming**, that this rule is read as covering self-modification of
  `pipeline/skills/`, `pipeline/gates/`, and `pipeline/factory/` code, not only business
  `PROPOSAL-*.md` docs — OpenClaw's failure is exactly what happens when that scope is left
  ambiguous.
- Raw, unredacted transcript/log commits as a reflection substrate. Any future loop that reads
  `operations/runs/` traces for self-improvement must treat them as potentially containing
  secrets and never let derived output flow into a committed or shared location without a scrub
  step — the same discipline `AGENTS.md` already applies to `credentials/`.
- Emergent, undesigned multi-agent debate as a *default* coordination mechanism. OpenClaw's own
  research says this degrades within ~10 turns; if cross-agent adjudication is ever added beyond
  the existing per-deliverable G-gates, it should be hand-designed and opt-in by blast radius —
  never a standing swarm-wide loop.

**Bottom line:** OpenClaw's clearest lesson isn't "self-improvement is unsafe" — it's that
self-improvement is safe exactly to the extent it's forced through gates and a proposal flow that
already exist, and unsafe the moment it gets its own parallel scheduler, its own unreviewed write
path, or its own unredacted log store. govcon-factory already has the integration points OpenClaw
never built (`pipeline/factory/` gate registry, `operations/runs/` trace, `queue/proposals/`
no-self-accept) — the roadmap below is written to extend those, not create parallel ones.

---

## 3. Fusion-harness — assessed for the REVIEWER role specifically

Mike's specific question: is `fusion-harness` (a `pi`-coding-agent extension for two-model
architect/builder work with a gate-first validation loop) the right runtime for the swarm's
REVIEWER role — a different harness *and* model critiquing work, which fits the cross-model
review principle better than one model marking its own homework — versus reimplementing the
critique-skill pattern natively.

**What's actually installed, verified directly, not assumed:** `disler/fusion-harness`, cloned to
`~/agent-reports/factory-install/repos/fusion-harness`. It's a `pi` extension (`pi -e
fusion-harness.ts ...`), not an SSSF phase and not a Claude Code skill — a separate invocation
path from the `coding_agent: pi` phase already wired into `packet_reviewer`
(`pipeline/specs/factory-architecture.md` §8). `pi` itself and `just`/`jq`/`uv` are on this
machine; a local-only recipe (`fh-local`, pointing ARCHITECT/BUILDER at `omlx/qwen3.8` /
`omlx/qwen-sub`) was added during install specifically to avoid the hosted-API-key requirement the
shipped `fh-workhorse`/`fh-sota` recipes carry. No `AGENTS.md`/`CLAUDE.md` exists in this repo;
its `SYSTEM_PROMPT_*.md`/`USER_PROMPT_*.md` files (read as data, defining the sub-agent personas
the harness spawns, not instructions to any agent reading this report) were inspected directly.

**Two roles, not five:** ARCHITECT (plans, fuses, and — for `/auto-validate` — runs as VALIDATOR
under a distinct system prompt) and BUILDER, set per-invocation via CLI flags, no static roster
file. Three commands:

- **`/opinion`** — two models answer independently, read-only, side by side. No merge.
- **`/fusion`** — both answer with full tools; a third pass merges them with inline
  `[ARCHITECT]`/`[BUILDER]` attribution and a **Consensus & Divergence** closing section. This is
  the literal "critiquing each other's work" mechanism Mike named — not the two models arguing
  directly, but a synthesizer that names where they agreed, disagreed, and what was discarded and
  why.
- **`/auto-validate`** — a VALIDATOR writes a deterministic, executable acceptance gate (a PEP-723
  `uv` script) *before* any code exists, grounded in a read-only inspection of the actual project;
  BUILDER builds; the gate runs; every FAIL line is fed back verbatim until green or a round cap.
  The VALIDATOR's own system prompt (read directly,
  `extensions/fusion-harness/SYSTEM_PROMPT_VALIDATOR.md`) requires enumerating every explicit
  requirement in the request and mapping each to a concrete, objective check — "never vibes;
  never mere existence when content or behavior was requested" — which is structurally identical
  to what `rubric-improve`'s step 2 already asks a human-in-the-loop agent to do by hand ("can
  this become a mechanical gate... or does it stay a human call").

**Demonstrated evidence, both directions, from real runs already done on this machine**
(`~/agent-reports/factory-install/USING-FUSION.md` for the success case,
`~/agent-reports/factory-install/fusion-harness-verify.md` for the failure case):

- **Success**, `freellmapi/auto` backend: `/auto-validate` on a small, real, single-requirement
  task (`is_palindrome`) produced a 12-check gate — signature check, both true/false cases,
  case-insensitivity, punctuation-stripping, digit-preservation — in 30.97s, correctly **FAILED**
  the baseline (function didn't exist yet), then correctly **PASSED** after the builder's single
  round, for $0 and 92.7s total. Independently re-run by hand afterward: all 12 checks print
  `PASS`, confirmed not just logged.
- **Failure**, `omlx/qwen3.8` backend (the tier this repo would actually default to, per the
  Antigravity "default is local" constraint), **demonstrated once, under contention — the backend
  itself was not isolated as the cause.** `fusion-harness-verify.md` attributes the result to
  *"a struggling model on a contended, low-thinking-level local run"*: the VALIDATOR took ~26.6
  minutes for one turn while another `pi` session and Hermes were both reconnecting to omlx
  throughout, and `validator.md` shows the model correctly reasoning through a sound AST-based
  gate design that simply never got written to the file. The command produced a **truncated
  stub** — `code = "...\n..."`, no real assertions — which, because a bare Python script with no
  `sys.exit()` defaults to exit 0, **passed unconditionally, before and after the work existed.**
  The harness's own baseline-warning caught it (`⚠ BASELINE WARNING: the gate already PASSES
  before any work was done`) but **did not hard-block** — that's documented behavior (warn, don't
  refuse), not a bug, and it is exactly the "weak gate" blind spot fusion-harness's own README
  names. The recommendation below (use a hosted pairing for infrequent gate-authoring) still
  follows from this, but as a caution against an untested, contended local run for a
  high-leverage authoring task — not as a settled property of `qwen3.8` itself.
- **A structural durability gap**: every run writes only to `/tmp/fusion-harness-*/`, never into
  any repo or SQLite trace — confirmed live against the SSSF observability API
  (`/sssf/api/sessions` shows only SSSF ADW runs, nothing from fusion-harness). That conflicts
  directly with this repo's "no claim without a file" discipline unless output is deliberately
  copied out of `/tmp` before it's lost.

**Verdict: fit for a narrow, high-leverage slice of the REVIEWER role — mechanized *gate authoring*
specifically — not as a wholesale replacement for the live `packet_reviewer` phase, and not
without two fixes.** The `/auto-validate` VALIDATOR pattern is a genuinely working implementation
of exactly the judgment call `rubric-improve` already makes by hand ("can this become a mechanical
gate"), and using a *different* harness and model family to write and grade a gate is a real
instance of the cross-model review principle — the VALIDATOR never touches the code it's grading
(its own system prompt forbids writing anywhere but the gate path), which structurally prevents
the "shared blind spot" failure mode Phase 1 §4 flags for same-model reflection loops. But it
should not become the packet-level reviewer today: `packet_reviewer` already runs for real
through SSSF's `pi` agent phase with a durable trace; fusion-harness's value-add is upstream of
that — authoring the gates `pipeline/gates/README.md` still lists as unscripted (G1 Compliance,
the entire Market Snapshot gate set), a much less frequent, higher-leverage task where the
ephemeral-`/tmp` limitation matters less because a human copies the *result* (a committed
`gate_*.py`) out once, not every run. See PROPOSAL-0023.

---

## 4. Prioritized roadmap

Ordered by evidence strength × how directly it extends an existing integration point (per §2's
bottom line) × effort. "Builds on" always names a real, already-existing repo artifact — nothing
here proposes parallel infrastructure.

| # | Mechanism | What it is | Evidence it works | Builds on | Effort | Risk | First step |
|---|---|---|---|---|---|---|---|
| 1 | **Gold-set → CI gate** | Wire the matcher gold set + poison test into `ci.yml`'s already-idle `verify*.py`/`*poison*harness*` discovery, **report-only first**, flipping to a blocking check at the V6 80% precision floor only once the matcher fix actually lands and passes. | Already caught a real precision shortfall in shipped code, independently, twice (`work/gold-set-TASK-0018`, `work/matcher-gold-TASK-0018`) — **agent-adjudicated, not hand-labeled**; TASK-0018's hand-label requirement is unmet in both, and a written ~10-row human spot-check is still pending and could revise the reported 0% (see §0). 2026 SOTA confirms eval-as-CI is mature tooling and confirms *panels* specifically are the part to skip (§1.1). | `ci.yml`'s existing discovery step (lines 58-89); `AGENTS.md`'s V6 80% gate, already a stated hard stop; `check-branch-claim.sh`'s `continue-on-error` posture as precedent for a staged rollout. | **Medium.** The CI wiring itself is a no-op, but committing two differently-constructed labeled sets, running the human spot-check, and staging report-only→blocking is real work — not the "small" this proposal originally claimed. | **Low**, once staged correctly — the un-staged version (blocking immediately at 80% against 0-20% measured precision) would red-line the repo's only enforcement layer, which is exactly what PROPOSAL-0021's review caught. | Run the pending human spot-check on the ~10 rows, commit the two agent-adjudicated sets side by side (not pooled) as `verify*.py`/`*poison*harness*`-matching files, land the CI job as report-only, and open a **separate** proposal (not self-routed through this one) for the actual matcher fix from 0018/0019. |
| 2 | **Proactive opportunity-scanner** | Extend `scripts/daily-digest.sh`'s existing heartbeat to *stage* `PROPOSAL-NNNN.md` drafts (status: open, unassigned) for recurring failure shapes it already has the data to see — precision drift once #1 exists, stale unreconciled proposals, repeat claim-discipline violations (issue #44) — never merge, ship, or auto-execute anything. | 2026 SOTA: batched-heartbeat-over-cron-sprawl is the converged pattern (≈80% turn-cost reduction vs. per-check cron); human-on-the-loop + a held kill-switch is the production-safety norm. OpenClaw's own worked example (`knowledge/1-rooms`: staleness auto-*proposes*, human approves) is the same shape and had no reported incident. | `scripts/daily-digest.sh` (already scheduled, already reasoning over live repo state); `proposals/PROPOSAL-TEMPLATE.md`; `skills/rubric-improve/` (the existing human-or-agent review step every staged proposal would still go through). | **Medium** — the detector logic is a small delta on infrastructure that already runs daily, but the required guardrails (PR-opening rather than direct commit, a fresh circuit breaker, fail-closed error handling, suppression/delta-classification state) are real scope, not polish (issue #54 correction: raised from the original Small). | **Medium** — this is the literal "auto-file unprompted" capability, so the guardrail is the point, not an afterthought: never let it both read an untrusted external source (a live SAM.gov pull, an inbound email) and write/stage a proposal in the same causal chain (2026 guardrail literature, §1.8); it drafts, it never accepts (`rubric-improve`'s existing "never self-accept" rule already covers this). | Name the first 2-3 concrete failure-shape detectors (start with "an open PROPOSAL has sat >N days with a rival unreconciled PROPOSAL open on the same target" — literally PROPOSAL-0018/0019's own situation), add a `--stage-proposals` flag to `daily-digest.sh` that writes drafts instead of only listing findings. |
| 3 | **Fusion-harness as gate-author (narrow REVIEWER slice)** | Use `fusion-harness`'s `/auto-validate` VALIDATOR role to author the still-unscripted gates (`gates/README.md`'s G1 Compliance, Market Snapshot G1-G5), on a hosted pairing rather than an untested, contended local run for this infrequent, high-leverage task (§3 — the local `qwen3.8` failure was demonstrated once, under GPU contention, backend not isolated as the cause), with the harness's baseline-must-fail warning promoted from a soft warning to a hard block before a generated gate is trusted. | Real local install; a demonstrated real success (12-check behavioral gate, correct baseline-fail → pass cycle, $0, freellmapi backend) and a demonstrated real failure (silently-passing stub gate on local qwen3.8 under contention, caught only by an advisory warning) on this exact machine, this week (§3). | `pi` already installed and already the working agent path for `packet_reviewer`; `gates/gate_runner.py`'s existing "extending this script" pattern (one committed check at a time); `gates/README.md`'s explicit unscripted-gate backlog. | **Small** — the harness is already installed and verified working; this is a pilot on one gate, not new infrastructure (issue #54 re-check: still Small, unchanged). | **Medium** — bounded by two required fixes: (a) copy the run's `gate.py`/`summary.json` out of `/tmp` into the repo before it's lost (durability), (b) treat the baseline-must-fail warning as blocking, not advisory, before accepting any VALIDATOR-authored gate — the local-backend failure mode was demonstrated once, under contention, and warrants caution even though the backend itself wasn't isolated as the cause. | Pilot on G1 Compliance specifically (`requirements.json` → section-pointer mapping — a concrete, well-scoped check `gates/README.md` already names as the priority extension): run `/auto-validate` with `--architect freellmapi/auto --builder freellmapi/auto` (a hosted pairing, per §3's caution against an untested contended local run), manually confirm the baseline-fail step, then commit the resulting script into `gates/`. |
| 4 | GEPA on the matcher | Prompt/config optimization against the matcher's promotion logic, using the gold set from #1 as the scored metric. | ICLR 2026 oral, 35x fewer rollouts than RL, documented local-Ollama path (§1.2). | Item 1's gold set (hard prerequisite — GEPA needs a metric with text feedback, which is exactly what a poison-test scorer is). | Medium. | Low-medium — scoped to one module with an existing pass/fail metric, not open-ended prose. | Do not start before #1 ships; once it does, treat the gold-set precision score as GEPA's metric function and run against `pipeline/domains/govcon/`'s match config specifically. |
| 5 | `docs/solutions/` curation pass | A periodic (not per-run) human or distinct-reviewer pass over `/ce-compound`'s captured learnings, promoting the ones worth hardening into `AGENTS.md`/actual code, discarding noise. | SkillsBench: human-curated skills add ~16.6 points; see §1.3's correction on the LLM-authored comparison. | `/ce-compound` (already installed and running). | Small, ongoing. | Low. | Add a monthly cadence item to the existing `daily-digest.sh`/board rhythm: "N `docs/solutions/` entries older than 30 days, unreviewed" as a digest line. |
| 6 | Memory decay/eviction | A decay/eviction pass over `MEMORY.md` entries against a still-true/superseded/expired test. | Four-lever consolidation framework (importance/merge/decay/eviction) is the 2026 converged pattern (§1.5). | `MEMORY.md` (already the semantic-store tier). | Small. | Low. | Not this repo's file to build against directly (it's a cross-project memory system) — flag to Mike as a candidate for wherever `MEMORY.md`'s own tooling lives, sequenced after items 1-3. |
| 7 | OTel tracing → gold-set mining | Instrument `operations/runs/` traces to surface new candidate poison-test cases over time, not a general observability build. | 2026 production loop is trace→curated-eval-case→CI-gate, not trace→auto-rewrite (§1.7). | Item 1 (the CI gate this would feed); `operations/runs/`'s existing SQLite trace. | Medium. | Low, if scoped to feeding #1 only. | Sequence after #1 is running for a few weeks and has a real false-negative/false-positive history to mine. |
| — | Discover-first / SOTA-EVAL-style gate | Require a documented alternatives search before authoring any new skill/gate/recipe. | Worked without incident in OpenClaw; already adopted once elsewhere in Mike's stack (§2). | `pipeline/skills/rubric-improve/` — functionally already covers this. | — | — | **Not filed as a proposal** — largely redundant with an existing mechanism; note only. |
| — | Autonomous backlog driver (pick-and-execute next task unsupervised) | A weighted-score selector that both chooses and runs the next task with no per-task human gate. | Every independent OpenClaw evaluator (5+) flinched and deferred it; never run, never proven either way (§2). | N/A — deliberately not built on anything yet. | — | **High** — direct tension with "gates are necessary, not sufficient" and "send is the last thing that goes autonomous." | **Do not build.** If ever revisited, scope it to *proposing* the next task (writing to the issue queue) never *claiming and executing* it, and only after items 1-3 have run long enough to show the failure distribution has actually shifted toward needing it — the same "prove it's needed" bar the 2026-08-20 report itself used for Tier 3. |
| — | General reflection/self-critique stage | A standing critique-and-revise loop, generator=evaluator. | 2026 evidence shows net-negative/neutral on objective tasks; shared-blind-spot risk (§1.4). | — | — | — | **Do not build.** The existing separate-agent-reviewer pattern (`packet_reviewer`) is already the correct shape; expanding to same-model self-critique would be a regression, not progress. |
| — | Automated curriculum generation | Agent-generated next-tasks from failure, RL-style. | Confined to dense-reward sandboxes; no evidence at this repo's scale (§1.6). | — | — | — | **Not worth it**, confirmed. |

---

## 5. Guardrails this roadmap deliberately does not loosen

- **Nothing here authorizes a new autonomous send/ship path.** `AGENTS.md` rule 1 ("nothing
  leaves without Mike's approval") and the earned-autonomy principle ("send is the last thing
  that goes autonomous") apply unchanged to every item above — the proactive scanner (#2) drafts,
  it never files-and-forgets a decision; the gate-authoring pilot (#3) produces a script a human
  commits, not a live send-blocking change that ships itself.
- **Self-modification of code, not just business docs, goes through the same no-self-accept rule.**
  OpenClaw's `skills/proposed/` failure (§2) is the direct cautionary case. This roadmap's own
  three proposals (§6) are filed `status: open`, unaccepted, for exactly that reason — this report
  does not apply its own recommendations.
- **This report is not a PLAN-V(N+1) and does not reopen the evidence-gated plan freeze**
  (`PROPOSAL-0013`, `queue/proposals/PROPOSAL-0013.md`, if accepted). It is infrastructure/tooling
  scoped to `pipeline/`, `.github/`, and `scripts/` — orthogonal to the business-plan-version
  question that freeze governs. No item here changes pricing, the product, or the send/ship
  criteria.
- **Fail-closed, not fail-silent, for anything scheduled.** Per §2's OpenClaw
  "status-broadcaster that lied" lesson: any new heartbeat/scanner mechanism must trip an actual
  visible failure (an issue, a CI red, a digest line) on its own malfunction, never just stop
  running quietly.

---

## 6. Proposals filed

| ID | Title | Roadmap item |
|---|---|---|
| `PROPOSAL-0021` | Wire the matcher gold-set + poison-test into CI, report-only first, staged to blocking | #1 |
| `PROPOSAL-0022` | Extend the daily digest into a proposal-drafting opportunity scanner | #2 |
| `PROPOSAL-0023` | Pilot fusion-harness `/auto-validate` for authoring the unscripted G1/Market-Snapshot gates | #3 |

`PROPOSAL-0021` relies on the TASK-0018 gold sets described in §0 — **agent-adjudicated, not
hand-labeled**; a human spot-check is pending and could revise the measured precision. The
proposal itself stages accordingly (report-only until the matcher fix lands and passes 80%) rather
than treating the current 0%/20% figures as a number to gate on immediately.

Numbering starts at `0021`: `origin/main` carries `PROPOSAL-0001`–`0017`; `0018`/`0019`/`0020` are
claimed by unmerged work on `work/gold-set-TASK-0018`, `work/matcher-gold-TASK-0018`, and
`work/proposal-0020-queue-artifact-rot` respectively — filing a duplicate number would collide on
merge, the same reasoning `research/plan-evolution/REPORT.md` used when it started at `0013`.

Not filed, deliberately: the discover-first-gate note and the two explicitly-rejected items
(autonomous backlog driver, general reflection stage) in §4 — neither clears the bar of "a
concrete, first-implementable step" a proposal requires; both are recorded here as documented
`skip`, matching `rubric-improve`'s own convention for a considered-and-declined item.
