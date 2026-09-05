# Provider-neutral SDLC MVP from first principles

> **Destination correction, 2026-08-28:** the canonical source repository is now
> `redtrades/agent-platform`. References below that make `agent-mesh` the permanent
> destination are superseded; `agent-mesh` is migration evidence and a temporary
> candidate source. The SDLC invariants, lifecycle, and acceptance tests remain
> current.

**Date:** 2026-08-28
**Status:** approved architecture; incremental implementation is active in the clean repository
**Scope:** the smallest recoverable, reviewable delivery loop for Codex, Claude,
Hermes, Buzz, Pi, and OpenCode.

## Decision in one page

The MVP is a thin control contract over systems already in use. GitHub Issues
show the human task graph. Git refs and commits identify executable state.
Content hashes identify evidence. A compare-and-swap lease admits exactly one
mutating owner. One worktree contains that owner's changes. Transition-triggered
checkpoints make an abrupt stop recoverable. Deterministic gates run before a
different actor reviews the exact candidate. CI accepts only the reviewed SHA and
receipt set.

No database, daemon, workflow engine, or transcript parser is required. Session
resume is a convenience; branch, checkpoint, and receipt state are authority.

```text
Issue graph (intent and dependencies)
          |
          v
Admission lease -- one owner --> isolated worktree --> checkpoint commits
          |                               |                  |
          +---- resource/subscription ----+                  v
                                                        candidate SHA
                                                             |
                                          deterministic gates + hashes
                                                             |
                                          independent exact-SHA review
                                                             |
                                                    CI promotion gate
```

## 1. Intent checksum

**Outcome.** A human can assign work to any supported runtime, lose that runtime
to context, quota, process, or provider failure, and continue elsewhere without
losing candidate identity, worktree state, decisions, rejected approaches, or
verification boundaries.

**Users.** Mike is the owner and promotion authority. Agents are bounded writers,
reviewers, or observers. A runtime name is not an identity or an authorization.

**Required properties.**

1. One mutating owner per task and one owner per shared resource.
2. Every mutation occurs in an issue-linked isolated worktree.
3. Git commits and content hashes reconstruct the candidate without chat state.
4. A checkpoint is at most one meaningful state transition stale.
5. Deterministic gates precede independent judgment.
6. Review and promotion refer to the same immutable candidate SHA and artifacts.
7. Quota or resource exhaustion yields a recoverable checkpoint, not silent
   fallback or duplicate execution.
8. Provider-specific loading, tools, authentication, and session behavior remain
   inside runtime adapters.

**Authority order.** Owner instruction and approval > accepted Git ref/commit >
hashed artifact and receipt > Issue/PR state > semantic memory > runtime session
or chat. Lower layers may point upward; they cannot override them.

**Assumptions.** GitHub and the Git remote remain available enough to coordinate;
offline work may checkpoint locally but is not transferable or promotable until
its refs and manifests are durable remotely. Existing claims/lease machinery is
extended rather than replaced.

## 2. First-principles invariants

| Invariant | Enforceable observable |
|---|---|
| Issues are a task graph, not a mutex | An Issue claim without a successful lease cannot authorize mutation. |
| Candidate identity is immutable | One receipt names issue, base SHA, head SHA, artifact hashes, adapter, and gate versions. |
| Isolation and exclusivity differ | Worktree path proves file isolation; lease token proves ownership. Both are required. |
| Shared resources are explicit | GPU, model restart, live config, account window, and exclusive service ports have named leases. |
| Checkpoint on transitions | A completed step, decision, rejected approach, tree change, gate result, blocker, or ownership change updates the checkpoint. Timers only detect staleness. |
| Generator is not judge | Author identity and reviewer identity differ; self-receipts fail closed. |
| Evidence is exact | A changed head SHA or artifact hash invalidates prior gates and review. |
| Qualifiers travel with claims | Every quantitative or pass claim includes its boundary and unverified remainder. |
| Promotion is human-owned | Passing automation marks a candidate eligible; it does not grant merge, deploy, spend, memory promotion, or destructive authority. |

## 3. Minimal state model

There is no second task-state system. Current state is derived from existing
surfaces:

