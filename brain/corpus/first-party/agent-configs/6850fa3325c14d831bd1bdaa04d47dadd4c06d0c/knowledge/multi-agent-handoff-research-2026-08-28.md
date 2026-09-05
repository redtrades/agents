# Sequential multi-agent handoff: research, findings, and proposed design

Date: 2026-08-28
Scope: how a stopping agent hands work to a different agent, possibly from a
different vendor, without losing the order of events, the decisions and their
reasoning, the state of the working tree, or the next action.
Trigger: Claude Code, Codex, Grok and Gemini each hit usage limits mid-task on
this machine. Four times on 2026-08-28 alone.

**This report is analysis, not a build.** It proposes one amendment to an
existing rule, one new template, and two enforcement mechanisms. It modifies no
file under `rules/`. The proposed diff is `proposals/PROPOSAL-0004.md`.

**It is also a synthesis, not a competing proposal.** `~/agent-mesh/Agent SDLC.md`
is a peer analysis of the same question, produced by other models. §10 adjudicates
it against this research point by point, records what was adopted and what was
rejected with evidence, and lists what remains for Mike to decide. Where the two
agree independently, that agreement carried the most weight in §8.

Every external claim carries a URL and an access date. §9 lists what could not be
verified. §8 is a findings register of everything contradictory, stale or broken
found along the way, with file, line, evidence, correction and recommendation.

---

## 1. Method

Local state was read directly. In `~/agent-configs`: `MASTER-GUIDE.md`, every
file under `rules/`, `log/CORRECTIONS.log`, `DECISIONS.md`, all of `proposals/`,
`prompts/fork-summary-handoff-template.md`, and the prior
`knowledge/agent-sdlc-gap-analysis-2026-08-26.md`. Branch state was read with
`git branch -a`, `git diff main...<branch>` and `git show <branch>:<path>`,
because several relevant rules are not on `main`.

In `~/agent-mesh`, confirmed by Mike as his and intended: `AGENTS.md`,
`HANDOFF.md`, `WORKLOG.md`, `DECISIONS.md`, `README.md`, `Agent SDLC.md`,
`.agent/protocols/*`, and `git log`/`git status`.

External research used sources fetched on 2026-08-28, weighted toward vendor
documentation and preprint work over blog summaries.

---

## 2. The finding that changes the shape of the answer

I expected to find a gap in the design. There is no gap in the design. **The
design has been independently derived five times on this machine, and enforced
zero times.**

| Where | What it already says | Status |
|---|---|---|
| `agent-configs/rules/session-continuity.md` | Externalize state continuously, not as an end-of-session summary, because "a session that dies never gets to write its summary" | Written 2026-08-25. **Not on `main`.** Lives on branch `work/session-continuity-issue-16-clean`. Self-declared "Not mechanically enforced anywhere yet" |
| `agent-mesh/.agent/protocols/issue-as-spine.md` | A `HANDOFF BEGIN`/`HANDOFF END` block with Context, Changed, Verified, Next, Gotchas. Five same-turn writes. "An unlogged change did not happen. A change logged an hour later is a reconstruction, not a record" | Committed. No check |
| `agent-mesh/.agent/protocols/memory-write-discipline.md` | "A correction received from the human lands in the store in the same turn it was given, while the context that explains it still exists. Waiting for session end loses the why" | Committed. No check |
| `agent-mesh/AGENTS.md` | "Append to `WORKLOG.md` at every milestone (what, where, evidence). The worklog is the continuity mechanism — an unlogged change did not happen" | Committed. No check |
| `agent-mesh/Agent SDLC.md` | 1,831 lines of multi-model research reaching "handoff-first, file-and-git as the source of truth," with a nine-field handoff schema and a quota-switch ritual | **Untracked in git** (`git status` shows `?? "Agent SDLC.md"`). Invisible to any agent that clones the repo |

Five derivations. Four of them say the same thing in different words. None of
them fires when an agent skips the step.

That reframes the deliverable. The valuable work is not another handoff format.
It is (a) reconciling five formats into one, (b) adding the two fields all five
are missing, and (c) building the check. Mike's standing rule applies with force
here: a rule violated twice becomes a hook or a check, not a louder sentence.
This one has been written five times and violated at least seven.

---

## 3. What exists, audited

### 3.1 What works

**`agent-configs`: the correction and promotion loop.** `log/CORRECTIONS.log`
carries 20+ dated entries with real forensic detail, `rules/DONT.md` counts them
per row, and `scripts/consolidate-corrections.sh` auto-files a promotion proposal
at two violations. That loop is why this report can cite dated local incidents
rather than gesture at them.

**`agent-configs`: the rule surface itself.** `rules/verification-law.md`'s Iron
Law ("NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE"),
`rules/no-parallel-infrastructure.md`, `rules/hygiene.md`,
`rules/session-freshness.md`. These are good rules, written from real incidents,
with provenance.

**`agent-mesh`: the qualifier discipline, in live use.** This is the strongest
working practice found anywhere in either repo, and it is the direct antidote to
the 42-of-42-gates failure. `agent-mesh` writes explicit boundary statements on
its own claims. Verbatim from `WORKLOG.md`:

> **Boundary**: This validates candidate throughput length only. Semantic
> correctness, tool/JSON/multi-turn behavior, prefix/restart persistence,
> 30-minute soak, 64K/128K/262K, Q4, concurrency, and Hermes remain blocked.

and from `HANDOFF.md`:

> This tracking availability is not a model-promotion claim.

and

> **27B OMLX control, not exact Flash-Next**

That is a qualifier attached to the claim, in the same artifact, at the same
time. It is exactly what did not happen with the 42-of-42 claim. `agent-mesh`
solved this and nobody generalized it.

**`agent-mesh`: supersede-never-rewrite.** `DECISIONS.md` header: "Never rewrite
history; supersede explicitly." D-019, D-020, D-027, D-029 and D-032 are all
explicit supersede entries that name what they overturn and what survives. D-027
is a model of the form: it supersedes *only* D-026's scheduler-tuning claim,
states that "the observed 89.2-91.2 tok/s cell remains a workload measurement but
cannot be attributed to operator tuning of those fields," and leaves the rest of
D-026 standing.

**`govcon-factory`, one repo over: the concurrency primitives.** Per
`MASTER-GUIDE.md` §2 and §5, `scripts/issue-claim.sh` writes to a dedicated
`claims` branch and uses git's non-fast-forward rejection as a mutex, plus
leases, a stale-claim reaper, worktree hygiene, CI on a self-hosted runner, a
reviewer-bot App identity, and a mechanized tiered merge. Proven on live races.

### 3.2 What is missing

**A cold-start artifact that carries reasoning.** Compare the five existing
formats against what Mike's brief requires:

| Requirement | session-continuity `STATUS` | issue-as-spine `HANDOFF` | agent-mesh `WORKLOG` | `Agent SDLC.md` schema |
|---|---|---|---|---|
| Order of events | no | no | yes, by append | no |
| What is done | no | partial (`Changed`) | yes (`What`) | yes (4, 5) |
| Decisions | no | no | via `DECISIONS.md` | partial (6) |
| **Reasoning behind decisions** | no | no | via `DECISIONS.md` rationale column | no |
| **What was tried and rejected** | no | no | no | no |
| Working-tree state | no | no | no | partial (3) |
| Precise next action | yes (`NEXT`) | yes (`Next`) | no | yes (7) |
| Verification evidence | no | yes (`Verified`) | yes (`Evidence`) | yes (5) |
| **Qualifier on the claim** | no | no | **yes (`Boundary`)** | no |
| Stop reason | no | no | no | yes (9) |

Two columns are empty across all five: **what was tried and rejected**, and
**working-tree state**. Those are precisely the two things a successor cannot
reconstruct from git. Git shows what landed, never what was abandoned and why.

**No enforcement anywhere, in either repo.** `agent-configs` has no `.github/`
directory at all, so no CI, no required check, no auto-merge. `agent-mesh` has no
`.github/workflows/` either (checked). Every continuity claim in both repos rests
on an agent choosing to comply.

**No coordination between the two systems.** See §6.4.

### 3.3 What is written but not enforced, and what is not even merged

| Artifact | Believed status | Actual status, 2026-08-28 |
|---|---|---|
| `rules/session-continuity.md` | "in place" | **Not on `main`.** Branch `work/session-continuity-issue-16-clean` only |
| `rules/worktree-protocol.md` | Active per D-005 | **Not on `main`.** Same branch |
| `rules/review-independence.md` | Active per D-003 | **Not on `main`.** Same branch |
| `rules/model-routing.md` | Active per D-004 | **Not on `main`.** Same branch |
| `DECISIONS.md` D-002..D-005 | Recorded | **Not on `main`.** `main` stops at D-001 |
| `rules/session-freshness.md` | On `main` | Self-declared not mechanically enforced |
| `rules/no-parallel-infrastructure.md` | On `main` | No check exists |
| `MASTER-GUIDE.md` §5 reaper schedules | "2-hourly", "6-hourly" | Not scheduled. `session-continuity.md` records that `launchctl`, `crontab` and every LaunchAgent plist were checked directly and none references it |
| `proposals/PROPOSAL-0001.md` | `status: open` | D-005 (unmerged) records Mike ruled on it |
| `scripts/consolidate-corrections.sh` | Auto-escalates | D-005 records its skip check matches a proposal's existence, not its `status`, so escalation for `shared-working-directory-concurrent-checkout` has been off since 2026-08-24 |

The structural consequence: **the rule Mike believes is in force is a rule no
agent loads**, because no agent reads an unmerged branch. And the reason it is
unmerged is the Tier 2 policy in `DECISIONS.md` D-001, which reserves anything
under `rules/` to Mike's personal merge. The safety rail is the bottleneck. This
is the same conclusion gap 4 of `knowledge/agent-sdlc-gap-analysis-2026-08-26.md`
reached about incident #141 recovery.

---

## 4. Field research

### 4.1 AGENTS.md: real convention, partial coverage

