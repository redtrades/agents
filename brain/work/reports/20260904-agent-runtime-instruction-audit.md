# Agent instruction and runtime audit

Date: 2026-09-04. Status: audit and proposed repair plan complete; configuration repairs not applied. Requested by Mike in Codex task `01a06e26-a7e1-7932-b62d-96d791480565`.

**Recommendation:** Keep `agent-configs` for policy and runtime adapters, `agent-sdlc` for execution, and `agent-knowledge-archive` for history. Repair task identity and lifecycle checks first. Reduce the global contract to a small task router. Prove the behavior in Codex, Claude Code, and Antigravity before reorganizing historical files. Another controller, repository, broad skill installation, or recursive cleanup is unnecessary.

## Scope and evidence limits

Inspected shared contracts, deployment/profile code, native settings and selected hooks, skill inventories and core bodies, selected role definitions, live-repository entrypoints, existing claim/checkpoint code, Git worktree metadata, and current official documentation. Read GitHub issue #117 live. Avoided credentials, conversation-content mining, and exhaustive reading of frozen repositories or every third-party plugin body.

This is a static/configuration audit plus deterministic checks, not a fresh behavioral certification of every harness. This Codex session's injected instructions, tools, and catalog are directly observable. Other runtime loading remains partly unverified until fresh-session canaries run. Filenames do not establish which agent created a file; this report does not attribute the estate's failures to a particular author.

No runtime settings, hooks, skills, scheduler state, existing task records, or GitHub records were changed. This report is a local review artifact in the existing report destination, not promoted canon or a delivered implementation PR. The unrelated home `TASK.md` was preserved; this audit used a separate temporary checkpoint.

## Current flow

The intended route is:

`runtime adapter → archive START → global/repository contract → GitHub issue → accepted claim → isolated workspace → implement → verify → independent review → exact-head promotion → durable completion`

The structure is useful, but the entrypoint applies too much of it to every request, and runtime coverage is uneven.

| Surface | Observed configuration | What that actually establishes |
| --- | --- | --- |
| Shared / Codex | `~/.agents/AGENTS.md`, `~/.codex/AGENTS.md`, and source `agent-configs/AGENTS.md` match: 10,415 bytes, 167 lines, 1,406 whitespace-delimited words | Contract-copy parity. The shared contract is also present in this session. `.agents/AGENTS.md` alone is not a universal loader |
| Claude Code | Generated `~/.claude/CLAUDE.md`; settings contain 12 skills `on`, 94 `user-invocable-only`; Concise output style | Lean configuration is present; task hooks are registered in `~/.claude/settings.local.json`, not the documented user-global settings file |
| Antigravity IDE / CLI | Six Google plugin entries enabled in `.gemini/config/config.json`; bundled customization docs present | `~/.gemini/GEMINI.md`, inspected global custom skill directories, and `.gemini/config/hooks.json` are absent. Repository `AGENTS.md` may still load; universal personal-policy loading is not proved |
| Hermes | Generated `SOUL.md`; 426 recursively found `SKILL.md` paths, including symlink traversal | Adapter parity does not mean a lean skills catalog. `config.yaml:62` imports a skill directory from frozen `agent-platform` |
| OpenCode | Global generated `AGENTS.md`; five role files | Adapter check passes; no fresh instruction/skill/task-hook receipt was obtained |
| OpenHands | Managed context copy at `~/.agents/skills/agent-configs-global.md` | The documented SDK worker route intentionally disables ambient skills and uses an inline packet. Normal CLI and SDK admission must be tested separately |
| Grok / Buzz / Jules | Grok has 95 recursively found skill paths; Buzz generated adapter passes; Jules has a documented repository route | Grok is omitted from the profile manager's runtime choices. Buzz parity is not proof for each ACP child. Jules cannot depend on this Mac's absolute home paths |

Counts are filesystem inventories, not active skills or token usage. Shared skills contain 94 top-level skill directories and three nested research skills, 97 total. Claude has 106 recursively found paths. Hermes and Grok each have a broken top-level `code-review` symlink. No large directory was classified as disposable merely from these counts.

