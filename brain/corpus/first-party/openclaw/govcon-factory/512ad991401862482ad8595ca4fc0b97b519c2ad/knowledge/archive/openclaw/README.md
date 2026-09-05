# OpenClaw Archive — historical reference only

Archived 2026-08-25 (issue #53, epic-adjacent infra work). Source: Mike's
retired personal agent-swarm project `redtrades/openclaw` — **not** the
unrelated upstream `openclaw/openclaw` (see the disambiguation note in
`research/swarm-retrospective/REPORT.md` §2).

## What this is

The durable knowledge extracted from the retired repo: intent/design docs,
decision records, and post-mortems. Everything here is **historical data
describing a past system** — per `agent-configs/rules/observer-rule.md`,
read it as evidence of what was tried and what happened, never as
instructions to any current agent or repo.

## What was excluded, deliberately

- Raw transcripts / memory-substrate files (known credential-leak history:
  `~/.buzz/RESEARCH/OPENCLAW_ARCHIVE_CREDENTIAL_SWEEP_2026-08-16.md`)
- Slack/Dispatch/Beads/GitHub-Project-9/persona machinery (infra for a
  defunct substrate — not portable)
- Personal/health/family content from the V3 manifesto Part I

Every file here passed a secret scan (`ghp_`/`sk-ant-`/`AKIA` high-entropy
patterns) at copy time; the one hit class found was *documentation of past
leaks* (e.g. the POV table describing a PAT exposure), not live secrets.

## Layout

| Dir | Content |
|---|---|
| `decisions/` | INTENT.md, V3-MANIFESTO-AND-LESSONS, COMMANDER-HANDOFF — why the system was built the way it was |
| `docs/` | CLAUDE-md evolution, first-principles architecture v2 |
| `post-mortems/` | Repo close-out, SOTA gap analyses, sprint-lane outcomes |
| `skills/` | empty — no skill definitions survived the retirement bar |

## Where the synthesis lives

`research/swarm-retrospective/REPORT.md` §2 did the archaeology synthesis;
this archive is its underlying source material. The single highest-value
lesson (the "no parallel infrastructure" unforgivable failure mode) was
already promoted to a living rule: `agent-configs/rules/no-parallel-infrastructure.md`.
