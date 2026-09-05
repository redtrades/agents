# Financial model — SDVOSB deliverables factory

**Current model is v5:** `SUMMARY-v5.md` + `sdvosb-financial-model-v5.xlsx` (PLAN-V5, $699 packet). This file describes the retired v3 workbook. Do not quote it as current.

2026-08-22. Three workbooks — **lineage corrected 2026-08-22** (PROPOSAL-0009; this section previously mislabeled the unversioned original as "v2," and didn't mention the real v2 workbook existed at all — flagged by `SUMMARY-v2-standalone.md`, unresolved until this revision):

- **`sdvosb-financial-model-v3.xlsx` — current.** Models the integrated plan per PLAN-V4: outbound ramp 15→50→100–150/wk with reply-rate dilution, inbound growth funnel phased in per `research/growth-plan/REPORT.md`, delegated review as a direct cost from M4, founder time at **$60/hr** below the cash line. **BASE and OPTIMISTIC only.**
- **`sdvosb-financial-model-v2.xlsx` (v2)** — a real intermediate model (5 revisions: annual opex, $60/hr founder cost, delegable review, 100–200/wk outreach, newsletter inbound) built between v1 and v3. Full summary: `SUMMARY-v2-standalone.md`. Base M24 run-rate **$136.9K**. It's unclear whether v3 was built on top of this revision or independently re-derived from v1, skipping it — unresolved, flagged here so it isn't silently lost again.
- **`sdvosb-financial-model.xlsx` (v1, unversioned)** — retained unchanged; it holds the **Conservative** (failure-to-convert) case and the pre-delegation, founder-ceiling world. Its structural findings still stand (see "v2 findings that survive" below — named for the section that documents them, not the workbook version).

Assumptions sheet drives everything; blue cells are inputs, **yellow cells are working targets or guesses — none of them are measurements.**

## Headline numbers (v3)

| | Base | Optimistic |
|---|---:|---:|
| Revenue — Year 1 | $67.9K | $289.1K |
| Revenue — Year 2 | $161.3K | $794.0K |
| M24 run-rate (annualized) | $194.9K | $956.4K |
| EBIT — 24 mo. cumulative cash | **+$205.6K** | **+$1,022.6K** |
| True economic profit — 24 mo. (founder @ $60/hr) | **+$172.2K** | **+$992.3K** |
| Customers acquired — 24 mo. | 200 | 718 |
| Digest subscribers at M24 | 2,000 | 3,975 |
| Core subscribers at M24 | 9.8 | 47.4 |
| Delegated review cost — 24 mo. | $9.0K | $22.8K |
| Founder hours/wk — Y2 average | 5.5 | 5.2 |

**Revenue by source — Year 2 (the channel mix PLAN-V4 §6 targets):**

| Source | Base | Optimistic |
|---|---:|---:|
| Outbound deliverables | $83.5K (52%) | $465.1K (59%) |
| Inbound deliverables (digest → mini-snapshot → paid) | $39.4K (24%) | $156.7K (20%) |
| Feed licenses | $9.0K (6%) | $30.0K (4%) |
| Subscriptions (Core, ladder-fed) | $29.5K (18%) | $142.1K (18%) |
| Inbound share of *deliverables* revenue at M24 | 38% | 31% |

## What changed vs v1, and why the numbers moved

*(Section retitled 2026-08-22, PROPOSAL-0009 — this comparison is against the unversioned original workbook, "v1" per the corrected lineage above, not the real v2. It's unresolved whether v3 supersedes v2 or bypassed it — see the lineage note above.)*

Base M24 run-rate goes $72K (v1) → $195K (v3) — for comparison, the real v2's intermediate figure is $136.9K (`SUMMARY-v2-standalone.md`). Three drivers, all decisions, not optimism: (1) the **outreach cap moves** from 20/wk (founder-review-limited) to 100–150/wk under delegated review — v3 honestly dilutes reply rates with volume (Base 15%→8%, Opt 25%→12% across the ramp) rather than assuming validation-level precision at scale; (2) an **inbound funnel exists at all** — v2 had zero inbound; (3) **Core uptake is ladder-fed** (% of active customers/mo) instead of a flat subs/mo guess, calibrated so Optimistic lands at ~47 subs by M24, inside PLAN-V2's 45–58-subscriber analysis band.

The founder ceiling is gone as a revenue constraint and reappears as a **cost line**: delegated review runs $375–1,900/mo at scale ($40–60/hr contract/agent reviewers), founder drops to 15–20% spot-check minutes, and total founder load stays ~5–5.5 hrs/wk *in both scenarios* — the model's structural claim is that revenue scales while founder hours don't. Founder time is priced at $60/hr per Mike's convention (v2 used $150–250/hr; at $60/hr and positive cash, economic profit tracks EBIT closely — the interesting founder-time question is now hours, not dollars).

## Honest-assumptions ledger — what is measured vs not

- **Measured/validated:** review-minute targets, $39/mo stack, Stripe, LLM cost band (and local-Qwen routing lowering it). *(Corrected 2026-08-22, PROPOSAL-0009: "prices" removed from this line — prices are set, not validated; zero units have sold as of this revision. Opex removed too — see the missing-cost-lines note below; what's measured is the stack cost, not full opex.)*
- **Set, not validated:** prices ($450/$750/$1,500 ladder). This ledger's credibility rests on label discipline; the original "measured/validated: prices" line broke it.
- **Benchmark, not ours:** 15–25% reply on signal-triggered cold email; SEO month-6/7 indexing inflection.
- **⚠ Still THE untested assumption: reply→paid conversion (20%/35%).** Zero data, inherited by every outbound line, measured by the 30-day kill-gates. Unchanged from v2 and still the single number that decides viability.
- **Working targets (growth-plan §7, yellow-flagged):** all digest growth rates (40–100 Base / 75–200 Opt subs/mo), 15% sub→mini-snapshot, 7–10% mini-snapshot→paid, the digest→paid trickle, the 50/50 inbound first-purchase split, and Core uptake. External benchmarks mapped to our funnel; replace with measurements within 90 days of the digest launching.
- **Guesses:** reply dilution at full ramp, repeat/attach rates (v2 values), reviewer rate, overhead multiplier, full-ramp month.

**Flagged 2026-08-22 (PROPOSAL-0009), workbook update pending — TASK-0012:**

- **Core subscription revenue ($29.5K Base Y2 / $142.1K Optimistic Y2, 18% of revenue in both) is modeled for a product with no scope, price, or cadence document anywhere in this repo.** Treat every Core figure above as a placeholder wearing a number until a one-page Core product definition exists (founder call — scope/price/cadence) or the line is zeroed in the workbook. Do not quote Core revenue in planning conversations until one of those two things happens.
- **Missing opex lines**, individually trivial but collectively material to the quoted "~$17/mo" fixed-burn figure: E&O insurance (~$700–1,500/yr), one-time legal review of client terms (~$1–3K, PROPOSAL-0010), a refund/chargeback reserve (1–2% of revenue), and the second sending domain + tooling at ramp (PROPOSAL-0006, ~$10/yr + ~$25–30/mo GMass). **Restate "fixed burn" as ~$150–250/mo steady state, not ~$17/mo** — the $17/mo figure is quoted in planning conversations and is off by roughly 10x once these are included.
- **No pessimistic reply-rate row exists.** Base currently assumes 15%→8% reply dilution across the ramp; add a 5%→3% row so "kill-gates passed at low reply" has a pre-computed revenue meaning (PROPOSAL-0006).
- **No inbound-fails/outbound-only sensitivity exists.** v2's Conservative case predates the inbound funnel entirely; no current sheet shows what v3's Base looks like with digest growth = 0. Add that row so a stalled inbound funnel doesn't silently retro-justify the plan.

These four are workbook-formula changes, not documentation edits — this session had no `openpyxl` available to make them without risking the model's independently-verified 2,688-cell recomputation. Filed as `TASK-0012` rather than silently applied.

**Saturation caveat (Optimistic):** 150 sends/wk on a 3-touch cadence ≈ 217 new firms/mo; cumulative firms contacted by M24 ≈ 4,300 against the ~38.5K firm-code universe — the firm side alone shows no strain (revised 2026-08-22, PROPOSAL-0001; superseded the "4,000–8,000-firm" comparison, which used an underived figure — see `sop/PLAN-V3.md` §3). **The tighter constraint is notice supply, not firm supply**: only ~250–400 Sources Sought notices/yr survive content disqualifiers across the 6 target NAICS (`research/naics-selection/REPORT.md`, `research/feasibility-review/REPORT.md` F1). At one client per notice, 250–400 notices/yr × $450 caps response-only revenue at $112K–$180K/yr before any capture-rate discount — Optimistic's Y2 outbound line ($465K ≈ ~850 deliverables/yr) **exceeds the entire viable-notice supply of the 6-code set even at 100% capture**, and is only reachable via NAICS widening *and* selling multiple clients per notice (PROPOSAL-0002 — no policy exists yet for the latter). Base Y2 outbound ($83.5K ≈ ~150 deliverables/yr) fits inside the notice ceiling only with a Snapshot-heavy mix or NAICS widening; it is not a low-strain case on the notice axis the way it is on the firm axis. Base (~200 customers, ~2,900 firms contacted) has no firm-side strain.

## v1 findings that survive

*(Retitled 2026-08-22, PROPOSAL-0009 — was "v2 findings," but the findings below are v1's, per the corrected lineage.)*

The conservative case's shape still governs the downside: at failure-level conversion the cash loss is trivial and the real cost is founder time — which is why the kill-gates outrank everything (PLAN-V4 §0). The ~$1,000/founder-review-hour rule survives as a per-unit margin rule under delegation (PLAN-V4 §3). And the v1 ceiling finding inverts cleanly: lead flow was the binding constraint at 20/wk; v3 spends money (reviewers) to make it bind later.

## Verification

Built with openpyxl (formulas only, no hardcoded results). LibreOffice recalculation: **3,008 formulas, 0 errors.** Independent recomputation: the entire model was re-derived in a separate pure-Python implementation from the assumption values (no formula reuse) and compared cell-by-cell against the workbook's calculated values — **2,688 cells checked, 0 mismatches** across both scenario sheets. Summary-sheet aggregates cross-checked against the same recomputation.