Evidence: [profile manifest](/Users/man/agent-configs/runtimes/skill-profile.json), [runtime manager](/Users/man/agent-configs/scripts/manage-agent-runtime.py:1542), [cross-harness admission](/Users/man/agent-sdlc/docs/runbooks/cross-harness-agent-launch.md), [Hermes config](/Users/man/.hermes/config.yaml:62).

## Findings requiring repair

| Priority | Finding and consequence | Smallest proposed repair |
| --- | --- | --- |
| P0 | **Task identity is ambiguous.** `~/TASK.md:3` describes a different, estate-wide task. The injection hook selects `./TASK.md` before anything else, ignores the event's `cwd` and session identity, and prints only 25 lines. It can re-anchor an agent to the wrong work | Pass one explicit task-file path plus task/session/worktree identity. Validate identity before injection; never fall back to a different task in home |
| P0 | **Artifact rules contradict the hook.** `block-home-root-writes.sh:11` recommends `~/agent-reports/<dated-slug>/`; hygiene forbids new dated report folders. The hook also conflicts with mandatory home `TASK.md` creation | Route outputs from the active task's declared destination. Separate scratch, checkpoint, and durable deliverable; permit checkpoint setup before artifact enforcement |
| P0 | **Tracking is a reminder, not a completion check.** The hook always exits 0, checks no task schema, freshness, owner, evidence, or terminal state. There is no task-related Stop check in the inspected Claude settings | Reuse a small common task validator at admission, meaningful checkpoints, and completion. A hook checks missing evidence; it must not invent a status or force endless continuation |
| P0 | **Antigravity is omitted from “all.”** Native global rules are absent, and neither profile-manager runtime choices nor cold-start adapter checks cover it | Add an explicit Antigravity adapter and behavioral fixture for the installed IDE and CLI versions. Report unsupported/unverified surfaces honestly |
| P1 | **Codex lean regeneration can remove unrelated configuration.** Read-only rendering changes Sites to false and removes a marketplace section inserted inside the managed profile block | Fix ownership boundaries in the renderer first. Preserve unrelated keys; fail with an exact diff on unexpected block content. Do not run `--replace` blindly |
| P1 | **Lean-profile discovery differs across runtimes.** Codex's manager scans only top-level skills; Claude's scans recursively. Three nested research skills escape Codex's non-core suppression and are visible in this session | Use the runtime's actual discovery rules and test nested skills. Give every skill an explicit core/on-demand/disabled state |
| P1 | **Frozen policy can leak into execution.** Hermes imports `agent-platform/.agents/skills/operating-bounded-agent-lanes`. Several installed role files carry older voice, ledger, and artifact requirements | Review the referenced skill before selectively relocating or disconnecting it. Reconcile role instructions with the common contract; preserve provenance |
| P1 | **Startup repeatedly loads estate history.** The global contract repeats the engineering loop. Seven referenced archive files alone contain 6,011 words, before repository contracts, runbooks, debriefs, tools, memory, or skills | Make the estate map conditional on estate/repository work. Inline a short route and load one task-relevant operating document; leave history behind evidence pointers |
| P1 | **The purported live parent is closed.** `agent-sdlc#117` was CLOSED when fetched, updated 2026-09-04T17:53:47Z. It still contains stale “next chunks” | Retain #117 as provenance. Route active work to its actual issue/controller; do not let a historical parent prescribe the next task |
| P2 | **Skills still contain harness-specific assumptions.** `lean-build` refers to undefined “Native Core.” `using-superpowers` demands invocation at a 1% relevance threshold and before any response, contrary to lean routing | Keep broad routers opt-in; replace undefined dependencies only in owned/adapted copies. Preserve concise useful skills rather than rewriting everything |
| P2 | **Historical instructions remain executable-looking.** `MASTER-GUIDE.md` is bannered superseded but contains old factory queue commands and a routing paragraph sending work to frozen `agent-workspace`. D-001 still says active although merge-authority supersedes it | Replace active entry links with the current operating rule; clearly mark historical decision status without deleting history |

