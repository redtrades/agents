# Cross-Model Review Protocol

Source: agent-platform#REVIEW-PROTOCOL.md

## Overview

Records active exact-head review path. Issue #103 behaviorally proved separate Controller, Reviewer, and Promoter Apps. This is NOT a provisional shared-login protocol.

## Principal Roles

| Principal | Authority | Constraints |
|-----------|-----------|-------------|
| **Controller App** | Admits review packet | Does NOT review |
| **Read-only Cross-Family Adapter** | Inspects exact candidate | Produces typed result, no repository-write authority |
| **Reviewer App** | Posts authenticated GitHub review | Validates task, identity, exact head, result schema, findings, policy |
| **Promoter App** | Expected-head compare-and-swap | Alone may perform promotion; cannot generate, modify, push, or merge |

## Mandatory Separation Rules

### Rule 1: Generator ≠ Reviewer

**Anti-pattern** (AP-10): Self-review of own work.

**Rule**: `REVIEWER-FAMILY` must NOT equal `AUTHOR-FAMILY`.

**Proof**: Model families tracked in typed verdict. A model family cannot review its own candidate.

### Rule 2: Exact-Subject Binding (DFL-009)

**Anti-pattern**: Review approved SHA X; PR head changed to Y; promotion proceeds on Y anyway.

**Rule**: `COMMIT` SHA must match PR head SHA at time of promotion.

**Enforcement**: 
- Any subsequent push invalidates prior reviews
- Requires fresh review
- Expected-head bind: promote only if `HEAD == review_subject_SHA`

### Rule 3: Read-Only Adapter (DFL-007, DFL-004)

**Rule**: Cross-family adapter has:
- Zero repository-write authority
- Zero push authority  
- Zero merge authority

**Scope**: Read-only inspection only.

### Rule 4: Bounded App Post (DFL-004)

**Rule**: Reviewer App's only review-path write is authenticated GitHub review object after validation.

**Findings Route**: Non-pass findings return to implementation attempt, not PR comment.

## Typed Result Schema

### Required Fields

```text
VERDICT: pass | needs-fix | reject
REVIEWER-FAMILY: codex | claude | gemini | other:<name>
AUTHOR-FAMILY: codex | claude | gemini | other:<name>
COMMIT: <full 40-character git commit SHA>
```

### Field Definitions

#### VERDICT

| Value | Meaning | Binding | Next Action |
|-------|---------|---------|-------------|
| `pass` | Candidate satisfies all parent issue acceptance criteria, passes deterministic tests, introduces no unverified side-effects | Exact 40-char candidate SHA | Reviewer App posts APPROVE on exact head; Promoter may advance |
| `needs-fix` | Bounded defects repairable within same attempt branch | Exact 40-char candidate SHA | Findings return to implementer in same attempt; implementer fixes; fresh review |
| `reject` | Violates architecture, contains stale/ambiguous ownership, or requires new planning cycle | Exact 40-char candidate SHA | Findings return to implementer; decision to close issue or restart is implementer's |

#### REVIEWER-FAMILY

Model family of reviewing agent: `codex`, `claude`, `gemini`, `other:<name>`.

**Enforcement**: Must differ from AUTHOR-FAMILY (Rule 1).

#### AUTHOR-FAMILY

Model family of authoring agent: `codex`, `claude`, `gemini`, `other:<name>`.

**Validation**: Fetched from candidate Git trailers or metadata; reviewed must match claimed.

#### COMMIT

Exact full 40-hex object ID of candidate commit reviewed.

**Validation**: Must match:
- Candidate metadata
- PR head SHA at review time
- PR head SHA at promotion time

**Rule**: Any mismatch between COMMIT and actual head = DENY.

## Non-Pass Findings

### Format (needed-fix and reject)

Line-numbered findings in format:
```
path:line - description
```

**Example**:
```
src/controller.mjs:42 - Missing error handling on git checkout
tests/controller/gate_c.test.mjs:105 - Assertion does not cover stale generation case
```

### Scope

