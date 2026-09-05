# Autonomy Dial — read-only wiring (v2)

## Modes → Hermes flags

| Dial | Meaning (ADR-014) | Hermes cron effect (read-only view) |
|------|-------------------|-------------------------------------|
| **Watch** | observe-only, no wake | cron job `paused:true` / `enabled:false` / `state:"paused"` — tick does not enqueue an agent wake |
| **Assist** | approval-gated wake (default) | `paused:false` + `enabled:true` — tick may wake agent but pauses before Ambiguous/Irreversible actions |
| **Auto** | within-policy autonomous wake | `enabled:true` + `wakeAgent:true` (or equivalent `wake_agent`/`allow_wake`) — tick wakes within pre-authorized policy bounds |

Upstream Hermes stores per-job autonomy in `~/.hermes/cron/jobs.json` (`jobs[]` array). Issue #16 describes this as `wakeAgent` or similar — the exact key is load-bearing to verify, not assume.

Observed as of 2026-08-26 (all 5 jobs in `~/.hermes/cron/jobs.json`):

* Keys present: `id`, `name`, `prompt`, `schedule`/`schedule_display`, `enabled` (bool), `state` (`"paused"` vs `"active"`), `paused` (bool, on `[bot:*]` jobs), `paused_at`, `deliver`, `no_agent`, `monitor_script`, etc.
* No `wakeAgent` / `wake_agent` / `allow_wake` key exists yet on this install — the dial's Auto tier is therefore **reserved** (documented, not wired to a live flag).
* `[bot:*]` jobs (prime/scout/sentinel/morning-brief) are currently `paused:true`, `enabled:false`, `state:"paused"` — they map to **Watch** under the proxy rule below.

## Read-only inspection

### What v1 already exposed

`swarmclaw/api.py:780` `build_overview()` returns a static field:

```json
{
  "autonomy": "Assist",
  "autonomy_legend": [
    {"mode":"Watch","meaning":"read-only monitoring…"},
    {"mode":"Assist","meaning":"default — agents pause before Ambiguous/Irreversible actions…"},
    {"mode":"Auto","meaning":"agents execute within pre-authorized policy bounds"}
  ]
}
```

The PWA (`www/app.js`) renders this as an SVG dial + label. Value was hard-coded to `"Assist"` — correct as a global default but not per-bot.

### What v2 adds (this issue, read-only)

`api.py` now also returns `autonomy_detail` inside `GET /api/overview`:

```json
{
  "autonomy": "Assist",
  "autonomy_detail": {
    "source": "~/.hermes/cron/jobs.json",
    "per_bot": [
      {
        "bot": "prime",
        "mode": "Watch",
        "paused": true,
        "enabled": false,
        "job_id": "a0f43152fbaf",
        "job_name": "[bot:prime] waiting-on enforcement",
        "schedule": "5 8 * * 1-5"
      }
    ],
    "unbound_jobs": [],
    "note": null
  }
}
```

**Proxy rule (read-only, no writes):** for each bot in the roster (`/api/overview` `bots[]`), look up the cron job whose `name` contains `[bot:<bot>]` or whose `deliver` is `bot-chat:<bot>`. If found, `paused:true` (or `state:"paused"`) → **Watch**, otherwise **Assist**. `Auto` requires an explicit `wakeAgent`/`wake_agent` truthy flag — none exists today, so the proxy never emits `Auto`; when Hermes adds that flag, the same reader will surface it without API changes. Rows are also synthesized for cron-defined bots that have no roster usage yet (e.g., `prime` when idle) so the dial shows Watch even before first token.

* `per_bot` — one entry per roster bot plus any cron-defined `[bot:*]` job not yet in the roster; SSSF factory agents with no cron job get `paused:null, enabled:null, mode:"Assist", note:"no matching cron job; defaults to Assist"`; idle cron bots get `note:"cron-defined bot with no roster usage yet"`.
* `unbound_jobs` — cron jobs with no bot match are listed separately so the
  dial does not silently hide them. Jobs owned by other repositories are not
  part of the agent-mesh dial.
* `source` always points at the file read; `note` is non-null only when the file is missing/unreadable — the endpoint still returns 200.

No endpoint writes to `jobs.json`; the dial remains read-only until trust justifies a control.

### How to inspect manually

```bash
cat ~/.hermes/cron/jobs.json | python3 -c "import json,pathlib; d=json.loads(pathlib.Path.home().joinpath('.hermes/cron/jobs.json').read_text()); print(json.dumps(d['jobs'], indent=2))"
# per-bot paused proxy:
python3 -c "import json, pathlib, re; p=pathlib.Path.home()/'.hermes/cron/jobs.json'; j=json.loads(p.read_text())['jobs']; print([(x['name'], x.get('paused'), x.get('enabled'), x.get('state')) for x in j])"
curl -s http://127.0.0.1:8799/api/overview | python3 -m json.tool | grep -A2 autonomy
```

### Future writable dial (deferred)

If the dial ever becomes a control, the write path would flip `paused`/`enabled` (and eventually `wakeAgent`) in `jobs.json` via `hermes cron pause|resume` rather than direct JSON mutation — not implemented in this issue.

## Push notifications — deferred

Per #16, Web Push for `blocked-on-mike` and failing-run alerts (original M5) remains deferred until the dial story is trusted. No service-worker push subscription is added in this patch.

## References

* `swarmclaw/api.py:build_overview()` — static `autonomy` + new `autonomy_detail`
* `~/.hermes/cron/jobs.json` — source of truth (global `jobs[]`, per-job `paused`/`enabled`/`state`)
* `research/research-swarmclaw-command-center.md` §C — v2 direction (dial ↔ wakeAgent, read-only first)
* `swarmclaw/README.md` § v2 — status updated to reflect this wiring
