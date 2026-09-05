# Jundot Qwen3.8-27B-oQ4e-mtp: Control Architecture and Evidence Boundary

This document corrects the former Flash-Next architecture guide. It describes
the measured Jundot 27B oQ4e route only. It is not a Flash-Next architecture
guide or runtime receipt for the exact Qwen3.8-Flash-Next model.

Status labels are deliberate: **Observed** means a named receipt or source
record was inspected; **Official** means an upstream model identity/manifest
claim; and **Rejected** means the tested configuration crossed a resource or
correctness gate. A result for one engine/model is never transferred to another.

## Current identity boundary

| Claim | Status | Evidence boundary |
|---|---|---|
| `Jundot/Qwen3.8-27B-oQ4e-mtp` is the OMLX route used by the historical receipts. | Observed historical control | The committed receipts identify this 27B dense control. |
| `Qwen/Qwen3.8-Flash-Next` is the exact target model. | Official model contract | `qwen4_exp`; 125B main / 6B active, plus 51B n-gram and 4B MTP parameters. |
| The two identifiers name the same model. | False; superseded | D-030 and D-031 made this incorrect identification. Their 27B measurements remain historical control evidence only. |

The exact-model experiment and completed-result contract is
[`qwen38-flash-next-experiment.yaml`](qwen38-flash-next-experiment.yaml). It
selects an isolated local configuration; it does not rename the 27B control or
make a universal-default claim.

## Historical 27B control evidence

The following records retain their historical meaning: they measure the Jundot
27B oQ4e route through OMLX, not exact Flash-Next.

| Historical artifact | Classification now | What it can support |
|---|---|---|
| `evals/results_qwen38_27b_oq4e_control_2026-08-27.jsonl` | 27B-control evidence; renamed without changing receipt bytes | A past measurement of the Jundot route's cache/latency behavior only. |
| `evals/results_matrix_2026-08-27.jsonl` | 27B-control evidence | A past OMLX feature/performance comparison for the named Jundot checkpoint. |
| OMLX/Hermes setting descriptions formerly in this document | Historical configuration testimony | No claim about exact-model loadability, cache behavior, or promotion. |

The former guide's cache, MTP, switch-latency, memory, and output-token
numbers are deliberately not repeated here as Flash-Next facts. They may be
consulted only through their original receipts with the control label above.

## Engine boundary

### OMLX 0.6.2: 27B cache-performance control

OMLX 0.6.2 is retained as the measured 27B cache-performance control. It is not
an exact-model engine: it cannot establish Flash-Next correctness, context
capacity, tool use, or prompt-state reuse. The 2026-08-28 control gate did prove
8,192-token same-process, cross-request shared-prefix, and restart-restored SSD
reuse for `Jundot--Qwen3.8-27B-oQ4e-mtp` only (adjudicated receipt SHA
`43d57b969858cdb67655cc4e2564e5a71a91a73b31a436bd52fc2671ecc8fa81`).
The Hermes control then completed terminal/read-file tools and exact multi-turn
retention, with 6,144 cached tokens on its warm calls (receipt SHA
`8dd983f93ac987625e42c3a9d2a7fc13f9c087c807e841c69a95dff06b9b101d`).

Current upstream caveats, observed from their issue records:

