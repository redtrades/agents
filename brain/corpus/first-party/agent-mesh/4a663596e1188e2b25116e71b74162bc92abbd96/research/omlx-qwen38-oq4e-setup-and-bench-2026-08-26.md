# omlx + Hermes qwen3.8-oq4e — remaining gaps closed + benches

Agent-stack worker pass, 2026-08-26 ~15:35–15:50 ET. Did **not** redo Coder's
installer/0.6.3rc3 rollback. Did **not** restart launchd. Did **not** upgrade
omlx. Did **not** run a 262k soak.

Machine: m64, M1 Max 64GB, omlx **0.6.2**, LaunchAgent `com.mike.omlx-server`
pid 96900, `127.0.0.1:8300`, `--memory-guard-gb 59`.

## 1. What actually changed

### Hermes profiles — `max_tokens` vs context tiers

All three profiles had `model.max_tokens: 131072` regardless of tier.

| profile | before max_tokens | after max_tokens | context_length (model + providers.omlx.models.qwen3.8-oq4e) |
|---|---|---|---|
| `qwen38-oq4e-short` | 131072 | **65536** | 65536 (provider already 65536; added `model.context_length`) |
| `qwen38-oq4e-mid` | 131072 | **131072** (unchanged) | 131072 |
| `qwen38-oq4e-full` | 131072 | **262144** | 262144 (provider already 262144; added `model.context_length`) |

Paths: `~/.hermes/profiles/qwen38-oq4e-{short,mid,full}/config.yaml`
Backups: `config.yaml.bak-20260826-maxtokens-20260826-153843` next to each.

`hermes config set` rewrote those YAML files (comments dropped; values +
`mcp_servers: {}` + compression ratios preserved:
short 51200 / mid 102400 / full 204800 at threshold 0.78125).

### Default Hermes — mempalace hang came back

`~/.hermes/config.yaml` `mcp_servers` had `mempalace` (`enabled: true`,
stdio `~/tools/mempalace/.venv/bin/mempalace-mcp`) **in addition to**
gbrain + cloudflare_*. Profiles already had `mcp_servers: {}`.

**After:** `hermes config unset mcp_servers.mempalace`.
Now: gbrain, cloudflare_docs, cloudflare, cloudflare_bindings,
cloudflare_builds, cloudflare_observability. No mempalace key.
Backup: `~/.hermes/config.yaml.bak-20260826-mempalace-remove-20260826-153843`.

Left unchanged (already correct): `model.default` / `providers.omlx.default_model`
= `qwen3.8-oq4e`; provider `omlx` @ `:8300`.

### OpenCode

`~/.config/opencode/opencode.json` already listed `qwen3.8-oq4e` under
`provider.omlx-local.models` (Coder, backup `opencode.json.backup-20260826-152834`
only had `qwen3.8`). Additive: `limit.context: 262144` on that model entry.
Did not set a sticky default model (UI still picks).

### Not changed (already matching live state)

- omlx 0.6.2, plist `--memory-guard-gb 59`, settings `memory_guard_tier=custom`
  ceiling 59.0, idle_timeout 3600.
- `Jundot--Qwen3.8-27B-oQ4e-mtp` `is_default: true`; 8bit `is_default: false`.
- No model has `turboquant_kv_enabled` and `vlm_mtp_enabled` both true.
  8bit: vlm_mtp=true, turboquant=false. oq4e: both false (native `mtp_compat=true`
  but `mtp_enabled=false` — left alone, working completions did not need it).
- oq4e `settings.max_context_window` is null; live `model_context_length=262144`
  (`/v1/models` `max_model_len=262144`). Coder already prefilling past 32k, so
  null means native, not the global 32768. Not patched.
- LaunchAgent not touched. No brew services. No cache deletes. No 0.6.3rc3.

### TASK-0004

Does not exist under `agent-workspace/tasks/` (only TASK-0001..0003). Coder work
lived in the Claude session `90ae7fb9-…` + profiles + the preflight snapshot.

## 2. Benchmark numbers

No 262k soak. Unloaded 8bit **before** any large-ish work; never had both 27B
checkpoints resident during a long context run.

### 2a. Coder already did (cited, not rerun)

- oq4e short completion: **16 tokens, ~45s, no memory abort** (~15:31 ET).
- `hermes -z --provider omlx -m qwen3.8-oq4e` full default toolset: prefill
  through **28074** tokens, `LOCAL_OK`, exit 0 (on 0.6.2 after rc3 rollback).
- Same for 8bit `qwen3.8`. Grammar `json_schema` reverified on 0.6.2.
- 8bit small-prompt (earlier today, `LOCAL-LLM-OPTIMAL-CONFIG-20260826.md`):
  pong 4.4 / math 6.6 / para 7.5 tok/s (thinking on, contended).
  nothink walls 1.4–1.9s, 2–7 completion tokens.
- **Full-context soak: failed / unfinished.** `_tmp-longctx-response.json`
  (Coder): `prefill_memory_exceeded` — peak ~55.65GB vs dynamic ceiling 55.57GB
  with **current 46.29GB** (8bit almost certainly still resident). Second try
  ~56.85GB peak, current 47.36GB. Coder's later 144k prefill was still running
  at session end and is **not** on this process (uptime/request counters reset
  to a small-request server). Not rerun.

### 2b. oq4e vs 8bit, small prompts, 2026-08-26 15:40 ET

Direct `/v1/chat/completions`, temp=0, `enable_thinking=false` unless noted.
8bit confirmed not loaded before oq4e arm (`unload` → 400 "Model not loaded").
Switched by unloading oq4e then hitting 8bit (first 8bit call includes load).
Unloaded 8bit at the end.

