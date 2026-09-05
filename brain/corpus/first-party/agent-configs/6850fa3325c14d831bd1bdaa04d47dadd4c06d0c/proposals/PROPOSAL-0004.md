---
id: "PROPOSAL-0004"
title: "Promote the handoff record from convention to a checked artifact"
target: "rules/session-continuity.md (amend) + prompts/handoff-record-template.md (new) + scripts/check-handoff.sh (new) + .github/workflows/handoff-check.yml (new)"
proposer: "agent:claude-opus-5-cowork-2026-08-28"
status: "open"
date: "2026-08-28"
decision: null
---

## Insight

`rules/session-continuity.md` already contains the correct design. It was written
2026-08-25 for this exact trigger, it correctly rejects end-of-session summaries
because "a session that dies never gets to write its summary," and it correctly
reuses existing surfaces per `rules/no-parallel-infrastructure.md`.

It has never fired, because nothing makes it fire, and because it is not on
`main`.

**The same design has now been independently derived five times on this machine
and enforced zero times.** Full evidence in
`knowledge/multi-agent-handoff-research-2026-08-28.md` §2:

| Where | Status |
|---|---|
| `agent-configs/rules/session-continuity.md` | Not on `main`; branch `work/session-continuity-issue-16-clean`. Self-declared "Not mechanically enforced anywhere yet" |
| `agent-mesh/.agent/protocols/issue-as-spine.md` | Committed, no check |
| `agent-mesh/.agent/protocols/memory-write-discipline.md` | Committed, no check |
| `agent-mesh/AGENTS.md` "an unlogged change did not happen" | Committed, no check |
| `agent-mesh/Agent SDLC.md` | **Uncommitted draft**, referenced by nothing |

Writing it a sixth time is the one intervention guaranteed not to work.

**Violation count, which is what this proposal turns on.** `rules/DONT.md`
promotes a written rule at 2+ logged violations. `silent-long-running-work`
currently shows one dated 2026-08-25 incident covering three sessions. Since then:

- **2026-08-28, four more.** Three sessions died on usage limits mid-task, one
  stalled indefinitely on an unanswered approval prompt. Recoverable only because
  someone checked. Two had written a file just before dying, and that was the
  difference between recoverable and lost. **None of the four is in
  `log/CORRECTIONS.log`**, whose last entry is 2026-08-26, so the promotion loop
  cannot currently see them (filed as F-1 in the report).
- **The undocumented-qualifier variant, four instances across two repos.** A
  42-of-42-gates claim propagated through `govcon-factory` for days and was quoted
  as fact by multiple agents when it belonged to a different pipeline
  (Mike-reported, §9.7 unverified by me). Plus three verified in `agent-mesh`'s own
  ledger: D-032 supersedes "D-030/D-031's false identity claim" and every
  conclusion downstream of it; D-027 supersedes "only D-026's scheduler-tuning
  claim" where the measurement was real and the attribution was not; D-029
  supersedes D-028's enablement clause.

Two independent failure families, both past the threshold, both currently
unenforced.

## Proposed change

Four parts. Parts 2 and 3 are the substance; part 1 is a rule amendment; part 4
is the gate.

### 1. Amend `rules/session-continuity.md`

Not a new rule. The existing rule keeps its per-turn `STATUS` block unchanged and
gains a fuller record at one specific moment. **Proposed diff, against the file as
it exists on `work/session-continuity-issue-16-clean`:**

```diff
@@ Per-turn status (every session) @@
 STATUS: <issue/task id, or a short label if there is none>
 STATE: <in progress | blocked | done | handed off>
 NEXT: <the next concrete action>
 BLOCKED-ON: <none, or the specific blocker>
 ```

 This replaces silent long-running work with a check anyone can make on
 the issue itself: either there is a recent status, or there has not been
 a major turn since the last one, and the timeline says which.

