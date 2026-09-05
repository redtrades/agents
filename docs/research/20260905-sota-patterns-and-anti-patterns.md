# Catalog of SOTA Patterns & Anti-Patterns for Autonomous Swarms (2026)

**Date:** 2026-09-05  
**Context:** Canonical reference catalog synthesizing 13 research reports, Apple Silicon M1 Max roofline microarchitecture benchmarks, starred repository patterns (Runfusion/Fusion, paperclipai/paperclip, hatchet-dev/hatchet, conductor-oss/conductor, garrytan/gbrain, DietrichGebert/ponytail, JuliusBrussee/caveman), and local estate history.  
**Authority:** Architectural reference for `/Users/man/agents` and `/Users/man/Brain`.

---

## Executive Summary

This catalog establishes the definitive architectural boundary between production-grade state-of-the-art (SOTA) engineering patterns and the historical failure modes (anti-patterns) that led to worktree explosion, context amnesia, circular meta-work, and daemon gridlock.

Its purpose is to eliminate recurring debates, prevent ungrounded abstractions, and ensure all agents operating across harnesses (`claude`, `codex`, `opencode`, `cursor`, `agy`) build on verified engineering baselines.

---

## Domain 1: Swarm Orchestration & Control Planes

### SOTA Pattern: Single-Agent Baseline with Explicit State Transitions
- **Mechanics:** 
  - Solo-agent execution is the default. Multi-agent delegation occurs only across explicit, isolated supervisor-worker boundaries with disjoint file scopes.
  - Multi-step tasks execute as directed cyclic state graphs (LangGraph, Hatchet CEL concurrency, or Temporal workflows) where state is typed and persisted after every step.
  - Single Source of Truth: GitHub Issues and Pull Requests serve as the unified task queue.
  - Visual Telemetry: Runfusion Fusion on port 4040 operates purely as a lightweight viewer and DAG dependency visualizer over Git, not an independent state store.
- **Primary References:** `hatchet-dev/hatchet`, `conductor-oss/conductor`, `Runfusion/Fusion`.

### Anti-Pattern: The Multi-Agent Fallacy & Multi-Control-Plane Trap
- **Symptoms:**
  - Spawning 5 to 10 autonomous agents in a flat chatroom before a single-agent baseline has succeeded.
  - Running Buzz (Nostr relay on port 3000), Hatchet (Postgres), Fusion (port 4040), and OpenHands (Docker) simultaneously on a single workstation.
  - Cross-system state drift: a task is marked `done` in GitHub, `in-progress` in Fusion, and `pending` in Buzz.
  - Cognitive and memory collapse: 14 to 18 GB of RAM consumed by idle coordination daemons, while agents hallucinate completions.
- **Root Cause:** Layering new control planes on top of unretired legacy platforms without pruning.

### Estate Standard for `/Users/man/agents`:
- Single task queue anchored in GitHub Issues (`redtrades/agents`).
- Risk-Tiered Autonomy Ladder (L1 to L4) controls delegation.
- Maximum 2 concurrent working trees globally across the machine.

---

## Domain 2: State Externalization & Anti-Amnesia

### SOTA Pattern: Git-Backed Incremental Checkpoints (`CONTINUATION.md`)
- **Mechanics:**
  - State is externalized continuously to disk after every atomic action.
  - Git commits serve as the immutable, tamper-evident execution ledger (`git log -n 5 --oneline`).
  - A compact 50-line machine-readable `CONTINUATION.md` records task identity, completed commit SHAs, active step, and exact next shell command.
  - Cold-Start Resume: An incoming agent reads only `CONTINUATION.md` and runs `git diff HEAD~1`. It resumes execution in under 2 seconds for less than 500 tokens.
- **Primary References:** `OthmanAdi/planning-with-files`, `paperclipai/paperclip`.

### Anti-Pattern: Conversational Memory Dependency & Parallel JSONL Bloat
- **Symptoms:**
  - Relying on conversation history across session breaks, resets, or hourly quota cutoffs.
  - Re-ingesting 50,000 tokens of conversational transcript on every resume, burning budget and immediately hitting token limits.
  - Building bespoke JSONL event log databases that drift out of sync with actual git commit SHAs.
