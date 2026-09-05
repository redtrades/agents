# Workspace consolidation manifest — 2026-08-28

> **Destination correction, 2026-08-28:** the canonical platform source is the new
> `/Users/man/agent-platform` / `redtrades/agent-platform` repository. Any statement
> below naming `agent-mesh` as the permanent destination is superseded. Its inventory,
> preservation constraints, runtime boundaries, and cleanup waves remain evidence.

Status: **proposal and preservation map; no cleanup authorized**

This manifest records the current `/Users/man` agent-development sprawl and a
safe consolidation sequence. It does not authorize moving, deleting, pruning,
committing, pushing, changing refs, or mutating GitHub. State is changing while
multiple tasks are active, so every execution decision must be revalidated at
the moment of action.

## Executive finding

The problem is not just too many folders. Four different classes of state have
been mixed together:

1. canonical source repositories;
2. task worktrees and standalone review clones;
3. live runtime state for Codex, Claude, Gemini, Hermes, and Buzz;
4. caches, model data, raw run outputs, receipts, and historical reports.

Those classes need different durability and lifecycle rules. Combining platform,
product, vendor, runtime, and artifact state in one Git repository would make the
failure mode worse. The immediate target is one agent-platform source repository
(`agent-mesh`), separate product-factory and upstream/vendor repositories, one
human-managed worktree namespace, runtime-owned directories left native to their
runtimes, and separate artifact and cache stores.

## Snapshot and limitations

Read-only observations were collected on 2026-08-28 from:

- `git status --porcelain`, `git worktree list --porcelain`, local reachability,
  and dry-run worktree-prune output;
- live GitHub issue and PR metadata through `gh`;
- live remote-ref checks through `git ls-remote`;
- directory sizes and current-process working directories through `du` and
  `lsof`.

No fetch was performed because it would mutate local remote-tracking refs.
Reachability claims therefore distinguish local remote-tracking evidence from
live exact-SHA remote-ref evidence. Directory-size figures are allocated/logical
blocks and may overstate recoverable APFS space.

The snapshot itself demonstrates the race: `agent-mesh` grew from 10 registered
physical worktrees during the first audit to 19 during the final snapshot as
isolated research lanes were created. A static Markdown inventory is evidence,
not an execution lease or a live registry.

## Proposed source-repository boundaries

| Current path | Observed purpose | Proposed authority and disposition |
|---|---|---|
| `/Users/man/agent-mesh` | Platform research, runtime adapters, pipelines, evaluations, and deployment evidence | **Keep as the sole agent-platform source repo.** Contracts, runtime adapters, issue/board projections, control-plane logic, receipts, and evals belong as internal modules here; do not create a sibling `agent-contracts`, policy, or control repo. It is not the task queue, runtime state store, or global prompt authority. Primary checkout is dirty and actively used; do not move it in the cleanup phase. |
| `/Users/man/govcon-factory` | GovCon product code, domain knowledge, business artifacts, and product pipelines | **Keep as an independent product repo.** It must not absorb global agent policy or raw runtime state. Primary checkout contains protected research and financial-model work. |
| `/Users/man/.buzz/REPOS/buzz` | Clean clone of upstream `block/buzz` | **Keep separate as upstream product source.** `/Users/man/.buzz` is runtime state, not this repository. If a fork is required, give it its own explicit source path and remote. |
| `/Users/man/agent-configs` | Historical cross-project rules, skills, hooks, prompts, and roles | **Treat as a migration input, then archive/quarantine after extraction.** Its contents are candidates, not currently trusted global authority. Selectively tested contracts, adapters, or skill material belong in internal `agent-mesh` modules, never a replacement sibling repo. It was dirty during the snapshot and `MASTER-GUIDE.md` was deleted in the primary checkout. |
| `/Users/man/agent-workspace` | Historical file-and-Git coordination system, ADW code, knowledge, and Markdown task board | **Treat as a migration input, then archive/quarantine after extraction.** Unique platform harness/source code belongs in internal `agent-mesh` modules; unique evidence belongs in artifacts or `agent-mesh` research; product-specific material routes to its owning product factory. The Markdown queue/claim system must not remain a second active control plane beside GitHub. Do not merge blindly. |
| `/Users/man/hermes-webui` | Third-party `nesquena/hermes-webui` clone with local dependencies | **Keep as vendor source or recreate from a pinned upstream ref.** It is 56 commits behind and contains `node_modules`; do not treat its checkout as durable runtime state. |
| `/Users/man/.local/src/llama.cpp-qwen38-flash-next` | Third-party `ggml-org/llama.cpp` source with a custom worktree | **Keep separate as upstream engine source.** Preserve the custom worktree commit before any relocation. |
| `/Users/man/dotfiles` | Independent personal configuration repository | **Out of scope for repository consolidation.** It is dirty and must not be swept into agent policy. |

