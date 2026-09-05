---
id: "PROPOSAL-0001"
title: "One working tree per session — enforce with a session-start lock check"
target: "shared-working-directory-concurrent-checkout"
proposer: "agent:consolidate-corrections-loop"
status: "accepted"
date: "2026-08-24"
decision: "accept"
---

## Insight

`shared-working-directory-concurrent-checkout` has 2 logged violations in
`log/CORRECTIONS.log`, crossing the 2-violation promotion threshold:

- a govcon-factory collision earlier this week (per Mike; no independent
  paper trail found — `DECISIONS.md`/`CHANGELOG.md` searched, no match)
- today's `agent-configs` incident, directly observed: this session had
  `anti-pattern-registry-issue-2` checked out; local `main` briefly
  pointed at another session's commit mid-sequence, because both
  sessions were running git commands against the same literal working
  directory (`~/agent-configs`), not separate clones. Caught via an
  empty `git diff main <branch>` before `origin` was touched — no
  content was lost, but the mechanism that caught it was a manual,
  after-the-fact check, not a guard that would have stopped it from
  happening in the first place.

This machine runs 10-15+ concurrent Claude Code sessions routinely
(`agent-workspace/knowledge/project_shared_account_session_contention`-
tagged material). Distinct from that OAuth/rate-limit contention issue:
this is working-tree-level (checkout, index, HEAD, staged files), not
account-level (auth tokens, session limits). A related but different
failure mode — GPU/disk/model-store contention between full sessions —
is already documented and separately tracked in
`~/agent-reports/software-factory/2026-08-20-report.md` (its "category
7," recommending a resource lockfile read at session start); that
report explicitly notes worktrees don't address *that* failure mode
(GPU/model contention isn't a git conflict). This proposal's failure
mode is the git-checkout-state collision specifically, which worktrees
*do* address.

## Proposed change

**Convention:** a session doing non-trivial multi-step work in a shared
git repo (`agent-configs`, `govcon-factory`, `agent-workspace`, or any
repo under active multi-session use) works in its own `git worktree`,
not the primary checkout — `git worktree add ~/.worktrees/<repo>-<slug>
<branch>` instead of `cd ~/<repo> && git checkout -b <branch>`. The
primary checkout stays on `main`, read-mostly, for sessions that only
need to read current state.

**Enforcement — a session-start lock check**, reusing the lockfile
pattern the 2026-08-20 report already recommended for the GPU/model
case (same shape, different resource):

- On a git-mutating action (branch checkout/create, commit) against a
  repo's **primary checkout** (not a worktree — distinguish via
  `git rev-parse --git-common-dir` vs `--git-dir`; they differ inside a
  worktree, match in the primary checkout), check for
  `.git/agent-session-lock` in that repo.
- No lock, or a lock older than a staleness threshold (e.g. 30 min —
  long enough to not fire on normal pauses, short enough to recover
  from a crashed session without manual cleanup): write
  `session=<id> pid=<pid> claimed=<timestamp>`, proceed.
- A fresh lock held by a *different* session: block the action, surface
  the lock's contents (which session, since when) instead of a bare
  error, and suggest `git worktree add` as the fix.
- Release the lock at session end (a Stop hook) rather than only
  relying on staleness — keeps the common case (clean exit) fast to
  reclaim, staleness is the fallback for crashes/kills.

**Open implementation question, not resolved here** — whether this is a
`PreToolUse` hook on `Bash` (pattern-matching `git checkout|commit|
branch` invocations, consistent with the existing damage-control hook
style) or a `SessionStart` hook that claims/checks the lock once up
front. A `PreToolUse` hook is more precise (catches the actual mutating
command) but adds per-call overhead across every repo, not just shared
ones; `SessionStart` is cheaper but can't re-check mid-session if a
second session starts after the first already claimed the lock. Leaving
this to whoever accepts the proposal — it's an implementation trade-off,
not a judgment call this loop should make for itself.

## Rationale

A written rule alone (the standard `DONT.md` entry) didn't prevent the
2nd occurrence — the govcon-factory incident presumably already had
*some* awareness of the risk, and it happened again today in a
different repo. The pattern that already worked for the analogous
GPU/model-store risk (`~/agent-reports/software-factory/2026-08-20-
report.md` item 4: "a single durable resource-lock file read at session
start") is directly reusable here — same mechanism, scoped to git
working-tree state instead of hardware/model resources. Worth noting
the same report also flags a related, orthogonal gotcha worth reading
before implementing: concurrent `git worktree add` calls can themselves
collide on `.git/config.lock` under load (open Claude Code issue, April
2026) — the fix that's converged on there is `sparse-checkout` scoping
per agent, relevant background for whoever builds this, not a reason to
avoid worktrees.

## Evidence

- `log/CORRECTIONS.log`: both `rule=shared-working-directory-concurrent-checkout` lines (2026-08-24)
- `~/agent-reports/software-factory/2026-08-20-report.md` §"7. No locking between concurrent sessions..." and its worktree/`.git/config.lock` note
- This session's own transcript: local branch `anti-pattern-registry-issue-2` briefly showed tip `91aa16a` with an unexpected parent `c25fb4f`, both absent from anything this session pushed (verified: last push before the collision was `f2c5d15`); `git diff main anti-pattern-registry-issue-2` confirmed empty before the branch was deleted, so no content was actually lost — the report is precise that this was *caught*, not that it was harmless by design

---

## Decision (filled in by whoever accepts or rejects this)

- **Outcome:** accept.
- **Implementation, mechanically simpler than this proposal's own
  session-lock design:** rather than a `.git/agent-session-lock` file with
  a staleness threshold and a `SessionStart`/`PreToolUse` hook, `govcon-factory`
  shipped a pre-commit check
  (`scripts/hooks/checks/03-no-shared-checkout-work-commits.sh`, issue #264,
  merged to `main` `542e944` 2026-08-26) that refuses any `work/*` commit
  made outside a linked `git worktree` — detected via `git rev-parse
  --git-dir` vs `--git-common-dir`, no lock file or session identity
  needed. Paired with `scripts/worktree-for-issue.sh` (issue #269) so every
  session gets an isolated worktree at a canonical path
  (`~/gcf-wt/issue-<N>`) instead of picking its own. Mike's 2026-08-26
  workspace-protocol ruling (one issue = one worktree = one branch = one
  session; uncommitted work you didn't create means stop and report, not
  touch; push early/often; no defensive re-sweeping once inside your own
  worktree) is the behavioral half, codified in `govcon-factory/AGENTS.md`
  "Work queue".
- **Why the simpler mechanism, not this proposal's lock file:** the actual
  collision this proposal names is "two sessions committing in the same
  checkout," which a structural block at commit time prevents directly —
  a session-start lock only prevents a session from *starting* work there,
  and still needs staleness/release handling this doesn't. The open
  implementation question this proposal left ("PreToolUse hook vs
  SessionStart lock") is moot under the shipped design — enforcement is a
  git-level pre-commit check, not a Claude Code hook, so it also protects
  non-Claude-Code agent types with `gh`/git access.
- **Not yet done:** `agent-configs` itself (this repo) has no equivalent
  guard — the same anti-pattern recurred here 2026-08-26 (another
  session's uncommitted `patterns.yaml`/`CORRECTIONS.log` work found
  staged in this shared checkout). Porting the govcon-factory mechanism
  here is a follow-up, not covered by this acceptance.
- **Accepted by:** this session did not author PROPOSAL-0001 (`agent:consolidate-corrections-loop`
  did) — implementing/accepting a different agent's proposal, not
  self-accepting.

**An agent never accepts its own proposal.**
