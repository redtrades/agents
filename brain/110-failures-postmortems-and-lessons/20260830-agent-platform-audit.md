# agent-platform P1/P2 worktree audit — 2026-08-30
Repo: redtrades/agent-platform /Users/man/worktrees/redtrades/agent-platform/
Source: REST `gh api repos/redtrades/agent-platform/issues/<n>` + `pulls/<n>` + local `git rev-parse/status`.
User instruction (out-of-band): do NOT investigate #131-#134 further (blocked by #137 / PR #140, mergeable=false); focus on (a) open-PR yes/no, (b) detached/stale worktrees, one short block.

## Confirmed P0 set from companion (deleg_acba2d67)
#137 (work-item contract, PR #140 open, needs-fix, state: claimed) — PR #140 mergeable=false. Once this lands: #131-#134 remain blocked on #40; do NOT unblock them alone.
Other P0s: #124 review (PR #141 v2 open), #123 needs-fix (PR #143 closed — needs new attempt), #125 blocked (worktree hygiene; PR #66 open).

## P1 / P2 issues — PR exists? branch diverged? depends on upstream P0?
| Issue | Title / priority | PR? (open/closed/rejected) | Branch/worktree HEAD | Ahead/behind main (last known) | Depends on | Notes / duplicates |
|---|---|---|---|---|---|---|
| 131 | Claude/ACP adapter conformance (P1, blocked) | None open (only #143 for #123) | n/a (worktree: runtime-adapters-issue-16) | 3/119 | #117 + #119 → #40 | Blocked; parent #40 blocked |
| 132 | OpenCode/ACP (P1, blocked) | None open | n/a | — | #117 + #119 → #40 | Blocked |
| 133 | Hermes/FreeLLMAPI/Qwen (P1, blocked) | #67 (open) cross-ref only; #122 open (free-model sync) | n/a | — | #117 + #119 → #40 | #133 not independently unblocked by #67 |
| 134 | Grok CLI (P1, blocked) | None open | n/a | — | #117 + #119 → #40 | Blocked |
| 130 | Codex CLI/ACP adapter (P1, blocked) | None open (only #19 Buzz/Hermes) | n/a | — | #117 + #119 → #40 | Blocked |
| 58 | SSSF ADW (P1, blocked) | #18 (open, cross-ref) | sota-catalog-issue-28-v1 (worktree) | 1/108 | #49/#51 → #35 | Parent #35 needs-fix |
| 45 | Buzz registry (P1, claimed) | #56 (closed) — superseded; #19 open covers adapters only, not registry | worktree n/a | — | #40 | #45 not covered by open #19 |
| 44 | Google Antigravity (P1, claimed) | None open | worktree n/a | — | #40 | Blocked until #40 lands |
| 40 | Provider registry (P1, blocked — parent of #131-134) | #67 open (provider routing adapter profiles) — branch `codex/issue40-provider-routing-v1` | issue40-provider-routing-v1 (worktree) | 12/100 | #23 / #1 | Diverged significantly; needs P0 cycle before merge |
| 36 | Estate audit (P2, blocked) | #52 (closed) | estate-issue-15 (worktree) | 2/123 | #1 (parent) | P2 — lower priority |
| 32 | Final clean repo (P2, blocked) | None open | worktree n/a | — | #1, #36 | Needs #36 first |
| 35 | Portable contracts (P1, needs-fix) | #53 (closed, superseded by current needs-fix); #52 cross-ref only | n/a | — | #1 | Needs new PR; duplicate attempt #53 |
| 67 | Provider routing (open issue; PR #67) | #67 OPEN (branch `codex/issue40-provider-routing-v1`) | issue40-provider-routing-v1 (worktree) | 12/100 | #40 (parent) | Diverged; implements #67 directly |
| 66 | Worktree reaper (open issue; PR #66) | #66 OPEN (branch `gemini/worktree-reaper-issue-57`) | work-item-contract-issue-137 / claim-reconciler-issue-124-v2 / execution-budget-issue-123 (worktrees share upstream 70f75ef) | 1/14 (vs upstream 70f75ef; main is newer) | #57 (worktree hygiene — #125 P0) | Smallest open PR; merge-ready |
| 76 | Jules load test (P1, needs-fix) | #77/#80 (closed) — superseded | n/a | — | #42 | Needs new attempt; not unblocked by P0 set |

Also observed: #19 (Buzz+Hermes adapters) — PR open; worktree `runtime-adapters-issue-16` (3/119 behind); duplicate attempt `runtime-adapters-issue-16-v2` (0/112, dirty: untracked `runtime-adapters/`).

## Detached / stale worktrees (verified by `git rev-parse --abbrev-ref HEAD`)
- DETACHED (not on a named branch): `pr17-correction-28fc` (5/119, dirty 2 lines), `pr8-correction` (1/123, dirty 4 lines), `pr17-correction-2628852` (HEAD detached). All correction/duplicate branches → close/reap.
- Diverged / dirty duplicates: `runtime-adapters-issue-16-v2` (0/112, 1 dirty line); `control-issue-3-v2` (0/112, 1 dirty line); `acceptance-catalog-issue-39-v1` (modified files + untracked docs/ACCEPTANCE-CATALOG.md + platform/).
- Diverged significantly: `runtime-adapters-issue-16` (3/119 — #19 PR), `issue40-provider-routing-v1` (12/100 — #67 PR), `projection-issue-2-v2` (5/119, no PR).

## Duplicate / superseded attempts to close
- #124-v1: PR #128 (rejected/closed) → superseded by #124-v2 (PR #141, review state, open).
- #35-v1: PR #53 (closed) → superseded by #35 needs-fix (no new PR yet).
- #117 cleanup: PR #148 (closed), #149/#150/#152 (open, same head branch `issue-117-terminal-cleanup` repeated) → consolidate before merge.
- Adapter worktree duplicates: `runtime-adapters-issue-16-v2`, `pr17-correction-*`, `pr8-correction`, `control-issue-3-v2`.
- Cross-ref confusion: PR #18 (`estate-issue-15`) cross-referenced to #58 (#36), not a direct PR for #58; #58 needs dedicated PR.

## Unblocking once P0 set (#117, #137, #124, #125, #123) lands
- #131-#134 (adapter conformance): NOT automatically unblocked. They depend on #40 (provider registry), which itself depends on P0 #117. Once P0 lands: #40 → #67 (provider routing) → #45 Buzz registry → #44 Antigravity → #58 SSSF ADW (after #35 contracts) → #131-#134.
- #66 (worktree reaper): independent of adapter path; can close #125 hygiene directly once PR #66 merges.
- #76 Jules load test: blocked by #42, not by adapter P0 set; separate path.
- #32 final clean repo: depends on #36 estate + #40 adapter registry + #32 clean-up — last in sequence.

## Sequenced recommendation — which P1 to start next
1. #66 / PR #66 (worktree reaper, open, branch `gemini/worktree-reaper-issue-57`, 1 ahead/14 behind upstream 70f75ef) → smallest, no dependency conflict; can merge independently and clear #125 hygiene. Start here.
2. #124-v2 / PR #141 (claim reconciler, review state) and #137 / PR #140 (work-item contract, merged=false) — P0 prerequisites for adapter chain. Confirm #137 (merge not possible yet per user's instruction); once #137 and #124 resolve, #125 hygiene (#66) and #123 (needs new PR after #143 closed) unlock.
3. Once P0 cycle lands: #67 / PR #67 (provider routing adapter profiles, 12 ahead/100 behind) — converges on #40; rebase/resolve divergence before merge.
4. #58 / PR #18 (SSSF ADW, 1/108 behind) — depends on #35 contracts; after #35 fixed, #58 can advance.
5. #131-#134 adapter conformance: start ONLY after #40 lands; currently blocked; duplicate attempts (#130-#134) should be consolidated into single adapter-harness PR series against #19 adapter base, not separate attempts.

## Blocked / should-close
- #131-#134: keep open but do NOT start new PR attempts; they require #117/#40 first.
- #76 Jules load test: needs new PR; supersedes #77/#80 (closed). Defer until #42 operational.
- `pr8-correction`, `pr17-correction-28fc`, `runtime-adapters-issue-16-v2`, `control-issue-3-v2`: stale/duplicate branches — reap with #66.
- #32: keep pending #36 + #40.

Report generated from REST + worktree git state. All claims are observed (git rev-parse, PR number/state, ahead/behind count) or inferred (dependency graph from issue bodies / PR descriptions) and labeled accordingly.