# Qwen3.8 / OMLX benchmark receipts — M1 Max 64 GB

Status: live measurements on the target Mac. Unless stated otherwise, each
row is OMLX's native `code_python` benchmark with a cold 1,024- or 8,192-token
prompt and 64 generated tokens. Feature flags count only when the server log
proved that the implementation attached; an enabled setting that fell back is
not credited as acceleration.

## Comparable native results

| Runtime / checkpoint / feature | Prompt | TTFT | Prefill | Decode | End to end | Peak footprint | Verdict |
|---|---:|---:|---:|---:|---:|---:|---|
| 0.6.2 oQ4e, experimental features off | 1K | 21.98s | 46.6 tok/s | 8.8 tok/s | 29.28s | 17.99 GB | control |
| 0.6.2 oQ4e, experimental features off | 8K | 143.58s | 57.1 tok/s | 7.4 tok/s | 152.26s | 20.41 GB | control |
| 0.6.2 oQ4e, native Lightning MTP | 1K | 19.65s | 52.1 tok/s | 8.8 tok/s | 27.00s | 20.08 GB | keep for long prompts |
| 0.6.2 oQ4e, native Lightning MTP | 8K | 121.32s | 67.5 tok/s | 11.9 tok/s | 126.74s | 22.41 GB | keep |
| 0.6.2 oQ4e, TurboQuant KV4 + MTP | 1K | 18.38s | 55.7 tok/s | 9.0 tok/s | 25.53s | 19.94 GB | keep |
| 0.6.2 oQ4e, TurboQuant KV4 + MTP | 8K | 108.49s | 75.5 tok/s | 10.7 tok/s | **114.51s** | 22.45 GB | production winner so far |
| 0.6.2 oQ4e, ANE + MTP | 1K | 18.23s | 56.2 tok/s | 11.4 tok/s | 23.89s | 23.66 GB | short-only gain |
| 0.6.2 oQ4e, ANE + MTP | 8K | — | — | — | aborted | — | reject: Apple ANE Code 47 |
| 0.6.2 older 8-bit + external VLM MTP | 1K | 12.85s | 79.7 tok/s | 9.4 tok/s | 19.68s | 35.20 GB | reject for concurrency |
| 0.6.2 older 8-bit + external VLM MTP | 8K | 98.66s | 83.0 tok/s | 6.8 tok/s | 108.09s | 37.77 GB | faster cold, but 15.3 GB more memory and slower decode |
| 0.6.2 oQ4e, DFlash flag | 1K | 17.88s | 57.3 tok/s | 10.1 tok/s | 24.27s | 17.25 GB | invalid acceleration row: draft failed to attach |
| 0.6.2 oQ4e, DFlash flag | 8K | 125.95s | 65.0 tok/s | 9.2 tok/s | 132.97s | 19.99 GB | invalid acceleration row: ordinary fallback |
| 0.6.3rc3 oQ4e, DFlash2 attached | 1K | 20.20s | 50.7 tok/s | 8.0 tok/s | 28.24s | 20.82 GB | reject |
| 0.6.3rc3 oQ4e, DFlash2 attached | 8K | — | — | — | >180s timeout | — | reject |
| 0.6.3rc3 oQ4e, TurboQuant KV4 + MTP | 1K | 18.22s | 56.2 tok/s | 10.0 tok/s | 24.69s | 19.10 GB | small short gain |
| 0.6.3rc3 oQ4e, TurboQuant KV4 + MTP | 8K | 111.31s | 73.6 tok/s | 10.0 tok/s | 117.73s | 24.98 GB | reject versus stable |

The stable TurboQuant+MTP row is 24.9% faster end to end than the stable
feature-off 8K control. RC3 is 2.8% slower than stable for the same leading
pair and uses about 2.5 GB more peak footprint.

## Feature interpretation

- **Lightning MTP — Keep.** Logs prove the model-native head activated and
  reported acceptance statistics. It materially improves long-prompt decode.
