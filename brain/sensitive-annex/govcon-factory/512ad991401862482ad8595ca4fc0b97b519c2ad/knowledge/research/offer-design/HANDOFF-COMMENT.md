# Handoff note for the code session

This research session had no `gh` binary and no GitHub token, so it could not open the issue or post
the coordination comment itself. Open an issue on `redtrades/govcon-factory` titled something like
**"Offer design: what fills the $500-subscription-to-four-figure-consulting gap"**, paste the block
below into it, then commit the new file. Nothing else in the tree was touched, and nothing was
committed.

**New, untracked:** `knowledge/research/offer-design/REPORT.md` (plus this note).

---

```
Offer-design research pass complete (read-only). New file: knowledge/research/offer-design/REPORT.md.
Not committed; this session had no gh/token. Please commit as-is or with a squash message like
"Add offer-design research (price ladder, ranked adjacent products, three low-four-figure designs)".

Commissioned question: if per-deliverable proposal starters alone cannot sustain the business, what
else can the same public data and the same factory produce that people demonstrably pay four figures
for? Mike asked for (a) a low-four-figure price point, (b) an offer strong enough to justify it,
(c) lead magnets that pull the right buyer.

RECOMMENDATION IN ONE LINE
Test a fixed-price $1,500 "Recompete Pursuit File": one named federal contract that must recompete in
the next 6 to 18 months, everything a small firm needs to decide whether to chase it, built only from
public records, gated and cited like the existing samples, with a gaps page and an explicit
"do not chase this one" outcome. Design C in the report.

THE SIX FINDINGS THAT CHANGE THE PLAN

1. The "report built from public data" category collapsed in price, downward, since the last pass.
   Fed-Spend sells AI competitive analysis, pricing benchmarks and recompete predictions at $49/mo
   and $199/mo with a free tier. GovCon API sells a recompete watchlist, teaming finder, price
   benchmarks, protest data and contracting-office intelligence at $19/mo and $79/mo. Note for the
   repo: govconapi Pro was $39/mo in research/govconapi-exploration/REPORT.md on 2026-08-22 and is
   $79/mo as of 2026-08-26. That price line in the exploration report is stale. Consequence:
   no standalone information product from this data is worth four figures. Ever.

2. A competitor already claims our positioning and has priced it. PrimeRFP SCOUT's pricing page says
   verbatim: "HigherGov's $500/year buys the dataset. Tactics buys the decision." Tactics $290/mo
   ($2,958/yr), Strategic $670/mo ($6,030/yr), Strategic+ $1,290/mo ($11,610/yr) which includes
   "Discovery Reports on demand, full per-opportunity reports (25/mo)". They also run a $90-for-90-days
   pilot and a $29/mo MCP tier. This is the most important competitive fact in the file. "We sell the
   decision, not the data" is no longer an available sentence.

3. Observed four-figure money in this market goes to four things, none of them a report: filings that
   produce a durable asset (Advance GSA publishes a $7,600 flat fee for a GSA Schedule package;
   Winvale says $20-25K full service and $15-30K/yr maintenance; ez8a lists $1,600 for HUBZone),
   bundled data-plus-workflow subscriptions (EZGovOpps $2,695 / $3,695 / $4,695 / from $5,995
   annually, plus $299 setup, annual commitment, published no-refund policy), blocks of a named
   expert's hours (Bidspeed $1,095 / $1,595 / $2,995), and training (weakest evidence, "valued at"
   marketing numbers).

4. THE GAP IS REAL AND SPECIFIC. Nothing observed between $995 and $2,995 is a fixed-price,
   done-for-you, per-pursuit deliverable requiring nothing from the buyer. The band is subscriptions,
   hours and courses. The nearest thing is Bidspeed's $995 Custom Market Research Package, and its own
   product page lists what the customer must supply: "Past experience, Past performance summaries,
   Company website, Company logo (optional), Teaming partners (if applicable)." brand/customer.md's
   zero-input asymmetry is confirmed on a competitor's checkout page.

5. THE PURSUIT WORTH FOUR FIGURES IS A RECOMPETE, NOT A SOURCES SOUGHT. A four-figure price and an
   eight-day window are incompatible; every observed four-figure purchase is made with time to think.
   A recompete has a 6-to-18-month influence window, a named incumbent, a published contract value,
   and an offer count that says whether it is contestable. This also breaks feasibility F1's binding
   constraint: the product stops being rationed by SAM's posting calendar. PrimeRFP counts 10,452
   recompetes in a 14-month window at a $10M floor, ~$1.28T, and our buyer lives below that floor.

6. TWO FACT-SHAPED ASSETS NOBODY PACKAGES AS A DELIVERABLE, both vendor-measured and both to be
   re-derived in our six NAICS before entering copy:
   - Certification lapse: roughly 3,300 active contracts entering their recompete window in 18 months
     carry an incumbent whose SBA set-aside certification lapses before the contract ends, out of
     about 16,300 whose set-aside maps to a specific SBA program. That is a takeover list. Our G3
     gate already knows how to read cert exit dates. Fires only on a dated exit; absence of a record
     produces no signal, because roughly half of firms have no profile.
   - Contestability: 37% of NAICS 541512 contracts labeled "full and open competition" drew exactly
     one bidder; 46% for "full and open after exclusion of sources." GAO independently found ~13% of
     obligations FY05-09 were single-offer and ~18% of sampled contracts were miscoded on competition
     (GAO-10-833). A deliverable whose job is to say "this says competed but it is wired, do not spend
     your evening on it" is the paid version of the repo's own no-sale rule, and it is the refusal an
     engagement-measured subscription cannot profitably make.

RANKED OPPORTUNITY LIST (full table in section 3, with pain evidence, buyer, price comparable, build
and fastest test for each)
  1 Recompete pursuit file        6 Pricing benchmark exhibit (ship inside 1 and 4, never standalone)
  2 Cert-lapse takeover list      7 Teaming map (commoditized at $79/mo, ship as a section)
  3 Agency beachhead file         8 PE/corp-dev diligence (competitor already at $90; wrong buyer now)
  4 Bid/no-bid decision file      9-11 Capability statements, standalone benchmark reports, data feed: no
  5 White-label capture desk

The pattern: every candidate that is a fact you can look up has a sub-$100/mo substitute shipping
today. Every candidate that is a decision someone must own has no substitute under $995. The dividing
line is not the data, it is whether a human is accountable for the conclusion.

WHO ELSE BUYS (section 4)
- Proposal consultants and boutique capture shops, as a white-label supplier: most reachable of the
  five. PrimeRFP maintains a dedicated "Consultants & capture shops" door, so the segment is real.
  Sequence the referral term before any wholesale term; a soured wholesale relationship costs a
  channel-2 referral partner.
- Primes seeking small-business partners: obligation is real (FAR 19.702, 52.219-9 at $750K/$1.5M),
  but the need is a warm vetted partner, the list version costs $79/mo, and supplying both sides is
  feasibility F2's conflict problem in a new costume. Defer, unchanged from the GTM report.
- PE / corp dev: real money, wrong fit now. PrimeRFP already runs a diligence door with a $90 entry.
  Revisit only if the recompete file works, because the rollups are the same rollups.
- Associations / APEX / SBDC: near-zero direct spend, real indirect. Govology's model (sell at ~$75
  to individuals, license to centers who give it away) is the observable precedent. Give them the
  free report; do not build a paid product for them.
- Cert-prep firms: four-figure spend is documented but it is a filing business, with an
  eligibility-advice component and mostly client-supplied facts. Sell to them as a referral source.

LEAD MAGNETS (section 6). Honest framing: no published conversion data exists for this niche.
Cross-industry benchmark, vendor-published: generic ebooks ~3%, free scoped audit 5-15% opt-in and
wins on booked-call quality. Three to build, each feeding the recompete offer:
  1. The recompete cliff for one NAICS. Aggregate counts public, named rows gated behind a UEI. This
     is PrimeRFP's shortlist mechanic executed below their $10M floor, which is where our buyer is.
  2. The one-contract free read. Buyer names a PIID or an incumbent; gets back five citable facts,
     including the official competition flag printed next to the real offer count. That single screen
     is the product's whole argument.
  3. The "wired or contestable" share by NAICS, aggregate, linkable, citing GAO-10-833 alongside our
     own measurement so the claim does not rest on one vendor's blog.
Do not build another ebook or Sources Sought how-to guide. SamSearch owns that SERP (feasibility F3).

THE TEST, CHEAPEST DISCONFIRMING EVIDENCE FIRST (section 8). No dependency on the unresolved
contact-source counsel question until step 4.
  1. Count the population across the six NAICS, agent time only. Kill if fewer than ~100 contracts
     survive with a usable offer count.
  2. Build one file end to end and time the founder review. Kill/reprice if it does not fit the
     ~20-minute unit rule by build 2. Do not paper over it (PLAN-V5 section 7).
  3. Put it next to Fed-Spend's free tier and PrimeRFP's $90 pilot. If a non-expert cannot name the
     difference in 30 seconds, this is GTM assumption 4 arriving in a new product.
  4. Sell three at $1,500 prepaid. Kill at 0 paid after 40 qualified exposures, twice.
  5. Ship the free per-NAICS recompete-cliff magnet from step 1's output.
Number to instrument from file one: what fraction of buyers who receive a "do not chase this one"
verdict come back for a second file. If the refusal produces repeat business the positioning holds.
If it produces silence, we are paying for a benefit that does not exist.

REPO ACTIONS THIS FLAGS, NONE TAKEN HERE
- STALE PRICE: research/govconapi-exploration/REPORT.md section 5 quotes govconapi Pro at $39/mo.
  It is $79/mo as of 2026-08-26. Fix when that file is next touched.
- Three vendor-measured statistics (37%/46% single-bidder, ~3,300 cert-lapse, ~1-in-20 subaward
  coverage) must be re-derived from USASpending in our own six NAICS before any of them enters a
  customer-facing document. That re-derivation is step 1 of the test, so it is already scheduled.
- Two single-source claims may not enter copy as written: the r/govcon quotation ("treat recompete
  dates as your real watch list, not SAM") which is secondhand from a vendor page, and "recompetes
  are 60-70% of annual obligations by dollar value."
- govmates.com did not resolve to a govcon site on 2026-08-26 (returned unrelated non-English content
  with a canonical tag pointing elsewhere). Excluded from the analysis rather than speculated about.
  Worth one manual check if the teaming segment is ever revisited.

LIMITS, same wall as the last two passes: Reddit is on the fetch blocklist and the search index
returned no thread bodies, LinkedIn was unreachable, and no keyword-volume or lead-magnet conversion
data exists for this niche. All pricing in the report is list price, never transaction price. If
community sentiment matters, it needs a human with a browser, not another agent pass.
```
