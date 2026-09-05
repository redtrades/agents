# Task Lifecycle & GitHub History Ledger

This directory stores archived, completed task records.

## Operating Lifecycle

1. **Active Task Execution (WIP <= 2):**
   - Active tasks execute strictly out of `TASK.md` and `CONTINUATION.md` at the repository root.
   - Every atomic step commits incrementally to Git using conventional commit syntax (`feat:`, `chore:`, `fix:`).
   - Commits are pushed to `origin/main` on GitHub so remote state is always synchronized.

2. **Task Completion & Snapshot:**
   - Once all acceptance criteria pass deterministic verification (exit code 0), the active `TASK.md` is frozen and copied here:
     `docs/tasks/YYYYMMDD-<TASK-ID>.md`
   - The active `TASK.md` is reset for the next authorized task.

3. **Immutable History on GitHub:**
   - Git commits serve as the permanent, tamper-proof transaction log.
   - GitHub Releases / tags freeze estate-wide milestones.

## Archived Tasks

| Task ID | Completed Date | Owner | Description | Final Commit |
| :--- | :--- | :--- | :--- | :--- |
| *No archived tasks yet; active work is in TASK.md.* | - | - | - | - |