| Concern | Canonical surface | Why |
|---|---|---|
| Goal, dependencies, human status | GitHub Issue/Project | Visible task graph and discussion, but no atomic claim semantics. |
| Mutating ownership | Existing remote claims ref/branch using compare-and-swap | A rejected non-fast-forward update gives one winner. |
| Shared-resource ownership | Existing remote leases ref/branch plus process-held local lock where useful | Remote coordination plus OS release for local benchmark processes. |
| Work bytes | Bounded task/review-attempt branch commits | Auditable, recoverable, provider-neutral. |
| Working copy | One registered worktree per bounded mutating task or review attempt, reused across runtime handoffs | File isolation without per-session proliferation; never a substitute for a resource lease. |
| Large/raw evidence | Content-addressed storage outside worktrees | Survives worktree removal and avoids repository bloat. |
| Evidence index | Small committed manifest and receipts | Hash, location class, producer, timestamps, and exact candidate. |
| Review and promotion | PR plus CI status on exact head SHA | Prevents stale review from blessing later edits. |

The Issue receives pointers and human-readable transitions. It does not duplicate
the receipt ledger or own executable truth.

### Admission transaction

Before the first mutation, the adapter must establish all of these or stop:

1. eligible Issue and explicit bounded objective;
2. successful atomic task lease with attempt ID, owner, heartbeat, expiry, stop
   condition, takeover rules, and teardown owner;
3. branch, base SHA, worktree path, and clean initial tree;
4. required resource/subscription leases;
5. initial checkpoint committed and remotely durable.

This is one admission decision even if the existing Git and GitHub surfaces need
several writes. The admission receipt records a successful compare-and-swap
lease; the receipt itself is evidence, not the mutex. Partial admission releases
acquired leases and leaves an Issue note; it never proceeds with a merely posted
`claiming` comment.

### Transition checkpoint

The branch checkpoint is the cold-start record. It names:

- Issue, objective, owner identity, adapter, branch, worktree, base SHA, head SHA;
- phase, stop reason, next action, blocked-on, expected-until;
- tree state, last-known-good commit, remotely durable refs;
- events since the prior checkpoint;
- decisions with rationale and provenance;
- rejected approaches with stable IDs, do-not constraints, and current hypothesis;
- completed checks with commands, artifacts, hashes, boundaries, and unverified work;
- active task/resource/subscription leases and their release or handoff state.

The same checkpoint is posted or linked from the Issue for discovery. Branch
content is authoritative if the two views differ.

## 4. Runtime adapter contract

Each adapter translates one runtime into the same lifecycle:

`inspect -> admit -> start/resume -> checkpoint -> stop -> emit candidate`

Input is the issue packet, exact base ref, worktree path, lease tokens, context
manifest, capability/data policy, and bounded run budget. Output is structured
events, checkpoint updates, artifact manifests, candidate SHA, and an honest stop
classification. Adapters do not decide acceptance.

| Runtime | Adapter boundary for the MVP |
|---|---|
| Codex | Keep the verified compact global and nearest-repository `AGENTS.md` inputs; retrieved memory remains supporting data. Use native task/session controls, but reconstruct from Git/checkpoint on resume. Emit exact model/effort when observable. |
| Claude Code | Keep sanctioned Claude Code subscription access and the compact home `CLAUDE.md`. Current active hooks enforce pre-tool rules and log skill use; they do not checkpoint quota stops. Any future stop hook is an approved adapter addition, while branch state remains the fallback. |
| Hermes | Respect verified loader priority: one project-context type plus profile `SOUL.md`. Pin profile, model, effort, toolset, and run budget. Default skills are currently disabled; profile-local enablement is not global activation. |
| Buzz | Treat Buzz as a launcher as well as a human surface: it creates the nest, manages the bounded roster, sets `~/.buzz` as provider cwd, and spawns provider/ACP runtimes whose native loaders read that context. Assignment is not the execution lease; generated and custom regions keep separate ownership. |
| Pi | Respect the verified loader walk over agent-directory and cwd ancestors, taking the first `AGENTS.override.md` / `AGENTS.md` / `CLAUDE.md` per directory. JSON mode is the machine-consumption boundary, not proof that no inherited context exists. |
| OpenCode | Keep provider config and explicitly selected named agents behind the common lease/worktree boundary. Automatic base `AGENTS.md`/`CLAUDE.md` discovery is locally unverified, so the adapter must probe it before claiming project instructions are active. |

