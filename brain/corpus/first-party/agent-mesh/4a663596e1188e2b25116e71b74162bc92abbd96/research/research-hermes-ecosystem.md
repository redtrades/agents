# Research: NousResearch/hermes-agent Ecosystem

**Date:** 2026-08-26 · **Scope:** official docs + community ecosystem, verified against live sources
**Mike's deployment context:** macOS desktop app, `~/.hermes`, omlx backend (qwen3.8) on :8300, FreeLLMAPI gateway on :3100

---

## 1. Official config surface (verified current)

### Version status — correction to brief

The brief assumed "~0.17.x"; **current stable is v0.20.5 (tag `v2026.8.19`)**, published 2026-08-21 ([releases](https://github.com/NousResearch/hermes-agent/releases), [Hermes Atlas](https://hermesatlas.com)). Release line since June:

| Tag | Date | Name | Scale |
|---|---|---|---|
| v0.17.0 (`v2026.6.19`) | Jun 19 | "The Reach Release" | ~1,475 commits, 245 contributors |
| v0.18.0 (`v2026.7.1`) | Jul 1 | "The Judgment Release" | ~998 PRs, 949 issues closed |
| v0.19.0 (`v2026.7.20`) | Jul 20 | "Quicksilver" | ~1,065 PRs, 450+ contributors |
| v0.20.0 (`v2026.8.3`) | Aug 3 | "The Herald Release" | ~1,400 PRs, ~1,200 issues closed |
| v0.20.5 (`v2026.8.19`) | Aug 19/21 | patch rollup (~323 PRs since 0.20.4) | current |

Source: GitHub releases API, https://github.com/NousResearch/hermes-agent/releases

### Directory & config.yaml essentials

Everything lives under `HERMES_HOME` (`~/.hermes`, or `~/.hermes/profiles/<name>/`): `config.yaml`, `.env`, `auth.json`, `SOUL.md`, `memories/` (MEMORY.md + USER.md), `skills/`, `cron/`, `sessions/`, `logs/` ([Configuration](https://hermes-agent.nousresearch.com/docs/user-guide/configuration)).

Key schema blocks verified in [Configuration](https://hermes-agent.nousresearch.com/docs/user-guide/configuration):

- **model/provider**: `hermes model` picker writes `model.default` + provider; precedence CLI arg > config.yaml > `.env` > defaults. Custom OpenAI-compatible endpoints supported everywhere via the universal triple `provider` / `model` / `base_url` (+ `api_key`) — this is how omlx:8300/FreeLLMAPI:3100 slot in.
- **providers.<id>**: per-provider `request_timeout_seconds`, `stale_timeout_seconds`, and per-model overrides; env substitution `${VAR}` / `${env:VAR}` works throughout ([Configuration](https://hermes-agent.nousresearch.com/docs/user-guide/configuration)).
- **delegation**: `delegation.model/provider/base_url/api_key/api_mode` route subagents to a different endpoint than the parent; `max_concurrent_children` (default 3), `max_spawn_depth` (1–3), `worktree_isolation`, `orchestrator_enabled`.
- **moa**: named Mixture-of-Agents presets appear as selectable models under the virtual `moa` provider — see below.
- **mcp_servers**: block accepts Cursor-style `${env:}` SecretRef snippets unchanged; MCP tool results spill to disk at 50K chars by default (`tool_budget.mcp_result_size_chars`). Full key reference: [MCP Config Reference](https://hermes-agent.nousresearch.com/docs/reference/mcp-config-reference).
- **platform_toolsets**: per-platform toolset toggles written by `hermes tools`; global kill-switch is `agent.disabled_toolsets` (applies *after* platform config).
- **skills**: `skills.external_dirs`, `skills.write_approval`, `skills.guard_agent_created`, `skills.config.*`, `trusted_project_dirs`, `project_discovery`.
- **agent.reasoning_effort**: `none|minimal|low|medium|high|xhigh|max|ultra` (default medium), plus spelling-tolerant per-model `agent.reasoning_overrides`. Runtime `/reasoning high --global`. Per-cron-job reasoning pins too ([Configuration](https://hermes-agent.nousresearch.com/docs/user-guide/configuration)).
- **prompt_caching.cache_ttl**: `"5m"` or `"1h"` Anthropic-tier breakpoints; caching itself is always-on when provider supports it — no disable knob ([Prompt caching](https://hermes-agent.nousresearch.com/docs/user-guide/configuration#prompt-caching)).
- **memory**: `memory_enabled`, `user_profile_enabled`, `memory_char_limit` (2200), `user_char_limit` (1375), `write_approval`.

### Profile anatomy (= a Bot)

A profile is a full Hermes home: its own `config.yaml`, `.env`, `SOUL.md`, `memories/`, `sessions/`, `skills/`, `cron/`, `state.db`, plus `profile.yaml` (carries optional `display_name`) ([Profiles](https://hermes-agent.nousresearch.com/docs/user-guide/profiles)). Create with `hermes profile create <name>` (`--clone`, `--clone-all`, `--clone-from <p>`, `--no-skills`, `--description "<role>"`); each profile auto-aliases to a command (`coder chat …`). One agent process per home — never two writers on one profile.

### SOUL.md authoring guidance

Official guide: [Use SOUL.md with Hermes](https://hermes-agent.nousresearch.com/docs/guides/use-soul-with-hermes). Slot #1 of the system prompt, fully replaces default identity; scanned for prompt-injection patterns; capped by `context_file_max_chars` (dynamic, floor 20K chars). Rules of thumb:
- SOUL.md = identity/tone/avoid-list only; project facts go to AGENTS.md (first-match order: `.hermes.md` → AGENTS.md → CLAUDE.md → .cursorrules) ([Context Files](https://hermes-agent.nousresearch.com/docs/user-guide/features/context-files)).
- Suggested structure: `# Identity / # Style / # Avoid / # Defaults`. Strong = stable, voice-specific, 4–8 lines to start; weak = project details, contradictions, generic filler.

### Skills system

Skills are SKILL.md documents compatible with the **agentskills.io open standard**, living in `~/.hermes/skills/` with progressive disclosure (list ≈3k tokens → `skill_view` on demand) ([Skills System](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills)). Frontmatter supports `platforms:`, conditional activation (`requires_toolsets` / `fallback_for_toolsets`), declared env vars, and per-skill config settings. Registries integrated: official optional catalog, **agentskills.io Skills Hub**, Vercel's skills.sh, well-known endpoints, direct GitHub taps (openai/skills, anthropics/skills, huggingface/skills, NVIDIA/skills…), ClawHub, LobeHub, browse.sh, raw URLs — all security-scanned, trust-tiered, with `--force` unable to override a `dangerous` verdict. Skill bundles group multiple skills under one slash command (`~/.hermes/skill-bundles/*.yaml`).

### Memory system

Bounded curated files: MEMORY.md (2,200 chars ≈800 tok) + USER.md (1,375 ≈500 tok), injected as a frozen snapshot at session start (preserves prefix cache); agent self-manages via the `memory` tool (add/replace/remove, consolidation on overflow) ([Memory](https://hermes-agent.nousresearch.com/docs/user-guide/features/memory)). Beyond that: SQLite FTS5 `session_search` over all past sessions (free, no LLM). **Mem0 is a first-class external provider** — one of 8 memory-provider plugins (Honcho, OpenViking, Mem0, Hindsight, Holographic, RetainDB, ByteRover, Supermemory), exposed as `mem0_profile` / `mem0_search` / `mem0_conclude` tools, managed cloud or self-hosted Apache-2.0 ([Memory Providers](https://hermes-agent.nousresearch.com/docs/user-guide/features/memory-providers), [Atlas entry](https://hermesatlas.com/projects/mem0ai/mem0)); setup: `hermes memory setup`.

### Cron / routines syntax

Single `cronjob` tool + `hermes cron` CLI; schedules are natural language (`every 2h`, `every sunday 9am`), relative one-shots (`30m`), cron expressions, or ISO timestamps ([Cron](https://hermes-agent.nousresearch.com/docs/user-guide/features/cron)). Notable mechanics: per-job model+reasoning pin (drift guard fails closed if global default changes); skill attachment (multi-skill); `deliver:` targets including **`bot-chat` / `bot-chat:<profile>`** (output lands in a bot's canonical chat and costs it a real agent turn); `context_from` job-chaining; `continuity=true` dedupe against own last output; `no_agent --script` script-only watchdogs; `wakeAgent:false` pre-run gates ($0 ticks); `[SILENT]` suppression; execution ledger + failure-streak nudges + ackable incidents.

### Mixture of Agents

Virtual provider; preset = reference models (advisors, no tools) + aggregator (acting model) ([MoA](https://hermes-agent.nousresearch.com/docs/user-guide/features/mixture-of-agents)). HermesBench: opus-4.8 aggregator over gpt-5.5 reference scores 0.8202 vs 0.7607 solo. Cache-safe by construction (advisor output appended at tail only). Cadence knobs: `fanout: user_turn` (default since Jul 2026) / `per_iteration` / `every_n:N`; `reference_max_tokens` caps advisor verbosity; per-slot `reasoning_effort`; `privacy_filter: display|full`.

---

## 2. Bot Mode specifics (confirmed shape)

Source: [Bot Mode](https://hermes-agent.nousresearch.com/docs/user-guide/bot-mode). The brief's shape is essentially correct, with corrections noted:

- **Bot = profile.** Isolated config/memory/skills/credentials/chat under `~/.hermes/profiles/<name>/`. Bot Mode is a bundled desktop plugin, **on by default**; everything visible from CLI (`hermes -p <bot> chat`).
- **Creation:** desktop "New Agent" (Name/Title/Description + Advanced: clone-from, create-empty, **per-bot model & provider pin**, custom SOUL.md, per-skill/per-toolset/per-MCP enablement, shared OAuth/token pool). CLI equivalent: `hermes profile create` (+ `hermes profile rename` makes bots retaggable, e.g. `@research-buddy`).
- **Roster:** one row per profile (avatar, preview, timestamp) + "Active now" strip (gateway-busy or wrote within 90s). **Correction:** there is no documented `roster.json` file — look/title/avatar/memberships live in the profile's backend-synced *metadata*; cross-machine rosters propagate over Desktop Connections sockets. Peer links *are* config: `bot_peers` in config.yaml + `HERMES_PEER_<NAME>_KEY` in `.env`.
- **Inter-bot messaging:** `message_agent(target="<name>", message="…")` exists **only in canonical Bot Chats**; fire-and-forget, attribution-prefixed, teammate roster (names+roles) injected into every bot chat's system prompt via `agent.bot_mode_protocol: true` (default). Failed turns retry once max, with typed reason codes (`provider_rate_limit`, `context_overflow`, `runtime_offline`, …). Group chats: 2–6 bots, ≤3 serial rounds, ≤10 msgs/send, members may pass; `@user` escalates with a needs-you badge.
- **Routines:** plain cron jobs named `[bot:<name>] <routine>` — visible in `hermes cron list`; runs land in the bot's own chat history. Structured schedule picker in desktop; raw Hermes schedule string in Advanced field.
- **Proactivity/wakeups — yes, three layers:** (1) cron/routines on the gateway's 60s tick ([Cron internals](https://hermes-agent.nousresearch.com/docs/developer-guide/cron-internals)); (2) [Session Heartbeats](https://hermes-agent.nousresearch.com/docs/user-guide/features/heartbeat) (`/heartbeat every 10m <prompt>` re-enters idle sessions) and [Recurring Loops](https://hermes-agent.nousresearch.com/docs/user-guide/features/loops); (3) bot-initiated DMs — `message_agent` anytime, and cross-machine `hermes peer dm spark/researcher < file` which runs a turn remotely and prints the reply. Live interrupt of a busy bot is explicitly future work; delivery is per-invocation.
- **Multi-machine:** Desktop Connections relay (rosters propagate; `message_agent(target="moxie@<connection>")`; Desktop must be running — it's the courier), and Desktop-less **`hermes peer add spark --url http://spark.lan:8377 --key <API_SERVER_KEY>`** after which bots autonomously learn peer targets (`target="spark/researcher"`). Same-named agents across machines disambiguate as `@name-device`.

---

## 3. Community ecosystem

### 0xNyk/awesome-hermes-agent (5.5k★, independent, CC-BY-4.0)

[Repo](https://github.com/0xNyk/awesome-hermes-agent) — maturity-tagged (production/beta/experimental), ecosystem last reviewed 2026-07-16 @ v0.18.2. Categories: Official Resources; Skills & Plugins (Community Skills / Plugins / agentskills.io Ecosystem / Skill Registries & Discovery); Memory Providers; Tools & Utilities (Deployment); Integrations & Bridges; Detection & Media Forensics; Multi-Agent & Swarms; Domain Applications; Forks & Derivatives; Guides & Documentation; Operational Playbooks; Level-Up Blueprints. Notable entries:
- **oh-my-hermes** (witt3rd) — orchestration suite: deep-research, deep-interview, `ralplan` Planner→Architect→Critic consensus, `ralph` verify-loop, triage, autopilot ([repo](https://github.com/witt3rd/oh-my-hermes)).
- **mission-control** (builderz-labs) — fleet/dispatch dashboard with cost tracking ([repo](https://github.com/builderz-labs/mission-control)).
- **rtk-hermes** — `pre_tool_call` shell-output compression plugin, 60–90% token cut on terminal output ([repo](https://github.com/ogallotti/rtk-hermes)).
- **eagle-eye** — 5-layer skill routing (hard triggers→FTS5 BM25→synonyms→embeddings→RRF) before each call ([repo](https://github.com/willingning-coder/eagle-eye)).
- **cronalytics** — cron cost analytics plugin ([repo](https://github.com/8bit64k/cronalytics)).
- **hermes-incident-commander** — autonomous SRE detection/self-healing paired with cron ([repo](https://github.com/Lethe044/hermes-incident-commander)).
- **hermaguard** — adversarial bug-hunt review: 3 parallel attacker subagents + consolidator ([Atlas](https://hermesatlas.com/projects/Sahil-SS9/hermaguard)); same author's **hermes-simplify-swarm** (Hygiene/Clarity/Correctness parallel sub-agents).
- Playbooks worth stealing verbatim: nightly self-evolution + a second verification cron to block optimization gaming; curate USER/MEMORY.md as high-signal infrastructure ([Playbooks section](https://github.com/0xNyk/awesome-hermes-agent#operational-playbooks)).

### hermesatlas.com

[Site](https://hermesatlas.com) — community map, 240+ repos / 12 categories, weekly curation, source repo ksimback/hermes-ecosystem. Tracks core at v0.20.5 / 236.6k★. Curated lists include Best memory providers, Top skills, Deployment options, **Multi-agent frameworks**, Developer tools, Workspaces & GUIs. Highlights: hermes-webui (nesquena, 17.7k★), fathah/hermes-desktop (14k★), cc-switch (129k★ multi-agent manager), SkillClaw (AMAP-ML, collective skill evolution), mnemosyne (zero-dep sub-ms memory), gbrain (garrytan).

### Skill hubs/registries beyond official

- **skilldock.io** (chigwell) — registry of reusable skills on the AgentSkills spec ([Atlas](https://hermesatlas.com/projects/chigwell/skilldock.io)).
- **hermeshub** (amanning3390) — community browse/search/one-click-install hub ([Atlas](https://hermesatlas.com/projects/amanning3390/hermeshub)).
- Official integrations remain the primary path: agentskills.io, skills.sh, browse.sh, ClawHub ([Skills System](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills)).

### nyk.dev session-management guide takeaways

[Guide](https://www.nyk.dev/blog/hermes-agent-session-management-guide) (Jul 15 2026): sessions are transcripts, not project memory; one immortal chat degrades the agent. Decision rule: **resume** while scope unchanged, **compress** when bloated (write a repo "session receipt" first so constraints survive summarization), **new** when the deliverable changes, **branch** before competing implementations. Name sessions after artifacts; prune with `--dry-run` + age bounds; export receipts before deletion; weekly audit. Ships a paste-ready "Session Control Card."

---

## 4. Known issues / version notes

- Velocity is extreme (v0.19→v0.20 alone: ~3,650 commits, ~1,400 PRs — [release](https://github.com/NousResearch/hermes-agent/releases/tag/v2026.8.3)); pin tagged releases rather than main for anything unattended.
- **Bot Mode maturity:** shipped into the desktop app, on by default, CLI-parity guaranteed (bots are just profiles). Documented gaps: no live interrupt of a mid-turn bot (fire-and-forget only); cross-machine Desktop-relay delivery requires the Desktop running (use `hermes peer` for always-on); group chats cap at 6 members / 10 messages per send ([Bot Mode](https://hermes-agent.nousresearch.com/docs/user-guide/bot-mode)).
- Cron drift guard: unpinned jobs **fail closed** when the global model changes (#44585) — pin models on unattended jobs ([Cron](https://hermes-agent.nousresearch.com/docs/user-guide/features/cron)).
- Cron-run sessions can't create cron jobs unless `cron.allow_agent_scheduling: true`; workdir jobs serialize on the scheduler tick.
- Two writers on one profile compound memory state — the docs warn repeatedly ([Profiles](https://hermes-agent.nousresearch.com/docs/user-guide/profiles)).
- awesome-list's snapshot (v0.18.2) lags current; re-check any pinned community project before adopting ([awesome-hermes-agent](https://github.com/0xNyk/awesome-hermes-agent)).

---

## 5. Adoption recommendations for a diagnostic-swarm setup

Relevant to Mike's stack (omlx qwen3.8 :8300, FreeLLMAPI :3100, desktop app):

1. **Scout/research bots as profiles with pinned cheap models.** `hermes profile create scout --description "Reads sources, writes findings."` then pin the bot's model in New Agent → Advanced (or inherit). Keep omlx qwen3.8 as scout model; FreeLLMAPI for aggregators. Bots stay reachable as `@scout` in any chat ([Bot Mode](https://hermes-agent.nousresearch.com/docs/user-guide/bot-mode)).
2. **Morning-brief bot = routine + `bot-chat` delivery + continuity.**
   ```
   hermes -p briefing cron create "0 7 * * *" \
     "Summarize overnight findings from scouts; flag anomalies." \
     --deliver bot-chat --continuity --provider <freellm-api> --model <id>
   ```
   `--continuity` gives dedupe against yesterday's brief; delivering to `bot-chat` makes the bot *act* on it rather than just post ([Cron](https://hermes-agent.nousresearch.com/docs/user-guide/features/cron)).
3. **Pipeline pattern:** chain collector → triage → reporter with `context_from` (docs' worked example maps 1:1 onto a diagnostic swarm), and put `wakeAgent:false` pre-check scripts on frequent pollers so idle ticks cost $0.
4. **Auditor bot pattern:** give the auditor a minimal capability surface (per-skill/toolset/MCP toggles in Advanced), `skills.write_approval: true` on writer bots, and adopt hermaguard-style parallel adversarial review (3 attackers + consolidator) as a skill bundle: `hermes bundles create audit --skill … ` ([bundles](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills)).
5. **Cross-machine swarm:** register homelab boxes with `hermes peer add <name> --url http://<host>:8377 --key <key>`; then `message_agent(target="box2/scout")` works from every bot chat with zero Desktop dependency ([Bot Mode](https://hermes-agent.nousresearch.com/docs/user-guide/bot-mode)).
6. **Escalation ladder instead of always-MoA:** run single-model bots normally; define one MoA preset (`reference_max_tokens: 600`, `fanout: user_turn`, aggregator on your strongest endpoint) and `/moa` hard diagnoses one-shot ([MoA](https://hermes-agent.nousresearch.com/docs/user-guide/features/mixture-of-agents)).
7. **Ops hygiene:** nyk.dev Session Control Card for long-lived diagnostic sessions; cronalytics for spend attribution; `[SILENT]` on healthy-tick monitors; ack incidents via `hermes cron incidents ack`.

---

## SOURCES

- https://hermes-agent.nousresearch.com/docs/llms.txt
- https://hermes-agent.nousresearch.com/docs/user-guide/bot-mode
- https://hermes-agent.nousresearch.com/docs/user-guide/configuration
- https://hermes-agent.nousresearch.com/docs/user-guide/profiles
- https://hermes-agent.nousresearch.com/docs/user-guide/features/skills
- https://hermes-agent.nousresearch.com/docs/user-guide/features/memory
- https://hermes-agent.nousresearch.com/docs/user-guide/features/memory-providers
- https://hermes-agent.nousresearch.com/docs/user-guide/features/cron
- https://hermes-agent.nousresearch.com/docs/user-guide/features/mixture-of-agents
- https://hermes-agent.nousresearch.com/docs/guides/use-soul-with-hermes
- https://hermes-agent.nousresearch.com/docs/reference/mcp-config-reference
- https://github.com/NousResearch/hermes-agent/releases (+ releases API)
- https://github.com/0xNyk/awesome-hermes-agent
- https://hermesatlas.com
- https://www.nyk.dev/blog/hermes-agent-session-management-guide
