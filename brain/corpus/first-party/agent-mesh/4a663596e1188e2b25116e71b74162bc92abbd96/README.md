# agent-mesh

One brain, many harnesses. Mike's consolidated agentic system: portable
`.agent/` assets (agents/skills/prompts/protocols/memory), Hermes bot
implementations, the daily-brief + second-brain pipelines, evaluation
harness, and the research corpus behind every design decision.

Built overnight 2026-08-26 from the mined intent of the retired OpenClaw
system (`redtrades/openclaw*` repos — now sanitized archival records),
first-principles SOTA research, and Mike's live direction.

## Map

| Path | What it is |
|---|---|
| `.agent/` | Portable cross-harness layer: personas, skills, prompts, protocols, memory conventions. Works with Claude Code / opencode / pi / Hermes / any OpenAI-compatible harness. See `.agent/AGENTS.md` for adoption into each. |
| `hermes/` | Nous hermes-agent deployment: bot definitions (SOUL.md etc.), routines (cron), model-routing policy, MCP config notes. Bots = profiles under `~/.hermes/profiles/<name>/`. |
| `pipelines/` | Runnable Python (stdlib-only): daily-brief fetchers → synthesis, intake normalizer, council aggregator, vault classifiers, command-center snapshotter. |
| `evals/` | YAML golden cases + stdlib runner + judge protocol (generator ≠ judge). |
| `research/` | Full cited research digests (12 files, ~3k lines) — the evidence base. Start with `research/INDEX.md`. |
| `command-center/` | Static dashboard v1 (SwarmClaw-inspired): snapshot script + single HTML page over sssf.db / hermes state / gh board. |
| `vault/` | Obsidian second-brain taxonomy + auto-sort/link tooling config. |
| `HANDOFF.md` | Read me first if you are a fresh agent picking up work. |
| `WORKLOG.md` | Append-only log of everything done, by whom, when. |
| `DECISIONS.md` | Decision ledger D-001… with rationale + provenance. |

## Governing rules

Universal rules live in `~/agent-configs` (referenced doc-only, zero git
coupling — no submodule, ever). This repo's own working agreement:
`AGENTS.md`.

## Quickstart (Mike)

```sh
# 1. Hermes roster
# The current replacement roster is owned by agent-configs issue #36.
# Read hermes/README.md before using the historical bot install notes.
open hermes/README.md

# 2. Morning brief dry run
python3 pipelines/brief/run.py --dry-run

# 3. Command center
python3 command-center/snapshot.py && open command-center/index.html
```
