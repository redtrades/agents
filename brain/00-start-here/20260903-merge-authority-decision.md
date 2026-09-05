# Merge authority decision

Date: 2026-09-03
Status: approved, active
Decision owner: repository owner
Scope: how agent-authored pull requests are merged, across every repository in
the estate

## Decision

**Merge authority is risk-adaptive. A change's blast radius, not its file path,
decides who merges it.**

This supersedes the earlier path-based tiers (agent-configs `DECISIONS.md`
D-001: "no agent merges Tier 2, ever" for anything under `rules/`, plans, SOPs,
or `MASTER-GUIDE.md`). That rule over-blocked: a one-word clarification to a
rule and a new hard-blocking hook were both "Tier 2" despite carrying very
different risk, so every trivial governing edit waited on the owner and did not
scale with pull-request volume.

### Class A — an agent may merge

On green checks plus an independent review by a different model family than the
author:

- Documentation, evidence, dated reports, run artifacts, non-governing notes.
- Code that passes its checks and review.
- Low-risk governing changes: additive prose that transcribes a directive the
  owner already gave; verbatim extraction, relocation, or de-duplication of
  already-approved content; a revert to a previously-approved state; typo, link,
  formatting, or cross-reference fixes; a new judgment-tier rule file that adds
  no mechanical check.

### Class B — the owner merges

- Any change to an enforced mechanism: merge authority itself, permission
  posture, allow/deny/ask lists, hook logic, gate thresholds, required checks,
  branch protection.
- Any new or altered standing constraint on agent behavior that is not a direct
  transcription of an owner directive.
- Security or trust boundaries, credential handling, schema, data-loss guards.
- Structural changes to a repository's master guide or lifecycle definition.
- Anything an agent is not confident is Class A. **Unsure is Class B.**

### Conditions on every agent-merged Class-A governing change

1. The pull-request body names the class and the specific reason it qualifies.
2. The cross-family reviewer confirms the class call, not only the content.
3. The change is revertable in one commit.
4. One line records what was merged and under which class, in that repository's
   decisions log or a dated evidence file.

Unchanged: an agent never accepts its own proposal; owner-reserved issues are
never self-assigned; merges are real merge commits, not squashes.

## Provenance

Owner directive, 2026-09-03: "merge and then change their merge authority so
it's risk adapted that we establish that in the knowledge archive and other
repositories." Issued after a session held a pull request of three additive
prose rule files, citing the flat D-001 rule as a blocker. The owner's ruling
is that the flat rule does not fit the stated 95%-autonomy target, which needs
the owner in the loop for changes that can break the system, not for every edit
under a governing directory.

## Operative locations

- **agent-configs** `rules/merge-authority.md` and `DECISIONS.md` D-006 — the
  enforced version agents read.
- **agent-sdlc**, **agent-platform** — align their "user-held merge authority"
  references to this class model; agent-platform keeps its stricter
  promoter-app promotion path where one exists, as an additional control, not a
  contradiction.
- This file is the canonical cross-repo statement. Per this archive's own
  boundary (`HOW-TO-READ-THIS-ARCHIVE.md`), recording the decision here does not
  itself enforce anything; the enforcement lives in the operative repositories
  above.
