# AISDLC MVP implementation plan

Date: 2026-08-31
Status: approved architecture; implementation not yet started
Decision: [AISDLC architecture decision](20260831-aisdlc-architecture-decision.md)

## Goal

Prove that an existing lifecycle engine can execute approved intent through an
isolated, verifiable, independently reviewed, promotion-controlled workflow
across both a software change and one evidence-heavy GovCon-derived fixture.

The MVP is an adoption and assurance trial. It is not a new autonomous company,
full SaaS product, universal workflow language, or replacement control plane.

## Definition of done

The MVP is complete only when:

- one pinned Fusion revision passes the neutral acceptance suite;
- one pinned Paperclip revision has been run against the same applicable suite
  as a mutually exclusive challenger;
- Codex plus at least one local-model path execute the same bounded software
  fixture through replaceable adapters;
- Promptfoo and Inspect AI produce reproducible, exact-candidate evaluation
  records;
- concurrency, interruption, duplicate-effect, stale-head, missing-evidence,
  and rollback scenarios have deterministic results;
- the GovCon-derived fixture proves evidence classes, deterministic/judgment
  separation, human promotion, sealed evaluation, and sensitive-data boundaries;
- quality, cost, latency, reliability, risk, operator attention, and
  reversibility are reported for each candidate; and
- an independent reviewer and the owner approve the keep/adapt/defer/reject
  decision. Passing a smoke test is not completion.

## Phase 0 — establish the delivery ledger

Approval gate before any Phase 0 mutation: the owner separately authorizes
creation of the `agent-sdlc` repository and its initial issue tree. Approval of
this architecture and planning document is not execution authorization for
repository creation, engine installation, or runtime configuration.

1. Create the private `agent-sdlc` repository with issues enabled and a minimal
   branch/PR promotion path.
2. Add one program issue and child issues for the tasks below. Put only ready,
   dependency-clear work on the existing Agent Platform Factory board.
3. Record `AGENTS.md` with repository-specific commands, authority boundaries,
   sensitive-data exclusions, and the rule that adopted engines—not local
   wrappers—own lifecycle state during the trial.
4. Record an ADR index and a decision log. Link this architecture decision as
   the approved source; do not copy the historical archive into the new repo.

Verification:

```text
repository is private
issues and PRs are available
default branch and promotion path are documented
no secrets or absolute machine paths are committed
```

## Phase 1 — scaffold only the assurance surface

Create:

```text
package.json
pnpm-workspace.yaml
tsconfig.base.json
apps/cli/
packages/contracts/
packages/evidence/
packages/governance/
packages/adapters/{fusion,paperclip,github,codex,hermes}/
packages/testkit/
workers/python/
evals/{promptfoo,inspect,public-fixtures,baselines}/
policies/
workflows/
tests/{contract,integration,fault-injection,acceptance}/
docs/{adr,runbooks}/
```

Required first contracts:

- `work-item.schema.json`
- `authority-grant.schema.json`
- `candidate.schema.json`
- `verification.schema.json`
- `review.schema.json`
- `approval.schema.json`
- `promotion.schema.json`
- `action-receipt.schema.json`
- `capability.schema.json`

Author canonical schemas once and generate TypeScript types. Python workers
validate against the same schemas rather than maintaining parallel models.

Tests first:

- schema dialect and version are explicit;
- unknown optional fields round-trip;
- unsupported required capabilities fail closed;
- identities and hashes remain stable;
- secret values and absolute paths are rejected from portable records; and
- receipts name actor, purpose, scope, target, authority, inputs, outputs,
  timestamps, verification, effect, and budget when applicable.

Rollback: delete the unpromoted topic branch; no runtime or data migration exists.

## Phase 2 — encode the neutral acceptance fixtures

### Fixture A: bounded software change

Use a disposable repository with a small typed behavior change, deterministic
tests, one intentionally stale base, one injected reviewer rejection, and one
interrupted run. The expected outcome is one reviewed candidate and at most one
promotion.

### Fixture B: GovCon-derived evidence workflow

Use synthetic, non-sensitive records only. The fixture reconstructs versioned
inputs, builds a stable source-linked requirement graph, produces an
evidence-bounded artifact, separates deterministic checks from labeled
judgment, routes unresolved evidence to human review, and refuses promotion when
a critical source or approval is missing.

This fixture must not contain CMP proposal text, real company data, procurement
legal advice, outreach, pricing, or the GovCon implementation roadmap.

### Fault matrix

Test at minimum:

- competing claimants for one work item;
- worker termination before and after producing a candidate;
- duplicate callback or retry;
- stale expected head at promotion;
- candidate changed after verification or review;
- approval referring to a different candidate;
- missing source, failed extraction, unsupported claim, and unresolved reviewer
  conflict;
- local model unavailable or rate-limited provider;
- receipt store temporarily unavailable; and
- clean uninstall and restoration of the pre-trial state.

Approval gate: owner approves the exact public fixtures and confirms that no
sensitive GovCon material entered Git.

## Phase 3 — run the Fusion-first trial

1. Select and record an exact Fusion revision, license, documented security
   posture, services, ports, storage paths, and uninstall procedure.