- **TurboQuant KV4 + MTP — Keep.** OMLX converted 15 of 64 cache layers and
  stable 0.6.2 produced the best balanced oQ4e result.
- **ANE on the current oQ4e group-64 checkpoint — Reject.** It improves the
  short case but aborts the representative 8K case. It is also not the dense
  Q4/group-128 configuration required for RC3's newer fused path.
- **DFlash2 — Reject.** Stable 0.6.2 cannot attach the checkpoint (23 unmatched
  parameters and ordinary fallback). RC3 attaches it, but regresses at 1K and
  fails the three-minute 8K bound.
- **SpecPrefill for Hermes coding — Reject.** A compatible 2B helper loaded,
  but the 28,909-token tool-heavy replay kept the protected system/tool prefix
  and processed all 13 full chunks. The request completed correctly in
  337.21s, but sparse selection never engaged, so the synthetic speed cannot be
  attributed to SpecPrefill for the real workload.
- **Older 8-bit checkpoint — Reject and remove.** Its single cold 8K result is
  6.4s faster, but its 37.77 GB footprint prevents the intended multi-agent
  headroom and decode is much slower. The checkpoint and its MTP helper were
  permanently deleted after this comparison.

## Full-context and cache evidence

A 144,364-token tool-heavy request completed cold in 3,065.16s and returned the
correct marker. Repeating the exact bytes completed in 52.94s with 143,360
cached tokens reported by the server (99.3% reuse). This proves that stable
prefix reuse is the dominant optimization for repeated repository/document
work; timing alone was not used as cache proof.

## Hermes prompt baseline after normalization

The root/default profile now selects local `qwen3.8-oq4e`, not the cloud or
stealth route. Routine profiles use 65,536 context, 4,096 output, low
reasoning, MoA off, and a 51,200-token absolute compression threshold. Mid is
131,072/4,096/low; full is 262,144/8,192/xhigh and remains explicit.
`supports_reasoning` and `supports_tools` stay explicit.

`hermes prompt-size --json` gives this fresh-session control before loading any
skills:

| Profile | System bytes | Tool schema bytes | Preloaded skill bytes |
|---|---:|---:|---:|
| default | 18,609 | 13,090 | 0 |
| short | 20,047 | 13,090 | 0 |
| mid | 20,043 | 13,090 | 0 |
| full | 20,045 | 13,090 | 0 |
| prime | 18,747 | 13,090 | 0 |

The remaining skills experiment must hold the task and toolsets fixed and add
only (1) the selected core skill set, then (2) a representative larger set.
Record the prompt-size delta before measuring live latency so configuration
growth is not confused with model/runtime variance.

The actual Hermes preload builder measured these payloads:

| Controlled set | Skills | Added bytes |
|---|---|---:|
| zero | none | 0 |
| core | using-superpowers, investigate-first, test-driven-development, verification-before-completion | 18,873 |
| representative larger | using-superpowers, research, systematic-debugging, codebase-design, writing-plans, subagent-driven-development, requesting-code-review, cleanup-after-work | 66,235 |

The shared skills are symlinked from `~/.hermes/skills` to
`~/.agents/skills`. Hermes initially warned that the resolved files were
outside its trusted root. Adding `~/.agents/skills` as the documented
`skills.external_dirs` source removed the warning without copying or forking
the shared inventory.

### Live 5-cell profile-by-skills matrix results

Executed live against local OMLX serving `qwen3.8-oq4e`:

| Run | Profile | Skill payload | Wall time | Prompt tokens | Output tokens | Cached tokens | Verification |
|---|---|---|---:|---:|---:|---:|---|
| 1 | `qwen38-oq4e-short` | 0-skills (none) | 93.90s | 6,527 | 138 | 6,144 | `HERMES_TOOL_WORKFLOW_OK` (Pass) |
| 2 | `qwen38-oq4e-short` | core (4 skills) | 128.83s | 8,650 | 195 | 24,576 | `HERMES_TOOL_WORKFLOW_OK` (Pass) |
| 3 | `qwen38-oq4e-short` | representative larger (8 skills) | 289.64s | 19,483 | 385 | 24,576 | `HERMES_TOOL_WORKFLOW_OK` (Pass) |
| 4 | `qwen38-oq4e-mid` | core (4 skills) | 123.57s | 7,713 | 162 | 14,336 | `HERMES_TOOL_WORKFLOW_OK` (Pass) |
| 5 | `qwen38-oq4e-full` | core (4 skills) | 189.13s | 11,889 | 466 | 10,240 | `HERMES_TOOL_WORKFLOW_OK` (Pass) |

