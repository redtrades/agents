# Routing policy — mesh model traffic

Routing-policy history for humans and bots. The retired Sentinel design used a
weekly deep audit against this file; it is not a current scheduled auditor.
Current route changes come from the admitted issue-36 templates, drift remains
report-only, and spending decisions of any kind are Mike-only.

> **Supersession notice (2026-08-28):** the retired
> `qwen38-oq4e-short`/`mid`/`full` catalog is no longer the Hermes roster.
> Current managed profiles are `mesh-primary` (Hermes `default`, exact IQ4
> Flash-Next on llama.cpp `:8318`), `cloud-coordinator` (FreeLLMAPI
> `auto:code` on `:3100`), and `local-27b-control` (the separately named dense
> 27B OMLX control on `:8300`). `agent-configs` issue #36 and its admitted
> inventory are authoritative; legacy cascade rows below are historical where
> they conflict with those routes.

Sources: staging/research-free-routing-subscriptions.md (cascade,
failure-class timers, stealth census), staging/research-hermes-ecosystem.md
(pin mechanics), ~/agent-configs/MASTER-GUIDE.md section 4 (stack
topology).

## Cascade table

| Task class | Primary | Fallback chain | Kill-switch |
|---|---|---|---|
| Interactive / judgment / frontier drafting (Mike or blocking session) | Claude Max via Claude Code, leased, max 2-3 concurrent sessions | `mesh-primary` exact IQ4 Flash-Next with a degraded-mode note | Fail closed. Claude work never spills into free pools (data + quality); alert, queue for the next 5h window |
| Exact-model local agent work | `mesh-primary`: exact IQ4 Flash-Next via llama.cpp at http://127.0.0.1:8318/v1 | none; fail closed | Never route silently to OMLX or cloud |
| Controlled dense-model comparison | `local-27b-control`: `Jundot--Qwen3.8-27B-oQ4e-mtp` via OMLX at http://127.0.0.1:8300/v1 | none; fail closed | Comparison runs only; never call it Flash-Next |
| Cloud coordination / bounded bulk extraction | `cloud-coordinator`: FreeLLMAPI `auto:code` at http://127.0.0.1:3100/v1 | none beyond its admitted route; queue + notify Mike | Never cross the workload's sensitivity boundary or silently route to local controls |
| Embeddings | bge-m3 llama-server sidecar (D-010) | Cloudflare Workers AI within neuron budget | Hard-stop at budget; queue to next reset window |
| Nightly batch / digests | Gemini Flash-Lite on the dedicated never-billed free project | Groq remainder -> Cloudflare -> OpenRouter :free | Abort cleanly and resume if <20% daily budget remains at start |

Ordering principle: sensitivity boundary first (never leak a data class
across pools), then capability, then cost.

## Stealth models — never-depend rule

No workflow, profile pin, or fallback chain may depend on a stealth
model. Every stealth slot carries a written removal date at adoption;
rotate any stealth slot out every 7 days regardless of observed health;
run capability probes before promoting any replacement.

Historical observation: the FreeLLMAPI block in the generic `local` profile
once pinned `stealth/ox-alpha` (recorded 2026-08-26). That profile is retired;
the current admitted roster contains no stealth model. A future fallback needs
its own explicit non-stealth policy and receipt; it cannot quietly become a
second baseline.

## Historical Qwen3.8-oq4e context tiers and contention policy

This section records the retired three-tier OMLX design and benchmark
assumptions. It is not a profile-creation or selection instruction. Use the
three-profile roster in the supersession notice for current Hermes work.

`qwen38-oq4e-profiles.yaml` is the checked-in contract for the three
Hermes profile names. It records declared configuration only; live selection
and runtime state must still be observed before a workload starts.

| Profile | Context tokens | Output cap | Reasoning | Selection policy |
|---|---:|---:|---|---|
| `qwen38-oq4e-short` | 65,536 | 4,096 | low | default reliable cold-serving tier |
| `qwen38-oq4e-mid` | 131,072 | 4,096 | low | explicit warm continuation tier |
| `qwen38-oq4e-full` | 262,144 | 8,192 | xhigh | explicit isolated deep-context tier |

