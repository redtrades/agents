# The AISDLC swarm: full arc, root-cause analysis, and a SOTA-grounded redesign

**Date:** 2026-09-04
**Author:** Claude (Sonnet 5), reading session
**Status:** Extends the 2026-09-03 RCA (`110-failures-postmortems-and-lessons/selected-originals/20260903-death-spiral-rca.md`) with a second, live occurrence of the same failure mode, a today-dated root-cause update, and a SOTA-grounded redesign proposal.
**Canon:** [`00-start-here/START.md`](../00-start-here/START.md) · Parent board [agent-sdlc#117](https://github.com/redtrades/agent-sdlc/issues/117).

This document does not re-litigate intent. The north star is settled
(`INTENT-AGGREGATE.md`, `20260831-current-intent-decisions.md`): AISDLC proof
first (issue → verify → independent review → exact-head merge, WIP=1), then
GovCon (~$8-10k/mo buyer-actionable deliverable). This document is diagnosis and
a build proposal, not a new intent round.

---

## Section 1 — Full arc history

### 1.1 Why this started

`MIKE-INTENT-DEBRIEF-2026-08-28.md` (`agent-configs` `6850fa3:knowledge/`) states
the goal precisely: a business that sells federal-contracting deliverables
produced by an agent swarm, and a swarm that survives agents dying mid-task and
does not depend on any single vendor. The financial target is $8,000-$10,000/mo
profit by month 12, with Mike's own attention capped near 40 hours/week and the
swarm running continuously. The SDLC exists to let work survive session death
and vendor quota exhaustion, not as process for its own sake — his stated target
is 95% autonomy with himself involved only in planning and final checks.

The debrief also names the mechanics Mike had already ratified by 2026-08-28:
GitHub Issues as the single work queue ("one of the original sins of trying to
do things from scratch" was the markdown-task-file approach that preceded it),
one worktree per session, tiered merge authority, cross-model-family review as
non-negotiable, and — critically — **"max three active work threads. Everything
else waits as a queue issue. He accepted the speed cost explicitly."** That WIP
cap was stated as owner intent on 2026-08-28. It has never been mechanically
enforced in any of the five attempts below.

### 1.2 The succession of platforms

Five same-goal implementation attempts exist on disk, in a strict lineage each
successor is aware of and none of them killed cleanly before starting the next:

| # | Repo | Built | Approach | Fate |
|---|---|---|---|---|
| 1 | `agent-platform` | pre-2026-08-26 (evidence includes 98 stale git worktrees) | "Clean, provider-neutral infrastructure," genetic/portfolio-style experiment swarm, its own `docs/START-HERE.md` claiming to be sole cold-start authority, its own `DELIVERY-FAILURE-LEDGER.md` | Frozen 2026-09-03. Its own README today carries a FROZEN banner citing the estate-structure decision. Never shipped a completed issue-to-merge cycle under its own lifecycle. |
| 2 | `agent-mesh` | overnight, 2026-08-26 | "One brain, many harnesses" — portable `.agent/` cross-harness layer, Hermes bot deployment, `command-center/` static dashboard, built explicitly from "the mined intent of the retired OpenClaw system... first-principles SOTA research, and Mike's live direction" | Sibling of #1 and #3, not a distinct architecture — the estate's 2026-09-03 structure decision reclassifies all three as "SAME-ATTEMPT family... not three roles." Frozen. |
| 3 | `agent-workspace` | overlapping with #2 | Plain-files-and-git coordination: `tasks/*.md` frontmatter, `scripts/claim-task.sh`/`complete-task.sh`, git pre-commit hooks as the only enforcement, no GitHub Issues, no CI, no reviewer bot | Frozen. Same root failure as #1/#2 restated with a lighter mechanism — coordination-by-convention with no mechanical gate. |
| 4 | `agent-sdlc` (Symphony + Codex, ADR 0001) | began ~2026-08-31 per Decision 58 | Bounded Fusion adoption trial vs. Paperclip as a mutually-exclusive challenger over a neutral lifecycle contract; `agent-sdlc` explicitly scoped to start as "a composition and assurance repository rather than a second controller" | **Live.** This is the sanctioned implementation target. Produced the first genuine issue→verify→independent-review→exact-head-merge proof (#119/PR #120, Goal B canary) on 2026-09-03. |
| 5 | Fusion (control plane, inside #4) | deployed 2026-09-04 | `@runfusion/fusion` v0.77.0 (Mike's fork `redtrades/Fusion`), embedded PostgreSQL, running natively on port 4040, task board (`SWARM-*` ids) polling `redtrades/agent-sdlc` | **Live, currently in the second documented death spiral (see 1.4).** |

`govcon-factory` is a separate, earlier lineage (the original business
implementation, frozen 2026-09-03, harvest-only — its `PLAN-V5.md` briefly
contradicted its own freeze banner nine lines down and was fixed in PR #464).
It is evidence for the business goal, not part of the swarm-platform succession
above.

The pattern across attempts 1-3: each restated "clean, provider-neutral,
first-principles" framing (`agent-platform`'s README literally says "This
repository starts clean... their instructions and structure are not
inherited") while re-deriving the same orchestrator-worker-plus-git-queue
architecture the prior attempt had already built. None reached a completed
issue-to-merge cycle before the next reboot began. `agent-mesh` was "built
overnight" the same week `agent-platform` existed; `agent-workspace` overlapped
both. The estate's own 2026-09-03 structure decision had to formally declare
these three "not three roles" — one attempt, restated three times, was mistaken
for progress until an owner ruling collapsed them back into one line in
`HISTORIC-INDEX.md`.

### 1.3 The first documented death spiral (2026-09-03)

Captured verbatim in the existing RCA (`20260903-death-spiral-rca.md`),
summarized here for continuity rather than duplicated:

- 10+ `agent-sdlc` issues all reduced to "format a GitHub issue/PR/commit
  reference" — a ~5-line function — retried and re-retried, every one
  `sdlc:blocked`.
- 30+ PRs merged in one day, zero completed issue-to-merge for the actual MVP.
- Another agent had already written the same RCA days earlier (issue #106:
  "agents follow cwd, not the estate — worktrees + many controllers + unread
  freeze"). Nobody acted on it — a diagnosis was filed, not fixed.
- Issues opened to re-decide already-decided intent (#96-#99, #105) while the
  MVP sat unbuilt.
- 110 `AGENTS.md` files and 86 `CLAUDE.md` files existed under `~/`; ~250 stale
  git worktrees; two competing "first-principles reboots" both claiming sole
  authority at once.
- The session writing that RCA was itself an instance of the failure it
  diagnosed: it drifted from "trace your config" through six unrelated
  workstreams across 20+ PRs in 6 repos over one session.

That RCA's own prescribed test was: **in 30 days, either a govcon deliverable
a buyer could receive, or a swarm issue-to-merge with no human touch — or the
freeze did not hold.** One day later, the freeze did not hold; see 1.4.

### 1.4 The second, live death spiral (2026-09-04) — verified today

`fusion task list` today (2026-09-04, this session) shows the `SWARM-*` board
in exactly the shape the RCA predicted: 36 Todo, 9 In Progress, 10 In Review,
22 Done, 18 Archived. Of the 36 Todo + 10 In Review + 18 Archived items, a
concrete count against the live GitHub issue tracker:

```
$ gh issue list --repo redtrades/agent-sdlc --state all --limit 300
total issues: 169         (created 2026-09-01 04:47 UTC → 2026-09-04 17:12 UTC, i.e. under 4 days)
open: 30   closed: 139
"SWARM-013" / "spawnedBy" duplicate-titled issues: 24
"GovCon evidence workflow" duplicate-titled issues: 10
merged PRs: 71, all authored by the single shared `redtrades` login (no distinct per-agent identity)
```

That is **34 near-identical duplicate issues** chasing exactly two stuck tasks:

1. **SWARM-013** ("Set up a low-risk fixture issue for SWARM-008 canary
   testing") — stuck at step 3/7, "Verify the fixture via REST API," for over
   five hours by its own log (`8:00 AM` → `12:22 PM` entries), re-seeded three
   times ("Re-seeded for re-specification — new dependency added" at 11:28,
   11:58, 12:11) without the underlying blocker changing. Each re-seed spawned
   a new GitHub issue announcing the same unmet dependency.
2. **SWARM-098** ("Verify GovCon evidence workflow integrity and approval
   chain completeness") — its own task log shows the actual mechanical cause:
   `Workflow graph failed at node 'parse' (missing-implementation-steps) —
   automatic recovery cannot move 'in-progress' backward; card remains in
   place`. The task references `workflow_id: "SWARM-098"` on its own
   dependents, but only Fusion's built-in workflow ids exist
   (`builtin:coding`, `builtin:coding-ideas`, etc.) — SWARM-098 points at a
   workflow that was never registered. Every agent that picks this up
   diagnoses the same missing-workflow error fresh and files a new
   verification/investigation issue rather than fixing the one-line
   `workflow_id` reference or registering the workflow.

**Root cause of both, verified directly in this session:**
SWARM-013's own execution log (`fusion task logs SWARM-013`) shows the
executor calling `fn_secret_get(key=GITHUB_TOKEN, scope=project)` and
receiving `{"error":"not-found"}`, then `bash env | grep -i github` returning
nothing, then `fn_task_done(outcome=blocked, obstacle=outside-worktree,
reason=... no usable GitHub token is available ...)`. **Correction from an
earlier draft of this document:** `/Users/man/.fusion/settings.json`'s
top-level `"github": false` field is a *research-source* toggle
(`researchGlobalGitHubEnabled`), and `tokenStrategy.token: null` belongs to
remote-access/tunnel auth — neither is the per-project secret store and
neither proves the credential gap on its own (caught by independent
cross-family review, see Addendum). The task-log evidence above is direct and
sufficient: SWARM-013's step 3 ("Verify the fixture via REST API") cannot
complete without live GitHub API access; it silently stalls rather than
failing loud, so the scheduler treats it as "needs re-specification" and
spawns a fresh attempt instead of surfacing "credential missing, operator
action required."

The pattern is identical to the 2026-09-03 spiral in every structural respect
except the specific stuck task: a mechanical/credential gap causes silent
stall → no circuit breaker distinguishes "blocked, needs one fix" from
"unknown, try again" → agents re-diagnose from scratch → each re-diagnosis
files a new issue instead of correcting the earlier one → the board fills with
near-duplicate investigation/verification issues that consume review and merge
capacity without producing product movement → nobody notices the WIP cap and
duplicate-issue guardrails discussed in the first RCA were never built. This
recurred **one day** after the first RCA's freeze was declared and honored on
paper. Some genuine product work did land in the same 2026-09-04 window (see
`DONE-LEDGER.md` "pass 5": PR #166 Graphify spike merged, PR #179 continuity
canary merged, PR #248 ledger reconciliation merged, GovCon Decision 53 rung 1
delivered) — the spiral and real throughput coexisted on the same board at the
same time, which is itself diagnostic: duplicate-chasing work did not block
all product work, but it did consume a majority of issue volume (34 of the
last ~70 issues, roughly half) for zero net progress on the two stuck tasks.

---

## Section 2 — Root cause analysis (updated)

The 2026-09-03 RCA named seven root causes (RC1-RC7). Status of each as of
2026-09-04, checked against `DONE-LEDGER.md` and live repo/board state rather
than taken on claim:

| # | Root cause (2026-09-03 framing) | Status today | Evidence |
|---|---|---|---|
| RC1 | Recursive meta-work, no product goal above agents/rules/repos | **Partially fixed.** North star is now written once (`START.md`, `INTENT-AGGREGATE.md`) and cited as canon by all live repos. But Fusion board work is itself now meta-work-shaped again: SWARM-013/SWARM-098 chase infrastructure verification, not the AISDLC MVP or GovCon deliverable directly. | `DONE-LEDGER.md` pass 5 shows real product PRs merged same day as the spiral — so RC1 is contained, not solved; the containment is coincidental (other sessions worked the real board items) not structural. |
| RC2 | No single source of truth; everything cross-references everything | **Fixed at the doc layer, not at the runtime layer.** `START.md`/`HISTORIC-INDEX.md` collapsed the doc sprawl to one entry point, all 7 harness adapters verified to resolve the same absolute paths (`agent-configs` PR #75, `verify-cold-start.sh` exits 0). But the *task* layer now has a second source-of-truth problem: Fusion's `SWARM-*` board and GitHub Issues are two representations of the same work that can drift (a Fusion task re-seed writes a new GitHub issue; GitHub issue closure does not reliably clear Fusion task state — SWARM-013 is Done in neither system after 5+ hours). | Fusion task log for SWARM-013; issue count mismatch between "36 Todo" board rows and 30 open GitHub issues. |
| RC3 | No enforced work queue with exactly-one-owner and a WIP cap | **Not fixed. This is the proximate cause of the 2026-09-04 spiral.** "Max three active work threads" was stated as owner intent on 2026-08-28. No mechanism in Fusion, GitHub, or `agent-configs` enforces it. 9 tasks sit "In Progress" and 10 "In Review" simultaneously on one board today. | `fusion task list` output this session; `MIKE-INTENT-DEBRIEF` §3. |
| RC4 | Every agent can write everywhere, concurrently, and does | **Improved.** `scripts/check-branch-claim.sh` (govcon-factory) and `scripts/github-claim.mjs` (agent-sdlc PR #158) now exist as serialized-claim validators. `DONE-LEDGER.md` pass 4 (2026-09-04) documents 27 peer sessions on the shared `redtrades` login, several acting as controllers on one board, causing agent-sdlc #150-153 to be filed and closed by another session within 40 seconds — i.e. RC4 caused a live incident on 2026-09-04 itself, fixed same-day by making Symphony a persistent LaunchAgent (PR #155) rather than a per-session process. | `DONE-LEDGER.md` "2026-09-04 (pass 2)". |
| RC5 | Meta-work has no acceptance test, so it never ends | **Not fixed for the new failure shape.** "Format a GitHub reference" (RC5's original example) is done. But "verify GovCon evidence workflow integrity" — SWARM-098's task — has no acceptance test either: it is a verification task with no defined "verified" terminal state distinct from "keep re-checking." Ten near-duplicate issues exist because nothing defines what evidence would let an agent mark it done and stop. | 10 "GovCon evidence workflow" duplicate issue titles, this session's `gh issue list` count. |
| RC6 | Marathon sessions, no turn/wall-clock cap | **Unclear / likely still unfixed.** No evidence of a session-length hook in `agent-configs` hooks directory checked this session (not directly re-verified this pass — flagged as unverified, not claimed fixed). | Not independently re-checked this session; carry forward as open. |
| RC7 | "While I'm here" scope creep treated as free | **Structurally improved, behaviorally recurring.** `TASK.md` SCOPE discipline is now written into the global contract (`~/.claude/CLAUDE.md` "How to work" §, this document's own operating instructions). But the SWARM-013 re-seed pattern (three re-specifications in under an hour, each adding a new dependency rather than fixing the one blocker) is RC7's mechanism operating inside a single task rather than across a session — "while I'm here, let me also add this dependency" repeated by the scheduler/agent loop itself. | Fusion task log, SWARM-013. |

### New root cause named today: RC8 — silent credential/config gaps produce infinite re-diagnosis instead of one fix

Neither 2026-09-03 RC list named this explicitly, though RC5 gestures at it.
It deserves its own line because it is now the single largest driver of
duplicate-issue volume observed:

**RC8 — A missing credential or misconfigured reference (here: `GITHUB_TOKEN`
unset in Fusion; `workflow_id: "SWARM-098"` pointing at an unregistered
workflow) fails silently or ambiguously rather than raising a distinct,
actionable "blocked: operator action required" state. Every agent that
encounters the stall re-diagnoses from first principles, and — because the
board rewards closing an issue over fixing a shared blocker — files a new
issue naming the same root cause instead of correcting the one broken
reference.** This produced 34 of the last ~169 issues (20%) in under 4 days,
for zero forward progress on either underlying task. Severity: **high** —
directly measurable, directly reproducible (visible right now on the board),
and it is generic: any future missing secret, unregistered workflow, or
misconfigured integration will reproduce it exactly, because nothing detects
"N agents have independently filed a variant of this same diagnosis" or
"this task has failed identically K times" and halted new spawns.

### Severity ranking, today

| Root cause | Severity | Status |
|---|---|---|
| RC3 (no WIP cap) | **Critical** | Open, unenforced, proximate cause of both spirals |
| RC8 (silent credential/config gaps) | **Critical** | Open, newly named, actively producing duplicates right now |
| RC2 (N sources of truth) | High at task layer | Fixed at doc layer; open at Fusion/GitHub task-state layer |
| RC5 (no acceptance test for meta/verification work) | High | Open for verification-shaped tasks specifically |
| RC4 (uncontained concurrent writers) | Medium | Materially improved (persistent Symphony, claim scripts); residual risk from shared-login sessions remains |
| RC1 (recursive meta-work) | Medium | Contained by written north star; not structurally prevented |
| RC7 (scope creep as free) | Medium | Improved at session level; recurring at sub-task level |
| RC6 (marathon sessions) | Unknown | Not re-verified this pass |

---

## Section 3 — SOTA-grounded redesign

### 3.1 What current (2026) tooling and research say about this exact failure class

**Anthropic's own multi-agent research system** (engineering writeup,
retrieved 2026-09-04, anthropic.com/engineering/multi-agent-research-system)
hit this estate's exact failure mode during its own development and named the
fix. Early versions showed "agents creat[ing] 50 subagents for simple
queries" and, absent detailed task boundaries, subagents that "misinterpreted
the task or performed the exact same searches as other agents" — duplicate
work from underspecified delegation, structurally identical to SWARM-013's
repeated re-seeding. Their fix was not a smarter model; it was mechanical:
the lead agent must give each subagent "an objective, an output format,
guidance on the tools and sources to use, and clear task boundaries," combined
with explicit effort budgets scaled to task complexity ("simple fact-finding
requires just 1 agent with 3-10 tool calls; complex research might use more
than 10 subagents"). For state-loss risk they use checkpointing so a failure
resumes from a checkpoint rather than restarting from scratch — because
"minor system failures can be catastrophic for agents" once a task has run
for a while. This maps directly onto RC8: a checkpoint-and-resume discipline
with an explicit "blocked, awaiting operator" terminal state would have
stopped SWARM-013's three re-seeds cold.
(Source: Anthropic Engineering, "How we built our multi-agent research
system," retrieved 2026-09-04 via anthropic.com/engineering/multi-agent-research-system.)

**GitHub shipped native duplicate-issue detection in June 2026** — the exact
mechanism this estate is missing at the GitHub-issue layer. "Issue creation
now flags potential matches against existing issues in the repository as
issue details are being populated... up to three suggestions," in public
preview as of the changelog. **Correction (cross-family review):** this is a
*suggestion* surfaced to the person/agent filing the issue — it does not
block creation, so on its own it would not have stopped the 34 near-duplicate
issues filed today; it still requires the filer to notice and act on the
suggestion. The estate's own recommendation below (#2, an enforced
similarity check that blocks auto-creation above a threshold) is stronger
than GitHub's native feature and is the one actually needed here — GitHub's
feature is corroborating evidence that duplicate detection at creation time
is an emerging pattern, not a drop-in fix by itself.
(Source: GitHub Changelog, "Detecting Duplicate Issues - Public Preview and
issue fields MCP support for GitHub Issues," 2026-06-18, retrieved
2026-09-04, github.blog/changelog/2026-06-18-duplicate-detection-and-issue-fields-mcp-support-for-github-issues.)

**GitHub Copilot's coding agent** (GA in 2026, ~90% Fortune 100 adoption per
industry reporting) enforces the queue discipline structurally: it "accepts a
GitHub Issue as input, works independently in a... sandbox, and delivers a
pull request for human review," and splits backlog into "a
Copilot-delegatable pile and a human pile," never self-assigning or
commenting without explicit approval. **Correction (cross-family review):**
GitHub issues support up to ten assignees, so assignment alone is not an
exactly-one-owner mechanism the way this document originally implied —
Copilot's actual gate is that *it* only acts on issues explicitly delegated
to it, not that assignment itself prevents two agents working one issue. The
estate's own WIP=1 claim discipline (a single claim-comment marker per issue,
`scripts/github-claim.mjs`) is the real exactly-one-owner mechanism already
in place here; Copilot's delegate/don't-self-assign pattern is corroborating
evidence for explicit-delegation-over-self-assignment as a norm, not a
stronger primitive than what already exists.
(Source: aggregated 2026 reporting on GitHub Copilot coding agent, retrieved
2026-09-04; cross-checked against github.com/features/copilot.)

**Durable-execution engines (Temporal and peers) are the emerging 2026
pattern for exactly the "agent dies mid-task, must resume without loss"
requirement this estate wrote as its own founding goal.** "Temporal Workflows
automatically capture state at every step, and in the event of failure, can
pick up exactly where they left off. No lost progress, no orphaned processes,
and no manual recovery required" — the replay-from-event-history model
(schedule/start/complete events, deterministic replay skipping completed
steps) is a stronger version of what Fusion's task-log-and-checkpoint model is
reaching for by hand. Industry commentary specifically ties 2026 agent
platforms to this pattern: "The agents shipping in 2026 run for hours, pause
for a human approval that lands the next morning, resume from a crash with
the same tool-call history." Notably, Mistral's May-2026 "Workflows" product
explicitly built on Temporal-powered orchestration, evidence this is
converging as a default rather than a niche choice.
(Sources: Temporal.io product pages, retrieved 2026-09-04; Reactify
Solutions, "Durable AI agents in 2026," retrieved 2026-09-04; Olmec Dynamics,
"Temporal and the 2026 Shift to Durable Agentic Workflows," retrieved
2026-09-04.)

**Multi-agent swarm production data (2026) confirms the WIP/population-cap
requirement generically, not just for this estate.** Aggregated 2026 industry
coverage on multi-agent orchestration patterns states plainly that "swarm
patterns... require population-size caps to prevent runaway spawn," and that
"40% of multi-agent pilots fail within six months of production deployment" —
with reconciling contradictory concurrent output flagged as needing "a
dedicated aggregator... a synthesis step is usually required before the swarm
output is usable." This corroborates RC3/RC4 as a known, common failure class,
not an estate-specific pathology.
(Source: aggregated 2026 multi-agent orchestration pattern coverage, retrieved
2026-09-04 — treat as directional industry consensus rather than a single
citable authority; the concrete, sourced fixes above (Anthropic, GitHub,
Temporal) are the load-bearing citations for the redesign below.)

### 3.2 What to keep

- **GitHub Issues as the queue, `govcon-reviewer-bot` as independent review,
  exact-head merge, WIP=1 per session.** This is the correct, already-proven
  design — the Goal B canary (#119/PR #120) demonstrates it works end to end
  when followed. The problem is not the SDLC contract; it is the absence of
  mechanical enforcement around it.
- **Fusion as control plane.** It is the right shape (task graph, dependency
  tracking, checkpoint log per task) and it is already deployed and partially
  working (real PRs merged same day as the spiral). Replacing it would repeat
  attempts 1-3's mistake of restarting instead of fixing.
- **The worker pool** — Jules, Codex, Claude, Grok, Hermes/OpenCode via
  FreeLLMAPI — and its documented failover order (`rules/provider-pool.md`).
  This is sound and matches the industry pattern of a curated, verified model
  roster rather than an exhaustive one (the estate's own memory notes free
  tiers "decay constantly and silently" — this is a correctly-learned lesson,
  keep it).
- **The tiered/risk-adaptive merge-authority policy (D-006)** — blast-radius-based
  rather than path-based, matches how GitHub's own Copilot agent and Temporal-based
  systems separate "agent may commit" from "human must approve" by consequence,
  not by location.

### 3.3 What to cut

- **`agent-platform`, `agent-mesh`, `agent-workspace` as anything but read-only
  evidence.** Already frozen; keep frozen. Do not let any future session
  "revive" one for a plausible-sounding reason without an explicit owner
  decision, per existing `ANTI-PATTERNS.md` item 14.
- **Verification-shaped meta-tasks with no defined terminal state** — SWARM-098's
  shape ("verify X integrity and completeness") should not exist as an
  open-ended task type at all. Every task admitted to the board must carry a
  falsifiable acceptance test at creation time (see 3.4).
- **The Fusion re-seed-on-stall behavior as currently configured.** Re-seeding
  a task that has failed identically more than once should not spawn a new
  investigation; it should halt and surface, per the Anthropic checkpoint
  pattern and per RC8's fix below.
- **Any further "collapse to N repos" or "canonical decision" documents until
  goal #1 (one real swarm issue-to-merge cycle, no human touch, in 30 days
  from the 2026-09-03 RCA) is met or explicitly re-scoped by Mike.** This
  document is itself meta-work; it should be the last one until that test is
  met, exactly as the prior RCA said and was not honored for even 24 hours.

### 3.4 Concrete guardrails — what actually prevents recurrence

Each guardrail below is scoped to be buildable as one bounded `agent-sdlc`
issue, matching the estate's own "smallest runnable slice" discipline. None of
these require replacing Fusion or GitHub Issues.

1. **WIP cap, mechanically enforced, not just written.** Add a pre-claim check
   (extending `scripts/github-claim.mjs`, agent-sdlc PR #158) that refuses a
   new claim if the claiming identity (or the shared board) already has ≥3
   issues in `in-progress`/`in-review` state. This is literally the
   `MIKE-INTENT-DEBRIEF` "max three active threads" instruction from
   2026-08-28, finally made mechanical instead of advisory. Cheapest single
   fix with the highest leverage against RC3.

2. **Duplicate-issue circuit breaker at creation time**, mirroring GitHub's
   own June-2026 duplicate-detection feature: before a new issue is filed,
   require a title/body similarity check against open issues (a cheap
   embedding or even substring/fuzzy match against the last 50 open issues is
   sufficient at this volume) and block auto-creation above a similarity
   threshold, surfacing "possible duplicate of #N, comment there instead" the
   way GitHub's native feature does inline. This single check would have
   stopped 34 of the last 169 issues from ever being filed.

3. **A distinct "blocked: credential/config gap, operator action required"
   task state, separate from "failed, retry."** SWARM-013's actual state
   (missing `GITHUB_TOKEN`) and SWARM-098's actual state (unregistered
   `workflow_id`) are both one-line, operator-only fixes. Neither should be
   re-diagnosable by an agent; both should halt the task, tag it distinctly,
   and stop the scheduler from re-seeding dependents until the specific named
   blocker clears. This is the Anthropic checkpoint-and-resume pattern applied
   to config gaps specifically — "minor system failures can be catastrophic
   for agents" becomes tractable only if the system can tell the difference
   between "retry this" and "a human must act once." Concretely: wire
   `GITHUB_TOKEN` into Fusion's `tokenStrategy` now (the specific fix for
   today's spiral) and add the state distinction as the durable fix for the
   next one.

4. **Identical-failure counter with an automatic freeze, not a human noticing
   it.** If a task fails at the same graph node (`parse`,
   `missing-implementation-steps`, etc.) more than twice, stop spawning
   variants of it and instead open exactly one "root-cause: node X failing
   repeatedly" issue, then block further child-task creation until that one
   issue closes. This directly targets RC8's "N agents independently
   re-diagnose the same stall" pattern and matches the industry-standard
   "aggregator/synthesis step" requirement for swarm output, applied here to
   failure diagnosis rather than research synthesis.

5. **Meta-work freeze with a mechanical trigger, not a written promise.**
   The 2026-09-03 RCA's "freeze the meta layer for 30 days" was words on a
   page and lasted under 24 hours. Make it mechanical: any PR touching
   `AGENTS.md`, `rules/`, `DECISIONS.md`, or `00-start-here/` outside the
   `agent-configs`/`agent-knowledge-archive` repos' own explicitly-scoped
   maintenance issues gets an automatic `needs-mike` label and is excluded
   from agent auto-merge, regardless of its Class-A/B self-assessment. This
   converts "the freeze was not held" from a discipline failure into a
   structural one.

6. **A single per-task acceptance test recorded at admission, not
   discovered later.** No task enters the board (Fusion or GitHub) without a
   one-line falsifiable done-condition in its own description — matching the
   estate's own `TASK.md` DONE-WHEN convention but applied at the board layer,
   not just the session layer. "Verify GovCon evidence workflow integrity"
   is not admissible as written; "confirm steps 1-9 of pipeline X each have a
   matching artifact and approval record in commit Y, or list the exact
   missing ones" is.

7. **Identity separation for the shared `redtrades` login.** DONE-LEDGER
   already names this (27 concurrent sessions, one login, one session closing
   another's issues in 40 seconds) as a live incident, fixed ad hoc via
   persistent Symphony. The durable fix — distinct bot identities or PAT
   scopes per harness (Jules-bot, Codex-bot, Claude-bot) rather than one
   shared human login every agent authenticates as — is a known, generally
   available GitHub mechanism (the same App-identity pattern already used for
   `govcon-reviewer-bot` to get around GitHub's same-account APPROVE
   restriction) and should be extended to authorship, not just review.

### 3.5 What this buys, concretely

Guardrails 1-4 target RC3 and RC8 specifically — the two root causes that
produced both documented spirals and are, on today's evidence, still fully
open. They are each small (a pre-claim script check, a similarity check on
issue creation, one new task state, one failure counter) and fit inside the
estate's own "smallest runnable slice" rule rather than proposing a platform
rewrite — consistent with what has actually worked here before (Goal B canary,
the seven-adapter cold-start fix) and inconsistent with what has repeatedly
failed (five successive "clean, first-principles" reboots that never shipped
a full cycle).

---

## Appendix — sources for Section 3 claims

| Claim | Source | Retrieved |
|---|---|---|
| Anthropic multi-agent research system architecture, failure modes (runaway spawning, duplicate work, checkpoint/resume) | anthropic.com/engineering/multi-agent-research-system | 2026-09-04 |
| GitHub native duplicate-issue detection, public preview | github.blog/changelog/2026-06-18-duplicate-detection-and-issue-fields-mcp-support-for-github-issues | 2026-09-04 |
| GitHub Copilot coding agent GA, queue/assignment discipline | aggregated 2026 reporting; github.com/features/copilot | 2026-09-04 |
| Temporal durable execution pattern for long-running agent workflows | temporal.io; reactify-solutions.com/articles/durable-ai-agents-2026; olmecdynamics.com/news/temporal-durable-execution-agentic-workflows-2026 | 2026-09-04 |
| Multi-agent swarm population caps, 40% pilot failure rate, aggregator requirement | aggregated 2026 multi-agent orchestration pattern coverage (directional, not single-source) | 2026-09-04 |

## Appendix — primary-evidence sources for Sections 1-2 (this estate)

- `20260903-death-spiral-rca.md` (extended, not duplicated, by this document)
- `00-start-here/START.md`, `INTENT-AGGREGATE.md`, `20260831-current-intent-decisions.md`, `HISTORIC-INDEX.md`, `DONE-LEDGER.md`, `ANTI-PATTERNS.md`, `WHOLE-STORY.md`
- `agent-configs/MASTER-GUIDE.md`, `AGENTS.md`, `rules/provider-pool.md`
- `agent-configs` `6850fa3:knowledge/MIKE-INTENT-DEBRIEF-2026-08-28.md`
- `gh issue list --repo redtrades/agent-sdlc --state all --limit 300` and `gh pr list ... --state merged` (run this session, 2026-09-04)
- `fusion task list` / `fusion task show SWARM-013` / `fusion task show SWARM-098` (run this session)
- `/Users/man/.fusion/settings.json` (read this session — `"github": false`, `"tokenStrategy":{"token":null}`)
- `agent-platform/README.md`, `agent-mesh/README.md`, `agent-workspace/README.md` (read this session)