- **Root Cause:** Treating conversational context as durable state rather than ephemeral cache.

### Estate Standard for `/Users/man/agents`:
- Maintain `TASK.md` and `CONTINUATION.md` in repository root after every step.
- Zero uncommitted code left across turns.
- Resume protocol requires reading <500 tokens.

---

## Domain 3: Decision Lifecycle, Taxonomy & Promotion Ladder

### SOTA Pattern: 5-State Decision Machine with Operator Ratification
- **Mechanics:**
  - Decisions flow through 5 explicit lifecycle states: `PROPOSED`, `RATIFIED`, `SUPERSEDED`, `STALE`, and `REJECTED`.
  - Level A Architectural decisions are documented in MADR format under `docs/decisions/YYYYMMDD-NNNN-<slug>.md`.
  - Level B Operational and tactical decisions are tracked in `docs/decisions/DECISION_LOG.md`.
  - Human Ratification Gate: Ideas, explorations, and conversational nuances remain `PROPOSED`. Only explicit owner confirmation promotes a decision to `RATIFIED`.
  - Superseded decisions preserve history with explicit successor pointers (`-> DEC-xxx`).
- **Primary References:** Michael Nygard MADR standard, Boris Cherny ("Govern, don't inform").

### Anti-Pattern: Unratified Nuance Bleed & Re-Adjudication Sprawl
- **Symptoms:**
  - Casual brainstorming in chat is mistaken for ratified policy by subsequent agents.
  - Unconfirmed rules silently appear in operational instructions.
  - Constant re-adjudication: agents re-debate already settled architectural boundaries because previous decisions were never given immutable IDs or explicit states.
  - 110 competing `AGENTS.md` files scattered across unpruned directories.
- **Root Cause:** Lack of an explicit decision state machine and failure to decouple proposed ideas from ratified law.

### Estate Standard for `/Users/man/agents`:
- Operational ledger in `docs/decisions/DECISION_LOG.md`.
- Unconfirmed items remain `PROPOSED` until Mike explicitly confirms them.
- All governing rules in `rules/` and `AGENTS.md` must link to a `RATIFIED` decision.

---

## Domain 4: Tooling & Code Minimization (The Ponytail YAGNI Ladder)

### SOTA Pattern: Standard Tools First (SSSF Principles)
- **Mechanics:**
  - The Ponytail YAGNI Ladder: Standard OS/CLI tools > top installed packages / OSS libraries > minimal bespoke glue code.
  - Thin Agents, Fat Recipes: Execution mechanics live in standard Makefiles and shell scripts (`make test`, `make validate`, `make garden`); agents provide judgment, error diagnosis, and parameter selection.
  - Surgical Edits: Modify only lines directly relevant to the user request. Zero orthogonal damage to adjacent working code.
- **Primary References:** `DietrichGebert/ponytail`, `JuliusBrussee/caveman`, Disler Single-Source Software Factory (SSSF).

### Anti-Pattern: Bespoke Wrapper Proliferation (NIH Syndrome)
- **Symptoms:**
  - Writing custom Python wrappers (such as 2,760 lines of `src/adapters/` that wrapped `claude`, `codex`, and `opencode` CLIs with subprocess daemons).
  - Building custom file watchers, bespoke process monitors, and custom JSON parsers where `fd`, `rg`, `uv`, and `make` already exist.
  - Brittle abstractions that break whenever an upstream CLI tool updates its flags or output formatting.
- **Root Cause:** Not Invented Here (NIH) syndrome and reflexive coding before researching existing tooling.

### Estate Standard for `/Users/man/agents`:
- Zero custom Python wrappers for CLI harnesses. Harnesses execute directly via native CLI or Makefiles.
- 4 distilled living rule files in `rules/` (`communication.md`, `hygiene.md`, `task-tracking.md`, `verification.md`).

---

## Domain 5: Local Compute Right-Sizing (Apple Silicon M1 Max 64GB)

