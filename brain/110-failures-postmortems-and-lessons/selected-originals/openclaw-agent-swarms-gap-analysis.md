# SOTA Agent-Swarm Gap Analysis — 2026-05-23

> Author: openclaw-archivist subagent · Sources: ~22 web searches against verified primary sources (Anthropic, Cognition, OpenAI, arXiv, GitHub, official docs). Date: 2026-05-23.

---

## 1. TL;DR

Your stack is missing **three primitives the SOTA has converged on in the last 12 months**: (a) a *clarify-before-act* gate on every spawn (Anthropic's `AskUserQuestion`, the CLAM/AskToAct line of research), (b) a *shared blackboard / read-before-act* memory hook (Anthropic's "context engineering" + LangGraph's `StateGraph` + the blackboard literature), and (c) a *load-bearing-vs-preference* constraint primitive (closest analog: A2A "Agent Cards", PydanticAI structured constraints, and Symphony's tasks-as-tickets). Every other failure on your list cascades from missing one of those three. The industry pendulum has officially swung back to multi-agent (Cognition reversed publicly on 2026-03-19) but the consensus is now **hierarchical orchestrator + isolated children + single-threaded writes + shared read-only context**, which is roughly your shape — you just need to add the three primitives above and stop spawning duplicates.

---

## 2. BUILDING — adoption candidates this week

