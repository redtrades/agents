# Architecture evidence traceability — 2026-08-28

Status: **supporting research crosswalk; no implementation or cleanup authorized**

This document maps the proposed clean-room SDLC requirements and named subsystems
to the strongest evidence already collected. It does not repeat the architecture
brief or start a new landscape survey. “Observed” means a local file, process,
database, Git state, or upstream primary source was inspected. A file's presence
does not prove that a runtime loaded it, and a prior successful smoke test does not
prove current health.

KADR means **Keep**, **Adapt**, **Defer**, or **Reject**. A mixed disposition keeps
the useful mechanism while rejecting an unsafe authority claim.

## Evidence set and freshness

The three completed task outputs are:

- SDLC synthesis:
  `/Users/man/agent-mesh/docs/architecture/SDLC-MVP-FIRST-PRINCIPLES.md`
- live instruction/runtime audit:
  `/Users/man/agent-mesh/docs/research/LIVE-RUNTIME-INSTRUCTION-AUDIT.md`
- filesystem/worktree preservation map:
  `/Users/man/agent-mesh/docs/migration/WORKSPACE-CONSOLIDATION-MANIFEST.md`

All local observations below are from 2026-08-28. GitHub, process, branch, worktree,
and runtime state can change immediately; refresh it at admission, promotion, and
teardown rather than treating this Markdown as a live registry.

Repository boundary for this crosswalk: `/Users/man/agent-mesh` is the sole
agent-platform source repository. Contracts, adapters, Issues/Project projections,
control-plane logic, receipts, and evals are internal modules of that repo, not
sibling repositories. Product factories remain separate. Runtime state and
upstream/vendor source remain outside the platform repo. `/Users/man/agent-configs`
and `/Users/man/agent-workspace` are migration inputs to classify and selectively
extract, then archive/quarantine; they are not future co-authorities.

## Eight required properties

These are the eight numbered properties in the SDLC synthesis at lines 47–58.

