# Cohesive agent-factory vision and sourcing decision

**Evidence cutoff:** 2026-08-30 local / 2026-08-31 UTC  
**Status:** research and architecture-decision input; not governing documentation, approval, or implementation authority  
**Scope:** repository PR #283, `MASTER-NORTHSTAR-AND-INTENT.md`, accepted repository authority, five-month intent reconstruction, and refreshed primary-source market/OSS evidence

## Executive decision

The product is a **solo-operator system that builds, operates, and improves other systems**. It is broader than an issue-to-merge controller and narrower than a new general-purpose agent cloud.

Its durable product boundary is:

1. a declarative, portable company/project/swarm definition whose concrete format is selected by conformance rather than invented in advance;
2. one unambiguous authority model for goals, work, leases, effects, evidence, review, promotion, budgets, and terminal state;
3. replaceable agent workers, models, sandboxes, workflow engines, and hosted services;
4. both software-delivery and business-deliverable workflows;
5. an attention-oriented operator surface; and
6. an offline, evaluator-gated evolution loop whose candidates cannot judge or promote themselves.

The sourcing rule is equally important:

> **Own the authority, evidence, conformance, and safe-evolution seams. Adopt or buy the commodity execution planes. Never run two authorities for the same concern.**

This yields a low-cost baseline of GitHub, the existing local inference and Hermes assets, one local gateway, open evaluation tooling, and optional object backup. It does **not** justify installing Temporal, Hatchet, Dapr, Paperclip, Fusion, OpenShell, Langfuse, or another portal into the live estate today. Those are candidates for mutually exclusive, pinned trials after the current repository authority conflict and delivery freeze are resolved.

## 1. What is authoritative now

### Observed repository state

