# Pre-execution snapshot — Jundot/Qwen3.8-27B-oQ4e-mtp installer

Captured 2026-08-26 ~12:48 EDT, before executing
`.../uploads/7b49b6de-installhermesomlxqwen38.sh`. Purpose: rollback
reference if the installer runs and needs to be undone. Nothing in this
snapshot was modified — read-only pre-flight only.

## Script under review

Path: `.../local_ditto_e057b14c-af8c-42e8-87a5-4ae5a9e2b368_g2/uploads/7b49b6de-installhermesomlxqwen38.sh`

Installs `Jundot/Qwen3.8-27B-oQ4e-mtp` (4-bit quant, MTP head bundled,
~16GB download) via `hf download --local-dir ~/.omlx/models/<name>`,
brew-taps `jundot/omlx` and installs/upgrades the `omlx` formula, runs a
foreground `omlx serve --memory-guard-gb 56 ...` for 8s to persist
settings, calls `omlx stop`/`brew services stop omlx` first, then
`omlx start`, and runs `hermes config set` for
`model.provider/base_url/api_key/default/name` plus two new
`compression.*` keys.

## Live process state (2026-08-26 12:4x EDT)

```
$ lsof -nP -iTCP:8300 -sTCP:LISTEN
python3.1 93924  man  LISTEN 127.0.0.1:8300

$ lsof -nP -iTCP:8000 -sTCP:LISTEN
(nothing — port free)

$ launchctl print gui/$(id -u)/com.mike.omlx-server | grep -E 'state =|pid =|path ='
	path = /Users/man/Library/LaunchAgents/com.mike.omlx-server.plist
	pid = 93924
	state = active / running

$ curl -s localhost:8300/api/status
{"status":"ok","version":"0.6.2","uptime_seconds":26596.6,
 "models_discovered":3,"models_loaded":0,"active_requests":0,
 "waiting_requests":0,"total_requests":86,
 "model_memory_used_formatted":"0B","model_memory_max_formatted":"59.00GB"}

$ curl -s localhost:8300/admin/api/activity
{"active_models":{"models":[],"model_memory_used":1001884264,
 "model_memory_max":63350767616,
 "memory_pressure":{"pressure_level":"ok"},
 "total_active_requests":0,"total_waiting_requests":0}}
```

No model currently loaded in memory (idle-evicted, 3600s idle timeout,
uptime 26596s), zero active/waiting requests. Safe idle point for a
restart if one is later approved — RUNBOOK §2/§3 pre-checks satisfied
as of this capture.

`omlx` is NOT on PATH and NOT a brew formula (`brew info omlx` → "No
available formula"; `brew tap` shows only `mostlygeek/llama-swap`,
`oven-sh/bun` — no `jundot/omlx` tap present). The running binary is
`/Users/man/.venv-omlx/bin/omlx` (pip/venv install, not brew), invoked
by absolute path from the LaunchAgent plist. `~/.venv-omlx/bin/omlx
serve --help` confirms it already supports `--memory-guard-gb`,
`--paged-ssd-cache-dir`, `--hot-cache-max-size`,
`--max-concurrent-requests` — same flag surface the installer uses, so
this is very likely the same upstream project (jundot/omlx) already
installed via a different channel, not an unrelated tool.

## ~/.omlx/settings.json (full contents, pre-change)

