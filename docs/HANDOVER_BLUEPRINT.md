# Master Handover Blueprint: The Unified Swarm Estate & Operating Contract

**Date:** 2026-09-05  
**Canonical Source of Truth:** `/Users/man/agents` (backed by GitHub `redtrades/agents`)  
**Harnesses Covered:** Claude Code, OpenAI Codex, Google Antigravity, OpenCode, Hermes, Grok, OpenHands, Pi, Jules  

---

## 1. Executive Grounding: The True Intent and North Star

Mike is a solo operator building two interconnected systems:
1. **The Economic Engine (`govcon-factory` / `govcon-corpus` / `cmp1`)**:
   - Ingests federal solicitations (SAM.gov, FAR/DFARS).
   - Produces high-margin proposal deliverables and compliance matrices.
   - Financial target: $8,000 to $10,000 monthly profit.
2. **The Autonomous Swarm (`/Users/man/agents`)**:
   - Resilient multi-agent architecture with zero single-vendor dependency.
   - Designed to survive agents dying mid-task (rate limits, context limits).
   - Delivers 95% autonomy so Mike's time is reserved for high-level planning and final sign-off.

---

## 2. The Core Operational Rules (Non-Negotiable)

1. **2-Try Circuit Breaker**:
   - If an agent attempts an action or test and fails twice, it must STOP immediately.
   - Check official documentation, search online, or inspect primary files. Never brute-force a failing approach a third time.
2. **Request Complexity Tiering (Proportional Rigor)**:
   - **Tier 1 (Quick Fix / Typo / Doc / 1-line Config)**: Direct execution (<2 minutes). Zero review cycles. No multi-agent ceremonies. No production smoke tests.
   - **Tier 2 (MVP / Local Bug Fix / Small Feature)**: Lean build, isolated slice, focused test proof (`test exit 0`), minimal diffs (<30 minutes).
   - **Tier 3 (Standard Feature / Architecture Refactor)**: Full plan, isolated worktree, deterministic test suite, cross-model review.
   - **Tier 4 (Audit / Security / Compliance / Schema)**: Multi-agent security review, strict compliance checks, human sign-off.
3. **95% Intent Certainty**:
   - Infer necessary skills based on the request.
   - If intent is underspecified, ask targeted questions with options and trade-offs until 95% certain before altering code.
4. **Structured Communication**:
   - One decision per message.
   - Options and trade-offs presented in a single line each.
   - Exactly one clear recommendation, followed by the specific ask.
   - Key actions and decisions placed at the bottom under a clear heading.
   - **Strict Anti-Slop**: Zero em dashes anywhere in messages or documents.
5. **Durable On-Disk State (Survives Context Clears and Crashes)**:
   - State lives on disk in `TASK.md` (or `task_plan.md`, `findings.md`, `progress.md`), never only in prompt context.
   - An agent must update its on-disk checkpoint after completing each phase so mid-task deaths lose zero context.
6. **Isolated Worktrees**:
   - Exactly one dedicated git worktree per active session (`git worktree add`).
   - Never run concurrent sessions in a dirty root checkout.
7. **Cross-Model Review Separation**:
   - Tier 1 and Tier 2 code requires an independent review from a different model family than the author (e.g. Claude reviewed by Codex/Grok; Codex reviewed by Claude).

---

## 3. Anti-Patterns to Strictly Avoid

- **The Monolithic Context Dump**: Do not shove hundreds of skills into the system prompt. Keep the resident prompt lean (<800 tokens). Pull domain skills from the on-disk catalog only when required.
- **Rules About Rules**: Do not write essays about governance. Enforce rules mechanically in code (`aisdlc.ts`, pre-commit hooks, deterministic exit codes).
- **Blind Worktree Deletions**: Never run uninspected `git worktree prune`. Stale worktrees may contain uncommitted work (as proven by the 29 dirty worktrees in `agent-sdlc`). Always commit dirty files to backup branches and tarball first.
- **Circular Symlinks**: Never create circular relative symlinks (e.g. `cleanup-after-work/PROVENANCE.md` loops). Use absolute or well-bounded relative paths.
- **Ghost Tasks and Rebound Loops**: Keep GitHub Issues as the single backlog authority. When an issue closes on GitHub, sync its status to Fusion (port 4040) immediately to prevent task re-opening.

