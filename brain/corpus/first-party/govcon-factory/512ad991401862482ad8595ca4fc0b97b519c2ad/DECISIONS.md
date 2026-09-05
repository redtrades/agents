# DECISIONS

The decision record. One entry per significant choice: what we picked, what
we rejected and why, where the evidence lives. [CHANGELOG.md](CHANGELOG.md)
has the "what happened when" — this file has the "why," which outlives the
commit that implemented it.

**Rule:** a new significant decision (product/pricing shape, a rejected
alternative, a standing "never do X," a superseded architecture choice) gets
an entry here in the same PR that makes it. See AGENTS.md's "History and
decisions" section.

Status values: **active** (current), **superseded** (replaced by a later
decision — this file still explains why the earlier call was made),
**reversed-partially** (partly walked back, not fully).

---

### D-001: Price coverage/time, never a win-rate claim
- **Date:** 2026-08-21
- **Decision:** The product is priced and marketed as coverage/effort substitution ("we found and mapped this so you don't have to"), never as a win-probability or ROI claim.
- **Alternatives considered and rejected:** The original source plan priced a $5,000/yr subscription on "one won recompete = $500K–$5M+ → 100–1000x ROI" — an outcome/win-rate claim (candidate B in the MECE analysis). Rejected because no document in the repo, then or since, supplies the one number that claim requires: the probability the product changes a customer's win rate. Every piece of actual evidence (the plan's own "pain ranked by willingness to pay" section) pointed at discovery/coverage pain instead.
- **Status:** active — the one decision that survived unreversed through V2→V6, even as SKU count and price level changed repeatedly.
- **Source:** `archive/plans/plan-history/PLAN-V2.md:13,19-27,33`; restated `archive/plans/PLAN-V3.md:13`; current copy `sop/MARKETING.md:145-146`.

### D-002: Snapshot-first ladder → single $699 opportunity packet
- **Date:** 2026-08-21 (V2) → 2026-08-22 (V3 ladder) → 2026-08-23 (V5 single SKU)
- **Decision:** One product: a $699 opportunity packet (one live notice × one firm), plus a free industry report as magnet. No subscription tier, no ladder.
- **Alternatives considered and rejected:** V2 kept a $5,000/yr "Core" subscription with a promoted $750 Snapshot. V3 replaced Core with a three-rung ladder ($450 Sources Sought response → $750 Market Snapshot → $1,500+ compliance red-team), with "Core" deferred but never actually scoped, priced, or given a cadence anywhere in the repo (flagged in `sop/financial-model/SUMMARY.md:57`). V5 retired the ladder outright: "Do not silently revert to the $450/$750 two-SKU story" — Mike's own words, correcting a packaging drift from an earlier agent generation, not a product he'd asked for. Live copy still quoted $450/$750 for hours after V5 shipped; cleaned up separately by TASK-0021 (2026-08-23).
- **Status:** active (V5/V6 shape).
- **Source:** `archive/plans/plan-history/PLAN-V2.md:52,78`; `archive/plans/PLAN-V3.md:13,17`; `archive/plans/PLAN-V5.md:13,15,21,53-57`; commits `77a32a3`, `b078f89`, `1ab199c`, `067cee8` (TASK-0021).

### D-003: SSSF rejected as a hard dependency, then partially reversed to SSSF-shape-native
- **Date:** 2026-08-22 (rejected) → 2026-08-23 (partial reversal)
- **Decision:** The factory's deterministic pipeline stages (`ingest → normalize → triage → match → assemble → gate`) run for real as SSSF `kind="code"` ADW phases against Mike's live `~/agent-workspace/adws/` install. The one agent-driven stage (`synthesize`) does not use SSSF — it's plain Python making direct model calls.
- **Alternatives considered and rejected:** PLAN-V3 originally rejected running SSSF at all — "do not run the SSSF dependency (frozen repo, pi-only, broken diff gate)" — and specified reimplementing its `gate(envelope, run) → GateReport` pattern natively instead. That native reimplementation became `factory/` (typed envelopes, gate registry, runner). When Mike's SSSF install matured, the deterministic half was wired into it directly rather than staying purely native, because the installed SSSF's `coding_agent: claude_code` path is a confirmed stub (`agent_cc.py` raises `NotImplementedError` unconditionally) — so only the non-agent phases could run under real SSSF; `synthesize` (the one agent phase) shipped as a third path, judged "more literal" and needing zero new infrastructure.
- **Status:** reversed-partially — native for the agent stage, SSSF-integrated for the deterministic half.
- **Source:** `archive/plans/PLAN-V3.md:38`; `specs/factory-architecture.md:1-9, §8`; commit `f5241b0`; trace `runs/3e625951/sssf_trace_excerpt.json`.