```json
{
  "version": "1.0",
  "server": {"host": "127.0.0.1", "port": 8300, "log_level": "info",
    "cors_origins": ["*"],
    "server_aliases": ["localhost","127.0.0.1","m64.local","100.119.108.72","192.168.0.176"],
    "sse_keepalive_mode": "chunk", "auto_start_on_launch": true,
    "burst_decode_mode": "balanced", "preserve_mid_system_cache": true,
    "distributed_inference_enabled": false},
  "model": {"model_dirs": ["/Users/man/.omlx/models"],
    "model_dir": "/Users/man/.omlx/models",
    "model_fallback": false, "hide_helper_models": false},
  "memory": {"prefill_memory_guard": true, "memory_guard_tier": "custom",
    "memory_guard_custom_ceiling_gb": 59.0, "soft_threshold": 0.9,
    "hard_threshold": 0.95, "prefill_safe_zone_ratio": 0.8,
    "prefill_min_chunk_tokens": 32},
  "scheduler": {"max_concurrent_requests": 8, "embedding_batch_size": 32,
    "chunked_prefill": false, "prefill_priority": "context",
    "decode_fairness": true},
  "cache": {"enabled": true, "hot_cache_only": false,
    "gdn_ssd_split_enabled": true, "gdn_snapshot_storage": "auto",
    "gdn_ssd_pending_max_size": "512MB", "gdn_sidecar_precision": "fp32",
    "ssd_cache_dir": "/Users/man/.omlx/cache", "ssd_cache_max_size": "auto",
    "hot_cache_max_size": "8GB", "initial_cache_blocks": 256},
  "auth": {"api_key": "<redacted, see live file>",
    "secret_key": "<redacted, see live file>",
    "skip_api_key_verification": true, "sub_keys": []},
  "sampling": {"max_context_window": 32768, "max_tokens": 32768,
    "temperature": 1.0, "top_p": 0.95, "top_k": 0, "repetition_penalty": 1.0},
  "idle_timeout": {"idle_timeout_seconds": 3600}
  // ... mcp/huggingface/network/logging/claude_code/integrations/ui blocks
  // unchanged from defaults, omitted here for brevity — see live file.
}
```
Full untouched copy: `~/.omlx/settings.json` (as of this capture; no
`.backup-*` exists yet because the installer has not run).

## ~/.hermes/config.yaml (relevant excerpt, pre-change)

```yaml
model:
  provider: freellmapi          # <- installer overwrites to custom:local
  default: auto                 # <- installer overwrites to Qwen3.8-27B-oQ4e-mtp
  max_tokens: 131072
  thinking_budget: 400
  base_url: http://127.0.0.1:3100/v1   # <- installer overwrites to http://127.0.0.1:8000/v1
  key_env: HERMES_CUSTOM_FREELLMAPI_API_KEY
  # no top-level api_key currently — installer adds model.api_key: local-no-key
  # no model.name key currently — installer adds it (|| true, tolerant of failure)
providers:
  omlx:
    api: http://127.0.0.1:8300/v1
    default_model: qwen3.8
    api_key: <redacted>
  freellmapi:
    api: http://127.0.0.1:3100/v1
    default_model: stealth/ox-alpha
    extra_headers: {X-Sensitivity: public}
    discover_models: true
    key_env: HERMES_CUSTOM_FREELLMAPI_API_KEY
# no `compression:` top-level block exists yet — installer adds
# compression.threshold: 0.78, compression.threshold_tokens: 204800 (new keys, additive)
# no `custom_providers:` / named-custom-provider block exists for a
# provider named "local" — see report for why this matters.
_config_version: 39
```
Full file already has Hermes's own prior backups from other work
(`config.yaml.bak-20260826T004220-issue33`,
`config.yaml.bak-2026-08-25-maxtokens-fix`) — the installer's own
`cp -p` backup step is additive to that existing practice, not a
replacement for it.

## Launchd plist (unabridged) — `~/Library/LaunchAgents/com.mike.omlx-server.plist`

Label `com.mike.omlx-server`, `ProgramArguments` =
`/Users/man/.venv-omlx/bin/omlx serve --host 127.0.0.1 --port 8300 --hf-cache`,
`EnvironmentVariables` = `OMLX_QWEN35_Q8_MLP_MIN_TOKENS=256`,
`OMLX_QWEN35_Q8_LINEAR_MIN_TOKENS=256`, `OMLX_FA256_STEEL=0`,
`KeepAlive={SuccessfulExit:false, Crashed:true}`, `ThrottleInterval=10`.
Not touched by the installer script at all (script never edits this
plist or references its Label) — see report for why that matters.

## Models on disk

