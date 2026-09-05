# Agentic Operating Constitution: claude-agents

Production-ready agentic operating foundation: **100 plugins**, **202 agents**, **225 skills**, **105 commands**. Canonical source-of-truth across Claude Code (`CLAUDE.md`), OpenAI Codex CLI, Cursor, OpenCode, and Google Antigravity CLI (`agy`).

> **Operational Constitution:** Governed by Boris Cherny ("Govern, don't inform"), Andrej Karpathy (failure-mode guards), Garry Tan (memory externalization), and OpenClaw §0 unbreakable laws. Keep <=150 lines. Detail lives in `rules/`, `docs/`, and `plugins/`.
> **Dual Mission:**
> 1. **Production Factory:** Automated federal RFP proposal starter deliverables (`govcon-factory`, $8k-$10k/month revenue target).
> 2. **Swarm Foundation:** Sovereign, vendor-agnostic, resilient multi-agent operating engine (`redtrades/agents`).

## 1. Non-Negotiable Operating Invariants (Hard Gates)

- **Communication Grammar:** Lead with conclusion and verdict. When presenting >=3 findings, decisions, options, risks, actions, or questions, prefix each with standardized reference codes (`F1..FN`, `D1..DN`, `O1..ON`, `R1..RN`, `A1..AN`, `Q1..QN`). Format architectural choices as Decision Tables with explicit `(Recommended)` tag.
- **Strict Anti-Slop & Banned Phrases:** Zero em dashes anywhere in code, docs, commit messages, or responses (use single hyphens, colons, or parentheses). Banned exact phrases: "load-bearing", "worth stating plainly", "here's the honest truth", "the real tension", "carry the argument". Zero conversational flattery, zero cheerleading.
- **Risk-Tiered Autonomy Ladder:**
  - *L1 (Read / Discovery):* Grep, file viewing, web research, benchmarks. Zero gates (autonomous).
  - *L2 (Reversible Code / Tests):* Edits, tests, bug fixes, formatting. Autonomous gated by deterministic exit code 0.
  - *L3 (Structural / Swarm):* New dependencies, architectural pivots, multi-agent spawns. Soft gate: implementation plan with CPs and trade-offs required.
  - *L4 (Irreversible / Destructive):* Deletions, force-pushes, branch destruction, credentials, billing. Hard gate: explicit human go-ahead required.
- **SDLC Queue & Worktree Isolation:** GitHub Issues are the single work queue. Work in isolated worktrees (`work/<task-id>`); maximum 2 concurrent worktrees globally. Cross-model review required before merge; Mike holds final production merge authority.
- **Mandatory A Priori Research & Counter-Points:** Before proposing non-trivial architectures or writing code, automatically inspect internal research (`docs/research/`), benchmark top GitHub repositories and emerging SOTA patterns, and present explicit counter-points (`CP1..CPN`) with trade-offs. Never wait to be prompted.
- **Anti-Wholesale Ingestion Law:** Zero bulk copying or recursive migration of legacy folders (`agent-*`). Every promoted asset must pass selective distillation: proof of necessity, elimination of redundant/obsolete/trivial (ROT) cruft, and alignment with modern schemas.
- **Session Cold-Start Invariant:** On turn 1 of any session or task, read `CONTINUATION.md` (<500 tokens) and `TASK.md` to establish active in-flight phase before running modifying commands or generating prose.
- **Safety & Secret Preservation:** Never commit secrets. Never run destructive git commands (force-push, `reset --hard`, branch -D) without explicit authorization.

## 2. How to Work in This Repo

- **Tooling:** Python tooling uses **uv** (package manager), **ruff** (lint/format), **ty** (type check). Do not use pip / mypy / black. Standard Makefiles hold execution mechanics (`Thin Agents, Fat Recipes`).
- **File Naming & Hygiene:** All new docs, plans, analyses, and walkthroughs MUST begin with an 8-digit date prefix: `YYYYMMDD-<name>.md` (e.g., `docs/plans/20260905-plan.md`). Plans and walkthroughs persist to `docs/plans/` and `docs/walkthroughs/`.
- **2-Try Circuit Breaker:** If an action or test fails twice, STOP immediately. Consult documentation, search runtime state, or inspect root causes; never guess.
- **State Continuity Protocol:** Maintain `TASK.md` and `CONTINUATION.md` in repository root. Commit diffs incrementally after every step. Cold-start resume in <500 tokens without re-ingesting conversation history.
- **Ponytail YAGNI Ladder:** Standard tools > installed packages > minimal bespoke code. Surgical edits only; avoid orthogonal damage to adjacent working code.
- **Skill-First Discipline:** 225 skills live under `plugins/`. Inspect keywords against `docs/skills-moc.md`. Load matching skill via `view_file` (<8 KB) before acting. Announce `Using [skill] for [purpose]`.
- **Proportional Rigor:** Tier 1 (<2 min doc/fix) executes directly; Tier 2 (MVP) tests focused diffs; Tier 3/4 require formal plans, ADRs, and full verification.
- **Deterministic Proof of Work:** Verify completion via deterministic test assertions and exit code 0; avoid doubt theater.

## 3. Quality Gates & Verification

```bash
make validate STRICT=1     # structural validation across all 5 harnesses
make garden                # drift detection (dead links, stale artifacts, oversize skills)
make test                  # full pytest suite (plugin-eval + tools/tests/)
npm test                   # core contract validation suite
make generate-all          # sync artifacts to .codex, .cursor, .opencode, .antigravity
```

## 4. Operational Pointers

- **[ARCHITECTURE.md](ARCHITECTURE.md)** : architectural overview and harness matrix
- **[rules/README.md](rules/README.md)** : living operational rules (`communication.md`, `hygiene.md`, `task-tracking.md`, `verification.md`)
- **[docs/decisions/README.md](docs/decisions/README.md)** : ADR registry and operational decision log (`DECISION_LOG.md`)
- **[docs/skills-moc.md](docs/skills-moc.md)** : canonical skills Map of Content (225 skills by domain and tier)
- **[docs/GLOSSARY.md](docs/GLOSSARY.md)** : canonical estate glossary and taxonomy
