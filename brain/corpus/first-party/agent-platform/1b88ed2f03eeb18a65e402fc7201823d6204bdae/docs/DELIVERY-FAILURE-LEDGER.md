# Delivery failure ledger

This ledger records observed delivery failures that repeatedly prevented the
first autonomous lifecycle from becoming runnable. It is a prevention index,
not a status report. Every entry names the control that must prevent recurrence.

| ID | Observed failure | Required prevention control |
|---|---|---|
| DFL-001 | A local worktree or uncommitted diff was treated as delivered progress. GitHub could not run or review it. | A viable implementation phase ends with a pushed branch and linked pull request. Otherwise it is explicitly marked disposable or failed. |
| DFL-002 | Research and final-state proof blocked creation of the first executable skeleton. | Create the smallest runnable assembly point first. Add production substitutions behind explicit fail-closed adapter boundaries. |
| DFL-003 | Agents relied on prompt instructions to respect ownership and write boundaries. | Claims, generations, allowed paths, review separation, and promotion are enforced by controller transactions, CI, and credentials. |
| DFL-004 | Agents worked under broad or overlapping roles and changed architecture while assigned implementation or review. | Each phase declares one role, one owned output, allowed effects, forbidden effects, and a typed return envelope. |
| DFL-005 | Checkpoints reported analysis, hashes, or plans without files or executed commands. | Checkpoints are artifact-first: status, files, commands and results, blocker, next action. A bounded phase with no artifact progress releases ownership. |
| DFL-006 | Review findings started a new planning cycle or a new cold session. | Bounded defects return to the same implementation attempt with prior context preserved. A fresh reviewer checks the corrected exact subject. |
| DFL-007 | A reviewer or verifier could repair the work it judged. | Reviewer and verifier phases are read-only. Corrections return to the implementer. |
| DFL-008 | A green test or prose review was treated as whole-lifecycle proof. | Receipts remain scoped. Whole-lifecycle completion requires the complete issue-to-promotion chain and adversarial cases. |
| DFL-009 | Review evidence remained valid after the candidate changed. | Review and promotion bind the exact candidate identity. Changed-head promotion is denied and requires fresh gates and review. |
| DFL-010 | Two agents could race, a stale agent could resume, or cleanup could detach durable authority. | Executable adversarial tests cover exactly-one claim, generation fencing, restart integrity, idempotent effects, and authority-preserving cleanup. |
| DFL-011 | Every new steering request replaced the stable program plan. | Issue #1 remains the sole program queue. New requests update a child issue or status unless Mike explicitly changes the program objective. |
| DFL-012 | Component hardening expanded until it blocked the first integrated run. | Only dependencies exercised by the next runnable lifecycle gate may block that gate. Other hardening continues in parallel. |
| DFL-013 | A destructive-command guard rejected an exact temporary-directory cleanup as categorically forbidden instead of evaluating its target and rollback boundary. | The effect evaluator returns `AUTO_WRITE` for exact attempt-owned disposable cleanup, `APPROVAL_DESTRUCTIVE` for exact effects beyond the proven recovery envelope, and `DENY` only for ambiguous, stale, broad, unsupported, or unauthorized targets. Approval responses name the exact operation, target, scope, revision, recovery consequence, and expiry. |
| DFL-014 | A headless live dispatch initially depended on the runner's ambient GitHub CLI environment, so the intended principal and token binding were not proved before controller effects. The correction history is recorded in [PR #68](https://github.com/redtrades/agent-platform/pull/68). | Bind the scoped `GH_TOKEN` secret explicitly in preflight and execution, set the expected `HOME` and `GH_CONFIG_DIR`, query `gh api user --jq .login` with `GITHUB_TOKEN` removed, and fail closed on any principal mismatch. Never log or copy the token value. |
| DFL-015 | A repository archived during live Action work left the Action cancelled and unavailable as a reliable continuation authority. The cancelled first attempt remains attached to [workflow run 33252536463](https://github.com/redtrades/agent-platform/actions/runs/33252536463/attempts/1). | Treat Action cancellation or archival as an execution failure, not as proof of completion. Preserve the attempt receipt, reacquire the current fenced generation, and resume only from the durable control-state record. A cancelled or unavailable run must never be mistaken for a successful promotion. |
| DFL-016 | The first query after candidate publication found no visible checks even though exact-subject CI later passed, as recorded in the [issue #69 retry checkpoint](https://github.com/redtrades/agent-platform/issues/69#issuecomment-5462387690). | Poll only within a bounded timeout, distinguish `no checks reported` from an actual failed check, revalidate the exact pull-request head before each retry and before accepting green checks, and emit `DENY` with the visibility reason on timeout. |
| DFL-017 | The expired generation-1 attempt could not continue after takeover; the generation-2 attempt resumed against the same input, branch, and candidate. The stale replay denial and continuation are recorded in [issue #69](https://github.com/redtrades/agent-platform/issues/69#issuecomment-5462387690). | Require owner, attempt, generation, input revision, and expected control-state blob on every lease mutation and material effect. Increment generation on takeover, reject stale owners, and preserve the old history/tombstone so a replacement can resume without replaying effects. |
| DFL-018 | The exact-run monitor did not bind its result to the complete run ID, attempt, head SHA, job, conclusion, and receipt tuple, leaving the cancelled attempt, skipped job, and successful retry easy to conflate. Run 33252536463 has distinct attempt-1 and attempt-2 outcomes, while [PR #68's completion record](https://github.com/redtrades/agent-platform/pull/68#issuecomment-5462529094) identifies the accepted receipt. | Monitor the tuple of workflow run ID, attempt, head SHA, job name, conclusion, and receipt artifact. Require the expected attempt's successful job and durable receipt before reporting completion; otherwise retain the failure or unknown state and do not promote. |
| DFL-019 | Completed Gate C issues #91, #93, and #103 were closed and projected to `Done` with exact `PASS` receipts but retained active queue labels. A later dispatcher could therefore read contradictory terminal and eligibility state. | Reconcile exact terminal receipts against issue and Project state with the deterministic terminal-projection parity evaluator. Require exactly `state:done` and an exact candidate, merge, or canonical candidate-to-merge projection. Only the existing Projector transition may clear labels or write Project fields. Do not activate a blocking live postcondition until that writer and a chained parity receipt exist. |
| DFL-020 | A new issue #57 worktree inherited the prior issue #103 Git author from shared repository configuration. Without correction, the material commit would have been misattributed and rejected only after work was complete. | Configure identity with the worktree-local helper at attempt admission, verify it immediately, and run exact base..head identity validation before publication. Never infer worktree identity from the branch name or shared repository config. |

## Canonical proportional register

This file is the **sole canonical proportional anti-pattern register**. New
failure reports are candidates until their evidence, owner, enforcement, and
falsifier are recorded here; comments, prompts, dashboards, and competing
registries are supporting views only. Existing DFL IDs are stable and are never
renumbered.

### PATTERN-CANDIDATE envelope

Use this compact envelope for a new candidate or an update to an existing
pattern:

```text
PATTERN-CANDIDATE
pattern_id: DFL-<stable id> | AP-<next stable id>
fingerprint: sha256:<64 lowercase hex digest of canonical lower-case kebab-case mechanism>
observed: <incident or evidence locator>
scope: <bounded affected surface>
invariant: <property that must remain true>
enforcement: <controller, CI, credential, or operator-visible control>
falsifier: <test or observation that would disprove the control>
owner: <issue or responsible lane>
status: legacy-unmigrated | observed | proposed | adopted | retired
```

The fingerprint is the SHA-256 digest of the canonical lower-case kebab-case
mechanism, not its prose wording. Before adding an ID, deduplicate by the exact
digest: append new evidence to the existing pattern when the mechanism is the
same, and create a new candidate only when the mechanism or invariant is
materially different.

### Legacy DFL migration status

DFL-001 through DFL-020 are legacy-unmigrated historical rows. Their existing
incident and prevention text remains evidence, but this compact status does not
claim that every legacy row is fully adopted under the `PATTERN-CANDIDATE`
schema. Migrate a legacy row only when its update preserves its stable DFL ID
and records the complete envelope fields plus a current falsifier. Set
`status: adopted` only after the named enforcement and falsifier are current;
otherwise retain `status: legacy-unmigrated`, `observed`, or `proposed`.

### Legacy AP source-to-register mapping

The historical AP-01 through AP-23 source set began in issue
[#57](https://github.com/redtrades/agent-platform/issues/57): its initial table
named AP-01 through AP-20 and later candidate comments named AP-21 through
AP-23.
The table below brings those historical identifiers into this sole register
without copying their comment history or treating the issue as a competing
register. `Mapped` means the source mechanism has the same normalized mechanism
as an existing DFL. `Legacy-unmigrated` means the identifier is preserved here
but requires a complete `PATTERN-CANDIDATE` envelope before it becomes an
adopted current entry. AP-10 has conflicting historical source uses and remains
unmigrated until one normalized mechanism is selected.

| Historical ID | Minimal source mechanism | Canonical resolution | Status |
|---|---|---|---|
| AP-01 | canonical task record missing | no one-to-one DFL | legacy-unmigrated |
| AP-02 | dispatch before admission | no one-to-one DFL | legacy-unmigrated |
| AP-03 | competing queues or authority | no one-to-one DFL | legacy-unmigrated |
| AP-04 | unpushed work reported as candidate | DFL-001 | mapped |
| AP-05 | proof expands before thin lifecycle | DFL-002 and DFL-012 | mapped |
| AP-06 | custom infrastructure before adoption decision | no one-to-one DFL | legacy-unmigrated |
| AP-07 | split-brain coordination state | DFL-010 | mapped |
| AP-08 | moving main confused with candidate | DFL-009 | mapped |
| AP-09 | component proof reported as system proof | DFL-008 | mapped |
| AP-10 | self-review/wrong-head; later reused for worktree sprawl | no one-to-one DFL | legacy-unmigrated-source-collision |
| AP-11 | disproportionate ceremony | no one-to-one DFL | legacy-unmigrated |
| AP-12 | provider or harness becomes authority | no one-to-one DFL | legacy-unmigrated |
| AP-13 | secret material enters prompt or log | no one-to-one DFL | legacy-unmigrated |
| AP-14 | issue, Project, and receipt drift | DFL-019 | mapped |
| AP-15 | duplicate adapters, branches, or correction worktrees | no one-to-one DFL | legacy-unmigrated |
| AP-16 | steering silently replaces active goal | DFL-011 | mapped |
| AP-17 | status hides outcome/evidence/next action | no one-to-one DFL | legacy-unmigrated |
| AP-18 | cloud review targets local or unpushed work | DFL-001 | mapped |
| AP-19 | placeholder gate creates test theater | no one-to-one DFL | legacy-unmigrated |
| AP-20 | routine operator action called autonomous | no one-to-one DFL | legacy-unmigrated |
| AP-21 | committed suite absent from workflow | no one-to-one DFL | legacy-unmigrated |
| AP-22 | stale branch point distorts two-dot review diff | no one-to-one DFL | legacy-unmigrated |
| AP-23 | branch, not task checkpoint, governs resume | no one-to-one DFL | legacy-unmigrated |

### Current-ground-truth drift candidates

| ID | Mechanism | SHA-256 fingerprint | Observed evidence | Scope and invariant | Enforcement and falsifier | Owner / status |
|---|---|---|---|---|---|---|
| AP-24 | `stale-ground-truth-poisoning` | `sha256:1112a4b47206244fe71b787e5d3ec75b4fd6a920ff816f42149ff827a5370d57` | [PR #127](https://github.com/redtrades/agent-platform/pull/127) and issue #119 exposed cold-start prose that contradicted the distinct-App Gate C proof. | Governing and cold-start docs name only current authority and accepted gaps; historical material is labeled as evidence. | Cross-document drift checks reject the known stale claims; reintroducing one is the falsifier. | #119 / observed |
| AP-25 | `missing-evidence-authorization` | `sha256:a1675d936f4c2edb881276ec1e4b13466ec5310ec4e6601370bbf15d9eb406dd` | [PR #128](https://github.com/redtrades/agent-platform/pull/128) treated missing or unreadable claim evidence as permission to relabel work. | Missing, malformed, stale, or unreadable authority evidence is `DENY`. | #124 must prove the deny path before any label effect; a missing-evidence mutation is the falsifier. | #124 / observed |
| AP-26 | `snapshot-to-effect-race` | `sha256:d0997798cb8d9993bddafc0a8dd6318f313681417a7f26c12ff15832ab198c76` | [PR #128](https://github.com/redtrades/agent-platform/pull/128) read the wrong control-state subtree and lacked an immediately-pre-effect generation recheck. | A mutable effect binds current authority head, claim identity, owner, attempt, and generation. | #124 must revalidate that tuple immediately before its effect; a changed record reaching mutation is the falsifier. | #124 / observed |
| AP-27 | `component-test-live-topology-mismatch` | `sha256:dc27fb87063f62767021eed6e39c4ffe0a54c67c6f4b6a1247c4770e46ca5a81` | [PR #128](https://github.com/redtrades/agent-platform/pull/128) reported component tests while its live authority topology remained unsafe. | Component tests do not prove the live controller path or effect authority. | Exact workflow/topology tests bind the live adapter to the accepted authority; a green component suite with an unwired live path is the falsifier. | #119, #124 / observed |

### Interruption-safe checkpoints

Before interruption, quota exhaustion, handoff, or lease expiry, the active
attempt writes one issue checkpoint containing **status, files, commands and
results, blocker, and next action**. A candidate checkpoint also binds the
exact input/candidate and checks observed so far. L1 and L2 retain an attempt
only when a durable artifact is pushed and checkpointed: for example, an exact
commit, branch, pull request, receipt, or other repository-visible output.
Checkpoint prose documents a handoff but never substitutes for artifact
progress. Without that artifact, record the blocker and next action, then
release the attempt rather than retaining ownership from chat.

### Proportional work levels

Work level controls ceremony; [`OPERATING-MODEL.md`](OPERATING-MODEL.md)
controls effect authorization. The levels are:

| Level | Use | Required ceremony |
|---|---|---|
| L0 | An owning-issue `PATTERN-CANDIDATE` observation comment with no correction. | Observation/comment only: no branch, pull request, or review. |
| L1 | A nonmaterial correction. | A bounded nonmaterial correction with a focused falsifier test and ordinary CI; no heavyweight independent model review unless the Operating Model separately requires it. |
| L2 | Material code, architecture, or security work. | Affected integration tests, one independent exact-head review, and expected-head promotion only when the Operating Model authorizes it. |

L0 strictly means an owning-issue `PATTERN-CANDIDATE` observation comment with
no correction. L0 is observation/comment only: no branch, pull request, or
review. L1 strictly means a nonmaterial correction with focused deterministic
checks/CI. L1 is a bounded nonmaterial correction with a focused falsifier test
and ordinary CI. L1 does not require heavyweight independent model review unless
the Operating Model separately requires it. L2 material code, architecture, or
security work requires affected integration tests, one independent exact-head
review, and expected-head promotion only when the Operating Model authorizes it.
Deterministic CI remains cheap automatic evidence; it is not removed from a
proportional lane. Review must not expand into unrelated hardening. Work level
controls ceremony only and cannot waive any authorization or review gate
independently required by [`OPERATING-MODEL.md`](OPERATING-MODEL.md).
The operating model still classifies every exact operation as `DENY`,
`AUTO_READ`, `AUTO_WRITE`, or `APPROVAL_DESTRUCTIVE`; an L2 candidate cannot
grant itself authorization.

## Enforcement mapping

- `tools/controller/` plus the focused controller suites prove portions of the
  bounded Gate C controls for DFL-003, DFL-006 through DFL-010, DFL-014,
  DFL-016, and DFL-017. The current principal-separated proof is [Gate C run
  33281620826](https://github.com/redtrades/agent-platform/actions/runs/33281620826)
  for issue #103 and PR #110.
- `tools/controller/terminal_projection_parity.mjs` and its focused CI gate
  enforce the report-only portion of DFL-019 against explicit issue, Project,
  and receipt snapshots. Clearing stale labels, writing terminal Project fields,
  and activating a durable live postcondition remain owned by the existing
  projection and receipt authorities.
- `tools/identity/configure_git_identity.py`, the commit-range validator, and
  their deterministic tests enforce DFL-020 before a candidate is admitted.
- DFL-015 archive/cancellation recovery and DFL-018 exact-run monitoring remain
  observed incident evidence with required controls. No current repository suite
  enforces those controls end to end.
- The role and cookbook work in issues #28, #35, and #36 owns DFL-004 and
  DFL-005.
- Issue #27 and the clean-host acceptance work own production-scale claim,
  fencing, restart, and cleanup coverage beyond the bounded Gate C proof.
- Pull-request admission and issue #39 own exact-subject gate and review
  binding.
- The effect-policy evaluator and runtime adapters own DFL-013. Syntax-only
  command guards may remain defense in depth, but they cannot define platform
  policy.

An entry can be retired only when a current deterministic test or hard control
prevents the failure. A document, prompt, or passing component test alone does
not retire it.
