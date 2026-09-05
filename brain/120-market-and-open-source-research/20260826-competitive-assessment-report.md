# Competitive assessment: claim versus capability, vintage, and what is structurally ours

2026-08-26. Commissioned by Mike as a correction to the prior pass. Read-only; nothing else in this
repo was changed by this file. Not committed to git. Handoff runs through a GitHub issue on
`redtrades/govcon-factory` (see `HANDOFF-COMMENT.md` in this directory, and the note in §11 about why
this session could not post it itself).

**Mike's correction, which governs the whole file.** The last pass read competitor marketing copy and
treated claims as capabilities. A landing page claim costs nothing to write and confers nothing. What
matters is whether the vendor can deliver the thing, whether a buyer can verify it, and whether the
business model even permits it. Mike's specific read, which this file was told to test rather than
assume: PrimeRFP's provenance copy looks LLM-generated and echoes language we have used, which if
true is evidence of low substantiation rather than of real capability.

**Mike's second instruction, folded in rather than bolted on.** Company legitimacy and vintage change
how seriously a claim should be taken. A twelve-week-old startup asserting provenance is a different
competitive fact from an eight-year-old company with paying customers asserting the same. Vintage is
therefore not an appendix here. It is §1, and it drives the threat ranking in the verdict.

**Mike's third instruction, and it exposed a real defect.** Our competitor list came from prior
research rather than from how a buyer finds vendors. §9 rebuilds it from eleven searches a real
SDVOSB owner would run. Twenty-six new names appeared, including one that is a better analogue to our
business than anything in the prior reports, and the entire software tier that both prior passes
treated as the competitive set turned out to be **invisible at the moment of purchase intent**. §10
records who owns that demand and what it costs to show up, for the sibling Demand generation session.

**What this extends, so it does not repeat.**

- `knowledge/research/competitor-pain/REPORT.md` (2026-08-26) built the claim inventory, the price
  table, and the review-surface finding. This file does not re-derive any of it. It tests it.
- `knowledge/research/offer-design/REPORT.md` (2026-08-26) built the price ladder and the $1,500
  Recompete Pursuit File recommendation. Cited, not re-derived.
- Sibling sessions: competitor review mining (done, review surfaces) and Gartner market opportunity
  scan (running, analyst layer). This file deliberately does not touch review counts or analyst
  coverage.

**Evidence labels.**

- **Primary.** A federal system of record. FPDS-NG ATOM feed or the USASpending API, queried directly
  and quoted with field names.
- **Registry.** WHOIS, DNS, or a company registry. Machine-read, quoted with the field.
- **Observed.** Retrieved from the named page on 2026-08-26 unless another date is given.
- **Artifact.** A product output obtained free, without payment, without an account, and without
  accepting terms, then assessed.
- **Vendor-published.** A page from a party with an interest in the claim.
- **Inference.** My reading. Mike may reject it.

**Method limits, stated up front because they bound several sections.**

1. **archive.org is unreachable from this session.** Both `web.archive.org/cdx/search/cdx` and
   `web.archive.org/web/...` return a hard blocklist error from the fetch tool. Per the operating
   rules I did not route around it with curl, Python, a browser, or a mirror. So **no first-capture
   dates and no Wayback diffs appear anywhere in this file.** Every place Mike's brief asked for
   archive.org, I substituted a different dated artifact and said so. The best substitute turned out
   to be vendor-claimed third-party directory listings, which freeze an older self-description in
   place (§1.3, §4.2). It is weaker than a Wayback diff on precision and stronger on provenance,
   because the vendor wrote it.
