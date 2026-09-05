



C1
I'll check what you already have in the homelab and agent-orchestration work, then research current best practice before proposing anything.Research phase — no files or code yet. Let me survey what's actually current.# Research phase — nothing written yet

Here's what I found, then a proposal. No files or code until you confirm.

## The core finding

**Fidelity loss between agents isn't a memory problem — it's a state problem.** The best-documented practitioner work on this makes the distinction sharply: a knowledge base stores what stays true across tasks; what dies when quota runs out is the _live state_ of one task — which sub-steps are done, which approaches were already ruled out and why, whether a background build is still running, and which command to run next. Growing your knowledge base never fixes the handoff, because the thing that vanished was never knowledge.

So you need **three separate layers**, and most setups only externalize the first one.

|Layer|What it holds|Lifespan|Where it lives|
|---|---|---|---|
|**Knowledge**|How the repo works, conventions, build commands|Months|`AGENTS.md`|
|**Intent**|What "done" means for this feature|Weeks|Spec + task graph|
|**Live state**|What's mid-flight _right now_, with evidence|Hours|Handoff file / issue lease|

---

## What's actually alive out there

### Instruction layer — settled, use AGENTS.md

AGENTS.md was released by OpenAI in August 2025 and transferred to the Linux Foundation's Agentic AI Foundation in late 2025, and now covers 28+ tools and 60,000+ repos. Against your specific agent list:

|Agent|Reads AGENTS.md?|Notes|
|---|---|---|
|Codex CLI|Native|Originated the format|
|OpenCode|Native|Falls back to CLAUDE.md if no AGENTS.md; AGENTS.md wins when both exist|
|Grok CLI / Grok Build|Native|Merged from git root down to cwd, Codex-style; also reads CLAUDE.md natively|
|Claude Code|Yes, bridged|Added AGENTS.md support in spring 2026, but CLAUDE.md remains its richer native format|
|**Gemini CLI**|**No**|The remaining holdout — still uses GEMINI.md|

Practical rule: make AGENTS.md the only instruction file humans edit, bridge Claude Code with a one-line `@AGENTS.md` import or a committed symlink. Keep it short — a focused 50-line file outperforms a sprawling 1,000-line one, and Codex CLI silently truncates past `project_doc_max_bytes`.

### Intent layer — GitHub Spec Kit

Spec Kit provides a `specify` CLI and slash commands structuring work into a repeatable specify → plan → tasks → implement flow, with 30+ agent integrations. Liveness is not in doubt: 111k stars and 55+ releases. Specs externalize intent — they give the agent a stable contract and give future sessions a durable handoff artifact instead of a long prompt thread.

**What to avoid:** running full Spec Kit ceremony on small tasks. It's a harness, not a religion.

### Work-ledger layer — Beads (`bd`)

Steve Yegge's Beads is the strongest candidate. Distributed graph issue tracker for AI agents, powered by Dolt, with four dependency types (blocks, related, parent-child, discovered-from), automatic ready-work detection, `--json` flags for programmatic use, and git-versioned JSONL records synced across machines. Evidence of life: v1.1.0 release candidates as of March 2026, ~25k stars, setup shims for Codex, Claude, Cursor, Factory, and more.

**What to avoid:** Yegge is moving it fast — two upgrade-breaking migration regressions were reported against v1.1.0-rc.1. Pin your version. A Rust port exists partly because one maintainer needed a stable snapshot of the architecture he built around.

### Live-state layer — a handoff file protocol

This is the piece that directly answers your question, and it's the least tool-dependent. The best-documented version: one file per task, seven sections — frontmatter (task/status/owner/updated), Goal, Now, Done, Next, Gotchas, Resume — with two rules doing most of the work:

