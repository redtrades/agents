# Final review corrections

Date: 2026-08-31
Input: `5f17343fe62f8d0ed5e95e60e859d7828008fc80`
Branch: `codex/archive-review-fixes`

## Corrections

- Renamed the two copied exact-name `AGENTS.md` files to `AGENTS.md.inert`.
  Their original paths and SHA-256 values remain unchanged in the manifest;
  only `archive_path` changed.
- Excluded six personal-case-bearing originals: the owner-intent debrief,
  proactive-agent research, agent-mesh handoff, Hermes README, mine-v1 digest,
  and agent-configs Disler inventory. Also removed the four reading-pack copies
  of the excluded owner-intent debrief. No sanitized derivative was needed.
- Removed the excluded rows from the merged inventory and source fragments,
  removed active source-guide/report references, and recalculated inventory,
  byte, and reading-pack counts.
- Reconciled repository dispositions with capture evidence: `agent-platform` is
  selected-copy inert evidence; direct OpenClaw repositories are pointer-only
  while the ten screened narrative files retain their GovCon-extraction
  provenance; `workspace-main` and `work-ops` are pointer-only because neither
  has a selected manifest document.
- Split completed document-level source-root captures from the three genuinely
  unresolved roots. All 11 manifest pointer rows now route to existing pointer
  documents.
- Replaced the remaining annex access-control claim in `ESTATE-MAP.md` with
  separately routed restricted-evidence wording. No filesystem access-control
  claim is made.
- Completed the pointer-only screening record: `workspace-main` was reviewed
  across all 8 blobs and contains runtime/persona material; `work-ops` was
  reviewed across all 138 blobs and contains scoped workplace/personal context.
  Neither yielded a unique eligible cross-system intent document.
- Fresh exact-head review found and corrected one parallel wording conflict in
  the GovCon decisions record: restricted annex routing does not establish
  independent access control within this Git tree.

## Verification

| Check | Result |
| --- | --- |
| Active archive Markdown links | 97 files checked; 0 broken archive-navigation links. |
| Preserved-original source links | 53 source-relative links remain intentionally unresolved inside byte-preserved corpus/selected originals; the reading guide now explains this provenance boundary. |
| Manifest schema and paths | 243 data rows; every row has 15 columns; 232/232 selected-copy paths exist; 11/11 pointer paths exist. |
| Manifest hashes | 232/232 selected-copy files match SHA-256; 0 mismatches. |
| Selected-original identity | 45/45 selected originals match exactly one manifest source; 0 unmatched; 0 ambiguous. |
| Runtime-discoverable instruction names | 0 exact-name `AGENTS.md` files below the checkout; 2 `AGENTS.md.inert` files retain hashes `72f60c…` and `fd1009…`. |
| Personal-case specificity screen | 0 matches for case-associated names, protected case path, form numbers, diagnoses, leave terms, provider-letter, or claimant-statement patterns. |
| Broad case-term review | 12 files contain generic exclusion, privacy, false-positive-test, or skill-catalog mentions of TDIU/SSDI; manual context review found no personal disability/VA case facts. Generic GovCon veteran/VA procurement material was retained as allowed. |
| Repository disposition totals | 19 first-party repositories = 5 selected-copy + 7 pointer-only + 7 excluded; 54 external repositories remain pointer-only. |

## Limitation

Byte-preserved originals retain their historical source-repository relative
links and cannot be made self-contained without changing bytes and invalidating
their manifest hashes. They are source evidence, not archive navigation; active
archive-owned links are clean.
