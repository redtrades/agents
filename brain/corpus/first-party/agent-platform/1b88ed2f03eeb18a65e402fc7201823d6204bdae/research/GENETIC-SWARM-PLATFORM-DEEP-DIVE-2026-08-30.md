# Historical intent reconstruction: the genetic swarm platform

**Date:** 2026-08-30  
**Scope:** local first-party repositories, Git history, archived OpenClaw trees, migration records, and execution evidence  
**Status:** research evidence, not governing architecture and not an implementation authorization

## Executive conclusion

The system was never intended to be merely an issue-to-merge controller. The
repeated intent across the OpenClaw, agent-workspace, agent-mesh, and current
agent-platform generations was a **system that builds and improves systems**:

1. a declarative, provider-neutral population of agent roles;
2. replaceable execution bodies and model brains;
3. durable authority, knowledge, evidence, and work state outside any model;
4. reusable project or company blueprints that instantiate agents, workflows,
   tools, data policy, budgets, evaluations, schedules, and approval boundaries;
5. an autonomous improvement loop in which proposed mutations compete under
   deterministic tests, held-out evaluations, independent challenge, cost and
   safety constraints, and only then become inherited defaults; and
6. an attention-oriented command center through which one person directs
   outcomes and exceptions rather than manually operating queues.

This interpretation is not retrospective invention. The April OpenClaw intent
explicitly described an “agnostic, genetic harness,” a declarative Git-hosted
Mind, interchangeable harness Body, replaceable model Brain, baseline roles plus
on-demand and ephemeral agents, GitOps reconciliation, and config-swap failover
([archived `INTENT.md`, lines 76-184](</Users/man/Library/Mobile Documents/com~apple~CloudDocs/09-Archive/OpenClaw-System-History/openclaw-v1-1534commits-2026-04-05-to-05-23/INTENT.md>)). The May manifesto restated that model and added an explicit
adopt-upstream-first rule after documenting that eleven PRs of parallel scripts
had failed to integrate with OpenClaw, Hermes, or Symphony
([`V3-MANIFESTO-AND-LESSONS-2026-05-22.md`, lines 48-109](</Users/man/Library/Mobile Documents/com~apple~CloudDocs/09-Archive/OpenClaw-System-History/openclaw-v1-1534commits-2026-04-05-to-05-23/V3-MANIFESTO-AND-LESSONS-2026-05-22.md>)).

The historical diagnosis is therefore:

- The vision was coherent at the layer level.
- Delivery repeatedly collapsed the whole into whichever subsystem was being
  repaired: memory, a runtime, local inference, handoffs, gates, or claims.
- Agents then built parallel substitutes around that subsystem and called the
  substitute the platform.
- “Self-improvement” was often implemented as mutable memory, skills, scripts,
  or schedules without a stable genome, fitness test, lineage receipt, or
  promotion boundary. That is a poisoning mechanism, not genetic improvement.
- The current transactional spine is a necessary immune system, but it is not
  the organism and should not be allowed to consume the product vision.

## Method and evidence boundary

This pass treated archived `AGENTS.md`, `CLAUDE.md`, manifests, memories, and
handoffs as historical data rather than live instructions. It used:

- local repository Git objects and logs for `agent-platform`, `agent-mesh`,
  `agent-configs`, `agent-workspace`, and `govcon-factory`;
- the preserved OpenClaw v1/v2/v3 snapshots under
  `OpenClaw-System-History`;
- the curated `RepoVault-Consolidated` recovery tree;
- current migration digests and the full agent-repository audit; and
- runtime evidence only to distinguish implemented behavior from plans.

No secret-bearing OpenClaw configuration backup was opened. Paths that may
contain credentials are named only as quarantined archive zones. No external
platform comparison is attempted here; that belongs to the parallel current-
platform research lane.

## The intent model, from first principles

### 1. The product is an operating system for agent work

The April canonical north star was a personal force multiplier first and a
product path second: convert research into durable knowledge, code intent into
shipped software, meetings into artifacts, and operator attention into leverage
([`INTENT.md`, lines 76-99](</Users/man/Library/Mobile Documents/com~apple~CloudDocs/09-Archive/OpenClaw-System-History/openclaw-v1-1534commits-2026-04-05-to-05-23/INTENT.md>)). It was not limited to software development. Research, coding,
and swarm improvement were the first three jobs, in that order.

The May synthesis broadened the practical substrate flow: ingest a URL or idea
from any surface, research it, structure and cross-link it, feed a morning brief,
learn from reactions, and use local, subscribed, free-tier, or paid models in
that preference order. The same document placed agent work behind a router that
translated operator outcomes into GitHub/Symphony work and returned briefings,
not line-review burden ([`V3-MANIFESTO-AND-LESSONS-2026-05-22.md`, lines 28-91](</Users/man/Library/Mobile Documents/com~apple~CloudDocs/09-Archive/OpenClaw-System-History/openclaw-v1-1534commits-2026-04-05-to-05-23/V3-MANIFESTO-AND-LESSONS-2026-05-22.md>)).

The current master plan preserves the same generalized target: “one person can
direct a continuously operating, provider-neutral agent workforce” that produces
software **and business artifacts**, survives provider and machine failure, and
requires the operator for outcomes, policy, and exceptional effects rather than
routine queue movement ([`docs/MASTER-PLAN.md`, North star and Dogfood contract](/Users/man/agent-platform/docs/MASTER-PLAN.md)).

### 2. Mind, Body, and Brain are separate replacement seams

The strongest recurring architecture is:

```text
Mind (versioned declaration)
  intent, roles, skills, workflow contracts, policies, memory, evaluations
                         │
                         ▼
Body (replaceable harness/runtime)
  OpenClaw, Hermes, Codex, Claude, Gemini, Jules, Buzz/ACP, local runner
                         │
                         ▼
Brain (replaceable model route)
  frontier subscriptions, hosted free tiers, paid APIs, local models
```

The archived intent required the **same role manifest** to bootstrap as any
compatible Body × Brain pairing and required failover by configuration rather
than code edits ([`INTENT.md`, lines 128-180 and 490-503](</Users/man/Library/Mobile Documents/com~apple~CloudDocs/09-Archive/OpenClaw-System-History/openclaw-v1-1534commits-2026-04-05-to-05-23/INTENT.md>)). This is the durable meaning of “genetic” in the old record:
the operational genome is declarative and portable; a model or harness is one
expression environment, not the identity of the agent.

