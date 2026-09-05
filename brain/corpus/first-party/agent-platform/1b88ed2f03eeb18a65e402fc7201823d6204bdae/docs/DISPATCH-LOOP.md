# Dispatch loop

This document describes the selection half of the delivery loop: how eligible
work is chosen and offered a turn. Gate C (`docs/CONTROLLER.md`) executes one
already-admitted packet; nothing previously chose which packet, and this is
that missing step.

It is written so another agent or operator can understand the machinery, its
boundaries, and exactly what still stands between it and an autonomous pass,
without reading chat history.

## Authority boundary

The dispatcher is **not** an authority. It does not claim, lease, promote, or
merge. Gate C performs the control-state claim itself through the GitHub
compare-and-swap in `tools/controller/github_contents_authority.mjs`, so the
dispatcher only decides who is *offered* a turn.

A capacity answer is never ownership. Capacity is evaluated against a snapshot
taken before the race, so it cannot serialize anything; only the remote CAS
can. `tests/controller/four_worker_dispatch.test.mjs` asserts this directly: in
a simultaneous race local capacity admits all four contenders and the CAS
fences three of them with `already-leased`. That capacity-versus-CAS mechanism
is mapped to DFL-010 in the sole
[`DELIVERY-FAILURE-LEDGER.md`](DELIVERY-FAILURE-LEDGER.md); issue #57 is
supporting historical evidence.

## Modules

| Module | Responsibility |
| --- | --- |
| `tools/controller/dispatch_eligibility.mjs` | Pure translation from `gh issue list` JSON into candidates. No I/O. |
| `tools/controller/capacity_policy.mjs` | Pure bounded-admission decision. No I/O. |
| `tools/controller/dispatcher.mjs` | One bounded pass: order, gate, hand off. No sleep, no polling, no retry. |
| `tools/controller/run_dispatch.mjs` | Config-driven entry point; builds the real seams and writes a receipt. |

### Eligibility

A candidate is `ready` when it carries the configured ready label, carries no
blocking label, and is not an excluded type. Defaults:

- ready label `state:ready`;
- blocking labels `state:blocked`, `state:needs-fix`; `state:claimed` is a projection, not a mutex;
- excluded types `type:epic`, `type:program`.

Epics and programs are excluded because an epic is a container: dispatching one
claims a whole branch of the graph as a single attempt with no bounded scope.
The list is configuration, so `excluded_type_labels: []` opts back in.

Dependencies come from body lines containing "depends on" or "blocked by",
resolved against the set of closed issues. A bare `#7` with no dependency
phrase is deliberately not a dependency claim. Priority comes from a
`priority:P<n>` label, defaulting to 9 so unlabelled work sorts last.

### Capacity

`createCapacityPolicy(limits)` bounds `global`, `provider`, `harness`, `model`
and `resource`. Every bound is configuration and an unconfigured dimension is
unlimited, so "four workers" is a policy value rather than a topology.
Malformed limits or claims throw rather than admit. A worker re-presenting a
task it already holds is a replay that consumes no capacity, so a holder cannot
be stranded by its own retry.

### The pass

Ordering is by priority then issue number, never the order GitHub returned, so
a pass is reproducible from its inputs. A skip always carries a stated reason.
An exhausted global bound stops the pass and still accounts for every remaining
candidate; a narrower bound rules out only its own candidate and the queue
keeps draining. One candidate failing does not abandon the pass, and a failed
turn consumes no capacity, so a crash cannot starve the bound.

## Effects are opt-in

`dispatch.dry_run` defaults to **true** and guards execution twice: in a dry
pass the real executor is not constructed at all, and `dispatchOnce` is handed
a stub regardless. A live pass configured without an executor is refused before
any candidate is picked up, rather than claiming work it cannot run.

Run a dry pass first, read the receipt, and only then set `dry_run: false`. A
pass that has never been observed should not be the pass that first merges
something.

## Observed readiness

The historical pre-#103 readiness run [33276631445](https://github.com/redtrades/agent-platform/actions/runs/33276631445)
on controller head `90cb5ff4f2afacb6248d8bd666547b27b12af443` produced a RED
receipt with SHA-256
`fc7f1d3cc8d0995d1af8fe560408cba4962025b1c3c4989525e55a38555c20ff`.
Its reasons were missing Controller, Reviewer, and Promoter principals plus
`no-eligible-issue`; no issue was selected or dispatched.
It was superseded by readiness run
[33281597637](https://github.com/redtrades/agent-platform/actions/runs/33281597637)
and the principal-separated #103 Gate C proof on main `19246a5`.

The queue correction is now explicit rather than unresolved:

- issue [#46](https://github.com/redtrades/agent-platform/issues/46) is
  `state:blocked`. Its [correction comment](https://github.com/redtrades/agent-platform/issues/46#issuecomment-5465033723)
  records that its body is deferred/Todo until the first automatic lifecycle
  and minimum worker pool operate, so it must not be dispatched;
- issue [#103](https://github.com/redtrades/agent-platform/issues/103) is the
  completed first principal-separated canary. Its closed issue still carries a
  stale active queue label, which the terminal-projection parity gate reports;
  the GitHub lister considers only open issues, so the stale label cannot
  redispatch the closed canary;
- issue #29 is an epic and remains excluded by the type guard.

## What is not built

- **Cadence.** One pass is one pass. Nothing schedules it.
- **Capacity dimensions.** The Gate C packet carries no `provider`, `harness`
  or `model` fields, so those bounds are configurable but unpopulated.
- **The autonomous-drain fixture** required by issue #9: a passing candidate
  draining to terminal state, and a seeded review failure returning to the same
  attempt and later draining after correction.

## What blocks the next autonomous pass

The Controller, Reviewer, and Promoter Apps are provisioned and behaviorally
verified by the #103 chain. The next pass does not require a second dispatcher
or controller implementation. Its current preconditions are:

1. **Terminal reconciliation.** Exact completed receipts currently identify
   stale active labels on closed issues #91, #93, and #103. Only the existing
   Projector/projection path may correct them; the parity gate is report-only.
2. **Queue readiness.** A current read-only pass reports no open,
   dependency-clear, non-epic `state:ready` issue. The next canary must be made
   eligible through the issue queue, not by bypassing eligibility or reusing a
   closed fixture.
3. **Execution capacity.** The self-hosted runner and the distinct App/Projector
   bindings must pass readiness again at the exact next input revision.
