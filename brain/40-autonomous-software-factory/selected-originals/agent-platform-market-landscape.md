# External agent-factory research and market landscape — 2026-08-30

## Executive conclusion

The market now contains most of the infrastructure required to build a dependable
"system that builds systems," but it is split across distinct product categories.
There is no verified, maintained product that simultaneously provides:

1. a declarative company/project/swarm specification;
2. durable work admission and lifecycle authority;
3. interchangeable local and cloud workers;
4. software-delivery and non-software business workflows;
5. evidence-bound review and effect authorization;
6. controlled evaluation and self-improvement; and
7. a low-cost operator console suitable for one owner.

That finding does **not** justify rebuilding all seven layers. It implies a thin
owned control contract over bought or adopted substrates. The strongest current
buy/adopt candidates are:

- **GitHub plus GitHub Agentic Workflows (`gh-aw`)** for source, issues, review,
  CI/CD, triggers, and guarded repository writes.
- **A managed agent runtime**—AWS Bedrock AgentCore, Google Vertex AI Agent
  Engine, Microsoft Foundry Agent Service, or LangSmith Deployment—if and when
  the project needs production-hosted non-coding agents.
- **A coding-worker fleet**—Codex, Claude Code/Agent SDK, Factory Droid, Devin,
  Jules, OpenHands, or local Hermes—behind a provider-neutral worker contract.
- **A durable workflow engine only for workflows that prove they need it**.
  Temporal is the reliability leader; Prefect is materially cheaper and simpler
  for scheduled Python work; neither should own agent-company policy.
- **An existing portal/catalog only when operator inventory becomes painful**.
  Backstage/Port/Humanitec solve developer self-service and infrastructure
  provisioning, not autonomous-company lifecycle.

The practical **post-freeze landing hypothesis** for the current one-operator
system is therefore:

> GitHub Pro/Team plus a pinned, proven `gh-aw` as the repository-native event and delivery
> plane; retain a small provider-neutral authority/evidence kernel; run multiple
> worker harnesses through adapters; add a managed durable agent runtime only
> after a cross-domain workflow proves that GitHub Actions is insufficient.

OpenAI Frontier is the closest documented commercial vision to the whole target,
but it is enterprise-sales-led, pricing is undisclosed, and no public evidence
shows it is a self-serve or economical foundation for this project. ServiceNow
and Salesforce are the strongest business-process suites, but their value depends
on already living inside those systems of record. Factory and Devin are the most
complete engineering-worker products, not company operating systems. The new
"AI company" repositories are conceptually aligned but too young and
security-uncertain to be promoted without an adversarial exact-revision bake-off.

## Evidence policy

This report uses vendor documentation, vendor release material, vendor pricing,
and first-party repositories. Vendor adoption statements are labeled as such;
they are not independent validation. A feature is marked **GA**, **preview**, or
**unclear** only where a first-party source provides that status. The comparative
scores are reasoned assessments, not benchmark results. No platform was installed
or granted live credentials during this research.

This artifact is an untracked research note in a checkout observed 66 commits
behind `origin/main`; it is not a delivery-plan update. The current authoritative
remote handoff freezes all expansion and permits only exact-head review/
disposition of PR #280 followed by one atomic dogfood issue. Every market option
below is therefore **post-freeze research**, unless Mike explicitly approves a
governing plan change.

## First-principles requirements

The target is not "a multi-agent framework." It is a factory with seven separate
responsibilities. Combining them into one undifferentiated orchestrator recreates
the failure mode in which several systems believe they own the same task.

| Requirement | What must be true | What does **not** satisfy it |
|---|---|---|
| Company/project provisioning | A versioned definition can create roles, workers, workflows, budgets, policies, sources, artifacts, and environments repeatedly | A prompt that asks a manager agent to invent an org chart |
| Lifecycle authority | Exactly one system owns admission, identity, lease, retry, cancellation, and terminal state for a unit of work | Multiple issue trackers, queues, and agent managers all reconciling the same task |
| Execution | Workers run in isolated, reproducible environments with explicit tools, credentials, network, and budget | A shared shell with broad credentials |
| Evidence and governance | Outputs bind to exact inputs/candidates; policy and human approval precede material effects | A model saying tests passed or another agent informally agreeing |
| Operator experience | One owner sees goals, exceptions, cost, progress, evidence, and pending approvals across projects | Raw transcripts or separate vendor dashboards |
| Evaluation and improvement | Traces and outcomes produce candidates; candidates face offline/online evals and controlled promotion | Agents editing live prompts, policies, or skills based on self-judgment |
| Portability | Work definitions and receipts survive worker/vendor replacement | Provider-specific sessions as authoritative state |

## Market map

### 1. Repository-native forge and coding systems

#### GitHub, Copilot, and GitHub Agentic Workflows

