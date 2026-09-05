# omlx / Hermes notes moved to agent-mesh

2026-08-27. Per Mike's ruling, **`~/agent-mesh` owns the live Hermes + omlx
surface** (`~/.hermes/config.yaml`, `~/.omlx`, the omlx launchd service, model
downloads) and is the home for omlx/Hermes infra knowledge. `agent-workspace`
sessions do not edit those directly.

The five 2026-08-26 `omlx-qwen38-oq4e-*` notes that were briefly staged here
(untracked) are byte-identical to the canonical copies in agent-mesh and have
been removed. Read them there:

- `~/agent-mesh/research/omlx-qwen38-oq4e-installer-preflight-snapshot-2026-08-26.md`
- `~/agent-mesh/research/omlx-qwen38-oq4e-setup-and-bench-2026-08-26.md`
- `~/agent-mesh/research/omlx-qwen38-oq4e-profile-verify-2026-08-26.md`
- `~/agent-mesh/research/omlx-qwen38-oq4e-hermes-desktop-2026-08-26.md`
- `~/agent-mesh/research/omlx-qwen38-oq4e-ideal-config-2026-08-26.md`
- index: `~/agent-mesh/research/INDEX.md`

Newer work:
- MCP verified state + config-writer root cause:
  `~/agent-mesh/research/hermes-mcp-verified-state-2026-08-27.md`
  (agent-mesh PR #30, issue #29)
- Benchmarks: `~/agent-mesh/hermes/benchmark-results-2026-08-27.md`,
  `~/agent-mesh/hermes/MASTER-PERMUTATIONS-MATRIX.md`