The production target is stable OMLX 0.6.2 with at most three agents,
`prefill_priority: context`, chunked prefill off, decode fairness on, a 40GB
SSD cache target, 8GB hot-cache target, and fp32 GDN. It keeps short as the
default rather than treating every turn as a deep-context request.

The deep path is a separate admission mode: exactly one agent,
`prefill_priority: speed`, and an explicit full profile. Compress before the
cold-unservable region; never set `max_tokens` equal to the selected context
length. Controlled benchmarks use the agent-mesh nonblocking process lock at
`/tmp/agent-mesh-qwen38-hermes.lock` and refuse an established port-8300
client. A cache hit is reported only from explicit reused-token telemetry; no
timing, throughput, cache size, or quality result is promoted into that claim.

The Hermes target has explicit `supports_reasoning` and `supports_tools`, no
MoA baseline, and reasoning visibility separate from compute. Stable 0.6.2 is
the production baseline. RC3 is only an isolated experimental candidate; its
campaign must establish its own result. Its fused MLP/down path requires dense
Q4 at group size 128 and dual ANE, unlike the current oQ4e group size 64.
See `OMLX-HERMES-OPTIMIZATION.md` for the receipt-gated feature and skill
matrix; no candidate listed there is an executed result.

## Fallback timers — three failure classes

Copying LiteLLM's vocabulary: cooldowns are per-deployment; classify
errors and give each class its own recovery timer.

| Class | Signal | Response | Timer |
|---|---|---|---|
| Rate-limited (transient) | 429 with retry-after, RPM/TPM caps | Honor retry-after, immediate failover, return later | Seconds to minutes |
| Quota/credit-depleted | 402, insufficient_quota bodies, RPD-exhausted 429 | Do not retry. Failover instantly, mark route dead until reset wall-clock, notify Prime | Hours-days, aligned to resets: midnight PT (Gemini), 00:00 UTC (CF/OVH/OpenRouter), rolling 5h (Claude Max) |
| Down/degraded | 5xx, timeouts, connection resets | 1-2 retries with backoff, then open breaker with half-open probes | Minutes |

Router hygiene regardless of implementation: allowed_fails ~3/min,
failover stickiness ~60s to prevent flapping, total attempt budget <=4
across the cascade, SDK retries zeroed so the router owns retries, log
attempted-fallback counts everywhere (rising fallback rate predicts
incidents before status pages do). Policy/quota failures fail closed
past sensitivity boundaries; silent rerouting across a boundary is the
one unacceptable outcome.

## Budget guardrails

Thresholds apply to any metered spend (paid API dollars, Claude Max
window burn, neuron budget):

- **70% — WARN.** Log + message Prime. No behavior change yet.
- **75% — COMPACT.** Downshift models one tier, shrink contexts,
  defer all non-due work to the next reset window.
- **90% — KILL.** Stop non-interactive runs mid-flight where safe, queue
  the remainder, escalate to Mike. Nothing restarts until he says so.

Per-run caps: hard token cap per run/session; requests-per-session cap
per pool. Cost-velocity breaker: sustained spend >10x the planned rate
for that workload trips the breaker even while everything returns HTTP
200 — error-rate breakers never catch a runaway loop.

## Historical weekly pool-drift check (retired Sentinel step)

Runs the PROFILE-POLICY drift-SQL concept
(~/agent-reports/freellmapi-install/PROFILE-POLICY.md) against the
FreeLLMAPI store:

1. Curated-membership invariants must hold: notrain pool subset of
   {cloudflare, groq, ovh, requesty}; code pool exactly its declared
   rows; business pool subset of {groq}. Any platform leaking in = file
   an issue with the query output. Report only, never self-prune.
2. Live-probe every enabled pool member once (minimal completion, record
   HTTP status + X-Routed-Via). New 401 = dead key, persistent 429 =
   ceiling changed, 404 = model retired; update expectations.
3. Token-canary diff: fire each profile's fixed fingerprint prompt,
   compare token count vs last week. A jump means a silent model swap.
4. Fallback-rate review from gateway logs: sustained >1-2% on any pool =
   primary unhealthy, investigate.
5. Remember the monthly catalog snapshot lags reality by up to ~30 days
   on the free feed; stored ceilings are not proof of anything. The live
   probes above are the compensation.
