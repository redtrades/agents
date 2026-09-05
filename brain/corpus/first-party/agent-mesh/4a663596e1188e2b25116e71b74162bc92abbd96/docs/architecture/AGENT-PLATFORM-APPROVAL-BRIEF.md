# Agent platform — consolidated approval brief

> **Destination correction, 2026-08-28:** the user clarified that clean-room means a
> new repository. Replace every architectural occurrence of `agent-mesh` as the
> destination with `agent-platform`. Treat `agent-mesh` paths and implementation
> worktrees below as migration evidence or transplant sources. The authority model,
> module boundaries, slice order, and acceptance gates remain current.

**Date:** 2026-08-28
**Status:** architecture and migration contract approved for incremental implementation
**Current execution:** Slices 0-2 foundations are being built in isolated worktrees; destructive external controls, deployment, commits, pushes, and PRs remain separately gated

## Executive decision

Build one provider-neutral agent-platform source repository: **`agent-mesh`**.
Do not create a sibling contracts, policy, skills, or control-plane repository.
Inside `agent-mesh`, keep contracts, lifecycle control, runtime adapters,
instruction projections, skill packaging, memory interfaces, evaluation fixtures,
receipts, and enforcement as bounded modules.

Keep product factories such as `govcon-factory` separate. Treat Buzz, Hermes,
Codex, Claude Code, Pi, OpenCode, Grok, and Gemini as replaceable external
runtimes. Their credentials, sessions, databases, caches, model files, and
volatile configuration remain runtime-local. `agent-configs` and
`agent-workspace` are migration evidence to extract selectively and then archive
or quarantine; they are not permanent dependencies.

The smallest coherent delivery chain is:

```text
GitHub Issue (intent and dependencies)
  -> compare-and-swap attempt lease
  -> issue-linked isolated worktree
  -> deterministic phases + transition checkpoints
  -> immutable candidate SHA + artifact hashes
  -> deterministic gates
  -> fresh independent exact-candidate review
  -> human-controlled promotion
```

Chat, Buzz, semantic memory, dashboards, provider sessions, and raw transcripts
support discovery and recovery. None is authoritative execution state.

## What is observed now

### Working foundations

- GitHub Issues, branches, worktrees, deterministic evaluation fixtures,
  sanitized receipts, and exact-model evidence already exist.
- The local SSSF adaptation has executed typed phases, deterministic gates, and
  SQLite traces. Its Pi adapter worked; claimed provider neutrality did not.
- Existing resource-lease and Git-claim patterns show that remote compare-and-swap
  coordination is feasible.
- Buzz provides signed identities, issues, messages, replies, threads, and human
  coordination. It does not provide an atomic execution lease or durable ACP
  resume.
- Hermes contains useful lineage, prompt hashing, compare-and-set transitions,
  and workspace-byte checkpoints, but those are Hermes-specific and incomplete
  as cross-provider task state.
- MemPalace preserves source metadata and a restricted write-ahead log, but its
  transcript hook is provider-specific, timer-based, and not a durable task
  checkpoint.
- A GBrain service is currently running. Functional health, corpus quality, and
  retrieval accuracy remain unverified; it is not task authority.

### Verified failure pattern

The core design has been written repeatedly but rarely enforced. Recent sessions
survived quota/context death only when work happened to have been written first.
The missing capability is transition-triggered durability and admission control,
not another prose handoff format.

Other observed failures:

- mandatory global worklogs/artifacts conflicted with read-only work;
- the deleted master guide was treated as universal despite no native loader;
- copied skills, personas, and symlinks were mistaken for runtime activation;
- several runtime fields were unsupported while prose implied permissions;
- Buzz assignment was mistaken for a lease;
- SSSF and fusion runs stalled under local-model contention;
- prompt-cache results were overgeneralized across models;
- handoff formats omitted tree state, rejected paths, boundaries, or exact refs;
- worktrees multiplied without admission or teardown ownership;
- automated backup/consolidation jobs can publish branches or mutate governance
  outside a reviewed promotion path.

