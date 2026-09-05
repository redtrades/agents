# Cross-Model Review Protocol

This protocol records the active exact-head review path. Issue #103 behaviorally
proved separate Controller, Reviewer, and Promoter Apps; this is not a provisional
shared-login protocol.

The Controller App admits the review packet but does not review. A read-only
cross-family review adapter may inspect the exact candidate and produce a typed
result without repository-write credentials. The Reviewer App validates the task,
identity, exact head, result schema, findings, and required policy before posting an
authenticated GitHub review object. For a passing candidate it posts the GitHub
`APPROVE` event (recorded as `APPROVED`) on that exact head. The Promoter App alone
may perform eligible expected-head promotion; neither the adapter nor the Reviewer
App may change the candidate, push, or merge.

## Proportional review threshold

Work level controls ceremony only; [`OPERATING-MODEL.md`](OPERATING-MODEL.md)
controls effect authorization. L0 is an owning-issue `PATTERN-CANDIDATE`
observation comment with no correction. L0 is observation/comment only: no
branch, pull request, or review. L1 is a nonmaterial correction with focused
deterministic checks/CI. L1 is a bounded nonmaterial correction with a focused
falsifier test and ordinary CI; it has no heavyweight independent model review
unless the Operating Model separately requires it. L2 material code,
architecture, or security work requires affected integration tests, one
independent exact-head review, and expected-head promotion only when the
Operating Model authorizes it. Deterministic CI remains cheap automatic
evidence. Review must not expand into unrelated hardening. Work level cannot
waive any authorization or review gate required by the operating model; this
threshold does not change the four effect outcomes or authorize a write by
itself.

---

## 1. Required review evidence

A cross-family adapter returns this typed result for the exact candidate:

```text
VERDICT: pass | needs-fix | reject
REVIEWER-FAMILY: codex | claude | gemini | other:<name>
AUTHOR-FAMILY: codex | claude | gemini | other:<name>
COMMIT: <full 40-character git commit SHA>
```

The Reviewer App validates that result and posts the authenticated GitHub review
object; a top-level PR comment is not a substitute for the App review. A passing
result must produce the `APPROVE` event on the exact 40-character candidate. A
non-pass result remains a typed return to the implementation attempt and includes
the findings below.

### Typed-result fields
* **`VERDICT`**:
  * `pass`: The candidate satisfies all parent issue acceptance criteria, passes deterministic tests, and introduces no unverified side-effects.
  * `needs-fix`: The candidate contains bounded defects that can be repaired within the same attempt branch.
  * `reject`: The candidate violates architecture, contains stale or ambiguous ownership, or requires a new planning cycle.
* **`REVIEWER-FAMILY`**: The model family of the reviewing agent (`codex`, `claude`, `gemini`, or `other:<name>`).
* **`AUTHOR-FAMILY`**: The model family of the authoring agent.
* **`COMMIT`**: The exact full 40-hex object ID of the candidate commit reviewed.

---

## 2. Invariants & Rules

1. **Separation of Generator and Reviewer**:
   `REVIEWER-FAMILY` must **not** equal `AUTHOR-FAMILY`. A model family cannot review its own candidate.
2. **Exact-Subject Binding**:
   The `COMMIT` SHA must match the PR head SHA at the time of promotion. Any subsequent push invalidates prior reviews and requires a fresh review.
3. **Findings List on Non-Pass**:
   When `VERDICT` is `needs-fix` or `reject`, the typed result must provide
   line-numbered findings in `path:line - description` format.
4. **Read-only adapter; bounded App post**:
   The cross-family adapter has zero repository-write, push, or merge authority.
   The Reviewer App's only review-path write is the authenticated GitHub review
   object after validation; findings return to the implementation attempt.

---

## 3. Historical Record of Bootstrap Merges

The following early bootstrap PRs were merged into `main` during repository initialization prior to the enforcement of the cross-model review protocol:
* PR #12 (`codex/identity-issue-4-v2`)
* PR #13 (`codex/sota-issue-5`)
* PR #14 (`codex/master-plan-issue-10-v2`)
* PR #33 (`codex/policy-docs-issue-20-v2`)
* PR #34 (`codex/ci-receipts-issue-25-v1`)
* PR #37 (`codex/identity-gate-issue-21-v1`)
* PR #38 (`codex/ci-add-range-gate-issue-25-v2`)
* PR #41 (`codex/start-here-continuity-issue-1`)
* PR #47 (`codex/lifecycle-issue-27-mvp-v1`)
* PR #48 (`codex/backend-adoption-conformance-issue-22-v1`)

All pull requests merged after PR #50 adhere to this formal cross-model review protocol.
