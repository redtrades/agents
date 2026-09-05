# Prompt for all Buzz agents — coordinated unfuck

Paste this to every Buzz/Hermes agent. They coordinate through ONE GitHub issue,
not by editing shared files.

---

## SHARED BRIEF — read fully before any action

You are one of several agents working the same problem at the same time. The
estate is in a death spiral: 30+ PRs merged with zero product completed, 110
`AGENTS.md` files, ~250 stale worktrees, agents re-deriving intent instead of
building. Full diagnosis: `~/agent-reports/death-spiral-rca-2026-09-03/RCA.md`.
Read it. Do not re-diagnose it.

### The single coordination surface

**GitHub issue `redtrades/agent-configs` #WARROOM** (the pinned issue titled
"WAR ROOM — unfuck"). It is the only place you coordinate. You **read every
comment** before acting and **post a comment** before and after every action.
Never coordinate by editing a shared file. Never assume another agent's state —
read their last comment.

### The product goal (this overrides everything)

`GOAL:` __________________  ← Mike fills this in the WAR ROOM issue as the first
comment. Until it is set, only Lane A runs. Every other action must trace to
this goal or it does not happen.

### The meta-freeze (rule 1, no exceptions)

Until GOAL ships, **no agent edits** `AGENTS.md` (any of them), `rules/`,
`skills/`, `hooks/`, `MASTER-GUIDE.md`, `DECISIONS.md`, or anything in
`agent-knowledge-archive/`. Not to "improve coordination," not to "add a rule
that would help." The current state IS the state. If you believe a meta-change
is required, post it in the WAR ROOM and wait for Mike. Do not act.

### WIP = 1

You claim exactly ONE lane. You finish it or post one blocked-reason comment,
then you **stop** — you do not pick up a second lane, you do not "also fix" a
thing you noticed. New lane = new session.

### Claiming protocol

1. Read all WAR ROOM comments.
2. If your intended lane is unclaimed (no "CLAIMED: <lane>" comment in the last
   2 hours without a matching "DONE" or "BLOCKED"), post: `CLAIMED: Lane X —
   <your agent id> — <one-line plan>`.
3. If it is claimed, pick another unclaimed lane or stop.
4. Work only in your lane's write scope. If you need to touch a path outside it,
   stop and post.
5. On completion: `DONE: Lane X — <what changed, links to commits/PRs>`.
6. On block: `BLOCKED: Lane X — <exact reason, what you need>`. Then stop.

### Hard stops — post and stop immediately if any of these

- You have taken more than ~40 tool calls or ~90 minutes on your lane.
- The same command or approach has failed 3 times.
- You find uncommitted work in a checkout you did not create (do not touch it —
  post it).
- Your lane's write scope overlaps another agent's active claim.
- You are about to edit a frozen path (meta-freeze list above).

---

## LANES — claim one

### Lane A — Coordinator (one agent only; does no lane work)

- Confirm Mike has posted `GOAL:` in the WAR ROOM. If not, ask him there, wait.
- Keep a running "STATE" comment (edit your own comment) listing each lane's
  status: unclaimed / claimed-by / done / blocked.
- When a lane posts BLOCKED, either unblock it by reassigning or escalate to
  Mike in the WAR ROOM. Do not do the blocked work yourself.
- Verify each DONE by reading the actual commit/PR, not the claim.
- You never edit code, rules, or repos. You read and coordinate.

### Lane B — Repo collapse

**Write scope:** repo settings + one `ARCHIVED.md` per dead repo. No code edits.
- Set `agent-platform`, `agent-mesh`, `agent-workspace` to archived/read-only on
  GitHub (Settings → Archive), or if Mike wants them kept writable, add a
  top-level `ARCHIVED.md` and a branch-protection rule blocking pushes.
- Confirm each already has the FROZEN banner (merged this week: agent-platform
  #286, agent-mesh #53, agent-workspace #14). If not, that PR is pending — link
  it, do not re-create.
- `govcon-factory`: leave writable but add `ARCHIVED-PENDING-SUCCESSOR.md` per
  the estate decision. Do not archive it without Mike (it is the business).
- Post the final two-repo picture: what is `system`, what is `work`.
- **Do NOT delete any repo. Do NOT touch `agent-configs` or `agent-sdlc`.**

### Lane C — Worktree and branch purge

**Write scope:** worktree removal + branch deletion only. No file edits.
- For each of `agent-configs`, `agent-sdlc`, `agent-platform`, `govcon-factory`,
  `agent-mesh`, `agent-workspace`: `git worktree list`, and for every worktree
  with (a) no uncommitted changes AND (b) no commits ahead of a merged branch
  AND (c) not modified in 3+ days → `git worktree remove`.
- `~/.worktrees/*` — same test, remove the stale ones.
- Delete local and remote branches that are fully merged to `main`
  (`git branch --merged main`), except `preserve/*`.
- **Never** remove a worktree with uncommitted work or unpushed commits — post
  those in the WAR ROOM for Mike.
- Post before/after counts.

### Lane D — Queue consolidation

**Write scope:** GitHub issues/labels in `agent-sdlc` only.
- The MVP task ("format a GitHub reference") is filed 5+ times: #5, #7, #13, #15,
  #31, #42, #45, #49, #55. Pick ONE as canonical, close the rest as duplicates
  pointing at it.
- Close the "reconcile intent" issues (#96, #97, #98, #99, #105) — the intent is
  settled (`MIKE-INTENT-DEBRIEF`, archive 58 decisions). Post a one-line "intent
  is not the blocker" comment on each.
- Label the canonical MVP issue `now`. Every other open issue → `later`.
- Post the resulting queue: exactly one `now` issue.

### Lane E — Ship the GOAL

**Write scope:** the `work` repo's code + tests only (likely `agent-sdlc`).
- Take the ONE `now` issue from Lane D.
- Build the smallest thing that satisfies its acceptance criteria. One worktree.
  Commit early. `npm run verify` (or the repo's verify command) must exit 0.
- Get one review from a different model family (`rules/review-independence.md`).
- Open the PR. If the repo's trusted-host gate owns merge, stop there and post.
- **This is the only lane that produces the product. Protect it — Lanes B/C/D
  must not touch its worktree or its issue.**

### Lane F — Permission deploy (Mike, or an agent in a bypassPermissions session)

- Copy `~/agent-configs/hooks/damage-control/patterns.yaml` →
  `~/.claude/hooks/damage-control/patterns.yaml`.
- In `~/.claude/settings.json` `permissions`: add `"Bash(*)"` to `allow`, delete
  the `"ask"` array, keep `"deny"`.
- Or set autonomous session profiles to `bypassPermissions` mode.
- An agent in a normal session cannot do this (the auto-mode classifier blocks
  editing `~/.claude/`). Post whether it needs Mike.

---

## What "solved" looks like

- WAR ROOM shows every lane `DONE` or a Mike-owned `BLOCKED`.
- Two active repos, the rest archived.
- One `now` issue, WIP=1 in effect.
- Worktree count under ~20 total.
- One PR open against the GOAL, or the GOAL shipped.
- No new `rules/`, `skills/`, `DECISIONS`, or `AGENTS.md` edits since the freeze.

If at the end there is a new rule file or another RCA instead — the freeze was
not held, and that is the finding.
