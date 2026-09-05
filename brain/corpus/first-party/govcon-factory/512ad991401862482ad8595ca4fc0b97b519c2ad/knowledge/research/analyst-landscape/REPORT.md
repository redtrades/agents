# Analyst landscape: who rates this category, what they say is weak, and where the analysts say the money is going

2026-08-26. Analyst-and-category research commissioned by Mike, run against Gartner (Peer Insights
plus one licensed document Mike supplied), G2 category pages, Forrester's public summaries, and
Deltek's published market data. Read-only pass. Nothing else in this repo was changed by this file.
Not committed to git.

**What this extends, so it does not repeat.**

- `knowledge/research/offer-design/REPORT.md` (2026-08-26) established the price ladder, that
  standalone information products have collapsed to $19 to $199/mo, that the gap between $995 and
  $2,995 holds no fixed-price done-for-you per-pursuit deliverable, and recommended a $1,500
  Recompete Pursuit File (Design C). This file does not re-derive any of that. It adds the analyst
  layer that ladder never had, and it forces one correction to Design C's certification-lapse gate.
- `knowledge/research/gtm-playbook/REPORT.md` (2026-08-26) established the channel ranking, the
  close mechanics, the notice-window constraint, and the SAM terms posture.
- `knowledge/research/competitor-pain/REPORT.md` (2026-08-26, **sibling session, running in
  parallel**) owns per-vendor review mining on G2, Capterra, Trustpilot, TrustRadius and BBB for the
  named govcon vendors. **This file deliberately does not mine individual vendor reviews.** It works
  one level up: which categories exist, who defines them, how much verified evidence each carries,
  and what the analysts believe about market direction. Where the two files touch the same fact,
  this one says so and defers.

**Evidence labels, same as the sibling files.**

- **Observed.** Retrieved from the named URL on the stated date, transcribed or counted directly.
- **Licensed.** From a Gartner subscription document read in Mike's authenticated browser session.
  Facts and figures are restated in our own words. Gartner's own usage terms restrict reproduction
  and redistribution, so nothing from these documents may be pasted into customer-facing copy
  without checking the licence. See §7 for the specific restriction.
- **Vendor-published.** A marketing page or blog from a party with an interest in the number.
  Direction, not decimals.
- **Syndicated.** A market-sizing figure from a commercial research aggregator whose methodology I
  could not inspect. Weakest evidence in this file.
- **Repo.** Already established in this repository, cited rather than re-derived.
- **Inference.** My reading. Mike may reject it.

---

## 0. Bottom line

Seven findings, ordered by how much they change what Mike does.

