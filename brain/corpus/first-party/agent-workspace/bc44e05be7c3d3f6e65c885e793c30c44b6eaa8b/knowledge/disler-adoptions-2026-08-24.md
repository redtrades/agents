# Disler (IndyDevDan) pattern adoptions — 2026-08-24

**Superseded as the live copy 2026-08-24, same day.** Mike redirected all
disler-adoption content to a new dedicated repo, `~/agent-configs`
(`redtrades/agent-configs`) — universal rules/skills/hooks/prompts/roles
don't belong scattered across `govcon-factory`/`agent-workspace`. Every
item below now has a canonical, reorganized copy under `agent-configs/
{rules,skills,hooks,prompts,roles}/` — see that repo's `MASTER-GUIDE.md`
§7 for the item-by-item mapping. This file stays as the historical record
of the first (superseded) install pass; treat `agent-configs` as
authoritative for content, this file as authoritative for what happened
and when.

Mechanical-install phase of `knowledge/disler-github-survey-2026-08-24.md`'s
adoption shortlist. This file is both the pattern reference and, per this
repo's convention (git history + `knowledge/` docs are the audit trail, no
separate CHANGELOG), the changelog entry for that install. Everything below
was read from a fresh shallow clone in `~/agent-workspace/.tmp-disler-install/`
(scratch, not tracked, removed after this doc was written — see cleanup note
at the end) and is quoted or reimplemented per its license as noted per item.

Two things installed alongside this doc, not repeated here in full:
- `~/.claude/hooks/damage-control/` — a YAML-driven PreToolUse hook set
  (`claude-code-damage-control`, MIT), adapted with Mike's protected paths
  and the ollama-restart rule, built and smoke-tested in isolation, **not**
  wired into `~/.claude/settings.json` or `settings.local.json`.
- `~/.claude/skills/library/` — the-library skill (MIT) with a `library.yaml`
  catalog seeded from a read-only survey of `~/agent-workspace`,
  `~/.claude/skills/`, and `~/govcon-factory/skills/` (114 skills, 6 agents).

---

## 1. Tool-selection heuristic: 80/15/5 (external) and 80/10/10 (new internal)

**Source:** `disler/beyond-mcp`, `README.md` (root), "My Approach" and "Trade-off
Comparison" sections. License: none found — ported as prose, not copied
structure/code.

`beyond-mcp` builds the same integration four ways (MCP server, CLI, file-system
scripts, Claude Code Skill) specifically to make the cost of each concrete
before arguing for a default. Its stated ratios:

**For external tools** (an API/service someone else owns):
1. 80% — just use an MCP server. Don't overthink it.
2. 15% — CLI, if you need to modify, extend, or control the tool and its context.
3. 5% — scripts or Skills, for serious context preservation, portability, or
   ecosystem reuse.

**For new tools you're building internally:**
1. 80% — CLI + a prime prompt (works for you, your team, and your agents).
2. 10% — wrap in an MCP server only once you need multiple agents at scale and
   don't want to add "another thing" for agents to focus on.
3. 10% — scripts or Skills, same reasons as above.

