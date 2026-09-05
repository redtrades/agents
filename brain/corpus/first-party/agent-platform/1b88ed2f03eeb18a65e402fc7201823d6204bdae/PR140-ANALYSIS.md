# PR #140 Analysis: [#137] feat(controller): enforce the Project 12 work-item contract before dispatch

## Current State Summary

### 1. `tools/controller/work_item_contract.mjs` — EXISTS (untracked)
- **Status**: File present in working directory but not committed to git
- **Content**: Full implementation of pure deterministic validator `validateWorkItem` and batch evaluator `evaluateWorkItems`
- **Lines**: 286 lines
- **Exports**:
  - `validateWorkItem(item, options)` — validates a single atomic work item against the Project 12 contract
  - `evaluateWorkItems(items, options)` — batches validation for multiple items, returns eligibility summary
  - `REPORT_SCHEMA` — `'agent-platform.work-item-contract-report/v1'`
  - `SUPPORTED_TYPES` — `Object.freeze(['task'])`
  - `VALID_LIFECYCLE_STATES` — `Object.freeze(['state:ready', 'state:claimed', 'state:review', 'state:needs-fix', 'state:blocked', 'state:done'])`
- **Validation coverage**:
  - GitHub Issue metadata (number, state, labels, body)
  - Native parent issue requirement
  - Project 12 projection (issue_number match, status)
  - Parent issue status check (blocked/needs-fix parents rejected for `state:ready`)
  - Lifecycle-state-specific invariants:
    - `state:ready`: issue must be OPEN, dependencies must be CLOSED, no active unexpired CAS claim
    - `state:claimed`: issue must be OPEN, requires project_item fields (agent_actor, run_id, branch_candidate), live CAS claim, claim owner/run_id/must match project_item
    - `state:review`: issue must be OPEN, requires open PR with valid SHA40 head, candidate branch must include PR head SHA
    - `state:done`: issue must be CLOSED, project status must be 'Done'
  - `deny` function returns `{ eligible: false, reason, details }`
  - `main(argv)` — CLI entry point: `--input <snapshot.json>`, exits 0/1/2 based on eligibility

### 2. `tests/controller/work_item_contract.test.mjs` — MISSING
- **Status**: Not present in working directory
- **Expected**: 349-line test file from commit c5f1db6 covering:
  - Valid state:ready, claimed, review, done tasks pass evaluation
  - Denied cases: missing native parent, missing/project-item mismatch, duplicate/missing lifecycle labels, unsupported types (epic/story), unmet dependencies, blocked parent, active unexpired CAS claim, missing claimed fields, tombstoned CAS, owner/run_id mismatches, expired CAS lease, missing/invalid PR for review, done task with open issue/status mismatch
  - Batch `evaluateWorkItems` aggregation
  - CLI exit code behavior (0 for all-eligible, 1 for ineligible, 2 for malformed input)
  - CI workflow gate registration check

### 3. `.github/ISSUE_TEMPLATE/atomic-task.yml` — EXISTS
- **Status**: Present in working directory
- **Content**: Atomic task issue template with fields for parent, objective, owned-paths, acceptance criteria, dependencies, and pickup-contract
- **Purpose**: Provides the standard issue format for Project 12 atomic tasks

### 4. `.github/workflows/ci-gates.yml` — MODIFIED
- **Status**: Already includes `--gate-json '{"name":"work-item-contract","argv":["node","--test","tests/controller/work_item_contract.test.mjs"]}'`
- **Position**: Added as the last governing-policy gate before the receipt upload step

### 5. Work Tree `work-item-contract-issue-137` — NOT CHECKED OUT
- **Path**: `/Users/man/agent-platform/.worktrees/` is empty
- **Remote**: `remotes/origin/gemini/work-item-contract-issue-137` exists in the repository
- **Purpose**: The associated work tree for this PR was not checked out locally

### 6. Project 12 Contract Specification — `docs/ARCHITECTURE.md`
- Defines the bounded live path: `projected -> discovered -> loaded -> activated -> behaviorally verified`
- GitHub Free private boundary: coordination and evidence surface, not promotion mutex
- Deterministic local gates and receipts may mark a candidate eligible but cannot make direct pushes impossible
- External controller admits operations; independent reviewer evaluates exact candidate; separate expected-head promoter performs eligible promotion

