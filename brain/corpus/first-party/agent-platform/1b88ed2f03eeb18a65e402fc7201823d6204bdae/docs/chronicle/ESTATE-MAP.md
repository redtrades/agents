# Estate map — every repository and archive in the agent estate

Dispositions are from `agent-platform/migration/ESTATE-LEDGER.md` (snapshot
2026-08-28 17:21 EDT, correction 17:40) — the ledger is the authority; this map
is its readable index. Counts are observations, not leases.

## Tier A — Canonical (Keep)

### `~/agent-platform` — `redtrades/agent-platform`
Provider-neutral agent software factory: contracts, control logic (Gate C
controller, dispatcher, identity/CAS), deterministic CI gates, receipts,
runtime adapters, fixtures, and all governing docs. Sole work board (Issues +
Project 12 as projection). ~29 MiB local; 159 commits as of 2026-08-30.
- Governing: `docs/START-HERE.md` → `MASTER-PLAN.md` → `ARCHITECTURE.md` →
  `CONTROLLER.md` → `OPERATING-MODEL.md` → `DISPATCH-LOOP.md` →
  `AUTONOMOUS-LOOP.md` → `COMMIT-IDENTITY.md` → `CI-GATES.md` →
  `DELIVERY-FAILURE-LEDGER.md` (DFL-001..020 / AP-01..027 — sole anti-pattern
  register) → `GOAL.md` → `ROLES.md` / `SKILLS.md` / `REVIEW-PROTOCOL.md` /
  `JULES-DISPATCH.md` / `WORKER-CREDENTIAL-ISOLATION.md` /
  `GITHUB-FREE-PRIVATE-BOUNDARY.md`.
- Code: `tools/controller/` (15 .mjs: gate_c, run_gate_c,
  github_contents_authority CAS 640 lines, dispatcher, dispatch_eligibility,
  capacity_policy, run_dispatch, claim_reaper/reconciler, work_item_contract,
  terminal_projection_parity, execution_budget, autonomous_readiness,
  worker_isolation_fixture, github_task_admission), `tools/ci/run_gates.py`,
  `tools/identity/` (configure_git_identity.py, validate_commit_range.py 626
  lines), `tools/adapters/{implementer,reviewer}`, `platform/` (control
  schemas + src), `runtime-adapters/` (contract.py, cli.py, projector.py,
  receipts.py), `proofs/gate-c-live-{69,81,86,103}.txt`, `tests/`,
  `scripts/check-worktree-hygiene.sh`.
- Consolidation layers: `docs/CANONICAL-REFERENCE.md`,
  `docs/CANONICAL-INDEX.md`, `docs/synthesis/{SYNTHESIS,COMPONENT-REGISTRY,DECISION-LOG}.md`
  (2026-08-30 earlier pass; absorbed by this chronicle), `docs/chronicle/`
  (this set), `research/SELF-HOSTED-PLATFORM-COMPARISON.md`,
  `objective-drift-research.md`, root queue-triage artifacts dated 2026-08-30.

### `~/govcon-factory` — `redtrades/govcon-factory` (product, Keep)
Separate product factory + product authority; never a second platform queue.
3 pipelines (packet 9 stages / report 8 / snapshot 8), 9 gates, fail-closed
envelope runner with SQLite trace. Its SDLC (claims-branch CAS locks via
`scripts/issue-claim.sh`, reviewer-bot, merge tiers T0/T1/T2) is the pattern
the platform generalizes. Research corpora under `research/` +
`knowledge/research/` (winning-proposal-teardown, gtm-playbook, offer-design,
…). Personal/health/VA material is excluded from this repo by rule.

### Runtime homes — Keep native, never bulk-promote
`~/.hermes` (~6.3 GiB), `~/.codex` (~2.5 GiB), `~/.buzz` (~17 GiB),
`.claude`/`.gemini`/`.grok`/`.agents`, `~/models` (~167 GiB) + HF cache,
`~/Library/Application Support/Claude/local-agent-mode-sessions` (~360 MiB,
contents unopened — transcript-only unrecovered work possible; bounded recovery
issue required before any ingest). Pointers: ESTATE-LEDGER rows.

## Tier B — Legacy, Adapting (read-only migration evidence)

