# agent-mesh corpus capture

Capture date: 2026-08-31
Source: `/Users/man/agent-mesh` (`redtrades/agent-mesh`, branch
`preserve/uncommitted-2026-08-29`)
Captured revision: `4a663596e1188e2b25116e71b74162bc92abbd96`
Archive root: `corpus/first-party/agent-mesh/4a663596e1188e2b25116e71b74162bc92abbd96/`

## Result

66 commit-backed Markdown files were copied byte-for-byte, totaling 1,278,826
bytes. The manifest has 66 data rows using the 15-column
`manifests/SOURCE-INVENTORY.tsv` schema. All rows identify the full source
commit and `preserve/uncommitted-2026-08-29` source ref; no invented revision or
working-tree snapshot was used.

| Area | Files | Bytes |
|---|---:|---:|
| `research/` (all tracked research Markdown) | 28 | 532,250 |
| `docs/` | 11 | 378,437 |
| root intent/SDLC documents | 6 | 146,330 |
| `hermes/` substantive reports and policy | 10 | 163,111 |
| selected `.agent/` memory/protocol architecture | 5 | 22,360 |
| evaluation documentation | 2 | 7,192 |
| reviews | 1 | 13,613 |
| command-center/swarmclaw documentation | 3 | 26,608 |
| **Total** | **66** | **1,278,826** |

The root-document row includes `README.md`, `DECISIONS.md`, `HANDOFF.md`,
`WORKLOG.md`, `Agent SDLC.md`, and the repository `AGENTS.md`. The Hermes set
covers the README, OMLX/Hermes and Qwen architecture/optimization reports,
benchmark/evidence reports, the permutation matrix, and routing policy.

## Exclusions

- Executable or persona `.agent` surfaces: `.agent/AGENTS.md`, all five
  `.agent/agents/*.md`, all five `.agent/prompts/*.md`, and
  `.agent/protocols/x-retrieval.md`. Five architecture-bearing memory/protocol
  documents were selected as inert history; this is not a wholesale `.agent`
  copy.
- Credential-rotation history: `ROTATION-REQUIRED.md`.
- Evaluation receipts: both tracked README files under
  `evals/receipts/qwen38-flash-next-exact/`; receipt payloads/results and all
  executable evaluation code remain excluded.
- Hermes install/runtime/provider or machine-history notes:
  `hermes/bots/install-notes.md`, all four bot `SOUL.md` files,
  `hermes/m16-node.md`, and `hermes/mcp-config-notes.md`.
- Runtime/status or unrelated operational documentation: monitoring READMEs,
  pipeline READMEs/status, and all `vault/*.md` status/log files.
- All non-Markdown executable code, configs, services, launchd files, model
  metadata, runtime state, dashboards, receipts, and secrets.

The source working tree had exactly one dirty tracked path,
`.obsidian/workspace.json`, and no untracked paths. It was not copied because
it is volatile runtime/UI state. No selected source document differed from its
commit blob at capture time.

## Verification and uncertainties

- Source-to-copy SHA-256 comparison: 66 checked, 0 mismatches.
- Manifest validation: 15 header fields, 66 rows, 0 malformed rows.
- Full `git diff --check` reports 100 trailing-whitespace or blank-line-at-EOF
  warnings in preserved source Markdown; none were introduced or normalized.
  The scoped manifest/report check is clean.
- The source branch name describes a preserved dirty checkout; the captured
  bytes are nevertheless unambiguously from commit
  `4a663596e1188e2b25116e71b74162bc92abbd96`. `current_status` is therefore
  recorded as `local-working-tree` while each row's `source_commit` binds the
  actual bytes.
- Historical documents can mention paths, provider names, token terminology,
  or redaction procedures. No secret value was copied. Current activation of
  any captured instruction/protocol document is not implied; all corpus files
  are inert historical evidence.
