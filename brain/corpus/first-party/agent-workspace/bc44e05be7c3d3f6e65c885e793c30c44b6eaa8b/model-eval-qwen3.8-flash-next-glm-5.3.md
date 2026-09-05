# Adoption evaluation: Qwen3.8-Flash-Next, GLM-5.3 and GLM-5.3-Flash

Research date: 2026-08-26. All claims below carry a source URL and were accessed on 2026-08-26 unless noted.
Nothing in this document comes from model recall. All three releases postdate the knowledge cutoff.

Scope note: this is research and proposal only. No config was changed and no service was restarted.

---

## 1. Verdicts

| Model | Verdict | One-line reason |
|---|---|---|
| Qwen3.8-Flash-Next | **Skip for local. Defer on hosted.** | Smallest *complete* quant is 67.67 GB against a ~59 GB ceiling, an 8.7 GB miss at 3.0 bits per parameter. Re-examined in section 6 after challenge; verdict holds, reason changed. |
| GLM-5.3 | **Trial, hosted only, via OpenRouter direct.** | Reachable today, cross-family reviewer value is real, but it is unusually verbose and its weights are not out yet. |
| GLM-5.3-Flash | **Trial for high-volume batch, hosted, behind a structured-output bake-off. Skip for local.** | The economics are a genuine step change for triage and extraction. Reasoning cannot be disabled and JSON mode is not schema-enforced, so a hard gate cannot trust it yet. Local would fix cost and data exposure, but the smallest artifact in existence is 194.69 GB. Sections 5 and 6. |

**The one thing to act on this week, and it does not depend on either model:** grammar-constrained decoding with xgrammar on a model that *already* fits under 59 GB solves the exact structured-output failure that blocks the triage gate, at zero marginal cost and with no data-retention exposure. Section 6.5.

### What would change the Qwen verdict

Superseded by section 6.6, which re-derives this from measured repository sizes rather than one publisher's table. Kept here for the record:

- A working MLX quant at 3-bit or better that lands under ~54 GB with usable KV headroom, with someone other than the uploader reporting it runs. The real floor today is 67.67 GB, not the 78 GB stated below.
- Qwen releasing a smaller sibling on this architecture. The card compares against `Qwen3.8-27B`, which is a different model on the older architecture, not a small version of this one.
- Qwen3.8-Flash-Next appearing on OpenRouter or OpenCode Zen at a price competitive with what we already route to. Neither lists it today.

### What would change the GLM verdict

- Weights landing on `zai-org` (promised for roughly 2026-08-28) would open a self-host option and change the license calculus. It would not change the local-fit answer for our hardware; this is a ~750B model.
- Independent agentic-coding numbers on our own harness. Adopt-now becomes defensible if it holds up on our tier 1 review tasks against a cheaper incumbent.
- Reading Z.ai's data terms in full and confirming no-training. Until that is confirmed by reading the policy directly, keep it out of the notrain pool.

### What would change the GLM-5.3-Flash verdict

- A measured pass rate on strict JSON across a few hundred real notices. Above roughly 99.5% with a schema validator and a retry, it moves to adopt for triage. Below that, it stays a suggestion engine feeding a human or a stricter model.
- Confirmed rate limits and sustained concurrency. The cost case is decided; the throughput case is not.
- The same data-policy read that gates GLM-5.3. Same caution applies.

### Correction to an earlier method in this document

Section 3.1 originally established that GLM-5.3 weights were absent by querying the Hugging Face org listing endpoint (`/api/models?author=zai-org&sort=createdAt`). That endpoint turns out to be unreliable: it does **not** return `zai-org/GLM-5.3-Flash` even though that repo exists with `createdAt` of 2026-08-25, which is newer than every entry it does return. The GLM-5.3 conclusion still holds, because a direct lookup of `huggingface.co/zai-org/GLM-5.3` and its API record both return empty, but the method was weaker than presented. Direct model-ID lookups were used for everything in section 5.

---

## 2. Qwen3.8-Flash-Next

### 2.1 What it actually is

