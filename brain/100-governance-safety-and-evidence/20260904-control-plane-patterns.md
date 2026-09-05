# Control Plane Patterns

Source: agent-platform#CONTROLLER.md

## Overview

The controller is **deterministic software that owns the delivery loop**. It is NOT:
- An LLM persona
- A Project board
- A GitHub Actions workflow
- A prompt

Agents perform bounded phases inside the loop; they do not decide their own authority, acceptance, or promotion.

## Implementation Boundary

### Current Architecture

Bounded Gate C implementation uses:
- **Shared State Authority**: GitHub Contents API (compare-and-swap control-state)
- **Generic Executor**: Replaceable adapter-based harness (OpenCode, Codex, Hermes, etc.)
- **Decision Framework**: Operating Model effect classifier
- **Evidence**: Deterministic gates and receipts

### Historical Reference (Frozen)

Older work (AgentWorkforce Factory, SQLite control-kernel) provides donor/reference evidence only.

**Canonical Authority**: `agent-platform` owns:
- Portable contracts
- Policy evaluator
- Provider and harness adapters
- Deterministic gates
- GitHub projection
- Acceptance proof

**Non-Goal**: Platform must NOT add a second lifecycle engine or ledger beside admitted authority.

## Historical Gate C Proof (Frozen Reference)

### Production Status

Production Gate C is **frozen**. Current baseline and next action in [`START-HERE.md`](START-HERE.md).

### Proven Fixture

