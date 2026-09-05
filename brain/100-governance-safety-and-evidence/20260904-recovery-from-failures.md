# Recovery from Failures: Delivery Failure Ledger (DFL)

Source: agent-platform#DELIVERY-FAILURE-LEDGER.md

## Ledger Purpose

Records observed delivery failures that repeatedly prevented first autonomous lifecycle from becoming runnable. This is a **prevention index**, not a status report. Every entry names the required control.

## Core Patterns (DFL-001 through DFL-020)

### DFL-001: Unpushed Work as Delivered Progress

**Observed**: Local worktree or uncommitted diff treated as delivered; GitHub could not run or review.

**Prevention Control**: Viable implementation phase ends with pushed branch AND linked pull request. Otherwise explicitly mark disposable or failed.

**Evidence**: Multiple instances in issue lifecycle before push requirement.

### DFL-002: Research Blocking Executable Skeleton

**Observed**: Extensive research/final-state proof prevented creation of smallest runnable assembly point.

**Prevention Control**: Create smallest runnable assembly point first. Add production substitutions behind explicit fail-closed adapter boundaries.

**Rule**: Skeleton-first; hardening in parallel, not sequentially.

### DFL-003: Prompt Instructions vs. Enforcement (AP-03, AP-06)

**Observed**: Agents relied on prompt instructions to respect ownership and write boundaries.

**Prevention Control**: Claims, generations, allowed paths, review separation, and promotion enforced by:
- Controller transactions
- CI gates
- Credential isolation
(Not prompts, not documentation, not advice)

**Scope**: This is the single greatest risk to autonomous delivery.

### DFL-004: Overlapping Roles During Delivery

**Observed**: Agents worked under broad or overlapping roles and changed architecture while assigned implementation or review.

**Prevention Control**: Each phase declares:
- One role (implementer, reviewer, promoter, controller)
- One owned output
- Allowed effects
- Forbidden effects
- Typed return envelope

**Rule**: Read-only review cannot edit; implementer cannot review own work; promoter cannot generate or choose different candidate.

### DFL-005: Checkpoints Without Artifacts (AP-17)

**Observed**: Checkpoints reported analysis, hashes, or plans without files or executed commands.

**Prevention Control**: Checkpoints are **artifact-first**:
1. Status (pass/fail/blocked)
2. Files (code, config, test results)
3. Commands and results (what ran, output, exit codes)
4. Blocker (if stuck)
5. Next action (clear path forward)

**Rule**: Bounded phase with no artifact progress releases ownership. Do not retain from chat.

### DFL-006: Review Findings Start New Cycle

**Observed**: Review findings started new planning cycle or cold session instead of returning to implementer.

**Prevention Control**: Bounded defects **return to the same implementation attempt** with prior context preserved. Fresh reviewer checks the corrected exact subject.

**Rule**: Keep implementer and context alive across review+fix cycle. Do not start new issue/PR.

### DFL-007: Reviewer Repairs Own Findings

**Observed**: A reviewer or verifier could repair the work it judged.

**Prevention Control**: Reviewer and verifier phases are **read-only**. Corrections return to implementer.

**Role Boundary**: Reviewer(verdict) → Implementer(fix) → Reviewer(recheck).

### DFL-008: Green Tests as Whole-Lifecycle Proof (AP-09, DFL-012)

**Observed**: Green test or prose review treated as whole-lifecycle proof.

**Prevention Control**: Receipts remain scoped. Whole-lifecycle completion requires:
- Complete issue-to-promotion chain
- Adversarial cases
- Terminal receipt

**Rule**: Component tests do not prove live controller path or effect authorization.

### DFL-009: Review Evidence Stale After Candidate Change (AP-08)

**Observed**: Review and promotion proceed even after candidate HEAD changes.

**Prevention Control**: Review and promotion bind the **exact candidate identity**. Changed-head promotion denied; requires fresh gates and review.

**Check**: Before promotion, verify `HEAD == review_subject_SHA`.

### DFL-010: Race, Resume, Cleanup Authority Loss (AP-07, AP-10)

**Observed**: Two agents could race; stale agent could resume; cleanup could detach durable authority.

**Prevention Control**: Executable adversarial tests cover:
- Exactly-one claim (CAS fencing)
- Generation fencing
- Restart integrity
- Idempotent effects
- Authority-preserving cleanup

**Test Suite**: `tests/controller/four_worker_dispatch.test.mjs` + `gate_c_workflow.py`.

### DFL-011: Steering Replaces Program Plan

**Observed**: Every new steering request replaced stable program plan in issue #1.