`AGENTS.md` is plain Markdown at a repo root, described by its own site as "a
README for agents," claimed to be used by over 60k open-source projects, and now
stewarded by the Agentic AI Foundation under the Linux Foundation. Agents read
the nearest file in the directory tree and the closest one takes precedence.
(https://agents.md/, accessed 2026-08-28)

Coverage across Mike's four harnesses, from each vendor's own documentation:

| Harness | Reads by default | AGENTS.md | Size behaviour |
|---|---|---|---|
| **Claude Code** | `CLAUDE.md`, `CLAUDE.local.md`, `.claude/rules/*.md` | **Not natively.** Docs: "Claude Code reads `CLAUDE.md`, not `AGENTS.md`." Prescribed bridges: `@AGENTS.md` import, or `ln -s AGENTS.md CLAUDE.md` | Loads up to 4 MiB, skips larger, recommends under 200 lines |
| **Codex** | `AGENTS.override.md`, then `AGENTS.md`, then configured fallbacks, global then root then cwd | Native, primary format | Stops adding files at `project_doc_max_bytes`, **default 32 KiB**, then truncates |
| **Gemini CLI** | `GEMINI.md` global, workspace, and just-in-time on tool access | **Only if configured**: `"context": {"fileName": ["AGENTS.md", ...]}` in `settings.json` | Not documented as capped |
| **Grok Build** | `AGENTS.md`, `Agents.md`, `AGENT.md`, `CLAUDE.md`, `Claude.md`, `CLAUDE.local.md`, plus `.grok/rules/`, `.claude/rules/`, `.cursor/rules/` | Native, most permissive of the four | "Files are loaded in full, with no size cap" |

Sources: https://code.claude.com/docs/en/memory ;
https://learn.chatgpt.com/codex/agent-configuration/agents-md ;
`docs/cli/gemini-md.md` at `google-gemini/gemini-cli` `main` ;
https://docs.x.ai/build/features/project-rules . All accessed 2026-08-28.

Two operational consequences. Grok reading `CLAUDE.md` and `.claude/rules/`
natively means the existing Claude-shaped rule surface is already visible to one
of the three non-Claude harnesses at no cost. And Codex's 32 KiB cap means the
portable instruction file must stay small: the handoff **pointer** belongs in
`AGENTS.md`, the handoff **content** does not.

### 4.2 Spec-driven development and spec-kit

GitHub's `spec-kit` reached 1.0.0 and advertises 30+ agent integrations. The flow
is `/speckit-constitution` once, then specify, plan, tasks, implement, converge,
with durable artifacts in the repo: `constitution.md`, `spec.md`, `plan.md`, and
a `tasks.md` whose checkbox state is the progress record with explicit
`**Checkpoint**` lines between phases. `templates/commands/implement.md`
instructs the agent to mark each task `[X]` on completion. A separate command,
`taskstoissues.md`, converts `tasks.md` into dependency-ordered GitHub issues via
the GitHub MCP server. (https://github.com/github/spec-kit, cloned and read at
`main` on 2026-08-28)

What it solves: durable, agent-agnostic intent and progress state in the repo.
What it does not solve: the mid-task stop. Its `handoffs:` frontmatter key in
`clarify.md`, `constitution.md`, `specify.md`, `plan.md` and `tasks.md` chains
one speckit command to the next; it is not cross-session or cross-vendor context
transfer. A checkbox says a task is incomplete. It cannot say the agent got three
quarters through it, rejected two approaches, and left an unstaged edit.

### 4.3 Issues and pull requests as durable state

GitHub's own framing is direct. Its Copilot coding agent docs contrast IDE
assistants, where "decisions made during the session are **untracked** and lost
to time unless committed," with work on GitHub where "every step happening in a
commit and being viewable in logs." The same page records a constraint worth
adopting as convention: "Copilot can only work on one branch at a time and can
open exactly one pull request to address each task it is assigned."
(https://docs.github.com/en/copilot/concepts/agents/coding-agent/about-coding-agent,
accessed 2026-08-28)

That matches what `govcon-factory` does, what `agent-mesh/.agent/protocols/issue-as-spine.md`
prescribes, and what `rules/session-continuity.md` already chose.

### 4.4 Worktrees and branch isolation

Git's one-branch-per-worktree rule is a hard constraint. Codex's worktree docs
state it and reproduce the error: `fatal: 'feature/a' is already used by worktree
at '<WORKTREE_PATH>'`.
(https://learn.chatgpt.com/codex/environments/git-worktrees, accessed 2026-08-28)

All four harnesses ship worktree support: Codex creates managed worktrees under
`$CODEX_HOME/worktrees` in detached HEAD, keeps the most recent 15, and snapshots
before deleting (same source); Gemini CLI has `--worktree` behind
`experimental.worktrees` creating under `.gemini/worktrees/`
(`docs/cli/git-worktrees.md`, accessed 2026-08-28); Grok Build takes
`-w, --worktree [<NAME>]` and `--ref <REF>` with `grok worktree list|show|rm|gc`
(https://docs.x.ai/build/cli/reference, accessed 2026-08-28); Claude Code exposes
`WorktreeCreate` and `WorktreeRemove` hook events
(https://code.claude.com/docs/en/hooks, accessed 2026-08-28).

The detail that matters for a resuming agent: a worktree can be auto-deleted
while its branch survives. `log/CORRECTIONS.log` records the local version on
2026-08-25, where a worktree and its `.git/worktrees/` metadata both vanished
mid-task and the branch survived at zero commits. **The branch is the durable
unit. The worktree is not.**

### 4.5 Memory: MCP servers and vendor memory

The MCP reference **Memory** server is a knowledge graph persisted to a single
JSONL file, path set by `MEMORY_FILE_PATH`, defaulting to `memory.jsonl` in the
server directory. Its repository carries an explicit warning that the servers
there "are intended as **reference implementations** ... not as production-ready
solutions." (https://github.com/modelcontextprotocol/servers, README and
`src/memory/README.md` at `main`, accessed 2026-08-28)

Poor fit for handoff state on three counts: the reference implementation
disclaims production use; the default storage path is outside the repo, so state
is machine-local and unreviewable; and a knowledge graph is a bad representation
for an ordered event log, which is what a handoff needs.

Vendor memory is deliberately private and therefore worse:

- **Claude Code auto memory** at `~/.claude/projects/<project>/memory/`. Docs:
  "Auto memory is machine-local ... Files are not shared across machines or cloud
  environments." Only the first 200 lines or 25KB of `MEMORY.md` loads per
  session. (https://code.claude.com/docs/en/memory, accessed 2026-08-28)
- **Gemini CLI Auto Memory**: off by default, experimental, proposes `.patch`
  files to an inbox for human approval (`docs/cli/auto-memory.md`, accessed
  2026-08-28).
- **Codex Memories**: `memories` feature flag, default `false`, Experimental
  (https://learn.chatgpt.com/codex/config-file/config-basic, accessed 2026-08-28).
- **Grok Build**: `--experimental-memory`, `grok memory clear
  [--workspace|--global|--all]` (https://docs.x.ai/build/cli/reference, accessed
  2026-08-28).

Anthropic's own engineering guidance points at files rather than memory servers:
"Structured note-taking, or agentic memory, is a technique where the agent
regularly writes notes persisted to memory outside of the context window ... like
Claude Code creating a to-do list, or your custom agent maintaining a NOTES.md
file."
(https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents,
published 2025-09-29, accessed 2026-08-28)

---

## 5. The vendor-neutrality problem, tested

The hypothesis: durable state must live in the repository and the issue tracker
rather than in any agent's context. The test: can each vendor's persistence
mechanism be read by another vendor.

### 5.1 What each harness persists

| Harness | Transcript | Resume | Readable cross-vendor? |
|---|---|---|---|
| Claude Code | `~/.claude/projects/<project>/<session-id>.jsonl` | `--continue`, `--resume [name\|id]`, `/resume`, `--from-pr`, `/branch`, `--fork-session` | **No.** Docs: "The entry format is internal to Claude Code and changes between versions, so scripts that parse these files directly can break on any release" |
| Codex | `~/.codex/sessions/`, rollout JSONL | `codex --resume [id]`, `-c` | Not documented as a stable public format |
| Gemini CLI | `~/.gemini/tmp/<project_hash>/chats/` | `--resume [latest\|index\|uuid]`, `/resume` browser | Project-scoped by directory hash |
| Grok Build | `~/.grok/sessions/`, keyed by working directory | `-r`, `-c`, `--fork-session`, `/fork`, `/rewind` | Partially: `grok import` imports sessions **from Claude Code**, one direction |

Sources: https://code.claude.com/docs/en/sessions ;
`docs/cli/session-management.md` at `google-gemini/gemini-cli` `main` ;
https://docs.x.ai/build/features/sessions and https://docs.x.ai/build/cli/reference .
All accessed 2026-08-28. The Codex path comes from a secondary source and is
**not confirmed** against OpenAI documentation; see §9.1.

**The hypothesis holds.** Every resume mechanism is same-vendor by construction,
and Claude Code's own documentation warns against parsing its transcript. The one
documented cross-vendor path is `grok import`, one direction only, and it is a
session import rather than a live handoff. A transcript is never the medium.

### 5.2 Compaction destroys exactly the thing that matters

Claude Code's compaction table: project-root `CLAUDE.md`, unscoped rules, auto
memory and the plan-mode plan are re-injected from disk; files Claude read are
re-read, "up to five, most recently modified first"; "context that hooks added
earlier" is "summarized with the rest of the conversation." If an instruction
disappeared after compaction, "it was given only in conversation."
(https://code.claude.com/docs/en/context-window, accessed 2026-08-28)

Anthropic names the risk inside the summary: "The art of compaction lies in the
selection of what to keep versus what to discard, as overly aggressive compaction
can result in the loss of subtle but critical context whose importance only
becomes apparent later." (same engineering post, accessed 2026-08-28)

This is the mechanism behind Mike's complaint that an agent keeps a choice and
loses the reasoning. A summarizer keeps the decision, because the decision is a
fact about current state. It drops the rejected alternatives, because they look
like dead ends. The next agent then re-proposes a rejected alternative in good
faith. `Agent SDLC.md` line 183 makes the same observation independently and adds
a threshold worth testing: "Quality drops well before the advertised window is
full (~60-70% fill)." I could not verify that number; see §9.

### 5.3 The portable substrate, stated precisely

Four things are readable by all four harnesses with no vendor cooperation:

1. **Files committed to the git repository.** Read by any agent with `cat`.
   Reviewable, diffable, survives every process death.
2. **Git itself**: branch refs, commit messages, `git status`, `git diff`,
   `git stash list`, `git reflog`. Every harness has shell access.
3. **The GitHub issue and PR thread.** Reachable via `gh` from a shell by all
   four, and via the GitHub MCP server by all four.
4. **An instruction file loaded at startup**, subject to §4.1: `AGENTS.md`, plus
   a `CLAUDE.md` that imports it, plus a `.gemini/settings.json` entry naming it.
   Codex's 32 KiB cap applies.

Everything else, including every transcript, every auto-memory store, every
resume flag, and every MCP memory server's default location, is vendor-local or
machine-local.

### 5.4 What teams doing this at scale actually do

No published solved cross-vendor handoff exists that I could find, and one of the
most-cited practitioner sources says so. Cognition's "Don't Build Multi-Agents":
"At the moment, I don't see anyone putting a dedicated effort to solving this
difficult cross-agent context-passing problem."
(https://cognition.ai/blog/dont-build-multi-agents, published 2025-06-12,
accessed 2026-08-28)

Its two principles are the constraints any design must satisfy, and the second is
Mike's failure mode exactly:

> *Principle 1* Share context, and share full agent traces, not just individual messages
>
> *Principle 2* Actions carry implicit decisions, and conflicting decisions carry bad results

Cognition's own long-running answer is a dedicated compression model trained to
compress history "into key details, events, and decisions," which they call "hard
to get right." That is not adoptable here. The target shape of its output is:
**key details, events, and decisions.**

So the substrate question is settled and the open problem is not storage. It is
**authoring**: getting a dying agent to write a good record before it dies. Which
is why §7.4 is about enforcement and not about format.

---

## 6. What breaks

### 6.1 Today's four incidents, as primary evidence

Reported by Mike, 2026-08-28: three sessions died on usage limits mid-task, and a
fourth stalled indefinitely on an approval prompt nobody answered. In every case
the work was recoverable only because someone happened to check. **Two of the
four wrote a file just before dying, and that was the difference between
recoverable and lost.**

Three design conclusions follow, and they are load-bearing.

**First, the fourth incident is a distinct failure mode that no existing rule
covers.** A session stalled on an unanswered approval prompt is not dead. It
holds its claim, its worktree and its branch, it produces no output, and it
never fires a stop event of any kind. Every staleness check in this system
measures silence, and a stalled session is silent in exactly the same way a dead
one is, so a reaper would treat it identically and unclaim live work. `Agent
SDLC.md` line 62 already names the shape of the fix, from a different angle:
staleness must be phase-aware rather than clock-based, because a clock rule
flagged an overnight GPU run with 19 hours left as abandoned. The record needs a
`PHASE` field distinguishing `working`, `blocked-on-human`, `running-external`
and `waiting-approval`, plus an `EXPECTED-UNTIL` timestamp.

**Second, the two survivors prove the continuous-write principle rather than the
graceful-stop principle.** My earlier draft of this report organized §7 around a
graceful stop sequence, on the assumption that an agent that sees the limit
coming writes a good record. Today's evidence says the opposite is what mattered:
the file existed *already*, written during work, and the stop was abrupt. A
graceful-stop ritual is a bonus. It cannot be the mechanism, because in two of
four cases there was no graceful moment, and in the stall case there was no stop
at all. `rules/session-continuity.md` already states this and gives the reason:
"a session that dies never gets to write its summary, so the log has to already
exist by the time it dies." `agent-mesh/.agent/protocols/memory-write-discipline.md`
Rule 1 states it again: "Waiting for session end loses the why."

The design principle, restated so it is testable: **at any instant, an abrupt
stop must leave a recoverable record without any further action by the agent.**
That is a property of the file on disk at that instant, not of a procedure. It
implies a write cadence tied to state transitions, and it implies the record is
never worse than one state transition stale.

**Third, the write cadence must be transition-driven, not timed.** From
`Agent SDLC.md` line 61, and worth adopting verbatim as reasoning: "Save on state
transitions, never on a timer. A timer fires mid-thought and writes a snapshot of
confusion, a half-drafted approach, a command you were about to run but hadn't.
Whoever picks that up inherits your uncertainty as if it were a decision." This
is the correct refinement of `rules/session-continuity.md`'s "major turn"
definition, which already lists transitions rather than intervals.

**Finding: none of today's four incidents is in `log/CORRECTIONS.log`.** Its last
entry is dated 2026-08-26. `rules/DONT.md`'s operating rule requires an agent to
append before continuing. Four unlogged incidents means the `silent-long-running-work`
row is undercounted and the promotion loop cannot see them. See §8, F-1.

### 6.2 The undocumented-qualifier failure class

Mike's case study: a claim that the pipeline passed 42 of 42 gates propagated
through `govcon-factory` for days and was quoted as fact by multiple agents, when
it belonged to a different pipeline entirely. Nobody wrote down the qualifier.

This is not one incident. It is a recurring class, and `agent-mesh`'s own ledger
documents three more of it:

- **D-032** supersedes "D-030/D-031's false identity claim that
  `Jundot/Qwen3.8-27B-oQ4e-mtp` is exact `Qwen/Qwen3.8-Flash-Next`, and supersede
  every resulting exact-model/default/cache/engine conclusion," reclassifying
  their measurements as "historical 27B-control evidence only." A missing
  qualifier on a model identity contaminated two decisions and every conclusion
  downstream of them.
- **D-027** supersedes "only D-026's scheduler-tuning claim": the measurement was
  real, the attribution to operator tuning was not, because the fields turned out
  not to be operator-controllable. Same shape: the number survives, the qualifier
  was missing.
- **D-029** supersedes "D-028's enablement clause" after a fresh review found the
  skills index included capabilities outside repo scope.

Four instances of one class across two repos. By Mike's own two-strike rule this
is overdue for a check, not another sentence.

The countermeasure already exists and is already in production, in `agent-mesh`
and nowhere else: an explicit **`Boundary`** line attached to the claim in the
same artifact at the same time. `WORKLOG.md`'s entries carry it. `HANDOFF.md`'s
"Current truth" section is built out of it. The design work is to make it a
required field rather than a good habit, and to make its absence fail a check.

The precise rule that falls out, and it generalizes past handoffs: **a measured
result is reported with the thing it does not establish.** "32 of 32 tokens in
all eight cells" is incomplete. "32 of 32 tokens in all eight cells; this
validates throughput only; correctness, cache persistence and Hermes promotion
remain blocked" is complete. The second form cannot become a false fact
downstream, because the qualifier travels with the number.

### 6.3 The published taxonomy

"Why Do Multi-Agent LLM Systems Fail?" (Cemri et al., arXiv:2503.13657, v1
2025-03-17, v3 2025-10-26, accessed 2026-08-28) builds MAST, a 14-mode taxonomy
from 1600+ annotated traces across 7 frameworks, inter-annotator agreement
kappa = 0.88. Frequencies from §4 of the v3 HTML.

| Mode | Frequency | Relevance here |
|---|---|---|
| FM-1.3 Step repetition | 15.7% | Redoing completed work. Hit locally |
| FM-2.6 Reasoning-action mismatch | 13.2% | Not yet hit as a named mode |
| FM-1.5 Unaware of stopping conditions | 12.4% | Not yet hit. See §6.5 |
| FM-1.1 Disobey task specification | 11.8% | Task drift after handoff |
| FM-3.3 Incorrect verification | 9.1% | Hit repeatedly (`inert-regression-test`, 11 shapes) |
| FM-3.2 No or incomplete verification | 8.2% | Hit |
| FM-2.3 Task derailment | 7.4% | Scope creep across a handoff |
| FM-2.2 Fail to ask for clarification | 6.8% | Not yet hit as a named mode |
| FM-3.1 Premature termination | 6.2% | Not yet hit as a named mode |
| FM-1.4 Loss of conversation history | 2.8% | The literal trigger |
| FM-2.1 Conversation reset | 2.2% | The literal trigger |
| FM-2.5 Ignored other agent's input | 1.9% | Contradicting an earlier decision |
| FM-1.2 Disobey role specification | 1.5% | |
| FM-2.4 Information withholding | 0.85% | A bad handoff record is this |

Two findings bear on the design. Insight 2: "Solutions focused on context or
communication protocols are often insufficient for FC2 failures." A template is
necessary and not sufficient, which is why §7.4 exists. And the paper notes that
similar surface behaviour (missing information) can arise from withholding
(FM-2.4), ignoring input (FM-2.5), or context mismanagement (FM-1.4), which is
why the record must distinguish "I did not do this" from "I decided not to do
this."

### 6.4 Concurrent systems, which is a different problem from sequential handoff

Mike is right that this changes the brief. `~/agent-configs` and `~/agent-mesh`
are two agentic systems on one machine writing to overlapping state, and the
damage is documented in `agent-mesh`'s own worklog.

**Incident A, dropped MCP servers.** `WORKLOG.md` 2026-08-27 ~17:30: "mempalace
MCP re-added to `~/.hermes/config.yaml` (was dropped by yaml rewrite, now
gbrain+cloudflare*+mempalace 7 servers)." A whole-file YAML rewrite of live
config silently removed servers that the rewriting agent had no model of, and the
loss was found later by a different pass. Mike reports the drop as five servers;
the worklog states the restored total as 7 and does not state the dropped count,
so the exact number is unconfirmed (§9.5).

**Incident B, broken profile configs.** `WORKLOG.md` 2026-08-27 ~19:00: "root
cause brute-force yaml edit to `~/.hermes/config.yaml` (root default only) left
per-profile `~/.hermes/profiles/{prime,scout,sentinel,morning-brief}/config.yaml`
empty (`hermes profile list` showed '—')." And the earlier 2026-08-26 ~19:10
entry: "profiles lacked config.yaml, causing fallback to `model: ""` and empty
`providers: []`." Mike additionally reports an OpenCode config broken by a model
block missing a schema-required key; I found the OpenCode config path referenced
at `WORKLOG.md` line 146 but no entry describing that breakage, so it is
unconfirmed in the repo record (§9.6).

The common shape in both: **an agent rewrote a live config file whole, rather
than making a targeted change through the tool that owns it.** The fix is stated
in the repo's own record of incident B, which resolved it "properly via
`hermes -p <profile> config set model.provider/...`" instead of a YAML edit.

This generalizes into a rule the current surface does not contain, and it is not
a handoff rule. `rules/no-parallel-infrastructure.md` covers building a second
system; nothing covers a second system **writing to shared live state**. Three
constraints follow:

1. **Config owned by a tool is edited through that tool's own interface**, never
   by whole-file rewrite. A rewrite discards keys the writer did not model.
2. **Shared live state outside any repo** (`~/.hermes/`, `~/.omlx/`,
   `~/.config/opencode/`, `~/.claude/settings.json`) gets a
   read-diff-write-verify cycle: capture before, write, re-read, diff, and record
   the diff. Incident A was invisible precisely because nobody diffed.
3. **Shared live state is leased**, not raced. `govcon-factory` already has the
   lease mechanism (`scripts/lease-*.sh`, `leases` branch, non-fast-forward push
   as the check), and `agent-mesh` D-019 already restricts itself to "the
   canonical agent-mesh local process lock, active-client preflight, and
   OS-managed release" for benchmarks. Neither covers config files.

**This deserves its own rule and its own proposal, separate from the handoff
work.** It is a different failure with a different fix, and folding it into a
handoff rule would be the parallel-infrastructure mistake in reverse. Filed as
recommendation R-3 in §8.

### 6.5 What we have not hit yet

1. **FM-1.5, unaware of stopping conditions, applied to the handoff.** A resuming
   agent completes the named next action and keeps going, because nothing in the
   record defines done. `prompts/commands/no-early-stop-discipline.md` pushes the
   other way. Mitigation: the record carries an explicit exit condition, not only
   a next action.
2. **Handoff-record rot.** `log/CORRECTIONS.log`'s eleventh inert-test entry
   found a hand-built fixture "silently ROTS against upstream SHAPE changes." A
   handoff record is a hand-built fixture describing the repo. Mitigation: pin
   the SHA it was written against; the successor's first mechanical act is
   comparing it to `origin/main`.
3. **Two agents resuming the same handoff.** Nothing makes a record exclusive.
   Both read `STATE: handed off`, both proceed. Mitigation: a resume is a claim,
   taken through the existing claim mechanism before any edit.
   `agent-mesh/.agent/protocols/issue-as-spine.md` already has the claim protocol
   and the 48h expiry; it needs the handoff record to reference it.
4. **Handoff loops.** A hands to B, B dies in four minutes and hands back, and
   the pair burns context writing records. Mitigation: `HANDOFF-COUNT`; at three,
   stop and escalate, matching `rules/verification-law.md`'s existing
   three-failure hard stop rather than inventing a threshold.
5. **A confidently false handoff record.** `log/CORRECTIONS.log`'s
   `never-measured-reported-as-measured` entry establishes that "a confident
   false statement is WORSE in a client deliverable than a self-reporting
   'None'." A handoff record is read by a successor with no way to check it.
   Mitigation: every line is either a verified fact with its verifying command,
   or is under `UNVERIFIED`. `issue-as-spine.md` already says the same thing:
   "Claiming verification that did not happen is the one unforgivable protocol
   violation."
6. **Mid-edit partial state.** A limit hits between two edits of a three-file
   change. Nothing committed, tree syntactically broken, the working-tree diff is
   the only record. Mitigation: §7.5.

### 6.6 The failure the claim lock structurally cannot catch

From `log/CORRECTIONS.log`, 2026-08-26: PR #282 merged at 03:46:45Z; a different
session opened PR #288 seventeen seconds later implementing the same join point
independently. The entry's own conclusion: "an atomic issue-claim lock does not
prevent a DIFFERENT session from building the same capability under a DIFFERENT
issue/PR number entirely."

A claim lock is a mutex on an issue number, not on a region of code. The only
available defence is early visibility: a pushed branch and an open draft PR
touching those files is something another session can find with one `gh` query.
That argues for opening a draft PR at first push rather than at completion.

---

## 7. Design

### 7.1 The principle

Do not build a new state store. `rules/session-continuity.md` already chose the
surfaces, `agent-mesh` already runs on them, and
`rules/no-parallel-infrastructure.md` makes that choice binding. Five formats
already exist. The work is to reconcile them into one, add the two fields all
five lack, and build the check.

Stated as the property to satisfy: **at any instant, an abrupt stop leaves a
recoverable record with no further action by the agent.**

### 7.2 The handoff record

**Where it lives.** Two copies, both on already-chosen surfaces:

1. **`HANDOFF.md` at the root of the working branch**, committed and pushed. The
   cold-start copy. It arrives with the code, at the same commit as the code, and
   `git log HANDOFF.md` gives the successor a free ordered history of every
   handoff on this branch. This is the copy a resuming agent reads first.
2. **The same text as a comment on the tracked issue**, inside the
   `HANDOFF BEGIN` / `HANDOFF END` sentinels that
   `agent-mesh/.agent/protocols/issue-as-spine.md` already defines. The discovery
   copy, findable without checking anything out, and what a staleness check reads.

Note this reuses `agent-mesh`'s filename and sentinel deliberately. Two systems
on one machine should not have two names for the same artifact.

**The fields.** Reconciled from all six existing formats, the five in §2 plus
`Agent SDLC.md`. Provenance is given per field so nothing here reads as invented.
Six fields are required; the rest are written when they have content.

| Field | Req | From |
|---|---|---|
| `STATUS`, `STATE`, `NEXT`, `BLOCKED-ON` | yes | `rules/session-continuity.md`, verbatim, unchanged |
| `BRANCH`, `WORKTREE` | yes | `rules/worktree-protocol.md` |
| `BASE-SHA` | yes | The `origin/main` SHA this record was written against. Drift detection, §6.5 item 2 |
| `LAST-KNOWN-GOOD` | yes | `Agent SDLC.md` point 7. The last good commit **on this branch**, which is the fallback after a broken mid-edit stop. Distinct from `BASE-SHA` |
| `PHASE`, `EXPECTED-UNTIL` | yes | `Agent SDLC.md` line 62, phase-aware staleness. `working \| blocked-on-human \| waiting-approval \| running-external`. Covers today's stalled-on-approval incident |
| `STOP-REASON` | yes | `Agent SDLC.md` field 9: `task-complete \| context-budget \| quota \| blocker \| stalled-on-approval` |
| `HANDOFF-COUNT` | yes | New. §6.5 item 4. At 3, stop and escalate |
| `TREE` | yes | **New.** Empty in all six existing formats |
| `EVENTS` | | `agent-mesh/WORKLOG.md` append discipline, scoped to one branch |
| `DECISIONS` | | `agent-mesh/DECISIONS.md` `decision \| rationale \| provenance` triple |
| `REJECTED` | | **New to this repo.** `Agent SDLC.md` point 7 `FAILED APPROACHES`, adopted with its stable IDs (`F011`) so an entry is citable from a later handoff, commit or issue |
| `DO-NOT` | | `Agent SDLC.md` point 7. Negative constraints not derivable from `REJECTED`: what is forbidden for cost, scope, or a pending decision |
| `DONE` | yes | `issue-as-spine.md` `Verified` plus `WORKLOG` `Evidence`; each line carries its verifying command |
| `BOUNDARY` | yes when `DONE` has a numeric claim | `agent-mesh/WORKLOG.md`. The 42-of-42 countermeasure |
| `UNVERIFIED` | yes when `DONE` is non-empty | `rules/verification-law.md` plus `issue-as-spine.md`'s unforgivable-violation rule |
| `HYPOTHESIS` | | `Agent SDLC.md` point 7. For a stop mid-investigation, the most expensive thing to reconstruct |
| `GOTCHAS` | | `issue-as-spine.md` |

Two fields are genuinely new to every format surveyed, `TREE` and `BOUNDARY`-as-required,
and they are the two things a successor cannot reconstruct: git shows what landed,
never the tree state at the moment of death, and never the qualifier on a number.
`REJECTED`, `DO-NOT`, `LAST-KNOWN-GOOD` and `HYPOTHESIS` are adopted from
`Agent SDLC.md` (§10.5). Everything else is existing practice, reconciled.

**On cost, which is the binding constraint.** §10.2 found that the only voluntary
practice on this machine that survived contact with real work was `BOUNDARY`,
because it costs one clause inside the sentence making the claim. Six required
fields is already at the edge of what will get written. The optional fields exist
so a record is never blocked on having nothing to say in them, and the check in
§7.4 tests only the six.

Full template with worked example: `prompts/handoff-record-template.md`.

**Why not the fork-summary template already in `prompts/`.**
`prompts/fork-summary-handoff-template.md` covers the deliberate fork, where a
live agent spawns a successor and passes an in-memory prompt, and it is explicit
that the filled prompt is never written to disk. Correct for its case. A dead
agent has no live process to hold a string and no receiving process to hand it
to. Complementary, cross-referenced in both files, not merged.

### 7.3 Cold start: what a resuming agent reads, in order

Hierarchical, adopting `Agent SDLC.md` point 14's L0-through-L5 structure: read
cheap layers first and descend only when a step needs it. Mechanical until step 8.

**L0, orientation (about 1K tokens).**

1. `git fetch origin && git log --oneline -1 origin/main`. Record the SHA.
2. `cat HANDOFF.md` on the branch. If absent, fall back to the issue thread, then
   `git log` on the branch, and record in the first status that no record existed.
3. Compare `BASE-SHA` to current `origin/main`. If they differ, every path and
   line reference in the record is suspect until verified.
4. Check `PHASE` and `EXPECTED-UNTIL`. If `PHASE` is `blocked-on-human`,
   `waiting-approval` or `running-external` and `EXPECTED-UNTIL` has not passed,
   **do not take over.** The prior session may be alive and holding state.
   Escalate to Mike instead.

**L1, the record itself (2 to 4K).**

5. Read `NEXT`, `DO-NOT`, `BOUNDARY`, `REJECTED`, `GOTCHAS`. `BOUNDARY` before
   acting on any number: this is the step that stops a qualified result becoming
   an unqualified fact. `DO-NOT` and `REJECTED` before proposing anything: this is
   the step that stops re-litigating a settled dead end.

**L2, the tree and the claims (5 to 10K).**

6. `git status --short`, `git diff`, `git stash list`. Compare against `TREE`. A
   mismatch means something moved and the record is stale. If the tree is broken,
   `LAST-KNOWN-GOOD` is the fallback commit.
7. Verify each `DONE` line by running the command it names.
   `rules/verification-law.md` applied to someone else's claims.

**L3 and below, only if a step above left a real gap.** Source files, then the
issue thread and `DECISIONS.md`, then archived raw transcripts (§10.5 item 8) for
the one case they answer well: "why exactly did the previous agent reject
approach B" when `REJECTED` is too thin. Never as working memory.

**Then take the work.**

8. Claim through the existing mechanism before the first edit.
9. Post a status block naming the record resumed from and the result of step 7.

Steps 3, 6 and 7 turn claims into facts. Step 4 is what today's fourth incident
requires and what no current protocol has. Step 5's `BOUNDARY` read is what the
42-of-42 case requires.

### 7.4 Enforcement

`agent-configs` has no `.github/` directory, so this is also where it gets one.

**Rung 0, prerequisite: merge the four unmerged rules.** No enforcement of an
unmerged rule is possible. Tier 2, so Mike's, and it blocks everything below.

**Rung 1, repo-side, works for all four vendors.**

- `scripts/check-handoff.sh`: validates a `HANDOFF.md` against the six required
  fields. Fails if the file is missing; if `BASE-SHA` or `LAST-KNOWN-GOOD` names a
  commit not in the repository; if `PHASE` is set without `EXPECTED-UNTIL`, or
  `EXPECTED-UNTIL` is not a parseable timestamp; if `STOP-REASON` is outside its
  enum; if `HANDOFF-COUNT` is absent or is 3 or more without a `needs-mike` label
  on the issue; if any `DONE` line lacks a verifying command; if `UNVERIFIED` is
  absent while `DONE` is non-empty; if `BOUNDARY` is absent while `DONE` contains
  a numeric claim. Pure shell plus `git`, so it runs identically under every
  harness and in CI.

  The last rule is the 42-of-42 check, and it is the one worth building first: a
  handoff that reports a number without saying what the number does not establish
  fails the build. That converts §6.2's four-instance failure class from a habit
  into a gate, which is what Mike's two-strike rule asks for.
- `scripts/hooks/pre-push`: refuse a push to a `work/*` branch whose tip is more
  than N commits ahead of the last commit touching `HANDOFF.md`, unless the push
  is a single WIP commit. This is what makes the record never more than one state
  transition stale, which is the §7.1 property, enforced.
- `.github/workflows/handoff-check.yml`: run `check-handoff.sh` on every PR from
  a `work/*` branch. Model it on `govcon-factory`'s `check-decisions-entry.sh`,
  already proven to block a PR for a missing companion entry.

**Rung 2, vendor hooks, best effort where they exist.** Claude Code fires
`StopFailure` "when the turn ends due to an API error," with a matcher on error
type whose documented values include exactly `rate_limit`, plus `overloaded`,
`billing_error` and `max_output_tokens`
(https://code.claude.com/docs/en/hooks, accessed 2026-08-28). Grok Build has the
same event and reads Claude Code hook files: "Claude Code
(`.claude/settings.json`) and Cursor (`.cursor/hooks.json`) hook files are read
as well" (https://docs.x.ai/build/features/hooks, accessed 2026-08-28). So one
hook file covers two harnesses.

Codex has `SessionStart`, `SessionEnd`, `Stop`, `SubagentStop`, `PreCompact`,
`PostCompact`, `PreToolUse`, `PostToolUse`, `UserPromptSubmit`,
`PermissionRequest`, with no documented rate-limit-typed event
(https://learn.chatgpt.com/codex/hooks, accessed 2026-08-28). Gemini CLI uses a
different vocabulary entirely: `BeforeTool`, `AfterTool`, `BeforeAgent`,
`AfterAgent`, `BeforeModel`, `AfterModel`, `BeforeToolSelection`, `SessionStart`,
`SessionEnd`, `Notification`, `PreCompress` (`docs/hooks/reference.md` at
`google-gemini/gemini-cli` `main`, accessed 2026-08-28).

Two of four harnesses can detect a rate-limit stop; two cannot. **That is why
rung 1 is the enforcement and rung 2 is the accelerator.** The `StopFailure` hook
writes a machine-generated `HANDOFF.md` stub carrying `TREE`, `BRANCH`, `SHA`,
`STOP-REASON: quota` and the last N commits, then commits it. A machine stub is
worse than an agent-written record and far better than nothing, because it fires
when the agent can no longer act.

**Rung 3, the discipline that makes the rest cheap.** One verified sub-step, one
commit, pushed. Already the lesson of the 2026-08-25 vanished-worktree entry
("commit early/often even mid-implementation"), and it is what makes a machine
stub useful, because the commit log then supplies the events the stub cannot
infer.

**Deliberately not proposed:** a session-start lock hook.
`proposals/PROPOSAL-0001.md` proposed one and `DECISIONS.md` D-005 records that
Mike converted it to a convention. Re-proposing it would re-litigate a settled
call.

### 7.5 The limit-hit case

**Continuous, which is the actual mechanism.** Write `HANDOFF.md` at each state
transition, not on a timer and not at the end. A state transition is: a step
finishes, a file lands, a decision is made between alternatives, an approach is
rejected, a PR or issue changes state, a review or gate result arrives, a blocker
hits. This is `rules/session-continuity.md`'s "major turn" list, unchanged, now
attached to a richer artifact. The pre-push hook in rung 1 is what makes it
happen when discipline does not.

**Graceful stop, if the agent sees it coming.** At roughly 70% context or on a
usage warning, in this order, because the order is what survives an interruption
partway through:

1. `git add -A && git commit -m "wip: <honest description>"` and push. Code first,
   because it is the only thing that cannot be reconstructed.
2. Update `HANDOFF.md` with `STOP-REASON`, commit, push.
3. Post the same text to the issue.
4. Do not start a new slice.

**Ungraceful stop, mid-edit, no warning.** The successor establishes the tree's
actual state before deciding anything. This is a branch of step 5 in §7.3:

1. `git stash list` and `git status --short`. An uncommitted change with no
   `TREE` entry naming it is a mid-edit stop until proven otherwise.
2. Do not discard it, do not commit it blind. `rules/worktree-protocol.md` says
   to stop and report on uncommitted work you did not create; the handoff case is
   the exception, because here you know who created it, so the rule becomes
   preserve before acting: `git stash push -m "recovered-mid-edit-<date>"` gives
   a recoverable copy without polluting the branch.
3. Reconstruct intent from the diff, the last commit message and the issue
   thread. Write the conclusion under `UNVERIFIED`, never under `DONE`.
4. If the change is broken and its intent is not recoverable, say so and
   escalate. A guessed reconstruction is `never-measured-reported-as-measured`
   with a new costume.

**Stalled, not stopped.** The fourth incident. `PHASE: waiting-approval` plus
`EXPECTED-UNTIL` is what distinguishes it from death. A reaper that sees a live
`EXPECTED-UNTIL` posts a nudge to the issue and to Mike, and does not unclaim.
Past `EXPECTED-UNTIL`, it is treated as abandoned. This makes the stall visible
without making a live session's work stealable.

### 7.6 GitHub mechanics

Mostly porting rather than inventing.

**Branch and worktree.** `rules/worktree-protocol.md` unchanged: one issue, one
worktree, one branch, one session, `~/<repo-abbrev>-wt/<work-id>`. Git enforces
the one-branch-per-worktree half for free.

**Claiming without racing.** The `claims`-branch mutex from `govcon-factory`
`scripts/issue-claim.sh`, where a rejected non-fast-forward push is the
exclusivity check. Proven on live races. Port to `agent-configs`. Accept its
known limit from §6.6.

**Draft PR early.** Open a draft PR at first push, not at completion. This is the
only available mitigation for §6.6, and it matches GitHub's own
one-branch-one-PR-per-task constraint.

**Labels, as machine-queryable state:** `handed-off`, `limit-hit`, `mid-edit`,
`stalled-on-approval`, `needs-mike` (existing).

**Commit granularity.** One verified sub-step, one commit, pushed. Commit
messages are part of the event log, so they say what changed and why. The
exception is the graceful-stop WIP commit, explicitly labelled.

**Merge tiers** unchanged from D-001. Because this proposal touches `rules/`, it
is Tier 2 and no agent merges it.

---

## 8. Findings register

Per Mike's standing instruction: everything contradictory, stale or broken found
during this work, with file, line, evidence, suggested correction, and a
recommendation to fix, file, or escalate. Ordered by severity.

**F-1. Today's four incidents are not in the corrections log.**
File: `~/agent-configs/log/CORRECTIONS.log`, last entry line dated 2026-08-26T12:35:16Z.
Evidence: Mike reports three usage-limit deaths and one approval stall on
2026-08-28; the log has no 2026-08-28 entry. `rules/DONT.md` operating rule
requires the append to happen "**before** continuing the task that triggered the
correction."
Correction: append four entries with `rule=silent-long-running-work`, one per
incident, naming which two wrote a file and which did not.
Recommendation: **fix now.** This also moves `silent-long-running-work` past the
two-violation promotion threshold, which is the trigger for PROPOSAL-0004.

**F-2. Four rules Mike believes are in force are not on `main`.**
File: `~/agent-configs`, branch `work/session-continuity-issue-16-clean`, containing
`rules/session-continuity.md`, `rules/worktree-protocol.md`,
`rules/review-independence.md`, `rules/model-routing.md`, and `DECISIONS.md`
D-002 through D-005.
Evidence: `git diff --stat main...work/session-continuity-issue-16-clean` shows
650 insertions across 10 files; `main`'s `DECISIONS.md` ends at D-001; `ls
rules/` on `main` does not list any of the four.
Correction: merge the branch, or close it and re-land the content.
Recommendation: **escalate to Mike.** Tier 2 under D-001, so no agent can do it.
This is the single highest-leverage action available, because every other
enforcement proposal is downstream of it.

**F-3. `Agent SDLC.md` is untracked and would be lost with the machine.**
File: `~/agent-mesh/Agent SDLC.md`, 1,831 lines, 77 KB, modified 2026-08-28 01:47.
Evidence: `git status --short` in `~/agent-mesh` shows `?? "Agent SDLC.md"`.
Correction: commit it. Also rename to remove the space in the filename, which
breaks shell paths that are not quoted.
Recommendation: **fix now.** Additionally, by `MASTER-GUIDE.md` §1's own boundary
rule, universal cross-vendor SDLC research belongs in `agent-configs` or
`agent-workspace`, not a project repo. Suggest committing it where it is to stop
the bleeding, then moving it deliberately.

**F-4. `Agent SDLC.md` states Claude Code reads AGENTS.md. It does not.**
File: `~/agent-mesh/Agent SDLC.md` line 36.
Evidence: that line reads "Claude Code|Yes, bridged|Added AGENTS.md support in
spring 2026". Claude Code's own documentation, accessed 2026-08-28, states:
"Claude Code reads `CLAUDE.md`, not `AGENTS.md`," and prescribes an `@AGENTS.md`
import or an `ln -s AGENTS.md CLAUDE.md` symlink as the bridge
(https://code.claude.com/docs/en/memory).
Correction: change the cell to "No, bridge required: `@AGENTS.md` import in
CLAUDE.md, or symlink."
Recommendation: **fix.** A repo relying on this would ship an `AGENTS.md` that
Claude Code never loads, which is a silent whole-ruleset failure.

**F-5. `Agent SDLC.md` states Gemini CLI cannot read AGENTS.md. It can.**
File: `~/agent-mesh/Agent SDLC.md` line 38.
Evidence: that line reads "**Gemini CLI**|**No**|The remaining holdout — still
uses GEMINI.md". Gemini CLI's own docs document `context.fileName` accepting a
list, with `["AGENTS.md", "CONTEXT.md", "GEMINI.md"]` as the worked example
(`docs/cli/gemini-md.md` at `google-gemini/gemini-cli` `main`, accessed
2026-08-28). agents.md lists Gemini CLI as supported and links the same setting.
Correction: change to "Yes, with one line of config: `{"context": {"fileName":
["AGENTS.md", "GEMINI.md"]}}` in `.gemini/settings.json`."
Recommendation: **fix.** The current text would cause someone to maintain a
duplicate `GEMINI.md` unnecessarily, and duplicated rule surfaces drift.

**F-6. `WORKLOG.md` violates its own stated ordering.**
File: `~/agent-mesh/WORKLOG.md` line 3 states "Newest at bottom."
Evidence: line 31 is `2026-08-27 ~17:30`; line 33 is `2026-08-26 ~14:40`; line 41
is `2026-08-27 ~18:15`; line 43 is `2026-08-26 ~16:40`. At least four inversions.
Correction: either re-sort and note the re-sort, or amend the header to "grouped
by workstream, not strictly chronological" and add an explicit `ts` field per
entry.
Recommendation: **fix.** This is load-bearing for the design in §7.2: an
append-only log that is not actually ordered cannot supply order of events to a
cold-start reader. It is also the argument for the per-branch `HANDOFF.md`, where
git supplies ordering for free.

**F-7. `DECISIONS.md` violates its own stated ordering.**
File: `~/agent-mesh/DECISIONS.md` line 4: "New entries go at the bottom."
Evidence: line 38 is `D-016 | 2026-08-27`; line 40 is `D-017 | 2026-08-26`.
Correction: same as F-6. Note that ID order and date order genuinely can diverge
when two sessions allocate concurrently; the honest fix is to say so in the
header and keep ID order authoritative.
Recommendation: **fix.** Low cost, and `.agent/protocols/memory-write-discipline.md`
already prescribes the mechanism: "IDs allocate from the ledger itself (scan for
max, plus one) so parallel branches cannot collide silently."

**F-8. Shared live config is rewritten wholesale by agents, silently dropping keys.**
Files: `~/.hermes/config.yaml`, `~/.hermes/profiles/*/config.yaml`, and per Mike
`~/.config/opencode/opencode.json`.
Evidence: `~/agent-mesh/WORKLOG.md` 2026-08-27 ~17:30 ("mempalace MCP re-added to
`~/.hermes/config.yaml` (was dropped by yaml rewrite...)") and 2026-08-27 ~19:00
("root cause brute-force yaml edit to `~/.hermes/config.yaml` (root default only)
left per-profile ... config.yaml empty").
Correction: a rule requiring tool-owned config to be edited through the owning
tool's interface, plus a read-diff-write-verify cycle and a lease for shared
live state outside any repo.
Recommendation: **file as its own proposal.** It is a distinct failure with a
distinct fix; folding it into the handoff rule would repeat the
parallel-infrastructure mistake in reverse. Drafted as R-3 below.

**F-9. `MASTER-GUIDE.md` §5 documents scheduled reapers that are not scheduled.**
File: `~/agent-configs/MASTER-GUIDE.md` §5, rows "Stale-claim reaper ... 2-hourly"
and "Worktree/branch hygiene ... 6-hourly".
Evidence: `rules/session-continuity.md` (on the unmerged branch) records that
`launchctl list`, `crontab -l`, and every plist under `~/Library/LaunchAgents`,
`/Library/LaunchAgents` and `/Library/LaunchDaemons` were checked directly and
none references the reaper. The script's own header says it is "deliberately NOT
wired to auto-run on first ship."
Correction: change the cadence column to "on demand, not scheduled", or schedule
them.
Recommendation: **fix the doc now, schedule separately.** §7.5's stalled-session
detection depends on a scheduled reaper, so this blocks part of the design.

**F-10. `proposals/PROPOSAL-0001.md` frontmatter contradicts its own decision.**
File: `~/agent-configs/proposals/PROPOSAL-0001.md` frontmatter, `status: "open"`,
`decision: null`.
Evidence: `DECISIONS.md` D-005 on the unmerged branch records that Mike ruled on
it and it became `rules/worktree-protocol.md`.
Correction: set `status: "accepted"` and fill the Decision section.
Recommendation: **fix, bundled with F-2's merge.**

**F-11. `scripts/consolidate-corrections.sh` skip check is structurally wrong.**
File: `~/agent-configs/scripts/consolidate-corrections.sh`, the
`grep -rl "target: \"$rule\"" proposals/` check.
Evidence: `DECISIONS.md` D-005 (unmerged) records that it matches on a proposal's
existence rather than its `status`/`decision`, so auto-escalation for
`shared-working-directory-concurrent-checkout` has been off since 2026-08-24.
Correction: parse the frontmatter `status` and skip only when `status: accepted`
or `rejected`.
Recommendation: **fix.** Without it the promotion loop that is supposed to
enforce Mike's two-strike rule is silently disabled for any rule that already has
a proposal, which is exactly the rules under most pressure.

**F-12. `agent-configs` primary checkout is dirty and on a foreign branch.**
File: `~/agent-configs`, working tree.
Evidence: `git status --short` shows ` M hooks/damage-control/patterns.yaml`,
` M log/CORRECTIONS.log`, and `?? .claude/`, while `git branch` shows HEAD on
`work/single-queue-issue-243`, which is a `govcon-factory` issue number carried
into the wrong repo's branch name.
Correction: commit or stash the two modified files under their owning session,
return the primary checkout to `main`, and rename or delete the branch.
Recommendation: **escalate.** The modifications belong to another session and
`rules/worktree-protocol.md` says to stop and report rather than touch them. This
is at least the fifth logged instance of `shared-working-directory-concurrent-checkout`.
Note: the two files I wrote for this task landed in this dirty checkout as
untracked files. They are additive and touch nothing else, but Mike should commit
them deliberately rather than let them ride on that branch.

**F-13. `agent-mesh/AGENTS.md` commit policy is already past its own trigger.**
File: `~/agent-mesh/AGENTS.md`, Commit policy section.
Evidence: it reads "Direct pushes to `main`: allowed ... while the swarm is
small. The moment two agents work this repo concurrently, switch to PRs-only for
code." `WORKLOG.md` records concurrent-session reconciliation on 2026-08-26
~20:35 ("#22 reconciliation after concurrent-session handoff") and the repo has
had multiple agents in it since.
Correction: switch to PRs-only for code, per the file's own stated condition.
Recommendation: **escalate to Mike.** The condition the policy names has been met
and the policy has not changed.

**F-14. `agent-mesh` violated its own worklog rule on the document that prescribes
worklog discipline.**
File: `~/agent-mesh/AGENTS.md`, "Every session must" item 2.
Evidence: it requires "Append to `WORKLOG.md` at every milestone (what, where,
evidence). The worklog is the continuity mechanism — an unlogged change did not
happen." `Agent SDLC.md` is 77 KB, mtime `2026-08-28 01:47:12 -0400`. The newest
`WORKLOG.md` entry is `## 2026-08-27 ~23:33 EDT` and the file's mtime is
`23:37:57`, both before the document existed. `git log -- "Agent SDLC.md"` is
empty and `git grep "Agent SDLC"` finds only `.obsidian/workspace.json:208`.
Correction: append a `WORKLOG.md` entry naming the document, its purpose and its
status, and commit the file.
Recommendation: **fix now.** This is not a nitpick: it is the cleanest available
measurement of which practices survive real work, and it is the evidence base for
§10.2's conclusion that any practice needing a second write to a second file
fails without a mechanical consequence.

**F-15. `Agent SDLC.md` filename contains a space.**
File: `~/agent-mesh/Agent SDLC.md`.
Evidence: `git ls-files` output and every shell reference in this session required
quoting; an unquoted path silently splits into two arguments.
Correction: rename to `agent-sdlc.md` or `AGENT-SDLC.md`.
Recommendation: **fix**, bundled with F-3's commit. Cheap, and it removes a class
of scripting failure for every future agent that touches it.

**F-16. Two conflicting staleness models inside one document.**
File: `~/agent-mesh/Agent SDLC.md`, line 62 versus point 9 (around line 1188).
Evidence: line 62 records that a clock-based rule ("no update in 2 hours =
abandoned") wrongly flagged an overnight GPU run with 19 hours left, and concludes
staleness must be phase-aware. Point 9 then proposes a lease with
`expires_seconds: 300`, a far more aggressive clock rule, as the mechanism for
reclaiming a task from a disappeared agent.
Correction: keep line 62's phase-aware model; if a heartbeat is used, it is an
input to staleness, never the sole criterion.
Recommendation: **fix in the document when it is committed.** Adjudicated in
§10.4 D-3. A 300-second expiry would have unclaimed today's fourth incident,
the session stalled on an unanswered approval, within five minutes.

**F-17. Two vendor-capability claims in `Agent SDLC.md` are contradicted by
current vendor documentation.** See F-4 and F-5. Recorded here as a pair because
they share a root cause worth noting: both errors run in the direction of
training-data recall rather than a documentation read, overstating Claude Code's
`AGENTS.md` support and understating Gemini CLI's. Recommendation: **treat every
other tool-capability claim in that document as unverified until checked**, and
re-check them when it is committed.

### Recommendations not tied to a single finding

**R-1. Merge the four unmerged rules.** Blocks everything. Mike only.

**R-2. Accept or reject PROPOSAL-0004** (§7 as a rule diff plus the template plus
`check-handoff.sh`). Mike only, Tier 2.

**R-3. File a separate proposal for shared-live-state discipline** covering F-8:
tool-owned config edited through the owning tool, read-diff-write-verify for
shared state outside any repo, and a lease for it. Not part of the handoff rule.

**R-4. Reconcile the two systems' rule surfaces.** `agent-mesh/AGENTS.md` already
points at `~/agent-configs` and says "Where agent-configs rules and this file
conflict, flag it in `DECISIONS.md` rather than silently picking." That is the
right protocol and it has no check either. At minimum, `agent-configs` should
gain a root `AGENTS.md` so non-Claude harnesses opened in it load the rule
surface at all; today it has only `MASTER-GUIDE.md`, which nothing loads
automatically.

---

## 9. What could not be verified

1. **Codex session storage layout.** `~/.codex/sessions/YYYY/MM/DD/rollout-*.jsonl`
   comes from a secondary source
   (https://codex.danielvaughan.com/2026/04/13/codex-cli-session-persistence-resume-fork-analytics/,
   accessed 2026-08-28) and I could not confirm it against OpenAI documentation.
   The official pages document `~/.codex/config.toml`, `log_dir`, and
   `session-*.jsonl` as opt-in, without pinning the directory layout.
2. **Grok Build version and licence.** Search results describe v1.0 on 2026-08-07
   under Apache 2.0. The official CLI reference I read is dated "Last updated:
   July 21, 2026" and states neither, so I assert neither.
3. **Whether a usage-limit stop fires `SessionEnd` at all.** Claude Code's
   documented `SessionEnd` reasons are `clear`, `resume`, `logout`,
   `prompt_input_exit`, `other`. None names a rate limit. `StopFailure` with
   matcher `rate_limit` is documented and is what §7.4 relies on. Whether the
   process then also fires `SessionEnd`, and with which reason, is untested.
   **Test this before trusting the rung 2 hook.**
4. **Whether Grok loads a `.claude/settings.json` `StopFailure` hook.** The docs
   say Claude Code hook files "are read as well" and list `StopFailure` among its
   events, but I did not run `grok inspect` to confirm the combination. One
   command settles it.
5. **The MCP server drop count.** Mike reports five servers dropped from the
   Hermes config. `~/agent-mesh/WORKLOG.md` 2026-08-27 ~17:30 states mempalace was
   re-added and the total is now 7; it does not state how many were dropped. The
   number five is Mike-reported and not confirmed in the repo record.
6. **The OpenCode config breakage.** Mike reports a model block written without a
   schema-required key. `~/agent-mesh/WORKLOG.md` line 146 references
   `~/.config/opencode/opencode.json` as a file touched by the D-030/D-031 work,
   but I found no worklog or decisions entry describing the breakage. Unconfirmed
   in the repo record. **Recommend logging it**, since an unlogged incident
   cannot reach the promotion loop.
7. **The 42-of-42 gates case study.** Mike-reported. I have no `govcon-factory`
   access in this session and did not verify the propagation. The analogous
   `agent-mesh` instances (D-027, D-029, D-032) are verified in that repo's own
   ledger and carry the argument independently.
8. **`~/CLAUDE.md` content.** Outside the folders mounted in this session.
   `MASTER-GUIDE.md` §7 says it points at `rules/communication.md`. Whether it
   points at `session-continuity.md`, as unmerged D-002 claims it should, is
   unchecked.
9. **Live GitHub state.** No network access to GitHub from this session. Issue and
   PR numbers come from local files and branch names, not live queries. Whether
   `work/session-continuity-issue-16-clean` has an open PR, and its review state,
   is unverified.
10. **Context-degradation threshold.** `Agent SDLC.md` line 183 claims quality
    drops at roughly 60 to 70% context fill. I found no primary source for that
    number. Anthropic's post describes context rot as "a performance gradient
    rather than a hard cliff" without giving a percentage. §7.5's "roughly 70%"
    trigger is therefore a heuristic, not a measured threshold, and is labelled
    as such.
11. **AGENTS.md adoption count.** "Over 60k open-source projects" is agents.md's
    own claim linked to a GitHub code search. I did not run the search.
12. **Cognition's post is from 2025-06-12,** so its claim that nobody is working
    on cross-agent context passing is roughly fourteen months old. I found no
    contradicting source, which is not evidence the claim still holds.

---

## 10. Synthesis with `Agent SDLC.md`

`~/agent-mesh/Agent SDLC.md` is a peer analysis of this exact question, produced
by other models (its internal headers `C1`, `G0`, `G1` mark separate responses).
It is 1,831 lines. This section adjudicates it against my own research and
records what I took, what I rejected, and what is unresolved.

### 10.1 Provenance, which sets how much authority it carries

Checked directly, not inferred:

- `git ls-files --error-unmatch "Agent SDLC.md"` returns
  `error: pathspec 'Agent SDLC.md' did not match any file(s) known to git`.
  **It has never been committed.**
- `git log -- "Agent SDLC.md"` returns nothing.
- `git grep -n "Agent SDLC"` finds exactly one reference in the whole tracked
  repo, `.obsidian/workspace.json:208`, which is an editor's list of open files,
  not a citation.
- mtime `2026-08-28 01:47:12 -0400`. `WORKLOG.md`, `DECISIONS.md` and `HANDOFF.md`
  all carry mtime `2026-08-27 23:37:57 -0400`, written in the same second, and
  the newest commit `1cf77ce` is dated `2026-08-27 23:38:12 -0400`.

So the document was written **after** the last worklog, decisions and commit
update, and none of them mention it. **Verdict: it is an uncommitted draft.** Not
a ratified decision, not a filed proposal, not referenced by any decision entry
D-001 through D-034. It carries the authority of good research, which is real,
and none of the authority of a decision.

**On the future-dated worklog claim: I could not reproduce it.** `grep` for
`2026-08-28`, `2026-09` and later across `WORKLOG.md`, `DECISIONS.md` and
`HANDOFF.md` returns nothing, and the newest entry (`## 2026-08-27 ~23:33 EDT`)
precedes the file's own mtime by four minutes. What is true, and what I think was
seen, is that the worklog is **out of chronological order**, so entries appear to
move backwards in time: line 31 is `2026-08-27 ~17:30` and line 33 is
`2026-08-26 ~14:40`. Recorded as F-6. Correcting Mike's premise here rather than
adopting it, per the standing instruction.

### 10.2 Does agent-mesh follow its own document

This is the most useful question asked, and the answer is no, in a specific and
instructive way.

`agent-mesh/AGENTS.md` requires: "Append to `WORKLOG.md` at every milestone (what,
where, evidence). The worklog is the continuity mechanism — an unlogged change did
not happen." A 77 KB research document on the repo's own SDLC is a milestone by
any reading. It is unlogged, uncommitted, and unreferenced.

The same divergence appears in the two config incidents (§6.4). The repo's own
`.agent/protocols/issue-as-spine.md` mandates five same-turn writes and says "a
change logged an hour later is a reconstruction, not a record." The Hermes config
rewrite that dropped MCP servers was found and logged by a *later* pass, which is
by that protocol's own definition a reconstruction.

**The finding this yields is the one worth keeping.** Across both repos, the
practices that survived contact with real work are the ones with a mechanical
consequence, and the ones that did not are the ones that depended on an agent
choosing to comply:

| Practice | Mechanism | Survived? |
|---|---|---|
| Commit and push code | git, and the work is worthless uncommitted | **Yes**, consistently |
| `DECISIONS.md` supersede entries | Reviewed in PRs, cited by later work | **Yes**. D-019, D-020, D-027, D-029, D-032 all exist and are well formed |
| `Boundary` qualifiers on claims | None, habit only | **Yes**, surprisingly. The one voluntary practice that held |
| `WORKLOG.md` append at every milestone | None | **No.** Out of order, and misses `Agent SDLC.md` entirely |
| Five same-turn writes | None | **No.** Config incidents logged hours later |
| `HANDOFF.md` freshness | None | **Partial.** Current as of 23:37, stale by 2 hours at the time I read it |
| `agent-configs` continuous logging | None | **No.** Four incidents today, none in `CORRECTIONS.log` |

The one voluntary practice that held is `Boundary`, and I think the reason is
that it is written *inside* the sentence making the claim rather than in a
separate artifact. It costs one clause at the moment of writing, with no
context-switch. Everything requiring a second write to a second file failed.

**That is a design constraint, not a moral.** §7.2's record must be cheap to
write at the moment of the state transition, or it will go the way of the
worklog. It is also the argument for the pre-push hook in §7.4 over any amount of
additional prose.

### 10.3 Where we agree independently

Agreement between two analyses that did not see each other is the strongest
signal available, and these carried the most weight in §7.

1. **Durable state lives in files and git, not in any agent's context.** Its
   phrase is "handoff-first, file-and-git as the source of truth" (line 611). Mine
   is §5.3. Same conclusion, different routes: it reasoned from tool capability,
   I tested each vendor's persistence format for cross-vendor readability.
2. **The problem is state, not memory.** Its core finding (line 12): "Fidelity
   loss between agents isn't a memory problem — it's a state problem ... Growing
   your knowledge base never fixes the handoff, because the thing that vanished
   was never knowledge." This is the cleanest statement of the point in either
   document, and it independently explains why §4.5's memory servers are the
   wrong tool. **Adopted verbatim as the framing.**
3. **Three layers with different lifespans**: knowledge (`AGENTS.md`, months),
   intent (spec/tasks, weeks), live state (handoff, hours). My §4 treated these
   separately without naming the structure. Its table is better. **Adopted.**
4. **Evidence, not prose, in the Done field.** Its line 58: "'fixed the parser' is
   a claim; 'fixed the parser, `parser.py:88`, commit `a1b2c3d`, fixtures 11/11'
   is a state you can trust." Identical to my §7.2 `DONE` requirement and to
   `rules/verification-law.md`. Three independent derivations.
5. **The successor re-verifies the last Done before building on it.** Its
   four-step takeover, my §7.3 step 6, and `issue-as-spine.md`'s "unforgivable
   protocol violation" rule. Three independent derivations.
6. **Exactly one next action.** Its field 7 and its "NEXT EXACT ACTION" emphasis,
   my `NEXT`, `session-continuity.md`'s `NEXT`.
7. **Sequential beats parallel for one goal stream**; parallel only with
   non-overlapping file ownership via worktrees. Its line 267, my §7.6,
   `rules/worktree-protocol.md`, and Cognition's Principle 2.
8. **Do not trust an agent's self-report; CI is the only thing that cannot be
   fooled.** Its line 64, my §7.4, `verification-law.md`, and MAST Insight 3.
9. **`AGENTS.md` as the single human-edited instruction file, bridged per tool,
   kept short.** Its line 39, my §4.1. It independently notes the Codex
   truncation risk I found in the docs.

Nine independent agreements. Combined with the five in-repo derivations from §2,
the design is not in question. Only the enforcement is.

### 10.4 Where we disagree, adjudicated on evidence

**D-1. Does Claude Code read `AGENTS.md`?**
It says yes, bridged, "Added AGENTS.md support in spring 2026" (line 35). **This
is wrong.** Claude Code's own documentation, accessed 2026-08-28, states: "Claude
Code reads `CLAUDE.md`, not `AGENTS.md`," and prescribes an `@AGENTS.md` import
or `ln -s AGENTS.md CLAUDE.md` (https://code.claude.com/docs/en/memory).
**Adjudication: my finding stands, on the vendor's own current documentation.**
This matters operationally: a repo built on its claim ships an `AGENTS.md` that
Claude Code silently never loads. Filed as F-4.

**D-2. Can Gemini CLI read `AGENTS.md`?**
It says no, "the remaining holdout" (line 36). **This is wrong.** Gemini CLI's
own docs document `context.fileName` taking a list, with
`["AGENTS.md", "CONTEXT.md", "GEMINI.md"]` as the worked example
(`docs/cli/gemini-md.md` at `google-gemini/gemini-cli` `main`, accessed
2026-08-28), and agents.md lists Gemini CLI as supported with that setting.
**Adjudication: my finding stands.** Filed as F-5. Consequence of its version:
you maintain a duplicate `GEMINI.md`, and duplicated rule surfaces drift.

Note both errors run the same direction: it overstates Claude Code's
compatibility and understates Gemini's. That is the signature of training-data
recall rather than a docs read, which is worth knowing when weighing its other
tool claims.

**D-3. Heartbeat lease with a 300-second expiry, versus phase-aware staleness.**
Its point 9 proposes `expires_seconds: 300` with a heartbeat, so that when an
agent disappears the task becomes resumable. **Its own document contradicts this
elsewhere and the contradiction is decisive.** Line 62 records that a clock-based
staleness rule ("no update in 2 hours = abandoned") flagged an overnight GPU run
with 19 hours left as up for grabs, and concludes staleness must be phase-aware.
A 300-second heartbeat is a far more aggressive clock rule than the one it just
rejected, and it would have unclaimed today's fourth incident, the session
stalled on an unanswered approval prompt, inside five minutes.
**Adjudication: adopt its line 62, reject its point 9's bare timer.** §7.2 carries
`PHASE` and `EXPECTED-UNTIL`; a heartbeat may be added later as an input to
staleness, never as the sole criterion. This is the clearest case where the two
halves of its own document disagree and the evidence picks the winner.

**D-4. `CURRENT_STATE.json` as machine-readable state.**
Its G1 section proposes `.agent/CURRENT_STATE.json`. **Rejected**, on
`rules/no-parallel-infrastructure.md` and on evidence. `agent-mesh` already has
`HANDOFF.md`, `WORKLOG.md` and `DECISIONS.md`; `agent-configs` already has the
`STATUS` block; adding a fourth store is the exact pattern that rule was written
against. Its own JSON schema also drops the fields that matter most: no rejected
approaches, no reasoning, no qualifier. A `HANDOFF.md` with a fenced frontmatter
block is machine-parseable enough for a shell check, which is all the enforcement
in §7.4 needs.

**D-5. Adopt an external protocol wholesale** (`agent-work-mem`,
`cli-collaboration`, Beads, `handoff`, `claude-codex-handoff`).
Its "O1/O2 adopt first" recommendations. **Rejected for now**, on two grounds.
First, I could not verify any of them: I did not clone or read them, and its own
star counts and version claims are unverified (§9). Second, and more decisively,
§10.2 shows the binding constraint here is not the absence of a protocol, it is
that five protocols already exist unenforced. Adding a sixth from outside does
not change the compliance rate. Its own warning about Beads applies to the whole
class: "two upgrade-breaking migration regressions were reported against
v1.1.0-rc.1. Pin your version." **Unresolved, not closed:** if the §7.4 check
lands and compliance is still poor, revisiting these is the right next move, and
`handoff` and `claude-codex-handoff` look closest in shape.

**D-6. Full Spec Kit ceremony.**
We agree, and I am recording it because it is a rare case of a source arguing
against its own recommendation: "What to avoid: running full Spec Kit ceremony on
small tasks. It's a harness, not a religion." My §4.2 reaches the same place from
the mechanics: spec-kit's checkbox state cannot represent a mid-task stop.

### 10.5 What it found that I missed

Stated plainly, because these are real additions.

1. **The knowledge / intent / live-state layering** (§10.3 item 3). Better
   structure than anything I had.
2. **`FAILED APPROACHES` with stable IDs** (`F011`, `F012`). I had a `REJECTED`
   field; giving each entry an ID makes it citable from a later handoff, a commit
   message or an issue comment, which is what turns it from a note into a
   record. **Adopted into the template.**
3. **A `DO NOT` field.** Verbatim examples from its point 7: "repeat experiment
   #91", "change KV quantization until T018". This is a negative constraint that
   is not derivable from `REJECTED`: the latter says what failed, the former says
   what is forbidden for reasons that may include cost, scope or a pending
   decision. Neither my draft nor any of the five in-repo formats had it.
   **Adopted.**
4. **`LAST KNOWN GOOD` commit.** My `SHA` field pinned `origin/main` for drift
   detection. Its field pins the last good state *on the working branch*, which
   is what a successor needs to fall back to after a broken mid-edit stop.
   Different purpose, both needed. **Adopted as a second field.**
5. **`CURRENT HYPOTHESIS`.** For a stop in the middle of an investigation rather
   than an implementation, the working hypothesis is the single most expensive
   thing to reconstruct. **Adopted as optional.**
6. **Save on state transitions, never on a timer** (line 61), with the reasoning
   that a timer "writes a snapshot of confusion ... whoever picks that up inherits
   your uncertainty as if it were a decision." I had transition-triggered writes
   from `session-continuity.md` but not this justification for why a timer is
   actively harmful. **Adopted, cited in §6.1.**
7. **Hierarchical retrieval L0 through L5** (point 14). A cold-start reader should
   go `STATE` then `HANDOFF` then decisions then source then event log then raw
   transcript, and only descend when needed. My §7.3 read order was flat.
   **Adopted as the structure of §7.3.**
8. **Archive native transcripts as cold storage, not working memory** (point 15).
   This is the right resolution of a tension I left hanging: §5.1 concludes a
   transcript is never the handoff medium, but its point 15 observes that it is a
   valuable escape hatch for "why exactly did Claude reject approach B" when the
   `REJECTED` entry is too thin. Both are true. **Adopted**, with the caveat that
   Claude Code's docs warn its format "changes between versions," so archiving is
   safe and parsing is not.
9. **A concrete GitHub Actions failover skeleton** triggered on issue label, which
   I had not scoped at all. Useful raw material for §7.4's workflow, though
   unverified as written.

### 10.6 What I covered that it did not

1. **Provenance of every claim.** It cites tool capabilities without access dates,
   and two of those claims are wrong (D-1, D-2). This report's §11 and §9 exist so
   the next reader can check rather than trust.
2. **Vendor hook asymmetry as an enforcement constraint.** It does not mention
   hooks. The finding that Claude Code and Grok Build both expose `StopFailure`
   with a `rate_limit` matcher while Codex and Gemini CLI expose nothing
   equivalent is what forces enforcement to be repo-side rather than harness-side.
   This is the single most load-bearing mechanical fact in §7.4.
3. **The undocumented-qualifier failure class and the `BOUNDARY` countermeasure**
   (§6.2). It has no equivalent field, and this is the failure Mike named
   explicitly.
4. **Concurrent systems writing shared live state** (§6.4). It treats agents as
   sequential within one repo. The Hermes and OpenCode config damage came from two
   *systems* colliding outside any repo, which no field in its schema addresses.
5. **Published failure-mode frequencies.** MAST (arXiv:2503.13657) gives
   measured rates across 1600+ traces; it reasons from practitioner reports only.
6. **The audit of what is already written and unenforced here** (§2, §3.3). It
   proposes a system; it does not check whether one already exists on the machine.
   Four unmerged rules and five existing formats is the actual state of play.
7. **Compaction mechanics as the causal explanation** for losing reasoning while
   keeping the choice (§5.2), from the vendor's own compaction table.

**The union is the answer.** Its layering and field set, my provenance,
enforcement mechanics and qualifier discipline.

### 10.7 Taken, rejected, unresolved

**Taken into §7 and the template:** the state-not-memory framing; the three-layer
model; `FAILED-APPROACHES` with IDs; `DO-NOT`; `LAST-KNOWN-GOOD`;
`CURRENT-HYPOTHESIS`; `STOP-REASON` with its enum; transition-not-timer writes
and the reason; phase-aware staleness (line 61); hierarchical read order; the
70% context trigger as an explicitly unverified heuristic; transcripts as cold
storage; "files are mandatory, paste is optional."

**Rejected, with reason:** its Claude Code AGENTS.md claim (contradicted by
vendor docs, F-4); its Gemini CLI claim (contradicted by vendor docs, F-5); the
300-second heartbeat as sole staleness criterion (contradicted by its own line
61 and by today's stall incident); `CURRENT_STATE.json` as a fourth state store
(no-parallel-infrastructure, and it drops the fields that matter); wholesale
adoption of an external protocol (unverified, and it does not address the actual
constraint, which is compliance rather than format).

**Unresolved, for Mike:**
1. Whether to revisit `handoff` or `claude-codex-handoff` after the §7.4 check
   has run for a week and compliance is measurable. I recommend deciding on data,
   not now.
2. Whether `Agent SDLC.md` moves to `agent-configs` as universal content, per
   `MASTER-GUIDE.md` §1's own boundary rule, or stays in `agent-mesh`. It should
   at minimum be committed somewhere (F-3).
3. Whether the transcript archive in §10.5 item 8 is worth the disk, given four
   harnesses and 30-day default retention in at least Claude Code.
4. Whether `agent-mesh` and `agent-configs` share one `HANDOFF.md` format, which
   §7.2 assumes, or keep two. Sharing costs `agent-mesh` a migration; not sharing
   guarantees drift between two systems on one machine.

---

## 11. Sources

All accessed 2026-08-28.

**Vendor documentation**
- Claude Code memory: https://code.claude.com/docs/en/memory
- Claude Code context window and compaction: https://code.claude.com/docs/en/context-window
- Claude Code sessions: https://code.claude.com/docs/en/sessions
- Claude Code hooks: https://code.claude.com/docs/en/hooks
- Codex AGENTS.md: https://learn.chatgpt.com/codex/agent-configuration/agents-md
- Codex config basics: https://learn.chatgpt.com/codex/config-file/config-basic
- Codex worktrees: https://learn.chatgpt.com/codex/environments/git-worktrees
- Codex hooks: https://learn.chatgpt.com/codex/hooks
- Grok Build CLI reference: https://docs.x.ai/build/cli/reference
- Grok Build sessions: https://docs.x.ai/build/features/sessions
- Grok Build project rules: https://docs.x.ai/build/features/project-rules
- Grok Build hooks: https://docs.x.ai/build/features/hooks
- Gemini CLI at `google-gemini/gemini-cli` `main`: `docs/cli/gemini-md.md`,
  `docs/cli/session-management.md`, `docs/cli/checkpointing.md`,
  `docs/cli/git-worktrees.md`, `docs/cli/auto-memory.md`,
  `docs/hooks/reference.md`, `docs/cli/cli-reference.md`:
  https://github.com/google-gemini/gemini-cli
- GitHub Copilot coding agent: https://docs.github.com/en/copilot/concepts/agents/coding-agent/about-coding-agent

**Conventions and tooling**
- AGENTS.md: https://agents.md/
- GitHub spec-kit at `main`: https://github.com/github/spec-kit
- MCP reference servers and the Memory server: https://github.com/modelcontextprotocol/servers

**Research and practitioner sources**
- Cemri et al., "Why Do Multi-Agent LLM Systems Fail?", arXiv:2503.13657:
  https://arxiv.org/abs/2503.13657
- Anthropic, "Effective context engineering for AI agents", 2025-09-29:
  https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- Walden Yan, Cognition, "Don't Build Multi-Agents", 2025-06-12:
  https://cognition.ai/blog/dont-build-multi-agents
- Codex session persistence, secondary and unconfirmed, see §9.1:
  https://codex.danielvaughan.com/2026/04/13/codex-cli-session-persistence-resume-fork-analytics/

**Local sources, read directly**
- `~/agent-configs`: `MASTER-GUIDE.md`, `DECISIONS.md`, `README.md`,
  `rules/*.md` on `main`, `log/CORRECTIONS.log`, `proposals/*`,
  `prompts/fork-summary-handoff-template.md`,
  `knowledge/agent-sdlc-gap-analysis-2026-08-26.md`
- `~/agent-configs` branch `work/session-continuity-issue-16-clean`, via
  `git show`: `rules/session-continuity.md`, `rules/worktree-protocol.md`,
  `rules/review-independence.md`, `rules/model-routing.md`, `DECISIONS.md`
  D-002 through D-005
- `~/agent-mesh`: `AGENTS.md`, `HANDOFF.md`, `WORKLOG.md`, `DECISIONS.md`,
  `README.md`, `Agent SDLC.md`, `.agent/protocols/issue-as-spine.md`,
  `.agent/protocols/memory-write-discipline.md`, `.gitignore`, `git log`,
  `git status`
- Mike, verbally, 2026-08-28: the day's four incidents and the 42-of-42 gates
  case study