### Current workspace risk

The current snapshot contains 160 registered worktrees across four principal
repositories, including 51 prunable registrations and ten exact commits requiring
preservation review. Generated data, durable evidence, source, runtime state, and
caches are mixed across namespaces. No bulk prune, move, or deletion is safe.

## Repository and module boundary

Proposed logical modules inside `agent-mesh`:

```text
agent-mesh/
├── platform/contracts/       # task, lease, checkpoint, artifact, receipt schemas
├── platform/control/         # admission, transitions, takeover, teardown
├── platform/projections/     # module graph, deterministic renderers, drift checks
├── platform/adapters/        # Codex, Claude, Hermes, Buzz, Pi, OpenCode, later others
├── platform/skills/          # curated source, manifests, provenance, trigger tests
├── platform/memory/          # tier interfaces and promotion contracts
├── platform/artifacts/       # content-addressing and manifest interfaces
├── platform/policy/          # machine-enforced gates and owner boundaries
├── evals/                    # conformance, recovery, denial, cost, quality fixtures
└── research/                 # evidence and decisions, never implicit instructions
```

The paths are proposed; the module boundaries are the decision. Do not reorganize
the repository until the first migration slice proves the contracts and rollback.

Separate domains:

| Domain | Authority |
|---|---|
| Agent platform source | `agent-mesh` |
| Product behavior and domain templates | each factory repository |
| Runtime/vendor source | upstream or separately pinned vendor checkout |
| Runtime-local configuration/state | native runtime directories |
| Large immutable evidence | content-addressed artifact store |
| Rebuildable dependencies/datasets | shared cache store |
| Credentials | native secret stores; opaque references only |

## Authority and state model

| Concern | Authoritative surface |
|---|---|
| Goal, dependencies, acceptance, eligibility, human decisions | GitHub Issue and subissues |
| Mutating ownership | atomic attempt lease using an existing remote Git CAS seam |
| Shared GPU/service/account capacity | separate resource/subscription lease |
| Source bytes and candidate identity | exact immutable Git commit SHA plus artifact hashes |
| Large evidence | immutable artifact plus content hash |
| Gate/review result | receipt bound to exact candidate and artifact hashes |
| Working copy | one worktree per bounded mutating task or review attempt |
| Human promotion decision | explicit owner approval recorded on the exact candidate |
| Promotion enforcement | protected PR, CI, and server-side ruleset |
| Teardown | teardown owner named in the attempt lease; successful CAS release or transfer changes ownership, and the completion receipt records the outcome |

Projects, PRs, comments, labels, assignees, Buzz assignments, dashboards, and
Markdown owner fields are projections or interaction surfaces. They are neither
the intent authority nor mutexes.

### Admission contract

Before mutation, require:

1. eligible issue and bounded acceptance criteria;
2. successful task-attempt lease with owner, attempt ID, heartbeat, expiry,
   stop condition, takeover rule, and teardown owner;
3. base SHA, branch, registered worktree, and clean owned starting tree;
4. required resource/subscription leases;
5. remotely durable initial checkpoint.

Partial admission releases acquired leases and stops. A `claiming` comment alone
never authorizes mutation.

### Transition checkpoint

Write at meaningful transitions, not merely on graceful shutdown or a timer. The
checkpoint records objective, phase, refs, tree state, next action, decisions,
rejected approaches, do-not-repeat constraints, checks and artifact hashes,
claim boundaries, unverified work, leases, pending external effects, stop reason,
and takeover/teardown ownership. It may be at most one meaningful transition
stale.

## Runtime adapter contract

Every adapter implements:

```text
inspect -> admit -> start/resume -> checkpoint -> stop -> emit candidate
```

Adapters translate native capabilities; they do not decide acceptance. Unsupported
resume, hook, model, identity, permission, or telemetry behavior is recorded as
`unsupported`, never simulated.

An activation claim must trace:

