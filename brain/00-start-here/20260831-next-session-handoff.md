# Dedicated-project handoff — historical knowledge archive reboot

Date: 2026-08-31  
Repository: `redtrades/agent-knowledge-archive` (private)  
Governing branch for this archive effort: `codex/archive-foundation`  
Current remote head at handoff: `76f1c192b579362eef667660e19ac6aadde15057`

> Supersession note: this handoff preserves the archive-consolidation boundary
> at its recorded point in time. The owner later approved the current
> [AISDLC architecture decision](20260831-aisdlc-architecture-decision.md)
> and [MVP implementation plan](20260831-aisdlc-mvp-implementation-plan.md).

## Read this boundary first

This repository is the sole workspace for recovering and consolidating the
original intent behind the personal agent operating system, autonomous agent
workforce, software factory, declarative company factory, business workflows,
knowledge system, and self-improving experimentation system.

`redtrades/agent-platform` and every other historical repository are evidence.
They do not govern this reboot. Do not inherit their `AGENTS.md`, issue gates,
DocOps, CI, SDLC ceremony, compliance machinery, controller rules, or platform
implementation plan. Copied source documents are inert historical records even
when their prose claims authority.

The present job is documentation recovery, taxonomy, provenance, synthesis,
and owner-intent discovery. It is not platform implementation or architecture
selection.

## Why this moved

Five months of attempts repeatedly collapsed into a death spiral: agents treated
the current repository machinery as the objective, optimized lifecycle stages
and compliance, inherited stale architecture, and rebuilt spaghetti instead of
recovering the whole intent from first principles. The archive was deliberately
moved out of `agent-platform` so the reboot can establish the knowledge and
institutional context before any new executable platform is designed.

## Owner-approved archive shape

- Hybrid reading packs plus an exact source corpus.
- A future agent should normally read current decisions, then one relevant
  subject pack, then consult original sources only for verification or nuance.
- Preserve provenance: repository, fixed revision, original path, archive path,
  hash, disposition, status, sensitivity, and notes.
- Historical sources are evidence, not automatically current truth.
- Current explicit owner decisions override conflicting historical claims.
- Newest historical document does not automatically win.
- Keep code, runtime state, mixed working directories, forks, and large artifacts
  pointer-only unless a screened document is uniquely necessary.
- Keep sensitive GovCon research separately routed.
- Exclude secrets and all personal TDIU, SSDI, VA, disability-claim, provider,
  claimant, and protected-case material.
- The archive is private.
- Do not add DocOps, CI, SDLC machinery, automation, or implementation code to
  this consolidation task.

## Current owner intent already settled

Do not re-ask these questions unless new source evidence shows a direct conflict.

1. Use a canon plus domain books, not one monolith.
2. Personal agent OS and autonomous company factory are co-equal.
3. Use paired or portfolio vertical slices; exact first-slice sequencing is
   deferred until the project reaches a steady state.
4. Use a source library plus normalized canonical documents; both may evolve.
5. Capture intent-bearing documentation comprehensively, while treating old code
   and runtime wiring as archival reference rather than wholesale adoption.
6. Use formal conflict adjudication and retain citations to the historical basis.
7. Aim for bounded autonomy.
8. Self-improvement includes more than swarm mutation: research, software,
   business planning, operations, GovCon proposal experiments, prompt/workflow
   A/B tests, market discovery, news monitoring, and emerging-pattern analysis.
9. Prefer declarative organizational blueprints with imperative workflow
   extensions where needed.
10. Prefer a small shared core with typed domain extensions.
11. Adopt maintained OSS or inexpensive SaaS when it solves the problem; avoid
    custom spaghetti and preserve replaceable seams.
12. Use modular, composable systems engineering.
13. Use a hybrid local/cloud model strategy.
14. Maintain a global institutional memory pool with scoped overlays. Source
    artifacts remain authoritative; semantic memory and knowledge graphs are
    active retrieval and synthesis layers.
