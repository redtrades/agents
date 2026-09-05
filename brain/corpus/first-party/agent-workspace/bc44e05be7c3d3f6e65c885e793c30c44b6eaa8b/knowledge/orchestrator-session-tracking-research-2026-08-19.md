# Why orchestrators lose track of Claude Code sessions — Dispatch/Claude Code specifically

Scope note: narrowed mid-research at Mike's request to Dispatch and Claude Code's
own tooling, not general multi-agent-systems theory. Draft, uncommitted — see
`README.md` for this repo's convention of leaving research drafts untracked
until reviewed. Access date for all sources below: 2026-08-19.

## 1. What Claude Code itself actually provides

Claude Code has **three separate, non-unified mechanisms** for tracking other
sessions, each with different guarantees. An orchestrator has to know which
one it's actually riding on.

**a. Agent View / the supervisor daemon** (research preview — `claude agents`).
Each background session runs under a per-user supervisor process that persists
state to `~/.claude/jobs/<id>/state.json` across restarts. This is a genuine
status registry:
- `claude agents --json` returns each session's `state` (`working|blocked|done|failed|stopped`),
  `pid`, `waitingFor`, `sessionId`.
- `claude daemon status` reports supervisor health/version.
- `claude logs <id>` reads a session's output without attaching.
- Idle timeout ~1 hour after a session finishes unattached, unless pinned (`Ctrl+T`).
- Push notifications fire through the `Notification` hook (`agent_needs_input`,
  `agent_completed`) and the configured terminal channel — this *is* a real
  push path, not pure polling.