The reasoning behind the split, from the repo's own trade-off table: MCP and
CLI both consume full context on every tool call, while scripts and Skills use
progressive disclosure (load only what's needed) — but MCP and Skills are the
only two that get triggered automatically by the agent's judgment, while CLI
and scripts require an explicit decision to invoke. This is a direct,
citable default for agent-workspace and Hermes, which currently has no
documented decision rule for "should this be an MCP server, a CLI, a skill, or
a script" — this doc is that citation until/unless CONSTITUTION.md or a
project doc formalizes it (it isn't a CONSTITUTION-rule candidate itself; it
has no mechanical enforcer, so it stays here as a convention, not a rule).

---

## 2. Git-worktree N-way fan-out + `RESULTS.md` best-of-N comparison

**Source:** `disler/quick-data-mcp`, `.claude/commands/exe-parallel.md`
(full file, 24 lines). License: none found — pattern-only, reimplemented
below rather than copied verbatim.

The command spins up `N` isolated git worktrees (`trees/<feature>-1/`,
`trees/<feature>-2/`, ... `trees/<feature>-N/`), each an identical copy of the
current branch, and dispatches one subagent per worktree via the Task tool.
Each subagent independently implements the *same* plan end to end in its own
workspace, runs the project's real test command there (`uv run pytest
tests/` in the source repo), and — this is the part worth lifting — writes a
`RESULTS.md` at the root of its own workspace summarizing exactly what it
changed. Nothing auto-merges; a human (or a later synthesis pass) reads the
`RESULTS.md` files side by side and picks a winner, or cherry-picks pieces
from more than one.

Applicability: this is a ready template for govcon-factory's ADW pipeline
wherever a best-of-N implementation run is worth the extra compute — e.g.
multiple `deliverable-draft` attempts against the same requirements extract,
compared on the gate score before one is packaged. The mechanism (worktree +
subagent + own test run + own `RESULTS.md`) ports directly; the specific test
command and file layout would need to match whichever govcon-factory phase
adopts it.

---

## 3. Wave-based parallel-subagent orchestration ("Progressive Sophistication Strategy")

**Source:** `disler/infinite-agentic-loop`, `.claude/commands/infinite.md`
(full command, ~140 lines). License: MIT, confirmed via `README.md`
"## License" section ("MIT License, Copyright (c) 2026 disler") — quoted
substantially below since MIT explicitly permits it and this is meant to be
used as a direct template.

The command's core contribution is a concrete batch-size rule for fanning out
subagents, and a policy for *what changes between waves*, not just how many
agents run per wave:

**Sub-Agent Distribution Strategy** (verbatim):
> - For count 1-5: Launch all agents simultaneously
> - For count 6-20: Launch in batches of 5 agents to manage coordination
> - For "infinite": Launch waves of 3-5 agents, monitoring context and
>   spawning new waves

**Infinite Execution Cycle** (verbatim, the wave loop):
> ```
> WHILE context_capacity > threshold:
>     1. Assess current output_dir state
>     2. Plan next wave of agents (size based on remaining context)
>     3. Assign increasingly sophisticated creative directions
>     4. Launch parallel Sub Agent wave
>     5. Monitor wave completion
>     6. Update directory state snapshot
>     7. Evaluate context capacity remaining
>     8. If sufficient capacity: Continue to next wave
>     9. If approaching limits: Complete final wave and summarize
> ```

**Progressive Sophistication Strategy** (verbatim) — each wave is assigned a
harder dimension than the last, rather than just repeating the same
instruction N times:
> - **Wave 1**: Basic functional replacements with single innovation dimension
> - **Wave 2**: Multi-dimensional innovations with enhanced interactions
> - **Wave 3**: Complex paradigm combinations with adaptive behaviors
> - **Wave N**: Revolutionary concepts pushing the boundaries of the specification

Each agent in a wave is handed the same base spec plus a distinct "assigned
creative direction" so parallel outputs don't converge on the same answer,
and the orchestrator does a fresh directory-state snapshot before every wave
(not once at the start) so wave 2 knows what wave 1 actually produced, not
what was planned. Reusable in govcon-factory anywhere N-way *variant*
generation is wanted (e.g. multiple proposal drafts or outreach angles for
the same lead) rather than N-way *identical-plan* generation (that's pattern
2, above) — the distinguishing feature here is that each parallel stream is
deliberately pushed toward a different creative direction instead of
converging on one plan.

---

## 4. Status-marker phase-gated build loop

**Source:** `disler/planf3`, `.claude/skills/planf3/workflows/build-plan.md`
(full file, 6 numbered steps). License: MIT, confirmed via `LICENSE`
("Copyright (c) 2026 IndyDevDan") — quoted verbatim, permitted.

Four status markers stamped directly into a plan file as work proceeds:
`[]` idle, `[wip]` in progress, `[x]` complete, `[f]` failed. The loop
(verbatim):

> 1. Locate the Plan - From the `USER_PROMPT`, resolve the path to the target
>    plan `.html` file; if no path is given, infer the most likely plan from
>    `PLAN_OUTPUT_DIRECTORY` and confirm before building
> 2. Absorb Context - Read the full plan: all embedded images, the metadata
>    header, and every back reference (depth 1) so you fully understand
>    prior/related work before writing code
> 3. Execute Phases - For each phase in order, top to bottom:
>    - Announce the phase you are starting
>    - Set the phase and current task marker to `[wip]` in the plan file
>    - Implement the task's specific actions
>    - Run that phase's Testing Strategy commands; loop on failure until they pass
>    - Mark each task `[x]` when complete or `[f]` if it cannot be made to
>      pass, then move on
>    - Do not start the next phase until the current phase's tasks and tests
>      resolve
> 4. Final Validation - Run the global Validation Commands and confirm every
>    box passes
> 5. Update Metadata - Append the current ISO timestamp to `modified`, append
>    agent name / session id, and append the relevant commit SHA(s) to the
>    metadata header
> 6. Report - Summarize what was built per phase, the final status of every
>    task, and any `[f]` failures that need attention

The load-bearing rule is step 3's "do not start the next phase until the
current phase's tasks and tests resolve" — a phase gate, not just a status
label. `[f]` (failed, not silently skipped) matters as much as `[x]`: it
keeps a stuck phase visible in the plan file itself rather than letting an
agent quietly move on and report success later. Directly liftable into
govcon-factory's ADW plan-execution phase wherever a plan currently has no
explicit gate between phases.

---

## 5. Completion-contract sentinel + block-on-push-event + lead/worker edit boundary

**Source:** `disler/learning-cmux-with-agents`, `.claude/agents/lead.md`
(full file). License: MIT, confirmed via `LICENSE` ("Copyright (c) 2026
IndyDevDan") — quoted, permitted. Note: this repo's mechanism is specific to
the third-party `cmux` terminal app's `cmux events --category notification`
push feed; `cmux` itself is not being adopted. The three conventions below
are the portable part.

**The completion contract** — every worker prints one exact sentinel line
when done, so the lead never has to guess or fuzzy-match:
> ```
> FLOTION-DONE: <role> | <one-line summary>
> ```
Ending every dispatched task with an explicit instruction to print that exact
line ("End with exactly: FLOTION-DONE: build-fe | <summary + files
touched>") is what makes done-detection unambiguous — grep for the line, not
"does this output sound finished."

**Block on the push event, never busy-poll** (verbatim heading and rule):
> **Never busy-poll with `read-screen` + `sleep` loops.** cmux *pushes* you an
> event the instant a worker finishes its turn... **Block on that event, then
> do a single `read-screen`** to capture the ... summary.

with the explicit multi-worker form: "run one `cmux events --reconnect`
stream and react as each worker's notification arrives — one stream, many
workers, zero polling." And a verification note worth keeping regardless of
transport: "confirm the ... line is actually present before treating the
task as done (an agent may notify because it needs input, not because it
finished)" — the event firing is not itself proof of success, only proof
that a turn ended.

**Explicit lead/worker edit boundary** (verbatim): "You are the only agent
that talks to the others. **You delegate; you do not edit app code
yourself.**" and, in the Rules section: "**Never edit files under
`apps/flotion/`** — that is the builders' job. You may read them to
understand state and to integrate."

Applicability: Hermes's own lead/worker prompt templates, wherever an
orchestrator dispatches to workers and needs (a) an unambiguous way to detect
"this worker is actually done" versus "this worker's turn ended," and (b) an
explicit, stated rule that the orchestrator itself never touches the
worker's files. The event-driven-not-polling principle applies even without
`cmux`'s specific push mechanism — any transport with a completion signal
(a file write, a message queue, a exit code) should be blocked-on rather than
polled, for the same reason: polling wastes cycles and races the actual
completion state.

---

## 6. SKILL.md anatomy template (synthesized, not copied)

**Sources (structural reference only, both unlicensed):**
- `disler/agent-sandbox-skill`, `.claude/skills/agent-sandboxes/SKILL.md`
  (full file read)
- `disler/fork-repository-skill`, `.claude/skills/fork-terminal/SKILL.md`
  (full file read)

Neither repo carries a LICENSE file or a license section in its README —
checked both directly. **The template below is my own synthesis of the
pattern both repos independently converge on, written from scratch in my own
words and organization — not a verbatim or near-verbatim copy of either
SKILL.md.** What both actually share, observed by reading the files:

- **Frontmatter**: `name` + a `description` written as a trigger condition
  ("Use when the user requests X, or Y, or mentions Z") rather than a mere
  summary — the description IS the routing logic, since Claude Code decides
  whether to load the skill from this text alone.
- **A `## Variables` section** near the top: named, ALL-CAPS or bold
  placeholders (paths, flags, timeouts) referenced by name throughout the
  rest of the file instead of being repeated inline — one place to update
  per environment/fork.
- **Hard imperative rules**, stated as bullet commands, not suggestions —
  "ALWAYS", "NEVER", "CRITICAL" prefixes on the load-bearing constraints
  specifically (both repos reserve these words for genuine hard constraints,
  not routine steps — agent-sandbox-skill's "Never delete the sandbox unless
  explicitly asked" sits next to plain unmarked steps like "change directory
  to X").
- **An IF/THEN branch table** (fork-repository-skill's `## Cookbook`
  section) or a **template-tier table** (agent-sandbox-skill's `##
  Template Tiers`) — a compact decision table the agent scans once, that
  routes to more detail only for the branch actually taken.
- **Progressive-disclosure links**: a numbered `## Examples` or `##
  Cookbook` table where each row names a separate file (`examples/01_x.md`,
  `cookbook/browser.md`) and states plainly *when* to read it — "Read only
  the example you need for your specific task." The SKILL.md itself never
  inlines that detail; it only inlines the routing table. This is the "thin
  skill, fat cookbook" idea named explicitly elsewhere in the source survey
  (`inkwell-agent-sandboxes-and-software-factory`'s
  `sssf-sandbox-orchestrator/SKILL.md`).
- **A closing `## Reference`/`## Troubleshooting` section** — a flat list of
  known failure modes and the one-line fix for each, so common errors don't
  require reopening the whole file.

Synthesized template shape (mine, for reuse when writing a new
agent-workspace or Hermes skill):

```markdown
---
name: <skill-name>
description: <trigger-condition sentence(s) — when Claude should load this,
  written as "Use when..." not as a summary of what it does>
---

# <Skill Title>

One paragraph: what this skill does and what it explicitly does NOT do.

## Variables
- **SOME_PATH**: `<value>` — referenced as SOME_PATH below
- **SOME_FLAG**: `<value>`

## Hard Rules
- NEVER <the one thing that would cause real damage if skipped>
- ALWAYS <the one non-negotiable precondition>
- <routine steps go in Workflow below, not here — reserve caps for things
  that actually need them>

## Decision Table
| Condition | Action |
|---|---|
| ... | Read `cookbook/<x>.md` and follow it |

## Workflow
1. ...
2. ...

## Cookbook
| Topic | Read When | File |
|---|---|---|
| ... | ... | `cookbook/<topic>.md` |

## Troubleshooting
- **"<error text>"**: <one-line fix>
```

---

## 7. `.env`-file-access-blocking regex (documented, NOT wired)

**Source:** `disler/claude-code-hooks-mastery`, `.claude/hooks/pre_tool_use.py`,
function `is_env_file_access()` (lines ~54–82). License: none found — no
LICENSE file, no License section in README, checked both directly. Regex
patterns themselves carry low copyright risk either way, but per the task
scope this is documentation only — **not wired into any hook by this
session.** Mike should decide whether/how to fold it into
`~/.claude/hooks/` himself.

```python
def is_env_file_access(tool_name, tool_input):
    """
    Check if any tool is trying to access .env files containing sensitive data.
    """
    if tool_name in ['Read', 'Edit', 'MultiEdit', 'Write', 'Bash']:
        # Check file paths for file-based tools
        if tool_name in ['Read', 'Edit', 'MultiEdit', 'Write']:
            file_path = tool_input.get('file_path', '')
            if '.env' in file_path and not file_path.endswith('.env.sample'):
                return True

        # Check bash commands for .env file access
        elif tool_name == 'Bash':
            command = tool_input.get('command', '')
            # Pattern to detect .env file access (but allow .env.sample)
            env_patterns = [
                r'\b\.env\b(?!\.sample)',        # .env but not .env.sample
                r'cat\s+.*\.env\b(?!\.sample)',  # cat .env
                r'echo\s+.*>\s*\.env\b(?!\.sample)',  # echo > .env
                r'touch\s+.*\.env\b(?!\.sample)',     # touch .env
                r'cp\s+.*\.env\b(?!\.sample)',   # cp .env
                r'mv\s+.*\.env\b(?!\.sample)',   # mv .env
            ]

            for pattern in env_patterns:
                if re.search(pattern, command):
                    return True

    return False
```

Note for whoever (Mike) decides on this: the file-path check (`'.env' in
file_path`) is a plain substring test, so it also matches things like
`myapp.env.production.yaml` — broader than intended, and the bash-command
patterns operate on raw command text the same way the damage-control hook
does (naive substring/regex, not shell-tokenized), so it inherits the same
recall-over-precision trade-off documented in
`~/.claude/hooks/damage-control/patterns.yaml`'s header comment. Mike's own
`~/.claude/hooks/damage-control/patterns.yaml` (this session's item 1
install) already carries a `zeroAccessPaths` entry for `.env`/`.env.*`/
`*.env` that covers the same ground via the damage-control mechanism
(currently not wired live either) — if Mike wires one, the other may be
redundant; worth deciding together rather than both landing independently.

---

## Cleanup

`~/agent-workspace/.tmp-disler-install/` (11 shallow clones:
claude-code-damage-control, big-3-super-agent, the-library, beyond-mcp,
quick-data-mcp, infinite-agentic-loop, planf3, learning-cmux-with-agents,
claude-code-hooks-mastery, agent-sandbox-skill, fork-repository-skill) was
removed with the non-recursive-flag method (`find ... -depth -type f
-delete` then `find ... -depth -type d -empty -delete`), per
`~/CLAUDE.md` rule 1's `rm -rf` ban, same pattern as the original survey's
cleanup. Verified gone after.
