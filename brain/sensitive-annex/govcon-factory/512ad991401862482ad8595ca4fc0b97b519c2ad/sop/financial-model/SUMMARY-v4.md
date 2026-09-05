# Financial model v4 — target-backed

2026-08-26. Workbook: `sdvosb-financial-model-v4-target-backed.xlsx` (907 formulas, all live).
Build: `build_v4_target.py`. Market derivation: `tam/pull_sdvosb_tam.py`.

**Numbered v4 because it is target-backed, not because it supersedes v5's numbering.** v5 modelled
PLAN-V5 forward from drivers. This models Mike's stated target backward from month 12.

## The target

**$8,000–$10,000/month of net cash, after all costs, by month 12.** Founder time is not in the cash
line; it sits below it as a memo at $60/hr.

## Verdict: yes, on per-deliverable sales alone

| At month 12 | |
|---|---:|
| Net cash / month | **$8,821** |
| Deliverables sold / month | 14.4 |
| Paying customers that month | 14.4 |
| Firms emailed / week | 62 |
| Share of addressable notice supply | 36% |
| Sales capture (sales ÷ addressable moments) | 10.5% |
| Mike's hours / week | **7.1 of his 40** |
| Cumulative net cash, months 1–12 | $52,163 |
| First month at $3–5K (minimum viable) | **M5** |
| First month at $8K | **M12** |

No recurring revenue is counted anywhere in the base case.

## What changed from v5, and why

**1. Market size is derived, not inherited.** Mike's method: pull SDVOSB set-aside and sole-source
awards from USASpending (FY2023–FY2025, keyless, reproducible), count distinct winning firms and
their NAICS distribution, count new award actions per year and per code.

| | Value |
|---|---|
| Firms that actually **win** SDVOSB set-aside work | **~1,700/yr**, 2,989 distinct over 3 years |
| New award actions, all agency | 11,950 → 11,429 → **9,255** (FY23→FY25) |
| New award actions, VA only | 6,929 → 6,035 → **5,125** |
| Distinct NAICS touched | ~390 |

This replaces every firm-count proxy in the repo: 4,000–8,000 (never derived), ~1,500
(contradictory), 27,425/38,535 firm-code slots (double-counted), 14,979 certified UEIs (certified,
not winning). The certified pool is ~15,000; the pool with a demonstrated federal win is ~1,700/yr.

**TAM** ~$2.5M/yr · **SAM** (6 codes) ~$767K/yr · **SAM** (12 codes) ~$1.1M/yr · **SOM** ~$133K/yr.
SOM is 17% of the 6-code SAM, right at the top of what the feasibility review calls a strong capture.

**2. The 250–400 sellable-notice-moments figure is superseded.** It counted Sources Sought notices
only. Since issue #157 the factory produces four deliverable types and routes by notice type, so the
addressable set is every procurement with a pre-award moment. Award actions × the 30–50%
attachability haircut gives **555–924/yr in the 6 codes** and **883–1,472 in the top 12** — roughly
2.2× and 3.6× the prior figure. On the old denominator the base case would have run at 78% of
supply; on the derived one it runs at 36%. Keep 250–400 on the record as the Sources-Sought-only
number, which it correctly is.

*Standing caveat:* the 30–50% haircut was derived against Sources Sought flow and has **not** been
re-derived against the wider set. It is the one open number and it is computable from data we
already pull. Do that before treating the PASS as settled.

**3. Pricing is tiered by work content** (Mike, 2026-08-26), not flat $699:
T1 snapshot $299 · T2 Sources Sought packet $699 · T3 RFI/combined-synopsis $999 · T4 RFP response
starter $1,499. At a 20/50/20/10 mix the blended price is **$759**. Value/contingency pricing stays
at zero until counsel confirms legality.

**4. Recurring revenue is out of the base case entirely.** Data-feed licensing: removed, ToS-exposed
and competes with free. Alert-only subscription: removed, SAM.gov gives saved-search alerts away
free. Alerts-plus-a-draft retainer: removed as a wedge, HigherGov already ships one-click Sources
Sought drafting on a $500/yr plan. Pure SaaS: rejected, no USP against incumbents.

**5. Mike's time is not the constraint.** At a 40 hr/week ceiling with agent production costing
tokens rather than hours:

| Regime | Deliverables/month supported |
|---|---:|
| Today (current review reality, every review personally, per-item send approval) | **156** |
| SOP target review | 200 |
| Current reality + delegated first pass | 286 |
| SOP target + delegated | 341 |
| SOP target + delegated + **batch send approval** | 623 |

The target needs 14.6. Headroom is 142/month in the worst regime. Delegation at this volume is a
margin decision (~5% of price), not a capacity one. The fastest-growing line at scale is send
approval, not review — batch approval is the cheaper lever and should come first.

## The three assumptions everything rests on

1. **Reply → paid at 20%.** Never measured. PLAN-V5 calls its own 3% email-to-paid driver a
   non-measurement. At 10% the target slips well past month 12; at 5% it is unreachable in these
   NAICS at any volume the pond can feed.