### 3. Baseline roles are reusable blueprints, not permanent processes

The historical topology evolved from seventeen always-on agents to five baseline
roles—Prime, Forge, Scout, Sentinel, Operator—plus on-demand specialist
blueprints and ephemeral cloud workers. The archive explicitly says specialists
terminate on task completion, while GitHub and asynchronous messages coordinate
them ([`INTENT.md`, lines 142-184](</Users/man/Library/Mobile Documents/com~apple~CloudDocs/09-Archive/OpenClaw-System-History/openclaw-v1-1534commits-2026-04-05-to-05-23/INTENT.md>)).

That should be interpreted as a **role library and deployment policy**, not as a
requirement to keep five bots running. A project may instantiate only the roles
its workflow needs. The names are useful defaults, not the platform’s ontology.

### 4. The factory has two coupled loops

The record implies two distinct loops that later implementations repeatedly
mixed together:

```text
Production loop
outcome -> admitted work -> execution -> verification -> promotion -> receipt

Evolution loop
observe -> propose mutation -> isolated experiment -> fitness evaluation
        -> independent challenge -> select/reject -> versioned inheritance
```

The first loop builds projects and companies. The second improves the agents,
skills, prompts, models, routing, policies, tests, and workflow blueprints that
run the first loop.

The old self-improvement note had the seed of this loop—observe recurring
friction, detect a pattern, propose a fix, document it, and verify the next
occurrence—but allowed high-confidence changes to be applied directly and
described the loop as a cognitive discipline rather than an enforceable system
([`RepoVault-Consolidated/memory-recovered/SELF_IMPROVING.md`](</Users/man/Library/Mobile Documents/com~apple~CloudDocs/09-Archive/RepoVault-Consolidated/memory-recovered/SELF_IMPROVING.md>)). The current master plan correctly tightens it to an isolated candidate,
fixed evaluation, independent challenge, policy promotion, and retained failure
receipts ([`docs/MASTER-PLAN.md`, Autonomous improvement loop](/Users/man/agent-platform/docs/MASTER-PLAN.md)).

### 5. A precise genetic model

The historical “genetic swarm” becomes technically meaningful when expressed as:

| Genetic concept | Platform equivalent |
| --- | --- |
| Genome | Versioned role, workflow, prompt, skill, tool, policy, routing, model, budget, and evaluation declarations |
| Phenotype | Observed behavior of an instantiated agent/swarm on a task and environment |
| Environment | A project/company blueprint plus its repositories, data, users, constraints, and workflows |
| Mutation | A bounded proposed change to one genome component |
| Fitness | Deterministic correctness, domain quality, safety, cost, latency, recovery, and operator-attention measures |
| Selection | Exact-candidate independent review plus effect-policy decision |
| Inheritance | Reviewed version bump promoted into a reusable blueprint |
| Lineage | Subject hashes, parent version, experiment receipts, evaluator identity, and decision rationale |
| Diversity | Multiple providers/harnesses or strategies tested without giving them shared promotion authority |
| Extinction | Rejection or retirement with the evidence retained so the same failure is not rediscovered |

Without lineage, fixed fitness tests, and controlled inheritance, “self-
improving” agents merely rewrite their own instructions. That is exactly the
kind of unbounded mutation that made later sessions inherit false claims,
conflicting rules, and broken runtime wiring.

## Declarative project and swarm provisioning

The historical record contained most of the ingredients but never assembled
them into one stable project module. A Terraform-like project declaration was
the implicit target:

```yaml
project:
  identity: govcon-opportunity-factory
  outcomes: [market-report, opportunity-packet, outreach, proposal-draft]
  authority: github

swarm:
  roles: [lead, research, analyst, reviewer, operator]
  scaling: {baseline: 1, on_demand: 4, max_parallel: 4}
  harnesses: [codex, hermes, local]
  model_policy: local_then_subscription_then_free_then_paid

workflows:
  - id: opportunity-intake
    trigger: schedule_or_manual
    stages: [discover, qualify, enrich, challenge, publish]
    effects: auto_write_reversible

controls:
  capabilities: least_privilege
  data_policy: provider_and_sensitivity_routing
  budgets: {monthly_usd: 100, operator_minutes_per_week: 30}
  evaluations: [source_grounding, completeness, hallucination, cost]
  promotion: exact_candidate_independent_review

deployment:
  substrates: [local_macos, github_hosted, optional_self_hosted]
  secrets: opaque_references
  observability: open_receipts
```

The archive already had declarative role manifests, a bootstrap schema, issue
handoff schema, policy files, GitOps reconciliation, an OCI/Nix ambition, and
project-board state. The OpenClaw mining digest records
`bootstrap.declarative.yaml`, JSON Schema validation, “edit the manifest, not
the runner,” task packet fields, and a config-swap composability law
([`agent-mesh/research/mine-v1-digest.md`, lines 28-51](/Users/man/agent-mesh/research/mine-v1-digest.md)). What was missing was a single stable **project module contract** connecting those
declarations to lifecycle authority and runtime adapters.

Terraform is a useful mental model for declaration, planning, drift detection,
and reconciliation, but the platform also needs workflow semantics: long-lived
tasks, human waits, evidence, retries, events, and business outputs. The desired
artifact is therefore closer to “Terraform modules plus workflow definitions
plus policy and evaluation packs” than infrastructure-as-code alone.

## Repository chronology and capability inventory

### March–April: RepoVault and early OpenClaw

`RepoVault-Consolidated` preserves the early personal-agent substrate:
identities, agent team manifests, heartbeats, memory systems, proactive
operations, Git workflow, second-brain architecture, and self-learning designs.
It establishes the earliest durable themes:

- persistent identity and role separation;
- proactive heartbeats and scheduled work;
- a Git/Markdown second brain;
- reusable skills and workflows;
- self-reflection and lesson promotion; and
- a control surface spanning chat, browser, and personal knowledge.

The value is intent and pattern evidence. It is not safe as a runtime source:
the tree also contains obsolete instructions, duplicated overlays, and a
separate secret-bearing archive zone.

### April 5–May 23: OpenClaw v1, 1,534-commit snapshot

This is the richest statement of the whole vision. It included:

- canonical `INTENT.md`, laws, bootstrap, role manifests, and many ledgers;
- a five-agent baseline plus specialist blueprints;
- Slack and GitHub work surfaces;
- SwarmClaw autonomy/attention/explainability UI plans;
- research intake, morning brief, meeting artifact, and recommendation loops;
- multiple model/harness/node routes;
- GitOps, sandboxing, observability, memory, and cross-vendor handoff plans;
- CI, issue dispatch, drift, schema, secret, and SDLC workflows; and
- explicit measurable MVP and pivot criteria.

Evidence quality is mixed. Some files describe shipped PRs and scripts, but many
end-state claims were declarative or contradicted by runtime failures. The May
manifesto itself records a status broadcaster claiming OpenClaw was healthy
while its daemon was down, a Hermes authentication failure masked by a fallback,
duplicate session dispatch, and incomplete transcript backup
([`V3-MANIFESTO-AND-LESSONS-2026-05-22.md`, lines 95-147](</Users/man/Library/Mobile Documents/com~apple~CloudDocs/09-Archive/OpenClaw-System-History/openclaw-v1-1534commits-2026-04-05-to-05-23/V3-MANIFESTO-AND-LESSONS-2026-05-22.md>)).

### May: OpenClaw v2, 90-commit snapshot

The v2 generation attempted a clean substrate with seventeen service units.
The mined inventory contains intake, daily brief, aligned-news, task tracking,
trio review, deterministic validation, autofix, knowledge bridge, Mem0, RAG,
Slack bot, Hermes skill factory, routing, rating loop, status, and SOTA scanner.
It also describes an intended integrated path from Slack intake through GitHub
work, guarded PR flow, memory, briefing, feedback, and GEPA tuning
([`agent-mesh/research/mine-v2v3-digest.md`, lines 88-139](/Users/man/agent-mesh/research/mine-v2v3-digest.md)).

However, that same inventory distinguishes implemented services from stubs and
specifications. The earlier manifesto is more candid: the service accumulation
was largely parallel Python and scheduling rather than native runtime wiring.
Therefore v2 proves the desired **capability map**, not a working integrated
factory.

### May: OpenClaw v3, one-commit clean-room scaffold

The v3 scaffold narrowed the problem to a LangGraph courtroom:
receive, plan, fan out, collect, one bounded debate, independent judge,
synthesis, and policy-gated landing. It persisted per-case artifacts and enforced
that a generator family could not judge itself. This is an important evaluation
pattern, but it reduced the broader personal/company operating system to one
multi-agent reasoning graph ([`agent-mesh/research/mine-v2v3-digest.md`, lines 143-195](/Users/man/agent-mesh/research/mine-v2v3-digest.md)).

### August 15: `agent-workspace`

The initial commit `5e2b97f4ca855fb12ccdaaff8c30029c45f22ee3`
implemented a plain-Git coordination workspace with five mechanically enforced
rules, task claims, completion evidence, stale-claim detection, and heartbeat
self-tests. This was a real, small control mechanism rather than a vision doc.
Its weakness was equally explicit: identity was a convention, claims relied on
Git conflicts, hooks were inert until each clone bootstrapped them, and it was
not adversarially safe ([`CONSTITUTION.md`](/Users/man/agent-workspace/CONSTITUTION.md),
[`README.md`](/Users/man/agent-workspace/README.md)).

### August 24: `agent-configs`

Initial commit `87ab4bd6213dba51a5dbaf25d75b0663519600ff`
collected universal rules, hooks, prompts, role boundaries, verifier guidance,
and skills. Its durable contribution is the **genome library**: reusable
behavioral components independent of a product repository. Its failure mode was
activation ambiguity and instruction sprawl—presence in a directory did not
prove that Codex, Claude, Hermes, Buzz, or another runtime loaded it. Later
consolidation logs themselves contain multiple corrections of “measured” claims,
showing why activation receipts are required.

### August 26: `agent-mesh`

Initial commit `618b9c8c6e73964d0b30131408ea65175971d5c5`
defined “one brain, many harnesses.” The next commit added portable `.agent/`
assets, Hermes bots, pipelines, evaluations, command center, and vault tooling.
The repository’s map separates portable behavior, Hermes deployment, runnable
pipelines, evaluation fixtures, research, UI, and knowledge taxonomy
([`README.md`](/Users/man/agent-mesh/README.md), [`DECISIONS.md`](/Users/man/agent-mesh/DECISIONS.md)).

This was the primary bridge from retired OpenClaw to Hermes. It intentionally
kept OpenClaw as a sanitized historical source, rebuilt Prime/Scout/Sentinel/
Morning Brief as Hermes profiles, retained the portable layer outside Hermes,
and used a static command center over existing stores. It adopted Hermes because
profiles, skills, cron, delegation, model/provider routing, bots, and ACP already
provided a usable Body. It did **not** establish Hermes as task, claim, review,
promotion, project, or company authority. The August recovery plan stated that
Hermes/OpenClaw could later serve as persistent gateways and Buzz as a
collaboration surface, but neither replaced Git/ledger authority
([`session-next-steps.md`, lines 70-91](</Users/man/Library/Mobile Documents/com~apple~CloudDocs/09-Archive/OpenClaw-System-History/00-inbox-agent-notes-2026-08-16/session-next-steps.md>)).

### August 22 onward: `govcon-factory`

Initial commit `78b34b0cd894c388693fae14670259ace51bd285`
began with a product plan and deliverable SOP, then added deterministic gates,
data-source recipes, outreach templates, and production-stage skills. This is
the most important product proof because it demonstrates what “different
projects or companies” actually means: domain-specific sources, schemas,
evaluation gates, workflows, offers, outputs, and commercial constraints should
live in a product factory that consumes the agent platform rather than being
hard-coded into the platform.

### August 28 onward: `agent-platform`

Initial commit `c517423` established the authority baseline. The same day added
provider-neutral lifecycle contracts (`cdd31d5`), attribution (`c9e7997`), a
self-hosted platform comparison (`c62680b`), and the master plan (`a744591`).
This repository finally turned recurring failures into exact contracts for
claims, candidates, evidence, independent review, promotion, and teardown.

Its strong contribution is the transactional spine and immune system. Its risk
is scope inversion: treating the controller and its contracts as the entire
factory instead of the authority layer that a broader maintained platform,
runtime, UI, and product ecosystem should obey.

### `agent-reports`, `agent-tools`, Buzz, and runtime homes

