# Swarm platform research: what to adopt for an autonomous, provider-neutral AI-SDLC

**Date:** 2026-08-29 (brief dated 2026-08-28) · **Status:** written continuously, sections land as they are verified · **Deliverable is uncommitted, on no branch, by instruction.**

**Nothing was installed, cloned, or configured during this research.** Every finding below came from reading published source, published documentation, or from files already on this machine.

---

## How to read this document

Every material claim carries three things: a source link, an access date, and an evidence class.

| Evidence class | Meaning |
|---|---|
| **SOURCE** | I read the actual code or config that implements the behavior |
| **DOCS** | I read the project's own documentation or release notes, but not the implementing code |
| **LOCAL** | I read a file on this machine |
| **INFERENCE** | I reasoned from the above; the project does not state it |
| **UNVERIFIED** | I could not confirm it and am saying so rather than guessing |

A capability is graded PASS only on SOURCE or on documentation specific enough that a wrong claim would be an outright falsehood. "The README says it does X" is PARTIAL at best, per the brief's point 6.

**Writing status:** complete. Section 0 is the local failure evidence, section 1 the candidate findings, section 2 the GitHub substrate, then A through F as the brief specifies them, and section 3 lists what could not be verified.

**The three findings that matter most, if you read nothing else:**

1. GitHub's merge API already accepts `sha`, "SHA that pull request head must match to allow merge", and returns `409` when it does not. That is the expected-head compare-and-swap the brief asks for, and it is one field. §2.1
2. The strongest candidate, Optio, gates every database write on a compare-and-swap and then merges **without** that field. Verified in source. §2.1
3. On this machine, `~/agent-workspace/adws/adw_modules/quality.py` lines 154, 163 and 173 still run `echo` commands that exit 0 for lint, typecheck and build. The framework's own README warns about this in bold. A written warning did not prevent it, which is the argument of the whole report. §1.4

---

## 0. Why this machine is the strongest evidence in the report

The brief lists fourteen hard controls. Every single one of them has already failed here, in a way somebody wrote down. That matters for two reasons. It means the requirements are not theoretical, and it means the binding constraint is enforcement rather than design.

The clearest statement of that is in a proposal sitting untracked on this disk:

> "The same design has now been independently derived five times on this machine and enforced zero times."
>, `~/agent-configs/proposals/PROPOSAL-0004.md`, accessed 2026-08-29 (LOCAL)

That single sentence should govern the recommendation. A report that produces a sixth design is the one intervention with a known failure record.

### The local failure ledger, mapped to the hard controls

