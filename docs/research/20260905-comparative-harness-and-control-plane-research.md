# Comparative Research: Agent Harnesses & Control Planes (2026)

## Executive Summary

An autonomous software engineering swarm requires distinct subsystems operating in harmony: a decentralized coordination and messaging layer, a visual SDLC orchestration board, an execution harness protocol, and specialized coding agents. 

This survey documents the architectural capabilities, protocols, unique superpowers, and swarm integration roles of the leading 2026 platforms: **Buzz**, **Goose**, **Runfusion / Fusion**, **OpenHands**, **Aider**, and **Hermes Agent**.

---

## 1. Deep Capability Analysis by Tool

### 1.1 Buzz (Block / Jack Dorsey)
- **Origin & Governance:** Open-source agent-native collaboration platform released by Block in July 2026.
- **Underlying Protocol:** Decentralized Nostr protocol using a relay (default `http://localhost:3000`).
- **Core Concept:** Treats humans and AI agents as first-class, cryptographically identified citizens. Every message, task, patch, and review is signed with an agent keypair (`nsec`/`npub`).
- **Key Capabilities:**
  - **Decentralized Git Collaboration (NIP-34):** Host git repositories, issue tracking, patch proposals, and pull requests over Nostr events without central server lock-in.
  - **Agent Channels & Direct Messages (NIP-01/02):** Structured communication spaces for agent-to-agent debate, status feeds, and direct task delegation.
  - **Persistent Memory & Engrams (NIP-AE):** Cryptographic agent memory persistence allowing agents to recall past tasks and cross-repo context across sessions.
  - **Collaborative Canvases:** Shared live documents where agents co-author specifications and architectural plans before writing code.
- **Swarm Superpower:** Provides the censorship-resistant, decentralized communication bus and identity layer for autonomous agent collaboration.

---

### 1.2 Goose (Block / Linux Foundation AAIF)
- **Origin & Governance:** Open-source on-machine developer agent created by Block, contributed to the Linux Foundation Agentic AI Foundation (AAIF).
- **Architecture:** High-performance Rust CLI and desktop application.
- **Dual Protocol Support:**
  - **Agent Client Protocol (ACP):** Standardizes editor-to-agent communication. Goose runs as an ACP server over stdio (`goose acp`) or WebSocket/HTTP (`goose serve`), allowing any IDE or orchestrator to drive it seamlessly.
  - **Model Context Protocol (MCP):** Connects the agent to external tools, databases, APIs, and container runtimes.
- **Key Capabilities:**
  - **Autonomous Execution:** Writes, compiles, executes shell commands, runs tests, and iterates without manual intervention.
  - **Recipes (`goose recipe`):** Scripted, shareable, declarative workflow playbooks for repetitive engineering procedures.
  - **Diff Review Engine (`goose review`):** Native capability to inspect, parse, and verify git diffs before staging.
  - **Model Agnosticism:** Bring-your-own-model via local runners (Ollama, oMLX) or cloud providers.
- **Swarm Superpower:** The premier lightweight, headless, on-machine execution worker. Integrates cleanly via ACP without container bloat.

---

### 1.3 Runfusion / Fusion (Runfusion.ai)
- **Origin & Architecture:** Multi-node agent orchestrator and "software factory" running on port 4040 with an embedded database.
- **Core Concept:** Manages software development as an industrial assembly line across hierarchical levels (Missions -> Milestones -> Tasks).
- **Key Capabilities:**
  - **Visual SDLC Kanban Board:** Real-time visibility into task phases: Planning, In Progress, Review, and Done.
  - **Adversarial SDLC Gating:** Enforces mandatory review kinds (`plan-review`, `code-review`) where peer agents must emit an `APPROVE` verdict before promotion.
  - **Multi-Node Worktree Coordination:** Orchestrates work across local machines, servers, and VMs using isolated git worktrees with checkout lease epochs.
  - **Token & Cost Accounting:** Tracks input, output, and cached tokens in real time broken down per model provider (e.g., FreeLLMAPI, Anthropic, OpenAI).
- **Swarm Superpower:** Serves as the visual control plane, DAG dependency engine, and token accounting cockpit for human oversight and governance.

---

### 1.4 OpenHands (All-Hands-AI, formerly OpenDevin)
- **Origin & Architecture:** Open-source platform for autonomous software engineering agents.
- **Core Engine:**
  - **Event Stream Architecture:** Central nervous system where all agent actions and environment observations are published as an append-only event log.
  - **Decoupled State:** Pure separation of the agent (stateless logic) from conversation history and runtime state.
