# Agent Platform Master Plan

This is the durable, implementation-agnostic blueprint and acceptance contract for
the independent agent software factory. It fixes the destination, authority model,
autonomy boundary, build order, and cost discipline. Research, task records, status
boards, and implementation plans support this plan but do not silently replace it.

## North star

One person can direct a continuously operating, provider-neutral agent workforce that
produces reviewed software and business artifacts. Work survives agent, context,
quota, machine, and vendor failure. Agents can be replaced without replacing the
factory. Mike defines outcomes, effect policy, and exceptional gates; the factory
researches, implements, tests, reviews, repairs, promotes eligible work, recovers, and
records evidence without making him drain routine queues.

The first proof is complete only when this chain works end to end:

```text
issue/subissues -> atomic admitted attempt -> isolated hydrated worktree
  -> durable checkpoints -> exact candidate -> deterministic gates
  -> fresh independent review -> effect-policy promotion -> teardown/transfer receipt
```

## One authority per concern

| Concern | Authority | Supporting views |
| --- | --- | --- |
| Intent, dependencies, acceptance | GitHub Issues and subissues | Project board, chat |
| Atomic ownership | Remote compare-and-swap ledger | Issue claim comment, assignee |
| Source and candidate identity | Git commit and artifact hashes | Branch, PR |
| Execution | Replaceable harness adapter | Buzz, terminal, dashboard |
| Verification | Deterministic checks plus fresh exact-candidate review | Traces, reports |
| Promotion | Effect policy plus exact-candidate eligibility receipt | PR review, approval receipt |
| Durable policy and knowledge | Reviewed versioned artifacts | Search, cache, memory |

An issue comment, board field, runtime session, transcript, or semantic-memory result
is never a mutex or promotion decision. A workflow engine may execute admitted work;
it does not become a second task authority.

## Dogfood contract

Every unit of work, including research, cleanup, documentation, evaluation, and
platform changes, starts as an issue or subissue on the canonical board. A claim records the
agent actor, run ID, owned path, branch, worktree, input revision, and acceptance
criteria. The remote ledger makes the claim atomic; the issue and board project that
state for humans and agents. Commits carry the same actor and run identity, and the PR
binds checks and independent review to the exact candidate.

No untracked multi-day work is an accepted factory output. A session that must stop
first writes a durable checkpoint or a teardown/transfer receipt.

Deterministic controller code owns polling, eligibility, sequencing, retries, phase
transitions, review routing, promotion policy, and cleanup. Agents are bounded workers
inside that loop. An eligible `AUTO_WRITE` candidate drains automatically: promote,
close the task, update the board, and tear down the workspace. A failed review returns
directly to the owning attempt with exact findings. The effect policy is defined in
[`OPERATING-MODEL.md`](OPERATING-MODEL.md).

## Autonomous improvement loop

Proactivity is a controlled loop, not permission to rewrite the factory:

```text
observe -> open bounded issue -> lease -> experiment in isolation -> measure
  -> exact candidate -> independent challenge -> policy promote/reject/escalate
  -> versioned lesson and next issue
```

Agents may proactively observe drift, failures, cost, latency, duplicated work,
missing coverage, and stale knowledge; propose issues; run reversible experiments
within policy; and prepare candidates. Self-improvement becomes durable only after
fixed evaluation, provenance and regression checks, independent review, and the effect
policy. The factory keeps failed experiments and reasons as
receipts so it stops repeating them.

## Repository and storage map

- `agent-platform`: canonical platform contracts, control logic, adapters, receipts,
  evaluation seams, and migration decisions.
- `govcon-factory`: separate product factory consuming stable platform interfaces.
- `agent-mesh`, `agent-configs`, `agent-workspace`, `agent-tools`, `agent-reports`,
  OpenClaw material, and old Codex workspaces: reference and selective extraction
  sources until each has a recorded disposition.
- Runtime homes such as `.buzz`, `.hermes`, `.codex`, provider profiles, model stores,
  caches, databases, credentials, and large run artifacts: runtime-local, outside the
  platform source repository.
- Archived research: immutable evidence indexed by topic and provenance, not injected
  into every agent prompt.

Nothing moves wholesale into `agent-platform`. Reusable behavior enters through an
issue, a bounded candidate, current verification, and independent review.

## Economical baseline

The default is zero incremental recurring software cost and minimal operator burden.
Prefer existing approved capacity, portable local components, and open contracts until
a measured requirement justifies another service or paid tier.

Build only the thin provider-neutral control contracts that are unique to this
factory. Reuse maintained systems for commodity capabilities:

- Source and task surface: select one forge that provides API-addressable issues,
  subissues, reviews, checks, packages, webhooks, backup, and restore. A mirror is not a
  second queue.
- Durable execution: keep the platform state machine authoritative. Add an external
  engine only after fixtures demonstrate unmet recovery, wait, retry, join,
  cancellation, or capacity-queue requirements.
- Agent graphs: use an in-process graph library only inside a bounded application that
  needs stateful branching or human-in-the-loop behavior; it is not the factory SDLC.
- Telemetry and evaluations: emit versioned open trace and evaluation contracts.
  Deploy a collector or UI only after a measured cross-runtime analysis need.
- Model access: expose a replaceable gateway adapter with supported authentication,
  routing, budget, outage, and receipt behavior. The gateway never owns task state.
- Secrets: keep values outside source behind opaque, scoped references. Add one central
  broker only when multi-host rotation and revocation require it.
- Sandboxes and artifacts: start with isolated workspaces and least-privilege operating
  system controls. Add a workspace service, registry, or object store only after a
  measured isolation, durability, scale, or remote-host need.

