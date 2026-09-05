# Willingness-to-pay evidence notebook — Pollen (@Research)

> **Plan-version note, added 2026-08-23 after the fact.** This file was written against
> `sop/PLAN-V5.md`. **`origin/main` had already superseded V5 with `sop/PLAN-V6.md`** before this
> council convened; our branch forked at the V5 commit and never fetched. Every measurement below
> is of the world or of the repo and is unaffected — V5 is cited only to say what a plan claimed,
> never as authority. Where a V5 reference appears, check V6 first: V6 tightened several of the
> same gates and, on the points this file measures, V6 is generally better supported. Specifically
> V6 §2 sets the packet quality floor at ~50% Covered+Partial, which is stronger than the 40% this
> council debated and which the live packet test below independently supports.
> **Companion file.** `2026-08-23-runtime-receipts-research.md` holds the runtime receipts, notice-fit funnel, the live packet test, and the `skills/` sweep. Cite that file for any window, funnel, fill-rate or extract figure.


Captured 2026-08-23. Companion to `2026-08-23-willingness-to-pay-research.md`.
This file holds raw pulls, method, dead ends, and findings that did not make the memo.
It is evidence, not an approved plan. Nothing here was committed, sent, or purchased.

## Method

Fiverr and Upwork both return HTTP 403 to `WebFetch` and to `curl` with a browser user-agent.
Fiverr was retrieved through the `r.jina.ai` reader proxy, which returned HTTP 200 markdown for
both search pages and gig detail pages. Only public product URLs were sent to the proxy — no
credentials, no repo content. Upwork stayed 403 through every route tried.

Parsing was a throwaway script at `/tmp/wtp/parse.py` (not added to the repo — see `AGENTS.md`
"do not add a 17th skill"). It pulls `[I will ...]` title anchors, the `**rating**(count)` line,
and the `[From$N]` line from the reader's markdown. Non-govcon gigs (SEO backlinks, logo design,
Amazon FBA) come back in Fiverr's results for these queries and were excluded by hand, not by the
parser.

## Full parsed Fiverr result set — query `sources sought`

45 gigs returned; 8 are govcon-relevant. Everything else was keyword noise on the word "source"
(ingramspark "lightning source" covers, "source files", "sourcing agent", "talent sourcing").
That noise ratio is itself weak evidence that Fiverr's govcon SS/RFI supply is shallow.

Govcon-relevant, sorted by review count:

| Reviews | Rating | From | Gig |
|---|---|---|---|
| 117 | 4.9 | $245 | laurels_glow — prepare your rfp, rfq, tender, competitive response |
| 86 | 5.0 | $20 | vasymabys — government contracts, dod proposal writer, rfps, rfqs |
| 50 | 5.0 | $145 | laurels_glow — search, document, respond to county/state/federal |
| 41 | 4.8 | $10 | ruth_madison — find rfp, write bid proposal, rfq, rfi, grant |
| 33 | 4.8 | $30 | mudassir_taj — rfp, rfq, rfi, ss, eoi and tender |
| 31 | 4.9 | $300 | spirtex — prepare a rfp rfq rfi sources sought bid proposal |
| 29 | 5.0 | $150 | martin_mishat — respond to US state or federal government contracts |
| 16 | 5.0 | $85 | govconwriter21 — respond to sources sought notices and rfis |
| 6 | 5.0 | $20 | mia_hernandez3 — government contract proposal, rfp bid, rfi, sam gov |
| 5 | 4.8 | $60 | tahaqaxi — samgov contract research analysis and opportunity reports |
| — | — | $50 | adele_peters — prepare a tender rfp rfq rfi sources sought bid proposal |
| — | — | $50 | carmen_johns — prepare rfp rfq rfi sources sought bid proposal |
| — | — | $25 | pattersonna — prepare rfp rfq rfi sources sought bid proposal |
| — | — | $10 | annita_palms — prepare a rfp rfq rfi sources sought bid proposal |

Four of those have **no reviews at all**. Listing a gig is not demand.

## Gig detail — the closest comparable to our packet

`govconwriter21 / respond-to-sources-sought-notices-and-rfis-for-your-bids`

- Package: **"Sources sought / RFI response" — $85**
- Terms: **3-day delivery, 2 revisions, up to 500 words**
- Seller: Fiverr Pro, 5.0 (16) on this gig, **5.0 (143) lifetime across gigs**
- Seller location Morocco; member since Jun 2021; **avg. response time 2 days**
- **Last delivery: 2 months ago**
- Seller's own claim: *"I've helped clients secure awards ranging from $30K to $1.8M"* — vendor
  claim, untested.
- Seller's gig copy makes the same SDVOSB set-aside argument V5 makes: *"if your firm is a Service
  Disabled Veteran-owned Small Business and only you responded to the sources sought, then it is
  pretty much guaranteed that the solicitation released will be SDVOSB set-aside."*

Deliverable described as *"a standardized response format with a cover page, and corporate
overview"* — i.e. a template fill. **No award mapping. No market slice. No gaps page.** That is the
substantive difference between $85 and $699, and it is worth stating plainly rather than assuming.

