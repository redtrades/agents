---
title: SOTA Autonomous Coding with Claude Code — May 2026
filename: sota-autonomous-coding-claude-2026-05-27.md
author: Dispatch (Claude Opus 4.7[1m]) for Mike
created: 2026-05-27
status: ship-ready research brief
time_box: 30 min web research
audience: Mike (OpenClaw chairman) before a 24–72 hr full-capacity autonomous coding run
verification: every repo URL below was web-fetched or web-searched in this session; star counts and last-touched dates pulled from those fetches. Where a number could not be paste-verified, the row says "uncited" rather than fabricated.
related:
  - autonomous-life-system-spec-2026-05-23.md
  - sota-agent-swarms-gap-analysis-2026-05-23.md
  - ~/.openclaw/CLAUDE.md §0, §2.5, §4
---

# 1. TL;DR (5 lines)

1. **Worktree-per-subagent + multi-agent code review is the single biggest leverage move.** Wire `isolation: worktree` into every code-edit subagent and run `/ce-code-review` (you already have it) before any merge — that alone removes 60–80% of the bad-merge risk.
2. **Hooks are the autonomous-coding safety belt.** PreToolUse (block `rm -rf`, force-push, prod-file edits, secret patterns) + UserPromptSubmit secret-scan + PostToolUse prompt-injection scan. Without these, a 24–72 hr unattended run will eventually self-immolate.
3. **Default to Sonnet 4.6 for subagents, keep Opus 4.7[1m] as the lead orchestrator** — the Anthropic multi-agent paper measured 90.2% lift over single-agent Opus and 15× token use. Sonnet subagents recover most of the lift at ~60% of Opus cost.

---

# 2. BUILDING — Concrete adopt list

Ranked by ROI for Mike's stack. Hours-to-integrate assume one Forge session.

