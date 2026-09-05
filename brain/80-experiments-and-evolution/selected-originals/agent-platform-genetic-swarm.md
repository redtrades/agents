# The genetic swarm — lineage of Mike's founding direction

"Genetic" in Mike's usage is the **agnostic, composable, plug-and-play swarm**
(any model, any harness, any agent interchangeable), with the *evolutionary
self-improvement* research (GEPA = Genetic-Pareto) as its learning mechanism.
This file traces that idea from its verbatim origin to where each piece lives
now.

## 1. The founding utterance (verbatim, Mike, 2026-04-24)

> "I still want to have the agnostic, genetic harness and plug-in play brain
> and body so that any model can be implemented into the baseline or any of the
> other agents... Think of composable modular architecture, but for agentic
> swarms."

Pointer: quoted verbatim in
`~/Library/Mobile Documents/com~apple~CloudDocs/07-Data-Backups/Pre-Reset-Snapshots/pre-wipe-backup-2026-07-27/SWARM-CONSTITUTION.md`
§2 (drafted 2026-07-29, "the night before the reset"; status there: proposed,
never formally ratified — superseded in practice by the 2026-08-26+ rebuild,
but never retracted).

## 2. Mind / Body / Brain (the genetic frame)

From the same constitution §2:
- **Mind** — declarative, in git: operating rules, intent, agent manifests,
  skills, memory ledgers. Bootable by any harness.
- **Body** — the swappable harness/CLI (Claude Code, Hermes, Codex CLI, Gemini
  CLI…), translating Mind → native tool calls.
- **Brain** — the swappable LLM chosen per task/cost/DLP fit.
- Working definition: the same role definition boots under ≥2 (body × brain)
  pairings with only a config swap. Anti-pattern named there: a manifest that
  works only because one harness's undocumented behavior papers over a gap.

Where it survives now:
- Mind → `~/agent-mesh/.agent/` (personas, protocols, prompts, memory —
  harness-neutral, no provider/port/model IDs) + `agent-platform/docs/ROLES.md`
  + `agent-configs/roles/`.
- Body → `agent-platform/runtime-adapters/` (ACP adapter contracts) +
  `docs/START-HERE.md` §"end state connects Codex, Claude, Gemini, Grok,
  Jules, Antigravity, Hermes, Buzz, OpenCode, Pi…" + issues #130–#134, #40, #44, #45.
- Brain → model-routing policy `~/agent-mesh/hermes/` + FreeLLMAPI/stealth
  rotation research (`~/agent-mesh/research/research-free-routing-subscriptions.md`)
  + the local model program (D-016..D-035).

## 3. The swarm topology (Baseline-5 → five personas)

- Origin: OpenClaw v1 `AGENTS.md` Appendix — Swarm Taxonomy v2.5: Tier 1
  persistent Baseline-5 = **Prime** (orchestrator), **Forge** (code/PRs),
  **Scout** (research/intake), **Sentinel** (observability/drift),
  **Operator** (infra/cron); Tier 2 = 17 on-demand specialist manifests
  (sisyphus, prometheus, judge, hephaestus-01..06, scout-01..08); Tier 3 =
  ephemeral cloud (Jules/Codex cloud/Antigravity) coordinated via GitHub+Slack.
  Pointer: `.../09-Archive/OpenClaw-System-History/openclaw-v1-1534commits-2026-04-05-to-05-23/AGENTS.md`
  (Appendix — Swarm Taxonomy) and SWARM-CONSTITUTION §3 (three tiers
  "confirmed still the right shape").
- Survivor rule: the v1 mining digest found "Prime [is the] only complete
  persona survivor" (`~/agent-mesh/research/mine-v1-digest.md`).
- Today: five personas rebuilt harness-neutral at
  `~/agent-mesh/.agent/agents/{prime,scout,forge,sentinel,operator}.md`
  (identity+voice+avoid-list; no provider/model/port). Hermes bots seeded
  2026-08-26 (D-006: Prime, Scout, Sentinel, Morning Brief; later tiers filed
  as issues, not built — the over-commit guard). Baseline-5 persona set is
  being rationalized now under issue #183 ("Hermes profile rationalization,
  canonical bot roster alignment") — open as of 2026-08-30.
- Councils (the non-monotonic swarm pattern): start 3 / cap 5,
  `research-proactive-agents.md` §4 + `research-harnesses-councils.md`;
  implemented in `~/agent-mesh/pipelines/` council aggregator (D-006 lineage).

## 4. The verification-gap doctrine (what killed the last swarm)

SWARM-CONSTITUTION §0: five independent 2026-07-28/29 incidents, all one shape
— "something got declared working before anyone checked that it actually ran"
(trio-review vaporware SKILL.md; verify_task_completion.py 12k-char truncation;
the claim loop silently claiming 0 for unknown cycles; Hermes-primary cutover
on a failing-13/24-CI PR; two Scout digest launchd jobs dead for 3 days).
Corollary: "restoring a daemon is not fixing it"; loaded ≠ working.

