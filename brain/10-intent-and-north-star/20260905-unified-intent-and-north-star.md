# Unified Intent & North Star: The Sovereign Solo-Operator Operating System

**Date:** 2026-09-05  
**Status:** PROPOSED (Draft Pending One-by-One Operator Ratification)  
**Authority:** Candidate Intent Synthesis for `/Users/man/agents` and `/Users/man/Brain`  
**Supercedes:** Historical positions in `CURRENT-HISTORICAL-SYNTHESIS.md` and fragmented legacy roadmaps.

---

## 1. The Core Purpose: Sovereign Solo-Operator Enterprise OS

The irreducibly simple objective of this estate is to operate as a **Sovereign Solo-Operator Enterprise Operating System** (Terraform for Swarms and Companies):

> A system that defines, instantiates, operates, evaluates, improves, and retires agent-run initiatives and projects, while one person (Mike) directs goals, budgets, policy, and exceptions.

### The Two Interlocking Engines:
1. **The Commercial Revenue Engine (Value Delivery):**
   - Anchored in the GovCon capture and proposal factory (`cmp1` / `govcon-corpus`).
   - Deliverable: High-scoring, compliant federal proposals generating **$8,000 to $10,000/month recurring net profit**.
   - Pipeline: 1M token free ingestion (Gemini 2.5 Flash) -> local privacy-preserving compliance shredding (Qwen 2.5 Coder 14B on Apple Silicon) -> high-judgment proposal drafting (Claude Code) -> deterministic compliance verification (`pytest`).
2. **The Self-Improving Machine (Sovereign Foundation):**
   - Centered in `/Users/man/agents` (`redtrades/agents`).
   - Governed by an immutable constitution (`AGENTS.md`), 4 distilled living rules (`rules/`), and an authoritative glossary (`docs/GLOSSARY.md`).
   - Builds, tests, evaluates, and refines capabilities with zero custom wrapper bloat.

---

## 2. Ratified Operating Invariants (Sep 5, 2026)

All agents operating across harnesses (`claude`, `codex`, `opencode`, `cursor`, `agy`) must adhere to these foundational principles:

### A. Single Source of Truth
- **Code & Tooling:** Centralized in `/Users/man/agents` (`git@github.com:redtrades/agents.git`).
- **Clean Fork Split:** Upstream `wshobson/agents` is retained solely as a dormant remote alias for quarterly diff checks. Proprietary estate assets live in dedicated namespaces (`plugins/estate-*`) with `provenance: estate-native`.
- **Knowledge Vault:** Centralized in `/Users/man/Brain` (the single canonical knowledge archive).

### B. Risk-Tiered Autonomy Ladder
- **L1 (Read / Discovery):** Fully autonomous (grep, search, file view, benchmarks). Zero gates.
- **L2 (Reversible Code / Tests):** Autonomous gated by deterministic verification (exit code 0).
- **L3 (Structural / Swarm):** Soft gate. Implementation plan with counter-points (`CP1..CPN`) and trade-offs required before execution.
- **L4 (Irreversible / Destructive):** Hard gate. Deletions, force-pushes, branch destruction, billing, or credentials require explicit human go-ahead.

### C. Anti-Wholesale Ingestion Law
- Zero bulk copying or recursive migration of legacy folders (`agent-*`).
- Every promoted asset must pass selective distillation: proof of necessity, elimination of redundant/obsolete/trivial (ROT) cruft, and alignment with modern schemas.

### D. Ponytail YAGNI Ladder & Disler SSSF Principles
- Standard OS/CLI tools > top installed packages / OSS libraries > minimal bespoke glue code.
- Thin agents, fat recipes: Execution mechanics live in standard Makefiles and shell scripts; agents provide judgment, error diagnosis, and parameter tuning.
- Zero custom Python wrappers for CLI harnesses.

### E. Zero-Amnesia State Continuity (`CONTINUATION.md`)
- Work is committed incrementally to Git before handoff (`git log -n 5 --oneline` is the event ledger).
- Every agent maintains `TASK.md` and `CONTINUATION.md` in repository root.
- Cold resumes take under 2 seconds and consume <500 tokens (`git diff HEAD~1`).

### F. 5-State Decision Lifecycle
- Decisions flow through: `PROPOSED`, `RATIFIED`, `SUPERSEDED`, `STALE`, and `REJECTED`.
- Only `RATIFIED` decisions (confirmed by Mike) govern agent behavior. Unconfirmed ideas remain `PROPOSED`.
- Superseded decisions point explicitly to successor IDs.

### G. Strict Anti-Slop
- Zero em dashes anywhere in code, documentation, commit messages, or responses. Use single hyphens, colons, or parentheses.

---

## 3. Estate Roadmap & Execution Horizons

```
+-----------------------------------------------------------------------------+
| HORIZON 1: Constitutional Foundation & Governance (COMPLETE)                |
| - Single repo root at /Users/man/agents                                     |
| - Pruned 2,760 lines of custom Python adapters in src/adapters/             |
| - Codified AGENTS.md (invariants + guidance, <=150 lines, zero em dashes)   |
| - Established docs/GLOSSARY.md, rules/, and docs/decisions/DECISION_LOG.md   |
| - Compiled SOTA Patterns & Anti-Patterns Catalog                            |
+-------------------------------------+---------------------------------------+
                                      |
                                      v
+-----------------------------------------------------------------------------+
| HORIZON 2: Knowledge Grounding & Estate Isolation (ACTIVE)                  |
| - Brain vault established at /Users/man/Brain (zero legacy symlink cruft)   |
| - Ratify 20260905-unified-intent-and-north-star.md in Brain                 |
| - Clean split from upstream fork (dormant remote alias for quarterly diffs) |
| - Establish plugins/estate-* namespaces for proprietary estate skills       |
+-------------------------------------+---------------------------------------+
                                      |
                                      v
+-----------------------------------------------------------------------------+
| HORIZON 3: Selective Asset Extraction & Cold Archiving                      |
| - Review candidate tools (agent-mesh/evals, agent-configs/hooks) via SDLC   |
| - Harvest verified high-leverage assets into plugins/estate-*               |
| - Package and move historic agent-* folders into ~/archive/                 |
| - Clean up user home directory and iCloud Drive                             |
+-------------------------------------+---------------------------------------+
                                      |
                                      v
+-----------------------------------------------------------------------------+
| HORIZON 4: GovCon Proposal Factory & Revenue Acceleration                   |
| - Wire RFP solicitation shredder (Gemini Flash 1M context free tier)        |
| - Wire local FAR/DFARS compliance extractor (local Qwen 14B on Apple Silicon)|
| - Automate technical volume drafting and static pytest verification         |
| - Deliver $8k to $10k/month recurring capture revenue                       |
+-----------------------------------------------------------------------------+
```

---

## 4. Grounding Principles for Successor Agents

1. **Do Not Re-Litigate Settled Decisions:** Consult `docs/decisions/DECISION_LOG.md`. If a decision is `RATIFIED`, execute within its boundaries.
2. **Do Not Ingest Wholesale:** If instructed to inspect or bring in legacy work, perform zero-token mechanical triage first. Extract only what is necessary and verified.
3. **Keep Residents Lean:** Keep resident prompts under 800 tokens via 3-Tier Map of Content progressive disclosure. Load skill bodies on demand.
4. **Tether Code to Value:** Every automated tool must serve either sovereign system governance or the GovCon revenue pipeline.
