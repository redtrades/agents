# claude-agents : multi-harness agentic operating constitution

Production-ready agentic operating foundation: **100 plugins** (98 local + 2 external), **202 agents**, **225 skills**, **105 commands**. Canonical source-of-truth across Claude Code (`CLAUDE.md`), OpenAI Codex CLI, Cursor, OpenCode, and Google Antigravity CLI (`agy`).

> **Operational Constitution:** Governed by Boris Cherny ("Govern, don't inform"), Andrej Karpathy (Wiki-LLM, failure-mode guards), Garry Tan (MCP memory externalization), and OpenClaw §0 unbreakable laws. Keep <=150 lines. Detail lives in `docs/` and skills.

## Map

- **[ARCHITECTURE.md](ARCHITECTURE.md)** : top-level architectural overview (adapter framework, source-of-truth invariant, capability matrix summary)
- **[rules/README.md](rules/README.md)** : living operational rules (communication, hygiene, task-tracking, verification)
- **[docs/decisions/README.md](docs/decisions/README.md)** : architecture decision records (ADR) and operational decision log
- **[docs/skills-moc.md](docs/skills-moc.md)** : canonical skills Map of Content (225 skills by domain and difficulty tier)
- **[docs/GLOSSARY.md](docs/GLOSSARY.md)** : canonical estate glossary and taxonomy
- **[docs/architecture.md](docs/architecture.md)** : detailed design principles
- **[docs/plugins.md](docs/plugins.md)** : full plugin catalog (100 plugins by category)
- **[docs/agents.md](docs/agents.md)** : agent reference (202 agents, model tiers)
- **[docs/agent-skills.md](docs/agent-skills.md)** : skill reference (progressive disclosure model)
- **[docs/usage.md](docs/usage.md)** : commands, workflows, examples
- **[docs/authoring.md](docs/authoring.md)** : portable-content style guide (read before adding plugins)
- **[docs/harnesses.md](docs/harnesses.md)** : per-harness capability matrix
- **[docs/plugin-eval.md](docs/plugin-eval.md)** : three-layer quality evaluation framework
- **[docs/round-trip-results.md](docs/round-trip-results.md)** : real-CLI verification recipes
- **[docs/mlops.md](docs/mlops.md)** : MLOps lab pipeline (W&B, Hugging Face, model release)
- **[CONTRIBUTING.md](CONTRIBUTING.md)** : how to contribute

## Working in this repo

- Python tooling: **uv** (package manager), **ruff** (lint/format), **ty** (type check). Do not use pip / mypy / black.
- Plugins live under `plugins/<name>/` with auto-discovery. Plugin names: lowercase, hyphen-separated. Never use `__`.
- File Naming & Hygiene: All new docs, plans, analyses, and walkthroughs created by agents MUST begin with an 8-digit date prefix: `YYYYMMDD-<name>.md` (e.g., `docs/plans/20260905-plan.md`).
- Artifact Persistence: Plans and walkthroughs must be committed to `docs/plans/` and `docs/walkthroughs/`, never left only in ephemeral memory.
- 2-Try Circuit Breaker: If an action or test fails twice, STOP immediately. Consult documentation or web search; never guess.
- Continuation Protocol: Maintain `CONTINUATION.md` in the repository root. After every step, commit diffs incrementally. On session reset, rate limit, or quota cutoff, incoming agents read `CONTINUATION.md` and resume in <500 tokens without re-ingesting conversation history.
- Proportional Rigor: Tier 1 (quick fix/doc/config) executes directly (<2 min) with no reviews or smoke tests; Tier 2 (MVP) tests focused diffs; Tier 3/4 require formal plans and cross-model review.
- Strict Anti-Slop: Zero em dashes anywhere in code, docs, or messages.
- Never commit secrets. Never run destructive git (force-push, `reset --hard`, branch -D) without explicit ask.

## Universal agent contract (OpenClaw §0 + Karpathy + Boris + Disler Principles)

### Non-negotiable operating invariants (Hard Gates)

- **Risk-Tiered Autonomy Ladder:**
  - *L1 (Read / Discovery):* Grep, file viewing, web research, benchmarks. Zero gates (fully autonomous).
  - *L2 (Reversible Code / Tests):* Edits, tests, bug fixes, formatting. Autonomous gated by deterministic exit code 0.
  - *L3 (Structural / Swarm):* New dependencies, architectural pivots, multi-agent spawns. Soft gate: implementation plan with CPs and trade-offs required.
  - *L4 (Irreversible / Destructive):* Deletions, force-pushes, branch destruction, credentials, billing. Hard gate: explicit human go-ahead required.
- **Anti-Wholesale Ingestion Law:** Zero bulk copying or recursive migration of legacy folders (`agent-*`). Every promoted asset must pass selective distillation: proof of necessity, elimination of redundant/obsolete/trivial (ROT) cruft, and alignment with modern schemas.
- **Strict Anti-Slop:** Zero em dashes anywhere in code, docs, commit messages, or responses. Use single hyphens, colons, or parentheses.
- **Safety & Secret Preservation:** Never commit secrets. Never run destructive git commands (force-push, `reset --hard`, branch -D) without explicit authorization.

### Distilled operational guidance (Best Practice Principles)

