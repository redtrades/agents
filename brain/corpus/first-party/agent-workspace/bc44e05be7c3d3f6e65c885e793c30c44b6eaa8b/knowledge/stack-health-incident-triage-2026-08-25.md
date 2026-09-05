# Stack-health incident triage, 2026-08-25 evening

Three symptoms Mike reported in one message, treated as one pass: broken
Tailscale sites, FreeLLMAPI "models running out," omlx failing via Hermes.
Filed as [`redtrades/agent-configs#15`](https://github.com/redtrades/agent-configs/issues/15),
self-assigned, left open (real follow-ups remain: Mike's own phone
confirmation on Tailscale, his Cloudflare key correction, optional
`openai-compat.ts` patches). This file is the durable record;
`~/agent-reports/RUNBOOK.md` §7.5.1/§8/§9 carries the operational detail
for omlx and Tailscale; `agent-workspace` `TASK-0002` carries the
Tailscale task thread specifically.

## Symptom 1: Tailscale sites not working

Root cause was **two separate stale/broken routes on top of an
already-fixed collision**, not a fresh Tailscale/tailscaled problem --
`tailscale status`/`tailscaled` were healthy the whole time.

1. `/freellm` sub-path (:443) served FreeLLMAPI's dashboard `index.html`
   fine (200) but the page was broken in any real browser: its JS/CSS
   bundle uses root-relative paths (`/assets/index-*.js`), which under a
   sub-path resolve against Hostname's `/` -- Hermes WebUI's root -- and
   302 to its login page instead. Identical bug class to the `/api`
   collision TASK-0002 already fixed, just on the asset side. Fixed by
   giving FreeLLMAPI its own port, `:8444`, matching the SSSF `:8443`
   precedent, and retiring `/freellm` on :443.
2. The m64 status dashboard's own `STATS_URL` (`~/agent-reports/monitoring/dashboard/index.html`)
   still pointed at `/omlx-admin/admin/api/stats`, a mount name from
   before the current `/admin` mount existed -- so its omlx panel has
   been silently broken (302-via-Hermes-login) independent of whether
   omlx itself was up. Fixed to `/admin/api/stats`.

Every route was verified end-to-end via a real HTTPS fetch through the
tailnet hostname (not just presence in `tailscale serve status --json`),
matching the discipline `verify-persistence.sh` was fixed to use during
TASK-0002. Definitive URL index is in `RUNBOOK.md` §9.1 -- six routes now:
`/`, `/status/`, `/gpu/json`, `/admin/api/stats` (all :443), plus `:8443/`
(SSSF) and `:8444/` (FreeLLMAPI), each confirmed live.

**Not yet confirmed:** Mike's own phone/external-client load. This is the
second round of "looks fixed from m64, Mike says it's still broken" for
this same hostname -- see `TASK-0002`'s note on why self-testing from m64
isn't sufficient evidence.

## Symptom 2: FreeLLMAPI "models running out"

**Not profile drift** -- re-ran the drift-check query from
`~/agent-reports/freellmapi-install/PROFILE-POLICY.md`; all three curated
profiles (`notrain`, `code`, `business`) match policy exactly (notrain:
cloudflare 21 / groq 9 / ovh 13 / requesty 8 = 51; code: openrouter 1;
business: groq 4). The 2026-08-25 `TASK-0003` fix is holding.

**The real problem: of the `notrain` pool's 51 nominal candidates, a large
fraction can't actually serve a real Hermes request:**

- **Cloudflare (21/51, ~41%) — 100% broken, a config bug, not quota.**
  Every single call fails: `Cloudflare API error 404: Could not route to
  /client/v4/accounts/mikeninov@gmail.com/ai/v1/chat/completions`. The
  stored API key is parsed as `account_id:api_token`
  (`server/src/providers/cloudflare.ts:38-41`) -- whoever configured this
  key put Mike's **email address** in the account-id slot instead of his
  actual Cloudflare Account ID (the 32-char hex string in the Cloudflare
  dashboard sidebar). The key's own health check shows `status: healthy,
  last_health_error: (empty)` -- the health check hits a different
  endpoint than actual inference calls, so it never caught this. **Fix
  needs Mike:** re-enter the Cloudflare key via the FreeLLMAPI dashboard
  (now reachable at `https://m64.tailfb03be.ts.net:8444/`, Settings/Keys)
  as `<real_account_id>:<api_token>`. Not something to fix by editing
  `encrypted_key` directly -- that's a credential value, out of scope for
  an agent to write blind.
- **Groq (9/51, ~18%) — structurally too small for real traffic, not
  exhaustion.** Two failure classes seen: several models rejected before
  any call attempt ("no tool-calling support" -- correctly filtered since
  Hermes requests need tools) and the tool-capable ones (`gpt-oss-120b`,
  `gpt-oss-20b`, `gpt-oss-safeguard-20b`, `qwen3.6-27b`) rejected for
  `tpm_limit 8000 < estimated 117425` / `tpm_limit 6000 < estimated
  117425` -- Groq's free-tier tokens-per-minute ceiling can't cover a
  single large tool-heavy Hermes call (skills/tool-catalog payloads
  routinely estimate 100k+ tokens). This isn't a quota that "runs out" --
  it structurally can't serve this shape of request at all, ever, on the
  free tier.
- **OVH (13/51, ~25%) — real quota exhaustion, some real 429s recharging
  over time**, plus two distinct request-shape bugs seen repeatedly:
  `400 feature 'reasoning_effort for this model' is not currently
  supported` (a param sent unconditionally for models that don't accept
  it) and `400 ... messages.2.assistant.name Extra inputs are not
  permitted` (the shared `openai-compat.ts` provider passes through a
  caller-supplied `name` field on assistant messages -- OVH's validator
  is stricter than OpenAI's own spec here and rejects it). Neither patched
  this session (out of the triage's scope; flagged as a follow-up, see
  below) -- fixing both would recover real OVH capacity beyond just
  waiting out the 429s.
- **Requesty (8/51, ~16%) — real quota exhaustion.** `429 You exceeded
  your current quota` and `429 You've hit the rate limit for free
  models... switch to a paid model` -- genuinely out of free-tier budget
  at observation time, not a bug. No documented reset cadence found this
  session; Requesty's own dashboard (whatever key-status surface
  FreeLLMAPI's admin UI exposes) would have the actual window.
- **Multiple requests failed with "routing exhausted (no upstream tried)"
  before any provider was even attempted** -- e.g. `candidates=51:
  cloudflare/@cf/meta/llama-3.3-70b-instruct-fp8-fast: context 24000 <
  estimated 117425` -- meaning the estimated prompt (skills + tool
  catalog + history) exceeds every single notrain-pool model's context
  window, not just the first one tried. This is a capacity mismatch
  between what Hermes actually sends and what a free-tier fallback pool
  can hold, independent of the other three bugs above.

**Net effect:** of 51 nominal notrain candidates, ~21 (cloudflare) never
work at all, ~9 (groq) structurally can't take a real tool-heavy request,
leaving effectively ~21 (ovh + requesty) as the pool's real working
capacity -- and those two are the ones observed rate-limited. "Models
running out" is an accurate description of what's happening, just not for
the reason ("awaiting account signups") originally suspected -- the four
already-configured providers have real, mostly-fixable problems of their
own before a fifth/sixth provider would even help.

**On OpenCode Zen / Nous / Cline (the "awaiting signups" providers):**
confirmed via the DB (`SELECT DISTINCT platform FROM models` /
`api_keys` table) that `opencode` already has catalog entries but **no
active API key** (not in `api_keys` at all), and `nous`/`cline` aren't in
the catalog as platforms yet -- both are genuinely unconfigured, matching
the "awaiting signups" framing for these three specifically. This is
separate, additive work (new provider onboarding) from the four
already-wired providers' bugs above -- worth doing, but won't fix today's
errors on its own since it doesn't touch the four failing providers.

**Recommended next steps (not done this session, out of triage scope):**
1. Mike re-enters the correct Cloudflare account ID (see above) -- single
   highest-leverage fix, recovers ~41% of the pool instantly.
2. Patch `openai-compat.ts` to drop the `name` field on assistant
   messages for providers that reject it (or drop it universally --
   check whether any provider actually needs it) and to stop sending
   `reasoning_effort` to OVH models that don't support it (per-model
   capability flag, similar to `supports_tools`).
3. Consider whether Groq's tool-capable models belong in `notrain`'s
   default-deny fallback chain at all, given they can't serve a single
   real Hermes-shaped request -- they're not *wrong* to be there (they
   are genuinely no-train), just never useful as a fallback target under
   real traffic.

