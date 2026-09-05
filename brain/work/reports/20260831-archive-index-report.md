# Archive-index report

Observed: 2026-08-31. Scope was limited to the central manifest, archive statistics, external-fork pointers, and this report.

## Commands and exact outcomes

- git status --short --branch -> ## codex/archive-index; clean before edits.
- Final-review correction supersedes the original snapshot counts below: the merged inventory now has 243 data rows and one 15-column header (232 selected-copy; 11 pointer-only).
- Merge check -> no exact full-row duplicates or duplicate source-ID/archive-path keys.
- Archive path check -> all 232 captured selected-copy files exist; every pointer row routes to an existing pointer document.
- SHA-256 check -> 232/232 captured corpus/annex files match the manifest; 0 mismatches.
- Reading-pack identity check -> 45/45 selected-originals/ files match a corpus or annex file; each has exactly one manifest match; 0 unmatched and 0 ambiguous.
- Fork inventory check -> 54/54 fork entries copied as pointer-only rows in pointer-only/EXTERNAL-FORKS.md; no clone/copy performed.
- git diff --check -- manifests/SOURCE-INVENTORY.tsv manifests/ARCHIVE-STATISTICS.md pointer-only/EXTERNAL-FORKS.md pointer-only/UNRESOLVED-SOURCE-ROOTS.md work/reports/20260831-archive-index-report.md -> exit 0; no whitespace errors.
- git status --short -> four correction files changed; captured fragments and source files unchanged.

## Commit

- Prior index commit: 3075e8c170fc96400dfa88d2d4e11ab4cd6288f9; correction commit contains this report and the verified files.

## Concerns

- Six source roots remain unresolved for document-level selection; they are pointer-only and documented in pointer-only/UNRESOLVED-SOURCE-ROOTS.md.
- Functional fork groupings are retrieval labels from the inventory, not content findings; forks remain pointer-only.
