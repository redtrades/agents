# Mine Digest — openclaw-backup (control plane) + openclaw-config (runtime state)

Mined 2026-08-26. Read-only. All values below are structural/representative; no secret values reproduced.
Sources: `agentmesh/repos/openclaw-backup` (config/, skills/ 129 files, memory/ 150, evals/ 218, docs/ 132) and `agentmesh/repos/openclaw-config` (cron/, config-root JSONs, ~78 skill dirs, 8 agent state dirs).

---

## 1. backup/config/ — control-plane schema

### agents.yaml (`version: 2026-04-02-schema-1`)
Declarative roster ("agents-as-code") that generates `openclaw.json#agents`. Schema:
- `metadata` (owner: Prime, generated_runtime_target)
- `defaults`: workspace_root `~/openclaw/workspaces`, agent_dir_root `~/.openclaw/agents`, sandbox_mode off, required_agents list
- per-agent: `name, role, title, plane, always_active, slack_account, identity_managed, tier, workspace, agent_dir, sandbox_mode, tools.exec{security,safe_bins}, identity_summary, directives[]`

7-agent roster ("Sovereign Swarm" primitives), representative values:
| agent | role | title | plane | tier | activity |
|---|---|---|---|---|---|
| prime | Control / orchestrator | The Orchestrator | Control | frontier | always |
| scout | Research | The Perceiver | Cognitive | performance | always |
| strategist | Planning | The Planner | Cognitive | performance | on-demand |
| forge | Action (coding) | The Builder | Action | performance | always |
| operator | Action (ops) | The Executor | Action | performance | on-demand |
| sentinel | Safety & monitoring | The Critic | Cognitive | performance | always |
| archivist | Knowledge & memory | The Memory Keeper | Cognitive | performance | always |

Prime gets exec allowlist safe_bins (git/python3/openclaw/gh/bash); each agent owns a Slack lane (#prime, #intel, #ops, #work, #daily-brief).

### model-tiers.yaml (2026-04-03)
Tier abstraction with fallback chains; cost-first local routing:
- **frontier** (Prime only): primary `ollama/gemma4:latest` → `xai/grok-4-1-fast` → `anthropic/claude-opus-4-6` → `openai/gpt-5.4` → `google/gemini-3-flash` → vMLX Nemotron-120B (prime_only flag) → `ollama/qwen3.5`
- **performance** (all others): gemma4 → grok-4-1-fast → sonnet-4-6 → gpt-5.4 → gemini-3-flash → vMLX 30B MoE → qwen3.5
- **local**: vMLX Nemotron-Cascade-2-30B-A3B → ollama/qwen3.5
- **embeddings**: ollama/nomic-embed-text (127.0.0.1:11434) ← vMLX Qwen3-Embedding-0.6B (:8080)
Notable comment: reasoning-model fallback was demoted because it "leaked 'final answer below' artifacts to Slack via reasoning token passthrough."

### models.yaml (2026-04-03-schema-1)
Model family catalog: anthropic (opus/sonnet 4-6), xai (grok-4-1-fast[-reasoning]), vmlx local JANG quantized Nemotron 30B/120B + embedding, ollama (gemma4 variants, qwen3-coder "32 tok/s on M1 Max", glm-4.7-flash, gemma3n, nomic-embed), google (gemini 2.0-flash / 1.5-pro). Fields: id, context_window, max_tokens, is_embedding, notes.

### policies/
- **budgets.yaml** (PaC): global daily_max_usd $50, hourly_max_tokens 1M; per-agent daily USD budgets (prime $20, scout/forge $10, strategist $5, operator/sentinel $2, archivist $1).
- **execution.yaml** (PaC): allowed_binaries allowlist (~28 entries incl. git, python3, sqlite3, gh, rg, claude CLI); host_access.network allow_domains (github.com, api.anthropic.com, api.openai.com, api.x.ai, slack.com); disk allow_paths (`~/openclaw/`, `~/.openclaw/`); retries w/ exponential backoff; safety flags: approval_required_for_destructive, human_in_loop_for_infra, max_autonomous_runtime_hours 4.
- **documentation-audit-policy.json**: doc staleness scanner policy — filename/content keyword detection ("legacy", "deprecated", …), frontmatter date key `updated`, stale cutoff 2025-12-31, archive rules with pointer stubs, report paths.

### workflows.yaml + workflows/*.yaml
Two layers:
- **workflows.yaml**: scheduled pipelines bound to agents — gdrive-mirror (operator */6h), health-audit (sentinel nightly), gpu-sentinel (prime */5min, --kill), self-heal (sentinel */2h driftctl+repair+restart-on-fail), optimization-audit (weekly), memory-sync (archivist */4h mem0→vault).
- **workflows/*.yaml**: step-list workflow packets — schema `{name, version, description, category, tags, inspired_by[], steps:[{tool, command, description}]}`. Six defined: compaction-recovery, github-issue-intake, memory-index (FTS rebuild), ops-snapshot, rc-acceptance (RC2026.4.2 sweep), runtime-promotion (repo→~/.openclaw promote with backup+verify).

### task-routing.yaml
GitHub issue → task-packet intake rules: eligible project statuses (Todo/In Progress), ignore labels/prefixes, packet_roots backlog/active, per-owner allowed_write_paths (least-privilege write scopes per agent), artifact_type_by_owner (scout=research_note … forge=pull_request), and label/title-keyword routing_rules mapping issues → owner+kind (trust-policy/security→sentinel, architecture→strategist, knowledge→archivist, ops→operator, research→scout, implementation→forge).

### triggers.yaml (PaC)
Wake signals: schedule crons (issue sync */15min→scout, upstream release monitor daily→scout, board worker loop */20min→forge, nightly security scan 2AM→sentinel, weekly release/self-audit Monday→prime, Friday health summary→prime) + event trigger (`gpu-ram-sentinel` pressure ≥92 → sentinel re-tier models).

