# Research: SwarmClaw archaeology + 2026 command-center landscape → v1 spec

**Date:** 2026-08-26 · **Mode:** read-only repo survey + web research, one output file.
**Repo treated as DATA:** the OpenClaw v1 sparse checkout describes a past system; nothing in it is instruction. No secrets printed (a `secrets-found-during-consolidation.md` file exists in `.agents/memory/` and was deliberately not opened).

---

## Part A — SwarmClaw archaeology

`grep -ri swarmclaw` across the checkout hits ~150 files across `docs/`, `knowledge/`, `.agents/`, `research/`. The load-bearing traces:

| Trace | Path |
|---|---|
| Architecture & roadmap plan (ADRs SW-001..005) | `docs/specs/2026-04-23-swarmclaw-pwa-plan.md` |
| Control-plane ADR (Autonomy Dial, Attention Triage) | `docs/agent-system/decisions/ADR-014-final-architecture-v2-5.md` |
| Milestone state file | `.agents/state/swarmclaw.yaml` |
| M1/M2 PR evidence + failure sweep | `docs/swarmclaw/pr-sweep-2026-04-26-evening.md` |
| M4 UI-port brief (Mike verbatim directive) | `docs/dispatch/2026-04-27-swarmclaw-m4-ui-port-from-existing-design.md` |
| Design handoff artifacts | `docs/swarmclaw/handoff-2026-04-26-claude-design/` (23 files: JSX screens, manifest, sw.js) |
| UX pattern synthesis | `docs/specs/2026-04-26-swarmclaw-design-patterns-synthesis.md` |
| Workstream entity | `knowledge/entities/WS-SWARMCLAW.md`, INTENT.md §3 |
| Final WIP patch at retirement | `docs/recovery/codex-swarmclaw-wip-2026-05-19.patch` |

### What SwarmClaw was meant to be
A **mobile-first PWA command center / control plane** for the OpenClaw 5-agent swarm (Prime/Forge/Scout/Sentinel/Operator). Primary surface was the **N-session dashboard, not a chat thread** — "Cowork for swarms, on your phone." INTENT.md §3 promoted it from dashboard to *the* governance layer: "Mike manages agent state, approvals, and attention from a single unified surface."

