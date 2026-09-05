# omlx qwen3.8-oq4e Hermes DESKTOP path — 2026-08-26

Times America/New_York. omlx **0.6.2** left running. No launchctl restart. No 0.6.3rc3. No 8bit load. No brew. No mempalace re-enable. No 144k/262k soak. agent-configs not touched. **Not committed.**

Closed the unfinished Claude session `90ae7fb9` work: first-token desktop path (full profile tools, **not** `-t file`). SHORT_OK/MID_OK from the earlier writeup used `-t file` ~5986 prompt and is **not** this path.

## 1. What changed (paths, before/after)

| Path | Before (this afternoon / Claude pending) | After (16:31 ET live) |
|---|---|---|
| `~/.hermes/config.yaml` `mcp_servers` | duplicate-key hang; last-key-wins left **mempalace enabled** (gbrain/cloudflare dropped). Later a worker commented **all** MCP. | **one** block. `yaml.safe_load` keys: `gbrain`, `cloudflare_docs`, `cloudflare`, `cloudflare_bindings`, `cloudflare_builds`, `cloudflare_observability`. **No mempalace.** gbrain+cloudflare kept. |
| `~/.hermes/config.yaml` `moa.enabled` | `true` (grok-4.6 + opus aggregator) | **`false`**. Default model is oq4e; MOA would fan out on desktop `hi`. Prime profile has no `config.yaml` (not edited). |
| `~/.hermes/config.yaml` `model.max_tokens` | 131072 | **4096** |
| `~/.hermes/profiles/qwen38-oq4e-short/config.yaml` | MOA on; max_tokens 65536; 20 cli toolsets; mcp `{}` | MOA **off**; grok ref **disabled**; max_tokens **2048**; context **65536** (Hermes 64k floor — did not try 16384); `reasoning_effort: none`; thinking_budget 256; `platform_toolsets.cli` **and** `api_server`: `[file, terminal, todo]`; mcp `{}` |
| `.../qwen38-oq4e-mid/config.yaml` | MOA on; max_tokens 131072 | MOA **off**; grok ref **disabled**; max_tokens **4096**; context **131072**; same lean toolsets |
| `.../qwen38-oq4e-full/config.yaml` | MOA on; max_tokens 262144 | MOA **off**; grok ref **disabled**; max_tokens **8192**; context **262144**; same lean toolsets |
| Hermes.app `Info.plist` `LSEnvironment` | `MallocNanoZone=0` only (code default `HERMES_DESKTOP_POOL_MAX` **3**) | **`HERMES_DESKTOP_POOL_MAX=12`**. Real knob: `apps/desktop/electron/main.ts` `POOL_MAX_BACKENDS`. **Needs Hermes.app relaunch to take effect.** `launchctl setenv` also 12. |

Backups this pass: `~/.hermes/config.yaml.backup-20260826-161754-stack-desktop`, per-profile `config.yaml.backup-20260826-161754`. Other workers: `config.yaml.backup-20260826-161640-oq4e-desktop`, `...-163000-oq4e-desktop-restored`.

16:29 ET: default `config.yaml` was briefly truncated to 0 bytes during an enable-flag edit (other worker); restored. File parses.

Not changed: omlx 0.6.2, LaunchAgent `com.mike.omlx-server`, idle_timeout, 8bit checkpoint (registered, **unloaded**), turboquant_kv, caches, brew.

gbrain: not restarted by this worker. Live at 16:31 as child of `hermes --profile local serve` (watchdog + `bun gbrain serve`). Default-profile gbrain pid from 15:31 was gone by 16:31 (desktop respawned backends ~16:24).

## 2. prompt-size before/after

`hermes --profile qwen38-oq4e-short prompt-size --json` (offline). Desktop gateway uses `api_server` toolsets; measured both.

| | system chars | skills index chars | tools count | tools JSON bytes | approx fixed tokens (chars/4) |
|---|---|---|---|---|---|
| **before** (20 cli toolsets) | 36090 | 14673 | 24 | 59968 | ~24k |
| **after cli** | 17178 | 0 | 7 | 13767 | ~7.7k |
| **after api_server** (desktop-equivalent) | 16947 | 0 | 7 | 13767 | ~7.7k |

Default (fat cloud toolset, comparison): system 45690, skills 24512, tools 24 / 59914.

16:08 desktop `hi` on the fat path: omlx `Prefill interrupted at 8192/27006` — that is why oq4e profiles were shrunk (file+terminal+todo only). Skills toolset off → skills index 0.

Wired prompt tokens on a real `-z` (not `-t file`): **7648**.

## 3. DESKTOP_OK proof + desktop-equivalent turn

### A. `DESKTOP_OK` (this worker) — NOT `-t file`

```
/Users/man/.local/bin/hermes --profile qwen38-oq4e-short --yolo --reasoning none -z "Reply with exactly: DESKTOP_OK"
```

- stdout **exactly** `DESKTOP_OK`
- **exit 0**
- wall **180.73s** (16:21:11–16:24:11 ET)
- usage: in **7648**, out **80**, api_calls **1**, session `20260826_162111_ec1d6a`
- artifacts: `~/agent-reports/2026-08-26-oq4e-desktop-usable/desktop-ok.*`

