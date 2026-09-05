# Self-hosted platform comparison for the provider-neutral factory

**Research status:** read-only decision brief. No component in this document is
installed, configured, adopted, or approved by this comparison.

**Access date:** 2026-08-28. External links are current upstream documentation,
upstream source, or upstream release pages accessed on that date. GitHub stars,
``awesome`` lists, and vendor popularity claims were not used as fit evidence.

## 1. Intent checksum

The target is the smallest clean, solo-operated, provider-neutral agent software
factory. Its first proof is an issue-to-teardown chain with leased attempts,
isolated worktrees, immutable candidates and artifacts, deterministic gates, a
fresh independent review, explicit human promotion, and teardown. The current
repository explicitly keeps product factories, credentials, provider accounts,
live sessions, runtime databases, model files, and caches outside this source
tree; it also says to prove one complete workflow before adding semantic-memory
planning, workflow engines, or large swarms. [Current goal](../docs/GOAL.md)
[Architecture boundary](../docs/ARCHITECTURE.md)

This comparison therefore asks a narrower question than “what is the most
featureful platform?”: which self-hostable systems could be introduced later
without taking over source, acceptance, promotion, or durable-policy authority?

### Evidence labels

- **Observed locally** means a statement read from the repository documents above.
- **Officially documented** means a linked upstream source says it.
- **Inference** is explicitly marked and is not an installation claim.
- **Proposed** is a decision option only; it requires a later approved plan.
- **Apple Silicon status** is conservative: “documented” requires an upstream
  ARM/Darwin-arm64 statement or asset. “Undocumented” is a lab-validation gap,
  not evidence that the software cannot run on Apple Silicon.

### Historic baseline retained and challenged

Earlier research concluded that Git, worktrees, portable procedures, immutable
artifacts, and local receipts remain the initial seam; a durable external runtime
is only worth investigating after recorded failures in recovery, durable wait,
child join, cancellation/budget control, or stateful human-in-the-loop branching.
It also deferred Temporal, LangGraph, OpenTelemetry/Phoenix as supervisors and
deferred vector memory until a measured recall/provenance/eviction failure. That
baseline is preserved below rather than silently replaced.

## 2. Current authority map and non-negotiables

| Boundary | Current authority | A later service may own | It must not own |
|---|---|---|---|
| Source, intent, candidate identity | Git objects; GitHub Issues/PRs as current evidence surfaces; exact hashes | Replica/transport of source or artifacts | The sole source of truth or candidate identity |
| Promotion | Explicit human action after independent exact-candidate review | Nothing automatically | Merge/deploy authority or a policy/memory promotion decision |
| Attempt lifecycle | Platform contracts, worktrees, checkpoints, receipts | Execution-state mirror or bounded retry state | Source acceptance or human approval |
| Model access | Per-runtime/provider adapters | Provider translation, routing, retry, and budgets | Task lifecycle, credential source, or promotion |
| Secrets | Opaque references outside the repo | One explicitly approved runtime-secret broker | Secret values in this repository or a second competing broker |
| Observability | Hashed receipts and local evidence | A redacted trace/evaluation mirror | The receipt, gate, or promotion authority |
| Memory | Git artifacts, ADRs, run summaries, SQLite receipts, FTS | Advisory retrieval after measured need | Canonical policy, task truth, or automatic promotion |
| Execution isolation | Per-task isolated workspace plus operating-system controls | A sandbox runtime with explicit capability grants | Unbounded host access, home-directory mounts, or a Docker socket by default |

This map is **observed locally** from the goal and architecture documents; the
service limits in the following tables are **proposed synthesis**.

## 3. Integrated source, issue, review, CI, and policy systems

