# Estate ledger

Issue: [#15](https://github.com/redtrades/agent-platform/issues/15)

Snapshot: 2026-08-28 17:21 EDT

Correction evidence: 2026-08-28 17:40 EDT. Existing observations remain bound to
the original snapshot; only metadata for the previously omitted Claude session root
was added at correction time. No other volatile count or state was refreshed.

Machine-readable source: [`estate-ledger.json`](./estate-ledger.json)

## Verdict

No estate evidence contradicts the architecture in PR
[#14](https://github.com/redtrades/agent-platform/pull/14) at the comparison head
observed during final reconciliation,
`1503c5d4b7d739402d7e3d171820504b4cc25195`.

The canonical destination, separate GovCon product boundary, selective extraction,
runtime-local state, human destructive gate, and
Keep/Adapt/Archive/Quarantine/Delete phase all match the live evidence. The plan's
phase 4 is a future completion target, not a claim that the estate is already safe
to consolidate.

The initial comparison head, `31eb6f2...`, contained a live-status paragraph that
became stale when PRs #12 and #13 merged. The current comparison head removes live
task status from the evergreen plan, so that earlier factual drift is not a current
contradiction. Issues and the Project remain the live task-state authority.

The ledger tracks eight operational safeguards that the evergreen plan does not
enumerate. **None requires an update to `docs/MASTER-PLAN.md`.** The plan already
governs selective extraction, runtime-local boundaries, exact evidence, recoverable
consolidation, and the human destructive-action gate. These safeguards are issue #15
execution details and future receipt requirements; this ledger cannot create or
change platform policy.

| ID | Safeguard | Master-plan disposition |
| --- | --- | --- |
| `estate-op-01` | Point-in-time owner/state/disposition registry | Ledger execution detail; implements the existing phase-4 estate index |
| `estate-op-02` | Never move mixed live/sensitive `agent-reports` as one root | Ledger execution detail; source-specific hold under existing runtime/sensitive boundaries |
| `estate-op-03` | Owner release plus process, LaunchAgent, path, worktree, issue, and PR preflight | Ledger execution detail; evidence for existing lifecycle/teardown outcomes |
| `estate-op-04` | Exact-head and dirty/untracked/ignored artifact preservation with restore proof | Ledger execution detail; mechanics under existing Git/artifact authority |
| `estate-op-05` | Class-specific routing, including transcript-only unrecovered work | Ledger execution detail; taxonomy under the existing storage map |
| `estate-op-06` | Pre/post manifests, checksums, rollback, retention, and separate deletion approval | Ledger execution detail; receipts under existing recoverability and destructive gates |
| `estate-op-07` | Sanitized-first OpenClaw extraction and raw-object fallback | Ledger execution detail; source-specific application of selective extraction |
| `estate-op-08` | Explicit owners and shutdown/export plans for Qwen, GovCon, FreeLLMAPI, and SSSF | Ledger execution detail; concrete ownership under existing platform/product/runtime boundaries |

If later evidence exposes a new durable policy or architecture boundary, a separate
issue and decision record must update the master plan. This ledger is not that update.

## Machine contract

The JSON schema uses typed `source_locators` arrays. Locator types are `path` and
`glob`; every locator has a globally unique ID. Lifecycle is exactly `active`,
`terminal`, or `unknown`. Aggregate records that contain more than one lifecycle use
`unknown` until their children are split for an approved action. Record IDs, locator
IDs, artifact-class references, requirement IDs, lifecycle values, and master-plan
dispositions are deterministic contract checks.

## Current routing map

| Work surface | Purpose and authority | Current owner/state | Unique value | Disposition | Next action |
| --- | --- | --- | --- | --- | --- |
| `/Users/man/agent-platform` | Canonical platform; Issues/Project 12 own intent, Git/artifact hashes own candidates | Active; `main` `a06660122ef5`; 7 worktrees, 3 dirty | Reviewed contracts, fixtures, receipts | **Keep** | Continue issue-bound delivery; import no legacy root wholesale |
| Agent-platform worktrees/PRs | Exact candidates and review/failure receipts | Mixed; #12/#13/#14 merged, #7/#11 closed, #6/#8/#17 open; issue #16 active | Candidate and exact-head review history | **Keep** | Protect open lanes; retain terminal evidence; teardown only after issue reconciliation and release |
| `/Users/man/agent-mesh` | Legacy benchmark/runtime/migration evidence, not platform authority | Active/dirty; 17 worktrees, 8 dirty; active and idle-unreleased task cwd references | Contracts, eval fixtures, receipts, large Qwen evidence | **Adapt** | Preserve four local-only heads and dirty owners; finish/transfer tasks and benchmarks; extract bounded verified components |
| `/Users/man/agent-configs` | Legacy guidance/config patterns, not governing instruction | Dirty; 5 worktrees; loaded absolute-path LaunchAgent; unique `8449fb2` absent from `origin/*` | Hard-control and adapter patterns | **Adapt** | Preserve unique state, extract tested patterns, separately repoint consumer, then consider quarantine |
| `/Users/man/agent-workspace` | Legacy ADW/harness prototypes, not a second queue/platform | Dirty; 4 worktrees; primary `main` two commits behind upstream at snapshot | Typed phases, gates, traces, adapter fixtures | **Adapt** | Bind dirty owners, separate secrets, test bounded candidates, then consider quarantine |
| `/Users/man/agent-tools` | Loose PR-380 utilities plus opaque outputs | Terminal/unknown; 3.3 MiB, 42 files; no cwd/LaunchAgent refs | Two GovCon PR-380 artifacts; 40-output unknown batch | **Quarantine**, conditional | First preserve/hash PR-380 pair under GovCon, manifest residual batch, refresh path checks, and obtain move approval |
| `/Users/man/agent-reports` | Mixed reports, live installs, vendor trees, caches, backups, credentials | Active/mixed; 2.4 GiB; 53 dirs/12 files; 6 dirty nested repos; 3 live cwd and 8 LaunchAgent consumers | Nearly every artifact class | **Keep and split in place** | Never root-move; route children by owner/class after fresh live and sensitive checks |
| FreeLLMAPI + SSSF report children | Live gateway/server/visualizer and dirty vendor/source trees | Active; node/bun cwd consumers and loaded services | Runtime state, source deltas, operational receipts | **Keep** | Separate export/shutdown/rebuild/repoint/rollback plans and explicit owner release |
| Qwen benchmark evidence | Local-model runs, schemas, receipts, summaries, raw evidence | Active/mixed; `qwen38-flash-next` ~985 MiB; issue #33 active; custom llama.cpp head `a0ccc47` is local-only | Reproducible fixtures, unique raw results, custom cache-persistence source | **Archive** | Preserve custom head; hash and sensitivity-class raw runs; keep small sanitized schemas/summaries; exclude caches/models |
| `/Users/man/govcon-factory` | Separate product factory and product artifact authority | Active/dirty; 81 worktrees, 15 dirty; 21 open-issue, 51 closed-issue, 9 without issue keys | Product code, domain evidence, business artifacts | **Keep** | Protect open lanes; closed-clean still requires release/equivalence; closed-dirty and no-issue remain unresolved |
| Seven former `/private/tmp` GovCon heads | Terminal exact review/work commits | Physical worktrees gone; exact commits still local/API-visible; no local `origin/*` contains them | Exact Git/review identity | **Archive** | Create approved refs/bundles, checksum, patch-compare, and restore-test before any prune |
| `/Users/man/.buzz` | Buzz runtime, nested source clone, research, logs, DBs, caches | Active; ~17 GiB; nested source clone dirty at `631b05c` | Runtime state and sanitized portable-contract research | **Keep** | Keep native; own dirty source separately; adapt only reviewed sanitized contracts; require export/shutdown/rollback for structural change |
| `/Users/man/hermes-webui` | Third-party WebUI source/vendor checkout | Clean tracked state; ~278 MiB; `83e4903`, 56 commits behind upstream | Rebuildable pinned vendor source | **Keep** | Confirm runtime owner/local patch absence, then retain pinned or recreate from verified upstream; exclude dependencies |
| `/Users/man/.hermes` | Hermes config, installed agent, sessions, caches | Active; ~6.3 GiB; live cwd and LaunchAgent | Native runtime state | **Keep** | Keep native; promote audited templates/fixtures only; never copy credential values |
| `/Users/man/.codex` | Codex tasks, managed worktrees, memories, plugins, attachments | Active; ~2.5 GiB; multiple cwd references | Runtime state and selected durable evidence | **Keep** | Prefer commits/issues/manifests over raw transcripts; require runtime teardown receipts |
| `.claude`, `.gemini`, `.grok`, `.agents` | Other native runtimes and installed skill bodies | Active/unknown; ~1.2 GiB, 232 MiB, 1.0 GiB, and 23 MiB | Provider-specific state and candidate adapters/skills | **Keep** | Verify projected/discovered/loaded/activated/behavioral states separately; no bulk promotion |
| `/Users/man/Library/Application Support/Claude/local-agent-mode-sessions` | Claude local-agent session recovery evidence | Unknown; ~360 MiB, 1,515 files; contents not opened | Possible transcript-only unrecovered work | **Keep** | Metadata-match to durable artifacts first; open a bounded recovery issue for unmatched unique work; inspect minimum transcript span only; never bulk-ingest |
| `/Users/man/.openclaw` | Restricted runtime-shaped historical snapshot | Inactive-looking but unreleased; ~3.3 MiB; no cwd/LaunchAgent refs | Historical evidence and possible sensitive state | **Archive** | Keep read-only pending owner release and secret-aware manifest |
| iCloud `OpenClaw-System-History` + `Reference-Archives/OpenClaw*` | Sealed historical evidence | Restricted; System History ~9.1 GiB; reference archives already placed | Provenance and missing-fact fallback | **Archive** | Use sanitized Buzz research first; object-tree inspect only missing facts; never import credentials/runtime wiring |
| Empty `agent-reports/2026-08-24-openclaw-archive` | Zero-value placeholder | Terminal; 0 bytes/children | None | **Delete**, future-only | Leave now; delete only in a separately approved housekeeping wave after final reference check |
| `/Users/man/models` and provider caches | Model weights and reproducible model/dataset/dependency stores | Active/unknown; models ~167 GiB; Hugging Face cache ~16 GiB | Rebuildable cache plus model identities | **Keep** | Keep outside Git; add identity/checksum manifests; separately approve cache contraction |
| Worktree namespaces | Human/runtime execution checkouts | Mixed; 114 registered across the five audited repos | Active source, exact heads, receipts, ignored artifacts | **Keep pending reconciliation** | Classify by owner/task/head/artifact/release, not age or process absence |

Counts and process state are observations, not leases. Absence of a process does not
release a path; presence is sufficient to block relocation. A future action must
refresh every volatile field.

## Terminal Git objects that must survive maintenance

The former physical `/private/tmp` worktrees are absent. These exact GovCon commits
remain Git objects locally and are retrievable through GitHub commit lookup, but no
local `origin/*` remote-tracking branch contains any of them:

- `30699faccbe38a6a50ea636455b5231c460a7de2`
- `75c0811edc638f579a06d7c51d605daf01b8f670`
- `7e3f3fc157b3af4a2fec71f262f738e8dcbb0a59`
- `7d4cd5212c965377b32049281bfe087f1f0ebf8a`
- `b97e4c281c5eab655630f3f390da68f289dc82b4`
- `023e90ede44948ea79076da261d7ceae7b2c8973`
- `7d8368ba5c09da5c6e95292ce041f2dd4e609a40`

Before any prune or Git maintenance, give each an approved preservation ref and
verified bundle; record checksum, issue/PR provenance, patch relationship, and an
isolated restore result. A similar later patch does not preserve exact review
identity. Four `agent-mesh` heads have the same preserve-before-release rule because
no local remote-tracking ref contains them and GitHub commit lookup did not resolve
them:

- `5e0762e88823000066614b852c74f0534b2e9ec2`
- `72f8ae3543c90eaf5d1330cf77297f840eaba89f`
- `7f69a3f2e2eda2cd322aa5cc188bf1a93a0f7936`
- `fdcf7ee06b5eb9bb2552e166930322cbbb7d0416`

The clean unique `agent-configs` head
`8449fb21353e807488959b758cb2bd4cc2dce365` is also local-only and must be
preserved before release.

## Artifact routing rules

| Class | Destination rule |
| --- | --- |
| Reviewed source/contracts | Issue-bound candidate in owning source repo; current tests, exact-candidate review, promotion under approved risk policy; destructive/high-risk gates remain human-held |
| Small deterministic fixtures/schemas | Owning source repo when sanitized and test-required |
| Durable receipts/summaries | Small summary and hash in Git; larger evidence in immutable artifact storage |
| Large raw evidence | Content-addressed archive with producer, provenance, sensitivity, and restore metadata |
| Product-owned artifacts | Product issue/artifact store, never `agent-platform` solely because an agent produced them |
| Live runtime/DB/log state | Native runtime until approved export, shutdown, path-independence, and rollback |
| Reproducible cache/model/dataset | Outside Git; remove only in a separate cache wave after consumer and rebuild checks |
| Secrets/raw private prompts/config backups | Restricted native or sealed store; opaque references only |
| Unknown provenance | One restricted batch manifest and quarantine; no content promotion without provenance |
| Sealed historical archive | Immutable restricted evidence; object-level extraction only for a missing fact |
| Transcript-only unrecovered work | Keep raw session restricted; metadata-match first; for unmatched work open a bounded recovery issue, inspect only the minimum needed span, and promote a reviewed durable artifact with provenance |

## Executable sequence

No action below is authorized by this ledger. A later issue must name exact paths and
the approved wave.

1. **Refresh and freeze.** Recheck GitHub, worktrees, dirty/untracked/ignored state,
   process cwd, LaunchAgents, static paths, sizes, and sensitive-presence indicators.
   Assign every candidate one owner, destination or hold, and release decision.
2. **Preserve Git and dirty work.** Create approved refs and bundles for endangered
   heads; checksum, verify, patch-compare, and restore-test. Route dirty files by
   owning task without blanket add or stash.
3. **Extract bounded value.** Adapt only issue-selected contracts, fixtures, schemas,
   and summaries. Archive large evidence by hash. Metadata-match session evidence to
   durable artifacts; recover transcript-only work only through a bounded issue and
   minimum necessary inspection. Keep products, runtimes, raw sessions, caches,
   secrets, and sealed history in their owning boundaries.
4. **Release consumers.** Obtain owner release, finish or transfer tasks, drain
   worktrees, and separately approve service export/stop/repoint/rollback. Repeat the
   exact path search.
5. **Quarantine reversibly.** For each exact approved path, record a pre-move manifest
   and checksums, move to restricted recoverable storage, verify counts/hashes, test
   rollback, and retain a source-to-destination receipt.
6. **Decide deletion separately.** After retention and fresh independent review,
   request human approval naming exact deletions. Quarantine never implies deletion.

The first plausible whole-root quarantine remains `/Users/man/agent-tools`, and only
after the PR-380 pair and residual batch clear their holds. No material move is safe
now. `/Users/man/agent-reports` is permanently excluded from whole-root movement.
