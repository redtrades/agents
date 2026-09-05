# Agent Factory Market Refresh

**Evidence cutoff:** 2026-08-30  
**Question:** Which maintained open-source systems, free tiers, and low-cost subscriptions can supply the control plane, durable runtime, secure worker, SDLC, observability/evaluation, and declarative provisioning for a system that builds and operates other systems?

## Method and claim labels

This refresh uses only first-party product documentation, pricing pages, source repositories, release pages, and security advisories. Prices are current list prices, excluding model/API consumption unless stated. Repository stars are omitted except where a first-party repository page is useful as weak maturity context; popularity is not proof of production fitness.

- **Documented** means the cited owner explicitly describes the capability.
- **GA / production-ready** is used only when the owner says so.
- **Preview / alpha** is retained even if the implementation looks broad.
- **Inference** identifies the architectural conclusion drawn from the evidence.

## Bottom line

The market now contains most of the layers required by the original vision. Building a new workflow engine, generic agent harness, sandbox, eval platform, developer portal, or infrastructure provisioner would duplicate maintained systems. What is still missing is a thin, provider-neutral authority layer that composes those systems without letting overlapping schedulers, approval systems, or agent memories become competing sources of truth.

The strongest low-cost starting split is:

1. **GitHub Free/Team plus Actions and `gh-aw`** for repository, issue, pull-request, CI, and agentic-workflow surfaces. Team is $4/user/month; public-repository Actions are free, and private-repository plans include minutes. `gh-aw` is a public preview, so use it for bounded repository automation rather than as the platform's sole authority. [GitHub plans](https://github.com/pricing), [included Actions usage](https://docs.github.com/en/billing/reference/product-usage-included), [`gh-aw` documentation](https://github.github.com/gh-aw/), [`gh-aw` public-preview announcement](https://github.blog/changelog/2026-06-11-github-agentic-workflows-is-now-in-public-preview/)
2. **Paperclip or Fusion only in a credential-isolated lab bakeoff** for the company/org/task control-plane experience. Paperclip is the closest documented company model; Fusion is the closer software-factory/SDLC model. Neither should yet own production credentials or final authority. Paperclip's published advisories make that security gate decisive. [Paperclip repository](https://github.com/PaperclipAI/paperclip), [Paperclip advisories](https://github.com/paperclipai/paperclip/security/advisories), [Fusion repository](https://github.com/Runfusion/Fusion), [Fusion releases](https://github.com/Runfusion/Fusion/releases)
3. **Hermes as a replaceable agent worker and OpenShell as the target local sandbox/policy substrate.** Hermes is MIT and actively released. OpenShell is Apache-2.0 and supplies declarative policy, credential brokering, and sandboxing, but currently labels itself alpha/single-player. NemoClaw proves a tested Hermes integration and Apple-Silicon path, while explicitly not asserting production parity. [Hermes repository](https://github.com/NousResearch/hermes-agent), [Hermes releases](https://github.com/NousResearch/hermes-agent/releases), [OpenShell repository](https://github.com/NVIDIA/OpenShell), [NemoClaw support matrix](https://docs.nvidia.com/nemoclaw/user-guide/hermes/reference/platform-support)
4. **Dapr Agents v1.0 or one established durable workflow engine—not several—as lifecycle authority.** Dapr Agents is now explicitly GA/production-ready and supplies durable workflows, state, messaging, observability, and cryptographic agent identity in a portable open-source stack. Temporal remains the conservative commercial durability option; Hatchet, Prefect, and Kestra provide cheaper or more declarative alternatives. [Dapr Agents](https://docs.dapr.io/developing-ai/dapr-agents/), [Temporal Cloud](https://temporal.io/cloud), [Hatchet pricing](https://hatchet.run/pricing), [Prefect pricing](https://www.prefect.io/pricing), [Kestra pricing](https://kestra.io/pricing)
5. **Inspect AI + Promptfoo + Phoenix or Langfuse OSS** for an offline, evaluator-driven improvement lab. These cover reproducible evaluation, adversarial testing, traces, datasets, and human annotation without inventing another evaluation platform. They do not justify unrestricted recursive self-modification. [Inspect AI](https://inspect.aisi.org.uk/), [Promptfoo pricing](https://www.promptfoo.dev/pricing/), [Phoenix self-hosting license](https://arize.com/docs/phoenix/self-hosting/license), [Langfuse OSS license](https://github.com/langfuse/langfuse-docs/blob/main/content/self-hosting/license-key.mdx)
6. **Nix for worker environments and OpenTofu for cloud resources.** Add Crossplane only if Kubernetes becomes an intentional platform boundary. These tools declare infrastructure and environments; they do not declare company goals, authority, or agent behavior. [Nix](https://nixos.org/), [OpenTofu](https://opentofu.org/docs/intro/), [Crossplane Compositions](https://docs.crossplane.io/latest/composition/compositions/)

## Requirements matrix for serious finalists

Legend: **Yes** = directly documented; **Partial** = useful subset, integration, or deployment-limited; **No** = not the product's responsibility; **Risk** = material maturity/security caveat. This is a requirements fit matrix, not a product-quality score.

| Candidate | Company / portfolio model | Declarative portable package | Task / approval authority | Durable waits / recovery | Runtime / model neutral | Sandbox / identity / policy | SDLC | Business workflows | Evals / observability | Deployment / economics | Maturity boundary |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Paperclip | **Yes**: companies, goals, org charts, budgets | **Yes**: company packages | **Yes**: tasks, approvals, heartbeats | Partial | **Yes**: adapters | Partial; provider-dependent | Partial | **Yes** | Partial | MIT, local | **Risk**: many 2026 advisories; lab-only until fixed-version security validation |
| Fusion | Partial: mission/control views | Partial | **Yes**: triage/executor/reviewer/merger flow | Partial | **Yes**: numerous agents/providers/ACP | Partial; external runtimes | **Yes** | No | Partial | MIT, local binaries/npm | Young project; independent security/multi-tenant evidence not established |
| GitHub + `gh-aw` | Portfolio through orgs/repos/projects | **Yes**: Markdown/YAML workflows | **Yes** inside repo/Actions permissions | Partial: Actions retries/events, not general durable execution | **Yes**: multiple agent engines | **Yes** for GitHub permission/safe-output boundary | **Yes** | Partial | Actions logs/cost controls | Free or $4/user/month Team; preview extension | GitHub mature; `gh-aw` public preview |
| GitLab + Duo Agent Platform | Groups/projects/epics/portfolio | **Yes**: CI/flows/config | **Yes** inside GitLab roles/flows | Partial | Partial: GitLab agent/model surfaces | Strong product governance tiers | **Yes** | Partial | Built-in SDLC/credit metering | Free; Premium $29/user/month; self-managed available | Core platform mature; agent platform version/credit dependent |
| Dapr Agents | No company model | Code/config, portable components | Partial: hooks and HITL | **Yes** | **Yes** | **Yes**: cryptographic identity/component policies | No | **Yes** | **Yes** | OSS/self-host; cloud-neutral | **GA / production-ready v1.0** |
| Temporal | No | Workflow code, namespaces | **Yes** within workflow | **Yes** | **Yes** | Partial; platform security + application controls | No | **Yes** | **Yes** | OSS or Cloud; AWS plan $100/month + actions | Mature durability substrate |
| Hatchet | No | SDK workflows | **Yes** within workflow | **Yes** | **Yes** | Partial; enterprise governance tiers | No | **Yes** | **Yes** | Free managed tier; Team $500/month; self-host support is Enterprise | Active releases; v1 engine, substantial but smaller ecosystem |
| Kestra | No | **Yes**: YAML, Git, versioned flows | **Yes** within flow | **Yes**: long-running state, retries/backfills | **Yes**: language/tool neutral | Governance mostly Enterprise | Partial | **Yes** | **Yes** | Apache-2.0 OSS; Cloud/Enterprise quote | OSS described as production-ready; enterprise gates governance |
| OpenShell + NemoClaw | No | **Yes**: YAML policies/versioned blueprints | Operator policy/approval, not task authority | Snapshots/recovery are substrate capabilities | **Yes** at OpenShell; NemoClaw has tested list | **Yes**: principal value | No | No | Runtime observability, not eval lab | Apache-2.0/local; no hosted SaaS | **Alpha/single-player**; NemoClaw early preview |
| AWS AgentCore | No | Partial: CDK/SDK deployment | Partial: policy/identity controls | **Yes**: runtime/memory/services | **Yes**: framework/model neutral | **Yes**: identity, Cedar policy, gateway | No | **Yes** | **Yes**: observability/evals | Managed usage pricing; AWS coupling | GA modules; strongest managed substrate, not a company control plane |
| LangGraph Platform / LangSmith | No | Agent graphs/config | **Yes** inside graph/HITL | **Yes** | Partial: LangChain ecosystem but model broad | Partial | No | **Yes** | **Yes**: core strength | Developer free; Plus $39/seat + usage; Enterprise hybrid/self-host | Managed platform mature enough for pilots; ecosystem coupling |
| CrewAI AMP | Teams/crews, not company portfolio | Crew/flow code | **Yes** inside flow | Partial | **Yes** | Enterprise governance/deployment | No | **Yes** | **Yes** | Basic free, 50 workflow executions/month; Enterprise private deployment | Useful business-agent layer; not durable authority or SDLC system |

Matrix sources: [Paperclip](https://github.com/PaperclipAI/paperclip), [Fusion](https://github.com/Runfusion/Fusion), [`gh-aw`](https://github.github.com/gh-aw/), [GitLab Duo Agent Platform](https://docs.gitlab.com/user/duo_agent_platform/), [Dapr Agents](https://docs.dapr.io/developing-ai/dapr-agents/dapr-agents-introduction/), [Temporal](https://docs.temporal.io/), [Hatchet](https://github.com/hatchet-dev/hatchet), [Kestra](https://kestra.io/pricing), [OpenShell](https://github.com/NVIDIA/OpenShell), [AgentCore](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/what-is-bedrock-agentcore.html), [LangSmith pricing](https://www.langchain.com/pricing), [CrewAI pricing](https://crewai.com/pricing).

## Layer-by-layer evidence

### 1. Repository, SDLC, and agentic work

#### GitHub / Actions / `gh-aw`

- **Documented:** `gh-aw` compiles natural-language Markdown/YAML workflows into GitHub Actions. It supports multiple agent engines, a read-only default, safe output mechanisms, network controls, threat detection, and cost controls. It is therefore an unusually good declarative repository-automation surface. [`gh-aw` docs](https://github.github.com/gh-aw/)
- **Status:** GitHub Agentic Workflows entered public preview on 2026-06-11. It should not be treated as the one durable orchestration authority. [announcement](https://github.blog/changelog/2026-06-11-github-agentic-workflows-is-now-in-public-preview/)
- **Economics:** GitHub Free is $0 and Team is $4/user/month. Included hosted Actions usage is plan-dependent; public standard hosted-runner work remains free. Current hosted Linux pricing begins at $0.002/minute for one core and $0.006/minute for two cores. [plans](https://github.com/pricing), [included usage](https://docs.github.com/en/billing/reference/product-usage-included), [runner pricing](https://docs.github.com/en/billing/reference/actions-runner-pricing)
- **Important correction:** GitHub announced, then postponed, the proposed $0.002/minute control-plane charge for self-hosted Actions. Do not budget it as an active charge. [GitHub's updated announcement](https://github.blog/changelog/2025-12-16-coming-soon-simpler-pricing-and-a-better-experience-for-github-actions/)
- **Inference:** Pay for GitHub Team only when private-team permissions or collaboration require it. Use Actions/`gh-aw` as an SDLC executor and event surface; keep cross-project admission, leases, approval grants, and promotion receipts in the platform's neutral authority layer.

#### GitLab

- **Documented/economics:** Free is $0 with 400 shared-runner compute minutes and unlimited use of a customer's own runners; Premium is $29/user/month billed annually with 10,000 minutes and a promotional $12 of monthly GitLab Credits per user. Ultimate is custom. [GitLab pricing](https://about.gitlab.com/pricing/)
- **Agent platform:** GitLab Duo Agent Platform is credit-metered and can be enabled on GitLab.com Free. Free namespaces can buy a monthly commitment pool without buying Premium/Ultimate; on-demand standard rate is $1/credit where available. [credits](https://docs.gitlab.com/subscriptions/gitlab_credits/), [availability](https://docs.gitlab.com/user/duo_agent_platform/turn_on_off/)
- **Inference:** GitLab is the strongest all-in-one alternative if consolidating source, CI/CD, planning, security, and agent flows is worth a migration. It is not a cheap add-on to a GitHub-centered system: Premium for a team costs far more than GitHub Team, and the agent layer remains consumption-metered.

#### OpenHands

- **Documented:** The core agent, CLI, SDK, agent server, and local GUI are MIT. OpenHands Cloud adds shared integrations and collaboration; Enterprise adds VPC/Kubernetes deployment, RBAC, and centralized controls. [OpenHands repository](https://github.com/OpenHands/OpenHands)
- **License boundary:** The separate Cloud application repository uses PolyForm Free Trial and permits evaluation for 30 days per calendar year without a commercial license. [OpenHands Cloud repository](https://github.com/OpenHands/OpenHands-Cloud)
- **Inference:** Reuse the MIT SDK/runtime or evaluate Cloud; do not mistake the source-available Cloud UI for unrestricted OSS. OpenHands is a capable coding worker, not the company/task authority.

#### Hermes

- **Documented/status:** Hermes Agent is MIT and provider/model extensible, with active signed releases; the current official release page shows v0.18.2 in July 2026. [repository](https://github.com/NousResearch/hermes-agent), [releases](https://github.com/NousResearch/hermes-agent/releases)
- **Inference:** Hermes remains a practical default local/general worker because it is replaceable and broad. Its memory, scheduler, messaging, or approval conveniences must not become the canonical company ledger or supersede controller authority.

### 2. Company and factory control planes

#### Paperclip

- **Documented:** Paperclip models companies, goals, org charts, agents, budgets, tasks, adapters, approvals, and heartbeat execution. Its companion company-package repository defines a portable package with `COMPANY.md`, agent definitions, skills, and metadata. Both are MIT. [Paperclip](https://github.com/PaperclipAI/paperclip), [company packages](https://github.com/paperclipai/companies)
- **Security evidence:** Paperclip's advisory page lists critical cross-tenant key/IDOR issues, unauthenticated RCE, command injection, DNS-rebinding RCE, and tool/skill exfiltration concerns. The unauthenticated RCE is fixed in `2026.416.0`, but a single patched advisory does not clear the complete threat surface. [all advisories](https://github.com/paperclipai/paperclip/security/advisories), [RCE advisory](https://github.com/paperclipai/paperclip/security/advisories/GHSA-68qg-g8mg-6pr7)
- **Inference:** This is the closest existing semantic/control-plane fit and should be studied or adapted, not rewritten from screenshots. It should be evaluated only on a pinned, advisory-cleared version with synthetic data, isolated credentials, restricted egress, and explicit tests for tenant and approval boundaries.

#### Runfusion / Fusion

- **Documented:** Fusion is MIT and describes a software factory with multi-node agents, worktrees, planning, execution, review/merge/ship stages, a board/mission-control UI, and numerous provider/agent adapters including Hermes and ACP. It publishes signed platform binaries and npm packages with provenance. [repository](https://github.com/Runfusion/Fusion), [release process](https://github.com/Runfusion/Fusion/blob/main/RELEASING.md)
- **Status evidence:** The repository has active beta/stable release tracks, but first-party public evidence does not establish the multi-tenant security or production adoption needed for it to become final authority. [releases](https://github.com/Runfusion/Fusion/releases)
- **Inference:** Fusion is a stronger candidate than building a fresh SDLC coordinator. Test whether its task/review/merge pipeline can sit behind the platform's admission and receipt contracts. Do not compose Fusion and Paperclip as two equal schedulers; choose one owner or narrow each to non-overlapping authority.

### 3. Secure execution and gateways

#### OpenShell / NemoClaw

- **Documented:** OpenShell is Apache-2.0 and provides sandboxed execution, declarative YAML policies, credential providers/routing, and deny-by-default network/filesystem controls. It supports multiple agent CLIs/runtimes. [OpenShell repository](https://github.com/NVIDIA/OpenShell)
- **Status:** OpenShell explicitly calls itself alpha, single-player software. NemoClaw is also alpha/early preview and has no hosted SaaS or production SLA. [OpenShell status](https://github.com/NVIDIA/OpenShell), [NemoClaw matrix](https://docs.nvidia.com/nemoclaw/user-guide/hermes/reference/platform-support)
- **Hermes and Mac evidence:** NemoClaw lists Hermes as tested with dedicated CLI, manifest, Dockerfile, and E2E lanes, while saying production parity with OpenClaw is not asserted. Apple Silicon with Colima/Docker Desktop is tested with limitations. [support matrix](https://docs.nvidia.com/nemoclaw/user-guide/hermes/reference/platform-support)
- **Policy evidence:** NemoClaw applies deny-by-default networking and an agent-specific Hermes baseline; unlisted destinations require operator approval. [network policies](https://docs.nvidia.com/nemoclaw/user-guide/hermes/reference/network-policies)
- **Inference:** This is the best-aligned local runtime-security substrate found, but its alpha boundary means phased shadow execution and hostile-input testing, not immediate credential-bearing production use.

#### E2B

- **Documented:** E2B supplies model-neutral Firecracker microVM sandboxes with command/file/internet APIs and managed cloud execution. Enterprise offers self-host/BYOC/on-prem deployment. [E2B](https://e2b.dev/), [SDK reference](https://e2b.dev/docs/sdk-reference/js-sdk/v2.10.5/sandbox)
- **Economics:** Hobby is free plus usage and includes a one-time $100 credit, one-hour sessions, and 20 concurrent sandboxes. Pro is $150/month plus usage with 24-hour sessions and 100 concurrent sandboxes. Compute is per second; current list price starts at $0.000014/vCPU-second plus $0.0000045/GiB-second. [pricing](https://e2b.dev/pricing)
- **Inference:** E2B is the managed-cloud escape hatch when local OpenShell cannot meet isolation or elasticity needs. It is not the first choice for an Apple-Silicon-first local factory because every sandbox becomes a metered external dependency.

#### agentgateway

- **Documented:** agentgateway is Apache-2.0, Linux Foundation/AAIF-governed gateway software for HTTP/gRPC, LLM, MCP, and A2A traffic, with JWT/RBAC, rate limiting, policy, tracing, and a developer portal. [documentation](https://agentgateway.dev/docs/standalone/latest/about/introduction/)
- **Inference:** Add it only when there are several networked tool/agent endpoints requiring centralized transport policy. It does not replace a sandbox, workflow authority, or company ledger.

### 4. Durable workflows and business automation

#### Dapr Agents

- **GA evidence:** Dapr Agents v1.0 is explicitly GA and production-ready. It combines agent identity, durable/stateful workflow execution, messaging, observability, hooks, and HITL with Dapr's portable components. [Dapr Agents](https://docs.dapr.io/developing-ai/dapr-agents/), [introduction](https://docs.dapr.io/developing-ai/dapr-agents/dapr-agents-introduction/)
- **Inference:** This is the most important new OSS candidate in the refresh. It may satisfy the portable lifecycle substrate better than building around an agent-framework-specific graph engine. A proof should test replay, idempotency, cancellation, external approvals, exact receipt binding, and host failure—not chatbot quality.

#### Temporal

- **Documented:** Temporal provides durable workflow execution with event histories, retries, timers, signals, and recovery. Temporal Cloud manages the service while application workers run in the customer's environment. [Temporal docs](https://docs.temporal.io/), [Temporal Cloud](https://temporal.io/cloud)
- **Economics:** The official AWS Marketplace route advertises a $100/month plan plus $50 per million actions, before storage/egress/support variables. [AWS Marketplace route](https://temporal.io/get-cloud/aws-marketplace)
- **Inference:** Choose Temporal when maximum durability maturity is worth operational or SaaS cost. Do not also let Dapr, Hatchet, Prefect, Kestra, LangGraph, Paperclip, and GitHub Actions each own the same retry/cancellation state machine.

#### Hatchet

- **Documented:** Hatchet is an open-source durable orchestration engine for background tasks and AI agents, with workflow signaling, durable sleep, cancellation/replay, SDKs, and an active release stream. [repository](https://github.com/hatchet-dev/hatchet), [releases](https://github.com/hatchet-dev/hatchet/releases)
- **Economics:** Developer Cloud is free with the first 100,000 task runs included, then $10/million. Team is $500/month plus usage; self-host support/BYOC is positioned in Enterprise. [pricing](https://hatchet.run/pricing)
- **Inference:** Excellent managed prototype economics, but the jump to a supported team deployment is large. It should win only on a measured simplicity/latency/operations bakeoff against Dapr/Temporal.

#### Prefect

- **Documented/economics:** Prefect has an open-source self-hosted server and a managed Hobby tier with two users, five deployments, 500 serverless minutes, and seven-day retention. Starter is $100/month; Team is $100/user/month. [pricing](https://www.prefect.io/pricing), [OSS comparison](https://www.prefect.io/compare/prefect-oss)
- **Inference:** Strong for Python/data/operational flows; less naturally aligned to company/agent authority than Dapr or Temporal. Use only if the real workloads are mostly Python pipelines.

#### Kestra

- **Documented:** Kestra OSS is Apache-2.0, declarative/event-driven, Git-versioned, tool/language-neutral, and supports long-running workflows, retries, backfills, failure handling, UI topology, and more than a thousand plugins. Enterprise adds RBAC, SSO, audit, secrets, multi-tenancy, and HA; Cloud is quote/pay-as-you-scale. [pricing and feature comparison](https://kestra.io/pricing)
- **Inference:** Kestra is the best fit here for non-code/business/infrastructure pipelines that operators must also understand visually. Governance gates make it less attractive as a zero-cost secure multi-user authority.

### 5. Evaluations, traces, and bounded improvement

#### Inspect AI

- **Documented:** Inspect AI is the UK AI Security Institute/Meridian open-source evaluation framework, with a large evaluation catalog, many provider integrations, agent bridges (including Claude Code, Codex, and Gemini), sandbox backends, logging, and a web viewer. [official documentation](https://inspect.aisi.org.uk/)
- **Economics/inference:** There is no platform subscription; model and compute costs remain. Use it for reproducible benchmark/evaluation jobs and independent candidate testing.

#### Promptfoo

- **Documented/economics:** Community is free and supports local/self-hosted evaluations, providers, assertions, and red-team testing; the pricing page currently includes 10,000 red-team probes/month. Enterprise/on-prem is custom. [pricing](https://www.promptfoo.dev/pricing/)
- **Inference:** Use for deterministic prompt/model/regression matrices and adversarial gates. Avoid letting its pass/fail output alone promote a material candidate; bind results to exact inputs and require calibrated human/model review where appropriate.

#### Phoenix

- **Documented/license:** Phoenix is ELv2 rather than OSI open source, but Arize permits free self-hosting without feature gates. Managed AX Free includes 25,000 spans/month, 1 GB/month, and 15-day retention; Pro is $50/month. [self-hosting license](https://arize.com/docs/phoenix/self-hosting/license), [pricing](https://phoenix.arize.com/pricing/)
- **Inference:** Good local trace/eval UI with low managed-upgrade cost. ELv2 matters mainly if reselling/hosting it as a service.

#### Langfuse

- **Documented/license:** All core Langfuse features/APIs are MIT without limits; enterprise features such as fine-grained RBAC, audit logs, retention policy, server-side masking, and SCIM require a license. [self-host licensing](https://github.com/langfuse/langfuse-docs/blob/main/content/self-hosting/license-key.mdx)
- **Economics:** Cloud Hobby is free with 50,000 units/month, 30-day access, and two users; Core is $29/month, Pro $199/month. [pricing](https://langfuse.com/pricing)
- **Inference:** Prefer Langfuse OSS when OpenTelemetry-oriented traces, prompt management, datasets, and collaborative annotation should be one local surface. Do not deploy both Phoenix and Langfuse until a concrete missing workflow justifies the duplication.

### 6. Portals and platform engineering

#### Backstage

- **Documented:** Backstage is an open-source developer portal framework centered on a software catalog and software templates. [official site](https://backstage.io/)
- **Inference:** It is a UI/catalog framework, not an autonomous company controller. Adopt only after the resource/project catalog is stable enough to justify maintaining a portal.

#### Port

- **Documented/economics:** Port is SaaS. Free has up to 15 seats, 10,000 entities, 400 runs, and limited AI-agent use with no time limit. Basic begins at $30/seat/month (sold as a 50-seat package); Standard at $40/seat/month. Dedicated tenancy/Private Link are Enterprise options. [pricing](https://www.port.io/pricing)
- **Inference:** The free tier is valuable for a portal/catalog proof-of-concept, but its paid floor and SaaS data/control-plane dependency make it unsuitable as foundational authority for a one-person local-first platform.

#### Humanitec

- **Documented:** Humanitec Platform Orchestrator consumes workload/resource specifications (including Score) and provisions resources through drivers. [Platform Orchestrator overview](https://developer.humanitec.com/platform-orchestrator/docs/platform-orchestrator/overview/), [Score specification](https://score.dev/)
- **Inference:** Evaluate when application-environment provisioning becomes the bottleneck. It does not provide company goals, agent task authority, or evaluation/evolution.

### 7. Declarative infrastructure and reproducibility

#### Nix

- **Documented:** Nix/NixOS is free software for reproducible, declarative builds and system configuration, with rollback and Linux/macOS support. [Nix](https://nixos.org/), [ecosystem](https://wiki.nixos.org/wiki/Nix_Ecosystem)
- **Inference:** Use Nix to make worker/tool environments reproducible on the M1 Max and Linux hosts. It complements, rather than replaces, container/sandbox policy.

#### OpenTofu

- **Documented:** OpenTofu is a Linux Foundation open-source infrastructure-as-code tool with providers, modules, state, and reusable/versioned configuration. [introduction](https://opentofu.org/docs/intro/)
- **Inference:** Use it for cloud/SaaS/network resources. Keep secrets and live state outside repository source, and treat plans as proposed effects rather than authority to apply.

#### Crossplane

- **Documented:** Crossplane Compositions create reusable composite resources through Kubernetes APIs. [Compositions](https://docs.crossplane.io/latest/composition/compositions/)
- **Inference:** Powerful only after Kubernetes is a deliberate substrate. Introducing Kubernetes merely to obtain Crossplane would be over-engineering for the present local-first factory.

### 8. Managed agent substrate

#### AWS Bedrock AgentCore

- **Documented/GA:** AgentCore exposes modular Runtime, Memory, Gateway, Identity, Policy, Observability, Evaluations, and Optimization. AWS describes it as framework- and model-neutral; modules can be adopted separately. [overview](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/what-is-bedrock-agentcore.html)
- **Economics:** AgentCore Runtime pricing is usage-based; AWS's GA Harness announcement lists $0.0895/vCPU-hour and $0.00945/GB-hour, with model, memory, gateway, and observability charges separate. [GA/pricing example](https://aws.amazon.com/blogs/machine-learning/amazon-bedrock-agentcore-harness-is-now-generally-available-go-from-idea-to-production-grade-agent-in-minutes/)
- **Inference:** This is the strongest managed modular production substrate in the shortlist. Use only for workloads that need AWS-grade elasticity/security/compliance; do not migrate the canonical company/task ledger or local-first workflow solely to consume it.

#### LangSmith / LangGraph Platform

- **Documented/economics:** LangSmith Developer is free with 5,000 base traces but no deployment. Plus is $39/seat/month plus usage and includes one small serverless deployment; Enterprise offers custom hybrid/self-hosted options. [pricing](https://www.langchain.com/pricing)
- **Inference:** This is a fast way to deploy and observe LangGraph agents, but it couples workflow semantics to the LangChain ecosystem and overlaps the durable/eval layers. Use for an application-level graph that clearly benefits, not as the universal factory authority.

#### CrewAI AMP

- **Documented/economics:** Basic is free with 50 workflow executions/month and two automations. Enterprise offers private cloud/VPC/self-hosted deployment and governance. [pricing](https://crewai.com/pricing), [enterprise docs](https://docs.crewai.com/enterprise/introduction)
- **Inference:** Attractive for quick business-agent workflows; not a durable SDLC/company control plane. Retain only as a replaceable application framework if a concrete workflow is materially faster to implement with crews/flows.

## Recommended spend and deployment split

### Self-host now (no platform subscription)

- Canonical provider-neutral authority/contracts in `agent-platform`; keep it thin.
- Hermes workers, with provider/model choice externalized.
- Nix worker environments; OpenTofu only for real external resources.
- Inspect AI + Promptfoo and **one** of Langfuse OSS or Phoenix.
- Dapr Agents proof for durable lifecycle. Temporal OSS/Kestra/Prefect are alternatives, not simultaneous authorities.
- agentgateway only after multiple MCP/A2A/network endpoints create a real policy problem.
- OpenShell/NemoClaw only in an alpha shadow lane until security and recovery tests pass.

### Use free tiers for evidence-producing trials

- GitHub Free + public Actions, or included private minutes.
- GitLab Free in a migration comparison, including purchased credits only if a bounded flow warrants it.
- Hatchet Developer for durability/operations comparison.
- LangSmith Developer for traces only; it does not include deployment.
- CrewAI Basic for a bounded non-code workflow.
- E2B Hobby credit for cloud-sandbox comparison.
- Port Free for portal/catalog UX only.
- Langfuse Hobby or Phoenix AX Free when external managed observability is useful.

### Low-cost subscriptions justified by a measured bottleneck

- **GitHub Team: $4/user/month** for private-team controls and the existing native SDLC surface.
- **GitHub Copilot individual plan:** only if its included AI credits/cloud coding agent reduce measured delivery time; monitor both AI-credit and Actions consumption because code review consumes both. [Copilot plans](https://github.com/features/copilot/plans), [billing change](https://github.blog/changelog/2026-06-01-updates-to-github-copilot-billing-and-plans/)
- **Langfuse Core: $29/month** or **Phoenix Pro: $50/month**, not both, when retention/collaboration saves more operations time than self-hosting.
- **LangSmith Plus: $39/seat/month** only if LangGraph deployment becomes an intentional application layer.
- **Temporal Cloud: starting route around $100/month** only after the durability proof shows that managed operations are worth it.
- **Prefect Starter: $100/month** only for a Python-pipeline-heavy workload.

### Defer or require an explicit enterprise case

- GitLab Premium ($29/user/month), Port paid plans, E2B Pro ($150/month), Hatchet Team ($500/month), Langfuse Pro ($199/month), CrewAI Enterprise, Humanitec, AgentCore at production scale, and enterprise governance tiers.
- Backstage until catalog ownership stabilizes.
- Crossplane until Kubernetes exists for independent reasons.
- Paperclip/Fusion credential-bearing production authority until exact-version security review, recovery testing, and authority-boundary tests pass.

## First-principles adoption decision

The correct answer is neither “build everything” nor “adopt one platform wholesale.” No candidate spans company goals and budgets, declarative packages, one authoritative task/lease/approval state machine, durable recovery, secure runtime policy, both code and business workflows, trace/evaluation-driven evolution, and portable deployment without important gaps or lock-in.

The differentiating platform work should therefore be limited to:

1. A canonical domain and authority contract: project/company, goal, task, lease, effect class, approval grant, candidate, receipt, review, and promotion.
2. Adapters that translate those contracts to one chosen controller/runtime per layer.
3. Exact-revision receipts and reconciliation across GitHub/GitLab, durable workflow history, sandboxes, and evaluators.
4. An offline evolution lab that proposes versioned changes, runs deterministic and model evaluations, and requires independent exact-candidate review before promotion.

Everything beneath that seam should be adopted, extended, or replaced through measured bakeoffs. The immediate research priority is a three-way vertical slice:

- Paperclip versus Fusion for operator/company/SDLC control-plane UX;
- Dapr Agents versus Temporal/Hatchet for one durable lifecycle authority;
- OpenShell/NemoClaw versus E2B for local versus managed sandbox/security.

The slice should run the same accepted task through admission, lease, execution, pause/approval, crash recovery, independent review, and exact-head promotion. That evidence will decide composition. Feature-count comparisons will not.