| Candidate | Officially documented license and self-host scope | What it can own; operational weight; Apple Silicon evidence | Overlap and previous conclusion status | Keep / Adapt / Defer / Reject |
|---|---|---|---|---|
| **Forgejo** | Current versions are [GPL v3+](https://forgejo.org/faq/). It is self-hosted, has issues, pull requests, projects, package registries, branch/tag protections, and [integrated Actions](https://forgejo.org/docs/latest/user/actions/overview/). | Could own a Git mirror/host, issue/PR surface, and CI job dispatch. A small instance can use [SQLite](https://forgejo.org/docs/latest/admin/installation/database-preparation/); Actions still require an available runner, which executes the workflow rather than the Forgejo server. That is light-to-medium operational weight plus the isolated-runner boundary. Exact Apple-Silicon server support was not stated in the reviewed upstream material. | It overlaps the current GitHub issue/PR/evidence surface but does not implement the platform’s leases, receipts, fresh review, or human promotion. Historic “keep Git/worktrees first” is **Confirmed**; Forgejo itself was not previously proven here, so self-host fitness is **Still unverified**. | **Adapt** if self-hosted source/CI becomes an explicit requirement. It is the smallest self-hosted forge candidate screened, not a current migration recommendation. |
| **GitLab Self-Managed Free** | Upstream states the core GitLab code is [MIT](https://docs.gitlab.com/administration/package_information/licensing/) and documents the Self-Managed Free offering, issues, merge requests, CI/CD, and protected branches. On Free, merge-request approvals are [optional rather than merge-blocking](https://docs.gitlab.com/user/project/merge_requests/approvals/). | Could own the widest integrated Git/issue/MR/CI/package surface. Official single-node baseline is [8 vCPU and 16 GB RAM](https://docs.gitlab.com/install/requirements/), with PostgreSQL, Redis/Valkey, Gitaly, and recommended object storage; that is high operational weight. The same requirements explicitly say ARM-based processors are supported. | It could replace much of the current GitHub surface, but Free does not turn ordinary approvals into the exact human-promotion mutex required here. No prior GitLab adoption conclusion exists: **Still unverified**. | **Reject** for the present solo foundation: it adds a large operating burden without closing the authority gap. Re-screen only if organization-scale GitLab requirements appear. |
| **OneDev** | The public core is [MIT-licensed](https://github.com/theonedev/onedev); upstream presents Git, issues, pull requests, CI/CD, package registries, workspaces, and agent-oriented workflows as one self-hosted system. | Could own Git, issue/PR flow, builds, packages, and some agent execution coordination. Its official Docker guide says it can run on a [2-core/2-GB host](https://docs.onedev.io/installation-guide/run-as-docker-container), with an embedded database or external PostgreSQL/MySQL/MariaDB. That guide mounts the host Docker socket for builds: a material execution authority that conflicts with the current default-deny host-boundary. macOS is documented for Docker use; exact arm64 server support is not. | It covers more of the factory than Forgejo, but would not replace immutable receipts, independent review, or owner promotion. It is genuinely new to this comparison: **Still unverified**. | **Adapt** only as the all-in-one alternative below, after a sandbox design eliminates the host-Docker-socket trust expansion. |

## 4. Durable workflow and agent orchestration

| Candidate | Officially documented license and self-host scope | What it can own; operational weight; Apple Silicon evidence | Previous conclusion status and fit | Keep / Adapt / Defer / Reject |
|---|---|---|---|---|
| **Temporal** | The server is [MIT-licensed](https://github.com/temporalio/temporal/blob/main/LICENSE), and upstream documents both [self-hosting and Temporal Cloud](https://docs.temporal.io/). It is built for workflows that resume after crashes, network failures, and outages. | Could own durable execution history, retries, waits, signals, and workflow recovery. It is a separate durable service plus workers and persistence, therefore materially heavier than local receipts. No project-specific Apple-Silicon deployment support was identified in the reviewed sources. | Historic conclusion: investigate only after observed process-death/recovery, durable-wait, child-join, cancellation/budget, or stateful-HITL failures. Current evidence supports that boundary: **Confirmed**. | **Defer** until a recorded trigger occurs. |
| **LangGraph OSS library** | The `langgraph` package is [MIT-licensed](https://github.com/langchain-ai/langgraph/blob/main/LICENSE). It is a Python/JS application library for stateful graph execution and application-owned checkpoints, not by itself a hosted factory control plane. | Could own an individual product agent’s graph state and application-level checkpoints. Operational weight is low in-process and rises with the chosen checkpoint store. The upstream package supports Python 3.10+; no project-specific Apple-Silicon runtime support statement was located. | Historic conclusion: use only for a concrete stateful graph application, not for platform supervision. **Confirmed**. | **Defer** as a product-runtime library, not a platform authority. |
| **LangSmith / LangGraph Platform (not LangGraph OSS)** | Upstream’s [self-host documentation](https://langchain-ai.github.io/langgraph/cloud/deployment/self_hosted_control_plane/) says hybrid and self-hosted platform modes are **Enterprise** offerings. The full platform includes a control plane and a data plane with Agent Servers and backing services such as PostgreSQL and Redis; it is not the MIT OSS library. | Could own graph deployment, persistence, observability, evaluation, and application-management control-plane state. It is commercial and multi-service. Apple-Silicon self-host support was not documented in the reviewed source. | Previous generic “LangGraph” deferral is **Revised** into two distinct facts: the OSS library remains deferred; the self-hosted LangSmith/LangGraph Platform is an Enterprise platform, not an open-source self-host substitute. | **Reject** as the open/self-hosted factory core. |
| **Hatchet** | Hatchet is [MIT-licensed](https://github.com/hatchet-dev/hatchet/blob/main/LICENSE), self-hostable, and documents durable workflows, tasks, agents, queues, retries, monitoring, and replay. For simple self-hosted workloads it says [PostgreSQL is the only infrastructure dependency](https://docs.hatchet.run/v1). | Could own durable event log, task/DAG state, retries, queueing, and worker concurrency. PostgreSQL-only minimum makes it a lighter durable candidate than Temporal, though it still becomes execution-state authority. Apple-Silicon server support is not documented in the reviewed upstream source. | This is a material new candidate. It does not invalidate the historic trigger rule, so current fit is **Still unverified** rather than a replacement decision. | **Defer**; if the trigger is met, compare a bounded Hatchet proof against Temporal before adoption. |
| **Windmill** | [AGPL v3](https://www.windmill.dev/platform/self-host-content); upstream documents fully self-hosted scripts, flows, jobs, webhooks, and UIs. | Could own workflow definitions, execution queue, users/secrets, and internal UIs. Its documented core is PostgreSQL + server + workers; production can add a load balancer and S3-compatible cache, so medium-to-high operational weight. Apple-Silicon server support is undocumented in the reviewed source. | No historic adoption conclusion; it overlaps both workflow execution and human-facing product surfaces, which is broader than this foundation needs: **Still unverified**. | **Defer**; it is useful for a later internal automation product, not the initial control plane. |
| **Trigger.dev** | Upstream documents [self-hosted containers](https://trigger.dev/docs/self-hosting/overview) and an [Apache-2.0 source license](https://github.com/triggerdotdev/trigger.dev/blob/main/LICENSE). | Could own TypeScript-first background-task runs, job traces, queues, and worker execution. Documented self-host architecture splits Webapp (including PostgreSQL and Redis) from workers/supervisor; medium operational weight. Apple-Silicon server support is undocumented. | No historic adoption conclusion. It is a credible code-first runner, but does not prove a provider-neutral factory lifecycle: **Still unverified**. | **Defer** until a TypeScript product requires durable background work. |
| **Prefect OSS** | Prefect is [Apache-2.0](https://github.com/PrefectHQ/prefect/blob/main/LICENSE), and a [self-hosted server](https://docs.prefect.io/v3/concepts/server) supplies UI and database-backed flow state. | Could own Python flow/task state, schedules, concurrency, deployments, logs, and artifacts. SQLite is documented for lightweight single-server use; PostgreSQL is documented for production/HA. Official installation output includes a `darwin/arm64` example, documenting Apple-Silicon client/runtime use. | Historic rule says a workflow engine waits for a demonstrated gap. Prefect’s data-pipeline orientation does not change that: **Confirmed**. | **Defer**. |

### Required LangGraph distinction

`LangGraph OSS` is an MIT application library. `LangSmith` / `LangGraph Platform`
is a separately documented Cloud, Hybrid, or Enterprise self-hosted platform. A
local Agent Server or a LangGraph package import is therefore not evidence that
the paid/self-hosted Platform is available, free, or selected.

## 5. Gateway, observability, and memory

| Candidate | Officially documented license and self-host scope | What it can own; operational weight; Apple Silicon evidence | Previous conclusion status and fit | Keep / Adapt / Defer / Reject |
|---|---|---|---|---|
| **LiteLLM** | Core outside `enterprise/` is [MIT](https://github.com/BerriAI/litellm/blob/main/LICENSE); upstream documents a self-hosted [proxy deployment](https://docs.litellm.ai/docs/proxy/deploy). | Could own provider normalization, virtual-key auth, budgets, routing/fallbacks/retries, and logging callbacks. A minimal proxy can be one process; production auth/tracking adds PostgreSQL and multi-instance cache/rate handling adds Redis. Apple-Silicon server support is undocumented. | Historic platform stance had no standalone gateway. Capability is verified, but a measured need beyond per-runtime adapters is **Still unverified**. | **Defer** until a recorded cross-runtime routing, credential, or budget-control gap exists. It must never own task lifecycle or secret truth. |
| **Langfuse** | Core outside `ee/` is [MIT Expat](https://github.com/langfuse/langfuse/blob/main/LICENSE); upstream documents self-hosted tracing, prompts, evaluations, and datasets. | Could own an observability/evaluation mirror. Its documented production stack is Web + Worker + PostgreSQL + Redis/Valkey + ClickHouse + S3/blob storage, with a published minimum around 11 CPU / 25.5 GiB before storage: [self-host](https://langfuse.com/self-hosting) and [scaling](https://langfuse.com/self-hosting/configuration/scaling). Apple-Silicon server support is undocumented. | Historic trace-host deferral is **Confirmed**: no measured multi-runtime trace-view need yet justifies this stack. | **Defer**. |
| **Arize Phoenix** | Phoenix is [Elastic License 2.0](https://arize.com/docs/phoenix/self-hosting/license), not Apache-2.0; upstream permits self-hosting on one’s own infrastructure. | Could own a trace/evaluation UI and collector. Upstream documents SQLite for local/single-user use and PostgreSQL for production: [architecture](https://arize.com/docs/phoenix/self-hosting/architecture). It also documents that UI web analytics are enabled by default unless disabled: [privacy](https://arize.com/docs/phoenix/self-hosting/security/privacy). Apple-Silicon server support is undocumented. | Historic Phoenix deferral is **Confirmed**. The current license screening is new evidence and must be carried into any later review; it is not a claim that a prior license decision was approved. | **Defer** pending a measured trace/eval need and an explicit data-redaction/privacy policy. |
| **OpenTelemetry** | The specification is [Apache-2.0](https://github.com/open-telemetry/opentelemetry-specification/blob/main/LICENSE). A [Collector](https://opentelemetry.io/docs/collector/architecture/) receives, processes, and exports telemetry; it is not a trace storage/UI backend. | Could standardize redacted trace IDs, spans, and attributes at the transport layer only. A Collector is optional until there is an export backend. Current collector releases publish `darwin_arm64` assets: [release](https://github.com/open-telemetry/opentelemetry-collector-releases/releases/latest). GenAI semantic conventions remain [Development](https://github.com/open-telemetry/semantic-conventions-genai/blob/main/docs/gen-ai/README.md). | Historic direction to adapt stable trace primitives but defer a hosted backend is **Confirmed**. | **Adapt** version-pinned, redacted basic tracing fields only; defer Collector/backend deployment. |
| **Semantic/vector memory** | No named candidate in this request is a canonical semantic-memory system. | A future retrieval service could only provide advisory recall with source links, freshness, provenance, retention, and eviction controls. It must not own task truth, policy, or promotion. | Historic conclusion to retain Git/SQLite/hashed receipts and defer vector memory until a measured recall failure is **Confirmed**. | **Defer**. |

## 6. Secrets, sandbox, and artifact systems

| Candidate | Officially documented license and self-host scope | What it can own; operational weight; Apple Silicon evidence | Previous conclusion status and fit | Keep / Adapt / Defer / Reject |
|---|---|---|---|---|
| **OpenBao** | [MPL-2.0](https://github.com/openbao/openbao/blob/main/LICENSE); it is a self-hosted secrets/auth/ACL/audit/dynamic-credential/PKI service. | Could own the runtime-secret and credential-issuance boundary. Raft or PostgreSQL storage, TLS, seal/unseal/KMS, backup/recovery, and audit make it medium-to-high weight: [architecture](https://openbao.org/docs/internals/architecture/) and [storage](https://openbao.org/docs/next/configuration/storage/). `darwin_arm64` is published in [v2.6.2](https://github.com/openbao/openbao/releases/tag/v2.6.2). | Historic opaque-reference/no-repo-secrets boundary is **Confirmed**. Need for a central broker remains **Still unverified**. | **Defer**. |
| **Infisical** | Root code outside `ee/` is [MIT Expat](https://github.com/Infisical/infisical/blob/main/LICENSE); the [EE paths have a restrictive license](https://github.com/Infisical/infisical/blob/main/backend/src/ee/LICENSE.md). It self-hosts secret/config/RBAC/audit/rotation functions. | Could own secrets, access policy, audit, and optional privileged-access authority. It requires PostgreSQL and persistent Redis in its documented requirements: [requirements](https://infisical.com/docs/self-hosting/configuration/requirements). Apple-Silicon server support is undocumented. | It overlaps OpenBao almost completely. Historic secret boundary is **Confirmed**; need for either broker is **Still unverified**. | **Defer** and never introduce it beside OpenBao without an explicit non-overlapping authority split. |
| **SOPS** | [MPL-2.0](https://github.com/getsops/sops/blob/main/LICENSE); this is a local encrypted-file CLI, not a self-hosted server. | It can encrypt configuration files with age/PGP/KMS. Its authority is only at-rest repository-file encryption, not live secret delivery or policy. `darwin.arm64` is published in [v3.13.3](https://github.com/getsops/sops/releases/tag/v3.13.3). | The current source boundary says no secret values belong in this repository. That historic boundary is **Confirmed**. | **Reject** for this repository; reconsider only for a separately approved encrypted deployment-config repository. |
| **Daytona** | Its last public snapshot is [AGPL-3.0](https://github.com/daytonaio/daytona/blob/v0.190.0/LICENSE). The current upstream README says public-repository updates, fixes, and releases stopped after core development moved private in June 2026: [status](https://github.com/daytonaio/daytona/blob/main/README.md). | Could own sandbox lifecycle, filesystem/process/network policy, snapshots, and execution state. Customer-managed runners need privileged Kubernetes/Docker/Sysbox, S3 snapshot storage, and a Daytona control-plane connection: [runner chart](https://github.com/daytonaio/helm-charts/blob/main/charts/daytona-region/README.md). Its CLI has `darwin-arm64`; native self-hosted runtime support is undocumented. | The earlier unratified generic sandbox-option posture is **Superseded** for Daytona by its current public-core status. The broader OS-control requirement remains unchanged. | **Reject**. |
| **E2B** | [Apache-2.0](https://github.com/e2b-dev/E2B/blob/main/LICENSE); upstream documents self-hosted microVM infrastructure. | Could own sandbox lifecycle, network isolation, templates, and snapshots. Its self-host design requires Linux/KVM/Firecracker and Terraform/Nomad/Consul/PostgreSQL/Redis/ClickHouse/object storage: [architecture](https://github.com/e2b-dev/infra/blob/main/docs/ARCHITECTURE.md), [self-host](https://github.com/e2b-dev/infra/blob/main/self-host.md). Local development requires Linux and `/dev/kvm`, so native Apple-Silicon self-hosting is undocumented: [requirements](https://github.com/e2b-dev/infra/blob/main/DEV-LOCAL.md). | The need for a separate high-isolation sandbox is not yet measured: **Still unverified**. | **Defer** until an OS-control test shows local/worktree isolation is insufficient. |
| **zot (OCI registry)** | [Apache-2.0](https://github.com/project-zot/zot/blob/main/LICENSE); self-hosted OCI registry with auth/TLS, sync, retention/GC, local or S3-compatible storage: [README](https://github.com/project-zot/zot). | Could own artifact publication/retrieval only. It is low-to-medium weight (Go binary plus persistent storage; optional extensions). `zot-darwin-arm64` is published in [v2.1.20](https://github.com/project-zot/zot/releases/tag/v2.1.20). | Git SHA plus artifact hash remain the identity; a registry is transport/storage, not authority. Demand is **Still unverified**. | **Adapt** only when OCI image/artifact transport is an actual accepted requirement. |
| **MinIO** | [AGPL-3.0](https://github.com/minio/minio/blob/master/LICENSE). The upstream README says the community distribution is source-only and production source builds are at user risk: [README](https://github.com/minio/minio/blob/master/README.md). | Could own S3-compatible blobs, artifacts, snapshots, and receipts but no workflow/secret authority. It adds source/image build, storage, backup, and topology operations; Linux/arm64 build is documented but native macOS Apple-Silicon server support is not. | The generic “artifacts stay outside Git but retain hashes” conclusion is **Confirmed**; MinIO’s current distribution posture is a new constraint: **Revised**. | **Reject** for the current foundation. |

## 7. What is genuinely new after the current-source challenge

1. **OneDev is the credible all-in-one alternative.** It can cover Git, issues,
   PRs, CI, packages, and agent-oriented workflows at a documented small-host
   footprint. Its official host-Docker-socket deployment pattern is the decisive
   security mismatch, not feature absence.
2. **Hatchet is the credible lighter durable-runtime challenger.** Its documented
   PostgreSQL-only minimum and MIT license give it a narrower future proof path
   than Temporal. It still must earn adoption through the same observed-failure
   trigger; it is not a reason to install a workflow engine now.
3. **LangGraph has to be split.** The MIT OSS library is not the Enterprise
   LangSmith/LangGraph Platform. Treating them as one self-hosted choice would
   incorrectly import a commercial control plane into the OSS assessment.
4. **Phoenix’s license screen matters.** Current upstream source identifies ELv2,
   while OpenTelemetry remains Apache-2.0 and is transport rather than a trace
   backend. Neither fact creates a current trace-host requirement.
5. **Daytona no longer qualifies as a current public-core sandbox choice.** Its
   upstream public-repository status changed, while E2B remains technically
   plausible but too infrastructure-heavy for a native Apple-Silicon initial
   foundation.

## 8. Proposed smallest coherent stack and all-in-one alternative

These are **proposed synthesis**, not adoption decisions.

### Smallest coherent path

1. Keep the current Git/GitHub issue-and-PR evidence surface, isolated
   worktrees, local deterministic lifecycle contracts, hashed artifacts, and
   SQLite receipts for the first complete workflow.
2. Add **no permanent self-hosted service** until an acceptance test establishes a
   real gap. Use OpenTelemetry-compatible, redacted identifiers only as a
   lightweight interface boundary; do not deploy a Collector or backend yet.
3. If an explicit self-hosted source/CI requirement is approved, evaluate a
   **Forgejo + dedicated isolated runner** proof. Preserve the platform’s leases,
   receipts, independent review, and human promotion outside the forge.
4. If and only if the durable-runtime trigger is met, conduct a bounded
   **Hatchet + PostgreSQL** versus Temporal recovery proof. The evaluation must
   cover process death, wait/resume, cancellation, lease/retry behavior, exact
   artifact binding, and human approval—not feature lists.
5. Add a provider gateway, central secret service, OCI registry, trace backend,
   semantic memory service, or microVM sandbox only after their individual
   evidence triggers. Every one remains a bounded subordinate service.

### All-in-one alternative

An isolated **OneDev** pilot is the all-in-one alternative worth evaluating if a
single self-hosted Git/issue/PR/CI/package surface becomes a hard requirement. It
must run on a separately controlled execution host or an equivalently isolated
runner design that does not hand platform code an unrestricted host Docker socket.
OneDev would still be a collaboration/execution surface; it would not replace the
candidate hash, independent review, owner promotion, or repository policy.

GitLab is not the selected all-in-one alternative for this solo foundation because
its officially documented baseline resource and component footprint are much
larger. That is an operational-scope observation, not a claim that GitLab is less
capable.

## 9. Deferred adoption gates and validation plan

No installation follows from this research. A later approved adoption brief must
include each relevant gate below.

| Proposed change | Evidence required before selection | Fail-closed condition |
|---|---|---|
| Self-hosted forge | Exact Git/issue/PR/CI workflow, branch/protection behavior, backup/restore, runner privilege boundary, and Apple-Silicon or target-host proof | Any direct path to unreviewed promotion or unbounded host execution |
| Durable runtime | Reproducible process-death, wait/resume, cancellation, stale lease, child join, replay, and human-approval tests | Recovery state cannot bind to exact inputs/artifacts or bypasses owner promotion |
| Model gateway | Measured multi-provider routing/credential/budget gap; provider-neutral request/receipt contract; outage/fallback tests | Gateway becomes lifecycle, secrets, or policy authority |
| Trace backend | Demonstrated need for cross-runtime trace correlation; prompt/tool-output redaction; retention/deletion/export test | Raw sensitive content is retained by default or traces substitute for receipts |
| Secret broker | Central-secret need, access policy, rotation/revocation, backup/recovery, and single-owner model | Two competing secret authorities or a secret value enters source control |
| Sandbox | Concrete host-isolation failure; filesystem/network/credential/elevation probes; teardown and snapshot hygiene | Home, Docker socket, or broad network becomes implicit capability |
| Registry/blob store | Accepted OCI/S3 artifact transport requirement; restore, retention, integrity, and cost/operations proof | Storage becomes artifact identity or gate/promotion authority |
| Semantic memory | Measured recall failure plus provenance, retention, eviction, permission, and stale-answer tests | Retrieved memory can silently become policy or source-of-truth |

## 10. Risks and constraints to retain

- A large integrated system can make administration feel simpler while silently
  concentrating source, execution, credentials, logs, and promotion power. The
  authority map is more important than the dashboard count.
- An “arm64” release asset proves only the cited binary/CLI/collector artifact;
  it does not prove a supported full production topology on an M-series Mac.
- Licenses in this brief are source-code/distribution findings, not legal advice.
  In particular, copyleft, open-core/EE splits, ELv2, and source-only distribution
  constraints require a legal/operational review before reuse or redistribution.
- A self-hosted UI is not automatically private: Phoenix’s upstream privacy note
  is a concrete reminder to inspect telemetry and analytics behavior separately.
- No workflow engine, forge, or sandbox is a substitute for an independent
  exact-candidate review and explicit owner-controlled promotion.

## 11. Approval question

The decision proposed for approval is limited to this sequencing: preserve the
current smallest foundation; treat Forgejo and OneDev as conditional source/CI
options; treat Hatchet as the new conditional durable-runtime challenger; and keep
all gateways, trace hosts, secret brokers, semantic memory, registries, and
sandbox services deferred or rejected as stated until their evidence gates are
met. It does **not** authorize installation, configuration, migration, a runtime
change, GitHub mutation, commit, or deployment.

APPROVAL STATUS: awaiting user confirmation
