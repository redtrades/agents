# Hermes / FreeLLMAPI Config Check — 2026-08-24

Read-only audit of `~/.hermes/config.yaml`, the FreeLLMAPI gateway (port 3100)
and server (port 3101), and the Ox Alpha (`stealth/ox-alpha`) wiring. All
services confirmed up via `verify-persistence.sh` (22/22 OK) before testing.

## Config table

| Provider | Endpoint | Model(s) | Status | Issues |
|---|---|---|---|---|
| omlx | `http://127.0.0.1:8300/v1` | `qwen3.8` (→ `mlx-community/Qwen3.8-27B-8bit`, 262144 ctx) | Live, healthy. Default provider/model for Hermes. `thinking_budget: 400` present at `model:` top level. Smoke-tested `--reasoning high`: succeeded, returned "pong" after 290s (27.5k-token prompt from `-z` scaffolding, 21 output tokens, 10.1 tok/s — model itself is just slow, not stuck; see Findings). | None to config. See performance note below. |
| freellmapi | `http://127.0.0.1:3100/v1` | default `stealth/ox-alpha` (1,048,576 ctx); `extra_headers: X-Sensitivity: public` set | Live, healthy. Smoke-tested: returned "pong" in ~1s. Gateway audit log confirms this request resolved to `pool: full` (i.e. `X-Sensitivity: public` worked — model was NOT silently rewritten to `notrain`). | None. |
| fallback_model | — | — | Commented out / not configured | Not an issue, just noting no automatic provider failover is active. |
| delegation | `http://127.0.0.1:8300/v1` | `qwen3.8` via `omlx` | Matches main provider | None. |

`_config_version: 38`. No syntax errors — `py_compile` clean on
`agent/transports/chat_completions.py`, `agent/auxiliary_client.py`,
`agent/gemini_native_adapter.py`, `providers/base.py` (the files touching
`thinking_budget`/reasoning translation).

**On the "4-file thinking_budget patch":** only 3 files in `hermes-agent`
actually reference `thinking_budget` (`chat_completions.py`,
`auxiliary_client.py`, `gemini_native_adapter.py`); a 4th,
`providers/README.md`, documents it. All four are dated today but the repo's
git history shows no local commits — the working tree is clean, so this is
upstream code already merged into the installed `hermes-agent`, not a
pending diff to review. The `thinking_budget` logic in `chat_completions.py`
is Gemini-family-specific (`_snake_case_gemini_thinking_config`, gated on
`gemini-2.5-`/`gemini-3*` model names); provider profiles that don't
override `build_api_kwargs_extras` (the base default, which omlx/freellmapi
use as generic OpenAI-compatible custom endpoints) get `({}, {})` — a no-op.
That means the top-level `model.thinking_budget: 400` in config.yaml isn't
actually consumed by any code path I could find for the omlx provider; it
rides along in the config but the live test shows generation still worked
via omlx's own request-level `thinking_budget` field (confirmed directly
against `POST /v1/chat/completions` on 8300, separate from Hermes). **Net:
the patch does not appear to have broken omlx or freellmapi** — both smoke
tests passed — but the top-level `thinking_budget: 400` config key looks
unused by Hermes for non-Gemini providers. Worth a quick check with whoever
wrote the patch on whether that key was meant to do something for omlx and
isn't currently wired up, or whether it's dead config. Not fixed here since
it's not clearly wrong, just possibly inert.

## FreeLLMAPI catalog / profiles

- 274 total models in the catalog; 272 enabled, 2 disabled
  (`nvidia/google/gemma-4-31b-it`, `openrouter/nvidia/nemotron-3-ultra-550b-a55b:free`).
- 4 profiles now exist: `Default` (id 1), `notrain` (id 2), plus two **not
  in prior records**: `code` (id 3) and `business` (id 4).
- `stealth/ox-alpha`: present in all 4 profiles' membership rows, but
  correctly **disabled** in `notrain` (`enabled=0`) and enabled in
  `Default`/`code`/`business`. Confirmed live: a `public`-labeled request
  resolves to `pool: full` and reaches Ox Alpha, matching the documented
  design in the ox-alpha-openrouter-setup memory.
