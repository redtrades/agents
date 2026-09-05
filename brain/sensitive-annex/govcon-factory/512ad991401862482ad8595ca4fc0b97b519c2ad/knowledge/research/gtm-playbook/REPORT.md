# GTM playbook: how businesses like ours actually find customers and close deals

2026-08-26. Deep go-to-market research for a solo, agent-powered capture/proposal deliverable
business selling to federal contractors. Read-only research pass. Nothing in this repo was changed
by this file.

**What this extends, so it does not repeat.** `research/growth-plan/REPORT.md` already ranked
*awareness* channels (SEO, LinkedIn, newsletter, communities, paid) and settled the paid-ads
question. `research/outreach-playbook/REPORT.md` already settled cold-email craft, cadence,
deliverability, and CAN-SPAM. `research/proposal-writing/COMPETITOR-SNAPSHOT-winacontract.md`
covered one SaaS competitor's content machine. `research/feasibility-review/REPORT.md` established
the notice-supply ceiling (~250–400 sellable notice-moments/yr in 6 NAICS) and the surviving wedge
(verified, accountable, zero-effort). `research/council/2026-08-23-willingness-to-pay-research.md`
established the price bands and named APEX as the free substitute.
`research/council/2026-08-23-legal-sources-terra.md` established that the contractor-contact route
for matched outbound is a counsel gate, not a solved input.

This file answers a different question: **not where attention is, but how money actually changes
hands in this trade**, and what a solo operator does on day 1, day 30, day 60, day 90.

**Evidence labels used throughout.**

- **Observed.** Retrieved from the named page on 2026-08-26 (or the date noted), quoted or transcribed.
- **Vendor-published.** A marketing or sales blog from a party with an interest in the number. Direction, not decimals.
- **Repo.** An internal finding already established in this repository, cited rather than re-derived.
- **Inference.** My reading. Mike may reject it.

**Naming note.** The brief that commissioned this file described the products as
"submission-ready-starter proposal packages." `brand/offer.md` retires "submission-ready" as a
claim. This file uses the repo's own vocabulary: **free industry report**, **$699 opportunity
packet**, **code watch**.

---

## 0. Bottom line

Six findings, in the order they change what Mike does this week.