| # | Required property | Strongest observed evidence | Failure or contradiction | KADR | Missing proof before approval |
|---:|---|---|---|---|---|
| 1 | One mutating owner per task and shared resource | GitHub Issues are already the human queue; Git-backed resource leases have been used; the Buzz contract distinguishes signed author and verifier identities. | `/Users/man/agent-mesh/.agent/protocols/issue-as-spine.md:10-19` incorrectly calls an Issue comment timestamp a mutex. Labels, comments, assignees, Markdown owner fields, and receipts are evidence, not compare-and-swap mutual exclusion. | **Adapt** existing claims into one atomic task/resource lease; **Reject** comment/file locks. | Race test with two contenders; one winner, zero loser mutations; explicit heartbeat, expiry, takeover, stop, and release semantics. |
| 2 | Every mutation is issue-linked and isolated in a worktree | Current repo policy and active lanes use Issues and worktrees. The workspace manifest found 109 physical worktrees and 51 prunable registrations, proving both real use and lifecycle need (`workspace-consolidation-manifest...:75-115`). | `/Users/man/agent-mesh/.agent/protocols/issue-as-spine.md:13-16` binds one worktree to one *session*, which caused proliferation; many dirty, unique, and process-active trees make blind consolidation unsafe. | **Keep** issue linkage and file isolation; **Adapt** to one worktree per bounded mutating task/review attempt; **Reject** per-session creation and shared dirty mutation. | Admission must prove common Git dir, issue, branch, exact base/head, clean initial state, owner/lease, and teardown owner; runtime-native exceptions need receipts. |
| 3 | Git commits and hashes reconstruct the candidate without chat | `/Users/man/agent-mesh/evals/tracking/receipt.py:39-52,240-269` records suite hashes, Git commit/dirty state, provider/model, and only a hash of private raw output. The memory design also requires committed-byte references and payload hashes (`.agent/memory/ARCHITECTURE.md:47-68`). | Dirty/unpushed trees, ignored evidence, moving PR heads, and endangered SHAs mean a branch name or chat link is insufficient. Git is unsuitable for large raw runs and caches. | **Keep** exact refs and hashes; **Adapt** with external content-addressed artifacts; **Reject** chat, moving heads, and worktree paths as candidate identity. | Cold reconstruction from exact base/head plus artifact manifest; remote durability of all required Git objects; hash verification with no session state. |
| 4 | Checkpoint is at most one meaningful transition stale | Existing handoff blocks require changed/verified/next/gotchas (`issue-as-spine.md:49-67`), and the SDLC synthesis defines transition checkpoints with exact candidate and lease state. | Current handoffs are prose-only and session-ended/timer-driven. Five same-turn writes and multiple ledgers (`issue-as-spine.md:23-34`) create partial-order drift rather than one atomic checkpoint. | **Adapt** to one transition checkpoint; **Reject** timers as durability and duplicated status stores as co-authority. | Forced-stop test after each meaningful transition; recovery loses at most one transition and never duplicates mutation. |
| 5 | Deterministic gates precede independent judgment | SSSF's local `sssf.db` contains `sessions`, `phases`, `events`, and `gate_results`; Buzz requires a different verifier pubkey (`PORTABLE_AGENT_CONTRACTS.md:156-202,294-305`); offline evals exercise seven contracts (`evals/LIVE-MODE.md:3-12`). | SSSF has only five recorded sessions and its known synchronous local-model run hung for 1,490 seconds (`disler-github-survey-2026-08-24.md:39-53`). File/role labels alone do not prove reviewer independence. | **Keep** deterministic-first and generator-not-judge; **Adapt** SSSF gate semantics and Buzz identity evidence; **Reject** self-receipts. | Exact actor/runtime identity correlation, fail-closed gate registry, injected deterministic failures, and independent exact-SHA review. |
| 6 | Review and promotion name the same immutable SHA and artifacts | The receipt schema validates exact Git SHA, suite hashes, raw-export hash, versions, and verdict consistency (`evals/tracking/receipt.py:357-467`). The workspace audit compared recorded worktree heads to live PR refs. | Several historical PR heads had moved; one physical `agent-mesh` head and multiple review heads were absent from live refs (`workspace-consolidation-manifest...:156-185`). Current receipts do not uniformly name base SHA, head SHA, artifact set, reviewer, and CI promotion target. | **Keep** exact-hash receipts; **Adapt** to one provider-neutral candidate envelope; **Reject** branch-name or stale-PR approval. | Negative test: changing PR head or artifact byte invalidates every acceptance receipt; CI must verify and promote that exact head. |
| 7 | Quota/resource exhaustion leaves a recoverable checkpoint, with no silent fallback or duplicate | The live eval uses a process-held lock and records recovery metadata (`evals/LIVE-MODE.md:14-49`); the SDLC synthesis specifies checkpoint-before-fallback and visible waiting. | SSSF lacks queueing/backoff for a contended local model. Buzz has no demonstrated durable same-run wake/resume. Existing routing research proposes fallbacks, but no universal adapter proves checkpoint, lease release/retention, and idempotent resume. | **Adapt** explicit resource leases and typed stop reasons; **Defer** automatic fallback until failure-injection passes; **Reject** silent model/provider substitution. | Inject quota, rate-limit, process death, and local-server contention in every adapter; prove exact candidate continuity and no duplicate external effect. |
| 8 | Provider loading, tools, auth, and sessions remain in adapters | The live runtime audit traces actual loaders separately: Codex global/repo contracts, Claude registered hooks, Hermes context priority and progressive skill loading, Buzz-generated cwd/context, Pi ancestor walk, and OpenCode named agents. | Cross-runtime “universal” instructions are false. OpenCode base `AGENTS.md`/`CLAUDE.md` discovery remains locally unverified; stale pre-cleanup sessions can retain old prompts; Hermes profile/toolset changes skill visibility. | **Keep** compact verified runtime contracts; **Adapt** a common adapter output schema; **Reject** bulk universal loading and “file exists = active.” | Fresh-session activation probes per runtime/profile, emitted context/skill inventory, auth/tool capability checks, and an explicit unsupported result where evidence is absent. |

## Named subsystem crosswalk

