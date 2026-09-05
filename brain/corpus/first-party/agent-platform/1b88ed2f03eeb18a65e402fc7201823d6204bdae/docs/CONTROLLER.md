# Controller contract

The controller is deterministic software that owns the delivery loop. It is not
an LLM persona, a Project board, a GitHub Actions workflow, or a prompt. Agents
perform bounded phases inside the loop; they do not decide their own authority,
acceptance, or promotion.

## Implementation boundary

The bounded Gate C implementation uses the GitHub Contents API as its shared
compare-and-swap control-state authority and a generic bounded executor. The
older AgentWorkforce Factory and SQLite control-kernel work are donor/reference
evidence, not live lifecycle dependencies. `agent-platform` owns the portable
contracts, policy evaluator, provider and harness adapters, deterministic gates,
GitHub projection, and acceptance proof. The platform must not add a second
lifecycle engine or ledger beside the admitted authority.

## Verified live proof

Issue [#103](https://github.com/redtrades/agent-platform/issues/103), merged
[PR #110](https://github.com/redtrades/agent-platform/pull/110), readiness run
[33281597637](https://github.com/redtrades/agent-platform/actions/runs/33281597637),
Gate C run
[33281620826](https://github.com/redtrades/agent-platform/actions/runs/33281620826),
and exact-subject CI run
[33281657677](https://github.com/redtrades/agent-platform/actions/runs/33281657677)
are the current principal-separated Gate C proof. The run executed the admitted
packet on controller input `a12d3a6967643f807475b3b851a54af777189d9c`
and concluded `PASS` with this chain:

```text
issue intake -> CAS claim -> isolated worktree
  -> committed candidate 9ec4b521316a8fb3a8690e3d8f493551a047f846
  -> exact-subject CI -> Reviewer App exact-head approval 5059477980
  -> Promoter App expected-head merge 19246a50369c54f2478a02b3f2453ae2372bf5fd
  -> issue and Project projection -> terminal receipt -> inspected cleanup
```

The run uploaded receipt artifact `gate-c-receipt-33281620826-1` (artifact ID
`9723173013`) with GitHub artifact digest
`sha256:e1fdb8d74df39bcbb0bb49aae970a0fd554dd1b69cb55fb618d94d1950288472`.

The proven scope is exactly: issue intake, CAS claim, isolated worktree,
committed candidate, CI, separate read-only exact review, expected-head merge,
issue and Project projection, terminal receipt, and inspected cleanup on the
current controller. Readiness and execution verified distinct authenticated
Controller, Reviewer, and Promoter App identities. The exact review and merge
were performed by the Reviewer and Promoter Apps respectively. A separate
Projector credential supplied only the user-owned Project reads and writes.

The gaps are exactly: repeatability after terminal-state reconciliation,
clean-host reconstruction, provider-neutral multi-harness coverage, and the
complete Master Plan scorecard.

Historical proof is preserved. Issue
[#81](https://github.com/redtrades/agent-platform/issues/81), merged
[PR #82](https://github.com/redtrades/agent-platform/pull/82), and Actions run
[33265987993](https://github.com/redtrades/agent-platform/actions/runs/33265987993)
remain the hardened pre-App proof on the PR #74 promotion-serialization base.
Issue
[#69](https://github.com/redtrades/agent-platform/issues/69),
[PR #70](https://github.com/redtrades/agent-platform/pull/70), and merged
[PR #68](https://github.com/redtrades/agent-platform/pull/68) established the
first behaviorally proven `AUTO_WRITE` fixture. The successful
[workflow attempt](https://github.com/redtrades/agent-platform/actions/runs/33252536463/attempts/2)
ran the exact admitted packet on controller head
`37444ecd24b27e0c59ce8de38c213dde44acc89a` with candidate
`6e3699b92d0c080952a3d43e90e41aad958ac3b1` and expected-head merge
`e8f58d56736a99699020da59279b5d60e39af172`.

## Terminal projection parity

The report-only terminal parity evaluator reconciles exact `PASS` Gate C
receipts against supplied issue and Project snapshots. A terminal issue must be
closed with exactly one lifecycle label, `state:done`; its Project item must be
`Done`; actor and run fields must match the receipt; and `Branch / Candidate`
must bind the exact candidate, merge, or canonical candidate-to-merge value.
The original input revision is not a valid terminal candidate projection.

The evaluator performs no network or mutation and does not create another
projection authority. It is not active in the live Gate C workflow yet. Live
activation requires the existing Projector transition to write the terminal
label and candidate projection first, plus a durable typed postcondition receipt
bound to the TaskPacket, terminal Gate C receipt, queried snapshots, producer,
candidate, and merge. Until both exist, the proven Gate C workflow remains
runnable and the evaluator is a deterministic report over explicit snapshots.

## Required input

Every attempt starts from one immutable task packet containing at least:

- task and attempt identifiers;
- exact issue and dependency inputs;
- exact source revision and owned paths;
- objective and acceptance criteria;
- selected role, provider, model, harness, and required skills;
- allowed capabilities and effect-policy constraints;
- budgets, expiry, and retry limits; and
- required output and receipt schemas.

## Owned state and behavior

The controller alone performs these transitions:

1. Read the issue graph and admit only dependency-clear, input-complete work.
2. Atomically claim the task and any exclusive resources with a lease,
   generation, and fence.
3. Hydrate one isolated workspace at the exact admitted revision.
4. Dispatch one bounded role phase through a replaceable harness adapter.
5. Persist phase checkpoints and resume without duplicating effects.
6. Bind the produced artifact and Git candidate to exact inputs.
7. Run deterministic gates as code.
8. Route the exact candidate to a distinct read-only reviewer or verifier.
9. Classify the requested effect as `DENY`, `AUTO_READ`, `AUTO_WRITE`, or
   `APPROVAL_DESTRUCTIVE`.
10. Ask the separate promoter to advance only the exact reviewed candidate
    against the expected head.
11. Project resulting state to the issue and Project board from receipts.
12. Remove or transfer the workspace without deleting durable authority.

Failed gates return to the same valid implementation attempt with context
preserved. Stale generations, changed candidates, missing bindings, self-review,
expired approvals, and ambiguous effects fail closed.

## Principals

| Principal | May do | Must not do |
|---|---|---|
| Controller | Admit, lease, sequence, checkpoint, evaluate policy, route phases | Generate code, review its own candidate, or mint destructive approval |
| Worker | Perform the bounded role phase in its owned workspace | Grant authority, review itself, project status, or promote |
| Reviewer or verifier | Read the exact request, candidate, and evidence; return a verdict | Modify the candidate or promote it |
| Promoter | Perform one expected-head compare-and-swap after all required evidence passes | Generate, review, choose a different candidate, or bypass policy |
| Projector | Derive issue and Project status from accepted receipts | Decide admission, ownership, review, or promotion |
| Mike | Supply intent and approve exact beyond-rollback effects | Perform routine claim, retry, review, promotion, or cleanup work |

Gate C mints short-lived installation tokens for the controller, reviewer, and
promoter with a commit-pinned GitHub action. Each action-produced App slug must
match its separately configured trusted role slug; missing, duplicate, shared,
or swapped bindings fail closed. The controller token owns issue, Project,
control-state, branch, and sequencing calls. The reviewer token probes its own
repository access and posts the exact-candidate PR review. Only the promoter
token performs and reconciles the expected-head merge. Because Project 12 is a
user-owned Project, a separate opaque Projector PAT performs only `gh project`
reads and writes; it is not an authoritative App principal and must differ from
all three App tokens. An organization-owned Project may later replace that PAT
with a Projector App after an explicit migration. Agent subprocesses receive
none of these tokens or App private keys. Installation tokens are
probed through repository endpoints; they are not treated as user tokens and
are never sent to `GET /user`.

The readiness workflow may use the separately named
`AGENT_PLATFORM_OBSERVER_TOKEN` for read-only runner and queue observation.
That observer credential is not an execution principal and never fills a
missing controller, reviewer, or promoter token or identity.

## Receipts

Every transition returns a typed receipt bound to the task packet, attempt,
generation, input revision, actor/run, artifact or candidate, and previous
receipt. A later transition rejects missing, stale, inconsistent, expired,
self-reviewed, or changed-subject evidence.

The minimum receipt chain is:

```text
admission -> claim -> workspace -> checkpoint -> candidate -> gates
          -> review -> policy -> promotion -> projection -> teardown/transfer
```

## Acceptance

The controller is not complete because one fixture or component tests pass.
Issue [#27](https://github.com/redtrades/agent-platform/issues/27) remains the
broader lifecycle acceptance gate. It must reproduce the chain on a clean host
and cover two claim contenders, stale generation rejection, interruption and
resume, failed-gate correction, self-review rejection, changed-head promotion
denial, policy hold/deny outcomes, automatic passing promotion, and
authority-preserving cleanup. Live provisioning and behavioral verification of
the separately wired controller, reviewer, and promoter Apps, provider-neutral
execution, and the Master Plan scorecard also remain open acceptance work.