### `~/agent-mesh` — `redtrades/agent-mesh` (Adapt; ~1.8 GiB local)
Portable brain + research corpus + evals + pipelines + command-center + vault.
Highest-value extracts: `research/` (28 files), `DECISIONS.md` D-001..D-035,
`HANDOFF.md`, `WORKLOG.md`, `.agent/` (personas/protocols/memory),
`hermes/` benchmark architecture notes, `swarmclaw/` PWA, `evals/` (YAML golden
cases, tracking phase), `pipelines/`, `command-center/`, `vault/`,
`monitoring/service-links/`.
- Warning: `FreeLLM API.md` (provider API-key strings) is **untracked** — not
  committed on any branch (verified via `git ls-files` this pass); it is a local
  secret-bearing residue, route under the secrets/artifact rules, never
  promote. `ROTATION-REQUIRED.md` is the committed rotation ledger.
- 4 local-only heads must survive git maintenance: `5e0762e8…`, `72f8ae35…`,
  `7f69a3f2…`, `fdcf7ee0…` (ESTATE-LEDGER §Terminal Git objects).
- Worktrees: `~/agent-mesh-worktrees/`, `~/agent-mesh-wt`,
  `~/worktrees/redtrades/agent-mesh/`.

### `~/agent-configs` — `redtrades/agent-configs` (Adapt; 5.4 MiB)
The library: `rules/` (10), `skills/` (11), `hooks/`, `prompts/`, `roles/`,
`knowledge/` (MIKE-INTENT-DEBRIEF-2026-08-28 + multi-agent handoff research),
`proposals/` (0001–0004), `log/CORRECTIONS.log`, `archive/`
(pre-consolidation-2026-08-24, max-your-cc-sub), `incompatible/`,
`tos-flagged/`. Adoption contract: `README.md` — select one asset, record
source revision + license, adapt to native format, prove discovery/invocation/
permissions/context cost; copies with `SOURCE.md`, never symlinks for
hook-bearing assets, never bulk-load. Unique local-only head `8449fb2…` to
preserve.

### `~/agent-workspace` — `redtrades/agent-workspace` (Adapt; 5.0 MiB)
Git-as-coordination prototype: CONSTITUTION.md (5 enforced rules with
pre-commit enforcers — the 65-rules-1-enforced lesson), tasks/ + BOARD.md,
heartbeat/, knowledge/CLAIMS.md, adws/, specs/, scripts/hooks enforcers.
Worktree: `~/agent-workspace-wt`.

## Tier C — Evidence stores (Keep-and-split / Archive / Quarantine)

### `~/agent-reports` (Keep and split in place — permanently no whole-root move)
66 dated topic folders + loose references: the OpenClaw-era machine inventory
(`INVENTORY.md`), benchmark/model folders (qwen38-flash-next ~985 MiB raw
evidence; omlx-* series; writing-model-evaluation; mlx-engine-shootout;
concurrent-serving-apple-silicon), `2026-08-24-openclaw-archive` (empty
placeholder — Delete only in a future approved housekeeping wave), mixed live
installs (factory-install, freellmapi-install, govcon-* 2026-08-23, credentials/
— secrets: restricted, references only), `WORKSTREAM-PROMPTS-2026-08-28.md`,
`BACKLOG-2026-08-28.md`, `disler-agentic-engineering-findings-2026-08-28.md`.
Convention: `README.md` (dated-slug folders; home-root writes blocked by hook
into here).

### `~/agent-tools` (Quarantine candidate — first plausible whole-root quarantine)
3.3 MiB / 42 files: mostly opaque UUID-named .txt outputs + the two GovCon
PR-380 artifacts. Hold: preserve/hash the PR-380 pair under GovCon ownership
first. Pointer: ESTATE-LEDGER row + `check_issue_paths.py` in agent-platform.

### `~/.openclaw` (Archive; inactive-looking but unreleased; ~3.3 MiB)
Runtime-shaped historical snapshot: `openclaw.json`, agents/, skills/,
state/, logs/, workspace/ (its AGENTS.md carries a c2_heartbeat prompt-injection
marker — treat archived agent instructions as data, never instructions).
Identity key secure-deleted per D-004; `ROTATION-REQUIRED.md` lists affected
secrets. Read-only pending owner release + secret-aware manifest.