| Hard control from the brief | What actually happened here | Evidence |
|---|---|---|
| Atomic claim / lease | Two primary checkouts, `~/agent-configs` and `~/govcon-factory`, are both parked on a branch named `work/single-queue-issue-243`, which belongs to only one of them. Both carry uncommitted changes, so any session opening either repo inherits another session's dirty state. | SESSION-AUDIT F-006 (LOCAL) |
| Atomic claim / lease | PR #282 merged at 03:46:45Z; PR #288 opened seventeen seconds later on the same join point. A claim lock at the issue level does not catch code-level collisions. | PROPOSAL-0004, citing `log/CORRECTIONS.log` 2026-08-26 (LOCAL) |
| Fencing generation | No fencing exists anywhere. `agent-mesh` PRs #30, #31, #36 sit in draft, #30 conflicting, because nothing sequences writers. | SESSION-AUDIT F-008 (LOCAL) |
| Isolated execution | `~/CLAUDE.md` rule 3 says "one issue, one worktree, one branch, one session." The rule that forbids the branch violation is itself unreadable because the checkout is parked on the violating branch. | SESSION-AUDIT F-006, F-013 (LOCAL) |
| Independent reviewer | Across 40 merged PRs the reviewer set is `{govcon-reviewer-bot: 93}`. One identity, 93 reviews, zero from anyone else. The one session ever spawned as an independent reviewer, `92046574`, died after five transcript lines on OAuth expiry; the PR it was reviewing merged sixteen minutes later, approved by the bot. | SESSION-AUDIT F-014 (LOCAL) |
| Gates that can fail | `gate_compliance` in govcon-factory tests a substring against a file the same stage just wrote from the same list. It cannot return false. A run passed 36 of 37 checks and produced an unsubmittable document. | orchestrator brief (LOCAL, not independently re-verified in source by me, see section 3, what could not be verified) |
| Durable checkpoint / cold resume | Five sessions died inside a 3 minute 52 second window when one shared five-hour quota drained. Two were recoverable only because they happened to write a file first. | SESSION-AUDIT F-002, F-004 (LOCAL) |
| Cold resume | ~240 KB of finished research across three repos exists as untracked files in single working copies. No branch, no PR, no backup. A `git clean` deletes it. | SESSION-AUDIT F-004 (LOCAL) |
| Deterministic receipts | 22 filed issues (#438 to #459) all cite `knowledge/research/winning-proposal-teardown/INDEX.md`. That file was never written, and the directory containing its siblings is untracked. From a clean clone, all 22 issues point at nothing. | SESSION-AUDIT F-011 (LOCAL) |
| No misleading completion claims | A "42 of 42 checks, all_green" claim is committed on `main` in `CHANGELOG.md:44`. The analysis disproving it, establishing that the number belongs to a different pipeline, is untracked. The false claim is durable; the correction is not. | SESSION-AUDIT F-012 (LOCAL) |
| Prompts cannot substitute for hard controls | `~/CLAUDE.md` cites six mandatory rule files. A session can read two. Three of the missing four sit in agent-configs PR #17, a conflicting draft for two days. Agents are not ignoring the governance layer; they cannot reach it. | SESSION-AUDIT F-013 (LOCAL) |
| Human not in the routine loop | Session `fcaae84e` stalled roughly 19 hours on an unanswered folder-access prompt, holding a concurrency slot and producing nothing, two days after the "allow all except destructive" permission fix merged. | SESSION-AUDIT F-003, A9 (LOCAL) |

### Three failure classes, not one

The audit's census across 187 Claude Code sessions separates causes that a single fix cannot address:

| Cause | Count | What actually fixes it |
|---|---|---|
| Usage-limit termination | 18 | Concurrency control, not "save more often" |
| OAuth expiry | 13 | Token refresh; unrelated to quota |
| Permission stall | at least 1 confirmed, indefinite duration | A default, or a human; blocks forever otherwise |

Source: SESSION-AUDIT Part B (LOCAL). This matters for candidate evaluation: a platform that solves crash recovery does nothing for OAuth expiry or for an unanswered approval prompt, and both of those killed more work here than crashes did.

### Reconciling with the peer document

`~/agent-mesh/Agent SDLC.md` (1,831 lines, untracked, single copy, 77,128 bytes, mtime 2026-08-28 01:47) is a multi-model research pass on this same question. It is a peer contribution, not a competitor, and it gets the central diagnosis right:

> "Fidelity loss between agents isn't a memory problem, it's a state problem."

Its three-layer split (knowledge lasting months in `AGENTS.md`, intent lasting weeks in specs, live state lasting hours in a handoff record) is sound and I adopt it below. Its final recommendation, a deterministic supervisor called `agentd` that claims, launches, observes, checkpoints, rotates and validates, is also directionally right.

Two places where I depart from it, argued in the sections that follow:

1. It carries specific numeric claims about third-party projects (star counts, adoption figures, governance transfers) that I could not confirm and in several cases appear wrong. Those are flagged individually in the feature matrix. This is exactly the undocumented-qualifier failure class PROPOSAL-0004 names, appearing inside the document arguing against it.
2. It recommends building `agentd`. I think the amount of it that must be new code is smaller than the document implies, and I say precisely which parts in section C.

---

## 1. Candidate findings, as verified

Ordered by how much of Mike's lifecycle each one actually covers. Grades and the full matrix are in section B; this section is the evidence behind them.

### 1.1 Last Light: nearform/lastlight

**Link:** https://github.com/nearform/lastlight · site https://lastlight.dev/ · accessed 2026-08-29 · **DOCS** (site and quick start read in full; source not read)

MIT, self-hosted, published by Nearform (an established Irish consultancy, so a named corporate maintainer rather than a solo account). It describes itself as an open-source alternative to Devin, Factory and 8090.

What it already implements against Mike's list:

| Requirement | What Last Light does | Class |
|---|---|---|
| Isolated execution | Every workflow phase runs in its own sandbox. Five backends behind one interface: a gondolin micro-VM by default, plus Docker, smolvm, Kubernetes, or none. | DOCS |
| Independent reviewer as a role | The build line is Guardrails, Architect, Executor, Reviewer, with fix-feedback loops stacked under the reviewer. Separate phases, separate sandboxes. | DOCS |
| Least privilege per step | Permission profiles downscope the GitHub App token per workflow: `read`, `issues-write`, `review-write`, `repo-write`. Their own words: "A triage run literally cannot push code." | DOCS |
| Config cannot be self-modified | Per-repo `.lastlight/` config is always read from the default branch, "so a PR can't reconfigure the agent reviewing it", and clamped so a repo can only be more conservative than the operator. | DOCS |
| Human approval only where wanted | Workflows pause at explicit human-in-the-loop checkpoints; approve or reject from a GitHub comment, Slack, or the dashboard, and the run resumes where it stopped. | DOCS |
| Provider neutrality | Runs on any model the `pi` coding agent supports. Also supports paying with an existing subscription via `lastlight oauth login` for Claude Pro/Max, ChatGPT Plus/Pro, or GitHub Copilot. | DOCS |
| Declarative rebuild | `npm i -g lastlight`, then a Claude Code skill (`lastlight-server`) that scaffolds, configures and launches the docker stack. Closest thing in the field to "one or two commands on a clean Mac". | DOCS |
| Observability | Eleven-tab admin dashboard, plus every run exports an OpenTelemetry trace with per-turn tokens and cost. | DOCS |
| Evidence and evaluation | Eval harness that runs the real production YAML against a mocked GitHub, with cases authored from the operator's own merged PRs pinned to real base and head SHAs. | DOCS |

Why this matters here specifically: Last Light is built on `pi`, and Mike already runs Pi as a harness. The permission-profile design is also a direct answer to the local failure where a session stalled 19 hours waiting for a folder-approval prompt: the token is downscoped by workflow rather than the human being asked per action.

**What I could not verify:** whether it implements an atomic claim, a fencing generation, or an expected-head merge. The site describes an event router and cron sweeps, both of which can double-dispatch without a claim. Enabling auto-merge on dependency PRs is mentioned, but not a compare-and-swap on the expected head SHA. Those three need a source read before any PASS. **UNVERIFIED.**

### 1.2 AgentWorkforce Factory: AgentWorkforce/factory

**Link:** https://github.com/AgentWorkforce/factory · README at https://raw.githubusercontent.com/AgentWorkforce/factory/main/README.md · accessed 2026-08-29 · **DOCS** plus one **SOURCE**-adjacent doc read

Apache 2.0, TypeScript, 3 stars, 1 fork, 57 open issues, last pushed 2026-08-27. It is the single closest textual match to Mike's brief that I found. Its stated loop is exactly his: discover ready issues, triage, dispatch implement and review agents, open a PR, merge gate, close the issue.

Claims in the README that map onto the irreducible hard controls, quoted rather than paraphrased because the precision is the point:

- **Fenced lease.** "The lifecycle (including a per-run branch, placement results, PR receipt, and a fenced owner lease) is persisted beside the configured loop registry so `factory start` or a replacement dispatch process on the same control-plane host can take over after a crash."
- **Monotonic generation.** On the Durable Object adapter: "Every mutation is checked against the current owner and monotonically increasing lease epoch; an expired host cannot write after takeover." That is a fencing generation with stale-write rejection, named as such.
- **Atomic claim.** For Notion intake: "before creating an issue or spawning an agent, Factory creates one immutable, digest-bound claim in the active Agent Relay workspace. Workspace-global claim-channel uniqueness stops two machines with independent caches from dispatching the same source key. A failed or ambiguous claim write blocks dispatch."
- **Claim writes are verified, not assumed.** "Factory applies the `factory:in-progress` label/state before the dispatch comment, confirms the GitHub label by provider read-back, and retries either write three times. An exhausted write is logged at error level as dead-lettered, recorded as a degraded claim in the registry, and fails the dispatch instead of reporting a clean dispatch with missing GitHub state." This is the exact countermeasure to the local misleading-completion failure class.
- **Cross-process fence on the file backend.** "`FileStateStore` holds a cross-process filesystem lock around the complete read/modify/write, so a second process waits, reloads after it acquires the lock, and then publishes through fsync plus atomic rename. The in-process operation queue alone is not the cross-process fence."
- **Deterministic worker identity.** "the reviewer for `AgentWorkforce/factory#244` uses `factory:dispatch:v1:github:agentworkforce/factory#244:reviewer`. A retry of that work unit can reclaim its deterministic agent name after a crash, while another repository's issue 244 cannot."
- **Fail closed by default.** `mergePolicy` defaults to `never`. Routed-PR babysitter activation is hard-disabled behind a named constant "until the durable lifecycle and completion-CAS design is reviewed." A project that ships the discovery surface with activation disabled pending a CAS review is a project that understands the problem.
- **Isolated workspaces.** Previews are provisioned "immediately after Factory creates the isolated issue worktree", so worktree-per-issue is the model.
- **Independent reviewer.** Separate `implementer`, `reviewer`, `babysitter` roles with distinct broker identities; the babysitter "always leaves the final review and merge to a human."

I confirmed one supporting document directly: https://raw.githubusercontent.com/AgentWorkforce/factory/main/docs/document-state-store.md (accessed 2026-08-29, **DOCS**) specifies a `WatchStateDocumentStore` port whose `runMutation` "must serialize a complete read/modify/write callback against all other writers that share the backend. A compare-and-set backend may retry that callback after a conflict. It must never translate an unreadable or uninitialized backend into `{ version: 3, workspaces: {} }`." That last clause is an explicit anti-fail-open rule at the persistence layer.

**The disqualifying caveats, and they are serious:**

1. **It is not standalone.** It runs against the `agent-relay` broker and, for the hosted control plane, Agent Workforce Cloud. Tokens are `rk_live_`, `at_live_`, `nt_live_`, `ot_live_`. Progress reporting to Cloud is **enabled by default**. That is a vendor dependency at the center of the control plane, which is the opposite of provider-neutral.
2. **Fencing lives on the hosted adapter.** The monotonic lease epoch is described for `DurableObjectHostedFactoryStateStore`, a Cloudflare Durable Object. The local `FileStateStore` gets a filesystem lock, which is mutual exclusion but not a fencing token: it cannot reject a write from a process that acquired the lock, stalled, and woke up stale. Mike's exact hard control is only satisfied on the hosted path. **INFERENCE from the two documents above; not confirmed in source.**
3. **Adoption is essentially zero.** 3 stars, 1 fork. Its dependency `agent-relay` has 804 stars, which is real but small. No verifiable production users outside the vendor.
4. **The merge is a squash merge shelled out to `gh`, and it declines under app identity.** The README's own table: guarded squash merge "cannot be performed as the app today", `"app"` declines and logs. So the promotion step is a `gh` call under a human user's credential, not an app identity. Whether it passes an expected head SHA is **UNVERIFIED**.

I could not read the source. `api.github.com` returned empty through the available fetch tool and GitHub code search requires a login, so every claim above is the project's own prose. Per the brief's point 6, none of it is graded PASS. It is graded PARTIAL with a note that a source read would likely upgrade several rows.

### 1.3 Symphony: openai/symphony

**Link:** https://github.com/openai/symphony · accessed 2026-08-29 · **DOCS** (SPEC.md located and confirmed to exist at 2,189 lines; not yet read in full)

Published by OpenAI on 2026-04-27 as a specification plus an Elixir/BEAM reference implementation. Its central idea is the same as Mike's: **use the issue tracker as the agent control plane**, one task to one dedicated agent, worked autonomously to completion. Reported internally at OpenAI as a 500% increase in landed pull requests, which is a vendor claim and should be treated as marketing until someone reproduces it.

Two things make it strategically important even if the Elixir implementation is not adopted:

1. It is a **spec**, so it is the closest thing to an interoperability standard for this exact lifecycle. A design that conforms to Symphony can later swap implementations.
2. There is already a Rust reimplementation, https://github.com/broomva/symphony ("polls Linear/GitHub/Markdown, creates isolated workspaces, dispatches agent sessions"), which is evidence the spec is separable from the reference code.

**UNVERIFIED and important:** whether the spec mandates an atomic claim, a fencing generation, and an expected-head merge, or leaves them to the implementation. The 2,189-line SPEC.md needs a full read before section B can grade Symphony honestly. Flagged as the single highest-value remaining verification.

### 1.4 SSSF: disler/super-simple-software-factory, and the copy already on this machine

**Link:** https://github.com/disler/super-simple-software-factory · README accessed 2026-08-29 · **DOCS**. Local copy read: `~/agent-workspace/adws/` · **SOURCE**

MIT. Its thesis is the correct one and it states it better than anything else surveyed: "code owns sequencing, retries, and acceptance, and the agent owns only the work inside one bounded phase." Deterministic Python owns the graph, agents are bounded nodes, typed JSON envelopes cross the seams, gates run after the fact against the envelope's own declarations, and every event streams into SQLite while it is still happening.

Genuinely strong parts, verified locally in `~/agent-workspace/adws/adw_modules/`:

- `gates.py` implements `artifacts_exist`, `files_non_empty`, `json_parses`, `diff_matches_claims`, `verdict_consistent`, and `tests_pass(command)`. A gate returns a report of what it checked, not a boolean, so a green gate says what it verified. (SOURCE)
- Write boundaries are enforced in code after every agent call by diffing the repo before and after, with unauthorized changes rolled back and the phase failed. Not a prompt instruction, an actual check. (DOCS, README; the implementing module `changes.py` exists locally but I did not read it)
- Correction rather than restart: a failed gate re-prompts the same live session with the specific violation, so the context window survives.

**And here is the finding that matters most for section F.** The SSSF README carries this warning verbatim:

> "The test phase reports green on a fresh install. `quality.py` ships placeholder commands that exit 0. Three ADWs run them as their test phase." … "Until you wire this, your test phase is theater."

On this machine, in `~/agent-workspace/adws/adw_modules/quality.py`, accessed 2026-08-29 (**SOURCE**):

- line 138 `test()` **is** wired to a real command: `argv=["bash", "tests/test-enforcers.sh"]`, with the inline comment "real suite, not the shipped placeholder".
- line 154 `lint()` is still `_placeholder("lint")`.
- line 163 `typecheck()` is still `_placeholder("typecheck")`.
- line 173 `build()` is still `_placeholder("build")`.
- `_placeholder()` at line 49 returns `["echo", "PLACEHOLDER ..."]`, which exits 0.
- `run_quality()` at line 214 runs all four blocks and collects failures. Three of the four cannot produce one.

So `adw_plan_build_test_quality` on this machine reports a passing quality phase for lint, typecheck and build no matter what the code does. This is the same shape as the `gate_compliance` fail-open in govcon-factory, it is present in a second repo, and unlike that one it is a **documented, expected consequence of an unfinished install** rather than a bug. That distinction is the whole lesson: the framework told the operator this would happen, in bold, and it happened anyway. Written warnings do not enforce.

**What SSSF explicitly does not do,** stated in its own README: "It runs on your current branch. There is no sandbox, no branch per run, no merge step, no cloud, and no human-in-the-loop approval phase." That is roughly half of Mike's lifecycle, absent by design.

### 1.5 Paperclip: paperclipai/paperclip (canonical) / agencyenterprise/paperclip-ai (mirror)

**Link:** https://github.com/paperclipai/paperclip · README read at https://raw.githubusercontent.com/agencyenterprise/paperclip-ai/master/README.md · accessed 2026-08-29 · **DOCS**

MIT, Node plus React, roughly 74k stars (widely reported; I did not read the star count from an API, so treat the figure as **DOCS**, not measured). Org charts, budgets, heartbeats, governance, ticketing, multi-company isolation, mobile-ready dashboard.

It claims one thing directly relevant: "**Atomic execution.** Task checkout and budget enforcement are atomic, so no double-work and no runaway spend." If true and if it extends to the code layer, that is an atomic claim. **UNVERIFIED in source.**

But Paperclip rules itself out of the primary role, in its own words:

> "**Not a code review tool.** Paperclip orchestrates work, not pull requests. Bring your own review process."

Mike's lifecycle *is* the pull request. Steps 6 through 12 of his brief are all PR mechanics. Paperclip is a plausible **command centre** and budget governor sitting above a lifecycle engine, and its cost-control feature is a direct answer to the local failure where five sessions drained one shared five-hour quota with no concurrency control. It is not the lifecycle engine.

**One practical collision worth flagging before anyone installs it:** Paperclip's quickstart starts its API server on `http://localhost:3100`. That is the exact port the FreeLLMAPI gateway occupies on this machine. (README, accessed 2026-08-29, cross-referenced with `~/agent-configs/knowledge/MIKE-INTENT-DEBRIEF-2026-08-28.md`.)

### 1.6 Gas Town and Beads: gastownhall/gastown, steveyegge/beads

**Links:** https://github.com/gastownhall/gastown · https://github.com/steveyegge/beads · accessed 2026-08-29 · **DOCS**

Beads is a git-backed, dependency-graph issue tracker for coding agents: SQLite locally, JSONL exported into git for sync, no central server, with automatic ready-work detection. Gas Town is the orchestrator built on it, running 20 to 30 agents in parallel, with work expressed as "molecules", chained sequences of small beads each carrying acceptance criteria, and a ledger recording every step.

Two corrections to the peer document `Agent SDLC.md`, which I flag because it is the failure class PROPOSAL-0004 names:

- It states Beads has "~25k stars" and Spec Kit "111k stars". I could not confirm either figure from a primary source in this pass. GitHub's HTML star counts were not retrievable through the tooling available to me, and I am not repeating an unverified number as fact. **UNVERIFIED.**
- It states AGENTS.md "was released by OpenAI in August 2025 and transferred to the Linux Foundation's Agentic AI Foundation in late 2025, and now covers 28+ tools and 60,000+ repos." I did not confirm the governance transfer or either count. **UNVERIFIED.**

The peer document's substantive judgement on Gas Town is sound and I agree with it: take the ledger, leave the town. Gas Town solves parallel fan-out across many Claude Code instances; Mike's problem is a single lifecycle that survives death. Adding roughly 189k lines of Go (also an unverified figure from that document) to get a ledger is a bad trade when GitHub Issues is already the ratified queue.

The genuine argument *for* Beads is the one thing GitHub Issues cannot do: a real dependency graph with `bd ready` computing eligible work. The genuine argument against is that Mike has explicitly ratified GitHub Issues as the single queue and called the markdown-file alternative "one of the original sins of trying to do things from scratch". Beads is a third store. Adding it violates the no-parallel-infrastructure rule that `~/agent-configs` already enforces.

### 1.7 gh-aw: github/gh-aw

**Link:** https://github.com/github/gh-aw · docs https://github.github.com/gh-aw/ · changelog https://github.blog/changelog/2026-02-13-github-agentic-workflows-are-now-in-technical-preview/ · accessed 2026-08-29 · **DOCS**

A GitHub-published CLI extension that compiles markdown workflow descriptions into standard GitHub Actions workflows executed by a coding agent. Built-in engines include Copilot, Claude Code, Codex, Gemini, and **Pi**. Technical preview announced 2026-02-13.

Two design decisions are directly load-bearing for Mike:

- **Read-only by default.** Workflows run with read-only permissions and perform write operations only through preapproved "safe outputs". That is a fail-closed default at the permission layer, which is the inverse of the local `X-Sensitivity: public` fail-open posture.
- **It compiles to ordinary Actions YAML.** So the deterministic CI substrate stays deterministic. GitHub's own positioning, per the peer document and consistent with the docs, is that agentic workflows augment CI/CD rather than replace it.

This is the most credible **harness adapter and trigger layer** in the survey, from the most durable maintainer, under a real support commitment. It is not a coordinator: it does not claim work, does not hold a lease, and does not own promotion.

### 1.8 Every name in the brief, resolved

| Name in brief | Resolves to | Status |
|---|---|---|
| AgentWorkforce Factory | `AgentWorkforce/factory` | Real. §1.2 |
| Last Light | `nearform/lastlight` | Real. §1.1 |
| Paperclip | `paperclipai/paperclip` | Real. §1.5 |
| OpenHands SDK / Automation | `OpenHands/software-agent-sdk` | Real. §1.13 |
| Symphony | `openai/symphony` | Real. §1.3 |
| SSSF / Disler Agentic Engineering | `disler/super-simple-software-factory` | Real, and already stamped into `~/agent-workspace/adws/`. §1.4 |
| The Verifier | `disler/the-verifier-agent` | Real. §1.11 |
| GitHub Agentic Workflows (gh-aw) | `github/gh-aw` | Real. §1.7, §1.12 |
| Gas Town | `gastownhall/gastown` | Real. §1.6 |
| Beads | `steveyegge/beads` | Real. §1.6 |
| Agentwerke | nothing found | **UNVERIFIED**. §1.16 |
| Machinist | nothing found | **UNVERIFIED**. §1.16 |
| apra-fleet | `Apra-Labs/apra-fleet` | Real. §1.10 |
| Optio | `jonwiggins/optio` | Real, and the primary recommendation. §1 and §A |
| Jules API | `jules.googleapis.com/v1alpha` | Real. §1.15 |
| ACP, A2A, MCP | see §1.14 | ACP verified locally against the installed SDK |

### 1.9 One answer to a standing open question

`~/agent-configs/knowledge/MIKE-INTENT-DEBRIEF-2026-08-28.md` §5 records an unresolved gap: *"something he calls 'oh my agent' from 'oh my openagent.' I have not been able to identify that project with confidence."*

It is **`code-yeongyu/oh-my-openagent`**, https://github.com/code-yeongyu/oh-my-openagent, accessed 2026-08-29 (**DOCS**, search result title read directly). Self-described as "omo/lazycodex: The coding agent for tokenmaxxers; the one and only agent harness for complex codebases. For your Codex, for your OpenCode." So it is a harness, in the same category as OpenCode and Pi, not an orchestrator. The debrief's gap is closed; the assessment of whether it is worth adopting is not, and I have not made one.

---

### 1.10 apra-fleet: Apra-Labs/apra-fleet

**Link:** https://github.com/Apra-Labs/apra-fleet · accessed 2026-08-29 · **DOCS**

Apache 2.0. A control plane for running agents across real machines: register any Mac, Linux or Windows box (local or over SSH) as a fleet member, dispatch to it, broker credentials. Driven conversationally through MCP, so any MCP-capable agent can operate the fleet. Uses Beads as its backlog.

The parts that matter for Mike's hard controls:

- **Resource ownership separate from task ownership.** The supervisor holds a "member reservation ledger" plus a crash watchdog. That is exactly the separation the brief asks for: a worker reserves a machine, distinct from claiming an issue.
- **Cross-provider review as a stated quality mechanism.** "a different model, with different blind spots, checks every change."
- **Durable workflows, not prompt chains.** "multi-hour, resumable, observable, with member reservations and atomic state", with a journal, turn budgets, and a cooperative pause/resume gate.
- **Anti-false-success on permission writes.** Quoted because it is unusually careful: "a grant is read back off the target member and structurally compared against what was intended before it is reported as applied, so a failed or partial write is surfaced as an explicit failure rather than a false success."
- **Secrets boundary.** Secrets go into a credential store out-of-band and are referenced as `{{secure.NAME}}`, "resolved server-side at execution, never visible to any LLM or log", with per-member scoping, TTL, and network egress policy.
- **The cost argument Mike should read.** Their framing: explore with an LLM orchestrating, then harden the control flow into a deterministic program so shell, git and file steps cost zero tokens and the model is called only at judgment nodes. Same conclusion as SSSF, arrived at independently, with a measured before-and-after on their own end-to-end run.

**What it does not give him:** GitHub Issues as the queue (it uses Beads), and nothing I found describes an expected-head merge. It is a **fleet and machine layer**, not a promotion authority. **UNVERIFIED** on atomic claim semantics and fencing.

### 1.11 The Verifier: disler/the-verifier-agent

**Link:** https://github.com/disler/the-verifier-agent · accessed 2026-08-29 · **DOCS** (README read in full)

MIT. A two-agent observer system for the Pi coding agent. A normal interactive Builder runs in the terminal; a sibling Verifier runs in its own window **with input disabled**, connects over a unix domain socket, reads the builder's session JSONL from disk, and independently re-runs the work with read-only tools. On failure it calls one tool, `verifier_prompt`, which is the only thing it can do that touches the builder. Loop caps at three, then escalates to a human.

Three properties are directly relevant, and one of them is the sharpest idea in this whole survey:

1. **The verifier is structurally un-promptable.** Its input bar is locked. You cannot type at it. The only thing that drives it is a rendered template. Their justification: "You can't fix bugs by typing at the verifier, you fix them by editing the persona, the script, or the prompt template. Improvements solve the entire problem class." That is the enforcement-over-exhortation principle, implemented.
2. **Decomposition is the verifier's job.** "break every claim into the smallest atomic unit that can be independently proven or disproven, then verify each against actual state. A single `PASS` that hides three unverified sub-claims is worse than three explicit `FAIL`s." That is the 42-of-42 failure, described in advance.
3. **Every report lists what could not be verified.** The `CONFIDENCE` ladder has a distinct `PARTIAL` grade meaning "no failures, but significant unverifiable gaps". A gate that can only say pass or fail cannot express that, which is how an unverifiable claim becomes a verified one.

**Limits, stated by the author:** "Read-only is by tool surface, not by sandbox." One verifier per builder, server-side enforced. Late-attach across processes is unsupported. It is a live terminal pairing, not a CI reviewer, so it does not satisfy "reviewer cannot write or merge the candidate" at the promotion boundary. It satisfies it at the authoring boundary, which is a different and also useful thing.

### 1.12 gh-aw safe outputs, verified in the reference docs

**Link:** https://github.github.io/gh-aw/reference/safe-outputs/ · accessed 2026-08-29 · **DOCS**

The one sentence that makes gh-aw architecturally important here:

> "Safe outputs enforce security through separation: agents run read-only and request actions via structured output, while separate permission-controlled jobs execute those requests. This provides least privilege, defense against prompt injection, auditability, and controlled limits per operation."

Read that against Mike's hard controls. "Generator cannot approve its own material work" and "reviewer cannot write or merge the candidate" are both instances of one pattern: **the agent proposes, a separate identity with narrow permissions disposes.** gh-aw ships that pattern as its default. It also has a staged mode in which "staged runs must not perform API side effects", which is a dry-run with teeth.

### 1.13 OpenHands SDK

**Link:** https://github.com/OpenHands/software-agent-sdk · docs https://docs.openhands.dev/sdk · accessed 2026-08-29 · **DOCS**, search-level only

A Python and REST SDK for building software agents: run locally or in the cloud, define custom behaviours and tools, with ready-made bash, file-edit, browse and MCP tools. Purpose-built for software engineering rather than general agents.

This is an **agent runtime**, one layer below everything else in this survey. It is a credible harness adapter and a credible way to run a worker, and it is not a coordinator, a queue, a reviewer, or a promotion authority. It does not compete with Optio or Last Light; it is a thing they could call. I did not verify it at source and have graded it accordingly.

### 1.14 Interop protocols: ACP, A2A, MCP

The most reliable evidence on this machine is already written down, verified against the installed SDK rather than a website: `~/agent-workspace/knowledge/acp-surface-antigravity-buzz-endpoint-2026-08-27.md`, accessed 2026-08-29 (**LOCAL**, itself **SOURCE**-grade against `agent-client-protocol` 0.9.0, schema tag v0.11.2, wire version 1).

Its finding, which I adopt unchanged:

> "ACP gives you sessions, prompts, streaming, permissions, and model selection. It does not give you profiles, toolsets, or provider registration." … "It does not give cross-vendor handoff, because Codex, Grok and Gemini do not speak it. That gap is why durable state has to live in the repo and the issue tracker rather than in any protocol."

That is the whole interop answer for this design. Model switch, fork and resume exist but are *unstable* protocol methods, live only because `entry.py` passes `use_unstable_protocol=True`. Building a lifecycle on an unstable method is a bad idea.

MCP is the one protocol with broad, stable, cross-vendor adoption in this survey: apra-fleet is MCP-native, Optio injects MCP servers into agent pods, gh-aw enables MCP toolsets, and the OpenHands SDK ships MCP tools. A2A is agent-to-agent messaging and, as apra-fleet's own comparison table puts it, a transport rather than an orchestration layer.

**Practical conclusion:** use MCP for tool access, use GitHub for coordination, and do not put any hard control on ACP or A2A. **INFERENCE**, supported by the sources above.

### 1.15 Jules API

**Link:** https://developers.google.com/jules/api/reference/rest/v1alpha/sessions · blog https://developers.googleblog.com/en/level-up-your-dev-game-the-jules-api-is-here/ · accessed 2026-08-29 · **DOCS**

`jules.googleapis.com/v1alpha`, authenticated with `X-Goog-Api-Key`. Three resources: Sources, Sessions, Activities. Sessions support `create`, `get`, `list`, `sendMessage`. Activities are the individual events inside a session (plan generated, message sent, completion) and support `get` and `list`.

For Mike's purposes this is a clean **asynchronous worker adapter**: create a session, poll activities, harvest the PR. It is `v1alpha`, so treat the surface as unstable. It carries no claim, no lease, and no promotion authority, and being Google-hosted it is the least provider-neutral worker in the set. It belongs behind an adapter, never in the control path.

### 1.16 Names I could not resolve

| Name in the brief | Result |
|---|---|
| Machinist | No matching agent-orchestration project found in this pass. **UNVERIFIED** |
| Agentwerke | No matching project found in this pass. **UNVERIFIED** |

Both may exist under a different spelling, in a private repo, or as something Mike saw referenced rather than published. I am not going to invent a project to fill a row.

Related projects surfaced during the search that are **not** in the brief and may be worth a look later, all **DOCS**-level only: `chankov/agent-fleet` (Pi-first dispatcher with a "Verification Contract"), `HKUDS/ClawTeam` (worker per git worktree plus tmux window), `desplega-ai/agent-swarm` (lead agent delegating to Docker-isolated workers), `broomva/symphony` (Rust implementation of the OpenAI Symphony spec), `AgentWrapper/agent-orchestrator`, `escapeboy/agent-fleet-o`.

---

## 2. Substrate: what GitHub already gives you for free

This section matters more than any project comparison, because three of Mike's hard controls turn out to be single API parameters he is not currently using. All verified in GitHub's own REST documentation on 2026-08-29 (**DOCS**, read directly from docs.github.com).

### 2.1 Expected-head compare-and-swap on merge: already exists

`PUT /repos/{owner}/{repo}/pulls/{pull_number}/merge` accepts a body parameter:

> `sha` string, "SHA that pull request head must match to allow merge."

and returns:

> `409`, "Conflict if sha was provided and pull request head did not match"

Source: https://docs.github.com/en/rest/pulls/pulls?apiVersion=2022-11-28#merge-a-pull-request, accessed 2026-08-29.

That is the entire "promotion must use an expected-head compare-and-swap" requirement, satisfied by one field. Any merge that omits `sha` promotes whatever is at the head of the branch at merge time, which is not necessarily the revision that was reviewed and tested.

**And Optio omits it.** Verified in source at https://raw.githubusercontent.com/jonwiggins/optio/main/apps/api/src/services/git-platform/github.ts, accessed 2026-08-29 (**SOURCE**):

```ts
async mergePullRequest(ri, prNumber, method): Promise<void> {
  await this.fetchJson(this.url(ri, `/pulls/${prNumber}/merge`), {
    method: "PUT",
    headers: this.headers(true),
    body: JSON.stringify({ merge_method: method }),
  });
}
```

The body carries `merge_method` and nothing else. The caller, `applyAutoMergePr` in `apps/api/src/services/reconcile-executor.ts`, passes only `(ri, parsed.prNumber, "squash")`. So the most rigorous candidate in this survey, the one that gates every database write on a compare-and-swap, does not gate its **merge** on one. If a commit lands on the PR branch between the review approving and the reconciler firing, Optio merges the unreviewed commit and closes the issue.

The fix is small and the data is already there: `mapPr()` in the same file already extracts `headSha: data.head?.sha`. It is captured, stored on the task row as part of the PR snapshot, and then not used at the one moment it matters.

### 2.2 An atomic claim primitive: already exists

`POST /repos/{owner}/{repo}/git/refs` requires `ref` and `sha` and returns `201 Created`. Creating a ref that already exists fails validation rather than overwriting. `PATCH /repos/{owner}/{repo}/git/refs/{ref}` takes `force`, documented as:

> "Indicates whether to force the update or to make sure the update is a fast-forward update. Leaving this out or setting it to false will make sure you're not overwriting work." Default: `false`.

Source: https://docs.github.com/en/rest/git/refs?apiVersion=2022-11-28, accessed 2026-08-29.

So `refs/claims/issue-123` is a real, server-side, atomic create-if-absent. First writer wins, second gets a validation failure, and the winner is recorded in git rather than in a process's memory. Renewing the lease is a non-forced ref update, which is itself a compare-and-swap against the previous value.

This matters because the local failure was precisely two sessions racing the same work in a shared checkout, and because Symphony, the OpenAI spec, keeps its claim set in one process's memory (see 2.4).

### 2.3 Mutual exclusion in Actions: exists, with a trap

GitHub Actions `concurrency` groups: "GitHub Actions ensures that only one workflow or job with that key runs at any given time." Source: https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#concurrency, accessed 2026-08-29.

The trap, from the same page: "If a new workflow run or job starts with the same concurrency key, GitHub Actions will **cancel** any workflow or job already running with that key." That is last-writer-wins, which is the opposite of what a claim needs. A newly started run would kill a healthy in-flight worker. With `cancel-in-progress: false` the newcomer queues instead, which is closer to correct but still gives you mutual exclusion without a fencing token: nothing stops a job that stalled, lost its slot and then woke up from performing a write.

**Concurrency groups are not a substitute for a fencing generation.** They are a useful second belt.

### 2.4 What this means for the candidates

Once you know the three primitives above exist, the candidate scoring changes:

- **Symphony** explicitly declines durable coordination. Its own spec: "Restart recovery is tracker-driven and filesystem-driven (**without a durable orchestrator DB**)", and its claim state is an in-process set (`state.claimed = set()`, `state.claimed.add(issue.id)`). Two orchestrators double-dispatch. Source: openai/symphony SPEC.md §7.1, §7.4, and the pseudocode at lines 1708 and 1820, accessed 2026-08-29 (**DOCS**, spec text read directly).
- **Symphony also stops before promotion.** Its own words: "Ticket writes (state transitions, comments, PR links) are typically performed by the coding agent" and "A successful run can end at a workflow-defined handoff state (for example `Human Review`), not [terminal state `Done`]". So the agent writes its own status and the human finishes the job. That is the self-report failure mode Mike already has, standardised.
- What Symphony **does** mandate and does well: per-issue workspace directories ("It isolates agent execution in per-issue workspaces so agent commands run only inside per-issue workspace directories"), global and per-state concurrency caps, blocker-aware eligibility, exponential-backoff retries, stall timeouts, and reconciliation before dispatch on every tick.

### 2.5 Durable-execution engines: Temporal, Restate, Hatchet, Inngest

**DOCS**, secondary-source level only. I did not read any of these projects' source in this pass and am not grading them PASS on anything.

The category is real and mature: a function that resumes exactly where it left off after a crash. Restate assigns each virtual object a key and replays a journal, giving exactly-once semantics without application-level idempotency keys. Temporal gives exactly-once replay of workflow decisions but at-least-once activities, so anything mutating external state still needs an idempotency key. Hatchet and Inngest occupy the same space with simpler operational models.

**My recommendation is not to adopt one, and the reason is specific.** These engines solve durable *execution*. Mike's binding constraint is durable *coordination and evidence*: which agent owns which issue, whether the thing that was reviewed is the thing that was merged, and whether a claimed pass is real. A durable execution engine would make the orchestrator survive a crash, which Optio's Postgres plus reconciler already does, and would add a second control plane, a second state store, and a second operational surface to a one-person operation. That is the parallel-infrastructure trap `~/agent-configs/rules/no-parallel-infrastructure.md` already names.

The honest counterargument: if the orchestrator itself becomes the thing that keeps dying, a durable execution engine is the right answer and the cost is worth it. Revisit this only if that happens.

---

## A. Executive recommendation

### The call: fork one project narrowly and add a thin control layer. Do not build an orchestrator.

**Primary recommendation: adopt Optio (https://github.com/jonwiggins/optio, MIT) as the lifecycle engine and fork it narrowly, in three places.**

The reason is not that Optio is the most featureful, though it is close. It is that Optio is the only candidate where I could open the source and see the hard controls implemented rather than described. Its reconciler reads a frozen world snapshot, runs a pure decision function with no I/O, and applies exactly one typed action through a compare-and-swap gated on the row version. When the CAS fails it returns `"stale"` and re-enqueues for a fresh pass rather than writing. Every one of the four run kinds goes through the same executor. That is Mike's "stale-generation write rejection" as running code, in a file I can name: `apps/api/src/services/reconcile-executor.ts`, function `casUpdate`, accessed 2026-08-29.

It also brings, for free, most of what would otherwise be greenfield: git worktree isolation per task, a separate code-review agent launched as its own subtask with its own prompt and model, CI polling with auto-resume on failure, merge-conflict rebase prompts, issue closure on merge, Postgres durable state, a Helm chart plus a `setup-local.sh` for a clean-host rebuild, GitHub App identity, encrypted secrets at rest, and adapters for Claude Code, Codex, Copilot, Gemini and OpenCode.

**The three narrow changes:**

1. **Pass `sha` to the merge call.** Verified missing at source (§2.1). `mapPr()` already captures `headSha`. Bind the reviewed revision to the promoted revision, and let GitHub's `409` be the enforcement.
2. **Make the reviewer a different principal, not just a different subtask.** Optio launches a review agent with a separate prompt and model, which is a good start and is not identity separation. Mike's local record shows exactly what happens without it: 93 reviews, one bot, 40 PRs. Give the reviewer its own GitHub App installation token with `pull-requests: write` and no `contents: write`, following the gh-aw safe-outputs pattern (§1.12). Then "reviewer cannot write or merge the candidate" is enforced by the token, not by the prompt.
3. **Add a git-ref claim in front of dispatch.** Optio's CAS protects its own database. It does not stop a second Optio instance, a Claude Code session, or Mike at a terminal from working the same issue. A `refs/claims/issue-<n>` ref carrying the owner and a monotonically increasing generation (§2.2) is roughly fifty lines and makes the claim visible to every tool on the machine, not just to Optio.

Everything else Mike listed is either already in Optio, or is deferred (see F).

**Strongest challenger: Last Light (https://github.com/nearform/lastlight, MIT).**

It wins on three axes Optio loses: no Kubernetes requirement, an explicit permission-profile system that downscopes the GitHub App token per workflow, and it is built on `pi`, which Mike already runs. It also ships an eval harness that replays the real production workflows against a mocked GitHub with cases pinned to real base and head SHAs, which is the closest thing in the field to a deterministic acceptance test for the orchestrator itself. And its per-repo config is always read from the default branch, so a PR cannot reconfigure the agent reviewing it.

It loses on one axis, and it is the deciding one: **I could not verify its claim, fencing, or merge semantics.** The site describes webhooks and cron sweeps, both of which double-dispatch without a claim, and describes enabling auto-merge on dependency PRs without mentioning an expected head. Those three questions are answerable in an afternoon by reading the repo, and if the answers are good, Last Light is the better fit for a solo operator on a Mac. **I am recommending Optio because I verified it, and flagging that this could reverse.**

**Runners-up, and what each is actually for:**

| Project | Right role | Wrong role |
|---|---|---|
| AgentWorkforce Factory | The design document. Read its README for the vocabulary. | The engine. It depends on a vendor broker and Cloud, with 3 stars. |
| Symphony (OpenAI) | The interoperability reference and a source of good eligibility rules. | The coordinator. No durable state, in-memory claims, stops before promotion. |
| gh-aw | The trigger and safe-output layer, and the pattern for reviewer isolation. | The coordinator. It holds no lease and owns no promotion. |
| SSSF | The in-repo phase runner for multi-step work inside one task. Already stamped here. | The lifecycle. No branch, no sandbox, no merge, by its own admission. |
| The Verifier | The authoring-time reviewer that catches claims before they reach a PR. | The promotion-time reviewer. Read-only by tool surface, not by sandbox. |
| apra-fleet | The machine and credential layer if work ever spans more than one box. | Today. One Mac does not need a fleet. |
| Paperclip | A budget and cost governor, and a possible phone-facing view. | The lifecycle. "Not a code review tool", in its own words. |
| Beads / Gas Town | Nothing here yet. | A second work queue, against a ratified decision. |
| Jules / OpenHands SDK | Worker adapters behind an interface. | Anything in the control path. |

**What must not be built:** a bespoke orchestrator. `~/agent-mesh/Agent SDLC.md` proposes one and calls it `agentd`, with the responsibility list "read workflow state, claim task, select provider, launch CLI, observe process, checkpoint, detect quota/error, rotate provider, run validation, update GitHub, repeat." Every line of that list exists in Optio today, tested, with the decision logic written as pure functions and exhaustively unit-tested. Writing it again is the sixth derivation.

---

## B. Feature matrix

**Grading rule, applied strictly.** PASS requires either code I read or documentation so specific that a wrong claim would be a falsehood, and every PASS carries its link below the table. PARTIAL means the capability exists but is incomplete, conditional, or only on one deployment path. FAIL means I have positive evidence it is absent. UNKNOWN means I could not determine it, which is different from FAIL and is said so.

Candidates carried into the matrix: the ones with a real repository and a real claim on the lifecycle. Beads, Gas Town, Jules, OpenHands SDK, The Verifier and Paperclip are scored on the rows where they compete and marked "n/a" where they do not compete at all, because grading a work ledger on merge authority is noise.

### B.1 Coordination and state

| Capability | Optio | Last Light | AW Factory | Symphony | apra-fleet | SSSF | gh-aw |
|---|---|---|---|---|---|---|---|
| Atomic task claim | PARTIAL | UNKNOWN | PARTIAL | PARTIAL | UNKNOWN | FAIL | FAIL |
| Resource locking separate from task | PARTIAL | UNKNOWN | UNKNOWN | PARTIAL | **PASS** | FAIL | PARTIAL |
| Fencing generation | PARTIAL | UNKNOWN | PARTIAL | FAIL | UNKNOWN | FAIL | FAIL |
| Stale-generation write rejection | **PASS** | UNKNOWN | PARTIAL | FAIL | UNKNOWN | FAIL | FAIL |
| Isolated workspaces | **PASS** | **PASS** | PARTIAL | **PASS** | PARTIAL | FAIL | **PASS** |
| Durable state | **PASS** | PARTIAL | PARTIAL | FAIL | PARTIAL | PARTIAL | PARTIAL |
| Checkpoint and resume | **PASS** | PARTIAL | PARTIAL | PARTIAL | PARTIAL | PARTIAL | FAIL |
| Crash recovery | **PASS** | UNKNOWN | PARTIAL | PARTIAL | PARTIAL | FAIL | PARTIAL |

### B.2 Evidence, review and promotion

| Capability | Optio | Last Light | AW Factory | Symphony | apra-fleet | SSSF | gh-aw |
|---|---|---|---|---|---|---|---|
| Exact input/candidate binding | PARTIAL | PARTIAL | PARTIAL | FAIL | UNKNOWN | PARTIAL | PARTIAL |
| Deterministic CI evidence | **PASS** | **PASS** | PARTIAL | FAIL | PARTIAL | PARTIAL | **PASS** |
| Independent reviewer identity | PARTIAL | PARTIAL | PARTIAL | FAIL | PARTIAL | PARTIAL | **PASS** |
| Expected-head automatic merge | **FAIL** | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | FAIL | FAIL |
| Issue and Project synchronization | PARTIAL | PARTIAL | PARTIAL | PARTIAL | FAIL | FAIL | **PASS** |
| Teardown and rollback receipts | PARTIAL | PARTIAL | PARTIAL | PARTIAL | PARTIAL | PARTIAL | PARTIAL |

### B.3 Neutrality, operability, health

| Capability | Optio | Last Light | AW Factory | Symphony | apra-fleet | SSSF | gh-aw |
|---|---|---|---|---|---|---|---|
| Provider neutrality | **PASS** | **PASS** | PARTIAL | PARTIAL | **PASS** | **PASS** | **PASS** |
| Harness neutrality | **PASS** | PARTIAL | PARTIAL | FAIL | **PASS** | PARTIAL | **PASS** |
| Declarative clean-host rebuild | **PASS** | **PASS** | PARTIAL | PARTIAL | **PASS** | **PASS** | PARTIAL |
| API / control-plane suitability | **PASS** | **PASS** | PARTIAL | PARTIAL | **PASS** | FAIL | PARTIAL |
| Mobile command-centre suitability | PARTIAL | PARTIAL | PARTIAL | FAIL | PARTIAL | FAIL | PARTIAL |
| Maintenance health | PARTIAL | **PASS** | PARTIAL | PARTIAL | PARTIAL | PARTIAL | **PASS** |
| License and commercial reuse | **PASS** MIT | **PASS** MIT | **PASS** Apache 2.0 | UNKNOWN | **PASS** Apache 2.0 | **PASS** MIT | UNKNOWN |

### B.4 Sources for every material PASS

All accessed 2026-08-29.

**Optio**
- Stale-generation write rejection: SOURCE. `casUpdate()` and the `"stale"` outcome in https://raw.githubusercontent.com/jonwiggins/optio/main/apps/api/src/services/reconcile-executor.ts. Every applicator returns `{status:"stale"}` on version mismatch and the worker re-enqueues; the executor's own docstring: "All DB mutations are CAS-gated on `updated_at == snapshot.run.status.updatedAt` so a decision made from a stale snapshot cannot overwrite a concurrent transition."
- Isolated workspaces, durable state, checkpoint/resume, crash recovery: DOCS, specific. https://raw.githubusercontent.com/jonwiggins/optio/main/docs/reconciliation.md ("A snapshot is frozen … the executor's CAS check refuses to write if the row moved underneath it"; "Periodic resync. Every 5 minutes … scans non-terminal runs across all four tables"; four reconcile columns in migration `1776686400_reconcile_columns.sql`) plus README ("creates a git worktree for isolation"; Postgres 16 for tasks, workflows, agents, inboxes, connections, logs, secrets).
- Deterministic CI evidence: SOURCE. `getCIChecks()` reads `/commits/{sha}/check-runs` in `git-platform/github.ts`; the reconciler's `autoMergePr` action fires only on "PR is approved, CI green, auto-merge enabled".
- Provider and harness neutrality: DOCS. `packages/agent-adapters/` for Claude Code, Codex, Copilot, Gemini, OpenCode, per README project structure.
- Declarative clean-host rebuild: DOCS. `./scripts/setup-local.sh` and `helm install optio optio/optio`.
- API/control-plane suitability: DOCS. Unified `/api/tasks` HTTP surface, `/api/internal/persistent-agents/*`, WebSocket log streaming.
- License: DOCS. MIT badge and `./LICENSE` in the repo root.

**Last Light**
- Isolated workspaces: DOCS. "Each workflow phase runs in its own sandbox, and five backends sit behind one interface: a gondolin micro-VM by default, or Docker, smolvm, Kubernetes, or none." https://lastlight.dev/
- Deterministic CI evidence: DOCS. Eval harness runs "the same triage, review, and build YAML that runs in prod" against a mocked GitHub, with cases from real merged PRs that pin "the real base/head SHAs".
- Provider neutrality: DOCS. "runs on any model the pi coding agent supports"; also subscription auth via `lastlight oauth login`.
- Declarative clean-host rebuild: DOCS. `npm i -g lastlight`, then the `lastlight-server` Claude Code skill scaffolds and launches the docker stack.
- API/control-plane suitability: DOCS. Built-in webhook listener on `:8644`, CLI-to-server split, `/admin` dashboard, OpenTelemetry export.
- Maintenance health: DOCS. Published under the `nearform` org with a public roadmap project board; a named company rather than an anonymous account.
- License: DOCS. "MIT License" stated on the site footer and in the repo.

**apra-fleet**
- Resource locking separate from task: DOCS, specific. "member reservation ledger, crash watchdog … run history" under the Supervisor; workflows have "member reservations and atomic state". https://github.com/Apra-Labs/apra-fleet
- Provider and harness neutrality: DOCS. "Claude, Codex, Copilot, Antigravity, local models (any OpenAI-compatible endpoint via OpenCode), mixed freely", across macOS, Linux and Windows members.
- Declarative clean-host rebuild: DOCS. `npm install -g @apralabs/apra-fleet` then `apra-fleet start`.
- API/control-plane suitability: DOCS. MCP server plus a supervisor HTTP API for launch, pause, resume and stop.
- License: DOCS. Apache 2.0 badge and `LICENSE`.

**Symphony**
- Isolated workspaces: DOCS, spec-mandated. "It isolates agent execution in per-issue workspaces so agent commands run only inside per-issue workspace directories" and a Workspace Manager component that "Ensures per-issue workspace directories exist". openai/symphony `SPEC.md` lines 29 to 30 and 99 to 103.

**gh-aw**
- Independent reviewer identity: DOCS, specific and architectural. "agents run read-only and request actions via structured output, while separate permission-controlled jobs execute those requests." https://github.github.io/gh-aw/reference/safe-outputs/
- Deterministic CI evidence: DOCS. Compiles to standard GitHub Actions workflows; the deterministic YAML is untouched.
- Issue and Project synchronization: DOCS. Safe outputs cover issue creation, comments, labels and project updates as separate permission-gated jobs.
- Provider and harness neutrality: DOCS. Built-in engines: Copilot, Claude Code, Codex, Gemini, Pi. https://github.com/github/gh-aw
- Maintenance health: DOCS. Published by GitHub, technical preview announced 2026-02-13 in the official changelog.

**SSSF**
- Provider neutrality: SOURCE, local. `provider/model-id` roster with per-agent overrides, verified in `~/agent-workspace/adws/adw_sssf_config/`.
- Declarative clean-host rebuild: DOCS plus local. `uv run .claude/skills/sssf/scripts/install.py`, idempotent, `--force` to refresh.
- License: DOCS. MIT.

### B.5 The gradings that will surprise, and why

**Optio scores FAIL on expected-head merge, and that is the single most important cell in the matrix.** Verified at source in §2.1. It is the only FAIL I am confident enough in to assert against a project that otherwise leads the table, and it is also the cheapest to fix.

**Optio scores only PARTIAL on atomic claim.** Its CAS protects its own `tasks` row. Two Optio deployments, or Optio plus a human at a terminal, are not mutually excluded. Given the local evidence of exactly that collision, the row is PARTIAL, not PASS.

**Optio scores PARTIAL on fencing generation.** The version token is a `timestamptz` truncated to milliseconds, not a monotonically increasing counter. The code carries a comment about a real bug this caused: a raw equality comparison "silently never matches rows whose updated_at carries microseconds … which made every standalone transition from such rows permanently stale." A timestamp is a usable version token and it is not a fencing generation, because two writes in the same millisecond are indistinguishable and a clock adjustment is a correctness event. Mike's brief says "monotonically increasing fencing generation" and means it.

**Nobody scores PASS on independent reviewer identity except gh-aw**, and gh-aw is not a coordinator. Optio and Last Light both launch a reviewer as a separate agent with a separate prompt and model, which is separation of *behaviour*. Mike's requirement is separation of *authority*: the reviewer must be unable to write or merge, enforced by credential. Only gh-aw's safe-outputs model does that structurally, and only because the agent has no write token at all.

**Nobody scores PASS on teardown and rollback receipts.** Every candidate logs. Several produce good traces: Optio's `reconcile.decision` lines with `applied | shadow | stale | deferred | error`, SSSF's seven-table SQLite trace, Last Light's OpenTelemetry spans. None of them produces a *receipt* in Mike's sense, meaning a durable, addressable artifact binding issue to input revision to candidate revision to test result to reviewer to promoted revision to cleanup. That is a genuine gap across the whole field and it is the second thing that has to be built.

**Symphony scores FAIL on durable state**, on its own testimony: "Restart recovery is tracker-driven and filesystem-driven (without a durable orchestrator DB)."

**AgentWorkforce Factory could not be graded above PARTIAL anywhere**, purely because I could not read its source. Its README describes more of Mike's hard controls, by name, than anything else in the survey. Per the brief's point 6, a description is not an implementation. If someone reads that source and finds it real, several of its cells move up, and its vendor-broker dependency still keeps it out of the primary recommendation.

---

## C. Architecture recommendation

The smallest thing that satisfies the brief. Four boxes, one of which is small and new.

```
                     GitHub  (the only durable coordination surface)
   Issues = queue          refs/claims/* = leases        Projects = human view
   PR + Checks = evidence  merge?sha = the CAS gate      Releases/comments = receipts
                                  │
              ┌───────────────────┼───────────────────┐
              │                   │                   │
      ┌───────▼───────┐   ┌───────▼────────┐   ┌──────▼───────────┐
      │  OPTIO        │   │  claim-fence   │   │  gh-aw workflows │
      │  (adopted)    │   │  (NEW, small)  │   │  (adopted)       │
      │               │   │                │   │                  │
      │ reconciler    │   │ git-ref claim  │   │ deterministic CI │
      │ CAS state     │   │ generation N   │   │ reviewer job     │
      │ worktrees     │   │ receipt writer │   │ safe outputs     │
      │ CI polling    │   │ merge?sha      │   │ read-only agents │
      │ auto-resume   │   └────────────────┘   └──────────────────┘
      │ review subtask│
      └───────┬───────┘
              │  agent-adapters (already in Optio)
    ┌─────────┼─────────┬──────────┬──────────┬─────────┐
    ▼         ▼         ▼          ▼          ▼         ▼
 Claude    Codex     Copilot    Gemini    OpenCode   (Pi, Jules,
  Code                                                Hermes/Buzz
                                                      via adapter)
```

### Adopted components, unchanged

| Component | Source | What it owns |
|---|---|---|
| Lifecycle engine | Optio, MIT | Discovery, dispatch, provisioning, worktrees, CI polling, auto-resume, review launch, issue closure, dashboard, cost tracking |
| State store | Postgres 16 (inside Optio) | Task, workflow, review and agent rows with CAS columns |
| Queue | Redis + BullMQ (inside Optio) | Reconcile queue with dedup key `${kind}__${id}` |
| Deterministic verification | GitHub Actions, plain YAML | Tests, lint, typecheck, build, security scans. Never agentic |
| Trigger and safe-output layer | gh-aw, GitHub-published | Read-only agent jobs plus separate permission-gated write jobs |
| In-task phase runner | SSSF, MIT, already stamped in `~/agent-workspace/adws/` | Multi-phase work *inside* one claimed issue: plan, build, gate, envelope |
| Agent adapters | Optio's `packages/agent-adapters/` | Claude Code, Codex, Copilot, Gemini, OpenCode. Add Pi and Hermes here later |

### Narrowly forked component

**Optio, three changes, all in files I have named.**

1. `apps/api/src/services/git-platform/github.ts`: add an optional `expectedHeadSha` to `mergePullRequest` and put it in the request body as `sha`. Treat `409` as a distinct, non-retryable outcome that reopens the review rather than an error.
2. `apps/api/src/services/reconcile-executor.ts`, `applyAutoMergePr`: read the head SHA that the *review* approved, not the head SHA at merge time, and pass it. The reviewed SHA must be stored on the review record when the approval lands.
3. `apps/api/src/services/review-service.ts`: mint the review agent's GitHub token from a second App installation that has `pull-requests: write` and lacks `contents: write`.

Fork discipline: these are three surgical patches carried as a branch, rebased on upstream. If they are good, they go upstream as PRs. Nothing else is modified, ever, or the fork becomes a rewrite.

### Platform-owned code that is genuinely unavoidable

Two things, and only two. Everything else is adoption.

**C1. The claim-fence.** Perhaps 150 lines.

- Claim: `POST /git/refs` creating `refs/claims/issue-<n>` pointing at a claim blob containing `{owner, generation, phase, expected_until, base_sha}`. 201 wins, 422 means someone else holds it.
- Renew: non-forced `PATCH /git/refs/...` with `generation + 1`. A forced update is never permitted.
- Every subsequent write by the worker carries its generation. Any write whose generation is lower than the ref's current generation is refused by the writer itself before the API call, and by the ref CAS if it races.
- `phase` and `expected_until` come straight from PROPOSAL-0004 and exist to solve one specific local failure: session `fcaae84e` stalled 19 hours on an approval prompt and was indistinguishable from a dead session. A reaper cannot tell stalled from dead without that field.
- Release: delete the ref, and record why.

**C2. The receipt writer.** Perhaps 200 lines. This is the thing no candidate provides.

One append-only JSON object per lifecycle event, written to a `receipts/` path on an orphan branch (so it never pollutes the code history) and mirrored as a single issue comment between sentinels. Seven receipt types, matching the brief: claim, implementation, tests, review, promotion, projection, cleanup, plus recovery.

The promotion receipt is the one that matters and it carries exactly six fields: `issue`, `base_sha` (the input revision), `candidate_sha` (what was tested and reviewed), `check_run_ids` (what actually ran), `reviewer_identity`, `promoted_sha` (what GitHub returned), and `generation`. If `candidate_sha` and `promoted_sha` differ, the merge was not a compare-and-swap and the receipt says so in writing.

Every receipt line that states a number also carries what it does not establish. That is the `BOUNDARY` field from PROPOSAL-0004, and it exists because a "42 of 42, all green" claim from a different pipeline propagated as fact on this machine for days.

### Authority and state boundaries

| Boundary | Rule | Enforced by |
|---|---|---|
| Who may claim | Anyone who can create a ref | GitHub ref create, 422 on collision |
| Who may write to a candidate branch | Only the holder of the current generation | Claim-fence check plus branch protection |
| Who may approve | The reviewer App installation only | Token scope, no `contents: write` |
| Who may merge | Only the Optio control plane, only with `sha` | GitHub 409 |
| Who may change gates, rules, AGENTS.md | Mike, Tier 2 | Branch protection with required review, CODEOWNERS |
| Who may delete anything | Nobody automatically | APPROVAL_DESTRUCTIVE, human |

### GitHub and App identities

Three GitHub App installations, not one. This is the single most important structural change relative to what exists here today, where one bot did 93 reviews.

| Identity | Permissions | Used for |
|---|---|---|
| `swarm-worker` | Contents RW, Pull requests RW, Issues RW, Checks read, Metadata read | Cloning, branching, pushing, opening PRs, claiming refs |
| `swarm-reviewer` | Pull requests RW, Contents **read only**, Metadata read | Submitting reviews. Structurally incapable of pushing or merging |
| `swarm-promoter` | Pull requests RW, Contents RW, Issues RW | The merge call and the issue close, nothing else. Invoked only by the reconciler |

The permission tables for both Optio and Last Light already enumerate the individual scopes, so splitting them is configuration rather than code.

### CI runners

GitHub-hosted runners for everything deterministic. Self-hosted runners only if a job needs local inference against `omlx` on `127.0.0.1:8300`, and in that case the runner is scoped to one repository and never runs a workflow from a fork. Deterministic YAML never invokes a model. gh-aw workflows are a separate, read-only lane.

Do not move to Forgejo, GitLab or OneDev. None of them eliminates work here: they all offer roughly the same merge and ref primitives, and switching costs the GitHub Projects command centre that Mike has already ratified. **INFERENCE**, based on the primitive set in §2 being generic to git forges.

### Receipt storage

Receipts live in git, on an orphan `receipts` branch in the same repository, plus the mirrored issue comment. Not a database, not S3, not a new service. Rationale: git is already the durable store, receipts must survive the orchestrator being deleted and reinstalled, and `no-parallel-infrastructure` forbids the alternative. Optio's Postgres holds live state; git holds the permanent record. Those are different jobs and it is correct that they are different stores.

### Secrets boundary

Provider keys in the existing FreeLLMAPI gateway and `~/.hermes/.env` / Keychain, referenced by name only, per the standing `agent-mesh` AGENTS.md rule. GitHub App private keys as Kubernetes secrets referenced by `existingSecret`, which Optio already supports. No secret ever appears in a task prompt, a receipt, an issue comment, or a log.

**One open security item, already found and unfixed, that this design inherits:** Hermes sets `X-Sensitivity: public` on its gateway provider in the root config and in all twelve profiles, so all traffic is labelled public and lands in the unrestricted pool by default. That is fail-open. Source: `~/agent-workspace/knowledge/acp-surface-antigravity-buzz-endpoint-2026-08-27.md` (LOCAL), also recorded as backlog item #24. It must be fixed before any customer data flows through a swarm task.

### Rebuild mechanism

```
git clone <infra-repo> && cd infra && ./bootstrap.sh
```

`bootstrap.sh` does four things and nothing else: install prerequisites, `helm install optio` with a values file from the repo, apply the three GitHub App configs from the repo, and stamp the gh-aw workflows. Everything it reads is in version control. Nothing it writes is.

**In git:** AGENTS.md, prompts, roles, skills, cookbooks, policies, gate definitions, workflow YAML, Helm values, the Optio fork patches, receipt schemas, the claim-fence source.

**Not in git, and gitignored with a comment saying why:** credentials, caches, sessions, the Postgres volume, Redis, model files, worktrees, `.pi/`, `adws/adw_data/sessions/`, `sssf.db`.

---

## D. First working vertical slice

One demonstration. It either passes end to end or the design is wrong. Nothing else gets built until it passes.

**Scope:** one repository, one issue label, one deterministic test command, one reviewer, two workers.

**The happy path being proved:**
GitHub issue → atomic claim → isolated implementation → deterministic checks → independent review → automatic expected-head merge → issue close → cleanup receipt.

### D.1 Setup

- A throwaway repo, `swarm-slice`, with one source file, one real test suite that can actually fail, and branch protection requiring a review from `swarm-reviewer` and a green `verify` check.
- One issue, `#1`, labelled `swarm-ready`: "Add a `slugify(text)` function. Must lowercase, strip punctuation, collapse whitespace to single hyphens. Tests are in `tests/test_slugify.py` and currently fail."
- Two worker processes started deliberately at the same time, on different models. Call them W-A (Claude Code) and W-B (Codex).

### D.2 The six things it must demonstrate

**1. Two competing workers, one winner.**
Both W-A and W-B poll, both see `#1`, both attempt `POST /git/refs refs/claims/issue-1`. Exactly one gets `201`. The other gets `422` and moves on without logging an error, because losing a claim is normal.
*Pass:* one claim ref exists, one worktree exists, one PR is eventually opened. The loser produced no branch, no commit, no comment.
*Fail:* two branches, or two PRs, or the loser wrote anything at all.

**2. A seeded failure, corrected without losing ownership.**
Before the run, plant a bug the tests catch: the acceptance suite also asserts that `slugify("Hello,  World!")` returns `hello-world`, and the prompt is written so a naive implementation returns `hello--world`. CI must go red on the first push.
*Pass:* the `verify` check fails, the reconciler fires `resumeAgent` with `reason: "ci_failure"`, the same claim generation continues, the fix is pushed to the same branch, CI goes green. The claim ref never changed hands.
*Fail:* the correction opens a second PR, or a different worker picks it up, or the generation increments in a way that invalidates the original owner.

**3. A stale-generation attempt, rejected.**
Manually revoke W-A's claim mid-flight (delete the ref, let W-B claim at generation `N+1`), then let the still-running W-A process attempt a push and a status write.
*Pass:* W-A's writes are refused. The refusal is recorded as a `recovery` receipt naming both generations. Nothing W-A wrote after revocation appears on the branch or the issue.
*Fail:* W-A's push lands, or its issue comment appears, or the refusal is silent.

**4. Process termination and cold resume.**
`kill -9` the worker mid-implementation, with no shutdown hook and no chance to write a summary. Then start a fresh worker in a fresh shell with no chat history and no environment beyond the repo URL.
*Pass:* the new worker reads the claim ref and the receipts, sees `phase` and `expected_until`, determines the prior owner is dead rather than stalled, takes the claim at `N+1`, verifies the last receipt's `DONE` line by re-running its stated command, and continues. Total human input: zero.
*Fail:* it restarts from scratch, or it takes over from an owner that is merely slow, or it trusts the last receipt without re-running the evidence.

**5. Expected-head compare-and-swap on promotion.**
After the review approves at SHA `abc123`, push one more commit to the branch before the reconciler's merge fires.
*Pass:* the merge returns `409`, the promotion is refused, the review is invalidated, and the reviewer runs again on the new head. The promotion receipt for the refused attempt records `candidate_sha != head_sha`.
*Fail:* the merge succeeds and an unreviewed commit reaches `main`. This is the test the current stack would fail today, verified at source in §2.1.

**6. No routine human approval anywhere.**
Instrument the run to count every point where a human was asked for anything.
*Pass:* zero prompts across claim, worktree creation, commit, push, PR open, CI, review, correction, merge, issue close, and cleanup. The only human-gated operation in the whole slice is a hypothetical branch deletion outside the rollback envelope, which never fires.
*Fail:* any prompt at all. Given that a session on this machine stalled 19 hours on an unanswered folder-access prompt two days after the "allow all except destructive" fix merged, this is not a formality.

### D.3 The receipt bundle the slice must leave behind

Eight objects, machine-readable, in git:

`claim` (owner, generation, base_sha) → `implementation` (candidate_sha, files, agent, model) → `tests` (check_run_ids, command, exit code, verbatim tail) → `review` (reviewer identity, verdict, reviewed_sha, what could not be verified) → `promotion` (candidate_sha, promoted_sha, merge response code) → `projection` (issue closed, Project column moved) → `cleanup` (worktree removed, branch deleted, claim ref released) → `recovery` (the stale-generation rejection and the cold resume, with both generations).

A cold reader with no context must be able to answer, from those eight objects alone: what was asked, what was built, what proved it, who checked it, what was merged, and whether the merged thing is the checked thing.

### D.4 What the slice deliberately does not include

No multi-repo. No Project automation beyond one column move. No mobile view. No cost routing. No free-tier failover. No semantic memory. No Beads. No second issue. If the slice needs any of those to pass, the slice is wrong, not the exclusion list.

---

## E. Adoption plan

Five steps, ordered strictly by dependency. Each is independently valuable and each has a stop condition, because the failure mode on this machine is not doing too little, it is doing four things at once until the quota drains.

### Step 1: Land what is already written

**Exact outcome:** the roughly 240 KB of finished research and the governance rules that exist only as untracked files or unmerged drafts are on `main` and readable by a cold session.

**Adopted component:** none. This is git.

**Smallest necessary changes:** resolve conflicts on `agent-configs` PR #17 and merge it, which alone restores four of the six rule files `~/CLAUDE.md` declares mandatory. Return the `agent-configs` and `govcon-factory` checkouts to `main`. Commit `Agent SDLC.md`, the four teardown documents, the seven untracked `agent-workspace/knowledge` files, `PROPOSAL-0004.md`, and the handoff research. Write the missing `INDEX.md` that all 22 teardown issues cite.

**Deterministic acceptance test:** in a fresh clone, `for f in $(grep -o 'rules/[a-z-]*\.md' ~/CLAUDE.md); do test -f "$f" || echo "MISSING $f"; done` prints nothing. And every path referenced by issues #438 to #459 resolves.

**Stop condition:** stop when it merges. Do not refactor the rules while merging them.

**Must not be built yet:** anything. This step is prerequisite to every other step because the enforcement work in step 3 amends a file that is not on `main`.

**Why first:** it is the only step where the work is already done and the risk is total loss. A `git clean` today destroys research that took days.

### Step 2: Verify the two finalists at source, then choose

**Exact outcome:** a one-page decision naming Optio or Last Light, with a source citation for each of five specific questions.

**Adopted component:** none yet.

**Smallest necessary changes:** read, do not install. For Last Light: does it claim work atomically before dispatch, does anything prevent a webhook and a cron sweep from double-dispatching the same issue, does the merge path pass an expected head SHA, does the reviewer hold a token that cannot push, and what happens to an in-flight run when the process dies. For Optio: confirm the merge finding in §2.1 against the current `main`, and check whether `review-service.ts` can already be pointed at a second App installation.

**Deterministic acceptance test:** every one of the ten answers cites a file path and a line range. No answer is "the docs say".

**Stop condition:** stop the moment the ten answers exist. Do not start installing while reading.

**Must not be built yet:** no fork, no cluster, no config.

**Why second:** my Optio recommendation rests on source I read and my Last Light reservation rests on source I did not. That asymmetry should be closed by evidence, not by my preference, and it is an afternoon of work.

### Step 3: The claim-fence and the receipt writer, standalone

**Exact outcome:** two small programs that work against a throwaway repo with no orchestrator involved at all.

**Adopted component:** GitHub's git-refs API (§2.2) and merge API (§2.1). Design vocabulary from PROPOSAL-0004's six required fields.

**Smallest necessary changes:** a `claim` command (acquire, renew, release, read) and a `receipt` command (append, verify). Both plain shell plus `gh`, or one small Python file, so they run identically under Claude Code, Codex, Gemini CLI, Grok Build and in CI. That portability requirement comes straight from PROPOSAL-0004 and is the reason not to write them as Optio plugins.

**Deterministic acceptance test:** a script that forks two processes racing the same claim, asserts exactly one 201 and one 422, revokes the winner, asserts the revoked process's next write is refused, and asserts a `recovery` receipt naming both generations exists. Runs in CI, exits non-zero on any deviation.

**Stop condition:** stop when that script is green. Do not integrate it with anything.

**Must not be built yet:** the orchestrator integration, the Project sync, the mobile view, any second receipt store.

**Why third:** it is the only genuinely new code in the whole architecture, it is small, and it is testable in complete isolation. Building it before choosing an engine means the choice in step 2 cannot be wrong in an expensive way.

### Step 4: Stand up the chosen engine and run the vertical slice

**Exact outcome:** section D passes, all six demonstrations, on the throwaway repo.

**Adopted component:** Optio or Last Light, per step 2, plus the three-patch fork if Optio.

**Smallest necessary changes:** install from the project's own documented path. Create the three GitHub App installations. Point it at one repo with one label. Apply the merge patch. Wire the claim-fence in front of dispatch and the receipt writer at each lifecycle transition. Nothing else.

**Deterministic acceptance test:** section D.2, items 1 through 6, each producing a named receipt, run three times consecutively with no human input and no manual cleanup between runs.

**Stop condition:** stop when it passes three times. Not once. A race condition that fails one run in three is the exact class of bug this whole exercise exists to catch.

**Must not be built yet:** a second repository, a second concurrent issue beyond the two racing workers, Project automation beyond one column, cost routing, free-tier failover, Beads, the PWA.

### Step 5: Point it at real work, bounded

**Exact outcome:** the swarm closes real issues in one real repository, with a hard concurrency cap.

**Adopted component:** everything from step 4, unchanged.

**Smallest necessary changes:** apply the `swarm-ready` label to real issues. Set the concurrency cap to **three**, matching Mike's already-ratified "max three active work threads". Enable the Projects column sync. Wire lint, typecheck and build in `~/agent-workspace/adws/adw_modules/quality.py`, replacing the three `_placeholder()` calls verified still present at lines 154, 163 and 173.

**Deterministic acceptance test:** twenty consecutive issues closed with a complete eight-object receipt bundle each, zero human approvals in the routine path, zero cases where `candidate_sha != promoted_sha`, and at least one recorded `409` refusal proving the CAS gate fires under real conditions.

**Stop condition:** stop expanding until those twenty are clean. Then, and only then, consider a second repository.

**Must not be built yet:** multi-tenancy, high availability, semantic memory, the mobile command centre, a plugin system, ACP-based cross-vendor handoff, or a second work queue. Every one of those is a step-6-or-later item and each has already consumed a session here.

---

## F. Contrarian conclusion

### Are we overengineering this?

**The design is not overengineered. The process around it is.** Those are different problems and conflating them is what has cost the most time here.

The fourteen hard controls are, with one exception, not excessive. Every one of them corresponds to a documented failure on this machine, not to a hypothetical. Atomic claim: two sessions raced the same work. Fencing: three checkouts parked on work branches, two on the same branch name. Independent review: one bot, 93 reviews, 40 PRs. Gates that can fail: `gate_compliance` tests a substring against a file the same stage wrote, and `quality.py` lines 154, 163 and 173 are still `echo` commands that exit 0. Cold resume: five sessions dead in 3 minutes 52 seconds, two recoverable only by luck. Exact binding: a 42-of-42 claim from a different pipeline propagated as fact for days. A control list derived from twelve real incidents is not overengineering; it is a postmortem.

The one requirement I would push back on is **"monotonically increasing fencing generation"** as stated. A generation counter is the textbook answer and it is only necessary when a stale writer can reach the resource *after* losing its lease. In this architecture the resource is a git ref and a GitHub API, both of which offer their own compare-and-swap. A claim ref whose value is a content hash, checked immediately before every write, gets you the same safety without a counter to keep monotonic across restarts. Keep the generation if it is free; do not block the slice on making it perfect.

What *is* overengineered is everything upstream of the code. Five independent derivations of the same design, zero enforcement. A governance layer citing six rule files of which a session can read two. Twenty-two issues filed pointing at an index that was never written. The brief itself asks for research into sixteen projects, and the honest finding is that **two of them would do**, one has a one-line gap, and the rest are reading material. The pattern is real and it is not a character flaw: it is what happens when planning is cheap and enforcement is expensive, so the system produces the cheap thing.

### Which requirements belong in the first working lifecycle

Six. All six are in section D and each one closes a failure that has already happened.

| Requirement | Closes |
|---|---|
| Atomic claim | Two sessions racing the same issue in a shared checkout |
| Isolated workspace per claim | Three checkouts parked on work branches, dirty state inherited |
| Gates that can actually fail | `gate_compliance`, and `quality.py` lines 154, 163, 173 |
| Independent reviewer that cannot write or merge | 93 reviews, one identity, 40 PRs |
| Expected-head merge with `sha` | Verified missing in the leading candidate's source |
| A receipt bundle a cold reader can verify | 42-of-42, and 22 issues citing a file that does not exist |

Stale-generation rejection and cold resume come along free with the claim design, so they are in the slice too, at eight.

### Which requirements should be deferred

Everything else, and specifically:

- **The mobile PWA command centre.** GitHub Projects is already a mobile view and Mike has already ratified it as the human surface. Building a second one before the backend works is the parallel-infrastructure mistake in a nicer skin.
- **Cross-harness cooperation across all ten named harnesses.** Optio already adapts five. Start with two: one implementer, one reviewer, on different model families. Ten adapters solve a problem you will not have until the first one works.
- **Free-tier and subscription routing.** Real, valuable, and orthogonal. The gateway on `:3100` is the right place for it and it is a separate workstream. Note also that free tiers decayed on five providers in a single day on 2026-08-27, so routing built on a documentation-derived list is wrong within days regardless.
- **ACP-based cross-vendor handoff.** Verified impossible today against the installed SDK: Codex, Grok and Gemini do not speak ACP, and the fork and resume methods that do exist are unstable protocol methods. Durable state in the repo and the issue tracker is the answer, and that is what the receipt bundle is.
- **Beads, Gas Town, Spec Kit, semantic memory, multi-tenancy, high availability.** All good. None of them makes the first lifecycle work.
- **A durable-execution engine.** Only if the orchestrator itself becomes the thing that keeps dying.

### The fastest credible path to a functioning swarm in days

Five days, assuming Mike's own time is the constraint and the agents do the work.

**Day 1. Land what exists.** Step 1 above. Merge PR #17, return both checkouts to `main`, commit 240 KB of finished research, write the missing `INDEX.md`. This is a day of merge conflicts and no thinking, and it is the highest-value day on the list because after it a cold session can read its own rules for the first time.

**Day 2. Read, then choose.** Step 2. Ten questions, ten file citations, one decision.

**Day 3. Build the only new code.** Step 3. The claim-fence and the receipt writer, standalone, with the racing-processes test green in CI. Roughly 350 lines total.

**Day 4. Stand up the engine and run the slice.** Step 4. Install, three App installations, one label, three patches, wire the fence and the receipts. Get section D passing once.

**Day 5. Make it pass three times, then point it at real work.** Step 4's stop condition, then step 5 with a concurrency cap of three.

Three things make or break the week, and none of them is a technology choice:

1. **Fix the fail-open gates before trusting any run.** `quality.py` lines 154, 163 and 173 are `echo` statements. Until they are real commands, a green quality phase means nothing, and the framework's own README says so in bold. This is a ten-minute fix that has been outstanding for weeks, which is itself the argument of this whole report.
2. **Cap concurrency at three from hour one.** Five sessions on one five-hour bucket is what killed the 2026-08-28 work, and no amount of checkpointing fixes a resource ceiling. Mike already accepted the speed cost of three threads. Enforce it in the engine's config, not in a rule file.
3. **Do not write a sixth design document.** Including this one. If this report leads to another proposal instead of a merged PR #17 and a claim-fence with a green test, it has failed in exactly the way its own strongest evidence predicts.

The honest summary: the swarm does not need to be invented. Two MIT-licensed projects already implement most of it, one of them has a single-parameter gap in the most safety-critical call in the system, and the remaining work is roughly 350 lines plus a week of merging things that are already written.

---

## 3. What could not be verified

Listed plainly, because a gap named is worth more than a gap papered over.

**Could not read source, graded on documentation only:** AgentWorkforce Factory (GitHub's code search requires a login and `api.github.com` returned empty through the available fetch tool), Last Light, apra-fleet, Paperclip, Beads, Gas Town, OpenHands SDK, Jules. For Last Light this matters most, because five specific questions decide whether it beats the primary recommendation. Step 2 of the adoption plan exists to close exactly that gap.

**Read the specification, not the implementation:** Symphony. The Elixir reference implementation may be stricter than SPEC.md requires.

**Numbers I declined to repeat:** star counts for Beads, Spec Kit, Paperclip and Gas Town; the "189k lines of Go" figure for Gas Town; the AGENTS.md adoption and governance claims; OpenAI's internal "500% increase in landed pull requests". Several of these appear in `~/agent-mesh/Agent SDLC.md` stated as fact. I could not confirm any of them from a primary source in this pass, and the failure class PROPOSAL-0004 documents is precisely a number outliving its qualifier.

**Asserted from the orchestrator brief but not re-verified by me in source:** the `gate_compliance` substring test in govcon-factory, and the "36 of 37 checks, unsubmittable document" run. I have direct source evidence of the same failure class in `~/agent-workspace/adws/adw_modules/quality.py`, so the pattern is real here, but the specific govcon-factory finding is second-hand in this document.

**Not attempted:** any installation, clone, configuration change, or execution against a live provider, per point 10 of the brief. No file outside this deliverable was created or modified.

**Version pinning:** every finding is a snapshot of 2026-08-29. Optio, Last Light and AgentWorkforce Factory were all pushed to within the last three days. The merge-without-`sha` finding in particular should be re-checked against current `main` before anyone acts on it, and step 2 says so.