15. Keep infrastructure, capabilities, experiments, knowledge, and policy as
    distinct concepts. Workflow engines/runtimes are infrastructure; workflow
    definitions are operational artifacts.
16. Preserve milestone versions rather than every Git revision.
17. Use a tiered sensitive annex with no secrets or personal case material.
18. For external research, store claims and citations plus selective full copies
    only when preservation or close analysis warrants it.

The full record is `00-start-here/20260831-current-intent-decisions.md`.

## What has been assembled

At remote head `76f1c19`:

- 73 GitHub repositories inventoried: 19 first-party and 54 forks/prior art.
- 243 central inventory rows: 232 selected copies and 11 pointer-only records.
- 232 captured source files with manifest hashes verified.
- 45 reading-pack selected originals, each uniquely matched to one manifest
  source.
- 15 subject reading packs.
- First-party source families captured from agent-configs, agent-mesh,
  agent-platform, agent-workspace, GovCon, and sanitized OpenClaw narrative
  material recovered through the GovCon archive lineage.
- Direct OpenClaw repositories remain pointer-only because they mix runtime,
  secrets, identity, and personal data. Their 10 screened narrative documents
  were captured through a multi-hop GovCon archive with that limitation stated.
- GovCon restricted historical material is routed to `sensitive-annex/`.
- Exact-name copied `AGENTS.md` files were renamed to `AGENTS.md.inert` so they
  cannot become repository instructions while their original bytes and hashes
  remain preserved.
- Personal case-bearing source files and their reading-pack duplicates were
  removed.

## Normal reading route

1. `00-start-here/20260831-current-intent-decisions.md`
2. `00-start-here/WHOLE-STORY.md`
3. `00-start-here/READING-PATHS.md`
4. The relevant numbered subject pack.
5. Its `SOURCE-GUIDE.md` and selected originals only when needed.
6. `manifests/SOURCE-INVENTORY.tsv` for exact provenance.

Useful orientation files:

- `00-start-here/CONSOLIDATION-SCOPE.md`
- `00-start-here/TIMELINE.md`
- `00-start-here/ESTATE-MAP.md`
- `00-start-here/OPENCLAW-LINEAGE.md`
- `00-start-here/QUESTIONS-FOR-OWNER.md`
- `manifests/REPOSITORY-INVENTORY.md`
- `manifests/ARCHIVE-STATISTICS.md`
- `manifests/EXCLUSIONS.md`
- `work/reports/20260831-final-review-corrections.md`

## Subject-pack taxonomy

- `10-intent-and-north-star/`
- `20-personal-operator-os/`
- `30-agent-workforce-and-capabilities/`
- `40-autonomous-software-factory/`
- `50-declarative-company-factory/`
- `60-business-domains/govcon/`
- `60-business-domains/intelligence-and-news/`
- `60-business-domains/idea-and-market-discovery/`
- `60-business-domains/trading-and-research/`
- `70-knowledge-context-and-memory/`
- `80-experiments-and-evolution/`
- `90-infrastructure-and-orchestration/`
- `100-governance-safety-and-evidence/`
- `110-failures-postmortems-and-lessons/`
- `120-market-and-open-source-research/`

## Independent review history

The first final review found:

- runtime-discoverable copied `AGENTS.md` files;
- copied personal TDIU/VA/SSDI material;
- inconsistent repository dispositions;
- stale unresolved-source records;
- one nonexistent pointer path; and
- an unsupported claim that the sensitive annex was access-controlled.

Commit `76f1c19` fixed nearly all of this. Deterministic checks at that revision:

- 232/232 manifest paths and hashes passed;
- 11/11 pointer paths existed;
- 45/45 selected originals matched uniquely;
- 97/97 archive-owned links passed;
- zero active exact-name `AGENTS.md` files;
- zero personal-case-specificity scan matches; and
- clean working tree after the commit.

