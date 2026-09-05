# SOTA Research Survey: Durable Execution & Modern Agent Architectures (2026)

## Executive Summary

Relying on ad-hoc daemon loops, bespoke bash reapers, and flat conversational agent chatrooms is an anti-pattern that collapsed under production loads. In 2026, elite AI systems engineering has converged on four decoupled architectural pillars:

1. **Durable Execution Engines** (Temporal, Hatchet, Inngest) as the state and lifecycle backbone.
2. **Cyclic State Graphs** (LangGraph, AgentOS/Agno, Microsoft Agent Framework) replacing flat agent chatrooms.
3. **Standardized Protocols** (Agent Client Protocol for IDE/client integration, Model Context Protocol for tool access) eliminating proprietary glue code.
4. **Hardware-Isolated MicroVM Sandboxes** (E2B Firecracker microVMs, Daytona) replacing brittle host execution and insecure raw Docker.

---

## 1. Durable Execution: The Real Backbone of Autonomous Swarms

### 1.1 Why Standard Daemons Fail for Swarms
Autonomous software engineering tasks take minutes or hours, require multi-step tool calls, hit API rate limits (HTTP 429), and fail non-deterministically. Traditional local daemons (bash loops, node workers) lose in-memory state on restarts, leak processes, and trigger duplicate work loops.

### 1.2 Temporal vs. Hatchet vs. Inngest

| Feature / Metric | Temporal (`temporal.io`) | Hatchet (`hatchet.run`) | Inngest (`inngest.com`) |
| :--- | :--- | :--- | :--- |
| **Primary Architecture** | Heavyweight distributed state engine (Go/Postgres/Cassandra) | Lightweight developer-first engine (Go/Postgres) | Serverless event-driven step functions |
| **Agent Replay & Caching** | Native LLM replay log; skips re-calling models on recovery | Step memoization and checkpoint persistence | Step-level caching and idempotent runs |
| **Concurrency Controls** | Worker throttles and activity semaphores | Built-in CEL concurrency keys (`concurrency_key`) | Concurrency groups and rate-limit windows |
| **Human-in-the-Loop** | Signals and Queries for approval gates | Webhook and event listeners for pause/resume | Step wait-for-event up to 1 year |
| **Resource Footprint** | Enterprise cluster required (Docker / Cloud) | Single binary + PostgreSQL database | Fully serverless cloud or lightweight dev server |

- **Temporal**: The enterprise standard. Its 2026 Agent SDKs natively record LLM completions in workflow history. If a machine crashes or reboots during a 30-minute agent run, the workflow replays instantly from history without burning additional API tokens.
- **Hatchet**: The premier local-friendly alternative. Provides high-throughput Go execution with native Common Expression Language (CEL) concurrency management, allowing strict limits like `WIP = 1 per repository` with zero custom code.

---

## 2. Multi-Agent Orchestration: Graphs vs. Flat Swarms

### 2.1 The Failure of Flat Swarms
Flat conversational architectures (where 5 to 10 agents broadcast messages in a shared channel) suffer from exponential token explosion, loss of focus, and hallucinated task completion.

### 2.2 LangGraph vs. Agno (Phidata) vs. Microsoft Agent Framework (MAF)

- **LangGraph**:
  - Models multi-agent systems as **directed cyclic graphs**.
  - State is explicitly typed and checkpointed after every node transition.
  - Features native time-travel debugging, durable checkpoints, and approval interrupts.
  - Dominates production systems where predictable state transitions and regulatory compliance are required.
- **Agno (formerly Phidata)**:
  - Built on **AgentOS** (FastAPI runtime), providing ultra-fast, lightweight execution.
  - Native multimodal streaming (text, image, audio, video) and built-in vector memory (pgvector).
  - Excellent for high-throughput, low-latency micro-agent pipelines where graph ceremony is unnecessary.
- **Microsoft Agent Framework (MAF)**:
  - Formed in 2026 by merging AutoGen with Semantic Kernel.
  - Retires legacy AutoGen group-chat patterns in favor of structured, typed enterprise workflow graphs.

---

## 3. Sandboxing & Workspace Isolation: MicroVMs vs. Docker

### 3.1 The Security and Performance Reality
Running autonomous agents directly on the host machine risks accidental deletion of local files or command injection. Standard Docker containers share the host Linux/macOS kernel, creating container escape vulnerabilities and consuming gigabytes of RAM.

### 3.2 E2B vs. Daytona vs. Git Worktrees

- **E2B (`e2b.dev`)**:
  - Runs tasks inside **Firecracker microVMs** with hardware-level isolation.
  - Cold starts under 150ms with session-scoped ephemeral lifecycles.
  - The gold standard for safely executing untrusted AI code, running automated test suites, and terminal commands.
- **Daytona (`daytona.io`)**:
  - Provides full, persistent developer environments with dev servers and GPU support.
  - Ideal when agents need to maintain long-lived state across multiple days or run continuous test daemons.
- **POSIX Ephemeral Git Worktrees**:
  - The zero-dependency alternative for local code generation.
  - Requires deterministic atomic locks (`.agents/locks/`) and a strict reaper daemon to prevent worktree leaks.

---

## 4. Standard Protocols: Eliminating Proprietary Glue

The industry has decoupled tools from agents using two universal standards:
1. **Agent Client Protocol (ACP)**: Standardizes how IDEs, terminal apps, and orchestrators communicate with agents (used by Goose, Zed, JetBrains, and Hermes).
2. **Model Context Protocol (MCP)**: Standardizes how agents communicate with tools, databases, APIs, and file systems.

---

## 5. The Composable 4-Tier Reference Architecture

```
+---------------------------------------------------------------------------+
|                          TIER 1: STATE & ORCHESTRATION                    |
|          Hatchet / Temporal / LangGraph (Durable State Engine)            |
|       - Handles retries, step checkpointing, CEL concurrency (WIP=1)      |
|       - Emits real-time state to Kanban / Observability dashboard         |
+-------------------------------------+-------------------------------------+
                                      |
                                      v
+---------------------------------------------------------------------------+
|                     TIER 2: AGENT PROTOCOL & ROUTING                      |
|                  Agent Client Protocol (ACP) + LiteLLM                    |
|       - Dynamic dispatch to interchangeable agents (Goose, Hermes, Claude)|
|       - Model gateway with automatic HTTP 429 failover & prompt caching   |
+-------------------------------------+-------------------------------------+
                                      |
                                      v
+---------------------------------------------------------------------------+
|                     TIER 3: MULTI-STAGE SDLC PIPELINE                     |
|           Planner -> Verifier -> Executor -> Adversarial Review           |
|       - Sizing / LOE classifier routes tasks to appropriate model tiers   |
|       - Independent model families enforce non-self-reviewing gates       |
+-------------------------------------+-------------------------------------+
                                      |
                                      v
+---------------------------------------------------------------------------+
|                    TIER 4: ISOLATED EXECUTION SANDBOXES                   |
|           E2B MicroVMs (Cloud) or Ephemeral Git Worktrees (Local)         |
|       - Hardware isolation, deterministic test verification               |
|       - Zero host clutter: auto-prune upon PR creation or direct merge    |
+---------------------------------------------------------------------------+
```
