# Comprehensive Comparative Research: Apple Silicon Inference Engines

**Target Architecture:** Apple Silicon M1 Max (10-core CPU, 32-core GPU, 16-core ANE, 64 GB Unified Memory @ 400 GB/s)  
**Evaluated Engines:** **oMLX**, **mlx-lm**, **vMLX (vllm-mlx)**, **llama.cpp (llama-server)**  
**Date:** 2026-08-27  

---

## Executive Summary & Feature Support Matrix

| Feature / Capability | **oMLX** (`jundot/omlx`) | **mlx-lm** (`ml-explore`) | **vMLX / vllm-mlx** | **llama.cpp** (`llama-server`) |
| :--- | :--- | :--- | :--- | :--- |
| **Multi-Token Prediction (MTP)** | **Native Integrated** (Auxiliary Lightning MTP heads, ~80.8–85.7% accept rate) | Draft-model speculative decoding only (`--draft-model`) | Draft-model speculative decoding & token trees | Draft models (`-md`) + native DeepSeek/Qwen MTP support |
| **KV Cache Quantization** | **TurboQuant KV4** (4.0-bit, skip-last FP16 attention sinks, 70.3% KV memory drop) | Native `--kv-bits 4/8` + `--quantized-kv-start 64` (PR #1353) | Mixed-precision / 4-bit / 8-bit paged KV blocks (JANGTQ / OptiQ) | Asymmetric `-ctk` / `-ctv` (`q8_0`, `q4_0`, `iq4_nl`, `f16`) + FlashAttention (`-fa`) |
| **Prefix / Prompt Caching** | **Radix/Trie multi-turn cache** with explicit server telemetry (`prompt_tokens_details.cached_tokens`) & `preserve_mid_system_cache` | In-memory LRU prompt cache (`--prompt-cache-size` / CLI `--prompt-cache-file`) | Trie-based Automatic Prefix Caching (APC) + multimodal token caching | Host RAM prefix cache (`--cache-prompt`) + KV-shift non-prefix reuse (`--cache-reuse`) |
| **Persistent SSD vs RAM Caching (GDN State Sidecars)** | **Tiered L1 RAM (8GB) + L2 SSD (100GB)**; caches GDN linear recurrent state sidecars ($S_t$) alongside KV blocks | **RAM only**; in-flight recurrent state calculation without native disk persistence | **L1 Paged + L2 Disk Cache**; session state disk persistence | **RAM slots + Disk Slot Save/Restore** (`--slot-save-path` + `POST /slots/{id}?action=save`) |
| **Continuous Batching & Concurrency** | Chunked prefill scheduler (`prefill_step_size=8192`), adaptive throttle (`context` vs `speed` priority), 1–3 agents | Basic multi-request batching / queueing; limited dynamic chunked prefill | High-throughput iteration-level continuous batching scheduler (`--continuous-batching`) | Production-grade continuous batching (`-cb`, `-np N` slots, chunked `-b`/`-ub`) |
| **Primary Strength** | Hybrid linear/attention models (Qwen3.8), long-context agent loops, native MTP | Official reference MLX, rapid upstream support, lightweight CLI/Python API | High-concurrency multi-tenant serving, vLLM API parity on Apple Silicon | Maximum ecosystem portability, GGUF ecosystem, lowest CPU/RAM overhead |

---

## 1. Deep-Dive Feature Analysis

### 1.1 Multi-Token Prediction (MTP) & Speculative Decoding
* **oMLX (Production Winner on Qwen3.8):** Supports model-native auxiliary MTP prediction heads trained with the base model (e.g., `Jundot/Qwen3.8-27B-oQ4e-mtp`).
  - *Mechanism:* Simultaneously predicts token $N$ and token $N+1$ in a single forward step.
  - *Empirical Performance:* Achieves **80.8% to 85.7% speculative acceptance** on structured coding and Hermes tool calls, boosting 8K decode throughput from **9.3 tok/s to 12.9 tok/s (+38.7% to +60.8% speedup)** with only $+2.0\text{ GB}$ static RAM overhead.
* **mlx-lm:** Supports classical speculative decoding via dual-model pairing (`--draft-model`).
  - *Golden Pairing:* Pairing `Qwen2.5-Coder-32B-Instruct-4bit` (18.5 GB) with `Qwen2.5-Coder-0.5B-Instruct-4bit` (0.4 GB) with `--num-draft-tokens 6` achieves **24–32 tok/s** at low temperature ($T \le 0.2$).
  - *Caveat:* If acceptance rate drops below $\sim 60\%$ (e.g., high-entropy creative tasks, $T > 0.7$), speculative verification overhead degrades performance by 20–30%.
* **llama.cpp:** Features mature speculative decoding (`-md` / `--draft-max` / `--draft-min`) as well as prompt-lookup speculative decoding (`--lookup-cache`), generating speculative tokens directly from matching n-grams in the input context without requiring an auxiliary model.

---

### 1.2 KV Cache Quantization & Attention Sinks
* **Hybrid Attention Scaling (Qwen3.8-27B):** 64 total layers with 16 full-quadratic attention layers and 48 linear GDN layers. Uncompressed FP16 KV cache consumes **$64\text{ KiB per token}$** ($16.0\text{ GiB}$ at 262k context).
* **TurboQuant KV4 in oMLX:**
  - Quantizes 15 of 16 full-attention layers down to 4.0 bits while preserving 1 layer at FP16 (`turboquant_kv_bits: 4.0`).
  - Reduces per-token KV footprint from **$64\text{ KiB}$ to $19\text{ KiB}$ (70.3% memory reduction)**.
  - At 8K context, decode speed increases from **9.3 tok/s to 12.1 tok/s (+30.1% speedup)** by dramatically reducing memory bus saturation on the 400 GB/s bus.
* **The Attention Sink Law (`--quantized-kv-start 64` / `turboquant_skip_last: true`):**
  - Tokens 0–64/128 act as massive activation sinks carrying high-magnitude softmax anchors.
  - Quantizing tokens 0–64 destroys downstream attention maps, resulting in immediate repetition loops and hallucinations. **Both oMLX and mlx-lm must protect the initial 64 tokens in FP16.**
* **llama.cpp Asymmetrical Cache Quantization:** Allows separate Key and Value quantization (`-ctk q8_0 -ctv q4_0` or `-ctk q4_0 -ctv q4_0`), enabling fine-grained quality vs memory trade-offs when combined with Metal FlashAttention (`-fa`).

---

### 1.3 Prefix Caching across Multi-Turn Agent Conversations
* **Empirical Multi-Turn Scaling (10-turn Hermes Agent Replay):**
  - **Turn 1 (Cold 4,096 tokens):** 4,096 tokens prefilled at **79.2 tok/s** (51.7s TTFT).
  - **Turn 10 (Warm 16,384 tokens):** 15,872 cached tokens (**96.9% cache hit rate**); only 512 delta tokens prefilled. TTFT drops to **5.5s** (**2,972.9 effective tok/s**, a **37.5x speedup**).
  - **Cumulative Savings:** Over 10 turns, prefix caching saves **1,089.9 seconds (18.17 minutes)** of latency.
  - **Full Document Test (144,364 tokens):** Cold run takes 3,065.16s; warm rerun completes in 52.94s (**~58x speedup**) with 143,360 server-verified cached tokens (99.3% reuse).
* **Engine Comparison:**
  - *oMLX:* Automatic longest-prefix matching with explicit server-side cached token telemetry returned in the OpenAI completion response (`usage.prompt_tokens_details.cached_tokens`).
  - *vMLX / vllm-mlx:* Radix-tree based shared prefix cache across multiple concurrent requests with multimodal vision token prefix caching.
  - *llama.cpp:* Slot-based host RAM caching (`--cache-prompt`) with KV-shift reuse (`--cache-reuse 2048`) for partially shifted conversation prompts.

---

### 1.4 Persistent SSD vs RAM Caching of Hybrid Recurrent Attention (GDN State Sidecars)
* **Gated Delta Networks (GDN) Architecture:**
  - Used in Qwen3.8 / hybrid linear-attention models to maintain a fixed-size recurrent state:
    $$S_t = \alpha_t S_{t-1} + \beta_t v_t k_t^T$$
  - GDN layers have $O(1)$ constant memory scaling relative to sequence length, but streaming recurrent states consumes $\sim 300\text{ GB/s}$ of L2/UMA memory bandwidth during prefill.
* **Tiered Storage Implementations:**
  - **oMLX:** Implements a two-tier architecture: **L1 Hot RAM Cache** (`--hot-cache-max-size 8GB`) + **L2 Paged SSD Cache** (`--paged-ssd-cache-max-size 100GB`, `ssd_cache_dir`). GDN linear attention recurrent state matrices ($\sim 64\text{ KB}$ per layer) are serialized alongside KV blocks into paged disk storage. When restoring a session, GDN recurrent states are restored without re-evaluating preceding tokens.
  - **llama.cpp:** Persists recurrent and KV slot states via the slot API (`POST /slots/{id}?action=save&filename=slot_0.bin`), enabling durable disk checkpoints across server restarts.
  - **mlx-lm:** Purely in-memory; loses active recurrent states upon process termination.

---

## 2. Hardware Architecture & Bottleneck Analysis (M1 Max 64GB)

### 2.1 Hardware Operational Limits
* **Bandwidth:** 512-bit LPDDR5-6400 UMA delivering **400.0 GB/s peak bandwidth** ($\sim 320–340\text{ GB/s}$ real Metal streaming bandwidth).
* **GPU Dense Compute:** 32 cores delivering **21.80 TFLOPS FP16**.
* **Apple Neural Engine (ANE):** 16 cores delivering **11.0 TOPS INT8** ($\sim 5.5\text{ TFLOPS FP16}$ equivalent).
* **SoC Ridge Point:** $\frac{21.80\text{ TFLOPS}}{400.0\text{ GB/s}} = \mathbf{54.5\text{ FLOP/Byte}}$.

### 2.2 Why Dense 27B Prefill Hits ~90–108 tok/s vs 403.7 tok/s Peak
1. **Dequantization ALU Overhead:** Apple G13 GPUs lack INT4 tensor hardware. Unpacking 4-bit weights into FP16 registers consumes $\sim 38\%$ of GPU ALU cycles.
2. **BF16 Emulation Penalty:** M1 Max lacks native BFloat16 ALUs. Running models in default `bfloat16` cuts SIMD throughput in half; converting to `--dtype float16` restores full SIMD speed (**108.1 tok/s vs 82.4 tok/s prefill, +31.2% speedup**).
3. **Metal Command Buffer Dispatch Overhead:** 64 transformer layers $\times$ 8 dispatches = 512 kernel launches per chunk ($1–2\text{ ms}$ driver dispatch latency).
4. **Apple Neural Engine (ANE) Rejection:**
   - On M1 Max, the GPU is **4x faster than the ANE** (21.8 TFLOPS vs 5.5 TFLOPS).
   - Offloading 27B models across sequence lengths $\ge 2048$ triggers macOS watchdog driver crashes (`com.apple.appleneuralengine Code=47`).
   - **Rule:** ANE offloading is permanently disabled on 27B+ models on M1 Max.

---

## 3. Engine-Specific Launch Flags & Optimal Configurations for M1 Max 64GB

### 3.1 Host OS Preparation (Mandatory for all engines)
```bash
# Unlock up to 60GB wired GPU allocation (default is 75% / 48GB)
sudo sysctl -w iogpu.wired_limit_mb=61440

# Verify configuration
sysctl iogpu.wired_limit_mb
```

---

### 3.2 Engine 1: oMLX (Production Champion for Agent Mesh)
```bash
/Users/man/.venv-omlx/bin/omlx serve \
  --host 127.0.0.1 \
  --port 8300 \
  --hf-cache \
  --memory-guard-gb 59 \
  --paged-ssd-cache-max-size 100GB \
  --hot-cache-max-size 8GB \
  --prefill-step-size 8192 \
  --max-num-batched-tokens 16384
```

---

### 3.3 Engine 2: mlx-lm (`mlx_lm.server`)
```bash
python -m mlx_lm.server \
  --model mlx-community/DeepSeek-Coder-V2-Lite-Instruct-4bit \
  --host 127.0.0.1 \
  --port 8000 \
  --kv-bits 4 \
  --quantized-kv-start 64 \
  --max-kv-size 32768 \
  --cache-memory-percent 85
```

---

### 3.4 Engine 3: llama.cpp (`llama-server`)
```bash
./llama-server \
  -m models/qwen2.5-coder-32b-instruct-q4_k_m.gguf \
  -md models/qwen2.5-coder-0.5b-instruct-q4_k_m.gguf \
  --host 127.0.0.1 \
  --port 8080 \
  -c 65536 \
  -ngl 99 \
  -fa \
  -ctk q8_0 \
  -ctv q4_0 \
  -cb \
  -np 4 \
  -b 2048 \
  -ub 512 \
  --cache-prompt \
  --cache-reuse 2048 \
  --cache-ram 8192 \
  --slot-save-path /Users/man/.llama_slots
```