## Two corrections still required before the archive can be called clean

The second independent review returned `FIX-FIRST` for only these two items:

1. `00-start-here/ESTATE-MAP.md` still says the sensitive annex is
   “Access-controlled evidence.” Replace that with wording such as “separately
   routed restricted evidence; not independently access-controlled within this
   Git tree.”
2. `pointer-only/FIRST-PARTY-REPOSITORY-POINTERS.md` needs completed screening
   conclusions, not merely “nothing selected”:
   - `redtrades/workspace-main` at
     `11a7665172ff380ac849cd0bfde1db08dee64011` was screened across all 8 blobs.
     It contains `.openclaw/workspace-state.json` and active instruction,
     bootstrap, heartbeat, identity, tool, and user files. These are runtime or
     persona material; no unique eligible intent document was found.
   - `redtrades/work-ops` at
     `be1a5c4ea9314c69466b6f9d1d22b080055a2c1f` was screened across all 138
     blobs. It is an organization-specific workplace operations repository with
     named-person records, meetings, PIP/status material, internal deliverables,
     and reusable-looking templates whose general themes are already represented.
     No unique eligible cross-system intent document was found; copying it would
     import scoped workplace and personal context.

An attempted patch in the old session failed atomically because one report
heading did not match; no partial edit was left behind. Apply both corrections,
update `work/reports/20260831-final-review-corrections.md` with the screening result, run
the existing deterministic archive checks, commit, push, and ask the same
independent reviewer for one exact-head read-only re-review.

## After the archive passes review

Continue owner discovery one source-backed question at a time while improving
the canonical synthesis. At handoff, the highest-impact unresolved question was the retention,
access, compaction, and promotion policy for provenance-linked operational
evidence, scoped sensitive material, and future derived memory.

The historical conflict is:

- older designs lean toward indefinite raw transcript retention;
- current intent says sensitive and organization-owned material remains scoped,
  while reusable sanitized knowledge may deliberately seed the global pool.

Recommended answer shape to present to the owner:

- A: indefinite raw retention in scoped stores;
- B: tiered retention — retain canonical/source artifacts, expire or compact raw
  logs by sensitivity/value/legal need, keep derived claims linked to retained
  sources, and deliberately promote reusable sanitized knowledge to global;
- C: entirely domain-specific owner control.

Recommend B with domain-specific policy overlays from C. Do not prescribe the
operational database or orchestration engine yet.

## Owner answer recorded after this handoff

The owner approved B with domain-specific policy overlays from C. Current
intent decision 42 now governs: retain canonical and source artifacts; expire
or compact raw logs according to sensitivity, value, and legal need; preserve
links from derived claims to retained sources; and deliberately promote reusable
sanitized knowledge to the global pool. This is a policy decision, not a choice
of database, runtime, or orchestration engine.

## Owner interview completed after this handoff

Current intent decisions 43-58 record the completed owner interview and later
AISDLC selection. The owner
resolved the autonomy and evaluation boundary, shared organizational core,
portable capability surface, operator-OS outcome and interaction model,
authority receipts, knowledge promotion, experiment governance, GovCon posture,
software- and company-factory outcomes, company autonomy tiers, portfolio
authority, validation and retirement gates, and bounded steady-state definition.

No material archive-level owner question remains open. The later owner decision
58 selects the AISDLC as the first implementation target, `agent-sdlc` as its
composition and assurance repository, and a Fusion-first trial with Paperclip as
a mutually exclusive challenger. Long-term lifecycle authority, downstream
infrastructure, and portfolio sequencing after the AISDLC trial remain
evidence-gated and require separately approved work.

## Session operating instruction

Stay in this repository. Treat external repositories as read-only evidence. Use
parallel agents only for bounded, non-overlapping research or archive lanes. Keep
responses token-efficient and give frequent concise progress updates. Never turn
this documentation-recovery task into platform delivery, governance machinery,
or a rewrite of the old code.