This is the direct ancestor of today's hard controls:
- generator ≠ judge + fresh exact-candidate review →
  `agent-platform/docs/CONTROLLER.md`, `REVIEW-PROTOCOL.md`, `.agent/protocols/`,
  D-008; the overnight-build adversarial review (`~/agent-mesh/reviews/`) is
  the same law applied to the rebuild itself.
- "last successful run timestamp is monitored, not 'is the plist loaded'" →
  artifact-or-nothing heartbeats (`research-agentic-engineering.md`),
  `agent-workspace/heartbeat/LOG.md`, terminal_projection_parity (#117),
  claim reaper (#125), execution-budget circuit breakers (#123).
- worktree-per-session default (ADR-020-era collision lesson,
  SWARM-CONSTITUTION §4 anti-pattern) → today's mandatory isolated hydrated
  workspaces per claim (`CONTROLLER.md` §Owned state).

## 5. The literal "genetic" line — GEPA and self-evolution

- Research: **GEPA (Genetic-Pareto)** — reflective evolution over execution
  traces; Pareto frontier of candidates; textual feedback (Actionable Side
  Information) not scalar scores; up to 10–20% over RL with ~35× fewer
  rollouts; DSPy `dspy.GEPA` `auto="light"`; strong reflection_lm + cheap
  task LM split; production proofs (Nubank LLM-judge kappa 0.00→0.745;
  Microsoft data-filter judge). Citation list is in
  `~/agent-mesh/research/research-agentic-engineering.md` §83 (GEPA+ACE as the
  practical pair; JUDGE_RUBRIC ≥32/40 gate from v1 carries over).
  Upstream: https://dspy.ai/api/optimizers/GEPA/overview/ ,
  https://github.com/GEPA-ai/GEPA , https://github.com/GEPA-ai/GEPA
- Nous implementation forked for reference:
  `redtrades/hermes-agent-self-evolution` — "Evolutionary self-improvement
  for Hermes Agent — optimize skills, prompts, and code using DSPy + GEPA"
  (public fork; pushed 2026-03-29).
- Status: **research-adopted, not yet implemented**. The platform's controlled
  improvement gate (MASTER-PLAN scorecard "Controlled improvement";
  CANONICAL-INDEX §5 row: "Eval harness; D-008 — open: fixed baseline +
  held-out gates + regression") is the placeholder GEPA would plug into once
  the lifecycle is proven. Nothing self-modifies today; the v1 ≥32/40
  gate + D-008 generator≠judge + effect policy are the preconditions.

## 6. Coordination substrate evolution (Slack era → GitOps era → issue-as-spine)

- OpenClaw v1: Slack `#prime` comms + JSONL ledgers + COP.json + SwarmClaw PWA
  Autonomy Dial (Watch/Assist/Autonomous) + Landlock OpenShell simulation.
  Pointers: v1 AGENTS.md §Comms; `~/agent-mesh/swarmclaw/docs/AUTONOMY-DIAL.md`
  (the dial preserved as spec); `research-swarmclaw-command-center.md`.
- SWARM-CONSTITUTION §4: "GitOps as reconciliation, not command" — truth in
  GitHub, attention in Slack, kill-any-agent-and-resume-from-GitHub-only test;
  anti-pattern: shared mutable checkout (stale index.lock collisions).
- Today: `~/agent-mesh/.agent/protocols/{issue-as-spine,blackboard}.md` +
  `agent-platform/docs/START-HERE.md` §Authority + CAS claim ledger
  (`github_contents_authority.mjs`); Buzz is human I/O only
  (`research-harnesses-councils.md`); SwarmClaw reborn as the planned mobile
  status/approval PWA (issue #31, `START-HERE.md` §end state; D-011 static v1
  first).

## 7. What "genetic swarm" means for the canonical implementation

Every property above is already named by the platform's own contracts — the
chronicle's role is to show the ideas were continuous, not invented late:
1. provider/harness neutrality ⇒ `docs/GOAL.md` first sentence; issues #40,
   #130–#134; `runtime-adapters/`.
2. replaceable workers, controller owns authority ⇒ START-HERE Decision #6.
3. versioned roles/prompts/skills/task packets/envelopes ⇒ Decision #8 +
   `docs/ROLES.md`/`SKILLS.md` + `agent-configs/` adoption law.
4. autonomy dial ⇒ effect policy 4 outcomes (`OPERATING-MODEL.md`) +
   L0/L1/L2 ceremony (`AGENTS.md`), with APPROVAL_DESTRUCTIVE as the human
   gate — the dial's "Assist" band.
5. evolution/self-improvement ⇒ deferred behind the controlled-improvement
   scorecard gate; GEPA is the candidate mechanism, never a self-approving one
   (the generator is never the judge).