## Symptom 3: omlx failing via Hermes -- root-caused, fixed, verified live

`com.mike.omlx-server` was **not loaded at all** (`launchctl print` -->
"Could not find service"), not just crashed-and-not-yet-restarted.

**Root cause:** `~/.omlx/settings.json` had `idle_timeout_seconds: 60`, a
test value set 2026-08-24 "while eviction is verified live" (per
`RUNBOOK.md` §8's prior text) and never reverted. That made idle-model
unloads ~60x more frequent than the intended 1-hour production cadence.
One of those unload cycles hit a real omlx bug: `engine_core.close()` hung
during teardown, `omlx/utils/fatal.py`'s `fatal_exit()` fired after its
60s internal timeout (`omlx-launchd.log`, 2026-08-25 00:26:41: `CRITICAL
... Engine teardown timed out after 60s ... exiting process so the
supervisor can restart with a clean state`), and called `os._exit(70)` --
a plain non-zero exit, not a signal. The plist's `KeepAlive`
(`Crashed=true`, `SuccessfulExit=false`) did not bring it back up; no
further log activity after that exit, and the service was found fully
unloaded. Whether that's a real gap in the `KeepAlive` conditions for this
specific exit shape, or something else unloaded it afterward, wasn't
resolved -- flagged in `RUNBOOK.md` §7.5.1 as unconfirmed, watch for it
recurring.

**Fixed and verified live, this session:**
- `idle_timeout_seconds` reverted 60 -> 3600 (backup:
  `~/.omlx/settings.json.bak-20260825-incident-triage`). Confirmed live
  via `GET /admin/api/global-settings` post-restart.
- Service restarted per `RUNBOOK.md` §3 (`launchctl bootout` then
  `bootstrap` -- bootout was a no-op since it was already unloaded,
  bootstrap succeeded, pid 19064, healthy within ~2s).
- Ran Mike's exact basic case: `hermes -z "Reply with exactly: PONG" -m
  qwen3.8 --provider omlx` -> `PONG`, exit 0. Confirmed via
  `/admin/api/activity` that the request was actually served by the
  loaded `mlx-community--Qwen3.8-27B-8bit` engine (not a cached/stub
  response) and that `ttl_remaining_seconds` tracked down from ~3600,
  confirming the new idle-timeout value is live.

No lease held on `govcon-factory`'s `leases` branch for `omlx-restart`/
`gpu-heavy` at the time of restart (checked `git ls-tree -r origin/leases`
-- empty), so no coordination conflict. Restart itself was gated on
Mike's explicit go-ahead in-session (the harness's own classifier blocked
the unconfirmed `launchctl bootstrap` call).

**Not fixed, flagged only:** the underlying omlx `engine_core.close()`
teardown hang itself is an upstream/vendored-library bug
(`~/.venv-omlx/lib/python3.12/site-packages/omlx/engine_core.py:1139`) --
mitigated by the idle_timeout revert (far fewer unload cycles = far less
exposure), not root-caused or patched. If `fatal_exit`/`os._exit(70)`
shows up again in `omlx-launchd.log`, that's this same bug recurring, not
a new one.
