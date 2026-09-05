# Qwen3.8-Flash-Next Apple Silicon evidence — 2026-08-27

## Scope and provenance

This note reconciles the X/article synthesis supplied by Mike on 2026-08-27
with the local M1 Max experiment. Claims in the external table below were
extracted from that supplied synthesis; they were not independently reproduced
on this host. Local acceptance still requires repository receipts.

## Useful external evidence

| Source | Provenance | Configuration and claim | Local interpretation |
|---|---|---|---|
| [Ikesan M1 Max article](https://lilting.ch/en/articles/qwen38-flash-next-llamacpp-m1max-test) | Reported firsthand, exact M1 Max 64 GB | AtomicChat IQ4 M64, 32K, pre-merge llama.cpp `213df585`; reported `pp512 181.69`, `tg128 17.59`, about 44.3 GiB RSS, and more than 22 GB swap while ComfyUI also used 7.7 GB | Strong feasibility evidence for split-shard PLE paging. It is a stressed floor, not a clean baseline or current lazy-read receipt. |
| [AtomicChat model card](https://huggingface.co/AtomicChat/Qwen3.8-Flash-Next-GGUF) | Publisher firsthand, M5 Max 64 GB | IQ4: 45.8 GB resident plus 39.1 GB SSD; Q4_K_M: 54.5 GB resident plus 38.4 GB SSD | Packaging, quality, and memory reference only; do not infer M1 throughput or Q4 admission. |
| [OMLX 0.6.3 post](https://x.com/jundotkim/status/2093022104094658562) and [release](https://github.com/jundot/omlx/releases/tag/v0.6.3) | Maintainer firsthand, M3 Ultra 512 GB | Exact Flash-Next oQ4e-MTP with SSD/resident PLE and roughly 73–81 GiB process peaks | Useful engine/cache reference, but current pack is not viable on a 64 GB M1 Max. |
| [Vontra MLX post](https://x.com/ashxhart/status/2092683660071956704) | Reported firsthand, incomplete M3 Ultra configuration | MTP throughput and acceptance claims without RAM, context, full command, or cache state | Insufficient for M1 comparison or promotion. |
| [OMLX issue #3222](https://github.com/jundot/omlx/issues/3222) | Failure report | Concurrent hybrid GDN/QSA cache-corruption handling | Concurrency must follow single-request correctness. |

## Code-version correction

Ikesan's pre-merge `213df585` is not an ancestor of the local pinned merge
`6c84c7d5`. The older tree does not expose the generic
`--tensor-read-lazy` option or mark the PLE tensor with the current lazy tensor
flag. It proves the earlier split-shard mmap approach, not the semantics of the
current explicit-lazy implementation.

The local baseline therefore remains:

- AtomicChat AD-3.84bpw-IQ4_XS-M64;
- merged llama.cpp `6c84c7d5`;
- mmap plus explicit `--tensor-read-lazy on`;
- one server and one slot;
- prompt cache disabled for throughput cells;
- unique input bytes and server-authoritative timings;
- swap delta, memory pressure, ownership, and cleanup evidence.

## Matrix consequences

Keep:

- a one-time lazy `auto` versus explicit `on` equivalence check;
- separate process-cold, filesystem-page-warm, prefix-warm, and
  restart-restored labels;
- a 30-minute sustained IQ4 soak before Q4 promotion;
- save, stop, restart, restore verification with output equivalence;
- correctness and Hermes gates before concurrency.

Defer:

- lazy `off` on the 64 GB host;
- Q4_K_M until IQ4 headroom and soak gates pass;
- OMLX/MTP, VLM, quantized KV, and parallel slots until the single-slot text
  path is correct;
- the historical pre-merge build unless a regression investigation needs it.

## Current local boundary

The first clean short screen established provisional **prefill-only** evidence,
but early EOS meant multiple cells generated fewer than the requested 32
tokens. Those cells are invalid for decode comparison. The campaign must not
declare a winner until the corrected anti-EOS confirmation and later
correctness/cache/Hermes gates pass. Track the live checklist in issue #35.
