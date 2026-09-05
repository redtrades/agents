# agent-platform

Clean, provider-neutral infrastructure for an independent agent software factory.

The platform coordinates replaceable models, agents, harnesses, memory systems, and
product factories through durable contracts rather than vendor-specific session state.
Its target delivery chain is:

```text
GitHub Issue -> leased attempt -> hydrated worktree -> checkpoints -> exact candidate
             -> independent review -> controlled promotion and teardown
```

This repository starts clean. `agent-mesh`, `agent-configs`, `agent-workspace`, runtime
directories, and historical archives are selective migration sources only; their
instructions and structure are not inherited.

Read [`docs/START-HERE.md`](docs/START-HERE.md) first. It is the complete
cold-start source of truth: goal, entry contract, decided architecture, controller, roles,
effect policy, current implementation state, critical path, failure-prevention
rules, and resume procedure. A new agent should not need chat history or every
supporting design document before it can identify the next legal action.

For a recurring failure or stale-current-state claim, use the sole canonical
[`docs/DELIVERY-FAILURE-LEDGER.md`](docs/DELIVERY-FAILURE-LEDGER.md) through
that cold-start path.

The deeper master plan, architecture, operating model, controller, identity, and
CI documents are supporting references linked from `START-HERE.md`; they are not
a mandatory sequential reading list.

The exact four-outcome effect policy remains normatively defined in
[`docs/OPERATING-MODEL.md`](docs/OPERATING-MODEL.md).

The current private-repository enforcement limits are recorded in
[`docs/GITHUB-FREE-PRIVATE-BOUNDARY.md`](docs/GITHUB-FREE-PRIVATE-BOUNDARY.md).
The Jules dispatch boundary is recorded in
[`docs/JULES-DISPATCH.md`](docs/JULES-DISPATCH.md); only native labeled GitHub
dispatch and exact remote-candidate direct API dispatch are admitted.
Run and interpret the first executable repository evidence boundary through
[`docs/CI-GATES.md`](docs/CI-GATES.md).
