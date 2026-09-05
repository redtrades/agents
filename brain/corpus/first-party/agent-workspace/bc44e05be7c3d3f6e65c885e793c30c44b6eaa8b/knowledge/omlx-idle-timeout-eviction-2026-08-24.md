# omlx idle-timeout model eviction — 2026-08-24

**Task:** configure omlx (0.6.2, m64) to evict the loaded model after 1hr idle.

**Finding:** the capability already exists natively — no custom watchdog script needed. `~/.omlx/settings.json` → `idle_timeout.idle_timeout_seconds` (global, `null`=disabled, 60s API floor). Per-model override also exists (`ttl_seconds` in `model_settings.json`, unset for all models currently, so global governs).

**Not discoverable from `omlx --help` / `omlx serve --help`** — neither the CLI nor `CONFIG-VALIDATION.md`/`RUNBOOK.md` (written 2026-08-23, one day prior) mention it. Found by grepping the venv source (`~/.venv-omlx/lib/python3.12/site-packages/omlx/settings.py`, `engine_pool.py`, `admin/routes.py`) after the settings-file schema (`~/.omlx/settings.json`) showed an `idle_timeout` key already present with a null value — i.e. the shipped default config already has the field, just unset.

**Key mechanism detail:** it's a **live, no-restart setting**. `POST /admin/api/global-settings {"idle_timeout_seconds": N}` applies immediately (polled every ~1s by the existing memory-enforcer loop) and persists to `settings.json` itself via the endpoint's own `.save()` call. No `launchctl bootout`/`bootstrap` cycle required at all — this task ended up not needing the restart the original instructions assumed.

**Safety property (verified by reading, not just docs):** `engine_pool.check_ttl_expirations()` skips any model with `has_active_requests()` or `in_use > 0`, refreshing `last_access` instead of evicting. A long-running request in flight postpones eviction indefinitely rather than getting killed mid-request.

**Verification status:** test value (60s, the API floor) set 2026-08-24 ~16:10 EDT. A genuine long-running request (1898s+ elapsed, 0.22 tok/s, real agent work) was active on the server at setup time — per the lease-protocol principle (never disrupt another session's active work), verification was staged as a background watcher polling `/admin/api/activity` rather than forcing/killing that request. The watcher waits for natural completion, confirms the model actually unloads within the 60s+poll window, then flips to the production value (3600s) via the same live API — see `~/agent-reports/RUNBOOK.md` §8 for the up-to-date confirmed state.

**Doc updated:** `~/agent-reports/RUNBOOK.md` §8 (new section).
