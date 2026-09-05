# The Agent Platform Chronicle — consolidated reference (2026-08-30)

**What this is.** One consolidated reference synthesized from a full audit of every
`agent-*` repository (local and GitHub), the five `openclaw*` archival repos, the
OpenClaw-era sealed history, the pre-wipe archives, and all research corpora
(OpenClaw mining, the genetic-swarm constitution, the 2026-08-26 overnight research
wave, the Apple Silicon model program, platform comparisons, and the product-factory
corpora). Every claim below carries a pointer to where the original file, commit,
receipt, or citation lives. Nothing in this chronicle is new authority: it is a
navigation and synthesis layer over the governing docs.

**Authority order (unchanged).** `agent-platform` GitHub Issues + Project 12 own
intent; Git objects and receipts own candidate state; `docs/START-HERE.md` owns
cold start; everything else here is evidence or a navigation map. Legacy repos
(`agent-mesh`, `agent-configs`, `agent-workspace`, `agent-reports`, `agent-tools`,
`govcon-factory`, `openclaw*`) are read-only migration evidence per
`docs/START-HERE.md` §Entry contract.

## Contents

| File | What it answers |
|---|---|
| `TIMELINE.md` | The full chronology: OpenClaw v1→v3 → pre-wipe archive → agent-mesh overnight build → agent-configs → agent-platform canonical authority. Every era with repo/commit pointers. |
| `ESTATE-MAP.md` | Every repository and archive location in the estate: what it is, its current disposition (Keep/Adapt/Archive/Quarantine per the estate ledger), and what to read inside it. |
| `RESEARCH-CATALOG.md` | Every research corpus across the entire history — OpenClaw mining digests, the overnight 12 + hardware 6 + 5 research files, platform comparisons, product corpora — with one-line takeaways and paths. |
| `GENETIC-SWARM.md` | The "genetic swarm" lineage: Mike's verbatim direction (2026-04-24), the SWARM-CONSTITUTION, Mind/Body/Brain, Baseline-5 topology, GEPA/evolutionary-self-improvement research — and where each concept survives today. |
| `CANONICAL-BASELINE.md` | The canonical reference implementation: what it is, the exact verified proof chain, the component registry, the open gaps, and the decision supersession chain. The one-page answer to "what should the canonical implementation be." |

## Read order

- New agent / cold start: `agent-platform/docs/START-HERE.md` → this README →
  `CANONICAL-BASELINE.md`.
- "How did we get here?": `TIMELINE.md` → `GENETIC-SWARM.md`.
- "Where does X live?": `ESTATE-MAP.md` → `RESEARCH-CATALOG.md`.
- Prior consolidation work is preserved and superseded-by-inclusion: the 2026-08-30
  earlier pass lives at `agent-platform/docs/CANONICAL-REFERENCE.md`,
  `docs/CANONICAL-INDEX.md`, and `docs/synthesis/` (SYNTHESIS.md,
  COMPONENT-REGISTRY.md, DECISION-LOG.md, S-001..S-010). This chronicle absorbs and
  extends them; those files remain valid for their audit-pass evidence.

## Method and honesty rules

- Synthesized from primary sources read this pass (2026-08-30): local working trees,
  `git log`/`ls-files`, GitHub API (`gh`), and the sealed archives. No receipts,
  commit IDs, decision numbers, or model numbers were invented; each is copied from
  a source document or live API answer named at its pointer.
- Where a claim can only be reconstructed (e.g., original OpenClaw repo URLs beyond
  the archive reference), it is labeled **[reconstructed]**.
- Volatile counts (issue states, worktree counts, sizes) are point-in-time
  observations dated 2026-08-30; refresh before acting on them, per
  `migration/ESTATE-LEDGER.md` §"Counts are observations, not leases."
