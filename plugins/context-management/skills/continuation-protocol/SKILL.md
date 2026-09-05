---
name: continuation-protocol
description: Enforces the CONTINUATION.md protocol for zero-loss agent task handoffs, incremental git checkpointing, and sub-500 token resumption upon token exhaustion or rate limits.
---

# Continuation Protocol Skill

## Purpose

When an AI agent runs out of tokens, reaches an API quota cap, or hits HTTP 429, conversational memory is severed. Without a strict handoff protocol, the next agent restarts from scratch, re-ingests files, and burns millions of tokens without making progress.

This skill enforces continuous state externalization so that any agent can stop at any second and an incoming agent can resume in under two seconds for less than 500 tokens.

---

## The 3 Invariants

1. **Never Leave Dirty Files in Working Tree:**
   Every verified code change or tool action must be committed locally to git (`wip/issue-<id>`). If a session crashes, git contains the exact source of truth.
2. **Always Update `CONTINUATION.md` Before Calling Tools:**
   Maintain a concise 50-line machine-readable file in the repository root (`CONTINUATION.md`).
3. **Cold-Start Resume Under 500 Tokens:**
   An incoming agent must NEVER re-read the entire conversation history. It reads ONLY `CONTINUATION.md` and runs `git diff HEAD~1`.

---

## Required Schema for `CONTINUATION.md`

```markdown
# Task Continuation State

**Task ID:** <TASK_ID>
**Goal:** <Concise single-sentence goal>
**Timestamp:** <ISO_8601_TIMESTAMP>
**Branch:** <git_branch> (commit: <HEAD_SHA>)

---

## 1. Active Phase & Status
- **Current Phase:** <Phase name>
- **Overall Status:** In Progress | Blocked | Complete

---

## 2. Completed Steps (Machine-Verified)
1. **<Step 1 Name>:** <Summary of what was verified> (Commit: `<SHA>`).
2. **<Step 2 Name>:** <Summary of what was verified> (Commit: `<SHA>`).

---

## 3. Active Step (In Progress)
- **Step Name:** <Current step being executed>
- **Target:** <Exact expected outcome of this step>

---

## 4. Modified & Created Files
- `<file_path_1>`
- `<file_path_2>`

---

## 5. Next Immediate Actions
1. `<Exact shell command to run>`
2. `<Next verification test to execute>`
```

---

## Execution Rules for Agents

- **Step A:** When starting a session, inspect the repository root for `CONTINUATION.md`. If it exists, read it first.
- **Step B:** Run `git status` and `git diff HEAD~1` to confirm file reality matches `CONTINUATION.md`.
- **Step C:** Execute the command specified in `Next Immediate Actions`.
- **Step D:** Upon completing or altering any step, overwrite `CONTINUATION.md` with updated progress before ending your turn.
