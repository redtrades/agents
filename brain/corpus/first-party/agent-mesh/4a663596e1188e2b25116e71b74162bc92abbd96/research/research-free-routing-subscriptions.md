# Maximizing Free Tiers & Subscriptions + Resilient LLM Routing With Auto-Fallback

**Researched 2026-08-26 · web sources primary-doc-first, practitioner reports 2025–2026 · read-only research artifact**

Scope: inventory of genuinely generous free LLM APIs as of Aug 2026, depletion/rate-limit fallback automation (LiteLLM semantics, health probing, circuit breakers), legitimate Claude-Max-class subscription maximization plus an explicit ToS-violation zone, stealth-model risk management, and a concrete routing policy for Mike's stack (local omlx :8300, FreeLLMAPI gateway :3100, OpenRouter, Claude Max, candidate Gemini/GitHub tiers).

---

## TL;DR decisions

1. **GitHub Models is dead** — fully retired 2026-07-30. Remove it from every plan and config comment that still names it ([GitHub docs](https://docs.github.com/en/github-models/use-github-models/prototyping-with-ai-models)). Several free-tier directories still list it as live — stale-directory data is itself a finding.
2. **Cerebras killed its always-free tier** mid-2026: new accounts get $5 trial credits requiring a verified payment method, expiring in 30 days; official FAQ states "no no-cost tier that renews automatically" ([rate-limits FAQ](https://inference-docs.cerebras.ai/support/rate-limits), [changelog](https://inference-docs.cerebras.ai/support/change-log)). Demote it from "permanent free" to "trial credits."
3. **Gemini free tier survives but shrank**: Flash/Flash-Lite families only since ~April 2026, ~1,000–1,500 RPD, trains on free-tier input by default, and enabling billing on a project deletes its free tier permanently — keep free testing on a separate never-billed project ([rate limits](https://ai.google.dev/gemini-api/docs/rate-limits), [billing trap](https://usagebox.com/articles/gemini-api-billing-free-tier-confusion)).
4. **Anthropic closed the subscription-arbitrage loophole**: since Jan 9 / Apr 4, 2026, Max-plan OAuth works **only inside Claude Code/Claude.ai**; third-party harnesses are server-blocked and accounts get banned. Legitimate maximization happens *inside* Claude Code scheduling, not through proxies ([The Register](https://www.theregister.com/software/2026/02/20/anthropic-clarifies-ban-on-third-party-tool-access-to-claude/5014546), [VentureBeat](https://venturebeat.com/technology/anthropic-cracks-down-on-unauthorized-claude-usage-by-third-party-harnesses)).
5. **Ox Alpha is a textbook stealth listing**: live since 2026-08-20, sole no-training carve-out among 14 stealth models, expected lifespan of the class is 1–2 weeks. Never a dependency; keep an exit date ([census](https://www.digitalapplied.com/blog/openrouter-stealth-model-census-who-they-turned-out-to-be)).

---

## 1. Free-tier inventory 2026

Only providers with a **current, verifiable** no-cost offering are listed. "Training posture" = what happens to your inputs by default on the free tier. Verify before relying: this landscape changes without notice (Google cut free quotas 50–80% in Dec 2025 alone — [usagebox](https://usagebox.com/articles/gemini-api-billing-free-tier-confusion)).

| Provider | Free allowance (2026-08) | Rate caps | Context | Training on free input (default) | Reliability notes |
|---|---|---|---|---|---|
| **Google AI Studio / Gemini API** | Flash + Flash-Lite families only; ~1,000–1,500 RPD/model | ~10–15 RPM, ~250K TPM | 1M | **Yes** (opt-out unavailable on free; EEA/UK/CH exempt) | RPD resets midnight PT; per-project not per-key; limits revised unannounced; enabling billing kills free tier on that project |
| **Groq** | Per-model daily quotas, e.g. gpt-oss-120b/qwen3.6-27b: 1K RPD, prompt-guard 14.4K RPD | 30 RPM, **8K TPM on most text models** (binding constraint), 70K TPM on compound | up to 262K | No — explicit no-train policy, free and paid | Very reliable; TPM 8K means big-context agent calls must go elsewhere |
| **OpenRouter `:free`** | 50 RPD if you've never bought credits; **1,000 RPD once ≥$10 lifetime credits** | 20 RPM hard | model-dependent (up to 1M) | Varies per model; most `:free` endpoints log/train; toggles exist | Rotating catalog (~25–29 models); popular models drop with no warning; negative balance blocks even free models (402) |
| **Cloudflare Workers AI** | 10,000 Neurons/day (≈$0.11/day value); frontier models (kimi-k2.x, glm-5.2, deepseek-v4) need paid plan | Neuron-metered, no fixed RPM published | up to large | No (enterprise-grade privacy posture) | Solid; good embeddings + mid-size Llama/Qwen/GPT-OSS; resets 00:00 UTC |
| **Mistral la Plateforme / AI Studio** | "Experiment"/Free mode: included monthly usage, ~1B tokens/mo reported | ~1 req/s (harsh concurrency cap) | up to 256K | **Yes — opt-out required** in Admin Console (Privacy toggle) immediately after signup | Phone verification; fine as diversity tier, not throughput |
| **NVIDIA NIM (build.nvidia.com)** | Trial usage, no time limit; credit system replaced by per-model rate limits | **~40 RPM baseline per model**, unpublished, no official increase path on free | up to 1M | Retention/training terms per model — check each card | Anonymous-ish (phone verify); agentic loops hit 429 constantly per forum reports |
| **OVH AI Endpoints** | Keyless/anonymous OK | 2 req/min per model anonymous (tight) | 262K | No training language found in catalog notes (best keyless data story) | Confirmed working locally via FreeLLMAPI |
| **Kilo Gateway** | Free, 200 req/hr per IP | 200/hr | up to 1M | **Logs prompts/outputs for training** (stated in FreeLLMAPI source) | Good throughput; sensitive content never goes here anyway (gateway boundary) |
| **Cerebras** | ⚠️ Changed: $5 trial credits / 30 days, payment method required; formerly 1M tokens/day always-free | Free tier historically 5 RPM / 30K TPM / 1M TPH / 1M TPD | 8K cap on free | No | Fastest tokens/sec in class when it worked; treat as dead-for-planning until policy reverts |
| **Z.AI (Zhipu)** | GLM-4.x-Flash models free | dynamic, per-model | 200K | Check per-model | GLM-5.2 via NVIDIA NIM is the community's top free workhorse by volume |
| **ModelScope** | 58 free models (Qwen/DeepSeek/GLM families) | registration-based | up to 1M | China-platform terms — treat as public-data | Needs Aliyun-cn binding for some models |
| **GitHub Models** | ❌ **RETIRED 2026-07-30** — playground, catalog, inference API all gone | — | — | — | Azure AI Foundry is the named successor; Copilot plans give separate model access |

Sources: [Groq](https://console.groq.com/docs/rate-limits) · [Gemini](https://ai.google.dev/gemini-api/docs/rate-limits)/[pricing](https://ai.google.dev/gemini-api/docs/pricing) · [OpenRouter limits](https://openrouter.ai/docs/api-reference/limits) · [Workers AI pricing](https://developers.cloudflare.com/workers-ai/platform/pricing/) · [Mistral](https://docs.mistral.ai/admin/billing-usage/usage-limits)/[help center](https://help.mistral.ai/en/articles/698531-why-am-i-hitting-api-rate-limits-and-how-do-i-increase-them) · [NVIDIA forum: credit system→rate limits](https://forums.developer.nvidia.com/t/request-more-4-000-credits-option-on-build-nvidia-com/344567), [40-RPM thread](https://forums.developer.nvidia.com/t/request-for-nvidia-build-api-rate-limit-increase-40-rpm-200-rpm/377605) · [Cerebras](https://inference-docs.cerebras.ai/support/rate-limits) · [GitHub Models retirement](https://docs.github.com/en/github-models/use-github-models/prototyping-with-ai-models). Cross-checked against maintained directories: [cheahjs/free-llm-api-resources](https://github.com/cheahjs/free-llm-api-resources), [xyzs996/free-llm-api](https://github.com/xyzs996/free-llm-api) (verified-per-provider, sources reviewed 2026-07-25), [open-free-llm-api/awesome-freellm-apis](https://github.com/open-free-llm-api/awesome-freellm-apis) (daily-refreshed; note it still lists GitHub Models — stale), and the [FreeLLMAPI catalog](https://freellmapi.co/models.html) (~7.4B free tokens/month across 34 providers, [repo](https://github.com/tashfeenahmed/freellmapi)). Note on the brief's "zai-freellm/free-llm-api": no such org was found; the canonical resources-repo lineage is **cheahjs/free-llm-api-resources** with xyzs996's verified fork-family as the 2026 successor generation.

**Practical reading of the table:** Groq (fast, no-train, low TPM) + Cloudflare (no-train, neuron-budgeted) + Gemini Flash-Lite on a dedicated unbilled project (1K+ RPD, trains by default) + OpenRouter `:free` after a one-time $10 top-up (1K RPD) covers ~95% of non-sensitive bulk work. That matches the notrain-pool design already running on the local gateway.

---

## 2. Depletion & fallback automation

### 2.1 LiteLLM semantics (the vocabulary to copy even if you don't run LiteLLM)

From the [routing docs](https://docs.litellm.ai/docs/routing) and [fallback docs](https://docs.litellm.ai/docs/proxy/reliability):

- **Cooldowns are per-deployment, not per-model-group.** Defaults: `allowed_fails: 3` failures in a minute, then `cooldown_time: 5s` out of rotation. A deployment is cooled **immediately** on a 429; also cooled on >50% failure rate in the current minute; and (importantly) on some *non*-retryable errors (401/404/408).
- **Fallback classes are separated**: `fallbacks` (everything else: 429, 5xx), `context_window_fallbacks`, `content_policy_fallbacks`. Ordered lists; `default_fallbacks` catch misconfigured groups. Fallback to a specific `model_info.id` **skips cooldown checks** — useful for "wake me only when primary recovers" escape hatches.
- **Deployment ordering**: `order: 1/2/3` in `litellm_params` gives priority escalation with per-level retry budgets before falling through to cross-group fallbacks. This is exactly the shape of a cascade table.
- **Retries**: `num_retries` ranks request-header > request-body > deployment > global; exponential backoff for RateLimitError, immediate retry for generic errors, `retry_after` floor. LiteLLM pins the provider SDK's own retries (`max_retries: 0`) to prevent `(1+N)²` call amplification — replicate this discipline in any custom stack.
- **Budgets**: [provider_budget_config](https://docs.litellm.ai/docs/proxy/provider_budget_routing) tracks spend per provider over a period (Redis-backed multi-instance) and returns `"No deployments available - crossed budget"` as a 429 when exhausted — i.e., **budget exhaustion surfaces through the same path as rate limiting**, so fallback chains catch it naturally. There is no separately named `budget_fallbacks` knob; the semantic is "budget-exhausted deployment becomes unavailable, router moves on." `/provider/budgets` exposes remaining budget for proactive probing.
- **Observability**: spend logs record `attempted_fallbacks` and `original_model_group` per row — measure fallback rate as a first-class metric (see 2.4).
- Caveat learned from practitioners: cooldown defaults (5s) are tuned for paid-API blips. For free tiers with **daily** quotas (RPD exhaustion), a 5-second cooldown just burns requests against a dead bucket — see 2.2.

### 2.2 Detecting credit-depleted vs rate-limited vs down (the three failure classes)

The single highest-value design idea in the 2026 practitioner literature: **classify errors into different buckets and give them different recovery timers** ([flatkey](https://flatkey.ai/blog/circuit-breaker-llm-api-gateway), [Parvesh Saini gateway guide](https://parveshsaini.com/blog/enterprise-llm-gateway), [DevOpsNess field report](https://www.devopsness.com/blog/architecture-review-llm-gateway-design-for-multi-provider-inference)):

| Signal class | Examples | Correct response | Recovery timer |
|---|---|---|---|
| **Rate-limited (transient)** | 429 with `retry-after`; per-minute RPM/TPM caps | Cooldown seconds, honor `retry-after`, immediate failover | Seconds–minutes |
| **Quota/credit-depleted (account state)** | OpenRouter 402 or RPD-exhausted 429; "quota"/"billing"/"insufficient_quota" in error body; Gemini RPD until midnight PT | **Do not retry.** Failover instantly; mark route dead until known reset; alert owner | Hours–days (align to reset wall-clock: midnight PT for Gemini, 00:00 UTC for CF/OVH, 5h windows for Claude) |
| **Down/degraded (health)** | 500/502/503/504, timeouts, connection resets | Retry budget (1–2 attempts w/ backoff), then open breaker | Minutes, half-open probes |

Concrete detection mechanics people run:

- **Parse error bodies, not just codes**: OpenAI-style `insufficient_quota` vs generic 429; OpenRouter carries `error.metadata.provider_code` upstream codes and distinguishes platform-vs-provider 429s ([limits doc](https://openrouter.ai/docs/api-reference/limits)); Groq returns rich headers (`x-ratelimit-remaining-requests/-tokens`, `retry-after`) **always**, not just on 429 — poll them proactively ([Groq docs](https://console.groq.com/docs/rate-limits)).
- **Proactive quota polling**: OpenRouter `GET /api/v1/key` returns `limit_remaining`, `usage_daily`, `is_free_tier` — check before dispatching batch jobs, not after 402s. LiteLLM `/provider/budgets` equivalent. FreeLLMAPI tracks per-(platform,model,key) RPM/RPD/TPM/TPD counters that "learn providers' reported ceilings" ([repo](https://github.com/tashfeenahmed/freellmapi)).
- **Reset-wall alignment**: store per-route reset times (midnight PT, midnight UTC, rolling 5h) and gate reactivation on the wall clock, not on blind retries. A depleted Gemini project at 09:00 PT is dead for 15 hours; no amount of retrying fixes that.

### 2.3 Circuit-breaker designs people actually run

Three patterns recur across 2026 practitioner posts:

1. **Per-provider isolation, shared nothing.** The most common production anti-pattern is one global breaker — one provider's outage cascades into all routes. Breakers must be per-provider *and* per-route/sensitivity-class ([ankurm Spring gateway](https://ankurm.com/llm-gateway-pattern-java-microservices/), [DeepInspect](https://www.deepinspect.ai/blog/ai-gateway-circuit-breaker)). This maps directly onto FreeLLMAPI's sensitivity profiles: the `notrain` pool's breaker state must never let a `notrain` request leak to a non-notrain provider during degradation.
2. **Classic thresholds + half-open probes.** resilience4j-shape: trip at ~50% failure over a window (LiteLLM's allowed_fails/cooldown is the same idea in-the-box); hold open ~90s; admit 3–10 labeled probe requests in half-open; require all success criteria before closing; double cooldown on failed recovery, capped (~30 min) ([DeepInspect](https://www.deepinspect.ai/blog/ai-gateway-circuit-breaker), [flatkey](https://flatkey.ai/blog/circuit-breaker-llm-api-gateway)).
3. **Cost-velocity breaker (the LLM-era addition).** A runaway agent loop returns HTTP 200 forever — error-rate breakers never trip while the meter runs. Trip a second breaker on token-spend velocity vs a workload-relative baseline (e.g., >10× planned rate sustained), plus a dumb hard token cap per session behind it ([dreaming.press](https://dreaming.press/posts/circuit-breaker-for-llm-api-calls.html)). For free-tier routing the same pattern applies inverted: a loop silently exhausts the day's entire RPD across providers — cap requests-per-session per pool.
4. **Failover stickiness.** Once failed over to provider Y for a route, pin subsequent requests to Y for ~60s; prevents flapping against a half-recovered primary ([DevOpsNess](https://www.devopsness.com/blog/architecture-review-llm-gateway-design-for-multi-provider-inference)). FreeLLMAPI's 30-minute sticky sessions implement a stronger version.
5. **Open-state actions are a decision, not a default.** Fallback / queue / degrade / **fail closed**. Policy/safety blocks and quota exhaustion should generally fail closed rather than silently reroute — silent fallback past a sensitivity boundary is the nightmare case for the notrain pool ([flatkey](https://flatkey.ai/blog/circuit-breaker-llm-api-gateway)).

### 2.4 Retry-budget hygiene

- Decide deliberately whose retries are authoritative: SDK-default retries (OpenAI/Anthropic SDKs retry twice by default with 600s read timeout) stack invisibly under your router's retries ([dreaming.press](https://dreaming.press/posts/circuit-breaker-for-llm-api-calls.html)). Set SDK `max_retries=0`, own retries in the router.
- Total attempt budget per request: 2–4 attempts across the whole cascade (e.g., primary ×1 backoff, then next provider, max_fallbacks≈5 ceiling like LiteLLM's weighted failover).
- Honor `Retry-After` where present (Groq, OpenRouter both send it); exponential backoff + jitter otherwise.
- Watch **fallback rate** as a leading indicator: rising fallback percentage predicts provider incidents hours before status pages update; also watch tokens-per-request drift (silent model swap signal — see §4) ([DevOpsNESS](https://www.devopsness.com/blog/architecture-review-llm-gateway-design-for-multi-provider-inference), [Saini](https://parveshsaini.com/blog/enterprise-llm-gateway)).

### 2.5 FreeLLMAPI-specific guidance

What the platform gives you natively ([repo README](https://github.com/tashfeenahmed/freellmapi)): automatic fallover on 429/5xx **with cooldowns and key rotation**; six routing strategies ranked by live speed/capability/reliability scores; unified models with strict in-group failover; per-key rate tracking that learns ceilings; sticky sessions (30 min) with optional compact context-handoff note on mid-chat switch; `X-Routed-Via` response header proving which provider served each call; `auto:<profile>` per-request profile selection; MCP endpoint for agents to introspect model/provider health mid-session.

Known trade-offs stated by the project itself: effective intelligence dips late in the day as top models hit daily caps, resetting UTC midnight; no SLA anywhere in the pool.

Local-install specifics (from `~/agent-reports/freellmapi-install/SETUP-REPORT.md`): the v0.8.3 pinned install predates some current features; the **monthly catalog snapshot** on free installs lags the live feed ~30 days / ~300 models — quota changes arrive late, so don't assume the DB's stored ceilings match provider reality; the weekly routine below includes a live-probe step to compensate. Note the brief's "zai-freellm" lineage pointer resolves to cheahjs's repo (above); FreeLLMAPI itself is tashfeenahmed/freellmapi.

---

## 3. Subscription maximization (legitimate) + the ToS warning zone

### 3.1 What the contracts actually say (2026)

| Provider | Binding rule | Source |
|---|---|---|
| Anthropic Consumer ToS (eff. 2025-10-08) | §2: may not share account login/API key/credentials or make the Account available to anyone else. §3(2): no reselling the Services. §3(7): except via an Anthropic API key or where explicitly permitted, no automated/non-human access. | [consumer-terms](https://www.anthropic.com/legal/consumer-terms) |
| Anthropic legal-compliance page (Feb 2026 clarification) | "Using OAuth tokens obtained through Claude Free, Pro, or Max accounts in any other product, tool, or service — including the Agent SDK — is not permitted." OAuth is for Claude Code and Claude.ai only. Enforcement may occur "without prior notice." | quoted in [The Register](https://www.theregister.com/software/2026/02/20/anthropic-clarifies-ban-on-third-party-tool-access-to-claude/5014546) |
| Anthropic enforcement reality (Jan–Apr 2026) | Server-side client-identity checks killed header-spoofed harnesses (OpenCode, OpenClaw, CLIProxyAPI, Cline-with-OAuth); Apr 4, 2026 cut off OpenClaw-class frameworks entirely; erroneous auto-bans occurred and were reversed. Multiple Max accounts are explicitly *not* a violation (Anthropic staff, on record); **sharing and reselling are**. | [VentureBeat](https://venturebeat.com/technology/anthropic-cracks-down-on-unauthorized-claude-usage-by-third-party-harnesses), [TNW](https://thenextweb.com/news/anthropic-openclaw-claude-subscription-ban-cost), [MetricNexus](https://metricnexus.ai/blog/anthropic-banning-multiple-claude-accounts) |
| OpenAI | Terms: "You may not share your account credentials or make your account available to anyone else." Services Agreement §3.3: no buying/selling/transferring API keys, no interfering with or circumventing rate limits or usage limits. Account Sharing Policy: one person per consumer account. | [Terms](https://openai.com/policies/row-terms-of-use/), [Services Agreement](https://openai.com/policies/services-agreement/), [Sharing policy](https://help.openai.com/en/articles/10471989-openai-account-sharing-policy) |
| Google (Gemini CLI / Code Assist) | Abuse detection explicitly targets "using Gemini CLI oAuth with third-party software"; since 2026-03-25 free-tier CLI users are Flash-only, traffic prioritized by license type and account standing. AI Pro = 1,500 CLI req/day; Code Assist individual = 1,000/day; API-key free tier = 250/day. Also: from 2026-06-19 the Gemini API rejects unrestricted API keys entirely. | [quota doc](https://github.com/google-gemini/gemini-cli/blob/main/docs/resources/quota-and-pricing.md), [service update](https://github.com/google-gemini/gemini-cli/discussions/22970) |

### 3.2 The warning zone — flagged, not recommended

These are documented-and-enforced violations as of 2026. Any tool or pattern in this class risks the entire $200/mo asset:

- **OAuth-proxy farms**: tools that extract the Max plan's OAuth token and serve it as an OpenAI-compatible endpoint to arbitrary harnesses (the CLIProxyAPI/OpenClaw class; the "max-your-cc-sub"-style billing/compliance-flagged tooling already surfaced to Mike in MASTER-GUIDE §7 sits adjacent to this space). Server-side client-identity verification makes these technically dead as well as ToS-dead.
- **Account sharing/reselling** of subscription capacity in any direction — including "my agents are me" arguments have failed for others; enforcement keys on behavioral fingerprints (shared IP + parallel heavy loops reads as resale).
- **Harness spoofing** (sending Claude Code's client headers from another binary) — explicitly named enforcement target; caused collateral bans.
- **Circumventing usage limits** — OpenAI's §3.3(i) names it; Anthropic's weekly-limit announcement explicitly cited 24/7 background Claude Code loops as abuse driving the change ([TechCrunch](https://techcrunch.com/2025/07/28/anthropic-unveils-new-rate-limits-to-curb-claude-code-power-users/)).

### 3.3 Legitimate maximization patterns

Within the rules, the levers are *when* and *where* work runs, not how to smuggle it through unofficial clients:

1. **Respect the real quota shape.** Max 20x ($200): ~900 messages/5h rolling window, plus weekly overall + weekly Opus limits ≈ 240–480 Sonnet-hours and 24–40 Opus-hours/week; overage purchasable at API rates ([help center](https://archive.ph/G51jH), [fewertools analysis](https://fewertools.com/pulse/anthropic-weekly-limits-aug-2025/)). Plan agentic sessions against the 5-hour window boundaries rather than discovering them mid-run.
2. **Session scheduling to avoid contention** (Mike's observed 12+-session OAuth contention, MASTER-GUIDE §4): serialize long Claude Code sessions through a simple lease/queue (the machine already has a leases mechanism for gpu-heavy/omlx-restart — extend that, don't build a parallel scheduler, per `rules/no-parallel-infrastructure.md`). Cap concurrent Claude Code processes at 2–3; stagger batch starts across 5-hour windows; move anything non-interactive off Claude entirely (below).
3. **Offload bulk work down-stack**: interactive/judgment work stays on Claude Max; extraction/classification/embedding/summarization goes to FreeLLMAPI's notrain pool or local omlx; nightly batch windows burn free-tier RPDs that reset overnight anyway (UTC-midnight resets align naturally with a 23:00–06:00 batch window).
4. **Batch-window usage**: schedule overnight runs against providers whose quotas reset at night (Gemini RPD at midnight PT ≈ 03:00 ET; CF/OVH at 00:00 UTC = 20:00 ET) so the full daily budget is fresh at job start.
5. **Opus discipline**: Opus consumes limits ~5× faster than Sonnet; reserve it for the subset of tasks that demonstrably need it, `/model` down mid-session ([help center](https://archive.ph/G51jH)).
6. **Keep the paid surface official**: Claude Code only, on the sanctioned binary; if a third-party harness is truly required for some workflow, that workflow belongs on API keys or on a different vendor's properly licensed path — never on subscription OAuth.

---

## 4. Stealth-model risk management

What the class is: OpenRouter's Stealth Program hosts anonymized models, free, for a limited window, **so the anonymous provider can collect user content for training** — that's the stated consideration ([Stealth EULA](https://openrouter.ai/terms/stealth)). A census of all 14 listings since Apr 2025 shows typical lifespan 1–2 weeks, 13 of 14 defaulted to training-in-scope terms, identities usually revealed by first-party statement after retirement ([Digital Applied census](https://www.digitalapplied.com/blog/openrouter-stealth-model-census-who-they-turned-out-to-be)). Ox Alpha (listed 2026-08-20, 1M ctx, $0/$0, mandatory reasoning, no-training carve-out — the sole exception) fits the pattern exactly; community fingerprinting points at the Zhipu GLM-5.x lineage, unconfirmed. Precedent (owl-alpha, buried 2026) says the slug retires and, if it resolves to a named commercial model, the successor lands at list price.

Policy, in order of importance:

1. **Never-depend rule.** No workflow, profile, or fallback chain may have a stealth model as a load-bearing member. Today the `code` profile pins to Ox Alpha *alone* (PROFILE-POLICY.md) — that violates this rule and needs a second member (§5). Every stealth dependency gets a written removal date at adoption time (MASTER-GUIDE already flags ~2026-08-27 for Ox Alpha — that's tomorrow; execute it or consciously renew with eyes open).
2. **Rotation policy**: rotate any stealth slot out of active routing every 7 days regardless of observed health; re-admit only after a fresh capability probe. Track candidates on [aimodelgraveyard.com/provider/openrouter](https://aimodelgraveyard.com/provider/openrouter/) or the OpenRouter deprecations feed rather than discovering deaths via 404s.
3. **Capability probes before promotion**: standardized mini-suite (tool-call round-trip, JSON-schema adherence, context-fill test, latency sample) run against any new free/stealth model *before* it enters a profile pool — FreeLLMAPI's dashboard playground or a scripted curl suffices; the point is evidence, not vibes (`rules/verification-law.md` applies to model choice too).
4. **Detect silent swaps/degradations**:
   - Log `X-Routed-Via` (FreeLLMAPI) and OpenRouter's `model`/`provider` fields on every response; alert on unexpected changes for a pinned alias.
   - Token-count drift detector: same fixed prompt daily, compare reported token counts — a jump means tokenizer/model swap underneath (this is exactly how the community fingerprinted Ox Alpha).
   - Quality canary: one fixed eval prompt per profile per week; score manually if needed. Falling quality + stable 200s = swap, not outage (per DevOpsNess drift-detection practice).
   - Watch OpenRouter model-page metadata diffs (context length, pricing, data-policy wording changes) — the census showed data-terms wording changes precede reveals.
5. **Data-posture asymmetry**: remember the *default* stealth contract trades your prompts for training. Ox Alpha's carve-out is a policy statement, not a technical guarantee, and is unique among 14. Treat all stealth traffic as public-data traffic — which the gateway boundary already enforces structurally.

---

## 5. Recommended policy for Mike's stack

### 5.1 Cascade table

Ordering principle: sensitivity boundary first (never let a pool's breaker push traffic outside its data class — fail closed beats leak), then capability, then cost.

| Task class | Primary | Fallback chain | Kill-switch |
|---|---|---|---|
| Interactive / judgment / frontier drafting | Claude Max via Claude Code (leased, ≤2–3 concurrent) | local omlx Qwen3 (degraded-mode note to user) | **Fail closed** — never spill Claude work into free pools (data + quality); alert, queue for next 5h window |
| Bulk extraction / classification (non-sensitive, notrain-safe) | FreeLLMAPI notrain pool: Groq gpt-oss-120b / qwen3.6 | Cloudflare (qwen3.8-27b, gpt-oss-120b) → OVH → local omlx | Fail closed to omlx-only mode; never leave notrain pool on 429-storm |
| Coding loops (`X-Sensitivity: code`) | Ox Alpha **until 2026-08-27 review**, then promote replacement | local omlx coder model (Qwen3-Coder-class) → Groq qwen3.8/coder-capable | If ox-alpha 404s/deploys degraded: auto-demote, pin code profile to omlx + Groq, no scramble |
| Business / tool-calling (`business` pool) | Groq tool-capable set (gpt-oss-120b/20b, safeguard, qwen3.6) | Cloudflare gpt-oss-120b (tools confirmed) → omlx | Fail closed; tool-calling fidelity is a correctness constraint, don't fall back to non-tool models |
| Embeddings / cheap vectors | Cloudflare Workers AI (neuron-budgeted) | Gemini embedding on the unbilled free project | Hard-stop at neuron budget; queue to tomorrow 00:00 UTC |
| Nightly batch / scheduled digests | Gemini Flash-Lite (unbilled project, 1K RPD) → Groq remainder | Cloudflare → OpenRouter `:free` (post-$10, 1K RPD) | Job aborts cleanly, resumable, if <20% daily budget remains at start |
| Research/exploration (public data) | OpenRouter `:free` rotation | FreeLLMAPI Default pool → omlx | Kill any `:free` model showing training-in-scope terms if content ever stops being public |
| Everything, final backstop | **local omlx** | llama.cpp idle fallback | Queue + notify Mike; never auto-upgrade to paid APIs without approval (spending is Mike-only per MASTER-GUIDE §8) |

Router settings worth copying regardless of implementation: per-deployment `order` levels matching the table; `allowed_fails≈2–3`/min with `cooldown_time` scaled by failure class (seconds for 429-transient, hours aligned to reset walls for quota-depleted); failover stickiness 60s; total attempt budget ≤4; per-session token/request caps (cost-velocity guard); SDK retries zeroed; log `attempted_fallbacks`-equivalents everywhere.

### 5.2 FreeLLMAPI pool-hygiene fix (profile drift)

Root cause is already understood and patched locally: `reinstateUpstreamRetiredCatalogModel()` used to re-enable models into *every* profile on catalog-sync, bloating curated pools toward whole-catalog (agent-configs#14, fixed 2026-08-25, DB pruned per `PROFILE-POLICY.md`). Remaining recommendations:

1. **Make drift detection continuous, not episodic**: run the PROFILE-POLICY drift query on a schedule and alert on any count mismatch (`notrain` ⊆ {cloudflare,groq,ovh,requesty}; `code` = exactly 1 openrouter row; `business` ⊆ groq). Fold it into the existing launchd/consolidation machinery rather than a new scheduler.
2. **Regression-test the invariant**: a unit test asserting `profileAllowsReinstatement()` respects `CURATED_*` sets for all four profiles, exercised on every catalog-sync code change — the bug class was "sync path mutates membership," so the test belongs at that layer.
3. **Treat the monthly snapshot lag as a quota risk**: stored ceilings trail provider reality by up to 30 days on the free feed; the weekly routine's live probes (below) are the compensation. Premium live-feed ($19/yr) is the cheap mechanical fix if drift incidents recur — flag to Mike, his call (spending decision).
4. **Re-pin `code` profile per §5.1** — single-member pool contradicts the never-depend rule; add the omlx/Groq members so a stealth death degrades instead of severing.

### 5.3 Weekly quota-hygiene routine (any agent can run)

A checklist, runnable end-to-end read-only except the drift prune (which needs approval):

1. **Pool-drift check** — run the sqlite query in `PROFILE-POLICY.md` §"Checking current drift"; any platform leaking into `notrain`/`code`/`business` = file issue, do not self-prune without approval.
2. **Live-probe every pool member** — one minimal completion per enabled provider through the gateway; record HTTP status + `X-Routed-Via`. New 401 (dead key), persistent 429 (ceiling changed), 404 (model retired) → update catalog expectations.
3. **Quota-ledger snapshot** — `GET openrouter.ai/api/v1/key` (limit_remaining, usage_daily, is_free_tier); Groq limits page / response headers; Cloudflare neuron usage in dashboard; Gemini AI Studio per-project RPD. Record against expected budgets; investigate any provider consumed >80% by unknown callers.
4. **Token-canary diff** — fire the fixed fingerprint prompt (one per profile) and compare token counts + first-100-chars hash vs last week's log; a change = possible silent model swap (§4.4).
5. **Stealth-slot audit** — any stealth/`:free` model older than 7 days in an active profile: confirm its removal date is still defensible or demote it. Check aimodelgraveyard/OpenRouter announcements for pending deprecations touching enabled models.
6. **Fallback-rate review** — from gateway audit.log / analytics: fallback % per pool over 7d. Sustained >~1–2% on any pool = primary unhealthy, investigate before it becomes an incident.
7. **Subscription headroom** — Claude Max: confirm weekly-window consumption trend (Claude Code's own usage output), confirm no session was started outside the lease queue; flag if projected to hit weekly caps early two weeks running (that's a "buy extra usage vs shift workloads" decision — Mike's).
8. **Config drift** — confirm gateway denylist intact, ENCRYPTION_KEY still set in the plist (one-time restart decryption break still pending per PROFILE-POLICY.md), catalog-sync logs clean.

---

## SOURCES

Primary docs & terms:
- Groq rate limits — https://console.groq.com/docs/rate-limits
- Gemini API rate limits — https://ai.google.dev/gemini-api/docs/rate-limits · Gemini pricing — https://ai.google.dev/gemini-api/docs/pricing
- OpenRouter limits/status codes — https://openrouter.ai/docs/api-reference/limits · Stealth Program EULA — https://openrouter.ai/terms/stealth
- Cloudflare Workers AI pricing — https://developers.cloudflare.com/workers-ai/platform/pricing/
- Cerebras rate limits — https://inference-docs.cerebras.ai/support/rate-limits · changelog (free-tier change) — https://inference-docs.cerebras.ai/support/change-log
- Mistral usage/limits — https://docs.mistral.ai/admin/billing-usage/usage-limits · help center (tiers) — https://help.mistral.ai/en/articles/698531-why-am-i-hitting-api-rate-limits-and-how-do-i-increase-them
- GitHub Models retirement — https://docs.github.com/en/github-models/use-github-models/prototyping-with-ai-models
- NVIDIA developer forums (credit→rate-limit change; 40 RPM baseline; no free-tier increases) — https://forums.developer.nvidia.com/t/request-more-4-000-credits-option-on-build-nvidia-com/344567 · https://forums.developer.nvidia.com/t/request-for-nvidia-build-api-rate-limit-increase-40-rpm-200-rpm/377605
- LiteLLM routing — https://docs.litellm.ai/docs/routing · fallbacks/reliability — https://docs.litellm.ai/docs/proxy/reliability · budget routing — https://docs.litellm.ai/docs/proxy/provider_budget_routing
- Anthropic Consumer ToS (eff. 2025-10-08) — https://www.anthropic.com/legal/consumer-terms
- OpenAI Terms — https://openai.com/policies/row-terms-of-use/ · Services Agreement — https://openai.com/policies/services-agreement/ · Account Sharing Policy — https://help.openai.com/en/articles/10471989-openai-account-sharing-policy
- Gemini CLI quotas/pricing — https://github.com/google-gemini/gemini-cli/blob/main/docs/resources/quota-and-pricing.md · gemini-cli service update (abuse detection, Mar 2026 changes) — https://github.com/google-gemini/gemini-cli/discussions/22970
- FreeLLMAPI — https://github.com/tashfeenahmed/freellmapi · catalog — https://freellmapi.co/models.html

Practitioner reports & directories (2025–2026):
- Anthropic third-party-harness ban & OAuth clarification — https://www.theregister.com/software/2026/02/20/anthropic-clarifies-ban-on-third-party-tool-access-to-claude/5014546 · https://venturebeat.com/technology/anthropic-cracks-down-on-unauthorized-claude-usage-by-third-party-harnesses · https://thenextweb.com/news/anthropic-openclaw-claude-subscription-ban-cost · https://metricnexus.ai/blog/anthropic-banning-multiple-claude-accounts · https://tacavar.com/blog/claude-max-proxy-loophole-closed-agent-sdk-migration/
- Claude weekly rate limits (Aug 2025) — https://techcrunch.com/2025/07/28/anthropic-unveils-new-rate-limits-to-curb-claude-code-power-users/ · https://archive.ph/G51jH (Anthropic help: Pro/Max usage) · https://fewertools.com/pulse/anthropic-weekly-limits-aug-2025/
- Circuit breakers & gateways — https://flatkey.ai/blog/circuit-breaker-llm-api-gateway · https://www.deepinspect.ai/blog/ai-gateway-circuit-breaker · https://dreaming.press/posts/circuit-breaker-for-llm-api-calls.html · https://ankurm.com/llm-gateway-pattern-java-microservices/ · https://parveshsaini.com/blog/enterprise-llm-gateway · https://www.devopsness.com/blog/architecture-review-llm-gateway-design-for-multi-provider-inference
- Stealth-model census — https://www.digitalapplied.com/blog/openrouter-stealth-model-census-who-they-turned-out-to-be · deprecation tracker — https://aimodelgraveyard.com/provider/openrouter/
- Free-tier directories (cross-check; staleness noted inline) — https://github.com/cheahjs/free-llm-api-resources · https://github.com/xyzs996/free-llm-api · https://github.com/open-free-llm-api/awesome-freellm-apis · https://github.com/xinrui-z/free-llm · https://perkstack.co/blog/openrouter-free-models · https://tokenmix.ai/blog/cerebras-api-key-rate-limits-free-tier-2026 · https://pricepertoken.com/endpoints/mistral/free
- Gemini free-tier behavior analyses — https://usagebox.com/articles/gemini-api-billing-free-tier-confusion · https://pecollective.com/tools/gemini-free-tier-guide/

Local artifacts referenced:
- `~/agent-reports/freellmapi-install/PROFILE-POLICY.md` (pool definitions, drift-check SQL, encryption-key caveat)
- `~/agent-reports/freellmapi-install/SETUP-REPORT.md` (keyless provider ground truth, boundary architecture)
- `~/agent-configs/MASTER-GUIDE.md` §4 (stack topology, ox-alpha expiry flag, OAuth contention observation) · §7 (max-your-cc-sub compliance flag)