- **Key Capabilities:**
  - **Docker Sandboxing:** Every task runs inside an isolated Docker container, providing total isolation for risky build steps and package installations.
  - **AgentHub & Micro-Agents:** Pluggable library of specialized agents (code generation, web browsing, repo analysis) dispatched by a coordinator.
  - **Headless Mode:** Headless execution via CLI or REST API with structured JSONL event streaming (`--json`) for CI/CD integration.
- **Swarm Superpower:** Full container-level sandbox isolation and headless issue resolution, ideal for untrusted code execution in cloud VMs.

---

### 1.5 Aider (Paul Gauthier)
- **Origin & Architecture:** Terminal-native AI pair-programming tool tightly coupled with Git.
- **Key Capabilities:**
  - **Repository Map via Tree-Sitter & PageRank:** Analyzes the full git codebase to extract function signatures, classes, and variable references, then uses PageRank to identify key structural landmarks. Sends a token-efficient map to the LLM so it understands broad architecture without consuming excessive context.
  - **Architect Mode (`/architect`):** Two-stage division of labor. An "Architect" model reasons through the problem and outlines an implementation strategy, while an "Editor" model translates that strategy into precise file diffs.
  - **Git-Native Auto-Commit:** Automatically creates atomic, descriptive git commits for every successful modification.
- **Swarm Superpower:** Unmatched repository-wide structural reasoning using minimal tokens, and robust automated file-editing diff algorithms.

---

### 1.6 Hermes Agent (Nous Research, Feb 2026)
- **Origin & Architecture:** Autonomous agent framework designed as a persistent, 24/7 background daemon.
- **Key Capabilities:**
  - **Mixture of Agents (MoA):** Orchestrates multiple reference models to explore solutions in parallel, followed by a final aggregator model synthesizing the best combined output.
  - **Interactive Memory-Graph (`/journey`):** A visual and programmatic graph mapping acquired skills, project memories, and user preferences, which can be pruned and inspected.
  - **Self-Improving Skill Loops:** Discovers novel solutions during execution, refines them, and crystallizes them into permanent skills.
  - **Integrated Worktree Management (`hermes worktree`):** Audits and reclaims accumulated git worktrees and merged branches automatically.
- **Swarm Superpower:** Persistent daemon operation, parallel MoA reasoning, and autonomous skill crystallization.

---

## 2. Comparative Matrix

| Dimension | Buzz (Block) | Goose (Block) | Fusion (Runfusion) | OpenHands | Aider | Hermes Agent |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Primary Category** | Agent Relay / Bus | Developer Harness | Visual SDLC Factory | Sandbox Platform | Pair Programming CLI | Daemon / MoA Harness |
| **Protocol / Interface** | Nostr (NIP-34, AE) | ACP (stdio/ws), MCP | Web UI (:4040), REST | Event Stream, Docker | Terminal CLI, Git | ACP, TUI, CLI |
| **Workspace Isolation** | Git branches / NIP-34 | Host directory / ACP | Ephemeral Git worktrees | Docker containers | Git working tree | Git worktrees (built-in) |
| **Inter-Agent Messaging**| Decentralized Nostr | ACP client / server | Internal DAG queue | Event stream pub/sub | None (single agent) | Subagents, Telegram/Slack |
| **Review / Gating** | Signed NIP-34 reviews | Built-in diff review | Formal Plan/Code review| Human-in-the-loop UI | Interactive terminal | Aggregator model |
| **Token Tracking** | External | External | Real-time per-model | Session cost tracker | Per-model session stats | Per-run usage logs |
| **Resource Footprint** | Ultralight (Go/Rust) | Minimal (Rust native)| Moderate (Node/Vite) | Heavy (Docker daemon) | Minimal (Python) | Low (Python daemon) |

---

## 3. First-Principles Swarm Synthesis

To maximize throughput and eliminate human bottlenecks, these tools assemble into an efficient, layered systems engineering architecture:

1. **Coordination & Messaging (Buzz):**
   Agents communicate over Buzz Nostr channels, exchange specifications on live canvases, and coordinate git tasks via signed NIP-34 events.
2. **Visual Cockpit & SDLC Board (Fusion):**
   Fusion on port 4040 provides the visual dashboard, displays real-time task progress across columns, manages release gates, and aggregates token spend.
3. **Task Decomposition & Architecture (Aider / Hermes):**
   Incoming issues are mapped using Aider's tree-sitter repository map or analyzed via Hermes Mixture-of-Agents (MoA) to generate structured implementation plans.
4. **Autonomous Execution (Goose / Claude Code / Codex):**
   Headless workers execute code changes inside isolated ephemeral worktrees, running tests and verifying diffs.
5. **Multi-Model Review & Auto-Merge:**
   An independent reviewer model validates the diff against acceptance criteria. If deterministic tests pass and the review verdict is `APPROVE`, the branch merges directly to `main`.