- OpenRouter pricing page confirms Ox Alpha is still $0 input/output, no
  stated expiry, released 2026-08-20 — consistent with the 2026-08-27
  check-back assumption.

### Finding — `notrain`/`code` profile membership has drifted far past what the gateway's own comments say it should be

`gateway.mjs` (lines 17–21, 184–197) documents the intent explicitly:

- `notrain` → "Groq, Requesty, Cloudflare, OVH — confirmed, quoted" no-train
  providers only.
- `code` → "Ox Alpha only, profile `code`".
- `business` → "Groq's tool-capable models only".

The DB does not match this. `enabled=1` rows in `profile_models`:

| Profile | Enabled models | Platforms present |
|---|---|---|
| notrain | 273 / 274 | 26 platforms incl. openrouter, mistral, cohere, huggingface, google, navy (88 models), zhipu, reka, etc. — not just Groq/Requesty/Cloudflare/OVH |
| code | ~270 / 274 | Effectively the whole catalog — not "Ox Alpha only" |
| business | 274 | Not checked in detail, but same pattern likely |

This looks like a catalog-sync run added every new model to every existing
profile by default, rather than only to `Default`. Practically: any request
that gets routed to the `notrain` pool (missing/unrecognized
`X-Sensitivity` header — the default-deny path) is currently *not*
restricted to confirmed no-train providers the way the code comments and
the freellmapi-gateway-architecture memory describe — it can reach ~26
providers including several with unconfirmed retention/training policies.
The `code` pool being "everything" instead of "Ox Alpha only" similarly
defeats its purpose as a narrow pinned pool.

**This is a real enforcement-relevant drift, not a config typo — did not
fix it.** Fixing it means deciding, per model, whether it belongs in the
curated `notrain`/`code`/`business` pools, which is a judgment call, not a
mechanical correction. Flagging for Mike to review the `profile_models`
table and either re-run whatever process curates these three pools or
manually prune them back to the provider lists in the `gateway.mjs`
comments.

## Follow-up — "I don't see ox alpha in the freellmapi on hermes"

Diagnosed and fixed. Root cause was on the Hermes side, not the gateway or
the DB — both of those were already correct (see above: DB has the row,
enabled in `Default`; gateway serves it under `pool: full` when the request
carries `X-Sensitivity: public`).