- source: [Agent view — Claude Code Docs](https://code.claude.com/docs/en/agent-view)

**b. In-session background subagents.** A backgrounded subagent's completion
"reaches Claude as a completion notification in a later turn" — also push, not
poll — and the result is independently persisted (`/tasks`, viewable via
transcript) so it survives the caller's turn ending before it checks. This
directly contradicts the general claim that Claude Code has "no push
notification, no state between turns" — for this specific mechanism, both exist.
- source: [Subagents — Claude Code Docs](https://code.claude.com/docs/en/sub-agents)

**c. Cross-session messaging** (`ListAgents` / `SendMessage` — the tools this
very session used to track its own subagents above). This is a notice channel,
not a result channel: plain text only, no attached output, delivery depends on
the target session still being alive and registered via its inbox-socket file
on disk. A session that's mid-way through a long Bash tool call (e.g. a GPU
job) still receives messages between tool calls, but there's no field in this
mechanism that reports "still running your last instruction" vs. "ignored it."
- source: [Cross-session messaging — Claude Code Docs](https://code.claude.com/docs/en/cross-session-messaging)

**Confirmed gap — no query API, hooks are reactive only.** Outside of (a)'s
daemon-backed `claude agents --json`, there is no way to ask "is this session
still doing what I told it?" Hooks (`Stop`, `SubagentStop`, `SessionStart`,
`SessionEnd`) only fire at fixed lifecycle points; anything queryable outside
that moment has to be built by an external process recording hook events itself.
- source: [Hooks reference — Claude Code Docs](https://code.claude.com/docs/en/hooks)

**Confirmed gap — no resource locking for shared files.** Nothing above
prevents two sessions from touching the same file or resource. Agent teams'
shared task list *is* file-locked to stop two teammates double-claiming the
same task, but that's the only lock in the whole system, and it protects the
task list, not the actual work. Anthropic's own docs on avoiding this are
purely advisory: "Two teammates editing the same file leads to overwrites.
Break the work so each teammate owns a different set of files." That is a
convention, not an enforcer — exactly the class of thing this repo's own
[[feedback-five-enforced-rules]] says will fail under load.
- source: [Orchestrate teams of Claude Code sessions — Claude Code Docs](https://code.claude.com/docs/en/agent-teams)

**Documented, named footgun that matches the "results sat uncollected" pattern.**
When agent teams are enabled (`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`), Claude
can silently promote a subagent it names into a teammate. Teammates report
completion via the idle notification *with no output attached* — you have to
separately pull the task list or a message. Subagents report a result directly.
Anthropic's own troubleshooting page states outright: "An orchestration flow
that waits on subagent results can stall." If agent teams are on anywhere in a
chain that expects subagent-style direct results, this alone reproduces
"launched a background job, ended its turn, results sat uncollected."
- source: [Orchestrate teams of Claude Code sessions — Claude Code Docs](https://code.claude.com/docs/en/agent-teams) (Troubleshooting → "Claude spawns teammates instead of subagents")

**Unconfirmed — stop reliability against a live child process.** `claude
stop <id>` / `Ctrl+X` / `claude kill` exist and are verifiable via the `state`
field going to `stopped`. Docs describe the supervisor force-terminating a
session whose stop attempt failed ("the background service isn't responding").
I could not confirm from documentation whether stopping a *session* reliably
kills a long-running child process a Bash tool call spawned (e.g. an actual
GPU training job), versus only interrupting the model's turn. This is exactly
the shape of today's "told to halt, kept running for an hour" failure, and I'm
flagging it as unconfirmed rather than asserting either way.
- source: [Agent view — Claude Code Docs](https://code.claude.com/docs/en/agent-view)

## 2. What "Dispatch" is, specifically

Dispatch is a real Anthropic-shipped feature — "a command center inside Cowork
... a walkie-talkie that lets you send instructions from mobile while Claude
orchestrates real work on your desktop with one persistent thread and multiple
parallel tasks." I could not get past a paywall to the operational detail (the
source's own "Real PM Workflows" section, which is where session-tracking
behavior would actually be described, was not visible).
- source: [The Claude Dispatch Guide](https://www.productcompass.pm/p/claude-dispatch-guide) (partial — paywalled past setup/architecture)

I did not find independent documentation of Dispatch's own status/lifecycle
API beyond what it presumably delegates to Cowork/Claude Code underneath. This
is the one section of this report where the primary source ran out — treat
Dispatch's own internals as unconfirmed, not absent.

## 3. What Mike's own orchestrator (Buzz) already has — checked against its source

Buzz doesn't drive Claude Code's CLI/Agent View. It drives Claude Code over
ACP (`claude-agent-acp`) — a different embedding path — via its own Rust crate
`buzz-acp`. Checked directly against `~/.buzz/REPOS/buzz/crates/buzz-acp/src/pool.rs`
(2026-08-19): this is **not** an orchestrator with no heartbeat or timeout
concept. It already has:
- `heartbeat_session` / `heartbeat_turn_count` fields and a dedicated
  `PromptSource::Heartbeat` path
- an idle-timeout mechanism (`session_prompt_blocks_with_idle_timeout`)
- a `TimeoutKind` enum distinguishing an idle-clock cutoff from a hard
  wall-clock `max_turn_duration` cap
- a steer/cancel-and-merge control protocol for redirecting a running session

source: `~/.buzz/REPOS/buzz/crates/buzz-acp/src/pool.rs` (local repo, read directly)

This changes the diagnosis. The question isn't "does Buzz lack the primitives
production systems use" — it has heartbeat, idle-timeout, and hard-timeout
concepts already, independently of Claude Code's own Agent View daemon. The
open question is why the GPU-job session wasn't caught by `max_turn_duration`
or the idle clock, and that's a specific, answerable question about this one
session's configuration or about whether a long Bash tool call inside an ACP
turn is exempt from the timeout Buzz already has — not evidence that a new
timeout mechanism needs to be invented. I did not read far enough into
`pool.rs`/`queue.rs` (11,600+ combined lines) to answer that specific question;
it's the concrete next step, not a re-architecture.

## 4. Why an orchestrator using all of this still loses track

Three non-unified mechanisms (§1a–c) plus Buzz's own separate ACP-level
heartbeat/timeout layer (§3) means there is no single source of truth — an
orchestrator has to correctly wire together whichever of these its actual
harness rides on, and a gap in the wiring reads as "the orchestrator lost
track" even when a tracking mechanism exists somewhere in the stack. Given
Buzz talks to Claude Code over ACP rather than through Claude Code's own
Agent View/supervisor daemon, the daemon's `claude agents --json` /
`~/.claude/jobs/*/state.json` registry (§1a) is probably not in Buzz's path at
all — worth confirming, not assuming.

The two failures with no defense anywhere in the stack are the resource
conflicts (Ollama store deletion, config file double-edit): nothing in Claude
Code, Dispatch, or (as far as `pool.rs` showed) Buzz enforces exclusive access
to a shared file or resource. That gap is real and unaddressed by any layer
checked here.

## 5. One recommendation

**Don't build a new tracking mechanism. Audit whether the ones that already
exist (Buzz's own heartbeat/`max_turn_duration`, and whether agent-teams mode
is active anywhere in the chain) are actually being hit by the failure cases,
before assuming nothing is there.** Concretely: instrument or log why the
GPU-job session's `max_turn_duration`/idle-timeout didn't fire — that's a
bounded, checkable question against code that exists — and check whether
`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` is set anywhere in the chain that
produced the "background job, turn ended, uncollected results" pattern, since
that's a named, documented cause of exactly that symptom.

For the one gap nothing addresses — resource conflicts on shared files
(Ollama store, config files) — extend this repo's own existing stale-claim
lease pattern (`scripts/check-stale-claims.sh`) from git-tracked task files to
a lease file per shared mutable resource, enforced the same way the five
existing rules are: one script, one enforcer, proven against a deliberate
failing fixture before trusted. This is the smallest addition consistent with
[[feedback-five-enforced-rules]] — it's the same mechanism already proven to
work here, pointed at a new class of resource, not a new philosophy.

**Tradeoff:** this recommendation is diagnosis-first and deliberately does
*not* propose new supervision infrastructure, because the evidence found here
doesn't support "nothing exists" — it supports "something exists and either
isn't wired in or isn't being checked." That means the immediate next step is
unglamorous log-reading and code-reading inside `buzz-acp`, not a design
exercise, and it will surface follow-up questions (e.g., does Buzz's
`max_turn_duration` apply inside a single long Bash tool call, or only across
model turns?) that this report doesn't answer. The resource-lease extension
is cheap and consistent with what's already proven here, but it only fixes
the file-conflict class of failure — it does nothing for the "halt not
respected" or "results uncollected" failures until the audit above identifies
which wiring gap actually caused them.

## Sources

- [Hooks reference — Claude Code Docs](https://code.claude.com/docs/en/hooks) (accessed 2026-08-19)
- [Orchestrate teams of Claude Code sessions — Claude Code Docs](https://code.claude.com/docs/en/agent-teams) (accessed 2026-08-19)
- [Subagents — Claude Code Docs](https://code.claude.com/docs/en/sub-agents) (accessed 2026-08-19)
- [Cross-session messaging — Claude Code Docs](https://code.claude.com/docs/en/cross-session-messaging) (accessed 2026-08-19)
- [Agent view — Claude Code Docs](https://code.claude.com/docs/en/agent-view) (accessed 2026-08-19)
- [The Claude Dispatch Guide — Product Compass](https://www.productcompass.pm/p/claude-dispatch-guide) (accessed 2026-08-19, partial/paywalled)
- [Multiagent orchestration — Claude Platform Docs](https://platform.claude.com/docs/en/managed-agents/multiagent-orchestration) (accessed 2026-08-19 — separate Managed Agents API product, not Claude Code CLI; included for the push-event contrast in §1's framing but not otherwise cited above since Buzz doesn't use this API)
- `~/.buzz/REPOS/buzz/crates/buzz-acp/src/pool.rs` (Mike's local Buzz repo, read directly 2026-08-19)
