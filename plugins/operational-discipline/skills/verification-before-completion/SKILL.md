---
name: verification-before-completion
description: Use after changing executable code or configuration, before claiming the requested behavior works. Do not use for answers, research, reports, or tasks that made no implementation changes Use when verifying tasks with deterministic tests and exit code 0 before declaring completion.
---
# Verification before completion

Run the smallest fresh proof that supports the claim being made.

- For a simple local change, exercise the changed behavior with one focused test,
  command, or reproduction.
- For a cross-module or public-contract change, add the relevant nearby suite or
  build.
- Run full production, release, merge, or deployment gates only when the user or
  repository explicitly requires that boundary.
- Read the result and report failures or unavailable checks accurately.
- For delegated work, inspect the owned diff and run the focused proof. Do not
  repeat unrelated worker checks or add another reviewer unless risk or the
  request requires it.

Reuse still-current evidence when the inputs and candidate are unchanged. Stop
when the requested acceptance condition has proof.