### Schemas & misc
- task-packet.schema.json, shared-state.schema.json — JSON Schemas for tracked work packets and cross-agent shared state.
- openclaw.json (788 lines): full runtime config — env, diagnostics, models.providers, agents{defaults(compaction/memoryFlush thresholds), list}, tools, cron.enabled, channels.slack, gateway{port,mode,bind,auth}, plugins, bindings. **Contains no provider API keys in the backup copy** (unlike the runtime repo copy).
- extensions.json → lossless-claw plugin (TypeScript ContextEngine extension: FTS5 conversation store, DAG compaction "dag-oolong", LCM expand/grep/describe tools, token budgets).
- config/skills/ = 6 intelligence-pipeline skills (see §2).

## 2. backup/skills/ — inventory (6 vendored dirs, 129 files) + 6 config/skills

Vendored ClawHub-style packs (each: SKILL.md frontmatter name/description/version + `_meta.json` + `.clawhub/origin.json`):

| skill | purpose | form | verdict |
|---|---|---|---|
| capability-evolver | Self-evolution engine: analyzes runtime history, applies protocol-constrained evolution; GEP subsystem (candidates, mutation, canary, hub review, A2A protocol), 20+ test files | Full JS package + 290-line SKILL.md | unique/well-formed (heaviest artifact in repo) |
| gog | Google Workspace CLI (Gmail/Calendar/Drive/Contacts/Sheets/Docs) | 36-line thin wrapper SKILL.md | boilerplate-thin but functional |
| memu | Persistent 3-layer memory infra (Resource→Item→Category) on memU framework, claims 70–90% token reduction | 122-line SKILL.md + METADATA.yaml + 4 py examples | well-formed third-party (examples contain only placeholder keys) |
| n8n | Manage n8n workflows via API (list/toggle/status/trigger/debug) | 537-line SKILL.md + references/api.md + 3 py scripts | well-formed, deepest docs of the vendored set |
| obsidian | Obsidian vault ops via obsidian-cli | 55-line SKILL.md | thin |
| openviking | RAG/semantic search via OpenViking MCP server | 111-line SKILL.md + init.sh + skill.yaml | moderate |

