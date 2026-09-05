# Whole Orchestration Landscape, With Conductor

**Evidence cutoff:** 2026-08-30  
**Scope:** durable-execution engines, microservice and business-process orchestrators, developer workflow services, data/DAG orchestrators, cloud state machines, and agent-native graph runtimes.  
**Question:** Which existing system can execute admitted work beneath a separate company/work authority, without forcing the platform to rebuild durability, retries, waits, signals, scheduling, versioning, or operations?

## Method and terminology

Only official documentation, repositories, releases, pricing pages, and first-party security/licensing pages are used. A vendor saying “durable,” “exactly once,” or “production-ready” is recorded as its documented contract, not treated as independent proof of every failure mode.

The category contains materially different execution models:

- **Deterministic replay:** workflow code is re-executed against a persisted event history; code must obey determinism/versioning constraints. Temporal, Dapr Workflow, and Azure Durable Functions are in this family.
- **Persisted graph/state machine:** the engine persists each graph/task transition and resumes from stored state; it does not replay arbitrary orchestration code. Conductor, Camunda/Zeebe, Step Functions, Google Workflows, Kestra, Airflow, and Argo are in this family.
- **Step memoization/checkpointing:** ordinary code is re-entered or resumed while completed step results are reused. Inngest, Trigger.dev, DBOS, Restate, and LangGraph vary substantially within this family.
- **Job/DAG scheduling:** the primary contract is task dependencies, schedules, assets, backfills, or infrastructure jobs—not an indefinitely interactive business process. Airflow, Dagster, Prefect, Argo, and much of Kestra live here.