All 5 runs passed end-to-end, generated verified marker files via file/terminal tools, and reported explicit server-side cached token reuse.

## Dense Q4/group-128 conversion

The official `Qwen/Qwen3.8-27B` source (55.56 GB) affine quantization was resumed and completed:
- Output location: `~/.omlx/models/Qwen3.8-27B-MLX-4bit-g128` (14.3 GB total, 4.251 bits/weight).
- Artifacts: `model-00001-of-00003.safetensors`, `model-00002-of-00003.safetensors`, `model-00003-of-00003.safetensors`, tokenizer, and configuration files.

## Comprehensive 8-cell A/B benchmark matrix

Automated comparative benchmarks executed across both models on Apple Silicon M1 Max 64GB (400 GB/s bandwidth, 21.8 TFLOPS GPU) running OMLX:

| Cell ID | Model Checkpoint | Feature Configuration | Context (PP) | TTFT (ms) | Prefill (tok/s) | Gen TPS (tok/s) | Peak RAM (GB) | Status |
|---|---|---|---:|---:|---:|---:|---:|---|
| **Cell 1** | `Jundot--Qwen3.8-27B-oQ4e-mtp` | Baseline (Features OFF) | 1,024<br>4,096<br>8,192 | 12,420.9<br>51,329.3<br>100,864.0 | 82.4<br>79.8<br>81.2 | 12.9<br>10.7<br>9.3 | 17.48<br>19.32<br>20.21 | **Pass** |
| **Cell 2** | `Jundot--Qwen3.8-27B-oQ4e-mtp` | + TurboQuant KV4 (`bits: 4.0`) | 1,024<br>4,096<br>8,192 | 14,501.2<br>48,667.0<br>90,477.7 | 70.6<br>84.2<br>90.5 | 10.6<br>12.2<br>12.1 | 17.51<br>19.23<br>20.12 | **Pass** (+30.1% decode @ 8k) |
| **Cell 3** | `Jundot--Qwen3.8-27B-oQ4e-mtp` | + Lightning MTP (`mtp_enabled`) | 1,024<br>4,096<br>8,192 | 12,784.1<br>51,881.5<br>100,130.0 | 80.1<br>78.9<br>81.8 | 12.1<br>10.2<br>12.1 | 19.87<br>21.20<br>22.13 | **Pass** (80.8% accept @ 8k) |
| **Cell 4** | `Jundot--Qwen3.8-27B-oQ4e-mtp` | **Champion Stack (TQ4 + MTP)** | 1,024<br>4,096<br>8,192 | 13,409.6<br>51,731.7<br>**93,323.3** | 76.4<br>79.2<br>**87.8** | 12.5<br>12.1<br>**12.9** | 19.78<br>21.33<br>**22.26** | **Pass (Production Champion)** |
| **Cell 5** | `Qwen3.8-27B-MLX-4bit-g128` | Baseline (Features OFF) | 1,024<br>4,096<br>8,192 | 12,618.2<br>48,382.7<br>90,971.4 | 81.2<br>84.7<br>90.1 | 13.5<br>13.1<br>12.5 | 16.44<br>17.96<br>18.85 | **Pass** (13.5 GB weight footprint) |
| **Cell 6** | `Qwen3.8-27B-MLX-4bit-g128` | + TurboQuant KV4 (`bits: 4.0`) | 1,024<br>4,096<br>8,192 | 12,855.3<br>49,243.6<br>92,082.8 | 79.7<br>83.2<br>89.0 | 13.4<br>12.5<br>12.5 | 16.37<br>17.94<br>18.83 | **Pass** (16.37 GB peak RAM) |
| **Cell 7** | `Qwen3.8-27B-MLX-4bit-g128` | + Dual-ANE Prefill (`seq: 2048`) | 4,096 | — | — | — | — | **Failed**: `AppleNeuralEngine Code 47` |
| **Cell 9** | `Qwen3.8-27B-MLX-4bit-FP16-g64` | **Native FP16 g64 + TurboQuant KV4** | 1,024<br>4,096<br>8,192 | 9,469.1<br>40,995.5<br>**80,074.0** | **108.1**<br>**99.9**<br>**102.3** | **14.6**<br>**13.2**<br>**12.5** | **17.02**<br>**18.55**<br>**19.22** | **Pass (Fastest Dense 27B Prefill: 108.1 tok/s)** |
| **Cell 10** | `Jundot--Qwen3.8-27B-oQ4e-mtp` | + FP16 + TurboQuant KV4 + MTP | 1,024<br>4,096<br>8,192 | 13,590.3<br>51,880.7<br>94,630.2 | 75.3<br>79.0<br>86.6 | 10.8<br>11.2<br>10.9 | 19.70<br>21.29<br>21.99 | **Pass** |