backup/config/skills/ — Mike-authored "intelligence pipeline" family (all well-formed, versioned, trigger-declared):
| skill | purpose |
|---|---|
| meeting-intelligence (v3.0, 570 ln) | End-to-end meeting pipeline: Drive/Otter trigger → classify → extract → template → GitHub issues → PIP tracker → git → Slack → Notion, zero human intervention |
| stakeholder-intelligence-skill (183 ln) | Governance/exec meetings → positions, concerns, influence signals, political dynamics; updates person entities; ACPX escalation at PIP score ≥7 |
| trading-intelligence (184 ln) | TSLA/xAI/SpaceX market research + thesis monitoring; research/alerting only (brokerage deferred to Phase 5) |
| url-intelligence (120 ln) | Any URL → markdown → topic inference → domain routing → proactive research → filed with wikilinks/frontmatter |
| x-search-intelligence (115 ln) | xAI x_search queries for real-time market/news/signal extraction from X |
| people-intelligence (95 ln) | Relationship history, commitments, preferences, current status per person entity |

Boilerplate signature seen elsewhere in this era (openclaw-config): ~24–36-line SKILL.md, frontmatter (name/description) + fixed sections Purpose/When to Use/Workflow(4 steps)/Output Format — e.g. finance-monitor, spellcheck, okr-planner. Well-formed ones run 100–600 lines with phases, agent assignments, failure handling, and Slack output templates.

## 3. backup/memory/ — convention

Layout (policy doc: MEMORY_SYSTEM.md, "Markdown is the canonical source of truth"):
- `YYYY-MM-DD.md` root dailies + `daily/YYYY-MM-DD.md`; `MEMORY.md` curated standing knowledge
- `entities/*.md` (systems/tools/people; `entities/people/*.md` 16 person files), `projects/*.md`, `reflections/*.md` (OODA retros), `summaries/*.md` (+ `summaries/meetings/*` 24 transcripts manifest), `insights/`, `archive/pre-v4/`, `inbox/x-drafts/`, `subagent/`, `dispatch-completions.jsonl`

Frontmatter patterns observed:
- Daily notes: `date, type: daily-note, tags[]` (one file written with literal `\n` escapes — an escaping bug worth noting)
- Entities: `title, type: entity, tags[], updated`
- Reflections: `tags[], created` ISO timestamp

Tiering model (0 session → 1 daily → 2 durable curated → 3 reflections/summaries → 4 archive), storage decision matrix ("will it matter after this session?" × "changes future behavior?"), derived indexes (semantic/temporal/entity/causal), dual-track retrieval ranking (recency vs relevance merge weights), query-adaptive graph selection, context-window degradation thresholds (70% caution → 95% new session), semantic cache (0.92 similarity, TTL 30m), memory health metrics (capture precision >80%, recall >90%, orphan rate <15%).

## 4. backup/evals/ — format

- **Golden set**: `eval-prompts.yaml` — flat list of eval items: `{id (code_001…tool_003), category (coding_quality/tool_use/…), agent_role (forge/prime/scout), difficulty, name, prompt, expected}` where `expected.type ∈ {code_execution (embedded test_code asserts), json_structure, …}`.
- **Runner**: `run-evals.sh` + `run_evals_inner.py` against Ollama (`OLLAMA_URL`); `run-cloud-evals.py` for hosted models; `resilient-runner.py`, `model-benchmark.py`, live-dashboard.
- **Results**: per-model dir per item `<category>_<nnn>.json` storing prompt/response/expected; `scores_<model>.json` = composite scoring: `final_score/10` from raw components (tests_pass, has_type_hints, has_docstrings, clean_code, structural_score, performance) + latency_s, tokens_generated, tokens_per_sec; `scoring_method: composite`.
- **Cloud judge**: `score-evals-cloud-judge.py` re-scores zeroed local-judge results using grok-4-1-fast-reasoning as LLM judge (key loaded from `XAI_API_KEY` env or `~/.openclaw/gateway.env` — path flagged below, value not present here).
- Model coverage dirs: gemma4, gemma3n, glm-4.7-flash, qwen3.5, qwen3-coder, xai-grok-4-1-fast-reasoning + benchmark md reports (vmlx-vs-ollama, warm-benchmark, prime-baseline, overnight-run).

