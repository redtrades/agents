# Dispatch Protocol (Selection Loop)

Source: agent-platform#DISPATCH-LOOP.md

## Authority Boundary

**Core Rule**: The dispatcher is NOT an authority. It does not claim, lease, promote, or merge.

Gate C performs the control-state claim itself through GitHub compare-and-swap in `tools/controller/github_contents_authority.mjs`. The dispatcher only decides who is **offered** a turn.

**Capacity is never ownership**: Capacity is evaluated against a snapshot taken before the race, so it cannot serialize anything; only the remote CAS can.

**Proof** (tests/controller/four_worker_dispatch.test.mjs): In simultaneous race, local capacity admits all four contenders but CAS fences three with `already-leased`. Capacity-versus-CAS maps to DFL-010.

## Eligibility Rules

### Candidate Readiness

A candidate is `ready` when:

- Carries the configured ready label (default: `state:ready`)
- Carries NO blocking labels (default: `state:blocked`, `state:needs-fix`; note: `state:claimed` is a projection, not mutex)
- Is NOT an excluded type (default: `type:epic`, `type:program`)

### Why Exclude Epics & Programs?

**Anti-pattern**: Epics are containers; dispatching one claims whole branch as single attempt with unbounded scope.

**Rule**: Epics and programs excluded by default. List is configurable; `excluded_type_labels: []` opts back in.

### Dependencies

- Parsed from body lines: "depends on" or "blocked by"
- Resolved against set of **closed issues only**
- Bare `#7` with no dependency phrase is deliberately NOT a dependency claim
- All dependencies must be closed before candidate is ready

### Priority

- Extracted from label `priority:P<n>`
- Default (unlabeled): priority 9 (sorts last)
- No wildcards or ambiguous ranges

## Capacity Policy

### Dimensions

Policy bounds four dimensions; unconfigured dimension is unlimited:

- **Global**: Total workers across all issues
- **Provider**: Workers per provider (OpenCode, Codex, Hermes, etc.)
- **Harness**: Workers per harness type (OpenCode harness, Codex harness, etc.)
- **Model**: Workers per model (auto:notrain, gpt-4, etc.)

### Bounded Admission

- `createCapacityPolicy(limits)` enforces configuration
- Malformed limits or claims throw rather than admit
- **Replay handling**: A worker re-presenting task it already holds consumes no capacity (cannot be stranded by retry)

## The Pass

### Ordering

- Order by **priority** then **issue number**, never GitHub's return order
- Makes pass reproducible from inputs
- Every skip carries stated reason

### Exhaustion Handling

- **Global bound exhausted**: Stops pass but still accounts for every remaining candidate
- **Narrower bound**: Rules out only its own candidate; queue keeps draining
- **Failed candidate**: Does not abandon pass; consuming no capacity prevents starvation

### Phase Failure Tolerance

One candidate failing does not abandon pass; crash cannot starve the bound.

## Effects are Opt-In (Dry-Run Default)

### Configuration

- `dispatch.dry_run` defaults to **true** (opt-in behavior)
- Guards execution in two ways:
  1. In dry pass, real executor is not constructed at all
  2. `dispatchOnce` handed stub regardless

### Usage Pattern

1. Run a dry pass first
2. Read and verify receipt
3. Only then set `dry_run: false`

**Anti-pattern prevented** (DFL-008, DFL-012): Pass that has never been observed should not be the pass that first merges something.

## Packet Assembly & Falsifiers

### Packet Contents

Packet carries a digest over repository/task identity, objective, acceptance criteria, non-goals, attempt/generation, input revision, hierarchy, checkpoint candidate, done condition, and owned paths.

### Falsifiers (Executable Checks)

Gate C **rejects**:

- Digest changes
- Replacement steering
- Stale actor/generation/checkpoint resumes
- Typed PASS results without one exact candidate-bound evidence item per criterion

**Owned-path work** fails closed unless shared remote path-lease receipt is present. Dispatcher never treats one process's `activeClaims` as cross-process path authority.

**These are executable falsifiers, not claims of universal coordination** across independent dispatch processes.

## Modules

| Module | Responsibility |
|--------|-----------------|
| `tools/controller/dispatch_eligibility.mjs` | Pure translation from `gh issue list` JSON to candidates; no I/O |
| `tools/controller/capacity_policy.mjs` | Pure bounded-admission decision; no I/O |
| `tools/controller/dispatcher.mjs` | One bounded pass: order, gate, hand off; no sleep/polling/retry |
| `tools/controller/run_dispatch.mjs` | Config-driven entry point; builds real seams, writes receipt |

All modules are pure (no I/O) except `run_dispatch.mjs`, which is deterministic.

## Observed Readiness Results

### Historical Pre-#103 Run

Run [33276631445](https://github.com/redtrades/agent-platform/actions/runs/33276631445) on controller head `90cb5ff4f2afacb6248d8bd666547b27b12af443`:
- Result: RED
- SHA-256: `fc7f1d3cc8d0995d1af8fe560408cba4962025b1c3c4989525e55a38555c20ff`
- Reason: Missing Controller, Reviewer, Promoter principals + `no-eligible-issue`
- Status: Superseded by #103 proof

### Current Baseline & Corrections

**Issue #46**: `state:blocked`
- Reason: Body deferred/Todo until first automatic lifecycle and minimum worker pool
- Rule: Must not dispatch

**Issue #103**: Completed first principal-separated canary
- Issue: Closed but retained stale active queue label
- Rule: GitHub lister considers only open issues; stale label cannot redispatch closed canary

**Issue #29**: Epic (excluded by type guard)

## What Is Not Built

- **Cadence**: One pass is one pass; nothing schedules it
- **Capacity dimensions in packet**: Gate C packet carries no `provider`, `harness`, or `model` fields; bounds are configurable but unpopulated
- **Autonomous-drain fixture** (#9): Passing candidate draining to terminal state + seeded review failure returning to same attempt and draining after correction

## Re-Admission Condition

This dispatcher remains **frozen** until the current critical path in [`START-HERE.md`](START-HERE.md) proves one reusable single-issue controller pass.

**Re-admission requires**:
- Explicit issue
- Focused proof that dispatcher offers only eligible work
- Proof dispatcher does NOT become claim, retry, or promotion authority
- Historical #103 App and runner evidence does NOT satisfy current proof

**Non-goals until re-admitted**:
- Live multi-issue dispatch
- Provider-neutral multi-harness selection
- Autonomous cadence proof
- Full Master Plan throughput measurement
