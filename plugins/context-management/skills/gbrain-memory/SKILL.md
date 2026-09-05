---
name: gbrain-memory
description: Query and update Garry Tan GBrain PGLite WASM memory and canonical estate knowledge. Use when searching for documents or prior research, recalling past architectural decisions, looking up postmortems, or storing durable entity facts across sessions.
---

# GBrain Memory Skill

Retrieve and persist estate memory across sessions using Garry Tan's GBrain PGLite WASM engine and the canonical brain knowledge vault.

## When to Use This Skill

- Searching for prior research, architectural decisions, postmortems, or estate documents.
- Verifying whether a proposed pattern has already been ratified or rejected in `DECISION_LOG.md`.
- Looking up operator preferences, machine hardware specifications, and system history.
- Saving new durable decisions, architectural invariants, or postmortem lessons into memory.

## 1. Fast Retrieval Patterns

### A. Via MCP Tool (`recall`)
In Claude Code, OpenAI Codex, or Antigravity with MCP enabled:
```json
{
  "name": "recall",
  "arguments": {
    "query": "sovereign estate architecture",
    "limit": 5
  }
}
```
To retrieve entity-scoped facts:
```json
{
  "name": "recall",
  "arguments": {
    "entity": "m1-max-roofline"
  }
}
```

### B. Via Shell Command
When executing commands directly in terminal or subagent:
```bash
/Users/man/.bun/bin/gbrain query "sovereign estate architecture"
```
Or invoking the raw JSON-RPC verb:
```bash
/Users/man/.bun/bin/gbrain call recall '{"query": "sovereign estate architecture", "limit": 5}'
```

## 2. Memory Persistence Patterns

### A. Via MCP Tool (`remember`)
When a decision, architectural invariant, or critical failure lesson is ratified:
```json
{
  "name": "remember",
  "arguments": {
    "fact": "All new markdown documents must begin with an 8-digit date prefix YYYYMMDD-<name>.md.",
    "provenance": "AGENTS.md Section 2",
    "entity": "hygiene"
  }
}
```

### B. Expiring Outdated Facts (`forget`)
When a policy or fact is superseded:
```json
{
  "name": "forget",
  "arguments": {
    "id": "14"
  }
}
```

## 3. Maintenance & Syncing

When new documents are added or edited in `/Users/man/agents/brain/`:
```bash
make gbrain-sync
```
To verify that the resident prompt token overhead stays under the 800-token limit:
```bash
make gbrain-check
```