| Property | Value | Source |
|---|---|---|
| Release date | 2026-08-26 (today) | [GitHub README, News section](https://github.com/QwenLM/Qwen3.8-Flash-Next/) |
| Type | Multimodal MoE causal LM with vision encoder | [HF model card](https://huggingface.co/Qwen/Qwen3.8-Flash-Next-FP8) |
| Total parameters | 125B main + 51B n-gram embedding + 4B MTP | HF model card, Model Overview |
| Active per token | 6B | HF model card |
| HF-reported tensor size | 180B params | HF model card, Safetensors panel |
| Layers / hidden dim | 48 / 2560 | HF model card |
| Experts | 512 total, 10 routed + 1 shared active | HF model card |
| Attention | Hybrid Gated DeltaNet + Qwen Sparse Attention (QSA) | HF model card |
| Context | 262,144 native, extensible to 1,000,000 via YaRN | HF model card |
| Weights open | Yes | [HF collection](https://huggingface.co/collections/Qwen/qwen38-flash-next) |
| License | Qwen Community License 1.0 | [LICENSE](https://huggingface.co/Qwen/Qwen3.8-Flash-Next/raw/main/LICENSE) |
| MTP head | Yes. 1 layer, ~4B params, trained multi-step | HF model card |

License detail that matters for us: Qwen Community License 1.0 permits internal commercial use freely. It requires a separate license from Qwen only if you run a "Model as a Service" or "AI Work Assistant" business, and that carve-out explicitly excludes internal use where outputs and model capabilities are not made available to third parties. Attribution on the UI is required only above 100M MAU or US$20M monthly revenue. For our internal pipeline this is permissive. Source: [LICENSE text](https://huggingface.co/Qwen/Qwen3.8-Flash-Next/raw/main/LICENSE).

### 2.2 Relationship to the Qwen3.8 we already serve

This is the part most likely to be misread, so stating it plainly:

**Qwen3.8-Flash-Next is a distinct checkpoint on a new architecture. It is not a serving mode, not a quantization, and not a drop-in replacement for any existing Qwen3.8 model.**

Evidence:

- The HF config reports `model_type: qwen4_exp` and architecture `Qwen4ExpForConditionalGeneration`, not a Qwen3.8 architecture. Source: [HF API for a derived repo](https://huggingface.co/api/models/inferencerlabs/Qwen3.8-Flash-Next-MLX-Q9), which carries the base config.
- Qwen describes it as "an early preview of the architecture used in Qwen4" and says it "plays the same role that Qwen3-Next played for Qwen3.5." Source: [GitHub README](https://github.com/QwenLM/Qwen3.8-Flash-Next/).
- The model card benchmarks it *against* `Qwen3.8-27B` as a separate baseline model, which is what you would expect for a different checkpoint, not a variant of the same one. Source: HF model card benchmark table.
- Separately, `Qwen3.8-Flash` (no "Next") is a **different, hosted-only product**: "Qwen3.8-Flash is the official version based on Qwen3.8-Flash-Next with more production features, e.g., 1M context length by default, official built-in tools." Source: HF model card, top note. So there are three distinct things in play: `Qwen3.8-27B` (older arch, open), `Qwen3.8-Flash-Next` (new arch, open), `Qwen3.8-Flash` (new arch, Qwen Cloud hosted).

Practical consequence: swapping model IDs in a serving config will not work. Different architecture, different chat template, different sampling defaults, different tool-call format (`<tool_call><function=name><parameter=x>` XML rather than JSON), and a `reasoning_effort` parameter with values `xhigh` / `medium` / `low` where `xhigh` is the default. Any prompt or parser tuned to the current Qwen3.8 would need rework.

**Unverified:** I could not determine which specific Qwen3.8 checkpoint we currently serve, because `~/.hermes/config.yaml` and the omlx launchd plist are outside the folder I have access to. The comparison above is against the public Qwen3.8 family, not against our actual deployed artifact.

### 2.3 Benchmarks, and how much to trust them

**Every number below is vendor-published. As of today no independent evaluator has scored this model.** Artificial Analysis has no page for it, LMArena has no listing, and no Aider polyglot or third-party SWE-bench run exists. That is expected given it shipped hours ago, but it means the entire benchmark picture is Alibaba grading its own homework.

Vendor numbers relevant to our pipeline, from the [HF model card](https://huggingface.co/Qwen/Qwen3.8-Flash-Next-FP8):

| Benchmark | Qwen3.8-Flash-Next | Best baseline in table | What it tells us |
|---|---|---|---|
| SWE-bench Pro (Claude Code harness) | 62.5 | Qwen3.8-27B 61.7, Claude-Opus-4.6 53.4 | Agentic coding |
| SWE-bench Multilingual (mini-SWE-agent) | 81.0 | Claude-Opus-4.6 77.5 | Cross-language repair |
| DeepSWE 1.1 | 58.7 | DeepSeek-V4-Flash 54.4 | Agentic coding |
| NL2Repo-Bench | 48.1 | DeepSeek-V4-Flash 54.2 | Repo-scale generation. It loses here. |
| Toolathlon Verified (Pass@1) | 73.5 | DeepSeek-V4-Flash 70.3 | Real-world tool use |
| IFBench | 81.3 | Qwen3.8-27B 79.5 | Instruction following |
| LiveCodeBench v6 | 91.9 | DeepSeek-V4-Flash 90.6 | Competitive coding |
| CoWorkBench | 73.9 | Qwen3.8-27B 70.7 | In-house benchmark, unreproducible |

Skepticism notes worth carrying:

- `CoWorkBench` and `RecreationBench` are described in the card's own footnotes as in-house benchmarks. Treat as marketing.
- The SWE-bench Pro footnote says "Problematic tasks were corrected and all baseline models were re-evaluated on the refined benchmark." Qwen modified the benchmark, then reran competitors on their modified version. That is not the published SWE-bench Pro number for anyone in the table.
- HLE is "judged by GPT-4o" per footnote 6, which is a weak judge for a frontier-level eval.
- For MathVision and CharXiv the footnote states Qwen used a fixed prompt for itself but took "the higher score between runs" for other models. That cuts against them, so it is a point in favor of honesty, but it confirms the table is not apples to apples.
- Long-context retrieval specifically: **no needle-in-haystack, RULER, or comparable long-context retrieval score appears anywhere in the card.** The 262K native and 1M extended figures are capacity claims, not retrieval-quality claims. This is a gap for our pipeline.
- Structured-output reliability: not benchmarked. The card documents structured tool-call syntax but publishes no reliability metric.

### 2.4 Can we run it locally

> Section 6 revisits this in depth with measured repository sizes and an evaluation of SSD expert streaming. Read 6.2, 6.4 and 6.6 for the current answer. This subsection is the original first pass.

**No. Not at any quantization that preserves quality, and not at any quantization at all under our ceiling.**

Unsloth, who had day-zero access from Qwen, publishes this hardware table (units are total RAM plus VRAM, or unified memory). Source: [Unsloth docs](https://unsloth.ai/docs/models/qwen3.8-next.md):

| 1-bit | 2-bit | 3-bit | 4-bit | 6-bit | 8-bit |
|---|---|---|---|---|---|
| 78 GB | 85 GB | 100 GB | 110 GB | 128 GB | 156 GB |

Against our real ceiling of ~59 GB for omlx (leaving ~5 GB for the OS):

- 8-bit needs 156 GB. Over by ~97 GB.
- 4-bit needs 110 GB. Over by ~51 GB.
- Even 1-bit needs 78 GB. Over by ~19 GB.

Unsloth's own text confirms the floor: "You will need at least 78 GB of RAM or unified memory to run the model. Its smallest quantized version is larger than usual because of the model's architecture." They recommend a 96 GB machine as the practical minimum.

> **Superseded by section 6.2.** These figures come from one publisher's table. Measuring actual repository bytes across every quantized checkpoint gives a tighter floor of **67.67 GB of weights** (Vontra `MLX-oQ2`, 3.008 bits/param), against Unsloth's own 72.55 GB `UD-IQ1_S`. The 78 GB above is a total-system figure including runtime overhead, so it is consistent, but 67.67 GB is the number to argue against. The conclusion does not change; the margin narrows from ~19 GB to 8.7 GB.

Sanity check from first principles: HF reports 180B parameters of tensors. At 4 bits per weight that is ~90 GB of weights before KV cache, activations, or the vision tower. At 8 bits it is ~180 GB. The Unsloth figures are consistent with the parameter count. This is not a case where a smarter quant recipe closes a 20 percent gap; the shortfall is structural.

One architectural detail that looks like a way out but is not: the 51B n-gram embedding table (20M bigram/trigram entries at layer 2) is explicitly designed to be "asynchronously offloaded to host memory." On a discrete-GPU box that moves 51B params off the accelerator. On Apple unified memory there is no separate host pool to offload into, so it buys nothing. Source: [HF model card](https://huggingface.co/Qwen/Qwen3.8-Flash-Next-FP8), N-gram Embedding section.

Per the brief, that is where the local question ends. The rest of this subsection is recorded for completeness only.

**MLX conversion status (informational).** Checked via the HF models API on 2026-08-26:

- `inferencerlabs/Qwen3.8-Flash-Next-MLX-Q9` is a real in-progress conversion. Created 14:54 UTC, last modified 15:19 UTC. `library_name: mlx`, tags include `qwen4_exp`. It declares 16 safetensor shards; only 6 were present at check time, already totalling ~60 GB. Zero downloads. Source: [HF API](https://huggingface.co/api/models/inferencerlabs/Qwen3.8-Flash-Next-MLX-Q9?blobs=true).
- `Vontra/Qwen3.8-Flash-Next-MLX-8bit`, `-MLX-4bit`, `-MLX-oQ4`, `-MLX-oQ2`, `-MLX-oQ6` are **empty placeholder repos**. The 8-bit repo contains only `.gitattributes` and reports `usedStorage: 0`. Source: [HF API](https://huggingface.co/api/models/Vontra/Qwen3.8-Flash-Next-MLX-8bit?blobs=true).
- Every MLX-tagged repo for this model has zero downloads. Nobody has run these.

**Unverified:** whether upstream `mlx-lm` supports the `qwen4_exp` architecture. A GitHub code search against `ml-explore/mlx-lm` returned no result, and the GitHub releases API returned an empty body through the fetch tool. Qwen's own README lists SGLang, vLLM, TokenSpeed, transformers, llama.cpp and Unsloth as supported runtimes and does not mention MLX at all. Treat MLX support as unconfirmed. This does not affect the verdict, since the memory ceiling decides it either way.

**Draft / MTP head for speculative decoding.** The checkpoint does ship one: "MTP: 1 layer, trained with multi-steps," counted as ~4B params. Source: HF model card, Model Overview. So the speculative-decoding path we run today would in principle have a native drafter here. It is moot while the model does not fit. There is a community project, [MTPLX](https://github.com/youssofal/MTPLX), doing native MTP speculative decoding on MLX for Qwen 3.8 27B, which is worth a look for our *existing* setup independent of this evaluation.

### 2.5 How we would reach it if not local

Poorly, today.

- **Not on OpenRouter.** No `qwen3.8-flash-next` listing found. OpenRouter carries Qwen3.8 Max, Qwen3.7 Flash, Qwen3.6 Flash. Source: [OpenRouter Qwen models](https://openrouter.ai/qwen).
- **Not on OpenCode Zen.** The Zen model table (docs last updated 2026-08-25) lists Qwen3.7 Max, Qwen3.7 Plus, Qwen3.6 Plus, Qwen3.5 Plus. No 3.8 of any kind. Source: [OpenCode Zen docs](https://opencode.ai/docs/zen/).
- **HF Inference Providers: none.** The model card states "This model isn't deployed by any Inference Provider," with an open request thread asking for support.
- **Qwen Cloud direct** is the vendor path, and the production variant there is `Qwen3.8-Flash`, not `-Next`. Source: [HF model card](https://huggingface.co/Qwen/Qwen3.8-Flash-Next-FP8) top note, pointing to [qwencloud.com](https://www.qwencloud.com/models/Qwen3.8-Flash). **Unverified:** I could not retrieve Qwen Cloud pricing for Qwen3.8-Flash. Third-party pricing roundups covered Qwen3.8-Max and Qwen3.7-Flash but not this model.

**Unverified:** whether it is reachable through the FreeLLMAPI gateway on `:3100`. That is a local service and I have no network path to it from this session. Check with `curl -s localhost:3100/v1/models | jq -r '.data[].id' | grep -i qwen3.8` before assuming either way.

### 2.6 Fit against how we work

Under the standing rule, local models handle non-time-sensitive overnight and batch work. Qwen3.8-Flash-Next cannot be a local model on this hardware, so it cannot fill that slot. That is the whole story.

As a hosted model it would compete for the interactive slot, where we already have paths that work and this one has no reachable endpoint through OpenRouter, Zen, or the gateway. There is no version of "adopt now" that survives contact with those two facts.

Cross-model review value: Qwen is a genuinely different family from Claude, so it would satisfy the tier 1 different-family reviewer requirement. But we can already get Qwen-family review through Qwen3.7 Plus or Qwen3.7 Max on Zen at $0.40/$1.60 and $2.50/$7.50 per million. This release adds no new *family*, only a new checkpoint in a family we can already reach.

---

## 3. GLM-5.3

### 3.1 What it actually is

| Property | Value | Source |
|---|---|---|
| Vendor | Zhipu AI, operating internationally as Z.ai | [The Decoder, 2026-08-14](https://the-decoder.com/zhipu-ai-releases-glm-5-3-claims-its-the-strongest-open-weights-coding-model/) |
| Release date | 2026-08-14 per vendor and press; 2026-08-18 per OpenRouter and Artificial Analysis | [OpenRouter](https://openrouter.ai/z-ai/glm-5.3), [Artificial Analysis](https://artificialanalysis.ai/models/glm-5-3) |
| Base model | Same base as GLM-5.2. All gains from post-training. | [Z.ai docs](https://docs.z.ai/guides/llm/glm-5.3) |
| Architecture | MoE (GLM-5 family, `glm_moe_dsa` per the GLM-5.2 repo tags) | [HF zai-org listing](https://huggingface.co/api/models?author=zai-org) |
| Parameters | 753B per Artificial Analysis. Press reports 743B/744B. Z.ai's own model page states no count. | [Artificial Analysis FAQ](https://artificialanalysis.ai/models/glm-5-3) |
| Context | 1,000,000 tokens | [Z.ai docs](https://docs.z.ai/guides/llm/glm-5.3), [OpenRouter](https://openrouter.ai/z-ai/glm-5.3) |
| Max output | 128K per Z.ai docs; 131,072 per OpenRouter | both above |
| Modality | Text in, text out. Not multimodal. | Z.ai docs, Artificial Analysis |
| Reasoning | Always on, cannot be disabled. Effort `low` / `high` / `max`, default `max`. | [Z.ai docs](https://docs.z.ai/guides/llm/glm-5.3) |
| Weights open | **Not yet.** | see below |

The date discrepancy is most likely announcement (Aug 14) versus general API availability (Aug 18). Both are recorded rather than resolved. The parameter-count discrepancy is unresolved and Z.ai has not published a figure on its own model page.

**Weights status, verified directly.** As of 2026-08-26 the GLM-5.3 weights are **not** on Hugging Face. Querying the `zai-org` org sorted by creation date returns `GLM-5.2` (created 2026-06-16) as the newest text model. No GLM-5.3 repo exists. Source: [HF API, zai-org](https://huggingface.co/api/models?author=zai-org&sort=createdAt&direction=-1&limit=15), accessed 2026-08-26.

Z.ai committed to open weights roughly two weeks after launch, once security reviews complete, which puts the drop around 2026-08-28. Source: [The Decoder](https://the-decoder.com/zhipu-ai-releases-glm-5-3-claims-its-the-strongest-open-weights-coding-model/). Artificial Analysis currently classifies the model as **Proprietary**, weights not publicly available. Source: [Artificial Analysis](https://artificialanalysis.ai/models/glm-5-3).

So the "strongest open-weights coding model" framing in the press is a claim about a future state. Right now it is a closed model with an announced intent.

The security-review delay has a specific cause worth knowing: Z.ai trained GLM-5.3 heavily on vulnerability discovery, and it scores at or near the top of cyber-offense benchmarks. Releasing those weights is a different decision from serving them behind a monitored API, and Z.ai says so.

### 3.2 Benchmarks

**Vendor-published**, from [Z.ai's model documentation](https://docs.z.ai/guides/llm/glm-5.3):

| Benchmark | GLM-5.2 | GLM-5.3 | Note |
|---|---|---|---|
| Terminal-Bench 3.0 | 4.6 | 28.3 | Large jump off a very low base |
| DeepSWE v1.1 | 46.2 | 66.9 | Agentic coding |
| Agents' Last Exam | 23.8 | 28.5 | |
| Z.ai Code Bench (max effort) | 23.4% @ 96K tok | 34.5% @ ~75K tok | **In-house, private benchmark** |
| Z.ai Code Bench (high effort) | n/a | 31.4% @ ~50K tok | Beats Claude Opus 4.8 at 29.5% @ 120K |
| CyberGym | 77.2 | 84.5 | Best on benchmark, ahead of Mythos 5 at 83.8 |
| ExploitBench | 24.4 | 54.4 | Still well behind Mythos 5 at 78.0 |
| ExploitGym (6h budget) | 39 tasks | 130 tasks | Mythos 5 at 247 |

Credit where due: Z.ai's own writeup states plainly that GLM-5.3 "remains behind Claude Fable 5, which reaches 39.5% at Max effort," and that on the exploitation benchmarks "the wider the remaining gap to the closed frontier." A vendor page that names where it loses is more trustworthy than one that does not. That said, Z.ai Code Bench is private and unreproducible, and the headline "50% better coding" figure is measured on it.

**Independent**, from [Artificial Analysis](https://artificialanalysis.ai/models/glm-5-3):

| Metric | Value | Context |
|---|---|---|
| Intelligence Index v4.1.1 | **60** | Rank #9 of 187 in its class. Median for the comparison group is 35. |
| Output speed | 90.0 tok/s | Above the 73.9 median for similar reasoning models |
| TTFT | 1.65s | Better than the 2.88s median |
| Output tokens to run the index | **170M** | Median is 72M. It is roughly 2.4x more verbose than typical. |
| Cost to run the full index | $1,238.50 | |
| Cost per index task | $0.68 | |
| Cache discount | 81% | |

The Intelligence Index v4.1.1 aggregates nine evals including Terminal-Bench v2.1 (agentic coding and terminal use), τ³-Banking (agentic tool use), SciCode, AA-LCR (long context reasoning) and AA-Omniscience (hallucination). Artificial Analysis runs these itself rather than accepting vendor submissions, which is what makes the 60 meaningful. Source: [AA Intelligence Index methodology](https://artificialanalysis.ai/evaluations/artificial-analysis-intelligence-index).

**Unverified:** I could not extract the individual per-eval sub-scores (Terminal-Bench v2.1, τ³-Banking, AA-LCR specifically) from the Artificial Analysis page, which renders them in charts rather than text. Those three are the ones that matter most for our pipeline. Worth pulling manually before committing.

**Unverified:** no Aider polyglot score for GLM-5.3 was found. No independent SWE-bench Verified run was found. Searches surfaced only vendor claims and secondary blog aggregation.

The verbosity number is the one to plan around. Reasoning is always on and defaults to `max`. At 170M tokens across the AA index versus a 72M median, output-token cost is where the bill lands, and $4.40 per million output is not a rounding error at that volume. Z.ai's own data shows effort tuning works: `high` effort hit 31.4% at ~50K tokens per task versus `max` at 34.5% for ~75K. Roughly 9% relative capability for 50% more tokens.

### 3.3 How we reach it

| Path | Status | Detail |
|---|---|---|
| **OpenRouter** | **Available** | Model ID `z-ai/glm-5.3`. $1.40 in / $4.40 out per million, $0.26 cache read. One provider only (Z.ai direct), so no routing decisions and no fallback. 100% uptime over 3 days, 99.77% availability, 35 tok/s throughput, 3.88s P50 latency measured by OpenRouter. Source: [OpenRouter](https://openrouter.ai/z-ai/glm-5.3) |
| **OpenCode Zen** | **Not available** | Zen lists GLM 5.2, GLM 5.1, GLM 5 only. Docs last updated 2026-08-25. Source: [Zen docs](https://opencode.ai/docs/zen/) |
| **Direct Z.ai API** | **Available** | Model `glm-5.3`. Three protocols: OpenAI Chat Completions at `https://api.z.ai/api/paas/v4`, OpenAI Responses at `https://api.z.ai/api/v1`, Anthropic Messages at `https://api.z.ai/api/anthropic`. Source: [Z.ai docs](https://docs.z.ai/guides/llm/glm-5.3) |
| **FreeLLMAPI gateway :3100** | **Unverified** | No network path from this session. Check the gateway's own model list. |

Capabilities confirmed by Z.ai docs: function calling, structured output (JSON), context caching, streaming. All four matter for our pipeline and all four are documented rather than inferred.

**GLM-5.3-Flash** is a separate, cheaper, and notably *multimodal* sibling released today, 2026-08-26. $0.075 in / $0.25 out per million, currently at a 50% discount off a $0.15 / $0.50 list price. 1M context, 131,072 max output, 27 tok/s, 3.28s latency, one provider. Source: [OpenRouter](https://openrouter.ai/z-ai/glm-5.3-flash). At roughly 1/19th the output price of GLM-5.3 this is worth a look for high-volume batch review where top-end capability is not required. No independent scores exist for it yet.

**Free or preview tier.** There is no free tier of the GLM Coding Plan; the entry tier is Lite at $18/month. Secondary sources reference a `coding-glm-5.3-free` endpoint with 5 requests/minute, 500 requests/day and 1M tokens/day, but I could not confirm this against Z.ai's own documentation. **Treat as unverified.**

**Update: the Ox Alpha question is now resolved.** OpenRouter's FAQ raised "Was ZAI GLM-5.3 Flash the stealth model Ox Alpha?" and Z.ai's own documentation answers it: "Before release, we tested GLM-5.3-Flash anonymously as ox-alpha on OpenCode and OpenRouter to gather user feedback." Source: [Z.ai docs, GLM-5.3-Flash](https://docs.z.ai/guides/vlm/glm-5.3-flash.md). What this does and does not mean for us is worked through in section 5.4.

### 3.4 Data and training terms

This is the item that gates routing through the notrain pool, and it is the item I am least able to close out from here.

What is established:

- **OpenCode Zen**, as a gateway, states: "All our models are hosted in the US. Our providers follow a zero-retention policy and do not use your data for model training," with an enumerated exception list. GLM models are not on the exception list. But GLM-5.3 is not on Zen at all, so this protection does not currently apply to it. Source: [Zen docs, Privacy](https://opencode.ai/docs/zen/).
- **Z.ai** publishes a privacy policy and a Data Processing Addendum covering API services. Search results summarize it as stating that Z.ai does not store content that customers provide or generate, processing it in real time. Source: [Z.ai privacy policy](https://docs.z.ai/legal-agreement/privacy-policy).

**Unverified and important:** I did not successfully read the Z.ai privacy policy or DPA text directly. The characterization above comes from search-result summarization, not from the source document. Before routing anything sensitive to `z-ai/glm-5.3`, read [https://docs.z.ai/legal-agreement/privacy-policy](https://docs.z.ai/legal-agreement/privacy-policy) end to end and confirm the training clause explicitly. Do not put GLM-5.3 in the notrain pool on the strength of a search summary.

Note also that going through OpenRouter adds OpenRouter's own data policy on top of Z.ai's, and OpenRouter forwards every GLM-5.3 request to Z.ai directly since Z.ai is the sole provider. OpenRouter's ZDR controls are documented at [openrouter.ai/docs/guides/features/zdr](https://openrouter.ai/docs/guides/features/zdr) and are worth configuring if we route there.

**Rate limits: unverified.** Secondary sources report the paid Z.ai API now offers unlimited concurrency and that Coding Plan limits are dynamic and undisclosed, ranked Max > Pro > Lite. There is a public GitHub issue titled "[Critical] GLM-5.2 API is unusable due to severe rate limiting" on `zai-org/GLM-5`, which suggests capacity problems have bitten users before. Source: [GitHub issue #83](https://github.com/zai-org/GLM-5/issues/83). Z.ai has not published a rate-limit table I could locate. Plan for the possibility of throttling on long batch runs.

### 3.5 Fit against how we work

**Interactive and blocking work.** Hosted, so it qualifies under the standing rule. But reasoning cannot be disabled and defaults to `max`. At 3.88s P50 latency (OpenRouter measurement) plus deep-reasoning token generation, `max` effort is wrong for anything a human is waiting on. Use `reasoning_effort: low` or `high` for interactive paths. Z.ai's migration note is explicit that requests carrying `thinking.type: "disabled"` will **fail** against `glm-5.3`, so any existing GLM-5.2 call sites that disable thinking need editing before the model ID changes.

**Overnight and batch work.** This is where it fits best. Verbosity stops being a latency problem and becomes a cost line you can budget. At `max` effort on real agentic tasks Z.ai measured ~75K output tokens per task, which is roughly $0.33 per task in output tokens at $4.40/M. That is workable for review passes and unattended runs.

**Cross-model review, tier 1 merge policy.** This is the strongest argument for GLM-5.3, and it is worth separating from raw capability. The tier 1 policy requires a reviewer from a different model family than the author. GLM is a genuinely distinct lineage: different lab, different architecture family (`glm_moe_dsa`), different post-training regime. It is not a Qwen derivative and not a Claude derivative. A reviewer drawn from it will fail differently than the author, which is the entire point of the rule. At Intelligence Index 60 it is capable enough that its disagreements are worth reading rather than noise.

The cyber-security post-training is a genuine differentiator here too. A reviewer that reasons about exploitation chains will flag a class of defect that a general coding model routinely walks past. For merge review specifically, that is useful signal, not a curiosity.

Against that: we already have GLM 5.2 on OpenCode Zen at the identical $1.40 / $4.40 price with Zen's zero-retention guarantee attached. If cross-family review is the goal and cost is equal, GLM-5.2-via-Zen is the lower-risk incumbent and GLM-5.3-via-OpenRouter has to earn the switch on measured quality, not on vendor claims.

---

## 4. If adopting GLM-5.3: concrete steps

Proposal only. Nothing below has been applied.

**Important caveat:** I could not read `~/.hermes/config.yaml` or the omlx launchd plist. Only `~/agent-workspace` is accessible from this session. The snippets below are templates that need reconciling against the actual file structure, not drop-in patches.

### 4.1 Model identifiers

| Path | Exact identifier |
|---|---|
| OpenRouter | `z-ai/glm-5.3` |
| OpenRouter, cheap sibling | `z-ai/glm-5.3-flash` |
| Z.ai direct | `glm-5.3` |
| Z.ai base URL (OpenAI-compatible) | `https://api.z.ai/api/paas/v4` |
| Z.ai base URL (Anthropic-compatible) | `https://api.z.ai/api/anthropic` |

### 4.2 Hermes config sketch

```yaml
# ~/.hermes/config.yaml  -- PROPOSED, not applied
# Reconcile shape against the existing file before editing.
models:
  glm-5.3-review:
    provider: openrouter
    model: z-ai/glm-5.3
    base_url: https://openrouter.ai/api/v1
    api_key_env: OPENROUTER_API_KEY
    # Reasoning cannot be disabled on this model.
    # max is the default; do not leave it there for anything interactive.
    extra_body:
      reasoning_effort: high
    max_tokens: 32768
    role: reviewer            # tier 1 cross-family reviewer
    family: glm               # must differ from author family
    time_sensitive: true      # hosted, so eligible for blocking work

  glm-5.3-batch:
    provider: openrouter
    model: z-ai/glm-5.3
    base_url: https://openrouter.ai/api/v1
    api_key_env: OPENROUTER_API_KEY
    extra_body:
      reasoning_effort: max
    max_tokens: 131072
    role: batch
```

Do **not** carry over any `thinking: {type: disabled}` from a GLM-5.2 call site. Z.ai documents that this returns an error on `glm-5.3`.

### 4.3 omlx launchd plist

**No change needed.** omlx serves local MLX models. GLM-5.3 has no weights released and is a ~750B model besides, so it will never run under the ~59 GB ceiling. Leave the plist alone.

The same applies to Qwen3.8-Flash-Next. Nothing in this evaluation justifies touching omlx.

### 4.4 End-to-end verification

Run in order. Stop at the first failure.

```bash
# 1. Reachability and correct model echo
curl -s https://openrouter.ai/api/v1/chat/completions \
  -H "Authorization: Bearer $OPENROUTER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"z-ai/glm-5.3",
       "messages":[{"role":"user","content":"Reply with exactly: OK"}],
       "max_tokens":64}' | jq '{model, content: .choices[0].message.content}'

# 2. Is it reachable through the gateway we already run?
curl -s localhost:3100/v1/models | jq -r '.data[].id' | grep -i glm-5.3

# 3. Tool calling. Confirm a well-formed tool_call comes back, not prose.
curl -s https://openrouter.ai/api/v1/chat/completions \
  -H "Authorization: Bearer $OPENROUTER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"z-ai/glm-5.3",
       "messages":[{"role":"user","content":"What is the weather in Denver?"}],
       "tools":[{"type":"function","function":{"name":"get_weather",
         "parameters":{"type":"object","properties":{"city":{"type":"string"}},
         "required":["city"]}}}],
       "tool_choice":"auto"}' | jq '.choices[0].message.tool_calls'

# 4. Structured output. Must parse as JSON on 10/10 runs before trusting it.
for i in $(seq 1 10); do
  curl -s https://openrouter.ai/api/v1/chat/completions \
    -H "Authorization: Bearer $OPENROUTER_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{"model":"z-ai/glm-5.3",
         "response_format":{"type":"json_object"},
         "messages":[{"role":"user",
           "content":"Return JSON with keys verdict (approve|reject) and reason."}],
         "max_tokens":256}' \
  | jq -e '.choices[0].message.content | fromjson' > /dev/null \
  && echo "run $i ok" || echo "run $i FAILED"
done
```

Then, before it reviews anything real:

5. **Long-context retrieval.** Publish nothing on trust here. Plant a distinctive fact at 10%, 50% and 90% depth in a 200K-token document and confirm retrieval at each. The 1M context number is a capacity claim and I found no published retrieval-quality evidence for it.
6. **Token accounting.** Run five representative review tasks and record actual output tokens. Compare against the ~75K/task at `max` and ~50K/task at `high` that Z.ai reports. If our tasks come in materially higher, the cost model changes.
7. **Reviewer shadow run.** Point it at the last 10 merged tier 1 PRs as a non-blocking second reviewer. Compare its findings against what the human or incumbent reviewer caught. Adopt only if it surfaces something real, not just more words.
8. **Read the Z.ai data policy** at [https://docs.z.ai/legal-agreement/privacy-policy](https://docs.z.ai/legal-agreement/privacy-policy) before any sensitive work touches this route.

---

## 5. GLM-5.3-Flash

Verdict: **trial for high-volume batch, behind a structured-output bake-off. Do not wire it into a hard gate until that bake-off passes.**

The headline is that the economics are real and large. On Artificial Analysis's blended measure it costs $0.10 per million tokens against GLM-5.3's $0.90, for 57 Intelligence Index against 60. That is 95% of the capability at 11% of the price. If it holds structured output, it changes what triage costs us by more than an order of magnitude. The reason this is a trial and not an adopt-now is one specific structural problem, described in 5.5, that no amount of document reading can settle.

### 5.1 What it actually is

| Property | Value | Source |
|---|---|---|
| Release date | 2026-08-26. HF repo created 2026-08-25, last modified 2026-08-26 13:50 UTC | [HF API, direct model lookup](https://huggingface.co/api/models/zai-org/GLM-5.3-Flash), [OpenRouter](https://openrouter.ai/z-ai/glm-5.3-flash) |
| Total parameters | 320B | [Z.ai docs](https://docs.z.ai/guides/vlm/glm-5.3-flash.md), [HF model card](https://huggingface.co/zai-org/GLM-5.3-Flash/raw/main/README.md) |
| Active per token | 18B | same |
| Layers | 45 | Z.ai docs |
| Architecture | Hybrid sparse plus linear attention, with IndexPool and Manifold-Constrained Hyper-Connections (mHC) | Z.ai docs |
| HF `model_type` | `glm5_next`, architecture `Glm5NextForConditionalGeneration` | HF API |
| Context | 1M per Z.ai and OpenRouter. **400K per Artificial Analysis.** | see conflict note below |
| Max output | 131,072 | [OpenRouter](https://openrouter.ai/z-ai/glm-5.3-flash) |
| Modalities in | Text, images, video, files | [Z.ai docs, Capabilities](https://docs.z.ai/guides/vlm/glm-5.3-flash.md) |
| Modalities out | Text | same |
| Weights open | **Yes, and already published** | [zai-org/GLM-5.3-Flash](https://huggingface.co/zai-org/GLM-5.3-Flash) |
| License | **MIT** | HF card metadata, `license: mit` |
| Repo size | 62 safetensor shards, ~657 GB reported storage | HF API |

**Not a distillation of GLM-5.3.** This is the question that most needed checking and the answer is unambiguous. The model card states "GLM-5.3-Flash starts from a newly trained base model, with its architecture and training recipe redesigned around capability and efficiency," and Z.ai's writeup separately reports evaluation results for "the base model of GLM-5.3-Flash" against previous GLM base models. It is a separate pre-training line on a 30T-token multimodal corpus, not a compressed 5.3.

The architecture tags confirm it independently. GLM-5, 5.1 and 5.2 all carry `model_type: glm_moe_dsa` in their HF metadata. GLM-5.3-Flash carries `glm5_next`. Different family, not a variant. Sources: [HF zai-org listing](https://huggingface.co/api/models?author=zai-org), [HF API for GLM-5.3-Flash](https://huggingface.co/api/models/zai-org/GLM-5.3-Flash).

Relative to GLM-5.3 the efficiency claim is specific and checkable in principle: "Compared with GLM-5.3, it reduces attention computation and KV cache size by 3.01x and 4.44x, respectively." Source: [Z.ai docs](https://docs.z.ai/guides/vlm/glm-5.3-flash.md).

**The open-weights inversion is worth naming.** The cheap sibling shipped with MIT weights on day one. The flagship did not ship weights at all and is still classified proprietary. If open weights matter to us for any reason beyond self-hosting, Flash is the one that actually delivers them. It does not help our hardware: 320B parameters at roughly 657 GB of published tensors, and even a 4-bit quant would land near 160 GB against a ~59 GB ceiling. Local is out for the same reason as everything else in this document. Supported serving stacks are SGLang, vLLM, TokenSpeed and KTransformers, with no MLX path listed.

**Conflict to be aware of.** Artificial Analysis lists the context window at 400K, while Z.ai's own model page and OpenRouter both say 1M. Artificial Analysis also records "Image Input Support: No" and "Open Source (Weights): No" for this model, and both of those are demonstrably wrong against the vendor documentation and the live MIT-licensed HF repo. AA's metadata is stale for a model released the same day. Treat AA as authoritative for the evals it ran itself and not for model attributes. Sources: [AA comparison page](https://artificialanalysis.ai/models/comparisons/glm-5-3-flash-vs-glm-5-3), [Z.ai docs](https://docs.z.ai/guides/vlm/glm-5.3-flash.md), [HF repo](https://huggingface.co/zai-org/GLM-5.3-Flash).

### 5.2 Reasoning behavior and what it costs

Flash carries the **same constraint as GLM-5.3**, and this matters more here than it does there.

- `thinking.type` supports `enabled` only. Thinking cannot be disabled. Source: [Z.ai docs, Capabilities](https://docs.z.ai/guides/vlm/glm-5.3-flash.md), stated verbatim as "thinking cannot be disabled."
- Text parameters are "consistent with GLM-5.3," which means the same three effort levels `low`, `high`, `max`. Source: same page.
- Z.ai's recommended settings are `temperature: 1`, `top_p: 0.95`, `reasoning_effort: max`, plus `thinking.clear_thinking: false`.

So the default posture is deep reasoning on every call, including a call whose entire job is to emit one label.

**Quantifying the verbosity.** Artificial Analysis measured output token consumption across the Intelligence Index:

| Model | Output tokens for the index | Median for its price tier | Ratio to median |
|---|---|---|---|
| GLM-5.3 (max) | 170M | 72M | 2.4x |
| GLM-5.3-Flash | 150M | 64M | 2.3x |

Sources: [AA GLM-5.3](https://artificialanalysis.ai/models/glm-5-3), [AA GLM-5.3-Flash](https://artificialanalysis.ai/models/glm-5-3-flash) via search extract. Flash is not meaningfully less verbose than 5.3 in relative terms. It is roughly as talkative, just cheaper per word.

**This is why "cheap" needs arithmetic rather than assumption.** Run the numbers at the discounted OpenRouter rate of $0.075 in and $0.25 out, and at the list rate of $0.15 and $0.50, for a triage-shaped task of 3,000 input tokens per notice:

| Output tokens per notice | Cost per 1,000 notices (discounted) | Cost per 1,000 notices (list) |
|---|---|---|
| 300 (terse label, reasoning suppressed by prompt) | $0.30 | $0.60 |
| 800 (short reasoning trace plus label) | $0.43 | $0.85 |
| 3,000 (`low` effort behaving like real reasoning) | $0.98 | $1.95 |
| 8,000 (`max` effort on an ambiguous notice) | $2.23 | $4.45 |

The spread between the best and worst case is more than 7x, and which one we land in is decided entirely by how much unsuppressable reasoning the model emits on our actual prompts. That is measurable in an afternoon and is not knowable from documentation. Note also that these figures ignore cache reads at $0.015 per million discounted, which should absorb most of the shared rubric or taxonomy text in a triage prompt and pull input cost down substantially.

The discount is temporary. OpenRouter shows the current price as 50% off, list being $0.15 in and $0.50 out. Budget against list.

### 5.3 Benchmarks, and where each number comes from

**Independent, run by Artificial Analysis:**

| Metric | GLM-5.3-Flash | GLM-5.3 (max) |
|---|---|---|
| Intelligence Index v4.1.1 | **57** | 60 |
| Blended price per 1M tokens (7:2:1) | **$0.10** | $0.90 |
| Cost to run the full index | **$138.02** | $1,238.50 |
| Output tokens for the index | 150M | 170M |

Sources: [AA comparison](https://artificialanalysis.ai/models/comparisons/glm-5-3-flash-vs-glm-5-3), [AA GLM-5.3-Flash](https://artificialanalysis.ai/models/glm-5-3-flash).

A 57 puts it level with Gemini 3.1 Pro Preview and GPT-5.4 at xhigh effort, at roughly a twentieth of the blended price. The Index aggregates nine evals including Terminal-Bench v2.1 (agentic coding), τ³-Banking (agentic tool use) and AA-LCR (long context reasoning), all run by AA rather than submitted by the vendor. That is the strongest evidence in this document for any of the three models.

**Vendor-published, from [Z.ai's model page](https://docs.z.ai/guides/vlm/glm-5.3-flash.md):**

| Benchmark | GLM-5.2 | GLM-5.3-Flash | Note |
|---|---|---|---|
| DeepSWE v1.1 | 46.2 | 63.4 | mini-SWE-agent harness, 400K context, 6h timeout |
| AutomationBench | 26.2 | 48.8 | v1.0.6 with a null-handling fix applied |
| Z.ai Code Bench v1.0 (max effort) | lower at every level | 29.0 | vs Claude Opus 4.8 at 29.5. **In-house private benchmark.** |

For comparison, GLM-5.3 scored 66.9 on DeepSWE v1.1 and 34.5 on Z.ai Code Bench at max effort. So on the vendor's own numbers Flash lands a few points below the flagship on coding, consistent with the 57-versus-60 independent gap.

**Where the sourcing gets thin, stated plainly:**

- The **full benchmark table is published only as an image** on both the HF card and the blog. I could extract only the figures Z.ai stated in prose. The card's footnotes reference HLE with tools, NL2Repo, Terminal-Bench 2.1, Toolathlon Verified, GDPval-AA v2 and BabyVision, but the scores for those live in the image and I have not read them.
- One footnote is worth crediting: "GDPval-AA v2: Models are evaluated by Artificial Analysis." Z.ai marking which rows are third-party run is more disclosure than most cards give.
- **No LMArena entry.** Searched, none found for Flash.
- **No Aider polyglot score.** None found, same as for GLM-5.3.
- **No independent SWE-bench Verified run.** Vendor DeepSWE numbers only.
- **Long-context retrieval:** AA-LCR is inside the Index and AA runs it, so a long-context reasoning signal exists, but I could not extract the AA-LCR sub-score from the page, which renders it as a chart. The 1M capacity claim remains a capacity claim. Note also the unresolved 400K-versus-1M conflict in 5.1: if AA evaluated against a 400K window, any long-context conclusion is bounded there.
- **Structured-output reliability: no benchmark from anyone.** Not from Z.ai, not from AA. This is the gap that decides the verdict.

One more thing that cuts against the vendor framing. Z.ai says Flash "outperforms GLM-5.2 across benchmarks and real-world workloads at one-tenth the price, while approaching Claude Opus 4.8." The AA Index has Flash at 57 and GLM-5.2 at 53 by inference from AA's note that GLM-5.3 was "up 7 points from GLM-5.2." A four-point independent gap is real but smaller than "across benchmarks, often by a wide margin" implies.

### 5.4 Availability, identifiers and terms

| Path | Status | Detail |
|---|---|---|
| **OpenRouter** | **Available** | `z-ai/glm-5.3-flash`. $0.075 in / $0.25 out per million at a 50% discount, list $0.15 / $0.50. Cache read $0.015 discounted. One provider (Z.ai direct), no fallback routing. Measured 27 tok/s throughput, 3.28s P50 latency. Source: [OpenRouter](https://openrouter.ai/z-ai/glm-5.3-flash) |
| **Z.ai direct** | **Available** | Model code `glm-5.3-flash`. Same endpoints as GLM-5.3. Source: [Z.ai docs](https://docs.z.ai/guides/vlm/glm-5.3-flash.md) |
| **OpenCode Zen** | **Not available** | Verified live against the Zen models endpoint, which returns `glm-5.2`, `glm-5.1`, `glm-5` and no 5.3 of either kind. Source: [opencode.ai/zen/v1/models](https://opencode.ai/zen/v1/models) |
| **GLM Coding Plan** | **Available, with 3x the quota of GLM-5.3** | Points-based quota. Off-peak hours and all weekend consume 50% of standard points. Source: [Z.ai docs](https://docs.z.ai/guides/vlm/glm-5.3-flash.md) |
| **Self-host** | Possible in principle, not for us | MIT weights, SGLang / vLLM / TokenSpeed / KTransformers. 320B parameters, no MLX path, ~657 GB of tensors. |
| **FreeLLMAPI gateway :3100** | **Unverified** | No network path from this session. `curl -s localhost:3100/v1/models \| jq -r '.data[].id' \| grep -i glm-5.3` |

**Two pricing oddities.** First, Z.ai's own [pricing page](https://docs.z.ai/guides/overview/pricing.md) does not list GLM-5.3-Flash at all, in either the text or vision table, as of today. OpenRouter's numbers are the only concrete per-token price I could source. Second, the 3x Coding Plan quota is a meaningful lever if we ever run this through a subscription rather than metered API, since the Lite plan is $18/month.

**Throughput is the operational risk, not price.** OpenRouter measures Flash at 27 tok/s, which is *slower* than GLM-5.3 at 35 tok/s. That is backwards from what the name suggests and may just be day-one serving noise, but it matters for batch. At 800 output tokens per notice and 27 tok/s, a single serial stream clears roughly 100 notices an hour. Any real volume needs concurrency, and concurrency is exactly what I could not verify.

**Rate limits: unverified.** Z.ai's rate-limit documentation URL redirects to a login-gated console page, so I could not read the actual limits. Secondary reporting says the paid API now offers unlimited concurrency and that Coding Plan limits are dynamic and undisclosed. There is a public issue titled "[Critical] GLM-5.2 API is unusable due to severe rate limiting" against `zai-org/GLM-5`, so capacity has bitten users before. Source: [GitHub issue #83](https://github.com/zai-org/GLM-5/issues/83). Do not plan a nightly batch window around an unverified concurrency figure.

**Free or preview tier.** Z.ai confirms Flash was served anonymously as `ox-alpha` on OpenCode and OpenRouter before launch. OpenCode Zen still lists `x-preview-f-free` ("Ox Alpha Free") in its live model list, and Zen's privacy documentation states that model's provider "follows a zero-retention policy and does not use your data for model training." That would be a free, no-train path to this model. **But the preview period is over**, and there is no guarantee that endpoint still routes to GLM-5.3-Flash rather than the next stealth candidate. Treat as an opportunity to check, not a path to build on. Sources: [Z.ai docs](https://docs.z.ai/guides/vlm/glm-5.3-flash.md), [Zen models endpoint](https://opencode.ai/zen/v1/models), [Zen privacy](https://opencode.ai/docs/zen/).

**Data retention: same caution as GLM-5.3, and it applies with more force here.** I did not read Z.ai's privacy policy or DPA directly; the fetch returned a page shell. Everything I have is search-summarized. Batch triage means feeding the model a high volume of notices and RFP content, which is a larger and more continuous exposure than an occasional review call. **Do not clear GLM-5.3-Flash for the notrain pool.** Read [https://docs.z.ai/legal-agreement/privacy-policy](https://docs.z.ai/legal-agreement/privacy-policy) end to end first. The MIT license on the weights says nothing about what the hosted API does with inputs; those are separate documents governing separate things.

### 5.5 Fit against the jobs we actually run in volume

Scope caveat first: **I cannot see the pipeline.** Only `~/agent-workspace` is mounted, so I have not read the ingest code, the triage prompts, the current model assignments, or any volume figures. What follows reasons from the job shapes as described, with the token math left parametric so real numbers can be dropped in. Every "today" comparison is against what the standing rules imply, not against measured incumbents.

**Job 1: notice triage and filtering across the ingest stream.** This is the best fit on cost and the worst fit on reasoning behavior, simultaneously.

Cost strongly favors Flash. Against GLM-5.3 at $1.40 / $4.40 on the same task shape, Flash is roughly 19x cheaper on output and 19x on input, or about 25x cheaper end to end once the heavier reasoning trace that `max` effort produces on 5.3 is counted. Against local Qwen3.8 on omlx the marginal token cost is worse, since local is effectively free, but local is throughput-bound and confined to the overnight window by the standing rule. Flash can run during the day.

The problem is that triage is a classification job and this model cannot stop reasoning. Every notice gets a thinking pass whether it needs one or not. For a notice that is obviously out of scope, that is pure waste, and it is waste of unpredictable size. `reasoning_effort: low` reduces it but does not remove it, and Z.ai's own guidance for GLM-5.3 warns that lower effort "can also lead to insufficient analysis, more failures, and repeated retries," which on a filtering job means more false negatives. There is a real risk that the cheapest configuration is also the one that drops notices.

**Job 2: requirements extraction from RFP attachments.** This is the strongest genuine fit, and the reason is multimodality rather than price.

Flash is natively multimodal over images, video and files, and Z.ai documents visual understanding as a first-class capability rather than a bolt-on. RFP attachments are exactly the content that breaks text-only extraction: scanned PDFs, tables rendered as images, drawings, forms. A model that reads the page as a page has a structural advantage here that no amount of cheap text tokens provides. The 1M context, if it is really 1M rather than AA's 400K, covers whole attachment sets in one call.

Worth pairing with a cheaper specialist: Z.ai also serves **GLM-OCR at $0.03 per million in and out**, which is a fifth of Flash's list input price. For pure text-off-the-page work, OCR first and Flash for the reasoning over extracted text may beat Flash doing both. Source: [Z.ai pricing](https://docs.z.ai/guides/overview/pricing.md).

**Job 3: first-pass matching.** Fit is good and the risk is moderate. Matching is a ranking and judgment task where a short reasoning trace is arguably useful rather than waste, which inverts the triage problem. At 57 on the Index it is capable enough to make defensible calls. Cost per comparison is low enough that a wider candidate set becomes affordable, which is often worth more than a better model on a narrow set. The caution is verbosity: matching over a large candidate list multiplies output tokens quickly, and the 2.3x-above-median verbosity is a multiplier on the whole job.

**Job 4: any classification step with a hard gate.** **This is the job it fails on current evidence, and it fails on structured output rather than on intelligence.**

The specifics matter:

1. Z.ai's structured output is **JSON mode, not enforced schema**. The parameter is `response_format: {"type": "json_object"}`. There is no `json_schema` variant documented and no constrained-decoding guarantee. Source: [Z.ai structured output docs](https://docs.z.ai/guides/capabilities/struct-output.md).
2. Z.ai's own documentation treats parse failure as expected. Every worked example in that page wraps the call in `try/except` catching both `json.JSONDecodeError` and `jsonschema.ValidationError`, and the recommended practice is explicitly "Multi-layer validation: Schema validation plus business logic validation" with a "Fallback plan: Prepare simplified backup Schema."
3. More telling, one of Z.ai's own extraction examples reads the result as `json.loads(response.choices[0].message.content)["properties"]`, unwrapping a `properties` key. That is the shape of a JSON **Schema**, not an instance of one. The vendor's sample code is working around the model returning the schema back instead of data. That is a specific, sourced reliability smell.
4. The model page for GLM-5.3-Flash lists structured output as supported, but the structured output guide names supported models as "`glm-5`, `glm-4.7`, `glm-4.5`, `glm-4.6`, etc." and does not name any 5.3 variant. The two pages are not in agreement.
5. No party, vendor or independent, publishes a structured-output reliability figure for this model.

A gate that acts on the model's output without a human in the loop needs a known failure rate. We do not have one, the vendor's own docs imply it is not negligible, and forced reasoning adds a second failure mode where the thinking trace leaks into the content field. Until measured, a gate cannot trust it.

**Head to head summary.**

| | Local Qwen3.8 on omlx | GLM-5.3 hosted | GLM-5.3-Flash hosted |
|---|---|---|---|
| Marginal cost | ~zero | $1.40 / $4.40 per M | $0.075 / $0.25 per M discounted, $0.15 / $0.50 list |
| Cost per 1k notices (3K in, 800 out) | ~zero | ~$8 and up, more at `max` effort | **$0.43 discounted, $0.85 list** |
| Availability window | Overnight and batch only, per standing rule | Any time | Any time |
| Throughput | Bounded by one machine | 35 tok/s measured | 27 tok/s measured, concurrency unverified |
| Quality signal | No independent index score for our checkpoint | AA Index 60 | AA Index 57 |
| Multimodal | Text (our current checkpoint) | Text only | **Images, video, files** |
| Structured output | Known behavior in our pipeline | JSON mode, unmeasured | JSON mode, unmeasured, vendor docs imply retries needed |
| Gate-safe today | Whatever we have already validated | No | **No** |

**The honest headline.** The cost case is genuine and it is the largest single economic lever in this evaluation: on Artificial Analysis's own blended measure, near-flagship capability at a ninth of the price, and roughly an order of magnitude below GLM-5.3 on the triage-shaped tasks we would actually run. That is worth pursuing seriously.

It is not adopt-now, and the reason is narrow and specific: **the classification-with-a-hard-gate job fails, because reasoning cannot be disabled and JSON mode is not schema-enforced, and nobody has published a reliability number.** Both halves of that are measurable in a day. Run the bake-off in 5.6, and if strict JSON clears 99.5% with a validator and one retry, this moves to adopt for triage and the economics change materially.

### 5.6 The bake-off that decides it

Proposal only. Nothing here has been run and no config was touched.

Model identifiers:

| Path | Identifier |
|---|---|
| OpenRouter | `z-ai/glm-5.3-flash` |
| Z.ai direct | `glm-5.3-flash` |
| Cheaper OCR specialist for attachments | `glm-ocr` |

Run these against a sample of at least 300 real notices, and against whatever handles that job today:

1. **Strict JSON pass rate.** Same triage prompt, `response_format: {"type": "json_object"}`, at `reasoning_effort: low`. Validate every response against the real schema with a validator, not just `json.loads`. Record: parse failures, schema violations, and specifically whether a `properties` wrapper or a leaked thinking trace ever appears in the content field. **Target: 99.5% or better with one retry.** This single number decides the verdict.
2. **Token accounting per effort level.** Run the same 300 at `low` and at `high`. Record actual output tokens per notice at each. Drop the real figures into the table in 5.2. This converts the 7x cost spread into one number.
3. **Triage agreement.** Compare labels against the incumbent and against a human-labeled gold set. Measure false negatives specifically, since a dropped notice is the expensive error in a filtering job and low reasoning effort is where they would appear.
4. **Concurrency ceiling.** Ramp parallel requests until errors appear. Record the ceiling and the error class. This is the only way to get a rate-limit number given the docs are gated.
5. **Attachment extraction.** Take 20 RFP attachments that currently fail or degrade, including at least five scanned or image-heavy ones. Run Flash natively multimodal. Compare against the current path and against a GLM-OCR-then-Flash two-stage pipeline on both accuracy and cost.
6. **Long-context sanity.** Resolve the 400K versus 1M conflict empirically. Plant a distinctive fact at 90% depth in a 500K-token document and see whether it is retrieved or the request is rejected.
7. **Read the Z.ai data policy** before any of the above touches real notice content, and keep the model out of the notrain pool until that read is done.

Cost of the bake-off itself: at 300 notices across two effort levels, roughly 600 calls, well under a dollar at these prices. There is no economic reason not to run it.

---

## 6. Re-examination: does MoE sparsity change the memory answer?

Added 2026-08-26 after Mike challenged the skip verdict on Qwen3.8-Flash-Next and sent the quantized-checkpoint listing, then asked for the same treatment on GLM-5.3-Flash.

Short version: the challenge was worth making, and it moves the numbers, but it does not reach a verdict flip today. The interesting part is that the reason has changed. It is no longer arithmetic. It is that the runtime that would make this work exists as an unmerged pull request, validated on CUDA rather than Metal, and neither model's architecture is supported by it.

### 6.1 The MoE claim, stated correctly

**Mixture of experts reduces active compute, not resident weight memory.** In a standard implementation every expert must be resident, because the router picks a different subset for every token and there is no way to know in advance which. Qwen3.8-Flash-Next activates 6B of 180B parameters per token, but a conventional loader still holds all 180B. Sparsity buys you FLOPs, not bytes. That part of the intuition does not hold.

The question worth asking is the one behind it: do the experts have to be *resident*, or can cold ones live on SSD and be paged in on demand? That is where MoE sparsity genuinely does buy something on memory, and it is a real technique with a real implementation. Section 6.4 works it through.

First, the actual byte sizes, since the earlier 78 GB figure came from Unsloth's table alone and deserved checking.

### 6.2 Qwen3.8-Flash-Next: every quantized checkpoint, measured

All sizes below are summed from repository file listings via the Hugging Face API, not from parameter-count math and not from any publisher's table. Accessed 2026-08-26, roughly 16:00 UTC. Everything in this ecosystem is hours old and moving fast.

| Repo | Weight bytes | Bits/param | Status |
|---|---|---|---|
| [Qwen/Qwen3.8-Flash-Next](https://huggingface.co/Qwen/Qwen3.8-Flash-Next) | ~360 GB | 16 | Official BF16. API reports exactly 179,999,981,424 BF16 params. 2,551 downloads |
| [Qwen/Qwen3.8-Flash-Next-FP8](https://huggingface.co/Qwen/Qwen3.8-Flash-Next-FP8) | ~180 GB | 8 | Official FP8. 451 downloads |
| [Vontra/...-MLX-oQ6-MTP](https://huggingface.co/Vontra/Qwen3.8-Flash-Next-MLX-oQ6-MTP) | **158.08 GB** | ~7.0 | MLX 6-bit **with MTP head**, tagged `omlx`, `speculative-decoding`. Created 15:48 UTC |
| [RadixArk/...-NVFP4](https://huggingface.co/RadixArk/Qwen3.8-Flash-Next-NVFP4) | **135.24 GB** | ~6.0 | NVFP4 via ModelOpt. 263 downloads, the most-downloaded community quant |
| [Sawfwair/...-MLX-4bit](https://huggingface.co/Sawfwair/Qwen3.8-Flash-Next-MLX-4bit) | **104.76 GB** | ~4.66 | MLX 4-bit |
| [Sawfwair/...-MLX-Mixed-2bit](https://huggingface.co/Sawfwair/Qwen3.8-Flash-Next-MLX-Mixed-2bit) | **73.11 GB** | ~3.25 | Mixed precision, MLX |
| [unsloth/...-GGUF](https://huggingface.co/unsloth/Qwen3.8-Flash-Next-GGUF) `UD-IQ1_S` | **72.55 GB** | ~3.22 | Dynamic 1-bit, imatrix. 3 shards, complete. **Only quant uploaded so far.** 219 likes |
| [Vontra/...-MLX-oQ2](https://huggingface.co/Vontra/Qwen3.8-Flash-Next-MLX-oQ2) | **67.67 GB** | **3.008** | **Smallest complete artifact.** 14 of 14 shards present. MLX 2-bit, tagged `omlx`, `mlx-vlm` |
| [inferencerlabs/...-MLX-Q9](https://huggingface.co/inferencerlabs/Qwen3.8-Flash-Next-MLX-Q9) | 60.6 GB and climbing | n/a | **Incomplete.** Declares 16 shards, partial. Was 49.9 GB an hour earlier |
| [DevQuasar/Qwen.Qwen3.8-Flash-Next-GGUF](https://huggingface.co/DevQuasar/Qwen.Qwen3.8-Flash-Next-GGUF) | 0.90 GB | n/a | **Upload in progress** |
| [Vontra/...-MLX-8bit](https://huggingface.co/Vontra/Qwen3.8-Flash-Next-MLX-8bit), `-oQ8` | 0 | n/a | **Empty placeholder**, `.gitattributes` only |
| [txgsync/...-MXFP4-MLX](https://huggingface.co/txgsync/Qwen3.8-Flash-Next-MXFP4-MLX) | 0 | n/a | **Empty placeholder** |
| [Baekpica/...-Mixed-Quant-GGUF](https://huggingface.co/Baekpica/Qwen3.8-Flash-Next-Mixed-Quant-GGUF) | 0 | n/a | **Empty placeholder** |
| [vcruz305/...-GGUF](https://huggingface.co/vcruz305/Qwen3.8-Flash-Next-GGUF), `-NVFP4` | 0 | n/a | **Empty placeholder** |
| [aj9o9](https://huggingface.co/aj9o9/GLM-5.3-Flash-GGUF)-style shells, `windowsxp811203/*` (4 repos) | 0 | n/a | **Self-labelled `placeholder` in their own tags** |
| `FlagRelease/*-FlagOS` (8 repos) | BF16/FP8 | 16 / 8 | Vendor-silicon repackages, not size reductions |

**Every one of these repos shows 0 downloads except the official Qwen repos and RadixArk.** Nobody has run any of the MLX or GGUF conversions. Treat all of them as untested.

**Correction to the earlier report.** I previously reported the floor as 78 GB on Unsloth's authority. The real floor today is **67.67 GB** of weights, Vontra's MLX oQ2, at 3.008 bits per parameter. Unsloth's 78 GB was a total-system figure including runtime overhead against their own 72.55 GB artifact, so the two are consistent, but the tighter number is the one to argue against.

**Against the ceiling:** 67.67 GB versus roughly 59 GB. Over by **8.7 GB**, or 4.0 GiB if you measure both in GiB (63.03 GiB versus 59 GiB). That is a much narrower miss than the earlier writeup implied, and it is before KV cache, activations, or the vision tower. It still does not fit.

**Why it will not quantize much lower, structurally.** Pulled from [the model's config.json](https://huggingface.co/inferencerlabs/Qwen3.8-Flash-Next-MLX-Q9/raw/main/config.json): `num_experts: 512`, `num_experts_per_tok: 10`, `moe_intermediate_size: 640`, `hidden_size: 2560`, `num_hidden_layers: 48`, and `ngram_vocab_size_base: 20000000` with `ple_embed_dim: 2560`.

That gives a clean parameter budget:

| Component | Params | Share | Per-token access pattern |
|---|---|---|---|
| Routed experts (512 × 48 layers × 3 × 2560 × 640) | 120.8B | 67% | 10 of 512 per layer, router-selected |
| N-gram embedding (20M entries × 2560) | 51.2B | 28% | **A handful of index lookups per token** |
| Attention, embeddings, vision tower, MTP, norms | ~8B | 5% | Always |

The n-gram table is 28% of the model and it is a lookup table. That is why the smallest quant is unusually large: 51.2B parameters of embedding cannot be squeezed the way expert matrices can without wrecking quality. It is also, as it happens, the single most streamable component in the model, and Qwen says so directly on the card: the table "can be asynchronously offloaded to host memory." Note "host memory." That design targets a discrete-GPU box where host RAM is a separate tier. On Apple unified memory there is no separate host tier to offload into. The only tier below unified memory is the SSD.

### 6.3 GLM-5.3-Flash: every quantized checkpoint, measured

Same method, same access date. This one is starker.

| Repo | Weight bytes | Status |
|---|---|---|
| [zai-org/GLM-5.3-Flash](https://huggingface.co/zai-org/GLM-5.3-Flash) | **656.69 GB** | Official. 62 shards |
| [zai-org/GLM-5.3-Flash-BF16](https://huggingface.co/zai-org/GLM-5.3-Flash-BF16) | **642.67 GB** | Official BF16 |
| [SinterForge/GLM-5.3-Flash](https://huggingface.co/SinterForge/GLM-5.3-Flash) | 656.69 GB | Byte-identical mirror of the official repo, not a quant |
| [ArchiveStudio/GLM-5.3-Flash](https://huggingface.co/ArchiveStudio/GLM-5.3-Flash) | 656.69 GB | Byte-identical mirror, not a quant |
| [LibertAIDAI/GLM-5.3-Flash-NVFP4](https://huggingface.co/LibertAIDAI/GLM-5.3-Flash-NVFP4) | **194.69 GB** | **Smallest real artifact in existence.** 4-bit NVFP4 |
| [unsloth/GLM-5.3-Flash-GGUF](https://huggingface.co/unsloth/GLM-5.3-Flash-GGUF) | **0** | `.gitattributes` and `README.md` only. No weight files |
| [AtomicChat/GLM-5.3-Flash-GGUF](https://huggingface.co/AtomicChat/GLM-5.3-Flash-GGUF) | **0** | README plus four PNGs including a `benchmark.png`. No GGUF files at all |
| [aj9o9/GLM-5.3-Flash-GGUF](https://huggingface.co/aj9o9/GLM-5.3-Flash-GGUF) | **0** | Empty |
| [vcruz305/GLM-5.3-Flash-GGUF](https://huggingface.co/vcruz305/GLM-5.3-Flash-GGUF), `-NVFP4` | **0** | Empty |

**There is no MLX conversion of GLM-5.3-Flash. Not one.** A Hugging Face API search for `GLM-5.3-Flash-MLX` returns an empty array. Compare Qwen, which has nine MLX repos within eighteen hours of release. Nobody is converting this for Apple Silicon, which is a signal in itself about who the model is aimed at.

**The smallest thing that exists is 194.69 GB.** That is 3.3x the ceiling. Every download counter across all of these reads 0.

The architecture explains why nobody has produced a small one, from [the config](https://huggingface.co/zai-org/GLM-5.3-Flash/raw/main/config.json): `n_routed_experts: 288`, `num_experts_per_tok: 8`, `n_shared_experts: 1`, `moe_intermediate_size: 2048`, `hidden_size: 4096`, `num_hidden_layers: 45`, `first_k_dense_replace: 3`.

| Component | Params | Share |
|---|---|---|
| Routed experts (288 × 42 MoE layers × 3 × 4096 × 2048) | ~304B | ~95% |
| Shared experts, 3 dense layers, MLA attention, embeddings, MTP | ~16B | ~5% |

GLM-5.3-Flash is 95% expert weights. A 2-bit quant would be roughly 84 GB, a 1.5-bit roughly 63 GB. Even a hypothetical aggressive dynamic quant lands above the ceiling, and 1.5 bits on a coding model is not a serious proposal. **No arithmetic gets this model under 59 GB resident at a quality worth having.**

Also worth recording since it bears on speculative decoding: the config has `num_nextn_predict_layers: 1`, so GLM-5.3-Flash ships an MTP head, same as Qwen.

### 6.4 Streaming experts from SSD, evaluated properly

This is the part of Mike's argument that has real substance, and there is now a concrete implementation to point at rather than speculation.

**The technique exists and it is not naive mmap.** [llama.cpp PR #25294, "llama : stream MoE routed experts from disk"](https://github.com/ggml-org/llama.cpp/pull/25294), opened 2026-07-04 by freedomljc, implements exactly this. The design is worth reading because it confirms plain mmap is the wrong tool:

- Routed expert weights are never materialized. Each streamed layer keeps a small device-side cache of expert slabs.
- A CPU id-remap op runs after the router top-k and maps expert ids to cache slots. Misses are demand-loaded from the GGUF by an async I/O worker pool.
- Eviction is decaying route hotness with an LRU tiebreak.
- **Enabling streaming auto-disables mmap, with a warning, because mmap prefetch would page the whole model into RAM and defeat streaming.** Mike's instinct to reach for mmap is the right family of idea and the wrong mechanism.
- Output is bit-exact against a non-streamed run.
- CLI: `--moe-stream`, `--moe-stream-cache <N|NGiB>`, `--moe-stream-io-threads N`, `--moe-stream-direct` for O_DIRECT.

**The measured numbers are the important part, and they are sobering.** The PR publishes a benchmark on a GB10 Grace-Blackwell with 128 GB unified memory, running **GLM-5.2-UD-Q2_K_XL**, a ~254 GB file, ~754B params, 256 experts, 512-token generation:

| Expert cache | Prefill | Decode | Cache hit rate |
|---|---|---|---|
| 64 slots (~56 GB) | ~1.57 tok/s | ~1.97 tok/s | 74% |
| 90 slots (~79 GB) | ~1.60 tok/s | ~2.33 tok/s | 80% |

Latency form: prefill 625 to 637 ms/token, decode 430 to 507 ms/token.

That is roughly **2 tokens per second**, on a machine with more unified memory than Mike's, at a cache budget of ~56 GB which is almost exactly our ceiling. Note also that the 74% hit rate at a cache holding only 22% of the file confirms real routing skew, which is the good news buried in these numbers. The bad news is that even at 80% hit rate the remaining 20% of misses sit on the critical path, one stall per layer per token, and I/O cannot be hidden because the router result is not known until the router runs.

**Scaling the anchor to our two models.** Both are much smaller than the GLM-5.2 in that benchmark, so both should do better. Expert bytes touched per token, which is what drives the I/O:

| Model | Active routed-expert params/token | At the smallest real quant | Bytes/token | Relative to the benchmark |
|---|---|---|---|---|
| GLM-5.2 (the benchmark) | ~35B est. | Q2_K_XL | ~8.8 GB | 1.0x baseline |
| **Qwen3.8-Flash-Next** | 2.60B (11 experts × 48 layers × 4.92M) | oQ2 at 3.0 bits | **~0.97 GB** | **~9x less** |
| **GLM-5.3-Flash** | 9.51B (9 experts × 42 layers × 25.2M) | hypothetical 2-bit | **~2.38 GB** | ~3.7x less |

So Mike's specific point about GLM-5.3-Flash is correct: **18B active out of 320B is a much worse sparsity ratio for streaming than Qwen's 6B of 180B, and it costs roughly 2.5x more paging per token.** Qwen is the better streaming candidate of the two by a wide margin, which is the opposite of the conclusion the hosted analysis reached.

Working-set coverage is the other half, and it is unfavourable for both. Probability an expert is untouched after N tokens is (1 - k/E)^N:

| Tokens generated | Qwen (10 of 512) | GLM-5.3-Flash (8 of 288) |
|---|---|---|
| 64 | 72% of experts touched | 84% |
| 128 | 92% | 97% |
| 256 | 99.4% | 99.9% |

Within a couple hundred tokens the working set is the entire expert table for both. Caching helps only through routing skew, not through a genuinely small working set. GLM saturates faster because it picks a larger fraction (2.78% versus 1.95% per layer).

**Does anything support this today, on our hardware?**

| Question | Answer |
|---|---|
| Is PR #25294 merged? | **No. Open, awaiting review from two code owners.** The bot flagged it as a large PR needing prior discussion |
| Was it validated on Metal at scale? | **No.** The PR states validation on "OLMoE Q4_K_M (fits in RAM; CPU + Metal) and GLM-5.2 (>>RAM; CUDA)". The over-RAM case was CUDA only |
| Does llama.cpp support `qwen4_exp`? | **Not in mainline.** Unsloth's own page says llama.cpp support is "Coming very soon!" and requires "our specific PR" |
| Does llama.cpp support `glm5_next`? | Not established. No GGUF of GLM-5.3-Flash exists anywhere, which is strong circumstantial evidence that conversion does not yet work |
| Does mlx-lm or omlx do expert streaming? | **No evidence of any such feature.** MLX materialises arrays into Metal buffers before kernel launch; there is no demand-paging path into GPU-accessible memory mid-kernel. The `omlx`-tagged Vontra repos are ordinary quants, not streaming artifacts |
| Mac-specific hazards? | A llama.cpp issue titled ["Managed SSD offloading for MoE to prevent macOS kernel panics" (#19825)](https://github.com/ggml-org/llama.cpp/issues/19825) exists. I did not read it in full, but the title alone is a reason for caution |

One structural caution from the PR's own limitations section: **single-context only.** Concurrent decoding of multiple contexts from the same streamed model shares one cache and can corrupt output. `--parallel N` within one context is safe. For batch triage that wants concurrency, this matters.

**Honest throughput estimate if it all landed.** Anchoring on the measured ~2 tok/s and adjusting for ~9x less expert I/O per token and a far better resident fraction (59 GB against a 67.67 GB file is 87% of the model, versus 22% in the benchmark), Qwen3.8-Flash-Next streamed might reach somewhere in the range of 5 to 15 tok/s decode. **That is an extrapolation from one measurement on different hardware and a different architecture, and I would not plan against it.** The honest version is: the only measured number for this technique on a comparable machine is 2 tok/s, and the first real measurement on our setup could land anywhere between that and the optimistic end.

For GLM-5.3-Flash the same extrapolation gives roughly 3 to 6 tok/s, and there is no artifact to run it on regardless.

### 6.5 The xgrammar angle, which is the genuinely important idea here

Mike's strongest point in this exchange is not about memory. It is this: hosted GLM-5.3-Flash offers JSON mode with no schema enforcement, which is what failed the gate in section 5.5. Grammar-constrained decoding masks invalid tokens at each step, so schema-valid output is guaranteed by construction. [XGrammar](https://github.com/mlc-ai/xgrammar) "leverages constrained decoding to ensure 100% structural correctness of the output," and reports up to 3.5x speedup on JSON schema workloads over prior approaches. If omlx already has xgrammar installed, then a local model plus grammar constraints solves the exact failure that blocked the gate.

That is correct, and it is the right thing to chase. Three qualifications, in order of importance:

1. **It does not require these models.** Grammar constraints are a property of the decoding loop, not the checkpoint. If the goal is guaranteed schema-valid triage output, that is achievable today with whatever already runs under 59 GB on omlx. Waiting for Qwen3.8-Flash-Next or GLM-5.3-Flash to fit is not on the critical path for solving the gate problem. This is the actionable finding: **run the xgrammar experiment now, on a model that already fits, and decouple it from these two releases entirely.**
2. **Grammar constraints guarantee syntax, not semantics.** A schema-valid wrong label still fails triage. Constrained decoding moves the failure mode from "the gate crashes" to "the gate acts on a confidently wrong value," which is better but is not the same as trustworthy. The agreement and false-negative measurements in the section 5.6 bake-off still have to be run.
3. **There is a measured quality cost.** A 2026 study, ["Constraint Tax in Open-Weight LLMs: An Empirical Study of Tool Calling Suppression Under Structured Output Constraints"](https://arxiv.org/pdf/2606.25605), documents capability suppression under structured output constraints in open-weight models. Budget for a quality delta rather than assuming constraints are free.

Local also solves two things the hosted route cannot, both of which Mike named: no per-token cost, and no data-retention exposure, which retires the notrain caution entirely. Those are real and they are the reason to keep pushing on this. They just are not reachable through either of these two checkpoints this week.

### 6.6 Re-verdict

**Qwen3.8-Flash-Next: still skip, but the reason has changed and the watch list is concrete.**

The number that kills it is no longer 78 GB. It is **67.67 GB of weights against a ~59 GB ceiling, an 8.7 GB miss**, on Vontra's oQ2 at 3.008 bits per parameter, with KV cache and activations still to come out of what remains. Nothing smaller exists that is complete. At 3.0 bits per parameter the quality caveat is already severe for a coding and agentic workload, so even closing the last 8.7 GB by pushing to ~2.6 bits would be buying a checkpoint I would not trust for the jobs in section 5.5.

Streaming is a real path and not a fantasy, but the honest status is: unmerged PR, CUDA-validated rather than Metal-validated at scale, architecture unsupported, single-context only, with a Mac kernel-panic issue open against the general technique, and the one published measurement on comparable hardware showing 2 tok/s. Mike's rule says local models take overnight and batch work where slow is acceptable. 2 tok/s with an unmerged runtime is past where "slow is acceptable" stops being the operative question and "does it run at all" takes over.

Flip conditions, in order of likelihood: PR #25294 merges and gets Metal validation above RAM size; llama.cpp lands `qwen4_exp`; someone publishes a complete sub-60 GB quant with a perplexity number and a non-zero download count. Any two of those and this is worth an evening.

**GLM-5.3-Flash: skip for local, unambiguously. The hosted trial verdict in section 5 stands unchanged.**

The specific number that kills it: **194.69 GB, the smallest artifact that exists anywhere**, 3.3x the ceiling. Behind that, the structural number: 95% of its 320B parameters are expert weights, so a 2-bit quant is ~84 GB and you would need ~1.5 bits to reach 59 GB. There is no MLX conversion at all, no GGUF at all, both GGUF repos that claim to exist are empty shells, and every download counter reads 0. Its 18B active parameters mean ~2.5x more paging per token than Qwen, so it is also the worse streaming candidate of the two.

This is the answer to the most important version of Mike's question. Local GLM-5.3-Flash would indeed retire the per-token cost and the notrain exposure in one move, and that would be worth a lot. It is not available at any quality on this hardware, and nothing in the current trajectory suggests it will be.

**What should actually happen next:** run the xgrammar-plus-local experiment against a model that already fits, this week, and treat it as independent of both releases. If grammar-constrained decoding on an incumbent local model produces schema-valid triage output at acceptable agreement rates, that solves the gate problem without waiting for either of these, and it does so at zero marginal cost with no data exposure. That is the headline, and it does not depend on Qwen or GLM at all.

---

## 7. What could not be verified

Recorded honestly rather than glossed.

| Item | Why it matters | Status |
|---|---|---|
| Which Qwen3.8 checkpoint we currently serve | Drop-in question cannot be fully answered without it | `~/.hermes` not accessible from this session |
| Whether `mlx-lm` supports `qwen4_exp` | Would decide MLX viability if memory were not already decisive | GitHub code search returned nothing; Qwen's README omits MLX |
| Whether either model is on the `:3100` gateway | Determines whether new credentials are needed at all | No network path to localhost from here |
| Z.ai training-on-data clause, read directly | Gates the notrain pool | Only search-summarized, policy text not retrieved |
| Z.ai published rate limits | Affects batch run planning | No official table located |
| Artificial Analysis per-eval sub-scores for GLM-5.3 (Terminal-Bench v2.1, τ³-Banking, AA-LCR) | These three are closest to our workload | Rendered as charts, not extractable as text |
| Any independent eval of Qwen3.8-Flash-Next | The entire benchmark case is vendor-only | None exists; model is hours old |
| Aider polyglot for GLM-5.3 | Requested explicitly | No score found from any source |
| Qwen Cloud pricing for Qwen3.8-Flash | Would price the hosted fallback | Not published in any source located |
| GLM-5.3 exact parameter count | Minor | AA says 753B, press says 743B/744B, Z.ai publishes none |
| `coding-glm-5.3-free` endpoint and its limits | Would be a genuinely free path | Secondary sources only, not in Z.ai docs |
| Whether Zen's `Ox Alpha Free` still routes to GLM-5.3-Flash | Would be a free no-train path for batch | Z.ai confirms ox-alpha *was* Flash pre-launch; whether `x-preview-f-free` still points there today is unknown |
| GLM-5.3-Flash structured-output reliability | **Decides the triage verdict** | No figure published by anyone; vendor docs imply retries are expected |
| GLM-5.3-Flash context window, 400K or 1M | Bounds any long-context claim | AA says 400K, Z.ai and OpenRouter say 1M, unresolved |
| GLM-5.3-Flash full benchmark table | Most rows are only in an image | Published as a PNG on the HF card and blog; only prose-stated figures extracted |
| GLM-5.3-Flash AA sub-scores | Same reason as for GLM-5.3 | Model page fetch returned empty on two attempts; comparison page rendered but charts are not text |
| Our actual pipeline volumes, prompts and incumbent models | The head-to-head in 5.5 is parametric because of this | Only `~/agent-workspace` is mounted; pipeline not readable from here |
| GLM-5.3-Flash sustained concurrency | Decides whether batch throughput works | Z.ai rate-limit docs redirect to a login-gated page |
| Per-tensor bit allocation inside `UD-IQ1_S` and `oQ2` | Would show how much of the 67 GB is the n-gram table versus experts, and whether a split-residency scheme is even possible | Requires reading GGUF/safetensors headers. Cheap to do: the GGUF header sits at the start of the file, so a ranged read of the first few MB answers it without downloading 72 GB |
| Whether llama.cpp mainline supports `qwen4_exp` or `glm5_next` | Gates any GGUF or streaming path | Unsloth says llama.cpp support is "coming very soon" via their PR; no GLM-5.3-Flash GGUF exists anywhere |
| Metal behaviour of PR #25294 above RAM size | The published 2 tok/s figure is CUDA | PR states Metal was validated only on a model that fits in RAM |
| Contents of llama.cpp issue #19825 on macOS kernel panics | Safety of the whole streaming approach on this hardware | Title read from search results only, issue body not retrieved |
| Whether omlx's xgrammar integration covers JSON Schema and works with the incumbent local model | **Decides the actionable recommendation in 6.5** | omlx internals not readable from this session |
| Real quality of `oQ2` at 3.008 bits | Whether closing the last 8.7 GB would even be worth it | No perplexity, no eval, 0 downloads, uploaded hours ago |

Two inconsistencies worth naming:

1. Unsloth's hardware table lists BF16 at 56 GB, which is impossible for a 180B-parameter model and is smaller than every quantized entry in the same row. That cell is almost certainly an error in their table. The quantized figures are consistent with the parameter count and are the ones this evaluation relies on.
2. Artificial Analysis records GLM-5.3-Flash as having no image input and no open weights. Both are wrong: Z.ai documents native image, video and file input, and the MIT-licensed weights are live on Hugging Face. AA's evals are trustworthy; its model metadata was stale for a same-day release. This is a useful reminder that aggregators lag on launch day and primary sources have to be checked directly.

---

## Sources

Accessed 2026-08-26.

- [Qwen3.8-Flash-Next-FP8 model card, Hugging Face](https://huggingface.co/Qwen/Qwen3.8-Flash-Next-FP8)
- [QwenLM/Qwen3.8-Flash-Next, GitHub](https://github.com/QwenLM/Qwen3.8-Flash-Next/)
- [Qwen Community License 1.0](https://huggingface.co/Qwen/Qwen3.8-Flash-Next/raw/main/LICENSE)
- [Qwen3.8-Flash-Next collection, Hugging Face](https://huggingface.co/collections/Qwen/qwen38-flash-next)
- [Hugging Face models API, Qwen3.8-Flash-Next search](https://huggingface.co/api/models?search=Qwen3.8-Flash-Next&limit=100)
- [Hugging Face API, inferencerlabs MLX-Q9 repo](https://huggingface.co/api/models/inferencerlabs/Qwen3.8-Flash-Next-MLX-Q9?blobs=true)
- [Hugging Face API, Vontra MLX-8bit repo](https://huggingface.co/api/models/Vontra/Qwen3.8-Flash-Next-MLX-8bit?blobs=true)
- [Unsloth: Qwen3.8-Flash-Next, How to Run Locally](https://unsloth.ai/docs/models/qwen3.8-next.md)
- [MTPLX, native MTP speculative decoding on MLX](https://github.com/youssofal/MTPLX)
- [Z.ai developer docs, GLM-5.3](https://docs.z.ai/guides/llm/glm-5.3)
- [Z.ai developer docs, GLM-5.3-Flash](https://docs.z.ai/guides/vlm/glm-5.3-flash.md)
- [Z.ai pricing page](https://docs.z.ai/guides/overview/pricing.md)
- [Z.ai structured output guide](https://docs.z.ai/guides/capabilities/struct-output.md)
- [Z.ai documentation index](https://docs.z.ai/llms.txt)
- [zai-org/GLM-5.3-Flash on Hugging Face](https://huggingface.co/zai-org/GLM-5.3-Flash)
- [Quantized models for Qwen/Qwen3.8-Flash-Next](https://huggingface.co/models?other=base_model:quantized:Qwen/Qwen3.8-Flash-Next)
- [Quantized models for zai-org/GLM-5.3-Flash](https://huggingface.co/models?other=base_model:quantized:zai-org/GLM-5.3-Flash)
- [Qwen3.8-Flash-Next config.json (via inferencerlabs MLX mirror)](https://huggingface.co/inferencerlabs/Qwen3.8-Flash-Next-MLX-Q9/raw/main/config.json)
- [GLM-5.3-Flash config.json](https://huggingface.co/zai-org/GLM-5.3-Flash/raw/main/config.json)
- [Vontra/Qwen3.8-Flash-Next-MLX-oQ2 file listing](https://huggingface.co/api/models/Vontra/Qwen3.8-Flash-Next-MLX-oQ2/tree/main?recursive=true)
- [unsloth/Qwen3.8-Flash-Next-GGUF file listing](https://huggingface.co/api/models/unsloth/Qwen3.8-Flash-Next-GGUF/tree/main?recursive=true)
- [llama.cpp PR #25294, stream MoE routed experts from disk](https://github.com/ggml-org/llama.cpp/pull/25294)
- [llama.cpp issue #19825, managed SSD offloading for MoE to prevent macOS kernel panics](https://github.com/ggml-org/llama.cpp/issues/19825)
- [XGrammar](https://github.com/mlc-ai/xgrammar)
- [Constraint Tax in Open-Weight LLMs (arXiv 2606.25605)](https://arxiv.org/pdf/2606.25605)
- [zai-org/GLM-5.3-Flash model card README](https://huggingface.co/zai-org/GLM-5.3-Flash/raw/main/README.md)
- [Hugging Face API record, zai-org/GLM-5.3-Flash](https://huggingface.co/api/models/zai-org/GLM-5.3-Flash)
- [Artificial Analysis: GLM-5.3-Flash](https://artificialanalysis.ai/models/glm-5-3-flash)
- [Artificial Analysis: GLM-5.3-Flash vs GLM-5.3 comparison](https://artificialanalysis.ai/models/comparisons/glm-5-3-flash-vs-glm-5-3)
- [OpenCode Zen live model list](https://opencode.ai/zen/v1/models)
- [Z.ai privacy policy](https://docs.z.ai/legal-agreement/privacy-policy)
- [The Decoder: Zhipu AI releases GLM-5.3](https://the-decoder.com/zhipu-ai-releases-glm-5-3-claims-its-the-strongest-open-weights-coding-model/)
- [Artificial Analysis: GLM-5.3 (max)](https://artificialanalysis.ai/models/glm-5-3)
- [Artificial Analysis Intelligence Index v4.1.1 methodology](https://artificialanalysis.ai/evaluations/artificial-analysis-intelligence-index)
- [OpenRouter: z-ai/glm-5.3](https://openrouter.ai/z-ai/glm-5.3)
- [OpenRouter: z-ai/glm-5.3-flash](https://openrouter.ai/z-ai/glm-5.3-flash)
- [OpenRouter: Qwen models](https://openrouter.ai/qwen)
- [OpenRouter zero data retention docs](https://openrouter.ai/docs/guides/features/zdr)
- [OpenCode Zen docs, model list, pricing and privacy](https://opencode.ai/docs/zen/)
- [Hugging Face API, zai-org organization](https://huggingface.co/api/models?author=zai-org&sort=createdAt&direction=-1&limit=15)
- [zai-org/GLM-5 issue #83, GLM-5.2 rate limiting](https://github.com/zai-org/GLM-5/issues/83)
