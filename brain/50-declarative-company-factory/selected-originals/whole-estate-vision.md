# Whole-estate first-principles vision

**Date:** 2026-08-30  
**Status:** research and proposed target state; not an adoption or implementation authorization  
**Scope:** all first-party repositories, the complete fork radar, preserved OpenClaw research, the Hermes/SSSF migration, product factories, and the current open-source/managed market

## Executive answer

The intended product was never just an autonomous coding loop, an issue
controller, a multi-agent chat framework, or a GovCon pipeline. It was a
**solo-operator enterprise operating system**:

> A system that can define, instantiate, operate, evaluate, improve, and retire
> agent-run companies and projects, while one person directs goals, budgets,
> policy, and exceptions.

The system has two recursive outputs:

1. it builds and improves the agent workforce and the platform that governs it;
2. that workforce operates product companies and recurring personal/business
   workflows.

The recovered estate shows six recurring outcomes:

- turn attention, research, meetings, and market signals into durable knowledge
  and action;
- turn goals into declarative companies, departments, roles, workflows, and
  budgets;
- let interchangeable agents and models execute those workflows across local,
  subscribed, free-tier, and paid compute;
- produce evidence-grounded software and business deliverables rather than
  dashboards of activity;
- learn from outcomes through governed experiments rather than direct
  self-modification; and
- keep the operator focused on choices, approvals, and exceptions rather than
  queue maintenance.

The recommended ideal-state composition is **adopt-first**, not greenfield:

```text
Operator surfaces
  Paperclip mobile/web + concise briefings + selected native tools
                         |
Company/work authority  |  Paperclip candidate
  goals, org, budgets, work identity, admission schedule, governance, attention
                         |
Durable process fabric  |  Conductor OSS candidate
  versioned workflows, waits, signals, retries, forks, compensation, schedules
                         |
Agent workforce         |  Hermes, Codex, Claude, OpenHands, Pi, Jules, scripts
  replaceable runtime adapters and model routes
                         |
Department systems      |  GitHub for software; domain factories for products
  exact code/artifact history, data, schemas, gates, deliverables
                         |
Evidence and evolution  |  OTel + eval suites + governed GEPA/DSPy experiments
  receipts, fitness, lineage, independent selection, rollback
```

This is one authority per concern, not several competing control planes:

- the company layer owns **why and what work exists**;
- Conductor owns **the execution state of one admitted workflow attempt**;
- Git owns **the identity and history of source and reviewable artifacts**;
- each product factory owns **its domain data, rules, and outputs**;
- an agent runtime owns only **its live session and tool loop**;
- semantic memory and dashboards are derived views, never authority.

The company/work owner is also the only owner of schedules that create work.
Conductor timers and schedules may advance an already admitted workflow or emit
a proposal, but may not create a second authoritative work item. Company
governance approvals (strategy, hiring, plans, budgets) are distinct from exact
effect grants (send, spend, deploy, delete, merge). A Conductor Human/Wait result
is authenticated evidence supplied to the effect-policy authority; it is never
itself permission to perform the effect.

