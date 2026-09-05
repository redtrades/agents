# omlx + Hermes Qwen3.8-oQ4e profile verify — 2026-08-26

Closed the unfinished Claude session `90ae7fb9` (died at session limit ~14:55 ET while a 144k prefill was in flight). No parallel stack started; no repos cloned; omlx stayed on **0.6.2**. Slot is idle.

Times below are America/New_York.

## 1. Config (paths, before/after)

Live files re-read at 15:36 then again at 15:38–15:40. A concurrent writer (Hermes rewrite / other agent; stamp `config.yaml.bak-20260826-maxtokens-20260826-153843`) already closed the max_tokens gap and removed mempalace from the default config. This worker did **not** leave those production values changed.

| Path | Before (15:33 / session notes) | After (15:53, live) |
|---|---|---|
| `~/.hermes/config.yaml` `mcp_servers` | duplicate keys; YAML last-key-wins left **mempalace enabled** (gbrain/cloudflare dropped). Later merged into one block with mempalace still `enabled: true`. | **one** `mcp_servers` block. `yaml.safe_load` keys: `gbrain`, `cloudflare_docs`, `cloudflare`, `cloudflare_bindings`, `cloudflare_builds`, `cloudflare_observability`. **No mempalace.** Duplicate-key hang is gone. |
| `~/.hermes/config.yaml` model | `provider: omlx`, `default: qwen3.8-oq4e`, `max_tokens: 131072` | unchanged (default profile stays 131072) |
| `~/.hermes/profiles/qwen38-oq4e-short/config.yaml` | `model.max_tokens: 131072`, `providers.omlx.models.qwen3.8-oq4e.context_length: 65536`, `mcp_servers: {}` | `model.max_tokens: 65536`, `model.context_length: 65536`, same provider context, `mcp_servers: {}` |
| `.../qwen38-oq4e-mid/config.yaml` | `max_tokens: 131072`, context 131072, `mcp_servers: {}` | same (already matched 128k tier) |
| `.../qwen38-oq4e-full/config.yaml` | `max_tokens: 131072` vs context 262144 | `model.max_tokens: 262144`, `model.context_length: 262144`, `mcp_servers: {}` |
| `~/.omlx/model_settings.json` | oQ4e `is_default: true`; 8bit `is_default: false` (Coder ~15:29) | unchanged. 8bit still **registered** as alias `qwen3.8`, not default, not hidden, **not loaded**. |
| LaunchAgent `com.mike.omlx-server` | `--memory-guard-gb 59`; **no context flags** | unchanged. Env: `OMLX_QWEN35_Q8_MLP_MIN_TOKENS=256`, `OMLX_FA256_STEEL=0`. |

Backups taken this pass: `~/.hermes/config.yaml.backup-20260826-154054-stack-finish` and per-profile `config.yaml.backup-20260826-154054`. Earlier session backup `config.yaml.backup-20260826-142814` still holds the buggy duplicate-mcp state.

**Test-only patch (restored):** for `-z` smokes, `model.max_tokens` on short/mid was briefly set to 64 so Hermes could not request a 65k/128k generation soak, then restored to 65536 / 131072. Confirmed restored at 15:53.

**Not done (out of scope / keep diffs small):** hiding or deleting the 8bit checkpoint; enabling ANE `qwen35_prefill`; LaunchAgent context flags; 262k soak.

## 2. Three profile results

Resident model throughout: `Jundot--Qwen3.8-27B-oQ4e-mtp` alias `qwen3.8-oq4e`, **16.60GB** weights (actual ~15.91GB). Pressure 19–22GB, level `ok`. 8bit not loaded. omlx 0.6.2, guard 59GB.

Hermes `-z` used `--profile … -t file --provider omlx -m qwen3.8-oq4e` (lean file toolset ~6k tokens, not the 28–31k default toolset). Generation was capped at 64 tokens for the smokes.

| Profile | Context / compression | Hermes `-z` | omlx line | Memory | Marker | Verdict |
|---|---|---|---|---|---|---|
| **short** `qwen38-oq4e-short` | 65,536; thresh 0.78125 / 51,200. Floor: intended 16,384; Hermes refuses below 64k (tool schemas ~28–31k). | 15:49 ET. `SHORT_OK` present in stdout (model also narrated). exit 0, wall **140.57s** (3 API calls: 64-cap truncated a first reply, Hermes continued). usage: in 2175 + cache_read 4096, out 90. | `64 tokens in 52.23s (10.0 tok/s), prompt: 5986, finish=length`. Implied prefill ~46s → **~131 tok/s prefill**, **10.0 tok/s gen**. | 16.60GB | n/a | **PASS** |
| **mid** `qwen38-oq4e-mid` | 131,072; thresh 0.78125 / 102,400 | 15:50 ET. stdout exactly `MID_OK`. exit 0, wall **37.63s**. usage: in 1892 + cache_read 4096, out 33. | `33 tokens in 36.31s (11.6 tok/s), prompt: 5988, finish=stop`. Implied prefill ~33s (prefix cache) → **~180 tok/s prefill**, **11.6 tok/s gen**. | 16.60GB | n/a | **PASS** |
| **full** (bounded, not 262k) | 262,144; thresh 0.78125 / 204,800 | No Hermes `-z` on full (max_tokens 262144 would soak if the model rambling). Direct `/v1/chat/completions`, `max_tokens: 32`. | `14 tokens in 128.34s (0.1 tok/s wall), prompt: 11412, finish=stop`. Prefill-dominated: **~90 tok/s prefill**, 14 gen tokens. Server running avg after: prefill **64.1**, gen **7.3**. | model 16.60GB; pressure **19.5GB** ok | **`SECTION 4.2 CODE 8675309` exact** | **PASS (bounded 11.4k, not 144k/262k)** |

