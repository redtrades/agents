---
name: declarative-governance-and-promotion-architecture
version: 1.1.0
status: accepted
date: 2026-09-05
deciders: Mike, Antigravity
tier: audit
supersedes: []
superseded_by: []
---

# ADR 0001: Declarative Governance, Instruction Promotion, and Unified Versioning

## Context & Problem Statement

The multi-agent engineering estate historically suffered from recursive failure modes:
1. **Instruction Amnesia**: User steering and architectural choices in chat were applied as one-off actions, but were lost across context window compactions.
2. **Wholesale Copying Trap**: Past attempts to preserve rules dumped dozens of uncurated legacy files wholesale, reintroducing dead issue pointers, defunct repositories (`agent-sdlc`), and circular rules.
3. **Plan-Execution Disconnect (Infinite Re-Planning Loops)**: Agents repeatedly drafted long Markdown plans without tying them to an actionable, execution-tethered state machine, causing successor agents to re-plan instead of executing.
4. **Sycophantic Ad-Hoc Tooling**: Prematurely building custom logging layers (like bespoke JSONL ledgers or Python RPC wrappers) when native tools (Git, Markdown) already solve the problem.
5. **Rigid Turn Limits**: Flat iteration caps either strangle complex autonomous workflows (like `/goal` or multi-gate refactors) or provide too much leash for trivial fixes.

## Decision Drivers

- Establish a single, authoritative, clean-slate foundation centered on `/Users/man/agents`.
- Eliminate agent amnesia by tethering plans directly to Git-backed state files (`TASK.md` and `CONTINUATION.md`).
- Avoid reinventing the wheel: Git is the immutable event ledger; do not invent parallel JSONL log files.
- Standardize declarative metadata and versioning across all skills, rules, and decision records.
- Scale turn limits adaptively based on task complexity tiers with cadenced checkpointing.
- Ensure automated, self-healing documentation synchronization via `make garden` and `make catalog`.

## Ratified Decisions

1. **Single Source of Truth**: `/Users/man/agents` (fork `redtrades/agents`) is the sole canonical repository for all 92 plugins, 184 skills, and 202 agents. Historical archives reside in `/Users/man/Brain` (read-only evidence).
2. **The 5-Level Decision Promotion Ladder**:
   - Level 1: Ephemeral chat dialogue and scratch.
   - Level 2: In-flight task recovery spine (`TASK.md` and `CONTINUATION.md`).
   - Level 3: Architecture Decision Records (`docs/decisions/*.md`).
   - Level 4: Core operating contract (`AGENTS.md`) and distilled living rules (`rules/*.md`).
   - Level 5: Frozen historical canon (`/Users/man/Brain`).
3. **Declarative Metadata Schema**:
   All skills, rules, and ADRs must contain structured YAML frontmatter (`name`, `version`, `status`, `provenance`, `last_updated`, `tier`).
4. **Execution-Tethered Planning & Complexity-Tiered Turn Ceilings**:
   - Plans compile directly into checklist items in `TASK.md` with deterministic exit conditions (command exit code 0).
   - Git commits (`git log`) serve as the immutable event ledger. Completed items are bound to commit SHAs and locked against re-planning.
   - Turn ceilings adapt to complexity tier:
     - Tier 1 (Quick): 5 turns, $0.10 cap.
     - Tier 2 (MVP): 25 turns, $2.00 cap.
     - Tier 3 (Standard): 50 turns, $5.00 cap (checkpoint every 20 turns).
     - Tier 4 (Audit / Goal): 100 turns, $10.00 cap (checkpoint every 25 turns).
5. **Universal Agent Contract in AGENTS.md**:
   Every harness at cold start is bound by: mandatory a priori research, ask until 95% certain, objective engineering over sycophancy, reference-point coding, decision tables with recommendations, zero em dashes, and backlog isolation.

## Consequences & Trade-offs

- **Positive**:
  - Eliminates parallel logging infrastructure: Git log and `TASK.md` provide 100% of the audit trail with zero JSON formatting failures.
  - Complex autonomous workflows (`/goal`) have sufficient headroom (up to 100 turns) while remaining safe via cadenced checkpointing every 25 turns.
  - Context resets resume in <500 tokens without transcript re-ingestion.
  - Automated drift detection via `make garden` flags dead links, missing metadata, and conflicting decisions.
- **Negative / Constraints**:
  - Every architectural choice requires registering an ADR rather than leaving conversational notes.
  - Long-running workflows must strictly checkpoint to `CONTINUATION.md` at cadence.