- [#3176](https://github.com/jundot/omlx/issues/3176): OMLX 0.6.2 does not
  support the exact architecture.
- [#3167](https://github.com/jundot/omlx/issues/3167): Engram SSD offload is
  still open work.
- [#3181](https://github.com/jundot/omlx/issues/3181): `qwen4_exp` produces
  bad output in the reported path.
- [#3182](https://github.com/jundot/omlx/issues/3182): OMLX 0.6.3rc3 has an
  open long-prefix SSD-cache regression; it cannot establish parity for the
  exact-model experiment.

These upstream issues are neither a runtime receipt nor a claim that the
issues apply to every configuration. They block promotion from 27B-control
results to exact-model claims until independently reproduced or resolved.

### Pinned llama.cpp: selected exact-model bridge

The exact baseline uses `ggml-org/llama.cpp` pinned to
`6c84c7d5d8833c6e0df69628f75a0f599797934e`. The selected IQ4 operating point
is 131,072 total context, one slot, 4,096 practical output, mmap plus lazy tensor
reads, Flash Attention, batch 2,048, ubatch 512, all model layers on Metal, and
fitting disabled. This remains an isolated local selection, not a claim of
OMLX SSD prompt-state parity.

The separate PR #26004 test build at
`a0ccc47f540426b6e61841b2000dd2e87e022bab` passed explicit slot-file restart
restore: 8,208 cached prefix tokens plus a four-token checkpoint-tail replay
(receipt SHA
`5429465d690504fbc3409beba3baf259a11017dee59bc78bfed4310749100265`).
That proves functional operator-invoked persistence only. The server did not
automatically restore on startup or share the saved prefix with a new slot, and
the public API cannot prove internal QSA/GDN state identity.

## Exact-model experiment contract

| Field | Contractual value | Status |
|---|---|---|
| Source model | `Qwen/Qwen3.8-Flash-Next` / `qwen4_exp` | Official model identity. |
| GGUF publisher | `AtomicChat/Qwen3.8-Flash-Next-GGUF` at `142262902a46f7daed19c79d0771534c8106ad59` | Pinned source. |
| Artifact root | `/Users/man/models/qwen38-flash-next` | Actual root; variants use subdirectories. |
| Selected variant | `Qwen3.8-Flash-Next-AD-3.84bpw-IQ4_XS-M64`: 28 shards, 84,930,924,160 bytes | Passed direct and Hermes correctness, 128K recall, output, cache, and bounded concurrency gates. |
| Rejected variant | `Qwen3.8-Flash-Next-AD-4.27bpw-Q4_K_M-M64`: 33 shards, 94,525,394,976 bytes | Rejected at 128K after no semantic output, memory-pressure level 1, and about 60.87 GiB wired. |
| Single-agent server | `127.0.0.1:8318`, 131,072 context, one slot, mmap/lazy reads, Flash Attention, batch 2,048, ubatch 512, no fit | Maximum verified context is 128K; 262K was resource-rejected. |
| Practical output | 4,096 tokens | An 8K request ended naturally at 5,854 tokens and showed structural degeneration after about 4K. |
| Bounded concurrency | Two 65,536-token-capacity slots | Two 8,247-token direct prompts and two approximately 8.4K Hermes workflows overlapped; full-slot saturation and cross-slot cache reuse are unproven. |
| Promotion state | `selected-local-experiment` | Reproducible M1 Max selection, not a universal default or production deployment. |

The immutable 128K IQ4 receipt SHA is
`b1a19003338ac38356e713330e5113a3d77529be9ecda836ea2cf38b594d69d9`:
130,944 prompt tokens with exact beginning/middle/end recall, 67.885 tok/s
prefill, 6.559 tok/s decode, 49.09 GiB maximum RSS, and 52.14 GiB maximum
wired memory. The Q4.27 rejection receipt SHA is
`8eaebc127c5f2c5c530eae796c1d2468dfcaf66cf983784052dc0c2bfb148762`.

The bounded direct-concurrency receipt SHA
`0e3e13c6f12a752ded8611021316185f6a527273d66511e7c746fc2706c5f6d0`
proves overlap and zero swap growth for two 8K prompts. The linked Hermes
receipt SHA `00dd96a4bfe3d66ddc2347eb4054e7db28de24148eab7783dca279c3e86508f5`
proves two simultaneous two-tool workflows. Neither proves two fully occupied
64K slots or cross-slot prefix reuse.

## Operator rules

- Use the Jundot route only when referring to the 27B OMLX control.
- Use the full Qwen/AtomicChat identity only for the isolated exact experiment.
- Keep new 27B control results out of historical `results_flash_next_*` paths;
  the repaired evaluator writes a correctly named control result path.
- Do not describe explicit llama slot restoration as automatic persistence,
  cross-slot sharing, or OMLX-equivalent cache lifecycle behavior.
- Do not generalize the selected 128K/4K IQ4 configuration to 262K, Q4.27, or
  two context-filled agents; each of those claims failed or remains unproven.

## Record status

This document supersedes the false identity presentation in the removed
`QWEN-38-FLASH-NEXT-ARCHITECTURE.md`. The old historical decisions and worklog
entries remain unchanged for provenance; D-032 records their supersession and
D-035 records the completed M1 Max selection.