- `agent-reports` is a large evidence corpus: benchmarks, configuration
  diagnostics, installation traces, reviews, and incident records. It is not a
  runtime or design authority.
- `agent-tools` is a small collection of session receipts, not a task ledger.
- Buzz supplies collaboration, messaging, ACP, remote agents, and runtime
  surfaces. It does not by itself provide the user’s exact GitHub task and
  promotion authority.
- Hermes supplies a capable agent Body—profiles, tools, skills, cron,
  delegation, models, providers, and UI—but not the full cross-project factory.
- Local model and FreeLLMAPI work supplies economical Brain routes and empirical
  performance evidence. Model optimization is a platform service, not the
  platform’s purpose.

The consolidated audit reaches the same repository-role separation: mesh is
research/harness, configs is behavioral/config evidence, workspace is execution
artifacts, reports is observed execution, and platform is current authority
([`AGENT-PLATFORM-FULL-AUDIT.md`, lines 14-119](/Users/man/agent-reports/agent-configs-consolidation/AGENT-PLATFORM-FULL-AUDIT.md)).

## OpenClaw-to-Hermes migration: what it did and did not mean

The migration was not a rejection of the OpenClaw vision. It was an attempt to
stop rebuilding commodity runtime behavior.

### What Hermes plausibly replaced

- persistent profile/bot identity;
- per-profile memory and configuration;
- runtime-native skills;
- scheduling and cron delivery;
- tool execution and delegation;
- provider/model routing and local inference integration;
- a user-facing chat/UI surface; and
- ACP integration used by Buzz.

### What remained outside Hermes

- canonical project/company intent and dependency graph;
- atomic ownership and stale-worker fencing;
- isolated source candidate identity;
- deterministic product/domain gates;
- independently authenticated review and promotion;
- immutable cross-system receipts;
- cross-project effect policy and destructive-action authority;
- infrastructure/project blueprint reconciliation; and
- selection and inheritance of self-improvement mutations.

### Why the migration still fragmented

The portable `.agent/` layer, Hermes bot definitions, Buzz harness, SSSF/Pi
workflow runners, FreeLLMAPI, GitHub Issues, task ledgers, command center, and
product pipelines were all valid pieces but lacked one admitted lifecycle and
one declarative project module. A later installation report explicitly observed
that SSSF/fusion called Pi directly, Hermes/Buzz followed Hermes configuration,
and no dedicated integration existed between them
([`agent-reports/factory-install/USING-EVERYTHING.md`, lines 61-79](/Users/man/agent-reports/factory-install/USING-EVERYTHING.md)).

Hermes was therefore the easier **agent runtime**, not the easier implementation
of the entire system-that-builds-systems.

## Failure and poisoning diagnosis

### 1. Instruction poisoning

Old runtime instructions remained discoverable beside new rebuild contracts.
The April handoff warned that legacy `CLAUDE.md`, `AGENTS.md`, Make targets,
configuration chains, and CI guards directly contradicted the new build
([`DISPATCH-HANDOFF-2026-04-19.md`, lines 8-38](</Users/man/Library/Mobile Documents/com~apple~CloudDocs/09-Archive/OpenClaw-System-History/loose-root-files-2026-08-15/DISPATCH-HANDOFF-2026-04-19.md>)). Later migrations repeatedly reintroduced the same class of ambiguity through
multiple rule roots and config projections.

**Root cause:** instructions were copied as content without loader provenance,
version, scope, or activation proof.

### 2. State poisoning

Status prose, board projections, chat summaries, and memory entries were treated
as authority. The status broadcaster and Hermes fallback incidents show that a
plausible status artifact could disagree with the running system.

**Root cause:** discovered, loaded, activated, healthy, and behaviorally verified
were collapsed into one “configured/working” claim.

### 3. Parallel-substrate poisoning

New agents frequently built scripts or ledgers around a missing feature rather
than integrating the runtime’s native capability. The May manifesto names this
as the primary architectural mistake and explicitly records violation of the
adopt-upstream-first rule.

**Root cause:** the smallest locally visible gap became the unit of architecture;
no capability map or mandatory upstream seam evaluation preceded implementation.

### 4. Self-improvement poisoning

Learnings, prompts, skills, memory, and routing could be changed based on repeated
observations or user corrections, but a shared, immutable fitness corpus and
candidate promotion protocol were absent or inconsistently enforced.

**Root cause:** observation and inheritance were in the same authority domain.
The system could learn a false lesson and make that lesson part of its own future
judge.

### 5. Coordination poisoning

Duplicate spawns, concurrent configuration writers, stale claims, unfinished
background jobs, and model/context failure generated overlapping attempts whose
state was reconciled socially after the fact.

**Root cause:** communication was mistaken for ownership. Git conflicts, Slack
threads, session lists, and task boards are useful projections but insufficient
fences.

### 6. Verification poisoning

Reports frequently upgraded planned, installed, configured, or narrowly smoke-
tested behavior into “working.” Later independent passes repeatedly corrected
model identity, runtime activation, exact source, and review claims.

**Root cause:** the claimant authored the interpretation, and evidence was not
always bound to the same immutable candidate being promoted.

### 7. Overengineering as a recovery response

Every failure added another ledger, script, daemon, role, rule, service, or
dashboard. The April and May records both show fresh-rebuild attempts designed
to delete this accumulation. The August cold-start plan responded by deferring
Temporal, Kubernetes, vector memory, A2A, broad MCP, and autonomous spawning
until one repeatable loop and measurements existed
([`session-next-steps.md`, lines 18-54](</Users/man/Library/Mobile Documents/com~apple~CloudDocs/09-Archive/OpenClaw-System-History/00-inbox-agent-notes-2026-08-16/session-next-steps.md>)).

**Root cause:** mechanisms were accumulated to compensate for untrusted state,
instead of first reducing authorities and proving one end-to-end product slice.

## Contradictions that must be reconciled, not silently chosen