```text
authored source -> deployment mechanism -> runtime path -> documented loader
  -> observed discovery/invocation/denial probe -> activation receipt
```

File presence or another runtime's success is insufficient.

## Canonical instruction, skill, and configuration projections

The platform stores typed modules and a dependency graph, not one giant Markdown
file and not copies of runtime home directories. Module metadata includes ID,
type, dependencies, precedence, activation trigger, supported targets, context
budget, source hash, provenance, license, and rollback reference.

Adapters resolve only required modules and produce deterministic runtime-specific
projections. Prefer a native direct-file binding; otherwise write a fixed-path
managed projection. Generated regions carry source revision, module-graph hash,
adapter version, and projection hash. Explicit user zones survive regeneration.
The second identical projection must be a no-op, and drift must fail closed rather
than overwrite ambiguous local edits.

Repository-specific `AGENTS.md` files remain owned by their repositories. Shared
procedures remain invoked skills. Permissions and safety boundaries belong in
hooks, CI, runtime policy, and server-side rules—not prose alone.

### Buzz posture

The installed Buzz app is 0.5.19; the local source checkout is older and cannot
prove exact installed behavior. The bounded local measurement recorded in
`/Users/man/agent-mesh/docs/research/LIVE-RUNTIME-INSTRUCTION-AUDIT.md`
found 13,734 bytes in the older checkout's source `base_prompt.md` and 6,351
bytes in the live nest `AGENTS.md` after the approved bootstrap correction. This
does not measure the installed 0.5.19
binary's effective compiled prompt, which remains unverified.

Use two distinct platform projections:

- a minimal Buzz transport base referenced through the installed
  `BUZZ_ACP_BASE_PROMPT_FILE` interface;
- a separate nest-workspace projection through Buzz's managed template/version
  seam, preserving roster and user zones.

Do not copy one universal `AGENTS.md` into both. Begin with one adapter, explicit
least-privilege permissions, owner-only inbound triggers, exact installed-version
hashes, a prompt dump, signed-message smoke test, restart test, and rollback drill.

Current local facts: Buzz prefers Claude globally, but Claude ACP adapters are
absent; Codex ACP is also absent. Hermes is available, but the saved Buzz harness
uses Hermes's default `:8318` endpoint, not the cloud-coordinator `:3100` profile.
That routing must not be claimed until a selected-profile probe proves it.

## Memory, context, and caching

Keep five distinct tiers:

1. minimal policy kernel;
2. immutable session/evidence records;
3. Git checkpoints, decisions, manifests, and receipts;
4. semantic retrieval store;
5. human-reviewed durable knowledge vault.

Context assembly order is stable kernel, task contract, checkpoint, relevant
code/evidence, provenance-linked recall, then volatile current state. Raw provider
transcripts are forensic evidence of last resort, not the normal resume input.
Semantic memory may propose context but cannot overwrite a later Git decision.

Prompt/KV caches are optional performance adapters. A cache descriptor must bind
runtime, model, tokenizer, template, tools, prefix fingerprint, and telemetry.
Latency alone does not prove a hit, and no cache/session ID satisfies continuity.

## Artifacts, receipts, security, and observability

- Store small schemas, fixtures, summaries, and hashes in Git.
- Store large/raw evidence outside worktrees in content-addressed immutable storage.
- Record planned-but-unexecuted measurements as null, not success.
- Bind receipts to issue, attempt, base/head SHA, inputs, artifact hashes,
  adapter/runtime/model identity, commands, gate versions, boundaries, and actor.
- Sanitize external receipts; retain private raw evidence under explicit retention
  and access policy.
- Run deterministic checks before model judgment.
- Reject self-review, stale review, moving-branch review, or unverified actor identity.
- Require owner gates for merge, deployment, spending, destructive actions,
  policy promotion, and durable-memory promotion.
- Use OpenTelemetry-compatible events for observation, but never make telemetry
  the task ledger.

## State-of-the-art disposition