2. Start it in a disposable local environment with synthetic credentials and
   no production repository or provider authority.
3. Implement only the adapter needed to translate neutral fixture identity,
   state, candidate, verification, review, approval, promotion, and receipt
   evidence. Do not fork Fusion or patch its core during the first pass.
4. Run Fixture A with Codex, then the same fixture through one verified local
   model/harness route.
5. Run the applicable parts of Fixture B.
6. Run the fault matrix, export evidence, uninstall, and prove the pre-trial
   environment is restored.

Record observed capability separately from claimed capability. Any missing
contract becomes a named gap with evidence, not an automatic custom feature.

Stop conditions:

- duplicate or ambiguous promotion;
- inability to bind approval/review to an exact candidate;
- unrecoverable work or unexplained terminal state;
- host-wide unsandboxed authority beyond the approved trial;
- inability to export necessary evidence; or
- cleanup that cannot restore the original state.

## Phase 4 — establish evaluation and receipts

Promptfoo owns declarative provider/prompt regression and adversarial cases.
Inspect AI owns tool-agent tasks, sandboxed execution where applicable, scoring,
and inspectable logs. Neither owns production promotion.

For every run, store:

- exact fixture, workflow, policy, prompt/skill, model/provider, adapter, and
  candidate versions;
- deterministic result and independent-review result;
- machine time, tokens/cost where measurable, human review time, retries,
  interventions, rework, and operator attention;
- environment and isolation class;
- failure category, recovery result, rollback result, and residual effects; and
- content hashes linking the receipt to exact inputs and outputs.

Freeze the confirmatory suite before comparing candidates. Keep candidate
generators blind to held-out cases. A later change to criteria returns the run
to exploratory status.

## Phase 5 — run the Paperclip challenger

Run Paperclip in a separate disposable environment at an exact advisory-reviewed
revision. Apply the same neutral fixtures and measurement contract. Paperclip
may be evaluated for goals, budgets, approvals, schedules, and company semantics;
do not give it peer authority over a live Fusion run.

Where a fixture is not applicable, record `not-applicable` with the contract
reason. Do not award credit for features that were not demonstrated locally.

Stop immediately on unresolved credential, command-execution, cross-scope,
approval-attribution, or sandbox-boundary risk.

## Phase 6 — independent comparison and selection

The generator writes an evidence table but does not select itself. A fresh
independent reviewer checks the exact versions, fixtures, receipts, failures,
cleanup evidence, and proposed disposition.

For each candidate decide:

- **keep**: use without core modification;
- **adapt**: retain behind a thin, bounded adapter with named gaps;
- **defer**: promising but not justified by current requirements; or
- **reject**: fails a hard invariant or costs more to operate than it removes.

The decision must address quality, cost, latency, reliability, risk, operator
attention, reversibility, local-model behavior, evidence export, upgrade burden,
and clean removal. Feature count, stars, and marketing claims are not selection
criteria.

Approval gate: the owner approves the lifecycle authority before any production
repository, credential, scheduled work, or company workflow is connected.

## Phase 7 — first controlled use

After approval, run one low-risk real software change in a non-production
repository. Require a human approval before promotion. Compare the result with
the repository's normal Codex workflow and record the incremental benefit and
operator burden.

Only after that slice passes may the project plan:

1. a GovCon factory integration using the domain repository's own approved
   implementation sequence;
2. company declarations and tiered authority;
3. bounded self-improvement candidates; or
4. additional infrastructure.

## Issue sequence for `agent-sdlc`

Create these only when Phase 0 is authorized:

1. `Define neutral AISDLC contracts and receipt schemas`
2. `Build the software and GovCon-derived acceptance fixtures`
3. `Run the pinned Fusion lifecycle trial`
4. `Add Promptfoo and Inspect AI evaluation receipts`
5. `Run lifecycle recovery and fault-injection tests`
6. `Run the pinned Paperclip challenger trial`
7. `Review exact evidence and select the lifecycle authority`
8. `Run one controlled real-software vertical slice`

Each issue must state dependencies, exact scope, acceptance checks, rollback,
authority required, and the evidence needed to close it. Do not mark a child
ready until its predecessor's acceptance conditions pass.

## Decisions deliberately deferred

- production use of Fusion or Paperclip;
- a custom controller or universal workflow DSL;
- Temporal, Conductor, Backstage, Kubernetes, and cloud hosting;
- the tracing/evaluation UI;
- the final company declaration schema;
- the premium model subscription choice;
- extraction of contracts, capabilities, infrastructure, or company templates
  into separate repositories; and
- automatic promotion of self-improvement candidates.

## Documentation and evidence produced during execution

Every phase updates:

- the program issue and board item;
- an ADR or decision-log entry when a material decision changes;
- the relevant runbook before an operator-only step;
- an append-only experiment record with exact versions and receipts;
- a checkpoint describing completed work, pending effects, blockers, and next
  action; and
- the pull request with verification and independent-review evidence bound to
  its exact head.

Do not create a second status system. GitHub issues and the existing project
board are the work ledger; repository artifacts are the technical record.