| # | Action | Repo / Source | What it fixes (failure mode) | Hours to integrate | DR136 fit |
|---|---|---|---|---|---|
| B1 | **Wire `AskUserQuestion` into Dispatch spawn flow** as a mandatory pre-spawn step ("any constraint inferred, not stated, must be confirmed") | [Claude Code AskUserQuestion docs](https://code.claude.com/docs/en/agent-sdk/user-input) — native, no new dep | FM-1 (silent assumption), FM-8 (no disambiguation) | 2–4 h | Native to Claude Code; pure upstream adopt |
| B2 | **Adopt LangGraph `StateGraph` checkpointing for the swarm-level shared state** (or port the pattern into `.agents/memory/` as a typed Pydantic schema) | [langchain-ai/langgraph](https://github.com/langchain-ai/langgraph) — 32.7k stars, ACTIVE per LangChain release policy | FM-2 (no shared state), FM-3 (memory not reflexive), FM-7 (no orchestrator introspection) | 8–12 h to prototype on one workstream | Battle-tested at Klarna/LinkedIn/Uber/Replit |
| B3 | **Add a pre-flight capability probe as a `PreToolUse` hook** ("can this session run `gh`? does it have shell? is it Cowork sandbox or Code?") — emit a one-line tool-inventory dump on session start | [Claude Code hooks](https://code.claude.com/docs/en/hooks) (UserPromptSubmit + PreToolUse fire pre-execution) | FM-6 (Cowork-vs-Code hidden) | 2 h | Native hook system; no external dep |
| B4 | **Mirror Anthropic's lead-spawns-3–5-subagents-with-token-budget pattern** explicitly in BOOTSTRAP.md and the spawn approval gate (DR082). Each spawn gets a token ceiling and a stop-after-N-failures rule. | [Anthropic engineering: How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) (June 2025) | FM-4 (cascading spawns), FM-2 (no shared state across spawns), token usage 80% of variance | 4–6 h (constitution edit + DR082 amendment + budget enforcement script) | First-party Anthropic guidance — straight port |
| B5 | **Steal the Symphony "task as ticket" primitive** for marking load-bearing constraints. Every spawn brief becomes a structured ticket with `must_have` / `nice_to_have` / `assumed_from_inference` fields. | [openai/symphony](https://github.com/openai/symphony) (you have it vendored already — extract just the SPEC.md task shape) | FM-1 (silent assumption), FM-5 (no load-bearing primitive), FM-4 (cascading spawns) | 4 h to retrofit BOOTSTRAP.md brief template | Already vendored; extract small piece |
| B6 | **Adopt Reflexion-style verbal-feedback log** at the swarm level: on each `BLOCKED` (DR026/034), the failure summary gets appended to a swarm-wide JSONL that the next spawn reads first. | [noahshinn/reflexion](https://github.com/noahshinn/reflexion) (NeurIPS 2023, arxiv:2303.11366); pattern only — implement against your existing `.agents/memory/feedback/` | FM-3 (memory not reflexive), FM-4 (cascading spawns) | 3–4 h | Pattern adopt; you already have the storage layer |

Stop at six. Anything past this is gold-plating until B1–B6 actually ship.

---

## 3. SOTA snapshot table

| Framework / Pattern | Type | Stars / Citations (verified) | Maturity | Addresses failure modes | Adoption cost for Mike |
|---|---|---|---|---|---|
| **Anthropic multi-agent research system** ([blog](https://www.anthropic.com/engineering/multi-agent-research-system)) | Pattern + Claude Code primitives | First-party Anthropic, June 2025; +90.2% over single-agent on internal eval | Production (powers Claude.ai Research) | FM-1, FM-2, FM-4, FM-7 | Low — already your model |
| **Claude Code (subagents / hooks / skills / AskUserQuestion)** ([docs](https://code.claude.com/docs/en/agent-sdk/user-input)) | Harness | First-party; AskUserQuestion shipped v2.0.21 | Production | FM-1, FM-6, FM-8 | Native — already your harness |
| **OpenAI Agents SDK** ([repo](https://github.com/openai/openai-agents-python)) | Framework | ~19k stars (Python) + ~2.4k (JS) per search | Production (Stripe, etc.) | FM-7 (built-in tracing) | Medium — Python-first; not Claude-native |
| **LangGraph** ([repo](https://github.com/langchain-ai/langgraph)) | Stateful graph orchestrator | 32.7k stars; ACTIVE per LangChain release policy | Production (Klarna, LinkedIn, Uber, Replit) | FM-2, FM-3, FM-7 | Medium — pattern port is easy, full adopt is heavy |
| **CrewAI** ([repo](https://github.com/crewAIInc/crewAI)) | Role-based multi-agent | 50.8k stars (May 2026); 27M PyPI dl on core | Production | FM-7 (modest) | High — opinionated; would replace your topology |
| **Microsoft Agent Framework** ([learn.microsoft.com](https://learn.microsoft.com/en-us/agent-framework/overview/)) | Framework (AutoGen + SK merge) | GA 2026-04-07 | Production (enterprise) | FM-2, FM-7 | High — .NET/Python; not Claude-native |
| **AutoGen (microsoft/autogen)** ([repo](https://github.com/microsoft/autogen)) | Framework | 56.6k stars but **MAINTENANCE ONLY** since Oct 2025 | Frozen | n/a — do not adopt new | Skip |
| **AG2 fork** ([repo](https://github.com/ag2ai/ag2)) | Community AutoGen fork | Active but small community | Beta/community | FM-2 partially | Skip unless you need v0.2 GroupChat |
| **PydanticAI** ([repo](https://github.com/pydantic/pydantic-ai)) | Type-safe agent framework | 16.5–16.8k stars; v1 Sept 2025 | Production-ready | FM-5 (type-checked constraints) | Medium — Python-only; great primitive for FM-5 |
| **Mastra** ([repo](https://github.com/mastra-ai/mastra)) | TypeScript-first | 24.2k stars (May 2026); $22M Series A 2026-04 | Production | FM-2 partially | Skip — wrong language for your stack |
| **DSPy** ([repo](https://github.com/stanfordnlp/dspy)) | Declarative LM programming + optimizer | 28k+ stars (late 2025); Khattab, Stanford → MIT | Research-leaning | Optimization, not orchestration | Skip for swarm work; useful elsewhere |
| **Llama Stack** ([repo](https://github.com/meta-llama/llama-stack)) | Meta agent APIs | Active community calls | Active but narrow | Niche | Skip — Llama-centric |
| **Semantic Kernel** ([repo](https://github.com/microsoft/semantic-kernel)) | Microsoft framework | **MAINTENANCE ONLY** (Oct 2025) | Frozen | n/a | Skip |
| **OpenHands (ex-OpenDevin)** ([openhands.dev](https://www.openhands.dev/)) | Coding agent platform | ~65–70k stars | Production OSS | FM-6 (sandbox-aware) | High — would replace harness |
| **Symphony** ([repo](https://github.com/openai/symphony)) | Spec for ticket-driven orchestration | OpenAI spec, 2026-04-27; 6× PR throughput claim | Spec / reference | FM-2, FM-4, FM-5 | **You already vendored it** — extract the task primitive |
| **Letta (ex-MemGPT)** ([letta.com](https://www.letta.com/)) | Stateful memory framework | Production OSS | Production | FM-3 | Medium — strong on stateful memory if you want a server |
| **A2A Protocol (Google + Linux Foundation)** ([atlan.com](https://atlan.com/know/google-a2a-protocol/), [ibm.com](https://www.ibm.com/think/topics/agent2agent-protocol)) | Inter-agent open standard | 150+ org supporters; LF-governed | Stable spec (April 2025) | FM-2, FM-7 | Watch — useful when you need cross-vendor agents |
| **MCP (Anthropic)** ([modelcontextprotocol.io](https://modelcontextprotocol.io/)) | Tool/resource protocol | 500+ public servers; OpenAI/Google/Anthropic | Production | FM-6 (capability discovery) | Already adopted |
| **Mixture-of-Agents (MoA)** ([arxiv:2406.04692](https://arxiv.org/abs/2406.04692)) | Research pattern | 65.1% AlpacaEval (open models > GPT-4o); ICLR 2025 | Pattern | Aggregate-then-synthesize quality | Pattern, not framework |
| **Reflexion** ([arxiv:2303.11366](https://arxiv.org/abs/2303.11366)) | Self-reflection loop | NeurIPS 2023 | Pattern | FM-3, FM-4 | Pattern adopt — see B6 |
| **Tree of Thoughts** ([arxiv:2305.10601](https://arxiv.org/abs/2305.10601)) | Deliberate search | NeurIPS 2023; Yao et al., Princeton | Pattern | Hard reasoning only | Skip for swarm; useful in Sage-mode |
| **Voyager** ([arxiv:2305.16291](https://arxiv.org/abs/2305.16291)) | Skill library + lifelong learning | NVIDIA + Caltech; 3.3× items, 15.3× tech-tree speed | Pattern (Minecraft) | FM-3 (skill memory) | Pattern — inspire your skill registry |
| **AWM (Agent Workflow Memory)** ([arxiv:2409.07429](https://arxiv.org/abs/2409.07429)) | Workflow induction | +24.6% Mind2Web, +51.1% WebArena | Pattern | FM-3 (induce reusable workflows) | Pattern — inspire CTX/feedback induction |
| **SwiftSage** ([arxiv:2305.17390](https://arxiv.org/abs/2305.17390)) | Fast/slow dual-system agent | NeurIPS 2023 spotlight | Pattern | Routing simple-vs-complex | Mirrors your C4 routing already |
| **MetaGPT** ([repo](https://github.com/FoundationAgents/MetaGPT), [arxiv:2308.00352](https://arxiv.org/abs/2308.00352)) | Role-based SOPs (PM/Architect/Eng) | ICLR 2024 Oral | Pattern + framework | FM-2 partial | Skip framework; pattern overlaps your Prime/Forge/Scout |
| **AgentVerse** ([repo](https://github.com/OpenBMB/AgentVerse)) | Tsinghua/OpenBMB simulation | Research framework | Research | n/a | Skip — research-leaning |
| **CLAM** ([arxiv:2212.07769](https://arxiv.org/abs/2212.07769)) | Selective clarification for ambiguous Q | Kuhn/Gal/Farquhar | Pattern | FM-1, FM-8 | Pattern adopt — see B1 |
| **AskToAct** ([arxiv:2503.01940](https://arxiv.org/pdf/2503.01940)) | Self-correcting tool clarification | >79% recovery of unspecified intents; +48.34% clarification efficiency | Pattern | FM-1, FM-8 | Pattern reinforces B1 |
| **τ-bench** ([arxiv:2406.12045](https://arxiv.org/abs/2406.12045)) | Tool-Agent-User benchmark | ICLR 2025 (Sierra, **not** Anthropic) | Eval | n/a (use to score your stack) | Optional eval harness |
| **AgentBench / ScienceAgentBench** ([arxiv:2308.03688](https://arxiv.org/abs/2308.03688), [arxiv:2410.05080](https://arxiv.org/abs/2410.05080)) | Multi-domain agent evals | Tsinghua + OSU-NLP, ICLR'25 | Eval | n/a | Optional eval harness |
| **Sakana AI Scientist v2** ([arxiv:2504.08066](https://arxiv.org/pdf/2504.08066)) | Autonomous research via tree search | 1 paper through ICLR'25 workshop peer review (with hallucinations) | Research demo | Bear case for autoresearch | See §6 bear case |
| **Blackboard Multi-Agent Systems** ([arxiv:2507.01701](https://arxiv.org/html/2507.01701v1)) | Architecture pattern | Active 2025 literature | Pattern | FM-2, FM-3, FM-7 | Pattern — inspires §5 design |

---

## 4. Gap analysis — failure mode → SOTA solution → adoption path

| # | Failure mode | SOTA solution(s) | Adoption path for Mike |
|---|---|---|---|
| **1** | Silent wrong assumption + hack-stacking (Gmail-as-sender 290+ turns) | (a) Claude Code `AskUserQuestion` (v2.0.21, native); (b) CLAM (Kuhn et al., arxiv:2212.07769) — classify-then-ask two-step; (c) AskToAct (arxiv:2503.01940) — recovers unspecified intents >79% | **B1 + B5.** Add to BOOTSTRAP.md §0: "Any constraint inferred from a single mention is treated as ambiguous — `AskUserQuestion` it or mark `assumed_from_inference` in the brief." Make this a hook-blocked pre-spawn check. |
| **2** | No shared state across 200+ child sessions | (a) LangGraph `StateGraph` + checkpointer; (b) Blackboard MAS (arxiv:2507.01701) — global readable/writable space; (c) A2A protocol (April 2025, LF) — Agent Cards advertise state | **B2.** Port the StateGraph pattern into `.agents/memory/` as a typed swarm-state Pydantic model (you already started — schemas commit f353649083). Make `swarm-bootstrap.sh` inject a "what's currently in flight" digest. |
| **3** | Memory exists but not reflexively consulted | (a) Anthropic context engineering ([Anthropic engineering blog](https://www.anthropic.com/engineering/multi-agent-research-system)); (b) Letta/MemGPT stateful agent server; (c) AWM workflow induction (arxiv:2409.07429) — extract reusable workflows from trajectories; (d) Voyager skill library | **B6.** Add a `UserPromptSubmit` hook that injects top-N relevant `.agents/memory/feedback/` entries into the spawn context BEFORE the agent starts thinking. You already have DR088 doing top-N feedback injection in `swarm-bootstrap.sh` — extend it to per-spawn, not just bootstrap. |
| **4** | Failures cascade by spawning more tasks | (a) Reflexion (arxiv:2303.11366) — verbal-feedback log; (b) Cognition "Managed Devins" pattern (2026-03-19) — coordinator owns context, kills children, reports back; (c) DR026/034 hard-stop after 3 failures (you already have this — enforce it) | **B4 + B6.** Token-budget watchdog per spawn (Anthropic 80%-of-variance finding). After 3 BLOCKED, the orchestrator MUST escalate to Mike via Slack DM (DR091/092 §9), not spawn workaround N+1. Reflexion-style failure summary becomes the first thing the next spawn reads. |
| **5** | No first-class "load-bearing vs preference" primitive | (a) Symphony task-ticket structure (you vendored it); (b) PydanticAI typed constraints; (c) A2A Agent Cards with explicit capability constraints | **B5.** Brief template field: `must_have: []` / `nice_to_have: []` / `assumed_from_inference: []`. Spawn approval gate (DR082) rejects briefs missing those sections. |
| **6** | Cowork sandbox vs Code session hidden | (a) Claude Code hooks — `PreToolUse` fires pre-execution; (b) MCP capability discovery (list_tools on connect); (c) Codex sandbox preflight checks (Codex docs) | **B3.** A `session-start` hook that runs `which gh && which git && command -v claude-code` and posts the inventory to the first turn's context. If a brief requires `gh` and `gh` isn't on PATH, abort BEFORE the model burns turns. |
| **7** | Dispatch orchestrator has no introspection | (a) LangGraph checkpoint replay; (b) OpenAI Agents SDK tracing (built-in); (c) Anthropic orchestrator-worker pattern — lead reads subagent trajectories ([Cognition 2026-03-19](https://cognition.ai/blog/devin-can-now-manage-devins) explicitly cites this); (d) Blackboard architecture | **B2 (LangGraph state) + B4 (Anthropic pattern).** The orchestrator should be able to read the full trajectory of each child on completion — not just the final summary. Cognition's "Devin can read full trajectories of managed Devins" is the exact target. |
| **8** | AskUserQuestion rarely used mid-task | (a) Claude Code `AskUserQuestion` tool (native v2.0.21+); (b) CLAM two-step (classify ambiguity → ask); (c) Anthropic Plan Mode pattern (5–10 rounds of questioning before plan) | **B1.** Make it a §0 imperative: "If you would have to guess between two non-trivially-different interpretations, you must `AskUserQuestion` instead." Wire into the same hook as B1. Reframe: this is not about asking *more*, it's about asking *before* — Plan Mode style. |

---

## 5. Architectural pattern recommendations — "if greenfield v3 swarm tomorrow"

```
                    ┌──────────────────────────────────────┐
                    │   Mike (in-loop only for §9          │
                    │   irreversible / load-bearing-clarify) │
                    └────────────────┬─────────────────────┘
                                     │
                                     ▼
       ┌──────────────────────────────────────────────────────────┐
       │  PRIME orchestrator (Opus, single-threaded WRITES)       │
       │  - reads BOOTSTRAP.md + swarm-state.json on every turn   │
       │  - mandatory AskUserQuestion gate on inferred constraints│
       │  - 3-failure-then-escalate (DR026/034, enforced)         │
       └──┬────────────┬───────────────┬───────────────┬──────────┘
          │            │               │               │
   spawn ▼    spawn  ▼      spawn   ▼     spawn     ▼
   ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
   │ FORGE    │  │ SCOUT    │  │ SENTINEL │  │ OPERATOR │
   │ (code)   │  │ (research│  │ (health) │  │ (ops)    │
   │ Sonnet   │  │ Haiku)   │  │ Haiku)   │  │ Haiku)   │
   │ + token  │  │ + token  │  │ + token  │  │ + token  │
   │ budget   │  │ budget   │  │ budget   │  │ budget   │
   │ + 3-fail │  │ + 3-fail │  │ + 3-fail │  │ + 3-fail │
   └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘
        │             │             │             │
        └─────────────┴─────────────┴─────────────┘
                      │
                      ▼
       ┌──────────────────────────────────────────────────────────┐
       │  SHARED BLACKBOARD  (read-only for children, atomic writes from Prime) │
       │  - swarm-state.json   (current in-flight work)           │
       │  - context.jsonl      (append-only event stream)         │
       │  - feedback/*.md      (top-N auto-injected per spawn)    │
       │  - artifact-index.jsonl                                   │
       │  - claims.jsonl       (lock primitive)                    │
       │  - failure-log.jsonl  (Reflexion-style verbal feedback)   │
       └──────────────────────────────────────────────────────────┘
                      ▲
                      │ (UserPromptSubmit hook injects relevant slice)
                      │
                      │ (PreToolUse hook checks capabilities)
                      │
   Each spawn brief is a Symphony-shaped TICKET:
   { id, parent_id, must_have:[], nice_to_have:[],
     assumed_from_inference:[], capabilities_required:[],
     token_budget, failure_budget, success_criterion }
```

**Five primitives that must exist (named):**

1. **`Clarify-gate`** — Mandatory pre-spawn check. Any constraint inferred from a single user mention is either (a) confirmed via `AskUserQuestion` or (b) explicitly marked `assumed_from_inference` in the brief. CLAM-style two-step (classify-then-ask) so it doesn't fire on every spawn. Addresses FM-1, FM-8.

2. **`Ticket-brief`** — Every spawn is a structured ticket with `must_have` / `nice_to_have` / `assumed_from_inference` / `capabilities_required` / `token_budget` / `failure_budget` / `success_criterion`. Borrowed from Symphony task shape. Addresses FM-5, FM-4.

3. **`Blackboard`** — Single read-only-to-children, write-via-Prime shared state object (swarm-state.json + context.jsonl + feedback + failure-log). `UserPromptSubmit` hook injects the relevant slice into every spawn's first turn. Addresses FM-2, FM-3, FM-7.

4. **`Capability-probe`** — `PreToolUse` hook on session start that enumerates available tools/binaries and aborts if `must_have_capabilities` not present. Addresses FM-6.

5. **`Reflexion-log`** — Append-only `failure-log.jsonl`. On every BLOCKED (DR026), the failure summary lands here. Next spawn reads the most-recent N entries first. After 3 failures on the same workstream, escalate to Mike (DR091/092) — do NOT spawn N+1. Addresses FM-3, FM-4.

---

## 6. COUNTER-BUBBLE (the bear case — mandatory)

### 6.1 The single most damning critique: multi-agent debate often makes things *worse*

The Du/Li/Torralba/Tenenbaum/Mordatch 2023 paper "Improving Factuality and Reasoning in Language Models through Multiagent Debate" ([arxiv:2305.14325](https://arxiv.org/pdf/2305.14325)) is widely cited as the foundation of multi-agent reasoning. But follow-up work — "Talk Isn't Always Cheap: Understanding Failure Modes in Multi-Agent Debate" ([arxiv:2509.05396](https://arxiv.org/pdf/2509.05396)) and "Can LLM Agents Really Debate?" ([arxiv:2511.07784](https://arxiv.org/html/2511.07784v1)) — finds that:

- **Group accuracy often *declines* over successive debate rounds**, even when individual agents were correct.
- Agents are sycophantic: an eloquent-but-wrong agent sways the others.
- Triggering MAD on every query is computationally wasteful and can overturn correct single-agent answers.

**Implication for your stack:** Resist the temptation to add "debate" or "tournament-judging" layers without a measured baseline. Anthropic's pattern (orchestrator + isolated parallel children + single synthesizer) is *not* debate — children don't see each other. That distinction is load-bearing. The MoA paper (Wang et al. 2024, [arxiv:2406.04692](https://arxiv.org/abs/2406.04692)) is genuine aggregation (65.1% on AlpacaEval) but is still single-task, not orchestration. Don't blur them.

### 6.2 Cognition reversed publicly — but the reversal is narrower than the AI-bull press makes it sound

Walden Yan's "Don't Build Multi-Agents" ([cognition.ai/blog/dont-build-multi-agents](https://cognition.ai/blog/dont-build-multi-agents), June 2025) was the strongest stated single-agent position in the industry. On **2026-03-19**, Cognition shipped ["Devin can now Manage Devins"](https://cognition.ai/blog/devin-can-now-manage-devins) and followed with ["Multi-Agents: What's Actually Working"](https://cognition.ai/blog/multi-agents-working). That **is** a reversal — but the architecture they actually shipped is "single-threaded writes, additional agents contribute intelligence rather than actions." Specifically: a manager owns the full context, children get clean slates with narrow focus, children's actions are isolated, manager synthesizes. **Yan's "fragmented context" argument was not retracted** — it was solved by making children write-isolated rather than by going pure single-agent. The hype framing ("Cognition reverses") is louder than the substance ("Cognition adds a constrained sub-agent layer to single-agent core"). Your stack is structurally already on the post-2026 consensus; you don't need to change topology, just add the guardrails (§5).

### 6.3 Microsoft AutoGen and Semantic Kernel are dead — 56.6k stars notwithstanding

Both projects entered **maintenance mode October 2025** ([VentureBeat](https://venturebeat.com/ai/microsoft-retires-autogen-and-debuts-agent-framework-to-unify-and-govern), [Microsoft Learn migration guide](https://learn.microsoft.com/en-us/agent-framework/migration-guide/from-semantic-kernel/), and the [microsoft/autogen discussion #7210](https://github.com/microsoft/autogen/discussions/7210) confirming it). The Microsoft Agent Framework merger of the two GA'd 2026-04-07. **Do not adopt either AutoGen or Semantic Kernel today** — they have stable APIs but no new features and no model-quality work. If you see a "look at AutoGen for X" recommendation, it's stale. BabyAGI was archived 2024-09 per its repo readme; AutoGPT is still releasing but is essentially a legacy curiosity in 2026.

### 6.4 Sakana AI Scientist v2's headline result is shakier than the press release

Sakana's [v2 paper](https://arxiv.org/pdf/2504.08066) (April 2025) claimed an AI-authored paper passed ICLR 2025 workshop peer review. The post-hoc evaluation paper ["Evaluating Sakana's AI Scientist: Bold Claims, Mixed Results, and a Promising Future?"](https://arxiv.org/abs/2502.14297) found **hallucinations, fabricated results, and overestimated novelty** in the accepted paper. This is directly relevant to your autoresearch ambitions: tree-search-based research agents *can* produce paper-shaped outputs without producing actually-correct papers. Build the evaluator before you trust the generator.

### 6.5 The "multi-agent = parallelism" framing is mostly cope for context-window limits

Anthropic's own June 2025 blog reports multi-agent research costs **~15× more tokens** than chat for the same query, and that **token usage alone explains ~80% of performance variance** in BrowseComp. Read carefully: the multi-agent pattern wins because it spends more compute *more parallelizably*, not because "multiple agents collaborate" is intrinsically magic. If single-shot Opus-4.7-1M with the right context could see everything, the multi-agent win shrinks. Your 1M context model means **always prefer a single Opus turn with full context over a spawn**, and only spawn when (a) you need parallel I/O or (b) the child needs context isolation. The DR082 spawn approval gate is doing the right thing — keep it strict.

### 6.6 CrewAI's 50.8k stars are real, but the framework is heavyweight and opinionated

[CrewAI](https://github.com/crewAIInc/crewAI) has the largest community in the role-based-multi-agent space and credible production usage (per [getpanto.ai](https://www.getpanto.ai/blog/crewai-platform-statistics)). But its abstraction (Crew + Agent + Task + Process) is a different mental model than your Prime/Forge/Scout/Sentinel/Operator topology. Adopting CrewAI would be a *rewrite*, not an integration. Star count is not adoption fit.

---

## 7. SKIP — frameworks not worth Mike's attention

| Framework | Why skip |
|---|---|
| **CrewAI** | 50.8k stars but opinionated `Crew + Agent + Task + Process` model would require rewriting your topology. Star count != fit. Pattern is overlapping with what you already have. |
| **AutoGen (microsoft/autogen) + Semantic Kernel** | Both in maintenance mode since Oct 2025. No new features. Migrating to Microsoft Agent Framework is itself a heavy lift and the framework is .NET/Python-first, not Claude-native. |
| **Mastra** | Excellent TypeScript framework, 24.2k stars, $22M Series A, but **your stack is Python-first**. Wrong language tier-cost. |
| **MetaGPT (as framework)** | The PM/Architect/Eng role pattern overlaps with your Prime/Forge/Scout; adopting the framework would be redundant. Read the [paper](https://arxiv.org/abs/2308.00352) for SOP-encoding ideas — skip the codebase. |
| **AgentVerse** | Tsinghua research framework, code "being refactored." Lower production maturity than your alternatives. |
| **Llama Stack** | Meta-specific. You're on Claude. |
| **Tree of Thoughts (as orchestration pattern)** | Useful in deep-reasoning sub-tasks, not in swarm orchestration. Don't generalize it. |
| **Multi-agent debate (Du et al.)** | See §6.1 — known to *decrease* accuracy in many settings. Anthropic's parallel-isolated pattern is what works; debate is what doesn't. |

---

## 8. The one move that addresses 80% of pain

**Add a mandatory `Clarify-gate` on every spawn, wired through Claude Code's native `AskUserQuestion` tool, with a CLAM-style two-step (classify-ambiguity → ask-only-if-ambiguous) so it doesn't fire on every trivial call.**

Why this is the 80%:

- It directly stops FM-1 (silent assumption) at the source — the moment a constraint is inferred-not-stated, the gate fires.
- It stops FM-4 (cascading workaround spawns) because the cascade can only start if the wrong assumption gets past spawn #1. If spawn #1 must explicitly mark `assumed_from_inference: [Gmail-as-sender]`, spawn #2 reads that mark and either re-confirms or rejects the assumption. The Gmail-as-sender hack-stack cannot happen.
- It enables FM-5 (load-bearing-vs-preference) because the gate forces the structured `must_have / nice_to_have / assumed_from_inference` brief shape (§5 primitive #2).
- It's a *2–4 hour adopt* of native Claude Code v2.0.21+ infrastructure ([docs](https://code.claude.com/docs/en/agent-sdk/user-input)). No new dependency, no topology change, no rewrite. Pure DR136 upstream adopt.
- The pattern is the same one Anthropic ships in Plan Mode (5–10 rounds of questioning before any code), which means Anthropic's own research says it works.

**Concrete first action:** Add a one-paragraph §0 imperative to CLAUDE.md:

> **§0.8 — Always clarify-before-spawn.** If a brief contains any constraint inferred from a single user mention (not explicitly stated as load-bearing), the orchestrator must either (a) call `AskUserQuestion` to confirm, or (b) mark it `assumed_from_inference` in the brief. A child session that finds a constraint marked `assumed_from_inference` blocking its work must escalate to Prime, not spawn a workaround.

That single addition + the brief template field change closes the loop the Gmail-as-sender hack-stack opened. Everything in §2 BUILDING and §5 architecture builds on top.

---

## Sources

Direct primary citations used:

- [Anthropic — How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)
- [Claude Code AskUserQuestion / user-input docs](https://code.claude.com/docs/en/agent-sdk/user-input)
- [Claude Code Hooks reference](https://code.claude.com/docs/en/hooks)
- [Cognition — Don't Build Multi-Agents (Walden Yan, June 2025)](https://cognition.ai/blog/dont-build-multi-agents)
- [Cognition — Devin can now Manage Devins (2026-03-19)](https://cognition.ai/blog/devin-can-now-manage-devins)
- [Cognition — Multi-Agents: What's Actually Working](https://cognition.ai/blog/multi-agents-working)
- [OpenAI Agents SDK (Python)](https://github.com/openai/openai-agents-python)
- [OpenAI Symphony](https://github.com/openai/symphony) · [Symphony announcement](https://openai.com/index/open-source-codex-orchestration-symphony/)
- [LangGraph](https://github.com/langchain-ai/langgraph)
- [CrewAI](https://github.com/crewAIInc/crewAI)
- [Microsoft AutoGen (maintenance)](https://github.com/microsoft/autogen) · [Microsoft Agent Framework overview](https://learn.microsoft.com/en-us/agent-framework/overview/)
- [AG2 fork](https://github.com/ag2ai/ag2)
- [PydanticAI](https://github.com/pydantic/pydantic-ai)
- [Mastra](https://github.com/mastra-ai/mastra)
- [DSPy](https://github.com/stanfordnlp/dspy)
- [Llama Stack](https://github.com/meta-llama/llama-stack)
- [OpenHands](https://www.openhands.dev/)
- [Letta (ex-MemGPT)](https://www.letta.com/)
- [MCP](https://modelcontextprotocol.io/) · [A2A Protocol guide (IBM)](https://www.ibm.com/think/topics/agent2agent-protocol)
- [Mixture-of-Agents (Wang et al. 2024) arxiv:2406.04692](https://arxiv.org/abs/2406.04692)
- [Reflexion (Shinn et al. 2023) arxiv:2303.11366](https://arxiv.org/abs/2303.11366)
- [Tree of Thoughts (Yao et al. 2023) arxiv:2305.10601](https://arxiv.org/abs/2305.10601)
- [Voyager (Wang et al. 2023) arxiv:2305.16291](https://arxiv.org/abs/2305.16291)
- [Agent Workflow Memory (Wang et al. 2024) arxiv:2409.07429](https://arxiv.org/abs/2409.07429)
- [SwiftSage (Lin et al. 2023) arxiv:2305.17390](https://arxiv.org/abs/2305.17390)
- [MetaGPT (Hong et al. 2023) arxiv:2308.00352](https://arxiv.org/abs/2308.00352)
- [AgentVerse (Chen et al.) arxiv:2308.10848](https://arxiv.org/abs/2308.10848)
- [CLAM (Kuhn et al.) arxiv:2212.07769](https://arxiv.org/abs/2212.07769)
- [AskToAct arxiv:2503.01940](https://arxiv.org/pdf/2503.01940)
- [Asking Before Acting arxiv:2305.15695](https://arxiv.org/pdf/2305.15695)
- [τ-bench (Sierra) arxiv:2406.12045](https://arxiv.org/abs/2406.12045)
- [AgentBench arxiv:2308.03688](https://arxiv.org/pdf/2308.03688)
- [ScienceAgentBench arxiv:2410.05080](https://arxiv.org/abs/2410.05080)
- [Sakana AI Scientist v2 arxiv:2504.08066](https://arxiv.org/pdf/2504.08066) · [Evaluating Sakana arxiv:2502.14297](https://arxiv.org/abs/2502.14297)
- [Multi-agent debate (Du/Tenenbaum 2023) arxiv:2305.14325](https://arxiv.org/pdf/2305.14325) · [Talk Isn't Always Cheap arxiv:2509.05396](https://arxiv.org/pdf/2509.05396)
- [Blackboard LLM MAS arxiv:2507.01701](https://arxiv.org/html/2507.01701v1)
- [Karpathy Software 3.0 (YC keynote summary)](https://www.latent.space/p/s3) · [Karpathy 2025 year-in-review](https://karpathy.bearblog.dev/year-in-review-2025/)
- [VentureBeat — Microsoft retires AutoGen](https://venturebeat.com/ai/microsoft-retires-autogen-and-debuts-agent-framework-to-unify-and-govern)