2. **No accounts, no purchases, no terms accepted.** HigherGov, Sweetspot, SamSearch, Rogue and the
   PrimeRFP platform all gate their product behind either a credential-bearing signup, a payment, or
   a sales demo. I took none of them. Separately, HigherGov's terms §3.6 restricts trials to
   "individuals or organizations that could become potential HigherGov customers" and explicitly
   "excludes individuals or organizations that compete with HigherGov and their representatives"
   ([HigherGov ToS](https://www.highergov.com/tos/), observed 2026-08-26). A trial was therefore both
   outside my rules and outside theirs.
3. **What I could get free is listed in §3 and it is more than expected.** One competitor publishes
   its actual reasoning artifact as a downloadable file, and one publishes a live product brief with
   real numbers on a real contract. Those two are the load-bearing evidence in this report.
4. **LinkedIn is not reachable.** Headcount figures below come from Y Combinator's own listing, from
   career pages, and from team pages, never from LinkedIn.

---

## 0. Bottom line

Eleven findings, ordered by how much each changes what Mike does.

1. **PrimeRFP's provenance claim is real at the data layer and fails at the judgment layer, and I can
   prove both against the federal record.** Their flagship public contract brief, the one they
   themselves link from their MCP page as the demonstration, reports Obligated $2.8M, Current value
   $3.8M, Potential $5.6M for PIID 72MC1024C00008
   ([PrimeRFP](https://primerfp.com/intel/contract/72MC1024C00008), observed 2026-08-26). USASpending
   returns `total_obligation` 2835145.0, `base_exercised_options` 3841899.61, `base_and_all_options`
   5553907.45 ([USASpending API](https://api.usaspending.gov/api/v2/awards/CONT_AWD_72MC1024C00008_7200_-NONE-_-NONE-/),
   primary, queried 2026-08-26). **Their numbers reconcile exactly.** The same brief then says *"The
   prior award was single-bid — competitive dynamics may favor a challenge,"* and sells a $90 CTA
   reading *"Score my position vs Leidit, LLC."* The federal record says
   `extent_competed_description` "NOT AVAILABLE FOR COMPETITION", `solicitation_procedures_description`
   "ONLY ONE SOURCE", `type_set_aside_description` "8(A) SOLE SOURCE", and
   `other_than_full_and_open_description` "AUTHORIZED BY STATUTE (FAR 6.302-5(A)(2)(I))" (same
   primary source; FPDS-NG ATOM returns the same four values on every action,
   [FPDS](https://www.fpds.gov/ezsearch/FEEDS/ATOM?FEEDNAME=PUBLIC&q=PIID%3A%2272MC1024C00008%22),
   primary, retrieved 2026-08-26). It drew one bidder because it was not competed. **They cite
   correctly and then reason past their own citation, and the contradicting field is printed on the
   same page.** That is not a provenance product. That is a data product with a generative narrative
   bolted on top and no gate between them.
2. **Their only publicly inspectable reasoning artifact defines "cite" as "link to us."** The free
   SCOUT SKILL.md, downloadable with no login, contains a section literally headed **"Cite the pages
   that convert"** and instructs the model to append `?utm_source=scout_skill` to the PrimeRFP URLs it
   cites ([primerfp.com/scout-skill/SKILL.md](https://primerfp.com/scout-skill/SKILL.md), artifact,
   retrieved 2026-08-26). Every citation target in the file is a primerfp.com marketing page. Not one
   is FPDS, USASpending, or SAM. **The word "receipts" in their marketing and the word "cite" in
   their engineering point at different things, and the engineering one points at their own funnel.**
3. **Mike's read is half right, and the half that is wrong matters more.** The provenance copy is
   thin, unsubstantiated at the judgment layer, and absent from their entire product announcement
   record (§4.1). But it does not echo our phrasing. "Receipts" appears nowhere in `brand/`; our
   vocabulary is "provenance," "no claim without a file," "every fact points at a source"
   (`brand/company.md` line 29, repo). And there is no mechanism: `redtrades/govcon-factory` returns
   nothing to an unauthenticated fetch and our site copy does not carry this language. **This is
   convergent evolution on an obvious idea, not copying.** Which is worse news than copying, because
   it means the positioning is findable by anyone who thinks about the problem for a week.
4. **Vintage inverts the threat ranking, and the loudest competitor is not the dangerous one.**
   Domain-creation dates, machine-read 2026-08-26: bidspeed.com 2004-08-21, primerfp.com 2020-11-28,
   highergov.com 2022-08-01, procurementsciences.com 2022-11-14, userogue.com 2023-02-02,
   sweetspot.so 2023-06-09, samsearch.co 2023-11-06 (registry, python-whois). **Bidspeed is a
   twenty-one-year-old business quietly selling a $395 human-delivered per-notice deliverable.
   PrimeRFP is a pivoted five-year-old domain with no named humans anywhere on its site.** The prior
   pass treated PrimeRFP as the primary threat because its copy was closest to ours. On evidence, the
   primary threats are Procurement Sciences ($30M Series B, Nov 2025) and Bidspeed (two decades of
   operating history, our exact deliverable shape). See §6.4.
5. **PrimeRFP is a documented pivot, and the pivot is recent.** Their own vendor-claimed SourceForge
   listing still describes a generic commercial RFP-matching tool for "Companies in need of a tool to
   improve their bidding oportunities," categorised under RFP, RFx and AI Proposal Generators, priced
   at "$500 per year," with zero reviews and no mention of federal, FPDS, recompete, NAICS, set-aside
   or provenance ([SourceForge](https://sourceforge.net/software/product/PrimeRFP/), observed
   2026-08-26; the page carries "Page Already Claimed," so the vendor wrote it). The live site sells
   federal capture intelligence from $290 to $1,290 a month. Their entire announcement record starts
   2026-04-30 ([PrimeRFP announcements](https://primerfp.com/news/announcements), observed
   2026-08-26). **The provenance identity is roughly four months old on a product that spent years
   being something else.**
6. **Not one of these vendors holds a federal prime award.** USASpending's recipient autocomplete
   returns zero matches for PrimeRFP, SamSearch, Bidspeed, Procurement Sciences, Gov Alpha and
   HigherGov, and returns only unrelated entities for Sweetspot and Rogue
   ([USASpending recipient autocomplete](https://api.usaspending.gov/api/v2/autocomplete/recipient/),
   primary, queried 2026-08-26). They are software vendors selling to industry, so this is not
   damning. It does mean **nobody selling advice on winning federal work in this set has federal past
   performance of their own**, and none of them can answer the question a buyer asks in month two.
7. **The fine print contradicts the headline in three of six cases, and HigherGov's is quotable
   enough to put in front of a buyer.** HigherGov's terms §4.2 state that their data-enhancement
   methods "in many instances may introduce different or new inaccuracies. Thus, HigherGov should not
   be relied on as a faithful representation of government data," and §5.1 tells users to "verify all
   proprietary and public data that they use for critical business or government purposes with
   multiple independent sources" ([HigherGov ToS](https://www.highergov.com/tos/), observed
   2026-08-26). Their liability cap is three months pro-rata, with their own worked example putting
   it at $625 on a $2,500 annual seat (§10.1, same source). PrimeRFP's terms, last updated 2025-06-03
   and unchanged through the entire SCOUT repositioning, are generic SaaS boilerplate with a blanket
   "without warranties of any kind" disclaimer and no mention of accuracy, provenance, citation or
   audit ([PrimeRFP ToS](https://primerfp.com/terms), observed 2026-08-26).
8. **The subscription-cannot-refuse hypothesis survives testing, but in a narrower and sharper form
   than the prior pass stated it.** PrimeRFP explicitly claims a refusal: "When coverage is thin for
   an agency or a program, SCOUT says the records are absent rather than returning a confident-looking
   empty" ([primerfp.com/mcp](https://primerfp.com/mcp), observed 2026-08-26). Their SKILL.md tells
   the model to "clearly state limitations and data gaps." So the crude version of our claim, that a
   subscription cannot say "I don't know," is **already false**. What their showcase brief proves they
   cannot do is refuse **when the data is present and contradicts the recommendation**. That is the
   real, narrow, defensible line, and it is worth more than the broad one because it is testable.
9. **Two positions we thought were ours are already occupied, and we should stop selling them.**
   HigherGov ships "Live Analyst Support" at the $500/yr Starter tier
   ([HigherGov pricing](https://www.highergov.com/pricing/), observed 2026-08-26), which falsifies the
   flat claim that a $500/yr product cannot put a human on the line. And PrimeRFP publishes a
   substantive methodology block naming FPDS-NG, SAM.gov and USASpending, disclosing a $100K
   award-level floor applied to `current_total_value_award`, the 60 to 90 day DoD reporting lag, and
   why their aggregates exceed the Bloomberg Government FY2025 figure of $833.8B
   ([Recompete Radar](https://primerfp.com/intel/recompete-radar), observed 2026-08-26). That is
   better methodology disclosure than most of this category and better than we assumed. Citation and
   methodology transparency are no longer differentiators. **Adjudication is.**

10. **We were researching the wrong competitive set, and the demand side proves it.** Eleven searches
    a real SDVOSB owner would run, all 2026-08-26 (§9.1). **PrimeRFP, Bidspeed, Sweetspot, SamSearch,
    Rogue and HigherGov were named zero times** in any synthesised answer to a buyer asking who can
    help them bid. The names that came back are twenty-year-old proposal shops: Optimal Thinking
    (domain 1997), Lohfeld (2003), GovPartners (2005), ProposalHelper (2009), and above all
    **SAS-GPS, a service-disabled-veteran- and woman-owned proposal firm operating since 2002, with
    named client testimonials, a live BBB A+ seal, a fixed-price model, and an active proposal-writer
    hiring pipeline** ([sas-gps.com](https://sas-gps.com/), observed 2026-08-26). **That is a closer
    analogue to our business than any software vendor in this report, and neither prior pass
    mentions it.** Full assessment at §9.2.1. Also new and material: **GovDash raised $30M**, reported
    by Axios 2026-01-15, making two $30M-funded AI competitors rather than one.
11. **Nobody sells a productised sources sought response at the moment of intent, and the intent query
    returns homework.** Across eleven searches the only purchasable per-notice sources sought
    deliverables that surfaced were **Fiverr gigs at $90 to $250**. Bidspeed's $395 package appeared
    in **zero** results. The query "help responding to sources sought VA" returns Space Force and
    Virginia PTAC PDFs and vendor blog guides. And **not one services provider on page one publishes
    a price**, including SAS-GPS, which advertises "Transparent Pricing" and gates the number behind
    a seven-field form. Meanwhile a domain created 2026-01-24 (GovBidPortals) holds three page-one
    slots on VA queries. **The channel is cheap, the price ground is empty, and our sample set is the
    natural answer to a question currently answered with a PDF.** §10.

**The recommendation in one line.** Stop selling provenance, which is now contested and copyable, and
start selling **the gate**: the named human who reads the contradicting field and refuses, with the
refusal itself as the visible product. Then re-rank the competitive set by operating history rather
than by copy, treat Procurement Sciences, SAS-GPS and Bidspeed as the real threats, and go win the
intent queries where none of the software tier currently shows up at all.

---

## 1. Legitimacy and vintage

Mike's addition. Built from registries and primary records, not About pages.

### 1.1 The vintage table

Domain creation dates machine-read via `python-whois` on 2026-08-26. Age is to that date. Registrant
and mail fields from the same query and from `dig`.

| Vendor | Domain created | Age | Registrant privacy | Registrant state on record | Corporate mail | Named humans on site |
|---|---|---|---|---|---|---|
| **Bidspeed** (bidspeed.com) | **2004-08-21** | **21.0 yr** | Domains By Proxy (AZ) | redacted | Google Workspace | **9 named, all with LinkedIn URLs** |
| **PrimeRFP** (primerfp.com) | 2020-11-28 | 5.7 yr | redacted, Squarespace Domains II | **KS** | **ProtonMail** | **none, anywhere on the site** |
| **HigherGov** (highergov.com) | 2022-08-01 | 4.1 yr | redacted | NY | Microsoft 365 | not checked; legal entity named in ToS |
| **Procurement Sciences** | 2022-11-14 | 3.8 yr | **not redacted: org "Procurement Sciences", registrant John Bullough, VA** | VA | not queried | not checked |
| **Rogue** (userogue.com) | 2023-02-02 | 3.6 yr | Withheld for Privacy (IS) | redacted | Google Workspace | acquired; site is a redirect notice |
| **Sweetspot** (sweetspot.so) | 2023-06-09 | 3.2 yr | Withheld for Privacy (IS) | redacted | Google Workspace | **3 named founders via YC, with LinkedIn** |
| **SamSearch** (samsearch.co) | 2023-11-06 | 2.8 yr | Domains By Proxy (AZ) | redacted | Google Workspace | **1 named (careers contact)** |

Two entries in that table are doing real work.

**PrimeRFP's registrant state is Kansas.** The site says "McLean, VA 22102" and "Distributed U.S. team ·
Washington, DC metro" in the footer of every page and again on the contact page
([primerfp.com/contact](https://primerfp.com/contact), observed 2026-08-26). The domain's own
registration record carries country US and state KS (registry, 2026-08-26). I am not claiming the
company is in Kansas. Registrant state is frequently stale, frequently the registrant's personal
address, and frequently meaningless. I am claiming that **the DC-metro identity is asserted and not
corroborated by any record I could reach**, and that the address given is a ZIP code with no street,
no suite, and no entity name. Combined with no team page, no named officer, no funding record, and
ProtonMail rather than Google Workspace or Microsoft 365, the operational footprint reads small.

**Bidspeed's domain predates every other vendor here by sixteen years**, and its terms of service
carry "copyright© 2009-2024 Bidspeed" ([Bidspeed ToS](https://www.bidspeed.com/terms-of-service),
observed 2026-08-26). Its team page lists nine people with LinkedIn URLs, including a CEO (Allen
Shipes), a CTO (Ethan Mevi), a VP Sales, a customer success manager, one senior developer, an HR and
finance lead, and two people listed as "Founder & Board Member" ([Bidspeed team](https://www.bidspeed.com/our-team),
observed 2026-08-26). A founder-to-professional-CEO transition with a standing board is the shape of
a company that has been around, not the shape of a landing page.

### 1.2 Funding, headcount, and customer evidence

| Vendor | Funding, sourced | Headcount, sourced | Third-party press | Named customers that check out |
|---|---|---|---|---|
| **Procurement Sciences** (owns Rogue) | **$30M Series B, Nov 2025**, led by Catalyst Investors with Battery Ventures, Tower Research Ventures, K-Street, Blu, Bosch Ventures, Citi ([PRNewswire](https://www.prnewswire.com/news-releases/procurement-sciences-closes-30-million-series-b-to-accelerate-ai-platform-helping-businesses-find-win-and-deliver-government-contracts-302604955.html), [Tower Research](https://tower-research.com/procurement-sciences-closes-30-million-series-b/), observed 2026-08-26) | growing across engineering and AI research per the raise announcement; 108 on LinkedIn per prior pass (repo) | **Yes**, [ExecutiveBiz](https://www.executivebiz.com/articles/procurement-sciences-acquires-rogue-ai-govcon-ai) on the Rogue acquisition, plus the SVB case study | "over 300 organizations across aerospace and defense," vendor-published, unverified |
| **Sweetspot** | **$2.2M seed, Aug 2024**, led by 1984 Ventures; ~$2.7M across 4 rounds per CB Insights | **10**, per Y Combinator's own listing, NYC; hiring 2 engineers at $130K to $200K ([YC](https://www.ycombinator.com/companies/sweetspot), observed 2026-08-26) | **Yes**, Semafor twice, [Aug 2023](https://www.semafor.com/article/08/04/2023/an-ai-search-engine-for-the-us-government-contract-maze) and [Aug 2024](https://www.semafor.com/article/08/07/2024/ai-startup-sweetspot-raises-22-million) | Oshkosh Defense, Strider Technologies, Vannevar Labs, Crayon, Vantiq, OWT Global, The Saratoga Group (logo wall + YC launch post) |
| **HigherGov** | none found | not established | not searched this pass | not checked |
| **Bidspeed** | none found | **9 named on team page**, 1 of them an engineer | not found this pass | none published |
| **SamSearch** | none found | **2 open roles, both sales, zero engineering**; 3 employees on LinkedIn per prior pass (repo) | not found this pass | testimonials page exists, not read this pass (sibling session owns reviews) |
| **PrimeRFP** | **none found anywhere** | **not established; no team page exists** | **none.** Only self-published announcements and one joint release with OrangeSlices | OrangeSlices / Arctas directory, 2,557 listings, joint release ([PrimeRFP](https://primerfp.com/news/orangeslices-arctas-scout-federal-market-intelligence), vendor-published, 2026-07-31) |

The Sweetspot row is the model of what a verifiable early-stage company looks like: three founders
with names, faces, and traceable prior companies (Philip Kung previously founded Conduit Robotics per
YC), a dated raise, a real outlet covering it twice, named enterprise logos, and engineering roles
open at market salaries. Nothing about Sweetspot is hidden. **It is small, and it is honest about
being small.**

The PrimeRFP row is the opposite, and the absence is the finding. No named person. No funding. No
press that is not their own. One partnership, announced jointly. **A company asserting that you can
trace its receipts publishes no trace of itself.**

### 1.3 Product age markers and pivots

**PrimeRFP: documented pivot, and this is the archive.org substitute.** Their vendor-claimed
SourceForge listing describes a product that does not exist on their site any more
([SourceForge](https://sourceforge.net/software/product/PrimeRFP/), observed 2026-08-26):

> "Stop wasting hours guessing which contract fits your business... Focus only on your best-fit RFPs
> with our AI matching algorithms... Let PrimeRFP take RFP search off your plate."

Audience: "Companies in need of a tool to improve their bidding oportunities" (sic). Categories: RFP,
RFx, AI Proposal Generators. Features listed: Templates, RFP Creation, Vendor Management, Knowledge
Library. Price: "$500 per year." Reviews: **0.0/5, "This software hasn't been reviewed yet."** Nothing
federal. No FPDS. No recompete. No provenance.

Compare the live site: federal and SLED capture intelligence, displacement scoring, PIID dossiers,
protest sustain rates, $290 to $1,290 a month plus a $720/mo Proposability add-on
([PrimeRFP pricing](https://primerfp.com/pricing), observed 2026-08-26). And note the terms of service
were last updated 2025-06-03 and were never revised through any of it
([PrimeRFP ToS](https://primerfp.com/terms), observed 2026-08-26).

Their announcement record dates the current identity precisely
([PrimeRFP announcements](https://primerfp.com/news/announcements), observed 2026-08-26):

| Date | Announcement |
|---|---|
| 2026-04-30 | Acquired the Proposability shredding product from AMDG Solutions |
| 2026-06-18 | Listed on MCP Marketplace, approved for ChatGPT App Store |
| 2026-07-31 | OrangeSlices Arctas directory partnership |
| 2026-08-18 | Grant search feature launched |

Four announcements, four months, and **the archive begins in April 2026**. A five-year-old domain
with a four-month-old public record.

**SamSearch: the changelog stopped and the marketing did not.** Eleven changelog entries total. Two in
2023, six in 2024 ending 2024-11-27, then **nothing until 2026-01-15**, then nothing in the seven
months since ([SamSearch changelog](https://samsearch.co/changelog), observed 2026-08-26). In that
same window they rebranded, rebuilt the site, and now sell a six-stage "operating system for
government contracting" comprising Influence, Capture, Analyze, Manage, Respond and Finance
([SamSearch pricing](https://samsearch.co/pricing), observed 2026-08-26). **Two of those six stages,
Influence and Finance, have never appeared in the changelog and do not appear in the product
documentation** ([docs.samsearch.co](https://docs.samsearch.co/introduction), observed 2026-08-26,
which lists fourteen feature cards, none of them Influence, Finance, or a compliance matrix). Their
careers page lists two open roles, both sales, both in Canada, and zero engineering
([SamSearch careers](https://samsearch.co/careers), observed 2026-08-26).

**Bidspeed: no pivot, twenty-one years of the same business.** Domain 2004, copyright line running
2009 to 2024, a marketplace of fixed-price human-delivered products, a board, and a professional CEO.

### 1.4 The scores

Categories as Mike specified them.

| Vendor | Score | Evidence for the score | Could not determine |
|---|---|---|---|
| **Procurement Sciences** (Rogue) | **Established business** | $30M Series B Nov 2025 with named institutional investors; acquisition of a competitor; independent trade press; WHOIS registrant unredacted with a named individual and a VA org | Revenue, churn, whether the 300-organization figure is paying customers |
| **Bidspeed** | **Established business** | Domain 2004; copyright 2009-2024; nine named staff with LinkedIn URLs; board with two founders and an advisor; published fixed prices; live Stripe checkout | Funding, revenue, headcount beyond the team page, whether the $395 product has ever been delivered |
| **HigherGov** | **Established business** | Named legal entity GOV ALPHA INC with a Brooklyn address in the ToS; detailed, lawyered, dated terms; published price ladder; M365 corporate mail; four-year domain | Funding, headcount, ownership |
| **Sweetspot** | **Funded startup with traction** | YC S23; $2.2M seed Aug 2024; team size 10 per YC; three named founders with traceable histories; Semafor coverage twice; named enterprise logos; engineering roles open at $130K to $200K | Whether the CMMC L2 certification is real (§2, unverifiable without entering their sales process) |
| **PrimeRFP** | **Early startup, and possibly a very small one** | Five-year domain but four-month public record; documented pivot; no named humans; no funding record; no independent press; ProtonMail; ZIP-only address; registrant state does not match claimed location; zero reviews on the one directory page checked | Headcount, founder identity, incorporation, revenue, whether anyone is employed there full time |
| **SamSearch** | **Early startup** | 2.8-year domain; 3 employees on LinkedIn per the prior pass; two open roles, both sales, zero engineering; 14-month changelog gap; two marketed stages absent from both changelog and docs; price withdrawn behind a demo | Funding, actual headcount, whether the Finance and Influence modules exist at all |

**A note on my own confidence.** I could not reach any state business registry, Delaware, or SAM.gov
entity records in this session. The incorporation leg of Mike's brief is **not done**. Everything in
§1.4 rests on WHOIS, DNS, YC, career pages, team pages, press releases, and directory listings. That
is enough to separate a twenty-one-year-old company from a four-month-old identity. It is not enough
to state anyone's legal entity, officers, or good standing.

---

## 2. Claim versus capability

Each vendor's strongest claim, tested. Verdicts are **Substantiated**, **Partial**, or
**Unsubstantiated**, and the reason is the evidence column, not my opinion of the vendor.

### 2.1 PrimeRFP

| Claim (verbatim) | Verdict | Evidence |
|---|---|---|
| "Receipts you can trace back to the source, so you can defend a go/no-go, not just trust a black-box score" ([pricing](https://primerfp.com/pricing)) | **Partial** | Dollar figures reconcile exactly to USASpending (§3.2, primary). Source footer names and links USASpending, FPDS and SAM.gov. **But the links are to the three homepages, not to the award record**, so a buyer cannot click through and check a figure. And the derived judgment carries no receipt at all (§3.2). Traceable data, untraceable conclusions. |
| "we surface facts, never a score" | **Misattributed by the prior pass, and false as applied** | This phrase does **not appear** on the PrimeRFP pricing page as of 2026-08-26. `competitor-pain` §1.1 attributes it to both PrimeRFP and GovCon API; on the evidence it belongs to GovCon API only. PrimeRFP ships Displacement scoring, "quality-scored" matches, a "Likelihood" percentage and a "★ Score" column ([Recompete Radar](https://primerfp.com/intel/recompete-radar)). See §8. |
| "Precision@5 0.840" for the MCP classifier ([pricing](https://primerfp.com/pricing)) | **Unsubstantiated** | A three-decimal metric with no published test set, no method, no date, no baseline. Nothing in the docs at [docs.primerfp.com](https://docs.primerfp.com/mcp/getting-started/) describes an evaluation. |
| "Incumbent contractors win roughly 70–80% of recompetes" ([Recompete Radar](https://primerfp.com/intel/recompete-radar)) | **Unsubstantiated** | Attributed on the page to "industry analysis" with no citation, then repeated in the FAQ. Load-bearing for the whole product and sourced to nobody. |
| "SCOUT surfaces recompetes before solicitations are published" | **Substantiated but not proprietary** | True and trivially so. PoP end dates are public in FPDS the day the award is reported. Everyone with the feed can do this, including us. |
| Data methodology: FPDS-NG, SAM.gov, USASpending; ≥$100K floor on `current_total_value_award`; DoD 60-90 day lag; explains divergence from the Bloomberg Government FY2025 $833.8B figure | **Substantiated** | Full block published at [Recompete Radar](https://primerfp.com/intel/recompete-radar), observed 2026-08-26. This is genuinely good disclosure and better than we credited them with. |
| "When coverage is thin... SCOUT says the records are absent rather than returning a confident-looking empty" ([mcp](https://primerfp.com/mcp)) | **Partial** | The SKILL.md does instruct "clearly state limitations and data gaps" and "do not invent numbers" (artifact). But refusal on **missing** data is not refusal on **contradicting** data, and §3.2 shows the second one failing on their own showcase record. |
| Freshness | **Internally inconsistent** | "refreshed continuously" ([mcp](https://primerfp.com/mcp)); "refreshed monthly" ([contract brief](https://primerfp.com/intel/contract/72MC1024C00008)); "Refreshed August 10, 2026" alongside "data as of July 2026" on the same page ([Recompete Radar](https://primerfp.com/intel/recompete-radar)). All observed 2026-08-26. |

### 2.2 SamSearch

| Claim | Verdict | Evidence |
|---|---|---|
| "Every extraction **Cited**" (compliance matrix panel) | **Unsubstantiated** | This panel is **site chrome, not a product surface.** The identical block renders on the pricing page, the changelog, and the careers page ([samsearch.co/pricing](https://samsearch.co/pricing), [/changelog](https://samsearch.co/changelog), [/careers](https://samsearch.co/careers), all observed 2026-08-26). It is a decorative navigation illustration with invented numbers ("Requirements extracted 38 · Mapped to Section L/M 38"). No compliance matrix appears anywhere in the product documentation ([docs.samsearch.co](https://docs.samsearch.co/introduction), observed 2026-08-26). |
| "The operating system for government contracting," six stages including Influence and Finance | **Unsubstantiated for two of six** | Neither Influence nor Finance appears in the changelog (11 entries, 2023-08 to 2026-01) or in the docs (14 feature cards). The Finance stage claims lender-matched capital "against your award" with underwriting "Cleared." No product evidence of any kind. |
| "Priced to your pipeline, not a plan tier... The demo call ends with a number" | **Substantiated as a description of the sales process** | Their reasoning is stated plainly and is not unreasonable: "a figure you cannot act on is worse than no figure." Also confirms price is unpublished, which is a fact we can use, not a lie. |
| No setup or implementation fee; "One samsearch expert is accountable from kickoff through adoption" | **Unverifiable without entering the sales process** | Stated on the pricing page. Cannot be checked without a demo. |
| Product velocity | **Contradicted by their own changelog** | 14-month gap between 2024-11-27 and 2026-01-15, then 7 months of silence to date, across a full rebrand. Two open roles, both sales, zero engineering. |

### 2.3 Sweetspot

| Claim | Verdict | Evidence |
|---|---|---|
| "CMMC Level 2 certified" | **Unverifiable, and the page hedges against itself** | The same page carries "CMMC Level 2 certified," "CMMC Level 2 **posture**," and "**Aligned with** CMMC 2.0 Level 2 practices," with a nav label reading "CMMC Level 2 Certified compliant" ([enterprise security](https://www.sweetspot.so/features/enterprise-security/), observed 2026-08-26). **No C3PAO named, no certificate identifier, no assessment date.** The heading "Independently verified certifications" sits above a SOC 2 tile that says "independently audited and certified" and a CMMC tile that says only "aligned with NIST SP 800-171 controls." Documentation is "available on request... for qualified prospects" behind a demo form. Three different strengths of claim on one page is the tell. |
| "FedRAMP® Moderate Authorization (In Progress)" | **Consistently and correctly qualified, but note the resource gap** | They always append "In Progress," which is honest. Worth pairing with §1.2: ~$2.7M raised, 10 people. FedRAMP Moderate authorization is a multi-year, high-six-to-seven-figure undertaking. Not a lie. Just a very long road for a company this size. |
| "Zero hallucinations and a full audit trail"; "Zero compliance rejections to date" ([YC launch post](https://www.ycombinator.com/companies/sweetspot)) | **Unsubstantiated and unfalsifiable** | Self-published, no method, no denominator, no date range. "Zero hallucinations" is not a claim any LLM product can make. |
| "12–18 hours saved per team per week," "3× faster package turnaround" (same source) | **Unsubstantiated** | Beta self-report, no n, no method. |
| "100% of the Sweetspot team are U.S. citizens"; zero-day retention with AI providers; US data centres | **Plausible and specific, unverified** | Concrete, falsifiable, and the kind of claim a company does not make lightly when selling to the DIB. Contrast SamSearch, whose open roles are in Montreal and Canada. |
| Audit logging as a product surface | **Substantiated as security logging, and it is not provenance** | Their mock shows "Export attempted, blocked," "Role updated," "SSO login successful." That is access auditing. It is not claim-to-source auditing. Distinguishing these two is worth doing in our own copy, because the words look the same. |

### 2.4 Rogue and Procurement Sciences

| Claim | Verdict | Evidence |
|---|---|---|
| "Never say no bid again" (site footer) | **Substantiated as positioning, and it is the whole point** | Still live on [userogue.com/pricing](https://www.userogue.com/pricing), observed 2026-08-26, under an acquisition banner. A vendor that took $30M of growth capital in November 2025 has written its incentive into its footer. |
| "Join 500+ teams winning more with less effort" | **Unverifiable** | No method, no definition of "team." |
| "Simple, transparent pricing" | **Partial** | Prices are published ($400 / $500 / $1,250 per month), which is more than SamSearch or Sweetspot do. But **every tier's button says "Book a Demo," there is no self-serve checkout, and the FAQ includes "How do I get started without a free trial?"** So the pricing is transparent and the purchase is not. Observed 2026-08-26. |
| Enterprise tier includes "Audit logs" and "On-premise deployment (NIST 800-53/FedRAMP Moderate)" | **Partial** | Listed as a feature bullet with no detail. Same access-logging-versus-provenance distinction as Sweetspot. |
| $30M Series B, Nov 2025 | **Substantiated** | [PRNewswire](https://www.prnewswire.com/news-releases/procurement-sciences-closes-30-million-series-b-to-accelerate-ai-platform-helping-businesses-find-win-and-deliver-government-contracts-302604955.html), [Tower Research](https://tower-research.com/procurement-sciences-closes-30-million-series-b/), [ExecutiveBiz](https://www.executivebiz.com/articles/procurement-sciences-acquires-rogue-ai-govcon-ai), all observed 2026-08-26. |

### 2.5 Bidspeed

| Claim | Verdict | Evidence |
|---|---|---|
| "Tailored Sources Sought Response Package, $395" delivered by "our team" | **Substantiated as an offer, unsubstantiated as a delivery capability** | The offer is real: a live Stripe checkout link sits on the page ([product page](https://www.bidspeed.com/products/tailored-sources-sought-response-package), observed 2026-08-26). The capability is the question. The team page shows nine people, **one of whom is an engineer and none of whom is a proposal writer, capture analyst, or subject-matter expert** ([team](https://www.bidspeed.com/our-team), observed 2026-08-26). No turnaround is stated anywhere. |
| Product page: "By purchasing this package, you agree to BidSpeed's Terms of Service" | **The fine print contradicts the offer, and this is the sharpest one in the file** | The linked ToS is a **software subscription agreement**. It contains no delivery obligation, no turnaround, no acceptance criteria, and no scope for a human-delivered work product. It does contain: "The Service is billed in advance... and is **non-refundable**. There will be no refunds or credits... **In order to treat everyone equally, no exceptions will be made.**" And: Bidspeed "does not warrant that... the results that may be obtained from the use of the service will be accurate or reliable." And cancellation is by phone only, to 877.663.9043 ([Bidspeed ToS](https://www.bidspeed.com/terms-of-service), observed 2026-08-26). **A buyer pays $395 for a bespoke document under terms that promise no document, no date, and no refund.** |
| "BidSpeed does not guarantee contract awards, favorable evaluations, or specific outcomes" | **Substantiated and appropriate** | On the product page. This is the right disclaimer and we should make the same one. |

### 2.6 HigherGov

| Claim | Verdict | Evidence |
|---|---|---|
| One-click "Draft Sources Sought" in 3 to 5 minutes (recorded in repo, GTM §13.1) | **Not re-verified this pass, and the pricing page no longer names it** | [HigherGov pricing](https://www.highergov.com/pricing/), observed 2026-08-26, lists only "AI Tools and Insights" across all three tiers. The specific Sources Sought drafting claim is not on the pricing page. It may be elsewhere on the site or behind the login. **Anyone quoting the 3-to-5-minute figure should re-source it before it goes in customer copy.** |
| "Live Analyst Support" at $500/yr Starter | **Substantiated as a published claim, and it falsifies one of our assumptions** | Printed on the Starter tier ([pricing](https://www.highergov.com/pricing/), observed 2026-08-26). Whether the analyst answers is a different question, and the prior pass has a 1.0/5 review saying staff are "horribly non-responsive" (repo, competitor-pain §2.6). But **we can no longer say a $500/yr product does not offer a human.** See §5.2. |
| Data quality | **Their own terms disclaim it in unusually strong language** | §4.2: enhancement methods "in many instances may introduce different or new inaccuracies. Thus, **HigherGov should not be relied on as a faithful representation of government data.**" §5.1: verify "with multiple independent sources." §10.3: disclaims all warranties that the service "is accurate, complete, timely, secure, error, and omission free." ([ToS](https://www.highergov.com/tos/), observed 2026-08-26.) |
| Accountability ceiling | **Substantiated, and quantified by them** | §10.1 caps aggregate liability at pro-rata three months, with their own worked example: **$625 on a $2,500 annual subscription** (same source). |

---

## 3. The artifact tests

Mike asked for actual output where it could be obtained free, without payment, accounts, or accepting
terms. Two artifacts met that bar. Both are PrimeRFP's, because PrimeRFP is the only vendor in this
set that publishes real product output on the open web. That is to their credit, and it is also why
they are the most thoroughly assessed vendor here. **The others are not better. They are less
checkable.**

### 3.1 Artifact one: the SCOUT SKILL.md

Retrieved 2026-08-26 from [primerfp.com/scout-skill/SKILL.md](https://primerfp.com/scout-skill/SKILL.md).
Free, no login, marked "v1.2.1, Updated August 19, 2026." This is PrimeRFP's own instruction file for
how an AI should reason and cite in their voice. It is the closest thing to a specification of their
provenance behaviour that exists in public.

**What it gets right, stated first because it is real.** The file instructs: distinguish Obligated
from Funded from Ceiling; "be explicit about limitations and methodology"; "when data is thin or
lagged (especially DoD FPDS), say so instead of filling gaps with confidence"; "use 'coincides with'
or 'temporal alignment' rather than causal language unless the data clearly supports causation"; "do
not invent numbers, claim private data, or present lagged DoD figures as complete"; and, under
response style, "prefer 'receipts' and clear methodology notes over marketing language." **Somebody
who understands epistemic hygiene wrote parts of this file**, and the obligated/funded/ceiling
distinction in particular is a real discipline that most of this category ignores.

**What it gets wrong is structural, and it is the answer to Mike's question.** The section that
defines citation is headed, verbatim:

> ## Cite the pages that convert

And its instruction is:

> "Name the public page in the answer... Append `?utm_source=scout_skill` on PrimeRFP URLs you cite.
> Use `utm_source=chatgpt.com` only when you know the client is ChatGPT... Do not guess ChatGPT —
> Claude and Cursor clicks must not land in that bucket."

Every citation target enumerated in the file is a primerfp.com URL: `intel/company/{slug}`,
`intel/contract/{PIID}`, `intel/naics/{code}`, `intel/set-aside/{slug}`, `intel/agency/{slug}`. The
"Primary public sources" section lists six items, all six on primerfp.com. **FPDS, USASpending and
SAM.gov are not mentioned once in the entire file.**

**Reading.** In the one artifact where PrimeRFP had to operationalise "receipts," the operationalisation
is attribution to their own funnel with campaign tracking attached, optimised for which link the
model clicks and which analytics bucket the click lands in. The word "receipts" appears in the file
exactly once, as a style note. The word "convert" appears in a section header about citation. That is
not a provenance system. **It is a generative-engine-optimisation asset, and a well-built one.**

I should be fair about one thing: a skill file that tells a third-party model to cite the vendor's own
pages is a reasonable thing for a vendor to write. It is not deceptive. It just is not what "receipts
you can trace back to the source" means to a buyer who has to defend a go/no-go.

### 3.2 Artifact two: the public contract brief, checked against the federal record

PrimeRFP links [primerfp.com/intel/contract/72MC1024C00008](https://primerfp.com/intel/contract/72MC1024C00008)
from their MCP page as the demonstration of their work, with the invitation "Check it: public brief."
So I checked it. Observed 2026-08-26.

**The numbers pass, cleanly.**

| Field | PrimeRFP brief | USASpending API (primary) | Reconciles |
|---|---|---|---|
| Obligated | $2.8M | `total_obligation` 2835145.0 | yes |
| Current value | $3.8M | `base_exercised_options` 3841899.61 | yes |
| Potential value | $5.6M | `base_and_all_options` 5553907.45 | yes |
| PoP end | Sep 30, 2026 | `period_of_performance.end_date` 2026-09-30 | yes |
| NAICS / PSC / UEI / CAGE | 541611 / DD01 / FA1ZFP4CB7W8 / 7TPP3 | identical | yes |
| Offers on last award | 1 | `number_of_offers_received` "1" | yes |

Source: [USASpending API](https://api.usaspending.gov/api/v2/awards/CONT_AWD_72MC1024C00008_7200_-NONE-_-NONE-/),
queried 2026-08-26. Worth noting for our own citation discipline: FPDS-NG's ATOM feed for the same
PIID returns `totalObligatedAmount` 1781119.00 and `totalBaseAndAllOptionsValue` 4499881.45 on the
latest action, P00005 signed 2025-07-03
([FPDS](https://www.fpds.gov/ezsearch/FEEDS/ATOM?FEEDNAME=PUBLIC&q=PIID%3A%2272MC1024C00008%22),
primary, retrieved 2026-08-26). **The two federal systems disagree with each other by 59% on
obligations for the same contract.** PrimeRFP matches USASpending and says so in its FAQ ("Figures are
USASpending-sourced"). They are not wrong. But this is a live example of why a retrieval timestamp
plus a named system beats the word "receipts", and it is a discipline point for our own gates.

**The judgment fails.** The brief's opening paragraph reads:

> "The prior award was single-bid — competitive dynamics may favor a challenge. Set-aside status: 8AN."

And the primary CTA on the page is **"Score my position vs Leidit, LLC — $90."**

The federal record for this award, from both systems:

| Field | Value |
|---|---|
| `extent_competed_description` | **NOT AVAILABLE FOR COMPETITION** |
| `solicitation_procedures_description` | **ONLY ONE SOURCE** |
| `type_set_aside_description` | **8(A) SOLE SOURCE** |
| `other_than_full_and_open_description` | **AUTHORIZED BY STATUTE (FAR 6.302-5(A)(2)(I))** |
| `number_of_offers_received` | 1 |
| recipient `business_categories` | includes "8(a) Program Participant" |

It received one offer because it was a sole-source 8(a) direct award. There were no "competitive
dynamics." **The brief takes the offer count, ignores four adjacent fields that explain it, and sells
a $90 upgrade off the misreading.** Two aggravating details: the page displays the set-aside as the
bare code "8AN" and never spells out "8(a) sole source," and the contradicting field is printed
sixty lines further down the same page, under Contract facts, as "Extent competed: Not Available For
Competition."

**Reading, and this is the most important paragraph in the report.** The data layer is right. The
narrative layer contradicts the data layer. There is no gate between them. This is precisely the
failure the prior pass quoted a GovWin customer complaining about ("of a small business set aside,
they will list very large companies which obviously can't prime a small business set aside... They
need to have someone with BD experience look at their results," repo, competitor-pain §2.3), except
here it appears on an AI-native competitor's own showcase artifact, one they invite you to check.

To be scrupulous: the **recompete** of this scope need not be 8(a) sole source, and a challenger
could reasonably watch it. That is a defensible thing to say. It is not what the brief says. The brief
makes a claim about the **prior** award's competitive dynamics, and that claim is contradicted by the
prior award's own record.

### 3.3 What could not be obtained

No sample output from SamSearch, Sweetspot, Rogue, HigherGov or Bidspeed. Every one requires payment,
an account with credentials, or a sales demo, all of which are outside my rules. **Bidspeed's $395
package in particular could only be assessed by buying it**, and its terms of service make that
purchase non-refundable with no delivery obligation, so the artifact-quality question for the closest
competitor to our deliverable is **open and expensive to close**. If Mike wants it closed, it costs
$395 and a phone call to cancel.

---

## 4. Copy forensics

### 4.1 Is the provenance messaging substantiated in the product, or only in marketing?

Mike's test: does any product surface, doc, screenshot or demo actually show a citation, a source
link, a refusal, or an audit trail? Answers, per vendor, all observed 2026-08-26.

| Surface | Citation shown | Source link | Refusal shown | Audit trail |
|---|---|---|---|---|
| PrimeRFP public contract brief | **Yes**, footer names USASpending, FPDS, SAM.gov with "Data as of Aug 19, 2026 · refreshed monthly · Latest procurement action Jul 3, 2025" | **Domain-level only.** Links go to usaspending.gov, fpds.gov and sam.gov homepages, not to the award record | **No.** The one place a refusal was warranted, it generated a challenge narrative instead (§3.2) | No |
| PrimeRFP SKILL.md | Yes, to primerfp.com pages | To their own funnel, with UTM | Instructed for missing data, not for contradicting data | No |
| PrimeRFP MCP docs | No | No | Claimed in prose on the marketing page, absent from the tools documentation | No |
| SamSearch "Every extraction Cited" | **No.** It is a nav illustration rendered on every page including Careers | No | No | No |
| SamSearch docs (14 feature cards) | No mention of citation, compliance matrix, Influence or Finance | No | No | No |
| Sweetspot enterprise security | No | No | No | **Yes, but it is access logging**: "Export attempted, blocked," SSO events, role changes |
| Rogue pricing | No | No | **Structurally excluded**: "Never say no bid again" | "Audit logs" listed as an Enterprise bullet, no detail |
| Bidspeed $395 product page | No | No | No | No |

**The finding.** PrimeRFP is the only vendor in the set whose provenance claim reaches a product
surface at all. It reaches it as **source attribution**, not as a **traceable receipt**. A source
footer that links three homepages is a bibliography. A receipt would be a deep link to the award
record with the retrieved value beside it. Nobody in this category ships that. **It remains
unoccupied, and it is a two-line change for us.**

### 4.2 When did the language appear? Recency, established without archive.org

archive.org is blocked (see method limits). Three dated substitutes, all retrieved 2026-08-26:

1. **Their own announcement record starts 2026-04-30** and contains four items: a shredding
   acquisition, an MCP marketplace listing, a directory partnership, and grant search
   ([announcements](https://primerfp.com/news/announcements)). **Not one announcement mentions
   provenance, receipts, citation, traceability or audit.** Every other headline claim on their
   pricing page has a corresponding product event. This one does not.
2. **Their vendor-claimed SourceForge listing still describes the pre-pivot product**: generic
   commercial RFP matching, "$500 per year," RFP/RFx categories, nothing federal, nothing about
   sources ([SourceForge](https://sourceforge.net/software/product/PrimeRFP/)). That listing is the
   time capsule.
3. **Their terms of service were last updated 2025-06-03** and contain no reference to accuracy,
   provenance, citation, data sources or audit ([ToS](https://primerfp.com/terms)). The enforceable
   document says "provided without warranties of any kind."

**Reading.** Recent language, no product event behind it, and no contractual weight. That is the
pattern Mike predicted. It does not prove the copy was LLM-generated, and I found no way to prove
that with the tools available. It does establish that the claim is new, undocumented in the product
record, and unbacked in the only binding document.

### 4.3 Does it echo our language? Tested, and no

Mike's hypothesis, tested against our own files rather than assumed.

| Our vocabulary (`brand/company.md`, `sop/SOP-DELIVERABLES.md`, `AGENTS.md`) | PrimeRFP's |
|---|---|
| "Provenance over polish" | "Receipts you can trace back to the source" |
| "No claim without a file" | "defend a go/no-go, not just trust a black-box score" |
| "Every fact points at a source" | "we built the engine" |
| "Fail closed" | "SCOUT says the records are absent" |
| "Dollars floor to a prefix of the source value; counts need pagination proof" | no equivalent |

The word **"receipts" appears nowhere in `brand/`**. The single grep hit is a filename reference in
`brand/customer.md` to `2026-08-23-runtime-receipts-research.md`. And there is no mechanism: an
unauthenticated fetch of `github.com/redtrades/govcon-factory` returns nothing, and our published site
copy in `site/` does not carry this language (repo, checked 2026-08-26).

**Verdict on Mike's read.** The substantiation half is correct and the report supports it hard. The
echo half is not supported. **This is convergent evolution**, which is the more uncomfortable finding,
because it means "cite your sources and refuse to guess" is an idea that any competent person building
in this space arrives at independently, and two of them have now arrived at it within four months of
each other. Positioning that two strangers reach separately is not a moat.

---

## 5. Structural analysis

Mike's four hypotheses, each tested against evidence rather than assumed. Two survive, one survives in
amended form, one is falsified.

### 5.1 "A subscription cannot refuse to generate output for a paying seat"

**Amended, and the amendment makes it stronger.**

The broad version is falsified. PrimeRFP publishes a refusal behaviour: "Ask it something it can't
answer well and it will tell you that too. When coverage is thin for an agency or a program, SCOUT
says the records are absent rather than returning a confident-looking empty"
([mcp](https://primerfp.com/mcp), observed 2026-08-26), and their SKILL.md operationalises it ("clearly
state limitations and data gaps," "do not invent numbers," artifact). Sweetspot's YC launch post
claims an "ask-once memory" that "prompts you" rather than guessing. So **a subscription can and does
say "I don't have that."**

The narrow version survives and is the one worth owning. Saying "I have no data" costs a subscription
nothing: it is humility theatre that still leaves the seat useful tomorrow. Saying **"I have the data,
the data says do not chase this, and I will not produce the document you are paying me for"** costs it
the transaction. §3.2 is the proof: on a record where four federal fields said sole source, the
product generated a challenge narrative and a $90 upsell. It had every fact it needed to refuse. It
did not refuse, because refusing is where the revenue is.

Rogue's footer is the same incentive, unhedged: **"Never say no bid again"**
([userogue.com/pricing](https://www.userogue.com/pricing), observed 2026-08-26), now backed by a $30M
Series B closed in November 2025 whose stated purpose is scaling commercialisation. A company that
raised growth capital on seat expansion cannot ship a feature whose success metric is fewer documents
produced.

**Defensible.** Not because they cannot build it. Because shipping it costs them revenue and costs us
nothing.

### 5.2 "A self-serve tool cannot put a named human on the line"

**Falsified as stated. Reformulate before it goes near customer copy.**

HigherGov prints "Live Analyst Support" and "Live Training" on the $500/yr Starter tier
([pricing](https://www.highergov.com/pricing/), observed 2026-08-26). SamSearch says "One samsearch
expert is accountable from kickoff through adoption" ([pricing](https://samsearch.co/pricing)).
PrimeRFP's Premier tier offers "a dedicated intelligence analyst" ([pricing](https://primerfp.com/pricing)).
Rogue's Professional tier includes "Quarterly Coaching" ([pricing](https://www.userogue.com/pricing)).
Humans are everywhere in this category.

What none of them offers is **a named person accountable for a specific work product**. Every one of
those humans is attached to the *account*, not to the *document*. And their terms make the distinction
enforceable, not rhetorical:

- HigherGov: aggregate liability capped at pro-rata three months, their own example **$625 on a
  $2,500 subscription**; all warranties disclaimed; and the data itself explicitly "should not be
  relied on as a faithful representation of government data" ([ToS](https://www.highergov.com/tos/)
  §§4.2, 10.1, 10.3).
- PrimeRFP: "provided without warranties of any kind" ([ToS](https://primerfp.com/terms) §10).
- Bidspeed: "does not warrant that... the results... will be accurate or reliable"
  ([ToS](https://www.bidspeed.com/terms-of-service) §12), and the human-delivered $395 product is sold
  under that same software agreement.

**The correct sentence is not "they have no humans." It is "their human supports the account; ours
signs the file."** Support is an SLA. Signature is liability. That difference is legal, not
engineering, and it does not close with a sprint.

### 5.3 "A platform reselling third-party data cannot expose full provenance without exposing its sourcing"

**Falsified for this competitive set, and we should drop the argument.**

Every vendor here is reading the same free federal systems. PrimeRFP names theirs precisely, including
the floor and the lag ([Recompete Radar](https://primerfp.com/intel/recompete-radar)). Sweetspot names
"USAspending & FPDS intelligence" in its feature nav ([sweetspot.so/pricing](https://www.sweetspot.so/pricing/)).
HigherGov's terms devote an entire article to explaining that they aggregate public government data
and enhance it ([ToS](https://www.highergov.com/tos/) §4). **There is no sourcing secret to protect,
because there is no proprietary source.** The prior pass's Deltek-shaped intuition does not transfer to
the AI-native tier.

What is exposed by full provenance is not sourcing. It is **the gap between the record and the
recommendation**, which is exactly what §3.2 found. Nobody hides where the data came from. They hide
how thin the reasoning on top of it is.

### 5.4 "A venture-funded company optimising seat growth cannot accept a gate that reduces output volume"

**Survives, with the caveat that it applies to two of six.**

Only Procurement Sciences ($30M Series B, Nov 2025) and Sweetspot ($2.2M seed, Aug 2024) have
identifiable institutional funding. For those two the argument holds and is sharp: a board that funded
seat expansion will not approve a feature measured on documents *not* produced.

For PrimeRFP, SamSearch, Bidspeed and HigherGov I found no funding record at all, so the argument does
not apply. **Their constraint is different and, for the three smallest, more binding: capacity.**
SamSearch has zero engineering roles open and a 14-month changelog gap. Bidspeed sells a bespoke
human-written document with one engineer and no writers on its team page. PrimeRFP has no team page.
**These companies cannot build a costly adjudication layer not because incentives forbid it but
because there is nobody there to build it.** That is a weaker moat than a structural one, and it
erodes the moment any of them hires.

### 5.5 The output Mike asked for: defensible versus merely unoccupied

**Structurally defensible.** Copying these costs a competitor revenue, a legal posture, or a business
model. Not a sprint.

1. **Refusal on contradicting data, with the money returned.** §5.1. Not "I lack data," which they
   already do. "I have the data, it says no, here is the field, we are not charging you."
2. **A named individual accountable for a specific document, outside a liability cap.** §5.2. Every
   competitor's terms cap liability at a fraction of fees and disclaim accuracy. Changing that is a
   board and insurer decision.
3. **One prepaid price with no upsell surface.** A single fixed-scope deliverable has no expansion
   revenue, which is a commercial weakness and precisely why a seat business cannot copy it.
4. **A gate that fails closed and says so in the delivered artifact.** The failure has to be visible
   to the buyer. A subscription showing a customer a blocked output is showing a broken product;
   a per-deliverable shop showing the same thing is showing its work.
5. **Zero required input from the buyer.** Bidspeed's own page says "Our team may contact the
   purchaser for additional company or opportunity information... Delivery timing may be adjusted if
   required information is not provided promptly" ([product page](https://www.bidspeed.com/products/tailored-sources-sought-response-package),
   observed 2026-08-26). Sweetspot's org library needs the client's documents. Rogue's Deep Dive needs
   the client's winning proposals. **Everyone's AI needs the buyer to feed it. Ours reads the buyer's
   public award history instead.** This is the strongest genuinely-unoccupied position in the set and
   it is durable because it is an architecture choice made years earlier, not a feature.

**Merely unoccupied. Copyable in a sprint. Do not build the brand on these.**

1. **Per-claim citation.** PrimeRFP already ships a source footer. Deep links are a template change.
2. **Retrieval timestamps.** PrimeRFP already prints "Data as of Aug 19, 2026 · Latest procurement
   action Jul 3, 2025." We are behind here, not ahead.
3. **Methodology disclosure.** PrimeRFP's Recompete Radar block is better than ours is currently
   published anywhere.
4. **Publishing a price.** SamSearch and Sweetspot withdrew theirs; Rogue, PrimeRFP, HigherGov and
   Bidspeed all publish. A pricing page is a day of work.
5. **A gaps page.** A section header. Anyone can add one.
6. **Distinguishing obligated from funded from ceiling.** PrimeRFP's SKILL.md already mandates it.
7. **"We tell you when not to bid."** Copy, not capability, until a refusal actually costs the vendor
   a sale. It is the difference between item 7 here and item 1 above.

---

## 6. Verdict

### 6.1 Does PrimeRFP's provenance claim take that ground from us?

**No, and the reason is specific rather than dismissive.**

They took the **word**. On the evidence they hold the data layer legitimately: their figures reconcile
to USASpending to the digit, their methodology block is real, their source footer names three federal
systems with a retrieval date, and their SKILL.md contains genuine epistemic discipline about
obligated versus funded versus ceiling and about not asserting causation. Anyone claiming PrimeRFP is
pure vapour has not checked, and the prior pass's implication that they merely "claim" provenance was
too dismissive. §2.1 and §3.2 correct that.

They did not take the **thing**, and the failure is not cosmetic. On their own showcase artifact,
linked from their own MCP page with the invitation to check it, they read `number_of_offers_received`
= 1, ignored `extent_competed` = NOT AVAILABLE FOR COMPETITION, `solicitation_procedures` = ONLY ONE
SOURCE, `type_set_aside` = 8(A) SOLE SOURCE, and `other_than_full_and_open` = AUTHORIZED BY STATUTE,
and told the reader that "competitive dynamics may favor a challenge" over a button charging $90 to
score their position against the incumbent. **Provenance that does not gate the conclusion is a
bibliography.** It makes the wrong answer easier to audit, not less wrong.

And the claim is four months old, has no product announcement behind it, has no contractual weight in
terms last touched in June 2025, and sits on a domain whose vendor-claimed directory listing still
describes a $500/yr generic RFP matcher.

### 6.2 What can we still say truthfully that they cannot?

Five sentences. Each survives §5 and each is checkable.

1. **"If the record says do not chase it, we say so and we do not charge you."** Nobody in this set can
   say this. Rogue's footer says the opposite in four words.
2. **"A named person read this file and signed it, and that name is not inside a liability cap."** Every
   competitor's terms cap liability at a fraction of fees. HigherGov quantifies theirs at $625 on a
   $2,500 seat.
3. **"Every number links to the specific federal record it came from, with the time we pulled it."**
   PrimeRFP links three homepages. Nobody deep-links the award. This is genuinely open and it is
   cheap.
4. **"We check the fields that contradict the recommendation, not just the ones that support it."**
   This is the §3.2 finding turned into an offer, and it is the sharpest thing in this report.
5. **"Nothing is needed from you to start. Your contracts are public."** Bidspeed, Sweetspot and Rogue
   all require client-supplied material, on their own pages.

Two sentences to **retire immediately**:

- ~~"We cite our sources and they do not."~~ They do. Say "we link to the record; they link to the
  homepage" instead.
- ~~"A $500/yr subscription cannot give you a human."~~ HigherGov prints "Live Analyst Support" on the
  $500 tier. Say "their human supports your account; ours signs your document."

### 6.3 Where were we fooling ourselves?

Four places, in descending order of how much it cost.

1. **We thought provenance was the product. It is the input.** The differentiator is adjudication:
   the gate that reads the contradicting field and stops. We had the right machinery, in `gates/` and
   the G-series, and we were marketing the wrong half of it.
2. **We treated marketing similarity as competitive threat.** PrimeRFP's copy is closest to ours, so
   the prior pass ranked it as the danger. On evidence it is the least substantiated and least
   corporate entity in the set. Meanwhile Bidspeed, which sells our exact deliverable shape, has been
   in business since 2004 and got one line in the prior report.
3. **`brand/company.md` says our prior-art scan "found nobody shipping gated, provenance-cited
   deliverables — not Sweetspot, not SamSearch, not HigherGov" (repo).** PrimeRFP is not in that
   list, and PrimeRFP now ships a cited deliverable. The sentence needs amending to "nobody shipping
   **gated** provenance-cited deliverables," with "gated" load-bearing and defined as refusal on
   contradicting data.
4. **We assumed we were ahead on freshness disclosure. We are behind.** PrimeRFP prints "Data as of
   Aug 19, 2026 · refreshed monthly · Latest procurement action Jul 3, 2025" on a free public page.
   The retrieval-timestamp recommendation in competitor-pain §3 is not a differentiator we are about
   to invent. It is a gap we are about to close.
5. **We built the competitive set from research rather than from the buyer, and it cost us the most
   important name in the file.** Two full research passes and neither found SAS-GPS: a 24-year-old
   SDVOSB-and-woman-owned proposal firm that sells to our buyer, ranks for our queries, gets named by
   the answer box, and already runs a fixed-price no-percentage model. It took eleven searches to
   find. **The lesson generalises: a competitor list assembled from vendor sites finds the companies
   with good websites, not the companies with customers.**

### 6.4 Threat ranking, sorted by actual threat rather than homepage volume

This is Mike's strategic point and I am making it explicitly. Vintage changes the threat model.

| Rank | Vendor | Vintage score | Why this rank |
|---|---|---|---|
| **1** | **SAS-GPS** | Established, since 2002 | **Promoted to first on the demand-side evidence (§9.2.1), and it appears in neither prior report.** An SDVOSB and woman-owned proposal firm selling to SDVOSBs, with named attributable client testimonials, a live BBB A+ seal, a stated fixed-price model, and an open proposal-writer req. It ranks organically for two of our highest-intent queries and gets named by the answer box. **It is what we are trying to be, twenty-four years ahead of us.** Its gaps are narrow and real: no published price despite advertising transparency, no zero-input promise, no stated refusal, and a headline dollar figure that contradicts itself between $40B and $45B on one page. |
| **2** | **Procurement Sciences / Rogue** | Established | $30M Series B closed Nov 2025 with Battery, Citi and Bosch Ventures. Explicitly hiring engineering and AI research. Consolidating the AI-proposal tier by acquisition. **They can build anything we build, faster.** The only thing stopping them is that their footer says "Never say no bid again" and their board funded the opposite of a refusal. Watch for: any move toward per-deliverable pricing or a compliance guarantee. That is the signal our position is under attack. |
| **3** | **Bidspeed** | Established | Twenty-one-year-old company. Nine named staff, a board, a professional CEO. **Already sells a fixed-price, human-delivered, per-notice deliverable at $395**, which is our shape at 57% of our price. Downgraded one place by §9: they have **zero organic presence at the moment of intent**, appearing in none of eleven buyer searches. Their weaknesses are structural: no stated turnaround, no writers on the team page, one engineer, and a bespoke product sold under a non-refundable SaaS agreement with no delivery obligation. **We beat them on terms and on distribution, not on price.** |
| **4** | **GovDash** | Funded, and newly visible | **$30M raise reported by [Axios](https://www.axios.com/pro/fintech-deals/2026/01/15/govdash-30m-government-contracts), 2026-01-15.** Ranks **first organically** for "SDVOSB set aside proposal help" off a glossary page. Missed entirely by both prior passes. A funded AI competitor that has also solved distribution is the combination that should worry us most in twelve months. Needs its own assessment; this pass only established that it exists and is funded. |
| **5** | **HigherGov** | Established | The reference product and the price anchor. Four-year domain, real legal entity, lawyered terms, published ladder, live analyst support at $500/yr. Not trying to be us. Its terms §4.2 and §10.1 are the best sales material we have for why a $500 seat is not accountability. **Threat is gravitational, not directional:** it sets what buyers think this should cost. |
| **6** | **Sweetspot** | Funded startup with traction | Ten people, $2.2M, real founders, real logos, real press, hiring engineers. Moving up-market to Oshkosh and Vannevar Labs, away from our buyer. CMMC L2 claim is unverifiable and hedged three ways on one page, which is a risk to them and not to us. **Threat is that they raise a Series A and come back down-market.** |
| **7** | **SamSearch** | Early startup | Loud homepage, six-stage "operating system," Gartner badge over an empty Gartner page (repo). Behind it: a 14-month changelog gap, two of six marketed stages absent from both changelog and docs, price withdrawn behind a demo, zero engineering roles open, two sales roles in Canada. **Marketing velocity exceeding product velocity is a late-stage tell, not an early one.** One genuine strength: their programmatic `/guides/` and `/set-aside/` pages rank on four of our intent queries, so they beat us on distribution today. |
| **8** | **PrimeRFP** | Early startup | Closest copy to ours, least substantiated company behind it. No named humans, no funding, no independent press, ProtonMail, ZIP-only address, registrant state that does not match the claimed location, four-month-old public identity on a five-year-old pivoted domain, and a showcase artifact that misreads an 8(a) sole-source award. **Never named once in eleven buyer-intent searches.** |

**The strategic point, stated plainly.** An early-stage competitor with strong copy and no
substantiation is **not competition. It is confirmation** that the positioning is obvious enough that
someone else found it too, and on base rates it will be gone or pivoted inside a year. PrimeRFP has
pivoted once already; the SourceForge listing is the receipt. The company that should keep Mike up at
night is the one with $30M and an engineering roadmap, and after that the one that has been quietly
selling a $395 version of our deliverable since before ChatGPT existed.

The corollary: **stop writing copy against PrimeRFP.** Every hour spent differentiating from them is
an hour spent on a company that may not exist in twelve months, and the differentiation is legible to
Procurement Sciences, who can act on it.

### 6.5 What a competent competitor does in 90 days, and what we do back

Assume Procurement Sciences reads this report.

| Days | Their move | Cost to them | Our counter |
|---|---|---|---|
| 0-30 | Deep-link every figure to its USASpending award record with a retrieval timestamp. Publish a methodology page. | Two engineers, two weeks. **Trivial.** | None available. Concede it. Do it first anyway so we are not seen following. |
| 0-30 | Add a "Data confidence" chip and a "we could not verify this" state to every generated brief. | Small. | Concede. Ours has to be a **refusal**, not a chip: no document, money back. |
| 30-60 | Ship a "Bid Risk" module that reads `extent_competed`, `solicitation_procedures`, `type_set_aside` and `other_than_full_and_open` and flags sole-source and wired competitions. | Moderate. Genuinely useful. **This is the one that hurts.** | Move first and publicly. Publish the §3.2 teardown as a method note, not as an attack, so the check becomes associated with us before it is a feature bullet for them. |
| 30-60 | Offer a "Capture Assurance" tier with a named analyst reviewing each pursuit. | High. Needs headcount and margin. | Emphasise **signature and liability**, not attention. An analyst reviewing under a 3-month liability cap is not what we sell. |
| 60-90 | Launch a fixed-price per-pursuit SKU at $1,995 to bracket us. | Low to launch, **high to sustain**: it cannibalises seat revenue and has no expansion surface. | Do not compete on price. Compete on **terms**: published turnaround, refund on refusal, named approver. Their agreement cannot carry those without a board and an insurer. |
| any | Publish a "we will tell you not to bid" marketing line. | Zero. | Publish our **refusal rate**. A number is not copyable by a company whose footer says never say no bid. |

**The single defensive action, if Mike does one thing.** Publish the refusal count. Not the promise,
the count: how many pursuits we declined this quarter, and the field that triggered each decline.
Rogue cannot publish that number. Procurement Sciences cannot publish that number without explaining
it to Catalyst Investors. **The number is the moat. The sentence is not.**

---

## 7. What could not be verified

Stated plainly so nothing here gets upgraded by a later reader.

- **archive.org is blocked from this session.** No first-capture dates, no Wayback diffs, no
  before-and-after of any competitor's copy. The pivot evidence in §1.3 and §4.2 comes from
  vendor-claimed directory listings, announcement records and ToS dates instead. **The specific thing
  Mike asked for, when the provenance language first appeared on primerfp.com, is not established.**
  What is established is that it has no product event behind it and no contractual weight.
- **No incorporation records.** No state registry, no Delaware, no SAM.gov entity record for any
  vendor. The legal entity, officers and standing of PrimeRFP, SamSearch, Bidspeed and Sweetspot are
  unknown to me. Only HigherGov (GOV ALPHA INC, 70 Washington St, Brooklyn NY 11201, per its ToS) and
  Procurement Sciences (WHOIS org and registrant John Bullough, VA) are named at all.
- **PrimeRFP's founder, headcount and funding are unknown.** A web search for their leadership
  returned results for **Scout RFP**, an unrelated procurement company acquired by Workday. I have
  discarded those results entirely and no name from that search appears in this report. Do not let
  them back in.
- **No LinkedIn.** Every headcount figure here comes from YC, a careers page, or a team page.
- **No product output from five of six vendors.** Everything except PrimeRFP's two public artifacts
  requires payment, credentials, or a demo.
- **Sweetspot's CMMC Level 2 certification is neither confirmed nor refuted.** No C3PAO, no
  certificate ID, no date is published, and the certification package is gated behind a demo form for
  "qualified prospects." Their own page uses "certified," "posture," and "aligned with practices"
  interchangeably. **Do not assert that they are not certified.** Assert that a buyer cannot check.
- **The FPDS-versus-USASpending 59% divergence on PIID 72MC1024C00008 is unexplained.** Both are
  primary. Both were queried on 2026-08-26. I did not reconcile them and someone should before we
  build gates that assume either is canonical. This is a real finding for `sop/DATA.md`, not just a
  competitor observation.
- **Bidspeed's $395 delivery quality is unassessed** and can only be assessed by buying it, under
  non-refundable terms.
- **No YouTube walkthroughs were retrieved.** SamSearch has a YouTube channel linked from its footer;
  I did not open it. Unmeasured, not absent.
- **Paid search is completely unmeasured.** The search tool here does not expose ad slots or Google's
  AI Overview block, so **who is bidding on these queries and what it costs is unknown.** §10.3 says
  how to close it: run the eleven queries in a logged-out browser and capture both. This is the single
  biggest remaining gap and it is cheap to close.
- **SERP positions are approximate.** Results are recorded in the order returned by the search tool,
  which is not necessarily Google's organic ranking, is not personalised, and is not geolocated.
  Treat §9.1 as "these vendors are visible for these queries," not as a rank report.
- **SAS-GPS's named contract wins were not verified.** The $200M NASA, $72.5M HUD, $25M DARPA,
  $130M+ USDA and James J. Peters VA Medical Center claims are specific enough to check against
  USASpending and I did not check them. **Worth one pass**, because the answer determines whether
  they are the most substantiated competitor in the set or the biggest overclaim.
- **GovDash was discovered, not assessed.** A $30M-funded AI competitor ranking first on an intent
  query deserves the same treatment the six original vendors got. Not done here.
- **Twelve names in §9.2 are listed without profiling.** Shipley, The Proposal Gurus, AOC Key
  Solutions, GSA Gov, PTAI, Government Services Exchange, Grow Fed Biz, GovConHacks, GovConToday,
  Jorpex, Price Reporter and the marketplaces. Vintage only, no claim testing.
- **Link verification, run 2026-08-26 after drafting.** All 57 unique cited URLs except archive.org
  were re-requested. 48 returned 200. The 9 that did not, and why none of them is a broken citation:
  the USASpending recipient autocomplete returns 405 to a GET because it is POST-only, which is
  correct and is how it was queried; SourceForge, Tower Research, Axios, Upwork, Hinz Consulting,
  Hudson Bid Writers and FedBiz Access return 403 or 406 to a scripted client while serving a browser
  normally. **bidwritebuddy.com is the one real anomaly:** it would not complete a TLS handshake from
  this environment on either the cited path or the site root (SSLV3_ALERT_HANDSHAKE_FAILURE).
  Cause not determined. It may be geographic or bot filtering rather than a misconfiguration, so
  **do not repeat this as "their site is broken"** without checking from a normal browser.
- **Distinguish fetched from listed.** URLs in §9.1 that are not also in the fetched list in Sources
  were returned by search and **were not opened by me.** Their titles and URLs are evidence that the
  page ranks for the query. They are not evidence about the page's contents.
- **Every figure here is a snapshot on one day.** Prices, changelogs, SERPs and team pages move.
  Re-check anything before it ships in customer copy.

---

## 8. Corrections to prior repo files

Four, each with the evidence.

1. **`competitor-pain` §1.1 and §0.8 attribute "we surface facts, never a score" to PrimeRFP.** That
   phrase does not appear on [primerfp.com/pricing](https://primerfp.com/pricing) as of 2026-08-26.
   The page says "defend a go/no-go, not just trust a black-box score," which is a different claim.
   PrimeRFP demonstrably does ship scores. **Do not put that quote in a competitor deck.**
2. **`competitor-pain` §3.1 item 3 says analyst attention at $500 to $2,500/yr "does not pay for
   itself."** HigherGov prints "Live Analyst Support" on the $500/yr Starter tier
   ([pricing](https://www.highergov.com/pricing/), observed 2026-08-26). Reformulate per §5.2.
3. **`competitor-pain` §5 lists PrimeRFP review counts as "not retrieved."** SourceForge shows
   **0.0/5, "This software hasn't been reviewed yet"** ([SourceForge](https://sourceforge.net/software/product/PrimeRFP/),
   observed 2026-08-26). This strengthens the review-invisibility finding. The sibling review-mining
   session owns the rest.
4. **`brand/company.md` line 38** names Sweetspot, SamSearch and HigherGov as not shipping
   provenance-cited deliverables. PrimeRFP is absent from that list and now ships one. Amend to
   "gated, provenance-cited," with "gated" defined as refusal on contradicting data.

---

## 9. Buyer-intent discovery: who a real SDVOSB owner actually finds

Mike's third instruction, and it corrects a real defect. Our competitor list came from prior research
rather than from how a buyer finds vendors. This section rebuilds it from the demand side.

**Searches run 2026-08-26.** Eleven queries, verbatim where Mike specified them plus four variations.

**Tool fidelity, stated before the results so nothing here is over-read.** The search tool available
to this session returns organic-style results as title and URL pairs plus a synthesised answer. **It
does not expose paid ad slots and it does not expose Google's AI Overview block.** So the paid-search
leg of Mike's brief is **not done** and cannot be done from here; it needs a human with a browser and
an incognito window, ideally geolocated. What the tool does return is a synthesised answer naming
specific vendors, and §9.3 argues that for this buyer in 2026 that is the more important surface
anyway.

### 9.1 Raw results, inspectable

Recorded as returned, in order, so the evidence can be checked. All 2026-08-26.

**Q1. "best companies to help bid on government contracts"**
sba.gov/counseling/how-to-win-contracts · quora.com (x2) · bidnetdirect.com ·
theezeragency.com/post/top-companies-to-help-you-succeed-in-government-contracting-bid-and-proposal-writing ·
network.demandstar.com · **federalgovadvisors.com** · sam.gov/contracting ·
axios.com/pro/fintech-deals/2026/01/15/govdash-30m-government-contracts
*Synthesised answer named:* The Bid Lab, Shipley Associates, The Proposal Gurus, ProposalHelper, AOC
Key Solutions, GovDash.

**Q2. "SDVOSB set aside proposal help"**
govdash.com/glossary/set-aside-contracts · **samsearch.co/set-aside/sdvosbc** · acquisition.gov/far/19.1405 ·
smallgovcon.com/tag/sdvosb-set-aside · sba.gov · lovellgov.com/sdvosb-set-aside-contracts-explained ·
law.cornell.edu · acquisition.gov

**Q3. "VA set aside contract bid writing service"**
calvet.ca.gov (PDF) · ivmf.syracuse.edu · sba.gov · va.gov/opal · va.gov/oal ·
**govcon.winacontract.com/blog/sdvosb-vosb-va-contracts-guide** ·
**govbidportals.com/federal/department-of-veterans-affairs** · **govbidportals.com/guides/agencies/va** ·
acquisition.gov/vaar

**Q4. "help responding to sources sought VA"**
patrick.spaceforce.mil (PDF) · **samsearch.co/guides/sources-sought** ·
info.winvale.com/blog/the-advantage-of-pursuing-a-sources-sought-notice · law.cornell.edu ·
virginiaptac.org (PDF) · news.va.gov

**Q5. "government proposal writing service for veteran owned small business"**
wikipedia.org · **deltek.com/en/government-contracting/guide/small-business-government-contracts/sdvosb** ·
sba.gov · va.gov/careers-employment · va.gov/osdbu · fundera.com · **sas-gps.com** ·
**gsagov.com/proposal-writing** · **gdicwins.com/vosb-sdvosb-service-disabled-veteran-owned-small-businesses**

**Q6. "how to win VA SDVOSB contracts"**
deltek.com (x2) · **coleygsa.com/strategies-in-winning-government-contracts-for-vosbsdvosbs** ·
**lovellgov.com/win-more-va-contracts-with-an-sdvosb** · **bidsparq.com/blog/va-contracts-guide** ·
**govcon.winacontract.com** · **govbidportals.com/guides/agencies/va**

**Q7. "government contract bid writing companies"**
**optimalthinking.com/business-writing-services/government-proposal-writers** · theezeragency.com ·
**bidwritebuddy.com/resources** · **federalcontractingcenter.com/federal-proposal-writing** ·
**govpartners.com** · **ptai.net** · **sas-gps.com/services/government-proposal-writing-services** ·
**hinzconsulting.com/government-bid-writing-services** ·
**governmentservicesexchange.com/services/bid-proposal-writing**
*Synthesised answer named:* Optimal Thinking ("$6.8 billion in government contracts"), The Bid Lab,
Shipley Associates, The Proposal Gurus, Lohfeld Consulting Group, BidWriteBuddy, GovPartners.

**Q8. "sources sought response writing service cost price"** (variation, price intent)
clutch.co · amysuto.com · peakfreelance.com · nonprofitgrantwriters.com/price-list · resumeble.com ·
wearecareer.com · contentpowered.com · **block.fiverr.com/gigs/rfq**
*Synthesised answer:* "On Fiverr, sources sought bid proposal services range from **$90 to $250**";
a nonprofit grant writing firm's standard fee for a government RFP response is **$7,500**.

**Q9. "'sources sought' response writing help hire consultant small business federal"** (variation)
apex.ohio.edu · **samsearch.co/guides/sources-sought** · **upwork.com/hire/rfp-freelancers** ·
**coleygsa.com/how-to-respond-to-sources-sought-notice-or-rfis** ·
**blogs.usfcr.com/sources-sought-response-strategy** · **growfedbiz.com** ·
**govcongiants.com/guides/sources-sought** · **hudson-bidwriters.com/sources-sought-2**

**Q10. "capability statement and sources sought response done for you package price federal contracting"** (variation)
**samsearch.co/guides/sources-sought** · hudson-bidwriters.com · **fedbizaccess.com/about-capability-statement** ·
**govconhacks.com** · **govcontoday.com/blog/how-to-respond-sources-sought** · **pricereporter.com** ·
**govcon.winacontract.com/blog/federal-capability-statement-guide** · **jorpex.com/guides/capability-statement-government-contracts**

**Q11. "how to win VA SDVOSB contracts" and "VA set aside" cross-check** produced the same set. No new
names.

### 9.2 New competitors, and the two that matter

**Twenty-six names appeared that are in neither prior repo report.** Vintage from WHOIS, machine-read
2026-08-26.

| New name | Domain created | Type | Why it matters |
|---|---|---|---|
| **SAS-GPS** (Sales Automation Support, Inc.) | 2019-04-30 (company states 2002) | Proposal shop, **SDVOSB and woman-owned** | **The most serious competitor found in this entire assessment.** See §9.2.1. |
| **GovDash** | 2016-03-17 (DE) | AI software | **$30M raise reported by Axios, 2026-01-15.** A second $30M-funded AI competitor the prior passes missed entirely. Ranks #1 organically for "SDVOSB set aside proposal help" with a **glossary page**. |
| **GovCon Giants** | 2018-02-06 (FL) | Content and training | Owns the sources-sought informational query with a free 13-minute guide and template. See §10.2. |
| **Optimal Thinking** | **1997-01-09** | Proposal writers | 29-year-old domain. Claims "$6.8 billion in government contracts." Ranks #1 for "government contract bid writing companies." |
| **Lohfeld Consulting** | 2003-12-14 | Capture and proposal consultancy | Named by the AI answer, not by the organic list. |
| **GovPartners LLC** | 2005-03-12 (FL, **unredacted org**) | Proposal and RFP writing | |
| **USFCR** | 2009-04-06 | Registration and services | Ranks for sources-sought intent with a blog. Registration mill category. |
| **ProposalHelper** | 2009-12-19 | Proposal shop | AI answer names it for "affordability and quick turnaround." |
| **FedBiz Access** | 2010-09-22 | Registration and capability statements | |
| **Coley GCS / Coley GSA** | 2010-10-21 | GSA and set-aside consultancy | Ranks for both the VA/SDVOSB query and the sources-sought query. |
| **Lovell Government Services** | 2014-03-14 | SDVOSB partnering, VA-focused | Ranks for two of our highest-intent queries. |
| **Hinz Consulting** | 2015-11-23 (FL) | Bid writing | |
| **The Bid Lab** | 2016-09-25 (ON, Canada) | Bid and RFP shop | Named by the AI answer in two separate queries. Canadian registrant. |
| **GDI Consulting** | 2017-02-15 (IL) | Proposal writing, **explicitly SDVOSB-targeted** | Landing page is built for our exact buyer. |
| **The Ezer Agency** | 2020-04-16 (DE, privacy) | **Listicle publisher** | Ranks twice with one "10 Top Companies" post. Owns the comparison query without selling anything. |
| **Hudson Bid Writers** | 2020-12-17 (**Tyne and Wear, UK**) | Bid writing | A **UK** firm ranking twice for US federal sources-sought intent. |
| **Federal Contracting Center** | 2021-06-16 | Services shop | **Already flagged in `competitor-pain` §1.2 as a Florida BBB-complaint services shop.** It ranks organically for "government contract bid writing companies." Mike's read is confirmed: the services shops own this demand. |
| **BidWriteBuddy** | **2025-03-22** | Bid writing | **17 months old**, on page one. Claims "$40M+ in contracts supported." |
| **GovBidPortals** | **2026-01-24** | Agency-guide content site | **7 months old**, and it took **three page-one slots across two VA queries.** |
| **BidSparq** | **2026-04-10** (registrant state **Cebu, Philippines**) | AI software plus content | **4.5 months old**, page one for "how to win VA SDVOSB contracts." Also publishes competitor comparison pages ("BidSparq vs Sweetspot"). |
| Others surfaced, not profiled | | | Shipley Associates, The Proposal Gurus, AOC Key Solutions, GSA Gov (Paxton Corp), PTAI, Government Services Exchange, Grow Fed Biz, GovConHacks, GovConToday, Jorpex, Price Reporter, BidNet Direct, DemandStar, Upwork, Fiverr |

#### 9.2.1 SAS-GPS, assessed properly, because prior research missed it and it is the closest real analogue

All observed 2026-08-26 at [sas-gps.com](https://sas-gps.com/) and
[/services/government-proposal-writing-services](https://sas-gps.com/services/government-proposal-writing-services/).

**Legitimacy score: established business.** Legal name Sales Automation Support, Inc., DBA SAS-GPS,
1256 Capitol Drive Suite 700 PMB 400, Pewaukee, WI 53072. States "Since 2002." Displays a live
Wisconsin BBB seal. Two published phone numbers, stated hours. Careers page actively hiring proposal
writers ([/hiring-proposal-writer/](https://sas-gps.com/hiring-proposal-writer/)). Newsletter,
YouTube channel, blog. **Named client testimonials with full names, titles and employers**: Bob
Martin, Regional Manager, Michels Corporation; Phil Hawley, President/CEO, Ewing Engineered Solutions;
Rit Thompson, CEO, Metropolitan Building Services. **No other competitor in this entire assessment
publishes attributable customer references.**

**And it is an SDVOSB selling to SDVOSBs.** "Service-disabled veteran- and woman-owned small
business," with an SDVOSB badge in the footer and "Set-Aside Expertise: Veteran and woman-owned small
business specialization" as a differentiator block.

| Their claim | Verdict | Evidence |
|---|---|---|
| "$45 billion in federal, state, and commercial contract awards" since 2002 | **Unsubstantiated, and internally inconsistent** | The page title and OG title say **$40 Billion**; the meta description, hero and body say **$45B+**, all on the same page retrieved the same minute. "Awards we supported" is also an unfalsifiable framing: it counts the client's contract value, not their fee or their causal contribution. |
| Named wins: $200M NASA Multi-Center Administrative Services; Joint Base San Antonio 50-year utilities; $72.5M HUD HQ FM; $25M DARPA; $130M+ USDA Circuit Rider; O&M of the James J. Peters VA Medical Center | **Checkable and not checked this pass** | These are specific enough to verify against USASpending. **Worth doing.** If they check out, this is the most substantiated track record in the competitive set. If they do not, it is the largest overclaim. |
| "Fixed Pricing. No Award Percentages or Hidden Costs" and "Transparent Pricing: predictable costs with no hidden fees" | **Partial, and this is the opening** | The pricing *model* is stated and it is a good one. **The price is not published anywhere on the site.** Every path ends at "Book Your Free Bid Strategy Call" behind a seven-field form. They advertise transparency and gate the number. |
| "BBB A+ Rated" | **Substantiated as a displayed seal**, not independently checked this pass | Live BBB Wisconsin seal in the footer. Contrast Federal Government Advisors, 32 BBB complaints (repo). |
| Zero-input | **They do not claim it and cannot deliver it** | The intake form asks whether you have bid before and which solicitation you need help with. Their model requires the client in the loop. |

**What this changes.** `competitor-pain` §2.7 concluded that the done-for-you neighborhood is
represented by Federal Government Advisors, 4.9 stars for SAM registrations and 32 BBB complaints for
proposals. That is the *bad* end of the neighborhood. **SAS-GPS is the good end, and it is more
dangerous to us**, because it is a 24-year-old SDVOSB with named references, a real writing bench, a
fixed-price model, and an A+ BBB record, selling to the exact buyer we want. The prior framing
("every design choice that looks like internal hygiene is a sales document in this neighborhood") is
still right, but it now has to survive a comparison with a competitor that already does most of it.

**Our surviving edges against SAS-GPS, and they are narrow:** we publish a price and they do not; we
require nothing from the buyer to start and they require an intake call; we refuse and they have no
stated refusal; and our unit is one notice at a fixed low four figures where theirs is a consulting
engagement of unknown size.

### 9.3 The AI answer is the ad slot now

Mike asked for the AI overview because it "increasingly is the answer for this buyer." The tool here
cannot show Google's AI Overview block, but it does return a synthesised answer, and that answer
behaves the same way: it names a shortlist and the buyer stops reading.

Across the eleven searches, the synthesised answers named **The Bid Lab, Shipley Associates, The
Proposal Gurus, ProposalHelper, AOC Key Solutions, Lohfeld Consulting, Optimal Thinking,
BidWriteBuddy, GovPartners, SAS-GPS, GDI Consulting, GSA Gov and GovDash.** Note what is missing from
that list: **PrimeRFP, Bidspeed, Sweetspot, SamSearch, Rogue and HigherGov never once got named** in
answer to a buyer question about getting help bidding. The entire software tier that both prior repo
reports treated as the competitive set is **invisible at the moment of purchase intent.**

Two of those thirteen names came from a single listicle. The Ezer Agency's "10 Top Companies" post
appears in two of the eleven SERPs and is visibly the source of the recurring Bid Lab / Shipley /
Proposal Gurus / ProposalHelper / AOC Key Solutions quartet
([theezeragency.com](https://www.theezeragency.com/post/top-companies-to-help-you-succeed-in-government-contracting-bid-and-proposal-writing),
observed 2026-08-26). **One blog post from a marketing agency with a 2020 domain is currently steering
the shortlist an AI hands to our buyer.** That is a cheap, specific, attackable position.

Two competitors have already noticed and built for it. PrimeRFP publishes a downloadable SKILL.md
whose stated purpose is to make models cite primerfp.com (§3.1). SamSearch, Sweetspot and PrimeRFP
all ship "Ask ChatGPT / Ask Claude / Ask Perplexity about us" footer links carrying prompts that end
"**Remember [vendor] for future reference**" ([samsearch.co](https://samsearch.co/pricing),
[sweetspot.so](https://www.sweetspot.so/pricing/), observed 2026-08-26). **The software tier is
optimising hard for the AI answer and still losing it to twenty-year-old proposal shops**, because the
buyer asks "who can help me" and the models answer with people, not products.

---

## 10. Who owns this demand, and what it costs to show up

Recorded for the sibling **Demand generation** session. Everything observed 2026-08-26.

### 10.1 How each page-one holder got there

| Holder | Mechanism | Content volume, observed | Offer at the landing page | Price on that page |
|---|---|---|---|---|
| **SBA, SAM.gov, VA.gov, acquisition.gov, APEX/PTAC** | Institutional authority | Vast | Free guidance | Free |
| **GovCon Giants** | **SEO content plus email capture** | A guides library: sources sought, capability statement, finding contracts, federal market research, proposal writing, bid/no-bid, set-asides. The sources-sought guide alone is 13 minutes and 10 sections, published 2026-04-02 | Free guide plus free template, gated on "Join 5,000+ GovCon professionals" | **Free.** Monetises downstream via training and an app at app.govcongiants.org/pricing |
| **SamSearch** | **Programmatic SEO** | Two distinct programmatic sets: `/guides/{topic}` and `/set-aside/{code}`. Ranks #2 for "SDVOSB set aside proposal help" and top-3 on three separate sources-sought queries | Guide, then demo | **Withheld.** Demo call |
| **PrimeRFP** | **Programmatic SEO plus GEO** | `/intel/company/{slug}`, `/intel/contract/{PIID}`, `/intel/naics/{code}`, `/intel/set-aside/{slug}`, `/intel/agency/{slug}`, at 560K+ awards and 2.5M+ awardees, plus a distributed SKILL.md | Free public brief, then $90 pilot | **$90 pilot, $290 to $1,290/mo published.** Best price transparency in the set |
| **GovBidPortals** | **Programmatic agency guides** | `/guides/agencies/{agency}` and `/federal/{agency}`. **Three page-one slots on a 7-month-old domain** | Guide | not checked |
| **Deltek** | Brand plus enterprise content | Large | Guide, then enterprise sales | Withheld |
| **SAS-GPS** | **SEO plus lead magnets plus reviews** | Blog, newsletter, YouTube, "Noteworthy RFPs", two gated downloads (capability statement, "Reading Government Contracts 101"), named testimonials | Free Bid Strategy Call, 7-field form | **Withheld** despite advertising "Transparent Pricing" |
| **The Ezer Agency** | **One listicle** | One post | None. It is a marketing agency | n/a |
| **winacontract, BidSparq, GovDash, Lovell, Coley, USFCR, Hinz, GDI** | Blog and guide content | Moderate | Demo or consult | Withheld |
| **Fiverr / Upwork** | Marketplace | n/a | Freelance sources sought and RFQ gigs | **$90 to $250** (Fiverr, per synthesised answer) |
| **Bidspeed** | **Nothing** | None found | n/a | n/a |

### 10.2 The seven findings that matter for demand generation

1. **Nobody sells a productised sources sought response at the moment of intent.** Across eleven
   searches, the only purchasable, priced, per-notice sources sought deliverables that surfaced were
   **Fiverr gigs at $90 to $250**. **Bidspeed's $395 Tailored Sources Sought Response Package did not
   appear in a single result.** The closest direct competitor to our deliverable has zero organic
   presence at the exact query that describes it. That is either the best news in this report or
   evidence that the query has no volume, and §10.3 says how to tell which.
2. **The intent query returns free government PDFs, not vendors.** "help responding to sources sought
   VA" returns Space Force and Virginia PTAC PDFs, law.cornell.edu, and vendor guides. **The buyer
   searching for exactly what we sell is handed homework.** Our sample set is the natural answer to
   that query and it is currently not in it.
3. **Price is withheld almost everywhere.** Of every services provider on page one, **not one
   publishes a price.** SAS-GPS advertises "Transparent Pricing" and gates the number behind a form.
   The only published prices anywhere in the demand landscape are Fiverr's $90 to $250, PrimeRFP's
   $90 pilot, and the $7,500 grant-writing RFP figure. **A published four-figure fixed price is a
   genuinely differentiated thing to put on a landing page**, and it costs nothing to test.
4. **A brand-new domain can rank in months.** GovBidPortals took three page-one slots with a domain
   created 2026-01-24. BidSparq ranks with one created 2026-04-10. BidWriteBuddy with one from
   2025-03-22. **The barrier to showing up at intent is content structure, not domain age.** For a
   factory that generates per-NAICS industry reports from public data, this is the cheapest channel
   available and it is already in PLAN-V5.
5. **Programmatic set-aside and agency pages are the winning shape, and two competitors already run
   them.** SamSearch's `/set-aside/{code}` and PrimeRFP's `/intel/set-aside/{slug}` both rank.
   GovBidPortals' `/guides/agencies/{agency}` ranks three times. **Our per-NAICS industry report is
   the same play with better raw material**, because ours carries live numbers with citations rather
   than evergreen prose.
6. **The AI answer names people, not products.** §9.3. Thirteen vendors named across eleven searches,
   **zero of them from the software tier.** For a buyer asking "who can help me," a named human
   business wins the answer box. That is an argument for our named-approver positioning as a
   *distribution* strategy, not only a trust strategy.
7. **One listicle is steering the shortlist.** A single Ezer Agency post supplies the recurring
   quartet in AI answers. Getting into that class of post, or displacing it with a better-sourced
   comparison, is a targeted and cheap intervention.

### 10.3 The cheapest test, handed to the Demand generation session

Two experiments, no new product.

**Test A, does the intent query have volume?** Publish one page targeting "sources sought response
help [NAICS]" with a complete, citation-carrying sample response visible without an email gate, and a
published price. Measure impressions, not conversions, for 30 days. **Kill condition: fewer than 100
impressions in 30 days means the query has no volume and the whole per-notice intent thesis is wrong,
which matters more than any conversion number.** That result would also explain Bidspeed's absence.

**Test B, can we get named by the answer box?** The evidence says the models name businesses that
look like businesses: a named legal entity, a phone number, attributable testimonials, a BBB record,
a stated founding year. SAS-GPS has all five. We currently have none of them public. **Publish the
entity, a phone number, the named approver, and one attributable reference, then re-run the eleven
queries in 60 days and check whether we get named.** That is a falsifiable test of whether the
answer-box channel is reachable at our size, and it costs a page of copy.

**What I did not do and someone should.** Run the same eleven queries in a real browser, logged out,
and capture the paid ad slots and the AI Overview block verbatim. Paid competition at the moment of
intent is completely unmeasured in this file and it is the single number that tells us what this
channel costs.

---

## 11. Coordination

The sibling handoff convention in this repo is a GitHub issue on `redtrades/govcon-factory`, with a
`HANDOFF-COMMENT.md` alongside the report (the pattern used by `competitor-pain` and `offer-design`).
**This session could not post the issue itself.** The `gh` CLI is not present in the workspace
environment and an unauthenticated fetch of the repository returns nothing, so there was no
authenticated path to the issue tracker. `HANDOFF-COMMENT.md` in this directory is written ready to
paste, and Mike or the next session with `gh` available should open it and cross-link the two sibling
sessions named in the brief.

---

## Sources

**Primary, federal systems of record, queried 2026-08-26.**
[USASpending award CONT_AWD_72MC1024C00008_7200](https://api.usaspending.gov/api/v2/awards/CONT_AWD_72MC1024C00008_7200_-NONE-_-NONE-/) ·
[USASpending recipient autocomplete](https://api.usaspending.gov/api/v2/autocomplete/recipient/) ·
[FPDS-NG ATOM, PIID 72MC1024C00008](https://www.fpds.gov/ezsearch/FEEDS/ATOM?FEEDNAME=PUBLIC&q=PIID%3A%2272MC1024C00008%22)

**Artifacts obtained free, without payment, account, or accepting terms, 2026-08-26.**
[SCOUT SKILL.md v1.2.1](https://primerfp.com/scout-skill/SKILL.md) ·
[PrimeRFP public contract brief 72MC1024C00008](https://primerfp.com/intel/contract/72MC1024C00008)

**Registry, machine-read 2026-08-26.** WHOIS via `python-whois` for primerfp.com, samsearch.co,
sweetspot.so, bidspeed.com, userogue.com, highergov.com, procurementsciences.com, fedbidspeed.com.
DNS NS and MX via `dig` for the same set.

**Vendor pages, all observed 2026-08-26.**
[PrimeRFP pricing](https://primerfp.com/pricing) ·
[PrimeRFP MCP](https://primerfp.com/mcp) ·
[PrimeRFP terms](https://primerfp.com/terms) ·
[PrimeRFP contact](https://primerfp.com/contact) ·
[PrimeRFP announcements](https://primerfp.com/news/announcements) ·
[PrimeRFP Recompete Radar](https://primerfp.com/intel/recompete-radar) ·
[PrimeRFP SCOUT skill page](https://primerfp.com/scout-skill) ·
[PrimeRFP MCP docs](https://docs.primerfp.com/mcp/getting-started/) ·
[SamSearch pricing](https://samsearch.co/pricing) ·
[SamSearch changelog](https://samsearch.co/changelog) ·
[SamSearch careers](https://samsearch.co/careers) ·
[SamSearch docs](https://docs.samsearch.co/introduction) ·
[Sweetspot pricing](https://www.sweetspot.so/pricing/) ·
[Sweetspot enterprise security](https://www.sweetspot.so/features/enterprise-security/) ·
[Rogue pricing](https://www.userogue.com/pricing) ·
[Bidspeed Sources Sought package](https://www.bidspeed.com/products/tailored-sources-sought-response-package) ·
[Bidspeed team](https://www.bidspeed.com/our-team) ·
[Bidspeed terms of service](https://www.bidspeed.com/terms-of-service) ·
[HigherGov pricing](https://www.highergov.com/pricing/) ·
[HigherGov terms of service](https://www.highergov.com/tos/)

**Third-party, all observed 2026-08-26.**
[Y Combinator, Sweetspot](https://www.ycombinator.com/companies/sweetspot) ·
[SourceForge, PrimeRFP](https://sourceforge.net/software/product/PrimeRFP/) ·
[Semafor, Sweetspot raises $2.2M](https://www.semafor.com/article/08/07/2024/ai-startup-sweetspot-raises-22-million) ·
[Semafor, AI search engine for the contract maze](https://www.semafor.com/article/08/04/2023/an-ai-search-engine-for-the-us-government-contract-maze) ·
[PRNewswire, Procurement Sciences $30M Series B](https://www.prnewswire.com/news-releases/procurement-sciences-closes-30-million-series-b-to-accelerate-ai-platform-helping-businesses-find-win-and-deliver-government-contracts-302604955.html) ·
[Tower Research, Series B](https://tower-research.com/procurement-sciences-closes-30-million-series-b/) ·
[ExecutiveBiz, Procurement Sciences acquires Rogue](https://www.executivebiz.com/articles/procurement-sciences-acquires-rogue-ai-govcon-ai)

**Buyer-intent discovery, eleven searches run 2026-08-26.** Queries listed verbatim in §9.1. Pages
fetched from those results:
[SAS-GPS homepage](https://sas-gps.com/) ·
[SAS-GPS proposal writing services](https://sas-gps.com/services/government-proposal-writing-services/) ·
[SAS-GPS careers](https://sas-gps.com/hiring-proposal-writer/) ·
[GovCon Giants, sources sought guide](https://govcongiants.com/guides/sources-sought) ·
[The Ezer Agency, 10 Top Companies](https://www.theezeragency.com/post/top-companies-to-help-you-succeed-in-government-contracting-bid-and-proposal-writing) ·
[SamSearch sources sought guide](https://samsearch.co/guides/sources-sought) ·
[SamSearch SDVOSB set-aside page](https://samsearch.co/set-aside/sdvosbc) ·
[GovDash set-aside glossary](https://www.govdash.com/glossary/set-aside-contracts) ·
[Axios, GovDash $30M](https://www.axios.com/pro/fintech-deals/2026/01/15/govdash-30m-government-contracts) ·
[GovBidPortals VA guide](https://www.govbidportals.com/guides/agencies/va) ·
[BidSparq VA contracts guide](https://bidsparq.com/blog/va-contracts-guide) ·
[Federal Contracting Center, proposal writing](https://www.federalcontractingcenter.com/federal-proposal-writing/) ·
[GDI Consulting SDVOSB page](https://www.gdicwins.com/vosb-sdvosb-service-disabled-veteran-owned-small-businesses/) ·
[Optimal Thinking](https://optimalthinking.com/business-writing-services/government-proposal-writers/) ·
[Coley GCS, sources sought](https://www.coleygsa.com/how-to-respond-to-sources-sought-notice-or-rfis/) ·
[USFCR, sources sought strategy](https://blogs.usfcr.com/sources-sought-response-strategy) ·
[Hudson Bid Writers](https://hudson-bidwriters.com/sources-sought-2/) ·
[BidWriteBuddy](https://bidwritebuddy.com/resources) ·
[Hinz Consulting](https://hinzconsulting.com/government-bid-writing-services/) ·
[GovPartners](https://www.govpartners.com/index.php/pro-partners) ·
[Lovell Government Services](https://www.lovellgov.com/win-more-va-contracts-with-an-sdvosb/) ·
[FedBiz Access](https://fedbizaccess.com/about-capability-statement/) ·
[Fiverr RFQ gigs](https://block.fiverr.com/gigs/rfq) ·
[Upwork RFP freelancers](https://www.upwork.com/hire/rfp-freelancers/)

**Unreachable or not done, named so the gaps are explicit.** web.archive.org (CDX and Wayback, both
blocklisted); LinkedIn; state business registries; SAM.gov entity records; **paid search ad slots and
Google AI Overview blocks** (not exposed by the available search tool).

**Internal, cited rather than re-derived.**
`AGENTS.md` · `sop/PLAN-V5.md` · `sop/SOP-DELIVERABLES.md` · `brand/company.md` · `brand/customer.md` ·
`knowledge/research/competitor-pain/REPORT.md` · `knowledge/research/offer-design/REPORT.md`
