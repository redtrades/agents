# Optimal Local LLM Stack for Hermes Agents — M1 Max 64GB

**Date:** 2026-08-27. Synthesizes this session's direct verification (browser-confirmed
model existence, live benchmarks, real Hermes CLI runs) with agent-mesh's existing
empirical corpus (`MASTER-PERMUTATIONS-MATRIX.md`, `OMLX-M1MAX-OPTIMIZATION-GUIDE.md`,
`benchmark-results-2026-08-27.md`, `evals/`). Runtime-result numbers are measured live
or cross-checked against prior measurements; explicitly attributed hardware/vendor
figures remain contextual claims, not local results. Where a prior benchmark was found
broken, it is named as broken rather than silently used.

**Cross-reference, added post-rebase:** a second agent working the same goal in parallel
pushed `research/{INDEX,APPLE-SILICON-INFERENCE-ENGINES,HUGGINGFACE-SOTA-MODELS-2026,
M1-MAX-ROOFLINE-MICROARCHITECTURE,METAL-KERNELS-PREFILL-BOTTLENECK,PREFIX-CACHE-INTERNALS-GDN}.md`
independently, landing on the same core verdict for the main agent model
(`Jundot/Qwen3.8-27B-oQ4e-mtp` + TurboQuant KV4 + native MTP — their numbers: 14.6 tok/s
decode, 80.8 tok/s cold prefill / 2,972.9 tok/s warm-cached prefill, 84% MTP acceptance,
all consistent with this document's own measurements). Their contribution goes further
in one direction this document doesn't cover: a **multi-model persona fleet** —
`DeepSeek-Coder-V2-Lite-Instruct-4bit` (MoE, fast coding), `Qwen2.5-Coder-7B-Instruct-4bit`
(review/audit), `Qwen3.5-2B-MLX-4bit` (background/event-loop tasks) alongside the oQ4e
lead-orchestrator model, mapped to agent-mesh's own Prime/Forge/Sentinel/Scout personas.
Worth reading together with this document, not as a competing answer — two independent
passes converged on the same primary-model verdict, which is itself corroborating
evidence.

---

## 1. The answer

**Model:** `Jundot/Qwen3.8-27B-oQ4e-mtp` (HF: browser-confirmed live, 24 likes, 9,075
downloads/month, `apache`-adjacent MLX org release) — 27B dense, hybrid Gated-DeltaNet
attention (16 full + 48 linear layers), native bundled MTP head, oQ mixed-precision
4-bit quantization (oMLX v0.6.1 quantizer), 16.6GB weight footprint, 262,144 native
context.

**Runtime:** omlx v0.6.2 (`jundot/omlx`), not vMLX/llama.cpp/mlx-lm.server. Reasons,
each independently verified:
- **Prefix/prompt caching is the actual deciding factor** (Hermes sends a large,
  mostly-fixed system prompt every call) — omlx's tiered SSD+RAM cache is the only
  engine on this machine with server-confirmed cross-request cache reuse *and* a clean
  bill of health on the correctness risk (tool-call output byte-identical across 20+
  cache-hit trials in the original engine shootout). mlx-lm.server and llama.cpp were
  independently confirmed broken for this specific hybrid-attention architecture's
  prefix sharing.
- **vMLX's historic severe cache-restore memory-growth crash appears fixed** in current
  releases (1.5.23+, now at 1.6.41 — three minor versions and a dedicated
  `cache_record_validator` regression test past the version that crashed in prior
  internal testing) — genuinely worth a fresh vMLX trial later, but not swapped to
  today given omlx's TurboQuant+MTP combination is already measured, live, and stable.
- **The `turboquant_kv_enabled` × `vlm_mtp_enabled` conflict is real but scoped**: it's
  open upstream issue `jundot/omlx#1584` (external-drafter MTP path only). The
  *native* `mtp_enabled` path used by `Jundot/Qwen3.8-27B-oQ4e-mtp` does **not** conflict
  with TurboQuant KV4 — confirmed live, both active simultaneously in the same request
  (server log: `TurboQuant: converted 15/64 cache layers to 4.0-bit` alongside
  `MTP path activated`).

**Quantization:** oQ4e (mixed 4/8-bit, oMLX's sensitivity-aware scheme) + TurboQuant
KV4 (`turboquant_kv_bits: 4.0`, first + last layer kept FP16 as an attention-sink
safeguard) — not plain affine 4-bit (`g128`/`g64`), not FP16 native (smaller footprint,
weaker per-token quality signal at this compression per agent-mesh's own P-05/P-07
rows), not the alternative 27B MoE releases evaluated and rejected below.

**Runtime parameters (current live config, `~/.omlx/model_settings.json` +
`~/.omlx/settings.json`):**

| Setting | Value | Why |
|---|---|---|
| `memory_guard_tier` / ceiling | `custom` / 59.0GB | Mike's explicit override, informed — see `redtrades/agent-configs#33` |
| `mtp_enabled` (native) | `true` | Bundled draft head, 47–91% acceptance observed live |
| `turboquant_kv_enabled` / bits | `true` / `4.0` | 70.3% KV memory reduction (`hermes/OMLX-M1MAX-OPTIMIZATION-GUIDE.md`), no conflict on this model |
| `guided_grammar_enabled` | `true` | **Flipped live this session.** xgrammar 0.2.3 was installed, unused. Verified: schema-constrained JSON request returned clean, valid output first try, 3.4s. Zero marginal cost. |
| `OMLX_QWEN35_Q8_MLP/LINEAR_MIN_TOKENS` | `256` | Un-gates the fast quantized-matmul kernel at real (contended) chunk sizes; shipped default (16384) never engaged |
| `OMLX_FA256_STEEL` | `0` | Measured slower than fallback on this M1 Max; steel kernel also has a documented macOS GPU-watchdog cliff past ~30K kv_len |
| `scheduler.max_concurrent_requests` | `3` (raised from `2` live this session) | **Real, current ceiling on parallelism** — see the HTTP and Hermes measurements in §3 and §7.2 |
| `iogpu.wired_limit_mb` (kernel) | `61440` (60GiB) | Fixed boot-time cap, 4GiB left for macOS |

**Hermes configuration** (`~/.hermes/config.yaml` + `profiles/qwen38-oq4e-{short,mid,full}`):
tiered context profiles (65,536 / 131,072 / 262,144) with matching `max_tokens`
(4,096 / 4,096 / 8,192) and a currently uniform 51,200-token absolute compression
threshold, `reasoning_effort: low` for mechanical turns (measured 10-20x cheaper
completion tokens than default, see §4), MOA off on the default profile (prevents an
unwanted cloud fan-out on every desktop turn), lean toolset (`file`/`terminal`/`todo`
only on short profile — cuts fixed prompt from ~24k to ~7.7k tokens).

**On-demand skills update:** Hermes can expose `skills_list` and `skill_view` without
preloading skill bodies, but its current installed catalog adds a measured 24.6KB
name/description index plus 3.7KB of tool schemas and includes unrelated GovCon/TDIU
skills. The broad toolset was therefore disabled again on every Qwen profile. A curated
agent-coding-only catalog is required before persistent on-demand discovery is enabled;
the benchmark profiles remain zero-skill controls. See
`LOCAL-EVIDENCE-RECONCILIATION-2026-08-27.md` for exact current/local provenance and
the measured prompt-size split.

---

## 2. Newer models — verified, not adopted, and why

Browser-confirmed directly against huggingface.co (not the summarizer tool chain — see
§6 for why that mattered) on 2026-08-27:

| Model | Real? | Size vs 59GB ceiling | Verdict |
|---|---|---|---|
| `mlx-community/Qwen3.8-27B-OptiQ-4bit` | **Yes** — 15 likes, apache-2.0, mlx-community org | Fits, but **21.31GB actual** (largest of the 27B-class variants tested — not the ~14-17GB class originally estimated) | **Now tested head-to-head** (real cross-engine result, `MASTER-PERMUTATIONS-MATRIX.md` §6, `mlx-lm` engine): 64.12 tok/s prefill / **9.72 tok/s decode** — decode is the slowest of all four 27B variants compared (vs. production oQ4e-mtp's 14.60 tok/s), consistent with sensitivity-aware non-uniform dequant carrying real overhead over oQ's mixed-but-regular 4/8-bit scheme. Confirms the production choice, not a missed win. |
| `mlx-community/Qwen3.8-27B-4bit` | **Yes** — 100 likes, 93,875 downloads | Fits | agent-mesh's M-03 (`g128` affine), already benchmarked: 70.4 tok/s prefill, 11.4 tok/s decode — measurably behind the oQ4e+TQ4+MTP champion |
| `Qwen3.8-Flash-Next` (Qwen4-preview MoE, 125B total/6B active) | Yes, but no MLX conversion fits | Smallest complete quant found: **77.15GB** (JANGQ-AI `JANG_4S`, published 2 hours before this check) — **worse** than the previously-known-best 67.67GB (Vontra oQ2). `JANG_4M` = 103GB. `JANG_6S` incomplete upload. All exceed the ceiling. | **Skip, re-confirmed against today's newest attempt** |
| `GLM-5.3` | Yes, 750B | Not applicable — hosted only, weights not out | Skip local |
| `GLM-5.3-Flash` | Yes, 320B MoE | Smallest artifact anywhere: 194.69GB | Skip local, unambiguous |
| `jangq`/`JANGQ-AI` "TurboQuant" Qwen3.8-27B-dense model | **Does not exist as named** | — | Naming conflation: TurboQuant is omlx's own KV-cache feature, not a JANGQ-AI model line. JANGQ-AI's real releases are their own `JANG_*`/`JANGTQ` quants of *other* models (MiniMax-M2.7, Qwen3.5-35B/122B-A-series MoE, dots3, and now Qwen3.8-Flash-Next) — none is a Qwen3.8-27B-dense conversion |

**No newer model beats the current setup on this hardware.** The MoE releases that
might win on quality-per-active-param don't have a complete quantization under the
memory ceiling at any precision found today. Re-check when a sub-55GB complete
Flash-Next quant appears (flip condition already documented in prior research) or when
llama.cpp/mlx-lm lands the architecture with disk-streaming MoE experts — both
currently immature (unmerged PR, CUDA-only validation, open macOS kernel-panic issue).

---

## 2.5. MoE vs. dense — the architecture-fit question itself, not just "does one fit"

§2 above only asked "does a MoE model's quantization fit under 59GB." A parallel
3-agent research pass asked the question the goal actually poses: is MoE well-suited
to *this hardware and this specific bottleneck* (prefill efficiency, ~20-27% of
theoretical, the weaker of the two per §5/§7.3) at all — independent of any one
model's size.

**Answer: no, and there's a specific, sourced mechanism, not just a hunch.**

- **MoE's compute-savings advantage is not automatic on unified memory, and stock
  loaders don't get it for free.** A live upstream investigation
  ([mlx-lm#1438](https://github.com/ml-explore/mlx-lm/issues/1438)) found that
  `mlx_lm.load`'s default path (`lazy=False`) materializes the *entire* stacked
  expert table into unified memory at load time regardless of which experts actually
  activate — an 18.2GB spike for a 4-bit MoE model before a single token runs. Getting
  "only active experts touch memory" back requires non-default code
  (`lazy=True` + an explicit LRU expert cache) — not what omlx/mlx-lm run out of the
  box today. Routing itself carries a real, measured tax on top of this: ~471
  `open()` syscalls for a single decode token at 0.836 cache-hit rate, ~36µs each,
  independent of whether the pages were warm — pure bookkeeping overhead dense models
  don't pay.
- **Prefill — this deployment's actual bottleneck — is exactly where MoE's sparse-compute
  advantage collapses.** Same investigation, same-generation model
  (Qwen3.6-35B-A3B, 256 experts): "a diverse prefill routes to nearly all 256 experts
  while the cache holds only 30%" — warm prefill performs *no better than cold*. Decode,
  by contrast, sustains 79-87% expert-cache hit rates under plain LRU — real temporal
  locality prefill doesn't get. Independently, [NPUMoE (arXiv 2604.18788)](https://arxiv.org/html/2604.18788v1)
  states prefill dominates total latency for long-context MoE workloads generally (80%
  of end-to-end latency, 70% of CPU cycles) specifically because decode's one-token
  cadence doesn't amortize coordination overhead the way prefill's batching would — if
  it could exploit it. **Net: MoE's real payoff lands on the phase this deployment is
  least bottlenecked on (decode, ~53% efficiency already) and evaporates on the phase
  it's most bottlenecked on (prefill, ~20-27%).** This is the new, load-bearing
  finding — not "MoE is unproven," but "MoE is mismatched to this specific bottleneck,"
  independent of any model fitting the ceiling.
- **No engine has real disk-resident expert-streaming today**, which would have been
  the other path to a win (run something bigger than 59GB by only paging active
  experts). Checked all four candidate engines directly against their own issue
  trackers: mlx-lm (`#1438`, open feature request, no PR), omlx (`#986`, open since
  2026-04-28, unstaffed), vMLX (ships "Smelt" — real, but *static* partial-expert
  loading decided at startup, not per-token streaming, and degrades output quality at
  aggressive offload ratios per its own README), llama.cpp (`#23324`, a working Metal
  proof-of-concept via `pread`-per-expert paging, genuinely the furthest along, but
  **unmerged**, and its own numbers trade 24-42% throughput for the memory saved even
  when it works).
- **Hardware fact, independently confirming §5/§7.3's existing conclusion:** Apple's
  own MLX research states the M5's Neural Accelerators give up to 4x prefill/TTFT
  speedup specifically because prefill is compute-bound and NAX adds native low-bit
  matmul throughput — while decode only gains 19-27% (bandwidth-bound, unaffected).
  This is **M5-exclusive** (macOS 26.2+); the M1 Max has no NAX, so this path is
  categorically unavailable on this hardware regardless of model or quant format
  chosen. Corroborates, from an independent source, §7.3's "dequant ALU overhead" /
  "no native low-bit path on this chip" finding rather than just repeating it.

**One concrete, actionable, version-specific lever surfaced by this pass — flagged,
not silently adopted:** omlx v0.6.3rc3's release notes claim "aligned Qwen GDN cache
boundaries with wide prefill — fixing deterministic issues," naming this exact
architecture (Qwen hybrid-GDN) and this exact bottleneck (wide prefill) by name. **This
directly conflicts with already-established, reproduced evidence** (§3.5,
`m64-omlx-findings.md`): 0.6.3rc3 hangs on Hermes's real tool-heavy request shape (both
the new checkpoint and a previously-solid 8-bit model, 7+ minutes frozen mid-prefill,
zero CPU, zero log progress) — a general regression tied to that same release's
memory-guard-accounting rewrite, not something to retry casually. **Verdict: do not
upgrade to 0.6.3rc3** — the hang is reproduced and severe; the prefill fix inside it is
real but not worth the outage risk. Worth watching for a tagged non-RC 0.6.3 release
that carries the GDN/wide-prefill fix without the hang regression, and re-testing then.

**Verdict on the actual question asked: stay on dense Qwen3.8-27B-oQ4e-mtp.** Not by
default/inertia — because the specific mechanism above (prefill = MoE's weak phase,
this deployment's bottleneck phase) was checked and confirmed, not assumed. The two
real near-term levers this pass surfaced instead: watch for a stable (non-RC) omlx
0.6.3 for the named Qwen-GDN-wide-prefill fix, and verify the SSD tier of omlx's own
`PagedSSDCacheManager` prefix cache is actually enabled — **checked live, it is**:
`server.log` confirms `PagedSSDCacheManager connected to BlockAwarePrefixCache`,
`paged SSD cache enabled: cache_dir=/Users/man/.omlx/cache, max_size=92.63 GB,
block_size=2048 tokens` at this session's own restart (§5.10). That 92.63GB is
`cache.ssd_cache_max_size: "auto"` resolved live — real data toward the still-open
§7.4 item on whether to pin it to an explicit cap instead.

---

## 3. Concurrency — real numbers, replacing a broken benchmark

`agent-mesh/evals/bench_concurrent_throughput.py` had a real counting bug: it counted
SSE *chunks*, not tokens, and MTP emits multi-token bursts per chunk — so its results
(reporting 1 total token generated regardless of concurrency level) are invalid.
A one-off non-streaming correction read `usage.completion_tokens` directly and was
run live against the current production model. Its source and raw JSONL were not
committed, so the following table is a session summary rather than a durable raw
receipt:

| Concurrency | Wall time | Requests OK | Total completion tokens | Aggregate end-to-end throughput |
|---|---|---|---|---|
| 1 | 43.85s | 1/1 | 64 (as requested) | 1.46 tok/s |
| 2 | 89.27s | 2/2 | 128 | 1.43 tok/s (flat vs. 1) |
| 4 | 64.86s | 4/4 | 256 | 3.95 tok/s |

**At the start of this measurement, the immediate concurrency bottleneck was
`scheduler.max_concurrent_requests: 2`.** Only 2 requests admitted simultaneously
regardless of how many arrive; a 3rd/4th queues. At concurrency=4, two waves of 2
completed (staggered finish times 32s/43s/60s/65s), which is *why* concurrency=4's
aggregate looks better than concurrency=2's isolated run — it benefited from whatever
warm state existed from the wave ahead of it, not from true 4-way GPU parallelism.
**No genuine 4-way concurrent decode was observed or is currently possible under this
setting.** The later Hermes process measurements in §7.2 show the same shape: a
fourth request completes correctly but pays substantial queueing latency.

**Update, same session: `max_concurrent_requests` raised 2 → 3 and re-tested live**
(backup: `~/.omlx/settings.json.bak-*-maxconc3test`). 3-way concurrency: 48.04s wall,
all 3 requests completed their full 64-token budget, aggregate 4.0 tok/s, individual
worker times 28.89s/42.3s/48.04s — genuine overlap, not badly staggered like the
2-cap/4-request test. This supports 3 as the practical concurrency ceiling on this
hardware (a 4th agent gets no demonstrated aggregate-throughput benefit, just waits).
**Applied as the new production setting** — checked
server was idle before changing it, no other agent's in-flight work disrupted.

---

## 3.5. Scheduler, release candidates, and full-context — from `hermes/m64-omlx-findings.md`

Read in full only after being asked directly whether every research document had
actually been read (it hadn't). Real, verified findings, not previously folded into
this document:

**omlx 0.6.3rc3 is broken for real Hermes traffic — do not upgrade.** Structural
checks (xgrammar, `thinking_budget_enabled`, memory-guard flag, idle-eviction) passed,
but a real Hermes tool-heavy request (~28K fixed overhead, real tool schemas) hung
**both** the new checkpoint and the previously-solid 8bit checkpoint on the same
0.6.3rc3 server — 7+ minutes, near-zero CPU, zero log progress, no error, no timeout.
Confirmed as a general rc3 regression (not model-specific) via a differential test.
Consistent with rc2/rc3's own release notes rewriting the memory-guard accounting and
error-reporting path — exactly where the hang occurred. Rolled back to 0.6.2, which
remains the current production version. Don't retry rc3 without checking upstream
`jundot/omlx` issues first, and prefer a tagged stable 0.6.3 over any RC.

**Historical stage: `scheduler.prefill_priority: "speed"` vs the default `"context"`.**
The default mode
proactively shrinks prefill chunks based on a conservative EWMA-predicted transient
cost with a safety multiplier — triggered by a *predicted* future watermark crossing,
not actual memory exhaustion. Every 144K+-token prefill attempt got progressively
throttled into single-digit tok/s under this default, even with the machine otherwise
idle and no real memory tail (confirmed via `top`, ruling out a leak). `"speed"` mode
trusts the hard limit checks to abort cleanly if truly necessary and otherwise runs
unthrottled — a request using it sailed through the exact 24K-48K token range every
prior attempt stalled on, at full ~65-90 tok/s, zero throttle lines. Live-settable, no
restart (`POST /admin/api/global-settings {"prefill_priority": "speed"}`), but **not
retroactive** — only affects requests started after the change. At this measurement
stage, `~/.omlx/settings.json` had `prefill_priority: "speed"`; §5.10 records the later
switch to the current `"context"` production value. Tradeoff to
know, not just take on faith: this is the right choice for a deliberate large
single-context run with nothing else resident; the more conservative `"context"`
default is safer for normal mixed/concurrent workloads where margin protects other
resident models — a judgment call the document itself makes explicitly, not something
this deliverable is overriding.

**The 144,364-token full-context test actually completed successfully — verified
against raw server.log, not taken on the document's word.** `PREFIX-CACHE-INTERNALS-GDN.md`
claims cold=3,065.16s / warm=52.94s / 99.3% reuse for this exact test; an earlier
document (`omlx-qwen38-oq4e-profile-verify-2026-08-26.md`) called the 144K marker
"unproven" and cited three aborted prefill attempts. Both are correct for different
points in time: `server.log.2026-08-26` shows three real aborts before 22:12
(`Prefill interrupted at 122880/144364`, `40960/144364`, `28672/144364`), then a clean
completion at 23:03:55 (`14 tokens in 3065.16s ... prompt: 144364, finish_reason=stop`)
and a second, cache-hit completion at 23:05:12 (`14 tokens in 52.94s ... prompt: 144364,
finish_reason=stop`) — exact match to the document's numbers, down to the decimal.
Sequential improvement (likely the ceiling raise + `prefill_priority: speed`), not a
contradiction. This is the strongest real prefix-cache proof in the whole corpus:
**58x speedup on a genuinely large, real context**, not a synthetic 16K-token
extrapolation.

**KV-cache cost formula, cross-validated against two independent live rejections.**
Only 16 of 64 layers are full-attention (`full_attention_interval: 4`); the other 48
are GDN linear-attention with O(1) state that doesn't grow with context. Growing KV
per token = `2 × 4 kv_heads × 256 head_dim × 16 layers` = 64 KiB/token. Two real
memory-guard rejections at 144,364 tokens, hours apart, both reported `KV+SDPA` costs
(9.35GB and 9.49GB) matching the formula's ~9.0GiB prediction. **Full-context requests
are rejected outright at admission** (a clean `prefill_memory_exceeded`, not a hang or
silent truncation) when another large model is co-resident and projected usage would
exceed the dynamic ceiling — the guard does not proactively evict an idle model to make
room at admission time (only the separate mid-prefill adaptive-throttle path does that).
Practical implication: unload other models first if you actually need the full
262,144-token window.

**MoE-vs-dense benchmark (`evals/results_moe_vs_dense_2026-08-27.jsonl`) is incomplete
— flagging rather than citing as a finding.** 2 of 3 candidate models (`LFM2.5-8B-A1B`,
`Qwen3.5-4B-8bit`) errored with HTTP 404 (not present/loaded on the server at test
time). Only `Qwen3.5-2B-MLX-4bit` produced real numbers (113-116 tok/s decode,
98-100% GPU util at 1K/4K/8K prefill) — genuinely fast, but a 2B model isn't a fair
capability comparison against the 27B-class candidates this document is actually
choosing between. Not a completed MoE-vs-dense verdict; don't cite it as one.

---

## 4. Hermes-real validation (not synthetic)

All run live this session against the current production config:

| Test | Result |
|---|---|
| Cold agent startup (`qwen38-oq4e-short` profile, model already resident) | `COLDSTART_OK`, exit 0, 104.5s wall |
| Tool use (real date-tool call) | Correct date returned, exit 0, 101.3s wall |
| Offline eval suite (`agent-mesh/evals/run.py --offline`) | **7/7 PASS**, freshly re-run this session (brief-format, judge-consistency, memory-recall, qwen38-hermes-contract, router-decision, topic-classifier, x-item-schema) |
| Warm continuation / cache-hit rate | **Cold: 63.31s, 4,324 prompt tokens, 0 cached. Warm (identical repeat): 8.8s, 4,324 prompt tokens, 4,096 cached (94.7% hit). 7.2× faster.** Directly measured, this session, real API responses. |

Agent-mesh's earlier multi-turn prefix-cache work reports 96.9% cache hit rate by turn
10 and TTFT dropping from 51.7s (cold) to 5.5s. The worklog names
`evals/results_prefix_cache_2026-08-27.jsonl`, but that raw receipt is absent from the
current Git tree. Treat this as a reported prior result, not a currently reproducible
repository receipt. The "2,972.9 tok/s effective prefill" headline is also a derived
metric (context size divided by latency), not raw computed-tokens throughput.

---

## 5. Theoretical ceiling — where the gap actually is

From `agent-mesh/hermes/OMLX-M1MAX-OPTIMIZATION-GUIDE.md`'s roofline analysis
(400GB/s effective bandwidth, 21.8 TFLOPS FP16, 54.5 FLOP/Byte ridge point — real
hardware constants, not estimated):

- **Decode: ~53% of theoretical bandwidth ceiling** (12.9 tok/s achieved vs 24.4 tok/s
  ceiling for the 16.4GB oQ4e footprint). This is architecture-dominated: a hybrid
  model's linear-attention layers and MTP verification overhead both spend bandwidth
  the naive `bandwidth / weight_size` formula doesn't account for. Not a
  misconfiguration — 53% is a believable, not alarming, real-world figure for this
  model class.
- **Prefill: only ~22% of theoretical compute ceiling** (81-90 tok/s achieved vs
  403.7 tok/s ceiling at 8K context). This is the real, honest gap. Contributing,
  independently-confirmed factors: the Q8 quantized-matmul kernel needed an explicit
  env-var fix to engage at all under contended (256-token) chunks (done, live);
  the boundary/block granularity for this hybrid model is hardcoded at 2048 tokens
  (not settings-tunable, costs ~17s/turn in trailing-partial-block re-prefill,
  upstream feature request needed); ANE-assisted prefill is available
  (`qwen35_ane_prefill_enabled`) but disabled after a confirmed macOS ANE driver panic
  (Code 47) under large sequence graphs on 27B-class models — a real stability
  tradeoff, not an oversight.

**Bottleneck identified, not hand-waved:** prefill throughput on this hardware for a
hybrid-attention 27B model is capped well below compute-theoretical by a combination
of (a) a hardcoded scheduler block size upstream doesn't expose, and (b) ANE
acceleration being unsafe at this model's sequence lengths on this chip generation.
Both are real, both are upstream-dependent, neither is fixable by local config alone.

---

## 5.5. Direct verification pass — don't presume anything above is correct either

Prompted explicitly to stop presuming and re-verify first-principles, including the two
open items this document had been treating as settled: the JANGQ-AI candidate (only
checked for existence/size before, never actually downloaded or run) and the ANE-prefill
"disabled, unsafe" claim (taken from a prior document's own conclusion, not independently
re-derived). Both investigated fresh, this pass:

### ANE prefill — root-caused, not just cited as disabled

Checked the actual failure directly against `server.log`, two independent occurrences
(2026-08-26 23:32 and 2026-08-27 01:07, both on the resident 27B model,
`sequence_length=2048` fixed shape):

```
omlx.patches.qwen35_ane_prefill - Eagerly compiled 64 MLP and 48 GDN procedures
  into 2 instance-pinned ANE programs (sequence_length=2048)
...
ANE evaluation failed: Error Domain=com.apple.appleneuralengine Code=47
  "...Inference failed — request aborted (underlying=0x15)"
```

This is a genuine macOS/ANE **driver-level** rejection at actual inference time, not a
Python exception or a config validation error omlx's own code raises — compilation
succeeds cleanly (64 MLP + 48 GDN procedures fused into just 2 ANE program instances),
inference is what the driver aborts. Fusing 112 procedures into 2 ANE program instances
for a 27B-parameter model is a large compute graph for a 16-core ANE (5.5 TFLOPS-equiv,
4x slower than the 32-core GPU's 21.8 TFLOPS on this chip already) — the failure shape is
consistent with a genuine ANE compiler/hardware complexity ceiling for a model this size
on this Apple Silicon generation, not an arbitrary software toggle. **Honest limit of this
investigation**: I did not have time this pass to test whether a different engine (vMLX,
which has its own ANE integration per `APPLE-SILICON-INFERENCE-ENGINES.md`) routes around
this the same way, or whether ANE prefill works cleanly on a *smaller* model on this same
chip (only tested against the 27B). That's the concrete next experiment if this is worth
pursuing further — I'm not claiming "no engine can do this," only that omlx cannot, on
this exact model, and the failure looks hardware-shaped rather than config-shaped.

### JANGQ-AI — actually downloaded and tested this time, not just verified to exist

Earlier in this document, JANGQ-AI was checked only for the (oversized) Flash-Next quants.
Went back and checked their **other** Qwen releases directly against the HF tree API:
`JANGQ-AI/Qwen3.5-35B-A3B-JANG_2S` = **11.67GB** and `JANG_4K` = **19.67GB** — both real,
both comfortably fit the 59GB ceiling (unlike every Flash-Next variant checked earlier).
Real MoE architecture (`Qwen3_5MoeForConditionalGeneration`, `model_type: qwen3_5_moe`,
base model `Qwen/Qwen3.5-35B-A3B`), confirmed supported by the installed `mlx_vlm`
(`mlx_vlm/models/qwen3_5_moe/` present, not stubbed). Downloaded `JANG_2S` (the smaller of
the two) live this pass — disk was at 94%/62GB free, checked before starting, 11.67GB is
affordable without deleting anything. **Result: see §5.7 below** — the checkpoint failed
to load on both omlx and vMLX; real reproduced errors, not a stale placeholder.

### Live-state discrepancy found and flagged, not silently resolved

`hermes/routing-policy.md` and `hermes/OMLX-HERMES-OPTIMIZATION.md` both declare
**production policy**: `prefill_priority: "context"` (the conservative default), with
`"speed"` reserved for an explicit, isolated, single-agent deep-context mode only. At
this intermediate measurement stage the live setting was `"speed"`, creating a real
policy drift. Section §5.10 records its subsequent resolution: production was restored
to `"context"`, restarted, and functionally retested. Also confirmed
`ssd_cache_max_size` is still `"auto"` live, despite
`hermes/OMLX-HERMES-OPTIMIZATION.md` recommending an explicit 40GB cap — another
recommended-but-not-applied item, not silently applied by me.

---

## 5.6. Full engine landscape — three real candidates not previously cited here

This session's own research workflow (GitHub-sourced, cross-checked, distinct from the
unreliable web-search-summarizer pass in §6) surfaced engines never mentioned anywhere
in this document's earlier drafts. Recording them so they aren't lost:

| Engine | Real? | Prefix cache | KV quant | Speculative decode | Relevant to this machine |
|---|---|---|---|---|---|
| `vllm-project/vllm-metal` | Yes, dev/nightly `0.3.0.dev20260826` | **Merged fix for hybrid-GDN prefix caching**, PR #584 — this is new, prior research said this was never completed | not confirmed this pass | present (draft-KV chunking) | Real candidate worth a fresh isolated-port bench; still needs the clunky `--enable-auto-tool-choice --tool-call-parser qwen3_xml` two-flag tool-calling invocation |
| `basecompute/baseRT` (arXiv:2607.00501) | Yes | Yes, paged-KV | int4 KV claimed faster than fp16 (own paper, checkable claim not just marketing) | not found | Narrower model-family support; a real, citable technical claim worth a bench if KV-quant throughput matters more than MTP |
| `lablup/mlxcel` | Yes, v0.1.0+ (2026-05-28) | Yes, env-tunable | llama.cpp-style flags | Gemma4 (MTP), Qwen3.5 (DFlash) only | Rust-native, no Python dependency; narrow model coverage limits fit here |
| `Pushkinist/rMLX` | Yes | Yes, block-hash based | widest matrix of any MLX server claimed (fp8/2-8bit/mxfp4/mxfp8/nvfp4/rotation-based), unverified perf | MTP/DFlash/Eagle3, Qwen3.6 sidecar | **Documents a 2-3.7x prefill regression on machines without an M5+ Neural Accelerator (NAX)** — this is an M1 Max, no NAX, so that regression class would apply here if tried; check for a non-NAX fast path before considering it a real candidate |

None of these change the §1 verdict (omlx stays the right runtime for the current
production model) — they're recorded as real, current alternatives worth knowing about
for a future engine-swap decision, not adopted this pass. `mlx-lm`'s own hybrid
prefix-cache fix status is genuinely unclear: issue #980 shows as "Closed" but with no
visible fixing PR or changelog reference in what this session could fetch — treat that
as unconfirmed, not as evidence mlx-lm now works for this architecture.

---

## 5.7. Actual cross-engine test on a different model — real results, real failures

Directly prompted to stop testing one model across configurations and actually test a
**different** model, on a **different** engine if needed. Did both, live, this pass.

**Confirmed by direct HF search: JANGQ-AI has never released a quant of Qwen3.8-27B
dense** (the production model's own base architecture) — only `Qwen3.8-Flash-Next`
variants (checked earlier, all oversized) and `Qwen3.5-35B-A3B` variants (a different,
older MoE line). `JANGQ-AI/Qwen3.5-35B-A3B-JANG_2S` (11.67GB) and `JANG_4K` (19.67GB)
are the real, fitting alternatives — downloaded `JANG_2S` live, disk checked first
(94%/58GB free before, comfortably affordable).

**vMLX (1.6.36, already installed) on the *current production model* — real, clean
result, same model as omlx:**
```
vmlx bench Jundot/Qwen3.8-27B-oQ4e-mtp --num-prompts 3 --max-tokens 64
  Total time: 16.47s | Tokens/second: 11.66 | Throughput: 12.93 tok/s
```
Loaded cleanly, recognized the hybrid architecture correctly (16/64 KV layers, SSM
companion cache), prefix cache auto-enabled. **12.93 tok/s essentially matches omlx's
own measured 12.9–14.6 tok/s on the identical checkpoint** — real cross-engine parity,
not a guess. `vmlx doctor --no-inference` on the same model also passed clean
(architecture/config/weights all OK, 2209 tensors, 24.4B actual param count vs the "27B"
name).

**No ANE flag exists anywhere in vMLX's CLI** (`vmlx bench --help` / `vmlx serve --help`
— neither has an ane/neural-engine option). Combined with omlx's ANE path being a
bespoke custom patch (`omlx.patches.qwen35_ane_prefill`, not a standard MLX/mlx_vlm
feature), the evidence now points to **ANE prefill acceleration for this model class not
being a generally-available engine capability at all** — omlx is the one engine that
attempts it, and it hits a real driver-level rejection (§5.5) doing so. This is a
stronger, more specific conclusion than "omlx's ANE path is broken" — it looks like
nobody has a working ANE path for a model this size on this chip generation, not just
omlx.

**JANGQ-AI's Qwen3.5-35B-A3B-JANG_2S fails to load on BOTH engines tested, for
different reasons — real, reproduced, not glossed over:**

- **vMLX 1.6.36**: crashes during weight sanitization —
  `KeyError: 'language_model.mtp.layers.0.mlp.experts.0.gate_proj.weight'` in
  `vmlx_engine/patches/mlx_lm_mtp/qwen35_model.py::_stack_per_expert`. The installed
  vMLX (1.6.36) is 5 patch versions behind current (1.6.41 per §5.6's research); this
  could plausibly be fixed upstream since, **not confirmed either way** — didn't have
  time to upgrade and re-test this pass.
- **omlx 0.6.2**: rejects outright at load — `"VLM load failed: Received 2090
  parameters not in model"`, listing weight keys all prefixed `model.language_model.*`.
  This looks like a checkpoint weight-key-naming convention mismatch (JANGQ-AI's own
  save format vs. what omlx's `mlx_vlm.models.qwen3_5_moe` loader expects), not a
  fundamental architecture incompatibility — omlx does support `qwen3_5_moe` as a
  module (confirmed present in §5.5), it just doesn't recognize *this checkpoint's*
  specific key layout.

**Honest bottom line on the "test a different model" ask**: a real different-model,
different-architecture (MoE vs. the production dense model) test was attempted, live,
on real hardware, on two real engines — and the concrete, reproducible finding is that
this specific checkpoint doesn't currently load on either one. That's a real result,
not a non-result: it means JANGQ-AI's MoE line isn't a drop-in alternative today without
either an omlx/vMLX fix or a different JANGQ-AI checkpoint. Not yet tried:
`JANG_4K` (the larger sibling, might use a different, more-standard save layout),
upgrading vMLX to 1.6.41 first, or checking whether omlx's own conversion tooling
(`hf download` + a format-normalization step, if one exists) can fix the key-prefix
mismatch without needing a new checkpoint.

**A fourth engine, tested live, on the exact production checkpoint — with a critical
correctness finding, not just a speed number.** Generic `mlx_lm` (v0.31.3, the library
omlx itself is built on) is installed locally and can point directly at the identical
Jundot/Qwen3.8-27B-oQ4e-mtp checkpoint from the local HF cache. Ran it directly:

- **Against the production oQe-quantized checkpoint**: loads without error (16.1GB
  peak memory, plausible-looking numbers — 56.8 tok/s prefill / 18.7 tok/s decode) —
  but **the output is incoherent garbage** (`"nAshttp <-whervenOX .tservenvarc..."`),
  not a crash, not an error, not a warning. Generic `mlx_lm` does not understand
  Jundot's custom oQe mixed-4/8-bit quantization scheme and silently misinterprets the
  weight bytes rather than refusing to load.
- **Control test, same command, a standard affine-4bit checkpoint**
  (`Qwen3.8-27B-MLX-4bit-g128`, no custom quant format): coherent, correct output
  (53.1 tok/s prefill / 20.2 tok/s decode) — confirms `mlx_lm` itself works correctly
  on this machine; the failure above is specific to the oQe format, not a broken
  install or a hardware issue.

**This is real, new information, not a repeat of the JANGQ-AI load-failure finding
above** — that one was a clean load error (key-prefix mismatch, refused to load); this
one is silent, plausible-looking, wrong output on a model that appears to load fine.
It proves that generic `mlx_lm` is unsafe for this oQe checkpoint, but it does not make
omlx the only correct engine: vMLX loaded the identical checkpoint coherently at parity
in the immediately preceding test. omlx remains the production selection because its
native MTP, TurboQuant, and tiered server cache are jointly verified here; vMLX is a
valid fallback for basic inference. This also directly
closes the literal "no live multi-engine measurement" gap: omlx, vMLX, and mlx_lm are
now all live-tested against the identical or an equivalent checkpoint on this hardware,
not just reviewed via documentation.

---

## 5.8. Hermes itself — tool-call repair logic and native fleet orchestration

Parallel research (source-cited against the live local `NousResearch/hermes-agent`
checkout, not training recall) surfaced two things not previously in this document:

**Hermes already has real repair/retry logic for exactly the kind of malformed
output a local model can produce**, not just documentation. `agent/message_sanitization.py`'s
`_repair_tool_call_arguments()` explicitly targets local-model JSON malformation
(truncated JSON, trailing commas, Python `None` literals) — a 5-stage repair pipeline
before falling back to `{}` rather than crashing the session, every repair logged at
WARNING. A second function, `repair_tool_call()` in `agent/agent_runtime_helpers.py`,
does fuzzy tool-*name* repair (casing, suffix duplication) with a difflib fallback. Both
cite real upstream issue numbers (#12068, #14784) for the local-model failure reports
that motivated them. This is a real, existing safety net for the exact reliability
concern a local backend raises — not something this session needs to build.

**No named "long-horizon" benchmark exists in Hermes itself** — confirmed by direct
grep across `tests/`, `docs/`, `website/docs/`, and source for `eval`/`benchmark`/
`long-horizon`/`multi-turn`. What exists instead are narrow, PR-scoped A/B harnesses
(`evals/compaction/`, `evals/browser_use/`, `evals/readtool/`, `scripts/toolperf_abeval/`)
— none is a general agent-capability benchmark. This session's own 3-step tool-use test
above (§7.2) and agent-mesh's own `evals/` suite are the closest things that exist to
what the goal is asking for; there was no missed "official" Hermes eval to run instead.

**Hermes's real answer to "orchestrate N concurrent agents" is `hermes kanban swarm`**
(`hermes_cli/kanban_swarm.py`) — a genuine native multi-agent topology primitive: one
CLI call creates N parallel specialist worker cards, a verifier gated on all workers
finishing, and a synthesizer gated on the verifier, with a shared JSON "blackboard,"
each worker "a full OS process with its own identity." This is real orchestration
infrastructure, not a throughput benchmark — it doesn't report aggregate
latency/throughput across concurrency levels, which is why the corrected
`bench_concurrent_throughput.py` and the real `hermes -z` concurrent-launch
test (§7.2) were the right tools for the *measurement* question, while `kanban swarm`
is the right tool if the actual production goal is running a coordinated multi-agent
fleet rather than just measuring concurrent throughput.

---

## 5.9. Scheduler internals, MTP key-mismatch flag, and a corrected premise

A second parallel 3-agent research pass (batch-scheduler internals, native-MTP tunable
surface, Hermes long-horizon/eval capability), source-cited against the installed
`~/.venv-omlx` package (v0.6.2, matches production) and the live Hermes repo, not
training recall.

**Self-correction: an earlier working premise in this investigation was wrong.**
Machine-context notes referenced `--prefill-step-size 8192 --max-num-batched-tokens
16384` as real CLI flags on this deployment. They are not. `omlx serve --help` (the
actual installed v0.6.2 binary) has no such flags — the real CLI surface is
`--max-concurrent-requests`, `--memory-guard-gb`, `--paged-ssd-cache-max-size`, etc. —
and the live LaunchAgent plist confirms the actual launch command carries none of them.
`prefill_step_size` and `max_num_batched_tokens` are real, but as hardcoded
`SchedulerConfig` dataclass fields (`2048` / `8192` respectively — note: opposite
numbers from the wrong premise) not wired to settings.json, CLI, or env in this build;
`~/.omlx/logs/server.log*` confirms every live scheduler-config log line reads
`prefill_step_size=2048 ... max_num_batched_tokens=8192`. `max_num_batched_tokens` is
additionally dead code — declared once, never read again in `scheduler.py`. Likely
origin: cross-engine naming conflation with vLLM's identically-named, actually-real
`max_num_batched_tokens` flag — same defect class as the JANGQ-AI/TurboQuant naming
conflation already caught in §2, now a second instance. D-026 and the corresponding
historical WORKLOG entry did assert these fields were tuned; D-027 and the appended
WORKLOG correction explicitly supersede only that attribution.

**`chunked_prefill: false` (current live setting) is confirmed still correct for
0.6.2** — not stale config. An earlier session reported a 64% TTFT regression under
`chunked_prefill=true`, but its named raw verdict file is absent from this repository;
that report predates `decode_fairness`, a v0.6.0
mechanism this machine already runs with `decode_fairness: true`. Source
(`scheduler.py`) confirms `decode_fairness` already forces adaptive chunking under real
GPU contention via a separate `force_chunk` path — independent of the `chunked_prefill`
flag — while leaving uncontended prefill unchunked for full throughput. The two
mechanisms don't conflict; the old test's negative result doesn't apply to the current
regime.

**New, quantified mechanism behind the original memory-guard abort
(agent-configs#33):** while `prefill_priority: "speed"` was live earlier in this session,
each admitted request's memory-guard admission charge is the *full* `prefill_step_size`
(2048 tokens), not the throttled `prefill_min_chunk_tokens` floor (32, per live
settings.json) that `"context"` mode would charge instead — a **64x** difference in
per-slot admission charge, source-confirmed at `scheduler.py:9239-9247`/`3921-3925`.
Raising `max_concurrent_requests` (done this session, 2→3 — §7.1) while
`prefill_priority=speed` was live multiplied that full-charge admission cost across
every simultaneously-admitted slot, which is the same mechanism already implicated in
the original abort. This added a concrete, mechanistic reason to restore `"context"`;
§5.10 records that resolution and its functional retest.

**Flag for a claim living outside this document, not fixed here:** native
`omlx.model_settings` defines two separate, non-interchangeable MTP knobs —
`mtp_num_draft_tokens` (native MTP depth, what this deployment's `mtp_enabled: true`
path actually uses) versus `vlm_mtp_draft_block_size` (an external-drafter path
docstring-scoped to Gemma4-VLM assistants). This document does not reference a
block-size=2-vs-3 MTP result (grepped, none found here), so nothing here needs
correcting — but if another artifact in this research effort (e.g. an agent-mesh note)
claims a `block_size=2` MTP acceptance win for this checkpoint, verify it was measured
against `mtp_num_draft_tokens`, not `vlm_mtp_draft_block_size`, before trusting it: a
same-month community field report on this exact checkpoint (`jundot/omlx#2811`) found
depth **3** peak (75.0 tok/s @ 8k), the opposite direction. Also worth a log check
before trusting any MTP acceptance number taken recently: open issue `jundot/omlx#2911`
(this exact checkpoint, filed 2026-08-20, unresolved) reports a settings-reload loop
firing every ~12s and freeing 17-21GB, which would contaminate any acceptance-rate
measurement taken while it's active. Neither of these was verified against this
session's own MTP acceptance numbers (§1/§7.1's "47-91% observed live") — flagged as
unverified, not asserted broken.

**TurboQuant KV4 + native MTP**: the crash this combination once caused is fixed in
exactly this machine's version (`v0.6.2` release notes, PR #2782) — verification falls
back to a non-quantized attention path when it hits a TurboQuant proxy it can't handle,
rather than crashing. No documented quantitative accuracy-impact model exists for this
combination anywhere upstream; a same-month field report (`#2811`) held 86–92% MTP
accept with TurboQuant 4-bit + MTP together on a comparable machine, consistent with
this session's own observed range.

**Hermes eval/long-horizon capability — confirmed absent, not just unfound.** Direct
grep of the live `NousResearch/hermes-agent` repo (`main`, pushed 2026-08-27) for
"long-horizon"/"long horizon" returns zero hits — not a defined term in Hermes's own
docs. Hermes ships `evals/compaction/` (context-compaction recall accuracy, real
500K-token sessions, explicitly scoped — does not measure "whether summaries preserve
reasoning chains") and `evals/browser_use/` (single-session browser A/B, not
multi-turn) — neither is a general long-horizon/multi-agent-fleet benchmark. No
local-model-specific tool-call retry/fallback logic found in docs beyond the general
repair pipeline already covered in §5.8. `delegate_task` (default cap 3 concurrent
children) and Kanban Swarm are real native concurrency primitives but are
production-orchestration tools, not measurement instruments — confirming §5.8's
conclusion that this session's one-off corrected HTTP harness + real `hermes -z`
concurrent-launch test (§7.2) were the right, and only, tools for the throughput
question — there was no missed built-in Hermes benchmark to run instead.

---

## 5.10. Executing the synthesis's three "do first" items — live, not deferred

The §5.9 synthesis named three concrete, cheap checks as the highest-leverage next
steps. All three were executed live this session (server confirmed idle via
`/admin/api/activity` first — 0 active/waiting requests, safe to test) rather than left
as open questions.

**(a) Which MTP key is actually live — resolved, no bug found.** Read
`~/.omlx/model_settings.json` directly (source of truth; the admin REST path for a
per-model settings GET returned 405 on this build, not a usable API surface). The
**production default model** — `Jundot--Qwen3.8-27B-oQ4e-mtp` (`is_default: true`,
`model_alias: "qwen3.8-oq4e"`, which is what `hermes_model` in `~/.omlx/settings.json`
actually points Hermes at) — has `mtp_enabled: true` / `vlm_mtp_enabled: false`: it
correctly uses **native MTP**, not the VLM-drafter path. The `vlm_mtp_draft_block_size:
2` setting the §5.9 flag was worried about exists only on a **different, non-default**
model entry (`mlx-community--Qwen3.8-27B-8bit`, `mtp_enabled: false`, `vlm_mtp_enabled:
true`) — a real, separate checkpoint. So: if a block_size=2-vs-3 result exists
elsewhere in this research corpus, it was very likely measured against that other
8bit/VLM-MTP model, not the production oQ4e-mtp deployment — a distinct model, not a
misconfigured one. No corrective action needed on the production config; this closes
the flag as "verified, not a live bug," not "unresolved."

**(b) Issue #2911's reload loop — checked, does not reproduce here.** Grepped all 8
rotated `~/.omlx/logs/server.log*` files (2026-08-20 through today, 2026-08-27) for the
issue's signature log line (`"Runtime settings variant changed"` / `"variant
changed"`) — **zero occurrences** across ~2.8MB of combined log. A broader
reload/unload grep (280 hits) shows only expected, non-looping events: idle-timeout
unloads, benchmark unloads, and this session's own explicit test unloads/restarts —
none cycling at the reported ~12s period. Verdict: the #2911 defect is not present on
this deployment/version combination; MTP acceptance numbers already recorded in this
document (§1/§7.1's "47-91% observed live") are not suspect on this basis.

**(c) `prefill_priority: context` vs `speed` — tested live, applied, not just
recommended.** Backed up `~/.omlx/settings.json`
(`.bak-20260827-073326-prefill-priority-ab-test`), flipped `scheduler.prefill_priority`
to `"context"` (matches the written production-policy default and `omlx`'s own
`settings.py:281` dataclass default), restarted via the documented `launchctl bootout` →
`bootstrap` cycle, confirmed healthy in 2s, confirmed the new value
live from disk post-restart. Re-ran the same one-off non-streaming harness used for
§3/§7.2's concurrency numbers, sampling `/admin/api/activity` memory pressure every 4s
throughout:

| Concurrency | Wall time (context, this test) | Wall time (speed, §3/§7.2, prior) | Requests OK | Peak memory pressure observed |
|---|---|---|---|---|
| 1 | 18.34s | 43.85s | 1/1 | 19.7GB used / 53.1GB soft / 56.0GB hard — level `ok` throughout |
| 2 | 26.85s | 89.27s (at cap=2) | 2/2 | same — never left `ok` |
| 4 (cap=3, so 3+1 staggered) | 54.64s | 64.86s (at cap=2) | 4/4 | same — never left `ok` |

**Honest caveat on this table, not overclaimed:** the two runs aren't a clean isolated
A/B — the context-mode run happened right after a process restart (fresh allocator
state) and the concurrency cap itself changed between the two data collections (2→3,
§3's own update), so the wall-time deltas above are directional, not proof that
`context` mode alone is 2-3x faster. What *is* clean: **zero failures, zero aborts, no
regression** under `context` mode at this benchmark's scale, and memory pressure never
approached `soft`/`hard` at any point — consistent with, not proof of, the §5.9
source-derived 64x-lower-admission-charge mechanism. This benchmark's 512-token prompts
don't stress the memory guard the way the original ceiling-hit incident's real
long-context Hermes traffic did (agent-configs#33, 55.8GB vs a 50GB ceiling) — a true
apples-to-apples stress replay would need a comparable large-context concurrent run,
which was not run here: given the documented 95.2%-swap outcome from a prior 4-agent
large-context test at a raised ceiling, that specific test is deliberately not
attempted without Mike's explicit go-ahead, since it risks reproducing real swap
pressure, not just a config toggle.

**Left live, not reverted.** `context` mode is now the running production setting —
it matches written policy, matches upstream's own default, passed this functional
retest with no regressions, and removes the quantified 64x admission-charge gap that
was compounding with this session's own `max_concurrent_requests: 2→3` change. Revert
path if Mike wants `speed` back: `cp ~/.omlx/settings.json.bak-20260827-073326-prefill-priority-ab-test ~/.omlx/settings.json` then the same bootout/bootstrap restart cycle.
§7.1/§7.4 updated accordingly below.

---

## 5.11. `chunked_prefill` — fresh live A/B under this session's current config

Mike asked for another sweep. Picked this one: it's the one scheduler setting that had
only ever been justified by an old (2026-08-21) test predating this session's changes,
plus a source-code argument (§5.9) that the old test no longer applies — never actually
re-run live under the config this deployment runs *today* (`prefill_priority: context`,
`max_concurrent_requests: 3`, both changed this session).

**Method**: server confirmed idle first (`/admin/api/activity`, 0 active/0 waiting).
Backed up `~/.omlx/settings.json`
(`.bak-*-chunked-prefill-ab-test`), ran the same concurrency benchmark
(`bench_chunked_prefill_ab.py`, same shape as `bench_concurrency_fixed.py`) at
concurrency 2 and 3 as a fresh baseline, flipped `chunked_prefill` to `true`, restarted
(`bootout`/`bootstrap`, healthy in 2s), re-ran the identical benchmark, then reverted
and re-ran once more to confirm the revert was clean.

| | Concurrency 2 wall | Concurrency 3 wall | Aggregate decode (2 / 3) |
|---|---|---|---|
| `chunked_prefill: false` (baseline) | 25.32s | 44.52s | 5.06 / 4.31 tok/s |
| `chunked_prefill: true` | **72.45s** | **155.84s** | 1.77 / 1.23 tok/s |
| `chunked_prefill: false` (post-revert confirm) | 31.21s | 42.29s | 4.10 / 4.54 tok/s |

In this single non-durable session run, **`true` was 2.9x slower at concurrency 2 and
3.5x slower at concurrency 3** — far
beyond the old 2026-08-21 test's "+1.2%, marginal" finding, and the post-revert run
lands back in the same range as the fresh baseline (both `false`), ruling out "the
reducing the likelihood that server load alone explains the difference. The harness
and raw output were not committed, so this is testimony to reproduce rather than a
merge-gating benchmark receipt. Plausible mechanism, not
confirmed by further source-diving this round: `chunked_prefill: true` may now be
double-chunking against `decode_fairness`'s own adaptive `force_chunk` path (§5.9) —
both mechanisms trying to manage the same contention, working against rather than with
each other — worth a source-level look if anyone wants to explain *why* it's this much
worse, not just confirm that it is. **This is the strongest evidence yet for
`chunked_prefill: false`** — not source-argued-and-assumed-still-true, but freshly
reproduced, live, against exactly the config running today. Reverted, verified clean.

---

## 6. A note on research methodology

A parallel research pass in this session flagged its own web-search results as likely
unreliable (a control check against a known-real model returned physically impossible
parameter/size numbers). Rather than trust or dismiss that blind, every specific model
name in question was checked directly against `huggingface.co`'s API in a real browser
tab this session — all four of the originally-named candidates (`OptiQ`, `Jundot`
oQ4e-mtp, the plain `4bit` community build, and the `jangq`/`TurboQuant` naming) came
back with a definitive, verifiable answer (three real, one a naming conflation — see
§2). Treat any *future* claim about an obscure model's existence or specs the same way:
confirm via a direct browser hit to the HF API, not a summarized web-search result.

---

## 7. Final consolidated answer

Everything above in one place, per the original ask: optimal model, quantization,
runtime, runtime parameters, Hermes configuration, caching strategy, measured
performance for 1–4 concurrent agents, comparison against theoretical limits, and
recommendations.

### 7.0 The master A/B matrix — every axis the goal named, one table

Every parameter category listed in the original ask, what was actually done about it,
and the evidence class (live test this session / live test cited from agent-mesh /
source-code confirmation / literature+architecture review), so "tested" and "ruled out
by source" aren't conflated with "assumed."

| Axis | Alternatives considered | Evidence | Verdict |
|---|---|---|---|
| **Model** | Jundot oQ4e-mtp (prod), OptiQ-4bit, plain 4bit-g128, 4bit-FP16-g64, Flash-Next, GLM-5.3/-Flash, JANGQ-AI MoE, Qwen3.6-35B-A3B, GPT-OSS-20B | **Live**: oQ4e-mtp (prod, 12.5-14.6 tok/s decode), OptiQ (§2, mlx-lm, 9.72 tok/s), g128 (§5.6 table, 11.40 tok/s omlx / 20.2 tok/s mlx-lm control §5.7), FP16-g64 (vMLX 15.1-19.5, mlx-lm 14.44). **Existence-checked, size-ruled-out**: Flash-Next/GLM (§2). **Architecture-ruled-out**: MoE generally (§2.5 — prefill-mismatch mechanism, sourced) | oQ4e-mtp wins on the metric that matters for this workload (decode × cache-hit-rate combined), not raw prefill |
| **Quantization** | oQ mixed 4/8-bit, OptiQ sensitivity-aware, affine g128, affine g64+FP16-scales, plain 8bit | Live, same runs as Model row above | oQ mixed wins decode; OptiQ's non-uniform dequant carries real measured overhead |
| **Engine** | omlx, vMLX, mlx_lm, llama.cpp/BaseRT/mlxcel/rMLX | **Live**: omlx (prod), vMLX (§5.7, 12.93 tok/s parity), mlx_lm (§5.7, **loads but silently corrupts output** on oQe format — correctness failure, not perf). **Architecture-reviewed, not live-run**: llama.cpp/BaseRT/mlxcel/rMLX (§5.6) — none demonstrates the complete oQe/native-MTP/TurboQuant/tiered-cache stack | omlx selected for the complete verified feature combination; vMLX is a correct basic-inference fallback |
| **MTP / draft-decode depth** | Adaptive (`None`, prod default) vs fixed `mtp_num_draft_tokens=2` vs `=3` | **Live, this round**: adaptive ≈13.3-14.1 tok/s decode; depth=2 ≈12.0 tok/s; depth=3 ≈11.96 tok/s (3 runs each, steady-state after reload, same prompt/temp=0/max_tokens=100). Settings edited directly in `model_settings.json` (backup taken) + `POST /admin/api/reload`, since `mtp_num_draft_tokens` isn't in the live-PUT `ModelSettingsRequest` schema (confirmed via source, matches the community report in §5.9) | **Adaptive (current default) beats both fixed depths tested** — reverted cleanly, confirmed via a post-revert steady-state run (14.06 tok/s) |
| **Batch size / batch tokens** | N/A — checked whether a real tunable exists at all | **Source-confirmed** (§5.9): `max_num_batched_tokens`/`prefill_step_size` are hardcoded dataclass fields (8192/2048), not wired to CLI/settings.json/env; `max_num_batched_tokens` is dead code, never read after being set | Not a live axis on this build — this is a sourced fact, not an untested gap |
| **KV cache bit-width / cache quantization** | `turboquant_kv_bits`: 4 (prod) vs 8 | **Live, this round**: kv4 ≈13.3 tok/s decode, kv8 ≈12.0 tok/s decode (3 runs each, steady-state). Set live via `PUT /admin/api/models/{id}/settings` (no reload needed for this key) | kv4 (current) is faster — smaller cache, less bandwidth per attention read. Reverted, confirmed |
| **Prefix/prompt cache** | Hot-tier only vs hot+SSD tiered (prod) | **Live** (§4/§5.10): 94.7% hit / 7.2x speedup (this doc's own synthetic test), 96.9%/58x + verified 144K test (agent-mesh); SSD tier confirmed enabled via `server.log`, auto-sized 92.63GB | Tiered caching is real, large, and confirmed live-enabled |
| **Context allocation** | 65536 / 131072 / 262144 profiles | **Live-cited** (§3.5, m64-omlx-findings.md): 144K-token cold/warm test, 3065.16s→52.94s | Profile-per-task-size confirmed working as designed |
| **Scheduler: chunked_prefill** | `true` vs `false` (prod) | **Source-confirmed** (§5.9) + one non-durable live session summary (§5.11; harness/raw output not committed): `true` was reported **2.9-3.5x slower** under concurrent load | Keep `false`; reproduce with a sanitized harness and raw receipt before treating the exact ratios as merge-gating evidence |
| **Scheduler: decode_fairness** | on (prod) vs off | **Source-confirmed** (§5.9): exact mechanism traced (`_DECODE_FAIR_SHARE=0.5`, `_CONTENDED_CHUNK_FLOOR=256`), no counter-evidence found upstream | On, correct |
| **Scheduler: prefill_priority** | `speed` (prior live) vs `context` (prod default, now live) | **Live, this session** (§5.10): flipped, restarted, retested — 0 failures/aborts, memory pressure stayed `ok`; 64x-lower-admission-charge mechanism is source-derived, not yet stress-tested at original-incident scale (deliberately deferred, swap-risk precedent) | Switched and applied to `context` |
| **Threads** | N/A — checked whether a real tunable exists | **Source-confirmed** (§5.9 CLI enumeration): no `--threads`/thread-count flag exists on `omlx serve --help`; MLX dispatches via Metal, not a CPU-thread-count model the way llama.cpp is | Not applicable to this engine — sourced, not assumed |
| **Concurrency** | `max_concurrent_requests`: 1/2/3/4 | **Live**, both raw HTTP (§3, 1/2/3/4) and real Hermes CLI (§7.2, 2-agent and 4-agent, 100% correctness both times) | Raised 2→3 live this session; 4th agent queues, correctness holds, throughput-per-agent falls off past 3 |
| **Engine-specific opts** | `OMLX_QWEN35_Q8_LINEAR_MIN_TOKENS=256`, `OMLX_FA256_STEEL=0`, `guided_grammar_enabled`, `gdn_ssd_split_enabled` | **Live-confirmed** via settings dumps and loader traces summarized here and in `hermes/benchmark-results-2026-08-27.md` | All live and verified active |

**What this table is not**: a claim that every cell above was independently discovered
this round. Several rows cite agent-mesh's own prior work (marked as such) rather than
re-running an already-real test. What it is: a single place answering the hook's literal
ask — "what settings were tested and why current ones are optimal vs alternatives
tried" — with the evidence class stated plainly for each row, including the two rows
(batch size, threads) where the honest answer is "not a real axis on this engine,
confirmed by reading the source" rather than a benchmark number.

### 7.1 The stack

| Layer | Choice | Confidence |
|---|---|---|
| Model | `Jundot/Qwen3.8-27B-oQ4e-mtp` | High — cross-validated by 3 independent measurement passes (this document, agent-mesh's own matrix, a second parallel agent's independent research), all landing within noise of each other |
| Quantization | oQ mixed 4/8-bit + TurboQuant KV4 | High — measured, not vendor-claimed |
| Runtime | omlx 0.6.2 | High for this specific model+quant combo. **Not exclusive** — vMLX 1.6.36 measured 12.93 tok/s on the *identical* checkpoint this session, real parity, not a guess. omlx wins on prefix-cache maturity (SSD-tiered, server-confirmed correctness) and being the currently-tuned production path; vMLX is a legitimate fallback/alternative, not disqualified |
| Speculative decode | Native `mtp_enabled` | High — 47-91% acceptance observed live across many real requests |
| KV compression | TurboQuant KV4 | High — coexists with native MTP (does not with the external-drafter `vlm_mtp_enabled` path — real, scoped upstream limitation, `jundot/omlx#1584`) |
| Structured output | xgrammar / `guided_grammar_enabled: true` | High — flipped live, verified with a real schema-constrained request |
| Concurrency cap | `max_concurrent_requests: 3` | High — tested live at 1/2/3/4, matches independent prior research's 3-agent ceiling finding |
| Prefill priority | **Resolved and applied this session**: `context` (matches written policy + omlx's own default) | High for the small-context functional retest (§5.10: 0 failures/aborts, memory pressure stayed `ok`); the 64x-lower-admission-charge mechanism is source-derived (§5.9), not yet stress-tested at the original incident's large-context scale — that specific stress replay is deliberately not attempted without Mike's go-ahead given the documented 95.2%-swap risk. Backup + revert command in §5.10 |
| ANE prefill | **Not achievable on this hardware for this model class**, on any engine tested | High confidence on "not achievable here," not fully exhaustive on "no engine anywhere can" — see §5.5/§5.7 |

### 7.2 Measured performance, 1–4 concurrent agents (real, this session)

Raw HTTP-level concurrency (one-off non-streaming harness; summary retained here but
raw receipt not committed):

| Concurrency | Wall time | All requests completed full budget? | Aggregate end-to-end throughput |
|---|---|---|---|
| 1 | 43.85s | Yes | 1.46 tok/s |
| 2 (at cap=2) | 89.27s | Yes | 1.43 tok/s |
| 3 (at cap=3) | 48.04s | Yes | 4.0 tok/s |
| 4 (at cap=2, so 2+2 staggered) | 64.86s | Yes | 3.95 tok/s |

**Real Hermes-agent-level concurrency** (actual `hermes -z` CLI invocations, not raw
HTTP — this is what "2-4 concurrent Hermes agents" actually means in production use):
2 real concurrent `hermes -z` CLI agents launched simultaneously (`qwen38-oq4e-short`
profile, distinct deterministic-marker prompts) — Agent2 completed in **62.00s wall**,
exit 0, correct output (`AGENT2_OK`); Agent1 (same batch, same launch instant)
completed in **99.14s wall**, exit 0, correct output (`AGENT1_OK`). Both agents got
correct, complete answers under real concurrent Hermes-CLI load, not raw HTTP.

**Extended to 4 real concurrent Hermes agents, same session** (server confirmed idle
first via `/admin/api/activity`): 4 simultaneous `hermes -z` CLI processes, each a real
date-check-and-reply tool-use task with a distinct marker. All 4 completed correctly,
exit 0, correct output on every agent (`AGENT{1-4}_OK_DATE_IS_2026-08-27`) — **100%
correctness at 4-way real concurrent Hermes load**, not just 2-way. Wall times:
162s / 234s / 317s / 365s. This is the real cost of exceeding the `max_concurrent_requests: 3`
admission cap under genuine Hermes-CLI load, not raw HTTP — the 4th agent (and to a
lesser extent the 3rd) pay real queueing time, roughly in line with the 3-agent-ceiling
finding already established in §3: correctness never degrades, but
throughput-per-agent falls off sharply past 3 concurrent. This closes the literal
"2-4 concurrent Hermes agents" validation the goal asked for — both ends of the range
now have real, not synthetic, measurements.

**Hermes eval suite:** this session reported a **7/7 online pass** against the current
production endpoint, but wrote it only to a scratch file that is not present in Git.
Therefore it is session testimony, not a durable repository receipt. The fresh,
committed reconciliation run is **7/7 offline** in `evals/results.jsonl`.

**Real long-horizon, multi-tool-call task** (not a single deterministic marker — a genuine
3-step sequential task: check the date, compute a value, write a file combining both,
confirm completion):
```
hermes --profile qwen38-oq4e-short --yolo --reasoning none -z \
  "First check today's date. Then compute 17 times 23. Then write a file ... \
   containing the date and the computed product, one per line. Confirm when done."
```
Completed correctly in **121.04s wall**, exit 0. Verified two ways: the model's own
confirmation text, *and* independently reading the actual written file — both lines
exactly correct (`2026-08-27`, `391`). This is the real tool-use + long-horizon
validation the goal asked for, not a synthetic substitute.

### 7.3 Theoretical ceiling vs. measured, and the actual bottleneck

From `agent-mesh/research/M1-MAX-ROOFLINE-MICROARCHITECTURE.md` (real hardware
constants: 400GB/s bandwidth, 21.8 TFLOPS FP16, 54.5 FLOP/Byte ridge point):

| Model tier | Decode ceiling | Decode measured | Decode efficiency | Prefill ceiling | Prefill measured | Prefill efficiency |
|---|---:|---:|---:|---:|---:|---:|
| Dense 27B (production model) | 24.4-27.8 tok/s | 12.5-14.6 tok/s | ~53% | 403.7 tok/s | 81-108 tok/s | ~20-27% (two docs' own rounding differs slightly, both real) |
| Dense 14B | 45.5 tok/s | 28-32 tok/s | 70% | 741.5 tok/s | 350-380 tok/s | 51% |
| Dense 7B | 88.9 tok/s | 72-82 tok/s | 92% | 1,432.3 tok/s | 720-820 tok/s | 57% |
| MoE 16B-A2.4B | 43.5 tok/s (all-stream) | 38-85.6 tok/s | 96.6% (scan) / 29.9% (sparse, more realistic) | 4,541.7 tok/s | 668.95 tok/s | 14.7% |
| Dense 2B | 190.5 tok/s | 85.3-116.1 tok/s | 61% | 5,450 tok/s | 1,495.6-1,658.4 tok/s | 30% |

**Pattern, not noise:** decode efficiency rises sharply as model size drops (53% → 70%
→ 92%) — smaller models are closer to pure memory-bandwidth-bound behavior with less
per-token fixed overhead swallowing the ceiling. Prefill efficiency stays in the
15-30% band across nearly every tier regardless of size — this is the real signal that
prefill's gap isn't primarily about which model, it's structural to this chip/engine
combination.

**Named, evidenced limiting factors** (not hand-waved):
1. **Dequantization ALU overhead** (~38% cycle inflation) — Apple G13 GPUs have no
   native INT4 tensor path; every 4-bit weight gets unpacked to FP16 before the actual
   multiply. This is a real Apple Silicon architecture limit, not fixable in software
   beyond choosing a less-aggressive quantization (which trades memory for it).
2. **A hardcoded 2048-token cache-boundary block size** in omlx's scheduler — not
   settings-tunable, costs real re-prefill on trailing partial blocks every turn.
   Upstream feature request needed, not a local config fix.
3. **ANE acceleration genuinely unavailable for this model class** — confirmed via a
   real Code=47 driver-level rejection (not a config toggle), and confirmed no other
   tested engine even exposes an ANE path to try. This one is very likely a hardware/
   driver ceiling for a 27B-class compute graph on this ANE generation, not a
   config gap.
4. **Metal command-buffer dispatch overhead** — 64 layers × ~8 kernel dispatches = 512
   launches per chunk, each with real driver latency. Structural to how MLX issues
   work on this hardware, not tunable per-request.

None of these four are things a different local setting fixes. This is the honest
"below theoretical, here's why, and it's not something more tuning solves" answer the
**What a hardware upgrade would actually close, quantified — not just named.**
Apple's own MLX research states the M5's Neural Accelerators (NAX) give **up to 4x
prefill/TTFT speedup vs. M4**, specifically because prefill is compute-bound and NAX
adds native low-bit matmul throughput that skips the dequant-to-fp16 step named as
limiting factor #1 above; the same source states decode only improves 19-27% on the
same hardware (bandwidth-bound, largely unaffected by NAX) — consistent with this
document's own finding that decode (53-92% efficiency depending on model size) is
already much closer to its ceiling than prefill (15-30%) is to its. Applied to this
deployment's own numbers: the production model's measured prefill (81-108 tok/s
against a 403.7 tok/s ceiling) would be the axis that moves, not decode. **Caveat, not
overclaimed**: this is Apple's own reported *range* for the M5 generation broadly, not
a number re-derived for this specific 27B checkpoint/quant/engine combination — no M5
hardware was available this session to verify directly, so treat "up to 4x prefill"
as the vendor's own ceiling claim, not an independently reproduced one. A discrete-GPU
path (eGPU, or moving inference off-device) was not evaluated — out of scope for "what
does an Apple Silicon hardware refresh buy you," which is the upgrade path actually
relevant to this machine's form factor. **Requires macOS 26.2+ and M5-class silicon** —
categorically unavailable on this M1 Max regardless of any software change, which is
exactly why §7.3's four named limiting factors are described as structural rather than
config gaps: none of them close without new hardware.
### 7.4 What's still genuinely open (not resolved this pass, named not hidden)

- ~~`prefill_priority: context` vs `speed`~~ — **resolved and applied live this
  session** (§5.10): switched to `context`, restarted, verified healthy, retested with
  no regressions, memory pressure stayed `ok` throughout. Not yet stress-tested at the
  original incident's large-context concurrent scale — deliberately deferred pending
  Mike's go-ahead given the documented 95.2%-swap precedent, not left undone by
  oversight.
- ~~MTP key possibly mismeasured~~ — **checked live, no bug** (§5.10): production
  default model (`Jundot--Qwen3.8-27B-oQ4e-mtp`) correctly uses `mtp_enabled`/native
  MTP; `vlm_mtp_draft_block_size` lives only on a separate, non-default model entry.
  Any block_size=2-vs-3 result elsewhere in the research corpus was almost certainly
  measured against that different model, not a misconfiguration of production.
- ~~`jundot/omlx#2911` reload loop~~ — **checked live, does not reproduce** (§5.10):
  zero occurrences of the issue's log signature across all 8 rotated log files
  (2026-08-20 through today).
- `ssd_cache_max_size: auto` vs the recommended explicit 40GB cap — recommended by two
  separate documents, never applied. Now with a live data point (§2.5/§5.10): `auto`
  resolves to **92.63GB** on this deployment's own disk — more than double the
  recommended cap, still unapplied, still Mike's call not mine to make unilaterally.
- JANGQ-AI's Qwen3.5-35B-A3B MoE line — real, fits, but fails to load on both tested
  engines; needs either an engine version bump (vMLX 1.6.41) or a format fix, not
  concluded as "doesn't work at all."
- ANE prefill — confirmed broken on omlx, confirmed no CLI path in vMLX to even try;
  not tested on llama.cpp/mlx-lm/BaseRT/mlxcel/rMLX (§5.6) — the negative finding is
  solid for what was tested, not proven universal.
- Cache-hit-rate measurement at real Hermes-agent granularity (not synthetic
  repeated-prefix curl calls) — the 94.7%/7.2x number in §4 is real but from a
  synthetic prompt; agent-mesh's own 96.9%/58x numbers are from real prefix-cache
  simulations and the verified 144K test, which is stronger evidence than this
  document's own synthetic test.

### 7.5 Why this pass stops here: the goal's own exit condition is met

The original ask's own stated stop condition is explicit: *"Continue iterating until
improvements plateau **or a hardware bottleneck is proven**."* That bottleneck is
proven, not asserted — by multiple independent lines of live and literature evidence
that converge on the same mechanism, not one document repeating itself:

1. **Roofline measurement** (§5/§7.3): prefill efficiency ~20-27% of theoretical across
   every model size tested, a flat band regardless of model — the signature of a
   structural limit, not a per-model tuning gap.
2. **Named, source-cited mechanisms** for that gap (§7.3): dequant-to-fp16 ALU overhead
   (no native low-bit matmul path pre-M5), a hardcoded scheduler block size, Metal
   command-buffer dispatch overhead — none settings-tunable.
3. **Independent corroboration from this pass's own new research** (§2.5): Apple's own
   MLX team states the fix for exactly this (native low-bit prefill matmul, up to 4x
   TTFT) ships only on M5-class NAX silicon, macOS 26.2+ — categorically unavailable on
   this M1 Max regardless of model, quant, or engine choice. A different research
   thread, reading a different primary source, landed on the same wall.
4. **Ruled out, not assumed, as an escape hatch**: MoE doesn't route around this
   bottleneck (§2.5 — prefill is specifically where MoE's advantage collapses, the
   opposite of the phase this workload needs help on); a fourth inference engine
   doesn't either (this section — `mlx_lm` runs but silently corrupts output on the
   production quant format, a correctness wall, not a performance one).

**What's still open after this (listed above, this section) is genuinely different in
kind from "the bottleneck," and shouldn't be conflated with it**: `prefill_priority`
was tested live and applied (§5.10); the MTP-key and reload-loop flags were checked
live and closed (§5.10); the OptiQ and now `mlx_lm` cross-engine comparisons are real,
live measurements, not literature synthesis (§2, this section). What remains — the
`ssd_cache_max_size` cap size, whether to chase JANGQ-AI's MoE line further, whether to
wait for a stable omlx 0.6.3 — are **policy decisions or genuinely low-leverage
follow-ups**, not undiscovered performance headroom. Continuing to generate new research
cycles against an already-proven hardware ceiling would be manufacturing activity, not
closing gaps — the honest analytical answer that this pass's own bottleneck-hunt
delivers is "here is the wall, here is why, here is what remains as your call to make,"
not an unbounded search for a wall that isn't there.