### 7. Existing Validation Patterns in `tools/controller/`
- `dispatch_eligibility.mjs` — builds dispatch candidates from GitHub issues (label-based eligibility)
- `dispatcher.mjs` — one bounded dispatch pass: poll eligible, order deterministically, gate on capacity, hand to executor
- `dispatch_eligibility.buildCandidates()` — translates issues into `{issue_id, task_id, owner, ready, dependencies_met, priority, labels}` candidates
- `gate_c.mjs` — Gate C execution: claims, implements, reviews, promotes with full admission chain
- `github_task_admission.mjs` — validates TaskPacket against GitHub issue, parent hierarchy, Project 12 projection, and accepted-branch revision
- `work_item_contract.mjs` — **new**: pure deterministic validator (no I/O, no network) that enforces the Project 12 atomic task contract before dispatch

### 8. How Work Items Are Currently Dispatched
Flow (without work-item-contract enforcement):
1. `run_dispatch.mjs` → `listIssues()` → `buildCandidates()` → `dispatchOnce()`
2. `buildCandidates()` in `dispatch_eligibility.mjs` filters by: ready label, blocking labels, excluded types, unmet dependencies
3. `dispatchOnce()` in `dispatcher.mjs` orders candidates, checks `ready` and `dependencies_met`, evaluates capacity policy, then builds packet and executes
4. **Gap**: No deterministic work-item contract validation between candidate building and dispatch

Flow **with** work-item-contract enforcement (PR #140 implementation):
1. Same initial steps
2. Before dispatch, each candidate's issue data is validated via `validateWorkItem()` against the Project 12 contract
3. Only eligible items proceed to dispatch
4. Ineligible items are rejected with specific diagnostic reasons (missing parent, unmet dependencies, expired lease, etc.)

### 9. Association with Gate C
- The work-item-contract validation sits **before** Gate C in the dispatch pipeline
- Gate C (`gate_c.mjs`) performs its own admission verification (claim, checkpoint, implementation, review, promotion)
- The work-item-contract ensures the **input** to Gate C conforms to the Project 12 atomic task contract
- This separation: contract validation (deterministic, pure function) → Gate C (stateful, effectful execution)
- CI gate: `work-item-contract` registered in deterministic CI workflow alongside `governing-policy`, `identity-helper`, `identity-range`, `ci-runner-tests`, etc.

### 10. What's Already Implemented vs What Remains

| Component | Status |
|---|---|
| `validateWorkItem` function | ✅ Complete (286 lines) |
| `evaluateWorkItems` function | ✅ Complete |
| `REPORT_SCHEMA`, `SUPPORTED_TYPES`, `VALID_LIFECYCLE_STATES` | ✅ Complete |
| CLI `main` entry point | ✅ Complete |
| `.github/ISSUE_TEMPLATE/atomic-task.yml` | ✅ Complete |
| CI gate registration in `ci-gates.yml` | ✅ Complete |
| `tests/controller/work_item_contract.test.mjs` | ❌ Missing (needs to be created) |
| Local work tree `work-item-contract-issue-137` | ❌ Not checked out |
| Integration with `dispatcher.mjs` / `run_dispatch.mjs` | ⚠️ Not wired (validation exists but not called during dispatch) |

### 11. Recommended Next Steps

1. **Create the test file** `tests/controller/work_item_contract.test.mjs` from commit c5f1db6 to ensure 100% test coverage and CI pass
2. **Checkout/activate the work tree** `work-item-contract-issue-137` if remote tracking is needed
3. **Wire validation into dispatch pipeline**: Modify `run_dispatch.mjs` or `dispatcher.mjs` to call `validateWorkItem` on candidates before dispatch (or create a bridge function)
4. **Run the deterministic CI gate** to verify: `node --test tests/controller/work_item_contract.test.mjs`
5. **Verify the full CI workflow** passes with the work-item-contract gate active