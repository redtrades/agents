# omlx + Hermes ideal config for qwen3.8-oq4e — 2026-08-26

**Retarget (17:09 ET): long-context *agentic* coding** (TEST-PLAN §4 Hermes tool-loop, median ~19K / p75 ~29K, `file`/`terminal`/`todo`, prefix cache). Not magenta, not genetic, not desktop `hi`, not a generic first-token matrix.

**Hub / SDLC (Mike asked):** this oq4e/Hermes work is **not** on a hub-repo branch and has **no PR**. Applied knobs live only in `~/.hermes/config.yaml` and `~/.hermes/profiles/qwen38-oq4e-{short,mid,full}/`. Notes are **untracked** files on `agent-workspace` `main` (this file plus sibling `omlx-qwen38-oq4e-*.md`). `agent-configs` was not used for this. That is **not** proper SDLC; a follow-up should land the profile YAML + this note on an `agent-workspace` worktree/PR (one-worktree-per-issue).

**Slot (17:09 ET):** yielded. Another agent is on omlx (FCFS `active=1`). `govcon-factory/scripts/lease-acquire.sh` exists (`gpu-heavy` / `omlx-restart`); `origin/leases` is empty. Did **not** acquire over the other tester. No further `-z` until we hold a lease.

**Agentic target vs what the 16:35 sweep actually applied:** target is `qwen38-oq4e-mid` (128k) daily agentic default + `full` (256k) large-repo; short 65k triage only. The sweep below applied the first-token winner to **default + short** (`max_tokens` 2048, reasoning none, 3-tool). **mid was not patched** (row 4 lost because yaml `reasoning: high` rambled). Do not apply mid while the other tester holds the GPU. Cite `~/agent-reports/omlx-optimization/LOCAL-LLM-OPTIMAL-CONFIG-20260826.md` + `TEST-PLAN.md` §4.

The table below is the measurements already taken (SWEEP_OK rows). They are **not** the agentic 19K tool-loop proof. That proof is deferred until a lease.

---

Times America/New_York. Sweep occupied the omlx slot. Completions **one at a time** (FCFS). No `-t file` on counted rows except the labeled fat comparison (prompt-size only). Prior SHORT_OK/MID_OK `-t file` rows **do not count**. Desktop LRU still respawns extra profile `serve`s (saw default/short/mid/full/scout/sentinel/morning-brief/coach/local/hermes-* at once while `HERMES_DESKTOP_POOL_MAX=3`); not fought.

omlx **0.6.2** (launchd `com.mike.omlx-server`, 127.0.0.1:8300, memory_guard 59GB). Hermes **v0.20.5**. MCP disabled (no mempalace; gbrain/cloudflare `enabled: false`). MOA off. No brew restart. No 0.6.3rc3. No turboquant_kv. No ANE qwen35_prefill flip. No HF/omlx cache delete. No agent-configs commit.

## Winner (applied)

| Knob | Value | Paths |
|---|---|---|
| model | `qwen3.8-oq4e` / `Jundot--Qwen3.8-27B-oQ4e-mtp` | omlx default; Hermes default + short |
| toolset | `file`, `terminal`, `todo` on **cli and api_server** | `~/.hermes/config.yaml` `platform_toolsets`; `~/.hermes/profiles/qwen38-oq4e-short/config.yaml` |
| max_tokens | **2048** | default + short `model.max_tokens` |
| reasoning | **none** | default + short `agent.reasoning_effort` |
| thinking_budget | **256** | default + short |
| context | **65536** (Hermes 64k floor) | default `model.context_length` + omlx provider model; short already 65536 |
| compression | 0.78125 scaled: **threshold_tokens 51200** at 65k | default rescaled with context; short already 51200. **Not** an experimental flip. |
| 8bit | **unloaded** | only oq4e resident |

Backups: `~/.hermes/config.yaml.backup-20260826-170341-ideal-sweep`, `~/.hermes/profiles/qwen38-oq4e-short/config.yaml.backup-20260826-170341-ideal-sweep`. Mid **not** patched (did not win). Full not patched.

### Why this beat the other rows