### SOTA Pattern: 14B Q4 Fast Local Models on MLX
- **Mechanics:**
  - The Apple M1 Max features 64 GB of unified memory with ~400 GB/s bandwidth. Operating system and development tools consume 14 to 18 GB, leaving ~46 GB for inference and cache.
  - The Sweet Spot: Qwen 2.5 Coder 14B (MLX Q4_K_M) requires ~9 GB for weights and ~5 GB for a 32k KV cache (14 GB total).
  - Generates 38 to 48 tokens/second, providing instant responses for lint fixing, syntax parsing, unit test authoring, and privacy-sensitive compliance shredding.
  - Leaves 45 GB of free RAM, avoiding swap and keeping host performance snappy.
- **Primary References:** Apple Silicon Roofline Microarchitecture benchmarks (Aug 27 & Sep 5).

### Anti-Pattern: Sluggish 32B/70B Models Triggering Memory Thrashing
- **Symptoms:**
  - Running Qwen 2.5 Coder 32B or 70B locally on the M1 Max.
  - Memory consumption exceeds 34 GB, forcing macOS into swap memory compression.
  - Token generation speed plummets to 12 to 14 tokens/second.
  - Agent workflows experience massive latency, causing timeouts and operator frustration.
- **Root Cause:** Benchmarking model parameter count on paper rather than evaluating tokens/second throughput and system memory headroom.

### Estate Standard for `/Users/man/agents`:
- Local inference workhorse: Qwen 2.5 Coder 14B (MLX 4-bit) for high-speed local tasks.
- Cloud frontier models: Claude 3.7 Sonnet / Opus 4.8 / GPT-5 for high-judgment architecture and synthesis.

---

## Domain 6: Context Window Economics & Progressive Disclosure

### SOTA Pattern: 3-Tier Map of Content (MOC) & Externalized Memory
- **Mechanics:**
  - Progressive disclosure prevents prompt blowout:
    - Tier 0: Domain Index in resident prompt (<300 tokens).
    - Tier 1: Category Manifest listing skill titles and single-line triggers.
    - Tier 2: Execution Body (`SKILL.md`, <8 KB loaded on demand).
  - Externalized Memory: Garry Tan GBrain (`~/.gbrain/brain.pglite` via WASM MCP) + Karpathy Wiki-LLM (interlinked Obsidian Markdown vault in `/Users/man/Brain` with `[[wikilinks]]`).
  - Context tokens are treated as finite, high-cost working memory, not a long-term storage bin.
- **Primary References:** `garrytan/gbrain`, Andrej Karpathy LLM-Wiki / AutoResearch.

### Anti-Pattern: Raw Skill Ingestion & Context Pollution
- **Symptoms:**
  - Dumping 184 raw skill instructions directly into agent system prompts, consuming 27,000+ tokens before the user has even typed a character.
  - Prompt cache invalidation caused by constantly shifting system prompts.
  - Diluted attention: LLM loses focus on core instructions and hallucinates non-existent tools.
- **Root Cause:** Failure to decouple skill discovery from skill execution.

### Estate Standard for `/Users/man/agents`:
- Resident agent prompt capped under 800 tokens.
- Skills loaded strictly on demand via 3-Tier MOC.
- Canonical Knowledge Vault centralized in `/Users/man/Brain`.

---

## Domain 7: Value Delivery & Revenue Alignment (GovCon Proposal Factory)

### SOTA Pattern: Four-Stage Hybrid Pipeline Tethered to Revenue
- **Mechanics:**
  - All agent infrastructure exists to serve production value delivery, principally the GovCon capture factory ($8,000 to $10,000/month revenue target).
  - Stage 1: RFP Ingestion via Gemini 2.5 Flash Free Tier (1M token context digests complete 250-page DoD/GSA solicitations for $0.00).
  - Stage 2: Compliance Shredding via local Qwen 2.5 Coder 14B (extracts FAR/DFARS compliance matrices locally without leaking proprietary proposal data).
  - Stage 3: High-Judgment Proposal Drafting via Claude Code Sonnet/Opus (drafts Technical Approach Section C against the shredded matrix).
  - Stage 4: Deterministic Compliance Verification via static `pytest` assertions (verifies every mandatory requirement is explicitly addressed).
- **Primary References:** `cmp1` / `govcon-corpus` specifications.

