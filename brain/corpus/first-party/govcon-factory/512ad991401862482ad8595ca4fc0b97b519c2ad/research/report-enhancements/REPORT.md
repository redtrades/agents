# Report Enhancements — raising Sources Sought Responses and Market Snapshots to best-in-class

2026-08-22. Research task: benchmark our two products against premium GovCon intelligence (GovWin IQ, BGOV, Leadership Connect), Shipley-style capture practice, and practitioner BD literature; identify what is derivable from data we already touch but don't use; produce a prioritized enhancement list per product and concrete SOP amendment text for the cheap wins. Inputs: `SOP-DELIVERABLES.md` (2026-08-22 draft), the 10-deliverable `sample-set/`, `PLAN-V3.md`. Every recommended enhancement passes the provenance rule (public, verifiable, citable); anything that doesn't is explicitly binned **skip**.

**Bottom line:** the biggest gaps between our Snapshot and a $15–40K/yr GovWin seat are (1) **pre-RFP/forecast intelligence** — GovWin's core value is tracking opportunities before they hit SAM, and agency procurement forecasts are public; (2) **incumbent-health depth** — competition fields, modification history, protest records, and FAPIIS integrity records are all public and we pull none of them; (3) **people/relationship context** — mostly *not* publicly derivable, skip. Six cheap wins can go into the SOP now with ~zero founder-review-time increase because they extend the existing mechanical-gate pattern. Win-theme/hot-button/pWin-scored capture content is real premium-tier material (a third rung between Snapshot and red-team) but raises review time and should not be folded into the $750 product.

---

## 1. What the premium products actually contain

### 1.1 Deltek GovWin IQ (~$13K floor, ~$29K average, $119K enterprise/yr)

