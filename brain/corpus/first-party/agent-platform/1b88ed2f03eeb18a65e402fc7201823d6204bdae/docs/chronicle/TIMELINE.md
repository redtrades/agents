# Timeline — the full chronology of the agent estate

Every era, dated, with pointers to the primary evidence. Dates are from GitHub
repo metadata (`gh api repos/redtrades/<repo>`) and `git log` unless noted.

## Era 0 — Pre-repo experiments (2026-03-31 → 2026-04-05)

Sealed snapshots of the earliest agent-home experiments (OpenClaw predecessor
state, launchd/daemon era).
- Pointer: `~/Library/Mobile Documents/com~apple~CloudDocs/09-Archive/OpenClaw-System-History/pre-repo-era-snapshots-2026-03-31-to-04-07/`
- Related: `.../09-Archive/Ovault-Recovered/OPENCLAW_CONCEPTS.md`,
  `OPENCLAW_ARCHITECTURE.md` (the vault-era conceptual layer).

## Era 1 — OpenClaw v1 "Personal Intelligence Mesh" (2026-04-05 → 2026-05-23)

Repo `redtrades/openclaw` (created 2026-04-05T04:06:47Z; 1,534 commits in the v1
window per the archive folder name). Self-described "OpenClaw Swarm v2.5.0"
in the v1 README. The original swarm: AAIF `AGENTS.md` standard, `CLAUDE.md`
constitution with 138 Decision Rules (DR0xx), JSONL append-only ledgers
(CTX/claims/active-watch), COP.json mission state, Slack `#prime` comms,
SwarmClaw control plane + Autonomy Dial (Watch/Assist/Autonomous), three-tier
swarm topology (Baseline-5 / 17 specialist manifests / ephemeral cloud),
Landlock/OpenShell sandbox simulation, Recsys spine.
- Primary pointers:
  - `~/Library/Mobile Documents/com~apple~CloudDocs/09-Archive/OpenClaw-System-History/openclaw-v1-1534commits-2026-04-05-to-05-23/` (AGENTS.md, CLAUDE.md era files)
  - `.../openclaw-secrets-backup-2026-04-19/` (sealed; never import)
  - `redtrades/openclaw` GitHub repo (sanitized 2026-08-26, tip @ `38cefef` era per WORKLOG; `-1762` files)
  - Mining digest: `~/agent-mesh/research/mine-v1-digest.md` — v1 constitution,
    personas, ledgers, research mapped; "Prime only complete persona survivor";
    JUDGE_RUBRIC ≥32/40 gated all self-improvement.
- Verbatim direction that still governs (Mike, 2026-04-24, the "genetic swarm"
  quote): see `GENETIC-SWARM.md` §1 — pointer:
  `~/Library/Mobile Documents/com~apple~CloudDocs/07-Data-Backups/Pre-Reset-Snapshots/pre-wipe-backup-2026-07-27/SWARM-CONSTITUTION.md` §2.
- Retired-intent doc: `~/.openclaw/INTENT.md` (710 lines, 2026-04-29) — cited by
  the SWARM-CONSTITUTION's source list (read in full there; local copy not
  verified this pass **[reconstructed location]**; iCloud/Drive vault copies
  exist, e.g. `.../Pre-Reset-Backup-2026-05-22/Reference-Docs/INTENT.md`).

## Era 2 — OpenClaw v2 (2026-05-13 → 2026-05-23) and v3 (created 2026-06-02)

`redtrades/openclaw-v2` ("fresh start with gbrain canonical +
commit_transaction primitive", created 2026-05-13T02:05:56Z; 90 commits in the
v2 window) and `redtrades/openclaw-v3` (created 2026-06-02T02:40:20Z, courtroom
topology). Companion archives: `redtrades/openclaw-backup` (created
2026-03-29T18:29:33Z) and `redtrades/openclaw-config` (created
2026-03-29T18:23:02Z).
- Pointers: `.../OpenClaw-System-History/openclaw-v2-90commits-2026-05-12-to-05-23/`;
  mining digests `~/agent-mesh/research/mine-v2v3-digest.md` (92 intel scans,
  reference-grade skill templates, v3 courtroom topology w/ generator≠judge
  proof + `proposal.schema.yaml`) and `mine-backup-config-digest.md`
  (declarative control plane, 7-primitive roster, tier routing, PaC budgets,
  bimodal skills, 16-job cron schema, eval golden-set format).
- Sanitized repo tips (per WORKLOG 2026-08-26 ~05:30): v2 @ `4a5a872` (−81,534
  files), v3 @ `b5c8c56`, backup @ `44c027f`, config @ `cf1d130` (−613, 15
  secret paths). Forward-commit removal, history intact — decision D-002,
  pointer: `~/agent-mesh/DECISIONS.md`.

## Era 3 — The wedge and the pre-wipe archive (2026-07-27 → 2026-08-15)