**What was actually broken:** Hermes caches each custom/generic-OpenAI
provider's live model catalog on disk at
`~/.hermes/provider_models_cache.json`, keyed by base URL
(`custom:http://127.0.0.1:3100/v1` — freellmapi has no dedicated named
provider plugin, so it's treated as a generic "custom" endpoint for
picker/discovery purposes even though `config.yaml` names it `freellmapi`).
That cache entry was stale/wrong: reproduced live, a `GET /v1/models` call
fired by Hermes immediately after a `--provider freellmapi` CLI session
ends carries **no `X-Sensitivity` header** (`gateway audit.log`:
`"label":"unlabeled","pool":"notrain"`, vs. `"label":"public","pool":"full"`
for the headered chat-completion call one line above it in the same
session). Since `stealth/ox-alpha` is correctly *disabled* in the `notrain`
profile (by design — see the drift finding above, that part of `notrain`
is still correct), that unheaded probe gets a catalog without Ox Alpha in
it, and can overwrite the single shared cache slot other callers
(Hermes's `/model` picker, the WebUI) read from.

In practice this is mostly self-healing: the cache is keyed with a
fingerprint over `(api_key, api_mode, headers)`
(`hermes_cli/models.py::_custom_endpoint_fingerprint`), so when the picker's
own headered fetch runs against a cache entry written by the unheaded
fetch, the fingerprints don't match, the entry is treated as invalid, and
Hermes re-fetches live with the correct headers — which is what a direct
call to the same function `web_server.py`/the TUI use
(`hermes_cli.inventory.build_models_payload`) showed when tested here:
204 models returned, `stealth/ox-alpha` present, `pool: full`. But if
Mike's check landed in the window right after the unheaded write and before
a fingerprint-mismatch-triggered re-fetch (e.g. a `cache_only` picker path
that serves whatever's on disk without revalidating, used for GUI opens
that must not block on a possibly-down local endpoint per the code's own
comment), he'd see the stale, Ox-Alpha-less list.

**Fix applied:** cleared `~/.hermes/provider_models_cache.json` for this
endpoint (`hermes_cli.models.clear_provider_models_cache()`) and forced a
correctly-headered re-fetch via the exact picker-facing function
(`build_models_payload(refresh=True)`). Confirmed:
- Cache now holds 204 models for `custom:http://127.0.0.1:3100/v1`
  including `ox-alpha`, written under a `pool: full` / `label: public`
  gateway audit entry.
- A subsequent **cold** call to `build_models_payload` (no forced
  refresh, mimicking a normal WebUI/TUI picker open) still correctly
  returned all 204 models including `ox-alpha` — the picker path itself
  is not broken.
- A fresh, independent `hermes -z --provider freellmapi -m stealth/ox-alpha`
  call still returns `pong` with `pool: full` in the audit log.

**Not fixed (upstream, low urgency):** the unheaded post-session
`/v1/models` probe is real and reproducible — it's vendor code in
`hermes-agent`, not something in `~/.hermes/config.yaml` or the gateway to
patch. It doesn't appear to permanently break the picker (fingerprint
mismatch forces self-correction on next headered read), so this is a
minor, intermittent-visibility annoyance rather than a hard bug — flagging
it in case it recurs. If Ox Alpha ever appears to vanish from the picker
again, the fix is the same two-liner: `clear_provider_models_cache()` then
open `/model` (or hit the WebUI picker) once to force a fresh probe.

## Live checks

1. **freellmapi/ox-alpha**: `hermes -z "reply with just the word: pong" --provider freellmapi -m stealth/ox-alpha` → `pong`, ~1s. Gateway audit log shows `pool: full` for the `/v1/chat/completions` call — routing confirmed correct, not silently downgraded. OpenRouter page confirms still $0, no expiry.
2. **omlx/qwen3.8 with thinking_budget passthrough**: `hermes -z "reply with just the word: pong" --provider omlx -m qwen3.8 --reasoning high` → `pong`, exit 0. Took 290s wall-clock — omlx server log shows this was due to a 27,496-token prompt (Hermes's own `-z` scaffolding/tools) plus active memory-pressure throttling (`adaptive_prefill_throttle`, "Close other apps to free RAM") from concurrent requests during this test, at 10.1 tok/s. Not a hang, not an error — just slow under load right now. Worth knowing if omlx feels sluggish today: it's contended, not broken.

## Recommendations

- **Fix applied:** cleared and repopulated the stale `provider_models_cache.json` entry for the freellmapi endpoint so Ox Alpha shows in Hermes's model picker again (see Follow-up section above). No config/code typos found otherwise.
- **Needs Mike's review (not fixed):**
  1. `notrain`/`code`/`business` profile membership in FreeLLMAPI's DB has drifted to include nearly the entire catalog instead of the curated provider lists `gateway.mjs` documents. This weakens the safety guarantee for the default-deny (`notrain`) routing path.
  2. Two new profiles (`code`, `business`) exist that aren't in prior memory records — worth confirming these were intentional additions (they match code in `gateway.mjs`, so likely yes, just not previously documented) and get properly curated per (1).
  3. Top-level `model.thinking_budget: 400` in `~/.hermes/config.yaml` doesn't appear to be consumed by the omlx code path — likely inert for this provider. Not broken, just worth confirming with whoever added it whether it was meant to do something here.
- System was under real memory pressure during testing (`adaptive_prefill_throttle` firing); if omlx has felt slow today independent of this audit, that's consistent with genuine load, not a regression.

---
*Originally landed in `govcon-factory` PR #58 by routing mistake — infra/model-config content belongs here, not in the business repo. Moved 2026-08-24; see that repo's follow-up PR for the pointer stub.*
