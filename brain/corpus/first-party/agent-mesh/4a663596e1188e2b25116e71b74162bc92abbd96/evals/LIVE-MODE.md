# Evals — offline contract and opt-in live receipts

## Deterministic baseline

`python3 evals/run.py --offline --results <temporary-path>` exercises seven
repository contracts without network access. The `qwen38-hermes-contract`
case validates the checked-in omlx endpoint, `qwen3.8-oq4e` pin, stable-0.6.2
production mode, isolated deep-context mode, Hermes target policy, and the
profile declarations. It records RC3 only as a receipt-gated isolated
candidate; the offline run does not evaluate a runtime variant.
It never writes to `evals/results.jsonl` when an explicit temporary results
path is supplied.

## Qwen3.8-oq4e / Hermes live acceptance

Do not run this probe while OMLX is busy. It intentionally sends a stable
prefix twice and asks Hermes to complete one bounded file/tool workflow, so
it must be the only participating heavy probe against the single backend.
The live command is opt-in, loopback-only, time-bounded, and writes all
outputs under the user-selected artifact directory—not this repository.

The harness uses a nonblocking, process-held lock at
`/tmp/agent-mesh-qwen38-hermes.lock` and refuses to start if port 8300 already
has an established client. This isolation applies to benchmarks only; normal
Hermes traffic may use OMLX continuous batching with up to three agents.

```bash
python3 evals/qwen38_hermes.py

python3 evals/qwen38_hermes.py --live \
  --profile qwen38-oq4e-full \
  --artifact-dir /tmp/agent-mesh-qwen38-hermes \
  --server-log <omlx-server-log-path>
```

Use one of these declared profiles explicitly:

| Profile | Declared context | Output cap | Reasoning | Intended scope |
|---|---:|---:|---|---|
| `qwen38-oq4e-short` | 65,536 | 4,096 | low | default reliable cold serving |
| `qwen38-oq4e-mid` | 131,072 | 4,096 | low | explicitly selected warm continuation |
| `qwen38-oq4e-full` | 262,144 | 8,192 | xhigh | explicitly selected isolated deep context |

The receipt contains a bounded Hermes command (`--max-turns 4` and
`--run-budget`), a unique temporary tool-workflow directory, two request
summaries with a byte-identical system-prefix SHA-256, and lock recovery
status. It never uses `--yolo`, `--accept-hooks`, or an endpoint outside
loopback. The operating system releases the file lock if the process exits;
owner and PID metadata remain available for diagnosis.

## Offline quick-matrix planner

Before promotion or cleanup, generate a repeatable JSONL **plan** without
calling the endpoint or mutating runtime configuration:

```bash
python3 evals/qwen38_hermes.py \
  --write-quick-matrix-plan /tmp/qwen38-quick-matrix.jsonl
```

The planner defaults to a six-row bounded candidate grid: two models (oQ4e and
the older 8-bit checkpoint), stable-0.6.2, low reasoning / 1024 thinking
budget, a 65,536-token prompt, three controlled skill payloads, one repeat,
and the baseline feature state. It can accept comma-separated overrides:

```bash
python3 evals/qwen38_hermes.py \
  --write-quick-matrix-plan /tmp/qwen38-rc3-plan.jsonl \
  --matrix-models qwen3.8-oq4e \
  --matrix-runtimes rc3-0.6.3-isolated \
  --matrix-reasoning none,low,xhigh \
  --matrix-thinking-budgets 0,1024 \
  --matrix-prompt-sizes 65536,131072 \
  --matrix-skills 0-skills,core-agent-skills \
  --matrix-repeats 1 \
  --matrix-features rc3-fused-mlp-down
```

It refuses more than 24 rows, so an exploratory request cannot become a hidden
combinatorial campaign. Every row starts `planned-not-executed` and includes
null `wall_seconds`, `prompt_tokens`, `cached_tokens`, and
`completion_tokens`, plus `not-run` tool/cache/memory/reasoning/context fields.
Only a later, owned receipt may fill those fields.

Keep RC3 isolated and receipt-gated. Its fused MLP/down candidate requires
dense Q4 at group size 128 plus dual ANE, which is not the current oQ4e group
size 64 configuration. ANE, TurboQuant, DFlash, SpecPrefill, and MTP are
first-principles candidates, not passed settings. SpecPrefill requires a
compatible draft model; MTP requires a compatible draft model or native MTP
head before its rows can leave `not-run`.

## Cache-evidence rule

The live receipt marks cache reuse `pass` only if the supplied post-request
server-log tail has explicit reused-token telemetry at or above the OMLX
2,048-token block. For example, `re-prefilled 10247/16391, reused 6144`
supports a reuse observation. Timing, response quality, cache-directory size,
or a populated `n_past` value alone do not. Without a readable log or an
explicit field, the receipt says `unsupported` (or `ambiguous` for `n_past`)
instead of claiming a cache hit or speedup.

## Existing brief and memory probes

The previous brief-format live command remains a separate, deferred probe:

```bash
BRIEF_SYNTH_TIMEOUT=120 python3 evals/run.py --live \
  --endpoint http://127.0.0.1:8300/v1 --model qwen3.8-oq4e \
  --results /tmp/agent-mesh-brief-live-results.jsonl
```

`memory-recall.yaml` still validates its ten-probe schema offline using
`keyword_overlap` / `drawer_match`, not exact strings. Live memory retrieval
remains deferred until its stores are tuned; it is unrelated to the Qwen
long-context receipt.
