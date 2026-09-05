# agent-workspace

Shared, versioned workspace for Hermes profiles, Buzz agents and Claude.
Git is the coordination mechanism: commits are the messages, conflicts are
detected instead of silently overwritten, history is the audit trail, and
what gets learned survives a change of harness or model.

This is plain files and git. No service runs anywhere. Anything here works
with nothing more than a filesystem and a `git` binary.

Reusable agent assets and their provenance live in a separate source library:
[`redtrades/agent-configs`](https://github.com/redtrades/agent-configs) (private).
Clone it alongside this repository only when needed. Its contents are not
automatically active instructions; select and validate assets through the target
runtime's native discovery and permission mechanisms.

## First thing, every clone

Git does not version `.git/hooks` by default, so the enforcers in
`scripts/hooks/` are inert until you point git at them:

```sh
scripts/bootstrap.sh
```

This is idempotent and takes one line (`git config core.hooksPath
scripts/hooks`). Run it once per clone/checkout. Nothing else here works
without it — a commit that violates the constitution will go through
silently on an un-bootstrapped clone.

## Layout

```
CONSTITUTION.md      five enforced rules — read this first
tasks/                the task board: one file per task
BOARD.md              generated summary of tasks/ — never hand-edit
knowledge/CLAIMS.md    sourced claims — see rule 2
heartbeat/LOG.md       append-only liveness record for the enforcers
scripts/
  bootstrap.sh          point git at the hooks (run once per clone)
  generate-board.sh     regenerate BOARD.md from tasks/*.md
  claim-task.sh          claim an open task (commits the claim)
  release-task.sh        release your own claim back to open
  complete-task.sh       mark a task done (requires --evidence)
  check-stale-claims.sh  find claims past the staleness timeout
  heartbeat.sh            run all enforcers' self-tests, log liveness
  hooks/
    pre-commit            dispatcher — runs every check below
    checks/                one script per constitution rule
tests/
  test-enforcers.sh      proves each enforcer rejects a real violation
```

## Task board

A task is one Markdown file under `tasks/` with YAML frontmatter:

```yaml
---
id: TASK-0001
title: Short description
state: open           # open | claimed | done | blocked | withdrawn
owner: null            # null | "agent:<name>" | "human:<name>"
claimed_at: null       # ISO 8601 UTC, or null
done_definition: |
  Concrete, checkable statement of what "done" means for this task.
evidence: null         # required non-null once state: done
withdrawn_reason: null # required non-null once state: withdrawn
human_decision: null   # HUMAN-ONLY — see constitution rule 5
---

Free-text notes, context, links.
```

**Claiming is a commit.** `scripts/claim-task.sh TASK-0001 agent:buzz-1`
edits `owner`, `state: claimed` and `claimed_at`, then commits. If two
agents race for the same task, the second one to push/commit gets a merge
conflict on that file, not a silently duplicated claim — that's the whole
point of using git instead of a database row.

**Stale claims.** `scripts/check-stale-claims.sh [hours]` (default 4) lists
any `state: claimed` task whose `claimed_at` is older than the timeout, so
a human or another agent can release it back to `open` rather than it
sitting locked forever because the agent that claimed it died.

**Completing** a task is also a commit:
`scripts/complete-task.sh TASK-0001 --evidence "ran X, got Y"` — this is
the only path to `state: done`, and it's what rule 1's enforcer checks.

## Identity convention

Agents commit as `agent:<name>` (`git -c user.name=agent:hermes-buzz-1 -c
user.email=agent@local commit ...`); humans commit as themselves. This is
how rule 5's enforcer tells the two apart. It is a convention, not a
cryptographic guarantee — good enough for a shared workspace with a small,
trusted set of participants, not good enough for an adversarial one.

## Heartbeat

`scripts/heartbeat.sh` runs each enforcer against a known-bad fixture,
confirms it still rejects it, and appends one line per enforcer to
`heartbeat/LOG.md`. Anything that hasn't logged a fresh line in the
staleness window shows up flagged, not silently missing — that's the
lesson from a skill curator that sat dead for twelve days with nothing
noticing. Run it by hand, from cron, from CI — the mechanism doesn't care.
