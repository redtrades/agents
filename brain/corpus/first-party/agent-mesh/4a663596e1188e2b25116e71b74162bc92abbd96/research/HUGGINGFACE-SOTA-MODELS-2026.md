# Hugging Face SOTA Model Architecture Analysis for Apple Silicon (2026)

**Target:** Apple Silicon M1 Max 64GB  
**Date:** 2026-08-27  

---

## 1. Evaluated Candidate Models on Hugging Face

### 1. `mlx-community/DeepSeek-Coder-V2-Lite-Instruct-4bit` (MoE Champion)
* **Architecture**: Mixture of Experts (15.7B Total / 2.4B Active Parameters).
* **Quantization**: 4-bit affine quantization (~9.2 GB VRAM).
* **Context Window**: 128k context.
* **Measured M1 Max Performance**:
  - **1K Prefill Throughput**: **668.95 tok/s**
  - **Decode Throughput**: **85.63 tok/s**
  - **Total 1K Latency**: **1.94 seconds**
* **Best Role**: High-speed autonomous code generation, refactoring, and test suite execution (Forge Persona).

---

### 2. `Jundot/Qwen3.8-27B-Instruct-oQ4-MTP-mlx` (Dense Intelligence Champion)
* **Architecture**: 27.0B Dense Hybrid (SSM + Attention) with auxiliary Multi-Token Prediction draft head.
* **Quantization**: oMLX mixed-precision 4-bit (~16.5 GB VRAM).
* **Context Window**: 262k context.
* **Measured M1 Max Performance**:
  - **1K Prefill Throughput**: **80.8 tok/s** (Cold) / **2,972.9 tok/s** (Warm Cached)
  - **Decode Throughput**: **14.6 tok/s** (with TurboQuant KV4 + Lightning MTP)
  - **Speculative Draft Acceptance**: **84.0%**
* **Best Role**: Lead orchestrator, high-level task decomposition, long-horizon planning (Prime Persona).

---

### 3. `mlx-community/Qwen2.5-Coder-7B-Instruct-4bit` (Audit Champion)
* **Architecture**: 7.6B Dense Code Model.
* **Quantization**: 4-bit (~5.1 GB VRAM).
* **Context Window**: 128k context.
* **Measured M1 Max Performance**:
  - **1K Prefill Throughput**: **180.44 tok/s**
  - **Decode Throughput**: **21.98 tok/s**
  - **Total 1K Latency**: **7.18 seconds**
* **Best Role**: Blind council reviewer, syntax/lint checking, and fast security scanning (Sentinel Persona).

---

### 4. `mlx-community/Qwen3.5-2B-MLX-4bit` (Event Loop Champion)
* **Architecture**: 2.0B Dense Fast Baseline.
* **Quantization**: 4-bit (~2.1 GB VRAM).
* **Measured M1 Max Performance**:
  - **1K Prefill Throughput**: **1,495.6 tok/s**
  - **Decode Throughput**: **85.3 tok/s**
  - **Total 1K Latency**: **0.68 seconds**
* **Best Role**: Fast file searches, git operations, and lightweight background cron event loops (Scout / Operator Persona).
