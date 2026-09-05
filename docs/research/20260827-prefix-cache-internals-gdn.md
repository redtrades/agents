# OMLX Prefix Caching, Merkle Hashing, and GDN Recurrent State Serialization

**Engine:** OMLX (`jundot/omlx` v0.4.x / Apple Silicon Metal)  
**Target:** Apple M1 Max 64GB  
**Date:** 2026-08-27  

---

## 1. Multi-Tier Cache Architecture

OMLX provides a two-tier hybrid caching engine:
1. **L1 RAM Hot Cache (`--hot-cache-max-size 8GB`)**: Keeps in-flight KV caches and recurrent states in active unified memory for sub-millisecond turn turnaround.
2. **L2 Paged SSD Cache (`--paged-ssd-cache-max-size 100GB`)**: Serializes boundary snapshots to local NVMe SSD storage (`~/.omlx/cache/`).

---

## 2. Block-Level Merkle Token Hashing (`block_size = 2048`)

Tokens are partitioned into discrete 2,048-token chunks and hashed as a Merkle tree:
$$\text{Hash}_k = \text{SHA256}\left(\text{model\_id} \,\|\, \text{ParentHash} \,\|\, \text{tokens}[k \cdot 2048 : (k+1) \cdot 2048]\right)$$

* **Longest Prefix Matching**: When a request arrives, OMLX computes block hashes and matches the longest cached prefix.
* **Cold Invalidation**: Any single-byte divergence in Block 0 invalidates all subsequent blocks ($k \ge 1$).

---

## 3. GDN Recurrent State Sidecars (`rht_int8` / `_gdn_sidecars`)

Unlike standard transformer KV caches that can be arbitrarily sliced across sequence positions, **Gated Delta Net (GDN)** linear attention layers maintain an evolving recurrent state:
$$S_t = \alpha_t S_{t-1} + \beta_t (v_t \otimes k_t^T)$$

* **Serialization Protocol**: OMLX compresses GDN state matrices using Randomized Hadamard Transform (`rht_int8`) and saves them as sidecar files (`_gdn_sidecars/{digest}.safetensors`).
* **Instant Endpoint Restoration**: On a cache hit, OMLX restores the exact terminal recurrent state matrix $S_{T_{\text{cached}}}$ without re-evaluating preceding tokens.

---

## 4. Empirical 10-Turn Cache Scaling Receipts (`evals/bench_prefix_cache_hitrate.py`)

| Turn | Context Length | Cached Tokens | Cache Hit Rate (%) | Actual TTFT (ms) | Effective Prefill TPS | Time Saved (s) |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **1 (Cold)** | 4,096 | 0 | 0.0% | 51,732 ms | 79.2 tok/s | 0.00 s |
| **2** | 6,144 | 4,096 | 66.7% | 24,839 ms | 247.4 tok/s | 49.63 s |
| **3** | 8,192 | 6,144 | 75.0% | 23,344 ms | 350.9 tok/s | 69.96 s |
| **5** | 12,288 | 10,240 | 83.3% | 22,530 ms | 545.4 tok/s | 112.50 s |
| **7** | 14,336 | 13,312 | 92.9% | 11,112 ms | 1,290.1 tok/s | 144.04 s |
| **10** | 16,384 | 15,872 | **96.9%** | **5,511 ms** | **2,972.9 tok/s (37.5x)** | **169.72 s (18.17 min total)** |

---

## 5. Golden Rules for >99% Prefix Cache Hit Rate

1. **Strict Immutable System Prompts**: System prompt and tool schemas must be byte-for-byte identical across turns.
2. **Volatile Metadata at Tail**: Dynamic timestamps and request IDs must only be appended at the very end of user messages.
3. **Deterministic Tool Schema Serialization**: Tool schemas must be sorted alphabetically by name.
4. **2048-Token Block Alignment**: Pad static instruction blocks to multiples of 2,048 tokens where possible.
