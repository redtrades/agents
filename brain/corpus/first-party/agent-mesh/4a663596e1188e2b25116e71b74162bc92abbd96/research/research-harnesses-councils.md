# Best agent harnesses 2026 + how practitioners run multi-harness LLM councils

**Date:** 2026-08-26 · **Scope:** harness landscape, council patterns, inter-agent comms, recommended topology for Mike's macOS solo-operator diagnostic swarm (Claude Code Max, opencode, pi, Hermes/omlx :8300, FreeLLMAPI :3100, Buzz, gbrain/pglite).
**Method:** live GitHub-API activity checks (`pushed_at` read 2026-08-26), vendor docs, primary research papers. Repo ownership changed for three tools since common knowledge formed — verified below.

---

## 1. Harness landscape 2026

### Table

| Harness | What it is | Provider flexibility (omlx/FreeLLMAPI OpenAI-compatible?) | Subagents / teams | Hooks / extensibility | Cost posture | Activity (verified 2026-08-26) |
|---|---|---|---|---|---|---|
| **Claude Code** (anthropics/claude-code) | Terminal agentic coding tool; de-facto reference harness [S1] | Anthropic-native only (OAuth/API key, Bedrock, Vertex); custom endpoints must speak *Anthropic* wire format (`ANTHROPIC_BASE_URL`); OpenAI-compatible upstreams need a router shim (claude-code-router/LiteLLM class) [S2] | Yes: markdown-defined subagents, agent teams [S3] | Yes: PreToolUse/PostToolUse/etc. hooks, skills [S4] | Flat Max subscription; watch concurrent-session OAuth contention (observed on this machine, MASTER-GUIDE §4) | Pushed 2026-08-25; 143k★ |
| **opencode** (**anomalyco/opencode**, ex-sst) | Open-source terminal coding agent, MIT, client/server architecture [S5] | **Best-in-class**: models.dev catalog + any OpenAI-compatible endpoint via `@ai-sdk/openai-compatible` + `baseURL` — direct config for omlx :8300 / FreeLLMAPI :3100 [S6] | Yes: agents/subagents spawn isolated child sessions, @mention-invocable [S7] | Plugins, custom commands, Claude-Code-hook compat layer via plugins [S8] | Free OSS; bring your own subscriptions/providers | Pushed 2026-08-26; 201k★ |
| **pi** (**earendil-works/pi**, ex-badlogic/pi-mono; Mario Zechner) | Minimal harness: unified LLM API, agent loop, TUI, coding-agent CLI. Deliberately skips MCP, subagents, plan mode, background bash [S9] | 15+ providers incl. Ollama/OpenRouter + custom entries in `models.json` → hits any OpenAI-compatible endpoint [S10] | None built in — you compose `pi -p` / RPC calls yourself (that's the design) [S9] | TypeScript extensions, skills, prompt templates, packages; 4 modes: TUI / print-JSON / RPC-over-stdio / SDK [S10] | Free OSS; BYO keys/local models | Pushed 2026-08-26; 97k★; badlogic still committing |
| **oh-my-opencode** (code-yeongyu; now trending toward "oh-my-openagent") | Community plugin layer over opencode: async subagents, specialist agents (oracle/librarian/explore/Sisyphus), LSP/AST tools, runs Claude Code hooks [S11] | Inherits opencode's; per-agent model overrides incl. local models [S11] | Yes — its main pitch | Plugin + hooks compat layer | Free | Active through 2026; multiple mirrors, canonical repo code-yeongyu/* |
| **Codex CLI** (openai/codex) | Rust terminal coding agent, Apache-2.0 [S12] | Any OpenAI-compatible endpoint via `[model_providers.<id>]` `base_url` + `wire_api="chat"`; built-in ollama/lmstudio, `--oss` mode. Full-featured path prefers Responses API [S13] | Multi-agent fan-out patterns exist; TOML-driven [S14] | config.toml profiles, hooks, MCP servers [S13] | ChatGPT sub or API usage | Pushed 2026-08-26; 118k★ |
| **Gemini CLI** (google-gemini/gemini-cli) | Google's terminal agent, TypeScript [S15] | **Google-first.** `GOOGLE_GEMINI_BASE_URL` exists but was ignored in some auth states until PR #25357 (merged Apr 2026); ACP mode still forces Google auth (feature request closed not-planned) [S16][S17]. No OpenAI-compatible provider support | Subagents/extensions ecosystem | Extensions + hooks (MCP client/server) | Generous free tier w/ Google account | Pushed 2026-08-26; 107k★ |
| **Crush** (charmbracelet) | Go TUI coding agent ("aider-class" successor energy) [S18] | Multi-provider via catwalk catalog incl. OpenAI-compatible/local (Ollama-class) [S18] | No first-class subagent teams | LSP, MCP, sessions | Free OSS, BYO keys | Pushed 2026-08-26; 28k★ |
| **Aider** (Aider-AI/aider) | Python pair-programming CLI, git-native diffs [S19] | LiteLLM-based → any OpenAI-compatible endpoint [S19] | None | Weakest extensibility of the set | Free OSS | **Stalled: last push 2026-05-22** (~3 months quiet) — do not build new dependency on it |
| **Goose** (**aaif-goose/goose**, ex-block/goose) | Rust extensible agent; now under Agentic AI Foundation governance (Block is an AAIF founding member) [S20] | Multiple providers incl. local OpenAI-compatible; MCP extensions | Recipe/subrecipe automation; ACP support | MCP-first extension model | Free OSS | Pushed 2026-08-26; 53k★ |
| **Amp** (ampcode.com; spun out of Sourcegraph Dec 2025) | Autonomous agent CLI/IDE, "orbs" (parallel cloud sandboxes), Oracle subagent mode [S21] | **Closed ecosystem**: models routed by Amp; Unconstrained tier has BYO keys but through Amp's gateway — no arbitrary `baseURL` [S21] | Parallel orbs + named subagents (Oracle, Librarian) | Plugin API (new in Neo rebuild, May 2026) | Subscription $20/$200/mo; free tier closed to new signups since Feb 2026 | Very active (npm publishes hourly; news through 2026-08-23) |

### Prose notes

**Ownership moves to know about:** opencode moved from `sst` to the `anomalyco` org; pi moved from `badlogic/pi-mono` into Zechner's company org `earendil-works` (pi.dev, npm `@earendil-works/pi-coding-agent`) [S5][S9]; goose left `block` for `aaif-goose` under Linux Foundation Agentic AI Foundation governance; OpenHands consolidated under its own `OpenHands` org with a TypeScript V1 rewrite (pushed 2026-08-26, 85k★, MIT) — it remains the heavyweight option (Docker runtime, LiteLLM → any provider) and is overkill for a solo Mac swarm [S22]. Amp is Amp, Inc. since Dec 2025 [S21].

**The three that fit Mike's solo-operator diagnostic swarm best:**

1. **opencode** — the only major harness whose *native* config speaks directly to both of Mike's gateways (omlx :8300, FreeLLMAPI :3100) with zero glue [S6]; child-session subagents give per-judge context isolation for free; MIT means nothing locks in.
2. **pi** — the cheapest possible judge unit: `pi -p "..." --mode json` is a stateless, scriptable, ~3x-less-context call against local omlx (already proven on this machine: the SSSF `packet_reviewer` phase runs exactly `coding_agent: pi` against omlx) [S9][S10][MASTER-GUIDE §3]. Its no-subagent philosophy is irrelevant here because the orchestrator supplies the structure.
3. **Claude Code** — retained for the *heavy* role (code execution, deep review) on the flat Max sub, with hooks enforcing Mike's existing damage-control rules; kept out of the hot loop because of observed OAuth session contention at high concurrency [S3][S4].

Everything else is either redundant (crush, aider-stalled, goose overlaps pi's niche with heavier governance story), wrong-shaped for BYO-endpoint (Gemini CLI, Amp), or infrastructure-heavy (OpenHands).

---

## 2. Council implementations

### Lineage

- **Karpathy's `llm-council`** (created 2025-11-22): three-stage pipeline — independent answers → anonymous blind cross-ranking → chairman synthesis — shipped as a vibe-coded OpenRouter web app with an explicit "Vibe Code Alert… I'm not going to support it in any way" notice; 24.3k★, effectively frozen (one push ever) [S23]. It is a *pattern*, not a dependency.
- **Live successors:** a curated ecosystem index exists (danielrosehill/Awesome-LLM-Council-Projects, April 2026 snapshot) [S24]; working ports include a Gemini CLI extension with personas/investigator subagent [S25] and Claude Code skills that honestly document what breaks when all judges come from one lab (see anonymity below) [S26]. Commercial productizations (Roundtable et al.) add sequential debate modes [S27].

### How many judges is actually useful — the cited findings

- **Voting returns are non-monotonic in judge count.** Chen et al., *Are More LLM Calls All You Need?* (arXiv:2403.02419): voting-system accuracy "first increases but then decreases" with the number of LLM calls, because easy queries benefit while hard queries degrade; the optimal count is task-dependent but predictable from small samples [S28]. Practical floor: 3 (minimum for meaningful rank aggregation), practical ceiling: 5 — beyond that you mostly buy correlated votes.
- **Minority good ideas get dropped — twice confirmed.** Wang et al., *Rethinking the Bounds of LLM Reasoning* (arXiv:2402.18272): group discussion does not beat a strong single agent with a good prompt, and its case study identifies "good ideas of the minority dropped after discussion" as a core discussion failure mode; weaker members improve, stronger ones regress [S29]. Updated for 2026 models: *Minority Sentinel* (arXiv:2606.29270, June 2026) shows contemporary LLM errors are strongly correlated (shared pretraining corpora breaks Condorcet independence), and **roughly 1 in 4 divergent cases has the minority holding the correct answer** — a ~10-point recovery margin forfeited by naive majority voting; its prescription is "audit evidence, don't count heads" [S30].
- **Corollary for harness choice:** model diversity, not harness diversity, is what decorrelates errors — five Claude Code subagents share priors; a council spanning Anthropic + GPT + local Qwen does not. The llm-council-cc skill's README is the clearest practitioner statement of this: same-lab mixing "buys tier variation, not cross-lab independence," and reviewers must not share one prompt [S26].

### Anonymity mechanics

Blind ranking (answers shuffled to labels A–D, attribution stripped) is the load-bearing mechanic inherited from Chatbot-Arena-style eval: it prevents deference/anchoring to a prestige model and suppresses self-preference [S27][S31]. Known limit, stated honestly in the practitioner ports: models may recognize their own house style, and angle-personas are self-identifying — mitigations are reviewer-specific lenses, self-ranking exclusion, and compliance-checking each returned ranking before aggregating [S26].

### Consensus protocols: rank-then-synthesize vs vote vs debate

- **Rank-then-synthesize (recommended):** forced rankings averaged into a consensus order (Borda-style), then a chairman synthesizes only across disagreement — Karpathy's topology, cheapest per bit of signal [S23][S31].
- **Vote:** only sensible for closed-set answers; subject to the non-monotonicity and minority-suppression findings above [S28][S29][S30].
- **Debate:** multi-round argument improves weak models but costs multiples and lets confident-wrong members drag consensus (bias-reinforcement effects documented in the Ringelmann-effect scaling work on effective team size, arXiv:2606.02646) [S32]. Reserve one bounded synthesis round for split verdicts; never leave debates open-ended.

---

## 3. Inter-agent communication channels — honest evaluation

| Channel | Fits | Doesn't fit | Verdict |
|---|---|---|---|
| **Git/files-as-blackboard** | Task briefs, verdicts, diffs, transcripts; durable audit; every harness can read/write; zero new infra | Real-time conversation | **Primary bus.** Matches Mike's artifact-or-nothing instinct, verification-law (claims backed by files), and existing reviewer-bot/App pattern (MASTER-GUIDE §2). Consensus aggregation should be a deterministic script over verdict files, not another LLM call |
| **Hermes `message_agent` + roster/peers** | Dispatch, status pings, wake-ups, escalation to Mike; already-running bot mode on local omlx | Bulk artifacts, structured verdicts | Secondary signaling layer. Keep payloads tiny (pointers to files, not content) |
| **tmux/send-keys (drive skill)** | Driving CLIs with no headless mode; live observability of long runs | Preferred transport for anything with a print/RPC mode | Fallback only. pi has `-p --mode json`; opencode and Claude Code have headless exec modes — prefer native non-interactive modes, keep tmux for watching (pi's own philosophy: tmux over background bash [S9]) |
| **ACP / A2A / MCP reality check** | See below | — | None of these is needed for a same-machine swarm |
| **Buzz voice** | Human-facing output surface: spoken council-verdict summaries, hands-free "council disagrees" alerts; voice input for quick go/no-go | Coordination bus: no persistence, no addressing, lossy, slow | Input/output surface only. Never route agent↔agent coordination through it |

**Protocol status (so nobody re-litigates later):** MCP won the *vertical* (agent↔tool) layer — spec 2025-11-25 under Linux Foundation AAIF governance (founding members include OpenAI, Anthropic, Google, Microsoft, AWS, Block) [S33]. A2A owns the *horizontal* agent↔agent story on paper — Google Apr 2025 → Linux Foundation mid-2025, v1.0 early 2026, IBM's REST-native ACP merged into it Aug 2025 [S34] — but it targets cross-org HTTP deployments with Agent Cards and OAuth trust; a solo operator gains nothing from standing it up locally. The other ACP — Zed's Agent Client Protocol ("LSP for coding agents," editor↔agent transport; Gemini CLI's `--experimental-acp`, goose topic tag) — is about embedding agents in editors, not agent↔agent messaging [S35]. **Practical use of MCP here:** expose gbrain/pglite as an MCP server so every harness shares one memory surface — that is a legitimate MCP job. Message-passing between harnesses stays files + Hermes signals.

---

## 4. Recommended topology for Mike

**Principle:** orchestrate with cheap deterministic glue; spend LLM calls only where judgment is required; every stage emits an artifact or it didn't happen (verification-law compliant).

```
                    ┌─────────────────────────────┐
                    │ Orchestrator: opencode       │  ← FreeLLMAPI :3100 model for its own brain;
                    │ (or plain bash+jq scripts)   │    writes briefs to agentmesh/<task>/
                    └──────────┬──────────────────┘
        ┌──────────────────────┼────────────────────────┐
        ▼                      ▼                        ▼
  WORKER (code)         JUDGE POOL (cheap)       AUDITOR (independent)
  Claude Code           N× pi --mode json        opencode instance #2 on a DIFFERENT
  on a git worktree     against omlx :8300       FreeLLMAPI model family (+ optional
  (Max sub, hooks on)   (qwen3, parallel)        codex/gemini-cli for cross-vendor)
        │                      │                        │
        └──────────┬───────────┴────────────────────────┘
                   ▼
   council/<task>/judge-{N}.json  ← artifact-or-nothing; rankings + findings + confidence
                   ▼
   aggregate.py (Borda average-rank, deterministic, no LLM) → VERDICT.md + git commit
                   ▼
   Hermes message_agent → Mike; Buzz speaks the one-line verdict
```

- **Roles:** orchestrator/research = opencode + pi; code = Claude Code (worktree-per-session, per DONT.md worktree rule); audit/judges = mixed-model pool via opencode #2 + pi/omlx + optionally codex. Cross-*lab* diversity is the point (§2); cross-harness alone is cosmetic.
- **Judge count:** 3 default, 5 max (non-monotonic returns [S28]). On any 2–1 or 3–2 split: run one bounded evidence-audit round targeting the dissent, not an open debate (minority-truth rate ≈ 25% [S30]).
- **Scheduling/recording:** launchd or Hermes-cron triggers a council run; the run is valid iff `VERDICT.md` lands in git with all judge artifacts referenced. Reuse existing machinery — the SSSF phase-gate + `verdict_consistent` pattern and the reviewer-bot App identity are already the same shape (MASTER-GUIDE §2–3); extend them, don't stand up parallel infra (rules/no-parallel-infrastructure.md).
- **Minimal glue (all that's missing):** (1) `aggregate.py` — pure-Python rank aggregation over judge JSON, ~100 lines, no LLM; (2) two opencode provider blocks pointing at :3100/:8300 (config-only, [S6]); (3) a Hermes handler that reads `VERDICT.md` and announces. Nothing else.
- **Cost:** omlx and the Max sub are already paid/free; marginal cost of a 3-judge local council is minutes of M-series time. Amp/Gemini CLI add nothing this topology needs.

---

## SOURCES

- [S1] https://github.com/anthropics/claude-code · https://code.claude.com/docs/en/overview
- [S2] https://code.claude.com/docs/en/settings (env/model config, Bedrock/Vertex)
- [S3] https://code.claude.com/docs/en/sub-agents
- [S4] https://code.claude.com/docs/en/hooks
- [S5] https://github.com/anomalyco/opencode (GitHub API: pushed_at 2026-08-26, MIT)
- [S6] https://opencode.ai/docs/providers (custom `@ai-sdk/openai-compatible` provider + baseURL examples)
- [S7] https://github.com/rothnic/opencode-agents/blob/main/docs/opencode-config.md (subagent child-session isolation)
- [S8] https://github.com/code-yeongyu/oh-my-opencode (plugin, hooks compat layer)
- [S9] https://pi.dev/ · https://mariozechner.at/posts/2025-11-30-pi-coding-agent
- [S10] https://github.com/earendil-works/pi (modes, providers, models.json; pushed 2026-08-26) · secondary writeup incl. Databricks benchmark claim (reported, not independently verified): https://www.explainx.ai/blog/pi-minimal-agent-harness-mario-zechner-guide-2026
- [S11] https://deepwiki.com/code-yeongyu/oh-my-openagent · https://www.glukhov.org/ai-devtools/opencode/oh-my-opencode-agents/
- [S12] https://github.com/openai/codex (Rust, Apache-2.0, pushed 2026-08-26)
- [S13] https://github.com/openai/codex/blob/main/docs/config.md (`model_providers.base_url`, `wire_api`) · https://learn.chatgpt.com/docs/config-file/config-advanced (built-ins, OSS mode)
- [S14] https://codex.danielvaughan.com/2026/03/31/codex-cli-custom-model-providers/ (multi-agent fan-out caveat on non-OpenAI providers)
- [S15] https://github.com/google-gemini/gemini-cli
- [S16] https://github.com/google-gemini/gemini-cli/issues/15430 (GOOGLE_GEMINI_BASE_URL fix, PR #25357)
- [S17] https://github.com/google-gemini/gemini-cli/issues/16504 (ACP mode custom endpoint: closed not_planned)
- [S18] https://github.com/charmbracelet/crush
- [S19] https://github.com/Aider-AI/aider (API: pushed_at 2026-05-22 — stalled)
- [S20] https://github.com/aaif-goose/goose · https://apiscout.dev/guides/mcp-vs-a2a-agent-protocols-2026 (Block as AAIF founding member)
- [S21] https://ampcode.com/pricing · https://ampcode.com/ · https://locoroo.net/reports/2026-may/sourcegraph (spinout Dec 2025, Neo rebuild, free-tier closure Feb 2026)
- [S22] https://github.com/OpenHands/OpenHands
- [S23] https://github.com/karpathy/llm-council (created 2025-11-22; Vibe Code Alert disclaimer)
- [S24] https://github.com/danielrosehill/Awesome-LLM-Council-Projects
- [S25] https://github.com/theerud/gemini-llm-council
- [S26] https://github.com/Carlos-Padilla-Bravo/llm-council-cc (same-lab substitution analysis; blind-ranking limits)
- [S27] https://roundtable.now/solutions/llm-council · https://www.mindstudio.ai/blog/how-to-build-llm-council-ensemble-agents (blind-ranking rationale, 3–5 judge guidance)
- [S28] Chen et al., *Are More LLM Calls All You Need? Towards Scaling Laws of Compound Inference Systems*, https://arxiv.org/abs/2403.02419 (voting non-monotonicity)
- [S29] Wang et al., *Rethinking the Bounds of LLM Reasoning: Are Multi-Agent Discussions the Key?*, https://arxiv.org/abs/2402.18272 (strong-single-agent parity; minority-good-ideas-dropped case study)
- [S30] *Minority Sentinel: When to Overturn Majority Voting in Multi-Agent LLM Debates*, https://arxiv.org/abs/2606.29270 (correlated errors; minority correct ~1 in 4 divergences; audit-don't-count)
- [S31] *Let LLMs Judge Each Other: Multi-Agent Peer-Reviewed Reasoning*, https://arxiv.org/html/2606.15419v1 (peer-review mechanics)
- [S32] *The Ringelmann Effect in Multi-Agent LLM Systems*, https://arxiv.org/html/2606.02646v1 (effective team size)
- [S33] MCP → Linux Foundation AAIF (Dec 2025), spec 2025-11-25: https://codex.danielvaughan.com/2026/05/29/agent-to-agent-communication-protocols-a2a-vs-acp-vs-mcp-compared · https://www.metavert.io/mcp-vs-a2a
- [S34] A2A governance + IBM ACP merger: https://lfaidata.foundation/communityblog/2025/08/29/acp-joins-forces-with-a2a-under-the-linux-foundations-lf-ai-data/ · https://www.zdnet.com/article/linux-foundation-adopts-a2a-protocol-to-help-solve-one-of-ais-most-pressing-challenges · https://www.dreaming.press/posts/a2a-vs-acp-vs-agntcy-agent-interop-protocols.html
- [S35] Zed Agent Client Protocol (distinct from IBM ACP): https://www.dreaming.press/posts/a2a-vs-acp-vs-agntcy-agent-interop-protocols.html · https://github.com/block/goose → aaif-goose topics `acp`

*Local evidence cited:* `~/agent-configs/MASTER-GUIDE.md` §2–§4 (reviewer-bot pattern, SSSF pi+omlx reviewer phase, FreeLLMAPI port 3100, omlx cutover, Claude OAuth contention); `~/.claude/skills/drive-tmux-automation/SKILL.md` (drive/tmux pattern).
