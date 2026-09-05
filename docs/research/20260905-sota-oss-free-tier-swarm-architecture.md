# SOTA Research Survey & First-Principles Architecture: Lean Autonomous Swarm (2026)

## Executive Summary

To operate a declarative, self-improving, proactive autonomous engineering swarm as a solo operator, custom infrastructure code must be aggressively eliminated. Bespoke process managers, hand-rolled routing scripts, custom memory engines, and unpruned agent layers historically collapsed under maintenance overhead.

The state of the art in 2026 demonstrates that production-grade autonomous swarms are built by composing battle-tested open-source software (OSS), generous cloud free tiers, and zero-marginal-cost local Apple Silicon inference.

---

## 1. Top OSS & Free-Tier SaaS Platforms (2026)

### 1.1 Gateways: LiteLLM vs. OpenRouter vs. FreeLLMAPI

| Feature / Dimension | LiteLLM Proxy (`BerriAI/litellm`) | OpenRouter (`openrouter.ai`) | FreeLLMAPI (`tashfeenahmed/freellmapi`) |
| :--- | :--- | :--- | :--- |
| **Primary Architecture** | Self-hosted reverse proxy (Python/Docker) on port 4000/3100. | Managed cloud API gateway. | Self-hosted proxy (Go/Docker) tailored for free quotas. |
| **Failover & Resilience** | Granular fallback cascades, cooldowns, exponential retries, load balancing across keys. | Automatic fallback array via `models: ["provider/model-a", "provider/model-b"]`. | Round-robin and failover across 30+ free provider accounts. |
| **Prompt Caching** | Pass-through caching (Anthropic, DeepSeek, Google) plus local semantic Redis caching. | Native pass-through caching for supported upstream providers (Anthropic, DeepSeek). | Minimal or pass-through only; depends on upstream provider limits. |
| **Virtual Keys & Limits** | Enterprise-grade: per-key budgets, spend ceilings, RPM/TPM caps, Prometheus metrics. | Credit-based virtual keys, hard spend limits per key, activity dashboards. | Basic key encryption at rest; focused on quota rotation, not team billing. |
| **First-Principles Fit** | **Primary Local/VPC Gateway**: Total data privacy, zero markup, strict spend guardrails. | **Cloud Fallback Layer**: Zero infra maintenance, instant access to 250+ models. | **Free Tier Harvester**: Aggregates disparate free tiers into a single OpenAI-compatible `/v1`. |

- **LiteLLM Proxy**: The gold standard for self-hosted swarm routing. It unifies all downstream model providers behind a single OpenAI-compatible `/v1/chat/completions` endpoint. Its virtual key subsystem allows setting hard spend caps (for example, max $5/day per worker) and automated fallbacks when rate limits (HTTP 429) hit.
- **OpenRouter**: Ideal as a managed fallback. Provides instant access to upstream models without managing separate accounts, and transparently routes prompt cache hits.
- **FreeLLMAPI**: A specialized gateway designed to harvest free tiers from providers like Groq, Google AI Studio, NVIDIA NIM, Mistral, and GitHub Models.

---

### 1.2 Free Tier Models & Local Apple Silicon Acceleration

#### Google Gemini 2.5 Flash
- **Context Window**: 1,000,000 tokens.
- **Google AI Studio Free Limits**: 15 Requests Per Minute (RPM), 1,000,000 Tokens Per Minute (TPM), 1,500 Requests Per Day (RPD).
- **Context Caching**: Explicit context caching for prompts exceeding 32,768 tokens, radically lowering time-to-first-token (TTFT).
- **Role in Swarm**: High-volume ingestion. Ideal for digesting entire code repositories, 200-page government RFPs, and raw research dumps.
- **Trade-off**: Free-tier data is subject to Google model improvement logging; paid tier ($0.075 / $0.30 per 1M tokens) is required for strict privacy.

#### Groq Free Tier
- **Hardware Architecture**: LPU (Language Processing Unit) inference engine.
- **Speed**: 300 to 800 tokens per second.
- **Free Tier Models**: Llama 3.3 70B Versatile, Llama 3.1 8B, Mixtral 8x7B.
- **Rate Limits**: 30 RPM, 6,000 to 30,000 TPM depending on model, 14,400 RPD.
- **Role in Swarm**: Ultra-low-latency verification loops. Executes rapid AST parsing, regex validation, JSON structuring, and sanity checks where execution time must remain under 300ms.

