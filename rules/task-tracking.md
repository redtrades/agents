---
name: task-tracking
version: 1.1.0
status: active
provenance: native
last_updated: 2026-09-05
tier: quick
---

# Task Tracking & Continuation Rules

Canonical operational specification for planning with files, state machine lifecycles, complexity-tiered turn budgeting, and zero-loss session recovery across all agents.

## 1. The Core Invariant: State Externalization

AI agents lose in-memory context across session resets, API rate limits (HTTP 429), and context truncations. To prevent agent amnesia and token waste, state must be externalized continuously to disk:
1. **Never Leave Uncommitted Code Across Turns**: Verified diffs must be committed incrementally to git before handoff.
2. **Update Continuation State Before Calling Tools**: Maintain `CONTINUATION.md` in the repository root after every atomic step.
3. **Cold-Start Resume Under 500 Tokens**: An incoming agent reads ONLY `CONTINUATION.md` and runs `git diff HEAD~1`. Never re-ingest entire conversational transcripts.

## 2. In-Flight Focus vs. Parked Backlog

To eliminate task conflation:
- **Active In-Flight Priority**: Exactly one focused objective per agent session.
- **Parked Backlog**: Secondary issues, deferred refactorings, and future ideas must be placed into the "Parked Backlog" section of `TASK.md`. Never conflate parked items with the active in-flight task.

## 3. Git as the Immutable Event Ledger

Per the Ponytail YAGNI ladder, do not invent custom logging databases or redundant JSONL files:
- **Git commits are the immutable ledger**: Every completed subtask produces an atomic commit with a conventional commit message.
- **`git log -n 5 --oneline`** provides the tamper-evident, machine-readable history of execution.
- **`TASK.md`** maintains the human-readable checklist with commit SHA bindings.

## 4. Complexity-Adaptive Turn Guidance & Anti-Planning Loops

To prevent infinite re-planning loops while providing adequate headroom for multi-gate autonomous workflows:

| Tier | Complexity Scope | Guidance Turn Ceiling | Cost Ceiling | Checkpoint Cadence |
| :--- | :--- | :--- | :--- | :--- |
| **Tier 1 (Quick)** | Single-file doc, typo, config, or lint fix | ~5 turns | $0.10 | Upon completion (<2 min) |
| **Tier 2 (MVP)** | Standard feature, surgical bug fix, unit test | ~25 turns | $2.00 | At turn 20 or completion |
| **Tier 3 (Standard)** | Multi-component integration, refactor, contract | ~50 turns | $5.00 | Every 20 turns |
| **Tier 4 (Audit / Goal)** | Long-running workflow, `/goal`, full-estate sweep | ~100 turns | $10.00 | Every 25 turns |

### Execution-Tethered Planning Invariants:
1. **No Prose-Only Plans**: Every plan in `docs/plans/` must compile into an explicit checklist in `TASK.md`.
2. **Checklist Gating**: Each checklist item must declare the action command, deterministic exit condition (exit code 0), and resulting commit SHA.
3. **Frozen Completed Items**: Once marked `- [x] <SHA>`, an item is locked. Successor agents are prohibited from re-planning completed items.
4. **Cadenced Checkpointing**: In Tier 3 and 4 long-running workflows, agents must checkpoint to `CONTINUATION.md` and commit incremental progress every 20-25 turns, preventing context rot and securing work against mid-run interruptions.

## 5. 5-State Decision & Instruction Promotion Protocol

When architectural, operational, or policy ideas emerge:
1. **Capture as PROPOSED**: Log the item in `TASK.md` and `docs/decisions/DECISION_LOG.md` with status `PROPOSED`. Ideas and nuances never govern agent behavior while unratified.
2. **Explicit Operator Ratification**: Only when Mike confirms or ratifies the decision is its status updated to `RATIFIED`.
3. **ADR Registration (Level A)**: For major architectural changes, author a formal Architecture Decision Record in `docs/decisions/YYYYMMDD-NNNN-<slug>.md` using MADR format.
4. **Rule Distillation (Level B/C)**: If a ratified decision permanently governs agent behavior, promote it into `rules/` or `AGENTS.md`. Never leave governing policy trapped in chat.
5. **Superseding, Stale, & Rejection**: When an approach is replaced, mark it `SUPERSEDED` with a direct link to the successor decision ID; mark unused ideas `STALE` or `REJECTED`. Never silently overwrite past history.

## 6. Required CONTINUATION.md Schema

```markdown
# Task Continuation State

**Task ID:** <TASK_ID>
**Goal:** <Single sentence goal>
**Timestamp:** <ISO_8601>
**Branch:** <branch_name> (commit: <HEAD_SHA>)

---

## 1. Active Phase & Status
- **Current Phase:** <Phase Name>
- **Overall Status:** IN_PROGRESS | BLOCKED | COMPLETE

---

## 2. Completed Steps (Machine-Verified)
1. **<Step 1>:** <Summary> (Commit: `<SHA>`).

---

## 3. Active Step (In Progress)
- **Step Name:** <Current step>
- **Target:** <Expected outcome>

---

## 4. Modified & Staged Files
- `<file_path>`

---

## 5. Next Immediate Actions
1. `<Exact shell command or edit to run>`
```
