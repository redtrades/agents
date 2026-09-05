# rebase-141-fix-receipt.md

**Date:** 2026-08-30  
**PR:** redtrades/agent-platform#141 (branch `gemini/claim-reconciler-issue-124-v2`)  
**Task:** Investigate and fix the "Exact-subject repository gates" CI failure on the
claim-reconciler PR.

## Before state

- Branch HEAD: `d5449f72ac5b72359f5ef5d4647c6e2a04226b24`
- CI conclusion: **FAILURE** — Job "Exact-subject repository gates" (`ci-gates.yml`).
- Mergeable (tree-conflict) state: **true** (verified by parent subagent).

## Gate contract

Per `docs/CI-GATES.md` and `docs/OPERATING-MODEL.md`, the gate runner
(`tools/ci/run_gates.py`) is the first executable evidence boundary. It binds a
JSON receipt to the exact Git subject (commit OID + tree OID) and runs each
registered gate deterministically. A failed or stale subject returns non-zero and
still uploads its receipt; the controller fails closed on missing/stale evidence.

## Root cause (gate contract failed)

The branch was one commit ahead of `main`:
`d5449f7 ci(claim-reconciler): register the claim-reconciler gate in ci-gates.yml`.

That commit also added a second gate entry, `execution-budget` (from #123
predecessor), to the same workflow file. In doing so, it dropped the trailing
backslash `\` on the `work-item-contract` line, so the shell parsed the next
line as a new command:

```yaml
            --gate-json '{"name":"work-item-contract",...}'           <-- backslash MISSING
            --gate-json '{"name":"execution-budget",...}'             <-- broken command
```

Result: the `run_gates.py` invocation never even started, the receipt was never
written, the runner reported the job as "Exact-subject repository gates" failed
(stale/missing evidence), and the controller correctly failed closed per
`docs/OPERATING-MODEL.md` ("missing or stale expected-head … produces DENY").

The claim-reconciler module and its test suite are themselves correct — all 17
tests pass locally:

```
ℹ tests 17
ℹ pass 17
ℹ fail 0
```

The exact-subject gate contract was violated by the workflow YAML, not by the
new module.

## Fix applied

Single-character, fully reversible, workflow-only fix: restore the `\` line
continuation on the `work-item-contract` gate entry. `tests/controller/claim_reconciler.test.mjs`
already contains a self-test that asserts the workflow file matches the
registered gate, so this fix also satisfies that assertion.

**File modified:** `.github/workflows/ci-gates.yml` (one character: `\\`)
**Commit:** `97c6a95` on `gemini/claim-reconciler-issue-124-v2`
**Push:** `git push --force-with-lease` (remote advance `d5449f7..97c6a95`)

## After state

- Branch HEAD: `97c6a95c...` (pushed, no merge)
- YAML syntax: valid (verified with `python3 -c 'import yaml;yaml.safe_load(open(...))'`)
- Local gate evidence: `node --test tests/controller/claim_reconciler.test.mjs`
  → 17/17 pass (including the workflow-string self-assertion)
- PR remains **open**, not merged.

## Reversibility

The change is one character on one line. Revert with:

```bash
git revert 97c6a95
```

or `git reset --hard d5449f7 && git push --force-with-lease`. Both leave
`tools/controller/claim_reconciler.mjs` and `tests/controller/claim_reconciler.test.mjs`
intact.

## Files touched

- `/.github/workflows/ci-gates.yml` (+1 char, -1 char)
- `/Users/man/agent-platform/rebase-141-fix-receipt.md` (this file, new)

## Conclusion

- `gate_contract_failed`: "Exact-subject evidence (CI gate) — workflow YAML
  produced invalid shell due to missing backslash continuation, so
  `tools/ci/run_gates.py` could not run, receipt was never written, controller
  correctly failed closed per `docs/OPERATING-MODEL.md`."
- `fix_applied_file`: `.github/workflows/ci-gates.yml`
- `receipt_path`: `/Users/man/agent-platform/rebase-141-fix-receipt.md`
