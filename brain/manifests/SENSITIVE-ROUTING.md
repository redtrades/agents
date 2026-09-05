# Sensitive Routing

| Class | Archive handling | Routing rule |
| --- | --- | --- |
| Public or ordinary historical documents | `selected-copy` only after document-level review. | Record source path, commit (or `WORKING-TREE-ONLY`), and checksum when copied. |
| Internal operational history | Pointer or selected copy after review. | Keep executable content pointer-only. |
| Sealed OpenClaw/iCloud material | Pointer-only. | Use only to locate a later reviewed, safe document. |
| Credentials and runtime secrets | Exclude. | Never record values, hashes of values, or snippets. |
| TDIU/SSDI/provider/case material | Exclude. | Keep in its protected canonical location. |
| GovCon business material | Selected-copy only when non-case and independently reviewable. | Preserve source provenance and applicable license/terms. |

When a source is local-only or has uncommitted changes, label it `WORKING-TREE-ONLY`; do not invent a Git commit.