Pricing: no published sheet; entry single-seat ~$6–12K, most teams $20–42K with modules, average ~$29K per Vendr transaction data, minimum ~$13K, enterprise to $119K ([Civic IQ pricing teardown](https://civiciq.com/blog/govwin-iq-pricing-2026); [Fed-Spend pricing analysis](https://fed-spend.com/blog/govwin-iq-pricing-2026-deltek-cost-alternatives); [ITQlick](https://www.itqlick.com/govwin-iq/pricing)).

An **analyst-tracked opportunity brief** contains, per Deltek's own product literature ([Deltek: AI & UX in GovWin IQ](https://www.deltek.com/resources/articles/govwin-ai-ux-innovation/)):

| GovWin brief section | Do we have an equivalent? |
|---|---|
| Scope of Work summary | ✅ Snapshot §1 |
| NAICS | ✅ §1 |
| Funding / Contract Value | ⚠️ Partial — we report the notice's stated magnitude; GovWin adds program funding context |
| **Procurement timeline** (forecast → pre-RFP → RFP → award, with predicted dates) | ❌ We only have posted/due dates |
| **Latest analyst update** (narrative: what changed, what the agency said) | ❌ (our analog would be Q&A/amendment tracking — G5 checks freshness but the doc doesn't narrate change) |
| **Competitive landscape** | ✅ §3 — ours is arguably better-sourced (UEI-cited) |
| **Existing contracts & task orders** (incumbent vehicle detail) | ⚠️ Partial — §4 names incumbents but not the vehicles/orders structure |
| Related opportunities | ❌ |
| **Related pricing resources** (federal-exclusive) | ⚠️ Partial — §5 gives award-history calibration; GovWin adds labor-rate resources |
| Related contract documents | ✅ notice-raw inventory |

Two structural facts about GovWin worth copying strategically:

- **~75% of active analyst-tracked opportunities are in the forecast or pre-RFP stage** ([Deltek](https://www.deltek.com/resources/articles/artificial-intelligence-business-development-govwin-iq/)). The product's premium is *earliness*, not document quality. Our factory is notice-triggered; the public agency procurement forecasts (§3 below) are the free path to a slice of that earliness.
- **Smart Fit Score** ranks opportunities against a firm's profile using five criteria: Smart Tags (analyst classification), NAICS, description keywords, place of performance, and past history with the agency ([Deltek Smart Fit](https://www.deltek.com/resources/articles/machine-learning-govwin-iq-smart-fit-score/)). Our upstream candidate scoring (SOP §2.1) already does a crude version of this; the "past history with the agency" criterion is the one we don't use and could (client UEI × awarding sub-agency is one USASpending filter).

### 1.2 Bloomberg Government (~$5.7K–$10K+/yr reported)

BGOV's differentiator is **context wrapped around the data**: budget trends, agency leadership changes, and policy shifts that affect which contracts get funded, on top of a contracting dataset (3.85M solicitations, 47M+ task orders, 15M+ contracts) with incumbent and **burn-rate** analytics ([BGOV](https://about.bgov.com/); [Fed-Spend competitor teardown](https://fed-spend.com/blog/bloomberg-government-competitors-alternatives); [Civic IQ platform comparison](https://blogs.civiciq.com/2026/04/14/best-government-contract-tracking-software-for-2026-6-platforms-compared/)). Takeaways for us: (a) *burn rate* — outlays vs. obligated on an incumbent's contract, a field (`Total Outlays`) we already pull and never interpret; (b) budget context is mostly analyst labor we should not replicate at our price points, except where an agency forecast document hands it to us for free.

### 1.3 Leadership Connect (people intelligence)

Sells daily-verified org charts, bios, relationship maps, and contact data across government — 4,000+ verified changes/day ([Leadership Connect](https://leadershipconnect.io/); [FEDLINK vendor entry](https://www.loc.gov/flicc/contracts/VendorDirectory/le_leadershipconnectR.html)). This is the "customer relationship" leg of capture. **Verdict: skip as a product feature.** The only public, provenance-clean people data we touch is the CO/CS names on the notice and SBS contact records. Program-office org charts, personnel moves, and relationship maps are not derivable from our public sources without scraping that violates ToS (LinkedIn) or asserting facts we can't cite. The Snapshot already surfaces the CO/CS; one cheap addition (below) is listing the *other* contracting officers who signed comparable awards at the activity — that's in the FPDS record and is a legitimate, citable "who buys this here" signal.

### 1.4 Shipley-style capture practice

The Shipley capture plan structure: executive summary/objectives; **customer analysis incl. hot buttons**; competitive assessment (strengths/gaps); **win themes** (differentiators framed as customer benefit); risk register; action matrix. Win themes become section narratives, competitor weaknesses become **ghosting** fodder (unattributed emphasis of a competitor's weakness — "our approach avoids the transition risk of…"), and gap analysis surfaces teaming needs in time to act. pWin is re-estimated at gate reviews as intelligence improves. ([Shipley Capture Guide](https://www.shipleywins.com/tools-and-guidebooks/shipley-capture-guide); [Shipley on capture planning](https://www.shipleywins.com/blogs/capture-planning); [GovEagle Shipley guide](https://www.goveagle.com/blog/complete-shipley-process-guide); [Octant capture plan](https://octant.com/a-capture-plan-is-a-plan-to-win/))

Our Snapshot §7 is a bid/no-bid scorecard — the *decision* artifact. What Shipley adds beyond it is the *pursuit* artifact: hot buttons, win themes, ghost themes, gap/teaming actions. That content requires judgment on every line (it is advice, not aggregation), so it raises founder review time by design → premium tier, not a Snapshot amendment.

### 1.5 Down-market benchmark: Fed-Spend's pWin Verdict Engine

Directly relevant because it's built from exactly our data stack. Their published v1 model (vendor-published methodology — treat weights as reference, not gospel): **incumbent vulnerability 28%** (CPARS posture where available, terminations, exclusions, GAO protest sustain rate, contract growth, modification churn), **competition density 20%**, **profile fit 18%**, **price-to-win fit 14%**, **past-performance edge 12%**, **set-aside leverage 8%**, weights renormalizing when a signal is missing ([Fed-Spend pWin engine](https://fed-spend.com/blog/pwin-verdict-engine-win-probability-guide-2026)). Their practitioner-facing claims: a single incumbent GAO protest loss in 24 months is meaningful, two is a strong signal; incumbent win rate drops from ~68% to below 30% when multiple vulnerability factors stack ([Fed-Spend recompete guide](https://fed-spend.com/blog/recompete-strategy-guide); [find-recompetes guide](https://www.sweetspot.so/articles/government-contract-awards-find-recompetes/)). The signal *inventory* is the useful part: every input except CPARS is public, and we already pull half of them.

---

## 2. Data-source verification (provenance rule applied)

| Source | Public? | Access | Verdict |
|---|---|---|---|
| **CPARS ratings** | **No — confirmed.** Marked source selection information; visible only to government and the rated contractor itself; not releasable under FOIA (FAR 42.1503(d)) | n/a | **Skip as a direct source.** A client can hand us *their own* CPARS — usable as `[CLIENT PROVIDES]`, never for competitors. Fed-Spend's claim that FOIA can obtain competitor CPARS is contradicted by the FAR text; do not repeat it. ([FAR 42.1503](https://www.acquisition.gov/far/42.1503); [Watson](https://blog.theodorewatson.com/cpars-ratings-fapiis-past-performance-and-contractor-integrity-data-what-every-federal-government-contractor-needs-to-know-about-cpars/)) |
| **FAPIIS → SAM.gov Responsibility/Qualification records** | **Yes** (signed-in SAM.gov account, no role needed) | SAM.gov entity record, R/Q section | **Use.** Public records: terminations for default/for cause/for material failure, non-responsibility determinations, defective pricing, DoD contractor-fault determinations, trafficking, administrative agreements, subcontractor payment issues. The public proxy for "bad CPARS." ([GSA transition note](https://www.thompsongrants.com/editorial-commentary/gsa-transitions-fapiis-to-samgov-establishes-new-rq-site); [FAR 9.104-6](https://www.acquisition.gov/far/9.104-6)) |
| **GAO protest docket + decisions** | **Yes** | gao.gov/legal/bid-protests/search — searchable by protester, agency, solicitation; EPDS docket for active cases | **Use, with stated caveat:** most dismissals (incl. corrective-action dismissals) and withdrawals are never published, so absence of records ≠ absence of protests; published decisions + docket entries are a lower bound. ([GAO search](https://www.gao.gov/legal/bid-protests/search)) |
| **FPDS competition fields** (`extent_competed`, `number_of_offers_received`, fair-opportunity, set-aside type) | **Yes** | In the USASpending award record / same API we already call | **Use.** Turns "who won" into "how contested." ([FPDS Extent Competed](https://www.fpds.gov/help/Extent_Competed.htm); [SamSearch market-research guide](https://samsearch.co/guides/federal-market-research)) |
| **Modification history** (per-award transaction list: mod number, date, amount, description) | **Yes** | USASpending award-detail transactions endpoint, keyless | **Use.** Growth mods/option exercises = healthy incumbent; descopes, corrective mods, bridge extensions = vulnerable; T4D in the record = disqualifying-grade signal. ([Fed-Spend recompete field report](https://fed-spend.com/blog/2026-recompete-reset-bd-field-report)) |
| **USASpending subawards** (FSRS, migrated to SAM.gov Mar 2025) | **Yes** | Same `spending_by_award` endpoint with `"subawards": true`; sub-award fields variant | **Use with caveat:** self-reported by primes above the reporting threshold; known incomplete and duplicate-prone pre-2025; state coverage bounds in the doc. Reveals teaming relationships both directions. ([USASpending About the Data](https://www.usaspending.gov/data/about-the-data-download.pdf); [FSRS/DPC](https://www.acq.osd.mil/asda/dpc/ce/cap/fsrs.html); [GovSpend on subcontracting data](https://govspend.com/blog/federal-subcontracting-data-what-it-tells-us-and-how-to-use-it/)) |
| **Agency procurement forecasts** | **Yes** | [acquisition.gov/procurement-forecasts](https://www.acquisition.gov/procurement-forecasts) directory; **VA: VetBiz Forecast of Contracting Opportunities** ([vetbiz.va.gov/forecast](https://www.vetbiz.va.gov/forecast/)) | **Use.** VA's forecast is the single most relevant given our VA concentration; HHS/Interior/USDA/DHS also publish thousands of line items. Planning data, not commitments — say so. |
| **GSA CALC+ / buy.gsa.gov pricing tools** | **Yes** | buy.gsa.gov Quick Rate / CALC — awarded ceiling labor rates across GSA/VA schedule contracts, filterable by education/experience/size/clearance | **Use for services NAICS** (541xxx) pricing calibration; not applicable to construction (236220). ([CALC](https://calc.gsa.gov/about/); [buy.gsa.gov pricing](https://buy.gsa.gov/pricing/qr/mas)) |
| **IDV/vehicle structure** (parent IDV on orders, vehicle type) | **Yes** | Already in the award rows we pull (`Contract Award Type`, parent award fields) | **Use.** We compute award-type mix and stop; the parent-vehicle names are the actionable part. |
| **Key-personnel turnover** | **No** for provenance purposes (LinkedIn ToS bars scraping; no public system of record) | n/a | **Skip.** PLAN-V3 §7 already restricts LinkedIn to manual. |
| **Winning proposals** | No (FOIA Ex. 4) | n/a | **Skip** — already established in PLAN-V3 §6. |
| **Incumbent burn rate** | **Yes** | `Total Outlays` vs. `Award Amount` — already in our pull | **Use** — zero new API surface. |

---

## 3. Market Snapshot — prioritized enhancements

Effort scale: **S** = extend existing pull/template, <½ day agent work to SOP-ify; **M** = new endpoint or scrape + new section, 1–2 days incl. gate coverage; **L** = new capability. Review-time impact assessed against PLAN-V3 §5 (anything raising founder minutes must justify itself).

### Cheap wins — amend the SOP now (§7 has the text)

| # | Enhancement | The insight it buys | Source | Effort | Review-time impact |
|---|---|---|---|---|---|
| MS-1 | **Competition-history fields on comparable awards.** For the §5 comparable pull and §4 incumbent awards, report `extent_competed`, `number_of_offers_received`, set-aside type; add a roll-up line: "of N comparable awards, x% competed, median offers y, z% single-offer." | Answers "how contested is this market *here*" — distinguishes a real SDVOSB competition from a set-aside that always lands sole-source. Directly strengthens §2 rule-of-two math and §6 contestability. Single-offer prevalence is a known agency-competition red flag ([GAO-10-833](https://www.gao.gov/assets/a308886.html)). | FPDS fields via USASpending (already-called API) | **S** | ~0 — mechanical aggregate, G2-gated like the median |
| MS-2 | **Incumbent health block: modification history + burn rate.** For each named incumbent award: transaction list classified into option-exercises/scope-growth vs. descope/corrective/bridge; outlays÷obligated ratio. Verdict line: "healthy / mixed / vulnerable, per N mods." | The public proxy for CPARS. Scope creep = agency keeps buying more = entrenched; descopes and bridges = beatable. This is the highest-value single upgrade to §4 — it converts "incumbent exists" into "incumbent is(n't) beatable," which is what the client is paying $750 to know. | USASpending transactions endpoint + fields already pulled | **M** | +2–3 min (founder sanity-checks the health verdict) — justified: it feeds scorecard factor 1, the heaviest-weighted signal in every model surveyed (Fed-Spend weights it 28%) |
| MS-3 | **GAO protest screen** on incumbent + top-3 competitors + the solicitation lineage. Report published decisions/docket entries (count, dates, outcomes, links); explicit search-bounds line; explicit caveat that unpublished dismissals are invisible. | Protest history is an incumbent-vulnerability and an agency-behavior signal (a sustain against the activity's prior buy of this requirement predicts re-compete drama). 1 loss/24mo meaningful, 2 strong (practitioner heuristic, cite as such). | [gao.gov protest search](https://www.gao.gov/legal/bid-protests/search) (public; scrape-tier — no API) | **S–M** | ~0 when empty (the usual case); +1–2 min when hits found |
| MS-4 | **Integrity screen (FAPIIS/R-Q)** on incumbent + named competitors: terminations for default/cause, non-responsibility determinations, etc. "No R/Q records" as honest default with bounds. | Rare but decisive: a T4D on the incumbent flips the whole snapshot. Cheap insurance; mirrors our existing exclusions-screen pattern. | SAM.gov entity R/Q section (public, signed-in) | **S** | ~0 — boolean-style, exclusions-screen analog |
| MS-5 | **Agency-forecast cross-reference.** Check the agency's published procurement forecast (VA: VetBiz) for this requirement or its program; report forecast line (est. value, target quarter, anticipated set-aside) or "not in forecast." | Our slice of GovWin's pre-RFP earliness. A forecast entry corroborates timeline + magnitude from an official planning source; absence is itself a signal (unplanned/urgent buy). Also seeds §8 with the *next* recurring opportunity — the upsell hook. | [vetbiz.va.gov/forecast](https://www.vetbiz.va.gov/forecast/); [acquisition.gov directory](https://www.acquisition.gov/procurement-forecasts) for non-VA | **M** (no API; per-agency lookup, VA first) | ~0 — factual cross-ref with cite |
| MS-6 | **Vehicle/IDV analysis.** Name the parent IDVs the comparable dollars flow through (FSS, VA-specific IDIQs, GWACs); state whether the client holds access; flag "vehicle-gated market" where relevant. | The SeaPort-NxG trap (BATCH-NOTES #4) as a *product feature*: if 70% of comparable dollars move through a vehicle the client isn't on, that dominates bid/no-bid regardless of capability. | Parent-award fields already in our rows | **S** | ~0–1 min |

### Premium-tier features (justify a higher-priced rung — see §5)

| # | Feature | Why premium, not $750 | Source | Effort |
|---|---|---|---|---|
| MS-7 | **Teaming/subaward map**: who primes and who subs in this NAICS+agency; incumbent's sub network; ranked teaming-partner candidates for the client (firms with relevant subs experience, complementary certs) | Real analysis on incomplete self-reported data → needs judgment + caveating; actionable output (call these 3 firms) reads as advice | USASpending subawards (`"subawards": true`) | **M** |
| MS-8 | **Hot buttons, win themes, ghost themes** distilled from SOW language + incumbent-weakness evidence (MS-2/3/4 outputs): 3–5 customer hot buttons with SOW quotes; 2–3 draft win themes; ghosting angles tied to cited weaknesses | This is Shipley capture-plan content — every line is a judgment call the founder must own; est. +15–25 min review. Exactly what a four-figure capture consultant sells | SOW text (have) + new blocks | **M** |
| MS-9 | **Weighted pWin score** (0–100) replacing/augmenting the ▲/●/▼ scorecard, with published weights and per-component cites, renormalizing on missing signals | A quoted number invites reliance; needs calibration history we won't have for months (Fed-Spend logs outcomes to recalibrate). Keep ▲/●/▼ at $750; offer the number at the capture tier with a "directional, uncalibrated" label | All MS-1..6 signals | **M–L** |
| MS-10 | **Labor-rate calibration** for services NAICS: CALC+ awarded-rate bands for the labor categories the SOW implies | Approaches price-to-win consulting → liability-adjacent (SOP G4 already bans price recommendations); premium tier with the same calibration-only framing | [buy.gsa.gov CALC+](https://buy.gsa.gov/pricing/qr/mas) | **M** |
| MS-11 | **"Who buys this here"** — contracting-officer names on comparable awards at the activity | Legit public signal (FPDS record), but people-data is sensitive to get wrong and stale; premium, human-checked | FPDS/USASpending CO fields | **S** |

### Skip (not derivable from public data — do not fake with weaker proxies)

- **Competitor CPARS ratings** (FAR 42.1503(d): source-selection information, FOIA-exempt). MS-2/3/4 are the honest proxies.
- **Key-personnel turnover / program-office org charts / relationship maps** (Leadership Connect's product; no public system of record; LinkedIn ToS).
- **Analyst-narrated program gossip** (GovWin's "latest analyst update" from agency conversations — we have no analyst corps and shouldn't pretend).
- **Winning proposal content** (FOIA Ex. 4; already settled in PLAN-V3).

## 4. Sources Sought Response — prioritized enhancements

The response's only job (SOP §0.1) is making the CO's set-aside memo easy to write; almost all premium intelligence belongs in the Snapshot, not this document. Three cheap wins and one editing rule:

| # | Enhancement | The insight it buys | Source | Effort | Review-time impact |
|---|---|---|---|---|---|
| SS-1 | **Activity-precedent sentence** in Interest & Intent: "«Activity» has awarded N SDVOSB set-aside actions under NAICS «code» in the last 3 FYs (e.g., «contract», «$», permalink)." Omit when N=0. | Hands the CO precedent for the set-aside determination from their own shop — the strongest possible "your memo writes itself" evidence. No public guidance tells firms to do this; extends our wedge. | USASpending pull we already run for Snapshots (set-aside field) | **S** | ~0 — one G2-gated sentence |
| SS-2 | **Vehicle-holdings line** in company identification: relevant FSS/MAC/IDIQ contracts the firm holds, with contract numbers. | Sources sought notices routinely ask about vehicles; COs use it to pick the acquisition route. Derivable from the firm's own award history (parent IDVs) + `[CLIENT PROVIDES]` confirmation. | S3 firm history (parent-award fields) + intake | **S** | ~0 |
| SS-3 | **Hot-button vocabulary rule** (drafting rule, not a section): the capability narrative must reuse the notice/SOW's own priority terms (their compliance vocabulary — e.g. EHRM-SPL, infection control, phasing) verbatim where true. Add to §2.3 drafting guidance + a G1 soft check (top-5 SOW noun-phrases appear in the response where applicable). | Shipley customer-focus discipline applied at the document level; costs nothing, measurably improves how the response reads to the CO scanning for capability match. | SOW text already extracted | **S** | ~0 |
| SS-4 *(judgment-gated)* | **Rule-of-two awareness sentence**: optionally note that ≥2 certified SDVOSBs with relevant completed work exist (client among them), citing the SBS+USASpending join. | Directly feeds the two-prong test. But naming/attesting to competitors' capability from a respondent's mouth is a strategic call (it invites competition to help force the set-aside — right answer when the alternative is full-and-open or sole-source-to-other, wrong when client could be the sole source). | Snapshot §2 data | **S** | +1 min — founder decides per order; template carries both variants |

**Premium for responses:** none recommended. The response is priced on compliance + evidence discipline; intelligence upsells belong in the Snapshot/capture rungs. **Skip:** competitor ghosting inside a sources sought response (inappropriate in a market-research reply and would read as marketing — a §0.1 discount trigger).

---

## 5. Product-ladder implication: a "Capture Brief" rung

MS-7 through MS-11 cohere into a third product between Snapshot and red-team — effectively a Shipley capture-plan starter kit built on our provenance discipline: everything in the Snapshot **plus** incumbent teaming map, hot buttons/win themes/ghost themes with SOW quotes, uncalibrated pWin with per-component cites, and (services) CALC+ rate bands. Comparable analyst-grade content is what GovWin sells at $29K/yr average and capture consultants sell at four figures per pursuit. Estimated founder review 45–60 min → at the ~$1,000/founder-review-hour rule, price **$1,500–2,500**, matching the red-team's slot economics and completing the ladder's middle. Not part of this SOP amendment; flagged for PLAN-V4 consideration.

---

## 6. What this does to review time (PLAN-V3 §5 check)

Cheap wins net effect: Snapshot review target moves from 20–30 min to an estimated **22–33 min** (MS-2's +2–3 min is the only real add; MS-1/4/5/6 are gate-verified mechanical lines the founder skims). Response target unchanged at 10–15 min (SS-4 adds a per-order decision only when invoked). Both remain inside the $1,000/review-hour rule at current prices — the Snapshot's effective rate at 33 min is ~$1,360/hr. Stopwatch data from the next batch should confirm; if MS-2 review runs over, its verdict line (not its data) is the first thing to cut.

---

## 7. SOP amendment text (cheap wins — proposed revision, pending Mike's approval)

> Apply to `SOP-DELIVERABLES.md` as a dated revision. New text verbatim below; unchanged text elided with […].

**7.1 — §1.1 data-source table, append rows:**

```
| S6 | **USASpending award detail / transactions** (free, keyless) | `GET /api/v2/awards/<generated_internal_id>/` + `/api/v2/transactions/` by award | Competition fields, modification history, burn rate, parent IDV | `extent_competed`, `number_of_offers_received`, `type_of_set_aside`, transaction list (mod #, date, amount, description), `total_outlays` vs obligated, parent award id/name |
| S7 | **GAO bid-protest search** (public; scrape-tier, no API) | gao.gov/legal/bid-protests/search by protester name / agency / solicitation number | Protest screen on incumbents, competitors, and the requirement's lineage | B-number, parties, date, disposition, decision link. **Caveat in every use: most dismissals and withdrawals are never published — findings are a lower bound** |
| S8 | **SAM.gov Responsibility/Qualification (formerly FAPIIS)** (public with signed-in SAM account) | SAM.gov entity record → Responsibility/Qualification section | Integrity screen: terminations for default/cause, non-responsibility determinations, defective pricing, admin agreements | record type, date, agency |
| S9 | **Agency procurement forecasts** (public planning data) | VA: vetbiz.va.gov/forecast; other agencies via acquisition.gov/procurement-forecasts directory | Pre-RFP corroboration: forecast line for the requirement/program | est. value band, target FY/quarter, anticipated set-aside. **Always caveated: planning data, not a commitment** |
```

**7.2 — §3.1 inputs, append:**

```
6. **Award-detail enrichment** (S6): for every incumbent-candidate award and the top-N comparable awards,
   fetch award detail + transactions → data/award_detail_<piid>.json, data/transactions_<piid>.json.
7. **Protest screen** (S7): search GAO by (a) incumbent + top-3 competitor firm names, (b) the predecessor
   solicitation number if identified → data/gao_protests.json (empty result = record the search terms + date).
8. **Integrity screen** (S8): R/Q section for incumbent + named competitors → data/rq_screen.json.
9. **Forecast cross-ref** (S9): agency forecast queried for the requirement/program keywords + NAICS →
   data/forecast_check.json (hit or bounded miss).
```

**7.3 — §3.3 template changes:**

- §3.3 **Section 2 (rule-of-two math)**, append to "Must contain": *"Competition-history roll-up from the comparable pull: % competed vs. sole-source, median `number_of_offers_received`, % single-offer awards, set-aside-type mix (S6). State what the activity's own competition behavior implies for how this buy will be run."*
- §3.3 **Section 4 (incumbent analysis)**, append: *"Incumbent health block per named incumbent award: modification count and classification (option-exercise / scope-growth / descope / corrective / bridge, from transaction descriptions), burn rate (total_outlays ÷ obligated, with both figures), and a one-line health verdict (healthy / mixed / vulnerable) tied to the classified mods. Protest-screen result (S7) and R/Q-screen result (S8) with links or bounded-empty lines. A termination for default/cause found in R/Q is always surfaced in the section lede."*
- §3.3 **Section 5 (pricing history)**, append: *"Award-type/vehicle detail: parent IDVs carrying the comparable dollars, share of dollars through each, and whether the client holds access (client history parent-award join + [CLIENT PROVIDES] confirmation). Flag vehicle-gated markets explicitly."*
- §3.3 **Section 6 (contestability signals)**, replace the "Incumbent weakness" row's evidence spec with: *"mod-history classification + burn rate + protest screen + R/Q screen (S6–S8) — cite the specific rows; 'none found' requires the §3.4 G3 bounds statement."*
- §3.3 **Section 8 (recommended actions)**, append: *"Forecast line (S9): if the requirement or successor appears in the agency forecast, list it with target quarter as a follow-on watch item; if absent, note the absence and its implication (unplanned/urgent buy)."*

**7.4 — §3.4 gates:**

- **G2 Provenance**, append: *"Mod classifications must trace to transaction descriptions in `data/transactions_*.json`; burn-rate ratios must recompute from the two cited figures. Forecast values cite the forecast entry (S9) with retrieval date."*
- **G3 Scope honesty**, append: *"Protest and R/Q 'none found' claims state search terms, screens run, and retrieval date, plus the unpublished-dismissals caveat for GAO results. Health verdicts (healthy/mixed/vulnerable) must be supported by ≥2 classified data points or downgraded to 'insufficient signal.' CPARS is never cited, implied, or estimated — competitor performance claims rest only on S6–S8 evidence."*
- **G5 Freshness**, append: *"Forecast and R/Q retrievals within 14 days of delivery (slower-moving sources; notice-tied sources keep the 5-day rule)."*

**7.5 — §2.3 response template changes:**

- **Company identification** row, append: *"Contract-vehicle holdings relevant to the anticipated acquisition route (FSS/MAC/IDIQ contract numbers from the firm's award history parent-IDV fields; confirm via intake — [CLIENT PROVIDES: vehicle list confirmation])."*
- **Interest & Intent** row, replace "(3) set-aside support" with: *"(3) set-aside support — 'This response is offered to support a[n] «SDVOSB» set-aside determination under «authority».' (4) activity precedent, when N>0 — '«Activity» has awarded «N» SDVOSB set-aside actions under NAICS «code» in the last three fiscal years, including «contract» ($«amt», «permalink»).' (5) OPTIONAL, founder-gated per order: rule-of-two awareness — 'Public certification and award records indicate at least two certified SDVOSBs, including «Firm», have completed same-or-similar work for «agency».' Sentence 5 ships only when the founder approves it in the delivery-note review (§2.5 judgment item)."*
- Add to §2.3 drafting guidance (after the length rule): *"Hot-button vocabulary rule: where truthful, capability narratives reuse the notice/SOW's own priority terminology verbatim (program names, standards, constraint phrases). G1 soft check: the five most frequent distinctive noun-phrases in the SOW each appear in the response or are flagged N/A in the compliance matrix."*
- **§2.5 Human judgment**, append item: *"6. Rule-of-two awareness sentence (Interest & Intent #5) — include or omit per order; default omit."*
- **§2.4 G3**, append: *"G3c: activity-precedent sentence present when the Snapshot-style set-aside pull shows N>0 for this activity+NAICS (data must be in data/); absent otherwise."*

**7.6 — §1.2 citation format, append:**

```
- **Protest records:** GAO B-number + decision/docket URL — e.g. `B-416021.2 · gao.gov/products/b-416021.2`.
- **R/Q (FAPIIS) records:** `(Source: SAM.gov Responsibility/Qualification record for <UEI>, retrieved YYYY-MM-DD)`;
  empty screens follow the exclusions-line pattern.
- **Forecast entries:** `(«Agency» Forecast of Contracting Opportunities, entry «id/title», retrieved YYYY-MM-DD — planning data)`.
- **Dollar figures:** truncate (floor) to whole dollars so the document figure is a verbatim prefix of the source
  value (BATCH-NOTES rule, adopted).
```

---

## 8. Sources

Premium products: [Deltek — AI & UX in GovWin IQ](https://www.deltek.com/resources/articles/govwin-ai-ux-innovation/) · [Deltek — Smart Fit Score](https://www.deltek.com/resources/articles/machine-learning-govwin-iq-smart-fit-score/) · [Deltek — analyst + AI](https://www.deltek.com/resources/articles/artificial-intelligence-business-development-govwin-iq/) · [Civic IQ — GovWin pricing 2026](https://civiciq.com/blog/govwin-iq-pricing-2026) · [Fed-Spend — GovWin pricing/alternatives](https://fed-spend.com/blog/govwin-iq-pricing-2026-deltek-cost-alternatives) · [ITQlick — GovWin pricing](https://www.itqlick.com/govwin-iq/pricing) · [BGOV](https://about.bgov.com/) · [Fed-Spend — BGOV competitors](https://fed-spend.com/blog/bloomberg-government-competitors-alternatives) · [Civic IQ — platform comparison](https://blogs.civiciq.com/2026/04/14/best-government-contract-tracking-software-for-2026-6-platforms-compared/) · [Leadership Connect](https://leadershipconnect.io/) · [FEDLINK vendor entry](https://www.loc.gov/flicc/contracts/VendorDirectory/le_leadershipconnectR.html).

Capture methodology: [Shipley Capture Guide](https://www.shipleywins.com/tools-and-guidebooks/shipley-capture-guide) · [Shipley — capture planning](https://www.shipleywins.com/blogs/capture-planning) · [GovEagle — Shipley process](https://www.goveagle.com/blog/complete-shipley-process-guide) · [Octant — capture plan](https://octant.com/a-capture-plan-is-a-plan-to-win/) · [Fed-Spend — pWin Verdict Engine (vendor methodology)](https://fed-spend.com/blog/pwin-verdict-engine-win-probability-guide-2026) · [Fed-Spend — recompete strategy](https://fed-spend.com/blog/recompete-strategy-guide) · [Fed-Spend — 2026 recompete field report](https://fed-spend.com/blog/2026-recompete-reset-bd-field-report) · [Sweetspot — finding recompetes](https://www.sweetspot.so/articles/government-contract-awards-find-recompetes/).

Data-source verification: [FAR 42.1503](https://www.acquisition.gov/far/42.1503) (CPARS non-public, FOIA-exempt) · [Watson — CPARS/FAPIIS](https://blog.theodorewatson.com/cpars-ratings-fapiis-past-performance-and-contractor-integrity-data-what-every-federal-government-contractor-needs-to-know-about-cpars/) · [FAR 9.104-6](https://www.acquisition.gov/far/9.104-6) · [Thompson Grants — FAPIIS→SAM R/Q](https://www.thompsongrants.com/editorial-commentary/gsa-transitions-fapiis-to-samgov-establishes-new-rq-site) · [GAO protest search](https://www.gao.gov/legal/bid-protests/search) · [FPDS — Extent Competed](https://www.fpds.gov/help/Extent_Competed.htm) · [GAO-10-833 — single-offer competition](https://www.gao.gov/assets/a308886.html) · [SamSearch — federal market research](https://samsearch.co/guides/federal-market-research) · [USASpending — About the Data](https://www.usaspending.gov/data/about-the-data-download.pdf) · [DPC — FSRS](https://www.acq.osd.mil/asda/dpc/ce/cap/fsrs.html) · [GovSpend — subcontracting data](https://govspend.com/blog/federal-subcontracting-data-what-it-tells-us-and-how-to-use-it/) · [acquisition.gov — procurement forecasts](https://www.acquisition.gov/procurement-forecasts) · [VA VetBiz forecast](https://www.vetbiz.va.gov/forecast/) · [GSA CALC](https://calc.gsa.gov/about/) · [buy.gsa.gov pricing](https://buy.gsa.gov/pricing/qr/mas).

Internal: `SOP-DELIVERABLES.md` (2026-08-22 draft) · `PLAN-V3.md` · `sample-set/BATCH-NOTES.md` + 10 deliverables · `sample-set/541519-snapshot/SNAPSHOT.md` (baseline exemplar).