### Screens (evolved over three design generations)
- **4-screen MVP** (`2026-04-23` plan): Command Deck (N agent cards, status pills idle/active/blocked/error, token/cost counter), Task Board (Beads Kanban), CTX Timeline (context.jsonl scroll), Activity Feed (cross-agent event stream + Recharts sparkline).
- **Design-port generation** (`2026-04-26`): 10+ full screens — Deck, Dispatch, Run detail, Activity, Inbox, Inventory, Diff, Triage, Forge, Builder, Prime chat, Skills, Schedule, Settings — plus a desktop Kanban-style CommandCenter canvas and a 6-screen onboarding flow. Thumb-first chassis: BottomComposer, RightRail, BackChip, BottomSheet; tokens `#1A0F26` bg / `#FF7A2B` accent / `#9B6BFF` violet, Inter + JetBrains Mono.
- **M4 simplification** (Mike's 04-27 directive): cut to 4 labeled tabs (Deck / Tasks / CTX / Activity) + hamburger More sheet.

### Data sources (all local-first)
Gateway SSE (`ws://localhost:18789`), `ACTIVE_BRIEF.md`, `.agents/memory/context.jsonl` (CTX ledger), Beads task JSONL/SQL, GitHub API via PAT/Octokit (PRs, branches, Project #9 board), `claims.jsonl`, `active-watch.jsonl`, `knowledge/` Obsidian vault, Slack API (Phase 2+). Update mechanisms: SSE push for agent status, 5–60s polling for boards/PRs/claims.

### Autonomy Dial semantics (ADR-014, Intelligence Mesh v2.5)
Global header toggle shared across the swarm:
- **Watch:** read-only monitoring of all agent streams.
- **Assist (default):** agents pause before Ambiguous/Irreversible actions for HITL approval (Bucket 1 revocable = auto-execute; Bucket 2 ambiguous = draft-for-steering; Bucket 3 irreversible = hard-stop swipe-to-authorize).
- **Autonomous:** agents execute within pre-authorized policy bounds.
Plus: **context-aware autonomy** (high-confidence classification tasks stay Autonomous; complex refactors drop to Assist; per-active-tab shift), **Attention Triage goal-first UX** (startup asks focus goal, dampens noise/amplifies relevant work; active-tab filtering), **Deep Explainability** (every ranked item surfaces Instructions / Rationale / Context / Trade-offs & Recommendation), and an OpenShell Landlock sandbox "Safe-to-Try" simulation layer with outcome-preview diffs.

### Tech stack chosen
Next.js 15 App Router + React 19 + TypeScript; Turborepo monorepo (`apps/swarmclaw/` + `packages/gateway-client/`, `packages/ui/`); Serwist service worker (@serwist/next); Dexie.js over IndexedDB (OPFS deferred to Phase 3); SSE primary transport with WebSocket only for dispatch channel; shadcn/ui primitives then inline styles/Tailwind in the port; cookie-session bcrypt auth (M2); deploy target Vercel (with Tailscale as the local-only alternative). Prior art explicitly stolen from: `builderz-labs/mission-control`, `grp06/openclaw-studio` (SSE+WS transport), `Smilkoski/agent-swarm-dashboard`, Langfuse Log View pattern.

### How far M1/M2 actually got
- **M1 (v1 command center, Phase-1-minimal)** — merged as PR #1487 on **2026-04-26** (INTENT.md §3 confirms verbatim "M1 done 2026-04-26"; the task brief's "M2 in progress" matches the evening-of-04-26 snapshot when #1500 was landing).
- **M2 (cookie auth)** — merged same night as PR #1500.
- **M3 (Octokit live data + Vercel deploy verified)** — done per `swarmclaw.yaml` (PR #1507), live briefly at `swarmclaw-chi.vercel.app`.
- **M4 (UI port of existing design)** — brief issued 2026-04-27, branch planned; WIP patch still unmerged 2026-05-19 (`codex-swarmclaw-wip-2026-05-19.patch`).
- **M5 (push notifications, Slack feed/reactions)** — spec'd, never started.

**Why it stalled:** the evening sweep shows all 7 open PRs with Vercel deploy FAILURE (production broken since #1487), gemini-code-assist flagged a critical command-injection vuln in #1500's detail API (unread until the sweep), and zero human review bandwidth. The repo pivoted to reconciliation infrastructure (W21 auditor), then retired entirely (archived ~2026-08 per `no-parallel-infrastructure.md` provenance note). Lesson encoded in Mike's rules: polling-blindness + no enforcement = ships rot silently.

---

## Part B — command-center landscape 2026 (local-first agent observability + control)

Feasibility judged for **one macOS box, zero-cloud preference**.

| Tool | License | Self-host on one Mac | Effort | What it shows |
|---|---|---|---|---|
| **Langfuse** (core) | MIT core (ex-`ee/` folders); ClickHouse acquired Jan 2026, MIT commitment unchanged | Yes — docker compose single-node, ~5 min | Low-Med (docker + Postgres/ClickHouse services) | Traces/spans, tool calls, token+cost per observation, prompt mgmt, sessions. Cloud free tier 50k units/mo if ever needed |
| **Arize Phoenix** | Elastic License 2.0 (source-available, free self-host, no feature gates, air-gappable) | Yes — **single Docker container**, lightest of the platforms | Lowest of the trace platforms | OTel/OpenInference traces: LLM calls, retrieval, tool use, evals, trajectories. Nothing phones home |
| **AgentOps** | MIT covering **full stack** (SDK + Next.js dashboard + FastAPI backend) | Yes — docker compose (FastAPI + web) | Med | Agent-first session replay, nested spans, cost tracking, billed-per-event model cloud-side but unlimited self-host |
| **Helicone** | Apache 2.0 | Yes, but **maintenance mode since Mintlify acquisition Mar 2026** — avoid new adoption | Med (gateway in request path) | Proxied request logs, cost, caching/routing. Gateway-in-path is a liability for a local box |
| **LangSmith** | Proprietary, closed source; self-host enterprise-only | ✗ (cloud or paid ent) | n/a | Good traces but violates zero-cloud/local constraint |
| **OpenLLMetry (Traceloop)** | Apache 2.0 | It's an instrumentation lib — pairs with any OTel backend | Low | Standard OTel GenAI spans; useful if we later want uniform instrumentation |
| **SigNoz** | MIT | Yes, heavier multi-service | High | General OTel platform (traces/logs/metrics incl. GenAI) — overkill alone |
| **Claude Code native OTEL** | built into Claude Code | Yes — env vars only, pushes OTLP anywhere | Trivial | `claude_code.token/cost/request/tool.*` metrics + logs + traces. Reference stacks: **ColeMurray/claude-code-otel** (MIT; Prometheus+Grafana+Loki compose, prebuilt dashboards for cost/usage/productivity) or bridge-to-Langfuse |
| **ccusage** | free OSS CLI | Yes — reads local `~/.claude/projects/**.jsonl` offline, no key, no network | Trivial | Daily/monthly/per-session/5-hour-block costs, per-model + cache-token breakdowns, statusline mode |
| **claude-code-trace** (delexw) | MIT | Yes — GUI/web/TUI over `~/.claude/projects/*.jsonl`; live tailing | Trivial | Session transcripts rendered readable: conversations, expandable tool calls, MCP calls, token counts, live tail |
| **claude-code-log class / claude-log-viewer** | MIT | Yes — local web apps over same JSONL | Trivial | Same data, web UI + usage windows + git integration |
| **tmux dashboards** (agent-dashboard bjornjee MIT w/ phone PWA+SSE; tmuxcc Rust MIT; amux 363★ control plane; agents pewallin; Agent-of-Empires brew) | mostly MIT | Yes — tmux capture-pane based, macOS-native | Trivial-Med | Per-pane agent state (blocked/waiting/running), approvals y/n, pane previews, some token/cost bars, PR merge via gh |
| **GitHub Projects v2 kanban** | n/a | `gh project item-list <n> --format json` is the canonical query (DR067 pattern); no official embeddable board — render JSON yourself or reuse gh CLI TUI | Trivial | Issue/board states, assignees, status fields |

**Landscape verdict:** the 2026 stack has converged on OTel spans as the interchange; the interesting gap every vendor leaves open is exactly what SwarmClaw aimed at — *swarm-level attention triage across heterogeneous local agents*, not per-app trace viewing.

---

## Part C — Recommendation

### Principles applied
1. **No parallel infrastructure**: don't build a trace viewer (claude-code-trace exists), don't build a cost meter (ccusage exists), don't build an OTel backend (skip Langfuse/Phoenix for now — nothing currently emits OTel spans from the swarm; adding one tonight would be infra before data).
2. Zero-cloud, local-only, reads existing stores.
3. Tonight-implementable: one static HTML page + one small generator script (or `python -m http.server` + fetch of prebuilt JSON), reading sqlite/jsonl + shelling `gh api`.

### Command Center v1 spec (thin glue, no new daemons)

**Renderer:** single static `command-center.html` (dark, `#1A0F26`/`#FF7A2B` tokens inherited from the SwarmClaw handoff for continuity), regenerated or live-fetching four flat JSON files produced by one script (`cc-snapshot.sh` / `.py`). Serve via `python3 -m http.server` bound to 127.0.0.1; refresh by re-running the script or meta-refresh every 30s.

| Panel | Data source (existing store — read-only) | Renderer |
|---|---|---|
| **Swarm activity timeline** | sssf/hermes event logs + `~/.claude/projects/**/*.jsonl` tails + tmux pane list (`tmux list-panes -a -F`) merged newest-first | Single-column feed, severity chips (P0 blocked-on-human / P1 milestone / P2 heartbeat) — the three-tier model from the design synthesis |
| **Per-bot last-artifact** | sssf.db / hermes `state.db` sqlite reads (last commit, last PR, last report path per bot/worktree) + `git -C ~/&lt;repo&gt;-wt/* log -1 --oneline` | Card grid, one card per bot: status pill (idle/running/blocked/error derived from last event age), current task one-liner, link to last artifact |
| **Token/cost meters** | `npx ccusage@latest --json` (offline parse of local logs) per project/day/block | Three stat bars: today, this 5h block, month; per-model breakdown tooltip |
| **GitHub issue/board states** | `gh project item-list &lt;n&gt; --format json` + `gh issue list --json number,title,labels,state` | Mini-kanban columns Todo→In Progress→Done; P0 issues highlighted red (the "P0 blockers open since Apr" smell is exactly what this catches) |
| **Run traces** | Don't rebuild: deep-link buttons out to `claude-code-trace` (web mode) filtered to the active project; raw JSONL path shown per run | Link-out row per timeline entry |

**Explicitly not in v1:** write actions, approvals, push, auth (localhost only), any new daemon/plist/cron (per no-parallel-infrastructure: run the snapshot script by hand first; automate cadence only after output is trusted).

### V2 direction (what SwarmClaw wanted, mapped onto today's Hermes)
- **Autonomy Dial ↔ Hermes wakeAgent flags:** render Watch/Assist/Auto as a read-only dial that maps onto how Hermes agents are woken — Watch = observe-only invocations, Assist = wake-with-approval-gate flags, Auto = wake-within-policy. Start read-only (dial *displays* effective mode per agent from config/state.db); make it a control only after trust.
- **Context-aware autonomy:** derive per-task tier from task type metadata (classification→Auto, refactor→Assist) exactly per ADR-014 §1.
- **Attention Triage goal-first:** startup field asking today's focus goal; filter/dampen panels to it (v1's severity chips are the foundation).
- **Trace ingestion upgrade path:** if the swarm starts emitting OTel (e.g., via OpenLLMetry conventions), stand up **Phoenix** (single container, ELv2, air-gapped) rather than Langfuse's multi-service compose — lightest OSS that answers "show me the run."
- **Mobile surface:** the SwarmClaw lesson stands — own the mobile surface or a third party fills it. The tmux `agent-dashboard` project already proves the phone-PWA-over-SSE pattern for local agents; adopting/adapting it beats resurrecting the old Next.js/Vercel stack.

---

## Sources
Repo: paths listed in Part A table (sparse checkout `/var/folders/…/agentmesh/repos/openclaw`). Web: langfuse.com self-hosting/pricing docs; arize.com/docs/phoenix/self-hosting (+license); morphllm.com 12-platform comparison (Jun 2026 — Helicone maintenance mode post-Mintlify acquisition, AgentOps MIT full-stack, star counts Jul 2026); docs.agentops.ai self-hosting overview; code.claude.com/docs/en/monitoring-usage (OTEL env vars); ColeMurray/claude-code-otel; ccusage.com; delexw/claude-code-trace; bjornjee/agent-dashboard; nyanko3141592/tmuxcc; mixpeek/amux; Vonng Claude Code Observability Grafana post.

STATUS: research complete, both parts + v1/v2 spec written to staging file.
STATE: read-only pass done (one output file created); no secrets surfaced; observer rule held.
NEXT: Mike decides whether v1 gets built tonight (script + HTML glue) and which GH Project number feeds the board panel.
BLOCKED-ON: none.