```
~/.omlx/models/                     — empty (model_dir configured but unused;
                                        current models live in the HF cache instead)
~/.cache/huggingface/hub/models--mlx-community--Qwen3.8-27B-8bit        28G
~/.cache/huggingface/hub/models--mlx-community--Qwen3.8-27B-MTP-8bit   456M
~/.cache/huggingface/hub/models--Qwen--Qwen3-32B                        0B  (hidden placeholder, per RUNBOOK §1c)
```

## Disk space

```
$ df -h / ~
/dev/disk3s1s1   926Gi    12Gi   143Gi   8%   /
/dev/disk3s5     926Gi   743Gi   143Gi  84%   /System/Volumes/Data
```
143GB available (shared APFS container). Target model
`Jundot/Qwen3.8-27B-oQ4e-mtp` totals ~16GB across 4 safetensors shards
(5,016,415,582 + 5,017,583,687 + 5,001,653,251 + 1,936,029,038 bytes +
small config/tokenizer files), confirmed to exist on Hugging Face
(9,075 downloads, non-gated, `qwen3_5` arch, `bits:4`). Ample headroom;
existing 28GB + 456MB models are untouched by the installer regardless
(it never deletes, per its own header comment and code — no `rm` calls
present).

## omlx binary identity

```
$ which omlx          → not found (venv not on PATH)
$ brew info omlx       → No available formula
$ brew tap             → mostlygeek/llama-swap, oven-sh/bun (no jundot/omlx)
$ ~/.venv-omlx/bin/omlx serve --help
  --model-dir, --host, --port, --max-concurrent-requests,
  --memory-guard {off,safe,balanced,aggressive}, --memory-guard-gb,
  --paged-ssd-cache-dir, --paged-ssd-cache-max-size,
  --hot-cache-max-size, --no-cache
```
Running server = venv/pip install at `/Users/man/.venv-omlx`, version
0.6.2 per `/api/status`. `pip show omlx` unavailable (venv has no pip
module installed), so the exact package source (PyPI vs git vs vendored)
couldn't be confirmed from inside the venv itself — inferred to be the
same `jundot/omlx` project the installer taps, based on matching CLI
flags, but not proven identical (could be a fork or pinned older
version with drifted defaults).

## Execution outcome (2026-08-26, ~12:48–13:53 EDT)

Mike approved execution with four adaptations (existing model root, memory
guard 59 not 56, provider stays `omlx` not `custom:local`, upgrade via
brew as scripted). Pre-execution, a clarifying question resolved the
upgrade-channel conflict: since omlx was never brew-installed (confirmed
`direct_url.json`: installed via `uv pip install` from a GitHub release
wheel), Mike chose to upgrade the real venv install via the same
release-wheel channel instead of running the brew commands literally.

**What happened:**
1. `Jundot/Qwen3.8-27B-oQ4e-mtp` downloaded into the standard HF cache
   (`~/.cache/huggingface/hub/models--Jundot--Qwen3.8-27B-oQ4e-mtp`, 16GB,
   all 4 safetensors shards verified byte-exact against the HF API).
   Existing 28GB 8-bit checkpoint + 456MB MTP head untouched throughout.