| model | workload | wall | pt/ct | gen_tps (ct/wall) | mem (status / pressure) | abort |
|---|---|---|---|---|---|---|
| qwen3.8-oq4e | verify PONG | 1.299s | 18/2 | 1.54 | 16.60GB / 18.5GB ok | no |
| qwen3.8-oq4e | pong nothink | 0.784s | 17/1 | 1.28 | 16.60GB / 18.7GB | no |
| qwen3.8-oq4e | math 17*23=391 | 0.929s | 28/3 | 3.23 | same | no |
| qwen3.8-oq4e | para ~2 sentences | **3.896s** | 20/57 | **14.63** | same | no |
| qwen3.8-oq4e | pong thinking-on | 2.717s | 57/21 | 7.73 | same | no |
| qwen3.8 (8bit) | pong nothink **cold+load** | 16.078s | 17/1 | n/a | 28.85GB / 34.0GB | no |
| qwen3.8 | math 391 | 1.034s | 28/3 | 2.90 | 28.85GB / 34.0GB | no |
| qwen3.8 | para | **6.536s** | 20/56 | **8.57** | 28.85GB / 34.1GB | no |
| qwen3.8 | pong thinking-on | 4.165s | 57/31 | 7.44 | same | no |

Fair gen comparison is **para** (enough completion tokens; prefill tiny):
oq4e **14.6 tok/s** vs 8bit **8.6 tok/s** (~1.7×). Weight footprint 16.60 vs
28.85 GB. oq4e load later measured `model_load_duration=5.91s`. 8bit first
pong 16s wall is load-dominated.

PhysMem during 8bit arm: 62G used / 1.1G unused (wired 37G). After 8bit unload:
28G used / 36G unused. Swap at verify: 2559M / 4096M used (not the 95% shape).

`gen_tps` here is completion_tokens/wall (includes prefill). Not MTP-adjusted;
oq4e native MTP is **off**.

### 2c. Hermes profiles short/mid/full

Offline `prompt-size --json` (fixed budget; all three still full toolsets):

| profile | model | system_bytes | tools | tools_bytes | skills_bytes |
|---|---|---|---|---|---|
| short/mid/full | qwen3.8-oq4e | ~36607 | 24 | ~59966 | 14691 |

Tiers do **not** shrink the Hermes fixed prompt; they cap the window.

Oneshot (mcp empty, `-t file` so not the 25-tool 28k default prompt):
`hermes --profile <p> -t file -z 'Reply with exactly: LOCAL_OK' --provider omlx -m qwen3.8-oq4e`

| profile | wall | input | cache_read | output | result |
|---|---|---|---|---|---|
| short | **78.49s** | 5986 | 0 | 19 | LOCAL_OK exit 0 |
| mid | **55.41s** | 3940 | 2048 | 35 | LOCAL_OK exit 0 |
| full | **112.56s** | 3938 | 2048 | 297 | LOCAL_OK exit 0 |

Full's 297 output tokens is why it is slower (thinking/verbosity), not the
256k cap — the prompt was ~4–6k. No mempalace hang. No memory abort.
Did **not** fill 65k/128k/256k.

## 3. Still open / HOLD remaining

- **agent-mesh embeddings HOLD stays HOLD.** Issue #7 still OPEN
  (`llama-server --embedding bge-m3 :8301`, D-010). Live check: omlx
  `POST /v1/embeddings` → 400 "not an embedding model". `llama-server` binary
  exists (`/opt/homebrew/bin/llama-server`); **no bge-m3 in HF cache**; port
  8301 not listening. Pass2 commit `76c3b5e` / `bc5d536` explicitly deferred
  this to avoid racing omlx/qwen3.8 work. Standing up a new LaunchAgent + GGUF
  download would be a **new** stack, not finishing a started sidecar. Mempalace
  (the planned consumer) was removed from default mcp because it hangs, so
  there is nothing live that needs embeddings today.
- **Native MTP on oq4e** (`mtp_compat=true`, `mtp_enabled=false`). Not flipped.
  Would need its own A/B vs current 14.6 tok/s para baseline.
- **No 256k / 128k / 65k filled-context KV measurement** on oq4e-only (Coder's
  attempts OOM'd with 8bit co-resident). Safe to try later with 8bit unloaded
  and a stepped length (32k → 65k → 128k), not a cold 262k.
- **Hermes `stealth/ox-alpha` vs gateway `openrouter/ox-alpha`** alias drift
  (see free-window snapshot).
- **TASK-0004** never filed.
- agent-workspace already dirty (unrelated `adws/…`, other knowledge files).
  This note is an add; **not committed**. agent-mesh clean, not mutated.
  agent-configs not touched.

## 4. How verified

```
curl -s http://127.0.0.1:8300/v1/models
# qwen3.8-oq4e, qwen3.8, mlx-community--Qwen3.8-27B-MTP-8bit; max_model_len 262144

# tiny completion after config changes (15:48 ET, some queue delay)
# wall 30.13s text PONG usage pt=18 ct=2 finish=stop  (earlier 15:40 verify was 1.299s)

launchctl print gui/$(id -u)/com.mike.omlx-server
# path=…/com.mike.omlx-server.plist  state=running  pid=96900

rg mempalace ~/.hermes/config.yaml          # no hits
rg is_default ~/.omlx/model_settings.json   # oq4e true, all others false
# turboquant_kv_enabled=false on every model; vlm_mtp_enabled=true only on 8bit
```

Post-bench `/api/status`: version 0.6.2, loaded
`Jundot--Qwen3.8-27B-oQ4e-mtp` 16.60GB / 59.00GB, default that model.