Repository activity, license metadata, and adoption are screening evidence, not
proof of fit. This read-only GitHub API snapshot was checked on 2026-08-28;
license values are repository metadata and must be rechecked before code reuse.

| Repository | Exact default-branch revision | Last push (UTC) | License metadata |
|---|---|---|---|
| `disler/super-simple-software-factory` | `de31374882e7a4e3e5b7bb9bd09e69dc2f779356` | 2026-08-04 | MIT |
| `disler/fusion-harness` | `01a348202482cad0e7d3c34eada180f711aaddd7` | 2026-08-23 | MIT |
| `disler/the-verifier-agent` | `aa18d68bcf886fb2a061ca5a76c6d2e1f3516501` | 2026-05-03 | MIT |
| `github/gh-aw` | `7c9958c9abde37967bbefe16da92fb551139bee2` | 2026-08-28 | MIT |
| `OpenHands/OpenHands` | `d573456dc69332736250d265ca22b358f5aa7e30` | 2026-08-28 | MIT |
| `gastownhall/beads` | `71377f276968b452ee607177637970a4ff888584` | 2026-08-28 | MIT |
| `gastownhall/gastown` | `649b832b7672bc7a2dbef26f5983aba6198b819b` | 2026-08-19 | MIT |
| `garrytan/gstack` | `b5a951e62398abc8aea5beed429cc2617184fcc1` | 2026-08-28 | MIT |
| `first-fluke/oh-my-agent` | `ca736256275e4dc8c15a1fe967eb8c8d1df5fddc` | 2026-08-28 | MIT |
| `temporalio/temporal` | `5ed21eb39b8b46031666c59afc51ea3f87ad8fd0` | 2026-08-28 | MIT |

The original metadata snapshot is preserved at
`/Users/man/agent-mesh/docs/research/SOTA-GITHUB-METADATA-RECEIPT.md`. The
source-level comparison at
`/Users/man/agent-mesh/docs/research/SOTA-PRIMARY-SOURCE-COMPARISON.md` pins any
later revision used for architectural claims.

SLSA, in-toto, Sigstore, and OpenTelemetry are standards/ecosystem concepts in
this brief, not a claim that one repository or license governs the group. Any
code reuse requires a separate pinned-source and license review.

| System | Decision | Reusable mechanism / boundary |
|---|---|---|
| Disler SSSF | **Adapt** | typed phases, deterministic gates, trace events; reject Claude-specific packaging and SQLite as task authority |
| Fusion Harness | **Adapt** | independent attempt/fusion pattern for uncertain high-value work; defer routine fan-out |
| Verifier Agent | **Adapt** | fresh-context challenge; bind it to exact candidate and prohibit self-promotion |
| GitHub `gh-aw` | **Keep pattern** | compiled locked workflows, read-only defaults, validated safe outputs, and separately scoped mutation jobs |
| OpenHands | **Defer** | preserve the ACP/backend and multi-repository ownership lessons; its beta service is too large for the MVP control plane |
| Beads | **Adapt** | structured dependency data and explicit sync; do not add Dolt or a second task authority beside Issues/Git |
| Gas Town | **Reject as control plane** | retain capacity, escalation, and teardown lessons without importing its 20–30-agent orchestration stack |
| gstack | **Quarantine** | audit only selected projection, side-effect, egress-receipt, and eval-tier patterns in disposable runtime homes |
| oh-my-agent | **Quarantine** | test one composition/trigger mechanism at a time; do not adopt the full stack |
| Temporal | **Defer** | mature durable workflow engine; introduce only when measured recovery requirements exceed Git/CI leases |
| Cline | **Defer** | treat as an external runtime-adapter target; do not import its hub or marketplace into the platform |
| Goose | **Adapt** | reuse ACP/provider/MCP adapter seams and explicit confirmation/security posture; verify behavior per extension |
| GitHub Spec Kit | **Adapt** | reuse clarification, spec/plan/task artifact shapes and testable acceptance; Issues remain task authority |
| `agent-work-mem` | **Reject as authority** | keep only useful handoff fields; do not use Markdown/flock as execution ownership |
| `cli-collaboration` | **Adapt** | ownership/reserved zones, stop conditions, conflict checks, and destructive negative tests |
| `claude-codex-handoff` | **Adapt** | atomic claims, renewal/takeover, cursors, idempotency, bounded polling, and doctor checks |
| `AniruddhaHumane/handoff` | **Reject as authority** | fold concise snapshot fields into the typed checkpoint; do not create another state store |
| SLSA | **Keep vocabulary** | subject, builder, input, dependency, byproduct, and provenance fields; claim no maturity level |
| in-toto | **Adapt** | versioned Statement and agent-candidate predicate; keep signing separate |
| Sigstore | **Defer** | decide identity, transparency, offline, retention, and revocation policy before integration |
| OpenTelemetry | **Adapt stable core** | trace/link/status primitives as an optional mirror; quarantine version-unstable GenAI names and content export |

