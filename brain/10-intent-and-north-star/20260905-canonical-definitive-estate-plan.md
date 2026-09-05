---
name: canonical-definitive-estate-plan
version: 1.1.0
status: ratified
provenance: native
created: 2026-09-05
last_updated: 2026-09-05
tier: strategic
description: Master architectural plan for the sovereign multi-agent operating system across agents, brain, and archive.
---

# Canonical Definitive Estate Plan: The Sovereign Multi-Agent Operating System

**Date:** 2026-09-05  
**Canonical Source of Truth:** `/Users/man/agents` (GitHub `redtrades/agents`)  
**Canonical Knowledge Vault:** `/Users/man/agents/brain` (symlinked from `/Users/man/Brain` and `/Users/man/agent-knowledge-archive`)  
**Cold Archive:** `/Users/man/archive`  
**Status:** RATIFIED & CONSOLIDATED  
**Governing Documents:** `AGENTS.md`, `docs/GLOSSARY.md`, `rules/`, `brain/10-intent-and-north-star/20260905-unified-intent-and-north-star.md`

---

## 1. Executive Grounding & The Dual Mission

The estate operates as a sovereign, multi-agent software engineering engine designed to maximize operator leverage while preserving deterministic safety and cost efficiency.

```
┌───────────────────────────────────────────────────────────────────────────┐
│                    THE DUAL ENGINE OF THE OPERATING INTENT                │
├─────────────────────────────────────┬─────────────────────────────────────┤
│ 1. THE AUTONOMOUS SWARM FOUNDATION  │ 2. THE COMMERCIAL REVENUE ENGINE    │
│    (/Users/man/agents - ACTIVE)     │    (govcon-factory / cmp - PARKED)  │
│                                     │                                     │
│ - Vendor-agnostic, sovereign engine │ - Federal contracting automation    │
│ - 100 plugins, 202 agents, 225      │   (FAR/DFARS compliance matrices,   │
│   skills, 105 commands              │   Section L/M rubric shredding)     │
│ - Multi-harness: Claude Code, Codex,│ - Client-completable starters       │
│   Antigravity, OpenCode, Hermes     │ - Target: k-k/month net profit │
│ - Ephemeral isolated worktrees (<=2)│ - Status: Formal P0 Park until      │
│ - Deterministic CI + cross-review   │   swarm SDLC is fully hardened      │
└─────────────────────────────────────┴─────────────────────────────────────┘
```

---

## 2. Master Decision Ledger (Consolidated & Ratified)

This ledger consolidates the foundational decisions from the knowledge reboot (Decisions 1-58), estate ADRs (`DEC-01` to `DEC-23`), and the Phase 1 Contradiction Resolutions (`D1` to `D6`):

| Decision ID | Domain | Summary & Policy Binding | Status |
|---|---|---|---|
| **DEC-20260905-23** | Mission | Unified Estate Dual Mission: Swarm foundation active; GovCon parked. | `RATIFIED` |
| **DEC-20260905-22** | Governance | Streamlined `AGENTS.md` constitution (<=150 lines, invariants first). | `RATIFIED` |
| **DEC-20260905-21** | Compute | Cost-optimized compute routing (FreeLLMAPI :3100 + local OMLX Tier 0). | `RATIFIED` |
| **DEC-20260905-20** | Precedence | Historical docs, Brain notes, and turn requests are co-equal inputs. | `RATIFIED` |
| **DEC-20260905-19** | Namespace | Rejected `estate-*` namespaces; native plugins live in `plugins/`. | `RATIFIED` |
| **DEC-20260905-18** | Architecture| Sovereign split repo (`redtrades/agents`), detached upstream tracking. | `RATIFIED` |
| **DEC-20260905-14** | Execution | Adaptive hybrid execution: fat Makefiles + lean agent prompts. | `RATIFIED` |
| **DEC-58 (2026-09-03)** | SDLC | AISDLC contract first; deterministic exit code 0 gating. | `RATIFIED` |
| **DEC-53 (2026-08-31)** | GovCon | Staged ladder: diagnostic entry -> opportunity packet -> proposals. | `RATIFIED` |
| **DEC-10 (2026-08-31)** | Autonomy | Bounded autonomy: L1-L2 autonomous; L3-L4 gated by plans/human. | `RATIFIED` |
| **D1 (Phase 1)** | Governance | 5 critical mechanical gates in code/hooks; 15 policy docs in `docs/`. | `RATIFIED` |
| **D2 (Phase 1)** | Routing | FreeLLMAPI gateway (:3100) + local OMLX fallback chain preserved. | `RATIFIED` |
| **D3 (Phase 1)** | Tiering | Canonical taxonomy: `Quick`, `MVP`, `Standard`, `Audit`. | `RATIFIED` |
| **D4 (Phase 1)** | Review | Generator != Judge: independent cross-model review per PR. | `RATIFIED` |
| **D5 (Phase 1)** | WIP Cap | Atomic compare-and-swap locking; max 2 concurrent child worktrees. | `RATIFIED` |
| **D6 (Phase 1)** | Terminal State| GitHub Issues open/closed state is sole authority; terminate loops. | `RATIFIED` |

---

## 3. Non-Negotiable Operational Invariants (Hard Gates)

1. **Strict Anti-Slop Discipline:**
   - Zero em dashes anywhere in code, markdown documentation, commit messages, or responses (use single hyphens, colons, or parentheses).
   - Zero banned phrases: `"load-bearing"`, `"worth stating plainly"`, `"here's the honest truth"`, `"the real tension"`, `"carry the argument"`.
   - Zero sycophancy, zero conversational cheerleading.

