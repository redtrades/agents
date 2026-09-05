# Start here: agent-platform source of truth

Read this document first. It is the complete cold-start handoff for a new agent,
harness, or human operator. A reader should not need chat history or every other
design document to understand what is being built, what has been decided, what
is working, and what to do next.

Supporting documents contain deeper rationale and schemas. If they conflict
with this document, stop and correct the conflict through issue #1 rather than
silently choosing one.

## What we are building

`agent-platform` is a provider-neutral autonomous software factory. Its first
required outcome is one real delivery loop that runs without Mike performing
routine coordination:

```text
GitHub issue and dependencies
  -> atomic fenced claim
  -> isolated workspace
  -> bounded specialist agent phase
  -> durable checkpoint and resume
  -> exact candidate and deterministic CI evidence
  -> distinct read-only review
  -> effect-policy decision
  -> expected-head automatic promotion
  -> issue and Project projection
  -> teardown or transfer receipt
```

The end state connects Codex, Claude, Gemini, Grok, Jules, Antigravity, Hermes,
Buzz, OpenCode, Pi, FreeLLMAPI, local models, and admitted ACP/A2A/MCP adapters
through one capability and evidence registry. Product factories such as the
knowledge/radar pipeline and business experiments consume this backend. A later
SwarmClaw mobile PWA provides status, evidence, exceptions, and destructive
approvals. These later consumers do not block the first working lifecycle.

## Entry contract

1. **Single work board:** `agent-platform` (this repository) is the sole authoritative
   work board. Demoted repositories and legacy locations (`agent-mesh`, `agent-configs`,
   `agent-workspace`, `govcon-factory`, and `agent-reports`) are strictly read-only
   migration evidence.
2. **Explicit reading only:** An agent may read a legacy path only when an admitted issue
   on this board explicitly names that path.
3. **No legacy deliverables:** A document written into a legacy repository is not a
   deliverable. All deliverables land in this repository as a pull request or as a
   structured issue comment.
