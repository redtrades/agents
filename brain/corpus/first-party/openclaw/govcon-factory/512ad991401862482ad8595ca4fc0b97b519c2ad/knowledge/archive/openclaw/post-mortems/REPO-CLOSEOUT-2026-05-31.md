# Repo Closeout — 2026-05-31 (executed 2026-06-02)

Triage + merge of the 5 open PRs across the three OpenClaw repos. **Finding: 4 of 5 were already merged before this session; the 5th (v3 scaffold) is a DRAFT with failing CI and was correctly NOT merged.** No new merges were performed — the work was already landed. This artifact records the verified end state and files the three cleanup follow-ups.

## PR triage table

| # | Repo | Final state | Merge SHA | One-line summary |
|---|------|-------------|-----------|------------------|
| 2243 | redtrades/openclaw | **MERGED** | `c664dc515936fd44ec8c2b6fee06d91dc6213a6d` | SOTA scan: personal multi-vendor agent system (mid-2026) |
| 2244 | redtrades/openclaw | **MERGED** | `33b97fe80a04d8567590bd2eafb6ddbe264a438c` | GH housekeeping 2026-05-31 — branch/issue/tag cleanup readout |
| 2245 | redtrades/openclaw | **MERGED** | `dc57c472384709f95a7af0b3e184073391ed9b9a` | Sprint 2026-05-27 — autonomous 35+ commits across A–V + W–FF lanes |
| 377 | redtrades/openclaw-v2 | **MERGED** | `d7d9dc243e7d64752309e9b3d8c01f66580e458a` | Sprint 2026-05-27 — v2 substrate companion commits (13 commits) |
| 1 | redtrades/openclaw-v3 | **OPEN / DRAFT — NOT MERGED** | — | init: openclaw v3 scaffold — courtroom architecture |

All four merged PRs were squash/merge-committed prior to this session (consistent with `git log origin/main`). No `--admin`, no force-push, no force-merge used. Branches were not deleted (`--delete-branch=false` policy honored; `sprint-2026-05-27-push` retained for tag association).

## Why v3 #1 was not merged (needed a human touch)

Two independent blockers:

1. **It is a DRAFT PR** — not marked ready for review.
2. **CI `test` check is FAILING** — per the constraint "if a PR has failing CI, do NOT merge — surface and stop on that one."

Literal failure (`gh run view 26842577824 --log-failed`):

```
FAILED tests/test_graph.py::test_judge_is_cross_family - AssertionError: judge google shares a family with a generator ['google', 'xai']
assert 'google' not in ['google', 'xai']
1 failed, 33 passed in 0.87s
```

The judge-selection logic picked a judge whose model family (`google`) collides with a generator family — violating the cross-family invariant the courtroom architecture requires. This is a real correctness bug in the scaffold, not flake. **Mike / a code session must fix the judge cross-family selection (likely related to the YAML parse fallback filed as openclaw-v3#2) and mark the PR ready before it can merge.**

## Follow-up issues filed (NOT executed)

| Issue | Repo | Topic |
|-------|------|-------|
| [#2](https://github.com/redtrades/openclaw-v3/issues/2) | openclaw-v3 | YAML parse robustness — judge first-label fallback + grok double-fenced claim; reproducer case dirs under `agent_os/cases/` (`ed6199d2-…`, `_example/`); notes likely link to the failing `test_judge_is_cross_family`. |
| [#2263](https://github.com/redtrades/openclaw/issues/2263) | openclaw | Runaway issue-creator at #1640 spawned ~165 duplicate `[bug] BOOTSTRAP.md stale` issues — investigate + add dedup BEFORE bulk-close. |
| [#2264](https://github.com/redtrades/openclaw/issues/2264) | openclaw | Project #9 board sync blocked on missing `read:project` token scope — `gh auth refresh -s read:project` unblocks it. |

## Final-state verification (literal output)

`gh pr list --state open`:

```
=== openclaw ===
(exit 0)            # 0 open PRs
=== openclaw-v2 ===
(exit 0)            # 0 open PRs
=== openclaw-v3 ===
1	init: openclaw v3 scaffold — courtroom architecture	init-scaffold	DRAFT	2026-06-02T02:40:41Z
(exit 0)            # 1 open (DRAFT, failing CI — intentionally retained)
```

`git -C ~/.openclaw log origin/main -5 --oneline`:

```
c664dc515 Merge pull request #2243 from redtrades/sota-scan-2026-05-31
33b97fe80 Merge pull request #2244 from redtrades/gh-cleanup-2026-05-31
a728e8c8c chore(memory): resolve post-pull log conflicts
dc57c4723 Merge pull request #2245 from redtrades/sprint-2026-05-27-push
6f84673d8 docs(sprint): post-sprint push readout 2026-05-31 …
```

`git -C ~/.openclaw-v2 log origin/main -5 --oneline`:

```
76896ec1d chore(infra): sync hardened mem0 plist template from launchd [via dispatch]
d7d9dc243 Merge pull request #377 from redtrades/sprint-2026-05-27-push
3533c57ad Merge remote-tracking branch 'origin/main' into sprint-2026-05-27-push
5b54bc89c feat(hermes): load versioned prompt from ~/.openclaw + log version per call …
ba6f5a5bc feat(.agents): mirror v1 governance kernel via absolute-path symlinks …
```

`git -C ~/openclaw-v3 log origin/main -5 --oneline`:

```
b6cc780 chore: initialize repository
```
(v3 main holds only the init commit; the scaffold PR #1 is unmerged.)

Tag verification — `gh api repos/redtrades/openclaw/tags --jq '.[].name' | grep sprint-2026-05-27-final`:

```
sprint-2026-05-27-final
```

## Items that needed a human touch

| Item | Why | Resolution path |
|------|-----|-----------------|
| openclaw-v3 #1 | DRAFT + failing CI (`test_judge_is_cross_family`) — real judge cross-family bug | Fix judge selection (see openclaw-v3#2), un-draft, then merge |
| Project #9 sync | `read:project` scope missing on automation token | `gh auth refresh -s read:project` (filed as #2264) |
| 165 dup BOOTSTRAP-stale issues | Runaway creator at #1640 lacks dedup | Investigate before bulk-close (filed as #2263) |

---

*Generated during repo closeout. The four merges predate this session; this artifact verifies end-state and files follow-ups. This readout PR is the closeout artifact — Mike merges it last.*