**Prevention Control**: Issue #1 remains sole program queue. New requests:
- Update a child issue, OR
- Update status, BUT
- Only Mike changes program objective

**Rule**: Prevent issue #1 from being reprioritized by ad-hoc requests.

### DFL-012: Hardening Blocks First Run (DFL-002)

**Observed**: Component hardening expanded until blocking first integrated run.

**Prevention Control**: Only dependencies exercised by next runnable lifecycle gate may block that gate. Other hardening continues in parallel.

**Principle**: Thin skeleton first; feather in hardening; do not serialize.

### DFL-013: Destructive-Command Guard Over-Rejects

**Observed**: Guard rejected temporary-directory cleanup as categorically forbidden; did not evaluate target and rollback boundary.

**Prevention Control**: Effect evaluator returns:
- **AUTO_WRITE**: Exact attempt-owned disposable cleanup
- **APPROVAL_DESTRUCTIVE**: Exact effects beyond proven recovery envelope
- **DENY**: Ambiguous, stale, broad, unsupported, or unauthorized targets

**Rule**: Approval responses name exact operation, target, scope, revision, recovery consequence, expiry.

### DFL-014: Ambient GitHub CLI Token Authority (Issue #68)

**Observed**: Live dispatch depended on runner's ambient GitHub CLI environment; intended principal and token binding not proved before controller effects.

**Prevention Control**: Bind scoped `GH_TOKEN` secret explicitly in preflight and execution:
1. Set expected `HOME` and `GH_CONFIG_DIR`
2. Query `gh api user --jq .login` with `GITHUB_TOKEN` removed
3. Fail closed on any principal mismatch
4. Never log or copy token value

**Evidence**: PR #68 correction history.

### DFL-015: Repository Archive During Live Action (Issue #69)

**Observed**: Repository archived during live Action work left Action cancelled and unavailable as continuation authority. Cancelled attempt remained attached.

**Prevention Control**: Treat Action cancellation or archival as **execution failure**, not completion proof:
- Preserve attempt receipt
- Reacquire current fenced generation
- Resume only from durable control-state record
- Cancelled/unavailable run must never be mistaken for successful promotion

**Rule**: Only actual successful promotion evidence counts; administrative state changes do not.

### DFL-016: No Checks Visible Immediately After Publication (Issue #69)

**Observed**: First query after candidate publication found no visible checks even though exact-subject CI later passed.

**Prevention Control**: CI polling must:
1. Only poll within bounded timeout
2. Distinguish `no checks reported` from actual failed check
3. Revalidate exact pull-request head before each retry and before accepting green checks
4. Emit DENY with visibility reason on timeout

**Rule**: Timing is not proof; revalidate continuously.

### DFL-017: Expired Generation Cannot Continue (Issue #69)

**Observed**: Expired generation-1 attempt could not continue after takeover; generation-2 resumed against same input/branch/candidate. Stale replay denial and continuation recorded.

**Prevention Control**: Require on every lease mutation and material effect:
- Owner
- Attempt ID
- Generation
- Input revision
- Expected control-state blob

**Rule**: Increment generation on takeover; reject stale owners; preserve old history/tombstone for resumption without replay.

### DFL-018: Run Monitor Binding

**Observed**: Exact-run monitor did not bind result to complete run ID, attempt, head SHA, job, conclusion, and receipt tuple. Cancelled attempt, skipped job, successful retry easy to conflate.

**Evidence**: Run 33252536463 has distinct attempt-1 and attempt-2 outcomes; PR #68 completion record identifies accepted receipt.

**Prevention Control**: Monitor tuple of:
- Workflow run ID
- Attempt
- Head SHA
- Job name
- Conclusion
- Receipt artifact

**Rule**: Require expected attempt's successful job and durable receipt before reporting completion. Otherwise retain failure/unknown state; do not promote.

### DFL-019: Issue, Project, Receipt Drift

**Observed**: Completed Gate C issues #91, #93, #103 closed and projected to Done with exact PASS receipts but retained active queue labels. Later dispatcher could read contradictory terminal and eligibility state.

**Prevention Control**: Reconcile exact terminal receipts against issue and Project state with deterministic **terminal-projection parity evaluator**:
1. Require exactly `state:done` label
2. Require exact candidate, merge, or canonical candidate-to-merge projection
3. Only existing Projector transition may clear labels or write Project fields
4. Do not activate blocking live postcondition until writer and chained parity receipt exist

**Evidence**: Terminal-projection-parity check in `tools/controller/terminal_projection_parity.mjs`.

### DFL-020: Worktree Inherits Shared Repository Author Identity

**Observed**: New issue #57 worktree inherited prior issue #103 Git author from shared repository config. Material commit would be misattributed without correction.