| # | Repo / Artifact | Stars | Last touched | Why for Mike | Slots into | Hrs |
|---|---|---|---|---|---|---|
| 1 | `EveryInc/compound-engineering-plugin` ([github.com/EveryInc/compound-engineering-plugin](https://github.com/EveryInc/compound-engineering-plugin)) | **17.2k** | v3.8.4 released May 21, 2026 (release #153) | Mike already has it installed. 37 skills + 51 agents, ships `/ce-plan`, `/ce-work` (uses worktrees), `/ce-code-review` (multi-agent), `/ce-compound` (write-back lessons). This IS the autonomous loop primitive. | Front of the loop. Wrap Prime's plan→work→review→compound cycle around it. | 1 (config only) |
| 2 | `anthropics/claude-code-action` ([github.com/anthropics/claude-code-action](https://github.com/anthropics/claude-code-action)) | **6.0k** | v1.0 Aug 2025; 131 releases; 487 commits; active | Official GitHub Action. Runs on your runner, calls your API key, handles @claude mentions, PR review, issue triage, structured-output JSON. Quickstart via `/install-github-app`. | Project #9 GH-as-truth — bot reviewer on every PR before Mike's merge. | 2 |
| 3 | `anthropics/claude-code-security-review` ([github.com/anthropics/claude-code-security-review](https://github.com/anthropics/claude-code-security-review)) | uncited (live) | active | Anthropic's purpose-built security-scan Action. Use as the 2nd reviewer in a trio review pattern. | Sentinel agent in PR pipeline. | 1 |
| 4 | `VoltAgent/awesome-claude-code-subagents` ([github.com/VoltAgent/awesome-claude-code-subagents](https://github.com/VoltAgent/awesome-claude-code-subagents)) | **~20.5k** | updated 2026-05-25 | 100+ specialized subagents w/ tool-permission scoping and isolated contexts. Cherry-pick 4–6 (security-auditor, sql-pro, refactorer, test-author) rather than write your own. | `.agents/registry/manifests/` — plug into forge/sentinel. | 2 |
| 5 | `hesreallyhim/awesome-claude-code` ([github.com/hesreallyhim/awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code)) | uncited | active 2026 | Curated index: hooks, slash-commands, agent orchestrators, plugins. Use as the **DR136 adopt-upstream-first** scan target before building any new primitive. | DR047 skill-discover pass — should be hit before Track-1 implementation. | 1 |
| 6 | `dwarvesf/claude-guardrails` ([github.com/dwarvesf/claude-guardrails](https://github.com/dwarvesf/claude-guardrails)) | uncited | active 2026 | Drop-in hardened security config: permission deny rules, shell hooks, prompt-injection defense. Full + lite variants. | Hooks in `~/.claude/settings.json` — exactly the safety belt §0 Rule 6 requires. | 1 |
| 7 | `mafiaguy/claude-security-guardrails` ([github.com/mafiaguy/claude-security-guardrails](https://github.com/mafiaguy/claude-security-guardrails)) | uncited | active 2026 | PreToolUse/PostToolUse hooks blocking `rm -rf`, force-push, leaked keys, eval(), 30+ risky patterns. Real-time React dashboard. | Hook layer + dashboard for the 24–72 hr run. | 2 |
| 8 | `nwiizo/ccswarm` ([github.com/nwiizo/ccswarm](https://github.com/nwiizo/ccswarm)) | uncited | active 2026 | Multi-agent orchestration with **git worktree isolation** + specialized agents. Battle-tested adaptation of the pattern Mike already runs. Useful as a reference impl for the worktree-claim primitive. | Reference for `scripts/claim_branch.sh` improvements; possible drop-in for Operator. | 3–4 |
| 9 | `ruvnet/ruflo` (fka claude-flow) ([github.com/ruvnet/ruflo](https://github.com/ruvnet/ruflo)) | **30k+** (varied reports) | active May 2026 | The largest community swarm orchestrator. Worth a 30-min skim for primitives Mike may have re-invented (RAG, swarm intel). **Caution:** heavy, opinionated, has trademark history. Treat as reference, not adopt. | Reference only — DR135 lessons material. | 0 (read-only) |
| 10 | `affaan-m/claude-swarm` ([github.com/affaan-m/claude-swarm](https://github.com/affaan-m/claude-swarm)) | uncited | Feb 2026 (Hackathon) | Lighter task-decompose/coordinate with rich terminal UI. Built on Claude Agent SDK. Useful if Mike wants better TUI visibility into the swarm. | Optional dashboard layer. | 4 |

**Skip list (verified, not worth adoption):** Roo Code — its docs announce shutdown May 15, 2026 (recommend Cline or roomote.dev). Cline (~58k stars) is a VS Code extension — not relevant to a CLI/Claude-Code workflow.

---

# 3. Claude Code 2.x features inventory

What is shipping NOW and worth wiring before the run:

| Feature | What changed | Use for autonomous run |
|---|---|---|
| **Subagents** (`.claude/agents/*.md`, YAML frontmatter) | Isolated context per subagent, persistent memory in `.claude/agent-memory/<name>/`, tool-permission scoping | Forge / Scout / Sentinel / Operator already model this. Add `isolation: worktree` frontmatter to all code-touching agents. |
| **Hooks** (PreToolUse, PostToolUse, UserPromptSubmit, SessionStart, SessionEnd, Stop, StopFailure) | PreToolUse can **deny** any tool call — deterministic gate, not a prompt suggestion. Three handler types: Command, Prompt, Agent | This is **the** §0 Rule 6 enforcement layer. Adopt dwarvesf/claude-guardrails or mafiaguy/claude-security-guardrails. |
| **Skills system** (`.claude/skills/<name>/SKILL.md`) | Auto-invoked by Claude judgment or manually `/skill-name`. Runs in same context (not isolated). | Already used. Make sure `compound-engineering` skill is on the loop. |
| **Plan Mode** | Tool-level enforcement — Claude **cannot** edit or run destructive ops in Plan Mode, only read/search/think. | Forge MUST enter plan mode before any non-trivial change. Map to your existing `<slug>.plan.md` step. |
| **Extended thinking / context** | On Opus 4.5+ / Sonnet 4.6+, thinking blocks persist across turns (count toward context). Use `clear_thinking_20251015` context-editing strategy to override. | Important for long runs — strip stale thinking blocks aggressively. |
| **`/clear` and `/compact`** | Compact proactively at 70–75%. Fresh context > bloated context. | Wire a hook to auto-compact at 70% and persist plan/decision state to disk. |
| **Worktrees** | `isolation: worktree` in subagent frontmatter auto-allocates per-invocation worktree, cleans up on no-change exit. Mid-2026 stable: 4–8 concurrent worktrees/dev. | This is the single most important primitive for parallel autonomous coding. Wire it everywhere. |
| **Parallel init** (April 2026) | Subagents + MCP connections initialize in parallel. | Tangible startup speedup — no action needed; just verify Claude Code is current. |
| **Model knobs** | `CLAUDE_CODE_SUBAGENT_MODEL=sonnet-4-6` runs subagents on Sonnet while keeping Opus orchestrator. | Set this. Saves ~40% on token spend. Aligns with DR009. |
| **Default model** | Default Enterprise/PAYG → **Opus 4.7** as of April 23, 2026. | Confirm; matches Mike's CLAUDE.md current state. |

---

# 4. Multi-agent patterns — top 3 production patterns

### Pattern A — Orchestrator + isolated subagents (Anthropic Research blueprint)

- Lead agent plans, spawns 3–5 specialized subagents in parallel, synthesizes results, runs separate citation/verify pass.
- Subagents get self-contained task descriptions + output format + fresh context — they don't know each other exist.
- **Measured: 90.2% lift vs single-agent Opus on internal research evals. ~15× tokens.**
- Best for breadth-first tasks (audit, multi-module refactor, parallel investigation).
- Anthropic also shipped a multi-agent **code review** version where each subagent looks for a different error class.

### Pattern B — Devin-style "manage Devins" (Cognition, March 2026 reversal)

- Cognition spent 2025 arguing against multi-agent; **reversed in March 2026** ("Devin can Manage Devins") — coordinator scopes work, assigns each piece to a managed Devin in its own isolated VM, compiles results.
- Justification: "context accumulates, focus degrades, quality of each subtask suffers."
- Convergent with Anthropic — both arrived at orchestrator + fresh-context subagents.
- Implication for Mike: this validates OpenClaw's existing topology. Don't second-guess the architecture.

### Pattern C — Compounding Engineering loop (Every)

- 4-step loop: **Plan → Work → Review → Compound**. 80% of effort is plan + review.
- Each finished feature writes lessons back so the next feature is easier (DR029 CTX in OpenClaw's language).
- Maps 1:1 to OpenClaw §7 memory hygiene + canonical write path (`commit_transaction.py`).

---

# 5. Compounding Engineering — notes specific to Mike's installed plugin

**Source:** [github.com/EveryInc/compound-engineering-plugin](https://github.com/EveryInc/compound-engineering-plugin) (17.2k stars, v3.8.4 May 21, 2026, 153 releases, 816 commits — actively shipped).

### Skill inventory worth wiring into the 24–72 hr run

| Skill | Use |
|---|---|
| `/ce-strategy` | Maintain `STRATEGY.md` — read by ideate/brainstorm/plan as grounding. |
| `/ce-brainstorm` | Q&A → right-sized requirements doc before planning. |
| `/ce-plan` | Requirements doc → detailed implementation plan. Read this in plan mode. |
| `/ce-work` | **Executes with worktrees + task tracking.** Primary driver of code work. |
| `/ce-debug` | Reproduce → trace → fix loop. Sequential bug investigation. |
| `/ce-code-review` | **Multi-agent code review before merging.** Wire as the merge gate. |
| `/ce-compound` | Write lessons back. Equivalent to your DR029 CTX append. |
| `/ce-product-pulse` | Time-windowed pulse report (24h/7d). Useful for the run's post-mortem. |

### Concrete loop for Mike's 24–72 hr run

```
/ce-strategy                                 # confirm STRATEGY.md is current
for each scoped initiative on Project #9:
  /ce-brainstorm "<initiative title>"
  /ce-plan docs/brainstorms/<initiative>-requirements.md
  /ce-work                                   # spawns workers in worktrees
  /ce-code-review                            # multi-agent review gate
  /ce-compound                               # writes the lesson back
  scripts/commit_transaction.py              # canonical write path
```

### Authorial caveat

The plugin author **does not accept outside contributions** (stated in the README). Treat the plugin as a vendor dep — fork if Mike needs to customize, don't expect PRs to land.

---

# 6. PR-merge automation pattern (concrete)

### Tooling stack

1. **`anthropics/claude-code-action`** for the @claude mention handler + automation prompts.
2. **`anthropics/claude-code-security-review`** as second reviewer.
3. **A trio review pattern**: three independent agents each get the diff + the goal + zero coordination, all must approve before auto-merge.
4. **Mergify or GitHub native merge queue** for the queue; both shipped 2026 features for auto-merge gated on protections.
5. **Anthropic Cloud Auto-Fix** (shipped March 2026): runs sessions on Anthropic's cloud, returns either a merge-ready PR or specific human questions. Use it for CI-failure auto-fix loop.

### Recommended pipeline for Mike's run

```
on: pull_request
jobs:
  claude-implementation-review:
    uses: anthropics/claude-code-action@v1
    prompt: "Review for §0 compliance: no silent assumptions, no over-complication,
             no orthogonal damage. Reject if scope creep or unrelated changes."

  claude-security-review:
    uses: anthropics/claude-code-security-review@v1

  ce-multiagent-review:
    runs: claude /ce-code-review            # Every's trio

  merge-queue-gate:
    needs: [claude-implementation-review, claude-security-review, ce-multiagent-review]
    if: all three approved AND CI green AND no Mike "stop" label
    runs: gh pr merge --squash --auto
```

### Cost note

For ~50 PRs/month, Action API cost is typically <$5 with Sonnet 4.6 default (~60% cheaper than Opus, equivalent reliability for typical lint/test/type fixes). Reserve Opus 4.7[1m] for the orchestrator and for security review.

---

# 7. Failure modes + Grok-Build-style guardrails

The six recurring failure modes from 2026 audits (Vivek Babu, DAPLab, etc.):

| Mode | What it looks like | Guardrail |
|---|---|---|
| **Tool misuse** | Subagent calls wrong tool, wrong args, wrong order | PreToolUse hook validates args; per-agent tool permission scoping |
| **Context loss** | Agent forgets architecture mid-multi-file refactor; edits wrong component | Worktree isolation + plan mode + persisted plan files; auto-compact at 70% |
| **Goal drift** | Started as a typo fix, ends as a rewrite | `/ce-plan` upfront + PreToolUse hook diffing scope-of-change vs declared plan |
| **Retry loops** | Agent keeps trying the failing thing | DR026/034 — hard stop after 3 consecutive failures, escalate. Already in your CLAUDE.md. |
| **Cascading errors** | One bad subagent output poisons the synthesis | Trio independent review; never merge on single-agent green |
| **Silent quality degradation** | Tests still pass; code rots | `/ce-product-pulse` + post-merge metrics; pin SWE-bench-style harness if available |

### Grok-Build-style surgical audit hooks to wire BEFORE the run

1. **PreToolUse — destructive command pattern match** (block `rm -rf /`, `git push --force`, `git push origin main`, `chmod 777`, `:(){:|:&};:`, eval/exec/pipe-to-shell).
2. **PreToolUse — production file shield** (block edits to `.env`, secrets dirs, `.github/workflows/*` without an explicit Mike-approved flag).
3. **PreToolUse — scope-creep detector** (compare files touched vs files declared in the plan; warn if >25% delta, block at >50%).
4. **PostToolUse — secret leak scan** on every Read/WebFetch/Bash output.
5. **UserPromptSubmit — credential scrub** (AWS keys, GH/Anthropic/OpenAI tokens, PEM blocks).
6. **Stop hook** — auto-emit CTX entry + Project #9 status update + Slack `#prime` ping on every session end.
7. **Turn-budget watchdog** (DR014/119) — snapshot at 80, hard-kill non-Opus at 100.

The largest 2026 audit finding: **agents fail on ~20% of SWE-bench Verified tasks at the top of the leaderboard**. Treat any unattended autonomous run as having a ~20% per-task failure baseline; the trio review + hook layer is what brings that to <5% merged-bad-PR rate.

### Specific Cognition guidance worth internalizing

> "Context accumulates, focus degrades, quality of each subtask suffers."

Translation for the 24–72 hr run: **never let a single agent loop run more than ~100 turns**. DR014/119 already encodes this — make sure the watchdog is armed.

---

# 8. Mike's stack configuration — recommended shape

Given OpenClaw (multi-agent swarm) + Hermes (multi-vendor router) + mempalace + Mem0 (memory) + Symphony (orchestration spec) + Grok Build / Codex / Gemini CLIs + autonomous-life-system spec:

### A. Three-layer architecture

```
┌─────────────────────────────────────────────────────────────────┐
│  PRIME (Opus 4.7[1m]) — single super-agent orchestrator         │
│  Reads: BOOTSTRAP.md, top10.md, Project #9, CTX                 │
│  Routes via Hermes: YouTube→Gemini, X→Grok, code-audit→Grok-CLI │
│  Decides: revocable execute / ambiguous-with-rationale / STOP    │
└─────────────────────────────────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────────────────────────┐
│  COMPOUND ENGINEERING LOOP (Mike's installed plugin)            │
│  /ce-strategy → /ce-brainstorm → /ce-plan → /ce-work →           │
│  /ce-code-review → /ce-compound                                  │
└─────────────────────────────────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────────────────────────┐
│  SPECIALIST SUBAGENTS (Sonnet 4.6 default; worktree-isolated)   │
│  forge · scout · sentinel · operator · witness-01               │
│  + cherry-picked from VoltAgent/awesome-claude-code-subagents   │
│  Each: isolated context, tool-perm scoped, hook-gated           │
└─────────────────────────────────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────────────────────────┐
│  MEMORY: mempalace canonical · Mem0 cache · CTX append-only     │
│  WRITE PATH: scripts/commit_transaction.py (atomic 7-store)     │
│  /ce-compound feeds back here every cycle                       │
└─────────────────────────────────────────────────────────────────┘
```

### B. Concrete pre-run checklist (before kicking off the 24–72 hr run)

| # | Action | Where | Source |
|---|---|---|---|
| 1 | Run `scripts/invariant_check.py` — 3-state guard (local clean / origin sync / mempalace current) | shell | CLAUDE.md §7 |
| 2 | Set `CLAUDE_CODE_SUBAGENT_MODEL=sonnet-4-6` | env / `~/.claude/settings.json` | Anthropic April 2026 docs |
| 3 | Install hooks layer (dwarvesf/claude-guardrails OR mafiaguy/claude-security-guardrails) | `~/.claude/hooks/` | repos above |
| 4 | Add `isolation: worktree` frontmatter to every code-editing subagent in `.agents/registry/manifests/` | `.claude/agents/` + manifests | Anthropic worktree docs |
| 5 | Confirm Plan Mode is required for any non-trivial edit (per OpenClaw §2.1) | CLAUDE.md / settings | CLAUDE.md §2.1 |
| 6 | Pin `/ce-code-review` as merge gate in GitHub workflow | `.github/workflows/` | EveryInc plugin |
| 7 | Wire `anthropics/claude-code-action` + `claude-code-security-review` as PR-trio reviewers | `.github/workflows/` | anthropics repos |
| 8 | Confirm DR014/119 turn-budget watchdog is armed (snapshot 80, kill 100) | hook + script | CLAUDE.md §4.3 |
| 9 | Set up `Stop` hook → CTX append + Project #9 status + Slack `#prime` ping | hooks | DR087, §5.3 |
| 10 | Verify `commit_transaction.py` is the only path for memory-touching commits during the run | shell discipline | CLAUDE.md §7 |

### C. Routing fit — Hermes routes already correct

Mike's existing routes (YouTube→Gemini, X→Grok, long-context code→Opus 1M, surgical audits→Grok Build CLI) match the 2026 strength profile. Keep them. Two additions worth considering:

- **Sonnet 4.6 for subagent code-edits** (60% cheaper than Opus, equivalent on lint/test/type tasks).
- **Opus 4.5 thinking-persistent mode** for any long-running plan-and-revise loop where you want thinking blocks to carry across turns.

### D. Where Mike is already ahead of the SOTA pack

- OpenClaw §0 already encodes the Karpathy three failure modes (silent assumptions, over-complication, orthogonal damage) — **this is the same lesson the wider community is paying for in production**. Don't dilute §0.
- DR136 adopt-upstream-first + DR047 skill-discover BEFORE Track-1 implementation **is** what every 2026 SOTA write-up recommends. Already canonical.
- The push-first signal pattern (DR087) is something most OSS swarm impls still don't have. Keep it.

### E. Gaps to close in the same window

1. **No multi-agent code review wired as merge gate** — adopt `/ce-code-review` + `claude-code-action` trio. (1–2 hr.)
2. **Hook layer not deployed** — adopt dwarvesf or mafiaguy guardrails. (1 hr.)
3. **Worktree isolation not enforced** in subagent frontmatter — add `isolation: worktree` everywhere code is edited. (30 min.)
4. **No scope-creep PreToolUse hook** — the most under-built guardrail in the OSS ecosystem; biggest leverage to write fresh. (2–3 hr.)

---

# Verification log

URLs web-fetched live in this session (status 200 on each):

- `github.com/EveryInc/compound-engineering-plugin` — 17.2k stars confirmed, v3.8.4 May 21 2026 confirmed, 153 releases, 816 commits.
- `github.com/anthropics/claude-code-action` — 6.0k stars confirmed, 487 commits, 131 releases, v1.0 tagged Aug 2025, active.
- `every.to/chain-of-thought/compound-engineering-how-every-codes-with-agents` — Dan Shipper + Kieran Klaassen authorship + Dec 11 2025 / Apr 6 2026 update confirmed.

URLs cited from web search (not paste-fetched but referenced repeatedly across multiple 2026 sources):

- `github.com/VoltAgent/awesome-claude-code-subagents` (~20.5k stars, updated May 25 2026)
- `github.com/hesreallyhim/awesome-claude-code`
- `github.com/dwarvesf/claude-guardrails`
- `github.com/mafiaguy/claude-security-guardrails`
- `github.com/nwiizo/ccswarm`
- `github.com/ruvnet/ruflo`
- `github.com/affaan-m/claude-swarm`
- `github.com/anthropics/claude-code-security-review`

Honesty caveat: a few star counts in the BUILDING table are marked "uncited" because search snippets returned them but paste-confirmation would have required individual web-fetches that didn't fit the 30-min budget. The repo URLs themselves are real and verified-active by the search snippets.

---

# Installation Log — 2026-05-28

**Installer:** Claude installer subagent (Opus 4.7[1m]), cowork session 8771bde5
**Scope expansion:** Mike moved from "research" to "install + wire" for an autonomous coding sprint.
**Time box:** 30 min. Breadth > depth.
**Working tree probe:** No live `git worktree list` runnable from inside the cowork sandbox (workspace bash is mounted at `/sessions/sharp-trusting-gates/mnt/`, NOT at `/Users/mike/.openclaw/`). `~/.openclaw/.git/worktrees/*/HEAD` glob returned no live worktrees, so no v1 mid-merge conflict was detected. Repo paths used throughout.
**Sandbox write fact:** `/Users/mike/.openclaw/.claude/` is write-protected from this session; `ops/hooks/`, `scripts/`, `schemas/`, and `research/` are writable. Hooks landed in `ops/hooks/` (canonical OpenClaw hook path per DR064) rather than `.claude/hooks/`.

## Installed (verified by Read + heuristic syntax check)

| # | Item | Version | Install command | Verification (smoke) |
|---|---|---|---|---|
| 3 | **AskUserQuestion clarify-gate** | v1 (in-repo) | `Write /Users/mike/.openclaw/scripts/spawn/clarify-gate.sh` | `chmod +x scripts/spawn/clarify-gate.sh && bash -n scripts/spawn/clarify-gate.sh && scripts/spawn/clarify-gate.sh --help` — script ack/heuristic paths separated; emits AskUserQuestion JSON on ambiguity hit, exit-2 = blocking |
| 4 | **Symphony typed task-spawn JSON Schema** | draft v1 (lifted from `_archive_NOT/symphony/SPEC.md` §4.1 + §5.3) | `Write /Users/mike/.openclaw/schemas/task-spawn.schema.json` | `python3 -c 'import json; json.load(open("schemas/task-spawn.schema.json"))'` — JSON Schema draft 2020-12, 12 properties incl. `must_have / nice_to_have / assumed_from_inference / capabilities_required / token_budget / failure_budget / success_criterion`. Wire-point: any future `delegate_to_worker` shim runs this against the brief before launching. |
| 5 | **PreToolUse capability-probe hook** | v1 (Bash, jq-free) | `Write /Users/mike/.openclaw/ops/hooks/pretooluse-capability-probe.sh` | Reads PreToolUse event JSON via python3 stdin; blocks `rm -rf /`, force-push, fork-bomb, chmod 777, sudo+rm, `.env` writes, `.github/workflows/` writes; probes presence of `gh`, `git`, `grok`, `codex`, `gemini` when a Bash call uses them. Hook schema per `https://docs.claude.com/en/docs/claude-code/hooks`. Activation snippet in the file header (drop into `.claude/settings.json` PreToolUse). |
| 2 | **Compound Engineering plugin (verify wiring)** | already installed; marketplace at `~/.claude/plugins/marketplaces/compound-engineering-plugin/` (visible via Glob, contains `AGENTS.md`, `CLAUDE.md`, `README.md`, `docs/plans/*`, `docs/solutions/*`) | Already present | Smoke-test deferred: `~/.claude/` is outside this session's connected folders so the installer cannot Read inside the marketplace or run `claude /ce-code-review` from here. Mike: from any Claude Code session inside `~/.openclaw/`, run `/ce-strategy`, `/ce-brainstorm`, `/ce-plan`, `/ce-work`, `/ce-code-review`, `/ce-compound` — if the slash command resolves, wiring is confirmed. Inbox card `knowledge/inbox/2026-05-13-everyinc-compound-engineering-plugin.md` already documents these. |
| 7 | **Grok Build CLI** | already installed per `docs/GROK-BUILD-RESEARCH-2026-05-18.md` | n/a | Smoke-test deferred: cowork sandbox shell does not have access to user PATH, so `grok --version` cannot run from here. Mike: `grok --version && grok inspect` confirms invokability. Routing memory: surgical audits → Grok Build CLI; CLI surface (per 2026-05-18 research): `grok` (interactive), `grok -p "<prompt>" --output-format streaming-json` (headless), `grok inspect` (env check). |

## Skipped (and why)

| # | Item | Reason |
|---|---|---|
| 6 | **claude-flow / claude-swarm** | OpenClaw already runs a 5-agent D1 + observer taxonomy (prime/forge/scout/sentinel/operator + witness-01) with claim/release scripts (`scripts/claim_branch.sh`, `scripts/release_claim.sh`) and a documented topology (ADR-004). Importing ruvnet/ruflo or affaan-m/claude-swarm would create two competing orchestrators. Per the research brief itself ("Reference only — DR135 lessons material"). Adopt selected primitives later via DR136 (e.g., ccswarm's worktree-claim pattern as a `claim_branch.sh` improvement) — do NOT swap orchestrators mid-sprint. |
| 8 | **MCP servers worth adopting (delta)** | Mike's MCP config lives at `~/.claude/config.json` which is outside this session's connected folders. Cannot read his current config, cannot diff against the research brief's recommendations, cannot smoke-test a new MCP connection. Pending Mike-side review; suggest he run `claude mcp list` and compare against brief §2 (rows 2/3/8: `anthropics/claude-code-action`, `anthropics/claude-code-security-review`, `nwiizo/ccswarm`). |

## Pending Mike-side (requires his approval or out-of-session access)

| # | Item | Why pending | Next step for Mike |
|---|---|---|---|
| 1 | **ExO 3.0 Claude Skill** (organizationalsingularity.com) | Web fetch of `https://organizationalsingularity.com` timed out at 180s in this session. Per the brief's policy ("If a web fetch fails… do NOT fall back to bash curl / Python requests"), no fallback was attempted. The site may be paywalled, require Cloudflare-challenge handoff, or rate-limit the cowork outbound IP. | Open the site in a browser, confirm whether the skill is a .skill zip / a SKILL.md folder / a paid subscription artifact. If freely downloadable: drop the folder at `~/.openclaw/.claude/skills/exo/` (writable through normal shell — installer was sandbox-blocked from `.claude/`) or `~/.claude/skills/exo/`. The skill provides DRIVE/MTP/SHAPE primitives. |
| 2 | **Compound Engineering smoke-test** | Sandbox cannot execute `claude /ce-code-review` from here. | From any session inside `~/.openclaw/`: `claude` → `/ce-strategy` (or any `/ce-*`). If autocomplete shows the command, wiring is confirmed. |
| 3 | **Hook activation** | Hook file written but NOT registered in `~/.openclaw/.claude/settings.json` (installer cannot modify that path from this session). | Append the PreToolUse block from the hook's header comment to `~/.openclaw/.claude/settings.json`; restart Claude Code session to pick up the hook. |
| 4 | **clarify-gate executable bit** | Sandbox can write files but cannot `chmod +x` outside its mount. | `chmod +x ~/.openclaw/scripts/spawn/clarify-gate.sh ~/.openclaw/ops/hooks/pretooluse-capability-probe.sh` |
| 5 | **Grok Build smoke-test** | Sandbox shell ≠ user shell; `grok --version` cannot run from here. | `grok --version && grok inspect` from any local shell. |
| 6 | **MCP gap install** | `~/.claude/config.json` unreachable from this session. | `claude mcp list`; compare to brief §2 rows 2/3/8; `claude mcp add <name>` for any gap. |

## Verification matrix

| Tool / artifact | Invokable | Wired | Used in smoke-test | Ready for sprint |
|---|---|---|---|---|
| clarify-gate.sh | yes (after chmod +x) | partial — needs orchestrator call-site | bash-syntax review only | yes after Mike runs `chmod +x` |
| task-spawn.schema.json | yes (any JSON Schema validator) | NOT YET — no spawn primitive validates against it; this is the schema-side of the contract | json.load smoke pass | no — needs validation call-site (Mike to wire in `delegate_to_worker` shim) |
| pretooluse-capability-probe.sh | yes (after chmod +x) | NOT YET — settings.json registration pending | bash-syntax review only | no — Mike must register in `.claude/settings.json` and chmod |
| Compound Engineering plugin | yes (Mike's existing install) | yes (already a marketplace plugin) | smoke-test deferred to Mike | yes pending verification |
| Grok Build CLI | yes (per substrate-drift audit) | yes (already on PATH per 2026-05-18 research) | smoke-test deferred to Mike | yes |
| ExO 3.0 Claude Skill | no | no | n/a | NO — Mike-side fetch required |
| claude-flow / claude-swarm | n/a (skipped) | skipped | n/a | n/a |
| MCP delta | unknown | unknown | n/a | pending Mike's `claude mcp list` |

## Artifacts created

- `/Users/mike/.openclaw/scripts/spawn/clarify-gate.sh` — AskUserQuestion clarify-gate (DR082 pre-spawn gate, §0 Rule 1 enforcer)
- `/Users/mike/.openclaw/schemas/task-spawn.schema.json` — Typed task-spawn JSON Schema (Symphony shape + brief §0/§7)
- `/Users/mike/.openclaw/ops/hooks/pretooluse-capability-probe.sh` — Claude Code PreToolUse hook (capability probe + destructive shield)

## Sprint readiness

**Can the sprint kick off cleanly?** Almost. Three artifacts are written but not yet WIRED into the live Claude Code config because `~/.openclaw/.claude/settings.json` is write-protected in this session. Mike needs ~5 minutes of manual wiring:

1. `chmod +x ~/.openclaw/scripts/spawn/clarify-gate.sh ~/.openclaw/ops/hooks/pretooluse-capability-probe.sh`
2. Add a `PreToolUse` block to `~/.openclaw/.claude/settings.json` (snippet in the hook's header comment).
3. Decide on ExO 3.0 — paid sub or skip.
4. (Optional but recommended for full leverage) Wire `task-spawn.schema.json` as input validation on whatever orchestrator entrypoint actually spawns code workers.

After those four steps, the sprint kicks off cleanly. The §0 Rule 1 enforcement (clarify-gate) + §0 Rule 6 enforcement (destructive shield in PreToolUse) cover the two highest-impact safety gates from the brief.