- **Toolset file+terminal+todo** vs file-only: file-only cuts ~1.7k prompt tokens (7677→5987) and ~10s wall, but drops terminal/todo. Slim 7-tool set already killed the 24/33-tool ~28k desktop abort path. Keep the three-tool agent set.
- **Fat 24/33-tool**: prompt-size ~33 tools / 62.5k tool JSON + 14.7k skills index. Prior desktop `hi` aborted `8192/27006`. No live fat completion this sweep (labeled).
- **max_tokens 2048**: fastest clean stop (20 tok / 23.69s / 13.0 tok/s). **512 length-stopped** (512 tok then a retry). 4096/8192 invited extra ramble (36–248 tok) with no first-token win.
- **reasoning none**: yaml `high` (default 1a, mid 4) dumped 191–226 tokens for `SWEEP_OK`. CLI `--reasoning high` on yaml-none was a no-op (21 tok). Keep yaml **none**.
- **oq4e vs 8bit**: 8bit 28.85GB weights / 34.4GB pressure, **51 tok in 134.28s (5.2 tok/s)** cold 7643 prompt. oq4e 16.60GB, warm 13 tok/s, cold desktop-class ~50s at 7.6k. 8bit stays unloaded.
- **short 65k vs mid 128k**: same ~7648 prompt. Mid yaml had been mutated to reasoning high → 191 tok / 71.76s. No extra free-memory reason to prefer 128k for this prompt. **Skip 144k/262k** (below).

## KV math for skipped 144k/262k

