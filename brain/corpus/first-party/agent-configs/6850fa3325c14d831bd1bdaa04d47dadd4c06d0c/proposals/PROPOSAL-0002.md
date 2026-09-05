---
id: "PROPOSAL-0002"
title: "Extend damage-control guardrails to Hermes sessions and spawned subagents"
target: "hooks/damage-control/ + Hermes toolset/approval configuration"
proposer: "agent:ox-alpha"
status: "open"
date: "2026-08-25"
decision: null
---

## Insight

The swarm runs on two agent runtimes on this machine — Claude Code and
Hermes Agent — but the damage-control enforcement layer
(`hooks/damage-control/`, `env-file-blocking/`, `block-rm-rf.sh`,
`block-home-root-writes.sh`) is wired **only** into
`~/.claude/settings.json` PreToolUse hooks. A Hermes session (CLI,
desktop, gateway, or any `delegate_task` subagent) executes Bash, Write,
and Edit with none of these guardrails.

Observed directly 2026-08-25: a Hermes desktop session ran all day with
unrestricted shell access — including a flagged `rm -rf` test that was
auto-approved by its smart-approval classifier with no hook in the path.
The same command through Claude Code is hard-blocked exit 2 by
`bash-tool-damage-control.py`. The protection gap is transport-shaped:
the rules exist; one of the two runtimes can't see them.

This violates the repo's own premise (README: universal configs that
"behave the same way whether the working repo is X or Y") — currently
they behave the same only if the runtime is Claude Code.

## Proposed change

Port the same rule logic to Hermes's enforcement surfaces — no new
protection logic, second transport for the existing rules:

1. Audit what Hermes actually offers at the tool-call layer
   (`command_allowlist` exists today in config.yaml; check docs/source
   for PreToolUse-equivalent hooks or plugin points before designing).
2. Wire `damage-control` bash/edit/write checks to fire on Hermes
   tool calls, fail-open on malformed input exactly as the Claude Code
   copies do.
3. Add a drift check to the config-sentinel proposal (PROPOSAL-0003)
   asserting both runtimes' wiring stays in sync with
   `agent-configs/hooks/`.

Open question for whoever implements: whether Hermes subagents inherit
session-level approval config or need it set per-spawn — the
`delegation:` section shows children resolve credentials independently,
so assume nothing.

## Rationale

A guardrail that covers half the fleet's traffic is a partial control,
and the uncovered half (autonomous subagents running unattended) is the
higher-blast-radius half. Extending existing infra matches D-030's
lesson and `rules/no-parallel-infrastructure.md`: same hooks, new
mount point.

## Evidence

- 2026-08-25 session: `rm -rf /tmp/testdir` probe via Hermes terminal
  returned "auto-approved by smart approval" — no hook consulted.
- Same input piped to `~/.claude/hooks/damage-control/bash-tool-damage-control.py`
  directly: blocked, exit 2 (verified same day).
- `~/.claude/settings.json` PreToolUse block: four wired hooks, all
  Claude Code-only by construction.

---

## Decision (filled in by whoever accepts or rejects this)

- **Outcome:** accept | reject
- **If accepted:** commit hash applying the change, referencing this
  proposal's id.
- **If rejected:** reason. Moves to `proposals/rejected/` unchanged
  except this section — a recorded outcome, not a deletion, so the next
  pass doesn't re-litigate it.

**An agent never accepts its own proposal.**
