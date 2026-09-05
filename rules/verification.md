---
name: verification
version: 1.0.0
status: active
provenance: native
last_updated: 2026-09-05
tier: quick
---

# Verification Law & Quality Gates

Canonical specification for empirical test gating, proportional rigor, the 2-try circuit breaker, and review independence across all harnesses.

## 1. The Deterministic Verification Law

- **No Completion Without Proof**: An agent must never declare a task, phase, or bug fix complete without deterministic proof.
- **Valid Proof**: Exact command line invocation, exit code 0, and passing test assertions.
- **Prose Assertions Invalid**: Statements such as "The code looks good" or "All logic verified" without an exit code 0 run transcript are strictly rejected by quality gates.

## 2. Proportional Rigor by Complexity Tier

- **Tier 1 (Quick / Doc / Config)**:
  - Execution time <2 minutes.
  - Focused single-file edit or documentation touch.
  - Verification: Run linter, schema validator, or single targeted check directly.
- **Tier 2 (MVP / Standard Feature)**:
  - Execution time 2 to 15 minutes.
  - Modular code addition or surgical bug repair.
  - Verification: Run unit test suite (`npm test` / `pytest`) with 100% pass rate.
- **Tier 3 / 4 (Architecture / Security / Cross-Harness)**:
  - Requires written plan in `docs/plans/` and ADR in `docs/decisions/`.
  - Verification: All four repository quality gates must pass:
    ```bash
    make validate STRICT=1     # Structural validation across all 5 harnesses
    make garden                # Drift detection, dead links, skill size limits
    make test                  # Full pytest suite
    npm test                   # Core contract suite
    ```

## 3. The 2-Try Circuit Breaker

If an action, build step, or test run fails twice:
- **STOP Immediately**: Do not attempt a 3rd blind variation.
- **Research First**: Search web documentation, consult upstream repository issues, or inspect local logs.
- **Never Guess**: Formulate a verified hypothesis before making another change.

## 4. Generator vs. Reviewer Independence

- **No Self-Approval**: A model family cannot serve as the sole reviewer of its own non-trivial code.
- **Cross-Model Review**: Work authored by Claude Code should be cross-reviewed by Codex or Grok; work authored by Codex should be cross-reviewed by Claude.
- **Human Authority**: Final merge authority for production branches resides with Mike.
- **Exact-Head Merge Binding**: The git commit SHA reviewed must byte-for-byte match the commit SHA merged to prevent post-review drift.
