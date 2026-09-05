# AISDLC architecture decision

Date: 2026-08-31
Status: approved for implementation planning; control-plane specifics amended
2026-09-03 (see below)
Decision owner: repository owner
Scope: first implementation of the system that builds the system

> **Amendment, 2026-09-03** (`20260903-estate-structure-decision.md`): the
> MVP control plane is **Symphony + Codex** per `agent-sdlc`'s
> `docs/adr/0001-symphony-codex-mvp.md`, not the bounded Fusion trial specified
> below. The Fusion / Paperclip control-plane bakeoff is deferred until a
> working end-to-end issue-to-merge loop exists. The neutral lifecycle contract,
> authority boundaries, and acceptance suite in this document are unchanged and
> still bind whatever control plane is used. The body below is the original
> 2026-08-31 record, retained unchanged.

## Decision

The first system to validate is the agentic software-delivery lifecycle
(AISDLC). It will turn an approved intent into isolated implementation attempts,
deterministic verification, independent exact-candidate review, human- or
grant-controlled promotion, and durable evidence.

The initial implementation will **adopt and compose** an existing lifecycle
engine rather than build another controller. Fusion is the first bounded trial
because its native unit of work is closest to the required software lifecycle:
planning, task execution, Git worktrees, review, and merge. Paperclip is the
immediate control-plane challenger and the later company-factory candidate. The
two must not run as peer authorities over the same work.

`agent-sdlc` will therefore begin as a small composition and assurance
repository. It will hold the neutral acceptance contract, adapters, evaluation
fixtures, policy instances, and exact receipts needed to decide whether Fusion,
Paperclip, or a later candidate is fit. It will not contain a second task
scheduler or lifecycle state machine during the adoption trial.

## Authority boundaries

| Concern | Initial authority | Boundary |
| --- | --- | --- |
| Product intent and source | Owning Git repository | Chat, model memory, and control-plane databases are not product truth. |
| Work identity and lifecycle | One selected lifecycle candidate | Fusion and Paperclip never share authority for the same work item. |
| One agent turn | Selected harness, such as Codex, Hermes, or OpenHands | Harness sessions do not become durable task truth. |
| Workspace isolation | Git worktree or stronger sandbox | A worktree is not a security boundary. |
| Verification | Repository-defined deterministic commands | Model self-report is not verification. |
| Review | Independent reviewer bound to the exact candidate | A generator cannot approve its own material change. |
| Promotion and consequential effects | Human approval or an explicit bounded grant | Approval names the target, scope, and candidate identity. |
| Evidence | Append-only receipts linked to immutable artifacts | Derived summaries do not replace source evidence. |
| Live operational state | Selected control plane's transactional store | Git does not act as a concurrent queue or lease database. |

## Non-negotiable lifecycle contract

Every candidate must support the same externally testable sequence:

```text
intent
-> bounded work item
-> plan and authority check
-> isolated attempt
-> deterministic verification
-> independent exact-candidate review
-> approval or bounded grant
-> expected-head promotion
-> receipt and recovery evidence
```

The acceptance suite must prove:

1. one stable work identity and one terminal outcome;
2. atomic ownership or lease behavior under concurrency;
3. isolation of attempts and preservation of unrelated work;
4. recovery after interruption without duplicate promotion;
5. verification bound to exact inputs and candidate hashes;
6. reviewer independence and review of the exact candidate;
7. approval bound to the exact proposed effect;
8. fail-closed behavior for missing evidence, ambiguous authority, or unresolved
   critical findings;
9. expected-head promotion, rollback, and an attributable action receipt; and
10. measured quality, cost, latency, reliability, risk, operator attention, and
    reversibility.

## Initial implementation stack

