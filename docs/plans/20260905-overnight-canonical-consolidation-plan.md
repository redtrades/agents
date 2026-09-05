# Autonomous Overnight Execution Plan: Canonical Consolidation & Non-Destructive Estate Organization

**Date:** 2026-09-05
**Author / Orchestrator:** Antigravity (Solo Operator Mike offline / sleeping)
**Safety Guardrails:** Zero destructive git operations, zero deletion of models or active configs, zero data loss.
**Usage Optimization:** Maximum reliance on free tiers (Google Gemini 1M context, FreeLLMAPI, local inference, Claude Haiku 4.5 via OAuth subscription) preserving session headroom.

---

## 1. Objectives & North Star

Transform the scattered estate into an organized, self-healing, declarative multi-agent foundation centered on `/Users/man/agents`:
1. **Preserve Qwen 3.8 Flash Next & Enable SSD KV Cache:** Re-link `llama_ssd_cache_lifecycle.py` on port 8318 to `/opt/homebrew/bin/llama-server` so Qwen 3.8 Flash functions with its SSD KV cache without deleting any model weights.
2. **Standardize Cross-Harness Configuration (`AGENTS.md`):** Ensure all harnesses (Claude Code, Codex, OpenCode, Buzz, Hermes) read canonical instructions from `/Users/man/agents/AGENTS.md` and enforce the `CONTINUATION.md` zero-loss handoff protocol.
3. **Eliminate Prompt Bloat:** Restructure Hermes and Buzz skill directories to use progressive disclosure pointers rather than loading 250+ full skill files into resident context, restoring 90%+ prompt cache hit rates.
4. **Establish the Canonical Brain Archive (`/Users/man/Brain`):** Create the `/Users/man/Brain` non-destructive symlink pointing to `/Users/man/agent-knowledge-archive` and initialize the Karpathy Wiki structure (`wiki/MOC_INDEX.md`, `wiki/GOVCON_MOC.md`, `wiki/SWARM_MOC.md`).
5. **Organize Estate Documentation with 8-Digit Date Prefixes:** Catalog, sort, and date-prefix unstructured documentation across repositories without destroying legacy work.
6. **GovCon Capture Engine Preparation:** Stage the FAR/DFARS compliance matrices and solicitation templates in `Brain/wiki/govcon/` ready for Gemini 1M ingestion and local Qwen shredding.

---

## 2. Phase-by-Phase Execution Plan

### Phase 1: Local Inference Repair (Qwen 3.8 Flash SSD KV Cache)
- **Action:** Update `/Users/man/.config/agent-mesh/llama-lifecycle.json`:
  - Point `child_argv[0]` to `/opt/homebrew/bin/llama-server`.
  - Update `expected_child_sha256` to match `/opt/homebrew/bin/llama-server`.
- **Verification:** Restart lifecycle daemon on port 8318 and send test completion to `http://127.0.0.1:8318/v1/chat/completions`. Verify SSD KV cache slot initialization.
- **Safety:** Do not delete `/Users/man/models/qwen38-flash-next/`.

### Phase 2: Cross-Harness Standardization & Prompt Optimization
- **Action:**
  - Link `~/.buzz/AGENTS.md` and `~/.hermes/AGENTS.md` to `/Users/man/agents/AGENTS.md`.
  - In `~/.hermes/config.yaml`, ensure `skills` are loaded via progressive disclosure on-demand rather than bulk-loading 255 skills into the base prompt.
  - Verify Claude CLI config defaults to `haiku` (Claude Haiku 4.5 via OAuth subscription).
- **Verification:** Run `hermes -z "ping" < /dev/null` and `claude -p "ping" --model haiku < /dev/null`. Check prompt token counts to ensure base prompts remain sub-800 tokens.

### Phase 3: Canonical Brain Symlink & Karpathy Wiki Architecture
- **Action:**
  - Create symlink: `/Users/man/Brain` -> `/Users/man/agent-knowledge-archive`.
  - Establish `Brain/wiki/` directory with:
    - `MOC_INDEX.md`: Top-level Map of Content linking to all estate domains.
    - `SWARM_MOC.md`: Architecture, harnesses, protocols, and control planes.
    - `GOVCON_MOC.md`: FAR/DFARS shredding, solicitation templates, and proposal volumes.
    - `DECISIONS_MOC.md`: Ratified MADR decision records.
- **Verification:** Confirm Obsidian vault can open `/Users/man/Brain` and resolve `[[wikilinks]]`.

### Phase 4: Non-Destructive Estate Documentation Sorting
- **Action:**
  - Scan loose notes in `agent-platform`, `agent-mesh`, and `agent-sdlc`.
  - Create date-prefixed mirrors (`YYYYMMDD-<name>.md`) under `Brain/wiki/` or `agents/docs/`.
  - Leave originals intact; mark deprecated files with header breadcrumb pointers to the canonical version.
- **Verification:** Run `make garden` in `/Users/man/agents` to verify zero broken links.

### Phase 5: GovCon Capture Engine Staging
- **Action:**
  - Connect `govcon-corpus` and `cmp1` references into `Brain/wiki/govcon/`.
  - Create the automated FAR/DFARS shredding prompt template optimized for Gemini 2.5 Flash (1M free context) and local Qwen inference.
- **Verification:** Validate that no private client proposal data is committed to public or shared git remotes.

---

## 3. Verification & Acceptance Criteria

1. `curl http://127.0.0.1:8318/v1/chat/completions` returns valid completions from Qwen 3.8 Flash.
2. `claude -p "ping" --model haiku < /dev/null` executes via OAuth subscription in <2s.
3. `ls -l /Users/man/Brain` confirms active symlink to `/Users/man/agent-knowledge-archive`.
4. `make validate STRICT=1` and `npm test` exit 0 in `/Users/man/agents`.
5. `CONTINUATION.md` in `/Users/man/agents` is updated after every atomic step.
