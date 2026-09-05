# Gas Town on-demand specialists → Hermes `delegate_task` playbook

Not committed yet — drafted 2026-08-17 as part of mapping OpenClaw's
archived agent roster onto Hermes bot mode. Uncommitted so Mike can decide
whether this belongs in this repo, in a Hermes profile's own docs, or
somewhere else before it becomes tracked history subject to this repo's
constitution (see `CONSTITUTION.md` — nothing here claims `state: done`,
so no enforcer should fire either way, but it's still a draft).

## Why these 14 don't become Hermes bot profiles

OpenClaw's `_archive/agents-gastown-2026-06/` holds 19 YAML personas
(Sisyphus, Prometheus, Hephaestus-01 through 06, Scout-01 through 08, plus
homelab-agent/intake-agent/storage-agent) that were deliberately archived
in 2026-06-12 (decision B, GH #2308) — not deleted as cruft. `INTENT.md`
calls them "blueprints, NOT stale code," meant to be spawned lazily,
per-task, and terminated on completion, never run always-on. They were
retired specifically because running an 8-10-agent always-on roster hit a
documented ceiling failure mode (cited from MAST research in
`ADR-001-agent-role-taxonomy.md`).

That constraint — many narrow specialists, spawned on demand, no standing
identity — is exactly what Hermes's `delegate_task` tool already is: an
in-process, ephemeral sub-agent, inherits the parent's toolset (minus a
small blocklist), gets a fresh conversation with no bot-to-bot messaging
overhead, and reports a summary back with no persistent profile, cron job,
credential, or OAuth slot of its own. Giving each of these 14 a standing
Hermes bot profile would be a straight regression to the exact failure
mode they were archived to escape — 14 more profiles sharing the same
credential pool (Hermes caps concurrent leases per shared OAuth credential
at 1 by default), 14 more things to keep isolated from each other, for
roles that were never meant to persist between tasks.

**The correct port is a prompt-template library, not a bot roster.**

## The template

For each role below: when a task's shape matches, call `delegate_task`
with a prompt that opens by naming the role and its one job, same spirit
as the original YAML's `description` field, then the actual task. Don't
build 14 separate skill files or bots for this — a short table like the
one below, referenced from whichever profile is doing the delegating
(most likely wherever Mike is working interactively, or Operator once/if
that role exists), is the whole mechanism.

| Role | One job | Delegate when |
|---|---|---|
| Hephaestus-01 (Primary Coder) | Write new code from a clear spec | A well-scoped feature/file needs writing and the parent shouldn't hold the implementation detail in its own context |
| Hephaestus-02 (Refactor Specialist) | Restructure existing code without changing behavior | A refactor is scoped and mechanical enough to hand off whole |
| Hephaestus-03 (Unit Test Specialist) | Write tests for already-written code | Tests are needed for a change the parent just made or reviewed |
| Hephaestus-04 (Git Ops Specialist) | Branches, commits, PR prep | A git workflow step is mechanical and shouldn't consume the parent's turn |
| Hephaestus-05 (Knowledge Specialist) | Wiki/vault maintenance, distillation | A research-synthesis or wiki-cleanup pass is needed — note: `hermes-research`'s live protocols already cover the ongoing version of this job; only delegate a one-off pass that doesn't belong in that cron cadence |
| Hephaestus-06 (Bug Hunter) | Root-cause a specific failure | A bug needs isolated investigation separate from the fix |
| Scout-01 (Research Lead) | Web search / landscape survey | A parallel research sub-task is genuinely independent of the main thread |
| Scout-02 (Repo Explorer) | Grep/navigate an unfamiliar codebase | Code needs locating before it can be reasoned about, and doing it inline would bloat the parent's context — this is what the `Explore` agent already covers day to day; treat Scout-02 as the same job under a different name, not a second implementation |
| Scout-03 (Health Monitor) | `ps`/disk one-off check | A single ad hoc system check, not a recurring one — recurring health checks belong to the new **Sentinel** bot (see below), not a delegated sub-agent |
| Scout-04 (Security Watcher) | One-off vulnerability scan | Same distinction as Scout-03 — recurring security posture is Sentinel's job now |
| Scout-05 (Drift Detector) | One-off config-drift check | Same distinction — recurring drift detection is Sentinel's `PROTOCOLS/health-check.md` |
| Scout-06 (URL Intake) | Fetch + extract one URL | Already superseded by the live `url-intake` protocol on `hermes-research` for anything recurring; only delegate a genuinely one-off fetch outside that queue |
| Scout-07 (Signal Scorer) | Rank/filter a list | A one-off ranking task, not the micro-SaaS pipeline's ongoing gate (that's `hermes-scout`'s job, already built) |
| Scout-08 (Local Specialist) | Local-inference-heavy work | A task should run against the local model specifically (cost/latency), not the parent's pinned model — pass `--provider`/model context in the delegate prompt |

`homelab-agent`, `intake-agent`, and `storage-agent` are not in the table
above on purpose: `intake-agent` is fully superseded by the live
`url-intake` protocol; `homelab-agent` folds into **Operator**'s scope if
that role gets built (see the main port report — don't stand up a
near-duplicate of Operator for m16-specific work); `storage-agent`
likewise folds into Operator rather than getting its own identity.

## What this playbook is not

It's not a skill file, not a bot, not a cron job. It's a lookup table for
whoever (Claude, orchestrating; or Mike, working directly) is about to
call `delegate_task` and wants the same role-shaped framing OpenClaw's
archived personas already worked out, without re-deriving it from scratch
or re-instantiating them as 14 standing identities that don't need to
stand.