2. Memory guard ceiling pinned at **59GB** (not the script's 56) in both
   `~/.omlx/settings.json` (`memory_guard_custom_ceiling_gb: 59.0`,
   unchanged from Mike's 2026-08-26 explicit setting) **and** the launchd
   plist (`--memory-guard-gb 59` added to `ProgramArguments`), so a
   `settings.json` drift or reset can't silently regress it — the CLI
   flag re-asserts 59 on every launchd-triggered start.
3. Hermes stayed on provider `omlx` → `127.0.0.1:8300`. Registered the
   new model under the *existing* `providers.omlx.models` block as
   `qwen3.8-oq4e` (alongside `qwen3.8`), not a new `custom:local`
   provider. Set a matching `model_alias: qwen3.8-oq4e` +
   `thinking_budget_enabled: true` on the omlx side via
   `PUT /admin/api/models/{id}/settings` (mirrors the 8-bit model's
   settings), confirmed persisted to `~/.omlx/model_settings.json`.
   omlx auto-marked the newly-loaded model `is_default: true` on
   discovery; reset back to the original 8-bit checkpoint. Added
   `compression.threshold: 0.78` / `compression.threshold_tokens: 204800`
   to `~/.hermes/config.yaml` — confirmed via source read these are the
   standard auto-compaction keys, unrelated to and non-conflicting with
   the separately-gated `micro_compact` (stays off, untouched).
4. **omlx upgrade: attempted 0.6.2 → 0.6.3rc3, found a hang regression,
   rolled back to 0.6.2.** Full detail below — this is the one adaptation
   that did not end where planned.

### The 0.6.3rc3 regression (why it was rolled back)

Upgraded via `uv pip install` of the `v0.6.3rc3` release wheel (latest
tagged release; no non-RC release newer than 0.6.2 exists). Structural
checks passed: `xgrammar` unchanged at 0.2.3, `thinking_budget_enabled`/
`thinking_budget_tokens` fields still present in `model_settings.py`,
memory guard and `idle_timeout_seconds: 3600` both survived the restart
correctly persisted.

Then real verification (`hermes -z ... --provider omlx`, which sends
Hermes's actual ~28K-token default-profile prompt with 25 tool schemas)
hung twice:
- First attempt: mid-prefill, the memory guard evicted the idle 8-bit
  model to free headroom for the new model's large prefill (a "deep
  reset" of the scheduler, logged at 13:32:08) — the request never
  progressed again. Confirmed via a fresh, unrelated 30s-timeout request
  to the *same already-loaded* model getting no response at all.
- Second attempt, deliberately structured with **no** competing idle
  model (so no eviction could trigger): still stalled, this time cold,
  partway through prefill (frozen at a fixed token count for 7+ minutes,
  process CPU ~0.6-0.8%, zero new server-log lines).
- **Differentiating test**: ran the identical Hermes request against the
  *existing, previously-solid* 8-bit checkpoint (not the new model) on
  the same 0.6.3rc3 server. It froze too, on the very first prefill
  chunk. This proved the hang is a **general 0.6.3rc3 regression**
  affecting both models under real tool-calling traffic, not something
  specific to the new checkpoint.

Rolled back via `uv pip install` of the original `v0.6.2` wheel (same
package the venv started with). Re-ran the full chain on 0.6.2: the new
model's `hermes -z` call completed cleanly through the exact token
ranges that froze twice on 0.6.3rc3 (8192, 12288, all the way to
28074), returned the correct `LOCAL_OK`, exit 0. 8-bit model and
grammar-constrained decoding (`response_format: json_schema`) both
reverified working on 0.6.2 post-rollback.

**Net omlx version: unchanged at 0.6.2.** Everything else (model
install, memory guard pin, Hermes registration, compression settings)
stands as delivered — none of it depended on the omlx version.

### Backups written and verified

- `~/Library/LaunchAgents/com.mike.omlx-server.plist.backup-20260826-132247`
- `~/.omlx/settings.json.backup-20260826-132247`
- `~/.hermes/config.yaml.backup-20260826-132247`

All three confirmed non-empty and byte-identical to the pre-change files
at write time (`diff -q` before any edits were made).

### Recommendation for Mike

Don't retry the 0.6.3rc3 upgrade without checking upstream
(`jundot/omlx` issues) for a fix — the hang looks like a scheduler-state
bug tied to the VLM/tool-calling/GrammarCompiler path introduced or
disturbed somewhere in 0.6.1→0.6.3rc3, triggered reliably by any request
carrying Hermes's real tool schema set. Given it's a release *candidate*
(rc3, third RC), waiting for a tagged non-RC 0.6.3 is the lower-risk path
before retrying.

### Rollback: single command (current live version, 2026-08-26)

Current live version is v0.6.2, wheel originally installed from:

```
uv pip install --python /Users/man/.venv-omlx/bin/python3 \
  https://github.com/jundot/omlx/releases/download/v0.6.2/omlx-0.6.2-cp312-cp312-macosx_15_0_universal2.whl
```

(A local copy also lives at
`/private/tmp/claude-501/-Users-man/90ae7fb9-bc4d-41d3-a627-b3992f17f688/scratchpad/omlx-upgrade/omlx-0.6.2-cp312-cp312-macosx_15_0_universal2.whl`
for this session only — that path won't survive past the scratchpad's
lifetime, use the GitHub URL for any future rollback.) After reinstall:
`launchctl bootout gui/$(id -u)/com.mike.omlx-server && launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.mike.omlx-server.plist`.

### Release-notes review, 2026-08-26 (before any further upgrade attempt)

Newest release remains **v0.6.3rc3** (2026-08-24) — no non-RC release
newer than v0.6.2 exists yet. Read all of v0.6.1, v0.6.2 (baseline),
v0.6.3rc1, v0.6.3rc2, v0.6.3rc3 in full for the four dependencies:

- **xgrammar / grammar-constrained decoding**: zero mentions in any of
  rc1/rc2/rc3. No documented change.
- **thinking_budget**: zero mentions in rc1/rc2/rc3 (the one hit in
  v0.6.2 itself is distributed-cluster thinking-budget enforcement,
  already our baseline, not a pending change).
- **idle_timeout / idle eviction**: zero mentions in rc1/rc2/rc3.
- **Memory guard flag/semantics — CHANGED, twice:**
  - **rc2**: *"The memory guard now includes fixed ANE I/O surfaces and
    CPU-sharing allocations, preventing long prefills from repeatedly
    crossing the hard watermark on smaller-memory systems."* — a
    real accounting-logic change to what the guard counts against the
    ceiling, not just a tuning tweak.
  - **rc3**: *"Reported prefill-memory failures correctly. Fast
    non-streaming rejections now return the real HTTP error status
    instead of a successful HTTP 200 with an error body. Streaming
    OpenAI, Anthropic, and Responses API paths preserve structured
    memory-guard details instead of flattening them into generic server
    errors."* — changes how a memory-guard rejection is surfaced to the
    client on the exact code path that was hanging instead of erroring
    in this session's testing.
  - The `--memory-guard-gb` **flag name itself is unchanged** (confirmed
    directly: `omlx serve --help` on the installed rc3 wheel still shows
    `--memory-guard-gb MEMORY_GUARD_GB` and `--memory-guard
    {off,safe,balanced,aggressive}`, identical to 0.6.2).
  - rc1 also touches memory-guard code, but for cluster/remote-admission
    only (irrelevant to this single-node setup).
- **Teardown-hang behavior (RUNBOOK §7.5.1's `fatal_exit`)**: the one
  "teardown" hit (rc1) is about distributed cluster rank-process teardown
  (SIGTERM/SIGKILL for remote peers), not the single-node idle-unload
  path our known bug lives in. Not mentioned as fixed or touched.

**Conclusion**: rc2 and rc3 both make substantive, documented changes to
memory-guard accounting and to how memory-guard-triggered failures are
reported back to the client — exactly the subsystem where this session's
hang occurred (a prefill stalling under memory pressure with no error
ever surfacing, on both the new and the pre-existing model). This lines
up with the empirical hang from the earlier upgrade attempt closely
enough that re-attempting the upgrade without upstream fixing this first
would very likely reproduce it. Per the stop-and-report criterion, the
upgrade was not re-attempted this pass — the two data points (a real
reproduced hang, and a changelog entry describing a change to the exact
mechanism involved) corroborate each other rather than needing to be
re-tested.

hf/huggingface-cli already present on the system via mise
(`~/.local/share/mise/installs/python/3.14.7/bin/{hf,huggingface-cli}`)
— the script's install step is a no-op here, confirmed before touching
anything.

## Rollback pointers

- `~/.omlx/settings.json` — full contents captured above; not yet
  changed. If the installer runs, its own `.backup-<timestamp>` sits
  next to it; the copy above is a second, independent reference.
- `~/.hermes/config.yaml` — full relevant excerpt above; installer
  will also write its own `.backup-<timestamp>` next to it.
- LaunchAgent plist unchanged — no action needed to roll it back unless
  a future step edits it.
- No models deleted by the installer at any point.
