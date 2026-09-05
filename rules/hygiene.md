---
name: hygiene
version: 1.0.0
status: active
provenance: native
last_updated: 2026-09-05
tier: quick
---

# Workspace & Repository Hygiene Rules

Canonical specifications for ephemeral worktree management, file naming standards, secret preservation, and anti-slop formatting.

## 1. Concurrency Controls & WIP Limits

To prevent workspace sprawl and resource starvation on Apple Silicon:
- **Per-Agent Limit**: An agent may hold exactly 1 active task at a time.
- **Global Estate Limit**: Maximum 2 active concurrent working trees globally across the machine.
- **Backpressure**: If carrying capacity is reached, queue incoming tasks in the Parked Backlog until active work merges or checkpoints.

## 2. Ephemeral Worktree Protocol & Zero Data Loss

When working in isolated branches or multi-file refactors:
- **Provisioning**: Create isolated worktrees under `work/<task-id>` or `.worktrees/<task-id>`. Never run concurrent multi-file edits in the primary checkout.
- **Zero-Loss Pruning**: Before removing or pruning any worktree, all dirty or uncommitted files MUST be committed to a dedicated backup branch (`backup/worktrees/<task-id>`).
- **Terminal Cleanup**: Once diffs are backed up and merged, cleanly remove the worktree with `git worktree remove` to prevent disk bloat.

## 3. Date-Prefixed File Naming Standard

All persistent markdown documentation created by agents MUST begin with an 8-digit date prefix:
- Format: `YYYYMMDD-<name>.md` (e.g., `docs/plans/20260905-plan.md`, `docs/decisions/20260905-0001-adr.md`).
- Target Directories:
  - Plans: `docs/plans/`
  - Walkthroughs: `docs/walkthroughs/`
  - Decisions: `docs/decisions/`
  - Research: `docs/research/`

Never leave plans or findings only in ephemeral memory or IDE scratch directories.

## 4. Strict Anti-Slop Discipline

- **Zero Em Dashes**: Do not use em dashes anywhere in code, markdown, commit messages, or chat responses. Use single hyphens or colons only.
- **No Circular Symlinks**: Symlinks must point directly to absolute or relative canonical paths; never create chained or circular links.
- **Secrets & Credentials**: Never commit `.env` files, API keys, private tokens, or client proprietary data. Use environment variables or local keychain injection.
