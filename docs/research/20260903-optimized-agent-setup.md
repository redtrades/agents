# Optimized agent setup  -  intent inference and anti-drift

**Date:** 2026-09-03
**Author:** Claude (Sonnet 5), synthesis pass at Mike's request
**Method:** Read of Mike's intent corpus (`MIKE-INTENT-DEBRIEF-2026-08-28.md`,
`rules/`, `log/CORRECTIONS.log`, `DONT.md`, `DECISIONS.md`, `agent-sdlc/`),
GitHub starred repos (259, via `gh api user/starred`), and primary-source best
practice docs (Anthropic engineering blog, `planning-with-files`, Karpathy
guidelines). Every external claim is cited. Recommendations are **proposed**,
not adopted  -  acceptance is Mike's per `DONT.md` promotion rules.
**Problem statement (Mike's words):** agents "keep getting off track, stuck in
tangents trying to overcorrect something and losing track of their goal," and do
not infer intent correctly.

**Reconciliation with prior work (read this first).** A 2026-09-02 Codex session
already did a primary-source review of public agent-instruction files and skill
repos  - 
`knowledge/public-agent-instructions-and-skills-research-2026-09-02.md` on branch
`codex/basic-mvp-routing` (PR #43, mergeable, Tier 2, awaiting Mike). It reaches
the same verdict on the Karpathy skills, ECC, superpowers, wshobson, addyosmani
and compound-engineering: corroboration only, adapt the progressive-disclosure
principle, do not install wholesale. That evaluation is not repeated here. This
document's **net-new contribution** over PR #43 is: (1) `planning-with-files` as a
concrete adoptable mechanism (PR #43 does not cover it); (2) the
`CORRECTIONS.log` failure taxonomy mapped to counters (Appendix B); (3) the
context-rot / attention-budget framing from Anthropic's harness and
context-engineering posts; (4) the diagnosis tying the drift problem to
already-filed issues #38 / #16 / #40. Sections 2.5 and 2.6 below overlap PR #43
and are kept only for the `CORRECTIONS.log` mapping.

**Prior art already filed (do not re-file).** #38 rule reachability (root cause:
PR #17 conflicting 6+ days), #16 session-continuity rule, #40 unbounded `/goal`
Stop hooks, #39 review-independence collapse, #24 workspace-isolation port, #18
deletion guards. The bottleneck is execution and stale PRs, not missing
diagnosis.

---

## 1. Diagnosis  -  why agents drift here

### 1.1 The rules are written, not reachable

The 2026-08-28 audit already found the root cause and it is still true:
`~/CLAUDE.md` cited six mandatory rule files and a session could reach two
(`MIKE-INTENT-DEBRIEF-2026-08-28.md` §3). The current `~/.claude/CLAUDE.md` is a
single inlined contract, which is better, but the ten files in
`agent-configs/rules/` are **not in any session's context** unless a skill
happens to load them. `session-freshness.md`, `verification-law.md`,
`brief-pre-checks.md`  -  the exact rules that counter drift  -  are invisible to a
running session. An agent cannot follow a rule it never sees.

### 1.2 The rules that exist are conventions, not enforcement

`session-freshness.md`, `tool-selection-heuristic.md`, `skill-first.md` all carry
the same line: *"Not mechanically enforced  -  a convention to apply by judgment."*
Mike's stated position is the opposite: *"Rules are enforced, not written. A rule
violated twice becomes a hook or a check, never a louder sentence"*
(`MIKE-INTENT-DEBRIEF` §3). `no-parallel-infrastructure.md` cites OpenClaw's own
post-mortem: **a written rule against a failure mode did not survive contact with
the next work cycle.** Same applies to anti-drift rules.

### 1.3 No per-turn goal anchor

`CORRECTIONS.log` shows the concrete shapes. The goal-drift-adjacent ones:
`claimed-fix-not-in-tree` (3x one night  -  `str.replace` no-op reported as done),
`doubt-theater` re-running clean checks, `merge-on-review-of-a-different-commit`,
five `inert-regression-test` variants where the agent kept "fixing" tests that
pinned nothing. These are an agent that has lost the thread of *what it was
actually trying to prove* and is now servicing a proxy (a green suite, a
plausible string) instead of the goal. Anthropic's own framing: after 50+ tool
calls "the original goals get crowded out"
([planning-with-files](https://github.com/OthmanAdi/planning-with-files)); "as the
number of tokens in the context window increases, the model's ability to
accurately recall information decreases"
([Anthropic, effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)).

### 1.4 No context-loss recovery

Three sessions died on usage limits 2026-08-28; two survived only because they
"happened to write a file just before dying" (`MIKE-INTENT-DEBRIEF` §5). There is
no mechanism that writes goal + progress continuously, so an abrupt stop is not
survivable and the next session re-derives (or doesn't).

### 1.5 Overcorrection has no stop

`verification-law.md` has the 3-strikes rule and the doubt-theater rule written
down. Nothing counts strikes. An agent in a retry spiral has no external signal
to stop, and from inside the spiral "the failure mode is confident, plausible
output that doesn't converge, not an obvious crash" (`session-freshness.md`).

### 1.6 Intent inference is unassisted

`skill-first.md` clause 1 ("infer intent first") is a sentence with no scaffold.
There is no required step where the agent states its understanding of the goal,
the done-condition, and its assumptions **back to the user or to a file** before
acting. `brief-pre-checks.md` says "define done before starting" but nothing
makes the agent write it down where it (or the next agent) can check against it.

### 1.7 What is already right (keep, do not rebuild)

- `agent-sdlc/WORKFLOW.md`  -  the bounded-turn prompt is a model anti-tangent
  design: "one bounded execution turn," exact scope from `scope.json`, *"If the
  tool returns a failed or rejected result, make no change and exit. Do not
  attempt an internal repair loop."* This is the pattern; it needs propagating.
- `DONT.md` + `CORRECTIONS.log` + `consolidate-corrections.sh`  -  the
  violation→enforcement promotion loop exists and runs on m64.
- The damage-control hook stack  -  destructive actions are genuinely gated.
- Cross-model review requirement (different family than author)  -  correct, just
  not holding (collapsed to one bot, `MIKE-INTENT-DEBRIEF` §3).

---

## 2. Best practices from primary sources

### 2.1 Anthropic  -  effective harnesses for long-running agents

Source: [anthropic.com/engineering/effective-harnesses-for-long-running-agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)

| Technique | What it does |
|---|---|
| **Feature list as north star** | Initializer writes a requirements file, entries marked "failing"; agent cannot declare done while any entry fails. Prevents premature completion + scope creep. |
| **One feature at a time** | Explicitly counters "attempt to one-shot the app." |
| **Session handoff artifacts** | Progress file + descriptive git commits + `init.sh`. Next session reads git log + progress file to get up to speed. |
| **Start-of-session verification** | Run a basic test before implementing anything, to catch undocumented breakage. |
| **Do not edit/remove tests** | "Unacceptable"  -  a hard rule, not a preference. |

### 2.2 Anthropic  -  effective context engineering

Source: [anthropic.com/engineering/effective-context-engineering-for-ai-agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)

- **Context rot is real and architectural**  -  every token spent degrades recall.
  "Find the smallest set of high-signal tokens that maximize the likelihood of
  your desired outcome."
- **Just-in-time retrieval**  -  hold lightweight identifiers (paths, queries),
  fetch at runtime, don't pre-load.
- **Structured note-taking**  -  write persistent notes outside the window,
  retrieve later. Enables multi-hour runs across context resets.
- **Compaction**  -  summarize preserving "architectural decisions, unresolved
  bugs, implementation details"; maximize recall first, then precision.
- **Sub-agent isolation**  -  focused sub-agents with clean windows return
  1,000-2,000 token summaries; detailed exploration never enters the main window.
- **Tool minimalism**  -  "bloated toolsets create ambiguous decision points,
  forcing agents to waste tokens on poor choices." (Relevant: this session's env
  exposes ~200 deferred MCP tools.)

### 2.3 Anthropic  -  new rules of context engineering for Claude 5

Source: [claude.com/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models](https://claude.com/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models)

- Anthropic **removed >80% of Claude Code's system prompt** for newer models with
  no performance loss. Newer models have better judgment and need fewer
  guardrails. **Over-specification actively hurts.**
- CLAUDE.md: describe repo purpose briefly, spend tokens on **gotchas**, link to
  skills via progressive disclosure, don't state what Claude can read from the
  filesystem.
- **Rich references over rules**  -  code, test suites, rubrics as reference
  material beat procedural instructions.
- Auto-memory now handles most persistence; manual `#` memory-writing is largely
  obsolete.

**Direct implication for this system:** `agent-configs/rules/` is 34 KB of prose
across 10 files. That is the opposite direction from where the platform is
moving. The fix for drift is not a bigger ruleset  -  it is fewer, enforced,
in-context anchors.

### 2.4 planning-with-files (starred)

Source: [github.com/OthmanAdi/planning-with-files](https://github.com/OthmanAdi/planning-with-files)

The single most relevant off-the-shelf adoption. Mechanism:

| Failure it targets | Mechanism |
|---|---|
| Context wiped by `/clear`, compaction, crash | `task_plan.md` re-read from disk; `SessionStart` / `UserPromptSubmit` / `PreCompact` hooks carry current phase back in |
| Goal drift after 50+ tool calls | Plan head **re-injected every turn**; `PWF_INJECT=smart` keeps goal + next step + active phase in-window late in a long plan |
| Agent declares "done" early | **Stop gate** holds the stop while an `in_progress` phase remains, with a block cap + stall detection so an incomplete plan never traps a session |
| Plan silently rewritten by a tool result or bug | SHA-256 attestation; mismatched plan refused at injection with `[PLAN TAMPERED]` |
| Two sessions overwrite each other's phases | Parallel-write guard reports when checked items / completed phases regress |
| `/plan-doctor` | self-checks hook resolution, injection, attestation, latency (~289 ms/fire) |

Native Claude Code plugin; also Codex/Pi/Hermes (matches Mike's model-agnostic
requirement). Benchmark: fresh session resumed in 5.0 turns vs 13.3 raw; 3/3
blind A/B wins (author-run, limits documented).

### 2.5 Karpathy-inspired guidelines (starred: multica-ai/andrej-karpathy-skills)

Source: [github.com/multica-ai/andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills),
derived from [Karpathy's post](https://x.com/karpathy/status/2015883857489522876)

Four principles, one file. Maps 1:1 to the failure modes in `CORRECTIONS.log`:

| Principle | Rule | Counters |
|---|---|---|
| **Think before coding** | State assumptions explicitly; present multiple interpretations, don't pick silently; push back; stop when confused and name what's unclear | wrong-assumption drift, `never-measured-reported-as-measured` |
| **Simplicity first** | Minimum code; nothing speculative; "would a senior engineer call this overcomplicated?" | bloat tangents |
| **Surgical changes** | Touch only what the request traces to; match existing style; mention unrelated dead code, don't delete it; only clean up orphans your own change created | scope-creep-as-thoroughness |
| **Goal-driven execution** | Transform imperative tasks into verifiable goals ("write a test that reproduces it, then make it pass"); state a plan as `step → verify: check`; strong success criteria let the model loop independently | `inert-regression-test` (11x), doubt-theater, retry spirals |

Karpathy's "weak criteria require constant clarification, strong criteria let the
LLM loop independently" is the core insight for the intent-inference problem.

### 2.6 Other starred repos, mapped to needs

| Repo | Relevance | Verdict |
|---|---|---|
| [EveryInc/compound-engineering-plugin](https://github.com/EveryInc/compound-engineering-plugin) | The "mistake → permanent lesson" loop Mike built by hand (`consolidate-corrections.sh`) | Compare mechanisms; adopt if cleaner |
| [thedotmack/claude-mem](https://github.com/thedotmack/claude-mem) | Cross-session context capture + re-injection | Claude-only  -  conflicts with vendor-agnostic constraint; prefer repo-based progress files |
| [obra/superpowers](https://github.com/obra/superpowers) + skills | Skills framework + methodology; Mike already has `using-superpowers` (gated) | Already partially adopted; low marginal value |
| [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) | Source of `verification-law.md`'s doubt-driven-development | Already mined |
| [Nutlope/hallmark](https://github.com/Nutlope/hallmark) / [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill) | Anti-slop; Mike has `no-ai-slop` on | Marginal over current setup |
| [FrancyJGLisboa/agent-skills-platform](https://github.com/FrancyJGLisboa/agent-skills-platform) | Skill lifecycle governance: evidence, discovery, rollback, quarantine | Matches Mike's "prove discovery/invocation before promotion" (README); worth a look for the skill catalog |
| [ComposioHQ/composio](https://github.com/ComposioHQ/composio) | "turn intent into action"  -  tool/auth layer | Overlaps the FreeLLMAPI gateway; no adopt |
| [muratcankoylan/Agent-Skills-for-Context-Engineering](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering) | Context-engineering skill collection | Mine for specific skills, don't bulk-adopt (`skill-first.md` clause 2) |

---

## 3. Proposals  -  concrete changes, with repo paths

Ordered by leverage against the drift problem.

### P0-1: Adopt planning-with-files as the per-turn goal anchor

- **Install:** Claude Code plugin (`/plugin marketplace add OthmanAdi/planning-with-files`
  then `/plugin install`), or vendor the skill + hooks into
  `~/.claude/hooks/planning-with-files/` with a `SOURCE.md` / `PROVENANCE.md`
  pair matching `hooks/damage-control/`.
- **Wire:** `UserPromptSubmit`, `SessionStart`, `PreCompact`, `Stop` hooks in
  `~/.claude/settings.json`. Start with injection only (no Stop gate) for a week,
  then enable gated mode.
- **Convention:** `agent-configs/rules/` gains `planning-files.md`  -  for any task
  over ~5 steps or ~30 min, `task_plan.md` / `findings.md` / `progress.md` are
  created before work starts, `task_plan.md` opens with a one-line **goal** and a
  **done-condition**.
- **Why P0:** it is the only proposal that puts the goal back in the window
  *every turn* and holds an early "done." It is enforcement (a hook), not a
  sentence. It survives compaction and usage-limit death  -  directly the
  `MIKE-INTENT-DEBRIEF` §5 problem. Vendor-neutral.
- **Overlap check (`no-parallel-infrastructure.md`):** this replaces nothing  - 
  there is no current per-turn injection mechanism. `post-compact-reinject.sh`
  fires once on compact; this is the always-on generalization and
  `post-compact-reinject.sh` should fold into it.

### P0-2: Fix rule reachability  -  a SessionStart rules digest

- **Create:** `agent-configs/rules/DIGEST.md`  -  a ~40-line compression of the 10
  rule files: one imperative line each, plus the 5 highest-frequency
  `CORRECTIONS.log` failure shapes as "before you claim X, check Y."
- **Wire:** `SessionStart` hook (all sources, not just `compact`) in
  `~/.claude/settings.local.json` that cats `DIGEST.md`. Mirror the
  `post-compact-reinject.sh` shape.
- **Generate, don't hand-maintain:** `scripts/build-rules-digest.sh` extracts the
  first `## The rule` paragraph from each file so the digest cannot drift from
  its sources. Fits the existing `consolidate-corrections.sh` scheduled-script
  pattern.
- **Why P0:** the audit's named root cause. Costs ~600 tokens/session against a
  drift failure that costs hours.

### P0-3: Required intent-restatement preamble

- **Add to `~/.claude/CLAUDE.md`** "Order and work mode," one clause: *Before the
  first tool call on any non-trivial task, state in one block: the goal in one
  sentence, the done-condition as a checkable test, assumptions being made, and
  anything genuinely ambiguous (surface options ranked, pick one, say why  -  do
  not silently choose, do not stop to ask on reversible forks). Write it to
  `task_plan.md` when one exists.*
- **Source:** consolidates `brief-pre-checks.md` ("define done before starting"),
  `skill-first.md` clause 1, Karpathy §1, and `communication.md`'s ranked-options
  rule that already exists in fragments.
- **Why P0:** this is the intent-inference scaffold. It makes the agent's
  understanding inspectable *before* it has spent an hour on the wrong thing, and
  gives every later turn (and the next session) a fixed target to check against.

### P1-1: Fold the Karpathy four principles into the global contract

- **Edit `~/.claude/CLAUDE.md`**  -  replace the current thin "work mode" bullets
  with the four principles, ~12 lines total, phrased as Mike's system already
  phrases things (no em dashes, imperative). Keep it short per §2.3.
- **Retire** the overlapping prose in `communication.md` "Hard Operational
  Boundaries" and `brief-pre-checks.md` down to pointers, so there is one home.
- **Why P1:** high-value, but it is a Tier-2 governing-file change
  (`MIKE-INTENT-DEBRIEF` §3)  -  needs Mike, and needs P0-2 landed first so the
  contract and the digest do not fight.

### P1-2: Retry-spiral and doubt-theater stop hook

- **Create:** `~/.claude/hooks/stop-hook-validators/converge-check.py` (the
  `stop-hook-validators/` dir already exists as a stub with a README). On `Stop`,
  read the transcript tail: if the last N tool calls are the same command family
  failing, or a verification that already returned clean was re-run with no
  intervening edit, emit a block with "3-strikes: escalate, do not retry" or
  "doubt-theater: act on what is known or escalate."
- **Source:** `verification-law.md` "When to stop iterating"  -  the rule exists,
  the counter does not.
- **Why P1:** targets overcorrection specifically. Needs care not to trap
  legitimate iteration; ship in warn-only mode first.

### P1-3: Continuous session-continuity logging

- **Create:** `~/.claude/hooks/session-continuity/append.sh` on `PostToolUse`
  (matcher `Edit|Write|Bash`), throttled to once per ~10 calls: append a line to
  the task's `progress.md`  -  timestamp, last action, current phase from
  `task_plan.md`. Plus a `Stop`/`PreCompact` fuller flush.
- **Source:** `MIKE-INTENT-DEBRIEF` §5  -  "what an agent writes *continuously* so
  an abrupt stop is survivable. An end-of-session summary is worthless because a
  session that dies never writes one."
- **Overlap check:** if planning-with-files' autonomous-mode ledger (P0-1)
  already writes a progress tail, use that and skip this. Verify before building.
- **Why P1:** directly the usage-limit-death problem; lower urgency than P0
  because the git-commit-often habit partially covers it today.

### P1-4: Verify the allow-all-except-destructive permission posture actually holds

- **Investigate:** Mike says bash prompts still stall Cowork/Dispatch sessions
  (`MIKE-INTENT-DEBRIEF` §3). `~/.claude/settings.json` has `defaultMode: auto` +
  a broad allowlist, and the damage-control `patterns.yaml` adds `ask:` for
  `sudo`/`diskutil`/`git branch -D`/etc. Trace which specific calls prompt in a
  real Cowork session; the likely culprits are (a) commands not on the allowlist
  falling through to a prompt in a non-`bypassPermissions` mode, (b) an MCP tool
  with no allow entry.
- **Fix path:** widen the `settings.json` allowlist to `Bash(*)` with the
  damage-control hook as the only gate (the hook already blocks the irreversible
  set), or move Cowork/Dispatch to `bypassPermissions` mode with the hook stack
  intact.
- **Why P1:** a stalled session is a session that loses its thread while waiting.
  This is `investigate-first` shaped  -  diagnose before changing the posture.

### P2-1: Propagate the agent-sdlc bounded-turn prompt shape

- `agent-sdlc/WORKFLOW.md`'s turn prompt is the reference anti-tangent design.
  Extract its shape into `agent-configs/prompts/bounded-execution-turn.md`: read
  the scope record first, one phase active, on tool failure make no change and
  exit (no internal repair loop), on success leave the tree and exit.
- **Why P2:** valuable but the mechanism is repo-specific (Symphony hooks write
  `scope.json`); the portable part is the prose contract.

### P2-2: Tool-surface reduction for autonomous sessions

- This session exposes ~200 deferred MCP tools + many plugin skills. Per §2.2,
  that is an ambiguity tax on every decision. For Dispatch/autonomous profiles,
  cut MCP servers to the ones a run actually needs (Mike's `agent-mesh` already
  scopes `gbrain` to `prime` only for exactly this reason  -  `MIKE-INTENT-DEBRIEF`
  §6).
- **Why P2:** real but diffuse; the `prime`-only-gbrain precedent shows the team
  already knows to do this.

---

## 4. Prioritization

| Priority | Item | Impact | Effort | Depends on |
|---|---|---|---|---|
| **P0-1** | planning-with-files (per-turn anchor + Stop gate) | High | Low (plugin) / Med (vendored) |  -  |
| **P0-2** | Rules digest + SessionStart injection | High | Low |  -  |
| **P0-3** | Intent-restatement preamble | High | Low (contract edit) | Mike (Tier 2) |
| **P1-1** | Karpathy four principles into contract | High | Low | P0-2, Mike |
| **P1-2** | Retry-spiral / doubt-theater stop hook | Medium | Medium | P0-1 (reads `task_plan.md`) |
| **P1-3** | Continuous continuity logging | Medium | Low-Med | P0-1 (may already cover) |
| **P1-4** | Fix permission-stall posture | Medium | Low (investigate) |  -  |
| **P2-1** | Bounded-turn prompt template | Medium | Low |  -  |
| **P2-2** | Tool-surface reduction | Low-Med | Medium |  -  |

---

## 5. Risks and dependencies

- **Adding infra when the rule is "don't"**  -  every proposal was overlap-checked
  against `no-parallel-infrastructure.md` above. P0-1 and P1-3 have real overlap
  risk with each other; resolve by installing P0-1 first and checking what its
  ledger already writes.
- **Digest drift (P0-2)**  -  a hand-maintained digest becomes a fourth
  inconsistent copy of the rules. Mitigation: generate it from the source files,
  never edit it directly.
- **Contract fights digest (P0-2 vs P1-1)**  -  if the Karpathy principles land in
  the contract and also in the digest with different wording, that is the exact
  `MIKE-INTENT-DEBRIEF` §3 failure. Land P0-2's generator first; have it pull
  from the contract, not duplicate it.
- **Stop-gate traps a session (P0-1, P1-2)**  -  planning-with-files has block-cap
  + stall detection; the custom converge-check does not yet. Ship both warn-only
  first, watch `CORRECTIONS.log` for a week.
- **Plugin supply chain**  -  planning-with-files and any starred plugin are
  third-party. Pin a commit SHA, read the hook scripts before wiring (they run on
  every turn), record provenance. Same discipline as the disler adoptions.
- **Tier-2 approvals**  -  P0-3, P1-1 touch `~/.claude/CLAUDE.md`. Those are Mike's
  to merge (`DECISIONS.md` D-001, `MIKE-INTENT-DEBRIEF` §3).
- **This does not fix the coordination failures**  -  the dominant `CORRECTIONS.log`
  class is duplicate-work and stale-head merges across concurrent sessions. That
  is a work-queue/worktree problem (`agent-sdlc`), not a context problem, and is
  out of scope here.

---

## 6. Roadmap

**Week 1  -  reachability and anchoring (no Tier-2 needed)**
- P0-1: install planning-with-files as a plugin, injection-only mode. Read the
  hook scripts first. Run it on one real multi-step task, watch `/plan-doctor`.
- P0-2: write `build-rules-digest.sh`, generate `DIGEST.md`, wire the
  `SessionStart` hook in `settings.local.json`.
- P1-4: instrument one Cowork session, list every call that prompts.

**Week 2  -  enforcement**
- P0-1: enable gated Stop mode; fold `post-compact-reinject.sh` into it.
- P1-2: `converge-check.py` in warn-only.
- P1-3: decide (planning-with-files ledger vs new hook), build the smaller one.
- P1-4: apply the permission-posture fix, verify no prompt on a clean run.

**Week 3  -  contract (Mike in the loop)**
- P0-3 + P1-1: single PR to `~/.claude/CLAUDE.md`  -  intent preamble + Karpathy
  four principles, with `communication.md` / `brief-pre-checks.md` trimmed to
  pointers in the same PR. Mike merges (Tier 2).
- P2-1: extract the bounded-turn template.

**Week 4  -  measure**
- Compare `CORRECTIONS.log` entries/week and mean turns-to-resume before/after.
  planning-with-files' own claim is 13.3→5.0 turns; check it holds here.
- P2-2 if the tool-surface tax shows up in the transcripts.

---

## 7. The one-paragraph version

Mike's system already contains the right ideas  -  bounded turns, cross-model
review, enforce-don't-write, define-done-first, 3-strikes. They fail because
they live in files a running session never loads, as conventions nothing checks.
The platform is moving toward *fewer* in-context tokens, not more rules
(Anthropic cut 80% of Claude Code's prompt). So the intervention is not a bigger
ruleset: it is (1) a per-turn on-disk goal anchor that survives compaction  - 
adopt `planning-with-files`; (2) a generated rules digest injected at session
start so the anti-drift rules are actually visible; (3) a required
intent-restatement before the first tool call so the agent's understanding is
inspectable before it burns an hour. Everything else is second-order.

---

## Appendix A  -  starred-repo scan (agent-relevant subset)

259 stars total; the ~137 most recent are agent-infrastructure. Not adopted in
bulk per `skill-first.md` clause 2. Clusters: context-engineering
(`Agent-Skills-for-Context-Engineering`, `planning-with-files`,
`Prompt-Engineering-Guide`), memory (`claude-mem`, `mem0`, `supermemory`,
`MemPalace`, `OpenViking`, `claude-sessions`), skills frameworks (`superpowers`,
`addyosmani/agent-skills`, `compound-engineering-plugin`, `vercel-labs/skills`,
`wshobson/agents`, `agent-skills-platform`), anti-slop (`hallmark`,
`taste-skill`), harness/orchestration (`ECC`, `Archon`, `gstack`, `gbrain`,
`agentic-stack`, `CCPlugins`, `deep-agents`), Karpathy CLAUDE.md
(`andrej-karpathy-skills`). Mike's own: `redtrades/agent-configs`,
`redtrades/work-ops`, `redtrades/awesome-claude-code`, `redtrades/agent-academy`,
`redtrades/openclaw-config`, `redtrades/openclaw-backup`.

## Appendix B  -  CORRECTIONS.log failure taxonomy (input to P0-2 digest)

| Shape | Count | Digest line |
|---|---|---|
| `inert-regression-test` | 11+ | Before claiming a test pins a fix: revert the fix in a scratch copy (`git archive`), confirm the test fails. Assert on values (a constant, the payload, the rendered line) at the end of the chain, never on source text or a whole document. Build the fixture at the top of the chain the bug can occur in. |
| `shared-working-directory-concurrent-checkout` | 5+ | One worktree per session. Uncommitted work you did not create = stop and report. Never read a shared checkout's working tree as "current main"  -  use `git show origin/main:<path>`. Commit per-file, early, even mid-implementation. |
| `claim-discipline-before-commit` (duplicate work) | 3+ | Re-scan the issue list you already fetched; a full-text search with guessed terms is not a substitute. An atomic issue-claim lock does not stop a different session building the same join point under a different number. |
| `claimed-fix-not-in-tree` | 3 | After any programmatic edit, grep for the changed text before claiming the change. "I wrote a fix" and "the fix is in the tree" are different facts. |
| `merge-on-review-of-a-different-commit` | 2+ | A Tier-1 merge requires the approving review's commit_id == head SHA, and no CHANGES_REQUESTED on that SHA. |
| `never-measured-reported-as-measured` | 4 | When replacing a null with prose, the prose describes what the system did (not retrieved / not screened), never what the source contains, unless the system read the source. |
| `verification-law` (local pass ≠ CI) | 2+ | The gate this repo defines is CI. Check `gh pr checks` unpiped before `&&`, not a local run. |
| `review-independence` | 2 | Do not average an APPROVE over an unresolved disagreement on the same SHA  -  escalate it. |
