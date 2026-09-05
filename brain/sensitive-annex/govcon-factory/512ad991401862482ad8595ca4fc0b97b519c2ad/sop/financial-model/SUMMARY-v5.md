# Financial model v5

2026-08-23. Models PLAN-V5. Workbook: `sdvosb-financial-model-v5.xlsx` (formulas, three scenario sheets + Assumptions).

v1–v3 remain on disk as history. Do not quote them as current. They priced a $450 response factory and a Core subscription that was never defined.

## What v5 models

| Object | Price | Role |
|---|---|---|
| Opportunity packet | **$699** | Only default paid SKU |
| Industry report | $0 | Magnet |
| Newsletter / code watch | $0 | Hub |
| Consultant feed | **$249/mo** | Side test, not the company |

No Core line.

## Drivers (Assumptions sheet, yellow = untested)

| Driver | Conservative | Base | Optimistic |
|---|---:|---:|---:|
| Notices processed / week (after M2) | 2 | 5 | 8 |
| List-3 firms emailed / notice | 10 | 12 | 15 |
| Matched email → paid packet | **0.5%** | **3%** | **6%** |
| Inbound packets / month (UEI + newsletter), cap | 0 | 1→6 | 3→16 |
| Repeat (share of prior buyers / month) | 0 | 2% | 4% |
| Consultant seats (from M6) | 0 | 1 | 4 |
| Newsletter new subs / month | 0 | 40 | 80 |

Email→paid is the viability number. Conservative is near generic B2B cold conversion. Base assumes the “I already built your map” mail beats generic. Optimistic assumes the hub is warm. **None of these are measurements.**

## Headline numbers (computed)

| | Conservative | Base | Optimistic |
|---|---:|---:|---:|
| Revenue — Year 1 | $3.3K | $94.1K | $371.8K |
| Revenue — Year 2 | $3.6K | $150.2K | $634.3K |
| M24 run-rate (annualized) | $3.6K | $163.5K | $723.0K |
| Packets — Year 1 | 5 | 130 | 515 |
| Packets — Year 2 | 5 | 211 | 890 |
| Cumulative cash, 24 mo. | ~$0 | +$229K | +$963K |
| Newsletter subs at M24 | 0 | 960 | 1,920 |

Cash is after stack (~$50), E&O (~$100), sending (~$25), Stripe ~3%, LLM ~$3/packet, and a $2,000 legal/terms hit in month 1. Founder time is **not** subtracted from cash. At $60/hr it is a memo line, not a payroll line.

Founder hours, steady state: roughly **5 hrs/week** in Base (review ~20 min/packet + a weekly send/LinkedIn block). Optimistic M24 (~85 packets/month) pushes toward **~10 hrs/week** unless review drops or someone else takes first pass. That is the real ceiling. Do not “fix” it by inventing Core.

## What is different from v3 on purpose

- One price. No $450/$750/$1,500 ladder. No 18% Core fantasy.
- Volume is **notices × list-3**, not 100–200 generic emails/week.
- Inbound is UEI + newsletter clicks, not a mini-snapshot SKU.
- Conservative exists again (v3 had dropped it).
- Fixed burn is ~$175/mo + legal, not “$17/mo.”

## Saturation

Viable Sources Sought in the first six NAICS are still on the order of **250–400 attachable notices/year**. Base Y2 (~211 packets) fits if some notices sell more than one packet and some packets are RFIs, not only SS. Optimistic Y2 (~890 packets) **does not fit** that pond. It requires more NAICS, more cert types, and/or inbound from primes/consultants. Treat Optimistic as “the factory escaped the SDVOSB SS pond,” not as year-2 of the beachhead.

## Verification

Workbook built with openpyxl. Scenario sheets are formula-driven from Assumptions. A pure-Python recomputation of the same drivers produced the headline table above (see `sop/financial-model/build_v5.py`). Re-run that script after changing inputs; do not hand-edit result cells.
