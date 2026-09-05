# Architecture boundary

`agent-platform` owns portable source contracts, deterministic lifecycle control,
runtime projection adapters, receipts, verification fixtures, and evaluation seams.

It does not own product-factory logic, credentials, provider accounts, live sessions,
runtime databases, model files, caches, or large execution artifacts.

## Current lifecycle boundary

The bounded live path uses the GitHub Contents CAS authority for issue/task claims,
one isolated worktree, exact-candidate deterministic gates, and expected-head
promotion. Issue #103 behaviorally proved that path with distinct Controller,
Reviewer, and Promoter Apps plus a separate Projector credential. It is a bounded
fixture, not a claim that clean-host reconstruction, interruption/resume, or
provider-neutral multi-harness coverage is complete.

Terminal projection and cleanup require a receipt chaining the terminal effect,
Projector readback, and exact merged-branch cleanup. Current issue ownership and
execution status belong in the cold-start path and GitHub views, not this architecture
boundary. Runtime adapters remain incremental and must derive from observed loader
behavior; neither a provider nor a harness becomes lifecycle authority.

## State distinctions

Projection is not activation. Runtime claims use this progression:

```text
projected -> discovered -> loaded -> activated -> behaviorally verified
```

Receipts record the highest state actually demonstrated and bind it to exact inputs.

## GitHub Free private boundary

GitHub Issues, subissues, Projects, pull requests, ordinary reviews, Git objects, and
the included Actions quota are coordination and evidence surfaces. On the current
GitHub Free personal plan, a private repository cannot enable protected branches,
repository rulesets, required reviewers, required status checks, or enforceable
CODEOWNERS review.

Until a paid plan or another server-side enforcement seam is explicitly adopted:

- GitHub records intent, candidates, reviews, and decisions but is not the promotion
  mutex.
- Local deterministic gates and receipts may mark a candidate eligible; they cannot
  make direct pushes impossible.
- An external controller admits operations; an independent reviewer evaluates the
  exact candidate; a separate expected-head promoter performs eligible promotion; and
  a derived Project projector reflects the resulting receipts.
- CI results are evidence, not required merge checks.

The platform must report these controls as `unsupported` or `not_enforced`, never as
active protection. Effect classification is defined in
[`OPERATING-MODEL.md`](OPERATING-MODEL.md).