Conductor is a major correction to the earlier analysis. It is a maintained
Apache-2.0 continuation of Netflix Conductor with versioned JSON workflows,
polyglot workers, persistent long-running execution, Wait/Human/event tasks,
dynamic fork/join, sub-workflows, schedules, retries, and failure workflows.
Its declarative process model is unusually close to the old “Terraform for
swarms and companies” intent. It does not supply company goals, organizational
governance, artifact promotion, secure tenancy, or safe genetic evolution, so it
belongs beneath—not instead of—the company and authority layers.
([Conductor repository](https://github.com/conductor-oss/conductor),
[core concepts](https://github.com/conductor-oss/conductor/blob/main/docs/devguide/concepts/index.md),
[durable execution](https://github.com/conductor-oss/conductor/blob/main/docs/architecture/durable-execution.md))

## What the entire repository estate says

The authenticated inventory contains 73 repositories: 19 first-party and 54
forks. The full machine-readable and categorized account evidence is preserved
in [`REDTRADES-REPOSITORY-INVENTORY-2026-08-30.md`](/Users/man/agent-platform/research/REDTRADES-REPOSITORY-INVENTORY-2026-08-30.md).

### First-party lineage

| Repository | Recovered purpose | Place in the ideal system |
| --- | --- | --- |
| `openclaw`, `openclaw-backup`, `openclaw-config`, `openclaw-v2`, `openclaw-v3`, `workspace-main` | Personal/company OS, Mind/Body/Brain, baseline roles, schedules, research/vault, SwarmClaw, courtroom review, memory, autonomy | Historical product and capability specification; mine contracts, never restore the runtime wholesale |
| `agent-workspace` | Plain-Git work coordination, mechanically enforced evidence and human-decision rules | Proven small invariants and conformance fixtures |
| `agent-configs` | Provider-neutral roles, skills, hooks, rules, prompts, configurations | Genome source material; promote only versioned, scoped packages with activation receipts |
| `agent-mesh` | Research, portable brain, Hermes deployment, local inference, evaluations, proactive pipelines, SwarmClaw | Research/evaluation corpus and runtime adapter evidence |
| `agent-platform` | Cross-system authority, exact receipts, effects, review, reconciliation | Narrow invariant and conformance layer; not another full platform |
| `govcon-factory` | Public federal data to free reports and paid opportunity packets | First revenue-producing company/domain pack and primary dogfood slice |
| `work-ops` | Meetings, briefs, pipelines, tasks, OKRs, documents, second brain | Operator/productivity department patterns, now absorbed into the broader OS intent |
| `ninov-trader`, `tesla-swing`, `polymarket-arb` | Market data, options signals, backtests, prediction-market sentiment | Separate regulated/risk-bounded product experiments; research/paper mode by default |
| `curate-and-share-now`, `v0-news-ai` | News ingestion, summarization, curation, social content | Intelligence/content company pack and research-intake precedent |
| `webapp` | Generic product shell | Commodity starter only; no platform authority |
| `terraform-reference-architectures` | Declarative multi-account infrastructure and environment composition | Evidence for desired module/reconciliation UX; use OpenTofu/managed services rather than copy old infra |

The estate audit correctly identified which repository currently governs work,
but it answered a narrower authority question. It did not fully answer what the
five-month product was supposed to become. The stronger historical synthesis is
in [`GENETIC-SWARM-PLATFORM-DEEP-DIVE-2026-08-30.md`](/Users/man/agent-platform/research/GENETIC-SWARM-PLATFORM-DEEP-DIVE-2026-08-30.md),
while the audit remains useful evidence about repository status:
[`AGENT-PLATFORM-FULL-AUDIT.md`](/Users/man/agent-reports/agent-configs-consolidation/AGENT-PLATFORM-FULL-AUDIT.md).

### The fork estate is a deliberate prior-art radar

The 54 forks are not random. Together they describe the missing product planes:

- **factory and swarm topology:** Fusion, `factory`, `claude-flow`,
  `oh-my-claudecode`, `oh-my-codex`, `awesome-claude-agents`, `Subagents`,
  `agency-agents`, `deepagents`, `agentic-stack`;
- **coding bodies:** Codex, Claude Code, OpenClaude, AnyClaude, Claw Code,
  Shadow, Superpowers, gstack;
- **skills and workforce genomes:** `skills`, `awesome-openclaw-skills`,
  `awesome-claude-code`, `claude-agents`, `agents`, `agency-agents`;
- **memory and evolution:** MemPalace and Hermes Agent Self-Evolution;
- **tool and experience surfaces:** Chrome DevTools MCP, VibeVoice,
  social-media-agent;
- **model access and research:** Free LLM API Resources, OpenAI Cookbook,
  AI Crash Course, Awesome AI Agents;
- **declarative infrastructure and reproducibility:** Terraform guides/modules,
  HashiStack, autoenv, DevOps exercises;
- **older data/ML foundations:** ATM, machine-learning examples, data science,
  Fabric, visualization, and web-service boilerplates.

The account history therefore points consistently toward a provider-neutral
company/workforce platform with composable agents, not toward a single custom
controller. The correct use of the forks is **capability discovery and upstream
evaluation**, not mass installation or copied code.

## The original intent, reconstructed as a whole

### 1. Operator and attention OS

OpenClaw's first promise was personal leverage: research becomes knowledge,
meetings become artifacts, ideas become work, and the operator gets evenings
back. The intended surfaces included briefings, Slack, GitHub, a mobile
SwarmClaw command center, desktop chat, and later voice/wearables. Watch, Assist,
and Autonomous modes were an attention and authority contract, not a decorative
dial.

The ideal system therefore needs:

- one intake for links, ideas, meetings, messages, and exceptions;
- proactive sensors and a daily/weekly brief;
- an attention queue ranked by goal impact, risk, deadline, and uncertainty;
- previews of proposed effects and one-tap approve/reject/defer actions;
- evidence and explanations without requiring the operator to read raw traces;
- personal, sensitive, and company domains kept separate by policy.

### 2. Declarative company factory

The desired reusable artifact is not merely an agent manifest. It is a portable
company package. The schema is intentionally undecided; the following is an
illustrative capability shape, not an accepted `agentcompanies` version:

```yaml
apiVersion: candidate.example/v0
kind: Company
metadata:
  name: govcon-intelligence
spec:
  mission: produce evidence-grounded federal market reports and opportunity packets
  outcomes: [monthly_profit, customer_value, operator_attention]
  departments: [research, production, distribution, finance, platform]
  roles: [lead, scout, analyst, producer, reviewer, operator]
  workflows: [market-report, opportunity-packet, matched-outreach, weekly-review]
  budgets: {money: bounded, model_tokens: bounded, operator_minutes: bounded}
  authority: {default: assist, destructive: human, external_send: human}
  dataPolicy: {sources: allowlisted, sensitive_routes: local_or_approved}
  evaluations: [grounding, completeness, value, compliance, cost]
  deployment: {local: true, managed_workers: optional}
```

Like Terraform, the declaration needs validate, plan, apply, observe drift,
reconcile, export, and destroy. Unlike Terraform, it also needs long-running
workflows, human waits, retries, compensation, work products, and learning. This
is why company control and workflow execution are separate planes.

Paperclip currently documents `agentcompanies/v1-draft`, while other related
artifacts use `v1`. That inconsistency is evidence that no standard has been
selected. Paperclip and Fusion candidates must round-trip a hostile sample while
preserving unknown extensions and source/license provenance, rejecting embedded
executable content and secret values, and reproducing behavior before an owned
format is standardized.
([Paperclip company specification](https://github.com/paperclipai/paperclip/blob/master/docs/companies/companies-spec.md))

### 3. Agent workforce factory

An agent is a versioned genome expressed through a runtime and model:

```text
agent = role + objectives + skills + tools + memory policy + model policy
        + authority + evals + deployment profile
```

Prime, Forge, Scout, Sentinel, and Operator are useful default archetypes, not
five permanently running daemons. A company instantiates only the roles it
needs; specialists are ephemeral; independent review uses a distinct model or
principal when the risk requires it.

Hermes was adopted because it already supplied profiles, skills, tools, cron,
delegation, providers, local models, and ACP. That was the right adopt-first
move for an agent **Body**. It was never a replacement for company goals,
durable business processes, exact artifact authority, or evolution governance.

### 4. Durable process fabric

The platform needs processes that span minutes to months:

- research intake and morning brief;
- meeting to decisions, tasks, documents, and follow-up drafts;
- idea discovery to demand test, build, distribution, and kill/persist choice;
- GovCon ingestion to report, company match, packet, review, and outreach;
- software issue to isolated change, deterministic tests, review, promotion,
  deployment, and cleanup;
- skill/prompt mutation to evaluation tournament, selection, rollout, and
  rollback.

These are not all software-development workflows. This is precisely where
Conductor is stronger than an agent graph or coding-agent platform as the
general execution substrate.

### 5. Knowledge and intelligence OS

The system needs a source-aware knowledge graph and document store, but semantic
memory must remain a derived index:

- canonical reviewed knowledge and work products live in durable files/object
  storage/databases with provenance;
- raw transcripts and runtime memory are evidence inputs;
- MemPalace or another retrieval layer indexes canonical material and carries
  source, scope, freshness, and correction metadata;
- agents retrieve narrowly and disclose what was loaded;
- no memory entry can silently rewrite policy, skills, facts, or acceptance
  criteria.

### 6. Product and revenue factories

GovCon is the leading proposed first whole-company proof because it has real external data,
repeatable stages, measurable artifact quality, legal/compliance boundaries,
distribution, price, and operator-time economics. Its current intent is free
industry reports plus a $699 evidence-grounded opportunity packet—not a generic
dashboard and not invented “winning proposals.” See
[`PLAN-V5.md`](/Users/man/govcon-factory/sop/PLAN-V5.md).

The other first-party repositories establish later company packs:

- intelligence/news and content;
- product/idea discovery and validation;
- personal work/meeting operations;
- market research and paper-trading signals;
- software products created by the software department.

The platform should never absorb their domain schemas, commercial rules, or
data. It supplies the company, workflow, workforce, evidence, and economics
contracts they consume.

### 7. Genetic improvement without poisoning

“Genetic” means candidate variation plus measured selection, not agents editing
their own permanent instructions:

```text
observe failure/opportunity
  -> propose mutation
  -> fork isolated candidate genome
  -> run fixed + held-out evaluations
  -> compare quality, cost, latency, safety, operator time
  -> independent selection
  -> staged inheritance with rollback
```

Candidates can include prompts, skills, examples, model routes, tool sets,
workflow definitions, role configurations, or code. The evaluator corpus,
authority policy, and promotion mechanism cannot be mutated by the candidate
being judged. DSPy/GEPA can search candidates; it does not get to define fitness
or promote the winner.

## Current market: what should be adopted

### Company and portfolio control plane: Paperclip is the leading hypothesis

Paperclip now describes almost the exact missing abstraction: company as a
first-class boundary, goals, organization, agent adapters, tasks, atomic
checkout, heartbeats, budgets, approvals, routines, work products, attention,
mobile use, and company import/export. Its adapters include Codex, Claude,
Gemini, Pi/CLI processes, HTTP agents, and OpenClaw-style bots. The companion
Companies repository supplies portable templates.
([Paperclip repository](https://github.com/PaperclipAI/paperclip),
[product definition](https://github.com/PaperclipAI/paperclip/blob/master/doc/PRODUCT.md),
[adapter overview](https://github.com/PaperclipAI/paperclip/blob/master/docs/adapters/overview.md),
[Paperclip Companies](https://github.com/paperclipai/companies))

It is not approved for live use merely because the feature fit is strong. Its
official advisory register includes critical RCE, cross-company authorization,
command-injection, credential, XSS, and approval-attribution classes. Many older
issues list patched versions, but the full advisory/fix/dependency inventory and
the current trust boundaries must pass a disposable test before any real data,
credentials, or autonomous effects are attached.
([Paperclip advisories](https://github.com/paperclipai/paperclip/security/advisories),
[release history](https://github.com/paperclipai/paperclip/releases))

**Decision:** treat Paperclip as the leading company/control-plane candidate,
not as already selected infrastructure.

### Durable orchestration: Conductor belongs in the first bake-off

Conductor was missed because earlier research treated workflow engines mainly
as reliability internals for the software controller. Viewed against the whole
estate, its declarative graphs, human/event waits, subflows, polyglot workers,
schedules, dynamic branches, UI, and operational replay controls fit nearly
every company workflow.

Important boundaries:

- task delivery is at-least-once, so every external effect needs an idempotency
  key, exact receipt, and often compensation;
- the OSS API is open by default and must be private and protected;
- task domains are routing, not security tenancy;
- OSS is operationally material (server, database/queue/index/locking choices);
- Orkes Developer is free but non-production; production is custom-priced.

The full current comparison is
[`WHOLE-ORCHESTRATION-LANDSCAPE-WITH-CONDUCTOR-2026-08-30.md`](/Users/man/agent-platform/research/WHOLE-ORCHESTRATION-LANDSCAPE-WITH-CONDUCTOR-2026-08-30.md).
Orkes documents its free Developer Playground as prototype-only and its
production plan as custom-priced.
([Orkes pricing](https://orkes.io/pricing))

**Decision:** evaluate Conductor OSS first, with Dapr Workflow/Agents, Temporal,
and Restate or DBOS as fault-injected challengers. Do not build a workflow
engine.

### Agent execution bodies: retain several, standardize the adapter

- **Hermes:** default persistent/local general agent and inexpensive worker.
- **Codex/Claude/provider CLIs:** interactive coding, research, and independent
  challenge using subscription value already paid for.
- **OpenHands:** optional maintained coding/sandbox department worker; not the
  company or workflow authority.
- **Pi:** small scriptable local/hosted worker and judge unit.
- **Jules/GitHub-hosted agents:** asynchronous repository workers where their
  native hosted environment removes local operations.

The owned interface should be small: accept a signed work packet, report
checkpoint/heartbeat/cost, emit artifacts and evidence, honor cancel, and carry
the authority grant. Do not normalize every runtime feature.

### Software-factory suites: Fusion is also a whole-authority challenger

The account's newly refreshed Fusion fork is directly relevant. Current Fusion
positions itself as a model-neutral software factory spanning missions, tasks,
agents, Git, files, worktrees, planning, review, execution, and optional human
approval. It could retire substantial custom software-delivery orchestration if
its security, recovery, artifact identity, and authority behavior pass the same
fixtures. Its workflow import/export and broader lifecycle model mean it must
also be tested as a possible single lifecycle/control-plane path, not dismissed
solely as an SDLC worker. Its software-factory center still leaves operator,
general business-process, knowledge, and multi-company requirements to prove.
([Fusion repository](https://github.com/Runfusion/Fusion))

**Decision:** compare three mutually exclusive authority compositions: (A)
Paperclip plus a subordinate execution engine, (B) Fusion with only the minimum
non-overlapping extensions, and (C) the current GitHub/CAS contract plus a
subordinate execution engine. Do not run Fusion's task authority beside an
authoritative Paperclip/GitHub task system without disabling and proving one
side's ownership.

### Execution security: OpenShell is the leading local sandbox hypothesis

NVIDIA OpenShell deserves a bounded security trial rather than another custom
seatbelt/container wrapper. Its documented architecture separates a privileged
supervisor from an unprivileged agent child and combines filesystem policy,
capability removal, seccomp, network namespaces, a policy proxy, credential
injection, and inference routing. It lists Codex, Claude Code, OpenCode,
OpenClaw, Hermes through NemoClaw, and community Pi/Ollama paths.
([OpenShell repository](https://github.com/NVIDIA/OpenShell),
[sandbox architecture](https://github.com/NVIDIA/OpenShell/blob/main/architecture/sandbox.md))

That surface is powerful enough to require hostile-input, credential, egress,
callback, teardown, and Apple-Silicon tests. OpenShell should enforce a granted
capability envelope; it must never decide what work or effect is authorized.

### Software department: GitHub Pro and native automation

GitHub should remain the hosted software forge. Git objects identify exact
source and candidates; pull requests and Actions provide collaboration and
deterministic evidence. GitHub Pro's official price is $4/month and adds private
repository protections and increased Actions/Codespaces allowances. GitHub
Agentic Workflows can compile Markdown agent workflows into permission-bounded
Actions and is a promising way to retire custom repo monitors, triage, review,
documentation, and maintenance scripts, beginning read-only because it is still
preview software.
([GitHub pricing](https://github.com/pricing),
[GitHub plans](https://docs.github.com/en/get-started/learning-about-github/githubs-plans),
[GitHub Agentic Workflows](https://github.com/github/gh-aw))

Self-hosted GitLab is deferred. It would add upgrades, backups, runners,
availability, and security operations, while required approvals and merge
trains remain paid features in current GitLab plans.
([GitLab pricing](https://about.gitlab.com/pricing/),
[merge-request approvals](https://docs.gitlab.com/user/project/merge_requests/approvals/),
[merge trains](https://docs.gitlab.com/ci/pipelines/merge_trains/))

### Knowledge, evaluation, telemetry, and infrastructure

| Responsibility | Adopt/host choice | Why |
| --- | --- | --- |
| Canonical knowledge | Git + object storage + product databases | Inspectable provenance and domain ownership |
| Semantic retrieval | MemPalace pilot or a narrower proven index | Existing local evidence; replaceable derived service |
| Model gateway | Existing FreeLLMAPI/LiteLLM-compatible gateway | One routing, budget, sensitivity, and fallback seam |
| Evaluations | Promptfoo/Inspect plus domain deterministic suites | Fixed and held-out fitness outside candidate control |
| Prompt/skill search | DSPy/GEPA in isolated experiments | Implements the genetic search, not promotion authority |
| Telemetry | OpenTelemetry contract; Grafana Cloud Free pilot or one self-hosted backend | Avoid another custom dashboard/database |
| Object/backup | Cloudflare R2 free/low-cost tier | Cheap external artifact and backup store |
| Local environments | Dev Containers/Docker Compose first | Reproducible without premature Kubernetes |
| Infrastructure declaration | OpenTofu only for real cloud resources | Terraform-like lifecycle without custom IaC |
| Secure remote workers | GitHub-hosted runners first; E2B/Cloudflare/Daytona only when a workload requires | Pay for isolation rather than operate a cluster too early |
| Local agent sandbox | OpenShell restricted trial | Reuse maintained policy/isolation instead of custom sandbox infrastructure |

Pricing and free tiers are volatile and must be rechecked at procurement time.

### Managed modular substrate: AgentCore requires an explicit comparison

Amazon Bedrock AgentCore is the material managed alternative to piecing together
runtime, identity, gateway, policy, memory, sandbox tools, observability,
evaluation, and optimization. AWS documents the services as independently
usable with external models and frameworks, including an isolated runtime,
fine-grained Cedar policy, identity, MCP gateway, code/browser tools, OTel-backed
evaluation, and controlled optimization. It is consumption-priced and AWS-bound;
it does not replace portable company/work authority merely because it hosts the
workers.
([AgentCore overview](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/what-is-bedrock-agentcore.html))

**Decision:** after the local composition proves the workload, compare one
synthetic non-code company workflow on AgentCore. Reject it if AWS coupling,
artifact/trace export, policy mapping, teardown, or measured cost is worse than
the selected local/OSS path.

## What remains custom—and only this

The owned layer should shrink to contracts that the upstreams do not jointly
guarantee:

1. a secret-free portable company package and validation/conformance suite,
   with its concrete format selected only after round-trip tests;
2. exact cross-system identity mapping for company, work item, workflow attempt,
   worker session, artifact, review, and effect receipt;
3. effect authorization and approval grants that workers and workflows cannot
   mint for themselves;
4. source/candidate/review/promotion receipts bound to immutable revisions;
5. adapter conformance and reconciliation across Paperclip, Conductor, GitHub,
   and product factories;
6. fixed/held-out evolution fitness and lineage with staged inheritance and
   rollback;
7. teardown/orphan detection and disaster-recovery proof.

Everything else should be upstream configuration, a plugin, a worker, or a
domain package. Adoption must delete overlapping custom code; adding an upstream
without retiring a queue, scheduler, database, dashboard, or runtime is a
failed adoption.

## Ideal authority map

| Concern | One authoritative owner | Non-authoritative projections/executors |
| --- | --- | --- |
| Company mission, org, budgets, portfolio | Paperclip if it passes; otherwise current thin company contract | SwarmClaw, briefs, dashboards |
| Work identity, goal ancestry, assignee, approval state | Paperclip if it passes | GitHub issue, Conductor metadata, runtime todo |
| Work-creating schedules and admission | Same company/work authority | Conductor may advance an admitted attempt or emit a proposal only |
| Workflow attempt state, waits, retries, cancellation | Selected engine, with Conductor first finalist | Paperclip run view, OTel traces |
| Company governance decisions | Company/work authority | Briefs and UI projections |
| Exact external-effect grant | Independent effect-policy authority bound to effect hash and actor | Paperclip approval card and Conductor Human/Wait are evidence inputs only |
| Source and artifact identity | Git/object store/product DB | Paperclip attachment, Conductor payload reference |
| Software review and merge | GitHub rules plus exact-head promotion policy | Agent review summaries |
| Product facts and commercial rules | Product factory | Platform and company UI |
| Runtime session | Selected agent adapter | Company/work projections |
| Durable knowledge | Reviewed files/data | Semantic memory and chat recall |
| Mutation fitness and inheritance | External eval/promotion protocol | GEPA/DSPy candidate generator |

If Paperclip cannot be constrained to this map, it is rejected. If Conductor is
allowed to create authoritative work or approve effects, the composition is
rejected. If GitHub Issues remain the software department's native record, the
company work item must map to exactly one GitHub issue and reconcile terminal
state explicitly; neither can silently overwrite the other.

## The first end-to-end proof

This is the next **architecture evaluation** after the repository's currently
accepted transactional/recovery critical path is completed, or after the owner
explicitly approves a material-plan supersession. It should not be started
merely because this research exists. At that boundary, the proof should
instantiate one small GovCon company from a declaration and execute one
real-shaped, synthetic-data opportunity-packet workflow:

1. import the company package with all schedules disabled and no secrets;
2. show the planned org, budgets, workflows, tools, effects, and infrastructure;
3. admit one opportunity work item;
4. start one version-pinned Conductor workflow;
5. dispatch research/extraction/drafting/review tasks across at least two agent
   bodies and two model providers without changing the workflow contract;
6. kill the worker, workflow server, and host at separate points and resume;
7. inject a duplicate effect and prove idempotency/receipt behavior;
8. wait for a signed operator approval, rejecting replayed/wrong-task approval;
9. produce a grounded packet artifact and independent evaluation;
10. export the company/work/evidence package and rebuild it cleanly;
11. tear it down and prove no worker, schedule, credential, or lease remains.

The bake-off repeats the workflow on Dapr/Temporal and one lightweight candidate
using the same work packet. Measure operator minutes, duplicate effects,
recovery, custom code, idle resources, workflow-version friction, model cost,
and clarity—not star count or connector count.

## Sequenced plan

### Phase 0 — freeze invention and define the evaluation package

- Accept this document only as the proposed ideal state.
- Complete the accepted transactional/recovery critical path first, unless the
  owner explicitly approves a superseding material plan.
- Freeze new schedulers, ledgers, dashboards, memories, agent frameworks, and
  controller features outside a demonstrated production blocker.
- Convert the whole-system scenario above into executable, synthetic
  conformance fixtures.
- Define the minimum company package and identity mapping without choosing an
  implementation.

### Phase 1 — disposable upstream bake-off

- Pin and inspect a remediated Paperclip release; inventory every advisory,
  patch, reachable path, dependency, default credential flow, and company
  isolation boundary.
- Run Paperclip in a network-restricted disposable environment.
- Evaluate Conductor, Dapr, Temporal, and Restate/DBOS under the same fault and
  duplicate-effect fixtures.
- Compare the mutually exclusive Paperclip, Fusion, and GitHub/CAS authority
  compositions, including package round-trip and clean removal.
- Evaluate GitHub Pro/rules/Actions/`gh-aw` as the software department.
- Record the explicit custom components each candidate retires.

### Phase 2 — choose one composition

- Select one company/work owner and one workflow engine.
- Keep `agent-platform` as schemas, policy, adapters, receipts, conformance, and
  migration tooling—not a competing product UI or workflow engine.
- Migrate one GovCon vertical slice and delete its replaced custom orchestration.
- Do not migrate another company until recovery, teardown, cost, and operator
  attention targets pass.

### Phase 3 — restore operator leverage

- Connect the attention queue, morning brief, meeting-to-artifact pipeline, and
  mobile surface as projections over the chosen company/work authority.
- Add proactive sensors that may propose/admit bounded work but cannot silently
  alter policy, budgets, or send externally.
- Measure whether the system reduces prompting and operator minutes.

### Phase 4 — governed genetic evolution

- Introduce skill/prompt/model/workflow candidate tournaments only after the
  fixed/held-out eval and rollback path is proven.
- Promote through staged rollout; preserve losers and negative evidence.
- Expand to news/intelligence, idea factory, software products, and bounded
  market research as separate company packages.

## Explicit non-goals

- no wholesale OpenClaw restoration;
- no new orchestration engine;
- no permanent Kubernetes until an independently justified workload requires it;
- no single agent framework as the company authority;
- no semantic memory as policy or work truth;
- no unrestricted self-editing or self-approval;
- no autonomous trading or unapproved external outreach;
- no duplicated scheduler, queue, ledger, task identity, approval, or terminal
  state;
- no architecture chosen from a README demo without fault, security, cost, and
  teardown evidence.

## Final position

The ideal platform is a **declarative autonomous-company operating system with a
governed genetic workforce**. It is broader than the current software factory
and narrower than a bespoke replacement for every open-source component.

The current hypothesis to falsify is:

- **Paperclip** for company, goals, org, budgets, work, approvals, and operator
  attention—only after security and authority convergence pass;
- **Conductor OSS** for general durable declarative process execution, challenged
  by Dapr, Temporal, and Restate/DBOS under faults;
- **GitHub Pro + Actions/agentic workflows** for the software department;
- **Hermes, Codex, Claude, OpenHands, Pi, Jules, and scripts** as interchangeable
  workers;
- **Git/object storage/product databases** as canonical artifacts and knowledge;
- **Promptfoo/Inspect + DSPy/GEPA** for governed evolution;
- **OpenTelemetry plus low-cost managed infrastructure** for commodity services;
- **a very small owned contract/reconciliation layer** for the invariants that
  no upstream combination safely owns.

That composition honors the original intent and the hardest historical lesson:
adopt maintained responsibility planes, integrate through native seams, and
build only the missing contracts. The first task is now to falsify this
hypothesis with one whole-company vertical slice—not to continue expanding the
current controller.