### D-004: Markdown task board superseded by GitHub Issues
- **Date:** created 2026-08-22 (`ce4ec77`), superseded 2026-08-23 (PR #25)
- **Decision:** GitHub Issues on `redtrades/govcon-factory` is the live work queue every agent type pulls from (`gh issue list --label ready`). `tasks/*.md` is historical record only; `BOARD.md` generates from `status/issues-snapshot.json`, not from the markdown files.
- **Alternatives considered and rejected:** The original `tasks/*.md` + `BOARD.md` + claim/release/complete-script system (built 2026-08-22) worked but was a second, divergent store that only agents with repo write access could update, and gave no free auditing (labels, cross-references, auto-filed failures) that a real issue tracker provides. Superseded because it didn't scale to multiple agent types (Claude, Codex, Hermes, a cron poller) needing the same queue through a common interface — `gh` CLI, no special access.
- **Status:** superseded. `tasks/*.md` kept for git-blame provenance on why a task was framed a certain way; `github_issue:` frontmatter links old tasks to their live issue.
- **Source:** `AGENTS.md:68-122`; commits `ce4ec77` (created), `cad2836`, `d63f1b2`, `6fae993` (superseded), PR #25.

### D-005: Sell-first reversed to factory-first
- **Date:** 2026-08-21 (V2 sell-first design) → 2026-08-22 (reversed, `status/2026-08-22-dispatch-log/REPORT.md:36`)
- **Decision:** Build the packet speculatively before any customer contact — SAM/SBS/USASpending already supply name, UEI, certs, POC, and awards, so the firm reviews a finished packet and fills gaps if they want, rather than being asked for input first.
- **Alternatives considered and rejected:** V2's explicit design was sell-first: "Sell 5 real $750 Snapshots via targeted outreach before building anything past Ingest/Detect... near-zero conversion falsifies the entire funnel." This was reversed within a day — "Sell-first amended: one full sample set before outreach (done — 10 deliverables)" — ten gate-checked deliverables were built and their permalinks verified live before any real outreach happened. Driving reasons, per the swarm-retrospective (council-branch-only, unmerged): repeated cross-session drift on unversioned artifacts made it risky to put an unproven pipeline in front of a real prospect first, and a verified, repeatable sample set was judged the safer precondition for outreach that many concurrent agent sessions could build on without re-litigating quality each time.
- **Status:** active — formalized as doctrine by V5/V6 ("customer input is not required to start").
- **Source:** `archive/plans/plan-history/PLAN-V2.md:58,108`; `status/2026-08-22-dispatch-log/REPORT.md:36`; `archive/plans/PLAN-V5.md:57`; `sop/PLAN-V6.md:58`; `research/swarm-retrospective/REPORT.md` (council-branch-only, unmerged, commit `0f6d695`).

### D-006: Instantly/Smartlead rejected
- **Date:** 2026-08-22
- **Decision:** No email-sequencing tool at launch. Manual send through Google Workspace, every send approved by Mike.
- **Alternatives considered and rejected:** Instantly/Smartlead-class sequencing tools — rejected because at 10–20 personalized emails/week against a ~50-customer ceiling, "an Instantly-class tool is solving a problem this business is structurally forbidden from having." Upgrade path if volume sustainably exceeds ~40–50/wk is GMass, not Instantly/Smartlead, and even then sending stays manual-approval rather than automated.
- **Status:** active.
- **Source:** `research/stack-selection/REPORT.md:27,31`; `status/2026-08-22-dispatch-log/REPORT.md:15`.

### D-007: Vector DB deferred
- **Date:** 2026-08-22
- **Decision:** SQLite FTS5 handles search/matching for now. No vector database.
- **Alternatives considered and rejected:** "The honest answer is 'not yet'" — deferred rather than rejected outright. Trigger for revisiting: corpus reaches tens of thousands of notices AND FTS5 demonstrably misses matches. Pick when triggered: sqlite-vec (loadable extension, local MLX embeddings, zero new services) over LanceDB, unless vectors reach the millions.
- **Status:** active (deferred).
- **Source:** `research/stack-selection/REPORT.md:56,64`.

### D-008: Paid ads deferred, with CPL math
- **Date:** 2026-08-22
- **Decision:** No paid acquisition at current ticket sizes.
- **Alternatives considered and rejected:** Typical B2B cost-per-lead is $80–200; a $100+ CPL against a $450–699 deliverable requires roughly 1-in-4 lead→sale conversion just to break even on the first purchase, which nothing in the repo supports. "Nobody serving this buyer wins on paid ads — the market is too small and the tickets too specific." Revisit only if repeat purchase is proven, or if a future Core subscription ($3–6K/yr LTV) becomes the advertised product, which would support the higher CPL.
- **Status:** active (deferred).
- **Source:** `research/growth-plan/REPORT.md:22,67,71`; `archive/plans/PLAN-V4.md:42`; `specs/content-pipeline.md:186`.

### D-009: LinkedIn automation banned
- **Date:** 2026-08-22
- **Decision:** LinkedIn is manual-only, Mike-owned voice and send. Agents produce data and drafts; they never post or scrape.
- **Alternatives considered and rejected:** Any automated posting or scraping tool — banned outright because LinkedIn's Terms of Service bar scraping and automated activity; this is a hard compliance line, not a cost/quality tradeoff. Key-personnel/org-chart scraping via LinkedIn was separately ruled out in `report-enhancements/REPORT.md` for the same reason.
- **Status:** active.
- **Source:** `archive/plans/PLAN-V3.md:42`; `archive/plans/PLAN-V4.md:33`; `research/report-enhancements/REPORT.md:68`.

### D-010: Protest memo deferred
- **Date:** 2026-08-22
- **Decision:** No protest-memo product line yet.
- **Alternatives considered and rejected:** Was the fourth ladder rung in V3 ($1,500+, after Sources Sought response and Market Snapshot). Deferred until an attorney channel exists — this is advice-adjacent work the factory shouldn't ship without a licensed reviewer in the loop, a risk independently flagged by the outside feasibility red-team (F8, advice-adjacent liability with no legal wrapper).
- **Status:** active (deferred).
- **Source:** `archive/plans/PLAN-V3.md:17`; `research/feasibility-review/REPORT.md` (F8).

### D-011: VetBiz price-band competition avoided
- **Date:** 2026-08-22 (kill-test) → 2026-08-23 (feasibility-final)
- **Decision:** Do not price-compete against VetBiz Network's $49–149/mo feed. Treat VetBiz as a potential distribution partner (Door 6), not a peer competitor.
- **Alternatives considered and rejected:** Undercutting or matching VetBiz's price band — rejected because VetBiz is "not a mapped packet, a matched feed + cert shop," a different product shape entirely; its real threat is distribution (it already sits on newly certified firms), not drafting quality. "Do not spend another hour treating them as Awarded AI." Feasibility-final independently confirmed: "Cert assist is the real revenue... Channel, not peer."
- **Status:** active.
- **Source:** `research/kill-test/REPORT.md:23,58`; `research/feasibility-final/REPORT.md:117`.

### D-012: Firm-count market sizing rejected for a notice-moment denominator
- **Date:** 2026-08-22 (flagged) → 2026-08-23 (rebuilt)
- **Decision:** Size the market by viable Sources Sought notices/year (~250–400 after content-disqualifier haircut), not by firm counts.
- **Alternatives considered and rejected:** The repo carried three inconsistent, underived firm-count figures (~1,500 / 4,000–8,000 / 27–38K) simultaneously. All rejected as the wrong denominator: "the product is notice-tied — an order exists only when a viable notice is open, in a target NAICS, a certified firm plausibly matches it, and the notice isn't disqualified on content." Firms are necessary but not sufficient; the binding constraint is notice supply. This became the load-bearing number for every downstream capacity/kill-gate calculation through V6.
- **Status:** active. Filed as PROPOSAL-0001, accepted, commits `98fd07a`, `d52b4a6`.
- **Source:** `research/feasibility-review/REPORT.md` (F1); `research/feasibility-final/REPORT.md` §1; `proposals/PROPOSAL-0001.md:13,41-43`.

### D-013: Local extraction routes through raw omlx + `thinking_budget`, not Hermes
- **Date:** 2026-08-23
- **Decision:** The factory's `synthesize` stage extracts requirements with local qwen3.8 called directly via omlx, using the `thinking_budget` per-request parameter (plus the server flag `thinking_budget_enabled`) to force a stop token before the model exhausts its budget. Frontier `claude -p` stays for drafting/judgment stages.
- **Alternatives considered and rejected:** `response_format` JSON-schema-constrained decoding — found to be a no-op (xgrammar not installed; server silently falls back to prompt injection). `tool_choice` forcing — found to hang the server outright. Routing extraction through Hermes' multi-turn agentic loop instead — this *worked* (3/3 correct in testing) but was rejected for production: ~2–3 min cold-start overhead per call, one call that hung 14+ minutes, and no `thinking_budget` passthrough exists for the omlx provider through Hermes (a missing `"omlx"` alias in `plugins/model-providers/custom/__init__.py`, not fixed as of this writing).
- **Status:** active. Scoped narrowly to structured extraction — not a blanket "local models are fine now."
- **Source:** `research/local-model-eval/{LIVE-TEST.md §3b,6,7; CONFIG-VALIDATION.md}`.

### D-014: Local extraction near-abandoned, then rescued by a thinking_budget fix
- **Date:** 2026-08-22 (near-abandonment) → 2026-08-23 (rescue)
- **Decision:** Keep local models in the production pipeline for structured extraction, after a targeted fix produced a clean, reproducible pass.
- **Alternatives considered and rejected:** Dropping local extraction entirely and going frontier-only — this was the live trajectory as of 2026-08-22: `local-model-eval/REPORT.md` found qwen3.8 failed 5 of 6 pipeline stages, every failure showing `reasoning_content: null` because the model ran out of budget before hitting a stop token, and PLAN-V4 §5's claim that local extraction was "validated" was flagged false by feasibility-final (finding N1). Rescued 2026-08-23: with Mike's explicit go-ahead, `thinking_budget_enabled` was flipped on and the exact failing prompt re-run with `thinking_budget: 600` — first clean pass in the eval's history, valid JSON, `finish_reason: "stop"`.
- **Status:** active (rescued). See D-013 for the resulting production configuration.
- **Source:** `research/local-model-eval/REPORT.md` (failure); `research/local-model-eval/THINKING-BUDGET-ENABLED-TEST.md` (rescue); `research/feasibility-final/REPORT.md` (N1).

### D-015: council-branch-never-merges rule
- **Date:** 2026-08-23
- **Decision:** `research/council/` on `main` records analysis and proposals only. Anything drafted on `council/2026-08-23-research` (including PLAN-V7 and PROPOSAL-0013..0017) stays there until Mike explicitly directs otherwise.
- **Alternatives considered and rejected:** Merging council-branch output automatically once a plan draft looked complete — rejected because that branch reused TASK-0018/0019 for different jobs than `main`, so a merge would corrupt task/proposal numbering (confirmed by PROPOSAL-0013..0017 being deliberately numbered above 0012 specifically to avoid a collision on eventual merge). GitHub issue #8 makes the rule enforceable: "Do not merge council/2026-08-23-research or accept PLAN-V7."
- **Status:** active, standing rule.
- **Source:** `status/SWARM-2026-08-23.md:9-13`; GitHub issue #8; `research/plan-evolution/REPORT.md` (council-branch-only, unmerged, commit `0f6d695`).

### D-016: credentials-never-in-repo rule
- **Date:** 2026-08-22 (repo inception), restated through V6
- **Decision:** Credentials never enter git. Local `credentials/` directory or a password manager only.
- **Alternatives considered and rejected:** No exception carved out anywhere — stated identically and without qualification in three separate current-plan documents, which is itself the point: no agent generation gets to relax it by omission.
- **Status:** active, standing rule.
- **Source:** `AGENTS.md:56`; `sop/DATA.md:5`; `sop/PLAN-V6.md:142`.

### D-017: nothing self-hosted customer-facing
- **Date:** 2026-08-22
- **Decision:** No self-hosted service sits in any customer-facing path. Cloud/managed services only where a customer could hit them.
- **Alternatives considered and rejected:** Self-hosted alternatives were evaluated and passed over for every customer-facing function during stack selection — Listmonk (newsletter) over Buttondown, self-hosted DocuSeal over cloud DocuSeal, Postgres/Supabase over SQLite-in-repo for the notice DB — each rejected specifically because the Mac running local infrastructure must never be the thing a customer's browser or inbox touches directly. Local/self-hosted stays for internal tooling (local models, SQLite, git) only.
- **Status:** active, standing constraint on every stack decision.
- **Source:** `research/stack-selection/REPORT.md` §1-§9 (see esp. §2, §7).

### D-018: PLAN-V7 drafted, deliberately not accepted
- **Date:** 2026-08-23
- **Decision:** V6 remains the only accepted operating plan. A V7 draft exists (`research/council/2026-08-23-PLAN-V7-DRAFT-strategist.md`, council branch) but was never brought to Mike for acceptance.
- **Alternatives considered and rejected:** Accepting V7 on the strength of its own drafting process — rejected on process grounds, not content: the council-branch-never-merges rule (D-015) blocks it structurally, and the swarm-retrospective (council-branch-only) flags the V7 drafting spree itself as a symptom — "the very next thing this branch produced was eight commits of PLAN-V7 drafting" — of plan-writing displacing customer contact as the swarm's default activity.
- **Status:** active hold. Unblocks only on Mike's explicit direction.
- **Source:** GitHub issue #8; `research/plan-evolution/REPORT.md` §1 "W1" (council-branch-only, unmerged, commit `0f6d695`).

### D-019: Default per-notice exclusivity, pending a real conflict-of-interest policy
- **Date:** 2026-08-22 (flagged) → 2026-08-23 (temporary default set)
- **Decision:** Until Mike decides the standing conflict-of-interest policy, the factory defaults to exclusive — one packet per (notice, firm), no selling the same notice to multiple competing firms.
- **Alternatives considered and rejected:** PROPOSAL-0002 offered three options — exclusive-per-notice, capped-with-disclosure (N=2), or a Snapshot-only carve-out — and recommended the capped option contingent on terms language that didn't exist yet (PROPOSAL-0010, also needs-human-decision). The council synthesis overrode with the safer default (exclusive) rather than wait on two unresolved human decisions before shipping V6's gates. This is a temporary default, not a resolved policy — TASK-0013 (issue #4) is still open.
- **Status:** active (temporary default) — not yet superseded by Mike's actual COI decision.
- **Source:** `proposals/PROPOSAL-0002.md:7,51-53`; `research/council/2026-08-23-SYNTHESIS.md:19`; `sop/PLAN-V6.md:62`; GitHub issue #4.

### D-020: CI added; claim-discipline audit runs report-only, not blocking
- **Date:** 2026-08-24
- **Decision:** `.github/workflows/ci.yml` is now the required check on every PR (and on push to `main` as a stopgap — see D-021). It runs the gate registry self-tests, a samples spot-check, verifier/poison-harness discovery, the board/issues consistency check, a full-tree secret scan, and the new DECISIONS.md-entry check (D-022). The claim-discipline audit (`scripts/check-branch-claim.sh`) also runs, but with `continue-on-error` — report-only, not a merge blocker.
- **Alternatives considered and rejected:** Making claim-discipline a hard gate immediately — rejected because the audit found 3 real pre-existing violations in the current branch set (work/gold-set-TASK-0018, work/matcher-gold-TASK-0018 → #19; work/newsletter-issue13 → #13) that predate this CI and are unrelated to any given future PR's diff. A hard gate would block every PR on an unrelated backlog until someone independently cleans it up — disproportionate. It becomes a hard gate once that backlog is cleared (tracked in the follow-up issue this PR files).
- **Status:** active.
- **Source:** this PR; `.github/workflows/ci.yml`; issue tracking the claim-discipline backlog.

### D-021: Branch protection not enabled — blocked on GitHub plan, not skipped by choice
- **Date:** 2026-08-24
- **Decision:** `main` has no server-side branch protection or ruleset. Direct pushes to `main` are closed by *convention* (documented in AGENTS.md "PR discipline") — CI runs on push-to-main too as a partial stopgap — but nothing on GitHub's side actually refuses a force-push or a direct commit today.
- **Alternatives considered and rejected:** Implementing protection as specified — not possible: `gh api repos/redtrades/govcon-factory/branches/main/protection` and the rulesets equivalent both return 403 "Upgrade to GitHub Pro or make this repository public" (confirmed live against the account, not assumed). Making the repo public to unlock the free-tier feature — rejected, the repo holds financial models and business strategy that shouldn't be public. Mike chose (2026-08-24, asked directly): skip enforcement for now, document the gap, and file a tracking issue rather than pausing this PR on a plan-upgrade decision.
- **Status:** active gap, tracked. Resolves when Mike upgrades to GitHub Pro (or Team/Enterprise) and someone wires up the actual protection rules — see the tracking issue this PR files.
- **Source:** this PR; live `gh api` 403 responses against `redtrades/govcon-factory`.

### D-022: DECISIONS.md-entry check added (mechanical half of issue #29)
- **Date:** 2026-08-24
- **Decision:** `scripts/check-decisions-entry.sh`, run in CI on every PR, fails a PR that touches a "governing path" (`AGENTS.md`, `CLAUDE.md`, `business/sop/**`, `pipeline/specs/**`, `pipeline/domains/*/README.md`, `pipeline/factory/gates/registry.py`) without also touching `DECISIONS.md`.
- **Alternatives considered and rejected:** A broader trigger (any `.md` change, or any change at all) — rejected as both noisy (would fire on typo fixes throughout the repo) and impossible to make precise, since "significant decision" is a judgment call CI can't make; the governing-path list is the enforceable proxy, not a claim that it's complete. The check's own failure message says as much and allows a human override via PR description when a governing-path touch genuinely isn't a decision.
- **Status:** active. Closes the mechanical half of issue #29; the "is this actually significant" judgment stays human.
- **Source:** issue #29; `scripts/check-decisions-entry.sh`.

### D-023: Resource leases coordinate on a dedicated `leases` branch, not issue labels
- **Date:** 2026-08-24
- **Decision:** Exclusive-resource coordination (`gpu-heavy`, `omlx-restart`) uses `scripts/lease-acquire.sh`/`lease-release.sh`/`lease-status.sh` against a dedicated `leases` git branch. Acquiring writes a JSON file and pushes straight to that branch; a rejected non-fast-forward push is the actual exclusivity check.
- **Alternatives considered and rejected:** An issue-label convention (a `lease:<resource>` label + self-assignment on a standing issue) — rejected for the same reason issue #34 already flagged for claim discipline generally: every agent shares one `gh` login, so assignee identity can't distinguish holders, and `gh issue edit` has no compare-and-swap. A git branch push does have real atomicity (the remote rejects a non-fast-forward push), which is why leases live there instead of copying the pattern that's already known-broken for exclusivity. Putting lease state on `main` — rejected to keep lease churn (frequent, low-ceremony) out of the PR-reviewed history of the actual product.
- **Status:** active.
- **Source:** issue #34; this PR; AGENTS.md "Resource leases".

### D-024: SSSF is the local enforcement/review layer, not a parallel enforcement system
- **Date:** 2026-08-24
- **Decision:** `~/agent-workspace/adws/adw_govcon_pipeline.py` (Mike's already-installed SSSF, not a new tool) is extended to drive this repo's full 9-stage factory pipeline (previously only 6 of 9, a hand-maintained stage table that had drifted) as SSSF `kind="code"` phases, plus an opt-in `packet_reviewer` agent phase using SSSF's real `verdict_consistent` gate. GitHub CI + branch protection (when available) remains the remote gate for every PR regardless of origin. See AGENTS.md "Local vs remote enforcement".
- **Alternatives considered and rejected:** Building new local enforcement (a bespoke phase-blocking runner, a bespoke review-loop script) — rejected outright on Mike's direct correction: "this is why I keep telling you to use SSSF... The enforcement and review loops are all not there," meaning use the installed tool, don't reinvent it next to itself. `coding_agent: claude_code` as the review agent — not available, confirmed by reading `adw_modules/agent_cc.py` directly (raises `NotImplementedError` unconditionally in this v1 install); `coding_agent: pi` against local omlx is the only working agent-execution path, which is what the new `packet_reviewer` agent uses. A bounded auto-revise loop on reviewer rejection (mirroring `adw_build_review.py`'s builder↔reviewer loop) — rejected for this specific case: revising a rendered deliverable means re-running `synthesize` (a real-cost pipeline stage), not a cheap diff patch, and AGENTS.md rule 1 ("nothing leaves without Mike's approval") means a human decides what happens next on rejection, not another automated attempt.
- **Status:** active. Validated structurally (config loads, all 9 stage `module.fn`s resolve in YAML order, `packet_reviewer` agent validates) and with two live smoke tests against real `sssf.db` (a green 2-phase run, and a fail-closed run proving a raised exception halts the session and the next phase is never even recorded). A full live 9-stage run (needs omlx served + `claude` CLI + live network + real cost) was not executed in this pass — flagged for Mike, not run unilaterally.
- **Source:** `~/agent-workspace/adws/adw_govcon_pipeline.py` commit `cb88b38`; `pipeline/specs/factory-architecture.md` §8; `scripts/ci/check-sssf-wiring.sh`.

### D-025: Self-hosted GitHub Actions runner registered on this Mac
- **Date:** 2026-08-24
- **Decision:** A self-hosted runner (`m64-govcon-factory`) is registered against `redtrades/govcon-factory` and running as a `launchd` LaunchAgent. `ci.yml`, `ci-optional.yml`, and `worktree-hygiene.yml` target it.
- **Alternatives considered and rejected:** Staying on `ubuntu-latest` — rejected on two counts: metered GitHub-hosted minutes (a 237MB SAM.gov pull and real `claude -p` calls in `synthesize` add up), and, more importantly, no reach — a GitHub-hosted runner cannot see `~/agent-workspace` (SSSF) or local omlx, so `scripts/ci/check-sssf-wiring.sh` (this PR) would have been structurally impossible to run in required CI. A hand-rolled launchd plist — rejected in favor of the runner's own `./svc.sh install`, which handles start/stop semantics (including graceful shutdown mid-job) that a hand-rolled plist would have to reinvent — "use established tools over custom scripts."
- **Status:** active. Security posture: acceptable only because this repo is private with known collaborators (self-hosted runners execute arbitrary PR-branch code with this machine's own permissions) — every workflow targeting it also guards against fork PRs as defense in depth, and this runner must never be attached to a public repo (see AGENTS.md "Self-hosted runner").
- **Source:** `gh api repos/redtrades/govcon-factory/actions/runners` (`status: online`); `~/actions-runners/govcon-factory/`; `~/Library/LaunchAgents/actions.runner.redtrades-govcon-factory.m64-govcon-factory.plist`.

### D-026: Worktree/branch hygiene made a standing protocol, with a check + a prune script
- **Date:** 2026-08-24
- **Decision:** After a PR merges, the branch and its worktree get removed — not left to accumulate. `scripts/check-worktree-hygiene.sh` audits for merged-undelted/orphaned/dirty-stale worktrees across the whole machine; `scripts/prune-merged-branches.sh --apply` removes what's unambiguously safe (clean + genuinely merged, never `main`/`master` itself, never anything dirty). Scheduled every 6h via `worktree-hygiene.yml`.
- **Alternatives considered and rejected:** Flagging any branch that's an ancestor of `origin/main` — rejected without a same-SHA guard: a just-created, not-yet-started branch (`git worktree add ... -b work/x`) is trivially "an ancestor" of main before its first commit, which would make an auto-prune workflow delete brand-new work before an agent even committed to it. Caught live during this pass (the check initially flagged this session's own in-progress worktree) and fixed by requiring the branch SHA to actually differ from `origin/main`'s.
- **Status:** active. Also demonstrated live: pruned one genuinely stale redundant worktree (`~/agent-reports/govcon-factory-hygiene-2026-08-23/main-hygiene`, clean, tracking `main`) during this pass.
- **Source:** `scripts/check-worktree-hygiene.sh`; `scripts/prune-merged-branches.sh`; AGENTS.md "Worktree/branch hygiene".

### D-027: Branch protection re-confirmed blocked across every endpoint; local layer added as the stopgap
- **Date:** 2026-08-24
- **Decision:** Re-verified D-021's finding exhaustively rather than trust the earlier single check: `gh api` 403s identically on classic protection (GET), rulesets (GET), rulesets (POST, even a disabled test ruleset), and required-status-checks-alone. All four confirm the same "Upgrade to GitHub Pro or make this repository public" gate. `scripts/hooks/pre-push` (blocks local direct pushes to `refs/heads/main`) and `scripts/check-direct-main-pushes.sh` (audits `origin/main`'s first-parent chain since PR #48 for single-parent, i.e. non-PR-merge, commits) are added as the local enforcement layer in the meantime.
- **Alternatives considered and rejected:** Assuming no partial protection exists without testing — explicitly rejected per direct instruction ("use whatever rulesets/protection the free plan actually allows... test via API, don't assume"); tested comprehensively instead of re-asserting the prior finding. GitHub Pro upgrade (~$4/mo) would resolve this properly (turns three local-layer scripts into one server-side setting that can't be bypassed by a missing hook) — flagged for Mike, not purchased.
- **Status:** active gap, tracked (issue #43), with the local layer as a real-but-bypassable stopgap — not equivalent to server-side enforcement.
- **Source:** live `gh api` 403 responses (four endpoints, 2026-08-24); `scripts/hooks/pre-push`; `scripts/check-direct-main-pushes.sh`.

### D-028: A GitHub App, not a machine user, is the reviewer-bot identity
- **Date:** 2026-08-24
- **Decision:** `govcon-reviewer-bot`, a GitHub App owned by `redtrades`, is the identity agents review PRs as. `scripts/reviewer-bot-review.sh` mints a short-lived installation token (App private key -> JWT -> installation access token, no `gh` CLI involved) and calls `POST /repos/.../pulls/{pr}/reviews` directly. This fixes issue #52: GitHub refuses APPROVE/REQUEST_CHANGES when the reviewer and PR-author identity match (every agent authenticates as `redtrades` today), but the App's bot identity is a distinct account from `redtrades` as far as that check is concerned.
- **Alternatives considered and rejected:** A second machine-user account (issue #52 option 1) — works too, but costs a paid seat on GitHub Team/Enterprise pricing the moment the org has any private-repo billing tier beyond Free-for-one-account, and needs its own password/2FA/PAT lifecycle managed by hand. A GitHub App has none of that: free regardless of plan, no separate login, auth is a private key Mike controls, and permissions are scoped narrowly (pull requests read/write, contents read, checks read, issues read/write — no admin, no webhooks) rather than inheriting whatever a human account can do. `COMMENT`-only reviews as the permanent posture (option 3) — rejected per the issue's own reasoning: a verdict that lives only in comment prose is not a field anything can gate on, and combined with D-027's branch-protection gap leaves no enforcement mechanism at all.
- **Status:** active, live end-to-end. Registered via the manifest flow (one manual browser confirmation by Mike — GitHub's manifest flow has no pure-API path for the initial App creation step); installed by Mike with `repository_selection: all` (installation id `156252855`) — reaches every `redtrades` repo, not just this one, which matters for private-key exposure; narrowing to just `govcon-factory` is flagged as worth doing later (AGENTS.md "Reviewer bot"), not done unilaterally. Credentials stored at `~/agent-reports/credentials/govcon-reviewer-bot/` (outside the repo, chmod 600, matches this repo's secret-scan and `.gitignore` `credentials*` pattern). Live-tested against PR #57 (throwaway, closed unmerged): both `REQUEST_CHANGES` (pullrequestreview-5010508788, the exact verdict type that 422'd under `redtrades`) and `APPROVE` (pullrequestreview-5010509557) filed successfully as `govcon-reviewer-bot[bot]`.
- **Source:** issue #52; `scripts/reviewer-bot-review.sh`; `~/agent-reports/credentials/govcon-reviewer-bot/README.md`; AGENTS.md "Reviewer bot"; PR #56; PR #57 (closed, test evidence).

### D-029: Universal agent rules/skills/hooks/prompts/roles live in a dedicated `agent-configs` repo, referenced as a submodule
- **Date:** 2026-08-24
- **Decision:** Cross-project agent config (rules, Claude Code skills, hook scripts, prompt/command templates, role definitions) has one canonical home — `redtrades/agent-configs` (private) — referenced from this repo as a git submodule at `agent-configs/`. Nothing universal is duplicated inline in this repo's `AGENTS.md`/`CLAUDE.md`; they carry a one-line pointer instead.
- **Alternatives considered and rejected:** A symlink to `~/agent-configs` — rejected because it breaks on a fresh `git clone` anywhere else (the absolute path wouldn't exist on a new machine or a fresh checkout); a submodule resolves correctly via `git clone --recurse-submodules` regardless of machine. Leaving universal content duplicated per-repo (the initial state, 2026-08-24 morning) — rejected the same day it was created: a 53-repo disler/IndyDevDan pattern-survey's adoptions landed scattered across this repo (`PROPOSAL-0024`, closed PR #63) and `agent-workspace`, which is exactly the drift a single rule surface is meant to prevent. Both superseded PRs closed rather than merged (#63, #65).
- **Status:** active. `~/.claude/`-level installs (hooks/skills that must physically live under `~/.claude/` to load) stay copied, not submoduled, each copy carrying a `SOURCE.md` naming `agent-configs` as canonical.
- **Source:** `agent-configs/README.md`, `agent-configs/MASTER-GUIDE.md` §1/§7; issue #66; closed PR #63 (`redtrades/govcon-factory`), closed PR #65 (`redtrades/govcon-factory`).

### D-030: List-3 promotion is fail-closed; candidate pool is size-capped
- **Date:** 2026-08-24
- **Decision:** Geography is never sufficient for list 3. The dead awarding-sub-agency substring branch is removed. The USASpending pull sorts by Start Date (not Award Amount) and drops awards above `award_amount_max_usd` ($25M default). `uei` is stored only when the value matches a 12-char UEI; USASpending `recipient_id` hashes stay in `recipient_id`. An empty list 3 is a valid, fail-closed outcome. Commercial send remains blocked until a gold-set re-score clears 80% (issue #19).
- **Alternatives considered and rejected:** Tuning `_overlap_reason` with notice-body keyword overlap — measured at 18.2% in-sample and halved recall of true matches (PR #32 / PROPOSAL-0019). Restoring state-OR-agency promotion — 45/45 gold-set promotions were state-only; that is the 20% result. Sorting by dollars with no ceiling — 541330 pool's smallest row was $130M and contained zero of 28 named A/E firms. Joining DSBS/VetCert before ranking (PROPOSAL-0019 3(c)) — right structurally, blocked on issue #5.
- **Status:** active. Does not claim the 80% gate is met.
- **Source:** PR #32 measurement; `pipeline/factory/stages/match_rules.py`; `pipeline/factory/verify_match.py`.

### D-031: Match candidate pool is the DSBS certified-UEI snapshot
- **Date:** 2026-08-24
- **Decision:** After issue #5 landed, implement PROPOSAL-0019 3(c). List 2/3 emit only award recipients whose UEI is in the latest `operations/data/sbs/*/universe.json`. Missing UEI or a prime not in the snapshot is dropped, not emailed. No snapshot file is a hard fail.
- **Alternatives considered and rejected:** Name-only join — SBS and USASpending names mismatch (dba vs legal). Waiting for another gold-set before joining — the 20% failure was the wrong population; shrinking the pond does not lift the send stop (#19) but it stops Lockheed landing on a chemistry notice. Fuzzy name match as a fallback — rejected; no UEI means we cannot prove it is the pond.
- **Status:** active. Still does not claim the 80% gate.
- **Source:** PR #71 snapshot; `in_certified_pool` in `pipeline/factory/stages/match_rules.py`.

### D-032: Merges are delegated under a three-tier merge-authority policy
- **Date:** 2026-08-25
- **Decision:** Tier 0 (docs/evidence/runs) auto-merges once CI is green, no reviewer-bot approval required. Tier 1 (code: scripts, hooks, pipeline/application code, skill implementations) auto-merges once CI is green AND a reviewer-bot review is in. Tier 2 (governing docs: plans, SOPs, gate thresholds, `agent-configs/MASTER-GUIDE.md` itself, `DONT.md`, anything under `rules/`, plus `.github/workflows/` changes by precedent) merges only by Mike, personally — no agent merges this tier regardless of CI/bot status.
- **Alternatives considered and rejected:** The prior flat rule ("Mike merges every PR") — superseded on Mike's explicit ruling 2026-08-25 ("delegate merges"), given when the reserved-merge rule was surfaced to him with the trade-off explained; keeping the flat rule would have left every recovery PR from the #141 force-reset blocked on one human. Delegating Tier 2 as well — rejected; governing docs define what every other tier is allowed to do, so their merge stays with the human.
- **Status:** active. Provenance: `agent-configs/MASTER-GUIDE.md` §2 point 4 and §8 (which cite this ruling); the 2026-08-24 blocked-delegation classifier signal recorded there is retained as history, resolved by this ruling. Note: the GUIDE references this record as "D-001"; it is numbered D-032 here after the file was restored from the rescue branch post-#141 (see issue #141).
- **Source:** Mike's ruling 2026-08-25; `agent-configs/MASTER-GUIDE.md`; applied live to PRs #167/#170/#171/#172/#173/#175/#176/#179 merges on 2026-08-26.

### D-033: `tasks/*.md` + `BOARD.md` deleted from the working tree; GitHub Issues + Project board is the single queue
- **Date:** 2026-08-26
- **Decision:** Per Mike's direct instruction (issue #243), `tasks/*.md` and `BOARD.md` are deleted outright, not just deprecated in place. Every task file's work is represented in GitHub Issues (verified by reconciliation — every `TASK-00NN` id appears in at least one issue's title or body; issues #244/#245/#246 were filed retroactively, closed on creation, for the three tasks — TASK-0016/0026/0027 — completed before the D-004 migration existed and never previously logged). A GitHub Project (v2) board over the repo's issues adds the visual/status layer the plain issue list lacked.
- **Alternatives considered and rejected:** Repointing `AGENTS.md` while keeping the files as historical record — this was #222/PR #231's approach (see its D-034, filed independently and not yet merged as of this decision), reasoned as "git blame on why a task was framed a certain way is still worth having, and deletion is not reversible on someone else's evidence." Mike's ruling here supersedes that reasoning: git history retains the files (`git log -- tasks/`), so nothing is lost by removing them from the working tree, and two live artifacts claiming to be the queue was itself the problem being fixed (ambiguity read as "not using proper SDLC"). Reconciling every task against an issue first (rather than deleting and hoping) is what makes this safe.
- **Status:** active. **Numbering note:** PR #231 (unmerged at the time of this entry) independently claimed "D-034" for its own decision on the same topic — whichever of the two PRs merges second must renumber to avoid a collision; flagged in both PRs and in a comment on #222.
- **Source:** issue #243; reconciliation list in PR body; commits deleting `tasks/*.md`, `BOARD.md`, `scripts/generate-board.sh`, `scripts/refresh-issues-snapshot.sh`, `scripts/hooks/checks/01-board-must-be-regenerated.sh`, `scripts/ci/check-board-fresh.sh`, `scripts/migrate_tasks_to_issues.py`.