Adapter conformance is capability-based. Unsupported resume, hooks, identity,
telemetry, or tool semantics are recorded as `unsupported`; another runtime's
feature is not simulated with an unverified claim.

An adapter or instruction surface is `active` only when its activation receipt
traces authored source -> deployment mechanism -> runtime path -> documented
loader/discovery -> observed probe. File presence, a symlink, installation, or
success in a different runtime is not activation evidence. Unknown or duplicate
surfaces remain disabled or quarantined until that chain passes.

## 5. Agent-platform module and distribution seam

There is one agent-platform source repository: `agent-mesh` (rename only after a
separate approval). Contracts, runtime adapters, projection logic, control-plane
schemas, skill packaging, memory interfaces, evals, and enforcement live as
bounded modules/packages inside it. The repository stores a module graph, not one
giant Markdown file and not copies of runtime home directories.

Product factories remain separate consumer repositories. Buzz, Hermes, Codex,
Claude Code, Pi, and OpenCode are external runtimes. Their credentials, databases,
caches, sessions, and volatile configuration remain runtime-local. `agent-configs`
and `agent-workspace` are migration sources to extract, test, and quarantine; they
are not permanent authorities or live dependencies.

```text
agent-mesh source modules -> resolved module graph -> runtime adapter
       -> generated projection or direct-file binding -> activation receipt
```

| Module class | Ownership and distribution |
|---|---|
| Shared kernel | Small stable modules for authority, safety, verification, checkpointing, and review. Loaded only when the target contract requires them. |
| Repo-local instructions | Product/repository facts remain in the separate consumer repo. A compact `AGENTS.md` or runtime shim composes an accepted `agent-mesh` projection with local rules. |
| Invoked skills/commands | Triggered capabilities remain out of startup context. Adapters publish only supported metadata and bodies to the runtime's real discovery surface. |
| Hard controls | Hooks, CI checks, and command guards are executable projections with their own tests; prose never substitutes for enforcement. |
| Volatile config and secrets | Models, endpoints, permissions, credentials, quotas, databases, caches, and live profile state remain external-runtime-native. `agent-mesh` may declare a required capability or opaque secret name, never a value. |

Each source module has one ID, source path/hash, type, dependencies, activation
trigger, precedence, context budget, and supported targets. The resolver rejects
cycles, duplicate meanings, incompatible precedence, and a projection that
exceeds the target's context limit. The runtime adapter selects only the modules
needed by that repository/profile and renders them in stable-to-volatile order.

Prefer a direct-file binding when a runtime supports an explicit instruction
override and the source can remain read-only. Otherwise write the runtime's
required fixed-path projection. Buzz has two distinct verified seams: its ACP
base prompt can point directly to a minimal projection through
`--base-prompt-file` / `BUZZ_ACP_BASE_PROMPT_FILE`; its nest workspace remains a
separate fixed `~/.buzz/AGENTS.md` projection owned by the Buzz template and
generator. The managed roster stays between Buzz markers and the user/custom
suffix is preserved. Do not copy one universal `AGENTS.md` into both seams, and
do not treat edits inside a generated region as source changes.

Every generated file or managed region records generator ownership, source
revision, module-graph hash, adapter version, and projection hash. User-owned
zones sit outside explicit markers and survive regeneration. Projection is
idempotent: identical inputs produce identical managed bytes, and a second run
is a no-op.

The drift check rebuilds into a temporary destination, compares the managed
region byte-for-byte, identifies source drift separately from user-zone edits,
and refuses to overwrite ambiguity. Runtime-specific loader tests then prove the
actual path and activation behavior: Codex global plus nearest repo contract;
Claude startup file and registered hooks; Hermes project-context priority,
profile, and skills state; Buzz provider cwd and generated regions; Pi ancestor
walk; OpenCode explicit configuration and a discovery probe where automatic
loading remains unverified.

An activation receipt names source revision and hashes, resolved module IDs,
target runtime/version/profile/repository, deployment mode, runtime path,
projection hash, loader test, observed activation result, timestamp, and any
unsupported capability. Source presence is not activation: a loader may ignore
the path, choose a higher-priority file, disable skills, preserve a stale session
snapshot, regenerate over an edit, or start from another cwd/profile.