### 144k test from the dead session — not a pass

Request `29f60d61-3ac1-47c5-a79a-2f7af35f5127`, ~144,364 tokens, was **rejected by the prefill memory guard** at 14:55:57 ET:

`Prefill would require ~56.85 GB peak (current 47.36 GB + KV+SDPA 9.49 GB) but dynamic ceiling is 55.57 GB` (custom ceiling still pinned 59.00GB; dynamic ceiling lower). Saved body: scratchpad `longctx-response2.json` (error JSON). Claude task file claimed `HTTP:200 TIME:1118` — that is the error payload, not a generation. Marker at 144k is **unproven**. A prior admission with 8bit still resident was also rejected (~55.65GB). Isolated 144k was observed mid-prefill (47,104/144,364 at ~51 tok/s) then the session died; no completion log line exists.

KV formula from the dead session (unchanged, not re-measured at full window): 64 KiB/token at bf16 over 16 full-attention layers → short 4.0 GiB / mid 8.0 GiB / full 16.0 GiB at native window, plus 16.6GB weights. Full-window + 8bit resident (~29GB) does **not** fit the 59GB guard — admission reject, not idle-evict.

## 3. Leftover gaps

- **Kernels actually used?** `/api/status` `custom_kernels`: bonsai, glm_moe_dsa, minimax_m3, qwen35_prefill all `available: true`. On oQ4e: `qwen35_ane_prefill_enabled: false`. Logs: GDN Metal prefill patch **applied** on every load (`impl=blocked_seq, min_t=64`); Qwen quantized MLP/linear patch **applied** (`variant=8, q8_min_tokens=256` — LaunchAgent env). Explicit `No ANE prefill slices to release` on a 13:32 request. **ANE qwen35_prefill is available and not used.** GDN + Q8 MLP patches are loaded. Changed nothing (1534276d: check, don't flip).
- **LaunchAgent context flags:** still none. Only `--memory-guard-gb 59`. Model `max_model_len` 262144 comes from the checkpoint, not the plist.
- **agent-mesh HOLD (D-010):** embeddings stay on llama-server `--embedding` sidecar. Confirmed live 15:37:47: `POST /v1/embeddings → 400: Model 'Jundot--Qwen3.8-27B-oQ4e-mtp' is not an embedding model.`
- **max_tokens:** production profiles now match context tiers (65k/128k/256k). Default `~/.hermes/config.yaml` still 131072. Hermes `-z` with those production caps **will soak** if the model does not stop (saw mid generate toward 131072 at ~10 tok/s and full toward 262144). Killed those soaks. Profile `max_tokens` is a generation budget, not a safety timeout.
- **mempalace:** removed from live default mcp_servers; still installed at `~/tools/mempalace`. Do not re-enable — it hangs Hermes on MCP init. agent-mesh D-009 still names it as the semantic-store *target*.
- **8bit leftover:** default flag cleared 15:29. Still listed as `qwen3.8` / `mlx-community--Qwen3.8-27B-MTP-8bit`. Not loaded. One model resident.
- **MOA** still `enabled: true` on the three profiles (grok-4.6 + opus aggregator). These `-z` runs hit omlx (prompt sizes and `/api/status` match). MOA remains a contamination risk for “omlx-only” tests.
- **144k / native 262k attention:** skipped. Memory guard already refused 144k once today; Mike asked to free the slot; no unbounded 262k soak.

## 4. How verified

```
curl -sS http://127.0.0.1:8300/api/status          # 0.6.2, 1 model, 16.60GB, kernels available
curl -sS -X POST http://127.0.0.1:8300/admin/api/models/mlx-community--Qwen3.8-27B-8bit/unload
# → 400 Model not loaded
hermes --profile qwen38-oq4e-short -t file --reasoning none --yolo \
  --provider omlx -m qwen3.8-oq4e -z "Reply with exactly: SHORT_OK"
hermes --profile qwen38-oq4e-mid   -t file --reasoning none --yolo \
  --provider omlx -m qwen3.8-oq4e -z "Reply with exactly: MID_OK"
# marker: POST /v1/chat/completions max_tokens=32, ~11412 prompt tokens,
# needle SECTION 4.2 CODE 8675309 planted at start
python3 -c "import yaml; print(list(yaml.safe_load(open('/Users/man/.hermes/config.yaml'))['mcp_servers']))"
```

Key omlx log lines (`~/.omlx/logs/server.log`):

```
15:48:17 Chat completion: oQ4e-mtp, 64 tokens in 52.23s (10.0 tok/s), prompt: 5986, finish_reason=length
15:50:22 Chat completion: oQ4e-mtp, 33 tokens in 36.31s (11.6 tok/s), prompt: 5988, finish_reason=stop
15:52:35 Chat completion: oQ4e-mtp, 14 tokens in 128.34s, prompt: 11412, finish_reason=stop
14:55:57 Request 29f60d61 … rejected by prefill memory guard: ~56.85 GB peak
15:37:47 POST /v1/embeddings → 400 (not an embedding model)
```

Artifacts: `~/agent-reports/2026-08-26-qwen38-oq4e-profile-verify/` (`run.log`, `*-result.json`, `full-marker-result.json`, `summary.json`).

Soaks killed (not left running): other-agent `hermes --profile qwen38-oq4e-mid` generating under max_tokens 131072, and `…-full` under 262144. No soak at end. launchctl untouched. brew services untouched. turboquant_kv not enabled with vlm_mtp. HF/omlx caches not deleted. agent-configs not touched. No PR merge.
