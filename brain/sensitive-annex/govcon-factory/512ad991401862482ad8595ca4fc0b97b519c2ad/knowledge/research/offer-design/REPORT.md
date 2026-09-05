# Offer design: what fills the gap between a $500/yr subscription and four-figure consulting

2026-08-26. Market-demand research commissioned by Mike. Read-only pass; nothing else in this repo
was changed by this file.

**What this extends, so it does not repeat.**
`knowledge/research/gtm-playbook/REPORT.md` (Parts I and II) established the channel ranking, the
close mechanics, the SAM.gov terms posture, and the conclusion that survives here unchanged: SAM
gives away the notification layer for free, HigherGov ships a one-click Sources Sought draft at
$500/yr, GovTribe sells event-triggered AI runs, and the only differentiation left is per-claim
provenance, fail-closed gates, a named accountable human, and the willingness to say there is
nothing worth bidding. `research/feasibility-review/REPORT.md` established the notice-supply ceiling
(~250 to 400 sellable notice-moments/yr in six NAICS, F1) and the conflict, liability, and key-man
problems. `research/proposal-writing/` established the proposal rubric and the winacontract content
machine. `brand/` fixes the vocabulary and the claims we may not make.

This file answers a different question. Not "how do we sell the $699 packet," but **what else the
same public data and the same factory can produce that this market demonstrably pays $1,000 to
$3,000 for**, and which lead magnets pull that buyer.

**Evidence labels, same as the GTM file.**

- **Observed.** Retrieved from the named page on 2026-08-26, quoted or transcribed.
- **Vendor-published.** A marketing page or blog from a party with an interest in the number.
  Direction, not decimals.
- **Repo.** Already established in this repository, cited rather than re-derived.
- **Inference.** My reading. Mike may reject it.

---

## 0. Bottom line

Seven findings, in the order they change what Mike does.

