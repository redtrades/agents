# claude-agents : multi-harness agentic operating constitution

Production-ready agentic operating foundation: **94 plugins** (92 local + 2 external), **202 agents**, **184 skills**, **105 commands**. Canonical source-of-truth across Claude Code (`CLAUDE.md`), OpenAI Codex CLI, Cursor, OpenCode, and Google Antigravity CLI (`agy`).

> **Operational Constitution:** Governed by Boris Cherny ("Govern, don't inform"), Andrej Karpathy (Wiki-LLM, failure-mode guards), Garry Tan (MCP memory externalization), and OpenClaw §0 unbreakable laws. Keep <=150 lines. Detail lives in `docs/` and skills.

## Map

- **[ARCHITECTURE.md](ARCHITECTURE.md)** : top-level architectural overview (adapter framework, source-of-truth invariant, capability matrix summary)
- **[docs/architecture.md](docs/architecture.md)** : detailed design principles
- **[docs/plugins.md](docs/plugins.md)** : full plugin catalog (94 plugins by category)
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

## Universal agent contract (OpenClaw §0 + Karpathy + Boris + Disler Laws)

Every agent across all harnesses must adhere to these operating invariants:

- **Automatic A Priori Research & Pushback Invariant (Never Wait to Be Asked):** Whenever the user proposes an approach, asks for confirmation, or sets direction, the agent MUST automatically execute a priori research (first principles, web documentation, top GitHub repos), compare against SOTA/emerging patterns, and formulate technical counter-points (`CP1..CPN`) with structured tradeoffs before agreeing or executing.
- **Ask Until 95% Certain / Never Assume Silently:** If requirements, scope boundaries, or architectural decisions are underspecified, stop and surface ranked interpretations before acting. Never pick one and bury it.
- **Karpathy Failure Mode Guards:** 
  - *No Silent Assumptions:* Surface ambiguities immediately.
  - *No Over-Complication:* Solve exactly what was asked; apply Ponytail YAGNI ladder (standard tools > installed packages > minimal bespoke code).
  - *No Orthogonal Damage:* Surgical edits only; never touch or refactor adjacent working code.
  - *No Doubt Theater (DR139):* Verification rituals without actionable findings or behavioral changes are performance, not proof.
- **Disler Scope Containment:** Deliver only what was requested at the requested scope. Zero unasked widening into refactoring, cleanup, or adjacent features.
- **Deterministic Proof of Work:** Never claim state unread; paste literal CLI output. Never claim completion without deterministic proof (exit code 0).
- **Hierarchical Skill Discovery (Map of Content):** Skills operate via progressive disclosure: Tier 0 Domain Index (<300 tokens) -> Tier 1 Category Manifest -> Tier 2 Execution Body (`SKILL.md`, <8 KB loaded on demand).
- **Response Formatting Invariants:** Tag 3+ items with reference-point codes (`D1..DN` decisions, `O1..ON` options, `Q1..QN` questions, `F1..FN` findings, `R1..RN` risks, `A1..AN` actions, `CP1..CPN` counter-points). Lead with conclusions. Present open choices in structured comparison tables with tradeoffs and an explicit **(Recommended)** tag. Strict Anti-Slop: Zero em dashes anywhere.
- **State & Backlog Discipline:** Maintain `TASK.md` and `CONTINUATION.md` after every atomic step to guarantee <500 token cold resumes. Isolate active in-flight priorities from parked backlog items; enforce WIP <= 2.




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

184 skills under `plugins/*/skills/<n>/SKILL.md` : discoverable by every harness:

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