| Layer | Decision |
| --- | --- |
| Control-plane trial | Pin Fusion at an exact reviewed revision; run locally with synthetic credentials and data. |
| Challenger | Evaluate Paperclip against the same fixtures in a separate, mutually exclusive trial. |
| Primary platform language | Strict TypeScript with ESM output and pnpm workspaces. |
| Evaluation and model/data workers | Python, behind file/process contracts; no duplicate controller. |
| Human configuration | Schema-validated YAML. |
| Agentic workflow source | Markdown with small YAML front matter when prose is executable. |
| Cross-system contracts | Canonical JSON Schema with generated types; add OpenAPI or Protobuf only at a real service boundary. |
| Receipts and event export | Canonical JSON and append-only JSON Lines. |
| Evaluation | Promptfoo for declarative regression and adversarial cases; Inspect AI for rigorous agent/tool evaluations and logs. |
| Source and promotion | Git, GitHub pull requests, exact commit identities, and repository-native checks. |
| Local execution | Existing Apple-Silicon inference and replaceable cloud/provider adapters; no provider becomes architectural authority. |
| Observability | Structured receipts first; one trace/evaluation UI only after a measured bakeoff. |
| Local deployment | Process or container isolation as required; Docker Compose only where the adopted tool requires services. |
| Cloud deployment | None for v0. |

Do not add Temporal, Conductor, Backstage, Kubernetes, a second workflow engine,
or a custom portal in v0. Hatchet is the first durable-workflow candidate only
if measured recovery or timer requirements exceed the selected control plane.
Dagger is optional after cross-repository build reproducibility becomes a real
problem. Nx is optional after workspace graph or affected-build performance
justifies it.

## Repository topology

Create repositories only at a real ownership, trust, release, deployment, or
commercial boundary.

### `agent-sdlc` — create first

```text
agent-sdlc/
├── apps/
│   └── cli/                       # operator entry point after the trial proves useful
├── packages/
│   ├── contracts/                 # schemas, generated TS types, conformance fixtures
│   ├── governance/                # authority and promotion policy evaluation
│   ├── evidence/                  # artifact identities and receipts
│   ├── adapters/
│   │   ├── fusion/
│   │   ├── paperclip/
│   │   ├── github/
│   │   ├── codex/
│   │   └── hermes/
│   └── testkit/                   # reusable lifecycle and fault fixtures
├── evals/
│   ├── promptfoo/
│   ├── inspect/
│   ├── public-fixtures/
│   └── baselines/
├── workflows/                     # Markdown + front matter source where appropriate
├── policies/                      # schema-validated YAML instances
├── receipts/                      # schemas and ignored local output location
├── workers/python/                # bounded eval/data workers
├── docs/adr/
├── docs/runbooks/
└── tests/
    ├── contract/
    ├── integration/
    ├── fault-injection/
    └── acceptance/
```

This repository may grow into the shared delivery substrate only after an
adopted engine passes the acceptance suite. It must not begin by recreating the
engine being evaluated.

### `agent-knowledge-archive` — keep separate

```text
agent-knowledge-archive/
├── 00-start-here/                 # current decisions and navigation
├── <numbered-subject-packs>/      # normalized history and conflicts
├── manifests/                     # provenance and source identity
├── pointer-only/                  # material not copied into Git
└── work/reports/                  # evidence from archive assembly
```

Its different provenance and promotion rules make it inappropriate as runtime
code, live control state, or an implementation monorepo.

### One repository per operating company — create when admitted

Use literal business names, for example `govcon-factory`, rather than abstract
platform terminology.

```text
<company-repo>/
├── company.yaml                   # goals, ownership, authority ceilings, budgets
├── products/                      # offers and product-specific acceptance criteria
├── workflows/                     # domain business processes
├── roles/                         # domain roles extending shared blueprints
├── knowledge/                     # scoped, publishable knowledge and source pointers
├── policies/                      # domain authority and data-handling overlays
├── evals/                         # domain fixtures, rubrics, baselines, stop rules
├── apps/                          # customer/operator surfaces owned by the company
├── services/                      # domain services, only when required
├── tests/
└── docs/
```

Business-specific workflows belong here because they change with the business,
its evidence, customers, risk, and release cadence. The company consumes stable
AISDLC contracts; the AISDLC does not import company workflow code.

### `agent-company-template` — create after two company implementations agree

```text
agent-company-template/
├── template/
├── schemas/
├── examples/
└── conformance/
```

Do not extract this from one example. Promote only the structure proven common
to at least two materially different company repositories.

### Conditional trust-boundary repositories