## Inherited-component disposition

**Keep:** compact global/repo instruction concept; Issues task graph; Git refs;
worktree isolation; deterministic evals; sanitized receipts; exact-candidate review;
Buzz identity/notification; five-tier memory boundary; pinned-source mechanisms.

**Adapt:** SSSF phase/gate semantics; existing Git lease patterns; handoff fields;
Hermes lineage/checkpoint ideas; Buzz contracts; selected skills with immutable
provenance; context-cache telemetry; current eval and artifact tooling.

**Defer:** Gemini/Antigravity activation; broad Grok/OpenCode adoption; GBrain or
MemPalace as production retrieval; gstack live use; remote Buzz agents; workflow
engines; autonomous memory promotion; best-of-N swarms; new observability stacks.

**Quarantine:** `agent-configs`; `agent-workspace`; old `.agent` contracts;
unlocked/copied/drifted skills and personas; hidden compatibility imports; dormant
hooks; Hermes curator/local-control/stale ACP harness; all-interface WebUI;
historical bots; agent-tools debris; old session prompts and unverified worktrees.

**Reject:** universal master guide; automatic wholesale sync; direct-main or
push-all-branches automation; prompt-only permissions; infinite/no-early-stop
instructions; issue comments as locks; chat/memory/cache as task authority;
self-review; blanket `git add .`, stash, rollback, or worktree prune; a second task
database; automatic merge/deploy/destructive action.

The exhaustive current inventory is
`/Users/man/agent-mesh/docs/migration/INHERITED-COMPONENT-DISPOSITION-MANIFEST.md`:
354 logical inherited components are individually classified, with explicit
unknown-provenance rows instead of an unexamined “everything else” bucket.

## Migration sequence and gates

| Slice | Deliverable | Acceptance | Rollback |
|---|---|---|---|
| 0. Authority | approved architecture, authority table, migration inventory | no concern has two authorities | documentation-only |
| 1. Projection seam | internal module manifest, one inert module, `codex-agents-md@v1` adapter, versioned Codex 0.146.0 loader fixture, drift check, inactive projection receipt | render only to a temporary test destination; deterministic/no-op rebuild; invalid manifests, cycles, duplicate meanings, precedence/context-budget conflicts, ambiguous drift, changed user zones, or hash mismatch fail closed; local rollback probe passes; receipt says `inactive` and activation `unverified` | remove temporary destination and restore fixture baseline |
| 2. Admission | atomic task/resource lease, issue/worktree binding, initial checkpoint | two racing writers produce one winner; loser changes nothing | release lease; retain worktree if ambiguous |
| 3. Continuity | transition event/checkpoint schema and cold-start reader | forced stop after each transition resumes with at most one-transition uncertainty | last durable commit/checkpoint |
| 4. Evidence | artifact manifest and exact-candidate receipt | byte or head change invalidates receipt | preserve raw artifact; rebuild manifest |
| 5. Gates/review | deterministic gate registry, independent review receipt, CI exact-head check | self/stale review fails; corrected candidate reruns all gates | return to changes-requested checkpoint |
| 6. Adapters | conformance fixture for Codex, Claude, Hermes, Buzz, Pi, OpenCode | common fields or explicit unsupported result; activation chain proven | disable one adapter |
| 7. Exhaustion | resource/subscription wait and handoff | injected quota/resource loss creates durable checkpoint without duplicate mutation | queue original adapter or escalate |
| 8. Consolidation | preservation refs/bundles, artifact/cache separation, verified retirement | every head/artifact durable; no owner/process/lease; dry-run and restore checks pass | leave paths in place |