GitHub is already a credible low-cost control surface for source, issues, pull
requests, checks, Actions, protected branches, rulesets, and audit history.
GitHub Free includes 2,000 private-repository Actions minutes; Pro includes 3,000.
The public pricing page lists Team at $4/user/month, while Copilot is a separate
product: Copilot Pro is $10/month and includes cloud agent, code review, and
third-party Claude Code/Codex agents. See [GitHub pricing](https://github.com/pricing),
[included usage](https://docs.github.com/en/billing/reference/product-usage-included),
and [Copilot plans](https://github.com/features/copilot/plans).

`gh-aw` is unusually relevant because it turns Markdown plus YAML frontmatter
into hardened GitHub Actions workflows and supports Copilot, Claude Code, Codex,
Gemini, OpenCode, Cursor, Kiro, Aider, and other engines. Its default agent job is
read-only; structured safe outputs are applied by separately permissioned jobs.
It includes action pinning, scoped permissions, sandbox/network controls, output
sanitization, threat detection, cost budgets, OpenTelemetry, workflow composition,
issues, comments, checks, pull requests, and sub-issues. See the official
[overview](https://github.github.com/gh-aw/introduction/overview/),
[safe-output reference](https://github.github.com/gh-aw/reference/safe-outputs/),
and [security FAQ](https://github.github.com/gh-aw/reference/faq/).

GitHub labels both Agentic Workflows and its CLI **public preview** with expected
rough edges and change. In this repository, current hosted Actions runs fail
before checkout with no runner and zero steps. Documented fit is therefore not
current executability.

**Assessment:** best current declarative repository-automation substrate and the
largest later opportunity to delete custom code if a pinned evaluation passes.
It is not a cross-company
task authority, durable long-running workflow service, semantic business model,
or self-improvement system. Actions runs are finite jobs; repository objects are
not enough to model every business effect. GitHub Pro/Team also does not buy
Copilot usage. Use it for repository events and guarded writes, not as a universal
agent runtime.

#### GitLab Duo Agent Platform

GitLab now documents foundational and custom agents, multi-agent flows, an AI
Catalog, triggers, session logs, and a GA Software Development Flow. The flow
plans, operates in the IDE, stages changes, and keeps acceptance with the user.
The Software Development Flow became GA in GitLab 18.8 and became available to
Free GitLab.com users with purchased credits in 18.10. See the
[Software Development Flow](https://docs.gitlab.com/user/duo_agent_platform/flows/foundational_flows/software_development/)
and [Agent Platform getting-started guide](https://docs.gitlab.com/user/get_started/get_started_agent_platform/).

Agent use is credit-metered. Free users can buy credits without Premium; Premium
includes a small monthly credit allowance and broader SDLC governance. Self-hosted
AI has additional licensing and operational requirements. See
[GitLab Credits](https://docs.gitlab.com/subscriptions/gitlab_credits/),
[Premium](https://about.gitlab.com/pricing/premium/), and
[Duo add-ons](https://docs.gitlab.com/subscriptions/subscription-add-ons/).

**Assessment:** a compelling unified alternative for an organization that wants
to standardize source, planning, security, CI/CD, and agents in one vendor. For
one operator already on GitHub, migration and self-host operations exceed the
incremental value. GitLab's agents remain SDLC-centered and do not provide the
full multi-company semantic/economic layer.

#### OpenAI Codex cloud and app

Codex provides isolated cloud workspaces, parallel tasks, GitHub integration,
local/IDE/cloud continuity, code review, skills, multi-agent supervision, and an
SDK. OpenAI states Codex is generally available and reports adoption at Cisco,
Rakuten, Duolingo, Vanta, and internally; these are vendor-reported adoption
claims, not independent performance evidence. See [Codex GA](https://openai.com/index/codex-now-generally-available/)
and the [Codex app](https://openai.com/index/introducing-the-codex-app/).

**Assessment:** a high-capability worker and operator console, not the governing
factory. It should receive bounded tasks and return artifacts/receipts. Provider
sessions, memory, and app automations should not become authoritative state.

#### Claude Code and Claude Agent SDK

Claude Code is a local coding harness with filesystem/shell tools, resumable
sessions, subagents, hooks, MCP, checkpoints, sandboxing, and GitHub integration.
The Agent SDK exposes the same tools, context management, and permission framework
for custom agents. Enterprise plans add managed policies, usage analytics, spend
controls, compliance API, SSO/SCIM, roles, and audit logs. Claude Code can use
Anthropic, Bedrock, or Vertex endpoints. See Anthropic's
[Agent SDK announcement](https://www.anthropic.com/news/enabling-claude-code-to-work-more-autonomously),
[sandboxing architecture](https://www.anthropic.com/engineering/claude-code-sandboxing),
and [enterprise controls](https://www.anthropic.com/news/claude-code-on-team-and-enterprise).

**Assessment:** excellent worker SDK with strong local ergonomics and improving
containment. It does not supply durable company/project lifecycle, a forge, or an
organization-wide business control plane. Use behind the worker boundary.

#### Google Jules

Jules supplies cloud coding sessions, GitHub sources, plan approval, activities,
and an API for creating sessions and integrating with Slack, Linear, and GitHub.
The API is explicitly **alpha**. See the [Jules API](https://developers.google.com/jules/api).

**Assessment:** useful additional coding worker, especially for asynchronous
Google-hosted tasks. Alpha API status makes it unsuitable as the lifecycle owner.

#### Devin/Cognition

Devin offers cloud IDE/shell/browser environments, managed parallel sessions,
scheduled sessions, playbooks, knowledge, integrations, session timelines,
structured API output, budgets, and an organization API. Cognition explicitly
describes Devin as strongest on bounded work and advises decomposing larger tasks;
its own docs call it a junior engineer. See [Devin introduction](https://docs.devin.ai/get-started/devin-intro),
[when to use Devin](https://docs.devin.ai/essential-guidelines/when-to-use-devin),
and [advanced session APIs](https://docs.devin.ai/work-with-devin/advanced-capabilities).

**Assessment:** one of the most complete managed engineering-worker fleets. Its
playbooks, schedules, knowledge, and API could replace worker orchestration code.
It remains an engineering execution service, with proprietary workspaces and
consumption units; it should not own business intent or final promotion authority.

#### Factory.ai Droid and Software Factory

Factory documents a single Droid runtime across local, desktop, web, cloud
computers, CI, VMs, Kubernetes, hybrid, EU, and fully air-gapped deployments. It
supports models/gateways selected by the customer, project policy, service
accounts, org hierarchy, command policy, hooks, sandboxes, audit, OpenTelemetry,
and an automated SDLC spanning triage, implementation, review, QA, documentation,
and incidents. See [product documentation](https://docs.factory.ai/),
[enterprise architecture](https://docs.factory.ai/enterprise), and
[data flows](https://docs.factory.ai/enterprise/privacy-and-data-flows).

**Assessment:** the strongest documented commercial engineering substrate in
this survey for model independence, deployment flexibility, central governance,
and fleet observability. Pricing is not publicly disclosed for enterprise. It
still models software work, not arbitrary companies and economic workflows.
Factory should be evaluated as a replacement for the engineering body, not as
the constitution or multi-domain factory.

### 2. Enterprise-wide agent platforms

#### OpenAI Frontier

Frontier is the closest commercial statement of the full target: business context
across systems, agents with identities and permissions, local/cloud/OpenAI-hosted
execution, parallel work, durable memory, evaluation/optimization loops,
observability, and enterprise governance. OpenAI identifies HP, Intuit, Oracle,
State Farm, Thermo Fisher, and Uber as initial adopters and Cisco, BBVA, and
T-Mobile as pilot customers. These are first-party claims. See
[Frontier introduction](https://openai.com/index/introducing-openai-frontier/)
and [Frontier product page](https://openai.com/business/frontier/).

**Maturity:** commercial enterprise program; precise service GA boundaries and
pricing are not public. **Fit:** conceptually highest. **Blockers:** sales-only,
likely enterprise economics, strong OpenAI dependency, and no public self-serve
declarative company specification. It is a future buy candidate, not a present
foundation.

#### AWS Bedrock AgentCore

AgentCore is now the most complete modular managed runtime in the market. It is
framework- and model-neutral and provides Runtime, persistent Memory, Gateway,
Identity, browser/code tools, policy, observability, evaluations, and optimization.
Policy intercepts tool calls with deterministic Cedar rules; optimization uses
versioned bundles, A/B traffic, and trace/evaluation evidence. Runtime supports
real-time and long-running work, isolated sessions, persistent filesystems, MCP,
A2A, and consumption pricing. Policy and Evaluations are documented GA in 2026.
See the [AgentCore overview](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/what-is-bedrock-agentcore.html),
[release notes](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/release-notes.html),
and [runtime lifecycle](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html).

The official harness announcement lists runtime prices of $0.0895/vCPU-hour and
$0.00945/GB-hour, plus model, memory, gateway, and CloudWatch usage. See
[AgentCore harness GA](https://aws.amazon.com/blogs/machine-learning/amazon-bedrock-agentcore-harness-is-now-generally-available-go-from-idea-to-production-grade-agent-in-minutes/).

**Assessment:** best managed component set for production agent execution,
security, evaluation, and controlled optimization. AWS lock-in is meaningful,
but framework/model neutrality and modular adoption reduce it. It does not provide
the company/project semantics or repository delivery authority. Strong Phase-2
candidate after a real workflow exceeds GitHub Actions/local execution.

#### Google Vertex AI Agent Builder / Agent Engine

Agent Engine provides a GA managed runtime and observability, with sessions,
memory, code execution, A2A, evaluation, and optimization at mixed GA/preview
levels. It supports ADK and other Python frameworks. Google reports hundreds of
thousands of deployed agents and 4.7 million ADK downloads; these are vendor
metrics. See [Agent Engine overview](https://cloud.google.com/vertex-ai/generative-ai/docs/reasoning-engine/overview)
and [Agent Builder lifecycle](https://cloud.google.com/blog/products/ai-machine-learning/get-started-with-vertex-ai-agent-builder).

Published unit pricing includes runtime CPU/memory and metered sessions/memory.
New customers receive $300 Google Cloud credit. See Google's
[pricing update](https://cloud.google.com/blog/products/ai-machine-learning/new-enhanced-tool-governance-in-vertex-ai-agent-builder/).

**Assessment:** strong managed runtime and natural fit if Gemini, BigQuery, and
Google Cloud are strategic. Some context/evaluation features remain preview and
current documentation notes security-control gaps such as CMEK/data-residency
limitations for Agent Engine. Not a company operating system.

#### Microsoft Foundry Agent Service

Foundry supplies hosted agents, managed tools, identity, tracing, evaluations,
optimization, versioned deployment, and publishing to Teams/Microsoft 365. Hosted
agents support MCP, A2A, Skills, code interpreter, search, and custom orchestration;
compute is billed during active sessions. The platform is moving quickly and has
multiple old/new API surfaces. Current documentation also warns that published
agent applications do not yet provide native end-user conversation isolation in
one project and therefore expose only stateless responses in that path. See
[hosted agents](https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/hosted-agents)
and [agent applications](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/agent-applications).

**Assessment:** strong for Microsoft-centered enterprises and Teams/M365 delivery.
The API churn and documented isolation limitation demand a targeted proof before
use. It is not the cheapest or simplest first substrate for one operator.

#### Salesforce Agentforce

Agentforce provides low/no-code agent construction, Salesforce data/actions,
testing, monitoring, digital-wallet cost tracking, and business-channel delivery.
Foundations is listed at $0; consumption is $500 per 100,000 Flex Credits or $2
per conversation, with additional user/add-on structures. See
[Agentforce pricing](https://www.salesforce.com/agentforce/pricing/) and
[Testing Center](https://help.salesforce.com/s/articleView?id=ai.agent_testing_center.htm&language=en_US&type=5).

**Assessment:** excellent if Salesforce is the system of record for sales/service
work. Testing can execute real actions, so Salesforce explicitly recommends a
sandbox. Outside a Salesforce-centered company, the data model and action pricing
are lock-in rather than leverage. It does not solve software delivery.

#### ServiceNow AI Agent Studio, Orchestrator, Fabric, and Control Tower

ServiceNow offers the broadest documented enterprise governance suite: no-code
Agent Studio, multi-agent Orchestrator, cross-vendor Agent Fabric, AI asset
inventory, onboarding/offboarding/approval playbooks, access maps, risk and
compliance, value/adoption views, and an AI Control Tower. It reported nearly
1,000 signed AI-agent customers at the 2025 launch; this is a vendor claim. See
the [launch announcement](https://www.servicenow.com/uk/company/media/press-room/ai-agents-studio.html),
[Control Tower playbooks](https://www.servicenow.com/docs/r/intelligent-experiences/aict-playbooks-reference.html),
and [Build Agent governance](https://www.servicenow.com/docs/r/application-development/build-agent-governance.html).

**Assessment:** closest packaged business-process control tower, but valuable
only with ServiceNow workflows/data/licenses. Pricing is account-specific and the
surface is operationally heavy. It is evidence that governance, inventory, access
maps, and lifecycle playbooks should be requirements—not evidence to adopt
ServiceNow for a solo factory.

### 3. Agent frameworks and managed agent runtimes

#### LangSmith Deployment / LangGraph

LangSmith Deployment is a framework-agnostic durable agent runtime with threads,
runs, state, task queues, cron, webhooks, human approval, multi-agent composition,
streaming, MCP/A2A, versioned deployments, rollback, and self-host/hybrid options.
LangSmith adds tracing, datasets, evaluation, annotation, sandboxes, gateway cost
controls, and an Engine that clusters failures and proposes fixes/evals. See
[Deployment](https://www.langchain.com/langsmith/deployment) and
[deployment documentation](https://docs.langchain.com/langsmith/deployment).

Developer observability is free to 5,000 traces/month; Plus is $39/seat/month and
includes one small serverless deployment, then meters compute/storage. See
[LangSmith pricing](https://www.langchain.com/pricing). LangChain reported nearly
400 production companies at the original platform GA; that is a first-party claim.

**Assessment:** strongest self-serve managed agent lifecycle/evaluation platform.
Use when stateful product/business agents become real. Do not duplicate its thread,
run, retry, deployment, trace, and evaluation features. It still needs an external
company model, effect authority, and software forge.

#### CrewAI AMP

CrewAI's open framework models Crews and Flows; AMP adds visual design, deployment,
REST APIs, tracing, tools, GitHub integration, human input, guardrails, testing,
training, dashboards, and cloud/VPC/self-hosted enterprise deployment. The free
tier includes 50 workflow executions/month. See [pricing](https://crewai.com/pricing)
and [AMP documentation](https://docs.crewai.com/enterprise/introduction).

**Assessment:** fast route to role-based multi-agent business workflows and a
credible prototype platform. Its governance and training claims need hands-on
verification. It should own individual deployed crew execution, never the same
cross-project task lifecycle as GitHub/another controller.

#### Temporal Cloud

Temporal is a durable execution substrate, not an agent framework. Application
code stays in the customer's environment; Temporal persists event history and
reliably replays workflows across process failures. Temporal Cloud offers 99.9%
single-region and 99.99% replicated SLA tiers. The AWS Marketplace route lists
$100/month plus $50/million actions. See [Temporal Cloud](https://temporal.io/cloud),
[pricing](https://temporal.io/get-cloud/aws-marketplace), and
[terms/SLA](https://temporal.io/terms-of-service).

**Assessment:** adopt when a critical workflow must survive days, callbacks,
failures, retries, and human pauses with deterministic recovery. It is excessive
for short agent tasks already bounded by Actions or a managed agent runtime. Its
event history should not be confused with business evidence or authorization.

#### Prefect, Dagster, and Hatchet

Prefect is a flexible Python workflow orchestrator with scheduling, state,
retries, events, automations, workers, and managed serverless execution. Its free
Hobby plan supports two users, five deployments, 500 serverless minutes, and
seven-day history; self-hosted OSS is available. See
[Prefect pricing](https://www.prefect.io/pricing) and
[Cloud/OSS comparison](https://www.prefect.io/compare/prefect-oss).

Dagster is a declarative, asset-oriented data orchestrator with lineage,
observability, checks, partitions, branch deployments, and CI/CD. It is a strong
fit for research/data pipelines, not general agent work. Dagster+ Solo begins at
$10/month plus usage. See [Dagster overview](https://docs.dagster.io/) and
[pricing](https://dagster.io/pricing).

Hatchet is an adjacent open-source task/workflow orchestrator aimed at durable
background work. It merits a lightweight bake-off against Prefect when low-latency
task queues are needed, but current research did not find a first-party capability
or adoption basis strong enough to prefer it over Temporal/Prefect for the core.

**Assessment:** Prefect is the most economical managed scheduler for early
cross-domain Python workflows. Dagster wins when artifacts are fundamentally data
assets. Temporal wins for mission-critical durable business processes. Select
one per workflow domain; do not stack them reflexively.

### 4. Developer portals and declarative provisioning

Backstage provides an open-source software catalog and Software Templates for
creating components from governed templates. Port provides a hosted catalog,
blueprints, scorecards, and self-service actions. Humanitec's Platform
Orchestrator reads environment-neutral Score workload specifications and resolves
them to Terraform, Crossplane, Pulumi, CDK, and other resource definitions. See
[Backstage](https://backstage.io/), [Port](https://www.port.io/), and
[Humanitec Platform Orchestrator](https://developer.humanitec.com/platform-orchestrator/docs/platform-orchestrator/overview/).

**Assessment:** these products answer "what software/services exist and how do I
provision an approved environment?" They do not answer "which agent may commit
which effect, what evidence proves success, or how does an AI company improve?"
Their patterns—catalog, templates, scores, environment-neutral specs—should be
borrowed. Adoption should wait until multiple projects make inventory and golden
paths a real problem. Humanitec's historical small-team offer was roughly
$999/month, far beyond present economics.

### 5. Emerging agent-company repositories

These projects are directly aligned with the vision but currently provide weak
adoption evidence. Feature-rich READMEs are not production proof.

| Project | Documented proposition | Current evidence and risk | Decision |
|---|---|---|---|
| [Paperclip](https://github.com/paperclipai/paperclip) and [Companies](https://github.com/paperclipai/companies) | Multi-company operating system with org charts, goals, projects/issues, agents, budgets, approvals, audit, heartbeats/routines, adapters, and a portable Markdown/YAML `agentcompanies/v1` package | MIT, roughly 79,700 stars when inspected, active weekly releases, but created March 2026. GitHub lists twelve advisories across import/command execution, DNS rebinding, cross-company authorization, IDOR, and approval attribution; two July advisories listed no patched release when inspected | Strongest adopted/documented company-plane hypothesis; pinned disposable security evaluation only, never current trust anchor |
| [Runfusion/Fusion](https://github.com/Runfusion/Fusion) | Mission → milestone → slice → feature → task software factory, org/company import/export, worktrees, custom workflows, review/merge, approvals, mailbox/chat and mobile UI; imports Paperclip/company packages | MIT, approximately 1,170 stars, current first-party stable distribution `0.76.0` with a separate beta channel, created April 2026. Source/tests document leases, recovery, approval/audit isolation, deterministic authoritative scores and advisory AI scores, but adoption and security assurance are limited | Newly discovered whole-factory challenger; include in the same hostile bake-off, not wholesale adoption |
| [SynthOrg](https://github.com/Aureliolo/synthorg) | Synthetic organization with roles, departments, hierarchy, memory, budgets, governance, provider neutrality, dashboard | Declares itself pre-alpha; 8 stars and 1 fork when inspected; BUSL 1.1 rather than OSI-open-source; much runtime work tested with scripted providers | Study its domain model and tests; do not adopt as authority |
| [Kompany](https://github.com/Fei2-Labs/Kompany) | Solo-founder AI C-suite, debates, budgets, 24/7 directives | 2 stars/1 fork when inspected; AGPL; no independent production/adoption evidence | Mine economic/budget concepts only |
| [OpenZosma](https://github.com/zosmaai/openzosma) | Self-hosted hierarchical agent teams via web/WhatsApp/Slack, A2A, OpenShell sandbox option | Broad implementation and Apache-2.0, but young and operationally heavy (Postgres, Valkey, RabbitMQ, optional K3s); adoption unverified | Include in isolated bake-off, especially mobile/operator UI |
| [OpenCognit](https://github.com/OpenCognit/opencognit) | CEO orchestrator, persistent memory, execution, atomic budgets | AGPL; small-project maturity and production evidence unverified | Watch; no governing adoption |
| [OpenLegion](https://github.com/openlegion-ai/openlegion) | Per-agent containers/microVMs, credential vault, budgets, ACLs, multi-channel fleet | Strong security-oriented design claims and source available; young, no verified large production base | Evaluate its security model/components, not wholesale authority |
| [OpenCompany](https://github.com/tinyhumansai/opencompany) and similar names | Company host over agent modules; variants claim self-improving business operation | Fragmented naming, APIs/dependencies, and little verified adoption | Reject as foundation pending maturity |
| OpenAgentOS/AgentOS/Canopy/Agems/OpenZosma peers | Org charts, roles, agent registries, company dashboards | Many are prototypes, renamed projects, or thin shells; no common lifecycle standard or conformance evidence found | Research corpus only |

Paperclip security admission must begin with its complete
[advisory register](https://github.com/paperclipai/paperclip/security/advisories),
not only the especially relevant
[DNS-rebinding RCE](https://github.com/paperclipai/paperclip/security/advisories/GHSA-x8hx-rhr2-9rf7)
and
[inherited Codex capability failure](https://github.com/paperclipai/paperclip/security/advisories/GHSA-gqqj-85qm-8qhf).
Every affected/patched version, fix commit, reachable path and dependency must be
accounted for before selecting an executable revision.

The meaningful lesson is market convergence on org charts, budgets, persistent
memory, scheduled work, messaging, and operator dashboards. The missing shared
standard is promotion-safe lifecycle authority. A small internal `CompanySpec`
or `SwarmSpec` should not be invented first. Paperclip's
`agentcompanies/v1-draft` is the first concrete portable company-package format
found, and Fusion demonstrates a second importer. It lacks independent
governance, a conformance suite, and proven round-trip interoperability. Treat
it as a hostile pinned fixture/candidate—not the default internal schema—until
two independent implementations pass import, export, extension preservation,
hash/license, and behavior-equivalence tests.

### 6. NVIDIA OpenShell and NemoClaw

OpenShell supplies a sandbox/policy/inference runtime for Codex, Claude Code,
Copilot CLI, OpenCode, Hermes, OpenClaw, Ollama, and Pi. It separates credentials
from sandboxes and supports live network policies and logs. NemoClaw is a guided
reference stack on OpenShell for OpenClaw/Hermes. NVIDIA explicitly labels
NemoClaw **alpha, early preview, not production-ready**. See
[OpenShell](https://github.com/NVIDIA/OpenShell) and
[NemoClaw](https://github.com/NVIDIA/NemoClaw).

**Assessment:** OpenShell is a serious candidate for the provider-neutral local
execution boundary. NemoClaw is evidence and a reference integration, not a
production platform. This is a place to adopt rather than maintain home-grown
sandbox/network/credential routing if a bounded evaluation passes.

NVIDIA's current platform documentation explicitly covers both Hermes Agent and
OpenClaw, versioned blueprints, policy/sandbox/credential routing, and workspace
preservation. Apple Silicon is tested with stated limitations; NVIDIA does not
claim Hermes production parity on that platform. That makes OpenShell/NemoClaw
the strongest newly discovered candidate for the **local body**, while preserving
the distinction between a runtime substrate and the factory's authority. See
[NemoClaw overview](https://docs.nvidia.com/nemoclaw/user-guide/about/overview)
and [Hermes platform support](https://docs.nvidia.com/nemoclaw/user-guide/hermes/reference/platform-support).

### 7. Additional OSS components and rejection boundaries

| Component | Useful role | Boundary |
|---|---|---|
| [Dapr Agents](https://github.com/dapr/dapr-agents) | Closest composable OSS analogue to AgentCore when combined with Dapr Workflows, actors, state and pub/sub | Consider only if a managed-runtime gap is proved; sidecars and distributed state recreate substantial operations |
| [agentgateway](https://github.com/agentgateway/agentgateway) | Linux Foundation gateway for MCP, A2A and model routing, authorization, budgets and telemetry | Promising alpha gateway, not task/company authority |
| [Kubernetes Agent Sandbox](https://github.com/kubernetes-sigs/agent-sandbox) | Declarative sandbox CRDs, identity, templates and warm pools | Strong future multi-user substrate, but requires Kubernetes and is not a factory OS |
| [E2B](https://github.com/e2b-dev/E2B) | Managed/self-hostable sandbox API | Execution isolation only; self-hosting is operationally material |
| [Kestra](https://github.com/kestra-io/kestra) | Apache-licensed declarative YAML business workflows, triggers, retries and pause/resume human gates | Strong generic automation challenger if needed; application still owns agent policy and evidence |
| [n8n](https://github.com/n8n-io/n8n) | Very large connector catalog and internal automation | Sustainable Use license is not OSI open source and restricts hosted/white-label use; connector edge only |
| [Dify](https://github.com/langgenius/dify) | Visual LLM application, RAG and agent workflow construction | Modified Apache terms restrict some multi-tenant/branding uses and its application semantics do not match factory authority |
| [Flowise](https://github.com/FlowiseAI/Flowise) | Historical visual agent-flow builder | Archived with end-of-life announced for 2026-08-31; reject new adoption |
| [Microsoft Agent Framework](https://github.com/microsoft/agent-framework) | Production-ready embedded graph/workflow framework and AutoGen successor | Strong inside one application; not a global lifecycle authority |
| [AutoGen](https://github.com/microsoft/autogen) | Historical multi-agent framework | Officially in maintenance/community mode; reject for new foundation work |
| [Promptfoo](https://github.com/promptfoo/promptfoo) + [Inspect AI](https://github.com/UKGovernmentBEIS/inspect_ai) | Declarative regression/red-team gates plus rigorous tool-agent evals and sandboxed logs | Evidence generators only; Inspect correctly treats models/tasks as untrusted code |
| [Langfuse](https://github.com/langfuse/langfuse) / [Phoenix](https://github.com/Arize-ai/phoenix) | Traces, prompts, datasets and evaluations | Langfuse mixes MIT core and enterprise areas; Phoenix's current root license is ELv2 rather than OSI open source—review license and operations before selection |

Reassembling AgentCore from Dapr, agentgateway, a sandbox service, identity,
secrets, telemetry and eval products is technically possible. At present it is
more operationally expensive than either using the managed service or staying
local. Do not build that bundle speculatively.

## Comparative requirements matrix

Scores: **3** strong documented support; **2** useful but partial; **1** adjacent;
**0** absent/not the product's job; **?** insufficient public evidence. Scores do
not imply that overlapping products can safely share authority.

| Platform | Company/project model | Declarative provisioning | SDLC | Worker/runtime | Durable lifecycle | Eval/improvement | Governance | Operator UI | Portability |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| GitHub + `gh-aw` | 1 | 2 | 3 | 2 | 1 | 1 | 3 | 2 | 3 |
| GitLab Duo | 1 | 2 | 3 | 2 | 2 | 1 | 3 | 3 | 2 |
| Codex | 0 | 1 | 3 | 3 | 1 | 2 | 2 | 3 | 2 |
| Claude Code/SDK | 0 | 1 | 3 | 3 | 1 | 1 | 2 | 2 | 3 |
| Jules | 0 | 1 | 3 | 3 | 1 | 1 | 1 | 2 | 1 |
| Devin | 1 | 2 | 3 | 3 | 2 | 2 | 2 | 3 | 1 |
| Factory | 1 | 2 | 3 | 3 | 2 | 2 | 3 | 3 | 2 |
| OpenAI Frontier | 3 | ? | 2 | 3 | 3 | 3 | 3 | 3 | 1 |
| AgentCore | 1 | 3 | 1 | 3 | 3 | 3 | 3 | 2 | 2 |
| Vertex Agent Engine | 1 | 3 | 1 | 3 | 3 | 2 | 3 | 2 | 2 |
| Microsoft Foundry | 1 | 3 | 1 | 3 | 3 | 2 | 3 | 3 | 1 |
| ServiceNow | 3 | 2 | 1 | 2 | 3 | 2 | 3 | 3 | 1 |
| Salesforce Agentforce | 3 | 2 | 1 | 2 | 3 | 3 | 3 | 3 | 1 |
| LangSmith Deployment | 1 | 3 | 1 | 3 | 3 | 3 | 3 | 3 | 2 |
| CrewAI AMP | 2 | 2 | 1 | 3 | 2 | 2 | 3 | 3 | 2 |
| Temporal | 0 | 3 | 0 | 1 | 3 | 0 | 3 | 2 | 3 |
| Prefect | 0 | 3 | 0 | 2 | 3 | 1 | 2 | 3 | 3 |
| Backstage/Port/Humanitec | 1 | 3 | 2 | 0 | 1 | 0 | 3 | 3 | 2 |
| Emerging agent-company OSS | 3 | 2 | 1 | 2 | 1 | 1 | 1 | 2 | 2 |
| Paperclip | 3 | 3 | 1 | 2 | 2 | 1 | 2 documented/security-gated | 3 | 3 at package layer |
| Fusion | 3 | 3 | 3 | 2 | 2 | 2 | 2 documented/unproven | 3 | 2 |

### Finalist matrix against the complete factory contract

This is the decision matrix that should govern an actual bake-off. `H` means
strong documented support, `P` partial or requires an external component, `N`
not supplied, and `?` insufficient public evidence. It intentionally exposes
authority collisions: no row is a recommendation to combine lifecycle owners.

| Requirement | GitHub + `gh-aw` | AgentCore | LangSmith Deployment | Factory | Frontier | OpenShell/NemoClaw |
|---|---|---|---|---|---|---|
| Company/portfolio model | P | N | N | P | H | N |
| Declarative portable package | H for repo workflows | H via AWS IaC, AWS-bound | H for agent deployments | P, `.factory` policy | ? | H for versioned sandbox blueprints/policy |
| Single task/lease/approval/terminal authority | P, run/issue semantics | P, runtime sessions not business authority | H for threads/runs | P for engineering sessions | H claimed, details private | N, execution boundary only |
| Durable events/waits/retries/recovery | P | H | H | P | H claimed | P, sandbox lifecycle/snapshots |
| Runtime/model neutrality | H for supported engines | H | H | H | P, OpenAI-centered | H across supported harnesses/providers |
| Sandbox/identity/external policy | H for Actions/safe outputs | H, IAM/Cedar/Gateway | H, custom auth/sandbox | H | H claimed | H, core purpose |
| Software-delivery lifecycle | H | P | P | H | P | P, supplies workers not forge |
| Non-code/business workflows | P | H | H | P | H | P |
| Knowledge/memory provenance | P, Git is explicit | P, managed memory needs external provenance | P, state/memory plus external provenance | P | H claimed | N/P, worker storage only |
| Eval/optimization/evolution | P | H, bounded eval/A-B optimization | H | P | H claimed | N |
| Observability/cost budgets | H | H | H | H | H claimed | P/H for runtime telemetry/policy |
| Operator/proactivity UI | P | P | H | H | H | P, terminal/runtime UI |
| Deployment portability | H for source/workflows | P | P/H with self-host option | H documented | ? | H, local/self-hosted |
| Maturity/security/adoption/economics | GitHub mature/low cost; `gh-aw` public preview and current runner path unavailable | GA modular services, consumption cost | Deployment GA; Engine beta; self-serve $39/seat + usage | Strong docs, price opaque | Early enterprise, price opaque | OpenShell stable release; NemoClaw alpha |

**Interpretation:** GitHub + `gh-aw` and OpenShell are complementary because the
former can own repository workflows while the latter is only an execution
boundary. AgentCore and LangSmith are competing candidates to own durable agent
runs. Factory competes with the coding-worker fleet. Frontier competes with most
of the stack and cannot be safely composed until its authority/export seams are
publicly known.

## What the market now makes unnecessary to build

The following should be bought/adopted unless an exact conformance test proves a
hard gap:

- repository hosting, issues, PRs, review status, checks, branch protection, and
  ordinary CI/CD;
- Markdown-defined agentic repository triggers and guarded write jobs;
- coding-agent sandboxes, browser/shell tooling, streaming logs, and session UI;
- generic task queues, schedules, retries, heartbeats, and durable timers;
- generic tracing, token/cost measurement, datasets, and LLM evaluators;
- generic MCP gateway/registry, OAuth, secrets proxy, and agent runtime identity;
- enterprise SSO, SCIM, audit-log storage, and cloud resource provisioning;
- generic software catalog and environment templates.

The small owned layer should be limited to the product's actual differentiators:

- `CompanySpec`/`ProjectSpec`/`SwarmSpec` domain definitions;
- principal/effect classification and explicit authorization grants;
- the one authoritative cross-system work identity and state mapping;
- evidence receipts bound to exact candidates and reviewers;
- provider/runtime conformance adapters;
- experiment/promotion rules for self-improvement;
- a unified owner view composed from authoritative systems.

For the first item, `agentcompanies/v1-draft` should be the first external
fixture, not automatically the internal schema. Prove two-way conformance before
adopting or extending it. Treat packages as untrusted data: require schema
validation, immutable references and hashes, license/provenance preservation,
secret references rather than values, and executable content denied by default.

## Open interoperability standards

The market has converged on distinct protocol boundaries:

- [MCP](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization)
  connects agents to tools and data. HTTP authorization is useful, but it is
  optional and stdio implementations commonly inherit environment credentials;
  MCP is not a capability policy by itself.
- [A2A](https://google-a2a.github.io/A2A/specification/) connects independent,
  potentially opaque agent services. The Linux Foundation reported more than
  150 supporting organizations and production use in 2026. It is an
  interoperability boundary, not a queue, lease, approval, or evidence model.
- [AG-UI](https://docs.ag-ui.com/) standardizes event-based agent-to-user
  streaming, state, tools, and interaction. It is a better future command-center
  seam than another proprietary frontend protocol.
- [OpenTelemetry GenAI conventions](https://github.com/open-telemetry/semantic-conventions-genai/blob/main/docs/gen-ai/gen-ai-spans.md)
  cover inference, retrieval, memory, and tool execution, but remain under
  development. Map telemetry at one adapter seam so convention churn cannot
  become domain state.

These standards reduce adapter code. None supplies lifecycle or promotion
authority.

## Research reality: "self-improving" must mean bounded optimization

The research frontier does not support deploying a generally recursive,
self-improving autonomous company. What it supports is narrower and useful:

- Google's AlphaEvolve/AlphaDev line combines model-generated candidates with
  objective automated evaluators. The evaluator, search surface, and promotion
  criterion are externally fixed; the system is not allowed to redefine success.
  See [Google DeepMind's science overview](https://deepmind.google/science/).
- GEPA evolves textual components using trajectory feedback and an explicit
  metric over a bounded candidate population. The paper reports strong
  sample-efficiency, but that is prompt/program optimization on defined tasks,
  not constitutional self-modification. See the
  [GEPA paper](https://arxiv.org/abs/2507.19457) and
  [DSPy implementation contract](https://github.com/stanfordnlp/dspy/blob/main/docs/docs/diving-deeper/gepa-in-depth.md).
- Anthropic's production research system uses conditional orchestrator/worker
  parallelism, not a standing swarm for every query. Simple work receives one
  agent; complex research receives carefully divided subagents. See
  [Anthropic's multi-agent engineering report](https://www.anthropic.com/engineering/multi-agent-research-system).
- MLR-Bench found current agents produced fabricated or invalid experimental
  results in roughly 80% of evaluated cases. This is direct evidence against
  letting an agent generate, judge, and promote its own improvements. See the
  [NeurIPS 2025 paper](https://proceedings.neurips.cc/paper_files/paper/2025/hash/ab8dd000d6f87f40061a73f8bca7fae4-Abstract-Datasets_and_Benchmarks_Track.html).

Therefore the production architecture should contain an **offline evolution
lab**, not an autonomous mutation loop. It may propose changes to prompts, skills,
routing, tool descriptions, or bounded code surfaces; deterministic tests,
held-out evals, cost/regression limits, independent review, exact-candidate
receipts, and authorized promotion remain outside the optimizer. The market's
AgentCore Optimization and the currently **beta** LangSmith Engine are compatible
with this model when their proposal and traffic-promotion boundaries are
configured explicitly.

### What the research actually demonstrates

- [mini-SWE-agent](https://github.com/SWE-agent/mini-swe-agent) reports more than
  74% on SWE-bench Verified with an agent loop of roughly 100 lines. Whatever the
  benchmark's current limitations, this shows that stronger models and a small
  shell loop can rival elaborate worker scaffolds. A custom universal harness
  must beat that minimal baseline before it is justified.
- Anthropic's
  [production multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)
  found multi-agent coordination useful for independently parallel research,
  but roughly fifteen times as token-intensive as chat and poorly suited to work
  with tightly shared context and dependencies. Multi-agent operation is
  conditional test-time scaling, not a permanent org chart for every task.
- [AlphaEvolve](https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/)
  demonstrates meaningful improvements where candidate quality is automatically
  and quantitatively verifiable. That is the valid genetic pattern: fixed
  mutation surface, objective evaluator, budget, lineage, and external selection.
- [DSPy MIPRO](https://arxiv.org/abs/2406.11695) and
  [GEPA](https://arxiv.org/abs/2507.19457) demonstrate bounded optimization of
  prompts/program components against explicit datasets and metrics. They do not
  justify live constitutional self-editing.
- [Karpathy AutoResearch](https://github.com/karpathy/autoresearch) succeeds by
  constraining the editable file, experiment duration, metric, branch, and
  keep/discard rule. It is a laboratory pattern, not a company controller.
- [MLR-Bench](https://arxiv.org/abs/2505.19955) found fabricated or invalidated
  experimental results in roughly 80% of evaluated research-agent cases. This
  is direct counter-evidence to letting a generator judge and inherit its own
  research conclusions.

### Evaluation limits the architecture must respect

- OpenAI's 2026
  [coding-evaluation audit](https://openai.com/index/separating-signal-from-noise-coding-evaluations/)
  says SWE-bench Verified no longer provides a reliable primary capability
  signal because of design and contamination problems. Use private temporal
  fixtures plus a portfolio such as
  [Terminal-Bench/Harbor](https://github.com/harbor-framework/terminal-bench),
  [BFCL](https://gorilla.cs.berkeley.edu/leaderboard),
  [OSWorld](https://github.com/xlang-ai/OSWorld), and
  [WebArena](https://github.com/web-arena-x/webarena).
- [METR's time-horizon work](https://metr.org/time-horizons/) measures task
  difficulty at a success probability, not uninterrupted autonomous runtime;
  high-context real work is harder. It cannot authorize unattended company
  operation.
- [MemoryAgentBench](https://arxiv.org/abs/2507.05257) finds no current memory
  system masters retrieval, test-time learning, long-range understanding, and
  selective forgetting. Memory remains derived context, never authority.
- NIST's
  [agent-hijacking evaluation](https://www.nist.gov/news-events/news/2025/01/technical-blog-strengthening-ai-agent-hijacking-evaluations)
  and [AgentDojo](https://github.com/ethz-spylab/agentdojo) show that indirect
  prompt injection remains unresolved. External content cannot share a trust
  channel with authority-bearing instructions or credentials.
- LLM judges exhibit systematic bias and overconfidence; calibrated selective
  escalation can bound risk, but model judgment should remain secondary to
  deterministic checks and human review for consequential promotion
  ([Trust or Escalate](https://openreview.net/pdf?id=UHPnqSTBPO)).

## Recommended landing point

### Post-freeze smallest coherent option set

These are research recommendations for a later admitted architecture issue, not
actions authorized in the present frozen delivery sequence.

1. **Pay for GitHub's governance, not another forge.** Use GitHub Pro for a
   personal private repository or Team for an organization as needed. Enable
   branch/ruleset enforcement and use self-hosted runners where appropriate.
2. **Evaluate a pinned `gh-aw` release after hosted/self-hosted runner execution
   is proven.** Candidate fixtures are triage, research refresh, CI diagnosis,
   review preparation, documentation maintenance, and issue decomposition. Begin
   with read-only agents and separately permissioned safe outputs.
3. **Treat Codex, Claude Code, Factory, Devin, Jules, OpenHands, and Hermes as
   replaceable workers.** Run a fixed task packet through at least three to
   measure quality, cost, recovery, intervention, and receipt fidelity.
4. **Keep the owned kernel thin.** It owns identities, authority, mappings,
   receipts and promotion—never shell execution, generic queues, Git hosting, or
   model loops. A company-package profile remains undecided until conformance
   evidence exists.
5. **Use local SQLite/Git for the first declarative registry and receipts.** Do
   not deploy Kubernetes, Backstage, Temporal, or an enterprise agent platform
   merely to express ten roles and several projects.
6. **Evaluate OpenShell/NemoClaw as the local execution boundary.** It is the
   strongest current match for this Apple-Silicon/Hermes estate. OpenShell
   publishes a stable release; NemoClaw remains alpha, and NVIDIA explicitly
   withholds Hermes production-parity claims. Use exact revisions, synthetic
   credentials, adversarial policy tests, and a clean uninstall before
   considering activation.

### Whole-factory authority bake-off

After the accepted transactional/recovery critical path is proved—or after an
explicit owner-approved plan change—compare three mutually exclusive lifecycle
authorities:

1. Paperclip plus its `agentcompanies/v1-draft` candidate;
2. Fusion using its native/company-import model; and
3. GitHub Issues/Projects plus the thin current authority kernel and `gh-aw`.

| Authority requirement | Paperclip | Fusion | Current GitHub/CAS kernel |
|---|---|---|---|
| Company/goals/projects/budgets | Strong documented model | Strong documented model | Partial; product repositories and issues, no accepted company schema |
| Portable package | `agentcompanies/v1-draft`; no independent governance/conformance | Imports/exports company formats; round-trip equivalence unproven | No accepted package format |
| Authoritative work identity and terminal state | Paperclip issue state | Fusion mission/workflow/task state | GitHub issue plus remote CAS claim/tombstone |
| Atomic lease/fencing | Conditional checkout and workspace leases documented | Leases documented/tested | Proven bounded CAS generation/fencing fixture |
| Retry/recovery after loss | Outbox/dedupe/recovery actions documented | Recovery documented/tested | Partial bounded recovery; full clean-host run unproven |
| Approval/effect boundary | Runtime review/approval and budgets; prior approval-attribution advisories | Oversight/destructive/merge gates documented | Exact candidate/effect contracts; several phases remain operator-supplied |
| Software delivery | Adjacent; not its primary contract | Strong documented worktree/review/merge path | One bounded issue-to-merge fixture; broad path frozen |
| Non-code business workflow | Strong company/work abstraction | Documented custom workflows | Product-specific workflows external to kernel |
| Cross-company isolation | Claimed; prior cross-company advisories require hostile proof | Claimed/tested; independent proof absent | Separate repositories today; generalized company isolation absent |
| Exact candidate plus independent review | Partial; must be proved | Deterministic scores/review documented; exact independent identity needs proof | Exact-subject review/promotion contract proven only in bounded fixtures |
| Export, migration and uninstall | Company export documented | Import/export documented | Git/GitHub artifacts portable; controller replacement mapping undefined |
| Maturity/security | Very active and widely starred, but created 2026 with twelve advisories | Stable `0.76.0` distribution; young 0.x project with a separate beta channel, small adoption, and limited visible security process | Small owned codebase with known limitations and current freeze |

The matrix is documentation-level except where it explicitly says a bounded
fixture was proven. Replacement requires a migration map for every task, lease,
approval, receipt and terminal state; composition without that map is rejected.

Optio, OpenHands, Codex, Hermes, OpenShell, and managed runtimes may participate
only as workers or execution boundaries unless a candidate explicitly replaces
the lifecycle authority. Inject malicious company packages, prompt-injected
issues/documents, cross-company secret access, stale approval replay, wrong-actor
attribution, runner crash after an external effect but before acknowledgement,
lease expiry, double-worker races, lost events, network exfiltration, and
candidate-hash drift. Reject any candidate that cannot be the sole owner of task
identity, lease, approval, retry, and terminal state.

### Next: select one production agent substrate through a vertical slice

Evaluate **AgentCore**, **LangSmith Deployment**, and **CrewAI AMP** using one
non-software cross-domain workflow such as opportunity discovery → evidence
packet → review → approved outreach draft. Require:

- resume after worker/control-plane restart;
- deterministic principal/effect denial;
- per-run and per-project cost caps;
- trace and artifact export;
- model and worker replacement;
- human approval bound to exact proposed effect;
- no duplicate task authority;
- a clean removal path.

AgentCore leads on modular managed security/evaluation; LangSmith leads on
self-serve durable agent lifecycle and debugging; CrewAI leads on rapid role-based
workflow authoring. Select at most one as lifecycle owner for that domain.

### Later: conditions for heavier adoption

- Add **Temporal** only when a valuable workflow must survive long waits,
  callbacks, failures, and version changes beyond the selected agent runtime.
- Add **Prefect** for economical scheduled Python/research/data jobs that do not
  need Temporal's stronger replay model.
- Add **Backstage or Port** after there are enough factories/services that catalog
  and self-service provisioning clearly save operator time.
- Evaluate **Frontier** only if enterprise pricing becomes accessible and OpenAI
  provides exportable definitions, receipts, identities, and an acceptable exit.
- Consider **ServiceNow/Salesforce** only when a real company adopts those systems
  of record; do not purchase them to simulate a company.

## Decision in one sentence

The state of the market supports **buying or adopting almost every execution
capability, retaining only the authority/evidence/evolution invariants, and
selecting one lifecycle owner through an adversarial bake-off**. The current
delivery freeze remains authoritative. After it is satisfied or explicitly
revised, the safest architecture baseline is GitHub-native authority,
replaceable workers, and a separately evaluated OpenShell local boundary;
`gh-aw` remains a preview candidate until its runner path works. Paperclip and Fusion are credible
whole-factory challengers, not approved foundations. Add one managed runtime only
after a real non-code workflow proves local/Actions execution insufficient.

## Claims still requiring a live bake-off

- Whether `gh-aw` can express all required guarded repository effects without a
  parallel custom reconciler.
- Whether AgentCore or LangSmith can export enough state/evidence to preserve
  provider-neutral authority.
- Whether Factory's enterprise deployment and model independence are available
  at viable solo/small-company pricing.
- Whether emerging OpenZosma/OpenLegion security boundaries withstand adversarial
  testing and restart/recovery scenarios.
- Actual monthly costs for the representative workload across local models,
  Copilot/Codex/Claude, Factory/Devin, and managed agent runtimes.
- Whether one operator benefits from a new portal or whether the GitHub/Codex UI
  already provides the necessary exception view.