4. **No uncommitted path references:** No issue or task packet on this board may cite a
   path unless that path is committed on `main` of the repository that owns it. For
   example, in `govcon-factory`, 23 issues (#438-#460) cited `knowledge/research/winning-proposal-teardown/INDEX.md`
   which never existed on `main`, causing cascading recovery loops. Uncommitted paths must
   never be cited as task context.

## Decisions already made

Do not reopen these decisions without new contradictory evidence and an issue:

1. GitHub issue #1 and its native subissues are the sole program queue.
2. Project 12 is Mike's human view and a derived projection, not a lock or queue.
3. Git objects identify exact source and candidate state. Typed receipts bind
   claims, gates, review, promotion, projection, and teardown.
4. The bounded Gate C path uses the GitHub Contents API as its shared
   compare-and-swap authority and a generic executor. AgentWorkforce Factory and
   Last Light remain challenge/donor evidence. Do not build a second controller.
5. GitHub-hosted Actions run deterministic candidate checks. The bounded live
   Gate C fixture runs on an authorized self-hosted macOS runner; clean-host and
   broader runner portability remain open acceptance work.
6. Agents are replaceable bounded workers. The controller owns sequencing,
   retries, authority, policy, and acceptance.
7. The effect outcomes are exactly `DENY`, `AUTO_READ`, `AUTO_WRITE`, and
   `APPROVAL_DESTRUCTIVE`. Mike is not the routine promotion bottleneck.
8. Stable behavior uses versioned roles, prompts, skills, cookbooks, task
   packets, and typed output envelopes. Hard controls use controller code, CI,
   credentials, permissions, and forge policy, never prompt compliance alone.
9. Legacy `agent-*` repositories and OpenClaw archives are migration evidence,
   not competing authority.
10. The final `agent-swarm` repository decision happens only after the lifecycle,
    clean-host reconstruction, and bounded corpus admission are proven.

## Controller

The controller is deterministic software, not an agent persona, workflow file,
dashboard, or prompt. The bounded live implementation uses GitHub Contents
compare-and-swap control state and a generic executor. AgentWorkforce Factory is
donor/reference evidence, not the live lifecycle dependency. This repository
owns portable contracts, effect policy, provider and harness adapters,
deterministic gates, GitHub projection, and the acceptance proof.

The controller must:

1. admit dependency-clear, input-complete work;
2. claim tasks and resources atomically with lease, generation, and fence;
3. create one isolated workspace at the exact admitted revision;
4. dispatch one bounded role through a replaceable harness adapter;
5. checkpoint and resume without duplicate effects;
6. bind artifacts and candidates to exact inputs;
7. run deterministic checks as code;
8. route the exact candidate to a distinct read-only reviewer or verifier;
9. classify the requested effect;
10. ask a separate promoter to advance only the reviewed expected head;
11. derive issue and Project state from accepted receipts; and
12. clean or transfer the workspace without deleting durable authority.

The full interface and principal table are in [`CONTROLLER.md`](CONTROLLER.md),
but this section is sufficient to understand the boundary.

## Roles and workflow behavior

The verified Disler/SSSF pattern is adopted selectively:

- Orchestrator/dispatcher translates intent, selects a workflow, assigns
  non-overlapping ownership, and integrates results. It does not implement every
  phase itself.
- Scout locates code and evidence read-only.
- Planner creates an implementation plan and does not implement it.
- Builder/implementer changes only its owned paths and returns tested artifacts.
- Reviewer checks the request and exact candidate read-only. It does not fix.
- Independent verifier applies deterministic oracles and returns
  `verified`, `failed`, or `unsure` without write authority.
- Documenter describes the actual accepted diff, not intended future behavior.
- Promoter/controller is a software principal, not an LLM role.
- Known tests, lint, builds, Git operations, and gates are code phases, not a
  tester agent.

Each phase has one role, one owned output, allowed and forbidden effects, and a
typed final envelope. Checkpoints report: status, files, commands and results,
blocker, next action. Failed gates return to the same valid builder attempt with
context preserved. A bounded phase that produces no artifact progress releases
ownership.

## Effect policy

Every requested operation is classified from its exact target, operation,
scope, input revision, actor/run, capability, reversibility, evidence, budget,
audience, and expiry:

| Outcome | Result |
|---|---|
| `DENY` | Unsupported, ambiguous, stale, broad, prohibited, or unauthorized. No effect. |
| `AUTO_READ` | Admissible read-only operation. Execute and record evidence. |
| `AUTO_WRITE` | Scoped reversible write inside the proven rollback envelope with a valid lease, gates, and required review. Execute automatically and record a receipt. |
| `APPROVAL_DESTRUCTIVE` | Exact operation outside the proven recovery envelope. Require Mike's unexpired exact grant before execution. |

Exact attempt-owned disposable cleanup can be `AUTO_WRITE`. A broad or ambiguous
delete is `DENY`. An exact destructive effect beyond the rollback envelope is
`APPROVAL_DESTRUCTIVE`, not categorically forbidden.

Workers cannot grant authority or promote themselves. Reviewers cannot mutate.
The promoter performs one expected-head compare-and-swap only after all current
evidence passes. Changed candidate bytes invalidate prior gates and review.

## Current implementation state

Current as of the principal-separated Gate C proof on `main` at
[`19246a5`](https://github.com/redtrades/agent-platform/commit/19246a50369c54f2478a02b3f2453ae2372bf5fd):

- Accepted `main` has exact-subject deterministic CI for governing policy,
  worktree identity, logical commit-range identity, and the CI receipt runner.
- Issue [#103](https://github.com/redtrades/agent-platform/issues/103), merged
  [PR #110](https://github.com/redtrades/agent-platform/pull/110), readiness run
  [33281597637](https://github.com/redtrades/agent-platform/actions/runs/33281597637),
  Gate C run
  [33281620826](https://github.com/redtrades/agent-platform/actions/runs/33281620826),
  and exact-subject CI run
  [33281657677](https://github.com/redtrades/agent-platform/actions/runs/33281657677)
  are the current behaviorally proven `AUTO_WRITE` lifecycle. The run admitted
  the packet on controller input
  `a12d3a6967643f807475b3b851a54af777189d9c`, atomically claimed the exact
  issue/task in a repository+issue+task-scoped CAS control record, created one
  isolated worktree, ran the credential-free implementer, committed candidate
  `9ec4b521316a8fb3a8690e3d8f493551a047f846`, waited for exact-subject CI,
  accepted Reviewer App exact-head approval review `5059477980`, and merged PR
  #110 through the Promoter App by expected-head control to
  `19246a50369c54f2478a02b3f2453ae2372bf5fd`. It closed issue #103, projected it to
  Done, terminalized the control-state claim, and performed inspected cleanup
  of the attempt worktree. The run uploaded the durable terminal receipt
  artifact `gate-c-receipt-33281620826-1` (artifact ID `9723173013`) with
  GitHub artifact digest
  `sha256:e1fdb8d74df39bcbb0bb49aae970a0fd554dd1b69cb55fb618d94d1950288472`.
  Proven scope: issue intake, CAS claim, isolated worktree, committed
  candidate, CI, separate read-only exact review, expected-head merge, issue
  and Project projection, terminal receipt, and inspected cleanup. Readiness and
  execution verified distinct Controller, Reviewer, and Promoter App identities;
  the user-owned Project remains behind a separate Projector credential.
- Issue [#81](https://github.com/redtrades/agent-platform/issues/81), merged
  [PR #82](https://github.com/redtrades/agent-platform/pull/82), and Actions run
  [33265987993](https://github.com/redtrades/agent-platform/actions/runs/33265987993)
  remain the hardened pre-App lifecycle proof on the PR #74
  promotion-serialization base.
- Issue [#69](https://github.com/redtrades/agent-platform/issues/69),
  [PR #70](https://github.com/redtrades/agent-platform/pull/70), and
  [PR #68](https://github.com/redtrades/agent-platform/pull/68) remain
  historical proof of the first `AUTO_WRITE` fixture: controller head
  `37444ecd24b27e0c59ce8de38c213dde44acc89a`, candidate
  `6e3699b92d0c080952a3d43e90e41aad958ac3b1`, and expected-head merge
  `e8f58d56736a99699020da59279b5d60e39af172` recorded by the [successful
  workflow attempt](https://github.com/redtrades/agent-platform/actions/runs/33252536463/attempts/2);
  the same run's first attempt is preserved as cancelled evidence.
- This is still a bounded fixture on a self-hosted macOS ARM64 runner, not the
  platform scorecard. The gaps are exactly: repeatability after terminal-state
  reconciliation, clean-host reconstruction, provider-neutral multi-harness
  coverage, and the complete Master Plan scorecard. Gate C and readiness use
  distinct controller, reviewer, and promoter App identities and reject shared
  or swapped role bindings. User-owned Project 12 uses a separate Projector PAT
  restricted to `gh project` calls; it is a derived-view credential, not a
  fourth authoritative principal.
- Issue [#27](https://github.com/redtrades/agent-platform/issues/27) and issue
  [#39](https://github.com/redtrades/agent-platform/issues/39) remain the
  governing broader lifecycle and acceptance work. Do not infer their completion
  from this single passing fixture.
- Issue [#117](https://github.com/redtrades/agent-platform/issues/117) is the
  remaining terminal-projection and cleanup gap: it must chain Projector
  readback and exact merged-branch cleanup to the #103 terminal receipt before
  terminal parity is complete.

## Critical path

Do these in order. Do not replace this path with a new research program:

1. Reconcile completed lifecycle receipts against issue and Project state, then
   remove stale active queue labels through the existing projection authority.
2. Repeat the principal-separated bounded Gate C chain on another eligible issue
   and retain exact admission, candidate, review, promotion, projection, and
   teardown receipts.
3. Reproduce that chain from a clean host and exercise interruption, retry, and
   cold resume, then run the
   full adversarial lifecycle owned by issue #27.
4. Prove provider neutrality with the same packet through at least two harnesses
   and two providers, then measure the Master Plan scorecard.
5. Only after those gates resume broader adapters, product consumers, estate
   cleanup, and SwarmClaw in dependency order.

## Failures that must not recur

The **sole canonical proportional anti-pattern register** is
[`DELIVERY-FAILURE-LEDGER.md`](DELIVERY-FAILURE-LEDGER.md). Use its compact
`PATTERN-CANDIDATE` envelope, fingerprint dedupe rule, interruption-safe
checkpoint rule, and L0/L1/L2 matrix when recording or reviewing a new failure.
The most important
rules are:

- Uncommitted local work is not delivered progress.
- Build a runnable assembly point before final-state hardening.
- Prompts guide behavior; controller and CI enforce authority.
- Checkpoints lead with artifacts and executed commands, not plans or hashes.
- Review defects return to the same builder; reviewers do not repair their own findings.
- Component PASS never implies whole-lifecycle PASS.
- Steering updates a child task unless Mike explicitly changes the program goal.
- Only dependencies exercised by the next runnable gate may block that gate.

## Authority and durable state

- Program intent and task graph: issue #1 and native subissues.
- Human status view: Project 12.
- Exact source and candidates: Git objects and pull requests.
- Active owner, generation, fence, and lease expiry: the GitHub Contents
  compare-and-swap control-state record and receipt for the proven Gate C path;
  broader queue/resource authority remains unaccepted.
- Checks, review, policy, promotion, projection, and teardown: typed receipts.
  Gate C now proves this chain for one fixture, not for the whole scorecard.
- Credentials, sessions, caches, provider profiles, runtime databases, model
  files, and large artifacts: outside this repository behind opaque locators.
- Chat, raw transcripts, dashboards, semantic memory, and task summaries:
  retrieval aids only, never execution authority.

## Cold resume procedure

A new agent or harness performs these steps without reading prior chat:

1. Read this file and repository `AGENTS.md`.
2. Read issue #1 and then the selected child issue, dependencies, and latest
   checkpoint.
3. Inspect the exact accepted base, branch, PR, CI runs, review, and pending
   effect in GitHub.
4. Resolve the controller claim, lease, and checkpoint receipt. If absent, do
   not infer ownership from an assignee, label, comment, Project field, session,
   or local worktree.
5. Inspect the recorded workspace before writing. Confirm branch, revision,
   status, owned paths, and concurrent owners.
6. Continue only the next legal critical-path action above. On stale or
   ambiguous state, fail closed and write a correction checkpoint to the owning
   issue.

Cold resume succeeds when the agent can name the objective, exact source,
current attempt owner and fence, completed evidence, pending effect, and next
legal action without transcript recovery.

## Supporting references

These are deeper references, not mandatory sequential reading:

- [`MASTER-PLAN.md`](MASTER-PLAN.md): end-state outcomes, sequence, and scorecard.
- [`ARCHITECTURE.md`](ARCHITECTURE.md): repository and runtime boundaries.
- [`OPERATING-MODEL.md`](OPERATING-MODEL.md): effect-policy details and grants.
- [`CONTROLLER.md`](CONTROLLER.md): controller interface, principals, and receipt chain.
- [`DISPATCH-LOOP.md`](DISPATCH-LOOP.md): work selection, capacity bounds, and why a pass stays inert.
- [`GOAL.md`](GOAL.md): concise outcome statement.
- [`COMMIT-IDENTITY.md`](COMMIT-IDENTITY.md): attribution and exact-range validation.
- [`CI-GATES.md`](CI-GATES.md): current deterministic CI evidence boundary.
- [`GITHUB-FREE-PRIVATE-BOUNDARY.md`](GITHUB-FREE-PRIVATE-BOUNDARY.md): current forge limitations.

Stable changes update this document in the same pull request. Volatile execution
state updates the owning issue immediately. Project 12 is then projected from the
result rather than becoming a second source of truth.
