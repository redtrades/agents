# Estate map

Repository roles are fixed by
[`20260903-estate-structure-decision.md`](20260903-estate-structure-decision.md):
`agent-knowledge-archive` (canon), `agent-configs` (operative policy),
`agent-sdlc` (AISDLC implementation), and `agent-platform` / `agent-mesh` /
`agent-workspace` / `govcon-factory` (frozen historical evidence).

## Archive layout

| Area | Purpose | Read as |
| --- | --- | --- |
| `00-start-here/` | Current reboot decisions and archive navigation | Current archive record |
| Numbered subject packs | Concise syntheses, conflicts, and source guides by topic | Current interpretation plus labelled history |
| `corpus/first-party/` | Source-preserving first-party evidence at fixed revisions | Historical evidence, never activated instructions |
| `manifests/` | Repository inventory and provenance fragments | Retrieval and disposition evidence |
| `pointer-only/` | Repositories and material intentionally not copied | Pointer-only evidence |
| `sensitive-annex/` | Restricted historical business material | Separately routed restricted evidence; not independently access-controlled within this Git tree; not normal cold-start material |
| `work/reports/` | Capture and reading-pack receipts | Historical consolidation evidence |

## Important boundary

`corpus/first-party/agent-platform/` is evidence from a prior platform effort.
It is not the governing instruction set for this reboot. Likewise, the
OpenClaw repositories are pointer-only except for the screened, multi-hop
narrative capture described in [OpenClaw lineage](OPENCLAW-LINEAGE.md).

For repository-level disposition and fixed references, use the
[repository inventory](../manifests/REPOSITORY-INVENTORY.md).