2. **Communication Grammar:**
   - Lead with conclusion and verdict.
   - When presenting >=3 items, prefix each with standardized codes (`F1..FN`, `D1..DN`, `O1..ON`, `R1..RN`, `A1..AN`, `Q1..QN`).
   - Present architectural choices as Decision Tables with explicit `(Recommended)` indicators.

3. **Mandatory A Priori Research & Counter-Points:**
   - Automatically inspect internal research (`docs/research/`), benchmark top GitHub repositories, and surface counter-points (`CP1..CPN`) before proposing non-trivial architectures or writing code.

4. **Risk-Tiered Autonomy Ladder:**
   - **L1 (Read / Discovery):** Fully autonomous (grep, file viewing, web research, benchmarks). Zero gates.
   - **L2 (Reversible Code / Tests):** Autonomous gated by deterministic exit code 0.
   - **L3 (Structural / Swarm):** Soft gate. Implementation plan with counter-points and trade-offs required.
   - **L4 (Irreversible / Destructive):** Hard gate. Deletions, force-pushes, branch destruction, billing require explicit human approval.

5. **SDLC Queue & Worktree Isolation:**
   - GitHub Issues (`redtrades/agents`) is the sole work queue.
   - Maximum 2 concurrent child worktrees globally (`make worktree-spawn TASK=<id>`, `make worktree-clean TASK=<id>`).
   - Dirty diffs snapshot automatically to `backup/worktrees/<id>` before pruning.

6. **Date-Prefix Hygiene & State Continuity:**
   - All documents, plans, and analyses must start with an 8-digit date prefix: `YYYYMMDD-<name>.md`.
   - Maintain `TASK.md` and `CONTINUATION.md` in repository root for sub-500-token cold starts.

---

## 4. Multi-Harness Operating Matrix

All harnesses read shared instructions from `/Users/man/agents/AGENTS.md` and consume skills compiled via `make generate-all`:

| Harness | Primary Model | Operational Role | Skill Target Directory |
|---|---|---|---|
| **Google Antigravity CLI (`agy`)** | Gemini 2.5 Flash / Pro | Multi-plugin workflows, parallel subagent dispatch | `~/.gemini/antigravity-cli/plugins/` |
| **Claude Code** | Claude 3.7 Sonnet / Opus | Architectural planning, Class B reviews | `~/.claude/skills/` |
| **OpenAI Codex CLI** | GPT-5.5 / o3 | Deterministic code execution, test refactoring | `~/.codex/skills/` |
| **OpenCode** | Zen / Local | Fast terminal tool execution (<2 min tasks) | `~/.config/opencode/` |
| **Hermes / Buzz** | Gateway :3100 / Nous / OMLX | Background loops, long-running agent tasks | `~/.hermes/` |
| **Jules** | Cloud Provider | Autonomous GitHub PR worker (`jules` label) | GitHub App |

---

## 5. Phased Execution Horizons

```
┌───────────────────────────────────────────────────────────────────────────┐
│ HORIZON 1: CONSTITUTION & REPOSITORY FOUNDATION (COMPLETE)                │
│ - Single repo root at /Users/man/agents (redtrades/agents)                │
│ - AGENTS.md constitution hardened (52 lines, zero em dashes)              │
│ - Worktree manager implemented (concurrency <=2, zero-loss backups)       │
│ - GitHub Project 13 created and populated with Issues #1-#4               │
└─────────────────────────────────────┬─────────────────────────────────────┘
                                      │
                                      ▼
┌───────────────────────────────────────────────────────────────────────────┐
│ HORIZON 2: KNOWLEDGE VAULT HYGIENE & VERSIONING (COMPLETE)                │
│ - Brain vault (/Users/man/Brain) synchronized                             │
│ - 8-digit date prefix (YYYYMMDD-*) enforced across 83 Brain files         │
│ - Internal links updated and verified across all numbered packs           │
│ - Unified Intent & Master Decision Ledger consolidated                    │
└─────────────────────────────────────┬─────────────────────────────────────┘
                                      │
                                      ▼
┌───────────────────────────────────────────────────────────────────────────┐
│ HORIZON 3: HISTORIC ESTATE TRIAGE & COLD ARCHIVING (IN PROGRESS)          │
│ - Issue #2: Distill benchmark evals from agent-mesh & hooks from configs   │
│ - Issue #3: Package unneeded agent-* repos to ~/archive/                  │
│ - Issue #4: Wire Garry Tan GBrain PGLite memory for cross-session recall   │
└─────────────────────────────────────┬─────────────────────────────────────┘
                                      │
                                      ▼
┌───────────────────────────────────────────────────────────────────────────┐
│ HORIZON 4: MULTI-PROVIDER SWARM VERIFICATION & JULES ASYNC                │
│ - End-to-end canary issue verification across 5 harnesses                 │
│ - Cross-model review verification (Codex authored -> Claude reviewed)     │
│ - Jules GitHub App issue dispatch automation                              │
└─────────────────────────────────────┬─────────────────────────────────────┘
                                      │
                                      ▼
┌───────────────────────────────────────────────────────────────────────────┐
│ HORIZON 5: GOVCON PROPOSAL FACTORY ACTIVATION                             │
│ - Connect verified swarm to govcon-corpus and cmp1                        │
│ - Automated Section C/L/M shredding & compliance matrix generation        │
│ - Deliver ,000-,000/month recurring capture value                    │
└───────────────────────────────────────────────────────────────────────────┘
```
