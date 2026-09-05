# Durable intent — independent agent factory

One operator should be able to run a continuously improving software factory
through a provider-neutral agent swarm without depending on one model, vendor,
harness, session, or undocumented local convention.

The platform must be modular and composable. Any conforming agent, model,
runtime, memory system, evaluator, or provider can participate through an
adapter without becoming the authority for tasks, source, acceptance, or
promotion.

The durable execution chain is:

```text
GitHub Issue and subissues
  -> atomic attempt and resource leases
  -> isolated task worktree
  -> deterministic phases and transition checkpoints
  -> immutable candidate and artifact identity
  -> deterministic gates
  -> fresh independent exact-candidate review
  -> explicit human promotion
  -> teardown receipt
```

Work must survive context exhaustion, subscription limits, process failure,
handoffs, and provider changes without depending on raw conversation JSONL.
Chat, Buzz, semantic memory, dashboards, caches, and provider sessions support
the chain but never own it.

Use current state-of-the-art open-source mechanisms when they fit. Pin and
inspect source, license, dependencies, authority model, failure behavior, and
operational cost before adoption. Prefer adapting narrow proven mechanisms over
installing another overlapping control plane.

Existing files and systems—including `agent-mesh`, `agent-configs`,
`agent-workspace`, `agent-reports`, `.agents`, runtime homes, OpenClaw material,
SSSF/Fusion/Verifier adaptations, GBrain, MemPalace, and old handoff protocols—
are research and salvage inputs. Preserve completed work, extract what earns a
place, and retire duplicates only after the replacement and rollback evidence
exist.

There is one platform source repository. Product factories and genuinely
separate domains remain separate repositories. Runtimes, credentials, caches,
models, sessions, and large evidence remain outside the platform source tree.

The autonomy target is high, but the human retains promotion authority for
merge, deployment, spending, destructive action, credential policy, durable
memory/policy changes, and other irreversible effects.

