# m64 omlx findings — memory behavior, version regression, prefill tuning

Session findings from verifying the qwen38-oq4e three-tier profile setup
(short 65,536 / mid 131,072 / full 262,144) at real scale on m64. These
are independent of, and additional to, the profile/config work already
recorded in `DECISIONS.md` D-016 through D-018 and `hermes/qwen38-oq4e-profiles.yaml`
— this file covers what actually happens when you push the full tier to
genuinely large context, not just that the config parses.

## KV cache cost, computed and cross-validated

`Jundot/Qwen3.8-27B-oQ4e-mtp`'s `config.json` confirms a hybrid
architecture: 64 total layers, `full_attention_interval: 4` → only 16
layers are full attention (the ones whose KV cache grows with context);
the other 48 are `linear_attention` (GDN-style, constant-size state,
does not grow with context). Only the full-attention layers matter for
KV-cache sizing:

```
growing KV per token = 2 (K+V) × num_key_value_heads(4) × head_dim(256) × 16 layers
                      = 32,768 elements/token = 64 KiB/token at bf16
```

At native 262,144 tokens fully filled: ~16.0 GiB of KV cache alone.
Cross-validated against two independent real memory-guard rejections at
144,364 tokens (69% of native), both reporting KV+SDPA cost directly in
their error text:

- First rejection: `KV+SDPA 9.35 GB`
- Second rejection (hours later, different memory state): `KV+SDPA 9.49 GB`

Both agree closely with each other and with the formula's ~9.0 GiB
prediction at that same length. The formula is trustworthy.

## Full-context request: rejected outright, not silently evicted, when co-resident

Reproduced live, twice, independently: a large full-context request
(144,364 tokens) gets **rejected at admission** — before any compute —
when the 8-bit checkpoint (`mlx-community--Qwen3.8-27B-8bit`, 28.5GB) is
also resident and total projected usage would exceed the dynamic
ceiling (~55.5–56.9GB, itself under the raw 59GB guard due to safety
margins). The guard does **not** proactively evict the idle model to
make room at admission time — that eviction behavior only exists on the
separate mid-prefill adaptive-throttle path (see `omlx/scheduler.py`,
the LRU-eviction call inside `_admit_or_wait`-adjacent throttle logic).
A caller hitting this gets a clean, structured error
(`prefill_memory_exceeded`) — not a hang, not silent truncation. Practical
implication for anyone running the full tier: unload the other model
first (`POST /admin/api/models/{id}/unload`) if you want the true
262,144-token window genuinely available; don't assume it just works
alongside another large resident model.

## omlx 0.6.3rc3: do not upgrade to this build

Attempted upgrading the venv-installed omlx (v0.6.2, from
`https://github.com/jundot/omlx/releases/download/v0.6.2/...whl`) to the
latest available release, v0.6.3rc3. Structural checks passed (xgrammar,
`thinking_budget_enabled`, memory-guard flag name, idle-eviction setting
all intact), but real verification — sending Hermes's actual tool-heavy
request shape (~28K token fixed overhead, real tool schemas) — hung
**both the new model and the pre-existing, previously solid 8-bit
checkpoint**, each freezing mid-prefill for 7+ minutes with near-zero
CPU and zero log progress, no error, no timeout. This is a general
regression in 0.6.3rc3, not something specific to the new checkpoint —
confirmed via a differentiating test against the known-good 8-bit model
on the same 0.6.3rc3 server.

