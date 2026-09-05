# Canonical Estate Glossary & Taxonomy

Authoritative reference for terms, architectures, and taxonomies across the multi-harness estate.

---

## 1. Core Systems & Repositories

- **`agents` (`/Users/man/agents`):** The primary multi-harness agentic execution engine (fork `redtrades/agents` from `wshobson/agents`). Houses universal Markdown agents, skills, commands, and the consolidated `brain/` knowledge vault.
- **`Brain` (`/Users/man/agents/brain`):** The single, canonical Markdown Knowledge Vault, symlinked from `/Users/man/Brain` and `/Users/man/agent-knowledge-archive`. Houses operator intent, North Star, architecture ADRs, domain models, and post-mortems. Governed by Karpathy Wiki principles.
- **`GBrain` (`garrytan/gbrain`):** A lightweight Model Context Protocol (MCP) server built with Bun and PGLite (embedded WASM Postgres). Serves persistent operator memory and vector search over `/Users/man/agents/brain/`.
- **Historic Repositories:** Legacy implementation attempts (`agent-platform`, `agent-mesh`, `agent-workspace`, `agent-sdlc`, `agent-configs`). Slated for selective distillation and cold compression into `~/archive/`.

---

## 2. Governance & Promotion Ladder

- **Level 0 (Ephemeral Observation):** In-session reasoning, raw terminal output, and conversational exploration.
- **Level 1 (Task Checkpoint):** Operational state recorded in `TASK.md`, `CONTINUATION.md`, or snapshotted into `docs/tasks/`.
- **Level 2 (Living Rule / Operational ADR):** Project-level constraints recorded in `rules/<category>.md` or tactical choices in `docs/decisions/DECISION_LOG.md`.
- **Level 3 (Estate Canonical Knowledge):** High-level architectural records (MADRs) and permanent intent stored in `/Users/man/Brain/`.
- **Level 4 (Constitutional Core Law):** The universal, immutable rules hardcoded into root `AGENTS.md` (§0 Unbreakable Laws) governing all harnesses.

---

## 3. Autonomy & Execution Bands

- **L1 (Read / Discovery):** Grep, file viewing, web research, benchmarks. Zero gates (fully autonomous).
- **L2 (Reversible Code / Tests):** Edits, tests, bug fixes, formatting. Autonomous gated by deterministic exit code 0.
- **L3 (Structural / Swarm):** New dependencies, architectural pivots, multi-agent spawns. Soft gate: implementation plan with CPs and trade-offs required.
- **L4 (Irreversible / Destructive):** Deletions, force-pushes, branch destruction, credentials, billing. Hard gate: explicit human go-ahead required.

---

## 4. Architectural Patterns

- **SSSF (Super Simple Software Factory):** Disler architectural pattern: "Thin agents, fat recipes." Mechanical execution logic lives in deterministic `Makefile`/shell recipes; agents provide judgment. Ephemeral isolated execution with clean commit harvesting.
- **MOC (Map of Content):** Hierarchical progressive disclosure: Tier 0 Domain Index (<300 tokens resident) -> Tier 1 Category Manifest -> Tier 2 Execution Body (`SKILL.md` <8 KB loaded on demand).
- **Selective Distillation:** SOTA migration pattern (strangler fig). Extracting only verified, high-value assets and refining them to modern schemas while discarding Redundant, Obsolete, and Trivial (ROT) cruft.
- **Anti-Wholesale Ingestion Law:** Strict prohibition against recursive bulk-copying or importing legacy directories wholesale.
- **Ponytail YAGNI Ladder:** Hierarchy of implementation: Standard Unix/git tools > Established OSS packages / top GitHub repos > Minimal bespoke glue code.
- **Doubt Theater (DR139):** Anti-pattern where agents perform verification rituals without producing actionable findings or changing downstream behavior.