#### Cloudflare Workers AI
- **Free Allocation**: 10,000 Neurons per day on the free Workers plan.
- **Deployment**: Serverless execution at Cloudflare edge nodes in 300+ cities.
- **Available Models**: `@cf/meta/llama-3.3-70b-instruct`, `@cf/meta/llama-3.1-8b-instruct`, DeepSeek-R1 Distill, and BAAI BGE embeddings (`@cf/baai/bge-base-en-v1.5`).
- **Role in Swarm**: Event-driven triage, edge webhook processing, and free vector embedding generation without maintaining local server daemons.

#### OpenRouter Free Models
- **Catalog Suffix**: Models tagged with `:free` (for example, `meta-llama/llama-3.3-70b-instruct:free`, `deepseek/deepseek-r1:free`, `qwen/qwen-2.5-coder-32b-instruct:free`).
- **Rate Limits**: 20 requests/minute, 200 requests/day for zero-balance accounts (waived to higher limits by holding a minimal credit balance).
- **Role in Swarm**: Resilient overflow buffer when primary cloud accounts or local resources are saturated.

#### Local Apple Silicon MLX / oMLX (`jundot/omlx`)
- **Framework**: Apple MLX optimized for Apple Silicon unified memory (36GB to 192GB).
- **Breakthrough Innovation (oMLX)**: Paged SSD KV Caching. Standard local servers recompute the entire context prefix on every turn. oMLX stores KV cache blocks across RAM and fast NVMe SSD storage, restoring context prefixes instantaneously without GPU recomputation.
- **Continuous Batching**: Native macOS menu bar server supporting continuous batching, multi-model hosting (LLM, vision, embeddings, rerankers), and OpenAI/Anthropic drop-in API compatibility.
- **Target Models**: Qwen 2.5 Coder 32B (4-bit/8-bit), Llama 3.3 70B (4-bit).
- **Cost & Privacy**: Exact $0 marginal cost per token, 100% offline privacy, zero rate limits.

---

### 1.3 Asynchronous Cloud Workers

#### GitHub Jules (Google Labs)
- **Quota**: 100 autonomous sessions/day on Google AI Pro ($19.99/mo), with 15 concurrent sessions. Free tier provides 15 tasks/day.
- **Mechanism**: Connects directly to GitHub repositories. Upon issue assignment, it spins up an isolated cloud virtual machine, clones the repo, builds the project, plans changes, executes code edits, runs verification tests, and opens a fully formed Pull Request.
- **Swarm Value**: Completely frees local Apple Silicon compute and disk space from routine Tier 2/3 engineering chores (test suite generation, dependency upgrades, routine refactoring, bug fixes).

#### OpenHands (`All-Hands-AI/OpenHands`, formerly OpenDevin)
- **Architecture**: Modular, open-source agent platform. Uses an AgentHub core with an event-stream architecture.
- **Sandboxing**: Executes code, terminal operations, and web browsing inside isolated Docker containers.
- **Distributed Execution**: Supports Temporal-backed workers for durable, pause-and-resume execution across cloud instances.
- **Swarm Value**: The premier self-hosted, unmetered alternative to proprietary cloud coding agents.

#### Closed-Source vs. Open Alternatives (Devin, Copilot Workspace)
- **Devin (Cognition AI)**: Highly autonomous but expensive ($500/month seat or high compute unit pricing), creating vendor lock-in.
- **GitHub Copilot Workspace**: Interactive, task-centric specification and planning environment embedded in GitHub issues; excellent for human steering, less suited for headless background worker fleets.
- **First-Principles Assessment**: The combination of GitHub Jules (for managed cloud PR tasks) and OpenHands (for unmetered local Docker tasks) delivers full enterprise capability without bespoke code or high SaaS subscriptions.

---

### 1.4 Memory, Context, and Knowledge Management