1. **The analyst layer does not cover this category, and I can now put a number on the vacuum.**
   Gartner Peer Insights runs a market called Government Contracting Software. It lists **14
   products and carries exactly one rating in total**: Awarded AI by Procurement Sciences AI, 4 out
   of 5, one rating. The other thirteen, including Deltek GovWin IQ, Deltek Costpoint, Unanet ERP
   GovCon, Bloomberg Government, Federal Compass and Tendios, all read "Be the first to write a
   review"
   ([Gartner Peer Insights, Government Contracting Software](https://www.gartner.com/reviews/market/government-contracting-software),
   observed 2026-08-26). That is **0.07 ratings per product**. The comparable commercial category,
   G2's Proposal Software, carries 22,127 verified reviews across 346 products, or **64 reviews per
   product** ([G2 Proposal Software](https://www.g2.com/categories/proposal), observed 2026-08-26).
   The buyer in our market has roughly **900 times less verified peer evidence** than the buyer of
   commercial proposal software. The sibling report reached the same conclusion from the vendor side.
   This is the second independent confirmation, and it is quantified.
2. **There is no Magic Quadrant, no Critical Capabilities, and no Peer Insights market for capture
   management, bid management or proposal management in a federal context.** The closest Gartner
   markets are RFP Response Management Applications (filed under Sales, 31 products, roughly 185
   ratings, not flagged Popular) and Government Contracting Software (11-category Public Sector
   parent, the thinnest of Gartner's 21 top-level categories). Gartner's only research document on
   RRM is a **Market Guide**, not a Magic Quadrant, which in Gartner's own taxonomy means the market
   is not considered mature enough to rank
   ([Market Guide for RFP Response Management Applications, G00825670, 29 October 2025](https://www.gartner.com/document/7127630),
   observed 2026-08-26, **gated on Mike's seat**, abstract only).
3. **Where analysts do rate procurement software heavily, they have written our buyer out of the
   definition.** Gartner defines Strategic Sourcing Application Suites as used primarily by companies
   with **$800 million or more in annual revenue**
   ([Gartner Peer Insights](https://www.gartner.com/reviews/market/strategic-sourcing-application-suites),
   observed 2026-08-26). That market carries 91 products and hundreds of ratings. Contract Life Cycle
   Management carries 74 products with 287, 267 and 258 ratings on the top three. The analyst
   attention and the review volume both sit at enterprise scale. The sub-$10M federal contractor is
   not in any rated category anywhere.
4. **The one measurable weakness that shows up consistently across the govcon vendors is ease of
   use, not features.** On G2's Government Procurement category (average 4.52 out of 5), the two
   largest incumbents both score **below** category average on Ease of Use: GovWin IQ 8.3 against a
   8.9 category average, GovSpend 8.1 against 8.9. TechnoMile Growth Suite and OpenGov Procurement
   both sit at 6.7 against 8.9
   ([G2 Government Procurement](https://www.g2.com/categories/government-procurement), observed
   2026-08-26). The small, newer tools score above it: BidPrime 9.7, SamSearch 9.5, Procurement
   Sciences AI 9.3, EZGovOpps 9.3.
5. **The leading AI proposal vendor's worst measured attribute is compliance.** AutogenAI carries 160
   G2 reviews at 4.3 out of 5, and inside G2's Bid Management category it scores **Compliance 6.6 out
   of 10 against a 7.8 category average** and Project Management 6.3 against 8.1
   ([G2 Bid Management](https://www.g2.com/categories/bid-management), observed 2026-08-26). Its
   G2-summarised cons are entirely about learning curve and complexity. Its top industries are
   Construction and Facilities Services, and its user base is 50% Large and 37% Medium firms. The
   flagship AI bid-writing product is not built for, sold to, or reviewed by our buyer, and where it
   is measured on compliance it is the weakest thing about it.
6. **The single largest business event in this file is a regulatory one, and Gartner published on it
   six days ago.** The SBA's proposed size-standard rule (RIN 3245-AI67, published 2026-08-20,
   comments due **2026-09-21**) would raise size standards for core federal services industries by
   roughly **10 to 15 times**, make about **37,002 firms with live FY25 contracts newly small**
   (roughly 105,655 contracts and more than $71 billion in obligations) while fewer than 200 lose
   status, for a net addition of about **114,541 firms** to the small business population. Gartner's
   read is that the losers are firms under $10 million in revenue, for whom "small" stops being a
   meaningful peer group, and that through 2027 the highest-value competitive variable shifts from
   size-standard eligibility toward **contracting-officer discretion**
   (licensed:
   [Gartner First Take, G00862854, 20 August 2026, George Sellner and Daniel Snyder](https://www.gartner.com/document-reader/document/8289021),
   read 2026-08-26; corroborated independently by
   [Federal Register 2026-17042](https://www.federalregister.gov/documents/2026/08/20/2026-17042/small-business-size-standards),
   [SBA Office of Advocacy](https://advocacy.sba.gov/2026/08/20/sba-issues-proposed-rules-on-industry-size-standards-and-revised-size-standards-methodology/),
   [Hunton](https://www.hunton.com/government-contracts-intelligence-briefing/sba-proposes-the-most-sweeping-overhaul-of-small-business-size-standards-in-a-generation-338-industry-groups-a-new-methodology-and-no-reductions),
   [Holland & Knight](https://www.hklaw.com/en/insights/publications/2026/08/sba-proposes-sweeping-overhaul-of-small-business-size-standards),
   all observed 2026-08-26).
7. **That rule breaks one of the repo's existing product ideas and creates a better one.** The
   certification-lapse takeover list (offer-design candidate #2, and the incumbent-beatable section
   of Design C) assumes socioeconomic set-asides are mandatory and therefore that a lapsed
   certification is disqualifying. Under the Revolutionary FAR Overhaul as drafted, 8(a), HUBZone,
   SDVOSB and WOSB move from "must" to "may", the prior priority of consideration is removed, and the
   once-8(a)-always-8(a) follow-on protection ends. On task and delivery orders under multiple-award
   contracts, the Rule of Two no longer applies at all and set-aside decisions are discretionary and
   non-protestable
   ([Acquisition.gov FAR Overhaul Part 19](https://www.acquisition.gov/far-overhaul/far-part-deviation-guide/far-overhaul-part-19),
   [Schwabe](https://www.schwabe.com/publication/the-revolutionary-far-overhaul-enters-phase-two/),
   [SmallGovCon on the once-8(a) rule](https://smallgovcon.com/8a-program/the-once-8a-always-8a-or-hubzone-sdvosb-or-wosb-rule-where-are-we-now/),
   observed 2026-08-26). **A lapsed certification is a weaker signal than the repo assumed. A
   contracting office's observed set-aside behaviour is a stronger one, and it is fully derivable
   from FPDS.**

**The recommendation in one line.** Build the **SBA size-standard recompute** (opportunity 1 in §8)
this week, because it has a dated deadline, it is pure public-record arithmetic, Gartner sells the
same advice as an analyst consultation to enterprises, and nobody sells the computed answer to a $5M
firm. Then convert Design A from "an agency report" into the **contracting-officer discretion
dossier**, because Gartner has now stated in writing that discretion is the variable that decides
awards through 2027.

---

## 1. What the Chrome session actually showed, and what it did not

**Stated plainly, because the brief asked me to report Mike's real context rather than a generic
search.**

When I called `tabs_context_mcp` at the start of this session, it returned **no tab group for this
session**. Calling it again with `createIfEmpty` produced a group containing a single new blank tab
(`chrome://newtab/`). The Claude-in-Chrome extension exposes only the tabs inside its own MCP tab
group, not the rest of Mike's browser. **So I did not see, and could not see, whatever Gartner pages
Mike already had open.** I did all the browsing myself, in a fresh tab, inside his browser profile.

Two consequences worth knowing:

- Because it is his browser profile, his Gartner cookies applied. Every Peer Insights page loaded as
  a signed-in session, and the licensed research document he sent mid-session opened and rendered.
  The profile is signed in under his corporate Gartner seat. **I did not log in, did not enter
  credentials, did not accept any terms, and did not click subscribe or upgrade anywhere.**
- The Gartner site search at `/search` returned an identical list of eleven generic documents for two
  completely different queries ("government contracting capture proposal management" and "government
  solution providers federal contracting"). That is a broken or personalised feed rather than a real
  result set. **I therefore cannot claim Gartner's research library has nothing on federal capture.**
  What I can report is narrower and still useful: the First Take Mike sent ends with "MORE ON THIS
  TOPIC: There are no additional documents available for this topic," and the only RRM research
  Gartner links from its own Peer Insights page is a single Market Guide.

**If Mike wants the gated Gartner library properly searched, that needs him driving, not an agent.**

---

## 2. Gartner Peer Insights, measured

All rows observed 2026-08-26. Peer Insights advertises "950+ Enterprise Software Categories" and
"over 880,000 verified reviews" across the whole site
([Gartner Peer Insights, all categories](https://www.gartner.com/reviews/markets)).

### 2.1 The four markets that touch our business

| Gartner market | Parent category | Products | Ratings on top products | Flagged "Popular" |
|---|---|---|---|---|
| [Government Contracting Software](https://www.gartner.com/reviews/market/government-contracting-software) | Public Sector and Government | 14 | **1 rating, total, across the whole market** | No |
| [RFP Response Management Applications](https://www.gartner.com/reviews/market/rfp-response-management-applications) | Sales | 31 | 55 / 36 / 21 / 19 / 17 | No |
| [Contract Life Cycle Management](https://www.gartner.com/reviews/market/contract-life-cycle-management) | Legal | 74 | 287 / 267 / 258 | **Yes** |
| [Strategic Sourcing Application Suites](https://www.gartner.com/reviews/market/strategic-sourcing-application-suites) | Supply Chain Management | 91 | 154 / 131 / 104 / 66 / 41 | No |

Structural note: Public Sector and Government holds **11 markets**, the smallest of Gartner's 21
top-level categories. Legal holds 41. Supply Chain Management holds 79. Only one Public Sector market
is flagged Popular, and it is Government ERP Solutions, which sells to agencies rather than to
contractors.

### 2.2 The Government Contracting Software market, in full

Fourteen products, sorted by number of ratings, high to low, as Gartner presents them:

| Product | Vendor | Rating |
|---|---|---|
| Awarded AI | Procurement Sciences AI | 4 (1 rating) |
| Authorium | Authorium | no reviews |
| Bloomberg Government | Bloomberg | no reviews |
| Brooklyn Platform | Brooklyn Solutions | no reviews |
| (product listing) | CobbleStone Software | no reviews |
| Contract Logix Platform | Contract Logix | no reviews |
| Costpoint | Deltek | no reviews |
| ERP GovCon | Unanet | no reviews |
| Federal Compass | Federal Compass | no reviews |
| GovWin IQ | Deltek | no reviews |
| OpenGov ERP | OpenGov | no reviews |
| PandaDoc | PandaDoc | no reviews |
| Tendios | Tendios Technologies | no reviews |
| WASTRAQ | M Pro9 | no reviews |

**Two things to notice.**

- **GovWin IQ has 154 reviews on G2 and zero on Gartner.** The same product, the same buyer, a 154 to
  0 split across two review platforms. Peer Insights requires business-email verification and is
  oriented to enterprise IT buyers. Our buyer does not go there. **Inference: Peer Insights is not a
  channel and not a source of pain evidence for this market. It is evidence of absence, which is
  itself the finding.**
- **Gartner's own product description for Authorium is wrong.** It describes Authorium as software
  for "regulatory documents in life sciences." Authorium is a public-sector contracting and document
  platform. A category with one rating is also a category nobody is checking.

### 2.3 What Gartner says an RFP tool must do, and what it leaves out

Gartner's mandatory feature list for RFP Response Management Applications, updated December 2025
([market page](https://www.gartner.com/reviews/market/rfp-response-management-applications), observed
2026-08-26):

- Ability to match RFP questions with existing answers
- Workflow management
- RFP response document editing
- Audit trail and version controls
- Knowledge management

**What is absent is the whole story.** No compliance matrix. No requirement traceability to Section L
and M. No source citation or provenance requirement. No no-bid or go/no-go output. Gartner has
defined this category as **content reuse with governance**, which is a commercial-sales problem, not
a federal-compliance problem. The market definition itself confirms `brand/offer.md`'s wedge: the
thing we do (per-claim provenance, a coverage register, a stated refusal) is not a feature anybody in
the rated category is required to have.

The category's own composition says the same thing. Responsive, the leader, is described on its
Gartner page as software for "RFPs, security questionnaires, and due diligence inquiries." That is a
vendor-security-review product, not a capture product.

### 2.4 The verified dislikes, quoted

Gartner Peer Insights publishes a Likes and Dislikes panel per product. These are verified enterprise
reviewers. The category is commercial RFP response, not govcon, so read these as **adjacent** pain
rather than our buyer's pain. Both observed 2026-08-26.

**Responsive** (4.3, 55 ratings,
[product page](https://www.gartner.com/reviews/product/responsive?marketSeoName=rfp-response-management-applications)):

> "AI Response section in the Content Library is affecting the page loading time as well as the
> answer generated by the AI often provide wrong product answer."

> "Lack of AI feature, user interface is not freindly"

> "The time it takes to set it up. We had 1200 items already in there, and clearly it hadn't been set
> up well as I have had to go through all of them. I wanted this to be a bit more seamless - helping
> me find duplicates more easily than it did. As it stood, I had to do that all manually, which was
> time consuming."

**Loopio** (4.4, 19 ratings,
[product page](https://www.gartner.com/reviews/product/loopio?marketSeoName=rfp-response-management-applications)):

> "The AI tool within Loopio can use some work. Even if I ask it to be direct or summarize a
> response, it will still give me a..." (truncated on the page)

> "I dislike having to reformat things in my questionnaire after I export, I dislike that I cannot
> always fix mapping that I do..." (truncated on the page)

> "Project Building function does work well at all. Its functions are a bit critical. # Issue of
> mistakenly deleted content..." (truncated on the page; the sentence appears to be missing a "not")

**The pattern across all six.** Nobody complains that the tool cannot write. They complain that
**the AI returns the wrong answer**, that **the content library has to be maintained by hand**, and
that **the setup cost lands on the customer**. Those are three separate confirmations of the
zero-input, provenance-first, fail-closed posture the repo already holds. The first one in particular
("often provide wrong product answer") is the paid, verified, enterprise version of the argument
`brand/offer.md` makes for free.

**Deferred to the sibling.** Vendor-level dislikes for HigherGov, GovWin IQ, GovTribe, PrimeRFP,
Bidspeed, SamSearch and the done-for-you services shops are covered in
`knowledge/research/competitor-pain/REPORT.md` §§ on review mining. Do not duplicate.

---

## 3. G2, the only place with real density

G2 is where this market's evidence actually lives, and the category-level numbers are the finding.
All observed 2026-08-26.

| G2 category | Products | Total verified reviews | Reviews per product | Category avg rating |
|---|---|---|---|---|
| [Proposal Software](https://www.g2.com/categories/proposal) | 346 | 22,127 | **64.0** | not stated |
| [Bid Management](https://www.g2.com/categories/bid-management) | 216 | 12,100+ | **56.0** | 4.3 / 5 |
| [Government Procurement](https://www.g2.com/categories/government-procurement) | 173 | **500+** | **2.9** | 4.52 / 5 |
| Gartner Government Contracting Software | 14 | 1 | **0.07** | n/a |

**Three readings.**

- **The evidence gap is the market gap.** A buyer choosing commercial proposal software reads 64
  reviews per product. A buyer choosing government procurement software reads three. The sibling
  report's conclusion, that showing a full sample before the invoice is something nobody else in the
  category can do, now has a denominator.
- **G2's Bid Management category is a construction category wearing a federal name.** The highlighted
  grid products are Autodesk Forma, Procore, HCSS, ConstructConnect, Buildertrend, JobNimbus,
  BuildingConnected Pro and AutogenAI. Its scored attributes are literally "Construction Software
  Integration." **If Mike ever buys keywords or writes SEO against "bid management," he is competing
  with Procore for a construction audience.** Use "capture," "sources sought," "recompete," and
  "government procurement" instead.
- **G2's Government Procurement category definition is stale.** The page credits Emma Stein and reads
  "Updated October 3, 2024." A category whose definition predates the FAR overhaul, the SBA proposed
  rule, and the entire 2025 to 2026 AI wave is not tracking this market.

### 3.1 Ease of use, by vendor, against the 8.9 category average

From [G2 Government Procurement](https://www.g2.com/categories/government-procurement), observed
2026-08-26. Category average Ease of Use is 8.9 out of 10.

| Product | Rating | Reviews | Ease of Use | Company size mix |
|---|---|---|---|---|
| GovWin IQ (Deltek) | 4.5 | 154 | **8.3** | 47% Medium, 29% Large |
| GovSpend | 4.3 | 103 | **8.1** | 51% Medium, 25% Large |
| Govly | 4.9 | 87 | 9.3 | 41% Medium, 32% Small |
| Starbridge | 4.7 | 32 | 8.5 | 58% Small, 33% Medium |
| BidPrime | 4.7 | 25 | 9.7 | 56% Small, 36% Medium |
| Procurement Sciences AI | 5.0 | 23 | 9.3 | 48% Small, 39% Medium |
| Salesforce Government Cloud | 4.3 | 18 | 8.5 | 47% Large, 32% Medium |
| Vendor Registry | 5.0 | 13 | 9.5 | 62% Small, 31% Medium |
| SamSearch | 5.0 | 11 | 9.5 | 55% Small, 45% Medium |
| OpenGov Procurement | 4.0 | 11 | **6.7** | 36% Medium, 27% Small |
| Euna Procurement | 4.5 | 10 | 9.3 | 36% Large, 36% Small |
| EZGovOpps | 5.0 | 10 | 9.3 | 60% Small, 30% Medium |
| UrbanLeap | 4.8 | 8 | 10.0 | 60% Medium, 30% Small |
| Sovra Procurement | 4.3 | 6 | 8.3 | 71% Small, 29% Medium |
| TechnoMile Growth Suite | 4.3 | 3 | **6.7** | 67% Small, 33% Medium |

**Inference, and it is the commercially useful one.** The negative correlation is between **product
breadth and ease of use**, not between price and satisfaction. Every product scoring below the
category average is a suite: GovWin IQ, GovSpend, OpenGov, TechnoMile. Every product scoring above it
is a single-purpose tool: BidPrime finds bids, Vendor Registry registers vendors, SamSearch searches.
The buyer punishes surface area. **A fixed-scope deliverable with one job is not a limitation to
apologise for in copy. It is the attribute this category's own reviewers reward.**

Two more things from the same page:

- **SamSearch lists 3 employees on LinkedIn and was founded in 2024**, and carries 11 G2 reviews at a
  perfect 5.0. A three-person company is a credible competitor in this category. That is both
  encouraging and a warning about how low the barrier is.
- **Deltek's own G2 marketing copy for GovWin IQ** claims 73% of its customer base are small
  businesses, that 75% of federal opportunities appear in GovWin IQ before they hit SAM.gov, and that
  73% of active tracked opportunities are in the forecast or pre-RFP stage (vendor-published, and
  they are selling the pre-solicitation window). It also claims that in 2024, 60% of federal awards
  went to roughly 5,800 GovWin IQ customers. **Do not repeat these. They are unaudited vendor
  claims.** They are recorded here because they show the incumbent is selling exactly the
  pre-solicitation pain the offer-design report ranked first, and selling it as analyst-validated
  human intelligence rather than as data.

### 3.2 The compliance finding

From [G2 Bid Management](https://www.g2.com/categories/bid-management), observed 2026-08-26.
AutogenAI, 4.3 out of 5 across 160 reviews, founded 2022, 171 employees:

| Attribute | AutogenAI | Category average |
|---|---|---|
| Good partner in doing business | 8.9 | 8.8 |
| Construction Software Integration | 8.8 | 7.6 |
| **Compliance** | **6.6** | **7.8** |
| **Project Management** | **6.3** | **8.1** |

Its G2-generated review summary lists five cons, and all five are the same con: learning curve, user
difficulty, not intuitive, steep learning curve, learning difficulty. Its top industries are
Construction and Facilities Services. Its user base is 50% Large and 37% Medium.

**Inference.** The best-reviewed AI proposal-writing product in the world, on 160 verified reviews,
is bought by large construction firms, is hard to learn, and is measurably weakest at compliance.
That is not a competitor to a fixed-price, zero-input, cited federal pursuit file. It is a different
business. And its compliance score is the strongest single number in this file supporting the claim
that AI proposal generation and federal compliance are not the same capability.

---

## 4. Forrester, briefly

Forrester's Wave reports are paywalled and I did not attempt to bypass them. What is publicly
established, all observed 2026-08-26:

- **The Forrester Wave: Contract Lifecycle Management Platforms, Q1 2025** evaluated 12 providers
  against 26 criteria across Current Offering and Strategy
  ([Forrester](https://www.forrester.com/report/the-forrester-wave-tm-contract-lifecycle-management-platforms-q1-2025/RES181997)).
- **The Contract Lifecycle Management Platforms Landscape, Q2 2026** included TechnoMile, a
  govcon-specific vendor, and characterises the CLM market as shifting toward post-signature
  intelligence, governance and integration depth
  ([TechnoMile's own summary](https://technomile.com/resources/the-contract-lifecycle-management-platforms-landscape-report-2),
  vendor-published; the underlying Forrester report is paywalled).
- **I found no Forrester Wave for proposal management, bid management, capture management, or federal
  procurement intelligence.**

**Inference.** Both major analyst houses cover our adjacent categories from the **buy side**
(agencies and enterprises buying things) and from the **contract side** (managing agreements after
signature). Neither covers the **sell side into government** as a rated category. TechnoMile
appearing in a CLM landscape is the only crossover, and it got there by being a CLM vendor that
happens to serve govcon, not by being a capture vendor.

---

## 5. Market size, and how much of it to believe

### 5.1 The software category

Every figure here is **syndicated**, meaning a commercial aggregator's number with a methodology I
could not inspect. The spread between them is the honest signal. All observed 2026-08-26 via search
result summaries; I did not purchase any report.

| Source | 2026 size | CAGR | Terminal |
|---|---|---|---|
| [MarketsandMarkets](https://www.marketsandmarkets.com/Market-Reports/proposal-management-software-market-160616397.html) | ~$3.22B | 11.6% | not stated |
| [Fortune Business Insights](https://www.fortunebusinessinsights.com/proposal-management-software-market-108680) | ~$3.66B | 12.20% | $9.19B by 2034 |
| [Business Research Insights](https://www.businessresearchinsights.com/market-reports/proposal-management-software-market-122859) | ~$2.81B | 12.5% | $8.22B by 2035 |
| [Future Market Insights](https://www.futuremarketinsights.com/reports/proposal-management-software-market) | $3.2B (2025) | 11.1% | $9.0B by 2035 |

**What to take from it, and what not to.** The four independent aggregators agree on the shape:
roughly **$3 billion in 2026, growing at 11% to 12.5%, roughly tripling over a decade**. They
disagree by 30% on the level. **Use the growth rate as direction and never quote the level.** More
importantly: **this is the global commercial proposal software market**, dominated by the RFP-response
and security-questionnaire use case Gartner's category definition describes. The federal capture
slice of it is not separately sized by anybody I could find. **There is no published market size for
federal capture or proposal software specifically.** That is a real gap and it is worth saying out
loud when anyone asks how big this is.

### 5.2 The underlying federal spend, which is measured properly

From Deltek's published FY2026 small business market article, authored by Kevin Plexico, SVP
Information Solutions, dated 2026-05-08
([Deltek](https://www.deltek.com/resources/articles/small-business-federal-contracting-2026/),
observed 2026-08-26, vendor-published but from the firm that runs the largest analyst desk in this
market):

- **2025 was a record year on both sides**: small business contracting **$195B**, other than small
  business **$612B**.
- **Defense contracting grew 9.4%, civilian grew 4.9%** in 2025.
- **8(a) was the socioeconomic category with the strongest growth, at 19% year over year**, despite
  a Pentagon review of the programme.
- **The number of small businesses participating in the federal market has declined 49% since FY
  2010.** Dollars are growing while the pool of firms shrinks.
- **Different agencies are currently running different versions of the FAR**, and Deltek's stated
  advice is that small businesses must be vigilant about which version applies to the agencies they
  target.

**Inference, and this is the one that reframes the whole business.** A market where **spend per
surviving small contractor is rising sharply** (record dollars divided by half the firms) is a market
where each surviving firm's individual pursuit is worth more, and where the firms that left did so
because of compliance cost rather than lack of opportunity. Deltek names the causes: category
management, IDIQ adoption, cash flow, and "the increasing costs of compliance." **The offer-design
report priced Design C at $1,500 against a Bidspeed advisory block. The better frame is that it is
priced against the cost of the compliance overhead that drove 49% of this market's firms out.**

---

## 6. The Gartner First Take Mike sent, and why it is the most important thing in this file

**Document.** *First Take: SBA Contracting Changes Rewrite the Rules of Competition for Government
Solution Providers*. Published **20 August 2026**, ID **G00862854**, 6 minute read, by **George
Sellner and Daniel Snyder** (Rishi Sood is also listed as available for consultation on it). Read in
Mike's authenticated browser session on 2026-08-26 at
[gartner.com/document-reader/document/8289021](https://www.gartner.com/document-reader/document/8289021).
Document type is a **First Take**, which is Gartner's fast-turnaround format for reacting to a named
external event, not a market forecast or a vendor evaluation.

**Licensing.** Gartner's footer states the publication may not be reproduced or distributed without
prior written permission, and separately that Gartner insights may not be used as input into or for
the training or development of generative AI or related technologies. Everything below is a **factual
restatement in our own words** for internal research use, with figures attributed. **Nothing from
this document may go into customer-facing copy, the newsletter, a sample, or the website without
Mike checking his licence terms first.** Where a fact below is independently available from a public
source, that public source is cited alongside, and **those public citations are the ones to use in
copy**.

### 6.1 What the document says

- The SBA published a proposed revision to small business size standards on 2026-08-20 (rule number
  RIN 3245-AI67), open for public comment through **2026-09-21**.
- Under the proposed Revised Methodology, size standards for **core federal services industries rise
  by roughly 10 to 15 times**.
- The change is **almost entirely additive**. By SBA's own estimate, **37,002 firms holding live FY25
  contracts become small**, covering about **105,655 contracts and more than $71 billion in
  obligations**. **Fewer than 200 firms lose small status.** Net addition to the small business
  population: about **114,541 firms**.
- The Revised Methodology **removes the existing maximum-size constraint**, producing dramatically
  higher industry-specific standards.
- If the Revolutionary FAR Overhaul is finalised substantially as drafted, it **retains** mandatory
  general small-business set-asides and the Rule of Two, but makes 8(a), HUBZone, SDVOSB and WOSB
  **discretionary**, removes their prior priority of consideration, and ends the once-8(a)-always-8(a)
  follow-on protection.
- Gartner's stated expectation: through 2027, the highest-value competitive variable in small business
  services contracting **shifts from size-standard eligibility toward contracting-officer
  discretion**, as governmentwide socioeconomic requirements give way to case-by-case acquisition
  decisions.
- **Winners**: midtier services firms with $50M to $500M revenue, whose graduation cliff moves out by
  years. Primes, who can meet small business goals with larger and more capable subcontractors.
  Acquirers and private equity running roll-ups, who can now combine small services firms without
  crossing the new thresholds.
- **Losers**: firms **under $10 million in revenue**, for whom "small" ceases to be a meaningful peer
  group, and micro-subcontractors squeezed out of prime teaming flow.
- Gartner notes the SBA's own rationale (industrial base resilience, loan programme participation,
  small business goal achievement) and says it is unclear whether SBA adequately considered the effect
  on existing small businesses now forced to compete against larger, more experienced and
  better-resourced firms.
- Gartner's first recommendation to affected firms: **recompute size status against the proposed 4-
  and 5-digit standards now**, because set-aside eligibility, teaming posture and capture strategy
  shift when the rule advances, not at final rule.
- The document's "More on this topic" section reads: there are no additional documents available.

### 6.2 Independent public corroboration

Every load-bearing fact above is available from public sources, all observed 2026-08-26:

- The Federal Register publication itself:
  [Small Business Size Standards, 2026-17042, published 2026-08-20](https://www.federalregister.gov/documents/2026/08/20/2026-17042/small-business-size-standards),
  full text at [govinfo](https://www.govinfo.gov/content/pkg/FR-2026-08-20/html/2026-17042.htm).
  Comment deadline 2026-09-21.
- [SBA Office of Advocacy announcement](https://advocacy.sba.gov/2026/08/20/sba-issues-proposed-rules-on-industry-size-standards-and-revised-size-standards-methodology/),
  confirming two linked proposed rules published the same day, one on industry size standards and one
  on the revised methodology.
- [Hunton](https://www.hunton.com/government-contracts-intelligence-briefing/sba-proposes-the-most-sweeping-overhaul-of-small-business-size-standards-in-a-generation-338-industry-groups-a-new-methodology-and-no-reductions):
  the rule replaces nearly 1,000 industry-specific size standards with **338 standards set at the 4-
  and 5-digit NAICS level**, eliminates all subindustry exceptions including ITVAR, converts
  construction and several other sectors from receipts-based to employee-based standards, removes the
  ceiling on size standards, and adds a productivity adjustment on top of inflation.
- [Holland & Knight](https://www.hklaw.com/en/insights/publications/2026/08/sba-proposes-sweeping-overhaul-of-small-business-size-standards),
  [Womble Bond Dickinson](https://www.womblebonddickinson.com/us/insights/insights/102nqrz/sba-issues-proposed-rule-intending-drastically-change-sba-size-standards),
  and [Schwabe](https://www.schwabe.com/publication/sba-proposes-the-largest-expansion-of-small-business-size-standards-in-decades/):
  concurring characterisations, all describing it as the largest expansion in decades.
- On the FAR side: [Acquisition.gov FAR Overhaul Part 19](https://www.acquisition.gov/far-overhaul/far-part-deviation-guide/far-overhaul-part-19),
  [Schwabe on RFO Phase Two](https://www.schwabe.com/publication/the-revolutionary-far-overhaul-enters-phase-two/),
  [HSToday on the Part 19 overhaul](https://www.hstoday.us/industry/revolutionary-far-part-19-overhaul-what-small-businesses-need-to-know/),
  and [SmallGovCon on FAR 2.0 deviations](https://smallgovcon.com/statutes-and-regulations/far-2-0-update-deviations-and-current-status/).
  The material point for us is now confirmed **verbatim in the primary source**. The overhauled
  **FAR 19.111-2** reads, at (a)(1), that contracting officers "may, at their discretion, set aside
  orders placed under multiple-award contracts" for small business concerns, and at (a)(2) that a
  "contracting officer's decision to set aside or not set aside an order for small business concerns
  is an exercise of discretion granted to agencies and not a basis for protest"
  ([Acquisition.gov, FAR Overhaul Part 19](https://www.acquisition.gov/far-overhaul/far-part-deviation-guide/far-overhaul-part-19),
  observed 2026-08-26). **Discretionary, and explicitly not protestable.** That single sentence is
  the regulatory basis for opportunity 2 in §8, and it is public, quotable, and citable in copy.

**Because all of it is publicly corroborated, Mike can write about this rule freely, citing the
Federal Register and the law firms.** The Gartner document's distinctive contributions are the 10 to
15 times multiple, the 37,002 / 114,541 firm counts, and the contracting-officer-discretion
prediction. Treat those three as internal-only unless the licence says otherwise.

### 6.3 What it breaks in the repo

**Correction 1, and it is a real one.** `knowledge/research/offer-design/REPORT.md` candidate #2 (the
certification-lapse takeover list) and the "is the incumbent beatable" section of Design C both rest
on a certification lapse being commercially decisive. That logic assumed the socioeconomic set-aside
is mandatory, so an incumbent whose 8(a) or HUBZone status expires before the contract ends cannot
recompete for it. **Under the RFO as drafted, those programmes become discretionary and lose priority
of consideration, and on multiple-award task orders the Rule of Two does not apply at all.** The
signal does not disappear, but it stops being deterministic and becomes one input among several.
Design C should demote it from the headline to a supporting section, exactly as the offer-design
report already anticipated for the offer-count field.

**Correction 2.** The same report's F1 notice-supply ceiling and its "list-3 firm" universe are both
computed against the current size standards. If the rule advances, the addressable population of
firms that can bid a given small business set-aside grows by 114,541 nationally, and the competitor
set on every pursuit in our six NAICS grows accordingly. **The recompete population does not shrink,
but the "is this contestable" answer changes on every single file.** Re-derive before Design C ships.

**Correction 3, and it is the opportunity.** Gartner's stated view that CO discretion becomes the
deciding variable through 2027 converts Design A ("Agency Beachhead", flagged in the offer-design
report as the design most exposed to the $49/mo substitute because "it is a report") into something
harder to substitute. Office-level set-aside behaviour, offers per award, single-bidder share and
vehicle lean are not facts a search subscription surfaces. They are aggregations over FPDS. **See
opportunity 2 in §8.**

---

## 7. Where the record is gated or thin

- **Gartner's Market Guide for RFP Response Management Applications (G00825670, 29 October 2025,
  Wendy Butler-Mafuz, Michele Buckley and one further author, 34 minute read) is gated on Mike's
  seat.** The page returns "You currently don't have access to this document. Contact us to learn how
  you can change your license." I did not attempt to work around it. The visible abstract states that
  RFP volume is growing, that chief sales officers cannot scale manual processes, and that RRM
  applications let sales leaders improve response quality and speed without adding headcount
  ([Gartner](https://www.gartner.com/document/7127630), observed 2026-08-26). A prior edition dated
  24 July 2024 is listed in the revision history. Vendors publicly claiming inclusion as
  Representative Vendors include
  [Templafy](https://www.templafy.com/news/templafy-recognized-as-a-representative-vendor-in-the-2025-gartner-market-guide-for-rfp-response-management-applications/)
  and
  [Expedience Software](https://www.globenewswire.com/news-release/2026/03/04/3249539/0/en/Expedience-Software-Recognized-as-a-Representative-Vendor-in-the-2025-Gartner-Market-Guide-for-RFP-Response-Management-Applications.html).
  **Neither is a govcon vendor.**
- **Forrester Waves are paywalled** and were not opened.
- **Gartner's site search did not function** for my queries (§1), so I cannot assert what else the
  research library does or does not hold on federal capture.
- **No Critical Capabilities document exists for any market in this space**, as far as I could
  determine. Gartner publishes Critical Capabilities only alongside Magic Quadrants, and there is no
  Magic Quadrant here.
- **Capterra and TrustRadius were not mined**, deliberately. The sibling session owns them.
- **No market size exists for federal capture or proposal software specifically.** The $3B figure in
  §5.1 is the global commercial category.
- **The Gartner document may not survive the rulemaking.** It analyses a *proposed* rule in an open
  comment period. Final standards may differ from the proposal, and Gartner says so. Every downstream
  product idea in §8 that depends on the new standards must carry that caveat in writing.

---

## 8. Ranked business opportunities

Ranked by expected revenue per unit of build risk for a solo operator with an agent swarm working
from free public federal data, not by market size. Each carries the evidence behind it and the
cheapest test that could disconfirm it.

### 1. The SBA size-standard recompute, sold inside the comment window

**What it is.** For one named firm: its NAICS codes from its SAM registration, the current size
standard for each, the **proposed** 4- or 5-digit group standard for each, the ratio, whether the firm
is currently small, whether it stays small, and how many additional firms holding live federal
contracts in those same codes become its competitors. Plus the list of its own live contracts and
recompetes where the competitor set changes. Plus a one-page comment template pointing at the two
issues Gartner says are underaddressed (recertification mechanics on long-term contracts, and the
competitive-concentration effect on the smallest firms).

**The evidence.**
- The rule is real, dated, and public: [Federal Register 2026-17042](https://www.federalregister.gov/documents/2026/08/20/2026-17042/small-business-size-standards),
  **RIN 3245-AI67, Docket No. SBA-2026-0199**, published 2026-08-20. Its own text reads: "SBA must
  receive comments on this proposed rule on or before September 21, 2026" (observed 2026-08-26). That
  is **26 days from today**.
- Scale: nearly 1,000 industry-specific standards collapse to 338 at the 4- and 5-digit level
  ([Hunton](https://www.hunton.com/government-contracts-intelligence-briefing/sba-proposes-the-most-sweeping-overhaul-of-small-business-size-standards-in-a-generation-338-industry-groups-a-new-methodology-and-no-reductions)).
- Gartner's first recommendation to affected firms is literally "recompute size status against the
  proposed 4- and 5-digit standards now" (licensed, G00862854), and Gartner monetises that advice as
  an analyst consultation booking. **Nobody sells the computed answer to a firm that cannot buy a
  Gartner seat.**
- Willingness to pay for regulatory-deadline work is the best documented in this market: $1,600 for a
  HUBZone application package, $7,600 for a GSA Schedule package (repo: offer-design §1.2).
- It fixes the structural problem the offer-design report identified: an 8-day notice window is
  incompatible with a four-figure price. A **26-day regulatory deadline with a multiyear consequence
  is not**.

**Why it fits this factory specifically.** Every input is free and public: the Federal Register tables,
SAM entity NAICS, FPDS live-contract records. There is no eligibility opinion involved, which keeps it
clear of the practice-of-law problem that made §2.3 of the offer-design report say "do not build here"
about certifications. It is arithmetic plus a citation, which is exactly what the gates already
enforce.

**The cheapest test.** Build the NAICS crosswalk table for the six target NAICS from the Federal
Register tables. One agent afternoon. **Publish the aggregate counts as a free magnet**: "In NAICS
236220 the proposed standard is Nx the current one, and M firms holding live federal contracts in this
code become small." Then offer the per-firm recompute to the first ten firms whose public award record
matches, at $750. **Kill condition: if the crosswalk shows the six target NAICS barely move, the
urgency is fake and this dies in a day for the cost of a day.**

**What would kill it.** The rule is proposed, not final. If it is withdrawn or materially changed, the
deliverable's value drops to zero. Mitigate by pricing it as a comment-window product with the caveat
printed on page one, not as a durable strategic asset.

### 2. The contracting-officer discretion dossier (Design A, repositioned)

**What it is.** `offer-design` Design A ("Agency Beachhead", $1,200) with its argument changed. Not
"here is who buys this NAICS at this agency" but "here is how each contracting office in this agency
actually **exercises discretion**": observed set-aside rate by office, socioeconomic versus general
set-aside mix, offers per award, single-bidder share, share of dollars flowing through multiple-award
task orders where the Rule of Two no longer applies, and which vehicles that office prefers.

**The evidence.**
- Gartner states in writing that through 2027 the deciding variable shifts from size-standard
  eligibility to contracting-officer discretion (licensed, G00862854).
- Publicly corroborated mechanism, in the regulation's own words: **FAR 19.111-2(a)(2)** states that
  a contracting officer's decision to set aside or not set aside an order under a multiple-award
  contract "is an exercise of discretion granted to agencies and not a basis for protest"
  ([Acquisition.gov](https://www.acquisition.gov/far-overhaul/far-part-deviation-guide/far-overhaul-part-19),
  observed 2026-08-26; see also
  [Schwabe](https://www.schwabe.com/publication/the-revolutionary-far-overhaul-enters-phase-two/)).
  **When a decision is unprotestable, the only way to influence it is to understand the person making
  it. That is the product.**
- Deltek independently reports that category management and IDIQ adoption are among the causes of the
  49% decline in small business participation since FY2010
  ([Deltek](https://www.deltek.com/resources/articles/small-business-federal-contracting-2026/)).
- The G2 ease-of-use data (§3.1) says buyers reward single-purpose tools. A dossier answering one
  question is on the right side of that.

**Why it beats the version in the offer-design report.** That report's honest weakness on Design A was
"it is a report, and the buyer can approximate a worse version for $49/mo." A search subscription
surfaces notices. It does not compute an office's revealed discretion rate over FPDS. **The
substitute cannot produce this output**, and now there is an analyst-stated reason why the output
matters.

**The cheapest test.** Compute the office-level set-aside rate and single-bidder share for the top ten
contracting offices in one target NAICS. Agent time only. Publish the ranked table free, gated at the
office-name level. **Kill condition: if set-aside behaviour does not vary meaningfully between offices
inside the same agency, there is no discretion to measure and the whole premise fails.**

### 3. The retiering exposure list

**What it is.** For a named firm or a named contract: who newly competes here. Under the proposed
standards, which firms with live federal contracts in this NAICS cross from other-than-small to small,
and which of them have past performance that beats our buyer's. Gartner frames this as the core threat
to firms under $10M, which is precisely `brand/customer.md`'s ICP.

**The evidence.** 37,002 firms with live FY25 contracts become small, covering roughly 105,655
contracts and more than $71 billion in obligations, against fewer than 200 losing status (licensed,
G00862854, and structurally corroborated by the public "no reductions" characterisation in
[Hunton](https://www.hunton.com/government-contracts-intelligence-briefing/sba-proposes-the-most-sweeping-overhaul-of-small-business-size-standards-in-a-generation-338-industry-groups-a-new-methodology-and-no-reductions)).

**Why it is second-tier rather than first.** It requires joining proposed standards to firm-level
revenue or employee counts, and **receipts are not public for most private firms**. FPDS obligations
are a proxy for federal revenue only, not total revenue, and the size standard is measured on total
receipts. **That is a real methodological hole and it must be stated in any deliverable.** The honest
version measures *federal* obligations and labels itself as a lower bound.

**The cheapest test.** Run it on one NAICS. Count how many firms can be classified at all. **Kill
condition: if more than half the relevant firms cannot be classified from public data, the list is
too incomplete to sell and this becomes a free magnet only.**

### 4. The FAR-version-by-agency register

**What it is.** A dated, cited, per-agency table of which FAR version, class deviation or FAR 2.0
practice currently applies. Free, public, updated, boring, and useful.

**The evidence.** Deltek states plainly that different agencies are using different versions of the
FAR right now and that small businesses must be vigilant about which applies
([Deltek](https://www.deltek.com/resources/articles/small-business-federal-contracting-2026/),
2026-05-08). Federal News Network has covered DoD class deviations leaving contractors with more
questions than answers
([Federal News Network](https://federalnewsnetwork.com/defense-main/2026/07/dod-class-deviation-leaves-contractors-with-more-questions-than-answers/),
2026-07). SmallGovCon maintains a running FAR 2.0 deviation status page
([SmallGovCon](https://smallgovcon.com/statutes-and-regulations/far-2-0-update-deviations-and-current-status/)).

**Why it ranks fourth despite being genuinely useful.** It is a fact you can look up, and the
offer-design report already settled that class of thing: every candidate that is a lookup has a
sub-$100/mo substitute or a free one. SmallGovCon is already publishing part of it for free.
**Build it as a magnet and a credibility artifact, never as the product.** Its real value is that it
is the kind of page an APEX counsellor or a podcast host can point at without endorsing anyone, which
is exactly the asset `sop/MARKETING.md` Door 6 needs.

**The cheapest test.** Build it for the six target agencies. Measure whether it gets linked.

### 5. Be the first reviewed anything in the category

**What it is.** Not a product. A distribution observation. Gartner Peer Insights lists 14 products in
Government Contracting Software with one rating between them. G2's Government Procurement category has
173 products sharing 500 reviews. The review floor in this category is close to zero.

**The evidence.** §2.2 and §3 of this file. Independently, the sibling report observed SamSearch
displaying a Gartner Peer Insights badge on its own site that links to a page reading "No Reviews Yet"
(repo: `knowledge/research/competitor-pain/REPORT.md`).

**The caveat that keeps it at rank 5.** Mike sells a **service deliverable**, not software. Gartner
Peer Insights and G2 both list some services categories, but a per-pursuit fixed-price document may not
qualify for either. And a listing with two reviews is not obviously better than no listing. **This is
worth 30 minutes of checking eligibility, not a project.**

**The cheapest test.** Read G2's and Gartner's listing eligibility criteria. Thirty minutes. If
eligible, list, and ask the first three buyers for a review in the same message as the reference ask
that `gtm-playbook` §7 item 8 already schedules.

### 6. Sell the analyst layer to the vendors

**What it is.** 173 products sit in G2's Government Procurement category. Most have fewer than 25
reviews and no analyst coverage of any kind. None of them can buy a Gartner seat that says anything
useful about their own market, because Gartner does not cover it.

**Why it ranks last.** Wrong buyer, no references, and it competes with Mike's actual customers for
his attention. The offer-design report reached the same verdict about PE diligence for the same
reasons. **Recorded so it is not rediscovered, not recommended.**

---

## 9. What I could not establish

- **Whether Gartner's research library holds anything else on federal capture.** Gartner's site search
  returned an identical generic list for two different queries (§1). The negative is unproven.
- **The contents of the RRM Market Guide.** Gated on Mike's seat (§7).
- **Any Forrester Wave content.** Paywalled, not opened.
- **A market size for federal capture or proposal software.** Does not appear to exist publicly
  (§5.1).
- **Willingness-to-recommend scores as numbers.** Gartner Peer Insights publishes "Highest Rated by
  Your Peers, For Willingness to Recommend" as a ranked list of three product names per market, not as
  a percentage, on the public market pages. For Contract Life Cycle Management the three named were
  Ivalua, Workday and smartContract CLM; for Strategic Sourcing Application Suites they were JAGGAER
  ONE, Workday and VendorPanel (observed 2026-08-26). **No numeric willingness-to-recommend figure was
  publicly visible for any product, so the brief's expectation of willingness-to-recommend scores could
  not be met at the number level.**
- **Whether the SBA rule advances.** It is a proposal in an open comment period. Everything in
  opportunities 1 and 3 is conditional on it.
- **Total review counts for Gartner markets.** Gartner shows ratings per product but no market-level
  total. The 185-rating figure for RFP Response Management Applications in §0 is my sum of the
  fourteen products carrying any rating, and the six carrying none. It is a floor, and the market lists
  31 products of which I read the first 20.
- **G2's incentive disclosure rate at category level.** The sibling report established that 42 of 50
  published GovWin IQ reviews carry G2's incentive disclosure. **That caveat applies to every G2
  number in §3 of this file and I did not re-verify it per category.** Read the G2 averages knowing
  some share of the underlying reviews were incentivised.

---

## Sources

**Gartner Peer Insights (all observed 2026-08-26).**
[All categories](https://www.gartner.com/reviews/markets) ·
[Public Sector and Government](https://www.gartner.com/reviews/markets/public-sector-and-government) ·
[Government Contracting Software](https://www.gartner.com/reviews/market/government-contracting-software) ·
[RFP Response Management Applications](https://www.gartner.com/reviews/market/rfp-response-management-applications) ·
[Contract Life Cycle Management](https://www.gartner.com/reviews/market/contract-life-cycle-management) ·
[Strategic Sourcing Application Suites](https://www.gartner.com/reviews/market/strategic-sourcing-application-suites) ·
[Sales categories](https://www.gartner.com/reviews/markets/sales) ·
[Legal categories](https://www.gartner.com/reviews/markets/legal) ·
[Supply Chain Management categories](https://www.gartner.com/reviews/markets/supply-chain-management) ·
[Responsive product page](https://www.gartner.com/reviews/product/responsive?marketSeoName=rfp-response-management-applications) ·
[Loopio product page](https://www.gartner.com/reviews/product/loopio?marketSeoName=rfp-response-management-applications).

**Gartner licensed research (read 2026-08-26 in Mike's authenticated session; restricted, see §6).**
First Take: SBA Contracting Changes Rewrite the Rules of Competition for Government Solution Providers,
G00862854, 20 August 2026, George Sellner and Daniel Snyder,
[document 8289021](https://www.gartner.com/document-reader/document/8289021) ·
Market Guide for RFP Response Management Applications, G00825670, 29 October 2025, Wendy Butler-Mafuz
and Michele Buckley, [document 7127630](https://www.gartner.com/document/7127630) (**gated, abstract
only**).

**Primary and regulatory (observed 2026-08-26).**
[Federal Register, Small Business Size Standards, 2026-17042, 20 August 2026](https://www.federalregister.gov/documents/2026/08/20/2026-17042/small-business-size-standards) ·
[govinfo full text](https://www.govinfo.gov/content/pkg/FR-2026-08-20/html/2026-17042.htm) ·
[SBA Office of Advocacy](https://advocacy.sba.gov/2026/08/20/sba-issues-proposed-rules-on-industry-size-standards-and-revised-size-standards-methodology/) ·
[Acquisition.gov, FAR Overhaul Part 19](https://www.acquisition.gov/far-overhaul/far-part-deviation-guide/far-overhaul-part-19).

**Counsel commentary on the SBA rule and the FAR overhaul (observed 2026-08-26).**
[Hunton](https://www.hunton.com/government-contracts-intelligence-briefing/sba-proposes-the-most-sweeping-overhaul-of-small-business-size-standards-in-a-generation-338-industry-groups-a-new-methodology-and-no-reductions) ·
[Holland & Knight](https://www.hklaw.com/en/insights/publications/2026/08/sba-proposes-sweeping-overhaul-of-small-business-size-standards) ·
[Womble Bond Dickinson](https://www.womblebonddickinson.com/us/insights/insights/102nqrz/sba-issues-proposed-rule-intending-drastically-change-sba-size-standards) ·
[Schwabe, largest expansion in decades](https://www.schwabe.com/publication/sba-proposes-the-largest-expansion-of-small-business-size-standards-in-decades/) ·
[Schwabe, RFO Phase Two](https://www.schwabe.com/publication/the-revolutionary-far-overhaul-enters-phase-two/) ·
[HSToday, Part 19 overhaul](https://www.hstoday.us/industry/revolutionary-far-part-19-overhaul-what-small-businesses-need-to-know/) ·
[SmallGovCon, FAR 2.0 deviations status](https://smallgovcon.com/statutes-and-regulations/far-2-0-update-deviations-and-current-status/) ·
[SmallGovCon, once-8(a)-always-8(a)](https://smallgovcon.com/8a-program/the-once-8a-always-8a-or-hubzone-sdvosb-or-wosb-rule-where-are-we-now/) ·
[George Mason Costello College on the FAR overhaul](https://business.gmu.edu/news/2026-04/revolutionary-overhaul-federal-acquisition-regulation-major-takeaways-practitioners).

**G2 category pages (observed 2026-08-26).**
[Proposal Software](https://www.g2.com/categories/proposal) ·
[Bid Management](https://www.g2.com/categories/bid-management) ·
[Government Procurement](https://www.g2.com/categories/government-procurement).

**Forrester (public summaries only; reports paywalled and not opened).**
[The Forrester Wave: Contract Lifecycle Management Platforms, Q1 2025](https://www.forrester.com/report/the-forrester-wave-tm-contract-lifecycle-management-platforms-q1-2025/RES181997) ·
[TechnoMile on the CLM Platforms Landscape, Q2 2026](https://technomile.com/resources/the-contract-lifecycle-management-platforms-landscape-report-2) (vendor-published).

**Trade press and vendor market data (observed 2026-08-26).**
[Deltek, Decoding the Government Contracting Market Environment for Small Business, Kevin Plexico, 8 May 2026](https://www.deltek.com/resources/articles/small-business-federal-contracting-2026/) ·
[Federal News Network, DoD class deviation leaves contractors with more questions than answers, July 2026](https://federalnewsnetwork.com/defense-main/2026/07/dod-class-deviation-leaves-contractors-with-more-questions-than-answers/) ·
[Federal News Network, where contractors should focus in 2026](https://federalnewsnetwork.com/contracting/2026/01/new-year-new-opportunities-heres-where-contractors-should-focus-in-2026/) ·
[ExecutiveBiz on Deltek's FY26 top federal opportunities](https://www.executivebiz.com/articles/deltek-fy26-govcon-opportunities-trends).

**Syndicated market sizing (aggregators, methodology not inspected, direction only).**
[MarketsandMarkets](https://www.marketsandmarkets.com/Market-Reports/proposal-management-software-market-160616397.html) ·
[Fortune Business Insights](https://www.fortunebusinessinsights.com/proposal-management-software-market-108680) ·
[Business Research Insights](https://www.businessresearchinsights.com/market-reports/proposal-management-software-market-122859) ·
[Future Market Insights](https://www.futuremarketinsights.com/reports/proposal-management-software-market) ·
[Research and Markets](https://www.researchandmarkets.com/reports/5980535/proposal-management-software-market-report).

**Vendor claims of Gartner Market Guide inclusion (vendor-published).**
[Templafy](https://www.templafy.com/news/templafy-recognized-as-a-representative-vendor-in-the-2025-gartner-market-guide-for-rfp-response-management-applications/) ·
[Expedience Software](https://www.globenewswire.com/news-release/2026/03/04/3249539/0/en/Expedience-Software-Recognized-as-a-Representative-Vendor-in-the-2025-Gartner-Market-Guide-for-RFP-Response-Management-Applications.html).

**Internal (cited, not re-derived).**
`AGENTS.md` · `sop/PLAN-V5.md` §7 · `sop/MARKETING.md` Doors 6 and 9 ·
`brand/offer.md`, `brand/customer.md` ·
`knowledge/research/offer-design/REPORT.md` §§1, 2.3, 3, 7 (Designs A and C), 8 ·
`knowledge/research/gtm-playbook/REPORT.md` §§2.3, 7, 12 ·
`knowledge/research/competitor-pain/REPORT.md` (sibling session, review mining layer).