A system reset was planned; two snapshots were taken. The 2026-07-27 pre-wipe
backup holds the incident-rich `SWARM-CONSTITUTION.md` (drafted 2026-07-29 "the
night before the reset") — the bridge document between OpenClaw intent and the
rebuild; it is the canonical source for the genetic-swarm vision §Era 3 detail
in `GENETIC-SWARM.md`.
- Pointers: `.../Pre-Reset-Snapshots/pre-wipe-backup-2026-07-27/` (PRE-WIPE-SYSTEM-INVENTORY.md,
  SWARM-CONSTITUTION.md, core-configs, dispatch-cowork, hermes, repos, services);
  `.../Pre-Reset-Snapshots/_Pre-Reset-Backup-2026-05-22/` (older era mirror).
- Machine inventory of the running stack (services, LaunchAgents, tailscale,
  omlx/SSSF/FreeLLMAPI) — pointer: `~/agent-reports/INVENTORY.md` (compiled
  2026-08-20/21) plus the dated report folders in `~/agent-reports/` (66
  folders: benchmarks, cutovers, openclaw-archive placeholder, reviewer-bot,
  acp-harness-comparison, freellmapi evaluations, …). Convention of that store:
  `~/agent-reports/README.md`.

## Era 4 — Product workspaces (2026-08-15 → ongoing, `govcon-factory`)

`redtrades/govcon-factory` — the separate product factory (agent-produced
capture deliverables; PLAN-V5; fail-closed gates; SQLite trace runner). Local
first commit dated 2026-08 era; research corpora under `~/govcon-factory/research/`
and `~/govcon-factory/knowledge/research/`. Its SDLC (issue-claim CAS locks on
`claims` branch, reviewer-bot, merge tiers) became the model the platform
generalized. Disposition **Keep** per estate ledger.
- Pointers: `~/govcon-factory/AGENTS.md`, `sop/PLAN-V5.md`, `factory/README.md`,
  `~/agent-reports/govcon-prior-art.md`, `~/agent-mesh/research/govcon-overlap-map.md`.

## Era 5 — agent-workspace (2026-08-15 → 2026-08-29)

`redtrades/agent-workspace` (created 2026-08-26T03:20:45Z on GitHub; local git
history dated 2026-08-15). Git-as-coordination workspace: CONSTITUTION.md five
enforced rules with pre-commit enforcers ("five enforced beats sixty-five
aspirational"), task-file board, heartbeat log, ADW prototypes. Now demoted to
migration evidence (**Adapt**).
- Pointers: `~/agent-workspace/CONSTITUTION.md`, `README.md`, `BOARD.md`,
  `tasks/TASK-0001..0003.md`, `model-eval-qwen3.8-flash-next-glm-5.3.md`.

## Era 6 — agent-configs library (2026-08-24 → ongoing)

`redtrades/agent-configs` (created 2026-08-24T20:44:25Z). Split out of
agent-workspace + govcon-factory the same day; the source library of rules
(10), skills (11), hooks, prompts, roles, knowledge, proposals, log. Adoption
rule: select one asset + record provenance + prove behavioral activation; never
bulk-load. Disposition **Adapt** (unique local-only head `8449fb2…` must be
preserved before release, per estate ledger).
- Pointers: `~/agent-configs/README.md`, `knowledge/MIKE-INTENT-DEBRIEF-2026-08-28.md`
  (the two-projects-at-once thesis: govcon business + vendor-agnostic swarm),
  `proposals/PROPOSAL-0001..0004.md`, `log/CORRECTIONS.log`.

## Era 7 — The OpenClaw purge + agent-mesh overnight build (2026-08-26)

One night (timestamps from `~/agent-mesh/WORKLOG.md`, ~03:30→07:20):
1. Recon of the five `openclaw*` repos; ~190 extracted artifacts mined
   (staging `extracted/v1|v2|v3|backup|config`).
2. 12 parallel research agents produced the cited research corpus
   (`research/INDEX.md`) — see `RESEARCH-CATALOG.md` §Overnight wave.
3. Repo scaffolded (GitHub created 2026-08-26T08:37:11Z), D-001..D-015 recorded
   (`DECISIONS.md`): canonical archive = `redtrades/openclaw` with `folded/`
   (verified live: `folded/from-backup|config|v2|v3` on GitHub), sanitization
   whitelist, credential stripping + `ROTATION-REQUIRED.md`, secure-delete of
   `~/.openclaw/identity/device.json` (D-004; the ~3.3 MiB `~/.openclaw` residue
   remains read-only), new name `agent-mesh` (D-005).
4. Builders landed: `.agent/` portable brain (5 personas prime/scout/forge/
   sentinel/operator + protocols + memory architecture), `hermes/` bot package,
   `pipelines/`, `evals/`, `command-center/` (SwarmClaw-inspired static v1),
   `vault/`.
5. Sanitizer wave on all five openclaw repos (tips above, fast-forward,
   no-force); archive fold pushed @ `14212de` (208 files).
6. Hermes wiring: 4 bot profiles + 4 paused `[bot:*]` cron routines;
   SwarmClaw PWA v1 built+proofed; MemPalace 3.3.3 installed.
7. Adversarial overnight review filed (`reviews/2026-08-26-overnight-review.md`,
   verdict FIX-FIRST; P0 refuted on re-verification — a live example of
   generator≠judge working).
- Canonical pointers: `~/agent-mesh/README.md`, `HANDOFF.md`, `WORKLOG.md`,
  `DECISIONS.md` (D-001..D-035), `research/INDEX.md`, `.agent/AGENTS.md`.

## Era 8 — Model-program days (2026-08-26 → 2026-08-28)

Decisions D-016..D-035 (`~/agent-mesh/DECISIONS.md`) ran the local-model
program on the M1 Max: OMLX 0.6.2 + `Jundot/Qwen3.8-27B-oQ4e-mtp` three-tier
Hermes profiles → the comprehensive 8-cell matrix (D-026) → the supersessions
D-027 (scheduler fields are internal, not tunable), D-032 (**identity
correction**: the 27B oQ4e route ≠ exact `Qwen/Qwen3.8-Flash-Next`; the exact
model is `qwen4_exp` 125B/6B-active + 51B n-gram + 4B MTP, AtomicChat
`AD-3.84bpw-IQ4_XS-M64`), D-034/D-035 (exact Flash-Next IQ4 selected for the
isolated lane at 131,072 context, Q4.27 rejected at 128K, 262,144
resource-rejected). Benchmark evidence lives outside git at
`~/agent-reports/qwen38-flash-next/` (~985 MiB, per estate ledger); receipts
quoted in HANDOFF/WORKLOG tail (SHAs `0e3e13c6…`, `00dd96a4…`, `8dd983f9…`).
- Pointers: `~/agent-mesh/HANDOFF.md` ("Current truth" — the authoritative
  summary of what is proven), `research/` Apple-Silicon files (cataloged in
  `RESEARCH-CATALOG.md` §Hardware wave), `hermes/` notes.

## Era 9 — agent-platform canonical authority (2026-08-28 → ongoing)

`redtrades/agent-platform` (GitHub created 2026-08-28T20:30:56Z). Local git
began 2026-08-28 ("establish agent-platform authority baseline"); 159 commits
as of 2026-08-30. `docs/START-HERE.md` declares it sole work board; all legacy
repos demoted to migration evidence (Era 7+8 material now feeds it).

Key verified moments (from `docs/START-HERE.md` §Current implementation state +
`docs/CONTROLLER.md` §Verified live proof + `proofs/gate-c-live-*.txt`):
- Historical: #69/PR #68 first AUTO_WRITE (`37444ecd` → merge `e8f58d56`);
  #81/PR #82 (CI run 33265987993, pre-App).
- **Gate C complete proof**: issue #103 → PR #110 → merge commit
  `19246a50369c54f2478a02b3f2453ae2372bf5fd` (merged 2026-08-29T23:44:48Z,
  verified live via API this pass) with distinct Controller / Reviewer /
  Promoter Apps + separate Projector PAT; receipt artifact
  `gate-c-receipt-33281620826-1` (artifact ID `9723173013`); candidate
  `9ec4b521…`; exact-subject CI run 33281657677; reviewer verdict `5059477980`.
- Day of 2026-08-30: queue transition sweeps (root `QUEUE-*.md`,
  `CLAIM-QUEUE-TRIAGE*.md`, `triage-result-2026-08-30.json`,
  `worktree-reaper-report-2026-08-30.json`), P1/P2 worktree audit
  (`~/agent-platform-audit-2026-08-30.md`), the earlier consolidation pass
  (`docs/CANONICAL-REFERENCE.md`, `docs/CANONICAL-INDEX.md`, `docs/synthesis/`),
  and this chronicle.
- Open frontier (issue states as observed 2026-08-30, refresh before acting):
  #117 terminal projection (claimed), #9 autonomous loop (open; spec
  `docs/AUTONOMOUS-LOOP.md`), #27/#43 clean-host, #185 Temporal/LangGraph
  durable-execution research, #125/#126 swarm-coordination blockers, adapters
  #130–#134 blocked behind #40.

## Era 10 — Where the loose ends are (observed 2026-08-30)

- ~114 registered worktrees across the audited repos; many dirty — estate
  ledger sequence (refresh→preserve→extract→release→quarantine→delete) governs;
  pointers: `~/agent-platform/migration/ESTATE-LEDGER.md`,
  `estate-ledger.json`, `migration/PRESERVATION-2026-08-29.md` (the
  cross-repo "preserve uncommitted work as of 2026-08-29" commits on
  agent-mesh/agent-configs/agent-workspace/govcon-factory heads).
- Sealed history remains at iCloud `09-Archive` (OpenClaw-System-History 9.1 GiB
  verified this pass) + `09-Archive/Project-Exports/OpenClaw` (5.0 MiB) +
  Google Drive OpenClawVault mirrors (not exhaustively inventoried).
- Endangered local-only commits listed in ESTATE-LEDGER §"Terminal Git objects"
  (7 govcon + 4 agent-mesh heads + agent-configs `8449fb2…`) — preserve before
  any git maintenance.
