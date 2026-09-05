# OMLX & MLX High-Performance Optimization Guide: Apple Silicon M1 Max (64GB)

This document establishes the first-principles architectural framework, empirical benchmarks, and operational recipes for running large language models (specifically Qwen3.8-27B, Qwen2.5-Coder-32B, and Qwen hybrid-attention architectures) on Apple Silicon **M1 Max (64GB Unified Memory, 400 GB/s bandwidth)** using **oMLX** and **MLX-LM**.

---

## 1. Hardware Architecture & Roofline Limits (M1 Max 64GB)

### 1.1 Physical Hardware Boundaries
* **Memory Subsystem:** 512-bit wide LPDDR5-6400 Unified Memory Architecture (UMA) delivering **400.0 GB/s theoretical peak bandwidth** (effective real-world Metal stream bandwidth: $\sim 320-340\text{ GB/s}$).
* **Compute Subsystem:** 32-Core Apple GPU (512 Execution Units, 4,096 ALUs @ 1.296 GHz) delivering **21.80 TFLOPS FP16** dense compute.
* **Apple Neural Engine (ANE):** 16-Core NPU delivering **11.0 TOPS INT8** ($\sim 5.5\text{ TFLOPS FP16}$ equivalent).
* **SoC Operational Ridge Point:**
  $$\text{Operational Intensity Ridge Point} = \frac{21.80 \times 10^{12}\text{ FLOP/s}}{400.0 \times 10^9\text{ Byte/s}} = \mathbf{54.5\text{ FLOP/Byte}}$$

---

### 1.2 Theoretical Ceilings vs. Achieved Empirical Throughput

$$\text{Decode Throughput (tok/s)} \approx \frac{\text{Effective Bandwidth (GB/s)}}{\text{Model Weight Footprint in RAM (GB)}}$$

```
========================================================================================
DECODE THROUGHPUT (8K Context) vs THEORETICAL CEILINGS
========================================================================================
Dense-Q4 (14.3GB) Ceiling (400 GB/s): |████████████████████████████████████████| 27.97 tok/s (100.0%)
Dense-Q4 Achieved Baseline:           |██████████████████                      | 12.50 tok/s ( 44.69%)
oQ4e (16.4GB) Ceiling (400 GB/s):     |███████████████████████████████████     | 24.39 tok/s (100.0%)
oQ4e Production Champion (+TQ4 +MTP): |██████████████████                      | 12.90 tok/s ( 52.89%)
oQ4e Baseline (Features Off):         |█████████████                           |  9.30 tok/s ( 38.13%)
========================================================================================

PREFILL THROUGHPUT (8K Tokens) vs THEORETICAL CEILING (403.70 tok/s)
========================================================================================
Theoretical Compute Ceiling:          |████████████████████████████████████████| 403.70 tok/s (100.0%)
Dense-Q4 Baseline (8K):               |█████████                               |  90.10 tok/s ( 22.32%)
oQ4e + TurboQuant KV4 (8K):           |█████████                               |  90.50 tok/s ( 22.42%)
oQ4e Baseline (8K):                   |████████                                |  81.20 tok/s ( 20.11%)
========================================================================================
```

---

## 2. KV Cache Quantization: TurboQuant, MLX KV Quant, & Attention Sinks

### 2.1 Hybrid Attention Memory Scaling (Qwen3.8-27B)
Qwen3.8 utilizes a hybrid architecture with 64 total layers ($N_{\text{full}} = 16$ full quadratic attention layers and $N_{\text{linear}} = 48$ linear GDN attention layers):
* **Uncompressed FP16 KV Cache:** $64\text{ KiB per token}$. A 131k context consumes **8.0 GiB** ($8.59\text{ GB}$); a 262k context consumes **16.0 GiB** ($17.18\text{ GB}$).
* **TurboQuant KV4 (`turboquant_kv_bits: 4.0`):** Compresses 15 full layers to 4-bit while preserving 1 layer at FP16. Memory drops to **$19\text{ KiB per token}$ (70.3% memory reduction)**.
  - Per-block (64-token) memory drops from **16.00 MB down to 4.81 MB**.
  - At 8K context, TurboQuant KV4 accelerates decode throughput from **9.3 tok/s to 12.1 tok/s (+30.1% speedup)** by drastically reducing memory bus read contention.