#### Garry Tan's GBrain (`garrytan/gbrain`)
- **Core Technology**: PGlite (PostgreSQL compiled to WebAssembly) running locally on Bun/Node with `pgvector`, stored locally at `~/.gbrain/brain.pglite`.
- **Auto-Wiring Knowledge Graph**: Automatically derives typed entity relationships (`works_at`, `invested_in`, `mentions`) directly from Markdown files and notes without requiring dedicated LLM extraction passes.
- **Hybrid Retrieval**: Combines pgvector embeddings, BM25 text search, and Reciprocal Rank Fusion (RRF).
- **Model Context Protocol (MCP)**: Exposes search and storage tools directly to Claude Code, Codex CLI, and Cursor via MCP.
- **Prompt Cache Protection**: Keeps base system prompts lean (<800 tokens) by injecting memories dynamically on demand, maximizing prompt cache hit rates.

#### Mem0 (`mem0ai/mem0`, formerly Embedchain)
- **Architecture**: Multi-layered memory hierarchy encompassing User, Session, and Agent states.
- **Dynamic State Resolution**: Employs an intelligent extraction layer that resolves contradictory or updating facts over time (for example, updating a changed API key or user preference rather than appending stale duplicates).
- **Storage Engines**: Backed by Qdrant, Milvus, or Neo4j for hybrid graph and vector recall.

#### Karpathy Wiki-LLM Pattern
- **Reference**: Andrej Karpathy's LLM-Wiki / AutoResearch design.
- **Three-Tier Architecture**:
  1. *Immutable Raw Intake*: Web documents (`trafilatura`), YouTube transcripts, and raw notes remain untouched in a raw directory.
  2. *LLM Librarian Compilation*: A background worker (using Gemini Flash or local Qwen) processes raw intake once, compiles structured Markdown summaries, generates bi-directional `[[wikilinks]]`, and updates Map of Content (MOC) index files.
  3. *Progressive Disclosure*: Agents navigate the knowledge base by inspecting top-level index files (<50 lines) and following specific `[[wikilinks]]` only when relevant. The human operator browses an interconnected visual graph in Obsidian.

---

### 1.5 Self-Improvement & Proactivity

#### Compound Engineering Plugin (`EveryInc/compound-engineering-plugin`)
- **Core Philosophy**: Software engineering must be a compounding loop where every solved problem permanently improves future execution.
- **Workflow Cycle**:
  - `Brainstorm` -> `Plan` (`/ce-plan`) -> `Work` (`/ce-work`) -> `Review` (`/ce-code-review`) -> `Compound` (`/ce-compound`) -> `Autonomous Loop` (`/lfg`).
- **Mechanics**: The `/ce-compound` command captures post-task learnings, root-cause fixes, and architectural boundaries, committing them into repository rules and agent skills. Subsequent agents automatically read these rules, preventing regression loops.

#### DSPy (`stanfordnlp/dspy`)
- **Core Philosophy**: "Programming, not prompting." Replaces fragile prompt engineering with declarative, typed modules (`dspy.Signature`).
- **Teleprompters & Compilers (MIPROv2, SIMPRO)**: Automatically optimizes instructions and synthesizes few-shot demonstrations against objective evaluation metrics (such as unit test exit codes or validation schemas).
- **Swarm Value**: Removes hand-rolled prompt spaghetti; prompt instructions are compiled and version-controlled mathematically.

#### Hermes Self-Evolution Loops (NousResearch Hermes Agent)
- **Continuous Trajectory Feedback**: Captures tool usage, function calling, and multi-step reasoning traces.
- **Skill Discovery**: When an agent solves a novel engineering obstacle, it crystallizes the executable steps into a reusable `agentskills.io` skill file.
- **Trajectory Curation**: Trajectories with verified successful outcomes are staged for DPO/RL fine-tuning pools or local few-shot memory.

---

## 2. First-Principles Lean Architecture

### 2.1 The Historical Root Cause & Failure Modes

An analysis of past iterations (OpenClaw, Hermes Agent, Buzz, Fusion) reveals the primary pitfall: **Layering without retiring**.
- Systems accumulated 110 competing `AGENTS.md` files and 250+ unpruned worktrees.
- Operators wrote bespoke bash daemons, hand-rolled routing scripts, and custom SQLite state machines instead of using standard operating system and git primitives.
- Flat swarms with 20+ persistent agents collapsed due to communication storms, token exhaustion, and context pollution.