1. `Done` items are worthless without evidence — "fixed the parser" is a claim; "fixed the parser, `parser.py:88`, commit `a1b2c3d`, fixtures 11/11" is a state you can trust.
2. The person taking over re-verifies the last `Done` item before building on it. The four-step take-over: read the whole file, set `owner` to yourself and bump `updated` (that's the lock against two drivers), re-run the last `Done`'s evidence, then start at `Next`'s first item.

Two hard-won details worth stealing outright:

- **Save on state transitions, never on a timer.** A timer fires mid-thought and writes a snapshot of confusion — a half-drafted approach, a command you were about to run but hadn't. Whoever picks that up inherits your uncertainty as if it were a decision.
- **Staleness must be phase-aware, not clock-based.** The author's own rule ("no update in 2 hours = abandoned") flagged an overnight GPU training run with 19 hours left as "up for grabs." The hook wasn't broken — it faithfully executed a bad rule. Fix: a `phase` field (`running_external | waiting_user | blocked | working`) plus an `expected_until` timestamp.

### Verification layer — CI is the only thing that can't be fooled

"The report says done" is not done. When a delegated run reports success, the orchestrator re-runs the acceptance command itself. A report is a claim; acceptance is a command you run. GitHub Agentic Workflows went to public preview in June 2026, with supported engines including Copilot, Claude Code, Gemini, and Codex. Note GitHub's own positioning: agentic workflows augment CI/CD rather than replace it — don't use them instead of deterministic YAML for build, test, and release.

### Orchestration layer — Gas Town, and why I'd skip it

Gas Town coordinates 20–30 Claude Code instances in parallel; all state lives in Beads, serving as both data plane and control plane. Sessions are ephemeral cattle; agents are persistent identities. Its durability model is exactly your problem statement: all work is expressed as "molecules" — chained sequences of small tasks stored as Beads in Git, each with clear acceptance criteria. If an agent crashes mid-step, the next session picks up where it left off.

**But:** it solves _parallel_ fan-out, you're describing _sequential_ relay, it's Claude-Code-centric, ~189k LOC of Go, and Yegge explicitly warns developers at earlier stages will find it frustrating rather than productive. You already run a five-agent orchestrator in the homelab — bolting Gas Town on top would duplicate the control plane you have. My call: **take the Beads ledger, leave the town.**

---

## Proposal

### Recommended stack

|Layer|Pick|Alternatives considered|Why this won|
|---|---|---|---|
|Instruction|`AGENTS.md` + thin `CLAUDE.md` / `GEMINI.md` bridges|Per-tool files; symlinks|Widest native support; symlinks break on Windows and in some CI checkouts|
|Intent|**Nothing at first** — a `specs/<slug>.md` convention|Spec Kit, BMAD, Kiro|Spec Kit is excellent but earns its ceremony at feature scale, not task scale. Adopt at Phase 3|
|Work ledger|Beads (`bd`), version-pinned|GitHub Issues via `gh`; markdown TODOs|Dependency graph + `bd ready` is the thing GitHub Issues can't do. Markdown plans rot|
|**Live state**|**Handoff file protocol — 7 sections, evidence-bearing, phase-aware**|Session resume (`claude -r`, `codex continue`); memory MCPs|Session files are per-tool and don't cross vendors. Codex resume reconstructs state by re-reading the transcript, not from saved model state — a fresh agent infers, it doesn't know|
|Verification|Deterministic GitHub Actions + branch protection|Agent self-report|The only trust boundary that survives an agent lying to you|
|Continuous AI|`gh aw` agentic workflows|Custom Action + API keys|Native permissions, sandboxing, safe-outputs|

### Architecture

```
repo/
├── AGENTS.md              ← knowledge. ~50 lines. Includes the handoff protocol itself
├── CLAUDE.md              ← one line: @AGENTS.md
├── GEMINI.md              ← one line import (Gemini tax)
├── .beads/                ← work ledger, git-synced JSONL
├── .agents/
│   ├── handoffs/<slug>.md ← LIVE STATE. One per in-flight task
│   └── archive/
├── specs/<slug>.md        ← intent, when a task is big enough to need one
└── .github/workflows/     ← acceptance gates. The arbiter
```

**Flow:** `bd ready` → agent claims a bead → opens `.agents/handoffs/<slug>.md`, sets `owner`+`updated`+`phase` → works, writing on each state transition → opens a PR whose body links bead + handoff → CI runs the acceptance command → merge.

**Handoff at the quota wall:** agent writes final state → next agent (any vendor) runs one preflight command, reads the handoff, re-runs the last `Done` evidence, continues at `Next[0]`.

**Failure modes designed against:**

- _Two agents claiming one task_ → `owner` + `updated` lease in frontmatter, taken at claim time
- _Silent lying about progress_ → evidence required on every `Done`; CI re-runs it
- _False takeover of a long job_ → `phase` + `expected_until`, not a clock rule
- _Instruction drift across five tools_ → one human-edited file, everything else an import
- _Prompt injection via issue text_ → a May 2026 paper described "agentic workflow injection" — untrusted repo content (issue text, PR descriptions, comments) passed into agent prompts. Never let agent-authored text reach a privileged step unreviewed

### MVP — smallest thing that actually works

1. `AGENTS.md` with the handoff protocol written into it
2. `.agents/handoffs/` + a template
3. One preflight command (`make agent-start`) that prints: active handoffs, git state, ready work
4. One CI workflow: tests + lint on every PR, branch protection on
5. PR-per-task, acceptance command named in the ticket

**Explicitly excluded from MVP:** Beads, Spec Kit, Gas Town, `gh aw`, MCP memory servers, worktrees, any automatic quota-detection failover.

### Development sequence

|Phase|Ships|Proves|
|---|---|---|
|1|AGENTS.md + handoff protocol + CI gate|A cold agent from a different vendor can resume your half-finished task|
|2|Preflight command + `phase`/`expected_until` + stop-guard hook|Handoffs get written without you remembering to ask|
|3|Beads as the ledger; handoffs reduce to live state only|Multi-day, multi-agent task chains hold their order|
|4|Spec Kit for feature-sized work|Intent survives across the whole chain, not just the task|
|5|`gh aw` for triage / CI-failure analysis|Continuous AI, deterministic CI untouched|

### Non-goals

- **Parallel swarms.** You asked for sequential relay. Parallelism is a different problem with a different (much larger) tool bill.
- **Automatic quota-exhaustion failover.** Detection is unreliable across five vendors; the human deciding who picks up is a feature, not friction. Ownership should stay a human decision, with `owner` demoted to a routing hint.
- **A shared vector-memory MCP.** It solves recall, not state. Wrong layer.
- **Model-specific prompt tuning.** The handoff must read identically to Opus and to Gemini Flash, or it isn't a handoff.

### Improvements you didn't ask for

- **Write handoffs for a stranger, not for yourself.** No "as we discussed," no pronouns without antecedents. `file:line`, commit SHA, literal command. This is what makes cross-vendor work rather than just cross-session.
- **One preflight command, not five prompts.** Every agent's first action is the same shell command. Removes per-tool instruction drift entirely.
- **Land the plane at ~80%, not at the wall.** At around 80–90% of the useful window, stop starting new work, verify what's done, and leave a clean pickup point. Cheap habit, biggest single payoff.
- **Route by task shape, not by who has quota left.** Mechanical refactors to a cheap fast model, architecture to your best one. Ties directly into the cost work you already do in the homelab.
- **Enforce, don't just document.** Logged → documented → templated → enforced. A log entry every session re-reads is not the same as a template every session uses. Get the protocol into a stop-hook that refuses to end a session on a stale handoff.

### Open items I can't decide for you

- **Where do agents run?** Your M1 Max homelab, GitHub Actions runners, or both? Changes whether handoffs are file-based or Issue-based.
- **`.agents/` committed or gitignored?** Committed gives auditability and cross-machine sync; gitignored keeps PRs clean. I lean committed.

Three decisions gate the build:

# G0

**Do not pass chat history between Claude, Codex, Gemini, and Grok.** Treat the repo as the shared brain. Chat is disposable; disk + git + tests are the continuity layer. That is the 2026 consensus across Anthropic’s long-running harness, vendor-neutral memory protocols, and quota-switch kits.

I could not find a product named “Kid Hub.” The workable reading is **parent/child hub workflows** (one orchestrator, many workers) plus **STLC as gated phases**. If you meant GitHub Agentic Workflows, that is a separate CI runner, not a substitute for session memory.

## Conclusion

**D1.** Optimal setup is a **parent orchestrator + child workers**, with **durable project state outside every model**. When usage dies, the next agent boots from files, not from a pasted transcript.

**D2.** Continuity that survives vendor switch is four artifacts, always:

| Artifact | Job |
|---|---|
| Goal board (`features.json` or phase checklist) | What “done” means. Default `passes: false`. Agents may flip flags only after evidence. |
| Handoff contract (`AGENT_HANDOFF.md` / `SESSION_HANDOFF.md`) | Current task, files owned, last evidence, next single action, stop reason. |
| Event log (`work.log` or `progress.txt`) | Order of events. Append-only. |
| Git + tests | Implementation truth. Commits are the ledger. Tests are the ratchet (never delete failing tests to “pass”). |

**D3.** Isolation is a feature. A reviewer that cannot see the implementer’s rationalizations catches more. Do not try to reconstruct full conversational fidelity across models. Reconstruct **decisions, artifacts, evidence, and the next step**.

---

## Why chat handoff fails

**F1. Context is vendor-private.** Claude compact, Codex “handoff memo,” Gemini compression each destroy different things. Quality drops well before the advertised window is full (~60–70% fill).

**F2. Quota death is abrupt.** If closeout is not written *before* the limit, the next model inherits a dirty tree and a story that only existed in the dying session.

**F3. Shared context pollutes review.** Pipelines that keep one fat window accumulate assumptions. Role-split + fresh windows beat “one mega-transcript.”

---

## Architecture to install

Think in two loops.

```
Parent (you or a lead agent)
  owns: goal board, phase gate, who runs next
Child session (Claude | Codex | Gemini | Grok)
  owns: one slice, one ownership set, one stop condition
  writes: code + tests + handoff + log + commit
Gate
  evidence required (test output, screenshot, eval)
  then next child or next STLC phase
```

This is Anthropic’s initializer/coding-agent harness generalized to multiple vendors: first session bootstraps the board and boot script; every later session orients from disk, does one increment, leaves a clean tree.

### Repo layout

```
AGENTS.md                 # canonical rules (every tool reads this)
CLAUDE.md / GEMINI.md / GROK.md   # one-line pointers to AGENTS.md
AGENT_HANDOFF.md          # live contract (single source of truth)
features.json             # default-FAIL goal board
progress.txt              # last session narrative (short)
AIMemory/                 # optional hot/warm/cold event log
  INDEX.md
  work.log
  archive/
tests/                    # ratchet; deletion banned
.git/
```

Thin pointers (`CLAUDE.md` → `@AGENTS.md`) are how Codex/Claude/Gemini stay aligned without duplicating policy.

### Required handoff fields

Every closeout, including quota closeout, must contain:

1. Objective (one sentence)
2. Phase (STLC/SDLC stage)
3. Files touched / files still reserved
4. What landed (commit SHAs)
5. Evidence (test command + result; not “should pass”)
6. Open questions / constraints that must not be forgotten
7. **Next action** (exactly one)
8. Owner for that action
9. Stop reason: `task-complete` | `context-budget` | `quota` | `blocker`

That schema is the useful core of `cli-collaboration` and the session-governance quota-switch flow.

### Session boot (every agent, every time)

1. `git status` + `git log --oneline -20`
2. Read `AGENT_HANDOFF.md`
3. Read `features.json` + tail of `progress.txt` / `work.log`
4. Declare start gate (task, files, expected red/green test, stop condition)
5. Do **one** slice
6. Verify
7. Commit
8. Rewrite handoff **before** you are near the limit

Do not start implementing until orientation is done. That boot sequence is the part of Anthropic’s harness that actually transfers state.

---

## Who should do what

Use models as jurisdictions, not as interchangeable brains.

| Role | Best default | Must not own |
|---|---|---|
| Plan, spec, cross-file judgment, review | Claude | Unbounded “just keep coding” with no contract |
| Bounded implement + terminal/test loop | Codex | Product judgment / fuzzy scope |
| Onboard, synthesize long logs, red-team, wide-context QA | Gemini | Silent rewrite of the goal board |
| Research, second-pass critique, Grok-native runtime | Grok | Unilateral ownership of shared files |

Sequential is correct for one goal stream. Parallel only when file ownership does not overlap (worktrees or explicit reserved zones). Two implementers in one worktree is how fidelity dies.

---

## STLC as the sequence, not as a prompt

Map agents to **entry criteria → artifacts → exit criteria**, not to “please continue.”

| Phase | Entry | Artifact out | Exit |
|---|---|---|---|
| Test planning | Intent / spec exists | `test-plan.md` + risk list | Scope and environments named |
| Analysis | Plan accepted | Traceability: requirement → condition | Ambiguities listed, not guessed |
| Design | Conditions frozen | Test cases / evals, default fail | Cases reviewable without the author |
| Env setup | Cases exist | `init.sh` / fixtures | Boot script reruns clean |
| Execution | Env green | Results + failing IDs | Failures logged; tests not deleted |
| Closure | Execution done | Updated `features.json` + handoff | Next goal or stop |

A phase does not complete because an agent said it did. It completes when the next agent, in a **fresh window**, can verify the artifact. That is the default-FAIL + fresh-evaluator pattern.

Parent hub rule: the parent never implements. It only advances a phase when evidence is on disk.

---

## Quota switch (the actual ritual)

Do this at ~70% context or when the product warns about usage — not after the hard stop.

**On the dying agent**

```
Close out for vendor switch.
Update AGENT_HANDOFF.md and features.json.
Commit everything that works.
Do not start a new slice.
Stop reason: quota.
Next action: <one command or one file>.
```

**On the incoming agent**

```
Read AGENTS.md, AGENT_HANDOFF.md, features.json,
git log -20, and the last 30 work.log events.
Do not reconstruct prior chat.
Continue from Next action only.
Declare start gate before edits.
```

Paste is optional. Files are mandatory. The legacy session-governance kit is built for exactly this “CLI-A quota → CLI-B paste + files” path; the files matter more than the paste.

---

## What to adopt vs invent

Prefer existing protocols over a custom framework.

**O1. Adopt first:** [daystar7777/agent-work-mem](https://github.com/daystar7777/agent-work-mem) if you want multi-vendor memory with almost no glue (markdown + hot/warm/cold log). Works with Claude, Codex, Gemini CLI, Grok-class file agents.

**O2. Adopt first:** [Spe1977/cli-collaboration](https://github.com/Spe1977/cli-collaboration) if the failure mode is overwrite and dirty trees. It already names Claude, Codex, Gemini, and Grok, with ownership zones and a start/stop gate.

**O3. Copy the harness idea, not the brand names:** `features.json` + `progress.txt` + `init.sh` + git ratchet from Anthropic. That is the best known pattern for multi-session coding.

**O4. Optional live layer:** tmux panes (you already have a tmux skill) so co-located agents can ping each other, while the files remain canonical. agent-work-mem has a tmux handoff extension.

**O5. Do not make GitHub Agentic Workflows your memory.** Use them later for scheduled/CI agents. They run ephemeral VMs; they do not replace `AGENT_HANDOFF.md`.

Skip CrewAI/LangGraph-style in-process multi-agent for this problem. You are coordinating **separate products with separate quotas**, not functions in one Python process.

---

## What “no loss of fidelity” actually means

You cannot keep the dying model’s private chain-of-thought. You can keep:

- the ordered event log
- the code as committed
- the tests that still fail or pass
- the decisions written as constraints
- the next atomic action

That is higher fidelity for implementation than a 20k-token summary of “what Claude was thinking.”

**A1.** Bootstrap one repo with `AGENTS.md` pointers + `AGENT_HANDOFF.md` + `features.json` + the boot/closeout rules above.  
**A2.** Assign phases, not vibes: Claude plans/reviews, Codex implements, Gemini/Grok verify in a clean window.  
**A3.** Make closeout a habit before limits, not after.

If you want this dropped into `redtrades/agent-configs` as a reusable skill (handoff template + STLC gates + vendor pointers), say so and I will write that skill next.

# G1
To seamlessly pass context and execution state across different LLMs (such as Claude, OpenAI Codex/GPT, Grok, and Gemini) without losing fidelity, you cannot rely on passing raw conversation transcripts. Different models have distinct tokenizers, context window behaviors, tool-calling formats, and system prompt interpretations.


The industry standard approach is **Externalized State Management via Git as the Persistence Layer**. The repository itself—its file system, git commits, and structured state files—acts as the single source of truth.

  

# Multi-Agent STLC Architecture

In a structured Software Testing Life Cycle (STLC), each agent operates as a specialist or a sequential fallback. When an agent hits a token cap, rate limit (HTTP 429), or task budget, it commits its progress and writes a standardized state payload before handing execution to the next model.

  

```
                     +---------------------------------------+
                     |         GitHub Actions Runner         |
                     +---------------------------------------+
                                         |
     +-----------------------------------+-----------------------------------+
     |                                   |                                   |
+------------+ (429 Rate Limit)    +------------+ (Context Budget)     +------------+
| Claude 3.7 | ------------------> | OpenAI O3  | -------------------> | Gemini Pro |
+------------+                     +------------+                      +------------+
     |                                   |                                   |
     +-----------------> Writes to `.agent/` Workspace <---------------------+
                                         |
                                         v
                     +---------------------------------------+
                     |       Git Commit & Test Runner        |
                     +---------------------------------------+
```

## The STLC Phase & Agent Matrix

Each STLC stage requires specific inputs, deliverables, and validation criteria.

  

|**STLC Phase**|**Primary Agent**|**Fallback Agent**|**Primary Input**|**Produced Artifact**|**Quality Gate**|
|---|---|---|---|---|---|
|**1. Requirements & Planning**|Claude 3.7 Sonnet|Gemini 2.5 Pro|Issue / PR Spec|`TEST_PLAN.md`|Human Review / Spec Lint|
|**2. Test Case Generation**|Gemini 2.5 Flash|Grok 3|`TEST_PLAN.md`|Test Suite (`*.spec.ts`, `test_*.py`)|Syntax & Static Analysis|
|**3. Implementation & Run**|OpenAI Codex / O3|Claude 3.7 Sonnet|Test Suite + Code|Passing Code + Git Diff|CI Unit/Integration Tests|
|**4. Defect Analysis & Closure**|Grok 3 / Gemini|Claude 3.7|Test Logs + Trace|`STLC_SUMMARY.md`|100% Passing Gate|

## The Handoff Protocol: Standardized State Files

To prevent fidelity loss during transitions, never dump raw context strings into prompt variables. Maintain a reserved directory (`.agent/`) tracked in Git that every agent reads upon startup and updates upon exit.

  

### Core Persistence Files

- **`CURRENT_STATE.json` (Machine-Readable State):**
    
      
    - **Phase Tracking:** Stores current STLC phase, active subtask ID, and status (`IN_PROGRESS`, `BLOCKED`, `COMPLETED`).
        
          
        
    - **Agent Attribution:** Records the active model, handoff reason (e.g., `RATE_LIMIT_EXCEEDED`), and execution attempt count.
        
          
        
    - **Artifact Pointers:** Maps active test logs, modified file lists, and error output paths.
        
          
        
- **`ROADMAP.md` (High-Level Checkpoints):**
    
      
    - **Checklist Hierarchy:** Tracks high-level milestones broken into atomic, checkable task boxes.
        
          
        
    - **Definition of Done:** Lists strict acceptance criteria that the verifier checks before moving to the next phase.
        
          
        
    - **Scope Boundaries:** Explicitly lists "non-goals" to keep incoming agents from hallucinating extra requirements.
        
          
        
- **`DECISIONS.md` (Architectural Context Ledger):**
    
      
    - **Rationale Log:** Summarizes _why_ specific libraries, patterns, or test configurations were chosen.
        
          
        
    - **Discarded Paths:** Details failed attempts and compiler errors to prevent new agents from repeating known bugs.
        
          
        
    - **Environment Quirks:** Documents test fixtures, database mocks, and runtime dependencies discovered during runs.
        
          
        

## State Schema Example

Agents write to `.agent/CURRENT_STATE.json` at every execution milestone:

  

JSON

```
{
  "stlc_phase": "Test_Execution",
  "active_task": "TASK-04: Implement JWT Refresh Token Strategy",
  "last_successful_checkpoint": "TASK-03: Auth Middleware Unit Tests",
  "handoff_reason": "CLAUDE_RATE_LIMIT_429",
  "modified_files": [
    "src/auth/token.service.ts",
    "tests/auth/token.spec.ts"
  ],
  "next_action": "Run `npm test tests/auth/token.spec.ts` and fix failing mock assertion on line 42",
  "failing_tests": [
    "TokenService > should rotate refresh token when valid"
  ]
}
```

## GitHub Actions Orchestration Workflow

Below is a robust GitHub Actions workflow structure that executes sequential agent handoffs with automatic failover upon API exhaustion.

  

YAML

```
name: STLC Autonomous Agent Pipeline

on:
  workflow_dispatch:
  issues:
    types: [labeled]

jobs:
  run-stlc-cycle:
    if: contains(github.event.issue.labels.*.name, 'agent-stlc')
    runs-on: ubuntu-latest
    permissions:
      contents: write
      issues: write

    steps:
      - name: Check out Repository
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Set up Execution Environment
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Initialize Agent Workspace
        run: |
          mkdir -p .agent
          test -f .agent/CURRENT_STATE.json || echo '{"stlc_phase":"Planning","status":"START"}' > .agent/CURRENT_STATE.json

      - name: Run Primary Agent (Claude)
        id: primary_agent
        continue-on-error: true
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          npx ts-node .github/scripts/run-agent.ts --model=claude-3-7-sonnet

      - name: Fallback Agent (OpenAI Codex/O3)
        if: steps.primary_agent.outcome == 'failure'
        id: fallback_openai
        continue-on-error: true
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: |
          echo "Claude limit reached or failed. Triggering OpenAI with state snapshot..."
          npx ts-node .github/scripts/run-agent.ts --model=o3-mini

      - name: Fallback Agent (Gemini)
        if: steps.fallback_openai.outcome == 'failure'
        id: fallback_gemini
        env:
          GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
        run: |
          echo "OpenAI limit reached or failed. Triggering Gemini Pro..."
          npx ts-node .github/scripts/run-agent.ts --model=gemini-2.5-pro

      - name: Run Deterministic Verification
        run: |
          npm test -- --ci --bail

      - name: Commit Agent State and Diffs
        if: always()
        run: |
          git config --global user.name "Agent Orchestrator"
          git config --global user.email "agents@github-workflow.local"
          git add .agent/ src/ tests/
          git commit -m "chore(agent): handoff state update [skip ci]" || echo "No changes to commit"
          git push origin HEAD
```

## 3 Critical Safeguards Against Fidelity Loss

- **Enforce Deterministic Tooling via MCP (Model Context Protocol):**
    
      
    - **Unified Tool Interfaces:** Standardize all file editing, terminal execution, and git operations under unified MCP servers.
        
          
        
    - **Model-Agnostic Invocation:** Abstract tool calling so Claude, GPT, and Gemini call identical function signatures (`readFile`, `executeTest`).
        
          
        
    - **Zero Protocol Translation:** Prevents formatting errors when switching between different proprietary API tool specs.
        
          
        
- **Isolate Code Execution from Reasoning Traces:**
    
      
    - **Clean Commits:** Only write valid source code and structured summaries to repository files—never conversation chatter.
        
          
        
    - **Ephemeral scratchpads:** Let models use private thinking tokens, but mandate that all shared knowledge lands in `DECISIONS.md`.
        
          
        
    - **Context-Folding:** Compress historical logs into bulleted checkpoints every 3 cycles to keep incoming context payloads lean and dense.
        
          
        
- **Use Automated Quality Gates Before Phase Advancement:**
    
      
    - **Test-Driven Handoff:** An agent cannot mark a task complete in `CURRENT_STATE.json` unless the corresponding test suite passes cleanly.
        
          
        
    - **Linter and Static Checks:** Run ESLint, Prettier, or type checkers (`tsc`, `mypy`) as a GitHub step after every agent exit.
        
          
        
    - **Automatic Rollback:** If a successor agent breaks previously passing tests, git revert back to the last valid checkpoint automatically.



# G1 Research

**The optimal pattern in 2026 is “handoff-first, file-and-git as the source of truth.”** Agents start with fresh context, read durable artifacts, do scoped work, then write a structured handoff before exiting (or hitting limits). The next agent (Claude Code, Codex, Grok, Gemini CLI, OpenCode, etc.) picks up with near-zero loss of fidelity because continuity lives outside any single model’s window.

This is the dominant consensus across recent GitHub projects, X discussions, and agentic SDLC write-ups.

### Core Principles

- **Never treat conversation history as shared state.** Context windows fill, get compacted, or expire. Put goals, decisions, order-of-events, ownership, test status, and next concrete steps into version-controlled files.
- **Fresh context + structured brief** beats long-running sessions for multi-agent or limit-constrained work. Each agent (or iteration) starts clean and loads only what it needs.
- **Git is the persistence and audit layer.** Commits, branches, worktrees, issues/PRs, and diffs are the reliable record of “what has been done.”
- **Ownership + stop conditions** prevent trampling. Explicit file ownership and “stop when X” rules make sequential handoffs safe.
- **Goals live in tickets or a living plan**; progress lives in a handoff log + code + tests.

### Recommended File-Based Protocols (Best Starting Points)

These are lightweight, tool-agnostic, and already support Claude / Codex / Grok / Gemini / OpenCode:

1. **cli-collaboration (AGENT_HANDOFF.md)** — Excellent for sequential multi-CLI teams.
    - `AGENT_HANDOFF.md` is the single source of truth.
    - Every agent must read it first, declare: current task, files it will touch, expected red/green tests, reserved/frozen zones, and stop condition.
    - Ownership sections (`agent-owned`, `user-reserved`, `frozen`) + validation scripts prevent overwrites.
    - Designed exactly for Codex → Claude → Gemini → Grok handoffs (and single-agent resume across sessions).
    - Includes adapters/skills for each CLI.
2. **agent-work-mem (AIMemory/)** — Strong shared memory with tiered storage.
    - `INDEX.md` + `PROJECT_OVERVIEW.md` + append-only `work.log` (hot) → archive → cold digests.
    - Explicit handoff files (`handoff_*.md`).
    - One-prompt install; works with any file-reading agent. Optional tmux for live multi-pane delivery.
    - Prevents context bloat while preserving order of events.
3. **agent-vault** — Shared markdown blackboard (Obsidian-friendly or plain folder).
    - Append-only `events.md`, per-agent private namespaces, exclusive task ownership with handoff notes.
    - Entry pointers (`CLAUDE.md`, `AGENTS.md`, `GEMINI.md`) force every tool to load the protocol.

Other useful kits: `agent-handoff-kit` (SESSIONS.md + CONTINUE.md + branch-per-agent), simple `docs/HANDOFF.md` patterns, and master-workflow for automated loops.

**Minimal viable handoff template** (adapt from the above):

```
# AGENT_HANDOFF.md / HANDOFF.md
Last updated: <ISO timestamp> by <agent>
Goal / Issue: <link or summary>
Current status: <one paragraph + key decisions>
Files changed this session: ...
Tests: red/green + commands
Open concerns / blockers:
Next concrete step (for next agent):
Ownership:
### agent-owned
- path: AgentX — reason
### user-reserved / frozen
...
Stop condition: task-complete | usage-limit | blocker
```

### GitHub Workflows & SDLC Integration

- **Issues / PRs as goal containers.** Persist plans, decisions, and open questions as structured comments or checklists. Any agent can `gh issue view` or load context and resume.
- **Git worktrees** for isolation (especially if any parallel work occurs). Each agent or task gets its own worktree/branch; merge via PR after review.
- **GitHub Agentic Workflows + MemoryOps**: Use **Repo Memory** (dedicated branch for long-lived state) and **Cache Memory** for checkpoints. Multi-phase improvers already demonstrate multi-day sequential progress with resume-from-checkpoint.
- **master-workflow** (or similar harnesses): Deterministic loop of worker (fresh context) → git-diff review by a _different_ model → score ≥ threshold. Supports Codex, Grok, Claude, OpenCode, Kimi. Perfect when you want automatic cross-model sequential improvement until quality gates pass. Full filesystem ledger for audit/resume.
- Sequential pipeline pattern: Agent A finishes → commit + update handoff → Actions (or human) creates labeled issue / triggers next agent. Avoid concurrent writes to the same files.

### Practical Setup for Claude + Codex + Grok + Gemini + OpenCode

1. Add project entry points: `AGENTS.md`, `CLAUDE.md`, `GEMINI.md` (and any tool-specific) that all say “On start: read AGENT_HANDOFF.md / AIMemory/INDEX.md first.”
2. Install one of the protocols above (cli-collaboration or agent-work-mem is the fastest path).
3. Define roles/strengths in the handoff or a constitution file (e.g., Claude for planning/UI/semantics, Codex for backend/infra, Grok for bulk mechanical work, Gemini for QA/red-team).
4. Workflow discipline:
    - Start session → read handoff + recent git log + relevant tests.
    - Declare ownership and stop condition.
    - Work only on declared files.
    - Before exit (or when usage limit approaches): update handoff with exact next step, run/verify tests, commit with clear message, push if needed.
    - Next agent (or same agent after limit reset) loads the files and continues.
5. Optional automation: GitHub Actions that check for incomplete handoffs, run ownership validators, or trigger the next model via labels / scheduled multi-phase workflows.
6. For long SDLC: living roadmap/spec files + issue chaining + PR reviews by a different model.

### Handling Usage Limits Specifically

- Treat limit exhaustion as a normal stop condition.
- The exiting agent _must_ write a high-fidelity handoff (what was done, exact next atomic step, failing tests if any, architectural decisions).
- Prefer short, goal-oriented sessions over marathon ones.
- Use git history + test suite as the ultimate verifier of “what actually happened” (never trust an agent’s summary alone).

### Additional Patterns Seen on X and in the Wild

- tmux multi-pane for live observation while still using file handoffs as the real source of truth.
- Cross-model review loops (worker on one model, independent reviewer on another).
- Skills / MCP servers that enforce the read-handoff-first ritual.
- Avoid naive parallel execution unless worktrees + strict ownership are in place; sequential with clean handoffs is far more reliable for fidelity.

**Start here today**: Clone or one-prompt install `cli-collaboration` or `agent-work-mem`, put a real goal in a GitHub issue, create the initial `AGENT_HANDOFF.md`, and run the first agent. When it approaches its limit, force the handoff update and switch. You will immediately see continuity without loss of order-of-events or implementation context.

This approach scales from single-developer multi-model switching all the way to more automated agentic SDLC pipelines while remaining inspectable, auditable, and resilient to any single model’s limits.


# C1
Yes. I think you mean **GitHub workflows + SDLC** rather than “kid hub/STLC.” I looked at the current cross-agent tooling and patterns, including projects specifically designed for Claude Code ↔ Codex ↔ Gemini handoffs.

The key conclusion is that **you should not attempt to transfer the agents' conversational context**. There is still no reliable universal serialization format for Claude/Codex/Gemini/Grok sessions. The optimal design is to make the **repository itself the authoritative memory/state machine**, so whichever model starts next reconstructs the exact working state from Git + structured artifacts. ([Zylos](https://zylos.ai/research/2026-05-03-ai-agent-multi-runtime-permission-architectures/?utm_source=chatgpt.com "AI Agent Multi-Runtime Permission Architectures: Claude Code, Codex CLI, and Gemini CLI in Production | Zylos Research"))

For what you're describing, I'd build the system like this.

## The architecture I would use

```text
                     ┌─────────────────────┐
                     │      USER GOAL      │
                     │ "Optimize Hermes..."│
                     └──────────┬──────────┘
                                │
                         ORCHESTRATOR
                     determines next work unit
                                │
               ┌────────────────┴───────────────┐
               │                                │
        canonical state                   Git repository
               │                                │
    ┌──────────▼───────────┐         ┌─────────▼────────┐
    │ .agent/              │         │ branches/commits │
    │ STATE.yaml           │         │ tests/evals      │
    │ GOAL.md              │         │ implementation   │
    │ PLAN.md              │         │ artifacts        │
    │ DECISIONS.md         │         └──────────────────┘
    │ EVENTS.jsonl         │
    │ HANDOFF.md           │
    │ EVIDENCE/            │
    └──────────┬───────────┘
               │
      ┌────────┴──────────────────────────────────┐
      │                                           │
      ▼                                           ▼
 Claude ──→ Codex ──→ Gemini ──→ Grok ──→ Claude ...
  │          │           │          │
  └──────────┴───────────┴──────────┘
        SAME STATE, DIFFERENT MODEL
```

The important distinction is:

**Git is the truth.  
The event log is the history.  
HANDOFF.md is the current mental snapshot.  
The agent's conversation is disposable cache.**

That last sentence is the design principle I'd enforce.

---

# 1. Use one canonical instruction file

Don't maintain four independently evolving versions of the project instructions.

I'd make:

```text
AGENTS.md              ← canonical
CLAUDE.md
GEMINI.md
.grok/...
```

with the vendor-specific files effectively pointing the agent to the canonical state.

For example:

```md
# CLAUDE.md

Read and obey ./AGENTS.md.

Before doing any work:
1. Read .agent/STATE.yaml
2. Read .agent/GOAL.md
3. Read .agent/HANDOFF.md
4. Inspect git status/log
5. Read any files listed in STATE.yaml.required_context
```

Claude supports project-level `CLAUDE.md` memory and imports; Gemini has hierarchical `GEMINI.md` and can import other Markdown files. Gemini can even be configured to treat `AGENTS.md` as a context filename. ([Claude Platform Docs](https://docs.anthropic.com/zh-CN/docs/claude-code/memory?utm_source=chatgpt.com "管理 Claude 的内存 - Anthropic"))

Gemini's current CLI also supports `/memory show` and `/memory reload`, which gives you a useful way of verifying what context actually made it into the model. ([GitHub](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/tutorials/memory-management.md?utm_source=chatgpt.com "gemini-cli/docs/cli/tutorials/memory-management.md at main · google-gemini/gemini-cli · GitHub"))

So I'd make **AGENTS.md the invariant operating constitution**, not the project diary.

---

# 2. Separate durable knowledge from transient working state

This is one of the most important improvements.

Don't make a gigantic 30K-token `AGENTS.md`.

Use:

```text
.agent/
├── GOAL.md
├── STATE.yaml
├── PLAN.md
├── HANDOFF.md
├── DECISIONS.md
├── EVENTS.jsonl
├── FAILURES.md
├── FINDINGS.md
├── EVALS.md
├── agents/
│   ├── claude.md
│   ├── codex.md
│   ├── gemini.md
│   └── grok.md
├── tasks/
│   ├── T001.yaml
│   ├── T002.yaml
│   └── ...
└── evidence/
```

There are really **four different kinds of memory**.

|Layer|Purpose|
|---|---|
|`AGENTS.md`|Stable rules|
|`GOAL.md`|What the user ultimately wants|
|`STATE.yaml`|Machine-readable current state|
|Git + `EVENTS.jsonl`|Exact historical record|

Then `HANDOFF.md` is merely an optimized cache of that information for the next model.

This mirrors what the better cross-agent projects are converging on. `coding-agent-toolkit`, for example, explicitly separates persistent memory, transition/handoff records, and active work units. ([GitHub](https://github.com/stefan-jansen/coding-agent-toolkit?utm_source=chatgpt.com "GitHub - stefan-jansen/coding-agent-toolkit: Cross-agent workflow toolkit (Claude Code + Codex) — align/plan/ship/handoff verbs with shared .workspace/ as the host-swap primitive · GitHub"))

AIPass similarly externalizes persistent identity/state rather than relying on a CLI's conversation history. ([Codex Knowledge Base](https://codex.danielvaughan.com/2026/04/12/aipass-persistent-multi-agent-framework-codex-claude-gemini/?utm_source=chatgpt.com "AIPass: Persistent Multi-Agent Collaboration Across Codex CLI, Claude Code, and Gemini CLI | Codex Knowledge Base"))

---

# 3. Make STATE.yaml the source of current execution state

This is where I would depart from a lot of the Markdown-only implementations.

Markdown is excellent for models.

It isn't ideal for orchestration.

Use both.

Something along these lines:

```yaml
schema_version: 1

goal:
  id: hermes-perf-001
  status: active

phase: benchmark

current_task:
  id: T017
  title: benchmark-qwen38-mtp
  status: running

agent:
  current: claude
  session_id: null
  started_at: 2026-08-27T03:00:00-04:00

git:
  branch: agent/T017-qwen38-mtp
  base: main
  last_verified_commit: a891c2f

verification:
  tests: passed
  benchmark: partial
  regression: unknown

next_actions:
  - finish 32K-context benchmark
  - compare MTP enabled/disabled
  - update benchmark matrix

blocked_by: []

required_context:
  - docs/architecture.md
  - .agent/EVALS.md
  - benchmarks/results/qwen38.json

last_event: 1847
```

A new agent can understand this in seconds.

More importantly, **your orchestrator can understand it without asking an LLM**.

---

# 4. Maintain an append-only event ledger

This solves your concern about:

> understanding of the order of events and what has been done

Don't depend on summaries for chronology.

Have every significant action append something like:

```json
{"seq":1841,"agent":"claude","type":"task_started","task":"T017","ts":"..."}
{"seq":1842,"agent":"claude","type":"command","cmd":"pytest tests/...","result":"pass"}
{"seq":1843,"agent":"claude","type":"decision","id":"D042"}
{"seq":1844,"agent":"claude","type":"benchmark","artifact":"results/run-91.json"}
{"seq":1845,"agent":"claude","type":"commit","sha":"a891c2f"}
{"seq":1846,"agent":"claude","type":"quota_warning"}
{"seq":1847,"agent":"claude","type":"handoff","to":"codex"}
```

`EVENTS.jsonl` should be append-only.

That gives you an audit trail that isn't susceptible to an LLM rewriting history.

This is also a stronger version of the `work.log` approach used by `agent-work-mem`, which records prompts, decisions, actions, tests, and handoffs in shared files. ([GitHub](https://github.com/daystar7777/agent-work-mem?utm_source=chatgpt.com "GitHub - daystar7777/agent-work-mem: Persistent shared memory and handoffs across any combination of AI coding agents — Claude Code, Codex CLI, Cursor, Aider — using nothing but markdown. · GitHub"))

---

# 5. Use Git as the implementation checkpoint

This matters more than preserving 100% of a conversation.

Imagine Claude has modified:

```text
server.py
scheduler.py
benchmark.py
```

and hits its Max quota.

Codex doesn't actually need Claude's complete 60,000-token conversation.

It needs:

```text
Goal
↓
Why the chosen approach was selected
↓
Current Git SHA
↓
Uncommitted diff
↓
Tests run
↓
Tests not run
↓
Known failures
↓
Next operation
```

I would therefore require an agent to checkpoint periodically:

```text
git commit
     ↓
run tests
     ↓
record resulting SHA
     ↓
update STATE
```

not only when its session is ending.

A lot of current cross-agent tooling is converging on this exact insight: Git transports implementation state while structured handoff records transport intent and rationale. ([Handover](https://handover.sh/guides/preserve-context-across-ai-coding-agents?utm_source=chatgpt.com "How to preserve context across AI coding agents · Handover"))

---

# 6. Make every task atomic

The SDLC layer should break:

> "Optimize Hermes on my M1 Max"

into a DAG, not one giant prompt.

For example:

```text
G001 Optimize Hermes
 │
 ├─ T001 Inventory current implementation
 ├─ T002 Reproduce baseline
 ├─ T003 Validate benchmark harness
 │
 ├─ T004 MLX engine analysis
 ├─ T005 OMLX engine analysis
 ├─ T006 llama.cpp analysis
 │
 ├─ T007 MTP experiment
 ├─ T008 KV cache experiment
 ├─ T009 quantization experiment
 ├─ T010 32K prefill experiment
 │
 ├─ T011 concurrency 1
 ├─ T012 concurrency 2
 ├─ T013 concurrency 3
 ├─ T014 concurrency 4
 │
 ├─ T015 adversarial analysis
 ├─ T016 reproduce winning config
 └─ T017 Hermes end-to-end validation
```

Each task has:

```yaml
inputs:
outputs:
acceptance_criteria:
dependencies:
verification:
status:
agent_history:
```

Then it doesn't matter if:

Claude does T001–T004,

Codex does T005–T009,

Claude comes back,

Gemini reviews T010,

Grok researches T011,

etc.

The **task graph remains continuous even though the intelligence executing it changes**.

This is essentially the strongest aspect of the newer AI-native SDLC patterns: every stage produces a versioned artifact that becomes the input to the next stage rather than relying on conversational continuity. ([GitHub](https://github.com/bashebr/ai-native-sdlc?utm_source=chatgpt.com "GitHub - bashebr/ai-native-sdlc: AI-native SDLC workflow as a reusable Codex and Claude Code skill and plugin · GitHub"))

---

# 7. Handoffs should contain evidence, not just prose

I'd enforce a handoff contract like:

```text
HANDOFF
────────────────────────

TASK
T017

OBJECTIVE
...

STATUS
73% complete

LAST KNOWN GOOD
commit a891c2f

FILES MODIFIED
scheduler.py
benchmark.py

IMPLEMENTED
...

NOT IMPLEMENTED
...

DECISIONS
D039
D041
D042

FAILED APPROACHES
F011 – MTP=4 caused...
F012 – mmap configuration...

VERIFICATION
unit: PASS
integration: PASS
benchmark: PARTIAL
Hermes E2E: NOT RUN

ARTIFACTS
results/run91.json
results/run92.json

CURRENT HYPOTHESIS
...

NEXT EXACT ACTION
Run:
python benchmark.py ...

DO NOT
repeat experiment #91
change KV quantization until T018

OPEN QUESTIONS
...
```

Notice **NEXT EXACT ACTION**.

That's extremely useful.

A new model shouldn't spend its first 20 minutes wondering what to do.

The portable `handoff` project I found captures almost exactly these classes of information: current summary, next action, open tasks, key decisions, blockers, files touched, files to read first, and verification state. ([GitHub](https://github.com/AniruddhaHumane/handoff?utm_source=chatgpt.com "GitHub - AniruddhaHumane/handoff: Save and resume coding-agent context across Codex, Claude, and parallel agent workflows. · GitHub"))

---

# 8. Then agent rotation becomes trivial

Your supervisor becomes:

```text
while goal != DONE:

    load STATE

    choose next runnable task

    choose available agent

    start agent

    agent reads canonical state

    agent works

    periodic checkpoint()

    if task_complete:
        verify()
        transition()

    if quota_exhausted:
        checkpoint()
        produce_handoff()
        release_lease()
        choose_next_agent()
```

So:

```text
Claude
   │
   ├── quota remaining
   │       └── continue
   │
   └── quota exceeded
           │
           ▼
      atomic checkpoint
           │
           ▼
        Codex
           │
           └── reconstruct state
                 from Git +
                 STATE +
                 HANDOFF +
                 evidence
```

**This is much better than trying to export Claude's entire conversation into Codex.**

---

# 9. Use a lease so two agents don't accidentally own the same task

Something like:

```yaml
lease:
  task: T017
  holder: codex
  acquired: 2026-08-27T03:07:21-04:00
  heartbeat: 2026-08-27T03:08:54-04:00
  expires_seconds: 300
```

When Claude disappears because of usage limits:

```text
heartbeat expires
       ↓
task becomes resumable
       ↓
Codex claims lease
```

This also lets you eventually run parallel agents safely.

The OpenMOSS Claude/Codex handoff project uses **atomic leases, per-session cursors and append-only message streams**, which is a good model for this part. ([GitHub](https://github.com/OpenMOSS/claude-codex-handoff?utm_source=chatgpt.com "GitHub - OpenMOSS/claude-codex-handoff: Drop-in async file-based handoff protocol for two AI coding agents (Claude Code + Codex), installed as one shared .handoff/ in your project. · GitHub"))

---

# 10. Don't let every agent edit the same branch concurrently

For sequential rotation within **one task**, the next model can inherit the same branch.

For parallel work use:

```text
worktree/
   T021-claude/
   T022-codex/
   T023-gemini/
   T024-grok/
```

and:

```text
agent/T021-claude
agent/T022-codex
agent/T023-gemini
agent/T024-grok
```

Merge only after acceptance criteria pass.

This avoids the nightmare where Gemini changes a file while Claude is reasoning from its previous contents.

---

# 11. Make models verify the previous agent before continuing

This is a huge fidelity improvement.

When Codex takes over from Claude, don't prompt:

> Continue Claude's work.

Instead:

```text
1. Load STATE.
2. Inspect Git SHA and working tree.
3. Read HANDOFF.
4. Verify claimed completed work against repository state.
5. Verify tests/results referenced in the handoff.
6. Compare STATE with event-log tail.
7. Report inconsistencies.
8. Only then continue NEXT_ACTION.
```

So handoffs are **trust-but-verify**.

That prevents one agent's hallucinated state from becoming institutional truth.

---

# 12. GitHub should be the high-level coordination/control plane

I'd map the SDLC into GitHub like this:

```text
GitHub Issue
    = goal / feature / experiment

Sub-issues
    = atomic tasks

Labels
    = state
      ready
      active
      blocked
      verification
      done

Branch
    = implementation state

Commit
    = checkpoint

PR
    = integration boundary

Checks
    = deterministic validation

Artifacts
    = benchmarks/logs/evals

.agent/
    = agent cognitive state
```

GitHub Actions then validates the state transitions:

```text
Agent says DONE
       ↓
GitHub Action
       ↓
lint
tests
integration tests
benchmark sanity
artifact existence
schema validation
       ↓
PASS
       ↓
task becomes VERIFIED
```

The crucial point:

### The LLM should not be allowed to declare its own work correct.

It may declare:

```text
implementation_complete
```

but deterministic checks determine:

```text
verified
```

---

# 13. Claude/Codex/Gemini/Grok should have roles, but not permanent ownership

I'd initially configure:

|Agent|Preferred work|
|---|---|
|Claude|architecture, long-horizon implementation, repo understanding|
|Codex|implementation, debugging, code review, tests|
|Gemini|very large-context inspection, independent review/research|
|Grok|external research, alternative hypotheses, adversarial analysis|

But make this a **routing preference rather than a requirement**.

If Claude hits quota:

```text
Claude → Codex
```

If Codex hits quota:

```text
Codex → Gemini
```

If Gemini hits quota:

```text
Gemini → Grok
```

If Claude becomes available:

```text
Grok → Claude
```

Any model must be capable of taking any task.

That eliminates provider dependence.

---

# 14. Don't dump the entire history into every new context

This sounds counterintuitive, but it's important.

Suppose your project eventually accumulates:

```text
8 million tokens of conversations
4,000 commands
600 commits
900 benchmark runs
```

Do **not** recreate all of that.

Use hierarchical retrieval:

```text
L0 ~ 1K tokens
STATE.yaml
current objective

L1 ~ 2-4K
HANDOFF.md
active task

L2 ~ 5-10K
relevant decisions/findings

L3
specific source files

L4
historical event log / old benchmarks

L5
raw historical transcripts
```

Only go deeper when needed.

This is also where Gemini's hierarchical context mechanism is useful; Google's docs explicitly recommend focused project context rather than indiscriminately expanding `GEMINI.md`. ([GitHub](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/tutorials/memory-management.md?utm_source=chatgpt.com "gemini-cli/docs/cli/tutorials/memory-management.md at main · google-gemini/gemini-cli · GitHub"))

---

# 15. Preserve raw transcripts anyway

Although they shouldn't be your working memory, I **would** archive native transcripts.

Something like:

```text
.agent/transcripts/
  2026-08-27/
    claude-S341.jsonl
    codex-S912.jsonl
    gemini-S114.json
```

This gives the next model an escape hatch:

> I need to know exactly why Claude rejected approach B.

Then retrieve that specific section.

Projects such as `continues` are already parsing the different local session stores specifically to produce cross-agent handoffs, because Claude, Codex and Gemini maintain incompatible native session formats. ([Codex Knowledge Base](https://codex.danielvaughan.com/2026/06/01/codex-cli-cross-agent-session-portability-continues-casr-handoff/?utm_source=chatgpt.com "Cross-Agent Session Portability: Moving Codex CLI Sessions Between Coding Agents | Codex Knowledge Base"))

So I would preserve them as **cold storage**, not primary memory.

---

# The resulting SDLC

I'd use:

```text
INTAKE
  ↓
GOAL
  ↓
RESEARCH
  ↓
REQUIREMENTS
  ↓
ACCEPTANCE CRITERIA
  ↓
ARCHITECTURE
  ↓
TASK DAG
  ↓
IMPLEMENT
  ↓
TEST
  ↓
ADVERSARIAL REVIEW
  ↓
EVALUATE
  ↓
INTEGRATE
  ↓
END-TO-END VERIFICATION
  ↓
RETROSPECTIVE / MEMORY UPDATE
  ↓
DONE
```

But importantly, **the agent identity is orthogonal to this sequence**:

```text
Goal
 │
 ├── Research ───────── Gemini
 ├── Architecture ───── Claude
 ├── Implement ──────── Codex
 ├── Review ─────────── Grok
 ├── Fix ────────────── Claude
 ├── Benchmark ──────── Codex
 └── Final verification Gemini
```

or:

```text
Claude ─ quota ─┐
                ▼
Codex ─ quota ──┐
                ▼
Gemini ─ quota ─┐
                ▼
Grok ───────────┐
                ▼
Claude
```

The **workflow continues irrespective of who is executing it**.

---

# What I would use from the existing projects

After looking at the currently available systems, I **wouldn't simply adopt one wholesale**.

I would borrow:

**From `coding-agent-toolkit`:**  
`.workspace`-style shared state and explicit `handoff/continue`. ([GitHub](https://github.com/stefan-jansen/coding-agent-toolkit?utm_source=chatgpt.com "GitHub - stefan-jansen/coding-agent-toolkit: Cross-agent workflow toolkit (Claude Code + Codex) — align/plan/ship/handoff verbs with shared .workspace/ as the host-swap primitive · GitHub"))

**From `agent-handoff`:**  
structured snapshots and next-action handoffs. ([GitHub](https://github.com/AniruddhaHumane/handoff?utm_source=chatgpt.com "GitHub - AniruddhaHumane/handoff: Save and resume coding-agent context across Codex, Claude, and parallel agent workflows. · GitHub"))

**From `agent-work-mem`:**  
shared chronological work log. ([GitHub](https://github.com/daystar7777/agent-work-mem?utm_source=chatgpt.com "GitHub - daystar7777/agent-work-mem: Persistent shared memory and handoffs across any combination of AI coding agents — Claude Code, Codex CLI, Cursor, Aider — using nothing but markdown. · GitHub"))

**From OpenMOSS:**  
append-only channels + leases + cursors. ([GitHub](https://github.com/OpenMOSS/claude-codex-handoff?utm_source=chatgpt.com "GitHub - OpenMOSS/claude-codex-handoff: Drop-in async file-based handoff protocol for two AI coding agents (Claude Code + Codex), installed as one shared .handoff/ in your project. · GitHub"))

**From AI-native SDLC:**  
versioned artifact at every lifecycle transition. ([GitHub](https://github.com/bashebr/ai-native-sdlc?utm_source=chatgpt.com "GitHub - bashebr/ai-native-sdlc: AI-native SDLC workflow as a reusable Codex and Claude Code skill and plugin · GitHub"))

**From native Claude/Gemini/Codex capabilities:**  
provider-specific bootstrap files that point back into the common protocol rather than duplicating it. Claude and Gemini already have strong repo-level memory primitives for this. ([Claude Platform Docs](https://docs.anthropic.com/zh-CN/docs/claude-code/memory?utm_source=chatgpt.com "管理 Claude 的内存 - Anthropic"))

---

# What I think is optimal for your setup

I would actually build a small **provider-neutral agent supervisor** rather than make GitHub Actions itself the orchestrator.

```text
                    agentd
              ┌────────┴────────┐
              │                 │
        workflow engine    quota/router
              │                 │
      ┌───────┴──────────┐      │
      │                  │      │
 Git + .agent/       GitHub API │
      │                  │      │
      └──────────┬───────┘      │
                 │              │
       ┌─────────┼──────────────┼───────┐
       ▼         ▼              ▼       ▼
    Claude     Codex         Gemini    Grok
```

`agentd` would be deterministic code, **not another LLM**.

Its responsibilities would only be:

```text
read workflow state
claim task
select provider
launch CLI
observe process
checkpoint
detect quota/error
rotate provider
run validation
update GitHub
repeat
```

The LLM handles intelligence.

The supervisor handles reliability.

That separation is extremely important.

### The objective isn't actually “perfect context transfer.”

It is:

> **Make model replacement indistinguishable from a process restart.**

If we accomplish that, Claude can disappear at token 150,000, Codex can start 10 seconds later with a fresh context window, and the **software-development state has lost essentially nothing that matters**.

That's considerably more robust than trying to keep four enormous conversations synchronized.

Given your use case, I'd make **Git + `.agent/STATE.yaml` + append-only `EVENTS.jsonl` + task DAG + evidence-backed `HANDOFF.md`** the core, with Claude/Codex/Gemini/Grok treated as hot-swappable execution engines. That's the architecture I'd choose over any of the individual handoff projects I found.


P1
To achieve continuous, high-fidelity handoffs across heterogeneous AI models (Claude, Codex, Grok, Gemini, DeepSeek, etc.) when hitting rate limits or quota boundaries, you must **separate ephemeral model conversational context from persistent SDLC state**.[[mindstudio](https://www.mindstudio.ai/blog/workflow-state-vs-session-state-ai-agents)]

Treat the Git repository, pull requests, and structured issue state machines as the single source of truth.[[mindstudio](https://www.mindstudio.ai/blog/workflow-state-vs-session-state-ai-agents)][[fiddler](https://www.fiddler.ai/blog/github-ai-agents-dev-workflow)]

---

## 1. Context Decoupling and State Architecture

Never pass raw multi-turn conversation transcripts directly between heterogeneous models. Different LLMs parse system prompts, function calling, and conversation formatting differently, leading to context degradation and prompt bloat.[[epam](https://www.epam.com/insights/ai/blogs/single-responsibility-agents-and-multi-agent-workflows)]

Maintain three distinct state tiers:[[mindstudio](https://www.mindstudio.ai/blog/workflow-state-vs-session-state-ai-agents)][[nhimg](https://nhimg.org/articles/github-issue-persistence-for-ai-agent-workflows-and-auditability/)]

```
┌──────────────────────────────────────────────────────────┐
│ 1. Immutable Spec & Rules (AGENTS.md / Issue Spec)       │
├──────────────────────────────────────────────────────────┤
│ 2. Structured Task State Machine (state.json in PR/Task) │
├──────────────────────────────────────────────────────────┤
│ 3. Working Memory & Scratchpad (CHANGELOG/Handoff note)  │
└──────────────────────────────────────────────────────────┘
```

1. **Static Specification Layer (`AGENTS.md` / Issue Body):** Fixed repository architecture guidelines, test commands, linting rules, and acceptance criteria.[[nhimg](https://nhimg.org/articles/github-issue-persistence-for-ai-agent-workflows-and-auditability/)]
2. **Machine-Readable State Machine (`.github/agent_state.json` or Issue Frontmatter):**

```
{
  "task_id": "issue-142",
  "branch": "agent/feature-oauth2",
  "goal": "Implement GitHub OAuth login with refresh token rotation",
  "phases": [
    {"id": 1, "name": "DB Schema", "status": "completed", "agent": "claude-3-7-sonnet"},
    {"id": 2, "name": "Auth Service Core", "status": "in_progress", "agent": "gemini-2.5-pro"},
    {"id": 3, "name": "Unit/Integration Tests", "status": "pending", "agent": null}
  ],
  "last_checkpoint": {
    "commit_sha": "a1b2c3d4",
    "active_subtask": "Validate JWT expiry middleware",
    "unresolved_blockers": ["Need mock for provider auth endpoint"],
    "files_modified": ["src/auth/jwt.py", "src/auth/routes.py"]
  }
}
```

3. **Execution Scratchpad / Handoff Memo (`HANDOFF.md` or Issue Comment):** A 200-word delta log written by the exiting agent detailing:

- What was completed in the latest commit.
- What specific function/test is failing or in-flight.
- Exactly what the next agent must execute next.[[fiddler](https://www.fiddler.ai/blog/github-ai-agents-dev-workflow)]

---

## 2. GitHub-Native Orchestration Workflow

Run your orchestrator as a GitHub Actions matrix workflow, or via an external orchestration worker (e.g., Temporal, OpenClaw, or a lightweight Python CLI) triggered via `workflow_dispatch` or issue comments.[[fiddler](https://www.fiddler.ai/blog/github-ai-agents-dev-workflow)]

```
                  ┌────────────────────────┐
                  │ GitHub Action Trigger  │
                  └───────────┬────────────┘
                              │
                  ┌───────────▼────────────┐
                  │ Load agent_state.json  │
                  └───────────┬────────────┘
                              │
                    ┌─────────▼──────────┐
          ┌────────►│ Active Agent (CLI) │
          │         └─────────┬──────────┘
          │                   │
    429 / Quota Error?        ├─ Success ─► [Commit, Update State, Next Step]
          │                   │
          ▼                   │
  [Handoff Dump]              │
  [Switch Provider]           │
          │                   │
          └───────────────────┘
```

### Handoff Protocol on 429 / Usage Limit

1. **Trap the Exit:** Wrap API calls with an error handler checking for HTTP 429 / quota errors.[[github](https://github.com/NousResearch/hermes-agent/issues/24996)][[tamirdresher](https://www.tamirdresher.com/blog/2026/03/21/rate-limiting-multi-agent)]
2. **Auto-Stash & Commit:** The orchestrator stages current changes (`git add . && git commit -m "agent(checkpoint): pre-switch state"`).
3. **Write Handoff Artifact:** The outgoing agent (or a lightweight local backup model) outputs the `HANDOFF.md` summary.[[fiddler](https://www.fiddler.ai/blog/github-ai-agents-dev-workflow)]
4. **Fallback Switch:** The orchestrator switches the routing gateway (`active_provider = fallback_chain.pop()`) and initializes the next model with the standardized prompt bundle.[[github](https://github.com/NousResearch/hermes-agent/issues/24996)][[github](https://github.com/code-yeongyu/oh-my-openagent/issues/326)]

---

## 3. Standardized Context Ingestion Template

Whenever any new agent picks up a task, compile its prompt dynamically using this standardized skeleton:

```
# Role & Global Instructions
Refer to repository guidelines defined in `AGENTS.md`.

# Primary Goal
{{ issue.body }}

# Workflow State & Progress
Completed steps:
- [x] Phase 1: DB Schema (Validated)
Current subtask:
- [ ] Phase 2: Auth Service Core (In progress)

# Handoff Memo from Prior Agent
{{ latest_handoff_comment }}

# Verification Command
Run `pytest tests/auth/ -v` to check the current test suite state.
```

---

## 4. Multi-Agent SDLC Strategy Comparison

|Strategy|Context Overhead|Provider Compatibility|Failure Recovery|
|---|---|---|---|
|**Raw History Passing**|Extreme (token-heavy)|Poor (prompt format mismatches) [[epam](https://www.epam.com/insights/ai/blogs/single-responsibility-agents-and-multi-agent-workflows)]|Low (cascades errors)|
|**Model Context Protocol (MCP)**|Low to Medium|High (schema-governed tool calls) [[github](https://github.blog/ai-and-ml/generative-ai/multi-agent-workflows-often-fail-heres-how-to-engineer-ones-that-dont/)][[github](https://github.com/resources/articles/what-are-multi-agent-systems)]|High (standardized tool execution)|
|**Git-State-Machine Pattern**|Minimal (scoped deltas)|Universal (any CLI or model) [[fiddler](https://www.fiddler.ai/blog/github-ai-agents-dev-workflow)][[mindstudio](https://www.mindstudio.ai/blog/workflow-state-vs-session-state-ai-agents)]|Very High (fully traceable in Git) [[github](https://github.com/microsoft/autogen/discussions/7144)]|

---

## 5. Practical Implementation Checklist

- **Use Git Commits as Savepoints:** Ensure the workflow forces a commit whenever a unit test passes or an individual file edit completes.
- **Enforce Deterministic Tool Schemas:** Standardize file editing, command execution, and code inspection across all agents using the **Model Context Protocol (MCP)**.[[github](https://github.blog/ai-and-ml/generative-ai/multi-agent-workflows-often-fail-heres-how-to-engineer-ones-that-dont/)][[github](https://github.com/resources/articles/what-are-multi-agent-systems)]
- **Automate Verification:** Require the incoming agent to execute the existing test suite first to verify its baseline understanding before writing new code.
- **Use Issue Threads as the Ledger:** Post state changes and handoff summaries directly as PR/Issue comments to make context persistent, inspectable, and immune to local memory crashes.[[fiddler](https://www.fiddler.ai/blog/github-ai-agents-dev-workflow)][[nhimg](https://nhimg.org/articles/github-issue-persistence-for-ai-agent-workflows-and-auditability/)]

C1
# Bottom Line

**No cross-runtime session format exists — so stop trying to move context, and move _state_ instead.** No cross-framework serialization standard exists in production as of mid-2026. An agent session in Claude Code cannot hand off directly to a Codex container with its full context intact — each transition is a cold start. The winning pattern is to make the repo the memory, so a cold start costs you 90 seconds instead of 20 minutes.

_(Reading "kid hub" as GitHub and STLC/SDLC as your lifecycle gates — say the word if you meant something else.)_

---

## The Architecture: Four Layers

|Layer|Artifact|Changes|Who reads it|
|---|---|---|---|
|**Durable rules**|`AGENTS.md` (+ `CLAUDE.md` with `@AGENTS.md` import)|Rarely|Every agent, every session|
|**Living spec**|`specs/<feature>/{requirements,design,tasks}.md`|Per feature|Agent at task start|
|**Order of events**|GitHub Issues + Milestones + PR history|Per task|Agent at session start|
|**Volatile handoff**|`HANDOFF_<date>_<branch>_<topic>.md`|Per session|Next agent, first thing|

AGENTS.md is the cross-tool standard — 30+ agents read it, including Codex, Copilot, Cursor, Gemini CLI, and Aider, now stewarded by the Agentic AI Foundation at the Linux Foundation. Claude Code is the exception: it still loads CLAUDE.md, so point one at the other with a first-line `@AGENTS.md` import. Keep the root file to 20–30 lines — duplicating your README measurably hurts agent performance.

---

## The Handoff Contract

Treat it as **typed state, not prose**. This schema is the highest-leverage thing in the whole setup:

|Field|Value|Why|
|---|---|---|
|`status`|`active` / `blocked` / `done` / `stale`|Stops stale files posing as live ones|
|`branch`|Exact git branch|Prevents cross-branch drift|
|`goal`|One-sentence outcome|Keeps the fresh session narrow|
|`next-action`|Single executable step|Kills startup hesitation|
|`do-not`|Dead ends already tried|Stops re-running failed loops|
|`evidence`|Test command + last failing output|Verifiable ground truth|

The hard part is not writing a handoff file — it's quickly proving that a handoff is yours, current, and actionable before you spend tokens in the wrong branch. Once you run parallel sessions, handoffs become distributed-systems state management, not personal notes.

The `do-not` list is the field most people skip and the one that saves the most tokens.

---

## GitHub as the Sequencer

Don't let "what's been done" live in anyone's context window. Bind it to durable objects:

- **One Issue per task**, Milestones per phase, labels for priority/lane. A resuming agent queries issue state rather than reading history.
- **A `MASTER.md` index** in-repo that mirrors the board. If a session is interrupted, the agent resumes by reading the progress index at the start of a new session, then queries GitHub for the latest issue states — PRs may have been merged since.
- **Squash-merge with structured PR bodies.** Git log becomes the audit trail of order-of-events.

---

## Lifecycle Gates (Your STLC/SDLC Hook)

The handoff is a _claim_; the test suite is the _proof_. Bake this into the ritual:

1. **Preflight** — new agent runs `npm test` (or equivalent) before touching anything. Red/green state re-establishes reality in ~60 seconds, no trust required.
2. **Definition of done per task** — EARS-style acceptance criteria in `tasks.md`, so "done" isn't a vibe.
3. **Postflight** — agent updates `status`, appends evidence, commits the handoff **on the same branch** before it dies.
4. **CI validator** — a GitHub Action that fails if `HANDOFF` frontmatter is malformed, the branch doesn't match, or a file is >N hours old without a status change.

That validator is what turns discipline into infrastructure. Without it, this decays in about a week.

---

## Handling the Limit Wall Specifically

Two different problems people conflate:

|Situation|Solution|
|---|---|
|**API key hits 429**|Gateway-level failover (LiteLLM, agentgateway) — priority-based fallback across providers when models are rate-limited|
|**Subscription CLI limit (Claude Code / Codex plans)**|Artifact handoff only. No gateway helps — the _harness_ is gated, not the model|

For the second case, the practical trick is a **budget-aware checkpoint**: instruct each agent in `AGENTS.md` to write/refresh the handoff at natural task boundaries, not when it feels close to the limit. Agents are bad at predicting their own exhaustion — checkpoint on _task completion_, so the worst case is losing one task, not one session.

**Tools worth evaluating** rather than building from scratch:

- `akitaonrails/ai-memory` — a shared persistent wiki compiled from sanitized lifecycle observations; when a session ends, the next agent receives a bounded handoff, with native per-harness resume for higher-fidelity cross-harness continuity
- **GitHub Spec Kit** — the Specify → Plan → Tasks → Implement flow with executable specifications
- **Session-bridge converters** — but note the hard-won lesson: strip tool calls; mapping one CLI's edit format to another's works sometimes and breaks spectacularly otherwise. A universal markdown fallback is lower-tech and higher reliability.

---

## Fit With Your Homelab

Cron is the natural owner here — give it the watchdog role: flag handoffs that go stale, auto-set `status: stale` past an inactivity window, and post the resume prompt into Discord when a rate-limited agent's window resets. That turns the relay from a manual ritual into a scheduled one, and it reuses routing you've already built rather than adding a fourth orchestration layer.

One caution on Grok in this lineup: its harness ecosystem is thinner on `AGENTS.md` native support than Codex or Gemini CLI, so plan on an explicit "read this file first" bootstrap prompt for it rather than assuming auto-load.