Buyer reviews (5 most relevant, with Fiverr's own spend bands):

| When | Spend band | Duration | Text |
|---|---|---|---|
| 1 year ago | $50-$100 | 4 days | "Excellent Job" |
| 1 year ago | $50-$100 | 4 days | "did a great job of writing response to a Source Sought" (UAE) |
| 2 years ago | $100-$200 | 3 weeks | "Very communicative And knowledgeable" |
| 2 years ago | $50-$100 | 6 days | "did a great job with our response" |
| 3 years ago | $200-$400 | 2 weeks | "very detailed worked delivered" |

Note the durations: **3 weeks and 2 weeks** on two of five, against a 3-day advertised delivery.
Marketplace turnaround is not reliably inside a notice window either.

## Capability-statement volume — the adjacent market

Query `capability statement`, 48 gigs, review counts at the top of the distribution:

804 ($30), 746 ($20), 703 ($20), 558 ($25), 374 ($25), 368 ($50), 101 ($10), 95 ($15), 89 ($10),
44 ($25), 36 ($60).

These are **design** gigs — Photoshop layout of a one-pager. Different job, same buyer. They
establish that the buyer transacts online for govcon paper at $10–60 without hesitation.

## Supply-side comparables in the council record — could not confirm

Checked because two seats leaned on them to defend $699.

**Bidspeed** (<https://www.bidspeed.com/pricing>): no dollar figures anywhere on the page. Tiers
Bronze / Silver / Gold / Diamond differentiated by user count, state count, onboarding cadence,
proposal templates per month, and proposal support per month. "Automatic Sources Sought/RFI
Response" is Diamond-only. Only CTA is *"Schedule a Live Discovery Meeting."*

**GovCon Command Center** (<https://www.govconcommandcenter.com/>): lists GovCon Academy **$49/mo**
and GovCon Professional **$149/mo**, immediately qualified by *"GovCon Starter is free today.
Pricing for GovCon Academy and GovCon Professional is being finalized — join the waitlist and we
will share plans and pricing before launch. Consulting and services are quoted individually."*

Also relevant and not previously noted by the council: that same page gives away *"Free, practical
templates: capability statement, sources-sought, bid/no-bid, compliance matrix, pricing, and
more."* A sources-sought template is free from a competitor's front page.

No $697 and no $395/$595/$995 found on either site today. Possible the earlier figures came from a
different page, an archived version, or a quoted proposal. Flagged, not asserted as an error by
another seat.

## APEX Accelerators — full pull

| Source | Quote |
|---|---|
| CT APEX ([link](https://ctapex.org/counseling-services/)) | *"CT APEX's services are provided at no cost"* |
| CT APEX | *"Advising clients in the proper submission of applications, registrations, certifications, bids, proposals, etc."* |
| CT APEX | *"Assist with researching government procurement opportunities, including providing 'Bidmatching'"* |
| Ohio APEX ([link](https://apex.ohio.edu/services/)) | *"registrations, certifications, market research, collateral development, bid and proposal development, compliance and standards support, post award support, and education"* |
| Ohio APEX | *"a search profile in our Bid Matching services that send you daily bids from over 2800 different federal state and local databases"* |
| Louisiana APEX ([link](https://ptac.louisiana.edu/services/contracting)) | counselors *"assist you with bid preparation by way of reviewing bids/proposals to ensure that you have completed all required documents correctly and have addressed each issue spelled out in the solicitation"* |
| Virginia APEX ([link](https://virginiaapex.org/schedule-a-meeting/)) | *"Counselor's schedules are often booked 30-60 days in advance and, like any professional service provider, it is important that the limited time you have with your counselor is productive."* |
| Arizona APEX ([link](https://arizonaapex.org/request-appointment)) | *"It may take 3-4 weeks for new client meetings to be scheduled."* |

The review-not-write finding rests on the Louisiana wording plus the absence of any drafting offer
across the five sites read. It is a strong negative but not an exhaustive one — there are ~90 APEX
accelerators and I read five. If one drafts, the claim needs narrowing to "most."

## Dead ends, recorded so nobody repeats them

- **reddit.com — HTTP 403 on every route**: `WebFetch` ("unable to fetch"), `curl` with browser UA,
  `old.reddit.com`, `/search.json`, and the reader proxy (*"You've been blocked by network
  security. To continue, log in to your Reddit account or use your developer token"*). Practitioner
  sentiment is **unmeasured**. It would need a Reddit API token to do properly.
- **upwork.com — HTTP 403** to `WebFetch` and to the reader proxy path tried.
- **Fiverr gig pages via `WebFetch`** — 403. Reader proxy works; use it.
- Generic web searches for "sources sought consultant cost" return SEO listicles from vendors with
  no prices in them. Search engines were near-useless for this question; the marketplace pages were
  everything.

## Open questions I would take next

1. Fiverr **premium tier** prices on the top three SS gigs — likely $300–600 and would compress the
   gap to $699.
2. Whether any APEX accelerator drafts rather than reviews (five of ~90 read).
3. Real Sources Sought response windows sampled from live SAM notices, replacing the 7–30 day
   industry-advice figure with an observed distribution.
4. Practitioner sentiment, which needs a Reddit developer token.