- Remote `main` is currently `57915cc`, after PR #184 merged Hermes profiles, bot-roster templates, a LiteLLM proxy configuration, and UI patches.
- [PR #283](https://github.com/redtrades/agent-platform/pull/283) began as the three-document north-star/inference/persistence proposal at `97616fe`, but it is an actively mutating mixed-scope candidate. At the 2026-08-31 03:09 UTC read, its title had changed to “Define local inference resource arbiter contract,” its head was `1b88ed2`, and it contained 6 commits and 43 paths: the three original documents, Obsidian/worktree debris, prior reports and receipts, controller code/tests, and a new inference-arbiter spec/launchd template. Its merge state was `UNSTABLE`.
- Both current required checks then concluded failure before execution: neither job acquired a runner and each had zero steps; the Gate C execution job was skipped. This is infrastructure evidence, not content review. Exact head, path set, title, body, and checks must be re-read before any future claim about this actively changing PR.
- The accepted freeze handoff on `main` says all expansion is stopped and names exact-head review/disposition of PR #280 as the only previously admitted next implementation action ([handoff](https://github.com/redtrades/agent-platform/blob/main/docs/HANDOFF-2026-08-30.md)).
- A later [issue #1 comment](https://github.com/redtrades/agent-platform/issues/1#issuecomment-5472485957) proposes abandoning PR #280 correction work in favor of a quarantined clean ASF kernel, but explicitly labels that reset **proposed, not approved**.
- PR #283 and the subsequent Hermes merge broadened documentation/runtime scope without resolving that authority conflict. PR #283's continuing scope mutation is itself the delivery failure the consolidated vision is meant to prevent: unrelated artifacts and a new runtime controller cannot become one exact architecture candidate merely by sharing a branch. Their existence does not approve either the frozen path or the proposed reset.

### Consequence

No implementation recommendation in this report is presently admitted. Before any stack change, the owner must explicitly choose between:

1. resume the accepted freeze path; or
2. approve the proposed clean-kernel reset and supersede the freeze through the repository's material-design process.

The market research can shape that choice. It cannot silently make it.

## 2. Intent recovered from the latest PR and five-month record

PR #283's strongest contribution is its recovery of the broad intent in [`MASTER-NORTHSTAR-AND-INTENT.md`](/Users/man/agent-platform/docs/MASTER-NORTHSTAR-AND-INTENT.md):

- a solo-operator enterprise rather than a developer toy;
- a dual engine: the system-building software factory and revenue-producing product factories;
- provider-neutral, replaceable mind/body/brain components;
- continuous operation that survives provider, process, context, and machine failure;
- deterministic gates plus a distinct judge and promoter;
- reusable roles, workflows, tools, skills, data policy, budgets, and approvals; and
- roughly 95% autonomous completion for eligible routine work, leaving strategy and exceptional effects to the operator.

The historical reconstruction reaches the same conclusion with stronger provenance: the original system was intended to turn outcomes into research, software, and business artifacts through declarative project/company blueprints and a controlled genetic loop ([historical intent reconstruction](/Users/man/agent-platform/research/GENETIC-SWARM-PLATFORM-DEEP-DIVE-2026-08-30.md)).

### The complete product model

| Plane | Required outcome | Must remain replaceable? |
|---|---|---|
| Company/project | Goals, products, projects, data boundaries, budgets, schedules, outputs and success measures are declared | Definition format is portable; one accepted version is authoritative |
| Genome | Roles, prompts, skills, tools, model policies, workflows, tests and evaluators have versions and lineage | Yes |
| Work authority | One work identity, dependency graph, lease/fence, approval, effect class and terminal state | **No competing authority** |
| Worker/runtime | Codex, Claude, Jules, OpenHands, Hermes/local and later providers execute bounded tasks | Yes |
| Workflow | Events, schedules, waits, retries, joins, cancellation, human gates and compensation survive failure | Engine is replaceable; history for an admitted run is not |
| Evidence | Inputs, candidates, artifacts, tests, reviews, effects, costs and teardown are exact and correlated | Schema is owned; storage/viewer is replaceable |
| Knowledge | Reviewed canonical knowledge is distinct from derived search, summaries and memory | Retrieval/index implementation is replaceable |
| Evolution | Mutations compete against fixed and held-out evaluations with budgets and independent selection | Optimizers are replaceable; promotion policy is owned |
| Safety | Least privilege, sandbox policy, opaque secret references, data classification and destructive-effect grants | Enforcement substrate is replaceable; policy meaning is owned |
| Economics | Route by quality, privacy, quota, latency, cost, GPU/host capacity and operator minutes | Provider/router is replaceable |
| Operator | One attention queue for outcomes, evidence, blocked work, exceptions, health and approvals | UI is replaceable; decisions and receipts are not |
| Products | GovCon and future companies own their domain sources, evaluations, outputs and commercial rules | Yes; they consume stable platform contracts |

### The two coupled loops

The factory has an operating loop and an improvement loop:

```text
OPERATE
outcome -> admitted work -> lease -> isolated execution -> exact evidence
        -> independent review -> policy decision -> promotion -> teardown

EVOLVE
observation -> bounded hypothesis -> isolated candidates -> fixed/held-out evals
            -> independent selection -> authorized promotion or rejection
            -> lineage receipt
```

The second loop never edits the first loop's evaluator, authority policy, or production baseline in place.

## 3. What PR #283 gets wrong or states too early

These are correction requirements, not reasons to discard the recovered intent.

| PR #283 statement | Evidence problem | Cohesive correction |
|---|---|---|
| “GitHub Issues / Project 12 (Intent & Mutex)” | Accepted docs state that Issues define intent and Project is a projection; the remote CAS record owns atomic work | GitHub is the intent/forge surface; exactly one remote lease ledger owns the mutex |
| Temporal/Hatchet shown as the durable spine | No measured recovery fixture selected either engine; the Master Plan requires a demonstrated unmet gap | Treat Dapr Agents, Temporal and Hatchet as mutually exclusive durability candidates |
| LiteLLM fixed on port 3100 | Current `main` installs its Hermes LiteLLM proxy on port 4000, while the persistence ledger maps FreeLLMAPI to 3100 | Keep one verified inference gateway and one port map; never stand up a second router by prose |
| Gemini 2.0 experimental and Qwen 2.5 Coder routes | These model IDs and fixed quota claims are stale; current Gemini and Groq catalogs differ | Discover allowed models at runtime, pin policy aliases, and record exact provider/model in receipts |
| Free model tiers as general routing capacity | Gemini's official free tier says content may be used to improve Google's products; free quotas are model/account specific | Use free APIs only for public/non-sensitive data unless current terms and an explicit data policy permit more |
| Literal sample bearer/master keys and host paths | Conflicts with opaque secret references, portable configuration and secret hygiene | Documentation contains references/placeholders only; runtime injects scoped values outside Git |
| “Dual gate” followed by three gates | Promotion is an effect after evidence, not another verification gate | Deterministic check + independent exact-candidate review; then policy-authorized expected-head promotion |
| Continuous DSPy/GEPA optimization | SOTA supports bounded optimization under fixed evaluators, not self-authorized live mutation | Run an offline evolution lab with immutable baselines, held-out tests and independent promotion |
| Langfuse, Litestream/R2 and SQLite shown as selected | No current accepted requirement selects those products or makes SQLite the work authority | Emit portable telemetry/backup contracts first; deploy one viewer/store only after a measured need |
| Machine persistence inventory in the north-star PR | Volatile ports, processes, model caches and host settings age independently from product intent | Split evergreen intent, approved architecture, generated runtime inventory and disaster-recovery procedure |

PR #283 should therefore not merge as written. A future revision should preserve its intent synthesis, rebase onto current `main`, cite historical sources, remove volatile stack prescriptions, correct authority labels, and move host inventory into generated, timestamped operational evidence.

## 4. Current market conclusion

The market contains credible components for almost every commodity layer, but no single product proves the complete system.

### Whole-system control-plane candidates

| Candidate | Best fit | Material limit | Decision now |
|---|---|---|---|
| Paperclip | Closest company OS: companies, goals, orgs, budgets, agents, tasks, approvals, routines and portable company packages | Twelve official advisories include critical RCE, cross-tenant and credential classes; two advisories lack a declared patched version | Pinned, synthetic, restricted-egress lab only |
| Fusion | Closest integrated MIT software factory: missions, tasks, agents, worktrees, workflows, review/merge and operator UI | Young 0.x project; public multi-tenant/security assurance is limited | Pinned local lab candidate |
| GitHub + CAS kernel + later `gh-aw` | Strongest current source/intent/review/evidence base and least migration | More owned glue; `gh-aw` remains public preview; current Actions runner is unavailable | Safe baseline until a challenger passes conformance |

The three are alternative lifecycle authorities. Paperclip and Fusion must not be combined as equal schedulers with the GitHub/CAS kernel.

### Durable execution candidates

| Candidate | Why it matters | Cost/deployment | Decision |
|---|---|---|---|
| Dapr Agents 1.0 | New strongest OSS finding: GA/production-ready durable workflows, state, messaging, observability and cryptographic agent identity | Self-hosted, cloud-neutral OSS | First durability proof candidate after admission |
| Temporal | Most mature replay/durable-workflow substrate | OSS self-host; Cloud route roughly $100/month plus use | Conservative comparator; buy only if maturity offsets cost/ops |
| Hatchet | Agent/background-task focused, simple managed trial | Developer tier includes 100,000 task runs; supported Team is $500/month | Excellent trial comparator, poor immediate paid step |
| Kestra | Declarative YAML and strong visual business workflows | Apache-2.0 OSS; governance largely paid | Product/data workflow option, not universal authority by default |
| Prefect | Strong Python/data pipelines | OSS; Hobby free; Starter $100/month | Use only if product pipelines dominate |

Exactly one engine may own wait/retry/cancellation history for a given admitted workflow.

### Worker and sandbox candidates

- **Hermes** remains a good default local/general worker, not the task authority.
- **Codex, Claude, Jules and OpenHands** remain replaceable specialist workers. OpenHands core is MIT; its Cloud/Enterprise surface has separate licensing.
- **OpenShell** is the best-aligned local policy/sandbox candidate and has an active Apache-2.0 release stream with Apple-Silicon installation support. Its ecosystem remains early enough to require shadow execution and hostile fixtures.
- **NemoClaw** tests Hermes and Apple Silicon with limitations, but does not assert Hermes production parity.
- **E2B** is the managed cloud-sandbox escape hatch, not the local default.

### Evaluation and evolution

When an evaluation fixture is admitted, compare **Inspect AI + Promptfoo + one trace/eval UI** rather than building an evaluation platform:

- consider self-hosted Langfuse core if its MIT core workflow is preferred;
- consider self-hosted Phoenix if ELv2 is acceptable; or
- begin with portable OpenTelemetry receipts and a bounded Grafana Cloud Free trial for sanitized operational telemetry.

Do not operate Phoenix and Langfuse together without a measured gap. Model judgment remains advisory behind deterministic checks and independent challenge.

## 5. Make, self-host, use free, or buy

### Build and own

Only these boundaries justify custom product code:

1. neutral semantics and conformance rules for company/project/swarm declarations, after testing `agentcompanies/v1-draft` and Fusion import/export rather than inventing another schema first;
2. one cross-system work identity and authority mapping;
3. principal/effect classification and exact approval grants;
4. exact candidate, artifact, check, review, cost and teardown receipts;
5. worker/runtime conformance tests and adapters;
6. offline experiment lineage and promotion policy; and
7. the unified attention projection for the owner.

Do not create another general agent harness, workflow engine, sandbox service, model gateway, trace backend, developer portal, IaC engine or connector marketplace.

### Preserve the existing baseline

| Component | Role | Boundary |
|---|---|---|
| Existing Git/CAS contracts | Current authority/evidence baseline | Keep thin; do not add a parallel queue |
| Hermes and existing local inference | Replaceable workers and private inference | One capacity owner; serialize heavy GPU work |
| Existing gateway on current `main` | Model alias, quota and failover seam | Verify behavior; one gateway only; no work authority |

These are observed existing responsibilities. They do not authorize installation or migration.

### Self-host candidates after a measured requirement

| Candidate | Evaluate for | Admission condition |
|---|---|---|
| Inspect AI + Promptfoo | Reproducible and adversarial evaluation | A fixed cross-worker/provider fixture is admitted; bind outputs to exact inputs/candidates |
| Nix or another pinned environment mechanism | Reproducible worker tools | Clean-host reconstruction fails or costs material operator time; select one environment authority |
| OpenTofu | Actual external infrastructure | A real external resource is approved; plans remain proposed effects and apply operations require policy authority |
| SQLite/Git receipt store | Economical local evidence | The selected kernel needs a queryable receipt store; it cannot replace remote lease or Git candidate authority |
| Dapr Agents / Temporal / Hatchet | Durable waits, recovery and cancellation | One admitted chaos fixture proves the current lifecycle cannot satisfy the requirement; select one engine |
| OpenShell | Local sandbox and credential/network policy | A pinned hostile-input shadow test passes before any production credentials |

### Use generous free tiers for bounded trials

| Service | Current allowance/use | Restriction |
|---|---|---|
| GitHub Free/Actions | 2,000 private-repo Actions minutes; public standard runners free | Current no-runner outage must be diagnosed; a plan upgrade does not prove it fixes the outage |
| Hatchet Developer | First 100,000 task runs included | Trial only; do not create a second production lifecycle |
| CrewAI Basic | 50 workflow executions/month and two automations | One non-code workflow comparison |
| LangSmith Developer | 5,000 base traces/month | No deployment; external trace privacy policy required |
| Langfuse Hobby | 50,000 units/month, two users | Use instead of, not alongside, another trace UI |
| Phoenix AX Free | 25,000 spans/month, 1 GB and 15-day retention | External trace privacy policy required |
| E2B Hobby | One-time $100 credit, metered execution | Synthetic sandbox comparison only |
| Port Free | Up to 15 seats, 10,000 entities and 400 runs | UX experiment only; never authority |
| Gemini API Free | Free tokens on eligible models | Free content may improve Google products; public/non-sensitive workloads only |
| Groq Free | Model/account-specific organization limits | Discover live catalog/limits; public/non-sensitive workloads unless terms permit |
| Cloudflare R2 | 10 GB-month, 1M Class A and 10M Class B operations; free egress | Standard storage free tier; use encryption and tested restore |
| Grafana Cloud Free | 10k metric series and 50 GB each of logs/traces/profiles | Export only sanitized telemetry; hard free-tier limits |

Tailscale Personal is free for personal/non-commercial use. A revenue-producing company should budget the current Standard price of **$8/user/month** rather than assuming the Personal tier permits commercial production ([official pricing](https://tailscale.com/pricing)).

### Low-cost subscriptions worth paying for

| Subscription | Current price | Buy when |
|---|---:|---|
| GitHub Pro | $4/month for an individual | Private canonical repositories need required reviews, protected branches/CODEOWNERS and 3,000 Actions minutes |
| GitHub Team | $4/user/month | The canonical repositories move to an organization/team boundary |
| Tailscale Standard | $8/user/month | The tailnet supports commercial production rather than a personal lab |
| Langfuse Core | $29/month | Managed retention/collaboration saves more operator time than self-hosting |
| LangSmith Plus | $39/seat/month + usage | A deliberate LangGraph application needs managed deployment; not for the global factory |
| Phoenix Pro | $50/month | Choose instead of Langfuse when Phoenix wins the trace/eval comparison |
| Temporal Cloud | roughly $100/month starting route + use | A chaos/recovery fixture proves managed durability is worth the spend |

The recommended incremental base is therefore **$4/month for GitHub Pro** during personal development, or about **$12/month** when commercial Tailscale Standard is also required, excluding existing model/coding subscriptions and variable inference. Do not add a second paid agent platform merely to obtain more screens.

### Managed-runtime comparison after the local proof

A complete make/host/buy decision must also compare one managed non-software workflow. This is deliberately after the local integrated lifecycle: managed convenience is not evidence that the canonical authority should move.

| Candidate | Strongest reason to trial | Exclusion/promotion rule |
|---|---|---|
| AWS Bedrock AgentCore | Most modular managed production substrate: framework/model-neutral runtime, identity, policy, gateway, observability and evaluation | Exclude if AWS coupling, export limits or steady-state cost exceed the measured local path; never migrate the canonical work ledger merely to use a module |
| LangSmith Deployment | Fast self-serve durable agent deployment/debugging; Plus includes one small serverless deployment | Trial only for an intentional LangGraph application; exclude as universal factory authority if graph/trace semantics cannot export cleanly |
| CrewAI AMP | Fast role-based business workflow authoring; Basic provides 50 runs | Trial one bounded business flow; exclude if recovery, approval or exact-effect receipts require a second controller |

Use the same non-code vertical slice—such as opportunity discovery to evidence packet to reviewed outreach draft—and measure restart recovery, exact approval, trace/artifact export, model replacement, cost and clean removal. Select at most one managed substrate, and only if it materially beats the admitted local path.

### Defer

- GitLab migration or Premium while GitHub remains the authority;
- Paperclip or Fusion with production credentials;
- Temporal Cloud, Prefect Starter, Hatchet Team, E2B Pro or production AgentCore before a measured workload;
- Port paid, Backstage or Humanitec before the project/service catalog stabilizes;
- Crossplane or Kubernetes without an independent scale requirement;
- enterprise agent suites such as OpenAI Frontier, ServiceNow or Salesforce without an enterprise system-of-record and viable export contract.

## 6. Recommended target architecture

```text
OWNER INTENT
  GitHub issue/project/company declaration
                |
                v
THIN NEUTRAL AUTHORITY KERNEL
  work identity | lease/fence | effect policy | budgets | exact receipts
                |
       +--------+---------+
       |                  |
       v                  v
DURABLE RUNNER         PRODUCT FACTORIES
one of Dapr /          GovCon, research, future
Temporal / Hatchet     companies and projects
       |
       v
REPLACEABLE WORKERS
Codex | Claude | Jules | OpenHands | Hermes/local
       |
       v
POLICY SANDBOX + TOOLS
OpenShell candidate | E2B escape hatch | MCP/A2A adapters
       |
       v
EVIDENCE + OFFLINE EVOLUTION
Git/artifacts | OTel | Inspect | Promptfoo | one trace UI
       |
       v
OWNER ATTENTION VIEW
outcomes | exceptions | blocked work | approvals | evidence | health
```

Paperclip or Fusion can replace the top control-plane experience only if a bakeoff proves that one of them can become the **single** lifecycle authority while preserving or implementing the thin kernel's exact invariants. Otherwise they remain donor/reference systems.

## 7. Decision experiments, not installations

After the owner resolves the freeze/reset authority conflict, use one representative vertical slice and synthetic credentials.

### Bakeoff A: lifecycle/control plane

Compare:

1. GitHub + current CAS kernel;
2. Paperclip at an exact advisory-reviewed revision; and
3. Fusion at an exact stable revision.

Require one task identity, atomic lease, crash/restart recovery, approval bound to an exact effect, exact candidate review, expected-head promotion, clean uninstall and no duplicate terminal state. Test the `agentcompanies/v1-draft` candidate and Fusion's importer as hostile fixtures: import, export, round-trip behavioral equivalence, unknown-extension preservation, immutable source/hash/license provenance, secret references and executable-content denial. The internal declaration format remains undecided until two independent implementations pass.

### Bakeoff B: durable execution

Compare Dapr Agents 1.0, Temporal and Hatchet on the same workflow. Kill workers before and after an external effect, expire leases, replay signals, change workflow versions and prove no duplicate effect.

### Bakeoff C: execution security

Compare current local isolation, OpenShell/NemoClaw and E2B using prompt-injected documents, attempted secret reads, network exfiltration, malicious company packages, stale approvals and teardown/restart.

### Bakeoff D: managed non-code substrate

Only after the local proof, compare AgentCore, LangSmith Deployment and CrewAI AMP on one opportunity-discovery-to-reviewed-artifact workflow. Require restart recovery, exact-effect approval, trace/artifact export, model replacement, cost caps and clean removal. Select none if the local path is simpler or cheaper.

### Promotion rule

Select the smallest option that passes all required scenarios with the least operator time and lowest measured total cost. A feature-count winner that introduces a second authority loses automatically.

## 8. Phased roadmap after approval

### Phase 0 — settle authority and documentation

- Decide freeze resume versus clean-kernel reset.
- Do not merge PR #283 as written.
- Rebase and split it into evergreen intent, approved architecture, generated runtime inventory and disaster recovery.
- Correct authority, port, secret, model and evolution claims.

### Phase 1 — prove one integrated lifecycle

- Complete one issue-to-cleanup journey without operator-supplied stitching.
- Prove interruption and clean-session resume.
- Keep the worker fleet minimal and the current GitHub/CAS authority unchanged during the proof.

### Phase 2 — run the component bakeoffs

- Control plane: GitHub/CAS vs Paperclip vs Fusion.
- Durability: Dapr vs Temporal vs Hatchet.
- Sandbox: current local boundary vs OpenShell vs E2B.
- Managed non-code substrate: AgentCore vs LangSmith Deployment vs CrewAI AMP, only after the local proof.
- Record exact versions, costs, operator minutes, failure recovery and removal receipts.

### Phase 3 — provider and product proof

- Run the same packet through at least two harnesses and two providers.
- Run one real GovCon workflow from source evidence to reviewed business artifact.
- Apply data classification so confidential source material never enters an unsuitable free tier.

### Phase 4 — controlled evolution

- Introduce bounded prompt/skill/routing candidates.
- Evaluate against fixed and held-out fixtures.
- Require independent exact-candidate selection and reversible promotion.
- Preserve failed candidates and reasons so the factory stops repeating them.

### Phase 5 — command center and additional companies

- Build or adopt the attention view only after its underlying authorities are stable.
- Instantiate additional companies/projects from the accepted portable declaration.
- Add portals, cloud substrates or enterprise services only when measured operator load justifies them.

## Final answer

The coherent vision is not “an autonomous coding loop,” “a swarm of permanent personas,” or “a dashboard around several schedulers.” It is a **declarative solo-enterprise operating system** whose unique value is trustworthy authority and evolution across replaceable agents and product factories.

The economical implementation strategy is:

- keep GitHub as the forge and current safe authority baseline;
- pay $4/month for GitHub private-repository governance when needed;
- keep one verified local model gateway and existing local inference capacity;
- treat Hermes, Codex, Claude, Jules and OpenHands as replaceable workers;
- evaluate Dapr Agents first against Temporal/Hatchet for durability;
- evaluate OpenShell against the current boundary/E2B for execution security;
- evaluate Paperclip and Fusion only as mutually exclusive control-plane replacements;
- use free evaluation, observability and backup tiers with explicit privacy classification; and
- own only the neutral authority, receipt, conformance and offline-evolution contracts.

That is the smallest architecture that preserves the original five-month intent without rebuilding maintained infrastructure or surrendering the factory's essential control boundary to an immature upstream.

## Primary evidence index

- [Repository issue #1](https://github.com/redtrades/agent-platform/issues/1)
- [Latest documentation PR #283](https://github.com/redtrades/agent-platform/pull/283)
- [Accepted freeze handoff](https://github.com/redtrades/agent-platform/blob/main/docs/HANDOFF-2026-08-30.md)
- [Historical intent reconstruction](/Users/man/agent-platform/research/GENETIC-SWARM-PLATFORM-DEEP-DIVE-2026-08-30.md)
- [Full external market landscape](/Users/man/agent-platform/research/AGENT-FACTORY-MARKET-LANDSCAPE-2026-08-30.md)
- [Current market/pricing refresh](/Users/man/agent-platform/research/AGENT-FACTORY-MARKET-REFRESH-2026-08-30.md)
- [GitHub plans](https://docs.github.com/en/get-started/learning-about-github/githubs-plans), [included usage](https://docs.github.com/en/billing/reference/product-usage-included), [`gh-aw`](https://github.github.com/gh-aw/)
- [Dapr Agents](https://docs.dapr.io/developing-ai/dapr-agents/)
- [Paperclip](https://github.com/PaperclipAI/paperclip), [security advisories](https://github.com/paperclipai/paperclip/security/advisories)
- [Fusion](https://github.com/Runfusion/Fusion), [releases](https://github.com/Runfusion/Fusion/releases)
- [OpenShell](https://github.com/NVIDIA/OpenShell), [NemoClaw Hermes support](https://docs.nvidia.com/nemoclaw/user-guide/hermes/reference/platform-support)
- [Temporal](https://docs.temporal.io/), [Hatchet pricing](https://hatchet.run/pricing)
- [Inspect AI](https://inspect.aisi.org.uk/), [Promptfoo](https://www.promptfoo.dev/pricing/), [Langfuse](https://langfuse.com/pricing), [Phoenix](https://phoenix.arize.com/pricing/)
- [Cloudflare R2 pricing](https://developers.cloudflare.com/r2/pricing/), [Grafana Cloud pricing](https://grafana.com/pricing/), [Tailscale pricing](https://tailscale.com/pricing)
- [Gemini API pricing and data-use boundary](https://ai.google.dev/gemini-api/docs/pricing), [Groq rate limits](https://console.groq.com/docs/rate-limits)