| Question | Historical position A | Historical position B | Reconciliation |
| --- | --- | --- | --- |
| Primary purpose | Personal force multiplier first | Autonomous software/business factory | The platform serves both through project modules; first proof should be one high-value product workflow, while personal attention is an operator surface, not a competing platform |
| Promotion | “Agents draft; Mike reviews” | Eligible reversible work promotes automatically | Operator sets policy and reviews exceptions; exact eligible routine changes can auto-promote after independent gates |
| Permissions | Maximal agent-first permission | Least privilege and explicit capabilities | High functional autonomy inside an admitted capability envelope; no ambient authority outside it |
| Topology | Baseline five persistent roles | Ephemeral bounded workers | Five are reference role templates; instantiate only needed roles and scale on demand |
| Runtime | Fresh OpenClaw with zero custom glue | Hermes as default easier runtime | Runtime is replaceable; choose one maintained default Body, retain adapters, never make it lifecycle authority |
| Control plane | SwarmClaw PWA | GitHub Issues and receipts | GitHub/Git objects remain authority; UI is a projection and action surface |
| Self-improvement | Cognitive reflection and direct high-confidence fixes | Fixed evals and independent promotion | All durable mutations use the governed evolution loop; reflection only proposes |
| Infrastructure | Nix, OCI, K3s/Flux, OpenShell from the start | Thin repo-first loop before engines | Declarative host/project blueprints remain a target; deploy infrastructure incrementally when a product slice requires it |
| Memory | Rich semantic memory and recommendation engine | Git/file truth and no vector memory initially | Semantic memory is a derived retrieval service; reviewed versioned artifacts and receipts remain authority |

## What was implemented versus proposed

### Observed implementation

- OpenClaw repositories contain substantial code, workflows, manifests, skills,
  ledgers, UI scaffolds, and service implementations—not merely plans.
- `agent-workspace` has executable claim/completion/heartbeat scripts and tests.
- `agent-configs` has real hooks, rule sets, skills, and adoption records.
- `agent-mesh` has runnable pipelines, eval fixtures, Hermes deployment files,
  command-center code, and extensive live model/runtime evidence.
- Hermes, Buzz ACP, local OMLX/llama.cpp routes, and FreeLLMAPI were exercised in
  real runtime diagnostics.
- `govcon-factory` has a real domain pipeline, gates, data recipes, templates,
  and product artifacts.
- `agent-platform` has implemented controller contracts and adversarial fixtures
  around claims, review, evidence, effects, and projection.

### Proposed, partial, or contradicted

- A single command could not reliably stand up the entire swarm from a project
  declaration.
- SwarmClaw was scaffolded and repeatedly deferred; it was not a verified full
  operational command center.
- The morning brief, intake, rating, recommendation, and GEPA loop existed in
  pieces, but the record contradicts unattended end-to-end health.
- Cross-vendor handoff automation was defined but explicitly out of the first
  MVP ([`INTENT.md`, lines 507-528](</Users/man/Library/Mobile Documents/com~apple~CloudDocs/09-Archive/OpenClaw-System-History/openclaw-v1-1534commits-2026-04-05-to-05-23/INTENT.md>)).
- Nix/OCI/K3s/Flux/OpenShell described a desired reproducible deployment plane,
  not a consistently verified estate.
- Many v2 “services” were specs or stubs and did not share one lifecycle.
- The full genetic selection loop was never implemented across code, prompts,
  skills, memory, model routing, and workflow blueprints.
- No evidence found in this pass proves a reusable project/company declaration
  could instantiate, operate, evaluate, evolve, and tear down a complete swarm.

## Keep / Adapt / Defer / Reject

### Keep

- The system-that-builds-systems north star.
- Mind/Body/Brain separation and provider neutrality.
- GitHub/Git as intent and immutable candidate authority.
- Exact receipts, deterministic gates, independent challenge, and effect policy.
- Project/product repositories separated from platform contracts.
- On-demand role blueprints and ephemeral workers.
- Local/subscription/free-tier/paid routing order with measured economics.
- Operator attention surface, autonomy dial, exception queue, and explainability.
- Proactive research and drift detection that opens bounded work.
- Failed experiments and superseded lessons as durable negative evidence.

### Adapt

- Prime/Forge/Scout/Sentinel/Operator into a default role pack rather than fixed
  daemon topology.
- SwarmClaw into a projection over authoritative systems, not a new ledger.
- OpenClaw/Hermes skills into versioned genome packages with loader receipts.
- Heartbeats into health/event sensors that propose work rather than mutate
  globally.
- Semantic memory into a derived index with source and freshness metadata.
- Nix/OCI/GitOps assets into optional deployment modules driven by project needs.
- The recommendation/rating loop into one fitness signal among several, never a
  sole promotion criterion.
- Trio review/MoA into risk-triggered independent challenge, not mandatory
  debate for every task.

### Defer until a measured trigger

- Permanent Kubernetes or distributed workflow infrastructure.
- A large custom command-center application.
- Voice and wearable interaction.
- Broad shared vector memory.
- Automatic cross-vendor continuity before durable checkpoint recovery works.
- Unbounded autonomous agent spawning.
- Multi-company tenancy before one project module proves isolation and teardown.
- Self-modification of platform code without a complete fixed evaluation and
  rollback suite.

### Reject

- Wholesale restoration of OpenClaw runtime/configuration archives.
- A new custom implementation for every commodity runtime capability.
- Parallel queues, ledgers, memories, schedulers, or promotion authorities.
- Treating chat, dashboards, semantic recall, or issue comments as a mutex.
- Direct mutation of canonical prompts/skills/policy from reflection or ratings.
- One model or harness judging and promoting its own mutations.
- Static claims such as “installed,” “configured,” or “present” standing in for
  behavioral verification.
- Always-on role proliferation without workload evidence.
- Building infrastructure layers before a project slice requires them.

## Historical requirements for the whole platform

Any future architecture—adopted, extended, or custom—must be evaluated against
the **whole**, not only the SDLC controller:

1. **Project/company modules:** declarative outcomes, workflows, roles,
   capabilities, data rules, budgets, triggers, outputs, evaluations, and
   teardown.
2. **Agent genome registry:** versioned role, prompt, skill, model, tool,
   workflow, policy, and evaluation components with lineage.
3. **Runtime adapter plane:** at least two harnesses and two providers per
   critical role without changing task/evidence contracts.
4. **Lifecycle authority:** admission, leases/fences, checkpoints, candidate
   identity, review, promotion, and cleanup.
5. **Workflow plane:** events, schedules, waits, retries, joins, cancellations,
   human gates, and business artifacts.
6. **Evolution plane:** observation, candidate mutation, isolated tournament,
   held-out fitness, independent selection, safe inheritance, rollback.
7. **Knowledge plane:** provenance-aware retrieval, canonical reviewed
   knowledge, derived semantic indexes, correction and expiry.