**Evidence Chain**:
- Issue #103
- PR #110 (merged)
- Readiness run [33281597637](https://github.com/redtrades/agent-platform/actions/runs/33281597637)
- Gate C run [33281620826](https://github.com/redtrades/agent-platform/actions/runs/33281620826)
- Exact-subject CI run [33281657677](https://github.com/redtrades/agent-platform/actions/runs/33281657677)

### Execution Flow

Run executed admitted packet on controller input `a12d3a6967643f807475b3b851a54af777189d9c`:

```
issue intake
  → CAS claim (fenced)
  → isolated worktree (attempt-owned)
  → committed candidate 9ec4b521316a8fb3a8690e3d8f493551a047f846
  → exact-subject CI (deterministic gates)
  → Reviewer App exact-head approval 5059477980
  → Promoter App expected-head merge 19246a50369c54f2478a02b3f2453ae2372bf5fd
  → issue and Project projection (deterministic)
  → terminal receipt
  → inspected cleanup (authority-preserving)
```

### Receipt Artifacts

Uploaded receipt: `gate-c-receipt-33281620826-1` (artifact ID `9723173013`)

GitHub artifact digest: `sha256:e1fdb8d74df39bcbb0bb49aae970a0fd554dd1b69cb55fb618d94d1950288472`

### Proven Scope

Exactly:
- Issue intake
- CAS claim
- Isolated worktree
- Committed candidate
- CI
- Separate read-only exact review
- Expected-head merge
- Issue and Project projection
- Terminal receipt
- Inspected cleanup

**Verified**: Distinct authenticated Controller, Reviewer, and Promoter App identities.

### Known Gaps

Exactly:
- Repeatability after terminal-state reconciliation
- Clean-host reconstruction
- Provider-neutral multi-harness coverage
- Complete Master Plan scorecard

## Terminal Projection Parity

### Report-Only Evaluator

Deterministic evaluator reconciles exact `PASS` Gate C receipts against supplied issue and Project snapshots.

**Validations**:
- Terminal issue closed with exactly one lifecycle label: `state:done`
- Project item status: `Done`
- Actor and run fields match receipt
- `Branch / Candidate` binds exact candidate, merge, or canonical candidate-to-merge value
- Original input revision is NOT a valid terminal projection

### Network Scope

- Performs no network requests
- Performs no mutations
- Does not create another projection authority
- **Not active in frozen production Gate C workflow**

### Activation Requirements

For activation, requires:
1. **Existing Projector transition** to write terminal label and candidate projection first
2. **Durable typed postcondition receipt** bound to:
   - TaskPacket
   - Terminal Gate C receipt
   - Queried snapshots
   - Producer
   - Candidate
   - Merge

**Until both exist**: Evaluator is deterministic report over explicit snapshots only (not operational).

## Required Input for Every Attempt

Every attempt starts from one **immutable task packet** containing:

### Task Identity

- Task and attempt identifiers
- Attempt generation and lineage
- Run ID and timestamp

### Issue & Dependencies

- Exact issue number and URL
- Dependency inputs (which issues must be closed)
- Blocked-by and depends-on relationships
- Priority and metadata

### Source Revision

- Exact source revision (main branch SHA)
- Owned paths (repository boundaries)
- Branch name derivation (attempt-specific)
- Worktree root

### Objective

- Objective and acceptance criteria
- Non-goals (what is out of scope)
- Definition of done

### Execution Configuration

- Selected role (implementer, reviewer, promoter, controller)
- Provider (OpenCode, Codex, Hermes, Jules)
- Model (freellmapi/auto:notrain, gpt-4, etc.)
- Harness type (OpenCode harness, Codex harness, etc.)
- Required skills and capabilities

### Constraints & Budgets

- Allowed capabilities (read, write, network, compute)
- Effect-policy constraints (DENY, AUTO_READ, AUTO_WRITE, APPROVAL_DESTRUCTIVE)
- Compute budget (time, tokens, API calls)
- Retry limits and expiry

### Output & Attestation

- Required output schema (typed result structure)
- Receipt format and requirements
- Falsifier tests (how to verify result)

## Controller Owned Behavior

The controller (and ONLY the controller) performs these transitions:

1. **Read issue graph and admit work**
   - Only dependency-clear, input-complete work
   - Rejects stale or ambiguous dependencies
   - Fails closed on missing evidence

2. **Atomically claim task and exclusive resources**
   - Compare-and-swap through GitHub Contents API
   - Lease with generation and fence
   - Prevents duplicate ownership

3. **Hydrate isolated workspace**
   - One isolated workspace per attempt
   - At exact admitted revision
   - Worktree-local configuration

4. **Dispatch bounded role phase**
   - Through replaceable harness adapter
   - With scoped provider capability
   - In isolated environment

5. **Persist phase checkpoints and resume**
   - Without duplicating effects
   - Preserving context across interruption
   - Terminal checkpoint on completion/failure

6. **Bind produced artifact to exact inputs**
   - Commit hash to task packet
   - Branch to attempt ID
   - PR to issue
   - Receipt to run

7. **Run deterministic gates as code**
   - CI gates on exact subject
   - Identity validation on exact range
   - Policy evaluation on effect classification
   - No test theater; only real falsifiers

8. **Route exact candidate to distinct read-only reviewer**
   - Exact commit SHA fixed
   - Reviewer has zero write authority
   - Reviewer validates independently
   - Result is typed verdict (pass/needs-fix/reject)

9. **Classify requested effect**
   - Effect: `DENY`, `AUTO_READ`, `AUTO_WRITE`, or `APPROVAL_DESTRUCTIVE`
   - Based on target, operation, scope, reversibility, authority
   - Not based on labels or ceremony
   - Deterministic, fail-closed decision

10. **Ask separate promoter to advance exact reviewed candidate**
    - Only if verdict is PASS
    - Only if HEAD matches review subject
    - Compare-and-swap to expected-head
    - Separate principal with separate credentials

11. **Project resulting state to issue and Project board**
    - From accepted receipts only
    - Deterministic projection
    - Terminal labels and status
    - Candidate/merge binding

12. **Remove or transfer workspace**
    - Without deleting durable authority
    - Preserving receipt and history
    - Atomic cleanup order

## Principals and Boundaries

| Principal | May Do | MUST NOT Do |
|-----------|--------|-------------|
| **Controller** | Admit, lease, sequence, checkpoint, evaluate policy, route phases, bind artifacts | Generate code, review own candidate, mint destructive approval, promote, change candidate |
| **Worker (Implementer)** | Perform bounded role phase in owned workspace, commit to branch | Grant authority, review self, project status, promote, access other workspaces |
| **Reviewer** | Read exact request/candidate/evidence; return typed verdict | Modify candidate, promote, grant authority, change evidence, push/merge |
| **Promoter** | Perform expected-head compare-and-swap after all gates pass | Generate, review, choose different candidate, bypass policy, access other resources |
| **Projector** | Derive issue/Project status from accepted receipts | Decide admission, ownership, review, promotion; access control-state |
| **Mike (Owner)** | Supply intent, approve APPROVAL_DESTRUCTIVE effects | Perform routine claim/retry/review/promotion/cleanup; these are automated |

## App Principal Binding

Gate C mints short-lived installation tokens for three Apps:

### Token Generation

- Commit-pinned GitHub action
- Each action-produced App slug must match separately configured trusted role slug
- Missing, duplicate, shared, or swapped bindings fail closed

### Roles

**Controller App**:
- Owns: Issue, Project, control-state, branch, sequencing calls
- Token scope: Bounded to repository

**Reviewer App**:
- Owns: Exact-candidate inspection, review posting
- Token scope: Read-only to repository
- Post-only: GitHub review objects on exact commit

**Promoter App**:
- Owns: Expected-head merge only
- Token scope: Write to `main` branch only
- Fails closed on: HEAD mismatch, approval absent, review missing

### Projector PAT

Separate, opaque Projector PAT:
- Owns: Project reads and writes only
- NOT an authoritative App principal
- Must differ from all three App tokens
- User-owned Project (may later become Projector App for org-owned Project)

### Agent Subprocesses

Agent subprocesses receive:
- NO controller token
- Scoped provider capability only (opaque reference)
- Isolated environment
- Read-only access to candidate

## Required Evidence Gates

Failed gates return to same valid implementation attempt with context preserved.

**Stale or invalid evidence causes DENY**:
- Stale generations
- Changed candidates
- Missing bindings
- Self-review
- Expired approvals
- Ambiguous effects
- Missing receipt

## Effect Classification

Operation classified by: target, operation, scope, reversibility, and authority.

**NOT by**: Labels, work level, persona, or ceremony.

**Examples**:
- Rotating credentials → APPROVAL_DESTRUCTIVE
- Reading credentials by reference → AUTO_READ
- Bounded spending estimate → AUTO_READ
- Charge/debit → Classified by rollback
- Local deployment with tested rollback → AUTO_WRITE
- Public deployment outside rollback envelope → APPROVAL_DESTRUCTIVE
- Creating workflow run → Classified by effect test
- Changing policy → Classified by effect test
- Promoting memory → Classified by effect test
- Changing code → Classified by effect test

## Fail-Closed Decision Procedure

Controller denies on:
- Missing or stale expected-head
- Missing independent review
- Invalid approval grant
- Uncertain rollback boundary
- Ambiguous authority
- Missing provenance
- Stale evidence
- Contradictory state

**Manual Override**: Exceptional `APPROVAL_DESTRUCTIVE` decision requires receipt identifying:
- Override and approver
- Exact target, operation, scope
- Expiration
- Inputs
- Resulting effect

## Non-Goals

- This control plane does not serve as UI or workflow definition
- It does not assume particular platforms or tools
- It does not specify deployment topology
- It does not handle multi-tenant isolation (single-owner system)
- It does not manage resource accounting (budgets are inputs, not measured)
