# Operating Model Principles

Source: agent-platform#OPERATING-MODEL.md

## Core Decision Framework

### Four-Outcome Decision Table

Every operation is classified into exactly one outcome based on target, operation, scope, reversibility, and authority:

| Outcome | Meaning | Permitted Effect | Decision Rules |
|---------|---------|------------------|-----------------|
| `DENY` | Unsupported, prohibited, or not admissible | No effect; record reason | Missing provenance, stale revisions, ambiguous ownership, unsupported operation |
| `AUTO_READ` | Admissible, read-only operation | Gather and return evidence without mutation | No authority violation, evidence is current |
| `AUTO_WRITE` | Admissible scoped reversible write | Perform eligible write; record receipt | Bounded budget, bounded audience, valid lease, exact deterministic gates, independent-review gates present |
| `APPROVAL_DESTRUCTIVE` | Materially destructive or practically irreversible | Requires unexpired approval grant | Outside normal rollback envelope |

**Decision Logic**: In clean context, classify in order: (1) DENY if unsupported/prohibited; (2) APPROVAL_DESTRUCTIVE only outside rollback envelope; (3) AUTO_WRITE for eligible writes; (4) AUTO_READ otherwise.

## Common Admission Requirements

Every admitted operation must have:

- **Exact target**: Specific repository, branch, file, or resource
- **Clear operation**: One defined action type
- **Bounded scope**: Limited surface area and audience
- **Input revision**: Specific commit/version identifier
- **Actor/run identity**: Who/what performed the action
- **Valid authority path**: Authority for the operation exists and is active
- **Owned workspace**: Clearly marked boundaries
- **Capability boundaries**: Defined limits respected
- **Sufficient deterministic evidence**: Missing provenance, stale revisions, or ambiguous ownership = DENY

## Anti-patterns

### Pattern: Ceremony as Authorization (DFL-004, DFL-012)

**Anti-pattern**: Work-level labels or ceremony are treated as authorization gates.

**Rule**: Work level controls ceremony only. A work-level label cannot waive any authorization or review gate required by this operating model. The controller still evaluates:
- Target, operation, scope
- Reversibility 
- Authority
- Current deterministic evidence
- Required independent review

**Evidence**: Issue #103/#110 showed that ceremonial markers did not substitute for actual effect evaluation.

### Pattern: Missing Approval Grants (DFL-013, AP-25)

**Anti-pattern**: Operations outside the rollback envelope proceed without approval.

**Rule**: `APPROVAL_DESTRUCTIVE` operations require an unexpired approval grant signed by Mike (the owner). No worker, generator, controller, reviewer, promoter, or projector may issue such a grant.

**Grant Schema**: Must bind:
- Exact target
- Operation type
- Scope
- Expiration time
- Classified effect
- Candidate/input revision
- Receipt identifier

## Principal Separation

### Mandatory Separation

- **External controller**: Admits work, evaluates effects (cannot self-promote)
- **Workers/generators**: Cannot self-grant authority or self-promote
- **Independent reviewer**: Assesses exact candidate, cannot be its generator
- **Separate expected-head promoter**: Advances only reviewed candidates; fails closed on drift

### Receipt Binding

All decisions produce receipts that record:
- Classified effect outcome
- Candidate/input revision
- Authority path
- Timestamp
- Approver (if APPROVAL_DESTRUCTIVE)

## Fail-Closed Conditions

The controller denies (returns DENY) when:

- Expected-head is missing or stale
- Independent review is missing
- Approval grant is invalid or expired
- Rollback boundary is uncertain
- Authority is ambiguous
- Evidence provenance is missing

**Manual Override**: Exceptional APPROVAL_DESTRUCTIVE decisions are receipted and must record:
- Override identifier
- Approver
- Exact target, operation, scope
- Expiration
- Inputs
- Resulting effect

## Effect Classification Examples

**Key Principle**: Subject names alone do NOT determine outcome. Same subject can have different effects:

- **Reading credentials by opaque reference** → AUTO_READ
- **Exposing or rotating credentials** → APPROVAL_DESTRUCTIVE
- **Bounded spending estimate** → AUTO_READ
- **Actual charge/debit** → Classified by rollback properties
- **Local deployment with tested rollback** → AUTO_WRITE
- **Externally visible/public deployment outside rollback envelope** → APPROVAL_DESTRUCTIVE
- **Creating workflow run** → Classified by effect test, not label
- **Changing policy** → Classified by effect test, not label
- **Promoting memory** → Classified by effect test, not label
- **Changing code** → Classified by effect test, not label

## Key Decision Rules

1. **Failures are closed**: Ambiguity, missing evidence, or stale data = DENY
2. **Authority is specific**: Role, target, and scope must all be exact
3. **Reversibility matters**: Reversible writes within normal envelope = AUTO_WRITE; irreversible = APPROVAL_DESTRUCTIVE
4. **Evidence persists**: All decisions recorded with sufficient provenance to replay
5. **No self-review**: Generator cannot review own work; reviewer cannot generate
6. **Expected-head binding**: Promoter verifies HEAD matches expected before advancing
7. **Receipt audit trail**: Complete chain from intake → decision → effect → promotion

## Non-Goals

- This model does not define workflow UX or ceremony naming
- It does not specify particular tools or platforms
- It does not assume any particular distributed system
- Labels and markers are evidence inputs, not decision makers