A release tags the `agent-mesh` source revision, builds projections in isolation,
runs graph/projection/loader tests, activates one bounded target set, and records
receipts. Rollback restores the last accepted projection hash or direct binding
and reruns the same loader probe. Release and rollback never copy volatile config,
secrets, caches, sessions, or raw memory into `agent-mesh`.

## 6. Resource and subscription exhaustion

Task ownership, machine resources, and provider capacity are separate leases.
A task may remain owned while waiting for a GPU; a GPU lease never authorizes a
source edit. Subscription leases represent sanctioned runtime slots or usage
windows, never credentials.

On warning or graceful exhaustion, checkpoint durable bytes first, record
`waiting-resource` or `waiting-subscription`, release only the exhausted lease,
and post the pointer to the Issue. Continue on another adapter only when the
task's data, capability, cost, and authorization policy permits it. Otherwise
queue until the named window or owner decision.

On abrupt failure, adapter hooks may emit a minimal machine checkpoint. Lease
expiry never proves the prior process is dead: takeover also checks process
evidence, remote branch activity, worktree state, and the declared phase.
Ambiguity escalates rather than races.

Repeated handoffs are a diagnostic. A bounded handoff count triggers owner
review instead of cycling indefinitely across subscriptions.

## 7. Memory and context assembly

Keep the existing five tiers: L0 kernel, L1 immutable session evidence, L2 Git
ledgers, L3 semantic store, L4 reviewed vault. None is a task lease.

Assemble a new runtime context in this order:

1. **Kernel:** nearest project instructions and hard invariants, kept small.
2. **Task:** Issue objective, acceptance criteria, scope, permissions, and leases.
3. **Checkpoint:** exact refs, next action, tree, decisions, rejected paths,
   boundaries, and unverified work.
4. **Code/evidence:** only the relevant diff, tests, manifests, and cited source.
5. **Recall:** scoped L3/L4 retrieval with verbatim ancestors and provenance.
6. **Volatile state:** current command output and the immediate user turn last.

Raw transcripts are evidence of last resort, not context payloads. Semantic
retrieval may suggest context but cannot overwrite a later Git decision or claim
completion. Stable material precedes volatile material to preserve prompt-cache
reuse where the provider supports it.

## 8. Enforcement floor

Portable repository checks are the enforcement layer; runtime hooks are
accelerators.

**Before mutation:** refuse a shared checkout, dirty unowned tree, missing task
lease, missing worktree binding, or missing required resource lease.

**Before push/checkpoint:** require current head/tree metadata, decision and
rejection deltas, commands for completion claims, boundaries for numeric claims,
and explicit unverified work. The checkpoint may not lag more than one meaningful
transition.

**In CI:**

- validate issue/base/head/artifact references and content hashes;
- run deterministic task gates before enabling review;
- reject a receipt whose candidate differs from PR head;
- reject self-review or unverifiable actor identity;
- require independent review after the final candidate mutation;
- reject promotion when required leases remain active or artifacts are not durable;
- require an explicit owner gate for merge, deploy, spend, destructive action,
  durable-memory promotion, or policy change.

Runtime hooks should checkpoint on stop, compaction, quota/error, and destructive
tool attempts where supported. Missing hook support reduces convenience, not
safety, because CI and Git evidence remain portable.

## 9. MVP slices in dependency order