“Replay” is therefore not one interchangeable feature. Conductor's restart/rerun/retry controls, for example, are operational re-execution controls; Temporal's replay reconstructs workflow state from an event history; LangGraph time travel intentionally re-executes nodes after the chosen checkpoint, including model/API calls. [Conductor repository](https://github.com/conductor-oss/conductor), [Temporal documentation](https://docs.temporal.io/), [LangGraph persistence](https://docs.langchain.com/oss/python/langgraph/persistence)

## Conclusion

Conductor was underweighted in the earlier agent-platform comparison. Current Conductor OSS is an actively maintained Apache-2.0 continuation of Netflix Conductor, not the abandoned Netflix repository. It is a first-round hypothesis for a **separate, declarative, inspectable execution substrate** because it keeps orchestration in versioned JSON graphs, allows polyglot/stateless workers, persists every step, supports months-long waits, signals, human tasks, dynamic forks, schedules, retries, compensation patterns, and operational restart/rerun controls, while avoiding deterministic-code replay constraints. The comparative fit remains unproved until the common fault, security, versioning, operations, and cost fixtures run. [current Conductor OSS](https://github.com/conductor-oss/conductor), [workflow overview](https://orkes.io/content/developer-guides/workflows), [task catalog](https://orkes.io/content/developer-guides/tasks)

That does not make it an automatic winner:

- Conductor OSS is a substantial Java service with persistence/indexing infrastructure. Its community edition does not document the same tenant/security/control surface as Orkes Enterprise.
- Temporal supplies a long-running event-history/replay and workflow-versioning reference implementation for correctness-critical code workflows; whether that translates into the strongest fit here is a bake-off question.
- Dapr Workflow/Agents now offers an unusually strong portable open-source alternative, including multi-application workflows, access policies, durable external events/timers/retries, history propagation, and cryptographic history signing.
- Restate and DBOS are lighter modern entrants worth measuring: Restate combines a durable journal, RPC, stateful objects, and durable promises; DBOS embeds durability in the application/Postgres and documents exactly-once transactions when application writes and durability records share a transaction.
- Camunda is stronger where BPMN, explicit human work queues/forms, audit, and business-process governance dominate, but current production licensing is enterprise-only.
- Inngest, Trigger.dev, Hatchet, and Windmill document low-friction developer experiences and inexpensive managed trials, but each carries narrower language, platform, governance, or control-plane assumptions.

The practical shortlist for a controlled vertical slice is therefore **Conductor OSS, Dapr Workflow/Agents, Temporal, and Restate or DBOS**. Evaluate all against the same externally owned task/lease/approval/receipt contract. Do not adopt more than one as lifecycle authority for the same execution.

## Conductor first: corrected assessment

### Lineage and maintenance

- Netflix created Conductor for workflows spanning microservices. Netflix stopped maintaining its GitHub repository on 2023-12-13 and retained an internal fork. That archived repository is Apache-2.0 but is not the current project. [Netflix repository notice](https://github.com/netflix/conductor)
- The current `conductor-oss/conductor` repository says it is the continuation of the original Netflix project, actively maintained by Orkes and the community. It is Apache-2.0, has current releases, supports a one-command CLI/local server, and publishes a Docker image with UI. [repository](https://github.com/conductor-oss/conductor), [releases](https://github.com/conductor-oss/conductor/releases), [license](https://github.com/conductor-oss/conductor/blob/main/LICENSE)
- The latest stable release at the cutoff is v3.32.1 (2026-08-12). v3.32.2 release candidates and a warning-labeled Spring Boot 4 v4.0.0 alpha existed later in August; those are not equivalent to stable. [v3.32.1](https://github.com/conductor-oss/conductor/releases/tag/v3.32.1), [v4 alpha](https://github.com/conductor-oss/conductor/releases/tag/v4.0.0-alpha.1)
- Maturity is active but not risk-free: v3.32.1 includes security fixes, and the official tracker contains an open security-hardening epic plus a reported OTLP startup regression. A proof should pin an exact stable version and run dependency/advisory and telemetry startup tests. [security-hardening epic](https://github.com/conductor-oss/conductor/issues/1010), [OTLP regression report](https://github.com/conductor-oss/conductor/issues/1534)
- **Correction:** “Netflix discontinued Conductor” is incomplete. Netflix discontinued its repository; Conductor OSS continued under a different maintained repository.

### Execution semantics

- Workflows are stored as versioned JSON definitions and may be authored through APIs, UI, BPMN import, or code-generating SDKs. Static and runtime-generated dynamic workflows are supported. [workflows](https://orkes.io/content/developer-guides/workflows)
- Every task/step is persisted. Configurable retries, timeouts, rate/concurrency limits, pause/resume/terminate, restart, rerun, and retry survive worker/server failures. Conductor makes the graph/state machine deterministic; workers remain ordinary code and need not be replay-deterministic. [Conductor README](https://github.com/conductor-oss/conductor)
- Worker task delivery is at-least-once. A worker may repeat a side effect after failure/recovery, so idempotency keys, effect receipts, or explicit compensation remain mandatory. Persisted workflow state is not an exactly-once external-effect guarantee. [durable-execution architecture](https://docs.conductor-oss.org/architecture/durable-execution.html)
- Control flow includes switch, loops, static and dynamic fork/join, sub-workflows, runtime-selected dynamic tasks, asynchronous starts, and synchronous sub-workflows. [tasks](https://orkes.io/content/developer-guides/tasks), [dynamic fork](https://orkes.io/content/reference-docs/operators/dynamic-fork), [sub-workflow](https://orkes.io/content/reference-docs/operators/sub-workflow)
- Long waits can stop until a timestamp/duration or signal. Human tasks pause for human input, while the signal API targets the first non-terminal `WAIT` task rather than an arbitrary task or `HUMAN` task; integrations must preserve that distinction. [task catalog](https://orkes.io/content/developer-guides/tasks), [signals](https://orkes.io/content/developer-guides/sending-signals-to-workflows)
- Compensation is modeled with `failureWorkflow` and explicit compensating workflows/tasks, not an ACID rollback guarantee. The documented saga pattern is retryable/eventually consistent and requires idempotent compensation. [saga compensation](https://docs.conductor-oss.org/devguide/cookbook/saga-compensation.html)

### Versioning, workers, and portability

- Workflow definitions have integer versions. Running executions remain pinned to the definition version with which they started; new versions do not mutate in-flight graphs. [Conductor README/versioning FAQ](https://github.com/conductor-oss/conductor), [workflow definition](https://orkes.io/content/developer-guides/workflows)
- Workers are polyglot and poll/execute/report through SDKs. The maintained repository lists Java, Python, JavaScript, Go, and C# SDKs, with Ruby and Rust incubating. Workers may run independently of the server. [SDK list](https://github.com/conductor-oss/conductor)
- OSS supports Docker/JVM deployment and multiple persistence/message backends. The official `conductoross/conductor:3.32.1` image metadata lists both `linux/amd64` and `linux/arm64`, establishing native M-series Docker packaging. This is not an Apple-specific production support/performance commitment. [repository quickstart](https://github.com/conductor-oss/conductor), [image metadata](https://hub.docker.com/v2/repositories/conductoross/conductor/tags/3.32.1)

### Operations, tenancy, security, and price

- OSS includes UI, metrics, inspectable task input/output/timing/retry history, restart/rerun controls, rate limits, task domains, and independent server/worker scaling. [repository](https://github.com/conductor-oss/conductor)
- The OSS API is open by default; official docs direct operators to put it behind a reverse proxy or custom Spring Security filter. It must not be exposed directly. [Conductor API security note](https://docs.conductor-oss.org/documentation/api/)
- Task domains and queue partitioning are operational isolation tools; they are not security tenancy or a first-class company boundary. Orkes positions detailed users/groups/service identities, granular resource/domain permissions, SSO, audit, secrets, encryption/BYOK, custom deployment, and up-to-99.99% SLA in Enterprise. [task domains](https://docs.conductor-oss.org/documentation/api/taskdomains.html), [Orkes access/security](https://docs.orkes.io/content/category/access-control-and-security), [Orkes pricing](https://developer.orkes.io/pricing)
- Orkes Developer Edition is a free, no-SLA, limited non-production browser sandbox; Enterprise is custom-priced. The local full Orkes stack is for development/testing and the FAQ says it requires an Orkes subscription/token. This is distinct from Apache-2.0 Conductor OSS, which can be self-hosted without Orkes. [Orkes pricing](https://developer.orkes.io/pricing), [installation choices](https://docs.orkes.io/content/get-orkes-conductor), [Orkes FAQ](https://orkes.io/content/faqs/general-faqs), [Conductor OSS](https://github.com/conductor-oss/conductor)

### Fit beneath separate authority

Conductor can cleanly remain an execution substrate if the external controller owns admission, company/project/task identity, leases, approval grants, effect classification, candidate hashes, review, and promotion. Map one admitted execution to one Conductor workflow ID/version; treat Conductor task state as execution evidence, not as permission to create or promote work. This separation also prevents Conductor's Human/Wait/approval conveniences from becoming a competing source of authority.

## Whole-landscape matrix

Legend: **Native** means a documented first-class capability; **Pattern** means implementable with documented primitives but owned by application code; **Limited** means constrained or not the product's primary contract. “Substrate fit” asks whether it can execute beneath a separate company/work authority without needing to own that authority.

| System | Durable state / replay model | Waits, signals, human work, compensation | Graphs, schedules, versioning | Languages / local operation | Tenancy, ops, security | Managed economics / license | Substrate fit |
|---|---|---|---|---|---|---|---|
| **Conductor OSS / Orkes** | Persisted task/graph state; restart/rerun/retry, not deterministic code replay | Native Wait, signal, Human, events; compensation is explicit pattern | JSON graphs, loops, dynamic fork/join, subflows, schedules, pinned workflow versions | Java/Python/JS/Go/C#; Ruby/Rust incubating; JVM/Docker local | OSS UI/metrics/domains; enterprise RBAC/security/SLA | OSS Apache-2.0/free; Orkes sandbox free, production custom | **High**: declarative engine stays separate from authority |
| **Temporal** | Deterministic event-history replay; durable timers/signals/updates; Continue-as-New | Native signals/updates/timers; human and saga compensation are code patterns | Dynamic code workflows, schedules, child workflows; Worker Versioning GA | Go/Java/TS/Python/.NET/PHP; Rust preview; local dev server/self-host | Namespaces, mTLS, rich UI/metrics; mature Cloud controls | OSS MIT; AWS route $100/mo + $50/million Actions and storage | **High hypothesis**: mature replay reference with more code/versioning discipline |
| **Cadence** | Deterministic event-history replay for long-running workflows | Signals/timers; human and compensation remain code patterns | Code workflows and schedules; Go/Java SDK center | Go/Java workers; Docker and self-hosted clusters | UI and production cluster tooling; multi-service backend | Apache-2.0/self-host | **High hypothesis** if its older, narrower ecosystem is acceptable |
| **Dapr Workflow / Agents** | Deterministic replay over actor-backed histories; durable reminders/retries | Native external events/timers; compensation documented; agent hooks/HITL | Code workflows, child/multi-app workflows, versioning; schedules through Jobs/bindings | .NET/Java/Python/Go/JS coverage varies by feature; self-host/cloud/K8s | Namespace scoping, allow-list workflow access policy, identity; signed/history propagation | Apache-2.0/self-host; managed infrastructure depends on host | **High**: broad portable substrate, but sidecar/component operations |
| **Restate** | Journaled durable invocations/steps, reliable RPC and stateful objects | Native awakeables and named durable promises; suspension; compensation is code pattern | Workflows, services, virtual objects, delayed calls; code evolution requires journal compatibility | TS/Java/Kotlin/Python/Go/Rust; macOS/Linux binaries, Docker | CLI/UI/metrics; service/object keys aid isolation, not company tenancy | OSS permissive/free; Cloud free 100k actions, Starter $75/mo | **High**: compact runtime plus messaging/state; younger operational history |
| **DBOS** | Postgres-backed checkpoints; recovery reuses recorded results; exactly-once app transaction when co-committed | Durable send/recv/events/timeouts; compensation/human UI are patterns | Code workflows, queues, schedules; no visual declarative business graph | Python/TS/Go/Java; local library + Postgres | OSS observability UI; distributed HA recovery benefits from licensed Conductor | Core library open source/free; DBOS Conductor/Console production is proprietary | **High for app-embedded durability**; external authority remains clean |
| **Hatchet** | Durable workflow/task state with retries, signals, sleep, replay/cancel | Native signaling/sleep; human/compensation patterns | Code workflows, branching, scheduling, cancellation/replay | Python/TS/Go plus other SDK activity; local/self-host | Managed multi-tenant controls; audit/SSO/self-host support higher tiers | Cloud free 100k runs, then $10/million; Team $500/mo | **High**, especially prototype; supported self-host economics less attractive |
| **Inngest** | Step results persisted/memoized; function re-entry skips completed steps | Native sleep, `waitForEvent`, invoke/cancel; human via events; compensation pattern | Events/webhooks/cron, conditional/parallel code; deployments tracked | TS/Python/Go; local dev server; function code runs on own compute | Multi-tenant flow control; advanced RBAC/audit Enterprise | Free 50k executions; Pro $99/mo; self-host source exists but Cloud is center | **Medium-high hypothesis**: low-friction app model, hosted control-plane preference |
| **Trigger.dev** | Checkpoint/freeze/restore of long-running task process | Native waits, webhook/HITL approval, retries; compensation pattern | Async code, subtask fan-out, schedules, atomic deployment versions | Primarily TypeScript; Python invoked inside tasks; CLI hot reload, Docker/K8s self-host | Environments/preview branches; RBAC/SSO/security reports Enterprise | Apache-2.0; Cloud free $5 credits, Hobby $10, Pro $50 + compute | **Medium-high** for TS agent jobs; narrower language/control semantics |
| **Windmill** | Job/flow persistence; workflow-as-code v2 documents checkpoint/replay | Many triggers; enterprise approval steps; compensation pattern | Visual/code flows, schedules, Git/IaC; dynamic scripts in many languages | Python/TS/Go/Bash/SQL and more; AGPL self-host Docker/K8s | Community limits workspaces/groups; advanced audit/SSO/OTel Enterprise | Free self-host unlimited executions; Enterprise starts $120/mo and itemized compute/seats | **Medium-high hypothesis** for operator/business automation; lifecycle fit requires testing |
| **Kestra** | Persisted executions with retries/backfills/failure handling | Native Pause/resume/HITL; events/schedules; compensation pattern | Declarative YAML, subflows, dynamic tasks, rich schedules/triggers, Git versioning | Language/tool neutral through tasks; Docker/K8s/on-prem | UI/observability OSS; RBAC/audit/multi-tenancy/HA Enterprise | Apache-2.0 OSS/free; Cloud/Enterprise quote | **Medium-high** for declarative cross-domain pipelines |
| **Prefect** | Persisted flow/task runs, retries, caching, events; not event-sourced replay | Pauses/automations/events available; human/compensation patterns | Dynamic Python flows, schedules/deployments; strong work-pool model | Python; very easy local OSS server/cloud hybrid | Workspaces/roles/audit higher plans; good UI | OSS Apache-2.0; Hobby free, Starter $100/mo | **Medium hypothesis** when workflows are Python/data/ops heavy |
| **Dagster** | Persisted run/asset event log, retries/re-execution; asset lineage | Sensors/schedules; human/long interactive waits not core | Software-defined assets/jobs, partitions/backfills, dynamic mapping | Python; OSS local, Docker/K8s | Strong data catalog/observability; enterprise governance in Plus | OSS Apache-2.0; Plus Solo $10/mo + credits, Starter $100/mo | **Low-medium** outside data/ML asset orchestration |
| **Apache Airflow** | Metadata DB records DAG/task runs; retry/re-run/backfill, not durable code replay | Sensors/deferrable operators/event scheduling; indefinite interactive human flow is not core | Python DAGs, dynamic generation/mapping, schedules, backfills; versioned DAG bundles | Python, broad operator ecosystem; Docker/Helm/local | Mature operational UI/RBAC; docs say full multi-tenancy is not yet supported | Apache-2.0/self-host; managed services separate | **Low-medium** for general factory; **high** for data DAGs |
| **Argo Workflows** | Kubernetes CRD workflow/task state, retries/artifact archive | Suspend/resume and events through Argo Events; compensation/human task UI patterns | YAML DAG/steps, templates, cron, loops/fan-out; GitOps natural | Container-native; local requires Kubernetes/Docker VM on Mac | Kubernetes RBAC/namespaces; strong cluster isolation, high ops burden | Apache-2.0/free self-host | **Medium** only if Kubernetes is already intentional |
| **Camunda 8 / Zeebe** | Persisted BPMN token/event state; replay/reprocessing is engine-internal | Native BPMN messages/timers, user tasks/forms, incidents; compensation events modeled | BPMN/DMN, subprocesses, events, schedules, model versioning | Java clients plus REST/gRPC/connectors; local dev available | Mature Tasklist/Operate/Optimize/Identity; enterprise security/governance | Local non-production free; all production self-managed/SaaS requires Enterprise quote | **High** for governed human/business process; economics gate |
| **Flowable OSS** | Persisted BPMN/CMMN case and process state | Native BPMN events, CMMN cases, human tasks, DMN decisions | Open-standard BPMN/CMMN/DMN models | Java/JDK 17+; embeddable or server deployment | OSS engines and modeling; commercial platform adds broader enterprise surfaces | Apache-2.0 OSS/free | **Medium-high hypothesis** for business/case workflows; agent/runtime fit requires measurement |
| **AWS Step Functions** | Managed persisted state machine; Standard exactly-once state execution, Express at-least-once | Wait/callback task tokens, retries/catch; saga patterns; limited native human UI | ASL JSON/YAML, Map/Parallel, EventBridge schedules; published state-machine versions/aliases | Any worker via AWS integrations/Lambda; no true self-host | IAM, CloudTrail/CloudWatch, account/region isolation | Standard 4k transitions/mo free then per transition; Express request+duration | **Medium-high** within AWS; strong lock-in |
| **Azure Durable Functions** | Deterministic orchestrator replay from history | Indefinite external events/timers; compensation pattern; at-least-once external events | Code orchestrations/suborchestrations/entities; schedules via Functions | .NET/JS/Python/Java/PowerShell support varies; local emulator/tooling | Azure identity/monitoring; task hubs as isolation boundary | Functions compute + storage + replay invocations; wait time not billed; Durable Task Scheduler options | **Medium-high** within Azure; storage/replay cost and determinism constraints |
| **Google Cloud Workflows** | Managed persisted declarative state machine | Sleep/poll/callback, IAM-protected callbacks, retries; human through callback pattern | YAML/JSON steps, loops/parallel/subworkflows; deploy revisions | HTTP/Google-service orchestration; no self-host | IAM, audit/Cloud Logging; project/region isolation | 5k internal + 2k external steps/mo free; then $0.01/$0.025 per 1k | **Medium-high** for HTTP/cloud APIs; one-year max and GCP lock-in |
| **LangGraph / LangSmith Deployment** | Per-step graph checkpoints; recovery/time travel; replay after checkpoint re-executes later nodes and effects | Native interrupts/resume indefinitely; compensation pattern | Stateful cyclic graphs, subgraphs, threads; managed registry/revisions/crons | Python/JS OSS; local checkpointers; managed/hybrid/self-host Enterprise | Agent-centric auth/tracing/evals; not general business multi-tenancy | OSS MIT; Developer $0 no deployment, Plus $39/seat + usage | **Medium**: application-level agent graph, not universal workflow authority |
| **CrewAI / AMP** | Flow state persistence and resumable agent/workflow execution, less formal durability contract | HITL/triggers/automations; compensation pattern | Crews/Flows, event listeners, schedules/automations | Python; local OSS; cloud/private enterprise options | Enterprise control plane/governance/deployment | OSS core; Basic free with 50 executions/mo; Enterprise quote | **Low-medium**: replaceable agent/application framework |
| **n8n** | Database-persisted node executions, retries/error workflows; queue mode | Webhooks/waits/forms/manual interactions; compensation pattern | Visual node graphs, schedules, large connector catalog; Git/environments paid | JS/Python code nodes; self-host Docker; custom nodes | Community security/collab limits; paid SSO/RBAC/audit/scaling | Sustainable Use License, not OSI OSS; Cloud €20/mo; self-host Business €667/mo annual | **Medium** for internal connector automation; licensing/authority/HA constraints |

Matrix sources: [Conductor](https://github.com/conductor-oss/conductor), [Temporal](https://docs.temporal.io/), [Cadence](https://github.com/cadence-workflow/cadence), [Dapr Workflow](https://docs.dapr.io/developing-applications/building-blocks/workflow/), [Restate](https://docs.restate.dev/tour/workflows), [DBOS](https://docs.dbos.dev/), [Hatchet](https://github.com/hatchet-dev/hatchet), [Inngest](https://www.inngest.com/docs), [Trigger.dev](https://trigger.dev/product), [Windmill](https://www.windmill.dev/pricing), [Kestra](https://kestra.io/pricing), [Prefect](https://www.prefect.io/pricing), [Dagster](https://dagster.io/pricing), [Airflow](https://airflow.apache.org/docs/), [Argo Workflows](https://argo-workflows.readthedocs.io/), [Camunda](https://camunda.com/pricing/), [Flowable OSS](https://www.flowable.com/open-source), [Step Functions](https://docs.aws.amazon.com/step-functions/latest/dg/choosing-workflow-type.html), [Azure Durable Functions](https://learn.microsoft.com/azure/azure-functions/durable/durable-functions-orchestrations), [Google Workflows](https://cloud.google.com/workflows/docs/overview), [LangGraph](https://docs.langchain.com/oss/python/langgraph/persistence), [CrewAI](https://docs.crewai.com/), [n8n](https://n8n.io/pricing/).

## Durable-execution finalists

### Temporal

- Workflow state is reconstructed by replaying deterministic workflow code against the event history. Activities isolate external effects; signals, updates, queries, child workflows, durable timers, schedules, retries, and Continue-as-New are mature primitives. [Temporal docs](https://docs.temporal.io/)
- Worker Versioning reached GA in March 2026; Worker Controller became GA in May 2026. Rust SDK and serverless workers remained preview at the cutoff, and new Cloud “Projects” and Custom Roles were pre-release. [Temporal 2026 changelog](https://temporal.io/changelog/product-area/cloud)
- Temporal Cloud runs the service while customer workflow/activity code stays in the customer's environment. The AWS Marketplace route lists $100/month plus $50/million Actions; storage and optional support/HA add cost. [Cloud architecture](https://temporal.io/cloud), [AWS pricing route](https://temporal.io/get-cloud/aws-marketplace)
- **Fit hypothesis:** a mature replay reference, but deterministic workflow rules and event-history/versioning discipline are real implementation constraints. Temporal supplies no first-class company portfolio, work-admission, or human task inbox; those correctly remain above it.

### Cadence

- Cadence remains an active Apache-2.0 event-history/replay engine for scalable,
  fault-tolerant, long-running workflows. Its backend supports
  Cassandra/MySQL/PostgreSQL, optional Kafka/Elasticsearch, Docker Compose,
  Kubernetes, UI, and Go/Java workflow workers. Its latest release at the cutoff
  was v1.4.0 in February 2026. [repository](https://github.com/cadence-workflow/cadence)
- **Fit hypothesis:** a direct replay-family comparator that should be explicitly
  considered, but its narrower SDK ecosystem and multi-service operations give
  no documented reason to place it in the first four before the primary
  Conductor/Dapr/Temporal/lightweight trials.

### Dapr Workflow and Dapr Agents

- Dapr Workflow uses actor state/reminders to persist history, retry after crashes, and replay orchestrator code. Durable timers may wait years, external events are buffered into history even when they arrive before the waiter, and child workflows have independent histories. [features](https://docs.dapr.io/developing-applications/building-blocks/workflow/workflow-features-concepts/), [architecture](https://docs.dapr.io/developing-applications/building-blocks/workflow/workflow-architecture/)
- Dapr documents code-level compensation/saga patterns, retry policies, versioning, multi-application workflows, workflow access policies, history propagation, and cryptographic history signing. [patterns](https://docs.dapr.io/developing-applications/building-blocks/workflow/workflow-patterns/), [workflow index](https://docs.dapr.io/developing-applications/building-blocks/workflow/), [multi-app](https://docs.dapr.io/developing-applications/building-blocks/workflow/workflow-multi-app)
- Dapr Agents v1.0 is explicitly GA/production-ready and builds agent identity, hooks/HITL, messaging, and collaboration on Dapr's workflow/state/observability capabilities. [Dapr Agents](https://docs.dapr.io/developing-ai/dapr-agents/)
- **Fit hypothesis:** a broad provider-neutral OSS substrate. The cost is operating sidecars/control plane/component stores and accepting uneven SDK parity for newer multi-app features.

### Restate

- Restate combines durable execution with reliable RPC, durable state, services, keyed virtual objects, and workflows. The official repository lists TypeScript, Java/Kotlin, Python, Go, and Rust SDKs and prebuilt macOS/Linux binaries. [repository](https://github.com/restatedev/restate)
- Awakeables and workflow-scoped durable promises survive crashes, suspend compute while waiting, and may be resolved/rejected through SDKs or HTTP—good primitives for webhooks and external approval. [external events](https://docs.restate.dev/develop/ts/external-events)
- Cloud Free includes 100,000 actions/month; Starter is $75/month for 5 million actions. Self-hosting is free under a permissive license. [pricing](https://restate.dev/pricing)
- **Fit hypothesis:** worth testing when durable workflows, stateful objects, and reliable service messaging should share one smaller runtime. Its operational history and business/operator UI must be compared directly rather than inferred.

### DBOS

- DBOS adds durable workflows and queues as a library backed by Postgres, with Python, TypeScript, Go, and Java support. Workflow recovery re-enters code and uses recorded step/transaction results. [documentation](https://docs.dbos.dev/), [recovery](https://docs.dbos.dev/production/workflow-recovery)
- A top-level `RunAsTransaction` can atomically commit application writes and the durability record, after which recovery replays the recorded output; ordinary steps cannot guarantee against the crash-after-write-before-checkpoint window. [transaction guarantee](https://docs.dbos.dev/golang/tutorials/transaction-tutorial)
- Workflow messages are persisted; sends from workflows can have exactly-once delivery semantics. [workflow communication](https://docs.dbos.dev/python/tutorials/workflow-communication)
- The core library can run without a separate workflow server. DBOS recommends its Conductor control plane for distributed recovery/HA and operational tooling, but self-hosted production Conductor/Console requires a proprietary license. This product is unrelated to Orkes/Netflix Conductor despite the shared name. [architecture](https://docs.dbos.dev/architecture), [DBOS Conductor licensing](https://docs.dbos.dev/production/hosting-conductor)
- **Fit hypothesis:** a compact application-embedded option for a Postgres-centered platform with documented exactly-once database-effect patterns. It is not a declarative operator-facing process graph.

### Hatchet

- Hatchet v1 documents conditional workflows, signals, durable sleep, stable REST operations, replay/cancel, queues and SDKs; its repository has active signed releases. [v1 design/status](https://github.com/hatchet-dev/hatchet/discussions/1348), [releases](https://github.com/hatchet-dev/hatchet/releases)
- Developer Cloud is free for the first 100,000 task runs and then $10/million; Team begins at $500/month, while BYOC/self-host support is Enterprise. [pricing](https://hatchet.run/pricing)
- **Fit:** very strong prototype ergonomics and clear AI/background-task focus. A direct failure/recovery/versioning test is more useful than assuming equivalence to Temporal from the word “durable.”

## Developer-centric and operator-centric alternatives

### Inngest

- Functions run on the customer's compute. Inngest coordinates them over HTTP, persists/memoizes step results, retries failed steps, and re-executes the function while skipping completed steps. Non-deterministic effects must be inside `step.run`. [execution model](https://www.inngest.com/docs/learn/how-functions-are-executed)
- Native primitives include `step.sleep`, `step.waitForEvent`, child invocation, cancellation, concurrency, throttling, batching, webhooks, events, and cron. Waits may last months without compute. [durable execution](https://www.inngest.com/platform/durable-execution), [events](https://www.inngest.com/docs/features/events-triggers)
- TypeScript, Python, and Go are documented. Cloud Hobby is free with 50,000 executions; Pro starts at $99/month for one million, and a five-step function consumes six executions (run plus steps). [docs](https://www.inngest.com/docs), [pricing](https://www.inngest.com/pricing)
- **Fit:** low-friction for web/serverless applications, but its hosted coordinator and execution-unit pricing should be compared under realistic agent loops.

### Trigger.dev

- Trigger.dev checkpoints long-running tasks, freezes during waits, resumes on the same code line, supports retries, idempotency keys, human approval/webhook callbacks, fan-out, schedules, environments, preview branches, and atomic task versions. [product](https://trigger.dev/product)
- It is Apache-2.0 and self-hostable with Docker/Kubernetes, but the primary SDK/task model is TypeScript; Python is run from TypeScript tasks through a build extension. [repository](https://github.com/triggerdotdev/trigger.dev), [pricing FAQ](https://trigger.dev/pricing)
- Cloud Free includes $5/month credit, 20 concurrent runs, and five users; Hobby is $10/month; Pro $50/month plus compute and invocation charges. [pricing](https://trigger.dev/pricing)
- **Fit:** strong for TypeScript-heavy agent/background jobs, not a general polyglot company factory authority.

### Windmill

- Windmill is AGPLv3, self-hosted, multi-language automation with scripts, visual flows/apps, many triggers, Git/IaC, and “workflows as code v2” checkpoint/replay. [self-host/license](https://www.windmill.dev/platform/self-host-content), [pricing/features](https://www.windmill.dev/pricing)
- Community self-host is free with unlimited executions but limits workspaces/groups and gates approval controls, advanced observability, dedicated workers, and many governance capabilities behind Enterprise. Enterprise pricing is itemized from a $120/month base plus seats/compute. [pricing](https://www.windmill.dev/pricing)
- **Fit:** credible operator-facing automation and internal-tool substrate. Its enterprise approval/governance gates matter if the factory must safely serve several companies/users.

### Kestra

- Kestra is Apache-2.0, declarative YAML, event-driven, Git-versioned, tool/language-neutral, and documents long-running workflows, retries, backfills, failure handling, topology UI, and a large plugin catalog. [pricing/features](https://kestra.io/pricing)
- Pause/resume supports manual approval and human-in-the-loop input. [pause/resume](https://kestra.io/docs/how-to-guides/pause-resume)
- RBAC, SSO, audit, secrets, worker groups, multi-tenancy, and HA are Enterprise; Cloud is managed/quote. [pricing](https://kestra.io/pricing)
- **Fit:** a strong declarative pipeline/business automation option, especially when operators need visual YAML workflows, but enterprise governance economics must be included.

### n8n

- n8n offers a broad visual connector/workflow system, webhooks, schedules, retries, error flows, and self-hosting. Community is source-available under the Sustainable Use License, not OSI open source. Client-hosted/client-accessible and embedded uses can require commercial/Embed licensing. [license guidance](https://support.n8n.io/article/can-i-use-your-license-for-my-use-case), [pricing](https://n8n.io/pricing/)
- Cloud Starter is €20/month annually for 2,500 executions; Pro €50 for 10,000. Self-host Business is €667/month annually for 40,000 executions and unlocks SSO, environments, scaling, and Git version control. [pricing](https://n8n.io/pricing/)
- **Fit:** useful edge/integration automation, but licensing and governance make it a poor canonical substrate for a multi-company product. Keep it behind a narrow adapter if used.

## Data and Kubernetes orchestrators

### Prefect and Dagster

- Prefect OSS and Cloud focus on dynamic Python flows, task/flow retries, caching, work pools/deployments, events, schedules, and operational UI. Hobby is free for two users/five deployments; Starter is $100/month. [pricing](https://www.prefect.io/pricing), [OSS comparison](https://www.prefect.io/compare/prefect-oss)
- Dagster centers assets, partitions, sensors, schedules, lineage, backfills, and data-catalog operations. Dagster+ Solo is $10/month plus $0.040/credit and serverless compute; Starter is $100/month plus credits. [pricing](https://dagster.io/pricing)
- **Fit hypothesis:** choose either when actual work is predominantly Python/data/ML assets. Neither documents the full months-long interactive company-process contract without additional application logic.

### Apache Airflow

- Airflow 3.3 models scheduled/task-dependent DAG runs, dynamic DAGs/mapping, backfills, sensors, deferrable operators, and event-driven asset scheduling. It is Apache-2.0 with official Docker and Helm distribution. [DAGs](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dags.html), [event scheduling](https://airflow.apache.org/docs/apache-airflow/stable/authoring-and-scheduling/event-scheduling.html), [distribution](https://airflow.apache.org/docs/)
- Airflow's documentation says it does not yet support full multi-tenancy. Versioned DAG bundles help pin workers to the same source version. [architecture](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/overview.html)
- **Fit:** mature data scheduler, not a reason to force every business/agent workflow into Python DAG semantics.

### Argo Workflows

- Argo Workflows is an Apache-2.0 Kubernetes-native YAML workflow engine for container DAGs/steps, templates, artifacts, cron, loops, retries, and suspend/resume, with Argo Events for external triggers. [official docs](https://argo-workflows.readthedocs.io/), [repository](https://github.com/argoproj/argo-workflows)
- **Fit:** appropriate for cluster jobs after Kubernetes is already an intentional platform. On an Apple-Silicon local-first system, introducing Kubernetes solely for Argo creates more infrastructure than it removes.

## Business-process orchestrator

### Camunda 8 / Zeebe

- Camunda models BPMN/DMN processes spanning people, systems, and agents. Zeebe supplies persistent process execution; Tasklist supplies human task queues/forms; Operate and Optimize supply inspection/analytics. Camunda claims the same engine/APIs in SaaS and self-managed deployments. [platform](https://camunda.com/platform/)
- Camunda says more than 700 enterprises use the platform, including nine of the top ten US banks. This is first-party adoption evidence, not independently audited here. [platform](https://camunda.com/platform/)
- Current licensing is decisive: local/non-production Self-Managed development is free; production Self-Managed and SaaS require Enterprise/custom pricing. The SaaS trial lasts 30 days. [pricing](https://camunda.com/pricing/)
- **Fit hypothesis:** strong documented coverage for explicit business processes and human work. Use only when BPMN/governance justify enterprise cost and the common fixtures support it.

### Flowable OSS

- Flowable provides Apache-2.0 Java engines for BPMN processes, CMMN cases, DMN
  decisions, forms, and content. The OSS project supports embedded or server
  deployments and documents JDK 17+; commercial Flowable products add broader
  enterprise work and governance surfaces.
  [open-source overview](https://www.flowable.com/open-source),
  [OSS introduction](https://www.flowable.com/open-source/docs/oss-introduction)
- **Fit hypothesis:** a material open-standard alternative when governed human
  processes and case management dominate. It is excluded from the first
  orchestration shortlist only because agent adapters, operator experience,
  security boundaries, and local operational cost remain to be proven—not
  because Camunda is the only BPM option.

## Managed cloud state machines

### AWS Step Functions

- Standard Workflows are durable/auditable for up to one year and follow an exactly-once state-execution model unless retries are configured. Express runs at-least-once for up to five minutes. [workflow types](https://docs.aws.amazon.com/step-functions/latest/dg/choosing-workflow-type.html)
- Standard includes 4,000 transitions/month indefinitely free, then charges per transition including retries; Express charges executions, duration, and memory. [pricing](https://aws.amazon.com/step-functions/pricing/)
- **Fit hypothesis:** a managed substrate for AWS services; ASL definitions can be externally generated/versioned, but IAM/service integration and runtime semantics create AWS lock-in.

### Azure Durable Functions

- Orchestrator functions rebuild state through deterministic replay. External events may wait indefinitely without compute billing, but delivery is at-least-once and must be deduplicated. [orchestration replay](https://learn.microsoft.com/azure/azure-functions/durable/durable-functions-orchestrations), [external events](https://learn.microsoft.com/azure/azure-functions/durable/durable-functions-external-events)
- Consumption billing counts each orchestrator replay as a function invocation and separately charges the storage backend; wait/yield time itself is not billed. [billing](https://learn.microsoft.com/azure/azure-functions/durable/durable-functions-billing)
- **Fit:** strong when the execution plane is already Azure Functions; less neutral than Dapr or Temporal.

### Google Cloud Workflows

- Google Workflows is a managed YAML/JSON state machine for Google services and arbitrary HTTP APIs. It can hold state, retry, poll, sleep, or wait on callbacks for up to one year. Callback endpoints are IAM-protected and can implement human interaction without polling. [overview](https://cloud.google.com/workflows/docs/overview), [callbacks](https://cloud.google.com/workflows/docs/creating-callback-endpoints)
- Monthly free use is 5,000 internal and 2,000 external steps; additional steps are $0.01 and $0.025 per thousand respectively. [pricing](https://cloud.google.com/workflows/pricing)
- **Fit:** extremely cheap, low-ops orchestration for HTTP/GCP services; no self-hosting and limited worker-language semantics because the workflow is declarative service calls.

## Agent-native layers are not full substitutes

### LangGraph / LangSmith Deployment

- LangGraph persists graph state as per-step checkpoints for fault recovery, human interrupts, memory, and time travel. Time travel skips nodes before a checkpoint but re-executes all later nodes—including LLM/API calls—so effect idempotency remains an application obligation. [persistence](https://docs.langchain.com/oss/python/langgraph/persistence), [time travel](https://docs.langchain.com/oss/python/langgraph/use-time-travel), [interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts)
- LangSmith Deployment adds managed task queues, revisions/rollbacks, cron, webhooks, auth, streaming, and HITL. Developer ($0/seat) has no deployment; Plus is $39/seat/month plus usage and includes one small serverless deployment; Enterprise adds self-host/hybrid and governance. [deployment](https://www.langchain.com/langsmith/deployment), [pricing](https://www.langchain.com/pricing)
- **Fit:** use inside an agent application where cyclic graph state is valuable, below or within the durable substrate—not as the one company-wide authority.

### CrewAI / AMP

- CrewAI supplies Python Crews and Flows, persistence, events/listeners, HITL, triggers, automations, and managed/private enterprise deployment. [documentation](https://docs.crewai.com/), [enterprise](https://docs.crewai.com/enterprise/introduction)
- Basic is free with 50 workflow executions/month and two automations; production governance/private deployment is Enterprise. [pricing](https://crewai.com/pricing)
- **Fit:** a replaceable agent/application framework. Its crew/task vocabulary should not redefine authoritative work records, retries, or approvals.

## Decision criteria for the vertical slice

Run the same admitted operation through each finalist. The test must include:

1. Receive an external task carrying immutable company/project/task IDs and expected source revision.
2. Acquire and renew one controller-issued lease; reject stale or duplicate workers.
3. Run a dynamic parallel branch with one deliberately failing activity and deterministic retry bounds.
4. Wait at least one hour with all workers stopped; accept an externally authenticated approval signal; reject a replayed or wrong-task signal.
5. Crash the engine, state store, and worker at separate fault points, including after an external side effect but before acknowledgement.
6. Change workflow code/definition while an older execution waits; prove the in-flight version and migration behavior.
7. Execute compensation after a partial side effect and record whether the platform guarantees, retries, or merely schedules it.
8. Emit an exact-revision receipt and reconcile engine history with the external canonical work ledger.
9. Demonstrate per-company rate/concurrency budgets and that one company's event/credential cannot reach another.
10. Develop and run locally on Apple Silicon, then repeat on a Linux host without changing authoritative semantics.

Measure operational components, idle resource use, recovery time, duplicate effects, history growth, versioning friction, operator clarity, and real monthly actions/transitions. Do not choose by connector count or agent demo quality.

## Recommended deployment split for evaluation

### Self-host without subscription

- **Conductor OSS:** declarative graph/control-flow finalist; Docker/JVM with a production-like Postgres/OpenSearch or other supported backend.
- **Dapr Workflow/Agents:** portable replay/history/identity finalist; use a supported state store and exercise access policy/history signing.
- **Temporal OSS:** replay-family reference baseline.
- **Restate or DBOS:** lightweight entrant. Choose Restate when durable RPC/stateful objects matter; DBOS when Postgres/exactly-once application transactions dominate.

### Free/low-cost managed comparison

- Orkes Developer sandbox for UX only; it is not a production economics test.
- Restate Free (100k actions), Hatchet Developer (100k runs), Inngest Hobby (50k executions), Trigger.dev Free ($5 compute credit), Google Workflows free steps, and Step Functions free transitions.
- Temporal Cloud's listed AWS route begins at $100/month plus usage, so compare only after the OSS failure test establishes value.

### Defer unless a workload proves the category

- Camunda until BPMN/human work and enterprise governance justify a quote.
- Kestra/Windmill/n8n until visual non-code integration is a concrete workload.
- Airflow/Dagster/Prefect until data/asset pipelines dominate.
- Argo until Kubernetes exists for independent reasons.
- LangGraph/CrewAI as application libraries, never parallel lifecycle authorities.

## Final first-principles answer

The platform should not build another orchestration engine. The full market already supplies durable histories, long waits, external signals, dynamic graphs, scheduling, retries, compensation patterns, versioning, and operator UIs in multiple maintained forms.

What remains genuinely specific is a small authority-and-reconciliation layer above the engine:

- canonical company/project/work identity;
- admission, lease, budget, and effect authorization;
- authenticated approval grants;
- source/candidate/review/promotion receipts bound to exact revisions;
- adapter-neutral reconciliation between authoritative work state and execution history.

Conductor OSS is now a serious first finalist because its declarative, polyglot, persisted graph is unusually compatible with that separation. Dapr and Temporal provide stronger replay/history semantics; Restate and DBOS may deliver the same practical reliability with less infrastructure for narrower workloads. The next decision should come from the fault-injected vertical slice, not another greenfield framework or a feature-count winner.