New evidence may revise these candidates through an explicit architecture decision;
it may not create a parallel stack.

## Delivery sequence

### 0. Stop the bleeding

Establish the clean repository, short governing contract, master plan, GitHub Project,
issues/subissues, agent attribution, and PR workflow. Freeze legacy instructions as
reference. Completion: every new platform change has an issue, owner, worktree,
persona/run-attributed commit, PR, evidence, and board state.

### 1. Transactional spine

Accept the versioned instruction projection, lifecycle state contracts, and commit
identity contract after fresh review. Implement remote atomic claims, capacity-aware
dispatch, checkpoints, recovery, and teardown. Completion: two contenders produce
exactly one admitted owner, then a bounded four-worker fixture finishes without
duplicate ownership or lost state.

### 2. Harness and model adapters

Add Codex, Claude, Gemini, Hermes, Buzz, Pi, OpenCode, Grok, local-model, and gateway
adapters one observed interface at a time. Each adapter reports projected,
discovered, loaded, activated, and behaviorally verified state separately. Completion:
the same task packet can move between at least two harnesses and two providers without
changing its authority or artifact contract.

### 3. Evidence, evaluation, and knowledge

Emit correlated task, attempt, worktree, model, tool, cost, artifact, test, review, and
teardown receipts. Add fixed eval fixtures and provenance-aware retrieval. Promote
memory, skills, policy, prompts, and routing only through candidate, evaluation,
independent review, and effect policy. Eligible writes may promote automatically;
effects outside the normal rollback envelope require `APPROVAL_DESTRUCTIVE`.
Completion: a seeded unsupported claim is
rejected and an interrupted run resumes from reviewed state rather than raw transcript
recovery.

### 4. Consolidate the estate

Index legacy repositories and folders by Keep, Adapt, Archive, Quarantine, or Delete.
Extract unique value into the owning repository, preserve sensitive/runtime boundaries,
then retire duplicates in recoverable batches. Completion: each surviving top-level
workspace has one purpose and owner; old instructions cannot load into new sessions.

### 5. Prove the factory with a product

Run one real `govcon-factory` slice through the platform from issue to promoted,
reviewed deliverable. Measure operator minutes, cost, recovery, correctness, and
handoff quality. Completion: the run is reproducible from versioned inputs and receipts
and requires Mike only for outcome planning, policy exceptions, and effects outside
the normal rollback envelope.

## Factory acceptance scorecard

The platform is not complete until repeatable fixtures prove all of these outcomes:

| Capability | Passing evidence |
| --- | --- |
| Autonomous throughput | In the MVP fixture, at least 19 of 20 eligible routine tasks reach `DONE` with an accepted candidate without Mike moving an issue, retrying an agent, promoting a candidate, or cleaning a worktree. After launch, the same success rate stays at or above 95% over a rolling 100 eligible tasks. Eligible means classified `AUTO_WRITE`, dependency-clear, input-complete, within approved capability and budget, and not waiting on an external human or service. Blocked and rejected attempts must reach a durable, evidence-bounded terminal state, but they are tracked separately and never count as successful throughput. |
| Atomic dispatch | Concurrent contenders for one task admit exactly one leased attempt; stale actors and expired generations cannot mutate state. |
| Queue draining | Passing eligible `AUTO_WRITE` candidates promote and close automatically; failed candidates return to their owner; blocked work records a reason and dependency. |
| Continuity | Killing a worker, exhausting a subscription, or losing context resumes from a durable checkpoint without raw-transcript recovery or duplicate work. |
| Exact verification | Tests, gates, review, and promotion bind the same commit, tree, artifacts, inputs, and receipt chain. |
| Independent challenge | A generator cannot approve itself; the reviewer identity, model or provider, subject hash, findings, and verdict are durable. |
| Provider neutrality | One task packet completes through at least two harnesses and two model providers without changing authority or artifact contracts. |
| Controlled improvement | Prompt, skill, policy, memory, routing, and code changes beat a fixed baseline and held-out checks before promotion; losing experiments remain rejected receipts. |
| Proactivity | The factory detects drift, stale work, regressions, cost anomalies, and missing coverage; opens bounded tasks; and resolves eligible ones within policy. |
| Economy | Every run records cost, quota, time, retries, and resource use; no permanent service duplicates an existing authority or exists without a measured trigger. |
| Security and control | Secrets remain outside source; capability grants are explicit; any operation materially destructive, practically irreversible, or otherwise outside the normal rollback envelope requires `APPROVAL_DESTRUCTIVE`. |
| Estate clarity | Every surviving repository and runtime root has one purpose and owner; legacy instructions cannot load into new sessions. |
| Product proof | A real product-factory deliverable completes issue-to-receipt, survives interruption, passes independent review, and is reproducible from versioned inputs. |

## Decision gates

The controller classifies every operation under
[`OPERATING-MODEL.md`](OPERATING-MODEL.md): unsupported or prohibited operations are
`DENY`; admissible reads are `AUTO_READ`; eligible writes within the normal rollback
envelope are `AUTO_WRITE`; and only operations materially destructive, practically
irreversible, or otherwise outside that envelope require
`APPROVAL_DESTRUCTIVE`. Eligible candidates promote automatically after their exact
deterministic and independent-review gates pass. A new self-hosted service must
replace an existing responsibility or satisfy a measured unmet requirement; it cannot
create a second queue, ledger, identity, memory, or promotion authority.

Architecture changes update this file in the same PR as a decision record. Normal task
progress updates the issue and board, not this document.