This leaves three clear long-lived domains: one agent platform (`agent-mesh`),
separate product factories (`govcon-factory` and any future product-owned repos),
and upstream/vendor source (`Buzz`, Hermes WebUI, llama.cpp). `agent-configs` and
`agent-workspace` are temporary migration inputs only. After selected material is
classified, tested, and extracted to its owning `agent-mesh`, product, artifact,
or cache destination, preserve them as read-only archives/quarantine rather than
maintaining sibling platform repositories.

Moving the existing primary clones under a new `/Users/man/src` hierarchy is
**deferred**. Their absolute paths are embedded in app project records, services,
scripts, and active processes. The first cleanup should canonicalize new
worktrees and separate artifacts without moving the primary clones.

## Namespace map and exact proposed disposition

### Worktree namespaces

Current registered counts:

| Common repository | Physical | Prunable registrations | Immediate rule |
|---|---:|---:|---|
| `/Users/man/agent-mesh` | 19 | 0 | Active; keep and inventory by task/thread. |
| `/Users/man/agent-workspace` | 4 | 1 | Protect dirty primary; reconcile the stale registration. |
| `/Users/man/agent-configs` | 5 | 0 | Protect dirty primary and unique Hermes commit. |
| `/Users/man/govcon-factory` | 81 | 50 | Freeze creation; preservation pass before any prune. |
| **Total** | **109** | **51** | No bulk cleanup. |

Observed physical namespaces:

| Path | Observed size/state | Proposed disposition |
|---|---|---|
| `/Users/man/worktrees/redtrades/agent-mesh` | New canonical namespace; three isolated research lanes at final snapshot | **Keep.** This is the target for new human-managed worktrees. |
| `/Users/man/.codex/worktrees/*` | Seven live `agent-mesh` worktrees at final snapshot | **Runtime-managed exception.** Do not move while tasks exist. Register task/thread/path/base/head and let Codex lifecycle remove them after verified completion. |
| `/Users/man/agent-mesh-worktrees` | Seven legacy worktrees, about 15.7 MB | **Drain.** Retain open/dirty work in place until durable; recreate retained work under the canonical namespace only after it is inactive. |
| `/Users/man/agent-mesh-wt` | One legacy worktree, about 1.7 MB | **Drain** under the same rule. |
| `/Users/man/agent-workspace-wt` and `/Users/man/aw-wt` | One worktree each | **Drain** after PR and artifact reconciliation. |
| `/Users/man/.worktrees` | Mixed owners, about 5.59 GB: GovCon, agent configs, agent workspace, and llama.cpp | **Stop using as a mixed namespace.** Classify every child by common Git directory; preserve unique heads; then retire completed children individually. |
| `/Users/man/gcf-wt` | 15 GovCon worktrees, about 1.91 GB | **Drain** into the canonical namespace or retire after exact-head verification. |
| `/Users/man/govcon-factory-worktrees` | 19 top-level children, about 16.44 GB | **Drain carefully.** It includes 18 Git checkouts plus a non-Git RFP artifact directory and a standalone clone. |
| `/Users/man/govcon-factory-wt` | Empty | **Wave 3 removal candidate** only after confirming no path consumer references it. |
| `/Users/man/.buzz/.scratch/govcon-*` | Four standalone GovCon clones, not worktrees of the canonical clone | **Buzz-active protected.** Treat as review/source snapshots; prove reachability and extract any unique review evidence before retirement. |

Canonical human-managed worktree path:

```text
/Users/man/worktrees/<owner>/<repo>/<issue-or-pr>-<slug>
```

