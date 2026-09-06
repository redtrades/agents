# Hermes Progressive Disclosure & GBrain Memory Integration

**Date:** 2026-09-05  
**Status:** RATIFIED & OPERATIONAL  
**Target:** `~/.hermes/config.yaml`  

## 1. Context & Architecture

Hermes serves as the sovereign local model router and autonomous harness on Apple Silicon M1 Max. Prior to this integration:
1. `mcp_servers` was empty, leaving Hermes detached from Garry Tan GBrain PGLite memory (`~/.gbrain/brain.pglite`).
2. Skills were disabled in `agent.disabled_toolsets: [skills]`, preventing access to the 226 native skills.
3. `skills.external_dirs` was empty, creating isolation between Hermes and `/Users/man/agents/plugins`.

## 2. Implemented Configuration

In `~/.hermes/config.yaml`:

```yaml
agent:
  disabled_toolsets:
    - kanban
  reasoning_effort: medium

mcp_servers:
  gbrain:
    command: python3
    args:
      - /Users/man/agents/tools/gbrain_mcp.py
    env:
      GBRAIN_HOME: /Users/man
    connect_timeout: 30
    enabled: true

platform_toolsets:
  cli:
    - file
    - terminal
    - search
    - todo
    - clarify
    - skills

skills:
  external_dirs:
    - /Users/man/agents/plugins
```

## 3. Deterministic Verification

1. **MCP Connectivity & Tool Discovery:**
   - Command: `hermes mcp test gbrain`
   - Verdict: `✓ Connected (1105ms)`
   - Discovered Tools: `recall`, `remember`, `forget` (3 tools, 2,551 bytes schema, 286 tokens overhead)

2. **Native Skills Indexing:**
   - Discovered External Skills: 229 native skills indexed via `_build_external_skill_index()`.
   - Verified Presences: `gbrain-memory` (True), `investigate-first` (True), `research` (True), `writing-plans` (True).

3. **Progressive Disclosure Enforcement:**
   - Skills index overhead is strictly progressive: metadata only during scan, full instruction bodies loaded dynamically via `skill_view`.
