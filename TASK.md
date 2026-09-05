# Task Tracking: Swarm Unification & Clean Estate Architecture

## Goal
Establish a unified, zero-bloat multi-agent foundation centered on `/Users/man/agents` (fork `redtrades/agents`), install all cross-harness skills across Claude Code, Codex, OpenCode, and Antigravity, and safely declutter the estate without code loss.

## Next Step
Execute the Zero-Loss Worktree Backup and Pruning procedure in `/Users/man/agent-sdlc` (commit dirty changes in 29 worktrees to `backup/worktree/*` branches, create compressed tarball archive, then prune the 70 worktrees).

## Current Phase
Phase 2: Estate Decluttering & Zero-Loss Worktree Pruning

## Status
- **Phase 1: Multi-Harness Skill Installation & Validation**: COMPLETE
  - Generated artifacts for 5 harnesses (`make generate-all`).
  - Antigravity CLI: 92 plugins linked into `~/.gemini/antigravity-cli/plugins/`.
  - OpenCode: 490 skills and agents linked into `~/.config/opencode/`.
  - OpenAI Codex CLI: 288 skills linked into `~/.codex/skills/`.
  - Claude Code: 286 skills linked into `~/.claude/skills/` (103 estate + 183 marketplace).
  - Validation: `make validate STRICT=1` (exit 0), `npm test` 11/11 passing (exit 0).
- **Phase 2: Safe Worktree Pruning in agent-sdlc**: IN_PROGRESS
- **Phase 3: Circular Symlink & Estate Cleanup**: PENDING
- **Phase 4: Selective Harvesting (CLI Adapters & OMLX)**: PENDING
- **Phase 5: GovCon Pipeline Activation**: PENDING

## Evidence & Verification
- `make validate STRICT=1`: OK across 5 harnesses.
- `npm test`: 11/11 AISDLC governance tests pass.
- `git status`: working tree clean on `main` at `582de5e`.