omlx `~/.omlx/logs/server.log` (and launchd log, same lines):

```
2026-08-26 16:20:08,063 - omlx.scheduler - INFO - [-] - Prefill interrupted at 4096/7648 tokens: 1 request(s) aborted
2026-08-26 16:24:11,688 - omlx.server - INFO - [-] - Chat completion: model=Jundot--Qwen3.8-27B-oQ4e-mtp, 80 tokens in 179.46s (1.4 tok/s), prompt: 7648, finish_reason=stop, max_tokens=2048, request_max_tokens=2048
```

16:20 abort = Mac disconnect mid-prefill (same 7648 prompt), **not** a model fail. Successful completion is the **80-token / 179.46s** line. Implied cold prefill ~170s → **~45 tok/s**; gen ~10 tok/s once prefill done. max_tokens **2048** (cannot soak 131k/262k).

A sibling `-z` queued behind it (other worker) finished 16:26:36: `33 tokens in 317.16s, prompt: 7648`. That is **not** this DESKTOP_OK (this one exited 16:24:11 with 80 output tokens).

### B. Desktop-equivalent `hello` (warm prefix cache)

```
/Users/man/.local/bin/hermes --profile qwen38-oq4e-short --yolo --reasoning none -z "Say only: hello. Do not call tools."
```

- stdout `hello`
- **exit 0**
- wall **33.46s** (16:30:34–16:31:08 ET)
- usage: in **1506** + cache_read **6144** = 7650, out **36**, api_calls **1**

```
2026-08-26 16:31:08,197 - omlx.server - INFO - [-] - Chat completion: model=Jundot--Qwen3.8-27B-oQ4e-mtp, 36 tokens in 31.76s (5.8 tok/s), prompt: 7650, finish_reason=stop, max_tokens=2048, request_max_tokens=2048
```

A plain `hi` first (16:24:33) **did** first-token: `206 tokens in 173.69s, prompt: 7641, finish_reason=tool_calls`, then tool follow-up started `re-prefills 10247 of 16391` and was SIGTERM’d (EXIT 143) at 16:29:09 — aborted, not a soak. Retry used an explicit no-tools instruction so the turn could complete.

## 4. LRU cap 3

Real knob. `desktop.log`:

```
2026-08-26T19:10:29.268Z Evicting idle profile backend "qwen38-oq4e-short" (LRU cap 3)
2026-08-26T20:15:20.283Z Evicting idle profile backend "qwen38-oq4e-full" (LRU cap 3)
```

Code: `POOL_MAX_BACKENDS = Math.max(1, Number(process.env.HERMES_DESKTOP_POOL_MAX) || 3)` plus 90s keepalive (fresh backends are not evicted, so the pool can exceed 3 while tabs are open). plist now 12; **running Hermes.app still has 3 until relaunch**.

## 5. Leftover

- **Hermes.app must be relaunched** for `HERMES_DESKTOP_POOL_MAX=12`. Until then LRU cap 3 is live.
- **Cold 7648-token prefill ~3 min** vs a ~60s desktop WS orphan reap. CLI `-z` waited and passed. A **fresh** desktop `hi` on this profile can still get `interrupted_during_api_call` until prefix cache is warm. Warm hello was 32s.
- **Default toolset still fat.** oq4e-on-**default** desktop chat is still 24 tools / ~27k prompt. Use profile **`qwen38-oq4e-short`**.
- **Default `hermes serve` pid 19647** (15:31) was not recycled — in-memory MCP on that process may still be the 16:08 snapshot. New spawns read YAML (no mempalace).
- **Default max_tokens 4096 + MOA off** also caps/disables cloud-on-default if Mike switches the default model without raising them. Prime untouched (no profile config.yaml).
- **gbrain lock-contention** unchanged (not restarted).
- **8bit** still listed as alias `qwen3.8`, not loaded. One resident model: `Jundot--Qwen3.8-27B-oQ4e-mtp` 16.60GB.
- **144k/262k marker** still unproven. Not retried (first-token desktop now works; slot not re-eaten).
- PATH: a fresh non-login shell does not see `hermes` (`~/.local/bin/hermes`). Desktop/login shells do.

## 6. How verified

```
python3 -c "import yaml; print(list(yaml.safe_load(open('/Users/man/.hermes/config.yaml'))['mcp_servers']))"
# no mempalace; gbrain+cloudflare_* present
hermes --profile qwen38-oq4e-short prompt-size --json --platform cli
hermes --profile qwen38-oq4e-short prompt-size --json --platform api_server
/Users/man/.local/bin/hermes --profile qwen38-oq4e-short --yolo --reasoning none -z "Reply with exactly: DESKTOP_OK"
/Users/man/.local/bin/hermes --profile qwen38-oq4e-short --yolo --reasoning none -z "Say only: hello. Do not call tools."
curl -sS http://127.0.0.1:8300/api/status
# 0.6.2, loaded ['Jundot--Qwen3.8-27B-oQ4e-mtp'], 16.60GB, models_loaded=1
```

Live at 16:31 ET: omlx 0.6.2, oQ4e ~16.60GB, 8bit unloaded, 127.0.0.1:8300, active_requests 0.