Examples:

```text
/Users/man/worktrees/redtrades/agent-mesh/issue-42-repo-hygiene
/Users/man/worktrees/redtrades/govcon-factory/issue-435-perf-cache
/Users/man/worktrees/ggml-org/llama.cpp/pr-26004-cache-persist
```

Runtime-created worktrees may remain under a runtime-native directory, but the
admission receipt must record that exception and the runtime must own teardown.

### Runtime and control state

| Path | Observed role | Proposed disposition |
|---|---|---|
| `/Users/man/.buzz` | About 18.4 GB; live Buzz ACP, Node, and Codex processes; contains `REPOS`, `.scratch`, `OUTBOX`, `RESEARCH`, `WORK_LOGS`, and archives | **Keep live and separate.** Never fold the whole directory into Git. Separate the clean source clone from runtime databases, keys, caches, and durable outputs through a Buzz-specific shutdown and export plan. |
| `/Users/man/.hermes` | About 6.96 GB of live Hermes configuration/state/cache | **Keep runtime-native.** Promote only audited portable contracts/config templates; never copy credentials. |
| `/Users/man/.codex` | About 2.50 GB of tasks, worktrees, attachments, memories, plugins, and runtime state | **Keep runtime-native.** Do not consolidate raw sessions into a source repo. Export selected evidence through manifests. |
| `/Users/man/.claude` | About 1.28 GB | **Keep runtime-native and quarantined from global-policy redesign.** A Claude process had `/Users/man/agent-workspace` as cwd during the snapshot, even though active work status was uncertain. |
| `/Users/man/.gemini` | About 244 MB | **Keep runtime-native.** Audit loaded instructions independently before any shared-policy claim. |
| `/Users/man/.agents` | About 24 MB of skill material | **Quarantine and inventory.** Presence does not prove discovery or correctness. |
| `/Users/man/models` | About 179 GB | **Dedicated model store; never Git or worktree content.** Add model identity/checksum manifests elsewhere. |

### Artifacts, reports, and caches

| Path | Observed content | Proposed disposition |
|---|---|---|
| `/Users/man/agent-reports` | About 2.62 GB; reports, backups, worktree snapshots, and an explicit `credentials` directory | **Protected archive, not a repo.** Never blanket-`git init`, publish, or bulk-move. Inventory and secret-classify first; promote sanitized, unique reports by checksum. |
| `/Users/man/agent-tools` | About 3.4 MB; mostly UUID-named text outputs plus GovCon PR-380 restoration scripts | **Artifact/debris triage.** GovCon restoration code belongs with its issue evidence if still needed; opaque text outputs require provenance or archival disposition. It is not a coherent source repo. |
| `/Users/man/agent-mesh/evals` | About 1.89 GB | Split source/tests from generated evidence and dependencies. |
| `/Users/man/agent-mesh/evals/promptfoo/node_modules` | About 1.7 GB, ignored and reproducible | **Cache.** Recreate from the lockfile after consumers are stopped; never artifact-store or commit it. |
| `/Users/man/agent-mesh/evals/receipts` | About 5.77 MB; 11 small tracked receipt/schema files and ignored raw runs | **Durable evaluation artifacts.** Preserve raw request/response/log data in content-addressed artifact storage; keep small schemas, summaries, and hashes in Git. Review for prompt, topology, and provider-sensitive data. |
| GovCon `factory/.cache` across physical worktrees | About 14.88 GB aggregate | **Shared data/cache tier, not per-worktree.** One ignored `usaspending.db` is 13.71 GB, its source ZIP is 394 MB, and two worktrees each contain a 253 MB opportunities CSV. |
| GovCon `operations`, `runs`, and `samples` across physical worktrees | About 3.76 GB, 3.16 GB, and 1.32 GB aggregate | Separate durable raw run evidence from small deterministic fixtures. Current Git trees replicate roughly 37.5 MB of `runs` blobs and 15.8 MB of `samples` per worktree. |
| `/Users/man/govcon-factory-worktrees/any-rfp-issue-80` | Non-Git directory containing an extracted RFP run | **Protected artifact, not a worktree.** Preserve by checksum and sensitivity classification, then relocate only in an approved artifact wave. |
| `/Users/man/govcon-factory-worktrees/gf-health` | Standalone clean detached GovCon clone, not registered to the primary clone | **Duplicate clone candidate.** Verify exact remote reachability and absence of unique ignored artifacts before retirement. |
| `/Users/man/workspace` and `/Users/man/harness-eval-2026-08-16` | Empty at snapshot | **Wave 3 removal candidates** after path-reference search and explicit approval. |

