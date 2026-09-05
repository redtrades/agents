# REPORTS-SINK — `~/agent-reports/` is historic dump, not canon

**Path:** `/Users/man/agent-reports/` (not a git repository).  
**Canon pointer:** [START.md](START.md).

## What writes here

Agent sessions route inventories / STATUS / research / RCA dumps to
`~/agent-reports/<dated-slug>/` via:

1. `agent-configs` `rules/hygiene.md` (deliverables findable under dated slug, not bare `~`)
2. `agent-configs` `rules/session-continuity.md` (non-issue STATUS.md in that dated slug)
3. `~/.claude/hooks/block-home-root-writes.sh` (PreToolUse: blocks new top-level `$HOME` files/dirs; hints this sink)

## Authority

- Dumps here are **historic evidence**, not governing instructions.
- Do **not** cold-start from `~/agent-reports/`; cold-start from archive START.
- `~/agent-reports/credentials/` is an intentional secrets annex **outside git** (OK for local secrets; never commit).

## Folder index (2026-09-04, 74 folders)

Tags: **keep** = evidence, leave in place · **superseded** = captured in canon/memory, no action · **promoted** = copied into the archive.

### 2026-09
| Folder | Tag |
|---|---|
| x-bookmark-harvest-2026-09-04 | keep |
| worktree-prune-2026-09-04 | superseded (estate consolidation done) |
| harness-smoke-2026-09-04 | keep |
| estate-consolidation-2026-09-03 | keep (record of the freeze) |
| death-spiral-rca-2026-09-03 | **promoted** → `110-failures-postmortems-and-lessons/selected-originals/` |
| daily-repo-backup | keep (rolling) |
| codex-north-star-docs-2026-09-04 | keep |
| cmp-stage1-sdd, cmp-stage1-receipts, cmp-pilot-analysis-2026-09-01, cmp-mvp-analysis, cmp-minimal-organizer-2026-09-01, cmp-corpus-tools | keep (GovCon/cmp working notes) |
| cli-lanes-2026-09-04, cli-dispatch-2026-09-04 | keep |
| agent-setup-gaps-2026-09-03 | superseded (folded into this cleanup) |
| 2026-09-04-swarm-handover, 2026-09-01-coding-factory-landscape, 2026-09-01-aisdlc-foundation-handover | keep (handover history) |

### 2026-08 (all **keep** as historic evidence; research superseded by memory + subject packs)
Model/infra research: writing-model-evaluation, vmlx-config-search, sssf-provider-options, qwen38-*, ox-alpha-setup, omlx-* (6), mlx-* (3), monitoring, hermes-provider-routing-20260829, concurrent-serving-apple-silicon, acp-harness-comparison, 2026-08-26-* (5), 2026-08-24-superqwen-benchmark, 2026-08-19-benchmark-findings-preserved, 2026-08-20-* (2), 2026-08-25-hermes-webui-tailscale-fix, agent-memory, avo-supervisor, claude-academy-reference.
GovCon/factory history: sdvosb-business, software-factory, govconapi-exploration, govcon-factory-* (5), govcon-council-2026-08-23-worktree-backup, factory-optimization, factory-install, cmp-winner-location-inventory-2026-08-31, cmp-scan-2026-08-31, freellmapi-* (4), 2026-08-24-reviewer-bot.
Infra/config: worktrees, worktree backups, typed-failure-states, issue40-routing, google-subscription-antigravity, agent-configs-consolidation, 2026-08-22-settings-json-backup, 2026-08-24-openclaw-archive, video-reviews.
Annexes (not dated slugs): `credentials/` (secrets, never commit).

No deletions — `~/agent-reports/` is not a git repo; pruning is the owner's call.