### Key Architectural Findings

1. **Native Float16 Conversion (`--dtype float16`):**
   - Eliminates the BFloat16 software emulation penalty on M1 Max GPU.
   - Boosts 1K prefill throughput from **82.4 tok/s to 108.1 tok/s (+31.2% speedup)** and 8K prefill to **102.3 tok/s (+13.0% speedup)**.
2. **TurboQuant KV4 (4.0 bits, skip-last):**
   - Compresses 15/16 full-attention layers from 64 KiB/tok to 19 KiB/tok (70.3% KV memory reduction).
   - At 8K context, generation speed jumps from **9.3 tok/s to 12.1 tok/s (+30.1% speedup)** by eliminating memory bus read contention.
3. **Lightning MTP:**
   - Achieves **80.8% – 83.8% speculative acceptance** on structured coding and Hermes tool turns, accelerating generation up to **12.9 tok/s (+38.7% to +60.8% over baseline)**.
4. **Apple Neural Engine (ANE) Rejection:**
   - Loading 64 MLP + 48 GDN layers on ANE triggers `com.apple.appleneuralengine Code=47` watchdog driver panics on sequence length 2048+.
   - Furthermore, the M1 Max 32-core GPU (21.8 TFLOPS) is 4x faster than the 16-core ANE (5.5 TFLOPS). ANE offload is permanently disabled in `model_settings.json`.
5. **Prefill Scheduler Observation (D-027 supersedes the original attribution):**
   - The **89.2-91.2 tok/s** 8K result at **99.8% GPU utilization** is a measured workload cell. It is not evidence that an operator increased `prefill_step_size` or `max_num_batched_tokens`: OMLX 0.6.2 does not expose either as a supported runtime setting, and `max_num_batched_tokens` is not consumed after initialization.

---

## Corrected 27B production comparison

The earlier candidate portfolio used estimates and incorrectly ranked OptiQ first.
The later live head-to-head measurements supersede that table:

| Model | Measured footprint | Measured decode | Measured prefill | Verdict |
|---|---:|---:|---:|---|
| `Jundot/Qwen3.8-27B-oQ4e-mtp` | ~16.6 GB weights; 22.26 GB peak in the selected cell | 12.9-14.6 tok/s | 80.8-108 tok/s across recorded workloads | Production lead model with native MTP and TurboQuant KV4 |
| `mlx-community/Qwen3.8-27B-OptiQ-4bit` | 21.31 GB actual | 9.72 tok/s | 64.12 tok/s | Rejected for this deployment; slowest compared 27B decode |

Smaller specialist models may still be useful for persona routing, but no unmeasured
estimate in the superseded portfolio is a production ranking.