**Prevention Control**: Configure identity with worktree-local helper at attempt admission:
1. Verify identity immediately
2. Run exact base..head identity validation before publication
3. Never infer worktree identity from branch name or shared repository config

**Evidence**: Tools and tests in `tools/identity/`.

## Current Ground-Truth Drift Candidates

### AP-24: Stale-Ground-Truth-Poisoning

**Evidence**: PR #127, issue #119

**Rule**: Governing and cold-start docs name only current authority and accepted gaps. Historical material labeled as evidence.

**Prevention**: Cross-document drift checks reject known stale claims. Reintroducing one is falsifier.

### AP-25: Missing-Evidence Authorization

**Evidence**: PR #128

**Rule**: Missing, malformed, stale, or unreadable authority evidence is DENY.

**Prevention**: #124 must prove deny path before any label effect. Missing-evidence mutation is falsifier.

### AP-26: Snapshot-to-Effect Race

**Evidence**: PR #128

**Rule**: Mutable effect binds current authority head, claim identity, owner, attempt, generation.

**Prevention**: #124 must revalidate that tuple immediately before effect. Changed record reaching mutation is falsifier.

### AP-27: Component-Test/Live-Topology Mismatch

**Evidence**: PR #128

**Rule**: Component tests do not prove live controller path or effect authority.

**Prevention**: Exact workflow/topology tests bind live adapter to accepted authority. Green component suite with unwired live path is falsifier.

## Proportional Work Levels

Work level controls ceremony only; OPERATING-MODEL.md controls effect authorization.

| Level | Use | Ceremony | Proof Standard |
|-------|-----|----------|-----------------|
| **L0** | Owning-issue observation comment, no correction | Observation/comment only; no branch/PR/review | Comment with pattern fingerprint |
| **L1** | Nonmaterial correction | Focused deterministic checks/CI | Falsifier test + ordinary CI |
| **L2** | Material code, architecture, or security work | Affected integration tests + independent exact-head review + expected-head promotion | Fresh reviewer proof + Operating Model authorization |

**Key Rule**: Work level CANNOT waive any Operating Model authorization or review gate. Effect classification is independent of work level.

## Checkpoint Requirements

Before interruption, quota exhaustion, handoff, or lease expiry, active attempt writes one issue checkpoint containing:

1. **Status**: pass/fail/blocked
2. **Files**: Code, config, test results (artifact-first)
3. **Commands and results**: What ran, output, exit codes
4. **Blocker**: If stuck (clear statement)
5. **Next action**: Clear path forward

**Rule**: L1 and L2 retain attempt only when durable artifact is pushed and checkpointed (exact commit, branch, PR, receipt, or other repository-visible output).

**Checkpoint prose documents handoff but never substitutes for artifact progress.**

## Anti-Pattern Migration

### Legacy DFL Adoption

DFL-001 through DFL-020 are legacy-unmigrated. Existing text is evidence; compact status not yet complete for all entries.

Migrate when updating by preserving stable DFL ID and adding:
- Complete PATTERN-CANDIDATE envelope fields
- Current falsifier
- Set `status: adopted` only after enforcement + falsifier are current

### Legacy AP Source Mapping

Historical AP-01 through AP-23 (issue #57) brought into sole register:

| Historical ID | Mechanism | Resolution |
|---------------|-----------|------------|
| AP-01 | canonical task record missing | legacy-unmigrated |
| AP-04 | unpushed work reported | DFL-001 (mapped) |
| AP-07 | split-brain coordination | DFL-010 (mapped) |
| AP-08 | moving main confused with candidate | DFL-009 (mapped) |
| AP-14 | issue/Project/receipt drift | DFL-019 (mapped) |
| AP-16 | steering silently replaces goal | DFL-011 (mapped) |
| AP-18 | cloud review targets unpushed work | DFL-001 (mapped) |

## Enforcement Mapping

| Control | Enforcement | Evidence |
|---------|-------------|----------|
| DFL-003, DFL-006–DFL-010, DFL-014, DFL-016–DFL-017 | `tools/controller/` + controller suites | Gate C run 33281620826 (#103, PR #110) |
| DFL-019 | `terminal_projection_parity.mjs` | CI gate, report-only |
| DFL-020 | `configure_git_identity.py` + validator | Deterministic tests |
| DFL-015, DFL-018 | Observed incident evidence; no current end-to-end enforcement | Future work |
| DFL-004, DFL-005 | Role and cookbook work (issues #28, #35, #36) | Future deployment |

**Retirement Rule**: Entry can be retired only when deterministic test or hard control prevents failure. Document, prompt, or component test alone does not retire it.