| Slice | Deliverable | Acceptance gate | Recovery point |
|---|---|---|---|
| 0. Reconcile authority | One approved contract naming Issues, refs, artifacts, leases, and owner gates | No existing surface has two conflicting authority roles | Documentation-only rollback |
| 1. Distribution seam | `agent-mesh` module graph, one adapter, projection, drift check, and activation receipt | Second projection is a no-op; edited source changes graph hash; loader probe distinguishes present from active | Restore prior accepted projection/binding |
| 2. Admission | Atomic task/resource lease plus worktree binding and initial checkpoint | Two racing writers yield one winner; loser performs no mutation | Release leases; remove only proven-empty worktree |
| 3. Continuity | Transition checkpoint and cold-start reader | Forced stop after every transition resumes with at most one transition of uncertainty | Last-known-good remote commit |
| 4. Evidence | Content-addressed artifacts and exact-candidate receipt | Hash alteration or head change invalidates receipt | Preserve raw artifact; regenerate manifest |
| 5. Gates and review | Deterministic gates, independent reviewer, CI exact-head check | Self-review and stale review fail; corrected candidate reruns gates and review | Return to changes-requested checkpoint |
| 6. Adapters | Conformance fixture for all six runtimes | Each either completes the same bounded task or reports a precise unsupported capability without corrupting state | Disable one adapter; core loop remains usable |
| 7. Exhaustion | Resource/subscription waiting and handoff path | Injected quota/resource failure checkpoints, releases the correct lease, and resumes without duplicate mutation | Queue on original adapter or escalate |
| 8. Worktree retirement | Preservation manifest and verified cleanup gate | Exact head durable remotely; clean tracked/untracked/ignored state; no process/lease; every artifact resolves | Preserve ref/bundle and leave worktree in place |

Do not begin a later slice until the prior slice's negative tests pass.

## 10. Acceptance test matrix

1. **Claim race:** two adapters target one Issue; exactly one task lease wins and
   only its worktree changes.
2. **Isolation:** mutation from the shared checkout or another owner's worktree is
   refused before a file changes.
3. **Resource race:** two tasks request the same exclusive GPU/restart/config
   resource; one waits with a visible checkpoint.
4. **Abrupt stop:** terminate each adapter after a file change, decision, failed
   approach, and gate result; a fresh adapter reconstructs the next action and
   identifies any uncertain delta.
5. **Subscription exhaustion:** inject the runtime's exhausted/quota condition;
   no credential is copied, no unsanctioned harness fallback occurs, and the task
   either queues or resumes through an allowed adapter.
6. **Exact candidate:** change one byte or advance head after gates; CI invalidates
   all stale acceptance receipts.
7. **Independent review:** identical author/reviewer identity fails. A different
   runtime with the same underlying model family is labeled correlated, not
   falsely independent.
8. **Artifact durability:** remove a test worktree only after its remote head and
   every manifest hash resolve; missing unique commits block cleanup.
9. **Context provenance:** a retrieved memory claim without a verbatim ancestor
   cannot satisfy a gate; a later superseding Git decision wins.
10. **Distribution:** change one source module and prove only declared target
    projections change; user zones remain byte-identical; a second projection is
    a no-op; rollback restores the prior activation receipt.
11. **Adapter parity:** Codex, Claude, Hermes, Buzz, Pi, and OpenCode produce the
    common checkpoint/receipt fields or an explicit unsupported result. Each
    active adapter also resolves its source-to-loader chain and an observed
    activation probe.
12. **Authority reconciliation:** Issue status, branch head, and receipt conflict;
    the system reports the conflict and uses the declared authority order rather
    than silently choosing chat state.

## 11. Keep / Adapt / Defer / Reject

| Decision | Capability | Rationale |
|---|---|---|
| **Keep** | GitHub Issues as human task/dependency graph | Already canonical and visible; pointers belong here. |
| **Keep** | Git refs/commits, exact hashes, independent receipts | They survive runtime death and make stale claims detectable. |
| **Keep** | One worktree per mutating task | Proven file isolation with an auditable branch boundary. |
| **Keep** | Deterministic gates before independent review | Cheap failures are found before judgment; generator cannot bless itself. |
| **Keep** | Five-tier memory with verbatim ancestors | Preserves evidence while keeping prompt context bounded. |
| **Adapt** | `agent-mesh` internal instruction/config packages | Store typed modules and a dependency graph inside the one platform repo; project only the bounded target set and prove activation. |
| **Adapt** | Existing claims and lease branches | Make attempt, task, resource, heartbeat, stop, expiry, takeover, worktree, and teardown bindings explicit; Issue comments remain advisory. |
| **Adapt** | Existing handoff formats | Reconcile into one transition checkpoint with TREE, REJECTED, DO-NOT, BOUNDARY, UNVERIFIED, exact refs, and leases. |
| **Adapt** | Runtime-native hooks and resume | Use as accelerators behind the portable Git/CI contract. |
| **Adapt** | SSSF gates and SQLite trace ideas | Reuse typed phases and deterministic gate semantics; do not introduce its database as task authority. |
| **Adapt** | Buzz signed receipts and routing | Use identity and human notification; do not infer lease or durability. |
| **Defer** | Semantic-memory-driven planning, automatic promotion, best-of-N fanout | Valuable only after the single-task recovery loop is proven. |
| **Defer** | A2A server, Temporal/Inngest/LangGraph, agentd, new observability stack | No MVP failure requires another controller. |
| **Defer** | Timed heartbeat scheduler | Transitions create truth; a timer may detect stale state after the core loop works. |
| **Reject** | Chat/session/transcript as task authority | Runtime-private, mutable, and provider-specific. |
| **Reject** | Issue comment as atomic execution lease | No compare-and-swap ownership guarantee. |
| **Reject** | Self-review, timing-only evidence, or review of a moving branch | Cannot establish exact candidate correctness. |
| **Reject** | Blind worktree prune | Local registrations include unique/unpushed heads and prunable metadata is not proof of safe deletion. |
| **Reject** | Blanket `git add .`, automatic stash/commit, or automatic rollback in a dirty/shared tree | Ownership is ambiguous; automation can capture, overwrite, or hide another task's state. |
| **Reject** | A second task database or orchestration daemon | Duplicates Issue/Git truth and creates reconciliation failure. |