Proposed durable paths, subject to implementation approval:

```text
/Users/man/artifacts/<owner>/<repo>/<artifact-kind>/<run-id>/
/Users/man/caches/<owner>/<repo>/<dataset-or-tool>/
/Users/man/artifacts/git-preservation/<owner>/<repo>/<sha>/
```

Artifacts are immutable, content-addressed, checksummed, and described by a small
manifest. Caches are reproducible and disposable. Secrets and credentials stay
in runtime-native secret stores and are referenced only by opaque name.

## Endangered Git objects

### Prunable registrations with non-remote recorded heads

`git worktree prune -n -v` currently proposes removal of 50 GovCon
registrations. Seven recorded HEADs had commits absent from local remote-tracking
refs. Only the first exact SHA appeared in a live remote-ref check:

| Missing physical path | Recorded HEAD | Live evidence and required disposition |
|---|---|---|
| `/private/tmp/gf-r10-348` | `30699faccbe38a6a50ea636455b5231c460a7de2` | Exact SHA remains at `refs/pull/348/head`; merged PR 348. Still manifest/bundle before pruning if exact review provenance matters. |
| `/private/tmp/gf-r3-249` | `75c0811edc638f579a06d7c51d605daf01b8f670` | No live exact ref. PR 249 now points to `b82420802328640c239977fbdc40f9aae511b1ea`. Preserve and compare patches. |
| `/private/tmp/gf-r6-298` | `7e3f3fc157b3af4a2fec71f262f738e8dcbb0a59` | No live exact ref. PR 298 now points to `22ce84bfca9cbbe8189ce630827bc4cff17327b9`. Preserve and compare patches. |
| `/private/tmp/gf-rev-229` | `7d4cd5212c965377b32049281bfe087f1f0ebf8a` | No live ref or associated PR found. Preserve before registry pruning. |
| `/private/tmp/gf-rev-262` | `b97e4c281c5eab655630f3f390da68f289dc82b4` | No live ref or associated PR found. Preserve before registry pruning. |
| `/private/tmp/gf-rev-405` | `023e90ede44948ea79076da261d7ceae7b2c8973` | No live exact ref. PR 405 now points to `e05b23dc38179a3f3b1519e454e90ca4ce8dab28`. Preserve and compare patches. |
| `/private/tmp/govcon-pr-103-rereview-wt` | `7d8368ba5c09da5c6e95292ce041f2dd4e609a40` | No live exact ref. Merged PR 103 records head `e7aaa02650237d648d44c6c1c0c2a8638be8f0a0`. Preserve rereview evidence before pruning. |

The other 43 GovCon prunable registrations and the one `agent-workspace`
registration appeared reachable from local remote-tracking refs, but must still
be rechecked live before execution.

### Physical unique heads

| Physical path | HEAD | Protection reason |
|---|---|---|
| `/Users/man/agent-mesh` | `7f69a3f2e2eda2cd322aa5cc188bf1a93a0f7936` | Dirty and active. Exact local head was absent from live refs; open PR 36 had moved to `1cf77ce5391d268e6687bef47d4aa955a370bdf0`. |
| `/Users/man/.worktrees/agent-configs-hermes-clean-mesh` | `8449fb21353e807488959b758cb2bd4cc2dce365` | Clean but absent from live refs; issue 36 open and no PR found. |
| `/Users/man/.worktrees/llama.cpp-qwen38-cache-persist-pr26004` | `a0ccc47f540426b6e61841b2000dd2e87e022bab` | Clean local custom commit. Upstream PR 26004 points to a different SHA, `06d9d0ff54b586514a59268e2c780abc08473daa`. |

## Dirty and active protections

The final snapshot found substantive dirty state in:

- `/Users/man/agent-mesh`;
- `/Users/man/agent-mesh-worktrees/qwen-iq4-agentic-k123-issue-35-v2`;
- `/Users/man/agent-workspace`;
- `/Users/man/agent-configs`;
- `/Users/man/govcon-factory`;
- `/Users/man/.worktrees/gf-263`;
- `/Users/man/.worktrees/gf-294`;
- `/Users/man/.worktrees/govcon-factory-issue-181`;
- `/Users/man/gcf-wt/issue-388`;
- `/Users/man/gcf-wt/issue-391`;
- `/Users/man/gcf-wt/teardown-backlog`;
- `/Users/man/govcon-factory-worktrees/openwiki-pilot-issue-164`.

Seven additional GovCon worktrees contained only Hypothesis/cache residue, but
that classification must be repeated immediately before cleanup. Ignored files
are not safe merely because ordinary `git status` omits them.

Current-process cwd evidence protects at least:

- `/Users/man/.buzz`: many Buzz ACP, Node, and Codex processes;
- `/Users/man/agent-mesh`: Codex, model-server, Python, Node, and shell processes;
- `/Users/man/agent-workspace`: Claude and shell processes;
- `/Users/man/govcon-factory`: a shell process.

Process presence does not prove useful work, but it is sufficient to block
relocation or teardown until the owning task/runtime confirms release.

## Safe execution waves

### Wave 0 — freeze and live inventory

Goal: establish a trustworthy admission boundary before cleanup.

1. Stop creating manual worktrees outside
   `/Users/man/worktrees/<owner>/<repo>/...`.
2. Freeze cleanup mutations across all listed source, worktree, runtime, and
   artifact paths. Runtime-managed tasks may finish but must report ownership.
3. Generate a machine-readable inventory row for every checkout with:
   `repo`, `common_git_dir`, `path`, `branch`, `base_sha`, `head_sha`, `dirty`,
   `untracked`, `ignored_bytes`, `issue`, `pr`, `task_or_thread`, `owner`,
   `lease_expiry`, `last_heartbeat`, `process_evidence`, and `disposition`.
4. Query current GitHub issue/PR state and live remote refs. Do not infer an
   atomic lease from labels, assignees, comments, or a Markdown `owner` field.
5. Mark as protected if any of these is true: active process/task, substantive
   dirty state, untracked content, ignored durable evidence, open issue/PR,
   unreachable exact head, sensitive content, or unknown ownership.
6. Require an explicit owner release before a protected path enters a later wave.

Exit condition: every path is classified, every active lane is identified, and
no cleanup candidate has an unresolved owner or unknown durability.

### Wave 1 — preserve Git state and dirty work

Goal: make loss impossible before changing registrations or directories.

1. For each endangered SHA, create an approved namespaced preservation ref and
   a Git bundle under the Git-preservation artifact path.
2. Record bundle checksum, source common Git directory, exact SHA, subject,
   issue/PR association, and patch-equivalence result.
3. Verify with `git bundle verify` and an isolated restore test. A current PR
   containing similar content does not preserve an older review commit's identity.
4. For dirty work, enumerate files by owning task. Never use `git add .` or a
   blanket stash in a shared/contaminated checkout.
5. Secret-scan and preserve authorized source on an issue-bound branch/draft PR;
   preserve non-source artifacts by checksum. Conflicts or ambiguous ownership
   stop the wave for that path.
6. Re-run reachability and clean-state checks after preservation.

Exit condition: every unique commit is reachable from an intentional ref or
verified bundle, and every substantive dirty/untracked artifact has a durable,
owned destination.

### Wave 2 — separate artifacts and caches

Goal: stop every worktree from carrying runtime and evidence payloads.

1. Classify each generated path as source, small fixture, durable artifact,
   reproducible cache, secret, or unknown.
2. Copy durable artifacts first to a content-addressed destination; generate and
   verify manifests before any source removal.
3. Keep only schemas, small deterministic fixtures, summaries, and artifact
   hashes in source Git.
4. Move dataset caches and dependency installs behind explicit cache roots or
   configurable paths. Verify consumers against the new paths in isolation.
5. Keep credentials in runtime-native secret stores. Redact or seal historical
   outputs containing credentials, private prompts, client material, or topology.
