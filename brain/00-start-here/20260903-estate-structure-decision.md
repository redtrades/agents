# Estate structure decision

Date: 2026-09-03
Status: approved, active
Decision owner: repository owner
Scope: which repositories are canonical, operative, implementation, and historical
evidence; and the control-plane specifics of the AISDLC trial

Supersedes: the control-plane specifics of owner interview decision 58 and
`20260831-aisdlc-architecture-decision.md`. Confirms and operationalizes
interview decisions 6, 7, and 8. Historical documents remain unchanged; this
file is the current record.

## Context

A first-principles conflict analysis on 2026-09-03
(`~/agent-reports/estate-consolidation-2026-09-03/BRIEF.md`) found the estate
running two competing reboots. `agent-platform` performed a "clean rebuild"
around 2026-08-29 and its `AGENTS.md` still declares itself "the canonical
source." The 2026-08-31 owner interview (this archive, decisions 1-58) already
demoted `agent-platform` to historical evidence, but its agents kept working
there: it remained the most active repository in the estate (98 worktrees, 141
branches) and was running the AISDLC lifecycle in parallel with `agent-sdlc`,
both hitting the same failure class (death loops, duplicate task spawning, no
completed issue-to-merge). Everything else was frozen mid-flight.

## Decision

### 1. `agent-platform` is historical evidence, not canonical

Confirms interview decision 7. `agent-platform`'s "canonical source" claim is
superseded. Its `AGENTS.md` is demoted to a historical-evidence header; its
design docs (`START-HERE.md`, the delivery-chain contract, `REVIEW-PROTOCOL.md`,
the delivery-failure ledger) remain readable as evidence and migration sources,
never as governing instructions. Existing code carries no authority merely by
existing (interview decision 8).

### 2. One AISDLC effort: `agent-sdlc`

`agent-sdlc` is the sole implementation repository for the AISDLC trial
(interview decision 58). The parallel AISDLC lifecycle work in `agent-platform`
stops. Anything still useful in `agent-platform`'s parallel effort — failure
analysis, adapter code, the delivery-failure ledger patterns — is harvested into
`agent-sdlc` as evidence or migrated code, then `agent-platform` is frozen.

### 3. AISDLC control plane: Symphony + Codex first, not Fusion

Interview decision 58 and `20260831-aisdlc-architecture-decision.md` specified
a bounded Fusion adoption trial with Paperclip as a mutually exclusive
challenger. `agent-sdlc`'s own `docs/adr/0001-symphony-codex-mvp.md`
(2026-09-01, accepted) instead selected Symphony as the sole MVP-0 issue
controller and Codex app-server as the sole execution harness, on the reasoning
that every added candidate delayed the basic issue-to-merge loop. That narrowing
is ratified. The Fusion / Paperclip control-plane bakeoff is deferred to after a
working end-to-end issue-to-merge loop exists. The neutral lifecycle contract and
acceptance suite in `20260831-aisdlc-architecture-decision.md` are unchanged
and still bind whatever control plane is used.

### 4. Policy and rules: operative in `agent-configs`, canon here

The enforced rule surface, hooks, the runtime-adapter generator, and the
canonical `AGENTS.md` contract stay operative in `agent-configs`. The canonical
statement of every governing decision (merge authority, canonical-contract
model, this estate structure) lives here in `00-start-here/`. Each `agent-configs`
rule cites its canonical decision in this archive. This matches interview
decisions 16 (small stable organizational core) and 30 (policy is its own
concern). Whether `agent-configs` is later renamed or split into a clean core is
a separate, lower-priority decision.

### 5. Historical-evidence repositories, retired

`agent-mesh`, `agent-workspace`, and `govcon-factory` are historical evidence
(interview `selected-copy` disposition). Each gets a historical-evidence header
on its `AGENTS.md` / `README`. They are frozen: no new feature work, branches
pruned over time, worktrees removed. Their `preserve/uncommitted-2026-08-29`
branches are retained untouched as evidence. Reviving any of them for a named
reason is an owner decision.

## Resulting active surface

| Concern | Repository |
|---|---|
| Knowledge, canon, historical evidence | `agent-knowledge-archive` (this repo) |
| Operative policy, rules, hooks, contract source | `agent-configs` |
| AISDLC implementation trial | `agent-sdlc` (Symphony + Codex) |
| Runtime contract adapters (generated only) | `~/.agents`, `~/.claude`, `~/.codex`, `~/.hermes` |
| Historical evidence, frozen | `agent-platform`, `agent-mesh`, `agent-workspace`, `govcon-factory` |
| Deliverables the owner reads | `~/agent-reports/` (not a git repository) |

## Provenance

Owner directive, 2026-09-03: brief decisions 1-5 approved verbatim ("1-5 your
assumptions are correct. approved"), after the conflict analysis was reviewed
and one correction accepted (agent-sdlc has a live MVP session; leave it
untouched, ratify its ADR rather than realign it).
