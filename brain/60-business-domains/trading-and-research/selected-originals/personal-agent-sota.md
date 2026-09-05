# SOTA scan — best-in-class personal multi-vendor agent system (mid-2026)

**Date:** 2026-05-31 · **Scope:** single-operator stack — one orchestrator, multi-vendor routing, production memory, scheduled jobs, scriptable specialists. **Method:** WebSearch + WebFetch grounding only; all claims cited or marked unverified.

---

## The landscape (3–5 lines each)

### 1. Anthropic Agent SDK / Claude Code / Skills / Subagents / Hooks / Plugins / Routines
- **Primitive:** the **Skill** (a versioned `SKILL.md` folder, progressively disclosed) plus **subagents** for fan-out and **plugins** as the shipping unit (a bundle of skills + subagents + slash commands + hooks + MCP servers).
- **State:** files — `CLAUDE.md` + skill folders + `.claude/` settings; memory is a tool the model writes to, not a framework. Subagent fan-out runs as background **workflows**.
- **Auth:** API key / OAuth; MCP servers carry their own auth.
- **Deletes from a from-scratch build:** your own plugin loader, prompt-assembly layer, and sub-agent orchestration — Anthropic ships all three. ([Agent SDK overview](https://code.claude.com/docs/en/agent-sdk/overview), [anthropics/skills](https://github.com/anthropics/skills))
- **Solo example:** Every's Compound Engineering plugin (below) runs five products on this surface.

### 2. OpenAI Agents SDK (ex-Swarm)
- **Primitive:** the **handoff** — one agent explicitly transfers control + context to another. Plus guardrails, sessions, hosted tools.
- **State:** Sessions object; tracing captures every run (agents, tools, handoffs) to OpenAI's UI or third-party exporters.
- **Auth:** OpenAI API key; Responses API native.
- **Deletes:** your handoff router and your tracing/observability layer. v0.17.1 shipped 2026-05-11; Swarm is now an unmaintained educational reference. ([Handoffs](https://openai.github.io/openai-agents-python/handoffs/), [Tracing](https://openai.github.io/openai-agents-python/tracing/))

### 3. LangGraph + LangMem
- **Primitive:** the **state-graph node**; durable execution via a **checkpointer** (within-thread) + **BaseStore** (cross-thread, user-scoped).
- **State:** checkpointer (Postgres/Redis/SQLite/Mongo); LangMem adds semantic/episodic/procedural extraction on top.
- **Auth:** per-tool; self-hosted.
- **Deletes:** your persistence, resume, and time-travel logic. **Caveat:** LangMem p95 ≈ 59.8s — too slow for interactive recall; pair with Mem0/Zep for retrieval. ([LangChain memory docs](https://docs.langchain.com/oss/python/langgraph/add-memory), [atlan](https://atlan.com/know/long-term-memory-langchain-agents/))

### 4. Letta / MemGPT
- **Primitive:** **self-editing memory tiers** modeled on an OS — **core** (in-context/RAM), **recall** (searchable history/disk cache), **archival** (vector cold store). The agent pages memory in/out via tool calls.
- **State:** Letta server is the single source of truth for agent state.
- **Auth:** server-managed; model-agnostic.
- **Deletes:** your entire context-window management + memory-paging logic. ([vectorize](https://vectorize.io/articles/mem0-vs-letta), [agentmarketcap](https://agentmarketcap.ai/blog/2026/04/10/agent-memory-vendor-landscape-2026-letta-zep-mem0-langmem))

### 5. Mem0 + OpenMemory MCP
- **Primitive:** a **memory layer** with three standard scopes — episodic, semantic, procedural — and multi-signal retrieval (vector + BM25 + entity-match fused).
- **State:** vector + graph + KV store; multi-tenant by user/agent/run ID. **OpenMemory MCP** runs it **local-first** on your machine, shared across Claude/Cursor/Windsurf/VS Code.
- **Auth:** API key (cloud) or fully local (OpenMemory).
- **Deletes:** your bespoke vector store, entity extractor, and ranking. LOCOMO: 66.9% vs OpenAI memory 52.9%; ~91% lower p95 latency and ~90% fewer tokens vs full-context. ([OpenMemory MCP](https://mem0.ai/blog/introducing-openmemory-mcp), [State of AI Agent Memory 2026](https://mem0.ai/blog/state-of-ai-agent-memory-2026))

### 6. CrewAI / AutoGen / DSPy
- **Primitive:** CrewAI = **role-based crews** (role/goal/backstory + sequential task passing); AutoGen = **conversational GroupChat**; DSPy = **declarative, optimizable programs** (signatures, not prompts).
- **State:** mostly ephemeral/in-run; rely on external store.
- **Where they fail:** CrewAI's role metaphor is fastest to prototype but teams outgrow it (~18% token overhead); **AutoGen is now maintenance-mode** — merged into Microsoft Agent Framework v1.0 GA (Apr 2026). DSPy shines as an optimizer *under* an orchestrator, not as one. ([deepresearch.ninja](https://deepresearch.ninja/2026/05/AI-Agent-Frameworks-A-Comparative-Analysis-of-DSPy-Claude-Agent-SDK-OpenAI-Agents-SDK-CrewAI-AutoGen-LangGraph-and-Google-ADK/), [cordum](https://cordum.io/blog/crewai-vs-autogen-2026))

### 7. aider / Cursor agents / Devin / Replit Agent
- **Primitive:** a single-orchestrator **agentic loop** — receive goal + context → plan → edit files / run terminal → observe → repeat. Architecture is "remarkably consistent" across all of them.
- **State:** the repo + git history *is* the state; chat/session is ephemeral.
- **Split:** IDE-integrated (Cursor, Windsurf) vs autonomous/CLI (Claude Code, Codex, aider, Devin-in-cloud-sandbox).
- **Deletes:** your edit/plan/verify loop — adopt one rather than rebuild it. ([blink.new](https://blink.new/blog/best-ai-coding-agents-2026), [levelop](https://levelop.dev/blog/agentic-ai-coding-tools-how-they-actually-work-under-the-hood))

### 8. Karpathy — "small, sharp, one-thing" over frameworks
- **Primitive:** not a framework — a **posture**. Partial-autonomy co-pilots with an "autonomy slider," not untethered agents. Practical artifacts (`LLMs.txt`-style readable summaries) over heavyweight abstraction.
- **Why it beats extensible frameworks:** small composable tools keep the human in the loop, stay debuggable, and don't ossify around a vendor's abstractions. ([Sequoia: Software 3.0](https://inferencebysequoia.substack.com/p/andrej-karpathys-software-30-and), [travis.media](https://travis.media/blog/software-3-0-ai-changing-programming-karpathy/))

### 9. Compound Engineering (Every / indie solo scene)
- **Primitive:** a **4-phase loop — Plan → Work → Review → Compound** — where each task makes the next easier. Review fans out **~14 specialized agents** (security/perf/architecture/style) in parallel; lessons are written to **solution documents** that future sessions read.
- **State:** `docs/solutions/` markdown + git; a "best-practices" agent does genetic search to inject only relevant docs (avoids context bloat).
- **Solo example:** Dan Shipper + Kieran Klaassen run **five products with ~single-person teams** on this. ([rywalker](https://rywalker.com/research/compound-engineering-plugin), [joshbeckman notes](https://www.joshbeckman.org/notes/980312372))

### 10. Browser agents (Computer Use / Claude in Chrome / Antigravity / Operator)
- **Primitive:** a **vision-actuation loop** — screenshot → reason → click/type. Antigravity 2.0 (Google I/O, 2026-05-19) ships a built-in Chrome for the agent to *visually verify* its own UI work.
- **When browser > API:** no API exists, or you need to verify rendered UI / human-only flows. **When API > browser:** anything with a real endpoint — faster, deterministic, cheaper.
- **Auth:** the human's logged-in browser session. ([Antigravity](https://antigravity.google/blog/introducing-google-antigravity), [ChatGPT agent](https://openai.com/index/introducing-chatgpt-agent/))

### 11. Cloud-hosted background agents
- **Primitive:** a **saved task (prompt + repos + tools) on a trigger** — schedule, API call, or GitHub webhook — running in the vendor's cloud with no active session. **Anthropic Routines** (research preview, Apr 2026) = "cron for agents"; hourly is the finest granularity. **OpenAI Workspace Agents / Tasks** (Apr 22 2026) run after you close the laptop. GitHub Actions remains the DIY runtime.
- **Deletes:** your launchd/cron + always-on host. ([InfoQ: Routines](https://www.infoq.com/news/2026/05/anthropic-routines-claude/), [OpenAI Workspace Agents](https://openai.com/academy/workspace-agents/))

---

## Synthesis

### Convergent — what every credible 2026 system shares
- **One thin orchestrator, many cheap specialists.** Sub-agents/handoffs/crews fan out; the orchestrator stays small.
- **Memory is a managed external layer, not framework state.** Episodic + semantic + procedural scopes are now the de-facto standard (Mem0, Letta, LangMem all converge here).
- **The repo + git is the durable record.** Plans and learnings live as version-controlled markdown, re-read on the next run.
- **Scheduling moved to the vendor cloud.** Routines / Workspace Agents / Actions replaced self-managed cron+host.
- **Specialists are progressively-disclosed text** (Skills / solution docs), loaded on demand — not hardcoded prompts.

### Divergent — where credible systems disagree
- **Memory ownership:** self-editing tiers the agent controls (Letta) vs an extract-and-retrieve service the orchestrator calls (Mem0). Letta = more agent autonomy; Mem0 = faster, more debuggable.
- **Orchestration shape:** explicit graph/handoff (LangGraph, OpenAI SDK — auditable, verbose) vs emergent role-chat (CrewAI/AutoGen — fast, less controllable).
- **Framework vs no-framework:** adopt LangGraph's durability machinery vs Karpathy's "small sharp tools + git" minimalism. The indie-solo consensus leans minimalist.

### Recommendation for a single operator
- **Orchestrator → Claude Code / Anthropic Agent SDK.** It natively ships Skills + subagents + hooks + plugins, so the orchestration layer is bought, not built. *Why: zero custom orchestration code; the largest skill/plugin ecosystem.*
- **Memory → Mem0 via OpenMemory MCP (local-first).** *Why: standard 3-scope model, sub-second retrieval, one store shared across every MCP client, runs on your own machine.*
- **Router → LiteLLM proxy (self-hosted).** *Why: one OpenAI-compatible endpoint to 100+ providers with fallbacks, retries, per-key budgets, and cost tracking — the multi-vendor seam in one process.*
- **Scheduling → Anthropic Routines** for hosted recurring jobs; **GitHub Actions** for anything sub-hourly or repo-triggered. *Why: no always-on host; native to the orchestrator.*
- **Specialists → Skills + a `docs/solutions/` compound loop** (Plan→Work→Review→Compound). *Why: scriptable, version-controlled, and self-improving without new infrastructure.*
- **Vendor mix → Claude (Opus/Sonnet) for reasoning + code, GPT-5.x via LiteLLM for second-opinion/handoff, a local model (Ollama) for trivial/offline.** *Why: routed behind LiteLLM, vendor choice becomes a config line, not an architecture.*

### What gets deleted in a rebuild against this pattern
- **memPalace / multi-layer memory stack** → replaced by **Mem0 (semantic + episodic + procedural) behind OpenMemory MCP**; one store, one API.
- **hand-rolled `semantic.jsonl` + JSONL memory stores** → replaced by **Mem0's vector+graph store** (retrieval, dedup, ranking are the library's job).
- **138-rule `CLAUDE.md` constitution** → replaced by a **short `CLAUDE.md` + executable gate functions / hooks + tests**. Rules that matter become code that fails CI; the rest are deleted, not documented.
- **Per-action permission gates** → replaced by **one allow/deny policy in settings + a `careful`-style hook only on genuinely destructive ops** (rm -rf, force-push, secrets).
- **Custom dispatch/session-context + agent-comms ledgers** → replaced by the **SDK's built-in subagent/workflow tracing** + git history.
- **Bespoke cron/launchd scheduling host** → replaced by **Routines + GitHub Actions**.
- **Hand-built multi-vendor routing logic** → replaced by **LiteLLM proxy config**.

**Net:** orchestrator (Claude Code) + memory (Mem0/OpenMemory) + router (LiteLLM) + scheduler (Routines/Actions) + specialists (Skills + `docs/solutions/`). Five adopted components; almost everything custom in a v1 substrate becomes deletable glue.

---

*Unverified:* the exact phrase "small sharp tools" was not found verbatim in Karpathy's 2025 talk transcripts — the minimalist posture is sourced from Software 3.0 coverage, not a literal quote.