6. Do not alter live Buzz/Hermes/Codex/Claude/Gemini state until that runtime has
   a tested export, shutdown, and rollback procedure.

Exit condition: manifests resolve and verify, consumers pass deterministic tests,
and no unique evidence exists only inside a cleanup candidate.

### Wave 3 — approved worktree and namespace cleanup

Goal: retire only proven redundant state.

Preconditions for each worktree:

- inactive owner and no relevant process;
- clean tracked, untracked, and ignored durable state;
- exact HEAD live-reachable or intentionally preserved;
- issue/PR disposition reconciled;
- artifact manifests verified;
- no path consumer or runtime registration depends on its absolute path.

Sequence:

1. Re-run the full preflight immediately before action.
2. Preview stale metadata with `git worktree prune -n -v`.
3. Remove completed worktrees individually through `git worktree remove`, never
   by recursive filesystem deletion.
4. Treat local/remote branch deletion as a separate approval-gated operation.
5. Recreate retained inactive manual worktrees under the canonical namespace;
   leave runtime-owned worktrees native until their runtime tears them down.
6. Handle standalone clones and non-Git artifact folders through their own
   verified archive/removal procedures, not `git worktree` commands.
7. Remove empty legacy namespaces only after a path-reference search, rollback
   record, and explicit approval.
8. Re-run registry, reachability, GitHub, artifact, and process checks.

Exit condition: no stale registration, duplicate active clone, unexplained dirty
path, or unresolved artifact remains; every retained worktree has an issue/task,
owner, exact base/head, lease/heartbeat, and teardown owner.

## SDLC lifecycle mismatches to resolve

The current primary `/Users/man/agent-mesh/Agent SDLC.md` is valuable research,
not a coherent authority. The filesystem evidence exposes several contradictions
that the clean-room SDLC must settle:

- It proposes Beads, one-file-per-task ownership, `MASTER.md`, and GitHub Issues
  in different sections. Only one control plane should be authoritative.
- A Markdown `owner` plus timestamp is described as a lock, but current repo
  policy correctly states that issues, labels, comments, and files are not atomic
  execution leases.
- One section explicitly excludes worktrees from the MVP, while later sections
  require worktrees for parallel work. The live system already needs worktree
  lifecycle management because worktrees are being created automatically.
- “Git as persistence” is correct for source and small manifests, but the audit
  proves raw runs and caches multiply across every worktree. Raw artifacts need a
  separate content-addressed tier.
- Blanket `git add .`, automatic stash/commit, and automatic rollback suggestions
  are unsafe in shared dirty checkouts and must be rejected.
- Per-session worktrees without task admission and teardown receipts cause the
  exact proliferation observed here. The durable unit should be a bounded task or
  review attempt, not an unconstrained conversation.

The clean-room invariant should be:

> An issue records human-visible intent. A successful compare-and-swap execution
> lease, recorded by an admission receipt, binds one bounded attempt to an owner,
> task/thread, workspace, branch, base SHA, head SHA, heartbeat, stop condition,
> and teardown owner. The receipt proves acquisition; it is not the mutual-
> exclusion primitive. Git identifies source state; external artifact manifests
> identify generated evidence. Promotion and teardown require deterministic checks
> plus an independent exact-head review.

## Acceptance checklist for any future cleanup execution

- [ ] Current user approval names the exact cleanup wave and paths.
- [ ] Live owner/task/process inventory is refreshed.
- [ ] All seven prunable endangered SHAs and all physical unique heads are
      intentionally preserved or proven equivalent with recorded evidence.
- [ ] Dirty, untracked, and ignored durable content has an owner and verified
      destination.
- [ ] Sensitive reports, RFP data, financial models, credentials, and raw prompts
      are classified and protected.
- [ ] Artifact manifests and restore tests pass.
- [ ] `git worktree prune -n -v` is reviewed after preservation.
- [ ] Each removal is individual, recoverable where practical, and independently
      reviewed.
- [ ] Branch/ref deletion, GitHub mutation, runtime shutdown, and primary-repo
      relocation have separate explicit authority.
- [ ] Final registry, GitHub, artifact, runtime, and path-reference checks pass.
