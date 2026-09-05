# Repository skill candidates

This catalog records reviewed source candidates. It is **not runtime activation
evidence**. Each harness must separately prove discovery, invocation, activation, and
behavior against the exact package revision.

| Skill | Trigger | Source status | Runtime status |
| --- | --- | --- | --- |
| `operating-bounded-agent-lanes` | Steering competes with an admitted goal; process, ownership, harness coupling, or completion evidence needs routing | Repository candidate under issue #36 | Codex, Claude, Pi, Hermes, and other adapters unverified |

## Candidate contract

The skill keeps an admitted critical path active, separates additive steering into
owned lanes, scales process to effect risk, requires isolated writable ownership,
keeps controller execution harness-neutral, verifies exact-current claims, and reports
the operator outcome before internal mechanics.

Its pre-dispatch rule is owned by `redtrades/agent-platform#57`: no subagent or Codex
task starts without the canonical issue hierarchy, Project 12 item/status, session
identity, exact input, owned worktree/paths, effect, done condition, and checkpoint
target. An unavailable Project or any missing field returns `DENY`.

It routes to existing runtime skills where discovered and carries a compact fallback
when they are absent. It grants no capabilities and cannot broaden the requested effect.

## Evidence and provenance

- Package: [operating-bounded-agent-lanes](../.agents/skills/operating-bounded-agent-lanes/SKILL.md)
- Donor/adaptation record: [provenance](../.agents/skills/operating-bounded-agent-lanes/references/provenance.md)
- Pressure fixtures: `tests/skills/fixtures/operating-bounded-agent-lanes.json`
- Deterministic package checks: `python3 tests/skills/test_operating_bounded_agent_lanes.py`

Passing repository checks establish package integrity only. Behavioral verification
requires a fresh target-runtime pressure run using the fixture prompts. A copied file,
catalog entry, symlink, or successful load in another harness proves none of those
runtime states.

## Refresh, rollback, uninstall

Refresh by changing the provenance-pinned candidate in a reviewed issue branch and
rerunning its fixtures. Roll back with the reviewed Git revert for that candidate.
Remove the repository package through a reviewed issue/PR. None of these source actions
installs, activates, disables, or removes a runtime-global skill.