2. **Repeat purchase within 6 months at 20%.** Never measured, and now the swing variable, because
   all three subscription ideas are dead or blocked. Every 10 points of repeat rate removes ~18% of
   required outreach. At 0% the target still lands, but supply consumption goes 36% → 52%.
3. **The deliverable justifies a premium over a $500/yr subscription.** Our blended price is 1.5×
   their annual fee for one deliverable. The premium rests on four things a subscription
   structurally cannot sell: per-claim provenance, fail-closed gates, a named accountable human, and
   the willingness to say *nothing here is worth bidding*. All four are built. What is unproven is
   whether a buyer can see them before paying — and the 2026-08-26 e2e run says the artifact does not
   yet demonstrate them (F2–F5). Execution risk, not positioning risk.

A fourth is binary: counsel has not cleared DSBS/SAM contact use (PLAN-V5 risk 2, TASK-0019). If
that comes back no, the outbound leg disappears. Ask it before the domain finishes warming.

## Earliest validation dates

| Measurable | When |
|---|---|
| Deliverability + bounce rate | ~day 30 |
| Reply rate (n≈80) | ~day 55 / week 8 |
| **Reply → paid (~300 exposures)** | **~month 5–6** |
| 3-month partial repeat rate (early indicator) | ~month 6 |
| Repeat within 6 months, honest reading | ~month 9–12 |

PLAN-V5's 30-day go/no-go fires on 40–80 exposures, where expected sales at this model's own base
rate are one to two. One sale and zero sales are not distinguishable at that n. **The 30-day gate
can kill on reply rate and deliverability but not on conversion, and it should say so.** Put the
conversion kill-gate at ~300 exposures and diarise the date now.

## Recommendations

- **Commit publicly to $3–5K/mo for month 12; treat $8–10K as the month-18 number.** The plan does
  not change, only the date on the promise. That removes the pressure that would otherwise push
  toward loosening the matcher, emailing list 1, or discounting against the $500/yr anchor.
- **Widen NAICS to ~12 codes.** Highest-value additions: **238220** Plumbing/HVAC (266 FY25 actions,
  149 firms), **541310** Architectural (77/41), **238210** Electrical (94/72) — construction
  adjacencies where 236220 credibility transfers. Two current codes are thin: 541512 (30 actions)
  and 541611 (97). The manufacturing codes (339113, 339112, 337215, 334510) have high action counts
  but are catalogue buying; check attachability before committing.
- **If price is pressured, shift the mix up the ladder, do not cut prices.** A forced move to $525
  blended nearly doubles required outreach (256 → 584 firms/month) and puts the model at 79% of
  addressable supply — supply-capped. Contribution falls faster than price, because prebuild waste
  and review cost are fixed in dollars.
- **Instrument acquisition month, source and tier on the first sale**, so the repeat cohort exists
  to be read at month six rather than reconstructed from invoices.
- **Re-run `tam/pull_sdvosb_tam.py` quarterly.** SDVOSB set-aside award actions fell 23% (all-agency)
  and 26% (VA) between FY2023 and FY2025. Two more years at that rate erases the headroom above.

## Plan reconciliation (open item)

`AGENTS.md` points at `sop/PLAN-V5.md` as canonical and PLAN-V5 is the newest plan file on disk.
`CHANGELOG.md` says PLAN-V6 superseded V5 on 2026-08-23 and that PLAN-V7 is a blocked draft (#8).
Neither `PLAN-V6.md` nor `PLAN-V7.md` exists in the working tree. Either V6 should exist as a file,
or AGENTS.md should stop citing a version that does not.

## Verification

Workbook built with openpyxl, recalculated under LibreOffice: **907 formulas, 0 errors**. An
independent Python recomputation written from the stated method (not from the workbook's formulas)
agreed on **28 of 28** checks — blended price, contributions, the month-12 solve, all twelve funnel
months, cumulative cash, founder hours, capacity regimes, and the TAM/SAM figures. Re-run
`build_v4_target.py` after changing inputs; do not hand-edit result cells.

## Sources

Repo: `sop/PLAN-V5.md`, `sop/PLAN-V4.md` §3–§5, `sop/financial-model/build_v5.py`,
`research/outreach-playbook/REPORT.md`, `research/feasibility-final/REPORT.md`,
`research/feasibility-review/REPORT.md`, `research/growth-plan/REPORT.md`,
`research/stack-selection/REPORT.md`, `research/govconapi-exploration/REPORT.md`,
`research/e2e-validation-2026-08-26/REPORT.md`, `research/council/2026-08-23-*`, `AGENTS.md` (#80,
#157). External: USASpending API (pulled 2026-08-26, see `tam/`), Instantly 2026 cold-email
benchmark, Lavender, FTC CAN-SPAM guide, Mailivery warm-up guidance, Insureon E&O pricing, GTM
research 2026-08-26 (HigherGov $500/yr one-click drafting; SAM.gov free saved-search alerts;
GovTribe alerts plus event-triggered AI).