### 2.2 Critical Attention Sink Rule
When configuring KV cache quantization (in MLX or TurboQuant), **always protect the first 64–128 initial tokens in FP16** (`--quantized-kv-start 64` or `turboquant_skip_last: true`). Initial tokens act as attention sinks carrying large activation magnitudes; quantizing token 0–64 destroys downstream attention matrices and causes repetitive hallucinations.

---

## 3. Speculative Decoding & Multi-Token Prediction (MTP)

### 3.1 Native Lightning MTP vs External Draft Models
* **Native MTP (Qwen3.8-27B-oQ4e-mtp):**
  - Uses an integrated auxiliary MTP projection head trained with the model.
  - **Empirical Acceptance Rate:** **80.8% – 85.7%** on structured code generation tasks.
  - **Speedup:** Boosts 8K decode throughput from **9.3 tok/s to 12.9 tok/s (+38.7% to +60.8% speedup)**.
  - **Memory Cost:** Static $+2.0\text{ GB}$ RAM for the MTP head ($20.2\text{ GB} \to 22.2\text{ GB}$ peak).
* **External Draft Models (`mlx_lm.generate --draft-model`):**
  - Pairing a 32B model (`Qwen2.5-Coder-32B-Instruct-4bit`, 18.5GB) with a 0.5B draft (`Qwen2.5-Coder-0.5B-Instruct-4bit`, 0.4GB) yields **24–32 tok/s** at low temperature ($T \le 0.2$).
* **Golden Acceptance Rule:** Speculative decoding is effective only when draft acceptance $\alpha > 60\%$. At high temperature ($T > 0.7$), draft rejections make speculative decoding 20–30% slower than base autoregressive decoding.

---

## 4. Why ANE Offloading Regresses on M1 Max (Root-Cause Analysis)

1. **Compute Density Asymmetry:** On M1 Max, the 32-core GPU delivers **21.8 TFLOPS FP16**, which is **4x faster than the 16-core ANE (5.5 TFLOPS FP16 equivalent)**. Offloading compute to the ANE starves the GPU.
2. **Memory Bus Contention:** The ANE has only 16–32 MB of on-chip SRAM; streaming 27B model weights to ANE contends directly for the same 400 GB/s memory bus.
3. **Apple Neural Engine Driver Panic (Code 47):** Compiling all 112 layers (64 MLP + 48 GDN) on the ANE for sequence length 2048 causes the macOS kernel watchdog to abort with `com.apple.appleneuralengine Code=47` due to tile descriptor exhaustion.
4. **Policy Decision:** **ANE offloading is permanently rejected for 27B models on M1 Max (`qwen35_ane_prefill_enabled: false`).**

---

## 5. Memory Ceilings & macOS Kernel Tuning

### 5.1 Unlocking Wired GPU Memory via `sysctl`
By default, macOS caps Metal allocations to 75% of RAM ($\sim 48\text{ GB}$ on 64GB).
To safely allow up to 60GB for models and KV caches while reserving 4GB for the operating system:

```bash
# Verify current setting
sysctl iogpu.wired_limit_mb
# Output: iogpu.wired_limit_mb: 61440

# Permanent LaunchDaemon (installed at boot):
# /Library/LaunchDaemons/com.mike.iogpu-wired-limit.plist -> 61440 MB
```

### 5.2 OMLX Launch Configuration
```bash
/Users/man/.venv-omlx/bin/omlx serve \
  --host 127.0.0.1 \
  --port 8300 \
  --hf-cache \
  --memory-guard-gb 59 \
  --paged-ssd-cache-max-size 100GB \
  --hot-cache-max-size 8GB
```