---

## 4. Multi-Harness Onboarding and Roster

All skills and plugins are compiled and installed from `/Users/man/agents`:

| Agent / Harness | Model Provider / Endpoint | Role in Swarm | Installed Location |
|---|---|---|---|
| **Claude Code** | Claude 3.7 Sonnet / Opus 4.8 | Architectural planning, Tier 3/4 reviews, high-judgment engineering | `~/.claude/skills/` (286 skills linked) |
| **OpenAI Codex CLI** | GPT-5.5 / O3 | Deterministic code execution, lint/refactoring, cross-model review | `~/.codex/skills/` (288 skills linked) |
| **Google Antigravity CLI (`agy`)** | Gemini 2.5 Flash / Pro | Multi-plugin workflows, parallel subagent dispatch | `~/.gemini/antigravity-cli/plugins/` (92 plugins) |
| **OpenCode (`sst/opencode`)** | Zen / OpenRouter / Local | Fast terminal tool execution, bounded modules | `~/.config/opencode/` (490 skills and agents) |
| **Hermes / OpenHermes / Buzz** | Gateway `:3100` / Nous Free / OMLX Local (`:8300`) | Background agent execution, ACP session lifecycle | Configured via `~/.hermes/config.yaml` |
| **Grok ("Rock")** | xAI Grok / Fusion Worker `agent-035f4473` | High-speed text extraction, RFP parsing, fast review | Connected via Fusion API |
| **OpenHands** | Containerized execution | Isolated sandbox runs, repo-level repairs | Mounts `/Users/man/agents` |
| **Pi ("Pie")** | Gateway `:3100` | Lightweight terminal agent | Configured via FreeLLMAPI gateway |
| **Jules** | GitHub Cloud Agent | Autonomous cloud PRs via `jules` label, verified by `src/aisdlc.ts` | Connected via GitHub App |

---

## 5. Gateway and Local Inference Matrix

- **Port 3100 (`http://127.0.0.1:3100/v1`)**: FreeLLMAPI gateway. Single front door for free tiers (OpenRouter free, Nous free, Zen free) and paid subscriptions.
- **Port 8300 (`http://127.0.0.1:8300`)**: Local OMLX inference running Qwen on Apple Silicon. Reserved for non-time-sensitive, overnight, and batch work.
- **Port 4040 (`http://localhost:4040`)**: Fusion dual control plane and visual dependency graph.
- **Port 4200 (`http://localhost:4200`)**: Real-time AISDLC telemetry dashboard.

---

## 6. Execution Roadmap & Focus Areas

### Phase 1: Estate Decluttering (Immediate Next Step)
1. Safely archive and prune `agent-sdlc` worktrees:
   - Commit uncommitted files in the 29 dirty worktrees to `backup/worktree/*` branches.
   - Create a tarball snapshot (`agent-sdlc-fusion-worktrees-backup.tar.gz`).
   - Cleanly remove the 70 worktrees.
2. Clean broken circular symlinks in `agent-configs`.

### Phase 2: Asset Harvesting into `/Users/man/agents`
1. Move tested CLI adapters from `agent-platform/tools/adapters/` (`claude.py`, `codex.py`, `hermes.py`, `opencode.py`) into `agents/src/adapters/`.
2. Move OMLX/Qwen configs from `agent-mesh` into `agents/runtimes/omlx/`.
3. Move safety hooks from `agent-configs/hooks/` into `agents/src/hooks/`.

### Phase 3: Activating the GovCon Engine
1. Connect `/Users/man/agents` to `govcon-corpus` and `cmp1`.
2. Deploy the automated FAR/DFARS shredding pipeline and proposal starters.
