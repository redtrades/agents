# GitHub Free private-repository boundary

Verified on 2026-08-28 against the live `redtrades/agent-platform` repository and
current GitHub documentation.

## Available and in use

- Private repository, Issues, subissues, and pull requests.
- GitHub Project 12, linked to this repository.
- Ordinary reviews, comments, labels, assignees, and Git object identity.
- GitHub Actions within the GitHub Free allowance: 2,000 hosted-runner minutes per
  month, 500 MB artifact/package storage, and 10 GB cache storage per repository.
- Self-hosted Actions runners without hosted-runner minute charges.
- Dependabot alerts.

## Not available as enforcement on this plan

- Protected branches for a private repository.
- Repository rulesets for a private repository.
- Required pull-request reviewers or required status checks.
- Enforced CODEOWNERS review.
- Rules requiring signed commits, linear history, merge queue, or deployment success.
- GitHub Secret Protection or GitHub Code Security for this private personal-repo
  setup.

The live rulesets API returned HTTP 403: upgrade to GitHub Pro or make the repository
public.

## Architecture consequence

GitHub is the intent, discovery, collaboration, and evidence surface. It is not the
promotion mutex on the current plan. A separate external controller admits operations,
an independent reviewer evaluates exact candidates, an expected-head promoter performs
eligible promotion, and a derived Project projector reflects receipts. The effect
policy is defined in [`OPERATING-MODEL.md`](OPERATING-MODEL.md).

Server-enforced branch protection remains unavailable. That limit is distinct from
the behaviorally proven external App principal path: issue #103 proved separate
Controller, Reviewer, and Promoter App identities, GitHub Contents CAS claim state,
exact-head review, and expected-head promotion for one bounded fixture. Candidate
workers receive none of those App tokens. This path is external rather than a GitHub
branch rule, and it does not yet prove clean-host reconstruction or provider-neutral
coverage.

## Upgrade trigger

Reconsider GitHub Pro when the cost of maintaining the separate controller, reviewer,
promoter, and projector model exceeds the subscription cost or when unattended
promotion needs required reviews and checks. Making the repository public would also
unlock protections on GitHub Free, but that is not assumed or recommended for private
platform work.

## Official references

- https://docs.github.com/en/get-started/learning-about-github/githubs-plans
- https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches
- https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets
- https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners
- https://docs.github.com/en/billing/concepts/product-billing/github-actions