+## The handoff record
+
+The four-line block above is a liveness signal. It is not a handoff: it carries
+no order of events, no reasoning behind a decision, no record of what was tried
+and rejected, and no working-tree state. A successor reading only that block
+knows what to do next and not why, so it re-litigates settled calls.
+
+At a handoff, and at every state transition during work, the same session also
+maintains `HANDOFF.md` at the root of its working branch, committed and pushed,
+with the same text posted to the tracked issue inside the `HANDOFF BEGIN` /
+`HANDOFF END` sentinels. Format and worked example:
+`prompts/handoff-record-template.md`. Six required fields: `BASE-SHA`,
+`LAST-KNOWN-GOOD`, `PHASE` with `EXPECTED-UNTIL`, `HANDOFF-COUNT`, `TREE`,
+`DONE` with a verifying command per line, plus `BOUNDARY` whenever `DONE` states
+a number and `UNVERIFIED` whenever `DONE` is non-empty.
+
+**Write it at state transitions, never on a timer.** A timer fires mid-thought
+and writes a snapshot of confusion, which the next session inherits as if it were
+a decision. The transitions are the same "major turn" list above.
+
+**The property this has to satisfy:** at any instant, an abrupt stop leaves a
+recoverable record with no further action by the agent. That is a property of the
+file on disk right now, not of a shutdown ritual. On 2026-08-28, two of four lost
+sessions were recoverable for exactly this reason and two were not.
+
+**A number is reported with what it does not establish.** `BOUNDARY` is not
+optional politeness; it is the countermeasure to a qualified result becoming an
+unqualified fact downstream. Four logged instances of that failure across two
+repos are cited in `proposals/PROPOSAL-0004.md`.
+
@@ Resume protocol @@
-1. Read the log first: issue comments, or the task file / `STATUS.md`
-   body. This gives a claimed state, not a verified one.
+1. Read `HANDOFF.md` on the branch first, because it is the only copy guaranteed
+   to sit at the same commit as the code it describes. If absent, fall back to
+   issue comments, then the task file / `STATUS.md` body, and say so in your
+   first status. This gives a claimed state, not a verified one.
+1a. Compare `BASE-SHA` to current `origin/main`. If they differ, treat every path
+   and line reference in the record as suspect until checked.
+1b. Check `PHASE` and `EXPECTED-UNTIL`. If the phase is `blocked-on-human`,
+   `waiting-approval` or `running-external` and `EXPECTED-UNTIL` has not passed,
+   **do not take over**: the prior session may be alive and holding state.
+   Escalate instead. A session stalled on an approval prompt is silent in exactly
+   the way a dead one is, and a reaper cannot tell them apart without this field.
+1c. Read `BOUNDARY`, `DO-NOT` and `REJECTED` before proposing anything.
 2. Verify the claim against the actual repo before trusting it. [unchanged]
 3. Re-claim through the existing mechanism, not by working around it. [unchanged]

