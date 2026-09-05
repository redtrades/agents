# SwarmClaw

Mobile-first PWA control plane for the agent-mesh swarm. SwarmClaw aesthetics
(dark plum `#1A0F26`, claw-orange `#FF7A2B`, violet `#9B6BFF`, 4 thumb tabs,
Autonomy Dial, Attention Triage) backed by **real functional data** — the SSSF
factory run database is the backend of record. Zero dependencies: stdlib-only
Python server + vanilla JS PWA. The original Next.js 15 / React 19 / Serwist /
Dexie stack was deliberately **not** resurrected (see provenance below).

## Run

```
./start.sh          # nohup-launches api.py on http://127.0.0.1:8799
open http://127.0.0.1:8799
stop: kill $(cat swarmclaw.pid)   · log: tail -f swarmclaw.log
```

Install as an app: open in mobile Safari/Chrome → Share/Add to Home Screen.
Served localhost-only; no auth by design.

## Screens vs original SwarmClaw (M1–M3 provenance)

| Tab | This build | Original provenance |
|---|---|---|
| DECK | runs-today stat card w/ fail count, token meter bars, SVG Autonomy Dial (read-only), Attention list (top-5 P0/P1/P2), recent-runs → tap opens run-detail bottom sheet (`/api/run/<id>`) | Command Deck from the 2026-04-23 4-screen MVP (agent status cards, token/cost counter); Autonomy Dial semantics from ADR-014 (Watch/Assist/Auto, Assist default); Attention Triage goal-first UX from the same ADR, reduced to the severity-chip model of the 04-26 design-patterns synthesis |
| BOARD | kanban columns Backlog / Ready / In progress / Blocked-on-Mike / Done, grouped from live `gh api` issues in redtrades/agent-mesh (60s cache); Blocked column highlighted | Task Board (Beads Kanban) from the MVP + GitHub Project board panel from M3's Octokit live-data milestone |
| TIMELINE | merged reverse-chron feed: sssf events + hermes session_model_usage deltas + new files under ~/wiki/briefs + tidbits.jsonl tail; "Load more" paging | CTX Timeline (context.jsonl scroll) + cross-agent Activity Feed from the MVP, unified per the M4 directive that cut 10+ screens to 4 tabs |
| BOTS | roster cards for hermes profiles + sssf factory agents (model, sessions/runs, ctx, last active) with 7-day token sparkbars | Bot roster cards + Recharts sparkline from the MVP Activity generation |

Chassis details kept from the design handoff: bottom tab bar with safe-area
insets, bottom-sheet detail overlay (BottomComposer-era pattern), skeleton
loaders, dark theme with orange/violet accents, Inter/system + JetBrains Mono
stack. Service worker = Serwist's role replaced with a 40-line vanilla sw.js
(cache-first shell, network-first `/api`).

## API (all endpoints answer HTTP 200 with `{"error": ...}` on failure so the PWA never white-screens)

| Endpoint | Data source |
|---|---|
| `GET /api/overview` | sssf.db sessions/phases/events + hermes state.dbs + gh (for attention): bots roster w/ tokens_24h + 7d sparklines, runs summary {today,total,success,fail}, autonomy:"Assist" + autonomy_detail per-bot Watch/Assist/Auto from `~/.hermes/cron/jobs.json` paused proxy, attention top-5 (failing runs, blocked-on-mike issues, stale claims) |
| `GET /api/runs` | `~/agent-workspace/adws/adw_data/sssf.db` sessions table (PRAGMA-defensive column mapping; sessions IS the runs table) |
| `GET /api/run/<id>` | phases (by seq) + events (chronological) for one adw_id |
| `GET /api/board` | `gh api repos/redtrades/agent-mesh/issues` → label→column grouping, 60s in-process cache; GovCon remains a separate system |
| `GET /api/timeline` | merged newest-first: sssf events · hermes usage deltas · new briefs under `~/wiki/briefs` · `tidbits.jsonl` tail (path candidates: ~/wiki, ~/.hermes, ~/agent-workspace) |
| `GET /api/briefs` | listing + latest brief markdown (capped 20k chars) |
| `GET /*` | static PWA shell from `www/` |

Known-degraded sources are reported honestly in each payload (`notes`) and
surfaced at the bottom of the relevant tab rather than hidden: today that
means `~/wiki/briefs` exists but is empty and no `tidbits.jsonl`/`claims.jsonl`
exists yet — the endpoints still work.

## Files

```
swarmclaw/
├── api.py               stdlib-only ThreadingHTTPServer, port 8799, 127.0.0.1
├── start.sh             nohup launcher, pid file, prints URL
├── README.md            this file
├── docs/AUTONOMY-DIAL.md  Watch/Assist/Auto ↔ cron jobs.json paused/wakeAgent mapping (read-only)
└── www/
    ├── index.html       shell: 4 screens + bottom tab bar + run-detail sheet
    ├── styles.css       mobile-first tokens (#1A0F26/#FF7A2B/#9B6BFF), skeletons, safe-area
    ├── app.js           tabs, fetch+render, dial SVG, sparkbars, sheet, SW registration
    ├── manifest.webmanifest   name SwarmClaw, standalone, theme #1A0F26, inline-SVG maskable icon
    └── sw.js            cache-first app shell, network-first /api with offline fallback
```

## v2 — autonomy dial (read-only, done for #16)

- **Autonomy Dial ↔ Hermes wakeAgent flags — done (read-only):** `GET /api/overview`
  now returns `autonomy:"Assist"` (static global, unchanged) plus `autonomy_detail`
  with per-bot `Watch`/`Assist`/`Auto` derived read-only from
  `~/.hermes/cron/jobs.json` (`paused`/`enabled`/`state` proxy; `wakeAgent`/`wake_agent`
  reserved for future Auto). See `docs/AUTONOMY-DIAL.md` for mapping, proxy rule,
  and manual-inspection steps. Still read-only — no writes to `jobs.json`; control
  only after trust.
- **Attention Triage goal-first:** startup focus-goal field that dampens noise
  and filters panels (v1 ships the severity chips only) — still deferred.
- **Push notifications** (original M5): blocked-on-mike and failing-run alerts
  via Web Push — still deferred per #16 (dial must be trusted first).
- Deep-link run rows out to claude-code-trace instead of the built-in sheet — still deferred.
