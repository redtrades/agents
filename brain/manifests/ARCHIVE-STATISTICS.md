# Archive statistics

Observed: 2026-08-31. Counts are from the merged inventory and the files present in this archive repository.

## Repository counts

- 73 repositories in the estate inventory: 19 first-party and 54 forks/external prior-art repositories. The archive repository is excluded.
- First-party dispositions: 5 selected-copy, 7 pointer-only, and 7 excluded.
- External forks: 54 pointer-only; no fork was cloned or copied.

## Central inventory

- 243 data rows and exactly one 15-column header.
- Dispositions: 232 selected-copy and 11 pointer-only.
- The 232 selected-copy rows are captured source documents. The 11 pointer-only rows comprise four resolved captured-root pointers, three unresolved source-root pointers, three sealed OpenClaw pointers, and one local reference-root pointer. Repeated source IDs are retained when archive paths differ; no exact duplicate full rows or duplicate source-ID/archive-path keys were found.

## Copied source documents

| Source family | Documents | Bytes |
| --- | ---: | ---: |
| agent-configs | 12 | 153,073 |
| agent-mesh | 62 | 1,212,638 |
| agent-platform | 69 | 785,685 |
| agent-workspace | 22 | 372,536 |
| govcon-factory | 16 | 539,282 |
| openclaw | 10 | 184,439 |
| sensitive-annex/govcon-factory | 41 | 651,237 |
| **Total** | **232** | **3,898,890** |

All 232 captured archive files exist and match their manifest SHA-256 values (232/232; 0 mismatches). The sensitive annex contains 41 files (651,237 bytes) and remains separately routed; this routing statement does not claim independently established filesystem access control.

## Reading packs

- 15 reading packs contain 66 curated reading files and 45 selected-originals/ files.
- All 45 selected originals are byte-identical to at least one corpus or annex file (45/45). Each matched exactly one manifest source; ambiguity count is 0.

## Pointer-only and exclusions

- Central pointer-only items: 11. Four roots with completed document-level capture route to `pointer-only/CAPTURED-SOURCE-ROOTS.md`; three unresolved roots route to `pointer-only/UNRESOLVED-SOURCE-ROOTS.md`; three sealed OpenClaw roots route to `pointer-only/OPENCLAW-SOURCES-AND-EXCLUSIONS.md`; and one reference root routes to `pointer-only/REFERENCE-SOURCE-ROOTS.md`.
- Exclusion policy covers seven classes: secrets; executable/runtime material; TDIU/P&T/SSDI/provider/VA case material; OpenClaw state/backups; forks; unrelated projects; and unreviewed untracked local material.
- The GovCon/OpenClaw screen rejected 3 narrative documents and 17 council documents; no excluded source was copied.

## Working-tree sources

- 66 source rows are marked local-working-tree (62 agent-mesh documents plus 4 preserved root pointers).
- 10 rows are working-tree-only or use an explicit `WORKING-TREE-ONLY`/working-tree snapshot source status; no commit was invented.

## Unresolved provenance

- 0 unmatched selected originals; 0 ambiguous selected-original matches; 0 copied-file hash mismatches.
- Three source roots remain unresolved and point to `pointer-only/UNRESOLVED-SOURCE-ROOTS.md`. Resolved captured roots are documented separately. Every pointer row routes to an existing pointer document, and no copied destination is nonexistent.