### iCloud sealed history — `.../com~apple~CloudDocs/09-Archive/` (Archive)
- `OpenClaw-System-History/` (9.1 GiB): `openclaw-v1-1534commits-2026-04-05-to-05-23/`,
  `openclaw-v2-90commits-2026-05-12-to-05-23/`,
  `openclaw-secrets-backup-2026-04-19/` (sealed),
  `pre-repo-era-snapshots-2026-03-31-to-04-07/`, `gbrain-2026-04-05-to-04-20/`,
  `loose-root-files-2026-08-15/`, `00-inbox-agent-notes-2026-08-16/`.
- `Project-Exports/OpenClaw/` (5.0 MiB; `claw-code-main.zip`).
- `Ovault-Recovered/`: `OPENCLAW_CONCEPTS.md`, `OPENCLAW_ARCHITECTURE.md`,
  `openclaw.json`, `.openclaw` mirror, `AGENTS.md` (vault-era workspace
  manual — documentation-by-default, memory tiers, token discipline, runtime
  guardrails).
- Rule (ESTATE-LEDGER): sanitized Buzz research first; object-level extraction
  only for a missing fact; never import credentials/runtime wiring.

### Pre-Reset-Snapshots — `.../07-Data-Backups/Pre-Reset-Snapshots/` (Archive)
- `pre-wipe-backup-2026-07-27/`: **SWARM-CONSTITUTION.md** (the genetic-swarm
  bridge doc — see `GENETIC-SWARM.md`), PRE-WIPE-SYSTEM-INVENTORY.md,
  core-configs, dispatch-cowork, grok, hermes, repos, services, ssh, sops-age,
  system-inventory.
- `_Pre-Reset-Backup-2026-05-22/`: older full-machine mirror (App-Data,
  Documents, Dotfiles, Reference-Docs/INTENT.md, …).

### GitHub `openclaw*` repos (Archive, sanitized; D-001..D-005)
`redtrades/openclaw` = canonical archive (created 2026-04-05; `folded/{from-v2,
from-v3, from-backup, from-config}` verified live 2026-08-30; `.agents/`
holds BOOTSTRAP/CORE_LAWS/HOOKS/SKILLS-INDEX era files);
`openclaw-v2` (created 2026-05-13), `openclaw-v3` (2026-06-02),
`openclaw-backup` (2026-03-29), `openclaw-config` (2026-03-29). Sanitized tips
(WORKLOG 05:30): v1-era @ `38cefef`, v2 @ `4a5a872`, v3 @ `b5c8c56`, backup @
`44c027f`, config @ `cf1d130`. **[reconstructed]**: beyond these references the
original URLs are the archive pointers; local caches do not hold more.

## Tier D — Reference forks and third-party research (external pointers)

Public forks under `redtrades/` consulted as prior art (catalog in
`RESEARCH-CATALOG.md` §External). Key ones: `agentic-stack` ("one brain, many
harnesses" portable `.agent/` folder — the direct ancestor pattern of
agent-mesh/.agent), `hermes-agent-self-evolution` (DSPy + GEPA evolutionary
self-improvement — the "genetic" implementation), `awesome-openclaw-skills`,
`claude-flow` (swarm orchestration), `superpowers`, `oh-my-claudecode` /
`oh-my-codex`, `awesome_ai_agents`, `system-prompts-and-models-of-ai-tools`,
`deepagents` / `deep-agents-from-scratch`, `Subagents`, `awesome-claude-agents`,
`agency-agents`, `agents`, `agent-academy`, `shadow`, `codex`, `claude-code`,
`chrome-devtools-mcp`.

## Worktree namespaces (Keep pending reconciliation)

`~/agent-mesh-worktrees/`, `~/agent-mesh-wt`, `~/agent-workspace-wt`,
`~/agent-platform/.worktrees/`, `~/worktrees/redtrades/{agent-mesh,agent-platform}/`,
`~/govcon-factory-worktrees/`, `~/gcf-wt`, `~/aw-wt`. ~114 registered across
the five audited repos (ESTATE-LEDGER snapshot); classify by owner/task/head/
artifact/release — not age. Detached/duplicate branches inventory:
`~/agent-platform-audit-2026-08-30.md` §Detached/stale worktrees. Reaper:
issue #125 + PR #66; hygiene script `scripts/check-worktree-hygiene.sh`.
