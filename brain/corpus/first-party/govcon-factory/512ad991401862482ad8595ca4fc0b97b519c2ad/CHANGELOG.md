# CHANGELOG

Reverse-chronological. Grouped by day. Each entry cites the commit, PR, or
issue it came from — `git show <hash>` or `gh pr view <N> -R redtrades/govcon-factory`
gets you the full record. Decisions with lasting rationale (not just "what
shipped") are in [DECISIONS.md](DECISIONS.md) — this file is "what happened
and when," that one is "why, and what we said no to."

Plan-version arc (detail in DECISIONS.md and archive/plans/):

| Version | Date | One line |
|---|---|---|
| V2 | 2026-08-21 (pre-repo) | Found the pricing crux: sell coverage/time, not an unsupported win-rate claim. Kept a $5,000/yr Core + promoted $750 Snapshot. |
| V3 | 2026-08-22 | Dropped the subscription; became a per-decision deliverables factory. Ladder: $450 Sources Sought response → $750 Snapshot → $1,500+ red-team. |
| V4 | 2026-08-22 | Scaling document (governance, growth funnel, delegated review) layered on V3's unchanged product — written before a single email went out. |
| V5 | 2026-08-23 | Mike corrected a drifted packaging of his own idea. Retired the $450/$750 ladder. Single $699 opportunity packet + free industry-report magnet. Factory-first (build before contact) made explicit doctrine. |
| V6 | 2026-08-23 | Same product as V5. Council review (4 seats + synthesis) added hard gates: matcher gold-set ≥80% precision, ≥50% quality floor before pitching, default per-notice exclusivity, statistically real kill-gate volume, legal + benefits consults before first invoice. |
| V7 (draft) | 2026-08-23 | Drafted on `council/2026-08-23-research`. **Not accepted, not merged** — GitHub issue #8 explicitly blocks it. |

---

## 2026-08-24

### Evening — DSBS join on match (PROPOSAL-0019 3(c), D-031)
- List 2/3 now require a UEI present in the latest `operations/data/sbs/*/universe.json`.
- Missing UEI or a non-certified prime is dropped. Does not lift issue #19.

### Evening — DSBS/VetCert universe snapshot (issue #5)
- `pipeline/factory/ingest_sbs.py` pulls certified SDVOSB firms from SBA SBS `POST /_api/v2/search` using the captured zustand payload (not a `{filters: ...}` wrapper), dedupes on UEI, writes `operations/data/sbs/<date>/{universe,MANIFEST}.json`.
- Live run 2026-08-24T21:10:50Z: **14,979 unique UEIs** across the five target codes (236220: 4548, 541519: 6703, 541330: 4902, 541512: 6664, 561210: 4601). Canary on 236220 returned 4548 (2026-08-22 research count was 4551).
- Committed `universe.json` has contacts stripped. Full dump is gitignored until TASK-0019.

### Matcher fail-closed rewrite (PROPOSAL-0019 1 / 2 / 3(b))
- List 3 no longer promotes on PoP state or agency substring.
- Candidate pull sorts by Start Date and caps award size at $25M (`sources.yaml`).
- `uei` is a real UEI or null. `pipeline/factory/verify_match.py` pins the rules (9 checks, no network).
- Door 1 noindex landing scaffold copied from PR #35 (does not claim list-3 matches).
- Does **not** close issue #19. Gold-set PRs #32/#35 still need rebase onto current main.

## 2026-08-23

### Evening — factory proven end-to-end, PR #28 merged (20:37 UTC)
- `2b2980b` Implemented `synthesize` (requirements extraction) and `package` (deliverable assembly) stages per their documented contracts; `compliance`/`format` gates went from stubs to real checks.
- `a22e939` Full fresh pipeline run, all 9 stages OK, `gate_final/GATE-REPORT.json` **42/42 checks, all_green** — TASK-0022 (#20) acceptance test. Reproduced independently from a second clean worktree to rule out cached state.
- `b9e5ae2` Issues snapshot refreshed: TASK-0022 (#20), TASK-0023 (#21), TASK-0024 (#22) closed.
- `b6918f0` Board tasks for factory synthesize/package/second-source; AGENTS.md pointer added.
- Merged as `c1094b8` (PR #28, "factory: wire synthesize + package end-to-end, gate-green acceptance test") — current `main` HEAD.
- See [D-013, D-014](DECISIONS.md) for the local-model routing decision this stage depends on.

### Afternoon — brand context files, PR #27 merged (19:00 UTC)
- `411412d` Added `brand/{company,customer,offer,voice}.md` — load-as-context files for content generation, grounded in PLAN-V6 ("if anything here disagrees with V6, V6 wins"). Rescued from an uncommitted `brand/` directory that had been sitting in the working tree while checked out on the disputed council branch.
- Merged as `5c85e35` (PR #27).

### Afternoon — repo hygiene, PR #26 merged (18:52 UTC)
- `970abf4` Archived superseded plans (V3/V4/V5), old financial-model versions (v1/v2), and folded-in research (`opportunity-scan/`, `outreach-playbook/`) into `archive/` via `git mv` — history preserved, nothing deleted.
- `9055d57` Fixed 4 live references pointing at archived paths.
- `547ce90` AGENTS.md repo map added.
- `e917852` Issues snapshot refreshed (no state/label changes).
- Deliberately did **not** archive `research/feasibility-review/`, `feasibility-final/`, `council/`, or `govcon-prior-art/` — still cited by live docs.
- Could not quarantine the V3-era `skills/` layer per PROPOSAL-0015 — that proposal exists only on the disputed `council/2026-08-23-research` branch (see [D-015](DECISIONS.md)).
- Merged as `388429d` (PR #26).

### Afternoon — factory core + GitHub Issues work queue + SSSF, PR #25 merged (18:11 UTC)
- `c9d296f`/`7ec8aca` Factory core: typed JSON envelope contract, fail-closed gate registry, SQLite-traced runner (`specs/factory-architecture.md`). Deterministic `ingest → normalize → triage → match → assemble → gate` proven live against a same-day SAM.gov pull.
- `68f2af2` First live proof run (deterministic half only).
- `cad2836` Migrated 15 open `tasks/*.md` to GitHub Issues (dedup'd against 8 Mike had filed by hand).
- `d63f1b2` `BOARD.md` now generated from `status/issues-snapshot.json`, not `tasks/*.md`; claim/complete scripts require `--evidence`.
- `4f45fbb` Factory failures now auto-file GitHub issues (labeled `factory-failure`) instead of only printing to console.
- `f5241b0` Ran the pipeline as an SSSF ADW (`~/agent-workspace/adws/adw_govcon_pipeline.py`) — 7/7 deterministic phases green, 28 domain-gate checks mirrored into `sssf.db`.
- `6fae993` AGENTS.md documents the GitHub Issues work queue as canonical.
- Merged as `f8f4c5c` (PR #25). See [D-003, D-004](DECISIONS.md).

### Early afternoon — council review → PLAN-V6 cutover
- Council briefs from 4 seats (strategist, skeptic, gtm, factory — both Grok and fable-5 passes) plus a synthesis: `f46d287`, `4feec00`, `b9d9a2b`, `48a2a37`, `2730b07`, `16a1d81` ("Council SYNTHESIS 2026-08-23").
- `7d5bfc8` PROPOSAL-0012 filed: incorporate council + strategic-advisor amendments (matcher gold-set, stronger kill math, exclusive default, quality floor, legal/benefits gates).
- `8eb9d02`/`534851a`/`3745447` New tasks TASK-0018 (matcher gold-set), TASK-0019 (counsel on DSBS/SAM contact use), TASK-0020 (benefits advisor consult).
- `3451098` **PLAN-V6 supersedes V5** — accepts PROPOSAL-0012.
- `ea5ab9e`/`a9ab732`/`998a3ea` STATUS and AGENTS.md repointed at V6; PROPOSAL-0012 marked accepted.
- `72f87e3` Strategist seat brief (claude-fable-5) filed same day, post-cutover.
- See [D-002, D-018, D-019](DECISIONS.md).

### Morning — industry reports, samples, PLAN-V5 adoption
- `d907531` PLAN-V5 adopted as the operating plan, board retargeted.
- `937de29` → `15f319d` → `8bf6e82` → `a5d5ef9` → `5c46535` TASK-0016: first industry report, NAICS 236220, built and refined against live data; final revision withdrew a point estimate in favor of a reported interval. Merged `42582b3`.
- `630e02f` Independent NAICS 236220 replica (parallel build, not a duplicate close) — merged `4b43d28` "not a second TASK-0016 close."
- `f12bf7f` NAICS 541519 report as an extra magnet — merged `40c9f1c`.
- `63496d9` No-ship Talion packet sample + kill-test recon + STATUS cutover — the internal sample that passed the floor gate but 404'd on the S5 exclusions lookup, opening issue #7 (hold).
- `77a32a3`/`b078f89`/`1ab199c`/`067cee8` TASK-0021: retired live V3 outreach copy quoting $450/$750; SOP corrected.
- `d5df065` Fixed stale PLAN-V5 pointers once V6 became current.
- `1ab199c`/`175eb2d` Track-board merges (TASK-0018/19/20 board-state schema fix).

---

## 2026-08-22

Repo created this day (`78b34b0`, 21:41 local) — "Move canonical SOP + PLAN-V3 into repo; merge ten cheap-win SOP amendments," applying `research/report-enhancements/REPORT.md` §7 directly into `sop/SOP-DELIVERABLES.md`.

- `4facf21` `gate_runner.py` (portable) + `gates/README` documenting coverage gaps.
- `f1e60ad` Outreach email templates and fillable deliverable skeletons.
- `2d10631` Data-source recipes: govconapi, SAM.gov, USASpending, SBS/DSBS, protest/R&Q/forecast.
- `9c5a77d`/`bf78db2` Full 16-skill V3 pipeline map (production stages, lead-gen, feedback loop).
- `d8a8a04` AGENTS.md entrypoint added (model-agnostic); CLAUDE.md thinned to a pointer.
- `ce4ec77` Cross-agent markdown task board created (`tasks/`, `BOARD.md`, claim/release/complete scripts) — later superseded, see [D-004](DECISIONS.md).
- `e11693f`/`e36993f` Self-improvement/feedback loop: `proposals/` + `rubric-improve` extension.
- `bcae822` Sample batch and key research folded into the repo.
- `0dac525` `samples/` provenance sample (236220 MRI notice).
- `cf18d7a` `sop/plan-history/` added — PLAN-V2, source report, claim ledger, fable critique (all dated 2026-08-21, pre-repo).
- `b5d49ef` `status/` — dispatch log + business status handoff.
- `daae678` `sop/financial-model/` — v1 24-month scenario model.
- `a7e1651` Three-tier mirror model documented (GitHub canonical / iCloud mirror / Drive for Mike); iCloud sync script added.
- `e8986ac` Growth-plan research, TASK-0008/9/10, local-model-eval stage-3 results.
- `549f480` **PLAN-V4** (integrated operating plan) + financial-model v3.
- `52dd128` Programmatic content/SEO pipeline skeleton (spec + skills + `site/` scaffold).
- `7605b1f` Remaining local-model-eval stage-3 draft results.
- `07b2506` `feasibility-review/REPORT.md` added — outside red-team pass, verdict **GO-WITH-CHANGES**, 11 findings filed as PROPOSAL-0001..0011.
- `98fd07a`/`d52b4a6`/`37392a6`/`2411e26`/`f126857`/`91ee4d9` PROPOSAL-0001, 0003, 0004, 0005, 0006, 0007, 0008, 0009, 0011 applied (universe/wedge/sending-domain fixes, AI-SaaS objection handling, growth channels, notice-shape triage, SOP dated revision).
- `130d2aa`/`627ecc1` Rubric-improve decisions recorded for PROPOSAL-0001..0011; task board updated.
- `e96020c` omlx config validation pass reconciling local-model tuning research vs. live config (see [D-013](DECISIONS.md)).
- `23fc8be`/`6345710`/`be8c720`/`7a67c70`/`40855bb` Local-model-eval REPORT.md and remaining results; DRIVE-MANIFEST added; NAICS-selection raw data; financial-model v2 workbook completed (dedup sweep from `~/agent-reports`).

---

## 2026-08-21 (pre-repo)

No repository existed yet. This work happened in `~/agent-reports/` and was folded into the repo on 2026-08-22 (`cf18d7a`, now at `archive/plans/plan-history/`).

- **PLAN-V2** written: a five-step crux analysis (gap statement → MECE → crux → options → recommendation) that found the original business plan's $5,000/yr price rested on an unsupported win-rate claim. See [D-001](DECISIONS.md).
- **Claim ledger** consolidated from four independent research passes (competitor pricing, SDVOSB/VA policy, USASpending/SAM.gov ToS, billing/compliance) — VetBiz Network identified as an undiscussed $49–149/mo competitor; SAM.gov data-resale terms checked (CC0, commercial use permitted).
- **Fable critique** — a prior draft's proposal reviewed and treated as source material only, not adopted verbatim.

---

## Notes on sourcing

- Two reports — `research/swarm-retrospective/REPORT.md` and `research/plan-evolution/REPORT.md` — exist **only on branch `council/2026-08-23-research`** (commit `0f6d695`), never merged to `main`. They're cited in DECISIONS.md where load-bearing, flagged as council-branch-only each time.
- `git show council/2026-08-23-research:<path>` retrieves anything cited from that branch without checking it out.
- GitHub is canonical for issues/PRs; `status/issues-snapshot.json` is the committed fallback for an offline clone.