1. **The sales cycle is not a choice. The notice sets it.** Deals under $5K close in 7–21 days on
   one signature ([Optifai benchmark, 939 companies](https://optif.ai/learn/questions/sales-cycle-length-benchmark/), vendor-published),
   and the median currently-open Sources Sought has 8 days left with a quarter at 3 or fewer
   (n=1,029, repo: `research/council/2026-08-23-runtime-receipts-research.md`). Every close
   mechanic below has to fit inside a window shorter than the market's own fast lane. Discovery
   calls, SOW negotiation, and net-30 do not fit. Prepay, one CTA, and an artifact that arrives
   before the ask do.
2. **Contingency pricing is out, and the reason is a selling point.** FAR 3.402 makes a
   contractor's warranty against contingent fees statutory, FAR 3.404 puts the clause in
   solicitations over the simplified acquisition threshold, and remedies include annulment,
   recovery of the fee, and suspension or debarment referral
   ([FAR Subpart 3.4](https://www.acquisition.gov/far/subpart-3.4), observed). A working
   practitioner puts it plainly: "these days, no one ever hears of proposal consultants who will
   agree to work for a success fee"
   ([OST Global Solutions](https://www.ostglobalsolutions.com/how-do-capture-and-proposal-consultants-charge-for-their-services/),
   observed). Declining a success fee, and saying why, is a credibility move with this buyer.
3. **The observed one-deliverable market is $125 to $995, and a direct competitor publishes the
   whole ladder.** Bidspeed's marketplace, live today: Tailored Sources Sought Response Package
   **$395**, Industry Day Action Bundle **$595**, Custom Market Research Package **$995**,
   Government Buyers Report **$125**, Expiring Contracts Report **$149**, NAICS Procurement
   Forecast Report **$149**, advisory hour blocks at **$1,095 / $1,595 / $2,995**
   ([Bidspeed Marketplace](https://www.bidspeed.com/marketplace), observed 2026-08-26). $699 sits
   between their response and their market-research package. It is holdable. It is not cheap.
4. **Referral is the dominant channel in this trade, but the free counselors cannot be the referral
   engine.** Referrals and direct outreach remain the dominant lead sources for government
   contracting firms ([Hinge 2026 update](https://listeninnovategrow.com/high-growth-firms-are-not-just-better-at-marketing-they-are-better-at-go-to-market/), vendor-published),
   while SBA-side resource partners are structurally neutral: a representative SBDC referral page
   states it "does not endorse or recommend any of these firms or individuals"
   ([Lehigh SBDC](https://business.lehigh.edu/centers/small-business-development-center/for-existing-businesses/online-referral-book), observed),
   and SBA's own linking policy disclaims endorsement
   ([SBA](https://www.sba.gov/about-sba/open-government/about-sbagov-website/linking-policy), observed).
   Treat APEX and SBDC as **awareness and credibility**, and build the paid-referral loop with
   parties that can actually recommend: proposal consultants with too-small leads, cert and
   registration shops, bonding agents, GovCon CPAs.
5. **This buyer's market has a fraud base rate, and the first touch is competing against it.** GSA's
   own industry bulletin is titled "Don't Take the Bait: Beware of Misleading Marketing, Imposters,
   and Phishing" ([GSA IAE](https://buy.gsa.gov/interact/community/47/activity-feed/post/5251d26f-5781-483a-96fb-28eed2552f25/Don_t_Take_the_Bait_Beware_of_Misleading_Marketing_Imposters_and_Phishing), observed),
   and the well-documented pattern is third parties harvesting fresh SAM registrations and charging
   fees for a free government process
   ([BBB scam alert](https://www.bbb.org/article/scams/31197-bbb-scam-alert-watch-out-for-third-parties-claiming-to-help-with-your-government-grant-registration), observed).
   An unsolicited, prebuilt, firm-specific artifact from an unknown sender is structurally
   indistinguishable from that pattern at the moment of first read. This is the most underweighted
   GTM risk in the repo and it shapes every word of touch 1.
6. **The recurring-revenue shape that fits this trade is event-billed, not month-billed.** The same
   practitioner source notes that a retainer "works much better for capture, rather than proposal
   work" (OST, observed). Bid decisions are episodic. A monthly subscription whose value only fires
   when a matching notice appears will churn in the quiet months. `sop/MARKETING.md` Door 9 already
   has this right: code watch is free, and the packet is the bill.

**Channel ranking for this seller shape** (solo, no reputation yet, per-decision deliverable,
contact data legally unresolved). Ranked by expected paid orders per founder-hour in the first 90
days, not by audience size.

| # | Channel | Why it ranks here | Evidence | Gate |
|---|---|---|---|---|
| 1 | **Matched outbound on a live notice** | Only channel that reaches a firm *before* it has decided to bid, which is the entire business model | Buying-signal cold email runs 15–25% reply vs ~3.4% baseline (repo: outreach-playbook, vendor-published sources) | **Counsel** on contact source/field (repo: terra memo). Blocked until cleared |
| 2 | **Warm referral from paid peers** (consultants, cert shops, bonding agents, CPAs) | Referral is the dominant lead source in govcon; these parties *can* recommend and have leads too small to serve | Hinge (vendor-published); referral commissions cluster at 10–30%, commonly 20% ([Better Proposals](https://betterproposals.io/partners/), observed) | Needs one shipped sample and a written referral term |
| 3 | **Founder-led LinkedIn + live events** | High-growth govcon firms rank social networking #2 and live-event networking #3 among techniques they actually use ([Hinge 2024](https://hingemarketing.com/blog/story/5-things-we-learned-from-the-2024-high-growth-study-government-contracting-edition), vendor-published) | Same | Mike-time only, 2–3 hrs/wk. No auto-post |
| 4 | **APEX / SBDC / OSDBU as awareness** | Free counselors reach the exact buyer and can share free assets, but cannot endorse | SBDC/SBA non-endorsement language (observed) | Hand over free assets. Never pitch |
| 5 | **Answer-don't-pitch communities + podcast guesting** | Reaches buyers mid-question at zero cash cost | repo: feasibility F4 / PROPOSAL-0005 | Mike-only accounts |
| 6 | **Marketplace listing (Fiverr / Upwork)** | Demand is real but the price band is $85–$300, one to two tiers below $699 | repo: willingness-to-pay | Use as a **price test**, not a channel. Listing at $699 there anchors us against $85 |
| 7 | **SEO / content** | 6–12 month payback, and a competitor already has ~47 posts in our keyword space | repo: growth-plan §1, winacontract snapshot | Build cornerstone pages because outreach needs URLs, not because they will sell in 90 days |
| 8 | **Primes seeking subs (SBLO route)** | FAR 19.702 obliges primes to give SDVOSBs maximum practicable opportunity, so SBLOs need real teammate data ([FAR 19.702](https://www.acquisition.gov/far/19.702), observed) | Second-buyer thesis, unproven | Defer until after first sale |
| 9 | **Paid ads** | Already settled: no | repo: growth-plan §2 | Do not revisit before repeat purchase is measured |

---

## 1. How this trade actually acquires customers

### 1.1 The dominant channel is referral, and the study everyone cites says so with a caveat

**Vendor-published.** Hinge Research runs the only recurring study of marketing behavior among
government contracting firms. Their 2026 update states that referrals and direct outreach remain
dominant lead sources, and adds the caveat that matters for a new entrant: relationship-led growth
is "harder to sustain unless it is supported by visible expertise, targeted market presence, and a
deliberate way for buyers to encounter your firm before they ever speak to you"
([Hinge 2026 update](https://listeninnovategrow.com/high-growth-firms-are-not-just-better-at-marketing-they-are-better-at-go-to-market/)).

The 2024 GovCon edition (76 firms, $5.7B combined revenue) ranks the techniques high-growth firms
use most: **business development materials first**, social-media networking second, live-event
networking third, physical collateral and thought-leadership promotion tied fourth
([Hinge, 5 things we learned](https://hingemarketing.com/blog/story/5-things-we-learned-from-the-2024-high-growth-study-government-contracting-edition)).
High-growth firms in that sample grew at a median 45% and spent *slightly less* on marketing than
slower-growing peers.

**Inference, and it is load-bearing.** That ranking is about firms selling *to the government*, not
about consultants selling *to those firms*. What transfers is the buyer's own revealed preference:
these people believe in documents and in face-to-face contact, and they spend on BD materials
first. A seller whose entire product is a document, delivered before a meeting, is selling into a
preference that already exists. What does not transfer is the implied budget. A 76-firm sample
averaging $75M revenue is not our list-3 owner-operator.

### 1.2 The free counselors are the incumbent, not the partner

**Observed.** APEX Accelerators are free, present in all 50 states, and their service list overlaps
ours almost entirely (repo: willingness-to-pay §4). What the SBA-side network cannot do is
recommend a paid vendor. A representative SBDC referral page states it "does not endorse or
recommend any of these firms or individuals" and tells clients to check references before signing
([Lehigh SBDC](https://business.lehigh.edu/centers/small-business-development-center/for-existing-businesses/online-referral-book)).
SBA's linking policy makes the same disclaimer at the agency level
([SBA linking policy](https://www.sba.gov/about-sba/open-government/about-sbagov-website/linking-policy)).

**Inference.** `sop/MARKETING.md` Door 6 is right that counselors are a door and wrong if anyone
reads it as a referral pipeline. The realistic yield from a counselor relationship is: they list us
in a neutral resource directory, they share a free industry report in a training session, and they
mention us to a client who has a deadline they cannot fit. That last one is the only one that
produces revenue, and it happens because of the calendar constraint the repo already documented
(Virginia APEX publishes 30–60 day waits, Arizona 3–4 weeks, both observed 2026-08-23), not because
of a partnership.

### 1.3 The referral loop that can actually pay is peer-to-peer

**Observed.** Referral and affiliate commissions in adjacent professional-services software and
consulting cluster at 10–30%, with 20% a common published figure
([Better Proposals partner program](https://betterproposals.io/partners/), 20% ongoing). GovCon-side
affiliate programs exist for education products
([GC Advising](https://gcadvising.com/affiliate-sign-up), observed).

**Inference.** The three referral sources with the right incentive shape for a $699 per-decision
deliverable:

- **Proposal consultants** whose minimum engagement is four figures. A consultant billing $100–$200/hr
  in DC Metro (OST, observed) cannot profitably take a single small Sources Sought. Their too-small
  leads currently go nowhere. `sop/MARKETING.md` already plans these emails. The addition is a
  written referral term (15% of first packet, or reciprocal referral upward) rather than only a
  feed pitch.
- **Cert, registration, and VetCert-adjacent shops.** They meet the firm at the moment of
  certification, which is exactly when the firm has no BD motion yet.
- **Bonding agents and GovCon CPAs.** They see the firm's pipeline and are paid by the firm, not by us.

### 1.4 Live rooms are worth more per founder-hour than SEO in the first 90 days

**Observed, and this corrects a conflict inside the repo.** `research/growth-plan/REPORT.md` §4
says "NVSBE is gone" and points at decentralized VA Direct Access Program sessions. `sop/MARKETING.md`
says the event is on. **MARKETING.md is right.** VA OSDBU maintains a live NVSBE page and the event
is scheduled for **December 8–9, 2026, in Cleveland, Ohio**
([VA OSDBU NVSBE](https://www.va.gov/osdbu/nvsbe/), [NCMBC event listing](https://www.ncmbc.us/event/national-veterans-small-business-engagement-nvsbe-2026/), observed 2026-08-26).
The growth-plan line should be corrected when someone next touches that file.

**Inference.** NVSBE in December is a fixed point on the calendar 15 weeks out. It is the single
highest-density concentration of the exact buyer in the year, it is free to attend, and the cost of
being there with ten printed per-NAICS industry reports is travel. That is the one live-event
decision worth making early, because it constrains what the 90-day plan should produce: something
handable.

---

## 2. What actually converts

### 2.1 Pricing and packaging norms

**Observed, 2026-08-26, one competitor's full published ladder** ([Bidspeed Marketplace](https://www.bidspeed.com/marketplace)):

| Bidspeed product | Price | Shape |
|---|---|---|
| Government Buyers Report | $125 | Report, per-request |
| Expiring Contracts Report | $149 | Report, per-NAICS |
| NAICS Procurement Forecast Report | $149 | Report, per-NAICS |
| Tailored Sources Sought Response Package | $395 | Per-notice deliverable |
| Industry Day Action Bundle | $595 | Response + two reports |
| Build Your Acquisition Engine | $999 | Assessment package |
| Custom Market Research Package | $995 | Per-notice deliverable, "formatted to government standards" |
| 4 / 8 / 16 hour advisory blocks | $1,095 / $1,595 / $2,995 | Hours, $187–$274/hr effective |

**Observed, the labor band.** OST Global Solutions on its own market: consultants run "$60 an hour
on the low end to $250 an hour and up on the high end," and DC Metro experienced proposal or capture
managers fall "between $100 and $200 per hour"
([OST](https://www.ostglobalsolutions.com/how-much-do-consultants-charge/), retrieved 2026-08-23 per repo).

**Vendor-published, the upper band.** Consultants "charge $150 to $400 hourly or use fixed project
fees," with mid-size proposal external fees of $40K–$75K
([GovEagle](https://www.goveagle.com/blog/proposal-consultant-vs-ai-tool-government-contractors)).
GSA Schedule proposal writing is described as $3,500 for basic single-SIN work to $35,000 for
complex multi-SIN offers, with the common mid-size engagement at $8,000–$15,000
([Blackfyre](https://www.blackfyre.app/blog/how-much-to-budget-for-gsa-proposal-writers)).

**Observed, the floor.** Fiverr Sources Sought and RFI gigs sell from $85 to $300, and the one gig
selling only Sources Sought/RFI responses is $85 for up to 500 words, 3-day delivery, 2 revisions
(repo: willingness-to-pay §1, retrieved 2026-08-23).

**What the packaging evidence says.** The dominant model is hourly. "The majority of capture and
proposal consultants charge on a strictly hourly basis," with flat daily rates as the common
variant, and the same source says flatly: "I have not heard of any consultants who work on a fixed
fee basis, although a lot of businesses tend to think of it as a viable option"
([OST on consultant compensation](https://www.ostglobalsolutions.com/how-do-capture-and-proposal-consultants-charge-for-their-services/)).
Package pricing exists, and the source names exactly the conditions under which it works: "proposal
houses" that "have a lot of established processes and templates meant to streamline many
time-consuming tasks, have salaried staff, and are able to accurately estimate the effort."

**Inference, and this is the strategic read.** That sentence is a description of a factory. The
reason fixed-price is rare in this trade is that human consultants cannot estimate the effort. An
agent pipeline with frozen templates, gates, and a ~20-minute founder review budget (repo:
`sop/PLAN-V5.md` §7 unit rule) *can*. Fixed price is not a concession we make to be cheap. It is the
one packaging shape the incumbent labor model structurally cannot copy, and the pitch should say so.
Caveat: the OST compensation article is dated 2012 by its own byline. Treat its structure as
durable and its "these days" claims as needing a second source before they enter customer copy.

### 2.2 Contingency and success fees: legal posture

**Observed, primary.** [FAR Subpart 3.4](https://www.acquisition.gov/far/subpart-3.4):

- 3.401 defines a **contingent fee** as "any commission, percentage, brokerage, or other fee that is
  contingent upon the success that a person or concern has in securing a Government contract," and a
  **bona fide agency** as "an established commercial or selling agency, maintained by a contractor
  for the purpose of securing business, that neither exerts nor proposes to exert improper influence."
- 3.402 records that these arrangements "have long been considered contrary to public policy,"
  requires a warranty in every negotiated contract, permits the bona fide employee/agency exception,
  and provides that on breach the Government "may annul the contract without liability or deduct
  from the contract price or consideration, or otherwise recover, the full amount of the contingent fee."
- 3.404 inserts [52.203-5](https://www.ecfr.gov/current/title-48/chapter-1/subchapter-H/part-52/subpart-52.2/section-52.203-5)
  in solicitations and contracts above the simplified acquisition threshold, other than commercial
  products and commercial services.
- 3.405 lists the consequences of a suspected violation: reject the bid pre-award, annul or recover
  post-award, initiate suspension or debarment, refer suspected fraud to DOJ.

**Three things this does and does not mean.**

1. It is a **warranty by the contractor**, so the exposure lands on the client, not on us. That is
   worse, not better, for a seller who needs referrals.
2. The **bona fide agency exception is narrow and fact-bound**, and it exists to protect established
   selling agencies, not per-deal success splits. Practitioner commentary treats it as a defense to
   be proven, not a safe harbor ([SmallGovCon back-to-basics](https://smallgovcon.com/back-to-basics/back-to-basics-covenant-against-contingent-fees/)).
3. The clause is **not inserted for commercial-product or commercial-service acquisitions**, which
   is a real carve-out and precisely the kind of nuance that should never be relied on by a
   non-lawyer at the point of sale.

**Practitioner reality.** OST, a firm that would profit from success fees if they worked: "These days,
no one ever hears of proposal consultants who will agree to work for a success fee," listing the
risks (award delay, protest, scope cuts, enforcement) and noting "there are also aspects of the
success fee for winning Government contracts that are prohibited by the Federal Acquisition
Regulations (FAR)." The one variant that persists is a **blended model**, a discounted hourly or
daily rate plus a success payment, "similar to the way lobbyists are paid."

**Recommendation.** No contingency, no success fee, no percentage of award, ever, and say so on the
pricing page in one sentence. Add a fourth objection block alongside the existing three:

> "Can you do this on contingency?" No. Contingent fees on federal contracts trigger a warranty the
> *contractor* signs (FAR 52.203-5), and the remedies fall on you, not on me. Flat $699, one notice.

That answer costs nothing, is verifiable, and demonstrates domain knowledge to a buyer whose main
question is whether we are another SAM registration outfit.

### 2.3 Deal size, cycle, and who signs

**Vendor-published benchmarks, direction only.** Sub-$5K deals close in 7–21 days and are the
fastest-closing B2B segment because "one person can sign," with each additional $10K of annual
contract value adding roughly one stakeholder and one approval gate
([Optifai, 939 companies](https://optif.ai/learn/questions/sales-cycle-length-benchmark/)).

**Repo, and this is the harder constraint.** The median currently-open Sources Sought has 8 days
remaining and a quarter have 3 or fewer (n=1,029). The outreach playbook filters to notices with
10–20 days left so a 3-touch cadence fits.

**Inference.** Our effective sales cycle is the *shorter* of the benchmark and the notice window,
which means **3 to 12 days, with no second meeting available**. Consequences that fall straight out
of that number:

- No discovery call. There is no room for one, and asking for one converts worse than asking for
  permission to send a file (repo: outreach-playbook, CTA finding).
- The artifact must exist before the ask. A firm cannot evaluate a promise inside 8 days.
- Follow-up cadence is bounded by the deadline, not by best practice.
- A lost deal is not a lost customer. The firm is recycled into the next matching notice, which is
  the closest thing this business has to a nurture sequence.

**Who signs.** The owner. `brand/customer.md` already establishes the ICP as owner-run with no BD
staff and evenings as the binding constraint. The sub-$5K benchmark independently predicts a single
decision maker. This is the rare case where the ICP work and the external benchmark agree, so treat
"find the BD lead" as a failure mode: if a firm has a BD lead, HigherGov at $500/yr Starter
([HigherGov pricing](https://www.highergov.com/pricing/), observed) serves them better and
`brand/customer.md` already says to tell them so.

### 2.4 What proof they demand, and what we have

| Proof the buyer wants | What we have | Gap |
|---|---|---|
| A sample of the actual work | 10 gated samples, all green, double-bannered (repo: `samples/sample-set/`) | None. This is the strongest asset in the business |
| Evidence you read *their* record | One resolving PIID in sentence one, enforced as a send gate | None |
| References from firms like them | **Zero.** No customer has bought yet | The binding gap. First three buyers must be asked for a reference at delivery, not later |
| Win rates | Deliberately refused (`brand/offer.md`) | Refusal must be *stated*, or silence reads as evasion |
| Who you are | Named veteran owner, reply-to a person | Needs a real physical address in the footer (CAN-SPAM requires it anyway) |
| That you are not a scam | Nothing yet | See §5.5. This is the unaddressed one |

### 2.5 Objections that kill deals

The repo already has researched blocks for three: the AI tool substitute, APEX-is-free, and the
$699 price (`brand/customer.md`). Research adds three more that are live in this market:

1. **"Can you do it on contingency?"** Answered in §2.2.
2. **"Is this the SAM registration thing?"** The buyer has been called by people demanding $2,500 to
   "activate" a free registration ([BBB](https://www.bbb.org/article/scams/31197-bbb-scam-alert-watch-out-for-third-parties-claiming-to-help-with-your-government-grant-registration), observed).
   The answer is structural, not verbal: send the artifact or a real slice of it before asking for
   money, price in public, and never create urgency the notice did not already create.
3. **"My competitor might be buying this from you too."** `research/feasibility-review/REPORT.md` F2
   flagged this. Note the sharper version found in this pass: agency clauses require an offeror to
   disclose **consultant** conflicts, not only organizational ones. DHS's clause requires an offeror
   identifying a potential conflict to submit an Organizational and Consultant Conflicts of Interest
   Plan describing how it will "avoid, neutralize, or mitigate" it
   ([1252.209-70](https://www.acquisition.gov/node/54213/printable/print), observed), and DFARS has a
   parallel subpart ([DFARS 209.5](https://www.acquisition.gov/dfars/subpart-209.5-organizational-and-consultant-conflicts-interest), observed).
   The client may have to disclose us. The current default (one packet per notice, exclusivity until
   TASK-0013 decides) is therefore not just an ethics posture, it is the answer that keeps the
   client's own paperwork clean. Say that out loud.

---

## 3. Close mechanics

### 3.1 The $500–$2K motion (ours)

```
notice detected (10-20 days left)
   -> packet or map prebuilt, no customer input
   -> touch 1: one real PIID, the deadline, one CTA ("want the PDF?")
   -> reply -> send the artifact or the evidence preview
   -> price stated in public, no quote, no call
   -> Stripe invoice, card or ACH, PREPAID
   -> terms accepted at checkout (one page, liability cap, no-win-promise)
   -> deliver, then ask for the reference and the code-watch opt-in in the same message
```

Design rules, each with a reason:

- **No discovery call.** No room in the window (§2.3), and a call converts worse than an artifact ask.
- **Sample-first is the entire funnel.** Pilot-style proof-of-work selling is the documented pattern
  in adjacent AI service businesses (§6), and here it is cheaper: the sample already exists.
- **Prepay on the first order, always.** `research/feasibility-review/REPORT.md` F10 already
  recommends this. The reinforcing reason: prepay is the single clearest separator from the
  registration-scam pattern, because scams collect on a promise and we collect on a delivered or
  demonstrable artifact. Prepay *after* the preview, never before it.
- **Net-15 only for a second-time buyer who asks.** Our buyer lives on net-30 from the government and
  will ask out of habit. Granting it on order one converts a $699 sale into a $699 receivable from a
  firm we have never met.
- **No SOW.** A one-page order confirmation naming the notice, the firm, the exclusivity term, and
  what is not included. TASK-0014 (terms, refunds, money-back) is open and gates this.
- **Refund posture.** Publish a kill-fee rule before the first order: full refund before data pull,
  partial after pull and before draft, none after delivery. Cheap to write, expensive to improvise.

### 3.2 The $5K+ motion (not ours, and worth naming why)

At $5K and up the market runs on hours, references, and a scoped engagement: hourly or daily rates
(OST), external fees of $40K–$75K on mid-size proposals (GovEagle, vendor-published), discovery,
capture involvement over months. Each additional $10K of value adds a stakeholder and 5–10 days
(Optifai, vendor-published).

**Inference.** A solo operator cannot serve that band and keep the ~20-minute review unit rule.
The correct posture is to be the **referral destination** for the small end of that band and the
**referrer** for anything above it. That is not modesty, it is the mechanism that makes §1.3 work:
consultants refer down only to shops that refer up.

### 3.3 Procurement friction

Our buyer has no procurement department, which removes most friction and adds three specific asks:
a W-9, an invoice their bookkeeper can file, and occasionally a certificate of insurance. E&O runs
roughly $700–$1,500/yr for a small professional services firm (repo: feasibility F7, citing
Insureon). Have all three ready before the first close, because producing them mid-window costs days
we do not have.

---

## 4. Retention and expansion

**What the trade says.** Retainers "work much better for capture, rather than proposal work" (OST,
observed). Proposal work is episodic by nature; capture is continuous.

**What the substitutes charge for recurring.** HigherGov publishes $500/yr Starter, $2,500/yr
Standard, $5,000/yr Leader ([HigherGov pricing](https://www.highergov.com/pricing/), observed). That
is the price ceiling any subscription we invent is measured against, and it is one that ships a
search product plus AI drafting.

**What churn looks like in this segment.** Vendor-published SMB benchmarks put monthly churn at
3–5% and annual churn for sub-$15K ACV products at 10–15%, elevated because small businesses
themselves fail ([Optifai](https://optif.ai/learn/questions/b2b-saas-churn-rate-benchmark/)).

**The three expansion shapes, ranked.**

1. **Code watch, billed on the event.** Free to hold, and the next matching notice produces a packet
   order. `sop/MARKETING.md` Door 9 already specifies this. It is correct and the evidence above
   explains why: it removes the quiet-month churn mechanic entirely because there is nothing to churn
   from.
2. **Standing capture support for the firm that wins something.** A firm that converts a packet into
   an award enters a recompete cycle and a past-performance cycle. That is the moment a retainer
   fits, per OST. It is also the moment the founder-hour ceiling binds, so cap it at a very small
   number of clients or refer it out.
3. **Consultant feed at $249/mo.** Already a side test in `sop/PLAN-V5.md` §7. Note what the pricing
   evidence says about its risk: a consultant billing $150–$400/hr will drop a $249/mo feed the first
   month it produces nothing usable, and consultants are exactly the referral partners §1.3 depends
   on. A soured feed subscription costs a referral relationship. Sequence the referral term first.

**Observed churn drivers to instrument from order one:** no matching notice in the window the
customer expected (supply), the packet's fill rate landing below what the preview implied
(quality), and the customer not bidding at all (which is a *good* outcome under
`brand/offer.md`'s no-sale rule but looks identical to churn in the data). Log the reason, not just
the event.

---

## 5. What kills solo proposal and capture shops

Ranked by probability times damage for this specific business.

### 5.1 The contact-source ruling (existential, and already known)

`research/council/2026-08-23-legal-sources-terra.md` established that SAM's public Entity API
excludes POC email as FOUO/CUI, that the SBS/DSBS route is an undocumented internal POST with no
located commercial-use authorization, and that CAN-SPAM compliance does not grant sourcing
permission. If counsel says no, channel #1 disappears and the business becomes inbound-only with a
6–12 month SEO clock. **Nothing else in this report matters as much as closing that question.**

### 5.2 Notice supply, not firm count, is the ceiling

~250–400 sellable notice-moments/yr across the 6 target NAICS (repo: feasibility F1). Ten customers
is comfortably inside it. A hundred is not, without widening NAICS or selling multiple firms per
notice, and the latter collides with §2.5's exclusivity answer. Plan the first ten, not the first
hundred.

### 5.3 The founder-hour ceiling

Every send and every ship requires Mike by design (repo: AGENTS.md rule 1, feasibility F10). The
solo services ceiling before productization or hiring is widely put at roughly $225K–$300K in
vendor commentary ([Gigradar](https://gigradar.io/blog/marketing-consultant-freelance), vendor-published,
direction only), and the more binding version here is the unit rule: if founder review does not fit
in ~20 minutes, reprice or cut scope. Feast-famine follows mechanically when the same person does
delivery and selling, because selling stops during delivery. The mitigation that fits this business
is that **outreach is agent-prepared and Mike only approves**, so the pipeline does not go dark
during a delivery week. Protect that property. It is the actual product of the factory.

### 5.4 Concentration on one agency or one NAICS

Not yet a risk at zero customers, and a fast one at ten. The sample set already spans NAICS
deliberately. Keep the first ten spread across at least three codes and two agencies so that a
single agency's procurement pause does not zero the quarter.

### 5.5 Reputation collapse, and the specific way it happens here

Two mechanisms, both cheap to prevent and both fatal.

**Being mistaken for the scam.** GSA publishes an industry bulletin warning about misleading
marketing and imposters ([GSA IAE](https://buy.gsa.gov/interact/community/47/activity-feed/post/5251d26f-5781-483a-96fb-28eed2552f25/Don_t_Take_the_Bait_Beware_of_Misleading_Marketing_Imposters_and_Phishing)),
and BBB documents third parties charging for free SAM processes
([BBB](https://www.bbb.org/article/scams/31197-bbb-scam-alert-watch-out-for-third-parties-claiming-to-help-with-your-government-grant-registration)).
The buyer's prior on an unsolicited govcon email is fraud. Countermeasures, all already compatible
with repo rules: public pricing, a named person with a real address, no urgency beyond the notice's
own date, a verifiable PIID in sentence one, and never asking for money before something real has
been delivered or shown.

**A wrong number on a public page or in a packet.** Already the repo's own standard (a wrong public
number is a reputation gate failure). The community is small and talks; r/GovernmentContracting
alone is 41K+ members (repo). One bad artifact circulating with our name on it costs more than ten
sales.

### 5.6 Conflict on one notice

Covered in §2.5. The addition from this pass: the client may carry a disclosure obligation about
consultants, which converts our exclusivity default from a nicety into a service feature.

---

## 6. Adjacent proof: how comparable AI-powered service businesses go to market

Evidence here is thin and mostly vendor-published. Labeled accordingly, and included because the
pattern is consistent across weak sources rather than because any one source is strong.

**The recurring pattern is proof before commitment.** The most commonly described motion for AI
agent and automation service businesses is a pilot: 3–5 early customers at 50–70% off target pricing
in exchange for feedback, case-study rights, and testimonials, with a 30–60 day fixed-scope pilot and
named success metrics ([MindStudio](https://www.mindstudio.ai/blog/start-ai-automation-business-case-studies),
[Presta](https://wearepresta.com/ai-agent-startup-ideas-2026-15-profitable-opportunities-to-launch-now/), both vendor-published).
Founder accounts of first-ten-customer acquisition in productized services cluster on direct
outreach and existing communities rather than on content
([Indie Hackers threads](https://www.indiehackers.com/post/how-did-you-acquire-your-first-10-users-customers-23a6a259a2), anecdotal).

**What transfers:**

- **Proof-of-work before the ask.** Ours is stronger than a pilot because the artifact is already
  built and costs pipeline compute, not founder weeks.
- **Case-study rights traded for price.** Trade a discount for a named reference on the first three
  orders, since §2.4 identifies references as the binding proof gap. A discount is cheaper than the
  reference is valuable.
- **Narrow scope, published price, defined deliverable.** The same property that makes fixed-price
  possible for a factory (§2.1).

**What does not transfer:**

- **The 30–60 day pilot.** Our window is 8 days. A pilot here is one notice, not one quarter.
- **ROI-metric case studies ("30% time savings").** `brand/offer.md` forbids win-rate and ROI claims,
  and it is right: outcomes here are the CO's decision, not ours. The case study we can honestly
  publish is a **coverage** case study: this notice, this many requirements, this many Covered rows,
  this many gaps, delivered in this many hours.
- **Unlimited-scope subscriptions.** The consistent failure note across these sources is that the
  businesses that burned out promised unlimited work. The unit rule already prevents this. Keep it.

---

## 7. The 30/60/90 motion for a solo operator

Assumes Mike's marketing budget is roughly **5 founder-hours per week**, plus agent time that does
not compete with it. Every item names its gate.

### Days 1–30: prove the money question, gate everything else

| # | Action | Founder time | Gate / dependency |
|---|---|---|---|
| 1 | Close the **counsel question** on contact source, field, and outreach use | 2 hrs total | TASK-0014 scope extension (repo: terra memo, board implication). **Blocks item 3** |
| 2 | Ship the one-page site: free industry report, UEI box, newsletter, **public $699 price**, named owner, physical address, one-paragraph "how this is not a SAM registration service" | 3 hrs review | Existing TASK-0006 / issue #12 |
| 3 | **One matched batch**: 4–8 notices, 8–15 list-3 firms each, 3-touch compressed cadence, Mike sends | 4 hrs/wk | Item 1 cleared. If not cleared, substitute item 3b |
| 3b | *Fallback if counsel says no:* concierge evidence preview from inbound only. Same artifact, different door | 3 hrs/wk | None |
| 4 | Publish the **objection block on contingency** and the **exclusivity answer** (§2.2, §2.5) | 1 hr | None. Pure copy |
| 5 | Write the terms, refund/kill-fee rule, W-9, and E&O quote | 2 hrs | TASK-0014 |
| 6 | 2 LinkedIn posts/week from factory numbers, Mike-voiced | 1.5 hrs/wk | None |
| 7 | Register for **NVSBE, Dec 8–9, Cleveland** | 15 min | None. Cheapest calendar lock available |

**Day 30 gate.** Repo already fixes it: 0 paid after two matched batches of genuinely list-3 firms
means the offer failed, and the fix is the packet, not more channels. The GTM council's sharper
version (0 paid after 40 qualified exposures, twice) is the better denominator because it works for
both the outbound and the inbound-preview arm.

### Days 31–60: convert the first buyers into proof

| # | Action | Founder time | Gate |
|---|---|---|---|
| 8 | Ask every buyer for a **named reference and a coverage case study** at delivery. Trade a discount for it if needed | 15 min per order | Requires ≥1 sale |
| 9 | Send the **consultant referral emails** with a written referral term (15% of first packet or reciprocal), not only the feed pitch | 2 hrs once | Requires 1 shipped sample |
| 10 | Newsletter issue 1, only codes with a real report | 1 hr | Existing task |
| 11 | Hand free industry reports to APEX counselors in 3 states. No pitch, no ask | 1 hr | None |
| 12 | Instrument: reply rate, preview→paid, time-to-decision, founder review minutes, and **the reason for every no** | ongoing | Analytics decision still open (repo: feasibility F11) |
| 13 | Second matched batch, tuned on batch-one no-reasons | 4 hrs/wk | Item 3 |

**Day 60 gate.** At least one repeat or referred order, or the retention thesis in §4 is unfunded and
code watch stays free with no expansion work built on it.

### Days 61–90: make month 6 cheaper than month 1

| # | Action | Founder time | Gate |
|---|---|---|---|
| 14 | 5–10 cornerstone SEO pages, each leaning on provenance, which is the gap in winacontract's 47 posts | agent-built, 2 hrs review | Existing TASK-0009 |
| 15 | One podcast or APEX/SBDC webinar guest slot | 3 hrs | Needs the coverage case study from item 8 |
| 16 | Cert-shop, bonding-agent, and CPA referral intros, 3 each | 2 hrs | Item 9's term sheet |
| 17 | Decide TASK-0013 (conflict policy) on evidence from real collisions, not in the abstract | 1 hr | Needs ≥2 orders on one notice, or the default holds |
| 18 | Print ten per-NAICS industry reports for NVSBE | 1 hr | Item 7 |
| 19 | Re-derive the notice-supply ceiling from actual batch data and replace the estimate | agent time | repo: PROPOSAL-0001 |

**Day 90 gate.** Three questions with numbers attached: what does a paid packet cost in founder
minutes, what fraction of qualified exposures convert, and did any customer come from a channel
other than outbound. The third one decides whether the business is a channel business or an
outbound business.

---

## 8. The first ten customers, specifically

Not a funnel. A list of ten named slots with a source and a fallback.

| Slots | Source | Mechanism | Why this source, with evidence |
|---|---|---|---|
| **1–3** | Matched outbound, evidence-shaped notices only | 3-touch, deadline-bounded, exclusivity stated, prepay after preview | Buying-signal outbound is the only channel that reaches a firm before it decides to bid (repo). Restrict to notices at ≥50% Covered+Partial so the first three artifacts are the strongest the factory can make |
| **4–5** | Referral from customers 1–3 | Ask at delivery, in the same message as the code-watch opt-in | Referral is the dominant lead source in this trade (Hinge). The ask has to be scheduled, or it never happens |
| **6–7** | Proposal consultants' too-small leads | Written referral term, 15% of first packet or reciprocal referral upward | Consultants at $100–$400/hr cannot serve a single small Sources Sought profitably (OST, GovEagle) and currently drop those leads |
| **8** | Cert / registration shop or bonding agent or GovCon CPA | Same term sheet | These parties meet the firm at certification, before any BD motion exists |
| **9** | Inbound: LinkedIn or free industry report or newsletter click | UEI box, evidence preview, self-serve | Founder-led content and the free report are already funded and running by day 60 |
| **10** | APEX counselor deadline referral, or NVSBE floor | Free report handed over, no pitch | Counselors cannot endorse (SBDC/SBA, observed) but can point a deadline case somewhere. NVSBE is the year's densest buyer concentration (VA OSDBU, observed) |

**Rules that apply to all ten.**

- **Spread them.** At least three NAICS and two agencies (§5.4).
- **One packet per notice.** Exclusivity is the default until TASK-0013 decides otherwise, and §2.5
  gives the client-side reason to keep it.
- **Refuse the bad ones out loud.** Below the fill floor, send the free map and gaps and say there is
  nothing to buy. `brand/offer.md` already requires this. The no-sale is the referral.
- **Every one of the ten produces an artifact of proof**: a reference, a coverage case study, or a
  documented reason for no. Ten sales with no proof assets is a worse outcome than seven with ten
  documented reasons.

---

## 9. The three highest-risk assumptions in this plan

**1. That a firm will pay before it has decided to bid.**
The willingness-to-pay research found no observed precedent: the closest comparable product on the
market prices against an opportunity "you found" and asks which ones the buyer "intends to chase
after," placing the transaction boundary after the buyer's decision, twice, in its own copy (repo:
willingness-to-pay §4b). Everything in §7 and §8 assumes we can move that boundary earlier.
**Test:** the day-30 gate, denominated in qualified exposures rather than emails.
**If false:** the product is not a pre-decision packet but a post-decision one, the channel becomes
inbound-at-the-moment-of-decision, and the $699 price is exposed against Bidspeed's $395 and
Fiverr's $85–$300 rather than against a consultant's hours.

**2. That there is a legally cleared route to the contractor's inbox.**
Unresolved (repo: terra memo). Nine of the ten first customers in §8 depend on outbound directly or
on referrals seeded by outbound.
**Test:** one counsel session, days 1–5.
**If false:** channel #1 is zero, the first-ten plan shifts to slots 9 and 10 as the primary sources,
the timeline stretches from 90 days to 6–12 months on the SEO clock, and the day-30 kill gate has to
be restated in preview terms or it will fire for the wrong reason.

**3. That a cold, prebuilt, firm-specific artifact reads as credible rather than as the scam this
market is trained to expect.**
This is the assumption with the least evidence behind it in either direction. The federal small
business market has a documented fraud ecosystem aimed precisely at newly registered and newly
certified firms (GSA, BBB, both observed), and our first touch shares its surface features:
unsolicited, personalized from public data, arriving near a deadline, asking for money.
**Test:** it is already measurable in the batch-one data if the "no" reasons are logged. Watch
specifically for non-replies followed by no site visit, and for replies asking "who are you" or "is
this a scam," and count them as their own category rather than as generic rejection.
**If false:** the fix is not copy, it is sequence. The artifact goes first and completely free,
payment moves behind a delivered thing, and the introduction has to come through a human who is
already trusted, which promotes the referral and community channels above outbound regardless of
what counsel says.

---

## 10. What I could not establish

- **No public dataset** counts how many small firms buy proposal or capture help per year, at any
  price. Every band in §2.1 is assembled from published price pages and practitioner statements.
- **No observed conversion data** for any govcon service shop's channel mix. The Hinge study measures
  contractors, not the consultants who serve them, and its GovCon edition is paywalled beyond the
  free summary.
- **Bidspeed's volumes are unknown.** Their published ladder is real evidence about packaging and
  price. It is no evidence at all about demand. In particular, their paid $125–$149 reports do not
  overturn the repo's decision to give the industry report away.
- **APEX referral behavior is unmeasured.** Non-endorsement language was found at the SBDC and SBA
  level; I did not locate a national APEX policy document governing counselor referrals to paid
  vendors, and the network's roughly ninety centers vary. Quote only a prospect's own state center,
  per the existing repo guardrail.
- **The OST compensation article is from 2012.** Its structural taxonomy of pricing models is almost
  certainly still accurate; its "these days" claims about success fees need a second, current source
  before they enter customer-facing copy.
- **Reddit and Upwork remain unreachable** to this research method, as in the prior pass. Practitioner
  sentiment in those rooms is unmeasured, not absent.

---

## Sources

**Primary / regulatory.** [FAR Subpart 3.4 Contingent Fees](https://www.acquisition.gov/far/subpart-3.4) ·
[FAR 52.203-5 Covenant Against Contingent Fees (eCFR)](https://www.ecfr.gov/current/title-48/chapter-1/subchapter-H/part-52/subpart-52.2/section-52.203-5) ·
[FAR 19.702 Statutory requirements](https://www.acquisition.gov/far/19.702) ·
[FAR Subpart 9.5 Organizational and Consultant Conflicts of Interest](https://www.acquisition.gov/far/subpart-9.5) ·
[DFARS Subpart 209.5](https://www.acquisition.gov/dfars/subpart-209.5-organizational-and-consultant-conflicts-interest) ·
[HSAR 1252.209-70 Organizational and Consultant Conflicts of Interest](https://www.acquisition.gov/node/54213/printable/print) ·
[VA OSDBU NVSBE](https://www.va.gov/osdbu/nvsbe/) ·
[SBA linking policy](https://www.sba.gov/about-sba/open-government/about-sbagov-website/linking-policy) ·
[GSA IAE, Don't Take the Bait](https://buy.gsa.gov/interact/community/47/activity-feed/post/5251d26f-5781-483a-96fb-28eed2552f25/Don_t_Take_the_Bait_Beware_of_Misleading_Marketing_Imposters_and_Phishing).

**Observed competitor and market pricing.** [Bidspeed Marketplace](https://www.bidspeed.com/marketplace) (retrieved 2026-08-26) ·
[HigherGov Plans and Pricing](https://www.highergov.com/pricing/) ·
[OST, how capture and proposal consultants charge](https://www.ostglobalsolutions.com/how-do-capture-and-proposal-consultants-charge-for-their-services/) ·
[OST, how much do consultants charge](https://www.ostglobalsolutions.com/how-much-do-consultants-charge/) ·
[Better Proposals partner program](https://betterproposals.io/partners/) ·
[GC Advising affiliate program](https://gcadvising.com/affiliate-sign-up).

**Practitioner and trade commentary.** [SmallGovCon, Back to Basics: Covenant Against Contingent Fees](https://smallgovcon.com/back-to-basics/back-to-basics-covenant-against-contingent-fees/) ·
[The Contractor's Perspective on the Covenant](https://www.contractorsperspective.com/compliance/vernons-got-prospects-hes-bona-fide-understanding-the-covenant-against-contingent-fees/) ·
[NCMBC NVSBE 2026 listing](https://www.ncmbc.us/event/national-veterans-small-business-engagement-nvsbe-2026/) ·
[Lehigh SBDC referral book](https://business.lehigh.edu/centers/small-business-development-center/for-existing-businesses/online-referral-book) ·
[BBB scam alert on third-party registration](https://www.bbb.org/article/scams/31197-bbb-scam-alert-watch-out-for-third-parties-claiming-to-help-with-your-government-grant-registration).

**Vendor-published benchmarks (direction, not decimals).** [Hinge, 5 things from the 2024 High Growth Study GovCon edition](https://hingemarketing.com/blog/story/5-things-we-learned-from-the-2024-high-growth-study-government-contracting-edition) ·
[Hinge 2026 high-growth update](https://listeninnovategrow.com/high-growth-firms-are-not-just-better-at-marketing-they-are-better-at-go-to-market/) ·
[Optifai sales-cycle benchmarks](https://optif.ai/learn/questions/sales-cycle-length-benchmark/) ·
[Optifai churn benchmarks](https://optif.ai/learn/questions/b2b-saas-churn-rate-benchmark/) ·
[GovEagle, proposal consultant vs AI tool](https://www.goveagle.com/blog/proposal-consultant-vs-ai-tool-government-contractors) ·
[Blackfyre, budgeting for GSA proposal writers](https://www.blackfyre.app/blog/how-much-to-budget-for-gsa-proposal-writers) ·
[MindStudio, AI automation business case studies](https://www.mindstudio.ai/blog/start-ai-automation-business-case-studies) ·
[Presta, AI agent startup patterns](https://wearepresta.com/ai-agent-startup-ideas-2026-15-profitable-opportunities-to-launch-now/) ·
[Gigradar, solo vs agency ceiling](https://gigradar.io/blog/marketing-consultant-freelance) ·
[Indie Hackers, first 10 customers threads](https://www.indiehackers.com/post/how-did-you-acquire-your-first-10-users-customers-23a6a259a2).

**Internal (cited, not re-derived).** `AGENTS.md` · `sop/PLAN-V5.md` · `sop/MARKETING.md` ·
`brand/company.md`, `brand/customer.md`, `brand/offer.md`, `brand/voice.md` ·
`research/growth-plan/REPORT.md` · `research/outreach-playbook/REPORT.md` ·
`research/feasibility-review/REPORT.md` (F1, F2, F3, F4, F7, F10, F11) ·
`research/proposal-writing/COMPETITOR-SNAPSHOT-winacontract.md` ·
`research/council/2026-08-23-willingness-to-pay-research.md` ·
`research/council/2026-08-23-legal-sources-terra.md` ·
`research/council/2026-08-23-gtm-gpt-5.6-sol.md` ·
`research/council/2026-08-23-runtime-receipts-research.md` · `samples/sample-set/`.

---
---

# Part II: recurring revenue, the terms-of-service reality, and whether the wedge survives

Added 2026-08-26 in response to a sharpened question set. Three questions, answered in order:
is recurring revenue feasible and permissible, is "notification plus an already-drafted response"
a real wedge or a copyable feature, and what revenue architecture actually fits a solo operator.

Same evidence labels as Part I. Nothing below is legal advice. Where a term is quoted, it is quoted
verbatim so counsel can read the same words.

---

## 11. What the data terms actually say

Mike's instinct, that a raw data feed likely violates source terms, is **half right and the half
that is wrong matters more than the half that is right.** The restriction is real, but it is
field-scoped and date-scoped, and it lands on prospecting rather than on publishing.

### 11.1 SAM.gov: three operative sentences

All quoted from [SAM.gov Terms of Use](https://sam.gov/about/terms-of-use), retrieved 2026-08-26.

**On sharing.** Under Data Access, System Accounts and API Keys:

> "If you want to share data publicly, only share data from public versions of APIs."

And under Sensitive Information:

> "You may not use any sensitive API to build out a public view of any SAM data. You must use the
> public version of any API if you wish to display or disseminate the public-facing data."

**Inference.** These sentences do not prohibit dissemination. They **route** it. The terms
contemplate that a user will display and disseminate SAM data and instruct which endpoint to take it
from. A product built on the public Contract Opportunities API or the public bulk extract is inside
the sanctioned path. A product built on a sensitive or FOUO endpoint is not, and the repo's existing
fail-closed discipline already keeps us on public sources.

**On acquisition method.**

> "Automated data gathering, web scraping tools are prohibited and, if detected, will result in the
> associated account(s) being denied access to SAM.gov via Login.gov."

**Inference.** The prohibition is on scraping the site. The same paragraph names the permitted route
(`open.gsa.gov/api/` and `sam.gov/data-services`). This is why the repo's reverse-engineered SBS POST
is the exposed component and the documented APIs are not, which is what the terra memo already said.

**On copyright.** Under Reuse and Copyright:

> "Most material on our site is free of copyright and may be copied and distributed without
> permission. Works produced by federal government employees in the course of their employment are
> generally not protected by copyright and are in the public domain in the U.S."

### 11.2 The D&B carve-out is the real restriction, and it is narrower than it looks

Under Restricted Data Use, the operative sentence for anything resembling prospecting:

> "Except for data elements identified above as D&B Open Data, under no circumstances are you
> authorized to use any other D&B data for commercial, resale or marketing purposes (e.g.,
> identifying, quantifying, segmenting and/or analyzing customers and prospective customers)."

And for the Open Data subset (legal business name, street address, city, state or province name,
state or province code, state or province abbreviation, country name, county code, ZIP or postal code):

> "shall not access, use or disseminate D&B Open Data in bulk (i.e., in amounts sufficient for use
> as an original source or as a substitute for the product and/or service being licensed hereunder)"

with a written-attribution requirement to D&B.

**The scope limits, quoted.** The terms state exactly which records carry D&B data:

> "all entity registration records with a last updated date earlier than 4/4/2022, all exclusions
> records with a created date earlier than 4/4/2022, and all base award notices with an award date
> earlier than 4/4/2022. These records show D&B as the Entity Validation Service (EVS) Source in
> records with D&B data."

**Two consequences, and the second is the useful one.**

1. **The prohibited use is described in words that exactly match prospecting**: "identifying,
   quantifying, segmenting and/or analyzing customers and prospective customers." Any list-building
   step that touches a D&B-sourced field is the risky operation, not the publishing step. This is
   the same conclusion the terra memo reached, now with the verbatim basis attached.
2. **The restriction is bounded by a date and a flag.** Records carrying D&B data are identifiable
   because they carry D&B as the EVS Source, and they are all older than 2022-04-04. **Inference,
   flagged for counsel because it rests on a fact I did not separately verify in this pass:** SAM
   entity registrations must be renewed annually, so an entity that is *currently active* has a last
   updated date well after 2022-04-04 and therefore should not carry D&B-sourced fields at all. If
   that holds, the D&B restriction bites on historical and archived records, not on the live
   list-3 universe the matcher actually uses.

**Concrete, implementable recommendation.** Add a gate that reads the EVS Source field and the
last-updated date on every entity record entering the matcher, and fails closed on any record
flagged D&B or dated before 2022-04-04. That converts an open legal question into a mechanical
filter with a log. It is cheap, it is in the repo's existing fail-closed idiom, and it gives counsel
something concrete to bless rather than an abstract question.

### 11.3 USASpending and the affirmative basis for redistribution

The [OPEN Government Data Act](https://www.govinfo.gov/app/details/PLAW-115publ435) (Title II of the
Foundations for Evidence-Based Policymaking Act of 2018, P.L. 115-435), as summarized on the federal
data policy repository:

> "requires agencies to make their data publicly available in open, machine-readable formats and to
> apply open licenses so that if data are made public there are no restrictions on copying,
> publishing, distributing, transmitting, adapting, or otherwise using the information for any
> purpose, commercial or non-commercial"

and, on the same page, the copyright status:

> "Data and content created by government employees within the scope of their employment are not
> subject to domestic copyright protection under 17 U.S.C. § 105. Government works are by default in
> the U.S. Public Domain."

([resources.data.gov Open Licenses](https://resources.data.gov/open-licenses/), observed 2026-08-26.)

The federal open-data definition of an open license explicitly includes the right to sell:

> "The license shall not restrict any party from selling or giving away the work either on its own or
> as part of a package made from works from many different sources."

**Caveat retained from the terra memo.** The USASpending *codebase* is CC0; a dataset-wide license
statement for every field was not located, and the API documents a search-date floor of 2007-10-01.
The affirmative basis above is statutory and copyright-based rather than a per-dataset license grant,
which is a stronger footing than a vendor terms page but still worth one counsel sentence.

### 11.4 What this permits, forbids, and leaves open

| Product shape | Terms posture | Basis |
|---|---|---|
| Per-firm, per-notice **derived work product** (the packet) | **Clearly the safest.** A transformative work product built from public-API data, sold as analysis, not as data | OPEN Government Data Act, 17 U.S.C. § 105, SAM "share data from public versions of APIs" |
| **Free industry report** from public notice and award data | Same as above | Same |
| **Notification** that a public notice matches a firm | Permitted, and worthless as a paid product on its own (see 11.5) | Same |
| **Raw or near-raw data feed** resold by subscription | **Mike's instinct is right here.** Nothing forbids redistributing public-API notice data, but a feed is the product shape most likely to be read as a substitute source, it is the shape D&B's bulk language targets if any entity fields ride along, and it is competing with a free official product | SAM D&B bulk language; 11.5 |
| **Prospect list** built by segmenting entity records | **The actually restricted operation** if any D&B-sourced field is involved. Mitigated by the EVS/date gate in 11.2 | SAM Restricted Data Use, verbatim |
| **Contractor contact acquisition** for outbound | **Still the open counsel gate**, unchanged from the terra memo. Note how the incumbents solve it: GovTribe's own docs say Launch includes only "public points of contact listed on opportunity and award records, such as POC details available from public sources like SAM.gov," while Growth adds "broader Beacon contact data" and **Clearbit enrichment** ([GovTribe plan docs](https://govtribe.com/docs/govtribe-user-guide/guides/choose-the-right-govtribe-plan), observed). They license a commercial contact provider rather than deriving contacts from SAM. That is the route the terra memo asked counsel about, and a competitor has already taken it |

### 11.5 The fact that decides the subscription question

**SAM.gov gives away the notification layer.** A user with a free Login.gov account can save a
search and turn on notifications, and SAM emails matching new and modified notices daily. GSA
publishes the instructions itself
([Save Searches and Notify, GSA documentation PDF](https://s3.amazonaws.com/falextracts/Documentation/Search/Save_Searches_and_Notify.pdf)),
and an APEX Accelerator publishes a walkthrough
([Montana APEX](https://montanaapex.org/sam/beta_sam_gov/2020/how-to-get-email-notifications-for-saved-contracting-opportunities-searches-in-beta-sam-gov/)),
both observed. No entity registration or UEI is required to save searches and receive the emails.

**Inference, and it is the answer to question 1 in one line.** Any subscription whose core promise is
"we will tell you when a notice appears" is priced against zero, delivered by the authoritative
source, with no freshness disadvantage. **A notification subscription is not a business.** Whatever
recurring revenue exists here has to be sold on what happens in the minutes *after* the notification,
not on the notification.

---

## 12. Recurring models that actually exist in this market

Five shapes, observed, from free to five figures.

**1. Free at the source.** SAM.gov saved-search alerts (11.5). Price: $0.

**2. Subscription intelligence, self-serve.** The incumbents publish real numbers.

| Vendor | Tiers, annual | What is included at the entry tier |
|---|---|---|
| HigherGov | $500 Starter, $2,500 Standard, $5,000 Leader ([pricing](https://www.highergov.com/pricing/)) | Search, tracking, AI tools |
| GovTribe | $1,500 Launch (1 user, federal, 50 records per export, up to 10 active pursuits), $1,900 Launch Plus, $5,000 Growth (5 users), $6,000 Growth Plus, Scale custom ([official plan docs](https://govtribe.com/docs/govtribe-user-guide/guides/choose-the-right-govtribe-plan)) | Search, saved-search alerts, pursuits, GovTribe AI access, MCP access, credits billed separately at $0.09 pay-as-you-go |

Note for anyone quoting these later: third-party comparison blogs currently publish a *different*
GovTribe ladder ($1,350 / $4,000 / $1,800 / $5,500). The vendor's own documentation is the figure
above. Use the vendor page.

**3. Hybrid software plus drafting, monthly.** CLEATUS publishes $180/month, or $135/month billed
annually, for proposal-writing features
([Cleat.ai](https://www.cleat.ai/features/proposal-writer/write-proposals-for-government-contracts), observed).

**4. Monthly service retainer with capped deliverables.** This is the model Mike is asking about, and
it exists in the wild. GovBidWriters sells a "VIP Program" where, "for a single all-inclusive monthly
fee," clients receive capture management ("Every week we deliver a curated list of federal, state,
and local solicitations aligned with your capabilities, certifications, and contract vehicles"),
proposal writing and submission ("Our team prepares and submits qualified proposals each month"),
growth strategy, teaming, and certification help
([GovBidWriters](https://www.govbidwriters.com/), observed 2026-08-26). The price is not published.

Three things to take from it. The bundle is **curated notification plus done-for-you drafting on a
monthly fee**, so the model is proven to exist. It is sold by an agency claiming 50+ consultants,
which is who can absorb unbounded monthly demand. And they **submit for the client**, which our shop
explicitly does not do, so it is not a like-for-like comparable.

**5. Fractional BD or capture retainer.** Standard retainer shape is a fixed monthly fee for a
defined number of hours, usually 10 to 20 per week, with vendor-published figures around $7,000 per
month for a fractional BD manager and month-to-month terms
([GTM11](https://gtm11.com/blog/fractional-business-development-manager-cost),
[GovCon In A Box](https://www.govconinabox.com/fractional-bd), both vendor-published). This matches
the practitioner rule from Part I: retainers fit **capture**, not proposal work (OST).

**What none of them do.** None of the five sells a per-claim-cited, gated deliverable with a named
human accountable for the contents and an explicit refusal when the evidence is thin. That gap is
the same one the prior-art scan found, and it survives this pass.

---

## 13. Is "notification plus an already-drafted response" a real wedge?

**Short answer: no, not as stated. It is two features, both of which already exist, at two different
vendors, and each vendor is one release away from the other half.**

### 13.1 The half that is already shipped, in the vendor's own words

HigherGov's Proposal Generator, per its own documentation
([HigherGov docs, AI Proposal Drafting](https://docs.highergov.com/ai-tools-and-accelerators/ai-proposal-drafting), observed 2026-08-26):

> "HigherGov's Proposal Generator is an advanced one-click solution for creating high quality
> opportunity-specific proposal drafts with minimal configuration."

Draft options include **"Draft Sources Sought."** Linking a Federal Profile lets the generator use
"publicly disclosed information including capability statements, awards, contracting vehicles,
certifications, and a SAM registration." Drafts are "typically ready in 3–5 minutes," the user gets
an email when the draft is done, and output exports to Word or PDF.

Read that against `brand/company.md`. The public-record-derived, notice-specific draft is **not** our
differentiator any more. It is a documented button on a $500/year product.

### 13.2 The other half is also shipped, at the other vendor

GovTribe sells saved-search alerts at every tier, and separately sells **automations**, described in
its own docs as "scheduled or event-triggered GovTribe AI runs that need credit-powered access,"
alongside an MCP server that connects the data to outside AI clients
([GovTribe plan docs](https://govtribe.com/docs/govtribe-user-guide/guides/choose-the-right-govtribe-plan), observed).

**Inference.** Event-triggered AI runs plus a saved-search alert is, architecturally, "notify me and
draft it." The pieces are assembled and sold today. Nobody has bolted the two halves together into a
single marketed promise, but the engineering distance is a feature ticket, not a moat.

### 13.3 What is actually left, scored honestly

| Candidate differentiator | Do incumbents have it? | How hard for a funded SaaS to copy | Durable? |
|---|---|---|---|
| Notice-specific AI draft | **Yes** (HigherGov, Sweetspot, SamSearch per repo) | Shipped | No |
| Alert on a matching notice | **Yes**, and free at SAM.gov | Shipped | No |
| Draft triggered automatically by the alert | Not marketed as one product; GovTribe has both pieces | One release | No |
| Zero-input start from a UEI, no account, no org library | No. HigherGov "strongly encourages" uploading company documents; every tool needs an account | Medium. Cuts against their onboarding and data-capture model | Partly |
| **Per-claim provenance with fail-closed gates** | No, per the prior-art scan and this pass | Hard. It is an operational cost with no engagement upside, and it forces the product to say "I could not verify this" | **Yes** |
| **A named human who is accountable for the contents** | No. SaaS ships a tool, not a warranty | Hard. It does not scale and it creates liability they price out | **Yes** |
| **The refusal**: a stated fill floor, a gaps page, and "nothing to buy on this one" | No | Hard for a different reason: a subscription's incentive is to generate more, not to decline | **Yes** |
| Veteran-owned, reachable, small | No | Not copyable, but also not a purchase reason on its own | Partly |

**Verdict.** "Notification plus an already-drafted response" is a **feature**. The defensible position
is one layer down: **accountability for the contents of the draft**, expressed as citations, gates, a
gaps page, a human name, and a willingness to say the map is thin. That is not a feature a SaaS ships
because its economics point the other way. A subscription product measured on engagement cannot
profitably tell a user there is nothing worth bidding this month. A per-decision service can, and
Part I's evidence says the no-sale is what produces the referral.

**The corollary Mike should hear plainly.** If the differentiator is accountability rather than
automation, then the recurring product cannot be "our alerts." It has to be "our judgment, standing
by, on your codes." That is a retainer for capture, and per OST it is the one retainer shape this
trade actually supports.

---

## 14. Revenue architecture for a solo operator

### 14.1 The three candidates, scored

| | A. Pure per-deliverable | B. Per-deliverable + event-billed code watch | C. Per-deliverable + capped standing retainer |
|---|---|---|---|
| Shape | $699 packet only | $699 packet, free code watch, packet is the bill when it fires | B, plus a small number of monthly capture-support clients |
| Revenue predictability | None. Fully episodic | Low, but the list compounds | Partial floor |
| Notice-supply exposure | Full (250–400/yr ceiling, repo F1) | Full | Reduced. Retainer revenue does not need a notice |
| Founder-hour exposure | Bounded by the 20-minute unit rule | Same | **Highest risk.** Retainers are scope-open by default |
| ToS exposure | Lowest. Derived work product only | Lowest | Lowest |
| Churn mechanic | Not applicable | Nothing to churn from. There is no monthly charge to cancel | Standard SMB churn, 10–15%/yr for sub-$15K ACV (vendor-published, Part I) |
| Precedent in the wild | Bidspeed marketplace, Fiverr | No direct comparable found | GovBidWriters VIP, fractional BD at roughly $7K/mo |

### 14.2 Recommendation

**Architecture B as the core, with a strictly capped C on top, and no data feed.**

1. **The $699 packet stays the only advertised paid SKU.** It is the thing with observed comparables
   ($395 Bidspeed, $995 Bidspeed, $85–$300 Fiverr, $300–$800 consultant equivalent) and it is the
   thing the factory is built to produce inside the unit rule.
2. **Code watch stays free and event-billed.** `sop/MARKETING.md` Door 9 already specifies this. The
   evidence in 11.5 is now the *reason*: a paid alert competes with a free official product, and an
   event-billed watch has no quiet-month churn surface. Free code watch is also the cheapest retention
   asset available, because it is a standing permission to send a packet email, which is the thing the
   whole business needs.
3. **Reframe the $249/month consultant feed, or drop it.** As a *data feed* it is the single most
   ToS-exposed and least defensible shape in the catalogue (11.4), and it is priced against free
   alerts. As a **gated, qualified shortlist with a requirement map attached**, it is a derived work
   product, it is the thing consultants cannot get from SAM alerts, and it sits inside the same
   provenance discipline as everything else. If it cannot be reframed that way, drop it: Part I noted
   that a soured feed subscription costs a referral relationship, and referral partners are ranked
   channel #2.
4. **Add a capped standing capture retainer only after the first repeat buyer**, at a hard cap of two
   or three clients, priced against the fractional band rather than the deliverable band, and scoped
   in hours or in deliverable count, never "unlimited." The consistent failure note across the
   productized-services evidence in Part I is that the shops that burned out promised unlimited work.
   GovBidWriters can promise "qualified proposals each month" because they have 50+ consultants. A
   solo operator promising the same thing has sold an option on his own evenings.
5. **Never sell raw data.** It is the one shape where Mike's instinct, the terms text, and the
   competitive reality all point the same way.

### 14.3 What ten customers looks like under B

Using Part I's first-ten plan and the repo's own unit rule, not a forecast:

- 10 packets at $699 is $6,990 of one-time revenue, at roughly 20 minutes of founder review each
  plus send and support time.
- The durable asset is not the revenue. It is **ten code-watch permissions**, ten firms whose award
  records are already mapped, and (per Part I) ten proof artifacts: references, coverage case
  studies, or documented reasons for no.
- The second packet to the same firm costs almost nothing to originate, because the match is already
  built and the permission already exists. That is where the compounding is, and it is why the code
  watch matters more than any subscription line.

**The number to instrument from order one:** what fraction of code-watch holders buy a second packet
within six months. That single number decides whether this business has recurring revenue at all,
and it is measurable without inventing a product.

### 14.4 Kill criteria for the subscription hypothesis

- **No second packet from any code-watch holder within six months of the first ten sales.** Then the
  business is per-deliverable only, the ladder in `sop/PLAN-V5.md` §4 should be simplified, and
  nobody should model recurring revenue.
- **Any consultant feed subscriber who cancels citing "I can get this from SAM alerts."** That is the
  11.5 problem arriving in the wild, and it means the reframe in 14.2.3 failed.
- **Any retainer client whose monthly hours exceed the cap twice.** Scope-open retainers are the
  documented burnout path.

---

## 15. A fourth high-risk assumption, added to Part I's three

**4. That accountability is a purchase reason rather than a preference.**
Part I's three assumptions stand. This pass adds one. The entire wedge now rests on buyers paying a
premium for citations, gates, a gaps page, and a named human, over a $500/year tool that produces a
Sources Sought draft in 3 to 5 minutes with one click (13.1). That is a real difference in the
artifact, and it is an untested difference in the *wallet*. The willingness-to-pay research already
showed the Fiverr floor at $85 and the buy-now competitor at $395; neither of those buyers was paying
for provenance.
**Test:** it is the same kill-test the repo already specifies, aimed correctly. Put the factory packet
next to a HigherGov Proposal Generator output on the same notice and ask a non-expert to name the
difference in 30 seconds. If the difference is only visible to someone who already values citations,
the wedge is a preference, not a purchase reason.
**If false:** the business is competing on price and turnaround against a $500/year subscription, and
the correct response is to move up-market to the notices and firms where being wrong is expensive,
not to defend $699 on a feature comparison.

---

## Part II sources

**Primary.** [SAM.gov Terms of Use](https://sam.gov/about/terms-of-use) (retrieved 2026-08-26; Data
Access, Sensitive Information, Restricted Data Use, Reuse and Copyright) ·
[resources.data.gov Open Licenses](https://resources.data.gov/open-licenses/) ·
[OPEN Government Data Act, P.L. 115-435](https://www.govinfo.gov/app/details/PLAW-115publ435) ·
[17 U.S.C. § 105](http://www.copyright.gov/title17/92chap1.html#105) ·
[USASpending API](https://api.usaspending.gov/) ·
[GSA documentation: Save Searches and Notify](https://s3.amazonaws.com/falextracts/Documentation/Search/Save_Searches_and_Notify.pdf).

**Vendor documentation (observed, authoritative for that vendor).**
[HigherGov AI Proposal Drafting docs](https://docs.highergov.com/ai-tools-and-accelerators/ai-proposal-drafting) ·
[HigherGov pricing](https://www.highergov.com/pricing/) ·
[GovTribe plan documentation](https://govtribe.com/docs/govtribe-user-guide/guides/choose-the-right-govtribe-plan) ·
[GovBidWriters VIP Program](https://www.govbidwriters.com/) ·
[CLEATUS proposal writer pricing](https://www.cleat.ai/features/proposal-writer/write-proposals-for-government-contracts) ·
[Bidspeed Marketplace](https://www.bidspeed.com/marketplace).

**Vendor-published commentary (direction, not decimals).**
[GTM11 fractional BD cost](https://gtm11.com/blog/fractional-business-development-manager-cost) ·
[GovCon In A Box fractional BD](https://www.govconinabox.com/fractional-bd) ·
[Montana APEX SAM.gov alert walkthrough](https://montanaapex.org/sam/beta_sam_gov/2020/how-to-get-email-notifications-for-saved-contracting-opportunities-searches-in-beta-sam-gov/).

**Internal.** `research/council/2026-08-23-legal-sources-terra.md` (superseded on the redistribution
question by the verbatim terms in §11, extended rather than contradicted on the contact question) ·
`sop/MARKETING.md` Door 9 · `sop/PLAN-V5.md` §7 · `brand/company.md` · `brand/offer.md` ·
`research/feasibility-review/REPORT.md` F1, F3 · `research/govcon-prior-art/REPORT.md`.
