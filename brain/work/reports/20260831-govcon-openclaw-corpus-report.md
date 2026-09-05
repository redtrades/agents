# GovCon and OpenClaw corpus capture report

Captured 2026-08-31 from `redtrades/govcon-factory` commit
`512ad991401862482ad8595ca4fc0b97b519c2ad`.

| Route | Files | Bytes | Content class |
| --- | ---: | ---: | --- |
| `corpus/first-party/govcon-factory` | 16 | 539,282 | decisions, architecture, research, retrospectives, and stack selection |
| `corpus/first-party/openclaw` | 10 | 184,439 | sanitized OpenClaw narrative set observed in GovCon |
| `sensitive-annex/govcon-factory` | 41 | 651,237 | plans, financials, GTM, outreach, and screened council materials |
| **Total** | **67** | **1,374,958** | byte-preserved copies |

Every copied file has a row in `manifests/fragments/govcon-openclaw.tsv`, using
the 15-column source-inventory schema, an exact source commit, a full SHA-256,
sensitivity, and era authority. The OpenClaw rows record their multi-hop lineage
through the GovCon issue-53 archive extraction.

## Checks

- SHA-256 values were generated from each archive copy and verified against its
  source blob after capture.
- Secret-pattern scan found no matches among copied files.
- Case-material scan found no `TDIU`, `SSDI`, disability-claim, medical-record,
  or Veterans Benefits matches among copied files.
- Probable actual firm-identifier screening removed three candidate documents;
  the final copied set has no matches.
- A baseline-preserving `git diff --check` passed with blank-line and
  trailing-whitespace checking disabled. The default check reports inherited
  whitespace in four byte-preserved source documents; those bytes were not
  normalized.

## Exclusions and unresolved provenance

All OpenClaw direct repositories, local runtime, and sealed archive roots remain
pointer-only because they mix narrative material with runtime wiring, state,
credentials, backup contents, and/or personal or case material. No original
OpenClaw commit was inferred for the ten sanitized derivative documents; their
physical source is the recorded GovCon commit and their original lineage is
explicitly marked as unresolved beyond the issue-53 archive extraction.
