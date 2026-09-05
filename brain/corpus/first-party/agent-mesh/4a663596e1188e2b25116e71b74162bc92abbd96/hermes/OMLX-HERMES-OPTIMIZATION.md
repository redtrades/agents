# OMLX / Hermes optimization contract

This is the historical repository-side OMLX operating contract for the M1 Max
64GB path. The campaign and exact measurements are recorded in
[`benchmark-results-2026-08-27.md`](benchmark-results-2026-08-27.md). Re-observe
the machine before a future runtime change; do not infer current state from
this document alone.

> **Current roster (2026-08-28):** this document preserves the dense 27B OMLX
> benchmark campaign; it is not the active Hermes profile catalog. The retired
> `qwen38-oq4e-short`/`mid`/`full` names are historical. Current profiles are
> `mesh-primary` (exact IQ4 Flash-Next on llama.cpp `:8318`, 128K/4K),
> `cloud-coordinator` (FreeLLMAPI `auto:code` on `:3100`, 1M/8K), and
> `local-27b-control` (exact Jundot dense 27B OMLX control on `:8300`, 128K/8K).
> See `agent-configs` issue #36 for the inventory-admitted source of truth.

## Evidence status

**Imported, verified run evidence** is preserved in
[`m64-omlx-findings.md`](m64-omlx-findings.md): stable OMLX `0.6.2` completed a
144,364-token cold request in 3065.16 seconds, then the identical warm request
in 52.94 seconds with 143,360 cached tokens. The second value is explicit
server telemetry, not a timing inference.

The new campaign independently compared `0.6.3rc3` with stable. RC3 attached
DFlash2 but regressed and timed out at 8K. Its oQ4e TurboQuant+MTP result was
2.8% slower at 8K and used more memory than stable. RC3 therefore remains out
of production. Its dense-Q4/group-128 fused ANE path is a separate pending
eligibility test, not evidence for the current group-64 oQ4e model.

**Historical target policy** below is declarative evidence for the retired
OMLX tier campaign, not the current Hermes roster. Any reuse requires a
separate loopback receipt with the active runtime version and settings.

## Operating modes

| Setting | Production serving | Isolated deep-context work |
|---|---|---|
| OMLX version | stable `0.6.2` | stable `0.6.2`; RC3 only for the dense-Q4/group-128 gate |
| Admission | normal, at most 3 agents | exactly 1 agent |
| Prefill priority | `context` | `speed` |
| Chunked prefill | off | not promoted as a production optimization |
| Decode fairness | on | retain unless a bounded receipt disproves it |
| Default profile | `qwen38-oq4e-short` | explicitly select `qwen38-oq4e-full` |
| SSD cache target | 40GB | same cache budget, evidence still required |
| Hot cache target | 8GB | same cache budget, evidence still required |
| GDN precision | fp32 | fp32 |
| Decode acceleration | native Lightning MTP | same |
| KV compression | TurboQuant KV4 | same unless a receipt disproves it |

Production favors reliable cold serving. Deep mode is a consciously isolated
speed-priority path, not a way to make every normal request large. Compress or
split material before it reaches a cold-serving region the active memory guard
cannot admit; do not use a context-length-sized output cap as a workaround.

## Current Hermes roster and historical OMLX profile policy

The current inventory-derived roster is:

| Profile | Model/route | Context | Output | Policy role |
|---|---|---:|---:|---|
| `mesh-primary` (Hermes `default`) | `Qwen3.8-Flash-Next-AD-3.84bpw-IQ4_XS-M64`, llama.cpp `:8318` | 131,072 | 4,096 | exact-model primary, `xhigh`, minimal tools, no fallback |
| `cloud-coordinator` | `auto:code`, FreeLLMAPI `:3100` | 1,048,576 | 8,192 | bounded delegation and sole initial gbrain owner |
| `local-27b-control` | `Jundot--Qwen3.8-27B-oQ4e-mtp`, OMLX `:8300` | 131,072 | 8,192 | separately named comparison control |

The remainder of this section documents the retired OMLX tier policy and is
kept for interpretation of its receipts, not for current profile creation.

The 2026-08-27 OMLX campaign observed a root/default profile and three tiers
selecting local `qwen3.8-oq4e`. That state is historical; the generic `local`
profile was already legacy-only and was not a second baseline. Those profiles
did not use MoA or a stealth fallback.

The retired campaign target was:

- Canonical local path: `qwen38-oq4e-short` on `qwen3.8-oq4e`; mid and full
  are selected explicitly rather than becoming implicit defaults.
- Retire the stale `local` profile only after migration verification; it is not
  a parallel baseline.
- No MoA baseline and no stealth auxiliary model. A fallback needs its own
  explicit, non-stealth policy and receipt.
- Keep `supports_reasoning: true` and `supports_tools: true` explicit. Treat
  reasoning visibility as separate from its compute budget: a UI/display choice
  must not silently rewrite the profile's `thinking_budget` or output cap.
- `max_tokens` remains the declared output cap (4,096 short/mid; 8,192 full),
  never the selected context length.

| Profile | Context | Output cap | Reasoning | Policy role |
|---|---:|---:|---|---|
| `qwen38-oq4e-short` | 65,536 | 4,096 | low | default reliable cold-serving tier |
| `qwen38-oq4e-mid` | 131,072 | 4,096 | low | explicit warm tier |
| `qwen38-oq4e-full` | 262,144 | 8,192 | xhigh | explicit isolated deep tier |

## Completed compact A/B and remaining skill-growth contract

The quick native matrix is complete and the exact rows are in the benchmark
receipt. Stable `0.6.2` oQ4e with TurboQuant KV4 + native MTP is the balanced
winner. The older 8-bit checkpoint was measured, rejected for memory/decode,
and permanently removed. RC3 oQ4e and DFlash were measured and rejected. The
only unfinished runtime cell is RC3 fused ANE on a separately converted dense
Q4/group-128 checkpoint.

Change one axis per run group, always retaining the same bounded tool-call and
stable-prefix fixture:

1. Model comparison: complete (oQ4e retained; older 8-bit removed).
2. Acceleration comparison: complete for baseline, MTP, TurboQuant+MTP, ANE,
   SpecPrefill, DFlash, and RC3 oQ4e.
3. Dense Q4/group-128 RC3 fused test: deferred; the optional 55.56 GB source
   conversion was stopped before completion to preserve the verified stable
   handoff. No fused-ANE result is claimed.
4. Hermes reasoning and skill payloads: remaining post-runtime matrix.

Those groups are not a cross-product. Each receipt must explicitly contain
tool-call result, exact prompt/cached-token fields, memory observation, and
latency; a missing receipt is `not-run`, never pass.

### First-principles feature campaign

The campaign started from all features off and changed one axis or documented
compatible pair at a time. Native MTP and TurboQuant+MTP passed. ANE on the
current checkpoint, DFlash, and SpecPrefill for Hermes tool-heavy prompts were
rejected. Both compatible draft helpers were tested; they are no longer
unknown prerequisites.

After the runtime winner is restored, use this five-run
profile-by-skills matrix to measure real prompt growth without multiplying all
profiles by all skill inventories:

| Run | Profile | Controlled skill set | Why it exists |
|---:|---|---|---|
| 1 | short | 0 skills | lower-bound prompt and cold baseline |
| 2 | short | core agent skills | normal agent baseline |
| 3 | short | representative larger skills | controlled prompt-growth comparison |
| 4 | mid | core agent skills | context-tier comparison |
| 5 | full | core agent skills | deep-tier comparison |

Every matrix receipt records exact `prompt_tokens`, `cached_tokens`, latency,
memory, reasoning behavior, and context behavior. Keep all non-skill inputs
fixed. Cache reuse needs the server's explicit field; a shorter elapsed time,
cache directory size, or `n_past` alone is not proof.

The offline validator still does not contact the machine. It verifies the
declared contract and prevents a future change from silently rewriting the
measured decisions.

For an external JSONL plan without contacting the endpoint or changing runtime
configuration, use the offline-only planner after the manifest validates:

```bash
python3 evals/qwen38_hermes.py \
  --write-quick-matrix-plan /tmp/qwen38-quick-matrix.jsonl
```

It defaults to a bounded six-row candidate plan and can be parameterized with
comma-separated model, runtime, reasoning, thinking-budget, prompt-size,
skills-payload, repeat, and feature values. Each JSONL row starts as
`planned-not-executed` with null `wall_seconds`, `prompt_tokens`,
`cached_tokens`, and `completion_tokens`; a later receipt owns filling those
fields. The five-row profile-by-skills matrix above remains the prescribed
post-Hermes-fix measurement slice.
