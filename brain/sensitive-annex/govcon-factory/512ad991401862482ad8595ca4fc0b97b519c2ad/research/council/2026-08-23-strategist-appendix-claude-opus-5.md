# Strategist appendix — economics, power, and the correction log

**Author:** IdeaPlans (claude-opus-5), STRATEGIST seat · 2026-08-23
**Seat index and the proposed V6 amendments: `2026-08-23-V6-AMENDMENTS-strategist.md`. Parent brief: `2026-08-23-strategist-claude-opus-5.md`.**

**Why this file exists:** the council output contract caps the brief at ~1,200 words with headings 1-12 only. This holds the working detail the brief cites and cannot carry. Nothing here is a decision. Primary sources for inventory and firm counts are `2026-08-23-runtime-receipts-research.md`; competitor pages are `2026-08-23-market-scan-claude-opus-5.md`.

---

## A. Unit economics — three floors, with scopes

Inputs from `sop/financial-model/build_v5.py:23-31` ($699, Stripe 3%, `LLM_PKT = 3`, `LLM_EMAIL = 0.2`, `OPS_H_MO = 15`, `REVIEW_H = 0.33`, `LEGAL_M1 = 2000`, ~$175/mo burn). Prebuild means every exposure costs $3.20 whether or not it sells; net per sale is $678.

| Floor | Conversion | Meaning |
|---|---|---|
| Variable contribution | **0.47%** | Below this, every email loses money |
| Cash break-even (258 exposures/mo) | **0.67%** | Below this, the company is cash-negative |
| Practical (15 ops hrs/mo + release at $60/hr) | **~1.22%** | Below this, the founder works for nothing |

I first published 0.47% as "or it is not a business." That was variable contribution only, and wrong in the direction that flatters. Sol's corrections reproduce exactly. **The repo's Conservative 0.5% clears the first floor and fails the other two.**

**These are planning floors, not thresholds** (terra). They inherit a strict-eligible-firm denominator that has never been measured, so they size the problem and cannot gate it.

**Exposures for ~$1,150/week net** (~$60k/yr; target arbitrary, scales linearly):

| Conversion | Margin/exposure | Exposures/wk |
|---|---|---|
| 0.5% | $0.19 | 6,048 |
| 1% | $3.58 | 321 |
| **3%** | **$17.14** | **67** |
| 6% | $37.48 | 31 |

## B. Test power — what 30 days can and cannot measure

P(observing zero sales):

| Delivered | at 3% Base | at 1.22% practical | at 0.67% cash |
|---|---|---|---|
| 40 | 0.296 | 0.612 | 0.764 |
| 80 | 0.087 | 0.375 | 0.584 |
| **100** | **0.048** | **0.293** | 0.511 |
| 245 | 0.001 | 0.050 | 0.194 |

0/100 rejects the unmeasured 3% Base assumption at ~5%. It leaves a **29% chance of a zero even if the true rate is exactly the practical floor**. Rejecting 1.22% at 5% needs **245 delivered** (~$784 prebuild); the cash floor needs **446** (~$1,427).

**The 30-day test can reject the Base assumption and cannot separate "dead" from "worth doing slowly."** No cohort reachable in 30 days can. The month's output is a rate-and-factory measurement, not a verdict.

**On the cohort design:** 100 delivered, unsplit, all full machine drafts. At n=50 per arm P(zero | 3%) = 0.218 so a split cannot select a winner — and more decisively (terra), prebuilt-draft vs map-only changes the customer-facing delivery state, so a pooled result tests neither arm nor the offer V5 specifies.

## C. Release capacity

Giving *all* founder hours to release: 18 packets/wk at 10 min on 3 hrs, 9 at 20 min, 4.5 at 40 min — an upper bound only. **Operative figure adjusts for ops** (Sol): `OPS_H_MO = 15` means 5 total founder hrs/week (~21.7/mo) leaves ~6.5 hrs/mo for release — **~20 paid packets/month at 20 min, 10 at 40 min.** Base M24 is ~19/month, so release binds exactly at the top of Base and not before.

## D. Four failure shapes this council produced in its own work

Each was committed by a seat while arguing against it. These matter more than any single business finding here: they are the mechanism by which the repo's 250-400 sellable-notice ceiling became load-bearing.

1. **A gate that can never fire is worse than no gate** — it reads like a safeguard. Mine: "conversion under ~1% flips the prebuild policy," when no reachable cohort can measure a rate that low.
2. **`UNCALIBRATED` does not launder a bad provenance** — it makes an unusable number look careful. The minimum-candidate N derived from a truncated query (Pollen, struck by Pollen).
3. **Fix the primary source first, citing documents second** — a correction travelling downstream but not upstream leaves the wrong version at the most authoritative address (Pollen). The S5 scope error was fixed in two derived briefs, one of them in a message to Mike, while the origin kept it.
4. **A conditional guardrail inverts when its condition lapses** (Write). *"Do not put the gap count back while the split test is running"* became permission the moment I retired the split — no edit, no error. **State the invariant, not the experiment.** Only *instructions* carry conditions, so the audit belongs on `sop/`, `templates/` and `gates/`, not on research files; the retired PLAN-V3 digest routing in `email-3-last-call` is probably the same bug, older.

Underlying rules, attributed: **every count must paginate to `hasNext: false` or carry lower-bound status, with page count and stopping condition recorded** (terra). **`git diff` proves an edit landed; only a full read proves the document still agrees with itself** (Pollen, after breaking terra's).

## E. Correction log — claims I published and withdrew

| Claim | Status |
|---|---|
| "VA × 236220 is the first cell" | **Withdrawn.** Crossed two marginal distributions; that cell is empty |
| "334517 has six firms in the entire federal record at VA" | **Withdrawn.** Top-100-by-amount capped query, not a census; ≥54 paginated |
| "a six-fold spread" (then "seventeen-fold") | **Withdrawn.** Compares one complete census to three truncated floors |
| "0.47% or it is not a business" | **Corrected.** Variable contribution only; see §A |
| "conversion under ~1% flips the prebuild policy" | **Withdrawn.** A gate that could never fire |
| "S5 403 means nothing ships" / "stops everything" | **Corrected.** Blocks outbound targeting, not inbound or requested packets |
| "founder minutes are the ceiling" | **Corrected.** True past ~20 paid packets/month; false at launch volumes |
| TASK-0014 as the contact-path gate | **Withdrawn.** Its scope is terms/E&O/refund/SLA; a new counsel task is the TASK-0001 dependency |
| "0 paid in 40, twice" | **Superseded** by the 100-delivered unsplit cohort |
| "nobody pays for this at any price" | **Falsified** by marketplace evidence within the hour |

Six further stale items were found by reading the brief end to end after ten targeted patches, including a ~4x units contradiction between "packets/week" and "packets/month" in the headline verdict.
