> **✓ Version-numbering conflict — labels fixed 2026-08-22 in `SUMMARY.md` (PROPOSAL-0009).**
> This file describes `sdvosb-financial-model-v2.xlsx`, a real intermediate model (5 revisions: annual
> opex, $60/hr founder cost, delegable review, 100–200/wk outreach, newsletter inbound) built between
> the original unversioned workbook ("v1" per this file) and `sdvosb-financial-model-v3.xlsx`.
> The canonical `SUMMARY.md` in this directory previously didn't know this file existed — it called the
> *unversioned* workbook "v2" and cited a Base M24 run-rate of $72.0K as "v2," when that
> $72.0K figure is actually **v1's** number; the real v2's Base M24 run-rate is **$136.9K**, now
> correctly attributed there. **Still open:** whether v3 was built on top of this v2 revision or
> independently re-derived from v1, skipping it — the label fix doesn't resolve that provenance
> question, only the mislabeling.

# Financial model — SDVOSB deliverables factory (v2)

2026-08-22. Driver-based monthly model, 24 months from Sep-2026, three scenarios. Files: `sdvosb-financial-model-v2.xlsx` (current) and `sdvosb-financial-model.xlsx` (v1, kept for comparison). Blue cells = inputs; yellow = untested assumptions. v2 implements Mike's five revisions: annual opex line items, $60/hr founder opportunity cost, delegable review (no founder-hours ceiling), 100–200/wk outreach with matched-firm supply as the constraint, newsletter inbound, and benchmark-anchored conversion rates.

## Headline numbers (v2, with v1 in parentheses)

| | Conservative | Base | Optimistic |
|---|---:|---:|---:|
| Revenue — Year 1 | $3.1K ($1.7K) | $65.0K ($32.5K) | $415.8K ($133.1K) |
| Revenue — Year 2 | $4.5K ($2.0K) | $122.9K ($62.9K) | $863.5K ($309.8K) |
| M24 run-rate (annualized) | $4.8K ($2.0K) | $136.9K ($72.0K) | $955.7K ($365.1K) |
| Cumulative cash — 24 mo. | **−$2.2K** (−$5.7K) | **+$166.5K** (+$85.5K) | **+$1.22M** (+$427.5K) |
| True economic profit — 24 mo. | **−$27.2K** (−$110.5K) | **+$146.9K** (+$7.2K) | **+$1.21M** (+$357.1K) |
| Customers acquired | 15 (7) | 159 (46) | 927 (170) |
| Gross margin — Y2 | 45% | 91% | 96% |
| Founder hours/wk — Y2 avg | 4.0 | 3.1 | 2.4 |

## Why v2 moves so much — the deltas that matter

**Volume (change #4) is nearly the whole story.** Raising outreach from a 10–20/wk cap to 50/wk (M2) and 100–200/wk (M3+) multiplies the funnel roughly 8–10×. Base revenue roughly doubles-to-quadruples despite *lower* per-email conversion assumptions, because volume swamps rate. The modeled constraint is now matched-firm supply (100/200/400 emails/wk by scenario), and the pool diagnostic stays honest: 0.97–1.30 contacts per firm per year against the 4,000–8,000-firm pool — plausible, but list *precision at 10× volume is unproven* (v1's 10–20/wk was precise by construction).

**Delegable review (change #3) removes the ceiling and changes the founder-time story.** Reviews cost $5–40 each after month 3–4 instead of consuming founder hours ($8.2K total delegated cost in base over 24 mo — trivial against revenue). Founder time drops to ~2.5–4 hrs/wk. Combined with $60/hr (change #2), true economic profit now nearly equals cash EBIT — in v1 at $200/hr the base case barely broke even against Mike's alternative wage; in v2 it clears it easily. Note what is *not* priced: the provenance wedge is founder judgment, and non-founder review quality risk has no line item.

**Opex (change #1) shrinks and gets honest.** Fixed monthly padding ($250/mo blanket) is replaced by annual items charged when incurred: insurance $500–1,200/yr (researched solo-consultant GL ~$350 + E&O ~$450–670), LLC formation $300 + $150/yr renewal, accounting $200–500/yr. Total 24-mo opex: $3.7–5.2K (v1: $7.4–9.2K). The biggest costs are now correctly the stack — in conservative, pipeline LLM spend (~$163/mo at $0.50/email) exceeds all fixed opex and drags gross margin to 45%; in base/opt, LLM + review costs scale with volume as Mike specified.

**Conservative now shows failure-to-convert precisely:** at the *measured industry-average* end-to-end rate (0.18% email→customer — the derived B2B mean), the business is roughly cash-flat (−$2.2K over 24 months, EBIT-positive from M4 in most months) but earns ~$187/mo. Failure is nearly free in cash and costs ~$27K in founder time. The kill-test is still worth running purely because downside is so small.

## The assumptions that matter most (unchanged in kind, re-anchored in value)

1. **Reply→paid conversion (6/15/30%) — still THE untested assumption.** Now benchmark-anchored: conservative = the derived B2B average reply→close (~6%, from 0.215% email→deal ÷ 3.43% reply, Instantly/Reachoutly 2026 data); base/opt assume a $450 deadline-tied point purchase closes far above enterprise-deal averages. End-to-end email→customer runs 0.18% / 1.2% / 4.5% vs ~0.2% industry average — **optimistic is ~22× the measured average and should be read as a ceiling of belief, not a plan**. Nothing right of Conservative deserves belief until PLAN-V3 §8's kill-test returns a number.
2. **Precision at scale.** v2 silently assumes the 8% base reply rate (mid signal-based benchmark, 5–18% per Martal) *survives a 10× volume increase*. Signal-triggered quality at 10–20/wk is hand-picked; at 200/wk it depends on the matching pipeline. If reply rate degrades toward the 3.4% platform average at volume, base-case revenue falls ~55% toward conservative. This is the new second-biggest risk, created by change #4.
3. **Repeat purchase rate (0/5/10%/mo).** Still a month-one measurement, not a known. In base, repeats + snapshot attach are ~40% of deliverables revenue by M24; optimistic's $1.2M cash is mostly this compounding on a 900-customer base.

Newsletter inbound is modeled (2%/opt-in per email + organic, converting at 0.1–0.6%/mo per B2B newsletter benchmarks of ~3–5%/yr of subscribers) but stays modest: ~12% of customers in base — a floor-raiser, not a driver.

## Sources

Cold email benchmarks: [Instantly 2026 benchmark report](https://instantly.ai/cold-email-benchmark-report-2026), [Martal B2B cold email statistics](https://martal.ca/b2b-cold-email-statistics-lb/), [Reachoutly conversion benchmarks](https://reachoutly.com/cold-email/conversion-rate/), [Belkins response-rate study](https://belkins.io/blog/cold-email-response-rates). Newsletter conversion: [Averi B2B newsletter benchmarks](https://resources.averi.ai/benchmarks/email-newsletter-benchmarks), [Popupsmart B2B email benchmarks](https://popupsmart.com/blog/b2b-email-marketing-benchmarks). Insurance: [MoneyGeek consulting insurance costs](https://www.moneygeek.com/insurance/business/consulting/cost/), [TechInsurance consultant costs](https://www.techinsurance.com/consulting-insurance/cost), [Insurance Canopy consultant policies](https://www.insurancecanopy.com/consultants-insurance/cost). Internal: PLAN-V3 (`~/govcon-factory/sop/`), SOP-DELIVERABLES, claim-ledger, PLAN-V2.
