# Operating model

## Purpose and authority

This document is the single source of truth for the platform's effect policy. GitHub
Issues define intent and acceptance criteria; Git objects identify candidates; receipts
bind admissions, checks, review, decisions, and promotion to exact inputs. The
controller evaluates every requested effect under this policy and fails closed when
evidence is absent, stale, or ambiguous.

## Four-outcome decision table

| Outcome | Meaning | Permitted effect |
| --- | --- | --- |
| `DENY` | The operation is unsupported, prohibited, or not admissible. | No effect. Record the reason. |
| `AUTO_READ` | The operation is admissible and read-only. | Gather and return evidence without mutation. |
| `AUTO_WRITE` | The operation is an admissible, scoped, reversible write within the normal rollback envelope with a bounded budget, bounded audience, valid lease, exact deterministic gates, and independent-review gates. | The controller may perform the eligible write and record its receipt. |
| `APPROVAL_DESTRUCTIVE` | The operation is materially destructive, practically irreversible, or otherwise outside the normal rollback envelope. | An unexpired approval grant is required before the effect. |

## Common admission requirements

Every admitted operation has an exact target, operation, scope, input revision,
actor/run identity, and expected effect. It must have a valid authority path, respect
the owned workspace and capability boundaries, and have enough deterministic evidence
to classify its effect. Missing provenance, stale revisions, ambiguous ownership, or
an unsupported operation produces `DENY`.

## Ceremony is not effect authorization

Work level controls ceremony only. A work-level label cannot waive any
authorization or review gate or change the classification of an exact operation
required by this operating model. The controller still evaluates the target,
operation, scope, reversibility, authority, current deterministic evidence, and
required independent review under the four effect outcomes.

## Principal separation and expected-head promotion

The external controller admits work and evaluates effects. Workers and generators
cannot self-grant authority or self-promote. The independent reviewer assesses the
exact candidate and cannot be its generator. A separate expected-head promoter may
advance only the reviewed candidate whose expected-head still matches the recorded base;
it records the resulting head or fails closed on drift. The Project projector derives
status from these receipts and does not decide admission or promotion. An admitted
`AUTO_WRITE`, including eligible expected-head promotion, does not require a fresh
interactive request. `APPROVAL_DESTRUCTIVE` does require a valid approval grant.

## Effect classification examples

Subject names alone do not determine the outcome. The same subject can have different
effects depending on target, operation, scope, reversibility, and authority. For
example, reading credentials by opaque reference can be `AUTO_READ`, while exposing or
rotating them may require `APPROVAL_DESTRUCTIVE`; a bounded spending estimate can be
`AUTO_READ`, while a charge is classified by its rollback properties. A local
deployment with a tested rollback can be `AUTO_WRITE`, while an externally visible or
public deployment outside the normal rollback envelope can be `APPROVAL_DESTRUCTIVE`.
Creating a workflow run, changing policy, promoting memory, or changing code is
classified by the same effect test rather than its label.

## Approval grant schema

An approval grant binds the exact target, operation, scope, and expiration. Only
Mike/the owner may approve an `APPROVAL_DESTRUCTIVE` grant. No worker, generator,
controller, reviewer, promoter, or projector may issue that grant. It also records the
classified effect, the candidate or input revision, and a receipt identifier. A grant
is invalid for a different target, operation, scope, revision, or time window.

## Fail-closed and manual-override receipts

The controller denies on missing or stale expected-head, missing independent review,
invalid grant, uncertain rollback, or ambiguous authority. A manual override is an
exceptional `APPROVAL_DESTRUCTIVE` decision and must produce a receipt that identifies
the override, approver, exact target, operation, scope, expiration, inputs, and
resulting effect.

## Clean-context decision procedure

In a clean context, classify an operation in this order: `DENY` if unsupported or
prohibited; `APPROVAL_DESTRUCTIVE` only outside the normal rollback envelope;
`AUTO_WRITE` for eligible writes; otherwise `AUTO_READ`.