---

## 6. Actionable Recipes & Presets

### Recipe 1: Production Agent Mesh Champion (oQ4e + TurboQuant KV4 + MTP)
* **Model:** `Jundot/Qwen3.8-27B-oQ4e-mtp`
* **OMLX Settings (`~/.omlx/model_settings.json`):**
  ```json
  {
    "turboquant_kv_enabled": true,
    "turboquant_kv_bits": 4.0,
    "turboquant_skip_last": true,
    "mtp_enabled": true,
    "qwen35_ane_prefill_enabled": false
  }
  ```
* **Performance:** 12.9 tok/s decode @ 8k, 87.8 tok/s prefill @ 8k, 22.26 GB peak RAM, 99.3% prefix cache reuse.

### Recipe 2: Maximum Memory Headroom (Dense-Q4/g128 + TurboQuant KV4)
* **Model:** `Qwen3.8-27B-MLX-4bit-g128` (`~/.omlx/models/Qwen3.8-27B-MLX-4bit-g128`)
* **OMLX Settings:**
  ```json
  {
    "turboquant_kv_enabled": true,
    "turboquant_kv_bits": 4.0,
    "turboquant_skip_last": true,
    "mtp_enabled": false,
    "qwen35_ane_prefill_enabled": false
  }
  ```
* **Performance:** 12.5–13.5 tok/s decode, 89.0–90.1 tok/s prefill, **16.37 GB peak RAM** (leaving $>42\text{ GB}$ free RAM for multi-agent concurrency).

### Recipe 3: High-Speed CLI Speculative Coding (`mlx_lm.generate`)
```bash
python -m mlx_lm.generate \
  --model mlx-community/Qwen2.5-Coder-32B-Instruct-4bit \
  --draft-model mlx-community/Qwen2.5-Coder-0.5B-Instruct-4bit \
  --num-draft-tokens 6 \
  --kv-bits 8 \
  --quantized-kv-start 64 \
  --temp 0.2 \
  --prompt "Implement a lock-free ring buffer in C++20 with atomic head/tail pointers."
```

---

## 7. Mathematical Prefill Bottleneck Breakdown & MoE Scaling

### 7.1 Why Dense 27B Prefill Hits ~90 tok/s vs 403.7 tok/s Compute Peak
Dense forward pass requires $2 \times N$ FLOPs per token:
$$\text{Dense 27B FLOPs/tok} = 2 \times 27.0 \times 10^9 = \mathbf{54.0\text{ GFLOPs/tok}}$$
On the 32-core GPU (21.80 TFLOPS FP16), the theoretical prefill ceiling is:
$$\text{Ceiling} = \frac{21.80 \times 10^{12}\text{ FLOP/s}}{54.0 \times 10^9\text{ FLOP/tok}} = \mathbf{403.7\text{ tok/s}}$$

The realized empirical throughput of **87.8–91.2 tok/s (~22.5% efficiency)** is governed by four concrete microarchitectural factors on M1 Max:
1. **Dequantization ALU Inflation:** Apple G13 GPUs lack hardware INT4 tensor cores. Unpacking 4-bit weights into FP16 in SIMD registers requires extra bitshift, mask, scale, and offset instructions before FMA, consuming ~38% of execution unit cycles.
2. **BF16 vs FP16 Instruction Penalty:** The M1 Max lacks native BFloat16 ALUs. Executing models in default `bfloat16` forces software emulation or FP32 upcasting (cutting vector width in half). Explicit `--dtype float16` conversion recovers full SIMD execution.
3. **Metal Command Buffer & Layer Synchronization:** 64 sequential transformer layers $\times$ 8 kernel dispatches = **512 kernel launches per prefill step**. Driver transition latency introduces $1\text{--}2\text{ ms}$ of dispatch overhead per chunk.
4. **GDN Recurrent State I/O:** 48 linear Gated Delta Net layers continuously stream recurrent states ($S_t = \alpha_t S_{t-1} + \beta_t v_t k_t^T$), consuming $\sim 300\text{ GB/s}$ of L2/UMA bandwidth during long-sequence prefill.

