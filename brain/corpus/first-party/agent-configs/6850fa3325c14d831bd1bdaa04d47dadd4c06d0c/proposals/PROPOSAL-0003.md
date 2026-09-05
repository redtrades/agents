---
id: "PROPOSAL-0003"
title: "Config-drift sentinel: assert delegation inherit, gateway port, and copy-vs-source sync on a schedule"
target: "scripts/check-config-drift.sh (new, govcon-factory check-* family pattern)"
proposer: "agent:ox-alpha"
status: "open"
date: "2026-08-25"
decision: null
---

## Insight

Three drift classes went undetected on this machine until manually
noticed:

1. **Delegation model pin.** `~/.hermes/config.yaml` carried
   `delegation: {model: qwen3.8, provider: omlx, base_url:
   http://127.0.0.1:8300/v1}` — silently routing every spawned subagent
   to the local MLX server instead of inheriting the chat model.
   Found only when Mike asked why locals were being used (2026-08-25).
   Nothing in any config check flags this class of pin.
2. **Gateway port drift.** MASTER-GUIDE §4 documents FreeLLMAPI must be
   reached on **3100**, not 3101 — meaning something previously drifted
   to 3101 and the lesson was written down as prose, not enforced.
3. **Copy-vs-source fork.** Every `~/.claude/{hooks,commands,skills}`
   install carries SOURCE.md pointing back at `agent-configs`, but no
   mechanism detects when a copy silently diverges from its canonical
   source. The README's own words: "a future update is a deliberate
   re-copy, not a silent fork" — currently that's honor-system.

## Proposed change

A single idempotent script, `check-config-drift.sh`, following the
existing `check-*-*.sh` naming/exit-code conventions in
`govcon-factory/scripts/`:

- **Delegation rail**: fail if `delegation.provider` or
  `delegation.base_url` in `~/.hermes/config.yaml` is non-empty,
  unless a dated DECISIONS entry in the relevant repo records the pin
  as deliberate (grep by date + "delegation").
- **Port assertion**: curl the FreeLLMAPI health endpoint on 3100;
  fail if unreachable while 3101 answers (the known-wrong shape).
- **Fork detection**: for each file with a SOURCE.md or source comment,
  diff against its `agent-configs` canonical path; report drift, don't
  auto-overwrite (a fork may be deliberate — surface it, Mike decides).

Schedule via the existing cron/stale-claim-reaper cadence pattern
(2-hourly was good enough for claim reaping; hourly is fine here — all
checks are local and cheap). Report-only for a first week, then flip to
alerting once the false-positive rate is known.

## Rationale

All three failure modes are silent-by-default config states that
produce wrong *behavior* (wrong model routing, failed calls, stale
guardrails) rather than visible errors. Prose in MASTER-GUIDE already
documents two of them; enforcement converts documentation into a gate,
which is this repo's standing pattern (`rubric-improve`: recurring
judgment → mechanical check).

## Evidence

- Delegation pin found live 2026-08-25; resolution via
  `hermes config unset delegation.{model,provider,base_url}` same day;
  verified against `tools/delegate_tool.py::_resolve_delegation_credentials`
  that empty strings = inherit-parent semantics.
- Port rule: MASTER-GUIDE.md §4 bullet 3.
- Fork risk: agent-configs README "How consumer repos reference this";
  SOURCE.md files present at `~/.claude/hooks/{damage-control,env-file-blocking,purpose-gate}/`.

---

## Decision (filled in by whoever accepts or rejects this)

- **Outcome:** accept | reject
- **If accepted:** commit hash applying the change, referencing this
  proposal's id.
- **If rejected:** reason. Moves to `proposals/rejected/` unchanged
  except this section — a recorded outcome, not a deletion, so the next
  pass doesn't re-litigate it.

**An agent never accepts its own proposal.**