## 12. Explicit non-goals

- Building a universal agent runtime or hiding meaningful capability differences.
- Importing or parsing private transcript formats as the normal resume path.
- Automating merge, deployment, spending, destructive cleanup, policy promotion,
  or durable-memory writes.
- Replacing GitHub Issues, Git, existing resource leases, CI, or existing artifact
  storage.
- Synchronizing runtime home directories or collapsing kernel, repo facts, skills,
  controls, volatile config, and secrets into one copied Markdown file.
- Creating a sibling agent-contracts/config repository or keeping
  `agent-configs`/`agent-workspace` as permanent authorities.
- Guaranteeing exactly-once external side effects; the MVP permits only
  idempotent or separately receipt-gated effects.
- Solving distributed consensus, cross-organization trust, or unattended trading.
- Loading all research, memory, skills, or runtime instructions into every prompt.

## 13. Evidence boundaries and approval gate

**Observed locally:** issue-as-spine and worktree rules exist; exact-model and
sanitized receipt machinery exists; deterministic offline and bounded live evals
exist; SSSF has run typed gates and SQLite traces; Buzz issues/contracts exist;
MemPalace standalone search was smoke-tested; Git-based resource leases have been
used. Current worktree archaeology found many prunable registrations plus unique
or unpushed heads, so cleanup cannot trust registry labels alone.

**Observed gaps:** Issue claims are not execution leases; handoff designs are not
mechanically enforced; cross-runtime skill/runtime adoption is uneven; Buzz has no
durable same-run wake/resume; a GBrain service is currently present, but functional
health and retrieval quality remain unverified; Claude subscription and local GPU
contention have caused stalled work; exact evidence is frequently valid only for a
named model/runtime candidate. `agent-configs` and `agent-workspace`
contain migration candidates but are not coherent live platform authorities.

**Proposed synthesis:** the authority order, admission transaction, common adapter
lifecycle, exact-candidate CI gate, and nine-slice MVP above. They are not claims
of current implementation.

Primary local evidence:

- `.agent/protocols/issue-as-spine.md`
- `.agent/memory/ARCHITECTURE.md`
- `.agent/AGENTS.md`
- `evals/LIVE-MODE.md` and `evals/tracking/receipt.py`
- `HANDOFF.md` and `DECISIONS.md`
- `research/research-free-routing-subscriptions.md`
- `~/agent-configs/knowledge/multi-agent-handoff-research-2026-08-28.md`
- `~/.buzz/GUIDES/PORTABLE_AGENT_CONTRACTS.md`
- `~/agent-workspace/adws/` and `~/agent-reports/factory-install/`
- cross-read `research/live-runtime-instruction-audit-2026-08-28.md`
- cross-read `research/workspace-consolidation-manifest-2026-08-28.md`

Approval means approving this authority model and slice order for later bounded
implementation. It does not authorize runtime/config changes, GitHub mutations,
commits, deployment, cleanup, or a new state service.

APPROVAL STATUS: awaiting user confirmation