Findings must be **bounded and specific**:
- Actionable (not vague style preferences)
- Scoped to exact candidate
- Within implementer's authority to fix (no architectural rework)

## Proportional Review Threshold

Work level controls **ceremony only**; Operating Model controls **effect authorization**.

| Level | Review Requirement | Custom Model Review |
|-------|-------------------|-------------------|
| **L0** | Observation/comment only | None |
| **L1** | Ordinary CI; focused deterministic checks | None required (waived) |
| **L2** | Affected integration tests + one independent exact-head review | Required |

**Rule**: Work level cannot waive any Operating Model authorization or review gate.

Example: L1 code change still requires Operating Model DENY/AUTO_READ/AUTO_WRITE/APPROVAL_DESTRUCTIVE classification; L1 is ceremony waiver only.

## Evidence Binding

Reviewer App validates and posts GitHub review object with:

- Exact PR number
- Exact commit SHA reviewed (40 hex)
- Verdict (APPROVED, CHANGES_REQUESTED, COMMENTED)
- Findings list (for CHANGES_REQUESTED)
- Timestamp
- Reviewer App identity

**Post Location**: GitHub PR review object (not top-level comment).

## Historical Bootstrap Merges (Pre-Protocol)

The following early PRs merged before protocol enforcement:

- PR #12: `codex/identity-issue-4-v2`
- PR #13: `codex/sota-issue-5`
- PR #14: `codex/master-plan-issue-10-v2`
- PR #33: `codex/policy-docs-issue-20-v2`
- PR #34: `codex/ci-receipts-issue-25-v1`
- PR #37: `codex/identity-gate-issue-21-v1`
- PR #38: `codex/ci-add-range-gate-issue-25-v2`
- PR #41: `codex/start-here-continuity-issue-1`
- PR #47: `codex/lifecycle-issue-27-mvp-v1`
- PR #48: `codex/backend-adoption-conformance-issue-22-v1`

**Enforcement Start**: PR #50 onward.

All pull requests merged after PR #50 enforce this formal cross-model review protocol.

## Implementation Patterns

### For Implementer: Expect Review Round-Trip

1. Submit candidate (branch + PR)
2. Receive review verdict (pass | needs-fix | reject)
3. If `needs-fix`: Fix findings in same branch/attempt; request fresh review
4. If `reject`: Handle decision; do not re-submit same candidate
5. If `pass`: Promoter advances on expected-head

### For Reviewer (Adapter): Typed Result Only

1. Receive exact PR head SHA
2. Inspect candidate in isolation (read-only)
3. Return typed result struct with all four fields
4. Never modify candidate
5. Never push or merge

### For Reviewer App: Validate & Post

1. Validate result struct schema (four fields present, correct types)
2. Validate REVIEWER-FAMILY ≠ AUTHOR-FAMILY
3. Validate COMMIT matches PR head
4. Validate findings (if needs-fix/reject) are line-numbered, bounded
5. Post authenticated GitHub review object
6. Do NOT post to PR comments; use review object API

### For Promoter: Only on PASS + Expected-Head

1. Receive PASS verdict with exact commit SHA
2. Verify PR head == commit SHA
3. Perform expected-head merge (HEAD is expected value)
4. Record merge receipt
5. Release attempt claim

## Defects & Exceptions

### What Requires Fresh Review?

- Any push after review posted
- Rebase onto new base (HEAD changed)
- Merge commit reordering
- Any change to reviewed content

### What Does NOT Require Fresh Review?

- Test-only additions (no source logic changes)
- Comment-only updates (non-semantic)
- Same-as-reviewed commit re-queried for stale runner

## Key Decisions

1. **Separation is enforced, not trusted**: Model family validation in typed result
2. **Exact-head binding is mandatory**: SHA matches at review time AND promotion time
3. **Async and independent**: Reviewer and Promoter run separately after Controller integrates implementer
4. **Findings return home**: Non-pass findings sent to implementer attempt, not PR comment chain
5. **No self-review bridge**: Implementer, Reviewer, Promoter are distinct; no role overlap
