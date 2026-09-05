RCA disposition

The findings are valid and are now reconciled into the reviewed plan merged by PR #107:

- stale cwd and worktree ambiguity: recorded in the canonical status risk table; start every task from refreshed `origin/main`; #96 must report exact workspace and instruction sources;
- duplicate writers/controllers: proposed ADR 0004 assigns one lifecycle authority; #96 must reject a deliberate duplicate path claim before edit;
- cold-start instruction overload: #96 measures actual sources; do not add another AGENTS.md or skill layer;
- quota death: #98 implements same-issue checkpoint/failover;
- durable terminal processes: #99 remains the bounded Herdr task; and
- legacy checkout/ledger reconciliation: #109 performs terminal cleanup after acceptance canary #108.

No new implementation task is created from this RCA before #96 produces behavioral evidence. Retain this issue as evidence and close it completed; execute through the existing tasks.