@@ Enforcement @@
+A third mechanism, repo-side and vendor-neutral, is proposed in
+`proposals/PROPOSAL-0004.md`: `scripts/check-handoff.sh` plus a pre-push hook and
+a CI workflow. The two stale-claim fixes described above remain necessary and are
+not superseded by it.
```

### 2. New: `prompts/handoff-record-template.md`

Already written and staged, banner-marked PROPOSED, inert until this proposal is
accepted. It reconciles six existing formats and gives per-field provenance so
nothing in it reads as invented. Placed in `prompts/` because that directory
already holds `fork-summary-handoff-template.md`, and the two are explicitly
cross-referenced as complementary rather than merged.

### 3. New: `scripts/check-handoff.sh`

Pure shell plus `git`, no dependencies, so it runs identically under Claude Code,
Codex, Gemini CLI and Grok Build, and in CI. Exit 1 with a specific message when:

| Check | Rationale |
|---|---|
| `HANDOFF.md` missing on a `work/*` branch with commits | the base case |
| `BASE-SHA` or `LAST-KNOWN-GOOD` names a commit not in the repo | catches a rotted or fabricated record |
| `PHASE` present without a parseable `EXPECTED-UNTIL` | the stalled-versus-dead distinction |
| `STOP-REASON` outside its enum | typos silently defeat any downstream filter |
| `HANDOFF-COUNT` absent, or >= 3 without a `needs-mike` label | stops handoff ping-pong |
| any `DONE` line without a verifying command | `rules/verification-law.md`, applied to a reader who cannot ask |
| `UNVERIFIED` absent while `DONE` is non-empty | forces the facts/beliefs split |
| **`BOUNDARY` absent while `DONE` contains a numeric claim** | **the 42-of-42 check** |

Build the last one first. It converts a four-instance failure class into a gate.

### 4. New: `.github/workflows/handoff-check.yml` and `scripts/hooks/pre-push`

`agent-configs` has no `.github/` directory at all, so this is also where it gets
CI. Model the workflow on `govcon-factory`'s `check-decisions-entry.sh`, already
proven to block a PR for a missing companion entry.

The `pre-push` hook refuses a push to a `work/*` branch whose tip is more than N
commits ahead of the last commit touching `HANDOFF.md`, unless the push is a
single WIP commit. **This is the part that makes the record never more than one
state transition stale**, which is the property in part 1, enforced rather than
requested. Suggest N=3 initially and tune on real data.

**Vendor hooks as a rung above, not the mechanism.** Claude Code fires
`StopFailure` with a matcher on error type whose documented values include
`rate_limit` (https://code.claude.com/docs/en/hooks, accessed 2026-08-28), and
Grok Build has the same event and reads `.claude/settings.json` hook files
(https://docs.x.ai/build/features/hooks, accessed 2026-08-28), so one hook file
covers two harnesses and can write a machine-generated stub at the moment of a
quota stop. Codex and Gemini CLI expose no rate-limit-typed event. Two of four,
which is why the repo-side check is the enforcement and the hook is the
accelerator.

## Rationale

Why a mechanical enforcer instead of leaving this written-rule-only, in this
repo's own terms:

1. **The rule already exists and has never fired.** Five derivations, zero
   enforcement. A sixth sentence is the one intervention with a known failure
   record.
2. **`rules/DONT.md`'s promotion threshold is 2.** `silent-long-running-work` is
   at four incidents on 2026-08-28 alone, plus the 2026-08-25 entry. The
   undocumented-qualifier family is at four across two repos. Both are past it.
3. **Evidence about which practices survive.** The report's §10.2 measured this
   directly across both repos: every practice that survived contact with real work
   had a mechanical consequence, and the one voluntary practice that held
   (`BOUNDARY`) held because it costs one clause inside the sentence making the
   claim. Everything requiring a second write to a second file failed, including
   `agent-mesh`'s own worklog rule, which was violated by the very document
   prescribing worklog discipline (F-14). That is not a reason for more exhortation;
   it is the reason the required field set is six and the check is cheap.
4. **This is the `rubric-improve` pattern**: a recurring judgment call becomes a
   mechanical gate. Same pattern `MASTER-GUIDE.md` §6 already names.

**Not proposed, deliberately:** a session-start lock hook. `PROPOSAL-0001` proposed
one and `DECISIONS.md` D-005 records Mike converted it to a convention. Re-proposing
would re-litigate a settled call. Also not proposed: a fourth state store such as
`CURRENT_STATE.json`, rejected on `rules/no-parallel-infrastructure.md`; and
wholesale adoption of an external protocol, rejected as unverified and because it
does not address the binding constraint, which is compliance rather than format.
Both rejections are adjudicated in the report §10.4.

## Evidence

- `log/CORRECTIONS.log` 2026-08-25 `rule=session-freshness.md` and the
  `silent-long-running-work` row in `rules/DONT.md` on
  `work/session-continuity-issue-16-clean`
- 2026-08-28, four incidents, Mike-reported, **not yet in `log/CORRECTIONS.log`**;
  logging them is prerequisite F-1 and is what formally crosses the threshold
- `agent-mesh/DECISIONS.md` D-027, D-029, D-032, three verified instances of the
  undocumented-qualifier class in one repo's own ledger
- `log/CORRECTIONS.log` 2026-08-26 `never-measured-reported-as-measured`: "a
  confident false statement is WORSE ... because None is visibly broken and prose
  is not"
- `log/CORRECTIONS.log` 2026-08-25 vanished-worktree entry: "commit early/often
  even mid-implementation ... a worktree alone didn't protect against this
  machine's own automation"
- `log/CORRECTIONS.log` 2026-08-26: PR #282 merged at 03:46:45Z, PR #288 opened
  seventeen seconds later on the same join point, establishing that a claim lock
  cannot catch code-level collisions
- Full research, sourcing and adjudication:
  `knowledge/multi-agent-handoff-research-2026-08-28.md`

## Dependencies

**This proposal cannot be implemented until `work/session-continuity-issue-16-clean`
is merged.** It amends a file that is not on `main`. That merge is Tier 2 under
`DECISIONS.md` D-001 and is Mike's alone. Filed as F-2 and R-1 in the report, and
it is the highest-leverage action available, because every other enforcement
proposal here is downstream of it.

Related but deliberately **out of scope**, recommended as its own proposal (F-8,
R-3): shared-live-state discipline covering the Hermes and OpenCode config damage
of 2026-08-27. Tool-owned config edited through the owning tool's interface rather
than whole-file rewrite, a read-diff-write-verify cycle, and a lease for shared
state outside any repo. Different failure, different fix; folding it in here would
repeat the parallel-infrastructure mistake in reverse.

---

## Decision (filled in by whoever accepts or rejects this)

- **Outcome:** accept | reject
- **If accepted:** commit hash applying the change, referencing this proposal's id.
- **If rejected:** reason. Moves to `proposals/rejected/` unchanged except this
  section, a recorded outcome rather than a deletion, so the next pass does not
  re-litigate it.

**An agent never accepts its own proposal.** This one is Tier 2 regardless, since
it amends a file under `rules/`.