Given 64 KiB/token over 16 attn layers + 16.6GB weights, reading 64 KiB/**token total** (not per layer; per-layer would be ~1 MiB/token and 65k would not fit the 59GB guard, but 65k runs at ~21GB):

| ctx | KV | + weights 16.6GB | free under 59GB |
|---|---|---|---|
| 65,536 | 4.0 GB | 20.6 GB | 38.4 GB |
| 131,072 | 8.0 GB | 24.6 GB | 34.4 GB |
| 262,144 | 16.0 GB | 32.6 GB | **26.4 GB ≥ 20** |

Headroom exists, but **first-token is not already good** (7.6k still 24–50s; 27k historically aborted mid-prefill). Skip 144k/262k.

Compression: no measured row was near 0.78125 of the window (7.6k << 51,200). Left the scaled 0.78125 formula in place.

## Table — every sweep row

Same user text unless noted: `Reply with exactly: SWEEP_OK`. `gen tok/s` is the omlx Chat completion overall rate (includes prefill). **TTFT** ≈ time until decode (poll on 1d; else `total_s − out/11` using ~11 tok/s decode). Peak GB is engine-pool pressure when sampled (weights-only 16.60GB oq4e / 28.85GB 8bit).

| Row | Profile / toolset | max_tokens | reasoning | prompt tok | prefill≈s | TTFT s | gen tok/s | peak GB | finish_reason | notes |
|---|---|---|---|---|---|---|---|---|---|---|
| 1a | **default** file/term/todo | 4096 | yaml **high** | 7612 | ~57 | ~57 | 8.4 | 21.2 | stop | 226 out; cache_read 4096; wall 79.3s. stdout `SWEEP_OK`. |
| 1b | **short file-only** (yaml then restored) | 4096 | none CLI | 5987 | ~33 | ~33 | 9.5 | 20.3 | stop | 72 out; ~1.7k smaller prompt; wall 41.4s. Restored 3-tool after. |
| 1c | **fat known_builtin** (labeled, no live) | — | — | ~28k est | — | — | — | — | n/a | prompt-size: 33 tools, 62540 JSON B, skills 14673 chars, system 32666. Prior abort 8192/27006. |
| 1d | **short as-is** file/term/todo | 4096 (yaml mutated then) | none CLI | 7677 | 48.6 | **48.6** (poll) | 11.9 | **25.3** | stop | 36 out / 50.30s. Counted first-token path. |
| 2a | short 3-tool | **512** | none | 7647 then 8206 | ~23 then ~24 | ~23 | 11.0 then 11.3 | n/s | **length** then stop | First call 512 tok length-stop (69.26s); hermes retried max 1024. Wall 99s. **Too low.** |
| 2b | short 3-tool | **2048** | none | 7647 | ~22 | ~22 | **13.0** | n/s | stop | **20 out / 23.69s.** Winner. |
| 2c | = 1d | 4096 | none | 7677 | 48.6 | 48.6 | 11.9 | 25.3 | stop | Same as 1d. Extra ramble vs 2048, no TTFT win. |
| 2d | short 3-tool | **8192** | none | 7647 | ~24 | ~24 | 10.4 | n/s | stop | 248 out / 47.05s. Did not soak 8192; still slower. |
| 2e | short 3-tool | 2048 | CLI **high** (yaml none) | 7647 | ~28 | ~28 | 11.0 | n/s | stop | 21 out / 29.48s; reasoning_tokens 0. CLI flag did not match yaml-high cost. |
| 3 | short 3-tool **8bit** `-m qwen3.8` | 2048 | none | 7643 | ~130 | ~130 | 5.2 | **34.4** (28.85 wts) | stop | 51 out / 134.28s; cache 0 (cold after load). Then 8bit unloaded. |
| 4 | **mid** 128k 3-tool | 4096 | yaml **high** (mutated) | 7649 | ~54 | ~54 | 10.2 | 20.9 | stop | 191 out / 71.76s. Same prompt size as short. Did not win. |
| 5 | compression 0.78125 | — | — | — | — | — | — | — | skip | 7.6k << 51,200. No measured win. Unchanged formula. |
| skip | 144k / 262k | — | — | — | — | — | — | — | skip | Free ≥20GB on paper; first-token not good. See KV math. |

omlx Chat lines (counted):

```
2026-08-26 16:45:29,879 Chat completion: model=Jundot--Qwen3.8-27B-oQ4e-mtp, 36 tokens in 50.30s (11.9 tok/s), prompt: 7677, finish_reason=stop, max_tokens=4096  # 1d
2026-08-26 16:47:12,900 ... 226 tokens in 77.46s (8.4 tok/s), prompt: 7612 ... max_tokens=4096  # 1a
2026-08-26 16:48:12,886 ... 72 tokens in 39.81s (9.5 tok/s), prompt: 5987 ... max_tokens=4096  # 1b
2026-08-26 16:49:10,360 ... 20 tokens in 23.69s (13.0 tok/s), prompt: 7647 ... max_tokens=2048  # 2b WINNER
2026-08-26 16:50:21,276 ... 512 tokens in 69.26s (11.0 tok/s), prompt: 7647, finish_reason=length, max_tokens=512  # 2a
2026-08-26 16:51:38,671 ... 248 tokens in 47.05s (10.4 tok/s), prompt: 7647 ... max_tokens=8192  # 2d
2026-08-26 16:52:22,634 ... 21 tokens in 29.48s (11.0 tok/s), prompt: 7647 ... max_tokens=2048  # 2e
2026-08-26 16:53:48,561 ... 191 tokens in 71.76s (10.2 tok/s), prompt: 7649 ... max_tokens=4096  # 4 mid
2026-08-26 16:57:07,612 Chat completion: model=mlx-community--Qwen3.8-27B-8bit, 51 tokens in 134.28s (5.2 tok/s), prompt: 7643 ... max_tokens=2048  # 3
```

## 8bit unload incident (leftover)

8bit load 21.4s, 28.85GB. After the row, unload queued (`scheduler work drains`) while `active_requests=0`. A blocking `/v1/.../unload` finally `Engine stopped`, then **teardown timed out at 60s** (`omlx.utils.fatal`) and the process exited. launchd KeepAlive respawned **0.6.2** (new pid). oq4e reloaded; 8bit not loaded. **Not** a brew restart.

## Desktop LRU

`HERMES_DESKTOP_POOL_MAX` stayed **3** (`launchctl getenv`). Hermes.app still respawns many `--profile … serve` backends (keepalive/tabs). Noted, not fought.

## How verified

```
hermes --version          # v0.20.5
curl -sS http://127.0.0.1:8300/api/status
# 0.6.2, loaded [Jundot--Qwen3.8-27B-oQ4e-mtp], 16.60GB, models_loaded=1
python3 -c "import yaml; d=yaml.safe_load(open('/Users/man/.hermes/config.yaml')); print(d['model'], d['agent'], d['platform_toolsets'], d['moa']['enabled'], {k:v.get('enabled') for k,v in d['mcp_servers'].items()})"
hermes prompt-size --json --platform cli
hermes prompt-size --json --platform api_server   # 7 tools after apply (was 21)
hermes --profile qwen38-oq4e-short -z "Reply with exactly: IDEAL_OK"   # no -t file
```