| Subsystem | Strongest observed evidence | Failure or contradiction | KADR disposition | Unverified before approval |
|---|---|---|---|---|
| Disler / SSSF | The 2026-08-24 direct-source survey covered 53 Disler repos (`/Users/man/agent-workspace/knowledge/disler-github-survey-2026-08-24.md:1-37`). Local SSSF has phase scripts under `/Users/man/agent-workspace/adws/` and a 221,184-byte `/Users/man/agent-workspace/adws/adw_data/sssf.db` with 5 sessions, 18 phases, and 203 events. | The survey reused an earlier SSSF install audit rather than re-auditing upstream (`:39-56`); most surveyed repos lacked a license; synchronous model contention already produced a 1,490-second zero-token hang. `/Users/man/agent-mesh/swarmclaw/README.md:5-8` calls `sssf.db` the “backend of record,” conflicting with Issues/Git as authority. | **Adapt** typed phases, deterministic gates, trace schema, and selected independently licensed patterns. **Reject** wholesale import and SSSF DB as task authority. **Defer** sandbox/fan-out/autonomy. | Current upstream/version/license comparison, a fresh typed-gate run, contention recovery, and mapping SSSF events to the common candidate/receipt schema. |
| Buzz | `/Users/man/.buzz/REPOS/buzz` is the clean upstream source clone; live Buzz/ACP processes use `/Users/man/.buzz`. The portable contract uses signed pubkeys, independent receipts, bounded handoffs, and owner approval (`/Users/man/.buzz/GUIDES/PORTABLE_AGENT_CONTRACTS.md:12-23,42-52,156-202,294-310`). The runtime audit traces the actual managed template and provider cwd. | A Buzz assignment/thread is not an execution lease. Nest files are not automatically remote Git durable. “Buzz thread or issue is the task spine” must mean human intent/discovery, not source, lease, or promotion authority. | **Adapt** signed identity, launch/routing, notification, and independent receipt ideas. **Reject** assignment/chat as mutex or immutable truth. | Durable wake/resume, exact mapping of pubkey to runtime/model/human, artifact export, and adapter failure-injection. |
| GBrain | Current observation: `/Users/man/.gbrain` is about 42 MB; PID 5575 was running `gbrain serve --surface starter`; `/Users/man/.gbrain/brain.pglite/postmaster.pid` and `.gbrain-resolve.sock` were timestamped 2026-08-28 12:47 EDT. | This directly contradicts the SDLC draft's “GBrain is empty/unhealthy” statement. Presence and a process prove neither query correctness nor provenance. `/Users/man/gbrain/state/interview.json` is only 36 bytes and was not opened because it may be personal state. | **Defer** integration; later **Adapt** only scoped advisory recall. **Reject** GBrain as task, lease, candidate, or promotion authority. | Read-only health/query probe with approved scope, corpus provenance, privacy boundaries, temporal correctness, and a real golden set. |
| MemPalace | The install record names exact clone/version/store paths and a successful mine/search/MCP smoke test (`/Users/man/agent-mesh/pipelines/memory/mempalace-setup.md:1-48`). `/Users/man/.mempalace` currently exists (~664 KB); `/Users/man/tools/mempalace` exists (~472 MB). | Hermes wiring is explicitly draft-only (`:53-73`); no MemPalace process was observed. The claim “none blocking” (`:99-107`) applies to install, not production recall quality or runtime activation. It is independent from GBrain, so adopting both would create two semantic stores. | **Keep** the historical smoke receipt. **Defer** runtime integration. **Reject** it as handoff/task authority and reject dual-store adoption without measured need. | Fresh search/MCP health, approved data boundaries, runtime activation receipt, retrieval golden set, and a one-store decision. |
| Skills | The runtime audit proves progressive/on-demand loading for Hermes and Pi and distinguishes Codex plugin discovery from body injection. Local roots contain approximately 97 `.agents`, 9 Claude, 6 Codex, 10 `agent-configs`, and 18 GovCon `SKILL.md` files. | Multiple overlapping roots and selectively copied Disler material create provenance and activation ambiguity. Hermes default config currently suppresses the automatic skills catalog; a stale generated snapshot mentions old universal rules. Presence is not activation. | **Adapt** a minimal audited registry as an internal `agent-mesh` module, with source/license, explicit trigger, loader path, profile, and conformance probe. **Quarantine/Defer** the rest. **Reject** bulk sync, policy-by-skill, and a sibling skills/contracts repo. | Fresh per-runtime/profile discovery and invocation probes, source/license inventory, duplicate resolution, and negative tests showing unselected skills are not injected. |
| Caching | Existing research records official OpenAI and Anthropic cache mechanics and proposes stable-to-volatile prompt ordering (`/Users/man/agent-mesh/research/research-caching-routing.md:12-16,144-185`; [OpenAI](https://developers.openai.com/api/docs/guides/prompt-caching), [Anthropic](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)). Live eval policy accepts cache reuse only from explicit reused-token telemetry (`evals/LIVE-MODE.md:92-100`). | Timing, response quality, `n_past`, and cache-directory size do not prove reuse. Large generated caches are mixed into worktrees: `evals/promptfoo/node_modules` was ~1.7 GB and one GovCon `usaspending.db` was ~13.71 GB. Published layout guidance is not proof that current runtime requests preserve bytes. | **Keep** stable-prefix design and telemetry standard. **Adapt** per runtime adapter and separate artifact/cache roots. **Reject** timing-only claims and per-worktree large-cache copies. | Captured request-prefix hashes plus provider/server cache counters, controlled cold/warm runs, current loaded settings, and invalidation tests. |
| Handoffs | Issue handoff blocks already require context, changed, verified, next, and gotchas (`issue-as-spine.md:49-67`); the SDLC draft adds exact refs, tree state, rejected/do-not/boundary/unverified, and lease state. | `Agent SDLC.md`, `HANDOFF.md`, Issue comments, and multiple ledgers offer overlapping prose formats. They are not atomic and do not bind candidate identity. Timer/session-end handoffs can miss the last meaningful transition. | **Adapt** into one transition checkpoint linked from the Issue. **Reject** Markdown ownership as mutex and reject chat-only continuity. | Cold-start exercise across two different runtimes after forced termination; exact state reconstruction and no repeated side effect. |
| Worktrees | The preservation map is the strongest evidence: 109 physical worktrees, 51 prunable registrations, seven prunable endangered heads, three physical unique heads, dirty trees, and active cwd protections (`workspace-consolidation-manifest...:75-115,156-215`). | “Prunable” is registry metadata, not safe-to-delete proof. Physical state, ignored artifacts, active processes, and remote reachability diverge. Per-session creation generated the observed sprawl. | **Keep** one task/review-attempt worktree. **Adapt** canonical namespace and teardown receipts. **Reject** blind prune, blanket stash/add, shared dirty mutation, and bulk relocation. | Live re-inventory at execution, explicit owner release, exact-head preservation, clean tracked/untracked/ignored proof, no process/lease/path consumer, and artifact restore. |
| Receipts | The eval converter is fail-closed, uses allowlisted scalars, hashes private raw exports, validates exact schema, SHA formats, counts, and verdict (`evals/tracking/receipt.py:1-36,240-269,357-467`). Buzz independently rejects self-receipts. | Existing receipts are domain-specific and do not uniformly bind issue, attempt, lease token, base/head, artifact set, adapter, gate versions, author, reviewer, CI, and teardown. A receipt records successful lease acquisition; it is not the CAS primitive. | **Keep** hashes, sanitation, exact verdict, and independent signer. **Adapt** one provider-neutral envelope plus typed domain payloads. **Reject** self-receipts and moving-head receipts. | Schema compatibility tests, identity correlation, signature/attestation choice, private/public boundary tests, stale-candidate invalidation, and artifact restore. |
| GitHub Issues | `/Users/man/agent-mesh/.agent/protocols/issue-as-spine.md:1-6,69-75` correctly treats Issues as the human queue/pointer layer. GitHub supports native sub-issues ([GitHub documentation](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/adding-sub-issues)); issue #40 was observed using a cross-repo native subissue graph: [redtrades/agent-mesh#40](https://github.com/redtrades/agent-mesh/issues/40). | The snapshot also found parent and child work simultaneously labeled ready, agent-workspace issue #4 using narrative dependencies, and Project v2 #11 stale. Comments are non-atomic; Issue/Project/ledger status can disagree. | **Keep** Issues/subissues as intent, dependency, acceptance, and discovery. **Adapt** eligibility rules and one-way derived projections. **Reject** Issue comments as leases and Project/ledger as competing authority. | Refresh live graph and board; prove parents cannot admit while blocking children are open; establish reconciliation behavior when Issue, Git, and receipt disagree. |
| Evals | Offline mode deterministically checks seven contracts; live Qwen/Hermes mode is opt-in, loopback-only, time-bounded, locked, and writes outside Git (`/Users/man/agent-mesh/evals/LIVE-MODE.md:3-49`). The planner caps at 24 rows and marks every row `planned-not-executed` until a receipt fills it (`:51-90`). | Planned matrices are not executed evidence. Current memory retrieval is explicitly deferred (`:102-115`). Runtime/model quality, tool success, cache reuse, and independent judgment are separate claims and must not collapse into one “pass.” | **Keep** offline-first, bounded live, fail-closed receipts, and explicit unrun state. **Adapt** every eval to immutable candidate/adapter identity and external artifacts. **Defer** broad model tournaments. **Reject** self-judging and timing-only cache claims. | Exact current candidate run, tool/repository workflow quality, failure injection, independent review, privacy-safe artifacts, reproducibility, and CI exact-head binding. |

## Cross-artifact disagreements that must be resolved

1. **Lease versus receipt:** the only safe wording is: a successful CAS execution
   lease authorizes mutation; an admission receipt records that success. The receipt
   itself does not provide mutual exclusion.
2. **GBrain state:** replace “empty/unhealthy” in the SDLC draft with “live process
   and PGlite state observed; functional health, corpus provenance, and recall quality
   unknown.”
3. **SSSF authority:** SwarmClaw may read `sssf.db` for run observability, but the DB
   cannot be “backend of record” for task eligibility, candidate identity, or
   promotion. Issues, Git, leases, artifacts, and receipts have distinct authority.
4. **Buzz authority:** Buzz can be launcher, roster, signed identity, handoff surface,
   and human notification. Its thread/assignment cannot substitute for an execution
   lease or remote-durable candidate.
5. **Memory retention:** `/Users/man/agent-mesh/.agent/memory/ARCHITECTURE.md:35-45`
   says raw transcripts are retained forever and `:47-100` creates several Git
   ledgers. The clean-room SDLC instead needs classified retention, private artifact
   storage, and one task authority. Keep provenance and verbatim ancestors; reject
   universal forever-retention and ledger duplication until privacy/cost/authority
   policy is approved.
6. **Runtime activation:** the runtime audit disproves the assumption that one
   `AGENTS.md`, `CLAUDE.md`, or skill tree is universal. It also identifies active,
   dormant, explicit-only, generated, stale-session, and unverified surfaces. The
   adapter must emit an activation receipt rather than infer activation from files.
7. **Worktree unit:** the older session-bound rule conflicts with live sprawl and the
   SDLC's bounded-task unit. One task/review attempt may cross runtime handoffs while
   retaining the same worktree and lease.
8. **Artifacts versus caches:** Git can hold source, small fixtures, manifests, and
   summaries. Raw runs and durable evidence require content-addressed artifact
   storage; dependencies and regenerable datasets require a separate cache lifecycle.

## Approval blockers and minimum trace

Implementation approval should wait until one reconciled brief names:

1. the single authority map for intent, eligibility, mutual exclusion, source,
   evidence, review, promotion, and teardown, implemented through internal
   `agent-mesh` modules for contracts, adapters, projections/control, and evals;
2. the CAS lease primitive and its race-tested failure semantics;
3. the provider-neutral candidate, checkpoint, activation, and receipt envelopes;
4. the exact runtime adapters included in MVP and explicit unsupported behaviors;
5. artifact/cache/privacy retention classes and restore tests;
6. a thin end-to-end acceptance fixture proving issue -> lease -> worktree ->
   checkpoint -> deterministic gates -> independent exact-SHA review -> promotion ->
   teardown, including injected quota and process failure;
7. preservation of every endangered SHA and active/dirty path before any cleanup;
8. explicit owner choices for one semantic store (or none in MVP), skill quarantine,
   and whether Project v2 remains a derived view.

Until those are approved and mechanically tested, the existing files are evidence
and candidate patterns, not hard runtime law.
