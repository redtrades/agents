# Legacy source and archive catalog

This is the human-readable routing layer over the detailed manifests. It does
not make any legacy directory authoritative.

| Area | Observed role | Destination class | Next action |
|---|---|---|---|
| `/Users/man/agent-configs` | copied rules, skills, prompts, roles, and intent research | quarantine/source library | extract individually proven modules into `agent-mesh`; archive the remainder after provenance review |
| `/Users/man/agent-workspace` | experiments, SSSF adaptations, harness research, prototypes | research/prototype archive | extract proven mechanisms and fixtures; do not retain as a second platform |
| `/Users/man/agent-reports` | 2.4 GB mixed reports, raw runs, vendored installs, backups, product material, and credentials | split evidence store | separate immutable benchmark evidence, product artifacts, rebuildable caches/vendor copies, operational backups, and sensitive quarantine |
| `/Users/man/agent-tools` | mostly opaque UUID text artifacts plus a small number of recovery scripts | quarantine | resolve producer/provenance; keep only tools with an owner and interface |
| `/Users/man/.agents` | shared installed skill bodies and links | runtime projection/source candidates | use the component manifest; no wholesale promotion |
| `/Users/man/.claude`, `.codex`, `.hermes`, `.grok`, `.gemini`, `.buzz` | runtime-local instructions, plugins, sessions, caches, profiles, and generated state | runtime-local adapter targets | retain only native state; generate shared projections from the platform after adapter proof |
| `/Users/man/.openclaw` | live/historical OpenClaw runtime state | restricted historical runtime snapshot | never import wholesale; recover only reviewed contracts and evidence |
| `/Users/man/agent-reports/2026-08-24-openclaw-archive` | prior OpenClaw archive | reference archive | index Keep/Adapt/Defer/Reject results; no runtime reactivation by copying |
| `/Users/man/.buzz/RESEARCH/OPENCLAW_*` | OpenClaw cross-runtime research | research evidence | retain as cited evidence, then consolidate selected conclusions into the platform docs |
| `/Users/man/govcon-factory` | product factory | separate consumer repo | keep domain templates, gates, and product evidence outside the platform |
| `*-worktrees`, `*-wt`, `/Users/man/worktrees` | active, stale, prunable, and endangered Git worktrees | temporary execution state | preserve unique commits/artifacts, then retire in waves using the workspace manifest |

## `agent-reports` split

Do not move this directory wholesale into Git. Route each top-level item into one
of these classes:

1. immutable benchmark/run evidence;
2. concise reviewed findings and receipts;
3. product-factory research/deliverables;
4. runtime configuration backups;
5. vendored source/install trees;
6. rebuildable caches and generated logs;
7. historical archives such as OpenClaw;
8. sensitive quarantine.

Credential-like paths already identified by filename are listed only in the
detailed component manifest. Their contents were not opened or hashed. They stay
out of ordinary Git and require credential-owner review before retirement.

## Fast cleanup sequence

1. Keep this catalog and the detailed manifests as the shared map.
2. Preserve unique Git heads and irreplaceable ignored artifacts.
3. Move concise approved findings into `agent-mesh/docs` or the owning factory.
4. Move large immutable runs into a dated artifact hierarchy with manifests.
5. Quarantine sensitive and unknown-provenance material separately.
6. Mark vendored copies and caches as rebuildable; delete only in the later
   contraction wave.
7. Remove prunable worktree registrations and empty namespaces after active
   owners/processes are clear.
8. Archive or retire `agent-configs` and `agent-workspace` only after every kept
   component has a destination and rollback proof.