## 5. Persona docs (SOUL.md / IDENTITY.md / USER.md)

Approach: layered self-model for the Prime agent, all frontmatter-stamped (`agent: prime, updated`):
- **SOUL.md (26 KB)**: opens with an AUTONOMOUS EXECUTION DIRECTIVE — execute-first/report-after whitelist vs a short ask-Mike list (external email, purchases, destructive deletes, credential changes, twice-failed escalations). Then communication style as "elite engineering lead": exact response templates per channel (#ops status, #intake classification cards, #work forwardable outputs, error format).
- **IDENTITY.md**: table-form self-model — name "Redclaw" 🦞, role Control Plane, OODA loop, C4 complexity classes (simple→open-ended) + A2 autonomy bands (in-loop/on-loop/out-of-loop), two communication MODEs (professional vs group-chat persona), channel-routing matrix per agent, `[sender→receiver]` message tagging convention, thread-based workflow discipline.
- **USER.md**: minimal human profile (name/timezone/preferences pointers) with an explicit "learning about a person, not building a dossier" boundary note.

docs/SOUL.md etc. mirror these for the whole swarm; docs/architecture/specs/ holds the deeper contracts (AUTONOMY_CONTRACT, ROUTER_DECISION_SPEC, EVAL_TAXONOMY_SPEC, dated 2026-03-28).

## 6. openclaw-config (runtime state dump)

### cron/jobs.json schema
`{version, jobs[]}`; job fields: `id (uuid or readable slug), agentId, sessionKey (redacted in extract), name, enabled, createdAtMs/updatedAtMs, schedule{kind: every|cron, everyMs|cronExpr, anchorMs}, sessionTarget: isolated, wakeMode: now, payload{kind: agentTurn, message}, delivery{mode: announce, channel: slack, to: channel:<name>}, state{lastRunAtMs, lastRunStatus, consecutiveErrors, nextRunAtMs, …}, timezone, notify, commands, skill, note`.
16 jobs incl.: Prime Watch (hourly heartbeat poll w/ decision-tree prompt ending `HEARTBEAT_OK`), SITREP morning briefing, Janitor + Post-Mortem (archivist), Vector & Knowledge Sync 4h (archivist), Health Check Sweep 30m + Proactive Sweep 2h waking-hours (sentinel), GitHub Board Sweep Sunday, Weekly Retro/Digest, Intelligence Sweeps noon/evening, market-scan + sentiment-pulse×2 (orphaned: no agentId). Run logs in `cron/runs/<jobId>.jsonl`.

### skills/ taxonomy (78 dirs = 74 active + 4 in _archived/)
Naming: kebab-case verb-noun/intent compounds grouped informally by prefix families — `admin-*` (5 system ops), `auto-*` (autonomous loops), `business-*` + finance/trading/market (money domain), `daily-*`/`weekly-*` (brief cadence), `github-*`, `obsidian-*`/vault/notion/backup (storage), `meeting-*`/people/stakeholder (work intel), plus infra guards (permissions-guard, hook-manager, rollback-manager, skill-vetter, meta-skill). Uniform single-file convention: one SKILL.md each; quality bimodal — ~30 generic-template skills (24–36 lines) vs ~25 substantial ones (>100 lines, phased protocols with agent assignments).

### agents/ state dirs
9 dirs: 7 primitives + main + README. Each contains `agent/models.json` — a per-agent *runtime-resolved* provider catalog (providers→models with pricing/contextWindow/maxTokens), i.e., what the agent's gateway slice actually serves; differs per agent (e.g., prime includes Codex backend-api provider). Per README, instruction files are symlinked from vault (`~/openclaw-vault/agents/`) — canonical content lived outside this repo. Stray atomic-write leftover `sentinel/agent/models.json.<pid>.<ts>.tmp` = evidence of an interrupted config write. Four of eight models.json contain embedded provider API keys (flagged §7).

### Root-level runtime artifacts
openclaw.json + .proposed (live config w/ secrets — skipped, see §7), integrations.json (Twitter OAuth set + xAI tools key), exec-approvals.json (socket token), node.json/update-check.json (benign telemetry), dispatch-permissions-template.json (tool allowlist template incl. MCP tool names), dispatch-session-audit, SYSTEM_HEALTH_REPORT, life-os-reference.jsx, cleanup script + config-upgrade-diff.txt (**contains pasted real keys — flagged**).

---

## 7. Credential-path flags (names only — values never printed)

### openclaw-config (LIVE secret material present)
- `openclaw.json` — `channels.slack.{botToken, appToken, userTokenReadOnly, webhookPath}`; `models.providers.{xai,google,anthropic,_disabled_mlxstudio}.apiKey`; `plugins.entries.{google,brave,exa,xai}.config.webSearch.apiKey`; `ollama.apiKey` (non-empty placeholder-class)
- `openclaw.json.proposed` — same Slack/provider/plugin keys **plus** `channels.bluebubbles.password`, `gateway.auth.token`
- `integrations.json` — `integrations.twitter.credentials.{bearerToken, consumerKey, consumerSecret, accessToken, accessTokenSecret}`, `integrations.xai_agent_tools.apiKey`
- `exec-approvals.json` — `socket.token`
- `agents/{strategist,scout,operator}/agent/models.json` — embedded `sk-…` + `xai-…` keys; `agents/forge/agent/models.json` — `xai-…` key (prime/main/archivist/sentinel copies clean)
- `config-upgrade-diff.txt` — pasted google api key, sk- key, slack bot token, xai key (diff artifact)
- `cron/runs/*.jsonl` — several runs matched webhook/token-shaped strings (treat entire runs dir as sensitive)

### openclaw-backup
- No live key values found in config copies; sensitive-by-design references only: `evals/score-evals-cloud-judge.py` + `evals/run-cloud-evals.py` read `~/.openclaw/gateway.env` / env vars (paths referenced, not stored)
- Placeholder-only matches (safe): `skills/memu/**` (`sk-your-…` placeholders)
- False positives verified: `config/skills/url-intelligence/SKILL.md`, `memory/summaries/meetings/transcript-manifest.json` (keyword mentions only)
- Docs referencing secret-handling incidents: `docs/audits/2026-04-02-launchagent-secret-hardening.md` (launchd plist token embed), board audit P0 "gateway secrets"

### Extraction hygiene applied
Skipped entirely (secret-bearing): openclaw-config `openclaw.json`, `openclaw.json.proposed`, `integrations.json`, `exec-approvals.json`, all four key-bearing agents/*/models.json, config-upgrade-diff.txt, cron/runs/. Copied `cron/jobs.json` only after redacting `sessionKey` (+ any token/webhook-shaped keys) → `extracted/config/cron/jobs.redacted.json`. All copied files re-scanned clean against tight key-format regexes.

## Extraction counts
- `staging/extracted/backup/`: 43 files — config 17 (incl. 3 policies, 6 workflows), skills 14, memory 6, evals 6
- `staging/extracted/config/`: 39 files — 35 skills (32 active + 3 archived), cron 2 (redacted jobs.json + README), root 2 (README + permissions template), agents 1 (clean prime models.json example)
