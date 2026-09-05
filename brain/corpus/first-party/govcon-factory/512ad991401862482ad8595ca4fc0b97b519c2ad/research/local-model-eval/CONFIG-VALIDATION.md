# omlx Config Validation — Reconciling Tuning Research Against Live Config

**Date:** 2026-08-23 · **Scope:** cross-check every tuning conclusion from the multi-day `omlx`
optimization campaigns (`~/agent-reports/omlx-*`) against the live server config on this
machine (`m64`) and against today's eval findings (`~/govcon-factory/research/local-model-eval/{REPORT,LIVE-TEST}.md`).

**This is a validation/recommendation document only. No live config was changed, no
service was restarted, and no destructive command was run to produce it.** Every value
in the tables below was either read from a file, queried from the live `/api/status` and
`/v1/models` endpoints, or read from `launchctl`/`sysctl` — never assumed.

---

## 1. Settings table

| Setting | Current (live) value | Research-recommended value | Verdict | Source(s) |
|---|---|---|---|---|
| Context window (`qwen3.8`) | `262144` (full model ceiling; global fallback stays `32768`, unused for this model) | `262144` — already the model's advertised ceiling, can't go higher, no reason to go lower | **Optimal** | `~/.omlx/model_settings.json`; `~/.omlx/settings.json` (`sampling.max_context_window`); live `/v1/models` → `max_model_len:262144`; `omlx-proper-install/step4-context-settings.md` |
| `max_tokens` default | `32768` (global `sampling.max_tokens`) | `32768` — matches observed production caps; no source recommends a different global default | **Optimal as a ceiling** — but see §3(a): the real stage-1–4 failures are a completion problem, not a budget-size problem, so raising this further is explicitly **not recommended** (`REPORT.md` §4 item 3) | `~/.omlx/settings.json`; `agent-reports/RUNBOOK.md` §1b; `REPORT.md` §3–4 |
| KV cache quantization (`turboquant_kv_enabled` / `turboquant_kv_bits`) | `false` / `4` (configured but disabled) | Measured as a genuine no-op **solo** (no throughput, memory, or quality difference after a retracted-and-corrected re-measurement); the one plausible benefit regime — concurrent agents + long context, where KV is additive across sequences — was **never measured** | **No research consensus, and now known blocked, not just untested** — see below | `omlx-optimization/MEASUREMENTS.md` §H2 (incl. the retraction of the original "~7%/2.44GB" figure); `STATE.md` §1, §2 (H2), §3 (retraction #1); **new 2026-08-26**: attempting to enable it on `qwen3.8` fails outright — omlx rejects `vlm_mtp_enabled` and `turboquant_kv_enabled` both `True` on the same model ("choose one speculative path per model"). Since `vlm_mtp_enabled=true` is this doc's own adopted, measured-beneficial setting (row above), testing TurboQuant KV's concurrent/long-context regime means giving up MTP's 60-78% draft-acceptance speedup first — a real tradeoff this doc's "single most promising untested lever" framing didn't account for. Not applied; flagged for an explicit choice, same as this doc's own pattern for other open items. |
| Prefill chunk gate (`OMLX_QWEN35_Q8_MLP_MIN_TOKENS` / `..._LINEAR_MIN_TOKENS`) | `256` / `256` | `256` — final adopted value, superseding an earlier proposal of `2048` (`omlx-prefill-tuning/FINDINGS.md`) once contended-chunk behavior (`_CONTENDED_CHUNK_FLOOR=256`) was measured directly | **Optimal** — at the shipped default of `16384` this kernel *never* engaged at any prompt length; `256` is the value that lets it engage even on 256-token contended chunks | `com.mike.omlx-server.plist` (live env, confirmed via `launchctl print`); `RUNBOOK.md` §1a; `omlx-optimization/STATE.md` §2 (H1); `omlx-prefill-tuning/FINDINGS.md` |
| Scheduler chunking (`scheduler.chunked_prefill`) | `false` | `false` — tested `true` and rejected: +1.2% worse aggregate wall time, first-request TTFT +64% worse, no earlier finish for the queued request | **Optimal** | `~/.omlx/settings.json`; `omlx-optimization/STATE.md` §2 (H4); `RUNBOOK.md` §1b |
| MTP / speculative draft (`vlm_mtp_enabled`, `vlm_mtp_draft_block_size`) | `true`, block_size `2`, drafter `Qwen3.8-27B-MTP-8bit` | block_size `2` — measured better than the drafter's own default of `3` on both short (71.3% vs 67.2% acceptance) and long-context (75.4% vs 62.2%, turning a −10.3% regression into a +2.2% gain) prompts | **Optimal, but bounded** — block sizes `1` and `4` were never tested, so "2 is better than 3" is measured, "2 is the true optimum" is not | `~/.omlx/model_settings.json`; `omlx-optimization/MEASUREMENTS.md`/`STATE.md` MTP sections; `RUNBOOK.md` §1c, §6 |
| iogpu wired-memory limit | `61440` MB (60 GiB) | 60 GiB — explicit Mike choice, leaves 4 GiB of the 64GB machine for macOS/WindowServer/browser | **Optimal** | `sysctl iogpu.wired_limit_mb` (live, confirmed = 61440); `/Library/LaunchDaemons/com.mike.iogpu-wired-limit.plist`; `RUNBOOK.md` §1d |
| Memory-guard tier | **Changed 2026-08-26**: `custom`, `memory_guard_custom_ceiling_gb=59.0` (effective admission ceiling `59.0GB` per `process_memory_enforcer` startup log; the actual Metal wired-limit stays bound by the pre-existing 60GiB `iogpu.wired_limit_mb`, so the practical hard cap is `min(59, 60)`≈59GB) | Mike's explicit, informed direct instruction (redtrades/agent-configs#33 thread), given *after* being shown this exact table's `balanced`-tier verdict and the `95.2%` swap finding below — he chose to accept less OS headroom for a larger, stable ceiling. Not a re-litigation of the 2026-08-23 finding, a deliberate override of it. | **Changed on purpose — watch swap** | `~/.omlx/settings.json`; server.log `2026-08-26 01:10:52` (`Process memory enforcer started (tier=custom, ceiling=59.0GB)`); see §6 below for the full incident and the swap numbers observed after the change |
| Flash-attention config (`OMLX_FA256_STEEL`) | `0` (fallback/unfused path) | `0` — steel measured 3–7% slower solo and under concurrency, *and* the steel kernel dispatches an entire KV range in one Metal command buffer, which collapses 5–6× past ~30K kv_len on a documented macOS GPU watchdog cliff (`omlx` issue #2225) — almost exactly this campaign's own long-context test length | **Optimal** | `com.mike.omlx-server.plist` (live); `omlx-optimization/MECHANISMS.md`; `STATE.md` §2 (Flash Attention); `RUNBOOK.md` §1a |
| Thread / dispatch counts | No manual thread-count knob exists in omlx (unlike llama.cpp's `--threads`); the only related lever, `OMLX_FA256_DISPATCH_BUDGET`, is auto-calibrated at boot (`_auto_dispatch_budget()`) and moot with `STEEL=0` | N/A — nothing to tune | **Not applicable** — flagging explicitly rather than omitting, since the task asked for it | `omlx-optimization/MEASUREMENTS.md`, `MECHANISMS.md` (no thread-count references found in either file) |
| `thinking_budget` handling | **Changed since 2026-08-23**: `thinking_budget_enabled: true` for `qwen3.8` in `model_settings.json` (was `false`) — adopted by a session between then and 2026-08-26, no writeup found for the isolated test this doc's own §6 recommended first. Hermes-side passthrough gap (§4 below) not confirmed fixed either way this pass. | The 2026-08-23 recommendation was to test in isolation before adopting; can't confirm that happened | **Adopted, but the isolated-test evidence trail is missing** — re-verify quality on stage-1–4-style prompts before trusting this was a validated change, not just a flip | `~/.omlx/model_settings.json` (live, checked 2026-08-26); `REPORT.md` §4 item 1; `LIVE-TEST.md` §6 item 1 |
| `tool_choice` forcing | Confirmed live today: forcing a specific function **hangs the server** (two calls each ran >60s, stuck `active_requests` slot until manually dropped) | Never use forced `tool_choice` against this server; natural/auto tool offering is confirmed reliable | **Wrong / broken** — do not use | `REPORT.md` §2, §4 item 4; upstream `jundot/omlx` issue [#2877](https://github.com/jundot/omlx/issues/2877) (open, same problem area — forced tool_choice not honored) |
| Grammar-constrained decoding (`guided_grammar_enabled`) | **Changed since 2026-08-23**: `xgrammar==0.2.3` is now installed in `~/.venv-omlx` (confirmed live 2026-08-26: `importlib.metadata.version('xgrammar')` → `0.2.3`, matching this doc's own §5 recommendation exactly) — but `guided_grammar_enabled` is still `false` in `model_settings.json`, so the capability exists and is unused | Install `[grammar]` extra (done), then flip `guided_grammar_enabled: true` for `qwen3.8` and re-verify the stage-7 schema retest from `REPORT.md` | **Half-applied** — the hard part (native dependency install) is done and stuck; the easy part (one boolean) isn't | `~/.venv-omlx` (live, checked 2026-08-26); `~/.omlx/model_settings.json` (live) |

---

## 2. Live config snapshot (for reference)

Read live on 2026-08-23, no changes made:

- `curl /api/status`: `version=0.6.2`, `loaded_models=["mlx-community--Qwen3.8-27B-8bit"]`, `avg_prefill_tps=61.4`, `avg_generation_tps=5.4`, `model_memory_used=28.85GB`, `model_memory_max=50.86GB` (this surface's own accounting; `RUNBOOK.md` notes the admin surface reports a different ~58.0GB figure for the same ceiling by design — both are cited above, do not average them).
- `launchctl print gui/501/com.mike.omlx-server`: `state = running`, `pid = 10576`, env `OMLX_FA256_STEEL=0`, `OMLX_QWEN35_Q8_MLP_MIN_TOKENS=256`, `OMLX_QWEN35_Q8_LINEAR_MIN_TOKENS=256` — all match the plist exactly, no drift.
- `sysctl iogpu.wired_limit_mb`: `61440`.
- `~/.omlx/` directory: `model_settings.json`, `settings.json`, `logs/`, `cache/`, `models/`, `stats.json`, `bin/` — no undocumented config files found.
- omlx installed at `~/.venv-omlx` (manual venv, not Homebrew/DMG — confirmed no `pip` module either; this venv appears to have been built with `uv`), package version `omlx-0.6.2.dist-info`, exactly matching the live `/api/status` version.

---

## 3. Workload analysis

### (a) Agentic tool-call loops — many small requests, needs thinking headroom, fast prefill

**What helps:** the `256`-token Q8 gate and `_CONTENDED_CHUNK_FLOOR=256` are exactly the
shape this workload needs — they specifically un-gate the fast kernel path for the small,
contended chunks that dominate under concurrent tool-call traffic (`omlx-optimization/STATE.md`
§2, H1 concurrent hand-rolled harness: +14.6% on contended chunks). MTP block_size=2 also
measurably helps short-prompt decode (+12.3% vs no drafter). `decode_fairness=true` protects
an in-flight decode from being starved by a new prefill arriving mid-turn — directly relevant
to interleaved tool-call/tool-result turns.

**What hurts / is unresolved:** today's live-fire test (`LIVE-TEST.md`) found the *single
tool selection* pattern reliable (REPORT.md §2, stage 6: 2/2 correct picks, clean JSON,
34–200s) but **composite/judgment tool-call arguments fail completely** — 0 of 33 real
candidate-scoring calls produced a valid tool call, 100% `finish_reason=length`, because the
model reasons correctly but never stops reasoning in time to emit the call. Decomposing the
composite call into narrower single-field calls rescued only the near-mechanical dimensions
(`naics_firm_match`, `requirement_maturity`), not the two requiring genuine weighing
(`set_aside_signal`, `overall_priority`) — "the dividing line is judgment vs. lookup, not
call granularity" (`LIVE-TEST.md` §3). No current setting fixes this; more `max_tokens` was
explicitly ruled out as a fix (`REPORT.md` §4 item 3, `LIVE-TEST.md` §6). `thinking_budget_enabled`
is the one untested lever that might, and Hermes currently forwards **no** reasoning signal
to omlx at all regardless (§4 below), so even if that flag were flipped server-side, nothing
on the client side is currently positioned to tune it per-request.

**Separately, a capacity mismatch worth flagging:** Hermes's subagent delegation
(`delegation.max_concurrent_children`) defaults to **10** when unset in `config.yaml`
(confirmed absent from Mike's config, so the default is live) — `~/.hermes/hermes-agent/tools/delegate_tool.py:122`.
omlx's own tuning campaign measured and documented a **3-concurrent-agent practical ceiling**
(`RUNBOOK.md` §5: aggregate throughput identical within noise at 3 vs 4 agents; a fourth just
waits, and at full context a fourth may not fit in the 60GiB wired allocation at all). Nothing
in Hermes enforces the 3-agent ceiling — an agentic tool-call workload that fans out several
subagents at once could oversubscribe the server well past what any of this tuning validated,
and would surface as a memory-pressure abort that Hermes' error classifier can mislabel as a
billing error (`RUNBOOK.md` §7.1 — a related, already-documented Hermes bug, not fixed by
anything in this pass).

**Verdict for this workload:** current settings are well-tuned for narrow, closed-ended tool
selection. They do not and cannot fix the open-ended-judgment completion failure — that is a
model-behavior/completion-signal gap, not a config gap.

### (b) Long-running agentic coding — max usable context, sustained KV pressure, stability over hours

**What helps:** `max_context_window=262144` gives the full nominal ceiling with no policy
cap; `memory_guard_tier=balanced` and the 60GiB iogpu wired limit are conservative and
tested against `safe`/`aggressive`/`custom` alternatives, all of which were tried and
reverted for good measured reasons.

**What hurts:** the nominal 262144-token ceiling is **not** what's actually usable under
sustained pressure. Three independent, harness-level (not synthetic) measurements found:
- `adaptive_prefill_throttle` (a third, previously undocumented chunk-shrinking mechanism,
  distinct from both the contention floor and `chunked_prefill`) fires under sustained
  memory growth within a single long conversation, at a consistent **~40–58K-token** context
  depth, confirmed across three different harnesses (Hermes, `pi`, OpenCode) in the same
  session (`omlx-optimization/STATE.md` §2, "THIS SESSION" and §4).
- A cold ~70K-token prompt was **rejected outright, 2/2 attempts**, by the prefill memory
  guard under the current config, each attempt burning 6–10 minutes of GPU before dying
  (`omlx-optimization/PHASE0-REPORT.md`, point 3). The same context length works fine when
  built incrementally (cache-backed), so **cache eviction turns a long-running conversation
  into an unservable one** if the conversation ever needs a cold re-prefill at depth.
- The `pi` harness run in the same campaign ended in a hard rejection at 55,296 tokens with
  the omlx guard's own verbatim error (`predicted peak would exceed prefill safety cap
  45.7GB`), inheriting memory residue from an immediately preceding run with no restart
  between them — a real, load-bearing illustration of `RUNBOOK.md` §4's "memory tail."

**Practical ceiling, not nominal ceiling:** `RUNBOOK.md` §5's three-agent concurrency math
(three agents at full context peak 56.4GB against the 58.0GB ceiling; a fourth would need
~75GB, more than the 60GiB wired allocation) means multi-hour, multi-agent coding sessions
are bounded well below 262144 tokens × N agents in practice.

**Open lever specific to this workload:** TurboQuant KV quantization is the one setting
whose only plausible benefit regime — KV cache is additive across concurrent sequences while
weights are shared — is exactly this workload's shape, and it has never been measured under
concurrency or long context (only solo, where it's a confirmed no-op). This is the single
most promising untested lever for sustained multi-hour/multi-agent stability, ahead of
touching the memory-guard tier or ceiling again (both already tried and reverted).

**Restart hygiene matters over hours:** `RUNBOOK.md` §4 documents the memory tail precisely
(pre/post restart: 39GB→32GB footprint, 16GB→8.16GB compressed, swap freed ~920MB) and gives
explicit triggers for when a restart is warranted. This is process hygiene, not a setting,
but it's the single biggest lever for "stability over hours" that's already documented and
already correctly not automated (RUNBOOK's cadence rule: restart between tasks, not mid-work,
since Hermes depends on port 8300 and other services share this box).

---

## 4. The Hermes `thinking_budget` passthrough gap — found and localized this pass

**A discrepancy worth stating plainly first:** the task background for this pass asserted
that "`thinking_budget` works as a per-request param" and that Hermes's lack of a passthrough
for it was "source located today" in `REPORT.md`/`LIVE-TEST.md`. Neither claim is actually
in those files — I grepped both directly (`grep -rn thinking_budget`) and read them in full.
What they actually say is narrower: `thinking_budget_enabled` is a **model_settings.json
toggle**, currently `false`, never touched by any prior tuning campaign, and explicitly
flagged as *untested* — "its name suggests a hard cap on the reasoning phase... do not flip
it based on this report alone" (`REPORT.md` §4 item 1). Neither file names a Hermes file or
function. I'm flagging this per this task's own instruction not to invent grounded-sounding
claims — what follows is what I independently traced this pass, not something read out of
today's eval docs.

**What I found, tracing Hermes's own source (`~/.hermes/hermes-agent/`):**

1. `~/.hermes/config.yaml` defines the omlx provider under the literal name `omlx`
   (`providers.omlx.base_url: http://127.0.0.1:8300/v1`), and separately sets
   `agent.reasoning_effort: high`.
2. Hermes's provider-profile registry (`providers/__init__.py`, `get_provider_profile()`)
   resolves a provider name against registered plugins in `plugins/model-providers/*` and
   their `aliases` tuples. **No plugin is named or aliased `omlx`** — confirmed by grep
   across every `plugins/model-providers/*/__init__.py`.
3. `get_provider_profile("omlx")` therefore returns `None`. Per its own docstring
   ("Returns None if the provider has no profile (falls back to generic)"), the request
   builder (`agent/transports/chat_completions.py`) takes the **"Legacy fallback
   (unregistered / unknown provider)"** branch (line ~517) instead of the normal
   profile-based path (`_build_kwargs_from_profile`, line ~510).
4. That legacy branch has explicit, named handling for `is_kimi`, `is_tokenhub`,
   `is_lmstudio`, `is_openrouter`, `is_github_models`, and `provider_name == "gemini"` — it
   computes a `reasoning_config` but **has no branch for `omlx` or any generic local
   OpenAI-compatible provider**, so nothing ever turns `agent.reasoning_effort: high` (or any
   thinking/reasoning field) into an actual request parameter for omlx calls. Every call to
   the local model currently carries zero reasoning/thinking signal, regardless of what
   `config.yaml` says.
5. The `custom` provider profile (`plugins/model-providers/custom/__init__.py`) already
   implements exactly the right behavior for a local OpenAI-compatible reasoning endpoint —
   its own docstring names vLLM, Ollama, and llama.cpp as covered cases, and its
   `build_api_kwargs_extras()` emits `extra_body.think`/top-level `reasoning_effort`
   correctly. It is simply never reached for `provider: omlx` because `"omlx"` isn't in its
   `aliases` tuple (`("ollama", "local", "vllm", "llamacpp", "llama.cpp", "llama-cpp")`).

**Concrete, small fix (not applied):** add `"omlx"` to the `aliases` tuple in
`~/.hermes/hermes-agent/plugins/model-providers/custom/__init__.py` (currently line ~98–104).
This is a one-line change, Hermes-side only, no omlx server restart required — it routes
every future omlx call through the profile path instead of the legacy fallback and starts
forwarding `agent.reasoning_effort` as either `extra_body.think=False` (disabled) or a
top-level `reasoning_effort` string (enabled + effort set).

**What this fix does *not* resolve, and needs checking before trusting it:** everything
Hermes's `custom` profile forwards is a **categorical** `reasoning_effort` string
(`none`/`low`/.../`max`) or an Ollama-style `think` boolean — not a **numeric token-count**
`thinking_budget`. Whether omlx's own wire API accepts a numeric `thinking_budget` request
field at all (distinct from the `model_settings.json`-level `thinking_budget_enabled` flag)
is not established by anything read in this pass — that needs a check against omlx's own
source/API docs before assuming the `custom`-profile fix is sufficient rather than needing an
omlx-specific profile that emits a different field name.

---

## 5. omlx release / changelog findings (web research)

`omlx` (GitHub: [`jundot/omlx`](https://github.com/jundot/omlx)) is an MLX-based LLM
inference server for Apple Silicon — continuous batching, tiered (hot RAM + SSD) KV/prefix
caching, OpenAI-compatible API, menu-bar-managed. Confirmed via web search, not assumed from
context.

- **Version installed:** `0.6.2`, confirmed three ways — live `/api/status`, the venv's
  `omlx-0.6.2.dist-info`, and `omlx --version`. All three agree, no drift.
- **Newer releases exist:** `0.6.3rc1` (2026-08-19) and `0.6.3rc2` (2026-08-20) — both
  release candidates, not yet stable, one and two days before this pass respectively.
  ([Releases · jundot/omlx](https://github.com/jundot/omlx/releases))
- **Grammar-constrained decoding: already supported, not a version gap.** omlx 0.6.2 ships
  real xgrammar-based grammar-constrained decoding (logit-level bitmask enforcement, run in
  parallel with the forward pass) — declared in the package's own metadata as an optional
  extra: `xgrammar==0.2.3; extra == "grammar"` + `apache-tvm-ffi==0.1.11; extra == "grammar"`
  (`omlx-0.6.2.dist-info/METADATA`, read directly). Web research confirms **Homebrew and DMG
  builds of omlx include `xgrammar` by default; manual/pip/uv venv installs do not** — and
  this machine's install (`~/.venv-omlx`, documented in `omlx-proper-install/STATUS-consolidated.md`)
  is exactly that manual-venv case. Confirmed live: `xgrammar` is not importable in
  `~/.venv-omlx` (`ModuleNotFoundError`). This is the actual, fixable root cause of
  `REPORT.md` §3's finding — **not** something that requires upgrading omlx itself. Neither
  `0.6.3rc1` nor `0.6.3rc2`'s changelog mentions xgrammar or structured-output changes, so an
  upgrade wouldn't fix this either way — installing the existing `[grammar]` extra would.
- **`tool_choice` forcing hangs the server: no exact matching upstream issue found.** Searched
  `jundot/omlx` issues for `tool_choice` and for `tool_choice hang` specifically. The closest
  match is open issue [#2877](https://github.com/jundot/omlx/issues/2877), "OpenAI
  `/v1/chat/completions` honours only `tool_choice='none'`" — named-function forcing gets
  silently downgraded to auto mode, a *different* symptom (silent downgrade vs. hang) in the
  same problem area (forced `tool_choice` handling), still open as of this pass. Neither
  `0.6.3rc1` nor `0.6.3rc2`'s release notes mention `tool_choice` at all. **No existing GitHub
  issue was found describing the specific hang behavior Mike's session discovered today** —
  as far as this search could tell, that appears to be a newly-observed, unreported bug, not
  a known/tracked one. If this is confirmed to reproduce reliably, it's worth filing upstream
  with the two-call repro from `REPORT.md` §4 item 4.

---

## 6. Recommended changes

### Low-risk (per-request params / Hermes-side code, no omlx server restart) — can likely be applied anytime

1. **Never send forced `tool_choice` to the omlx provider.** Confirmed hang (`REPORT.md` §4
   item 4), open upstream issue in the same area (#2877), no fix in sight. Use natural/auto
   tool offering only — already how stage 6 in `REPORT.md` was run, and it's reliable.
2. **Add `"omlx"` to the `custom` provider profile's `aliases` tuple** in
   `~/.hermes/hermes-agent/plugins/model-providers/custom/__init__.py`. One-line, Hermes-side
   only. Benefit: starts forwarding `agent.reasoning_effort` (currently silently dropped for
   every omlx call) as `extra_body.think`/top-level `reasoning_effort`. Risk: low and
   reversible (revert the one line), but verify first whether omlx's wire API wants a
   categorical `reasoning_effort` or a numeric `thinking_budget` — this fix delivers the
   former; confirm that's actually useful before relying on it (§4, last paragraph).
3. **Not recommended:** retrying stage-1-style extraction/scoring prompts with a larger
   `max_tokens`. `REPORT.md`'s own 8000-token schema-constrained retest already failed for a
   structural reason (no grammar enforcement existed) unrelated to budget size; `LIVE-TEST.md`
   §6 restates this explicitly. Don't spend GPU time on this direction.

### Server-restart / live-config changes — other services share this GPU/server; **flagging for Mike's explicit go-ahead, nothing here was applied**

1. **Install the `xgrammar` extra to enable real grammar-constrained decoding.**
   `uv pip install --python ~/.venv-omlx/bin/python "omlx[grammar]==0.6.2"` (this venv has no
   `pip` module at all — confirmed live — so it must go through `uv pip` or an equivalent,
   not a bare `pip install`). Then restart per `RUNBOOK.md` §3, and re-verify via
   `~/.omlx/logs/server.log` for a grammar-compiler load line before re-running `REPORT.md`'s
   stage-7 schema retest. **Expected benefit:** real schema-enforced JSON for every future
   stage that currently relies on `response_format` for structural safety (stages 1, 2a, 4 in
   `REPORT.md` all hit this). **Risk:** new native dependency (`apache-tvm-ffi`) in a shared
   venv, never tested against this exact model/omlx-version combination on this machine;
   treat as its own isolated smoke test before trusting it in production, consistent with
   `RUNBOOK.md`'s standing cadence rule (never mid-work, always between tasks, health-poll
   before handing the port back).
2. **Test `thinking_budget_enabled: true` for `qwen3.8`** in `~/.omlx/model_settings.json`.
   Untested by every prior campaign; flagged today as the top candidate fix for the
   stage-1–4 "never stops reasoning" completion failures, with an explicit "do not flip it
   based on this report alone." Needs a small isolated test (a handful of stage-1-style
   calls) after a model reload before any production use. **Expected benefit:** could force
   an earlier transition from reasoning to final content on exactly the open-ended/judgment
   calls that currently fail 100% of the time (`REPORT.md` §4, `LIVE-TEST.md` §6). **Risk:**
   model reload required, unknown quality/behavior effect, genuinely untested — this is an
   experiment, not a known-good change.
3. **TurboQuant KV cache under concurrency + long context** — still an explicit "Mike's call,
   not a measurement result" to leave off, and the campaign's own stated next step if he
   wants it revisited: the only unmeasured regime is exactly the one workload (b) above
   depends on for stability. Recommend this as the next concurrency/memory experiment ahead
   of touching the memory-guard tier or ceiling again (both already tried and reverted with
   clear negative results).
4. **Not urgent:** upgrading to `0.6.3` once it leaves release-candidate status. No changelog
   evidence it fixes either the tool_choice hang or the grammar gap (both are better addressed
   directly, above) — nothing here argues for or against the upgrade on its own merits.

---

## 7. Open questions / gaps

- **Whether omlx's wire API accepts a numeric per-request `thinking_budget` field at all**,
  distinct from the `model_settings.json`-level `thinking_budget_enabled` toggle — not
  established by anything read in this pass. Needed before treating the Hermes `custom`-alias
  fix (§4/§6) as sufficient.
- **TurboQuant KV under concurrency + long context** — flagged as unmeasured in at least three
  separate documents (`MEASUREMENTS.md`, `STATE.md`, `TEST-PLAN.md`) and never closed.
- **MTP block_size 1 and 4** — never tested; "2 is better than 3, measured" is not the same
  claim as "2 is the optimum."
- **Whether further prompt decomposition rescues more of the judgment-requiring tool-call
  dimensions** (`LIVE-TEST.md` §3) — only spot-checked on one candidate (2/4 succeeded);
  not generalized across the 33-candidate pool or any other task shape.
- **The 95.2% swap usage after the H3 four-agent custom-ceiling test** — flagged by the
  original researchers as unattributed (could be that test, could be prior machine uptime,
  could be other concurrent sessions) and never resolved either way (`STATE.md` §2, H3).
- **Whether the tool_choice hang reproduces reliably enough to file upstream** — observed
  twice today, consistently, but not stress-tested at N>2 or across different tool schemas.
- **The vMLX/RCA/vmlx-config-search research** (`~/agent-reports/vmlx-config-search/`) was
  read per this task's checklist but concerns a different, non-adopted serving stack (vMLX,
  a JANG-fork-based engine, investigated 2026-04-08/09, predating the omlx production
  cutover) — no settings from it transfer to the current omlx config. Included here for
  completeness, not because it changed any conclusion above.
- **`mlx-engine-shootout/RESULTS.md`** (2026-08-20) is the source of the historical "stay on
  llama.cpp" recommendation and predates the actual omlx production cutover — treat as
  decision history, not current guidance; it also claims "omlx exposes no KV-cache-quantization
  flag at all" (checked against `omlx serve --help` only), which the later `omlx-optimization`
  campaign's admin-API-based TurboQuant testing directly contradicts — flagging the
  disagreement rather than silently picking one, since the later, admin-API-based finding is
  the one consistent with the live `model_settings.json` schema actually observed today.

---

## 6. 2026-08-26 — memory-guard abort, ceiling change, and a model-cache incident

**Trigger:** Mike hit a live "Request aborted: process memory limit exceeded (usage 55.8 GB,
abort threshold (hard watermark) 47.5 GB, static ceiling 50.0 GB)" from Hermes, surfaced in the
UI as a billing/payment error. Full incident, root cause, and the first round of fixes:
`redtrades/agent-configs#33`. This section folds the outcome in here, per Mike's instruction
that this file be the one authoritative settings record — `#33` and `agent-workspace` TASK-0004
have the blow-by-blow.

### 6.1 Root cause (memory-guard abort)

A long multi-turn Hermes↔omlx tool-calling session on `qwen3.8` (MTP draft head co-resident)
grew its prefix-cached prompt to ~77K tokens. The abort limit is `min(static_ceiling, metal_cap)`
— `metal_cap` is meant to be pinned by the pre-existing 60GiB `iogpu.wired_limit_mb` kernel
sysctl (§1d), but under this machine's known concurrent-session swap pressure (confirmed at
82-90% swap used repeatedly through this session) the *effective* binding ceiling was observed
swinging 47.7GB↔58.0GB within one server run — well below both the nominal `balanced`-tier
static ceiling (58GB) and the 60GiB kernel cap. The exact internal mechanism for why the
"static ceiling" label itself moved wasn't fully pinned down (see Open questions); the practical
effect is confirmed directly from `server.log`, not inferred.

### 6.2 Ceiling change — `balanced` → `custom`, 59GB

Table row updated above. Mike was shown this doc's own `balanced`-tier verdict and the §7.2/
`STATE.md` H3 finding (a 59GB custom ceiling drove swap to 95.2% in a 4-agent test, reverted)
*before* confirming he still wanted the change — this is a deliberate override, not a
re-litigation done in ignorance of the prior finding. Applied: `memory_guard_tier: custom`,
`memory_guard_custom_ceiling_gb: 59.0`, `soft_threshold` set explicitly to `0.9` (was the
legacy-sentinel `0.85`, which under `custom` tier would silently default to `0.85` instead of
inheriting `balanced`'s `0.90` — see `process_memory_enforcer.py`'s `_SOFT_THRESHOLD_BY_TIER`).
`hard_threshold` left at `0.95` (already gives ~56-57GB off a 59-60GB ceiling, matching what
Mike asked for without needing to touch it). Confirmed live post-restart:
`Process memory enforcer started (tier=custom, ceiling=59.0GB)` — survived the restart, on disk
and in the running process. **Swap watch, not yet resolved:** swap was already at 82-90% before
this change (pre-existing, not caused by it) and climbed to 90.3% shortly after in this session's
own monitoring — consistent with the §7.2 warning, not yet contradicted by it. Next person to
touch this: check `sysctl vm.swapusage` and `scripts/verify-persistence.sh`'s new memory-headroom
check (agent-workspace, TASK-0004) before assuming this is settled.

### 6.3 TurboQuant KV × MTP: real conflict, not just untested (table updated above)

Attempting `turboquant_kv_enabled: true` on `qwen3.8` while `vlm_mtp_enabled: true` (the adopted,
measured-beneficial setting) fails model-settings validation outright and, worse, **silently
drops the entire per-model settings block** for the model that failed to validate — including
`model_alias: qwen3.8` — on the restart where it was tried. Caught via `/v1/models` showing the
alias missing; reverted immediately, re-verified clean on the next restart. Anyone revisiting
"TurboQuant KV under concurrency + long context" (this doc's own top recommendation, §6 old
numbering) needs to first decide whether it's worth trading away MTP's block_size=2 speedup —
not evaluated here, flagged for an explicit choice.

### 6.4 Hermes "billing" mislabel — real fix found and applied (not just filed this time)

An earlier pass on `#33` traced this into the wrong repo (`hermes-webui`, a `nesquena` fork) and
found no match. The actual bug is in **`~/.hermes/hermes-agent`** (`NousResearch/hermes-agent`
— confirmed as the repo Hermes's `provider: omlx` config actually routes through), matching
`RUNBOOK.md` §7.1's own prior finding almost exactly: `agent/auxiliary_client.py::_is_payment_error`
treated a connection-level exception (`status_code=None` — the shape a local omlx call produces
under hard memory pressure) as eligible for its billing-keyword scan, with no provider/loopback
gate at all. Applied the smaller of `RUNBOOK.md` §7.1's / `typed-failure-states/2026-08-20-report.md`'s
two-path fix ("Path B", self-contained): dropped `None` from the eligible-status set. Verified:
existing 402/403/404 test-class assertions still pass (direct execution; pytest isn't installed
in that venv), a synthetic omlx-abort exception with no status code now returns `False`. Committed
locally on `local-patch/loopback-billing-misclassify-fix` (1 commit, checked out — the live fix
is active) — **not pushed**, `hermes-agent` is `NousResearch`'s repo, not Mike's. "Path A"
(`error_classifier.py::classify_api_error`, needs provider/base_url threaded through ~9 call
sites) is unapplied, per both prior docs' own recommendation that it's Mike's call, not a
self-contained fix.

### 6.5 Unrelated incident: model cache deletion mid-session

Between two restarts in this session (a ~48-second window), `~/.cache/huggingface/hub`'s
`mlx-community--Qwen3.8-27B-8bit` (28GB) and `Jiunsong--SuperQwen3.8-27b-abliterated-MLX-4bit`
(15GB) directories disappeared — not caused by anything in this session. Ruled out: the
`nightly-cleanup.sh` LaunchAgent (reads its own source: permanently, deliberately excludes
`~/Library/Caches/huggingface` and any model store, by design); no cron job; nothing in omlx's
own source deletes HF cache. Disk usage dropped from 94% (58GB free) to 88% (106GB free) in the
same window, and another live Claude Code session (started ~5 minutes before the deletion) was
running concurrently on this machine — the most plausible explanation, not confirmed. Model
re-download triggered afterward (Mike confirmed via a live debugging exchange, having reverted
`~/.hermes/config.yaml`'s `model.default` back to `qwen3.8` himself in the middle of this). See
`#33` for the full timeline. **Not yet re-verified against the original abort scenario** — that
needs the re-download to finish first.

### 6.6 Prefix caching — confirmed live, not re-benchmarked

`server.log` shows cross-request prefix-cache reuse happening continuously and by default
throughout this session (`prefix cache: request ... re-prefills N of M tokens (reused K)`),
consistent with `mlx-engine-shootout/RESULTS.md`'s server-confirmed ~8x hit speedup finding.
Nothing to enable — it's on. Not independently re-measured this pass on a controlled
repeated-system-prompt workload; the existing shootout numbers stand.

### Open questions added 2026-08-26

- **Why the abort-limit's binding ceiling swings well below both the tier's static reserve and
  the 60GiB kernel wired-limit cap**, given `get_effective_metal_cap_bytes()` reads a supposedly
  fixed kernel sysctl value when it's set. Traced the source (`process_memory_enforcer.py`,
  `memory_monitor.py`, `exceptions.py::describe_ceiling_binding`) at length without a fully
  conclusive answer — documented as a real gap, not silently resolved. Whoever revisits this:
  start from `describe_ceiling_binding`'s `binding` label on a live abort and confirm which
  component (`static`/`dynamic`/`metal_cap`) is actually reported, with fresh log evidence,
  before trusting either this doc's or `#33`'s prior theories.
- **Whether the disk-cache deletion (§6.5) recurs** — no root cause confirmed, only ruled-out
  candidates. If it happens again, check which other session/process was active at the exact
  timestamp before assuming it's the same cause.