8. **Economics plane:** model/harness/substrate routing, quota, cost, latency,
   cache, GPU/host capacity, and operator minutes.
9. **Safety plane:** data sensitivity, least privilege, secrets by opaque
   reference, sandbox policy, destructive-action boundary.
10. **Operator plane:** attention triage, explainability, approvals/exceptions,
    outcome previews, health, evidence, and mobile access.
11. **Product plane:** domain factories such as GovCon consume stable contracts
    and own their sources, schemas, evaluations, outputs, and commercial rules.
12. **Proactivity:** sensors can discover drift, cost anomalies, stale work,
    missing knowledge, market signals, and improvement opportunities, then open
    bounded tasks without silently changing authority.

## Current-source synthesis from the parallel platform lane

This section is deliberately separated from the historical findings above. It
records the parallel current-platform research result supplied on 2026-08-30;
this historical lane did not independently clone or execute these candidates.
The finding must therefore be treated as a **candidate-selection input**, not an
adoption decision or a behavioral verification receipt.

### Paperclip plus `paperclipai/companies` is the strongest documented-fit hypothesis found

The current Paperclip design maps unusually closely to the recovered whole:

- company is a first-class boundary rather than merely a repository;
- goals, organizational structure, agents, budgets, heartbeats, work, and
  governance are modeled as one operating system;
- agent runtimes are adapters rather than the identity or authority of the
  company;
- multiple companies can be represented without hard-coding one product domain;
  and