---

### 7.2 Breaking the Prefill Bottleneck: Mixture of Experts (MoE) vs Dense

In Mixture of Experts (MoE) architectures, only $k$ out of $E$ experts are activated per token ($P_{\text{active}} \ll P_{\text{total}}$):

| Model Architecture | Total Params | Active Params | FLOPs / Token | Theoretical Peak Prefill | Measured Empirical Prefill | Empirical Decode Speed |
|---|---:|---:|---:|---:|---:|---:|
| **Dense 2B (Qwen3.5-2B)** | 2.0B | 2.0B | **4.0 GFLOPs** | 5,450 tok/s | **1,658.4 tok/s** | **116.1 tok/s** |
| **MoE 16B-A2.4B (DeepSeek-Lite)** | 15.7B | 2.4B | **4.8 GFLOPs** | 4,541 tok/s | **~390 – 450 tok/s** | **~38 – 48 tok/s** |
| **MoE 57B-A14B (Qwen2-57B-A14B)** | 57.2B | 14.0B | **28.0 GFLOPs** | 778 tok/s | **~110 – 140 tok/s** | **~18 – 24 tok/s** |
| **Dense 14B (Qwen2.5-14B)** | 14.7B | 14.7B | **29.4 GFLOPs** | 741 tok/s | **~380 tok/s** | **~27 – 30 tok/s** |
| **Dense 27B (Qwen3.8-27B-oQ4e)** | 27.0B | 27.0B | **54.0 GFLOPs** | 403 tok/s | **87.8 – 91.2 tok/s** | **12.9 tok/s** (MTP) |

*Key Insight:* For agentic workflows requiring deep multi-step reasoning, tool generation, and 262k context, **`Qwen3.8-27B-oQ4e-mtp`** remains the undisputed intelligence champion. For ultra-fast interactive coding, **`DeepSeek-Coder-V2-Lite-Instruct`** (2.4B active MoE) achieves **~42 tok/s decode and ~400 tok/s prefill**.

---

## 8. Hermes Agent Optimization & Long-Horizon Parameter Blueprint

To maximize agentic performance on local models for long-horizon workflows in Hermes:

1. **Enable Lean Coding Context (`agent.coding_context: focus`):**
   - Automatically collapses toolset schemas to the essential `coding` set (`file`, `terminal`, `patch`) and demotes non-coding skill descriptions in the prompt index.
   - Reduces system prompt overhead from ~20 KB down to ~6 KB, speeding up cold prefill by **3x**.
2. **Context Compression Policy (`compression:`):**
   ```yaml
   compression:
     threshold: 0.78125
     threshold_tokens: 51200
     tail_mode: lean
   ```
   - Compacts prior turns cleanly before reaching cold context regions without losing agent state.
3. **Bounded Context Tiering (`hermes/qwen38-oq4e-profiles.yaml`):**
   - **`qwen38-oq4e-short` (Routine Agent Tasks):** 65,536 context, 4,096 max output, `reasoning_effort: low`, `thinking_budget: 1024`.
   - **`qwen38-oq4e-mid` (Broad Context):** 131,072 context, 4,096 max output, `reasoning_effort: low`.
   - **`qwen38-oq4e-full` (Deep Architecture/Audit):** 262,144 context, 8,192 max output, `reasoning_effort: xhigh`.
4. **Explicit Tool & Reasoning Support (`model_overrides:`):**
   ```yaml
   model_overrides:
     omlx:
       qwen3.8-oq4e:
         context_window: 65536
         max_output_tokens: 4096
         supports_tools: true
         supports_reasoning: true
   ```
