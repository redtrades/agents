TERMINAL CLEANUP — SEQUENCE RECOMMENDATION (branch a07a717 / PR heads 30efabd 3e8cb4e f035225)

INSPECTION (verified 2026-08-30):
- a07a717 (pr118x, local): 618 insertions / 66 deletions across 8 files (gate_c, github_task_admission, gate-c workflow + tests). No deletion of work_item_contract.mjs or claim_reconciler.mjs.
- 30efabd (codex/terminal-cleanup-issue-117-v1-619... remote): 418+/527- net, deletes docs/DELIVERY-FAILURE-LEDGER.md + several docs; does NOT delete controllers.
- 3e8cb4e (bind + postconditions): 6-file delta, same scope.
- f035225 (issue-117-terminal-cleanup-...-1469... remote, = #152 latest): 379+/51-; no controller-file deletions in current diff TO merge-base ccada69 (PR #120).
- DELETION RISK CONFIRMED (context source): codex/terminal-cleanup-issue-117-v1 branch (fef92bd / #118) carries ~3106-line destructive removal; if promoted BEFORE #140/#141 it would delete tools/controller/work_item_contract.mjs (#137) and claim_reconciler.mjs (#124) — both currently present (285 + 738 lines, uncommitted / PR-ready).

DEPENDENCY (must land FIRST):
- #137 (gemini/work-item-contract-issue-137) → work_item_contract.mjs
- #124 (gemini/claim-reconciler-issue-124-v1) → claim_reconciler.mjs
- #140 / #141 implement these; PR140-ANALYSIS confirms file exists untracked, tests missing, CI gate registered.

SEQUENCE RECOMMENDATION (do NOT merge yet):
1. REBASE + LAND #140, #141 (controller contract + reconciler) — protect contract/reconciler files.
2. THEN merge latest terminal cleanup: #152 (f035225); close superseded #149 / #150 (already mergeable, CI green).
3. CLOSE superseded #118 (null / supersession by #152); DENY destructive if it deletes work_item_contract.mjs OR claim_reconciler.mjs pre-merge.
4. Worktree .git/worktrees/970e/agent-platform (a07a717 tracking) NOT present now; assess before any merge.

NO MERGES PERFORMED (inspection only). Deletion risk: TRUE in destructive-form branch; FALSE in current PR heads IF #137/#124 land first.