- the companion [`paperclipai/companies`](https://github.com/paperclipai/companies)
  repository makes company configurations/templates portable—the closest
  current analogue to the desired Terraform-like “stand up this company/swarm”
  declaration.

Primary current references: [Paperclip README](https://github.com/paperclipai/paperclip/blob/master/README.md),
[company specification](https://github.com/paperclipai/paperclip/blob/master/docs/companies/companies-spec.md),
[adapter model](https://github.com/paperclipai/paperclip/blob/master/docs/adapters/overview.md),
and [`paperclipai/companies`](https://github.com/paperclipai/companies).

This changes the historical August 29 classification. That earlier local report
graded Paperclip from documentation only, called it a command center and budget
governor rather than a PR lifecycle, and explicitly recorded that source had not
been read ([`swarm-platform-research-2026-08-28.md`, lines 187-201 and 894-902](/Users/man/agent-workspace/knowledge/swarm-platform-research-2026-08-28.md)). The older conclusion remains useful for one boundary: Paperclip's own
positioning did not make it the exact-candidate code-review and merge authority.
But that is no longer a reason to dismiss it as the **whole-system substrate**.
It may be the company/goal/budget/agent/work/operator layer under which the
transactional SDLC controls run as extensions or governed workflows.

### Strong documented fit does not mean current admissibility

Two especially relevant published security advisories materially gate evaluation:

- [`GHSA-x8hx-rhr2-9rf7`](https://github.com/paperclipai/paperclip/security/advisories/GHSA-x8hx-rhr2-9rf7)
- [`GHSA-gqqj-85qm-8qhf`](https://github.com/paperclipai/paperclip/security/advisories/GHSA-gqqj-85qm-8qhf)

They are not the complete security corpus. The current
[Paperclip advisory register](https://github.com/paperclipai/paperclip/security/advisories)
contains twelve advisories, including additional command-injection,
cross-company authorization/credential, IDOR, XSS, and unauthenticated-RCE
classes. Evaluation must inventory every advisory, affected and patched version,
fix commit, reachable path, and relevant transitive dependency before selecting
an executable revision.

Therefore the correct current status is:

| Claim | Status |
| --- | --- |
| Strongest documented recovered-intent fit hypothesis | Current-source synthesis from the parallel research lane; not behaviorally ranked |
| Safe to install into the live agent estate | **Not established** |
| Approved as canonical platform | **No** |
| Appropriate next evidence step | Pin an exact remediated revision; inspect advisory-affected paths and fixes; run only in a disposable, network-restricted sandbox with synthetic data and no live credentials |
| Eligible for live data or autonomous effects | **No, until security, isolation, authority, and teardown fixtures pass** |

The evaluation question is no longer “Can Paperclip replace the SDLC controller?”
It is:

> Can Paperclip/Companies supply the broad company, goals, budgets, agents,
> adapters, work, and operator experience while `agent-platform` contributes the
> exact authority, evidence, review, effect-policy, and promotion extensions it
> does not natively prove?

That is a hypothesis to test, not permission to combine three authorities.
Paperclip claims tasks, atomic checkout, approvals, schedules, budgets, and
terminal work state; Optio claims reconciliation and an issue-to-merge loop; the
current controller claims admission, leases, and promotion. A production design
may have only one authoritative task identity, lease, approval decision, and
terminal state. The evaluation must prove one of two outcomes:

1. one upstream replaces the current lifecycle authority through an explicitly
   approved architecture decision, while `agent-platform` becomes contracts,
   conformance fixtures, and any demonstrably missing boundary; or
2. the current authority remains, and the upstream can be technically restricted
   to a non-authoritative definition, projection, or worker role with its
   overlapping controllers disabled.

If neither is possible, that composition is rejected regardless of feature fit.

## Account-wide repository poll

The authenticated account inventory found 72 owned repositories: 18 active
first-party repositories, 53 forks, and one archived first-party repository.
The complete categorized inventory is recorded in
[`REDTRADES-REPOSITORY-INVENTORY-2026-08-30.md`](/Users/man/agent-platform/research/REDTRADES-REPOSITORY-INVENTORY-2026-08-30.md).

The inventory changes the interpretation of the history in two ways:

1. OpenClaw, the four current `agent-*` repositories, `govcon-factory`, and the
   trading/news/work products form a coherent first-party lineage: one reusable
   platform was meant to instantiate multiple domain factories.
2. The large fork collection is a prior-art radar—agent frameworks, harnesses,
   skills, memory, evolution, coding runtimes, and infrastructure—not evidence
   that any of those projects was adopted, integrated, or behaviorally active.

The correct use of that estate is to evaluate current upstreams, preserve exact
provenance, and delete overlapping custom substitutes when an admitted upstream
passes the same scenarios. Keeping stale forks as an implicit architecture is
another form of poisoning.

## Current build, buy, and adopt decision brief

The first-principles result is **not** “build from scratch” and it is not
“install one giant project and trust it.” It is to adopt maintained systems for
whole responsibility planes, then keep a narrow owned boundary for the unusual
authority and evolution invariants.

| Plane | Preferred current candidate | Owned delta that remains |
| --- | --- | --- |
| Company/portfolio definition and experience | Paperclip plus `agentcompanies/v1` documented-fit hypothesis, security-gated | Must either own the single lifecycle after an approved replacement decision or be demonstrably non-authoritative |
| Engineering delivery | Optio versus Last Light/Actions evaluation | Must either own the single lifecycle after an approved replacement decision or operate only as a bounded worker/projection |
| Repository automation | GitHub Actions plus GitHub Agentic Workflows (`gh-aw`) | Cross-project authority, resource arbitration, and policies beyond one repository |
| Coding/research workers | Codex, OpenHands, Hermes/local, and native provider CLIs as adapters | Common task, artifact, capability, checkpoint, and cost contract |
| Environment declaration | Dev Containers first; Docker Compose locally; OpenTofu for actual infrastructure | Project-to-environment binding and teardown receipt |
| Evaluation/evolution | Promptfoo plus Inspect AI; bounded AutoResearch/OpenEvolve patterns | Immutable baselines, lineage, independent selection, effect-policy promotion |
| Telemetry | OpenTelemetry contracts and Grafana Cloud Free pilot | Exact task/candidate/decision identifiers and retention policy |

### Why OpenHands, Temporal, and LangGraph are not root platforms

- [OpenHands SDK](https://github.com/OpenHands/software-agent-sdk) is a strong
  coding-agent and sandbox runtime. It does not own companies, portfolios,
  budgets, durable cross-project authority, or promotion.
- [Temporal](https://github.com/temporalio/temporal) provides exceptionally
  durable workflow execution. It does not provide the agent-company, software
  delivery, knowledge, or evolution domain model. Add it only if recovery and
  chaos fixtures show that the selected operational platform cannot meet the
  required waits, retries, cancellation, and resume semantics.
- [LangGraph](https://github.com/langchain-ai/langgraph) is appropriate inside a
  bounded stateful product workflow. The OpenClaw v3 courtroom already proved
  why an agent graph is not the whole factory.

### Why Optio is a department, not the company

[Optio](https://github.com/jonwiggins/optio) is a strong engineering-lifecycle
candidate because it already provides tasks, standalone jobs, persistent agents,
triggers, harness adapters, isolated workspaces, reconciliation, CI feedback,
costs, APIs, and UI. Rebuilding those features to preserve a few custom
invariants is unjustified.

It should not automatically become the root platform because it is centered on
engineering delivery and its Kubernetes/PostgreSQL/Redis deployment is material
operational weight for a one-operator M1 pilot. Paperclip models the missing
company/goal/budget/organization/attention layer. Optio or a lighter Last Light
plus Actions path should compete to become an engineering department adapter.

### GitHub economics and native capabilities

Current official plan evidence supports buying GitHub Pro for private canonical
repositories at **$4/month**. It adds protected branches, required reviewers,
CODEOWNERS/rulesets, 3,000 Actions minutes, and additional Codespaces capacity
([GitHub plans](https://docs.github.com/en/get-started/learning-about-github/githubs-plans),
[pricing](https://github.com/pricing), and
[included usage](https://docs.github.com/en/billing/reference/product-usage-included)).
That is cheaper and stronger than reproducing private-repository governance in
custom code.

Important boundaries remain:

- private-repository merge queues require Enterprise Cloud
  ([merge queue documentation](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-a-merge-queue));
- required environment reviewers for private repositories also require
  Enterprise ([environment documentation](https://docs.github.com/en/actions/reference/workflows-and-actions/deployments-and-environments)); and
- GitHub Pro does not include an AI coding agent. Copilot Pro is a separate
  subscription and remains a bounded one-repository worker, not factory
  authority ([Copilot plans](https://github.com/features/copilot/plans)).

The narrow expected-head promoter and separately identified reviewer therefore
remain useful even after upgrading. They should complement server-side rules,
not emulate every Enterprise feature.

[`gh-aw`](https://github.com/github/gh-aw) is the most consequential overlooked
GitHub-native layer. It compiles versioned Markdown workflows into locked-down
Actions, supports Codex, Claude, Gemini, Copilot, and experimental Pi engines,
is read-only by default, and separates agent reasoning from permissioned safe
outputs. It can replace substantial custom scheduling, repository inspection,
issue triage, review, documentation, CI investigation, and proactive maintenance
code. It is still public preview, so evaluation must pin an exact release and
begin with read-only or staged outputs
([architecture](https://github.github.com/gh-aw/introduction/how-they-work/),
[staged mode](https://github.github.com/gh-aw/reference/staged-mode/), and
[sandboxing](https://github.github.com/gh-aw/reference/sandbox/)).

### Why not self-host GitLab now

GitLab is a credible integrated DevSecOps challenger, but the free self-managed
edition does not bypass the feature gates that matter. Required approvals and
merge trains remain Premium capabilities. Premium is currently $29 per user per
month billed annually, while Duo Agent Platform consumes credits
([GitLab pricing](https://about.gitlab.com/pricing/),
[approvals](https://docs.gitlab.com/user/project/merge_requests/approvals/), and
[merge trains](https://docs.gitlab.com/ci/pipelines/merge_trains/)).

A normal self-managed deployment also makes this factory responsible for GitLab
upgrades, backups, security, availability, storage, and runners. That is a new
product to operate before it proves any unique requirement. GitLab should receive
a time-limited challenger trial only if sovereignty, offline operation, or its
integrated agent flows become an explicit requirement.

### Low-cost services that can remove commodity work

- Grafana Cloud Free can receive OpenTelemetry metrics, logs, and traces instead
  of another custom observability backend.
- Neon Free can host a disposable PostgreSQL adoption proof without operating a
  database.
- Cloudflare Workflows and Durable Objects are a credible low-cost challenger
  for durable waits, timers, retries, and leases, but should be tested as an
  alternative to—not stacked beside—Optio/its database.
- GitHub-hosted runners should execute cheap deterministic and untrusted work;
  current self-hosted runners can handle local Apple-Silicon models and private
  services under explicit GPU/resource ownership.

## Concrete decision experiment before architecture change

No current candidate has earned production adoption. The bake-off below is a
proposed later architecture gate, not a replacement for the currently accepted
delivery sequence. The current critical path first completes terminal
reconciliation, another bounded Gate C proof, clean-host/recovery evidence, and
provider-neutrality evidence. Broad controller expansion should not occur while
those proofs are being completed. After that boundary—or after an explicit
owner-approved revision to the master plan—the next architecture execution step
is a disposable, exact-revision bake-off, not more framework code.

### Three candidates

1. Paperclip as the candidate single lifecycle authority, with Optio evaluated
   only if it can be reduced to a non-authoritative engineering executor.
2. Paperclip as the candidate single lifecycle authority, with Last Light/
   GitHub Actions/`gh-aw` evaluated only as bounded execution mechanisms.
3. The current `agent-platform` lifecycle authority plus GitHub Actions as the
   measured custom baseline, with Paperclip limited to company-package import/UI
   projection only if task checkout, approvals, scheduling, and terminal-state
   ownership can be disabled or bypassed safely.

OpenHands, Codex, and Hermes/local should be worker choices held constant across
the candidates where their adapters permit it.

### Required whole-system scenarios

1. Import a secret-free declarative company/project package in dry-run mode.
2. Instantiate a software team and a GovCon workflow without platform code
   branching on either domain.
3. Turn one outcome into admitted work with a hard budget and capability set.
4. Survive worker termination and resume without duplicate ownership.
5. Produce an exact candidate, deterministic evidence, independent review, and
   expected-head promotion or rejection.
6. Run a scheduled proactive sensor that opens a bounded proposal without
   mutating canonical policy.
7. Run one losing and one winning prompt/skill mutation against fixed and held-
   out evaluations; preserve both lineages and promote only the winner.
8. Export the company/project package without secrets and reconstruct it from a
   clean environment.
9. Demonstrate complete teardown and orphan cleanup.
10. Report model cost, infrastructure cost, operator minutes, recovery time,
    custom code retained, and every external effect.
11. Demonstrate exactly one owner for task identity, lease/fence, approval,
    retry/reconciliation, and terminal state; inject conflicting and stale
    events and prove every non-owner is rejected or projection-only.

### Mandatory falsifiers

- Paperclip is rejected for live adoption if any applicable advisory lacks a
  verified patched revision, advisory/dependency inventory is incomplete,
  company isolation fails, any live credential is inherited, or a worker can
  bypass effect policy.
- Optio is rejected as the engineering substrate if Kubernetes/Redis/PostgreSQL
  operational burden exceeds the measured value it removes or its reconciler
  conflicts with the authority boundary.
- The lighter Actions path is rejected if waits, cancellation, leases, recovery,
  or cross-project coordination cannot meet the same interruption fixtures.
- The current custom baseline is rejected if it requires materially more custom
  code or operator intervention without proving a unique invariant.

### Promotion rule

Choose the smallest composition that passes all scenarios. Every admitted
upstream responsibility must identify custom code, scripts, services, and docs
that it retires. An adoption that only adds another queue, ledger, scheduler,
database, UI, or memory fails even when its demo works.

## Execution plan

### Completed in this pass

- Reconstructed the original intent from primary OpenClaw archives and current
  first-party repositories.
- Separated implemented behavior from specifications, stubs, and contradicted
  health claims.
- Inventoried all 72 repositories owned by the GitHub account and categorized
  first-party lineage separately from forks.
- Re-evaluated documented current whole-platform, SDLC, worker, workflow,
  evolution, forge, and low-cost-service candidates from current primary
  sources; no candidate was cloned, executed, or behaviorally ranked in this
  pass.
- Produced the decision experiment, falsifiers, and retirement rule above.

### Next, after explicit approval of this material architecture evaluation

1. Complete the accepted current critical path: terminal reconciliation, another
   Gate C proof, clean-host/recovery proof, and provider-neutrality proof. Do not
   add broad controller/framework scope to those milestones.
2. Then create one architecture-evaluation issue with the eleven scenarios and
   exact acceptance thresholds, unless an explicit approved plan revision moves
   the evaluation earlier.
3. Pin candidate revisions and licenses; inventory all Paperclip advisories,
   patched versions, fix commits, reachable paths, and dependencies before
   execution.
4. Run Paperclip only in a disposable network-restricted environment with
   synthetic credentials and data; never point it at the live agent estate.
5. Implement only thin experimental adapters required to exercise the same work
   packet across the three candidates.
6. Publish receipts, operator-time measurements, failures, security findings,
   and the explicit custom-code retirement map.
7. Make one architecture decision: adopt, adapt, defer, or reject each plane.
8. Only then implement the winning composition and migrate one product slice.

## Open questions the archive does not settle

1. Is the primary first proof now the GovCon product factory, the software
   factory itself, or a personal research/brief workflow? The April ranking says
   personal research first; the current plan selects software/business factory
   infrastructure. This is a product-sequencing decision, not an architecture
   fact.
2. Which maintained runtime/platform owns the broad operational experience, and
   which exact gaps remain narrow extensions? Historical intent strongly favors
   upstream adoption, but current external source research must answer this.
3. Should GitHub remain the hosted authority, should a paid GitHub tier unlock
   native capabilities, or should a self-hosted forge own them? This requires a
   current cost/capability/administration comparison.
4. What is the minimum project module that can instantiate both a software
   workflow and a GovCon workflow without hard-coded branching?
5. Which genome components may evolve automatically, and what held-out tests
   prevent optimizing to the visible evaluation set?
6. What operator-attention budget defines success? Historical documents mention
   “briefings, not line review,” but lack a stable minutes-per-week target.
7. Which OpenClaw capabilities were genuinely unique and are not now covered by
   Hermes, Buzz, GitHub-native automation, or another maintained platform?
8. What evidence is required before any archived role, skill, memory, or workflow
   is allowed into a live runtime?

## Bottom line

The original architecture was not “build a controller.” It was:

> Define reusable agent and project genomes; instantiate them on replaceable
> runtimes and models; let them execute software and business workflows under
> durable authority; measure their outcomes; select safe improvements; and give
> one operator a concise command center for outcomes and exceptions.

The historical corpus also gives the governing implementation lesson in its own
words: **adopt upstream first, integrate through native seams, and build only the
missing contracts**. The transaction controller is one of those contracts. It
should become the invariant layer beneath the whole system, not the reason to
recreate the whole system around it.
