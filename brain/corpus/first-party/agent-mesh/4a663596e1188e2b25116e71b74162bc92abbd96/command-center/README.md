# command-center

Static, zero-daemon observability dashboard for the agent-mesh swarm. v1 of the
SwarmClaw-derived control plane: one snapshot script + one single-file HTML page,
both read-only over existing local stores. No new daemon, database, or scheduler
(per `AGENTS.md` hard lines — run the script by hand until its output is trusted).

Provenance: this is a direct descendant of **SwarmClaw** (the OpenClaw-era
mobile PWA command center for the 5-agent swarm, M1/M2 shipped Apr 2026, retired
~Aug 2026). The dark tokens (`#1A0F26` bg / `#FF7A2B` accent / `#9B6BFF` violet),
the three-tier severity model, and the Autonomy Dial legend are inherited from
its design handoff and ADR-014. Research/spec:
`research-swarmclaw-command-center.md` (staging).

## Files

| File | Role |
|---|---|
| `snapshot.py` | stdlib-only collector; reads local stores read-only, writes `data.json` |
| `data.json`   | emitted snapshot (gitignore-friendly; regenerate any time) |
| `index.html`  | dashboard; fetches `data.json`; works from `file://` or any static server |

## Data sources (all read-only)

1. **sssf factory** `~/agent-workspace/adws/adw_data/sssf.db`
   Note: there is no `runs` table — `sessions` *is* the runs table.
   Reads: `sessions` (runs), `phases`, `agent_sessions`, `events`. Schema is
   checked via `PRAGMA table_info` at runtime; unknown/missing columns are skipped.
2. **Hermes** `~/.hermes/profiles/*/state.db` → `session_model_usage`
   Per-profile rollups: api calls, input/output/cache/reasoning tokens, cost, last seen.
3. **GitHub** via `gh api` subprocess (issues only, PRs excluded):
   label counts per state for `redtrades/agent-mesh`. GovCon queues are owned
   by their separate repository and are intentionally not aggregated here.
4. **Briefs** `~/wiki/briefs/*.md` — latest by mtime (dir currently absent → `null`).

Any missing source becomes `null` plus a note under `sources.<name>.note`;
the page renders a degraded-source banner instead of breaking.

## Refresh

```sh
python3 snapshot.py && open index.html
```

Or serve it if your browser blocks `file://` fetches:

```sh
python3 -m http.server 8787 && open http://127.0.0.1:8787/index.html
```

## data.json schema (`command-center/v1`)

Top-level keys:

- `schema` — version tag string.
- `generated_at` — UTC ISO timestamp.
- `sources` — per-source `{path, note}`; `note` is null when healthy.
- `swarm_activity.timeline[]` — merged newest-first entries:
  `{ts, source ("sssf.phase"|"sssf.event"), kind, label, status,
    severity ("P0" fail = blocked-on-human | "P1" success milestone |
    "P2" heartbeat), ref (adw_id)}`. Capped at 120.
- `bots.factory_agents[]` — sssf `agent_sessions`: `{adw_id, agent, coding_agent,
  model, context_tokens, context_window, created_at, last_used_at}`.
- `bots.hermes_profiles[]` — per-profile usage rollups: `{profile, sessions,
  api_calls, input_tokens, output_tokens, cache_read_tokens, cache_write_tokens,
  reasoning_tokens, est_cost_usd, act_cost_usd, last_seen_epoch, source_db}`.
- `issues` — `{<repo>: {labels: {<label>: {open, closed}},
  totals: {open, closed, issues_counted}}}` or `null` per repo on failure.
- `runs[]` — sssf runs newest-first (capped 50): `{adw_id, adw_name, request,
  status, engineer, started_at, ended_at, total_tokens, total_cost,
  last_artifact: {name, kind, status, error, at} | null}`.
- `tokens.hermes_totals` — grand sums across profiles.
- `tokens.sssf_runs` — `{total_tokens, total_cost_usd}` summed over runs.
- `tokens.grand_total_tokens` — sssf run tokens + hermes in/out.
- `briefs` — `[{file, mtime}]` or `null`.
- `autonomy_dial.modes[]` — static Watch/Assist/Auto legend (v1 display-only).

## Explicitly not in v1

No write actions, approvals, push notifications, auth, or automation cadence.

## V2 direction

- **Autonomy Dial wired to Hermes wakeAgent flags** — render each mode as
  read-only derived state from how agents are woken (Watch = observe-only
  invocation, Assist = wake-with-approval-gate, Auto = wake-within-policy),
  sourced from Hermes config/state.db. Control surface only after trust.
- Context-aware autonomy per ADR-014 §1 (task-type tiering).
- Attention-triage goal filter on top of the P0/P1/P2 chips.
- If the swarm starts emitting OTel spans: stand up Phoenix (single container)
  rather than building trace views here.