Do not begin a later slice until the prior slice's negative tests pass.

No individual slice pass means the MVP is complete. The final end-to-end gate is
a controlled run of the whole chain:

```text
issue -> atomic attempt/resource leases -> isolated worktree
  -> transition checkpoint -> deterministic gates
  -> independent exact-SHA and artifact-hash review
  -> explicit owner promotion -> teardown receipt
```

The gate must inject quota exhaustion, process death, lease contention, stale
review, and teardown failure. It passes only when recovery produces no duplicate
mutation, no authority ambiguity, an auditable exact candidate, and a closed or
explicitly transferred teardown obligation.

## Immediate P0 controls requiring separate authorization

Before broad implementation, inspect and, if confirmed, disable or constrain:

1. any job that automatically pushes every local branch;
2. any consolidator that commits or pushes governing files without review;
3. Buzz agents accepting messages from `anyone`;
4. runtime profiles with broad host mutation or permission-bypass defaults;
5. old sessions/worktrees carrying superseded instructions;
6. any cleanup while endangered commits or unique ignored artifacts remain.

These are proposed operational changes, not authorized by approval of this brief
unless the user names them explicitly.

## Approved execution boundary

The user approved these two decisions on 2026-08-28:

1. **Architecture:** `agent-mesh` is the one agent-platform source repository;
   the authority model and nine-slice sequence above are the target.
2. **First implementation scope:** begin with Slices 0 and 1 in an isolated
   worktree—module manifest/schema, one inert representative module,
   `codex-agents-md@v1`, a versioned Codex 0.146.0 loader fixture, temporary-path
   projection, deterministic negative/drift/rollback checks, and an inactive
   projection receipt with activation marked `unverified`. No live runtime path
   may be written and no activation, cleanup, service change, GitHub mutation,
   commit, PR, deployment, or product-factory change is included.

## Evidence used

- `/Users/man/agent-mesh/docs/architecture/SDLC-MVP-FIRST-PRINCIPLES.md`
- `/Users/man/agent-mesh/docs/research/SOTA-PRIMARY-SOURCE-COMPARISON.md`
- `/Users/man/agent-mesh/docs/research/SOTA-GITHUB-METADATA-RECEIPT.md`
- `/Users/man/agent-mesh/docs/research/LIVE-RUNTIME-INSTRUCTION-AUDIT.md`
- `/Users/man/agent-mesh/docs/migration/WORKSPACE-CONSOLIDATION-MANIFEST.md`
- `/Users/man/agent-mesh/docs/migration/ARCHITECTURE-EVIDENCE-TRACEABILITY.md`
- `/Users/man/agent-mesh/docs/migration/INHERITED-COMPONENT-DISPOSITION-MANIFEST.md`
- `/Users/man/agent-configs/knowledge/MIKE-INTENT-DEBRIEF-2026-08-28.md`
- `/Users/man/agent-configs/knowledge/multi-agent-handoff-research-2026-08-28.md`
- `/Users/man/.buzz/GUIDES/PORTABLE_AGENT_CONTRACTS.md`
- `/Users/man/agent-workspace/knowledge/disler-github-survey-2026-08-24.md`
- current local loader/config/source inspection and current primary GitHub metadata

APPROVAL STATUS: approved for the incremental execution boundary above