### Anti-Pattern: Infrastructure Hobbyism & Detached Swarm Tinkering
- **Symptoms:**
  - Spending weeks writing agent orchestrators, swarm visualizers, and prompt frameworks that never touch customer contracts or revenue generation.
  - Accumulating technical debt across 5 disconnected repositories without shipping a single completed proposal volume.
- **Root Cause:** Treating agent engineering as an academic exercise rather than a commercial production asset.

### Estate Standard for `/Users/man/agents`:
- Every autonomous feature and skill must trace to either sovereign estate maintenance or GovCon proposal deliverables.

---

## Domain 8: Legacy Migration & Estate Consolidation

### SOTA Pattern: Strangler Fig Pattern & Zero-Token Mechanical Triage
- **Mechanics:**
  - Zero bulk copying of legacy folders (`agent-*`).
  - Selective Distillation: Mechanical scanners index legacy files without LLM token cost (`tools/triage_historic_estate.py`).
  - High-leverage assets are extracted, refined to modern schemas, and committed into dedicated estate namespaces (`plugins/estate-*`) with `provenance: estate-native`.
  - Legacy repositories are moved to cold archive (`~/archive/`) and deleted from the active path.
- **Primary References:** Martin Fowler Strangler Fig Pattern, Anti-Wholesale Ingestion Law.

### Anti-Pattern: Wholesale Migration & Recursive Folder Sprawl
- **Symptoms:**
  - Bulk copying legacy `agent-platform`, `agent-mesh`, and `agent-configs` into the new repo.
  - Importing thousands of dead symlinks, obsolete Python wrappers, and redundant prompt templates.
  - Creating circular symlinks between active code and legacy folders, causing infinite directory loops during searches.
- **Root Cause:** The fear of losing historical work leading to uncurated hoarding.

### Estate Standard for `/Users/man/agents`:
- Anti-Wholesale Ingestion Law enforced.
- Mechanical triage manifest (`docs/research/20260905-historic-estate-triage.json`) governs candidate asset selection.
- All promoted assets undergo SDLC review queue approval.

---

## Quick Reference: Pattern vs. Anti-Pattern Matrix

| Engineering Dimension | SOTA Pattern (Adopted) | Anti-Pattern (Banned) | Estate Mechanism |
| :--- | :--- | :--- | :--- |
| **Swarm Orchestration** | Directed cyclic state graphs (Hatchet/Temporal), single-agent baseline | Flat uncoordinated chatrooms, multi-control-plane sprawl | L1-L4 Autonomy Ladder, GitHub Issues queue |
| **Task State** | Git commits + `CONTINUATION.md` (<500 token cold resume) | Ephemeral conversation memory, parallel drifting JSONL | `TASK.md` + `CONTINUATION.md` |
| **Decisions** | 5-state lifecycle (`PROPOSED`, `RATIFIED`, `SUPERSEDED`, `STALE`, `REJECTED`) | Unratified nuance bleed, constant re-adjudication | `docs/decisions/DECISION_LOG.md` |
| **Tooling** | Ponytail YAGNI ladder, standard CLI tools, Makefiles | Custom Python wrappers, bespoke subprocess daemons | Native CLI harnesses, `Makefile` |
| **Local Compute** | Qwen 2.5 Coder 14B (MLX Q4, 38-48 tok/s, 14 GB RAM) | Sluggish 32B/70B models causing swap thrashing | Local MLX daemon on port 8318 |
| **Prompt Tokens** | 3-Tier Map of Content (<300 token resident prompt) | Raw bulk ingestion of 184 skills (27k token prompt) | Progressive disclosure in `plugins/` |
| **External Memory** | Garry Tan GBrain (PGLite WASM MCP) + Karpathy Wiki-LLM | Heavyweight vector DB clusters, unstructured text dumps | `/Users/man/Brain` Markdown vault |
| **Commercial Focus** | 4-stage GovCon proposal pipeline ($8-10k/mo revenue) | Detached infrastructure tinkering without revenue | GovCon proposal factory deliverables |
| **Estate Migration** | Strangler fig pattern, zero-token mechanical triage | Bulk copying legacy folders, importing dead ROT cruft | Anti-Wholesale Ingestion Law, `tools/triage_historic_estate.py` |
