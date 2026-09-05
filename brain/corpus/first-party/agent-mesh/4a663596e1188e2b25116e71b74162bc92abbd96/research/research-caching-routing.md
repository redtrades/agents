# Prompt Caching, Token Management & Routing — Local-First Multi-Harness Stack

**Researched:** 2026-08-26 (web + primary docs; local omlx config inspected read-only)
**Scope:** Re-validate OpenClaw doctrine DR066 (static-first caching, ~31x warm claim), DR086 (four-tier budget routing), turn-budget watchdogs (80/100), 70–75% compaction — against 2025–2026 sources. Stack: omlx Qwen3.8-27B-8bit @127.0.0.1:8300/v1 → FreeLLMAPI @:3100/v1 (sensitivity pools, `gateway.mjs`) → OpenRouter stealth/free → Claude Max.

---

## Verdict on the old doctrine (TL;DR)

| Doctrine | Status | Evidence |
|---|---|---|
| DR066 static-first prompt caching | **Holds — now table stakes on every provider.** Anthropic, OpenAI (GPT-5.6+ explicit breakpoints), llama.cpp, MLX servers, vLLM all reward identical stable prefixes; all punish any early-token mutation. | [Anthropic docs](https://platform.claude.com/docs/en/build-with-claude/prompt-caching), [OpenAI guide](https://developers.openai.com/api/docs/guides/prompt-caching) |
| "~31x warm speedup" | **Plausible for large prefixes only, not a constant.** Published numbers: 50–93% TTFT reduction (llama.cpp host-memory cache, ~2–14x), 7x for disk KV restore, up to 85% latency cut (Bedrock). 31x is reachable when re-prefill of a huge static prefix dominates (tens of k tokens); it is not what you'll see on a 2k prefix. | [llama.cpp tutorial #20574](https://github.com/ggml-org/llama.cpp/discussions/20574), [disk-KV proxy post](https://ai-muninn.com/en/blog/kv-cache-disk-restore-7x), [AWS claim](https://www.flexera.com/blog/ai/prompt-caching-breakdown) |
| DR086 four-tier budget routing | **Validated — LiteLLM now ships this exact shape natively** (budget fallbacks reroute exhausted keys to cheaper tiers; zero-cost models exempt from budget checks). | [Budget fallbacks](https://docs.litellm.ai/docs/proxy/budget_fallbacks), [zero-cost carve-out](https://docs.litellm.ai/docs/proxy/users) |
| Turn watchdog 80 snapshot / 100 kill | **Still sound; now a product feature elsewhere** (LiteLLM agent gateway exposes per-session `max_iterations` + `max_budget_per_session`). Keep yours in Hermes rather than adopting a new dependency. | [LiteLLM agents](https://docs.litellm.ai/docs/proxy/users) |
| 70–75% compaction trigger | **Correct as a *proactive* discipline; you cannot configure Claude Code's main-thread auto-compact to fire there** (hardcoded ~95%; the override env var applies to subagents only). Practitioners converge on manual compaction at 50–75% + structured state files. | [GH #24828](https://github.com/anthropics/claude-code/issues/24828), [GH #41818](https://github.com/anthropics/claude-code/issues/41818), [buffer analysis](https://claudefa.st/blog/guide/mechanics/context-buffer-management) |

---

## 1. Prompt caching in 2026

### 1.1 Anthropic (`cache_control`) — mechanics and pricing deltas

- **Multipliers (all current models):** 5-min cache write = **1.25x** base input, 1-hour write = **2x**, cache read = **0.1x** (90% off). Break-even: 1 read for 5-min TTL, 2 reads for 1-hour TTL ([official note](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)).
- Worked prices at Sonnet-class $3/M input: write $3.75 (5m) / $6.00 (1h), read $0.30 ([Flexera breakdown, Aug 2026](https://www.flexera.com/blog/ai/prompt-caching-breakdown)).
- **TTL behavior:** 5-min TTL *refreshes on every hit* (high-frequency agent loops effectively never expire); 1-hour TTL does not auto-renew. Secondary sources report the default TTL dropped from 1h to 5m in early 2026, inflating costs for bursty workloads — if your calls are >5 min apart, set `cache_control.ttl: "1h"` explicitly ([Alephant, Jun 2026](https://blog.alephant.io/prompt-caching-vs-semantic-caching-vs-exact-match)). Unverified-in-primary-source claims to treat with care: Claude Code Max subscriptions get 1h TTL via server-side flag while Pro/API keys stay at 5m ([Wentuo guide, Mar 2026](https://blog.wentuo.ai/en/claude-code-prompt-caching-ttl-pricing-guide-en.html)).
- **Mechanics that matter for layout:** match is on an encrypted hash of the concatenated `tools` + `system` + `messages` prefix up to each breakpoint — **byte-identical or miss**. Up to **4 breakpoints** per request. Cache scope moved from organization to **workspace level on Feb 5, 2026** — different workspaces don't share caches ([Wentuo](https://blog.wentuo.ai/en/claude-api-prompt-caching-pricing-5min-1hour-aws-bedrock-guide-en.html); verify against the official doc before relying on it).
- **New in 2026: pre-warming.** Send `max_tokens: 0`; the API ingests the prompt, writes breakpoints, returns without generating — kills first-call TTFT penalty ([official docs](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)). Directly usable by Hermes to warm session prefixes.
- Bedrock mirrors the multipliers but lags model support for 1h TTL; regional endpoints price ~10% higher ([Wentuo](https://blog.wentuo.ai/en/claude-api-prompt-caching-pricing-5min-1hour-aws-bedrock-guide-en.html)).

### 1.2 OpenAI — automatic, and since GPT-5.6 optionally explicit

From the current official guide ([developers.openai.com/api/docs/guides/prompt-caching](https://developers.openai.com/api/docs/guides/prompt-caching)):

- **On by default** for supported models; caches the *full rendered context* including hidden system content, tool definitions, and history. Reads cost **0.1x**; on GPT-5.6+ cache writes cost **1.25x**; pre-GPT-5.6 models have no write charge. Minimum cacheable prefix: **1,024 visible tokens** (GPT-5.6+) / **2,048** (older).
- **GPT-5.6+ explicit mode:** `prompt_cache_options.mode: "explicit"` + `prompt_cache_breakpoint` markers — up to **4 writes per request**, reads consider up to the last **50 breakpoints**. Default TTL `"30m"` via `prompt_cache_options.ttl`. Earlier models: implicit breakpoints every 2,048 tokens, `in_memory` (~5–10 min inactive, up to 1h) or `24h` retention.
- **Cache-aware routing exists:** requests hash-route to machines above 15 RPM; `prompt_cache_key` (`prompt_version:user/session`) keeps related traffic co-located. Cached tokens still count toward TPM.
- The official best practices are literally Mike's doctrine: *"Keep the prefix stable… If developer instructions contain timestamps, user-specific content, or other dynamic content, place those at the end"*; preserve history append-only; keep tools append-only (`tool_choice: "none"` or `allowed_tools`, never delete definitions mid-thread); compaction can reset reuse — compare total cost before/after.
- Historical discount was 50% ([Oct 2024 launch](https://openai.com/index/api-prompt-caching/)); current cached rate is up to 90% off on newer models — older "50%" blog posts are stale ([Prism explainer, May 2026](https://ssimplifi.com/blog/openai-prompt-caching-explained)).
- Monitor hit rates in the [Prompt Caching Dashboard](https://platform.openai.com/usage?usage_section=prompt-caching) or via `usage.input_tokens_details.cached_tokens` / `cache_write_tokens`.

### 1.3 Local OpenAI-compatible servers — KV-prefix caching exposure

All three families expose KV-prefix reuse; none bill for it — warm hits are pure TTFT savings:

- **llama.cpp (`llama-server`):** `--cache-prompt` (default on) restores longest matching prefix per slot; `--cache-reuse N` extends reuse to non-prefix chunks via KV-shift; `--cache-ram N` adds a host-memory hot cache of computed prefixes (auto save/restore across slots); `--slot-save-path DIR` + `POST /slots/{id}?action=save|restore` persists KV to disk across restarts ([manpage](https://manpages.debian.org/testing/llama.cpp-tools/llama-server.1.en.html), [tutorial #20574](https://github.com/ggml-org/llama.cpp/discussions/20574), [slot API how-to](https://github.com/ggml-org/llama.cpp/discussions/9781)). Reported results: 50–93% TTFT cut on ≥5k-token system prompts; a 60-line client-side proxy got 7x faster restore vs recompute using slot-save ([ai-muninn](https://ai-muninn.com/en/blog/kv-cache-disk-restore-7x)). Known footgun: `--cache-reuse` regressions have shipped before — verify against your pinned build ([issue #15082](https://github.com/ggml-org/llama.cpp/issues/15082)).
- **MLX-family (incl. omlx):** mlx-lm's server has an LRU prompt cache with automatic longest-prefix match; third-party Apple-silicon servers add disk-backed slots, retained-entry counts, and byte budgets ([MLX-Textgen](https://github.com/nath1295/MLX-Textgen), [mlx-openai-server `--prompt-cache-size/--max-bytes/--prompt-cache-dir`](https://github.com/cubist38/mlx-openai-server), [optiq "automatic prefix reuse"](https://mlx-optiq.com/docs/serve)). **Local inspection of Mike's install** confirms omlx v1.0 runs its own stack: `hot_cache_max_size: 8GB`, `ssd_cache_dir`, `ssd_cache_max_size: auto`, `initial_cache_blocks: 256`, `preserve_mid_system_cache: true` (`~/.omlx/settings.json`), i.e., RAM-hot + SSD-persisted KV — the same two-tier pattern llama.cpp users bolt on manually.
  - Caveat: open mlx-lm bug where windowed-cache models (chunked/sliding attention) can serve trimmed KV that doesn't match the keyed prefix — silently wrong output risk on llama4-style architectures; dense Qwen KV caches satisfy the trim contract ([ml-explore/mlx-lm#1494](https://github.com/ml-explore/mlx-lm/issues/1494)). Worth a one-time sanity check on qwen3.8 output after long sessions.
  - Server-side KV quantization flags exist for mlx-lm (`--kv-bits`, merged PR [#1353](https://github.com/ml-explore/mlx-lm/pull/1353)); omlx has the equivalent behind `turboquant_kv_*` per-model settings (`~/.omlx/model_settings.json`) — currently disabled for qwen3.8.
- **vLLM:** Automatic Prefix Caching reuses paged KV blocks hashed by `(parent hash, block tokens, extras)`; enable with `enable_prefix_caching=True` / `--no-enable-prefix-caching` to disable (verify your build's default). sha256 hashing default since v0.11; only full blocks cached; APC speeds prefill, not decode ([APC docs](https://docs.vllm.ai/en/latest/features/automatic_prefix_caching.html), [design](https://docs.vllm.ai/en/latest/design/prefix_caching/)).
- **Harness-induced cache breaks (the sneaky one):** Claude Code pointed at a llama.cpp backend stopped restoring checkpoints because an attribution header mutated the rendered prefix; fix is `CLAUDE_CODE_ATTRIBUTION_HEADER=0` ([writeup, Jun 2026](https://www.mykolaaleksandrov.dev/posts/2026/06/claude-code-llamacpp-prompt-cache-fix/)). **Audit anything that sits between harness and server** — including FreeLLMAPI's request-inspecting `gateway.mjs`: if it reorders fields, injects timestamps, or normalizes JSON differently per request, it destroys provider-side cache hits even when the logical prompt is identical (byte-identical requirement per [Wentuo](https://blog.wentuo.ai/en/claude-api-prompt-caching-pricing-5min-1hour-aws-bedrock-guide-en.html)).

### 1.4 Does "static blocks first, dynamic after" still hold?

Yes — it is now *more* uniform than when DR066 was written:

| Provider | Prefix rule | Explicit control | Notes |
|---|---|---|---|
| Anthropic | Byte-identical prefix through each breakpoint | `cache_control` ≤4 blocks, optional `ttl` | Tools+system+messages hashed in order |
| OpenAI | Entire rendered prefix must match; settings like `tools` order, `reasoning.effort`, `text.format` participate | `prompt_cache_breakpoint` (GPT-5.6+), `prompt_cache_key` | Hidden system tokens count toward rendering but not the minimum |
| Gemini | Implicit caching on 2.5+/3.x models, explicit option | min prefix 2,048; ~75% discount tier | ([Flexera cross-provider table](https://www.flexera.com/blog/ai/prompt-caching-breakdown)) |
| llama.cpp/MLX/vLLM | Token-level longest-prefix match per slot/LRU | flags above | Free (latency-only benefit) |

The one refinement 2026 adds: **append-only tools** (OpenAI `allowed_tools`/`tool_choice:none` instead of editing the tool list) and **explicit breakpoints after stable blocks** so volatile suffixes aren't written into the cache ([OpenAI guide](https://developers.openai.com/api/docs/guides/prompt-caching)).

---

## 2. Token management for long agent sessions

### 2.1 Context-window budgeting patterns

- **Layered budgeting:** fixed layers (harness/system, tools, project rules) should be sized once and kept stable; variable layers (history, retrieval) get the remainder. Multi-turn history reuse saves more input tokens than caching only instructions — append, never rewrite ([OpenAI guide](https://developers.openai.com/api/docs/guides/prompt-caching)).
- **Compaction thresholds in the wild:**
  - Claude Code main conversation: auto-compact fires near **~95% capacity** (hardcoded; feature requests to make it configurable closed as not-planned) ([GH #24828](https://github.com/anthropics/claude-code/issues/24828), [GH #41818](https://github.com/anthropics/claude-code/issues/41818)); the CLI historically ran down to ~1–5% remaining while the VS Code extension compacted around 35% remaining ([GH #11819](https://github.com/anthropics/claude-code/issues/11819)). One guide reports ~83% as the effective default with a 33k output-reserve buffer; treat exact percentages as version-dependent ([TurboAI, Mar 2026](https://www.turboai.dev/blog/claude-autocompact-pct-override-guide), [ClaudeFast, Aug 2026](https://claudefa.st/blog/guide/mechanics/context-buffer-management)).
  - Controls that do exist: `/compact [instructions]`, `/context` live meter, `DISABLE_AUTO_COMPACT=1`, `DISABLE_COMPACT=1`, PreCompact/PostCompact hooks, `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` (**subagents only**) ([CometAPI, Apr 2026](https://www.cometapi.com/what-is-auto-compact-in-claude-code/), [BSWEN, Mar 2026](https://docs.bswen.com/blog/2026-03-21-claude-code-auto-compact-settings/)). Note `autoCompact: false` in settings.json is ignored in some versions — use the env var ([GH #18264](https://github.com/anthropics/claude-code/issues/18264) via TurboAI).
  - Community best practice converges exactly on Mike's 70–75%: keep usage under 70–80%, compact proactively at ~50–66% with structured backups because lossy summarization destroys precision (variable names, error strings) ([CometAPI](https://www.cometapi.com/what-is-auto-compact-in-claude-code/), [ClaudeFast threshold-backup pattern](https://claudefa.st/blog/guide/mechanics/context-buffer-management), [badlogic compaction survey recommending 85–90% hard triggers + manual discipline](https://gist.github.com/badlogic/cd2ef65b0697c4dbe2d13fbecb0a0a5f)).
  - **Server-side compaction arrived in 2026**: Anthropic's API detects a token threshold, summarizes, inserts a compaction block, continues ([compaction doc, Jan 2026](https://platform.claude.com/docs/en/build-with-claude/compaction)); OpenAI exposes `context_management` (compaction) in Responses — both warn it invalidates prior cache from the change point ([OpenAI guide](https://developers.openai.com/api/docs/guides/prompt-caching)).
- **Session rotation beats marathon sessions:** late-session instruction drift on long contexts is documented behavior; rotate at phase boundaries and hand off explicit state ([session-freshness rationale](https://claude.com/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models), summarized in Mike's `agent-configs/rules/session-freshness.md`).

### 2.2 Token accounting / observability

- **OpenTelemetry GenAI semantic conventions** are the emerging standard: `gen_ai.usage.input_tokens/output_tokens` per span, `gen_ai.client.token.usage` counter, `gen_ai.server.time_to_first_token` histogram, `gen_ai.conversation.id` for session correlation. Still Development-status; v1.37 renamed `gen_ai.system→gen_ai.provider.name` and prompt/completion attributes moved to opt-in message attributes — pin versions or dashboards silently under-count ([field guide, Aug 2026](https://niteagent.com/blog/2026-08-07-otel-genai-agent-trace-field-guide/), [conventions repo](https://github.com/open-telemetry/semantic-conventions-genai/blob/main/docs/gen-ai/gen-ai-spans.md), [Uptrace metrics table](https://uptrace.dev/blog/opentelemetry-ai-systems)).
- **Langfuse** (self-hostable, MIT core) tracks per-call usage + cost out of the box, infers cost for self-hosted models via custom model definitions (match-pattern + price-per-token-type), and normalizes OTel `gen_ai.usage.*` subtracting cache reads/writes from input; native capture of LiteLLM and OpenRouter cost data ([token & cost tracking doc](https://langfuse.com/docs/observability/features/token-and-cost-tracking)). This fits "langfuse-lite, per-call meters": one Langfuse instance + LiteLLM callback covers every provider including local (define qwen3.8 as a $0 custom model so its token burn shows up in dashboards without dollars).
- **LiteLLM spend tracking** gives daily per-model/per-key breakdown APIs, virtual-key budgets, and reservation-based enforcement ([spend tracking](https://docs.litellm.ai/docs/proxy/cost_tracking), [budgets](https://docs.litellm.ai/docs/proxy/users)).
- For the self-hosting boundary argument (traces contain prompts; keep them in-boundary): [groundcover guide, Aug 2026](https://www.groundcover.com/guides/self-hosted-llm-observability-security).

### 2.3 Thinking-budget controls

- **Anthropic:** adaptive thinking is now the recommended mode — `thinking: {type:"adaptive"}` + top-level `effort` (`low|medium|max`; high = default). Manual `budget_tokens` still works on most models but is deprecated on 4.6+, rejected outright on newest ([effort doc](https://platform.claude.com/docs/en/build-with-claude/effort), [adaptive-thinking notes](https://spinchange.github.io/vulture-nest/anthropic-adaptive-thinking.html)).
- **OpenAI:** `reasoning_effort` (`minimal|low|medium|high`) — probabilistic dial, no hard cap ([reasoning guide](https://developers.openai.com/api/docs/guides/reasoning)).
- **Qwen family (Mike's local path):** `enable_thinking` + either `thinking_budget` (hard token cap — deterministic ceiling, good for watchdog math) or `reasoning_effort` levels; supported across Qwen3.x including the open-source series ([QwenCloud thinking doc, Apr 2026](https://docs.qwencloud.com/developer-guides/text-generation/thinking)). omlx already exposes this per-model (`thinking_budget_enabled: true` for qwen3.8 in `~/.omlx/model_settings.json`); SSSF phases set `thinking: high/low` per agent today ([MASTER-GUIDE §4]).
- Tradeoff framing (deterministic cap vs adaptive effort): [Inferensys comparison](https://inferensys.com/differences/multimodal-foundation-model-benchmarking/extended-thinking-mode-implementations/claude-45-thinking-budget-control-vs-gpt-5-reasoning-effort-api).

---

## 3. Routing

### 3.1 LiteLLM router — currency check: very much alive

- Active through Aug 2026: production Auto-Router report of **51% savings over 270k requests** by downshifting 95% of traffic off flagship tiers ([blog, Aug 10 2026](https://docs.litellm.ai/blog/auto-router-production-savings)).
- Router features relevant to Mike: multiple deployments per alias, six routing strategies incl. `cost-based-routing` and `latency-based-routing`, cooldowns (429 → immediate ~5s cooldown; `allowed_fails=3`), retries w/ backoff, three fallback classes (general / context-window / content-policy), Redis for shared state ([router setup guide, Jun 2026](https://www.gingerlabs.ai/blog/litellm-router-setup-guide), [routing docs](https://docs.litellm.ai/docs/routing)).
- **DR086-shaped primitives now first-class:** `budget_fallbacks` reroutes a key whose `model_max_budget` is exhausted to the next tier automatically ([budget fallbacks](https://docs.litellm.ai/docs/proxy/budget_fallbacks)); models with `input_cost_per_token: 0 / output_cost_per_token: 0` are **exempt from budget checks** — i.e., "local sunk-cost/free tiers stay reachable after paid caps blow" is a documented config, not custom code ([users/budgets doc](https://docs.litellm.ai/docs/proxy/users)). Gap worth knowing: budget-exhausted deployments aren't auto-cooldown yet — tracked issue [#37592](https://github.com/BerriAI/litellm/issues/37592).
- Agent gateway adds per-session caps: `max_iterations`, `max_budget_per_session`, `session_tpm_limit` ([agents section](https://docs.litellm.ai/docs/proxy/users)).

### 3.2 Router-for-free-providers patterns (freellmapi-like)

- **Classify failures, then act:** credential-class errors (401/402/403/429) → rotate key or cooldown deployment; transient 5xx → retry then failover provider. Gateways like Bifrost formalize retries + key rotation + provider fallback as separate layers ([Maxim/Bifrost, Aug 2026](https://www.getmaxim.ai/articles/handle-llm-rate-limits-and-outages-with-an-ai-gateway/)).
- **Key rotation & escalating cooldowns:** per-model escalating cooldown for failed keys, lockout after multi-model failures, mid-stream error recovery, paid-tier-before-free credential prioritization ([LLM-API-Key-Proxy README](https://github.com/Mirrowel/LLM-API-Key-Proxy/blob/main/src/rotator_library/README.md)).
- **Free-tier reality check (Aug 2026 survey):** nothing is unlimited. OpenRouter `:free` ≈ 20 RPM, ~50 req/day (<$10 lifetime credits) or 1,000/day (≥$10), lowest priority at peak; Groq per-model free limits (30 RPM/1,000 RPD on some models); Gemini free flagship tokens exclude grounding; Cloudflare Workers AI 10k Neurons/day ([Novita comparison, Aug 18 2026](https://blogs.novita.ai/free-llm-api-comparison-2026/), [OpenRouter limits](https://openrouter.ai/docs/api_reference/limits)).
- Hedging lesson from bulk evaluation: **18.5% of 54 providers errored on first attempt** even via OpenRouter's own retries — build fallback chains, refresh model lists immediately before use, use tiered timeouts ([Tygart Media, Jul 2026](https://tygartmedia.com/querying-llms-openrouter)).

### 3.3 Local-first cascade designs & when a local 27B wins

- Cascade shape validated across sources: Tier 1 local (~80% of tasks, $0 marginal), Tier 2 budget cloud (15%), Tier 3 frontier (5%) ([model-selection playbook, Jan 2026](https://godinim.github.io/2026/llm-model-selection)); hybrid SLM+LLM routing is called "the 2026 default," router policy tuned against evals ([FutureAGI, Aug 2026](https://futureagi.com/blog/comparison-slm-llm-language-models), citing NVIDIA's ["SLMs are the future of agentic AI"](https://arxiv.org/pdf/2506.02153)).
- **Where local 27B-class wins:** TTFT 0.1–0.3s vs cloud 0.8–1.2s; Qwen 3.6-27B-class scoring ~77% on SWE-bench — roughly last year's frontier; covers 80–90% of professional coding/writing tasks ([Zosma benchmarks, Jul 2026](https://www.zosma.ai/blogs/local-ai-models-vs-cloud-performance-comparison)). Latency compounds in agents (10–30 calls/task ⇒ 5–15s of pure network RTT saved locally) ([MindStudio, May 2026](https://www.mindstudio.ai/blog/local-ai-vs-cloud-ai-2026)).
- **Where it loses:** hardest multi-step reasoning, reliable complex tool-schema adherence, error recovery in long horizons, multimodal depth; open-weight trails frontier by ~3–6 months on agentic-shaped work, and that gap matters *most* in agent loops ([MindStudio](https://www.mindstudio.ai/blog/local-ai-vs-cloud-ai-2026), [PromptQuorum limitations, Jul 2026](https://www.promptquorum.com/local-llms/local-llm-limitations)).
- Net for Mike: interactive/blocking quality-gated work stays hosted (matches his standing routing rule); overnight/bulk/draft/extract work is local's domain — the open question flagged in his own eval report (stage-1 extraction on local with tuned thinking budget) remains a measure-it decision, not a doctrine.

### 3.4 OpenRouter stealth/free caveats

- **Retention ≠ training ≠ ZDR.** Read every layer: e.g., Ox Alpha on OpenRouter says prompts are *retained but not used for training*, while OpenCode separately claims ZDR for its own client path — a client-layer promise doesn't override provider-layer retention ([explainx forensics, Aug 22 2026](https://explainx.ai/blog/openrouter-ox-alpha-stealth-model-august-2026)). OpenRouter's own stance: retention is opt-in, provider training policies are documented per-model with routing controls to exclude trainers ([data collection doc](https://openrouter.ai/docs/guides/privacy/data-collection)).
- **Expiry risk is real and frequent:** free variants deprecate on short notice (six `:free` models deprecated July 19–21, 2026 alone) ([free-models gist](https://gist.github.com/rlnorthcutt/e6f392cd1ffb1339cc42dfb024c3cf7f)); stealth previews run free to harvest feedback, then graduate to paid pricing or vanish — Ox Alpha ($0/$0, 1M ctx, anonymous) carries exactly this caveat, and Mike's MASTER-GUIDE already flags removal ~2026-08-27. Never build a dependency on a stealth model.
- Free endpoints are served at lower priority — expect throttling/queuing at peak; mid-stream rate limits arrive as SSE `finish_reason:"error"` after streaming starts ([limits doc](https://openrouter.ai/docs/api_reference/limits), [free-tier guide](https://ask-coreai.com/blog/openrouter-free-models-2026-limits-catches)).
- Practical mitigations: one-time $10 credit raises free daily cap 50→1,000; route sensitive classes through paid/ZDR or local; pin model version strings; check data-policy tags per endpoint ([flo2 guide](https://flo2.com/blog/openrouter-free-tier-limits), [coding-fab tutorial](https://coding-fab.com/2026/05/30/openrouter-api-tutorial-unified-ai-gateway)).

---

## 4. Recommendation for Mike's stack

### 4.1 Routing policy table

Priority order = try top-down within a row. "Interactive" means a human or a gating step is waiting (per his model-routing rule).

| Task class | Route (in order) | Why |
|---|---|---|
| Interactive coding, reviews, merge gates, prose needing judgment | **Claude Max (frontier)** | Quality floor for agentic reliability; subscription absorbs cost; cache-warm loops keep it fast ([agentic gap evidence](https://www.mindstudio.ai/blog/local-ai-vs-cloud-ai-2026)) |
| Overnight batch, Hermes background goals, drafts, extraction, summarization | **omlx qwen3.8** (warm cache) | Sunk-cost hardware, 0.1–0.3s TTFT warm, 262k context, `thinking_budget` tunable per phase; keep llama.cpp idle fallback as today |
| Bulk cheap classification/public-data enrichment | **FreeLLMAPI `notrain` pool → default pool → OpenRouter `:free`** | Free tiers are real but low-priority and rotating; hedge with fallback chains given ~18.5% first-attempt failure rates ([Novita](https://blogs.novita.ai/free-llm-api-comparison-2026/), [Tygart](https://tygartmedia.com/querying-llms-openrouter)) |
| Experiments, novel prompts, model shopping | **OpenRouter `:free` / budget-paid**, capped | $10 lifetime credit → 1,000 req/day; never production-depend on `:free` ([limits](https://openrouter.ai/docs/api_reference/limits)) |
| Stealth models (Ox Alpha et al.) | **Sandbox/experiment only**, expiry-dated | Preview subsidies graduate-or-vanish; Ox Alpha flagged for removal ~08-27 — re-check before routing anything through it ([explainx](https://explainx.ai/blog/openrouter-ox-alpha-stealth-model-august-2026)) |
| Sensitive data (client, VA-claim-adjacent, credentials) | **Local omlx only**, or paid Claude; never free/default pools | Free endpoints may retain/train per-provider policies; verify the full chain, not the reassuring layer ([data collection](https://openrouter.ai/docs/guides/privacy/data-collection)) |
| Budget-exhausted overflow | **Cascade downward automatically** (paid → owned subs → free → local) | Implement declaratively via LiteLLM `budget_fallbacks` + zero-cost exemption instead of hand-rolled logic — DR086 as config, not code ([docs](https://docs.litellm.ai/docs/proxy/budget_fallbacks)) |

Gateway hygiene: whatever meters traffic (gateway.mjs, LiteLLM) must be **byte-transparent** on the prefix — no timestamp injection, no key reordering, stable JSON serialization — or it silently converts cache hits into full-price misses on both Anthropic and OpenAI.

### 4.2 Cache-stable prompt layout spec (works for Hermes, Claude Code, opencode)

One canonical ordering; every harness maps its pieces onto these layers. Static grows downward; volatile stays at the bottom.

```
┌ L0  harness/system block      — identity, global rules        STABLE (months)
├ L1  tool definitions          — sorted by name, append-only   STABLE (per session)
│      · disable with tool_choice/allowed_tools, never splice
├ L2  project context           — CLAUDE.md/AGENTS.md digest    STABLE (per repo)
├ L3  task brief                — goal, constraints, done-def   STABLE (per session)
├ ──── cache breakpoint(s) here (Anthropic ≤4; OpenAI explicit on GPT-5.6+) ────
├ L4  conversation history      — append-only, never rewrite    GROWS
├ L5  retrieved docs / tool outputs — appended at the tail      VOLATILE
└ L6  volatile header data      — timestamps, user turn, IDs    LAST, inside final user msg
```

Rules (each maps to a cited mechanism):
1. **No mutable byte before L4.** Timestamps, counters, random IDs, dates ("today is…") go in L6 or the final user message — mutating an early byte invalidates everything after it on all providers ([OpenAI](https://developers.openai.com/api/docs/guides/prompt-caching), [Wentuo byte-identity](https://blog.wentuo.ai/en/claude-api-prompt-caching-pricing-5min-1hour-aws-bedrock-guide-en.html)).
2. **One model per session.** Caches are per-weights; switching providers/models mid-session forfeits the whole prefix (both providers document model as part of the cache key).
3. **Breakpoint discipline:** put explicit markers after L1/L3 boundaries; in explicit-only mode volatile suffixes are never written, avoiding wasted 1.25x writes ([OpenAI explicit mode](https://developers.openai.com/api/docs/guides/prompt-caching)).
4. **Warm before first real call:** Anthropic pre-warm via `max_tokens: 0`; locally, send a throwaway 1-token request after boot so omlx's hot cache holds L0–L3.
5. **Keep prefixes above cache minimums:** ≥1,024 tokens (GPT-5.6+ / most Claude tiers) or the discount never engages; pad with useful stable material if short ([minimum-length trap](https://developers.openai.com/api/docs/guides/prompt-caching)).
6. **Claude Code specifics:** export `CLAUDE_CODE_ATTRIBUTION_HEADER=0` when pointing CC at local llama.cpp-class backends; durable rules belong in CLAUDE.md (re-read after compact), never only in chat history ([cache-killer writeup](https://www.mykolaaleksandrov.dev/posts/2026/06/claude-code-llamacpp-prompt-cache-fix/), [CometAPI](https://www.cometapi.com/what-is-auto-compact-in-claude-code/)).
7. **After compaction, accept the reset:** first post-compact call is a partial miss by design — compact at phase boundaries, not mid-task, and compare total input cost rather than hit rate ([OpenAI gotcha](https://developers.openai.com/api/docs/guides/prompt-caching)).

### 4.3 Token-budget guardrails

| Guardrail | Threshold | Action | Basis |
|---|---|---|---|
| Session context usage | 70% | Warn; start writing structured state file | Community practice band 50–80% ([CometAPI](https://www.cometapi.com/what-is-auto-compact-in-claude-code/)) |
| Session context usage | 75% | **Proactive compact/rotate** with explicit handoff (don't wait for harness ~95% cliff) | Mike's doctrine confirmed optimal; CC main-thread override unavailable ([#24828](https://github.com/anthropics/claude-code/issues/24828)) |
| Session context usage | 90% | Snapshot state, kill or force-rotate | Buffer exhaustion risk; lossy emergency compaction ([ClaudeFast buffer analysis](https://claudefa.st/blog/guide/mechanics/context-buffer-management)) |
| Turn count | 80 turns | Snapshot + status block posted | Watchdog doctrine; matches LiteLLM `max_iterations` semantics ([agents doc](https://docs.litellm.ai/docs/proxy/users)) |
| Turn count | 100 turns | Hard stop, escalate | Same |
| Per-session spend (hosted paths) | e.g. $2/session soft, $5 hard | Soft: downgrade tier; hard: refuse + fall through cascade | LiteLLM `max_budget_per_session` / virtual keys ([budgets](https://docs.litellm.ai/docs/proxy/users)) |
| Free-tier budget | ≤20 RPM, ≤~900 req/day (leave headroom under 1,000) | Queue or shift to local | OpenRouter published limits ([limits](https://docs.litellm.ai/docs/proxy/users) → [OpenRouter](https://openrouter.ai/docs/api_reference/limits)) |
| Thinking budgets | mechanical/local calls: `thinking_budget` low (e.g., 500–2k) or off; plan/review: high | Deterministic ceilings on local; effort levels on Claude | [QwenCloud](https://docs.qwencloud.com/developer-guides/text-generation/thinking), [Anthropic effort](https://platform.claude.com/docs/en/build-with-claude/effort) |
| Cache health | track cached_tokens/input ratio per session; <50% on a long session = investigate | Fix prefix mutators (timestamps, gateway rewriting, attribution headers) | [monitoring guidance](https://developers.openai.com/api/docs/guides/prompt-caching) |

Implementation note (no-parallel-infrastructure): the watchdogs belong inside Hermes' existing turn loop and the spend caps inside the existing FreeLLMAPI gateway / a LiteLLM layer in front of hosted calls — do not stand up a separate metering service. Langfuse (or OTel→an existing collector) is the only new component worth adding, and only if per-call cost visibility is currently missing.

---

## SOURCES

Primary documentation:
1. Anthropic — Prompt caching: https://platform.claude.com/docs/en/build-with-claude/prompt-caching
2. Anthropic — Compaction (server-side): https://platform.claude.com/docs/en/build-with-claude/compaction
3. Anthropic — Effort parameter: https://platform.claude.com/docs/en/build-with-claude/effort
4. OpenAI — Prompt caching guide: https://developers.openai.com/api/docs/guides/prompt-caching
5. OpenAI — Prompt caching announcement (historical 50%): https://openai.com/index/api-prompt-caching/
6. OpenAI — Reasoning models guide: https://developers.openai.com/api/docs/guides/reasoning
7. OpenAI — Prompt Caching Dashboard: https://platform.openai.com/usage?usage_section=prompt-caching
8. vLLM — Automatic Prefix Caching: https://docs.vllm.ai/en/latest/features/automatic_prefix_caching.html and https://docs.vllm.ai/en/latest/design/prefix_caching/
9. llama.cpp — llama-server manpage (--cache-prompt/--cache-reuse/--cache-ram/--slot-save-path): https://manpages.debian.org/testing/llama.cpp-tools/llama-server.1.en.html
10. llama.cpp — Host-memory prompt caching tutorial (Discussion #20574, PR #16391): https://github.com/ggml-org/llama.cpp/discussions/20574
11. llama.cpp — Slot save/restore walkthrough (Discussion #9781): https://github.com/ggml-org/llama.cpp/discussions/9781
12. llama.cpp — --cache-reuse regression report (Issue #15082): https://github.com/ggml-org/llama.cpp/issues/15082
13. mlx-lm — Prompt-cache reuse defect (Issue #1494): https://github.com/ml-explore/mlx-lm/issues/1494
14. mlx-lm — Server KV quantization flags (PR #1353): https://github.com/ml-explore/mlx-lm/pull/1353
15. MLX-Textgen (multi-slot KV caches): https://github.com/nath1295/MLX-Textgen
16. cubist38/mlx-openai-server (prompt-cache-size/max-bytes/dir): https://github.com/cubist38/mlx-openai-server
17. OptiQ serve docs (automatic prefix reuse, mixed-precision KV): https://mlx-optiq.com/docs/serve
18. QwenCloud — Thinking / thinking_budget / reasoning_effort: https://docs.qwencloud.com/developer-guides/text-generation/thinking
19. LiteLLM — Router: https://docs.litellm.ai/docs/routing ; Budgets & agents: https://docs.litellm.ai/docs/proxy/users ; Budget fallbacks: https://docs.litellm.ai/docs/proxy/budget_fallbacks ; Spend tracking: https://docs.litellm.ai/docs/proxy/cost_tracking ; Auto-Router savings blog: https://docs.litellm.ai/blog/auto-router-production-savings
20. OpenRouter — Limits: https://openrouter.ai/docs/api_reference/limits ; Data collection: https://openrouter.ai/docs/guides/privacy/data-collection ; Free models: https://openrouter.ai/collections/free-models
21. Langfuse — Token & cost tracking: https://langfuse.com/docs/observability/features/token-and-cost-tracking ; OTel integration: https://langfuse.com/integrations/native/opentelemetry
22. OpenTelemetry GenAI semantic conventions: https://opentelemetry.io/docs/specs/semconv/gen-ai/ and https://github.com/open-telemetry/semantic-conventions-genai/blob/main/docs/gen-ai/gen-ai-spans.md

Secondary / practitioner (2025–2026):
23. Flexera — Prompt caching breakdown (cross-provider table): https://www.flexera.com/blog/ai/prompt-caching-breakdown
24. Alephant — Prompt vs semantic vs exact-match caching (TTL-default change): https://blog.alephant.io/prompt-caching-vs-semantic-caching-vs-exact-match
25. WentuoAI — Claude Code TTL/pricing guides (workspace isolation, Max 1h flag): https://blog.wentuo.ai/en/claude-code-prompt-caching-ttl-pricing-guide-en.html and https://blog.wentuo.ai/en/claude-api-prompt-caching-pricing-5min-1hour-aws-bedrock-guide-en.html
26. Prism/Ssimplifi — OpenAI caching explained (90% current discount): https://ssimplifi.com/blog/openai-prompt-caching-explained
27. ai-muninn — Disk KV restore proxy (7x): https://ai-muninn.com/en/blog/kv-cache-disk-restore-7x
28. Mykola Aleksandrov — Claude Code attribution header cache killer: https://www.mykolaaleksandrov.dev/posts/2026/06/claude-code-llamacpp-prompt-cache-fix/
29. TurboAI — CLAUDE_AUTOCOMPACT_PCT_OVERRIDE guide: https://www.turboai.dev/blog/claude-autocompact-pct-override-guide
30. BSWEN — Auto-compact env vars: https://docs.bswen.com/blog/2026-03-21-claude-code-auto-compact-settings/
31. CometAPI — What is auto-compact: https://www.cometapi.com/what-is-auto-compact-in-claude-code/
32. ClaudeFast — Context buffer management: https://claudefa.st/blog/guide/mechanics/context-buffer-management
33. badlogic — Compaction research across Claude Code/Codex/OpenCode/Amp: https://gist.github.com/badlogic/cd2ef65b0697c4dbe2d13fbecb0a0a5f
34. anthropics/claude-code issues #24828, #11819, #41818 (threshold configurability): https://github.com/anthropics/claude-code/issues/24828 etc.
35. niteagent — OTel GenAI field guide (renames): https://niteagent.com/blog/2026-08-07-otel-genai-agent-trace-field-guide/
36. groundcover — Self-hosted LLM observability: https://www.groundcover.com/guides/self-hosted-llm-observability-security
37. Uptrace — OTel for AI systems (metrics): https://uptrace.dev/blog/opentelemetry-ai-systems
38. Ginger Labs — LiteLLM router production guide: https://www.gingerlabs.ai/blog/litellm-router-setup-guide
39. BerriAI/litellm#37592 — cooldown-on-budget-exhaustion gap: https://github.com/BerriAI/litellm/issues/37592
40. Maxim/Bifrost — Rate limits & outage handling patterns: https://www.getmaxim.ai/articles/handle-llm-rate-limits-and-outages-with-an-ai-gateway/
41. Mirrowel/LLM-API-Key-Proxy — rotation/cooldown library: https://github.com/Mirrowel/LLM-API-Key-Proxy/blob/main/src/rotator_library/README.md
42. Novita — Free LLM API comparison (verified limits, Aug 2026): https://blogs.novita.ai/free-llm-api-comparison-2026/
43. ask-coreai — OpenRouter free models limits & catches: https://ask-coreai.com/blog/openrouter-free-models-2026-limits-catches
44. flo2 — OpenRouter free tier limits: https://flo2.com/blog/openrouter-free-tier-limits
45. rlnorthcutt gist — OpenRouter free models + July 2026 deprecations: https://gist.github.com/rlnorthcutt/e6f392cd1ffb1339cc42dfb024c3cf7f
46. explainx — Ox Alpha stealth model forensics (retention/expiry caveats): https://explainx.ai/blog/openrouter-ox-alpha-stealth-model-august-2026
47. Tygart Media — 54-model OpenRouter reliability run: https://tygartmedia.com/querying-llms-openrouter
48. Godfrey Yang — LLM model selection playbook (tier cascades): https://godinim.github.io/2026/llm-model-selection
49. FutureAGI — SLM vs LLM 2026 (hybrid routing default; NVIDIA arXiv:2506.02153): https://futureagi.com/blog/comparison-slm-llm-language-models
50. Zosma — Local vs cloud performance benchmarks: https://www.zosma.ai/blogs/local-ai-models-vs-cloud-performance-comparison
51. MindStudio — Local vs cloud AI 2026 (agentic gap): https://www.mindstudio.ai/blog/local-ai-vs-cloud-ai-2026
52. PromptQuorum — Local LLM trade-offs: https://www.promptquorum.com/local-llms/local-llm-limitations
53. Inferensys — Thinking budget vs reasoning effort: https://inferensys.com/differences/multimodal-foundation-model-benchmarking/extended-thinking-mode-implementations/claude-45-thinking-budget-control-vs-gpt-5-reasoning-effort-api
54. spinchange notes — Anthropic adaptive thinking modes: https://spinchange.github.io/vulture-nest/anthropic-adaptive-thinking.html
55. Local artifacts (read-only inspection): `~/.omlx/settings.json` (hot_cache_max_size 8GB, ssd_cache_dir, initial_cache_blocks 256, preserve_mid_system_cache true, v1.0); `~/.omlx/model_settings.json` (qwen3.8 alias, max_context_window 262144, thinking_budget_enabled true, turboquant_kv disabled)

Confidence notes: Claude Code TTL-by-subscription and default-TTL-change claims rest on secondary sources (#23–25) — verify against Anthropic pricing pages before spending decisions. omlx internals cited from local config files, not public docs. Exact auto-compact percentages vary by Claude Code version (#29–32 disagree: ~83% vs ~95%); the actionable fact (no configurable main-thread threshold) is consistent across primary GitHub issues.