Local evidence: [task hook](/Users/man/.claude/hooks/task-tracking/inject-task.sh:13), [home-write hook](/Users/man/.claude/hooks/block-home-root-writes.sh:11), [Claude hook registrations](/Users/man/.claude/settings.local.json:51), [tracking rule](/Users/man/agent-configs/rules/task-tracking.md), [hygiene](/Users/man/agent-configs/rules/hygiene.md), [Codex profile block](/Users/man/.codex/config.toml:411), [discovery mismatch](/Users/man/agent-configs/scripts/manage-agent-runtime.py:877), [legacy guide](/Users/man/agent-configs/MASTER-GUIDE.md), [closed parent issue](https://github.com/redtrades/agent-sdlc/issues/117).

Two hook details strengthen the diagnosis. Official Claude documentation distinguishes user-global `~/.claude/settings.json` from project-local `.claude/settings.local.json`; registration in the latter does not demonstrate global activation in other repositories. Also, plain stdout from `PreCompact` is not a general context-injection channel. The existing SessionStart registration can help when actually loaded, but the claim that this script re-injects context at both events is too broad. Use documented event semantics and capture an actual loading receipt. [Settings](https://code.claude.com/docs/en/settings), [hook output behavior](https://code.claude.com/docs/en/hooks).

## Comparison with this Codex session

These are observed runtime constraints, not proposed user preferences:

- Native instructions place the current user request above repository defaults. “GitHub is authority” should govern repository assignment and delivery, not prevent Mike from correcting the task in chat.
- Native instructions preserve the task across compaction and accept user steering. The shared rule that goal/scope can never change and any change ends the session is too rigid. Record explicit amendments; do not silently widen scope or force a new conversation for every correction.
- This runtime requires progress updates during longer work. The global “no process narration” rule should mean no noisy tool-by-tool narration, while retaining brief findings, blockers, and completion updates.
- Subagent delegation depends on runtime support and authorization. Solo must remain sufficient; a global command to delegate every parallelizable activity cannot override runtime limitations.
- The installed Sol reviewer is another OpenAI model. It supplies independent context, but it does not satisfy the estate's different-model-family requirement for a Codex-authored change. A bot identity also does not by itself prove independent review reasoning.
- Disk Codex settings say `approval_policy = "never"` and `sandbox_mode = "danger-full-access"`; this session actually has managed workspace-write restrictions and automatic escalation review. Audit effective session permissions separately from file contents. Do not weaken permissions to make adapters appear consistent.
- The current catalog includes Canva and Notion capabilities despite false plugin flags on disk. Host-supplied tools, plugin state, cached session state, and config overlays must be distinguished. This observation does not identify the cause or prove every installed plugin loads in every session.
- Persistent memory in this runtime is advisory context; durable-memory writes require explicit user requests. Task checkpoints are operational state and must not be conflated with automatic memory promotion.

OpenAI documents global-to-project instruction loading and progressive skill loading. These support a thin portable contract plus task-specific detail; they do not make a copied file a universal runtime hook. [Instruction discovery](https://learn.chatgpt.com/docs/agent-configuration/agents-md), [skills](https://learn.chatgpt.com/docs/build-skills).

## Proposed working model

Use three modes, selected by the actual request:

| Mode | Default behavior | Durable state |
| --- | --- | --- |
| Answer | Answer directly; use targeted evidence when needed. Simple requests receive a few sentences | No task file or report unless requested |
| Investigate / plan | Inspect narrowly, keep a checkpoint for sustained work, deliver one report if the work warrants it | One task-local checkpoint and one named report destination |
| Implement | One authorized issue/task, accepted ownership, isolated writing workspace, smallest complete change, proportionate verification, required review and delivery | Existing issue/PR plus a compact task-local checkpoint |

**Solo:** one owner executes the whole loop. No swarm ceremony.

**Swarm:** the same loop, with one controller and one integration owner. Each worker gets task ID, parent ID, exact paths, workspace, acceptance check, output destination, allowed tools, budget/stop condition, and return format. Workers update their own packet/checkpoint; the integration owner alone updates aggregate status. Wait for the claim-accepted receipt before editing. Posting `/claim` is an asynchronous request, not immediate ownership.

Reuse the existing [claim workflow](/Users/man/agent-sdlc/.github/workflows/claim.yml), [claim implementation](/Users/man/agent-sdlc/scripts/github-claim.mjs), and [checkpoint/budget implementation](/Users/man/agent-sdlc/src/execution_budget.mjs). Their existence was verified; a live contention/failover test was not performed here. Do not create another task database, scheduler, or mirror board as part of this repair.

**Checkpoint:** retain `TASK.md` as the human-readable format, but bind it to an explicit task path. For repository work, place it in the owned worktree. For non-repository work, use the runtime's task directory. Include identity/owner/workspace, goal, acceptance, scope, destination, current state, evidence pointers, next action, and blocker. Add an amendment when Mike changes scope. Keep the current state short; leave full event history in the existing issue/PR or runtime transcript. Do not create a new dated Markdown file per heartbeat.

**Update points:** after acceptance/scope changes, completed subparts, verification, handoff, blockers, and final disposition. Update before risky context transitions when possible. At completion require evidence appropriate to the mode: a verified answer/report, or the implementation's delivery receipt. A blocked task may stop; completion checks must not trap it in a retry loop. If publication is temporarily unavailable, retain an explicit pending-publication checkpoint rather than falsely saying delivered.

**Artifacts:** code and tests go to the owning repository; durable cross-estate analysis goes to the existing archive report directory; ephemeral experiments go to task scratch. Runtime-created folders under Documents are not automatically canonical, nor automatically trash. Promote only the requested deliverable and retain its task link.

## Lean skills and plugins

Keep the existing 12-skill core as the first baseline. All 12 have three evaluation cases each, 36 total; that is good groundwork. The inspected evaluation docs describe a future/manual run and baseline process. This audit did not find a recorded golden result in the searched `agent-configs` filenames, so passing behavioral evaluations remain unverified. [Eval rule](/Users/man/agent-configs/rules/skill-evals.md), [installed cases](/Users/man/agent-configs/skills-evals/installed-skill-evals.json).

Retain domain, document, browser, design, and orchestration capabilities on demand. Explicit-only invocation and disabled installation are different states: Codex documents `allow_implicit_invocation: false` for explicit access, while the present manager disables many skills entirely. Use supported runtime-specific controls instead of assuming identical switches. [Codex invocation policy](https://learn.chatgpt.com/docs/build-skills), [Claude skill controls](https://code.claude.com/docs/en/skills).

The 229,375-byte `last30days/SKILL.md` is an oversized optional body, not evidence of that much startup overhead. Large third-party bodies deserve selective splitting or replacement only when their workflows are actually used. The Agent Skills specification recommends progressive disclosure and moving detailed references out of the main body. [Specification](https://agentskills.io/specification).

Antigravity now documents native rules, skills, plugins, and hooks. Use its own input/output schemas rather than copying Claude hook JSON. The docs and this installation expose differing paths across IDE/CLI generations, so pin the installed version in each receipt. [Rules](https://antigravity.google/docs/rules-workflows), [IDE skills](https://www.antigravity.google/docs/ide/skills/), [CLI plugins](https://www.antigravity.google/docs/cli/plugins/), [hooks](https://antigravity.google/docs/hooks).

Proposed budget: reduce the global contract to about 400 words, with one scoped operating reference for implementation. This is a design target, not an empirically proven optimum. Measure real input/output tokens and tool turns on representative tasks before choosing tighter limits. Simple requests should not activate planning, history recovery, or multi-agent review; an MVP should receive the smallest end-to-end implementation and a brief outcome/verification/limitation response.

Anthropic's context-engineering guidance favors a small set of high-signal context. Its long-running-agent work supports incremental tasks and explicit progress artifacts across sessions. Those patterns fit the current system without importing an elaborate new framework. [Context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents), [long-running harnesses](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents).

## Execution plan

Do these sequentially, with one active repair issue at a time. Use the existing repositories and independent cross-family review. Hook logic, permissions, standing constraints, and renderer enforcement are Class B under the current merge rule; prepare and verify the exact candidate before Mike's merge decision. [Merge authority](/Users/man/agent-configs/rules/merge-authority.md).

| Slice | Ownership and exact area to scope in its issue | Acceptance |
| --- | --- | --- |
| 1. Stop new tracking/routing failures | `agent-configs`: task-tracking and hygiene rules, their deployed hook sources, runtime-manager ownership handling and tests | Wrong-task fixture rejected; home-task collision preserved; output hint uses declared destination; regeneration preserves unrelated marketplace settings; apply/check/restore are idempotent in a fixture home |
| 2. Shorten and reconcile the contract | `agent-configs`: global contract, scoped solo/swarm operating text, stale active pointers and relevant role instructions | Answer/MVP/implementation routes are explicit; current user steering is preserved; no unconditional historical reading; cloud workers get portable packets; review/merge protections remain intact |
| 3. Prove runtime parity | Runtime adapters and existing task/checkpoint integration in `agent-sdlc`; one adapter at a time | Fresh Codex, Claude Code, Antigravity IDE and CLI sessions identify the right instructions and task, survive resume/context loss, update evidence and stop correctly. Then extend to secondary harnesses |
| 4. Tighten discovery and evaluate | Existing profile manifest, runtime discovery code, skill eval cases; no bulk upstream edits | Nested skills follow policy; optional routers do not fire on simple work; frozen external import is resolved; core positive/negative cases and task behavior fixtures have saved results with actual token counts |
| 5. Reconcile existing debris once prevention works | Inventory only the affected worktrees and agent-generated artifacts, linked to owning issues | Every move/delete candidate has owner, Git status, refs, delivery evidence, destination, and retention decision. Preserve dirty/unpushed/active work. Remove only explicitly approved candidates |

Do not automatically restore the present lean profile: the Sites setting may be intentional, and the renderer currently proposes deleting a marketplace section. Resolve the desired profile and repair preservation before deployment.

Minimum behavioral fixture set: simple answer; bounded MVP; explicit optional skill; two concurrent home tasks; resume with stale/wrong task; missing final evidence; overlapping worker claim; quota/failure checkpoint; unapproved artifact destination; cloud launch without `/Users/man`; profile drift/rollback. Save one compact result set with runtime version, configuration hash, discovered sources, task ID, checks, token usage when exposed, and failure notes. A file-existence check cannot substitute for these behaviors.

Stop after slices 1–4 pass for the three primary authoring harnesses and two real tasks complete without tracking/artifact drift. Broader cleanup remains a separately bounded operation. This plan does not promise that every agent will behave perfectly; it makes failures detectable and recoverable.

## Verification record

- `verify-cold-start.sh`: exit 0. Seven named adapter paths resolve. Its name overstates coverage; it does not test runtime loading or Antigravity.
- Lean manager checks: Codex exit 1 (drift); Claude, Hermes, OpenCode, OpenHands, Buzz each exit 0. Those are configuration checks, not behavioral certifications.
- In-memory Codex rendering: captured exact Sites/marketplace delta; did not apply it.
- Read-only task-hook fixture: event `cwd` pointed at this audit; process cwd was home. Exit 0; selected the unrelated home task. Demonstrates missing identity/event-cwd handling, not how frequently live sessions encounter it.
- Inventory: 59 registered `agent-sdlc` worktrees; 77 top-level directories in `agent-reports`; 25 entries at `Documents/Codex/*/*`. Counts are not deletion recommendations or disk-space measurements.
- `agent-sdlc` had unrelated modified/untracked files at inspection, including several plan/status/walkthrough files. Preserved all of them.
- Local contract hashes match where verbatim copies are expected. Wrapped adapters differ as expected.
- Audit status: complete. Implementation status: proposed, not applied. Next action: prepare slice 1 against one authorized issue, with its concrete fixture tests and reviewable diff.