- `agent-evals-private`: held-out fixtures and rubrics hidden from generators;
  create when public and sealed evaluation must be administered separately.
- `agent-infrastructure`: deployment configuration with distinct credentials,
  operators, or promotion cadence; local development remains with its owner.
- `agent-capabilities`: independently released, multi-consumer skill/plugin/MCP
  catalog; keep candidate capabilities with their first consumer until a second
  verified consumer exists.
- `agent-contracts`: independently versioned cross-repository schemas and
  generated bindings; keep them in `agent-sdlc` until at least two separately
  released consumers require independent versioning.

## GovCon factory as a bounded reference workload

The GovCon design contributes a demanding non-code acceptance scenario without
becoming the AISDLC roadmap. A representative run must:

1. preserve immutable, versioned source inputs;
2. build a stable, source-linked work graph;
3. distinguish observed fact, source assertion, reviewer judgment, inference,
   and unknown;
4. run mechanical checks separately from judgment reviewers;
5. stop or visibly degrade when inputs, authority, evidence, or reviewer
   resolution are incomplete;
6. require human promotion for material labels and customer-facing effects;
7. compare the exact candidate with frozen baselines and held-out cases; and
8. emit quality, cost, latency, retry, rework, human-attention, and promotion
   receipts.

Procurement schemas, solicitation logic, FAR and agency rules, proposal rubrics,
company evidence, product tiers, outreach, pricing, and the five-stage GovCon
roadmap remain owned by `govcon-factory`. Raw CMP material and identifiable or
sensitive review records remain outside the AISDLC repository and outside Git
where the GovCon design requires it.

## Self-improvement boundary

Prompts, skills, workflows, routing, roles, and retrieval strategies are
versioned candidates. A generator may propose and test a variant, but cannot
change its evaluation criteria, authority, budget, canonical knowledge, or
promotion decision. Automatic promotion is deferred until sealed fixed and
held-out evaluation, baseline-relative improvement, independent exact-candidate
review, regression limits, rollback, and an explicit bounded grant are all
implemented and demonstrated.

## Adoption decision and exit criteria

Fusion is retained only if the pinned trial passes the neutral lifecycle suite,
survives interruption and concurrency tests, exports sufficient evidence, can
be removed cleanly, and creates less integration and operating cost than a thin
composition layer. Paperclip then runs the same suite in isolation. The result
must be recorded as keep, adapt, defer, or reject with exact versions and
receipts.

If neither candidate passes, build only the smallest missing lifecycle kernel
proved necessary by the failures. Do not use a failed adoption trial as
permission to recreate every control-plane feature.

## Evidence basis

- [Current owner decisions](20260831-current-intent-decisions.md)
- [Autonomous software factory evidence pack](../40-autonomous-software-factory/README.md)
- [Infrastructure and orchestration evidence pack](../90-infrastructure-and-orchestration/README.md)
- [Governance, safety, and evidence pack](../100-governance-safety-and-evidence/README.md)
- [Experiments and evolution pack](../80-experiments-and-evolution/README.md)
- [Failures and lessons pack](../110-failures-postmortems-and-lessons/README.md)
- [Current open-source market research](../40-autonomous-software-factory/selected-originals/agent-platform-market-landscape.md)
- [Current cohesive architecture research](../90-infrastructure-and-orchestration/selected-originals/cohesive-agent-factory-vision.md)
- [Fusion](https://github.com/Runfusion/Fusion)
- [Paperclip](https://github.com/PaperclipAI/paperclip)
- [Promptfoo](https://github.com/promptfoo/promptfoo)
- [Inspect AI](https://github.com/UKGovernmentBEIS/inspect_ai)
- GovCon reference reviewed outside this repository:
  `/Users/man/agent-reports/2026-08-31-cmp-corpus-govcon-factory-mvp-design.md`

## Superseded or deferred positions

- The earlier archive boundary that deferred architecture selection is
  superseded for this approved decision; historical documents remain unchanged.
- No historical repository becomes governing merely because some code is
  reusable.
- The specific long-term lifecycle engine, trace UI, one premium model plan,
  production database topology, cloud host, and final company declaration
  schema remain decisions for measured trials.