- **Skill-First Discipline & JIT Discovery:** Inspect user request keywords and difficulty tier against `docs/skills-moc.md`. Load matching skill via `view_file` (<8 KB) before acting. Announce `Using [skill] for [purpose]`.
- **Search Before Asserting:** Live search fast-moving tech, runtimes, and models. Check live runtime state over disk files (`verify-before-asserting`).
- **Advisory Balance Precedence:** Treat historical documents, brain notes, and current turn instructions as co-equal advisory inputs, reconciling discrepancies dynamically (`DEC-20260905-20`).
- **Selective Swarm & Cost Routing:** Maximize free-tier cloud models (Gemini Flash, Groq) and Jules async cloud execution; reserve frontier subscriptions (Claude Max, Codex CLI) for interactive synthesis; run local M16 models for non-time-bound long runs (`DEC-20260905-21`).
- **Thin Agents, Fat Recipes (SSSF):** Standard Makefile recipes and native CLI commands hold execution mechanics; agents hold adaptive judgment. Avoid bespoke subprocess daemons (`DEC-20260905-14`).
- **A Priori Research & Pushback:** Research first principles and top repositories before proposing architectures. Surface counter-points (`CP1..CPN`) with clear trade-offs and explicit recommendations.
- **Ask Until 95% Certain:** Surface genuine ambiguities early with structured options; never pick an unverified assumption on structural choices.
- **Ponytail YAGNI Ladder:** Standard tools > installed packages > minimal bespoke code. Surgical edits only; avoid orthogonal damage to adjacent working code.
- **Scope Containment & Parked Backlog:** Deliver requested scope without unasked feature creep. Route side ideas to the parked backlog in `TASK.md` without derailing in-flight work.
- **Deterministic Proof of Work:** Verify completion via deterministic test assertions and exit code 0; avoid doubt theater.
- **Caveman Brevity & Compounding Loop:** High-density telegraphic style (65-75% token reduction); write-back post-task lessons and fixes into skills/rules to prevent regression (`EveryInc` loop).
- **Progressive Disclosure (Map of Content):** Conserve context tokens (<300 resident prompt); load detailed skill bodies and documentation on demand.
- **State Continuity:** Maintain `TASK.md` and `CONTINUATION.md` after atomic changes to ensure sub-500 token cold resumes across sessions.

## Quality gates (run these before pushing)

```bash
make validate STRICT=1     # structural validation across all harness outputs
make garden                # drift detection (dead links, stale artifacts, oversize skills)
make test                  # full pytest suite (plugin-eval + tools/tests/)
make smoke-test            # real-CLI subprocess tests against generated artifacts
```

CI (`.github/workflows/validate.yml`) runs all four on every PR plus installs OpenCode + Antigravity CLI for live verification.

## Regenerating per-harness artifacts

```bash
make generate HARNESS=codex        # .codex/skills, .codex/agents, .codex/plugins/<p>/, .agents/plugins/marketplace.json
make generate HARNESS=cursor       # .cursor-plugin/{marketplace,plugin}.json, .cursor/rules/
make generate HARNESS=opencode     # .opencode/{skills,agents,commands,plugins}/, opencode.json
make generate HARNESS=antigravity  # .antigravity/plugins/<p>/
make generate-all                  # all four
```

The small per-harness registries are **committed** so each harness installs natively from a clone / GitHub URL (native-install commands in [`docs/harnesses.md`](docs/harnesses.md)). The transformed skill and agent trees under `.codex/`, `.opencode/`, `.copilot/` and `.antigravity/` stay gitignored and are rebuilt locally. Run `make generate-all` before committing source changes : it also prunes artifacts whose source was removed; CI fails on drift. Source-of-truth lives only under `plugins/`; never hand-edit generated files.

## Skills (cross-harness)

225 skills under `plugins/*/skills/<n>/SKILL.md` : discoverable by every harness:

- **Claude Code**: auto-discovery via Anthropic's SKILL.md spec
- **Codex CLI**: mirrored to `.codex/skills/<plugin>__<skill>/` (8 KB body cap; detail in `references/details.md`)
- **OpenCode**: mirrored to `.opencode/skills/<plugin>-<skill>/` using hyphenated names for global install
- **Cursor**: reads `.claude/skills/` directly (no re-emit)
- **Antigravity CLI**: native plugins at `.antigravity/plugins/<p>/` : bare `skills/<skill>/SKILL.md` (no `<plugin>__` namespacing; the plugin dir already scopes it)
- **Skills-only installers**: `gh skill install wshobson/agents` and `npx skills add wshobson/agents` read `plugins/*/skills/` from GitHub directly (see `docs/harnesses.md`); `make smoke-test` runs both plus the agentskills.io spec check

## Subagents (cross-harness)

202 subagents under `plugins/*/agents/<name>.md`. Per-harness transpilation:

- **Codex**: `.codex/agents/<plugin>__<agent>.toml` (drop `tools:`, map model alias to the GPT-5.x family, infer `sandbox_mode`)
- **OpenCode**: `.opencode/agents/<plugin>__<agent>.md` with `mode: subagent` + `permission:` block (locked agents : those with source `tools: []` : get deny-everything except base `skill`/`task`)
- **Antigravity CLI**: `.antigravity/plugins/<p>/agents/<agent>.md` (Markdown + YAML frontmatter, `model:` is a tier alias : `inherit`/`flash`/`pro`); TOML commands at `commands/<p>/<cmd>.toml` (agy reports these as "converted to skills"); global install via `make install-antigravity` symlinks each plugin into `~/.gemini/antigravity-cli/plugins/`
- **Cursor**: reads `.claude/agents/` directly

## Why this file is short

Per OpenAI's harness-engineering practice: this file is a **map**, not an encyclopedia. Procedural detail lives in skills (loaded on demand by agents). Reference material lives in `docs/` (loaded when an agent navigates). A single bloated AGENTS.md crowds out the task, rots quickly, and is hard to verify mechanically. Keep it lean; push detail elsewhere.
