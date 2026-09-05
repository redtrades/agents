# Agentic Engineering + Diagnostic Swarm Patterns (2026 research consolidation)

Researched 2026-08-26. Purpose: build past the existing grounding (disler corpus in `~/agent-configs`, Anthropic orchestrator-workers, Cognition reversal basics, shared-blackboard, hard-stop-at-3-failures) toward the agentmesh target: a portable brain serving Claude Code / opencode / pi / Hermes, plus a diagnostic swarm that audits its own runs and acts proactively within guardrails. Every section ends with what this means for Mike's system specifically.

---

## 1. Portable brain patterns: one source of truth, many harnesses

### 1.1 The instruction-file layer has consolidated

AGENTS.md won. Originated by OpenAI August 2025, stewarded since late 2025 by the Agentic AI Foundation under the Linux Foundation alongside MCP; 60,000+ public repos carry one; 28+ tools read it natively (Codex, Cursor, Copilot, Gemini CLI, Jules, Windsurf, Devin, Amp, Aider, Zed, goose, opencode, and more). Sources: https://agents.md/ , https://codex.danielvaughan.com/2026/05/27/agent-instruction-files-agents-md-claude-md-cross-tool-portability-codex-cli/ , https://vibecoding.app/blog/agents-md-guide

Claude Code is the last big holdout and the picture is mixed as of mid-2026: some guides report AGENTS.md support landed spring 2026 (https://vibecoding.app/blog/agents-md-guide), while a systematic study of 2,853 repos found Claude Code still did not support it and that CLAUDE.md was typically created first with AGENTS.md added after (arXiv 2602.14690, https://arxiv.org/html/2602.14690v5). Treat "Claude Code reads AGENTS.md natively" as unverified until checked against current Claude Code docs; the safe pattern costs nothing either way.

The empirical result that matters for how much effort to spend: developer-written AGENTS.md improved agent success ~4% and cut agent-introduced bugs 35-55% across 138 real repos, while LLM-generated instruction files *decreased* success and raised inference cost >20% (Gloaguen et al. 2026, cited in https://codex.danielvaughan.com/2026/05/27/agent-instruction-files-agents-md-claude-md-cross-tool-portability-codex-cli/). Write your own, keep it short, maintain it like code. Codex enforces a 32 KiB combined cap (`project_doc_max_bytes`) and stops loading past it (https://developers.openai.com/codex/guides/agents-md).

### 1.2 The skills layer: one format, many paths, tiny portable subset

Agent Skills (SKILL.md in a named directory) became an open standard October 16, 2025 (Anthropic launch; spec at https://agentskills.io/home , maintained at github.com/agentskills/agentskills). By May 2026 six harnesses parse SKILL.md natively (Claude Code, Cursor 2.4+, Codex CLI, Cline, Antigravity, Gemini CLI) and the long tail gets it via installers like `npx skills add` (matrix: https://mcp.directory/blog/cross-agent-skills-cursor-codex-cline-antigravity-gemini-mastra-portability).

What actually ports:

- **Portable subset is `name` + `description` only.** Everything else is silently ignored somewhere. `allowed-tools` is spec-experimental, parsed only by Claude Code and Codex, and the delimiter differs (comma-delimited Claude Code vs space-delimited spec). Never put security-relevant logic in frontmatter fields that can be silently stripped. Source: https://codemyspec.com/blog/skill-portability , https://github.com/jamie-bitflight/claude_skills/blob/main/plugins/plugin-creator/skills/skill-creator/references/agent-plugin-ecosystem.md
- **Paths are the real fragmentation.** `.claude/skills/`, `.opencode/skills/`, `.agents/skills/`, `.cursor/skills/`. opencode is the portability hub: it reads `.opencode/`, `.claude/`, AND `.agents/` skills natively, project and global (https://opencode.ai/docs/skills/). Codex standardized on `.agents/skills/` (https://mcp.directory/blog/cross-agent-skills-cursor-codex-cline-antigravity-gemini-mastra-portability).
- **Body conventions that travel:** refer to tools by conceptual name, not prefixed identifiers (`mcp__github__create_issue` breaks on opencode's single-underscore scheme); put complex operations in sibling `scripts/`; declare requirements in `compatibility` prose (https://codemyspec.com/blog/skill-portability).

### 1.3 Symlink farms vs generated adapters: the field's verdict

Three coexisting mechanisms, each correct at a different scope:

| Mechanism | When it wins | Evidence |
|---|---|---|
| Symlink | Single-file compat, same semantics: `ln -s AGENTS.md CLAUDE.md`, `.agents/skills/<name> -> ../../.claude/skills/<name>` | https://benjamincrozat.com/agents-md , https://codemyspec.com/blog/skill-portability |
| Generated adapter/installer | When harness semantics diverge (hooks, permissions, command namespaces, colon-vs-hyphen slash forms) | agentic-stack generates per-harness installs (below); Superpowers ships separate plugin manifests per harness; GSD rewrites body text during `--gemini` install (https://github.com/glittercowboy/get-shit-done/blob/main/docs/USER-GUIDE.md) |
| Native multi-path reading | When a harness does the work for you | opencode reads all three skill dirs; Cursor 2.4+ scans five paths |

Public exemplars worth mining:

- **codejunkie99/agentic-stack** (Mike's fork: redtrades/agentic-stack, "one brain, many harnesses"): a portable `.agent/` folder (memory layers + seed skills + protocols + enforced permissions + nightly staging cycle) with an installer that emits per-harness adapters for Claude Code, Cursor, Windsurf, OpenCode, OpenClaw, Hermes, Pi, Codex, Copilot CLI, Gemini CLI, standalone Python. Its harness table documents exactly which config file and hook support each harness has. https://github.com/codejunkie99/agentic-stack
- **obra/superpowers**: methodology-as-skills (brainstorming -> worktrees -> plans -> subagent-driven dev -> TDD -> review -> finish), distributed as plugin manifests for 12+ harnesses including opencode, Pi, and Hermes Agent, installed separately per harness. Its differentiator is the enforcement bootstrap (`using-superpowers`: check for relevant skills before ANY response). https://github.com/obra/superpowers , install matrix: https://dev.to/rosgluk/superpowers-quickstart-install-workflow-and-tryout-505n
- **get-shit-done (GSD)**: ~50 Markdown commands + Node helper + hooks, `.planning/` state files (PROJECT/REQUIREMENTS/ROADMAP/STATE), fresh-context subagents per task, wave-parallel research, model profiles. Cautionary tale: moved to open-gsd governance in May 2026 after trust concerns about the original author (meme-coin incident); the original repo is flagged untrustworthy (https://www.codecentric.de/en/knowledge-hub/blog/the-anatomy-of-claude-code-workflows-turning-slash-commands-into-an-ai-development-system). Adopt ideas, pin forks, verify provenance.
- **oh-my-openagent** (formerly oh-my-opencode): unified `omo.jsonc` config read by OpenCode plugin + Senpi + Codex loader, with a migration engine that imports legacy files once and a precedence walk (user layer, then nearest project file wins). Named orchestrator agents (sisyphus/planner, oracle/architect, librarian/research), category-to-model mapping, provider fallback chains, background-task concurrency caps. https://github.com/code-yeongyu/oh-my-openagent/blob/dev/docs/reference/configuration.md

### 1.4 What works, distilled

1. Author once in a universal repo (this is exactly `~/agent-configs`' existing role, confirmed as the field's winning shape by the harness-engineering census: Context Files are near-universal, advanced mechanisms rare, Claude Code users employ the broadest range - https://arxiv.org/html/2602.14690v5).
2. Consumer wiring stays documentation-plus-copy, zero git coupling. Mike's submodule experiment (PR #67 merged then reverted same day, D-030) matches the field: nobody ships shared infra as a git object inside consumer repos; they symlink or generate.
3. Keep skill frontmatter to `name`+`description`; move harness-specific behavior (permissions, models, tool whitelists) to the harness's own config layer, declared in prose inside the skill.
4. Prefer "author in `.agents/skills/` + copy into `~/.claude/skills/` with SOURCE.md" over maintaining two trees; opencode reads both natively so opencode needs zero adapters.
5. An enforcement bootstrap beats a bigger skill library: the recurring lesson of superpowers and Mike's own skill-first rule is that skills get skipped under pressure unless a standing instruction forces the check every turn.

---

## 2. Diagnostic swarm architectures: orchestrator + research/code/audit specialists

### 2.1 The 2026 settlement of the multi-agent debate

Cognition's follow-up, "Multi-Agents: What's Actually Working" (April 2026, Walden Yan), keeps parallel-writer swarms condemned and names the three patterns that survive production: (1) Code-Review-Loop, a clean-context reviewer iterating against the coder (Devin Review finds ~2 bugs per PR average, ~58% severe, even reviewing Devin's own output; clean context makes the reviewer *smarter* because of attention math and context rot), (2) the Smart Friend consult, (3) map-reduce-and-manage delegation where writes stay single-threaded. Unstructured negotiating swarms remain "mostly a distraction." Source: https://cognition.ai/blog/multi-agents-working

This sharpens the known reconciliation (research fan-out parallelizes; coding shares state): the diagnostic swarm Mike wants is the *good* case, because auditors and researchers are readers. Reads commit nothing; writes take turns. Analysis: https://dev.to/harryfloyd/your-multi-agent-system-is-an-org-chart-k2e , https://agenticlab.sunilprakash.com/signal/003-multi-agent-decision-variable/

Cost note to keep the 15x-token finding honest: Cognition's Devin Fusion shows the routing half of the win without the token bill - a frontier main agent plus a cheaper persistent "sidekick," switched dynamically at compaction boundaries to dodge cache misses, held frontier-level quality at up to 60% lower cost, with 88% of internal merged PRs routed automatically. https://cognition.com/blog/devin-fusion

### 2.2 Evaluator-before-generator is now table stakes

- The Planner-Generator-Evaluator harness pattern (fresh contexts per role, evaluator sees only the artifact plus a frozen rubric, never the generator's reasoning trace; failed evals feed findings, not transcripts, back to the generator) is catalogued with failure-mode rationale: generator self-grading collapses into self-approval; shared context lets the evaluator inherit the generator's assumptions. https://www.agentpatternscatalog.org/patterns/planner-generator-evaluator-harness/ , https://www.shiplight.ai/blog/planner-generator-evaluator-multi-agent-qa
- Deterministic checks run before any LLM judge (schema validation, tests, linters); LLM evaluation reserved for genuinely subjective axes; hard iteration cap 3-5 plus a plateau guard (identical feedback twice = stop) - this is the formalized version of Mike's hard-stop-at-3-failures and doubt-theater rules. https://www.agentnotebook.dev/tutorials/agentic-workflow-evaluator-optimizer-python , https://wandb.ai/site/articles/agentic-ai-self-correction-how-to-build-systems-that-fix-their-own-mistakes/
- Maker is not verifier: independence matters more than judge strength; vary model family or use code evaluators to break correlated blind spots. https://jigarjoshi.in/blog/independent-verifier-loops-and-self-improving-agents/

### 2.3 LLM-as-jury: status of the Karpathy pattern

llm-council (three stages: parallel answers, anonymized cross-ranking, chairman synthesis) hit 21k stars, was explicitly a Saturday hack with no license and zero maintenance, and is now effectively abandoned (issue #192: "the repo is a tombstone"). Steal the anonymous-peer-review mechanic; do not build on the code. https://github.com/karpathy/llm-council , https://github.com/karpathy/llm-council/issues/192

Two findings to design around:

- **Self-preference bias is real**: models rank their own answers higher than peers rank the same answers (73,580 paired judgments); anonymity is the trick that fixes it. https://llmcouncil.ai/karpathy-llm-council
- **Councils smooth out spiky good ideas**: an experiment found blended councils kept only ~25% of good ideas that appeared in just one model's answer; peer review amplified consensus rather than preserving minorities. Mitigation: explicitly gather, rank, and store each reviewer's distinct findings *before* synthesis. https://www.strangeloopcanon.com/p/llm-councils-show-groupthink

Productization signal: Perplexity shipped Model Council to Max plan February 2026 (three frontier models plus synthesizer) - multi-model verification is becoming default for judgment calls, which matches Mike's review-independence rule (two reviewers, different models, disagreement escalated not averaged).

### 2.4 Prompt/context evolution: GEPA, DSPy, ACE - practical for a solo operator

- **GEPA (Genetic-Pareto)**: reflective evolution over execution traces; maintains a Pareto frontier of candidates; needs textual feedback (Actionable Side Information), not scalar scores. Up to 10-20% over RL with ~35x fewer rollouts; usable through DSPy's `dspy.GEPA` with `auto="light"` budgets and as few as 3 examples; strong `reflection_lm` + cheap task LM is the standard split. Production proof points include Nubank (LLM-judge prompt optimization lifted end-to-end eval agreement kappa 0.00 -> 0.745) and Microsoft using it to optimize a pre-training data-filter judge. Directly relevant: Nous Research ships a Hermes-agent self-evolution repo built on DSPy + GEPA. https://dspy.ai/api/optimizers/GEPA/overview/ , https://gepa-ai.github.io/gepa/ , https://github.com/GEPA-ai/GEPA , https://github.com/NousResearch/hermes-agent-self-evolution
- **ACE (Agentic Context Engineering, ICLR 2026)**: treats contexts as evolving playbooks maintained by Generator/Reflector/Curator roles with incremental delta updates and grow-and-refine redundancy control; prevents brevity bias and context collapse; adapts without labels by consuming natural execution feedback (+10.6% agents, +8.6% finance). This is the academic validation of Mike's append-and-consolidate CORRECTIONS.log/DONT.md pattern: localized deltas, deterministic merge, never monolithic rewrites. https://arxiv.org/html/2510.04618v1 , https://proceedings.iclr.cc/paper_files/paper/2026/file/8a94ff6f922d995d7d3f4ebf4143e442-Paper-Conference.pdf
- Solo-operator recipe: gold set + graded verifier ladder (already exists) become the metric-with-feedback; a scheduled GEPA-light pass proposes edits to gate prompts and SKILL.md descriptions; a Curator step merges accepted deltas into `agent-configs` through the normal proposal flow (an agent never accepts its own proposal).

### 2.5 Observability, drift, fabrication, regression watch

- **Drift investigation, not just tracing**: AgentPulse is an open-source reference implementation that splits agent/handoff/route drift as separate failure classes, requires corroboration before escalating severity (a lone moving metric stays low-confidence), walks the handoff graph upstream to find the originating component, attributes changes only when they could have caused the drift, and exposes findings to a coding agent via MCP plus bundled `drift-triage` / `release-regression-check` skills. Local SQLite, no server. This is the closest public artifact to Mike's "diagnostic auditor specialist." https://github.com/prove-ai/agentpulse
- **Claim-to-evidence auditing**: LEDGER builds layered trace graphs connecting claims to supporting actions, artifacts, and checks (typed edges: produces, checked_by, supports) so a reviewer walks backward from a conclusion to evidence; deliberately treats the graph as an aid, records stay authoritative. https://arxiv.org/html/2608.18398v1
- **Tamper-evident audit**: Audita pairs signed, Merkle-committed inter-agent records with counterfactual replay certification; motivation includes Who&When benchmark results where judge-style failure attribution tops out at ~53.5% agent-level accuracy. Lighter-weight OSS in the same space: AgentAudit (hash chain + RFC 6962 Merkle + Ed25519 + Rekor anchoring, EU-AI-Act-mapped exports). Relevant mainly because EU AI Act high-risk obligations become enforceable August 2, 2026. https://arxiv.org/html/2608.22160 , https://github.com/KaushikKC/AgentAudit
- **Platform landscape** (for awareness, not adoption at solo scale): span-per-tick tracing plus continuous LLM-as-judge sampling of production traces catches semantic drift weeks before user complaints; hierarchical traces localize failures across sub-agents. Guide: https://mlflow.org/articles/what-is-agent-observability-a-2026-developer-guide/
- **Health-check reality check**: "process alive" is not health. Zombie-task postmortem taxonomy: silent subagent death while parent heartbeat stays green, rate-limit sleeps that never wake, cron firing regardless of progress. Fixes: wall-clock budgets, output verification, independent watchdog, explicit completion acknowledgment (scheduler marks task stale if no `done` arrives). https://zemna.net/posts/autonomous-ai-agents-on-cron-a-zombie-task-postmortem/

### 2.6 What this means for the diagnostic swarm

- Orchestrator holds the only write authority to shared state; research/code/audit specialists are read-only reporters whose outputs are claims to be verified, matching the observer rule.
- The audit specialist's core loop: pull run traces (SSSF's SQLite `sssf.db` + CI logs already exist - extend, do not parallel-build, per the no-parallel-infrastructure rule), apply AgentPulse-style checks (drift class split, corroboration-before-severity, upstream origination), emit structured findings as issues, never fix silently.
- Fabrication detection maps onto spot-checking load-bearing claims (commit hashes exist, files contain what's cited) plus LEDGER-style claim->evidence edges in review reports.
- Add plateau/oscillation guards next to the 3-failure stop; make the verifier ladder emit machine-checkable feedback strings so the same output can later drive GEPA.

---

## 3. Proactivity: acting unprompted within guardrails

### 3.1 Trigger design

Field survey of scheduling paradigms (mid-2026): cron/periodic dominates production; event-driven and durable-execution (Temporal-style) fill latency and long-horizon gaps; most deployments sit at autonomy Level 2 of 5 - agents create/modify their own tasks inside hard infra-enforced limits. Claude Code Routines (scheduled remote agents) operate at Level 1-2. https://zylos.ai/research/2026-06-19-autonomous-task-scheduling-self-directed-execution/ , https://zylos.ai/research/2026-05-28-proactive-ai-agents-autonomous-monitors/

Heartbeat patterns, three kinds (pick by shape of work):

1. **Cron** - fixed cadence, same work every cycle (weekly digest).
2. **Signal/event** - webhook/email/issue-event triggers; honest causal record ("ran because X happened").
3. **Change-detection** - run often, compute a cheap state hash, exit unless changed; the right shape for monitors and drift watchers. https://www.knowlee.ai/blog/heartbeat-patterns-proactive-agents

Three disciplines that keep self-triggering fleets healthy (all three violated by Mike's lying-broadcaster anti-pattern history): every triggered run carries enough context to be reproducible; every run produces an artifact even when the answer is "nothing to do"; every run carries the same governance metadata as a human-triggered one. Same source.

Scheduler durability checklist (from a production postmortem corpus): IANA timezones not raw offsets; missed-window policy explicit per schedule (`skip` for anything write-capable, `coalesce` for read-only sweeps); overlap `forbid` on write jobs; idempotency keys from schedule_id + version + UTC tick; resume-from-checkpoint on deploy instead of re-enqueue; dead-letter queue with tick metadata. https://solana.garden/guides/llm-agent-scheduled-cron-job-trigger-systems-explained/

Policy-engine shape worth copying (Reactive Agents gateway): heartbeat policies always/adaptive/conservative with `maxConsecutiveSkips` forcing a fire after silence; daily token budgets; per-hour action caps; event merging (five PRs = one review); critical-priority bypass; kill switch outside the LLM's reach. https://docs.reactiveagents.dev/features/gateway/

### 3.2 Guardrails: external, not prompted

Consensus across sources: safety expressed only in prompts gets evicted, injected, or self-modified away. Required external controls: hard iteration caps per period, tool-call repetition detection, dollar/token circuit breakers, kill switches outside the agent's control surface (GitHub Copilot CVE-2025-53773: an agent exploited a vuln to rewrite its own approval settings). Cold-start hazard: agents with empty conversation history score 9-52% worse on safety benchmarks than warmed ones (arXiv 2606.07867), so a scheduled task's first fire is its most dangerous moment. Autonomy-ceiling argument for keeping Mike's Level-2 posture: "Fully Autonomous AI Agents Should Not be Developed" (arXiv:2502.02649) vs pragmatic overnight-operation needs. https://zylos.ai/research/2026-06-19-autonomous-task-scheduling-self-directed-execution/

OWASP published its Top 10 for Agentic Applications December 2025 (prompt injection, excessive agency, resource exhaustion among them); Microsoft open-sourced an Agent Governance Toolkit April 2026. https://zylos.ai/research/2026-05-28-proactive-ai-agents-autonomous-monitors/

### 3.3 Anti-pattern catalog (field-corroborated)

| Anti-pattern | Field evidence | Mike's existing counterpart |
|---|---|---|
| Lying broadcaster: scheduled reporter outlives the process it reports on | OpenClaw shipped "running" posts every 30 min for a dead process; rule: never wire a notifier to auto-run on first ship | `no-parallel-infrastructure.md` item 3 |
| Parallel infrastructure relapse: writing the rule, violating it 10 days later | OpenClaw DR136/137 postmortem; 11 PRs of unregistered orchestration scripts | Same rule, plus `skill-first.md` clause 4 (adopt over build) |
| Zombie tasks | Heartbeat green, work dead; silent subagent death | Stale-claim reaper (2-hourly) is the same fix for issues |
| Runaway loops | $86k/day burn example; iteration caps + repetition detector + budget mandatory | Hard-stop-at-3-failures covers reasoning loops; add dollar/time caps for scheduled loops |
| Prompt-only guardrails | CVE-2025-53773 self-modification | Damage-control hooks + pre-push/pre-commit = correct posture |
| Catch-up storms after outage | Replay-all default floods APIs | Missed-window=skip policy above |

### 3.4 What this means for agentmesh

launchd on m64 stays the scheduler of record (extend, don't add cron infrastructure). Each proactive job gets: a change-detection hash gate where possible, an artifact-or-nothing contract (writes a run record even on no-op), skip-on-missed-window, and budgets enforced in the wrapper script rather than the prompt. Agents may file issues and proposals autonomously; acceptance stays human or cross-session-reviewed, which is exactly the Level-2 ceiling the field converged on.

---

## 4. SDLC for agent swarms: issue-as-spine, claims, ledgers, handoffs

### 4.1 Public exemplars beyond govcon-factory's own

- **taskops** - shared milestone/card/subtask board for coding agents; truth is an append-only event log, cache disposable, leases sacred; eleven MCP tools; claim = one row, one winner; worktree per agent pinned to a branch for life; reports live as commits in git with the board holding only a pointer (file committed BEFORE registration - "a pointer to bytes that are not in history yet is a pointer to nothing"). Closest public analogue to govcon-factory's claim-discipline machinery. https://github.com/bernatch22/taskops
- **taskledger** - task-first durable ledger with a formal Multi-Actor Handoff Protocol: actor identity (human/agent/system), harness tracking (which tool ran each stage), handoff create -> claim -> close, lock transfer, full event trail. https://github.com/ledgerwerk/taskledger
- **agent-tasks** - MCP server with stage-gated pipelines (backlog -> spec -> plan -> implement -> test -> review -> done), DAG dependencies with cycle detection, decision artifacts (`chose X over Y because Z`), learning artifacts auto-propagated to parent/sibling tasks on completion, heartbeat-based cleanup failing tasks from dead agents. The learning-propagation idea is the missing piece in most systems. https://github.com/internet-dot/agent-tasks
- **IronCore PROTOCOLS.md** - the sharpest handoff format found: sentinel-delimited HANDOFF blocks (Context / Changed / Verified / Next / Gotchas) with field discipline stated as law: "Verified is commands + observed output, or the literal words 'not verified' with why. Claiming verification that didn't happen is the one unforgivable protocol violation." Plus a pickup ritual (read newest handoffs, check deps `[x]`, verify green baseline yourself before claiming), stale-claim reclaim after 3 days of inactivity, one-pass task sizing (<=10 lines description, <=500 line diff, <=90 min). https://github.com/RealDealCPA-VR/IronCore/blob/main/docs/PROTOCOLS.md
- **lead-protocol** - operational-state layer: `handoff.md` per (actor x agent) pair, append-only `decisions.jsonl`, JOURNAL.md, LESSONS.md; three-layer state model (framework / project / actor-x-agent, the third gitignored) solving cross-harness concurrent sessions; vendor-discovery via pointer CLAUDE.md + AGENTS.md files. https://github.com/leonardobuares/lead-protocol
- **OpenACCP** - workflow protocol with authority boundaries B0 (read-only discovery) through B3 (final authority reserved for the human owner by default), handoffs-as-evidence that become completion only after an explicit consume step, and return-wake packets so a child's return wakes its owner instead of waiting in a sidebar. The B0-B3 ladder formalizes Mike's tiered merge-authority policy. https://github.laiyagushi.com/0fuk/OpenACCP
- **agentgrid** - nine-role pipeline demonstrating structured handoff ledger over chat transcripts ("context never silently gets lost"), reviewer rejection loops with bounded rounds, and a deterministic Tester as ground truth ("no model sits between the suite and pass/fail"). https://github.com/ishanavasthi/agentgrid

### 4.2 Loop engineering (the Ralph lineage) as SDLC substrate

Ralph Wiggum technique: a bash loop re-feeding PROMPT.md, one task per iteration, filesystem as memory (`fix_plan.md`, `specs/`, `AGENT.md`), tests as backpressure, "sit on the loop, not in it." Huntley's own caveats: ~90% ceiling on greenfield, unsuitable for legacy, garbage files accumulate, senior-engineer judgment still required. https://ghuntley.com/ralph/ , https://github.com/ghuntley/how-to-ralph-wiggum , https://howaiworks.ai/blog/geoffrey-huntley-ralph-agentic-coding-loop

Named critique worth internalizing (Armin Ronacher): distinguish the agent loop (internal, tool-call cycle) from the harness loop (external queue deciding whether work actually ended); loop-driven code rots defensive and local, "slowly less understandable while appearing more robust." Loop engineering definition per Osmani: "replacing yourself as the person who prompts the agent." Boris Cherny (Claude Code lead): "My job is to write loops." https://howaiworks.ai/blog/geoffrey-huntley-ralph-agentic-coding-loop

Convergence with Mike's system: PLANNING/BUILDING alternating modes, gap-analysis-driven plan files, and commit-per-task map onto the wave-orchestration and status-marker prompts already installed. The novel adoptables: (a) explicit "search before assuming not-implemented" signs, (b) funnel framing (specs -> plan -> loop) with planning mode forbidden from committing, (c) treating every loop failure as prompt-engineering input, i.e., his CORRECTIONS.log loop.

### 4.3 What transfers to govcon-factory / agentmesh

- Keep Issues-as-spine; it matches the strongest public designs (stage gates, claims, leases, event-log truth).
- Adopt the IronCore HANDOFF block format verbatim as the cross-session handoff template in `agent-configs/prompts/` (it encodes verification-law as a document schema).
- Adopt decision + learning artifact types (agent-tasks) folded into `rubric-improve`: a completed task must emit either a decision entry or a learning entry, propagated to the relevant SOP section.
- Adopt report-pointer discipline (taskops): evidence bytes committed in git, boards/queues hold pointers only - already half-true in his CI evidence requirements.

---

## 5. Recommendation: the agentmesh reference architecture

Sized for one operator + subagents. Opinionated. Extends, never parallels, the existing estate (`agent-configs`, govcon-factory SDLC, SSSF runner, omlx routing, m64 launchd).

### 5.1 Components and dataflow

```
                    +--------------------------------------------------+
                    |  ~/agent-configs  (ONE BRAIN, source of truth)    |
                    |  rules/ skills/ prompts/ roles/ hooks/            |
                    |  AGENTS.md canon + CORRECTIONS.log + DONT.md      |
                    +----+-------------------------+-------------------+
                         | generated installs      | GEPA/ACE evolution
                         | (SOURCE.md copies,      | (scheduled, proposal-gated)
                         |  symlinks where legal)  v
        +----------------+------+          +--------------------------+
        | HARNESS SURFACE       |          | EVOLUTION LOOP           |
        | Claude Code (~/.claude)|         | gold sets -> metric w/   |
        | opencode (reads .claude|         | feedback -> GEPA light   |
        |   + .agents natively)  |         | -> Reflector deltas ->   |
        | pi (.pi/skills)        |         | proposals/ (never self-  |
        | Hermes (agentskills.io)|         | accepted)                |
        +-----------+-----------+          +------------+-------------+
                    |                                   |
                    v                                   v
        +-----------------------------------------------+-----+
        | WORK SPINE: GitHub Issues + Project v2 board          |
        | claim protocol, worktree-per-session, tiered merges   |
        | + IronCore-format HANDOFF blocks, decision/learning   |
        |   artifacts filed in the same PR as the work          |
        +---------------------+--------------------------------+
                              | runs produce traces
                              v
        +-------------------------------------------------------+
        | DIAGNOSTIC SWARM (reads fan out, ONE writer)           |
        |  orchestrator: dispatch, verify claims, sole merge     |
        |  research specialist: read-only, fresh context         |
        |  code specialist: bounded task cards, tests=backpressure|
        |  AUDIT specialist: trace analysis (sssf.db + CI logs),  |
        |    AgentPulse-style drift classes, corroboration gate, |
        |    fabrication spot-checks, regression watch -> files   |
        |    issues; clean-context reviewer iterates vs coder     |
        +----------------------------+--------------------------+
                                     | findings
                                     v
        +-------------------------------------------------------+
        | PROACTIVE LAYER (launchd on m64, Level-2 ceiling)      |
        |  heartbeat + inbox check + change-detection hashes     |
        |  artifact-or-nothing contract; skip-on-missed-window   |
        |  budgets/caps/kill switch in wrapper scripts           |
        |  smoke-test-by-hand before any cadence goes live       |
        +--------------------------------------------------------+
```

### 5.2 Adopt vs skip

| Candidate | Verdict | Why |
|---|---|---|
| AGENTS.md as canon + thin CLAUDE.md import/symlink per repo | **Adopt** | De facto standard; empirically cuts bugs 35-55%; matches agent-configs role |
| `.agents/skills/` as canonical skill tree + SOURCE.md copies into `~/.claude/skills/` | **Adopt** | opencode reads both natively; Codex reads `.agents/`; zero adapters for the two main harnesses |
| Frontmatter minimalism (name+description, space-delimited allowed-tools) | **Adopt** | Only portable subset; silent stripping elsewhere is documented |
| Superpowers-style enforcement bootstrap | **Already have** (skill-first rule + library meta-skill); align wording | Enforcement beats library size |
| codejunkie99/agentic-stack memory-layer layout | **Mine, don't install** | His fork exists; lift the four-memory-layer + nightly-staging-cycle structure into agent-configs conventions |
| oh-my-opencode | **Skip** | Heavy OpenCode-specific orchestration layer = parallel infrastructure risk; opencode native agents/skills cover the need |
| GSD (original repo) | **Skip the repo, mine the patterns** | Governance/trust incident; `.planning/` state files + model profiles + thin orchestrators are the transferable parts |
| Clean-context reviewer loop (Cognition Code-Review-Loop) | **Adopt** as the audit specialist's core | ~2 bugs/PR incl. severe, works because reads are free and context is clean |
| AgentPulse drift methodology (classes, corroboration, upstream attribution, MCP exposure) | **Adopt concepts, extend SSSF traces** | Reference implementation is Python/OpenAI-centric; the five design rules are the value |
| karpathy/llm-council code | **Skip code, steal mechanic** | Abandoned, unlicensed; anonymous peer review + preserve-minority-findings is the takeaway |
| GEPA via DSPy on gold sets (monthly, light budget) | **Adopt** after poison harness exists | Needs a metric-with-feedback; gold sets already defined; Nous Hermes repo is the adjacent adoptable |
| ACE-style delta curation for rules/skills | **Already convergent** (CORRECTIONS.log append-and-consolidate); cite as validation | Incremental deltas beat monolithic rewrites, per ICLR 2026 |
| taskops/taskledger/lead-protocol wholesale | **Skip tools; adopt schemas** | One queue already exists (Issues); lift HANDOFF block, decisions.jsonl, learning-artifact shapes into templates |
| Ralph-style unattended build loops | **Contraindicated for govcon deliverables**; acceptable for sandboxed research branches | 90% ceiling, defensive-code rot, Mike approves every send |
| Commercial observability SaaS (LangSmith/Langfuse/etc.) | **Skip for now** | Solo scale; SQLite + CI logs + audit agent cover the need; revisit if multi-machine fleet grows |

### 5.3 Sequencing (dependency order)

1. Wire AGENTS.md canon + skill-path convention (days, reversible, pure docs).
2. Formalize HANDOFF/decision/learning artifact templates in agent-configs (days).
3. Stand up the audit specialist against existing sssf.db/CI traces with AgentPulse's five rules as its checklist (weeks; extends existing pipeline, satisfying no-parallel-infrastructure).
4. Add proactive wrappers: change-detection gates, artifact-or-nothing, budgets in wrapper scripts; hand-smoke-test each before scheduling (rule already written).
5. Last: GEPA/DSPy evolution loop gated behind a built poison harness and gold-set metrics, filing proposals only.

Each step lands through the normal PR -> CI -> reviewer-bot -> tiered merge path; Tier-2 governing-doc changes stay Mike-merged.

---

## SOURCES

- AGENTS.md standard site - https://agents.md/
- OpenAI Codex AGENTS.md guide (precedence, 32 KiB cap) - https://developers.openai.com/codex/guides/agents-md
- Cross-tool portability survey incl. Gloaguen et al. 2026 findings - https://codex.danielvaughan.com/2026/05/27/agent-instruction-files-agents-md-claude-md-cross-tool-portability-codex-cli/
- AGENTS.md guide, adoption tables (March-May 2026) - https://benjamincrozat.com/agents-md , https://codersera.com/blog/agents-md-complete-guide-2026/ , https://vibecoding.app/blog/agents-md-guide , https://automationswitch.com/automation-engineering/agents-md-explained
- Harness engineering census, 2,853 repos (arXiv 2602.14690) - https://arxiv.org/html/2602.14690v5
- Agent Skills spec - https://agentskills.io/home ; Claude Code skills docs - https://code.claude.com/docs/en/skills.md ; opencode skills docs - https://opencode.ai/docs/skills/
- Skill portability deep dives - https://codemyspec.com/blog/skill-portability , https://mcp.directory/blog/cross-agent-skills-cursor-codex-cline-antigravity-gemini-mastra-portability , https://github.com/jamie-bitflight/claude_skills/blob/main/plugins/plugin-creator/skills/skill-creator/references/agent-plugin-ecosystem.md , https://agentskills.co.il/en/guides/multi-agent-compatibility
- obra/superpowers - https://github.com/obra/superpowers ; install matrix - https://dev.to/rosgluk/superpowers-quickstart-install-workflow-and-tryout-505n ; marketplace - https://github.com/obra/superpowers-marketplace
- GSD - https://github.com/glittercowboy/get-shit-done , user guide - https://github.com/glittercowboy/get-shit-done/blob/main/docs/USER-GUIDE.md , anatomy writeup + governance note - https://www.codecentric.de/en/knowledge-hub/blog/the-anatomy-of-claude-code-workflows-turning-slash-commands-into-an-ai-development-system , http://gsd.site/
- oh-my-openagent config reference - https://github.com/code-yeongyu/oh-my-openagent/blob/dev/docs/reference/configuration.md , omo.json reference - https://github.com/code-yeongyu/oh-my-openagent/blob/dev/docs/reference/omo-json.md
- codejunkie99/agentic-stack (forked as redtrades/agentic-stack) - https://github.com/codejunkie99/agentic-stack , https://github.com/redtrades/agentic-stack
- Cognition, "Multi-Agents: What's Actually Working" (Apr 2026) - https://cognition.ai/blog/multi-agents-working ; Devin Fusion - https://cognition.com/blog/devin-fusion
- Multi-agent reconciliation analyses - https://dev.to/harryfloyd/your-multi-agent-system-is-an-org-chart-k2e , https://agenticlab.sunilprakash.com/signal/003-multi-agent-decision-variable/ , https://dev.to/tony__vi/you-dont-need-sub-agents-1eh7
- Karpathy llm-council - https://github.com/karpathy/llm-council ; abandonment issue - https://github.com/karpathy/llm-council/issues/192 ; productization history - https://llmcouncil.ai/karpathy-llm-council ; council groupthink experiment - https://www.strangeloopcanon.com/p/llm-councils-show-groupthink ; architecture walkthrough - https://starlog.is/articles/llm-engineering/karpathy-llm-council
- Evaluator patterns - planner-generator-evaluator - https://www.agentpatternscatalog.org/patterns/planner-generator-evaluator-harness/ ; evaluator-optimizer tutorial - https://www.agentnotebook.dev/tutorials/agentic-workflow-evaluator-optimizer-python ; catalog entry - https://github.com/agentpatternscatalog/patterns/blob/main/patterns/evaluator-optimizer.md ; QA separation - https://www.shiplight.ai/blog/planner-generator-evaluator-multi-agent-qa ; verifier loops - https://jigarjoshi.in/blog/independent-verifier-loops-and-self-improving-agents/ ; self-correction guide - https://wandb.ai/site/articles/agentic-ai-self-correction-how-to-build-systems-that-fix-their-own-mistakes/ ; reflection loops - https://mortalapps.com/agents/architecture-patterns/agent-reflection-and-self-correction/ ; generator-evaluator loops - https://dev.to/eleonorarocchi/generator-evaluator-loops-for-ai-agents-4kd2
- GEPA - DSPy docs - https://dspy.ai/api/optimizers/GEPA/overview/ , https://dspy.ai/diving-deeper/gepa-in-depth/ ; project - https://gepa-ai.github.io/gepa/ , https://github.com/GEPA-ai/GEPA ; paper - https://arxiv.org/abs/2507.19457 ; Hermes self-evolution - https://github.com/NousResearch/hermes-agent-self-evolution
- ACE - https://arxiv.org/html/2510.04618v1 ; ICLR 2026 proceedings PDF - https://proceedings.iclr.cc/paper_files/paper/2026/file/8a94ff6f922d995d7d3f4ebf4143e442-Paper-Conference.pdf
- Observability/audit - AgentPulse - https://github.com/prove-ai/agentpulse ; LEDGER - https://arxiv.org/html/2608.18398v1 ; Audita - https://arxiv.org/html/2608.22160 ; AgentAudit - https://github.com/KaushikKC/AgentAudit ; AgentTrace - https://arxiv.org/pdf/2602.10133 ; 2026 observability guide - https://mlflow.org/articles/what-is-agent-observability-a-2026-developer-guide/
- Proactivity/scheduling - Zylos surveys - https://zylos.ai/research/2026-06-19-autonomous-task-scheduling-self-directed-execution/ , https://zylos.ai/research/2026-05-04-autonomous-agent-scheduling-self-direction/ , https://zylos.ai/research/2026-05-28-proactive-ai-agents-autonomous-monitors/ ; heartbeat patterns - https://www.knowlee.ai/blog/heartbeat-patterns-proactive-agents ; cron durability - https://solana.garden/guides/llm-agent-scheduled-cron-job-trigger-systems-explained/ ; policy-engine gateway - https://docs.reactiveagents.dev/features/gateway/ ; zombie-task postmortem - https://zemna.net/posts/autonomous-ai-agents-on-cron-a-zombie-task-postmortem/
- SDLC exemplars - taskops - https://github.com/bernatch22/taskops ; taskledger - https://github.com/ledgerwerk/taskledger ; agent-tasks - https://github.com/internet-dot/agent-tasks ; IronCore protocols - https://github.com/RealDealCPA-VR/IronCore/blob/main/docs/PROTOCOLS.md ; lead-protocol - https://github.com/leonardobuares/lead-protocol ; OpenACCP - https://github.laiyagushi.com/0fuk/OpenACCP ; agentgrid - https://github.com/ishanavasthi/agentgrid
- Ralph / loop engineering - https://ghuntley.com/ralph/ , https://ghuntley.com/loop/ , https://github.com/ghuntley/how-to-ralph-wiggum , https://howaiworks.ai/blog/geoffrey-huntley-ralph-agentic-coding-loop , https://www.abrahamberg.com/blog/spec-driven-development-and-the-ralph-loop-the-good-the-bad-and-the-ugly/ , https://devinterrupted.substack.com/p/inventing-the-ralph-wiggum-loop-creator

STATUS: research complete
STATE: deliverable written to staging/research-agentic-engineering.md (5 sections, ~40 cited sources, adopt/skip table + sequencing)
NEXT: Mike reviews; adopt-candidates 1-2 (AGENTS.md canon, handoff/artifact templates) are docs-tier and can land immediately
BLOCKED-ON: none
