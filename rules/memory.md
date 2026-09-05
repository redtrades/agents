---
name: memory
version: 1.0.0
status: active
provenance: native
last_updated: 2026-09-05
tier: quick
---

# GBrain Memory & Knowledge Grounding Rules

Canonical specifications for querying, updating, and grounding agent operations in Garry Tan's GBrain PGLite memory (`~/.gbrain/brain.pglite`) and the canonical brain knowledge vault (`/Users/man/agents/brain/`).

## 1. The Grounding Invariant

Agents must never guess past decisions, architectural patterns, postmortem lessons, or estate rules. Before initiating non-trivial changes, authoring specifications, or conducting research:
1. Query GBrain memory for relevant precedents, historical postmortems, and ratified decisions.
2. Verify all claims against primary source documents in `/Users/man/agents/brain/`.
3. When new facts, architectural decisions, or operational invariants are ratified, persist them back to GBrain.

## 2. When to Query GBrain

Query GBrain in the following operational scenarios:
- **Research & Investigation:** Before executing external web searches or recursive file crawling, query GBrain to inspect existing research in `brain/120-market-and-open-source-research/` and `docs/research/`.
- **Debugging & Postmortems:** When diagnosing bugs or regressions, check `brain/110-failures-postmortems-and-lessons/` for recorded failure modes and historical fixes.
- **Estate Decisions & Rules:** When validating policy, check `docs/decisions/DECISION_LOG.md` and `brain/10-intent-and-north-star/` before proposing contradictory designs.
- **Operator Context:** Look up operator preferences, machine hardware constraints (e.g. Apple Silicon M1 Max 64GB), and active life threads.

## 3. How to Invoke GBrain Across Harnesses

GBrain is accessible across all 5 agent harnesses through two standard interfaces:

### A. Model Context Protocol (MCP) Tools
When running inside Claude Code, OpenAI Codex CLI, or any MCP-enabled harness, use the lean memory tools (resident token overhead is under 300 tokens):
- `recall`: Search facts, entities, and markdown documents using hybrid/BM25 retrieval.
  - Arguments: `{"query": "<search terms>", "entity": "<optional entity>", "limit": 20}`
- `remember`: Store a durable fact or decision.
  - Arguments: `{"fact": "<claim>", "provenance": "<source/task-id>", "entity": "<optional entity>"}`
- `forget`: Expire an outdated or superseded fact by its numeric ID.
  - Arguments: `{"id": "<fact-id>"}`

### B. Shell & Makefile Automation
When running CLI tasks, shell scripts, or Makefile recipes outside MCP:
- Fast hybrid search: `/Users/man/.bun/bin/gbrain query "<terms>"`
- Raw tool invocation: `/Users/man/.bun/bin/gbrain call recall '{"query": "<terms>"}'`
- Sync brain vault: `make gbrain-sync` (or `/Users/man/.bun/bin/gbrain sync --source brain`)
- Token overhead verification: `make gbrain-check`

## 4. Two-Tier Storage Architecture

1. **Hot Memory Layer (`~/.gbrain/brain.pglite`):**
   - Embedded PostgreSQL WASM database running locally.
   - Provides sub-70ms hybrid vector and BM25 full-text indexing over 373 brain pages.
2. **Durable Knowledge Store (`/Users/man/agents/brain/`):**
   - Versioned Markdown vault with 8-digit date prefixes (`YYYYMMDD-<name>.md`).
   - Grounded claim links and git-tracked source provenance.