### 2.2 The Elimination Principles (Mike's Starred Repos)

1. **The Ponytail Decision Ladder (`DietrichGebert/ponytail`)**: Strict YAGNI (You Aren't Gonna Need It). The best code is code never written. Prioritize standard Unix utilities, git features, and established OSS tools before writing any custom scripts.
2. **Caveman Syntax Pruning (`JuliusBrussee/caveman`)**: Strip pleasantries and conversational filler from agent-to-agent interactions. Reducing prompt and response tokens by 65% to 75% saves budget and preserves context windows.
3. **Mechanical WIP Limits & Concurrency (`hatchet-dev/hatchet`)**: Enforce hard limits using POSIX atomic lockfiles (`.agents/locks/`). Allow exactly WIP = 1 per repository, and a global maximum of 3 concurrent active workers.
4. **Baseline 5 + Ephemeral N**: Maintain exactly 5 core roles; all specialist subagents spin up as ephemeral tasks in temporary worktrees and scale to zero upon completion.

---

### 2.3 The Lean Stack Architecture

```
+---------------------------------------------------------------------------+
|                          SOLO OPERATOR (Human Chair)                      |
|                Directs goals, reviews PRs, approves budgets               |
+-------------------------------------+-------------------------------------+
                                      |
                                      v
+---------------------------------------------------------------------------+
|                        BASELINE 5 ORCHESTRATION LAYER                     |
|  - Prime (Executive Planner)        - Forge (Implementation Engine)       |
|  - Scout (Proactive Research)       - Sentinel (Quality & Safety Gate)    |
|  - Operator (GitOps & Reaper)                                             |
+-------------+-----------------------+-------------------------+-----------+
              |                       |                         |
              v                       v                         v
+-----------------------+ +-----------------------+ +-----------------------+
|   KNOWLEDGE & MEMORY  | |   INFERENCE GATEWAY   | |   EXECUTION RUNNERS   |
|  - GBrain (PGLite MCP)| |  - LiteLLM Proxy      | |  - GitHub Jules (Cloud|
|  - Karpathy Wiki      | |    (:4000 / :3100)    | |    100 sessions/day)  |
|    (Obsidian vault)   | |  - Drop-in OpenAI /v1 | |  - Ephemeral Worktrees|
|  - Compound Skills    | |  - Prompt cache pass  | |    (10-min launchd    |
|    (/ce-compound)     | |  - Hard virtual limits| |     reaper daemon)    |
+-----------------------+ +-----------+-----------+ +-----------------------+
                                      |
              +-----------------------+-------------------------+
              v                                                 v
+---------------------------------------+   +-------------------------------+
|   ZERO-MARGINAL-COST COMPUTE          |   |   FRONTIER SUBSCRIPTIONS      |
| - Tier 0: Local Apple Silicon oMLX    |   | - Tier 3: Claude Code Max     |
|   (Qwen 2.5 Coder 32B, paged SSD KV)  |   |   (Sonnet 3.7 / Opus 4.8)     |
| - Tier 1: Gemini 2.5 Flash (1M free)  |   | - Tier 3: OpenAI Codex CLI    |
| - Tier 1: Groq Free (Llama 3.3 70B)   |   |   *Guarded by Sentinel        |
| - Tier 1: Cloudflare Workers AI       |   |   *2-try circuit breaker      |
+---------------------------------------+   +-------------------------------+
```

---

### 2.4 The Four-Tier Cost-Optimized Routing Matrix

1. **Tier 0: Local Apple Silicon Inference ($0.00)**
   - **Engine**: oMLX (`jundot/omlx`) running Qwen 2.5 Coder 32B or Llama 3.3 70B on port 8300.
   - **Use Case**: Offline loops, continuous test evaluation, code formatting, overnight research filtering.
   - **Advantage**: Paged SSD KV caching enables instant multi-turn prompt resume with zero token cost.

2. **Tier 1: Cloud Free Tiers ($0.00)**
   - **Google Gemini 2.5 Flash**: Context ingestion up to 1M tokens, RFP shredding, and Karpathy Wiki compilation.
   - **Groq Free**: High-speed AST parsing, JSON extraction, and fast linting (<300ms).
   - **Cloudflare Workers AI**: Edge webhook parsing and BAAI BGE vector embeddings.
   - **FreeLLMAPI / OpenRouter `:free`**: Quota overflow and failover routing.

3. **Tier 2: Asynchronous Cloud PR Engine ($20.00/month flat)**
   - **GitHub Jules**: 100 free tasks/day via Google AI Pro.
   - **Use Case**: Bounded issues, bug fixes, refactoring, documentation, and test creation. Runs entirely in isolated cloud VMs, opening clean PRs without local machine resource consumption.

4. **Tier 3: Frontier Subscriptions (Protected by Circuit Breakers)**
   - **Claude Code (Max Subscription) & Codex CLI**: Reserved strictly for high-judgment tasks: system architecture, complex multi-file engineering, and security audits.
   - **Sentinel Enforcement**: A mandatory 2-try circuit breaker immediately aborts loops if an action fails twice, preventing recursive token drain.

---

### 2.5 Concrete Elimination Ledger

| Bespoke / Fragile Component | Replace With Battle-Tested SOTA | Immediate Benefit |
| :--- | :--- | :--- |
| Hand-rolled Python routing scripts | **LiteLLM Proxy** (`BerriAI/litellm`) | Standards-compliant OpenAI `/v1`, automatic failover, virtual keys. |
| Custom database for agent memory | **Garry Tan GBrain** (`garrytan/gbrain`) | PGlite WASM + pgvector via MCP; zero server configuration. |
| Custom web scraping / knowledge store | **Karpathy Wiki-LLM** in Obsidian | Clean Markdown with `[[wikilinks]]`; progressive disclosure. |
| Heavy Kubernetes runners for agents | **GitHub Jules** + Ephemeral Worktrees | 100 cloud sessions/day; zero local worktree bloat. |
| Custom feedback/learning loop scripts | **Compound Engineering** (`EveryInc`) | Standard `/ce-compound` commits lessons into git rules. |
| Manual prompt tweaking and edits | **DSPy** (`stanfordnlp/dspy`) | Programmatic signatures, MIPROv2 objective auto-tuning. |
| Verbose agent chatter and token burn | **Caveman Syntax** (`JuliusBrussee/caveman`)| 65% to 75% reduction in token consumption. |
| Over-engineered bespoke tooling | **Ponytail Decision Ladder** (`DietrichGebert`) | Radical YAGNI; reliance on Unix stdlib and git primitives. |

---

## 3. Primary Sources & Repository Citations

1. **LiteLLM**: BerriAI/litellm (https://github.com/BerriAI/litellm)
2. **FreeLLMAPI**: Tashfeen Ahmed (https://github.com/tashfeenahmed/freellmapi)
3. **oMLX (Apple Silicon MLX Server)**: Jundot (https://github.com/jundot/omlx)
4. **GBrain (PGLite WASM MCP)**: Garry Tan (https://github.com/garrytan/gbrain)
5. **OpenHands (Autonomous Platform)**: All-Hands-AI (https://github.com/All-Hands-AI/OpenHands)
6. **Compound Engineering Plugin**: EveryInc (https://github.com/EveryInc/compound-engineering-plugin)
7. **DSPy Framework**: Stanford NLP (https://github.com/stanfordnlp/dspy)
8. **Mem0 (Long-term Memory)**: Mem0AI (https://github.com/mem0ai/mem0)
9. **Ponytail (Anti-Bloat Decision Ladder)**: Dietrich Gebert (https://github.com/DietrichGebert/ponytail)
10. **Caveman (Terse Token Optimization)**: Julius Brussee (https://github.com/JuliusBrussee/caveman)
11. **Hatchet (Workflow Concurrency)**: Hatchet Dev (https://github.com/hatchet-dev/hatchet)
12. **Hermes Agent & Function Calling**: NousResearch (https://github.com/NousResearch/hermes-agent)
13. **Google Gemini API**: Google AI for Developers (https://ai.google.dev)
14. **Groq LPU Inference**: Groq Cloud (https://groq.com)
15. **Cloudflare Workers AI**: Cloudflare Docs (https://developers.cloudflare.com/workers-ai/)
