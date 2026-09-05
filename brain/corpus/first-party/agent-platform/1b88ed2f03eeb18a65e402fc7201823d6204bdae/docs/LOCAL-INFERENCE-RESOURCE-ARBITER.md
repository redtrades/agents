# Local Inference Resource Arbiter

Status: proposed implementation contract (2026-08-31)

The persistence mechanism is a per-user launchd service. The repository template
is [`runtime-adapters/launchd/com.mike.local-inference-arbiter.plist`](../runtime-adapters/launchd/com.mike.local-inference-arbiter.plist).

## Problem

OMLX and llama.cpp are separate launchd services today. Each can be healthy while
the other owns GPU memory, so `/v1/models` can show a model that is only catalogued
and the host can still have both engines resident. Hermes profiles also select one
backend directly, bypassing a shared admission point.

## Required invariant

The Apple-Silicon GPU is one exclusive resource:

```text
GPU lease owner ∈ { none, omlx, llamacpp }
```

The arbiter is the only component allowed to start, stop, or expose a local engine.
An engine is not `loaded` until its health/model probe confirms residency. The
arbiter must never start the other engine while the current owner has a loaded
model or an active request. If ownership is ambiguous, admission fails closed.

The OMLX and llama.cpp launch agents must not independently use `RunAtLoad` and
`KeepAlive` once the arbiter owns them. Leave the arbiter persistent across login,
logout, and reboot; it starts the selected engine only after reconciliation and
keeps the non-owner stopped. A system restart therefore restores the arbiter and
its durable state, not two competing model servers.

## Interface

The arbiter owns a loopback control endpoint (suggested `127.0.0.1:8320`) and a
durable state file outside this repository. It exposes read-only status suitable
for the dashboard:

```json
{
  "gpu": {"owner": "llamacpp", "memory_limit_bytes": 61440000000,
          "resident_bytes": 0, "available_bytes": 61440000000},
  "engines": {
    "omlx": {"process": "running", "model": "catalogued", "loaded": false,
             "active_requests": 0, "queued_requests": 0, "tokens_per_second": 0},
    "llamacpp": {"process": "running", "model": "loaded", "loaded": true,
                 "active_requests": 0, "queued_requests": 0,
                 "prompt_tokens": 0, "completion_tokens": 0,
                 "tokens_per_second": 0}
  },
  "requests": {"active": 0, "queued": 0, "completed": 0,
               "rejected": 0, "concurrency_limit": 1},
  "observed_at": "2026-08-31T00:00:00Z"
}
```

The exact live values are observed, not inferred from configuration. The control
surface must support `status`, `acquire(engine)`, `release(engine)`, and
`restart(engine)`. `acquire` waits for active work to drain, verifies the other
engine is unloaded, records a generation/fence, then starts and probes the target.
`release` saves any supported checkpoint, stops the child, confirms its process and
model are gone, and only then clears the lease.

## Durability and recovery

Persist atomically (0600, temp-file plus rename) after every lease transition and
request counter update. State contains lease owner, generation, engine/model IDs,
PIDs, start/stop timestamps, request counters, token counters, checkpoint paths,
and last error. On restart, reconcile by process identity and endpoint probes; do
not trust a stale PID or stale state file. If both engines are resident, do not
choose a winner automatically: report `CONFLICT`, reject new local work, and
require an explicit recovery action after requests are confirmed idle.

The normal recovery sequence is reversible: drain -> checkpoint -> stop owner ->
probe unloaded -> acquire the other engine. A full system restart is a recovery
option, not the synchronization mechanism. GPU memory telemetry is advisory for
capacity and diagnostics; exclusivity is enforced by the lease and post-stop
residency probe.

## Hermes profiles

Hermes must retain two explicit profiles, both routed through the arbiter/gateway,
never directly to an engine:

| Profile | Engine selector | Use |
|---|---|---|
| `local-omlx` | `engine=omlx`, OMLX model ID | Qwen oQ4e control |
| `local-llamacpp` | `engine=llamacpp`, Flash-Next model ID | GGUF Flash-Next |

The profile selection is the request for an engine lease; it is not proof that the
model is loaded. Hermes status must display the arbiter generation and the returned
engine status. Cloud fallbacks remain separate and must never acquire the GPU lease.

## Acceptance checks

1. Starting OMLX while llama.cpp is loaded returns queued/busy and leaves OMLX
   unloaded.
2. Starting llama.cpp while OMLX is loaded returns queued/busy and leaves llama.cpp
   unloaded.
3. After a clean drain, the requested engine becomes loaded and the former engine
   is process-dead and probe-confirmed unloaded.
4. Status reports active/queued/completed requests, prompt/completion tokens, and
   a measured token rate for each engine.
5. Arbiter restart reconciles the same state without double-starting a model.
6. Hermes can select either local profile and the request is visible in arbiter
   status with the correct generation.
