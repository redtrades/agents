# Current goal

Build and prove the smallest clean, provider-neutral foundation for a solo-operated
agent software factory. The platform must let replaceable agents, models, harnesses,
memory systems, and providers collaborate without any one runtime becoming task,
source, acceptance, or promotion authority.

The first demonstrated workflow is:

```text
GitHub Issue and subissues
  -> atomic task and resource leases
  -> isolated worktree hydrated with the current instruction contract
  -> transition-triggered durable checkpoints
  -> immutable candidate and artifact hashes
  -> deterministic gates
  -> fresh independent exact-candidate review
  -> exact policy evaluation and eligible automatic expected-head promotion
  -> teardown or ownership-transfer receipt
```

## Current execution

1. `agent-platform` is the sole platform source; legacy material is read-only
   migration evidence.
2. The bounded Gate C path uses the GitHub Contents CAS with distinct Controller,
   Reviewer, and Promoter Apps. Issue #103 behaviorally proved one exact
   issue-to-merge lifecycle through that path.
3. Issue #117 remains the terminal-projection and cleanup gap; its Projector
   postcondition and exact merged-branch cleanup must chain to the terminal
   receipt without creating a second controller or cleanup path.
4. Clean-host reconstruction, interruption/resume coverage, and provider-neutral
   multi-harness coverage remain open before broader autonomy or adapter expansion.
5. New adapters enter one at a time from observed loader and activation evidence;
   product factories remain separate consumers.

Product factories such as `govcon-factory` remain separate consumers. The operating
policy has four outcomes: `DENY`, `AUTO_READ`, `AUTO_WRITE`, and
`APPROVAL_DESTRUCTIVE`. Eligible writes and expected-head promotion proceed
automatically; only effects outside the normal rollback envelope require an unexpired
`APPROVAL_DESTRUCTIVE` grant. See [`OPERATING-MODEL.md`](OPERATING-MODEL.md).