The release notes for rc2 and rc3 corroborate this: both rewrote
memory-guard accounting (*"The memory guard now includes fixed ANE I/O
surfaces and CPU-sharing allocations..."*, rc2) and the error-reporting
path for memory-guard-triggered failures (*"Reported prefill-memory
failures correctly... instead of flattening them into generic server
errors"*, rc3) — exactly the mechanism where the hang occurred. **Rolled
back to v0.6.2** (same wheel, reinstalled via `uv pip install`). Do not
retry rc3 without checking upstream `jundot/omlx` issues for a fix, and
prefer waiting for a tagged non-RC 0.6.3 release given rc3 is the third
release candidate, not a stable cut.

## The actual fix for slow/throttled long-context prefill

Every attempt at a genuine 144K+-token single-request prefill on m64,
across many hours and even with the machine otherwise idle, got bogged
down by `adaptive_prefill_throttle` — chunk sizes shrinking
progressively, throughput dropping from a normal ~85-90 tok/s baseline
down into single digits. This looked at first like resource contention
or a memory leak, but the omlx process's own footprint stayed clean
(confirmed via `top`, no accumulated "memory tail" per the operational
runbook's own diagnostic) — the slowdown was coming from somewhere else
entirely.

Reading `omlx/scheduler.py` directly (`_next_chunk_size`, around line
4080) explains why: the default `scheduler.prefill_priority` setting is
`"context"`, which proactively shrinks chunks based on a **conservative
EWMA-predicted per-token transient cost, with a safety multiplier**,
whenever the predicted peak for a full chunk would cross a target
watermark — not whenever memory has *actually* run out. The scheduler
has a documented alternative: `prefill_priority: "speed"` — quoting the
source comment, *"Speed priority: never shrink... the pre-chunk guard
and the post-chunk memory check abort cleanly instead of crawling at
floor-size chunks."* In other words: the default mode trades speed for
a wide safety margin against a worst-case memory spike; speed mode
trusts the hard limit checks to abort cleanly if genuinely necessary,
and otherwise runs unthrottled.

This is a live-settable field, no restart required:

```bash
curl -X POST http://localhost:8300/admin/api/global-settings \
  -H 'Content-Type: application/json' \
  --data-binary '{"prefill_priority": "speed"}'
```

**Caveat, confirmed by testing**: this does *not* retroactively affect a
request that's already mid-flight — `_prefill_speed_priority` is read
once per scheduler/request context, not re-checked live. Applying the
setting mid-request had no visible effect on that request; killing it
and starting a fresh one after the setting change is what worked —
confirmed live, the new request sailed through the exact token ranges
(24K-48K) that every prior attempt had gotten stuck in, at full ~65-90
tok/s with zero throttle log lines.

**Recommendation**: leave `prefill_priority` at the default (`context`)
for normal mixed/concurrent workloads where a conservative margin
protects other resident models — but switch to `speed` before any
deliberate large single-context run (RFP extraction, full-repo review,
etc.) where you've already confirmed nothing else needs to be resident,
matching the KV-cost math above.

## Full end-to-end confirmation, including prefix-cache reuse

With `prefill_priority=speed` applied cleanly to a fresh request (not
mid-flight — confirmed the setting isn't retroactive), the full
144,364-token payload completed cleanly: `finish_reason: stop`,
`cached_tokens: 0` (confirmed cold), 3065.16s total, and the model
correctly retrieved a marker planted near the end of the context
verbatim — real evidence of usable long-context retrieval, not just
successful prefill completion.

Sending the **exact same payload again immediately after** (prefix
cache now warm from the first run) completed in 52.94s —
**~58x faster** — with `prompt_tokens_details.cached_tokens: 143360`
of `144,364` (99.3%) reported directly by the server. This is the
server's own explicit field, not an inference from timing, matching the
cache-evidence bar this repo's `evals/qwen38_hermes.py` harness already
holds live cache claims to. Same correct answer both times. Real-world
read: a first pass over a large document is slow; repeat questions
against that same document are fast, which is the actual usage shape
for something like RFP attachment extraction.

## Superseding campaign scope: stable production, RC3 receipt-gated experiment

This section supersedes the earlier **policy conclusion** that RC3 should never
be retried; it does not rewrite the evidence above. Stable OMLX `0.6.2` remains
the production baseline. The prior RC3 Hermes-prefill regression and rollback
remain a material risk signal, but `0.6.3rc3` may be tested only as an isolated
experimental candidate. Its own campaign receipts—not this historical run—are
the only authority to promote or reject it.

The eligibility boundary is exact: the current oQ4e path is `group_size=64`.
The RC3 fused MLP/down path requires dense Q4 at `group_size=128` and dual ANE.
Those are different configurations; do not report an oQ4e result as an RC3
eligibility result, or vice versa.

The first-principles campaign begins with ANE, TurboQuant, DFlash, SpecPrefill,
and MTP disabled. Test one feature or documented compatible pair per cell, not
their cross-product. SpecPrefill is blocked until an explicit compatible draft
model exists; MTP is blocked until an explicit compatible draft model or
model-native MTP head exists. Those prerequisite states are unexecuted, not
failures. Every future row needs exact prompt/cached/completion tokens, wall
time, tool-call result, cache evidence, memory observation, reasoning behavior,
and context behavior.

## 2026-08-27 campaign result

The prerequisites above were resolved and tested. The model-native Lightning
MTP head activated successfully. TurboQuant KV4 converted 15 of 64 cache
layers and is compatible with MTP on stable `0.6.2`. At the representative 8K
prompt, feature-off stable took 152.26s, MTP took 126.74s, and TurboQuant+MTP
took 114.51s. The paired stable configuration is therefore the measured
production winner.

The older 8-bit checkpoint took 108.09s at 8K but consumed 37.77 GB and decoded
at only 6.8 tok/s, so it was rejected for a 64GB multi-agent machine and
permanently removed. ANE on the current group-64 oQ4e checkpoint aborted the
8K row with Apple ANE Code 47. A real 28,909-token Hermes tool-heavy replay did
not allow SpecPrefill sparse selection to engage because the system/tool prefix
is protected. Stable could not attach DFlash2; RC3 could, but its 8K row did
not complete inside three minutes.

RC3 with the same TurboQuant+MTP pair took 117.73s at 8K and peaked at 24.98
GB, versus stable's 114.51s and 22.45 GB. RC3 is rejected for the current oQ4e
production path. The one remaining RC3 question is its distinct fused ANE path
on dense Q4/group-128 weights; that result must not be conflated with the
group-64 oQ4e comparison. See `benchmark-results-2026-08-27.md` for the full
table and Hermes prompt baseline.