1. **The "report built from public data" category has collapsed in price since the last research
   pass, and it collapsed downward.** Fed-Spend sells AI competitive analysis, pricing benchmarks
   and recompete predictions at **$49/mo Researcher and $199/mo Professional**, with a free tier of
   10 searches per month ([Fed-Spend comparison post](https://fed-spend.com/blog/govtribe-vs-govwin-vs-fed-spend-comparison),
   observed). GovCon API sells a recompete watchlist, teaming partner finder, price benchmarks, bid
   protest data and contracting office intelligence at **$19/mo Developer and $79/mo Pro**
   ([GovCon API teaming page](https://govconapi.com/teaming-partner-api),
   [recompete watchlist](https://govconapi.com/recompete-watchlist), observed). The repo's own
   exploration recorded that Pro was **$39/mo** four days earlier (repo:
   `research/govconapi-exploration/REPORT.md`, 2026-08-22), so the ladder is moving, but the band is
   two orders of magnitude below the target price. **No standalone information product from this
   data is worth four figures.** Anything Mike sells at $1,000 to $3,000 must be a decision, a
   filing, or an accountability transfer, with the data as an input rather than the product.
2. **A direct competitor has already claimed the exact positioning Mike is reaching for, and priced
   it.** PrimeRFP SCOUT's pricing page says, verbatim: *"HigherGov's $500/year buys the dataset.
   Tactics buys the decision."* Tactics is **$290/mo, $2,958/yr**; Strategic is **$670/mo,
   $6,030/yr**; Strategic+ is **$1,290/mo, $11,610/yr**, and Strategic+ includes *"Discovery Reports
   on demand, full per-opportunity reports (25/mo)"*
   ([PrimeRFP pricing](https://primerfp.com/pricing), observed). They also run a **$90 for 90 days**
   pilot and a **$29/mo MCP** tier. This is the single most important competitive fact in this file.
   It does not kill the thesis, but it means "we sell the decision, not the data" is no longer an
   available sentence, and the surviving difference has to be the *form* of the deliverable and who
   is accountable for it, not the claim.
3. **The observed four-figure money in this market goes to four things, and none of them is a
   report.** Ranked by how well documented the price is: applications that produce a durable asset
   (**$7,600 flat** for a GSA Schedule full-service package at Advance GSA, observed;
   **$20,000 to $25,000** at Winvale, vendor-published; **$1,600** for a HUBZone application
   package at ez8a, vendor-published), bundled data-plus-workflow subscriptions (**$2,695 to
   $5,995/yr** at EZGovOpps, observed), blocks of a named expert's hours (**$1,095 / $1,595 /
   $2,995** at Bidspeed, observed), and training or coaching programs (**$1,997 to $2,997** headline
   values, vendor-published, and these are "valued at" marketing numbers rather than transaction
   prices, so treat them as the weakest evidence here).
4. **The gap in the market is real and specific.** Nothing observed in the $1,000 to $3,000 band is
   a **fixed-price, done-for-you, per-pursuit deliverable**. The band contains subscriptions, hours,
   and courses. The nearest per-deliverable product is Bidspeed's **$995 Custom Market Research
   Package**, and its own product page lists what the customer must supply: *"Past experience, Past
   performance summaries, Company website, Company logo (optional), Teaming partners (if
   applicable)"* ([Bidspeed product page](https://www.bidspeed.com/products/custom-market-research-package),
   observed). That is the zero-input asymmetry `brand/customer.md` already identified, sitting in
   plain sight on a competitor's checkout page.
5. **The pursuit worth four figures is a recompete, not a Sources Sought.** A Sources Sought has a
   median of 8 days left and a quarter have 3 or fewer (repo, n=1,029), which caps both the price
   and the sales cycle. A recompete has a 6 to 18 month influence window, a named incumbent, a
   dollar value on the public record, and an offer count that says whether it is contestable.
   PrimeRFP counts **10,452 contracts recompeting in a 14-month window at a $10M floor, roughly
   $1.28T** ([PrimeRFP Recompete Radar](https://primerfp.com/intel/recompete-radar), observed,
   and that floor is far above our buyer's band, so the small-contract count is larger still).
   Moving the product from the notice to the recompete removes the F1 notice-supply ceiling as the
   binding constraint, which is the most consequential structural change in this file.
6. **There is one fact-shaped asset in this data that nobody has packaged as a deliverable, and it
   creates a genuine takeover list.** GovCon API's recompete page reports that **roughly 3,300
   active federal contracts entering their recompete window in the next 18 months carry an incumbent
   whose SBA set-aside certification lapses before the contract ends, out of about 16,300 whose
   set-aside maps to a specific SBA program** ([GovCon API](https://govconapi.com/recompete-watchlist),
   observed, vendor's own measurement). They sell it as an API field. Nobody sells it as "here is
   the contract you can take, here is why the incumbent may not be able to bid, here is the office
   and the person." That is a decision with money attached, it is derivable from data the factory
   already pulls, and the repo's G3 certification-window logic is the exact gate that already knows
   how to read cert exit dates.
7. **The most underweighted competitive fact: the offer count contradicts the competition flag, and
   that gap is a sellable finding.** Measured on NAICS 541512, **37% of contracts labeled "full and
   open competition" drew exactly one bidder, and 46% of "full and open after exclusion of sources"
   drew one** ([GovCon API](https://govconapi.com/recompete-watchlist), observed, vendor's own
   measurement). Independently, GAO found that from FY2005 to FY2009 about **13% of obligations were
   on contracts competed with only one offer**, and that about **18% of the contracts it sampled
   were coded incorrectly** ([GAO-10-833](https://www.gao.gov/products/gao-10-833), observed,
   primary). A deliverable whose job is to tell a small firm "this one says competed but it is
   wired, do not spend your evening on it" is the paid version of the repo's own no-sale rule, and
   it is exactly the refusal a subscription measured on engagement cannot profitably make.

**The recommendation in one line.** Test a **fixed-price, per-recompete pursuit file at $1,500**,
sold on one named expiring contract in the buyer's own NAICS, built entirely from public records,
gated and cited like the existing samples, with a gaps page and a stated "do not chase this one"
outcome. Design C below, "Recompete Pursuit File."

---

## 1. What this market actually pays, observed

Every row retrieved 2026-08-26 unless noted. This is the ladder any new offer is priced against.

### 1.1 The information layer, which is now cheap

| Product | Price | Shape | Source |
|---|---|---|---|
| SAM.gov saved-search alerts | $0 | Notification, authoritative | repo (GTM Part II §11.5) |
| GovCon API Developer | $19/mo | Opportunity, contract, subaward, exclusion search | [pricing note on teaming page](https://govconapi.com/teaming-partner-api) |
| Fed-Spend free tier | $0 | 10 searches/mo, full results | [Fed-Spend](https://fed-spend.com/blog/govtribe-vs-govwin-vs-fed-spend-comparison) |
| PrimeRFP MCP Explorer | $29/mo | Classify plus search inside Claude or ChatGPT | [PrimeRFP pricing](https://primerfp.com/pricing) |
| Fed-Spend Researcher | $49/mo | Search, alerts, AI analysis | Fed-Spend, as above |
| GovCon API Pro | $79/mo | Recompete watchlist, teaming finder, contacts, price benchmarks | [GovCon API](https://govconapi.com/recompete-watchlist) |
| PrimeRFP Pilot | $90 for 90 days | Full Tactics access, one payment | [PrimeRFP pricing](https://primerfp.com/pricing) |
| Bidspeed Government Buyers Report | $125 | One-off report | [Bidspeed Marketplace](https://www.bidspeed.com/marketplace) |
| Bidspeed Expiring Contracts Report | $149 | Per-NAICS report | Bidspeed, as above |
| Bidspeed NAICS Procurement Forecast | $149 | Per-NAICS report | Bidspeed, as above |
| Fed-Spend Professional | $199/mo | Unlimited exports, CI reports, benchmarks | Fed-Spend, as above |
| PrimeRFP MCP Pro | $495/mo | Strategic toolset over MCP | [PrimeRFP pricing](https://primerfp.com/pricing) |
| HigherGov Starter | $500/yr | Search, tracking, AI tools | repo (GTM §12) |

**Inference, and it is the load-bearing one.** In four days between the repo's govconapi exploration
(2026-08-22, Pro at $39/mo) and this pass (2026-08-26, Pro at $79/mo), one vendor's price doubled
while another (PrimeRFP) was running a $90-for-90-days pilot and a $29/mo MCP tier. That is a market
in active price discovery at the bottom, not a stable band. Building a four-figure product whose
value is *access to derived facts* means competing with a category that is simultaneously
commoditizing and unstable. Do not enter that fight.

### 1.2 The four-figure layer, which is where the money is

| Product | Price | What justifies it | Source |
|---|---|---|---|
| Bidspeed Custom Market Research Package | $995 | Done-for-you response, but client supplies past performance and teaming | [Bidspeed](https://www.bidspeed.com/products/custom-market-research-package) |
| Bidspeed Build Your Acquisition Engine | $999 | Customized assessment and strategic planning package | [Bidspeed Marketplace](https://www.bidspeed.com/marketplace) |
| Bidspeed 4-hour advisory block | $1,095 | Named advisory team's hours | Bidspeed, as above |
| Bidspeed 8-hour advisory block | $1,595 | Same, more hours | Bidspeed, as above |
| ez8a HUBZone Application Package | $1,600 | A filing that produces a certification | [ez8a](https://www.ez8a.com/hubzone-certification/), vendor-published |
| GovTribe Launch | $1,500/yr | 1 user, 10 active pursuits | repo (GTM §12), vendor docs |
| HigherGov Standard | $2,500/yr | Search plus AI tools, more seats | repo (GTM §12) |
| EZGovOpps Bronze | $2,695/yr plus $299 setup | Analyst-researched opportunity updates, annual commitment, **no refunds** | [EZGovOpps pricing](https://ezgovopps.com/home/pricing/) |
| Bidspeed 16-hour advisory block | $2,995 | Named advisory team's hours | [Bidspeed Marketplace](https://www.bidspeed.com/marketplace) |
| PrimeRFP Tactics | $290/mo, $2,958/yr | "Tactics buys the decision" | [PrimeRFP pricing](https://primerfp.com/pricing) |
| EZGovOpps Silver | $3,695/yr | More credits, subcontract search | EZGovOpps, as above |
| EZGovOpps Gold | $4,695/yr | 3 users, labor pricing, CO purchasing history | EZGovOpps, as above |
| HigherGov Leader | $5,000/yr | Top self-serve tier | repo (GTM §12) |
| EZGovOpps Platinum | from $5,995/yr | 6+ users | EZGovOpps, as above |
| PrimeRFP Strategic | $670/mo, $6,030/yr | Pre-RFP policy signals, teaming, exports | [PrimeRFP pricing](https://primerfp.com/pricing) |
| Advance GSA full-service package | $7,600 flat | A GSA Schedule contract, published flat fee, stated ~100% approval rate 2023 | [Advance GSA](https://www.gsaschedulecontract.com/gsa-full-service-package.html) |
| PrimeRFP Proposability standalone | $720/mo | RFP shredding, compliance matrices | [PrimeRFP pricing](https://primerfp.com/pricing) |
| PrimeRFP Strategic+ | $1,290/mo, $11,610/yr | Protest patterns, PIID dossiers, 25 discovery reports/mo | PrimeRFP, as above |
| Winvale GSA acquisition, full service | $20,000 to $25,000 | Drafting plus authorized negotiator role | [Winvale](https://info.winvale.com/blog/how-much-does-gsa-schedule-consulting-cost), vendor-published |
| Winvale post-award maintenance | $15,000 to $30,000/yr | Compliance and mods, "all you can eat" | Winvale, as above |
| Deltek GovWin IQ | $13,000 to $119,000/yr, average around $29,000 | Analyst-validated pre-RFP leads, relationship intelligence | third-party buyer data, vendor-published |
| Price-to-win study | $20,000 to $300,000+ | Competitor cost modeling on a large program | [OCI](https://ociwins.com/government-proposal-consultants/what-is-the-cost-to-prepare-a-proposal/), vendor-published |

**Three readings of this table.**

- **What is absent is the opportunity.** Between $995 and $2,995 there is no fixed-price,
  done-for-you, per-pursuit deliverable that requires nothing from the buyer. There are hours, there
  are subscriptions, there is one $995 package that requires the client to write their own past
  performance. `brand/offer.md`'s zero-input promise ("Nothing needed from you to start: your
  contracts are public") is the only differentiator in that table that a competitor's own checkout
  page confirms they do not offer.
- **Price tracks irreversibility, not effort.** The $7,600 GSA package and the $1,600 HUBZone
  package are cheap in labor terms compared to a $20,000 Winvale engagement, and they hold their
  price because the output is a filing that either succeeds or does not, and the buyer cannot easily
  redo it. The subscriptions hold their price because they are annual commitments with published
  no-refund terms (EZGovOpps states refunds "are not available for users desiring to break their
  contract before its conclusion"). The reports at $125 to $149 hold nothing.
- **Hours are the price anchor a productized deliverable competes with.** Bidspeed's 4-hour block at
  $1,095 is $274/hr; the 16-hour block at $2,995 is $187/hr. If a factory deliverable is positioned
  as "this replaces N hours of a capture consultant," the honest comparison at the low four figures
  is 4 to 16 hours of a named advisor, and the factory must produce something a competent human
  could not produce in that time. Volume of public-record analysis is exactly that thing.

---

## 2. Pain signals, ranked by evidence of willingness to pay

I could not reach Reddit or LinkedIn with the tools available in this session (the fetch tool
returns a blocklist error for reddit.com, and the search index returned no r/GovernmentContracting
thread bodies). That is a real limit and it is the same limit the two prior research passes hit
(repo: GTM §10, feasibility F1). So this ranking is built on **revealed preference**, which is the
stronger evidence anyway: what vendors charge for, what free institutions run repeatedly, and what
the public record says is at stake.

Ranked from strongest evidence of willingness to pay to weakest.

### 2.1 Rank 1: "I found out too late." The pre-solicitation window

**The pain.** By the time a solicitation posts on SAM, the window in which a small firm could have
shaped it has closed. GovCon API's recompete page quotes the conclusion of a public r/govcon
discussion it links to: *"treat recompete dates as your real watch list, not SAM"* and *"anything
renewing in less than six months is too close to influence"*
([GovCon API, citing r/govcon](https://govconapi.com/recompete-watchlist), observed; the underlying
thread is [here](https://www.reddit.com/r/govcon/comments/1u7g14z/lost_a_bid_we_were_confident_about_found_out_the/)
and I could not open it in this session, so this is a secondhand quotation and should be verified
before it enters customer copy).

**Evidence of spend.** This is the pain that the entire four-figure subscription tier is sold
against. EZGovOpps Gold at $4,695/yr sells "Preforecast Dashboard" and CO purchasing history;
PrimeRFP Strategic at $670/mo sells "Pre-RFP Intelligence" as its headline; GovWin's whole
enterprise premium is analyst-validated pre-RFP leads at an average around $29,000/yr. Three
independent vendors at three price points all monetize the same complaint.

**Size of the prize.** PrimeRFP counts 10,452 recompetes in a 14-month window at a $10M floor,
around $1.28T, DoD 43% of value ([PrimeRFP](https://primerfp.com/intel/recompete-radar), observed).
Recompetes are claimed to be "60 to 70% of annual federal contract obligation by dollar value"
([govprocure](https://govprocure.northwest.net/what-is-recompete-contract.html), vendor-published,
uncorroborated, do not use in copy without a second source).

**Verdict: highest.** This is the pain with the most vendors, the highest prices, and the longest
decision window. It is also the pain our factory is best positioned to serve, because the input is
FPDS period-of-performance data plus SAM notices, both of which the pipeline already reads.

### 2.2 Rank 2: "Is this one even winnable, or is it wired?"

**The pain.** Small firms spend evenings on bids that were never contestable. The evidence that this
is a real and measurable phenomenon rather than folklore is unusually good for this market.
GAO found single-offer awards were about 13% of obligations across FY2005 to FY2009 and that about
18% of sampled contracts were miscoded on competition
([GAO-10-833](https://www.gao.gov/products/gao-10-833), observed, primary). GovCon API's own
measurement on NAICS 541512 puts the modern figure far higher: 37% of "full and open competition"
contracts drew exactly one bidder, 46% for "full and open after exclusion of sources"
([GovCon API](https://govconapi.com/recompete-watchlist), observed, vendor's own measurement, not
independently verified here). Separately, roughly $278B of about $793B in FY2025 obligations were
noncompetitive ([Legis1](https://legis1.com/news/federal-contracts-noncompetitive-one-third-of),
vendor-published, single source).

**Evidence of spend.** PrimeRFP Strategic+ at $1,290/mo sells "Protest Patterns plus Sustain Rates,
go/no-go risk intel." Bidspeed's advisory blocks list "review opportunities for Go/No go" as a use.
Go/no-go is what the hours are bought for.

**Verdict: high, and uniquely aligned with our brand.** `brand/offer.md` already requires us to say
"nothing to buy on this one" below the fill floor. Selling the no-bid as the product, rather than as
the honorable exception, converts an ethical constraint into the value proposition. This is the one
place where the repo's discipline is a commercial advantage rather than a cost.

### 2.3 Rank 3: "I need a certification, a schedule, or a vehicle"

**The pain.** Entry gates. And the willingness to pay here is the best-documented in the entire
market: $7,600 published flat fee for a GSA Schedule package
([Advance GSA](https://www.gsaschedulecontract.com/gsa-full-service-package.html), observed),
$20,000 to $25,000 for full service, $15,000 to $30,000/yr thereafter
([Winvale](https://info.winvale.com/blog/how-much-does-gsa-schedule-consulting-cost),
vendor-published), $1,600 for a HUBZone application package
([ez8a](https://www.ez8a.com/hubzone-certification/), vendor-published).

**Verdict: high willingness to pay, wrong business for us.** These are regulated filings with
approval-rate claims attached, an eligibility-advice component that edges toward practice of law,
and a work product that is mostly client-supplied facts rather than public-record analysis. The
factory's advantage (mass analysis of public records with citations) does not apply. **Do not build
here.** It is worth naming precisely because it is where the money visibly is, and it is a trap for
this particular business.

### 2.4 Rank 4: "What should I price this at?"

**The pain.** Pricing defensibility. Price-to-win studies run $20,000 to $300,000 on large programs
([OCI](https://ociwins.com/government-proposal-consultants/what-is-the-cost-to-prepare-a-proposal/),
vendor-published), so the pain is unquestionably worth money at the top of the market.

**Why it ranks fourth despite that.** The small-firm version is already free or nearly free. GSA's
CALC+ publishes prices paid on GWACs and MACs; Fed-Spend advertises AI pricing benchmarks at
$49/mo; GovCon API sells price benchmarks and GSA labor rates on the $79/mo Pro plan. And the
liability shape is bad: a pricing recommendation that loses a bid is a complaint waiting to happen,
against a business with no E&O policy yet (repo: feasibility F7, F8). A *factual* pricing exhibit
("here is what this office actually obligated on the last three awards in this NAICS, with
permalinks") is defensible and cheap to produce; a *recommendation* is not.

**Verdict: include as a section inside a larger deliverable. Never sell as the deliverable.**

### 2.5 Rank 5: "Who do I team with, and who is already inside?"

**The pain.** Real, and named by every vendor. But the answer is now $79/mo: GovCon API's Teaming
Partner Finder returns firms with proven past performance filtered by NAICS, agency, state, and
set-aside, ranked by obligated dollars, with named SAM points of contact
([GovCon API](https://govconapi.com/teaming-partner-api), observed). Its own caveats are the
interesting part: contacts are names without email or phone, performance is FY2025 onward, and it is
explicitly *not* a subaward relationship graph.

**Verdict: commoditized as a list, valuable only as a judgment.** The unmet part is not "who is
capable" but "who on this specific pursuit would actually take a call, and what do I say." That is
a service, not a data product, and it is founder-hour expensive.

### 2.6 Rank 6: "I lost and I do not know why"

**The pain.** Debriefs and protests. The primary numbers, from GAO's FY2025 Bid Protest Annual
Report to Congress: **1,688 protests filed** (down 6% from 1,803 in FY2024), **380 resolved on the
merits**, a **14% sustain rate** (down from 16%), and a **52% effectiveness rate**, unchanged, where
effectiveness counts voluntary agency corrective action plus sustained protests
(as summarized by [Pillsbury](https://www.pillsburylaw.com/en/news-and-insights/government-accountability-office-publishes-fiscal-year-2025-bid-protest-statistics.html),
[Crowell](https://www.crowell.com/en/insights/client-alerts/2025-gao-bid-protest-annual-report-where-have-all-the-protests-gone),
and [Fox Rothschild](https://governmentcontracts.foxrothschild.com/2025/12/articles/bid-protests/u-s-government-accountability-offices-fiscal-year-2025-bid-protest-report-to-congress-protest-filings-fell-while-the-overall-effectiveness-rate-stayed-above-50/),
all observed; the underlying GAO report is the primary source and should be cited directly in any
customer-facing use).

**Verdict: interesting as evidence, dangerous as an offer.** 1,688 filings per year across the whole
federal market is a thin market, protest advice is lawyer work, and PLAN-V3 §9.2 already flagged the
practice-of-law framing (repo). **Protest *patterns* as an input to a go/no-go section: yes.
Protest advice as a product: no.**

### 2.7 Rank 7: "I need training and a capability statement"

Abundantly supplied for free or near-free. SBA's own event calendar returned **1,023 events in the
next 30 days** on a single keyword query ([SBA events](https://legacy.sba.gov/events), observed),
Govology courses run around $75 a session with free access through many APEX centers
(vendor-published), and Fiverr sells capability statements at $105
([Fiverr](https://www.fiverr.com/chandoneaddis/create-a-professional-capability-statement), repo and
observed). **Do not build here.**

---

## 3. Adjacent products from the same data, evaluated

Every candidate from the brief, scored against four questions: is the pain evidenced, who is the
buyer, what is the observed price comparable, and what would the factory have to build. Ranked by
expected revenue per unit of build risk, not by market size.

Data sources referenced: **S-SAM** (SAM.gov notices and entity records), **S-USA** (USASpending and
FPDS-derived award history, including period-of-performance end dates, option runway, offer counts,
de-obligations, mod counts), **S-SUB** (FFATA subawards), **S-SBS** (SBA Small Business Search
certification profiles with entrance and exit dates), **S-GAO** (GAO protest decisions),
**S-FCST** (agency procurement forecasts).

| # | Candidate | Pain evidence | Buyer | Price comparable (observed) | Factory build | Fastest test |
|---|---|---|---|---|---|---|
| 1 | **Recompete pursuit file** on one named expiring contract | 10,452 recompetes in 14 months ≥$10M ([PrimeRFP](https://primerfp.com/intel/recompete-radar)); pre-solicitation window is the pain all four-figure subscriptions monetize | Small prime with matching past performance | Bidspeed 8h advisory $1,595; EZGovOpps Bronze $2,695/yr; PrimeRFP Tactics $2,958/yr | S-USA rollup by PIID with option runway, offer count, de-obligation, mod churn; S-SBS cert-exit join; S-SUB teaming map; S-SAM early notices; new "contract dossier" template plus gates | Build 3 from public data on real expiring contracts in target NAICS, show to 5 firms with matching PIIDs, ask for a signed order at $1,500 |
| 2 | **Certification-lapse takeover list plus pursuit file** | ~3,300 of ~16,300 set-aside recompetes in 18 months carry an incumbent whose cert lapses first ([GovCon API](https://govconapi.com/recompete-watchlist)) | Certified small firm hunting a takeover | Same band as #1; no observed direct comparable | #1 plus a strict cert-lapse gate: fire only on a dated exit before contract end, never on absence of a record | Run the query in 6 target NAICS, count the list, publish the count as a free finding, gate the named list |
| 3 | **Agency beachhead file** (one agency × one NAICS) | Market-entry pain sold by every vendor; contracting-office behavior (offers per award, single-bidder share, set-aside lean) is the input | Firm with commercial past performance entering federal, or entering a second agency | Bidspeed Build Your Acquisition Engine $999; Bidspeed Custom Market Research $995 | S-USA office-level aggregation, S-FCST forecast join, S-SAM notice-history, 12-month action plan template | Build one for a NAICS the repo already has an industry report for; offer it to the newsletter list at $1,200 |
| 4 | **Bid/no-bid decision file** on one live solicitation | 37% of "full and open" IT contracts drew one bidder ([GovCon API](https://govconapi.com/recompete-watchlist)); GAO-10-833 on miscoding | Firm holding a live solicitation and an evening to spend | Bidspeed 4h advisory $1,095 | S-USA contestability read, S-GAO protest patterns by office, price exhibit; reuses existing gates | Offer as a paid add-on to any packet buyer, $900, measure attach rate |
| 5 | **White-label capture desk** for proposal consultants and boutique capture shops | Consultants at $100 to $400/hr cannot serve small pursuits profitably (repo: GTM §1.3); PrimeRFP maintains a dedicated "Consultants & capture shops" door ([PrimeRFP](https://primerfp.com/consulting)) | The consultant, not the contractor | Their own billable rate; no observed wholesale comparable | Nothing new in the pipeline; needs an unbranded template, an SLA, and a referral or wholesale term | Send the existing 10 samples to 10 consultants with a wholesale price list; count replies |
| 6 | **Pricing benchmark exhibit** | PTW at $20k to $300k proves the pain at the top ([OCI](https://ociwins.com/government-proposal-consultants/what-is-the-cost-to-prepare-a-proposal/)) | Same firm, same pursuit | Free at CALC+; $49/mo Fed-Spend; $79/mo GovCon API | S-USA obligation history by office and NAICS with permalinks | Ship inside #1 and #4; never standalone |
| 7 | **Teaming and subcontractor map** | Real pain, named by every vendor | Small firm or prime | $79/mo ([GovCon API](https://govconapi.com/teaming-partner-api)) | S-SUB, thin coverage; GovCon API reports subaward data populated on roughly 1 in 20 IT recompetes | Ship as a section inside #1; do not price separately |
| 8 | **Federal revenue diligence** on an acquisition target | Real four-figure-to-five-figure pain in M&A | PE, corp dev, lenders | PrimeRFP already runs a diligence door at $90 pilot ([PrimeRFP](https://primerfp.com/diligence)); boutique DD engagements are five figures | Same S-USA rollups as #1, different framing | Do not test yet. Wrong buyer for a solo shop with no references |
| 9 | **Capability statement and past-performance packaging** | Demand is real | Newly certified firm | $105 Fiverr; $597 registration bundles | Formatting work, low analysis content | Skip |
| 10 | **Standalone industry benchmark report sold as research** | The repo already gives this away as the magnet | Anyone | $125 to $149 Bidspeed; free from us | Already built | Keep free. It is the magnet, not the product |
| 11 | **Raw or near-raw data feed** | Settled in the negative | Anyone | $19 to $79/mo | N/A | Never (repo: GTM §14.2.5) |

**The pattern across rows 6 through 11.** Every candidate that is *a fact you can look up* has a
sub-$100/mo substitute shipping today. Every candidate that is *a decision someone must own* has no
substitute under $995. The dividing line is not the data. It is whether a human is accountable for
the conclusion.

---

## 4. Who else buys, and what they would pay

Five segments beyond the small contractor, assessed for willingness to pay against the same
evidence standard.

### 4.1 Proposal consultants and boutique capture shops, as a white-label supplier

**Willingness to pay: moderate, and it is the most reachable of the five.**

The economics are already established in the repo: consultants bill $100 to $200/hr in DC Metro,
$150 to $400 in the wider market, and cannot profitably take a single small pursuit (repo: GTM
§2.1, citing OST and GovEagle). Their too-small leads currently go nowhere. Independent confirmation
that this is a recognized segment: PrimeRFP maintains a dedicated "Consultants & capture shops" door
in its site navigation ([PrimeRFP](https://primerfp.com/consulting), observed), and an outsourced
proposal-development industry exists specifically to lend capacity to other firms (iQuasar, OCI,
GDI Consulting, vendor-published).

**What they would buy.** Not a subscription. A per-file wholesale product they can mark up and put
their own name on, with a turnaround they can promise a client. The natural price is somewhere under
the retail price of the same file, and the natural term is the referral term the GTM report already
recommends (15% of first packet, or reciprocal).

**Risk.** The GTM report already warns that a soured subscription costs a referral relationship, and
referral partners are ranked channel #2 (repo: GTM §4). A wholesale relationship carries the same
risk with more surface area. Sequence: referral term first, wholesale second, never both at once
with the same firm before the first one has worked.

### 4.2 Primes seeking qualified small-business partners

**Willingness to pay: low for us, structurally.**

The obligation is real: FAR 19.702 requires the maximum practicable opportunity, and FAR 52.219-9
inserts a subcontracting plan in negotiated contracts expected to exceed $750,000, or $1.5M for
construction ([FAR Subpart 19.7](https://www.acquisition.gov/far/subpart-19.7), observed, primary).
GAO found agencies did not consistently follow oversight procedures for subcontracting plans, with
contracting officers failing to ensure reporting on more than half of 26 reviewed contracts
([CRS R47585](https://www.congress.gov/crs-product/R47585) summarizing the 2020 GAO study,
observed).

**Why it does not convert into revenue for a solo shop.** The prime's need is a vetted, warm,
capable partner they can put in a bid, which is a relationship deliverable, not a document. The list
version costs $79/mo. And the repo's own conflict analysis applies with force: supplying both sides
of a teaming relationship is the multi-client conflict problem (repo: feasibility F2) in a new
costume. **Defer, as the GTM report already concluded.**

### 4.3 PE, family offices, and lenders doing govcon diligence

**Willingness to pay: high per engagement, wrong fit.**

The buyer is real and the questions are exactly our data: recompete exposure, agency concentration,
protest posture, sustain rates, backlog quality (CohnReznick and PilieroMazza both publish diligence
checklists built on these, vendor-published). But a competitor has already built the product and
priced the entry at **$90** ([PrimeRFP diligence](https://primerfp.com/diligence), observed), the
real engagements are five figures and go to firms with names and insurance, and the buyer will ask
for references we do not have. **Not now. Revisit only if the recompete file works and produces
reusable rollups, because the analysis is the same analysis.**

### 4.4 Associations, APEX Accelerators, and SBDCs

**Willingness to pay: near zero directly, real indirectly.**

The repo already established that SBA-side partners cannot endorse (repo: GTM §1.2). What this pass
adds is the observable model for monetizing them anyway: Govology sells training to individuals at
roughly $75 a session and licenses it to APEX and SBDC centers, which then provide it free to their
clients (vendor-published). That is a B2B2C channel with a real precedent. **What they would take
from us is the free industry report and a data-driven speaking slot, which is exactly what
`sop/MARKETING.md` Door 6 already plans.** Do not build a paid product for this segment. Do build
the report so it is handable at NVSBE and in a counselor's training session.

### 4.5 Firms preparing for certification

**Willingness to pay: documented and four-figure, but for a different product than ours.**

$1,600 HUBZone packages, $7,600 GSA packages. See §2.3. The one honest adjacency: a certified firm's
**post-certification** question is "now what," and that is the agency beachhead file (candidate #3).
Cert shops meet the firm at exactly that moment, which is why the GTM report ranks them as referral
partners. **Sell to them as a referral source, not as a buyer.**

---

## 5. What makes a deliverable worth $1,000 to $3,000 rather than $500

Six factors, each tied to an observed price in §1.2 rather than asserted.

1. **The decision it serves has a number attached, and the number is large.** A $699 Sources Sought
   packet serves a decision worth an unknown future contract. A recompete file serves a named
   contract with a published current value. The buyer can do the arithmetic themselves, which is the
   whole reason a $7,600 GSA package sells.
2. **The window is months, not days.** Every observed four-figure purchase in §1.2 is made with time
   to think: an annual subscription, a filing, a block of hours. The repo's own finding is that the
   Sources Sought window (median 8 days, quarter at 3 or fewer) forces a compressed, one-CTA sale
   with no room for a second touch (repo: GTM §2.3). **A four-figure price and an eight-day window
   are incompatible.** Changing the object from the notice to the recompete is what makes the price
   reachable, and it is a structural fix rather than a copy fix.
3. **Scope is fixed and stated, and the buyer supplies nothing.** Bidspeed's $995 package lists five
   things the customer must supply. EZGovOpps requires an annual commitment and a $299 setup fee.
   The factory's asymmetry is that it starts from a UEI. That is worth stating as a line item, not
   as a tone.
4. **Someone is accountable for the contents.** Every observed four-figure product either names a
   team (Bidspeed advisory, Winvale) or makes a stated approval claim (Advance GSA's near-100%
   approval rate). Software at $500/yr names nobody. The GTM report already identified the named
   accountable human as one of three durable differentiators; §1.2 is the price evidence that the
   market pays for it.
5. **The refusal is part of the product.** PrimeRFP's own recompete page argues against scores:
   *"we surface facts, never a score. There is no '73% win probability.' A win score is a guess you
   would end up owning when it is wrong"* ([GovCon API](https://govconapi.com/recompete-watchlist)
   uses the same argument almost word for word). Two competitors independently arriving at
   facts-not-scores is strong evidence that this buyer punishes confident wrongness. Our version is
   stronger because we go one step further and decline the sale.
6. **Exclusivity, where it is honest.** The repo's default is one packet per notice pending
   TASK-0013, and the GTM report found the client-side reason: agency clauses can require an offeror
   to disclose consultant conflicts (repo: GTM §2.5). On a recompete, exclusivity is cheaper to hold
   than on a notice, because there are thousands of recompetes and only one buyer per contract needs
   this file.

**What does not justify the price, on this evidence:** more pages, more charts, faster turnaround,
or a bigger dataset. All four are available for $49 to $199/mo.

---

## 6. Lead magnets

**Honest framing first.** I found **no published conversion data for any lead magnet in the govcon
niche specifically**. What follows is (a) the observed magnet designs of vendors serving this exact
buyer, and (b) one cross-industry benchmark, clearly labeled. Anyone quoting §6 should carry that
caveat.

**Cross-industry benchmark, vendor-published aggregator, direction only.** Generic ebooks convert
near 3%; a free scoped audit converts at 5 to 15% opt-in and wins decisively on booked-call quality;
interactive assessments lead on raw opt-in; only about 12% of ebook downloaders finish reading
([shno.co aggregation](https://www.shno.co/marketing-statistics/lead-magnet-conversion-statistics),
[digitalapplied](https://www.digitalapplied.com/blog/lead-magnet-conversion-benchmarks-2026-b2b-data-reference)).
The operative advice in both sources is to score a magnet by how many opt-ins you would put on a
sales call, not by opt-in rate.

**Observed magnet designs in this market, 2026-08-26.**

| Vendor | Magnet | Gate | What it reveals |
|---|---|---|---|
| PrimeRFP | "Get the full shortlist for the federal pipeline: 10,452 expiring contracts, incumbents, and sustain rates" | Work email | Publishes the aggregate count free, gates the named rows |
| PrimeRFP diligence | "Run the target. Work email. **Two figures on this page, the rest in your inbox**" | Work email plus a named company | A firm-specific answer, partially shown |
| PrimeRFP | $90 for 90 days pilot, "one payment, no subscription" | Payment | A paid magnet that removes subscription fear |
| Fed-Spend | Free tier, 10 searches/month, full results, no credit card | Account | Argues explicitly it is "not a freemium bait-and-switch" |
| GovCon API | Free tools: vendor risk lookup, UEI lookup, contractor search, agency crosswalk, market pulse, daily snapshot | None | Six single-answer free tools feeding a $19 to $79/mo product |
| Bidspeed | Free webinars | Registration | Classic |
| Us, already built | Free per-NAICS industry report, free code watch, Form B free map plus gaps below the fill floor | UEI | repo: `brand/offer.md`, `sop/MARKETING.md` Door 9 |

**Three magnets to build, ranked, each matched to the offer it feeds.**

1. **The recompete cliff for one NAICS, aggregate free, named rows gated.** "In NAICS 236220, 41
   federal contracts held by small businesses reach their current period-of-performance end date in
   the next 6 to 18 months. 12 of them have no option years left. 3 have an incumbent whose SBA
   certification expires before the contract does." Publish the counts, gate the list behind a UEI
   and an email. This is PrimeRFP's shortlist mechanic, executed on the small-contract band they
   filter out at their $10M floor, which is where our buyer lives. It feeds Design C directly.
2. **The one-contract free read, a scoped audit.** Buyer names one contract, PIID or incumbent. They
   get back, free: current end date, potential end date, option runway, offer count next to the
   official competition flag, and whether the incumbent is excluded. That is five facts, all
   citable, all cheap for the factory, and it is the highest-quality-lead magnet shape in the
   benchmark above (a free scoped audit). It also demonstrates the product's actual argument in one
   screen: the official flag says competed, the offer count says one bidder.
3. **The "wired or contestable" calculator, for the top of funnel.** Aggregate, no personalization:
   pick a NAICS, see the share of awards in it that said "full and open" and drew a single offer.
   The number is the argument. Cheap, linkable, and the sort of thing a counselor or a podcast host
   can point at without endorsing anyone. Cite GAO-10-833 alongside our own measurement so the claim
   does not rest on one vendor's blog.

**What not to build.** An ebook, a checklist PDF, or another "how to respond to a Sources Sought"
guide. SamSearch owns that SERP (repo: feasibility F3), winacontract has around 47 posts in the
space (repo), and the benchmark above puts generic ebooks at roughly 3% with 12% read-through.

---

## 7. Three offer designs at the low four figures

All three are fixed price, prepaid, public-record-only, gated to the same standard as the existing
sample set, with a gaps page and an explicit no-sale outcome. All three assume the repo's existing
rules hold: nothing leaves without Mike's approval, fail closed, no claim without a file, and the
~20-minute founder review unit rule (repo: `AGENTS.md`, `sop/PLAN-V5.md` §7). Where a design breaks
the unit rule, that is stated.

### Design A: "Agency Beachhead", $1,200

**One agency × one NAICS, for a firm that wants in.**

What is in it: who buys this NAICS at this agency, by contracting office, with obligation totals and
permalinks. How each office buys: average offers per award, single-bidder share, set-aside lean. The
firms that actually win there and what they look like. The vehicles the work runs on and whether a
newcomer can reach it. What is forecast. The twelve notices of each type this agency posted in this
NAICS over the last year, with their response windows. A twelve-month action plan with named offices
and the pre-solicitation moments to aim at. A gaps page.

Price comparable: Bidspeed's Build Your Acquisition Engine at $999 and Custom Market Research at
$995, both observed, both requiring client input.

Factory build: office-level aggregation over S-USA, forecast join over S-FCST, notice-history over
S-SAM. Mostly new aggregation code, mostly reusing existing gate patterns. Moderate.

Honest weakness: **it is a report.** It is the design most exposed to the §1 finding that reports
have collapsed in price, and the buyer can approximate a worse version for $49/mo. Its defense is
completeness plus provenance plus a named human, which is exactly the untested assumption the GTM
report flagged as risk #4.

### Design B: "Bid Decision File", $900, sold as an add-on

**One live solicitation the buyer already has, answered before they spend an evening on it.**

What is in it: the contestability read (official competition flag next to the real offer count on
the predecessor contract), the incumbent's grip (de-obligations, mod churn, exclusion status, cert
window), the protest posture of that office and vehicle from S-GAO, a factual price exhibit of what
this office actually obligated on comparable work, the requirement map to the buyer's own public
awards, and a stated recommendation of the only two kinds this business is allowed to make: *the
record supports a bid and here is the coverage*, or *the record does not, and here is why*.

Price comparable: Bidspeed's 4-hour advisory block at $1,095, observed.

Factory build: smallest of the three. It is the existing packet's market slice plus a contestability
section plus a protest section.

Honest weakness: it is priced against hours, and 4 hours of a named human is a fair fight we might
lose on trust before we have references. It also arrives inside the same short window that caps the
$699 packet, so it does not fix the sales-cycle problem. **Best used as an attach to an existing
packet sale, not as a standalone acquisition offer.**

### Design C: "Recompete Pursuit File", $1,500. *Recommended first test.*

**One named federal contract that must recompete in the next 6 to 18 months, and everything a small
firm needs to decide whether to chase it and how to start.**

What is in it, all from public records, all cited:

- **The contract.** PIID, incumbent, awarding office, agency, NAICS, PSC, set-aside, current value,
  current period-of-performance end date, potential end date, option runway in days. The runway is
  the finding that separates a real recompete from a routine option exercise.
- **Is it contestable.** The official competition flag printed next to the actual offer count from
  the last cycle, with the gap between them named out loud. If it says full and open and drew one
  bidder, the file says so and the recommendation is do not chase.
- **Is the incumbent beatable.** De-obligations, contract-action churn, exclusion status, and the
  certification-window read: if the contract is set aside for a specific SBA program and the
  incumbent's certification for that exact program has a dated exit before the contract's end date,
  that is a takeover opening. **This signal fires only on a dated exit that we can cite. Absence of
  a certification record produces no signal**, because roughly half of firms have no profile at all
  ([GovCon API](https://govconapi.com/recompete-watchlist), observed), and reading absence as a red
  flag would be wrong about half the time. This is the same fail-closed discipline as G3.
- **Who is already inside.** The incumbent's named subcontractors from S-SUB, with the honest
  coverage caveat stated in the file itself: FFATA only requires first-tier subawards at or above
  the FAR 4.1403(a) threshold, so an empty list means nothing was reported, not that the incumbent
  works alone.
- **The buyer's own claim on it.** The requirement map from the incumbent's scope to the buyer's
  public award record, in the buyer's legal name, in the same Covered / Partial / Gap register the
  existing samples use.
- **What the office does.** Average offers per award, single-bidder share, set-aside lean, and the
  live sources-sought or pre-solicitation notices in that market right now with the contracting
  officer's name, email, and deadline.
- **The plan.** The pre-solicitation calendar working backward from the period-of-performance end
  date, with the specific moments at which a small firm can still act, and the draft of the first
  one that is available today.
- **The gaps page**, and where the record is thin, the sentence that says so.

**Price: $1,500.** Between Bidspeed's 8-hour block ($1,595) and its 4-hour block ($1,095), below
EZGovOpps Bronze ($2,695/yr), below PrimeRFP Tactics ($2,958/yr), and against a named contract whose
current value is printed on page one.

**Why this one and not the others.**

- **It breaks the ceiling that caps the business.** F1's binding constraint is sellable
  notice-moments, ~250 to 400/yr in six NAICS. Recompetes are a different and much larger
  population: 10,452 in 14 months above a $10M floor across all agencies (PrimeRFP, observed), and
  the small-contract band below that floor is not counted at all. The product stops being rationed
  by SAM's posting calendar.
- **It fixes the sales cycle.** A 6-to-18-month window is compatible with a four-figure price, a
  second touch, and a buyer who wants to think. The 8-day notice window never was (§5.2).
- **It is the pain with the most vendors and the highest prices** (§2.1), which is the strongest
  available evidence of willingness to pay in a market with no public purchase data.
- **The refusal is the product.** "This one says full and open and drew one bidder, do not spend
  your evening on it" is a sentence a subscription measured on engagement will not write, and it is
  the sentence `brand/offer.md` already requires us to write.
- **The factory mostly has the inputs.** S-USA period-of-performance and competition fields, S-SBS
  certification dates (the G3 gate already reads these), S-SUB subawards, S-SAM notices. The new
  work is a contract-level rollup, a new template, and new gates. That is a build, not a pivot.
- **It compounds with what already exists.** A firm that buys one recompete file has a mapped award
  record and a standing reason to hear from us on the next matching notice, which is the code-watch
  permission the GTM report identified as the real durable asset (repo: GTM §14.3).

**What would kill it, stated in advance.**

- **The offer-count field does not carry cleanly at the small-contract band.** Both the competition
  flag and the offer count are FPDS fields, and GAO found roughly 18% miscoding in its sample
  ([GAO-10-833](https://www.gao.gov/products/gao-10-833)). If the miscoding rate at our band is high
  enough that the contestability read is unreliable, the central claim of the file fails and the
  honest response is to demote it to one signal among several rather than the headline.
- **Coverage floor.** The repo recorded FPDS coverage from 2024-10-01 on the paid data layer and
  full history on USASpending (repo: `research/govconapi-exploration/REPORT.md` §1, §3). The
  recompete file needs *current* period-of-performance data, which is well inside every window, but
  the incumbent's history read needs the full USASpending record. Confirm before building.
- **The certification-lapse signal is thin in the target NAICS.** 3,300 out of 16,300 is a
  vendor-measured, government-wide figure. Re-derive it in our six NAICS before it appears in copy.
- **A competitor ships it as a report.** PrimeRFP already sells "Discovery Reports on demand" at
  Strategic+ ($1,290/mo) and GovCon API already sells the underlying fields at $79/mo. Neither sells
  a done-for-you, gated, cited file with a named human on it, but the distance is a packaging
  decision on their side.

### The comparison table

| | A. Agency Beachhead | B. Bid Decision File | **C. Recompete Pursuit File** |
|---|---|---|---|
| Price | $1,200 | $900 add-on | **$1,500** |
| Object | Agency × NAICS | One live solicitation | **One named expiring contract** |
| Decision window | Open-ended | Days | **6 to 18 months** |
| Supply ceiling | Unlimited but low urgency | F1's ~250 to 400/yr | **Thousands, and not notice-bound** |
| Nearest observed comparable | Bidspeed $995 | Bidspeed $1,095 (4 hrs) | **Bidspeed $1,595 (8 hrs)** |
| Buyer input required | UEI | UEI plus the solicitation | **UEI plus one PIID or incumbent name** |
| Factory build | Moderate, new aggregation | Small, extends the packet | **Moderate, new rollup plus template plus gates** |
| Exposed to the $49/mo substitute | **High** | Medium | **Low, because the conclusion is the product** |
| Founder review fits ~20 min | Probably not on first builds | Yes | **Unproven. Measure on build 1** |

---

## 8. The fastest test, in order

Sequenced so that the cheapest disconfirming evidence arrives first. No new legal exposure beyond
what TASK-0014 already covers, and no dependency on the unresolved contact-source counsel question
(repo: GTM §5.1) until step 4.

1. **Count the population, this week, agent time only.** Run the recompete query across the six
   target NAICS: contracts with a current period-of-performance end date 6 to 18 months out, small
   business or set-aside, value under the buyer's plausible band. Record how many carry a usable
   offer count, how many have exhausted options, how many carry a citable certification exit before
   the contract end. **Kill condition: if fewer than ~100 contracts across six NAICS survive with a
   usable offer count, the file has no supply and Design A becomes the fallback.**
2. **Build one file, end to end, and time the founder review.** Pick the single best contract from
   step 1. Build it against the existing gate discipline. **Kill condition: if the review does not
   fit inside the unit rule after the second build, reprice or cut scope, per `sop/PLAN-V5.md` §7.
   Do not paper over it.**
3. **Put it next to the substitutes, the same way the repo already specifies.** Same contract, run
   through Fed-Spend's free tier and PrimeRFP's $90 pilot. If a non-expert cannot name the
   difference in 30 seconds, the wedge is a preference and not a purchase reason, which is exactly
   assumption #4 from GTM §15 arriving in a new product.
4. **Sell three at $1,500, prepaid, to firms whose public award record matches the incumbent's
   scope.** Same close mechanics as the packet: artifact or evidence preview first, price in public,
   no discovery call, prepay after the preview. **Kill condition, borrowed from the repo's own gate
   discipline: 0 paid after 40 qualified exposures, twice.**
5. **Ship the free magnet built from step 1's output** (the per-NAICS recompete cliff, aggregate
   counts public, named rows gated). Measure opt-in and, more importantly, how many opt-ins were
   firms with a matching award record.

**The number to instrument from file one:** what fraction of buyers who receive a "do not chase
this one" verdict come back for a second file. If the refusal produces repeat business, the whole
positioning is confirmed and the price can hold. If it produces silence, the refusal is a cost we
are paying for a benefit that does not exist, and that should be known before it is built into the
brand any further than it already is.

---

## 9. What I could not establish

- **No community evidence, again.** Reddit is on the fetch tool's blocklist in this session and the
  search index returned no r/GovernmentContracting or r/govcon thread bodies. The one community
  quotation in §2.1 is secondhand from a vendor page that cites the thread. LinkedIn was not
  reachable either. Practitioner sentiment in those rooms remains unmeasured, not absent, and this
  is now the third consecutive research pass to hit the same wall. **If this matters, it needs a
  human with a browser, not another agent pass.**
- **No paid-search or keyword-volume data.** I found no published search-volume figures for
  "sources sought," "capability statement," "recompete," or adjacent terms. The demand ranking in §2
  is built on revealed preference (what vendors charge for) rather than on search demand.
- **No conversion data for any lead magnet in this niche.** §6's benchmarks are cross-industry and
  vendor-published aggregations.
- **No transaction prices, only list prices.** Every figure in §1 is a published price or a
  vendor-published range. Nobody publishes what was actually paid, what the discount was, or how
  many units sold. Bidspeed's ladder is evidence about packaging; it is no evidence about demand.
  The same caution applies to every row of §1.2.
- **Conference agendas were thin.** The 2026 NAPEX national conference is confirmed for August 16 to
  20, 2026, in Orlando, drawing "over 250 APEX Accelerator professionals"
  ([NAPEX](https://www.napex.us/national-conferences/), [SmallGovCon event listing](https://smallgovcon.com/events/event-2026-national-apex-accelerator-alliance-napex-conference-august-16-20-2026/)),
  but I could not retrieve a session-level agenda, so "which sessions sell out" is unanswered. Note
  also that NAPEX is a conference **for counselors**, not for contractors, which makes it a channel
  question rather than a demand signal.
- **The govconapi measurements are the vendor's own.** The 37% and 46% single-bidder figures, the
  3,300 certification-lapse count, and the 1-in-20 subaward coverage figure are all measurements
  published by a vendor with an interest in them. They are specific, falsifiable, and consistent
  with GAO's independent finding of significant single-offer competition, which is why I have relied
  on them. **All three should be re-derived from USASpending in our own six NAICS before any of them
  enters a customer-facing document.** That re-derivation is step 1 of §8, so it is already
  scheduled.
- **The r/govcon quotation and the "60 to 70% of obligations are recompetes" claim are both
  single-source and unverified.** Neither may enter copy as written.
- **govmates.com did not resolve to a govcon site.** A fetch of `https://govmates.com/` on
  2026-08-26 returned unrelated non-English content with a canonical tag pointing to a different
  domain. I have not concluded anything from this and have excluded govmates from the analysis
  rather than speculate. Worth one manual check if the teaming segment is ever revisited.

---

## Sources

**Primary / regulatory.**
[FAR Subpart 19.7, Small Business Subcontracting Program](https://www.acquisition.gov/far/subpart-19.7) ·
[FAR 52.219-9](https://www.acquisition.gov/far/52.219-9) ·
[GAO-10-833, Opportunities Exist to Increase Competition and Assess Reasons When Only One Offer Is Received](https://www.gao.gov/products/gao-10-833) ·
[CRS R47585, An Overview of Small Business Subcontracting](https://www.congress.gov/crs-product/R47585) ·
[SBA events calendar](https://legacy.sba.gov/events).

**Observed vendor pricing and product pages (retrieved 2026-08-26).**
[Bidspeed Marketplace](https://www.bidspeed.com/marketplace) ·
[Bidspeed Custom Market Research Package](https://www.bidspeed.com/products/custom-market-research-package) ·
[EZGovOpps pricing](https://ezgovopps.com/home/pricing/) ·
[PrimeRFP pricing](https://primerfp.com/pricing) ·
[PrimeRFP Recompete Radar](https://primerfp.com/intel/recompete-radar) ·
[PrimeRFP diligence](https://primerfp.com/diligence) ·
[PrimeRFP consulting](https://primerfp.com/consulting) ·
[GovCon API Recompete Watchlist](https://govconapi.com/recompete-watchlist) ·
[GovCon API Teaming Partner Finder](https://govconapi.com/teaming-partner-api) ·
[Advance GSA full-service package](https://www.gsaschedulecontract.com/gsa-full-service-package.html) ·
[Fed-Spend platform comparison](https://fed-spend.com/blog/govtribe-vs-govwin-vs-fed-spend-comparison).

**Vendor-published commentary (direction, not decimals).**
[Winvale, how much does GSA Schedule consulting cost](https://info.winvale.com/blog/how-much-does-gsa-schedule-consulting-cost) ·
[ez8a HUBZone certification](https://www.ez8a.com/hubzone-certification/) ·
[OCI, cost to prepare a proposal](https://ociwins.com/government-proposal-consultants/what-is-the-cost-to-prepare-a-proposal/) ·
[Legis1, noncompetitive federal contracts](https://legis1.com/news/federal-contracts-noncompetitive-one-third-of) ·
[govprocure, recompete contracts](https://govprocure.northwest.net/what-is-recompete-contract.html) ·
[shno.co lead magnet statistics](https://www.shno.co/marketing-statistics/lead-magnet-conversion-statistics) ·
[digitalapplied lead magnet benchmarks](https://www.digitalapplied.com/blog/lead-magnet-conversion-benchmarks-2026-b2b-data-reference) ·
[NAPEX national conferences](https://www.napex.us/national-conferences/) ·
[SmallGovCon, NAPEX 2026 listing](https://smallgovcon.com/events/event-2026-national-apex-accelerator-alliance-napex-conference-august-16-20-2026/).

**GAO FY2025 bid protest statistics, as summarized by counsel (the GAO report itself is the primary
source and should be cited directly in any customer-facing use).**
[Pillsbury](https://www.pillsburylaw.com/en/news-and-insights/government-accountability-office-publishes-fiscal-year-2025-bid-protest-statistics.html) ·
[Crowell & Moring](https://www.crowell.com/en/insights/client-alerts/2025-gao-bid-protest-annual-report-where-have-all-the-protests-gone) ·
[Fox Rothschild](https://governmentcontracts.foxrothschild.com/2025/12/articles/bid-protests/u-s-government-accountability-offices-fiscal-year-2025-bid-protest-report-to-congress-protest-filings-fell-while-the-overall-effectiveness-rate-stayed-above-50/).

**Internal (cited, not re-derived).**
`AGENTS.md` · `sop/PLAN-V5.md` §7 · `sop/MARKETING.md` Doors 6 and 9 ·
`brand/offer.md`, `brand/customer.md`, `brand/voice.md` ·
`knowledge/research/gtm-playbook/REPORT.md` Parts I and II ·
`research/feasibility-review/REPORT.md` F1, F2, F3, F7, F8, F10 ·
`research/govconapi-exploration/REPORT.md` §1, §3, §4 ·
`research/proposal-writing/PROPOSAL-RUBRIC.md` · `samples/sample-set/`.
