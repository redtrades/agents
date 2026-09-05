# Demand generation: the hook, the proof, the channels, and the cheapest way to find out

2026-08-26. Commissioned by Mike after his correction that integrity features are hygiene rather than
purchase drivers. Read-only research pass plus original measurement against public APIs. Nothing else
in this repo was changed by this work. Uncommitted; handoff runs through a GitHub issue on
`redtrades/govcon-factory` (see §8).

**Mike's correction, which governs the file.** Provenance, fail-closed gates and a named human on the
file are good practice. They stop us being bad. They do not make a busy, skeptical, previously burned
SDVOSB owner reach for a card. The problem is demand generation and proof, not differentiation.

**What this extends, so it does not repeat.**

- `knowledge/research/gtm-playbook/REPORT.md` ranked channels for a solo operator and settled cold
  email craft, the FAR 3.4 contingency posture, the SAM.gov terms question, and the finding that a
  notification subscription is not a business.
- `knowledge/research/offer-design/REPORT.md` established the price ladder, that the report category
  has collapsed to $19 to $199/mo, and recommended a $1,500 per-recompete pursuit file.
- `knowledge/research/competitor-pain/REPORT.md` established that the category is review-invisible
  and mapped six complaint clusters.
- `knowledge/research/competitive-assessment/REPORT.md` (sibling session, landed mid-pass) established
  that the software tier is invisible at the moment of purchase intent, that SAS-GPS is the closest
  real analogue, and that two of our positions are already occupied. **This file was partly rewritten
  after that one landed.** Where the two disagree, the sibling wins on competitive facts and this file
  wins on channel arithmetic.

**What is new here.** Four things the prior passes did not have. First, the size of the pond, measured
rather than estimated: **1,484 firms**, which changes every channel decision downstream. Second, an
independent re-derivation of the contestability signal from USASpending in our own six NAICS,
including its coverage rate, which offer-design flagged as an open kill risk. Third, a hook ranking
built on what is actually computable from keyless public APIs and what is not. Fourth, the copy
itself, in `assets/`.

**Evidence labels, same convention as the sibling files.**

- **Measured.** Computed in this session against a named public API on 2026-08-26, with the query
  shape recorded here so it can be re-run.
- **Observed.** Retrieved from the named page on 2026-08-26, quoted or transcribed.
- **Vendor-published.** A page from a party with an interest in the number. Direction, not decimals.
- **Repo.** Established elsewhere in this repository, cited rather than re-derived.
- **Inference.** My reading. Mike may reject it.

---

## 0. Bottom line

Nine findings, ordered by how much they change what Mike does this week.

1. **The pond is 1,484 firms, and that single number rewrites the channel plan.** Distinct prime
   recipients of SDVOSB set-aside contract awards across the six target NAICS in the 36 months to
   2026-08-26: **1,484**. Adding VOSB set-asides raises it to **1,503**. (Measured;
   `api.usaspending.gov/api/v2/search/spending_by_category/recipient/`, `set_aside_type_codes`
   `SDVOSBC, SDVOSBS, VSA, VSS`, `naics_codes` 236220, 541512, 541519, 561720, 541330, 238220,
   `time_period` 2023-08-26 to 2026-08-26, paginated to `hasNext=false`.) The cold-email industry
   sizes infrastructure for 1,000 sends a day. Our entire addressable universe, at three touches
   each, is about four thousand sends **in total, ever**. Volume tactics are not merely inefficient
   here, they destroy the only list we have.
2. **The strongest computable hook is the firm's own contract and its end date, not somebody else's
   recompete.** Two keyless API calls, 1.3 seconds wall clock, return a named contract, its end date,
   its potential end date, the offers it drew, the competition flag, the set-aside, the office and
   the UEI. (Measured, §2.) A fact about their own money with a date on it beats an opportunity we
   found for them, on three axes: it is unfakeable, it is uncheckable-by-anyone-else without doing
   the work, and it does not read like the pitch a scammer opens with.
3. **The contestability signal is real at our buyer's dollar band, and it is stronger there than at
   the top.** In a 577-award sample across the six NAICS at $150K to $5M, **34.9% of awards labelled
   FULL AND OPEN COMPETITION drew exactly one offer** (n=63), and 36.3% of FULL AND OPEN AFTER
   EXCLUSION OF SOURCES (n=135). In a separate 262-award sample skewed to large dollars, the same
   figures were 21.4% and 19.7%. (Measured.) This independently reproduces GovCon API's vendor-measured
   37% figure, which offer-design flagged for re-derivation, and closes that open item.
4. **And the same measurement finds the signal's cost: the offer field is missing about a third of
   the time at the small band.** `number_of_offers_received` was absent or zero on **188 of 577**
   small-band awards (32.6%) against **31 of 262** (11.8%) at the large band. (Measured.) Coverage
   gets worse exactly where our buyer lives. The hook must therefore fail closed on a missing offer
   count and fall back to the end-date fact, which has near-complete coverage.
5. **Give away the buyer's own record, not a sample of somebody else's.** The category is
   review-invisible (competitor-pain §2.1) but that stopped being the whole story when the sibling
   pass found SAS-GPS publishing named client testimonials with titles and employers. References are
   available to a competitor with customers, so they are not the gap. The gap is **the work product,
   published whole, before payment**, plus a free personalized artifact that costs us two API calls
   and zero founder minutes. §3 designs it so it never consumes founder review, which is the constraint that decides
   the whole thing.
6. **Only three of the eleven candidate channels get cheaper when an agent swarm runs them, and two of
   them are the same artifact.** The computed per-firm fact, the free one-page read, and the published
   teardown are one pipeline exposed at three levels of intimacy. Referral, events, LinkedIn and
   partnerships are the trade's dominant channels (Hinge, GTM §1.1) and every one of them is
   founder-hour bound. §4.
7. **Do not build programmatic entity pages.** A search for one contractor's name on 2026-08-26
   returned two HigherGov awardee pages, g2xchange, Fed360, USASpending and readthegovcontract before
   anything else (measured, §4.5). PrimeRFP runs the same page shape across 2.5M+ awardees
   (competitive-assessment §10.1). Google's spam policy names scraped-feed page generation as the
   central example of scaled content abuse
   ([Google Search Central](https://developers.google.com/search/docs/essentials/spam-policies),
   observed 2026-08-26). The open ground is the **adjudicated** page, one to two a week, with a
   verdict and a name on it.
8. **The contact question is smaller than the repo has been treating it, because the list is small.**
   The open counsel gate is about deriving contacts from SAM or DSBS at scale (GTM §5.1, terra memo).
   At 1,484 firms an agent can visit 1,484 company websites and record the address each firm
   publishes itself, with a URL and a retrieval timestamp per address. That is a different legal
   question and a much narrower one. §6.3. **This is the single highest-value unblock in the file and
   it is a one-hour counsel question, not a research problem.**
9. **The cheapest experiment does not start with sending anything.** Step one is counting how many of
   the 1,484 firms carry a hook at all, which costs agent time and nothing else, and which can kill
   the approach before a single email is written. §7.

**The recommendation in one line.** Lead with the firm's own contract end date, give away that firm's
own record free and machine-verifiable, sell one adjudicated file at $1,500, and treat the 1,484-name
list as a finite asset to be spent slowly rather than a funnel to be filled.

---

## 1. Method, and what to distrust in it

Every figure labelled **Measured** was computed in this session against `api.usaspending.gov`, which
needs no API key and carries no licence restricting redistribution of derived work (GTM §11.3, OPEN
Government Data Act). The queries are written out so anyone can re-run them.

Three limits, stated before the numbers rather than after.

- **Samples are not censuses.** The 577-award and 262-award samples in §0.3 and §0.4 were pulled with
  `sort` on award amount and a bounded page count, which is not a random sample. The two samples were
  built with opposite sort orders precisely so the bias runs in opposite directions, and the
  contestability result is stronger at the small band under both. Treat the direction as solid and
  the decimals as indicative.
- **FPDS miscoding is real and unquantified here.** GAO found roughly 18% of sampled contracts coded
  incorrectly on competition ([GAO-10-833](https://www.gao.gov/products/gao-10-833)). Nothing in this
  pass measures our own error rate. The specimen in `assets/04-public-teardown.md` is an example of a
  record that contradicts itself on its face, which is a reason to publish the fields side by side
  rather than a reason to trust either one alone.
- **The 1,484 count is a floor, not a ceiling, of the reachable market.** It counts firms that won a
  prime award under an SDVOSB or VOSB set-aside in those six NAICS in 36 months. Firms holding
  full-and-open awards, subaward-only firms, and firms certified but not yet awarded are all outside
  it. It is the right number for **list 3** as `AGENTS.md` defines it, and the wrong number for the
  newsletter audience.

---

## 2. The hook: what we can compute about one firm before we ever contact them

### 2.1 What the free record actually yields, measured

One search call plus one detail call against USASpending, keyless, **1.3 seconds** for the pair,
returns everything below for a named firm.

| Field | API path | Coverage in our samples |
|---|---|---|
| PIID, recipient legal name, UEI | `search/spending_by_award/`, `awards/{id}/` | Complete |
| Period of performance end date | `awards/{id}/period_of_performance.end_date` | Complete |
| Potential end date (base plus all options as recorded) | `.potential_end_date` | Near-complete; nulls occur |
| Offers received | `latest_transaction_contract_data.number_of_offers_received` | **67.4% at $150K to $5M; 88.2% above** (Measured) |
| Extent competed, with description | `.extent_competed_description` | Complete where a contract action exists |
| Type of set-aside, with description | `.type_set_aside_description` | Complete |
| Awarding office name and code | `awarding_agency.office_agency_name` | Complete |
| Solicitation identifier | `.solicitation_identifier` | Sparse. Null on most records I pulled |
| Full award history for a UEI | `search/spending_by_award/` with `recipient_search_text` | Complete back to FY2008 |

A worked pull, for the reader who wants to check the claim rather than take it: UEI `XCHST6L53NH6`
returns **169 prime awards since 2014, 125 of them in NAICS 236220, 138 of 169 (81.7%) at the Department
of Veterans Affairs**, and one contract, `36C24426N0808` at VA Pittsburgh, with an end date of
2027-10-04 and a potential end date of the same day. (Measured 2026-08-26.)

### 2.2 The ranking

Ranked by **hit strength × computability × distance from the fraud pattern**. That third factor is
not decoration: GSA publishes an industry bulletin about imposters and misleading marketing aimed at
this exact buyer, and GTM §9 already names "does this read as the scam" as the assumption with the
least evidence in either direction.

| Rank | Hook | The sentence it produces | Computable? | Fails how | Fraud-adjacency |
|---|---|---|---|---|---|
| **1** | **Their own contract's end date, with the option runway** | "36C24426N0808 ends 2027-10-04 and FPDS shows no option years recorded past it" | **Yes. 2 keyless calls, 1.3s.** Near-complete coverage | Nulls on `potential_end_date`; mods move dates; delivery orders under an IDV behave differently | **Lowest.** We are reading their own file back to them, not selling them a secret |
| **2** | **Concentration, as a share with a date attached** | "81% of your 169 awards are at one agency, and the biggest one ends in 14 months" | **Yes.** Same two calls | Legal-name splits across UEIs understate the total | Low |
| **3** | **The contestability gap on a named award** | "The solicitation said full and open. The award drew one offer." | **Yes, when the field is present.** Missing a third of the time at the small band | Missing offer count; GAO-measured miscoding; and the 8(a) sole-source case in `assets/04` where the flag and the set-aside contradict each other | Low, but needs a sentence of explanation, so it works better as fact two than as the lead |
| **4** | **A live notice at the office that already buys from them** | "The office that awarded you X posted Y, closing in 11 days" | Yes, via SAM Contract Opportunities API (free key) | The 8-day median window (repo) caps the price and kills the second touch | Medium. Deadline plus stranger is the scam silhouette |
| **5** | **Somebody else's recompete they could take** | "This contract in your NAICS ends in 9 months and the incumbent looks weak" | Yes | Speculative for them; it is an opportunity, not a fact about them | Medium-high. "I found something for you" is the opening line of the thing they were burned by |
| **6** | **Incumbent's set-aside certification lapsing before contract end** | "The incumbent's 8(a) exit predates the option year" | **Effectively no.** Source is S4, the unofficial DSBS POST, rated **High fragility** in `sop/DATA.md`, with no located commercial-use authorization (terra memo) | Fires rarely; absence of a certification record means nothing, and roughly half of firms have no profile (GovCon API, vendor-published) | Low, but the source problem is disqualifying for outbound |
| **X** | **Their SAM registration expiry** | "Your registration expires in 41 days" | Yes, and it hits hard | n/a | **Banned.** It is the literal opening line of the registration scams GSA and BBB warn about. Naming it here so nobody rediscovers it as a clever idea |

### 2.3 Why hook 1 beats hook 5, which was the brief's leading candidate

The brief listed "their incumbent contract expiring in N months" alongside "a recompete they are not
tracking." Those two look like one hook and they behave differently.

A recompete we found for them is a claim about the future of a contract they do not hold. It asks the
reader to trust our judgment before the fact means anything, which is the wrong order for a first
touch from a stranger. Their own contract's end date asks them to trust nothing. It is a date on a
record with their name on it, and they can check it in one click.

**Inference, and it is the one I would defend hardest in this file.** Three vendors can already
compute a fact about a firm, so computing one is not the advantage. The advantage is that we can
compute a fact **the firm itself has not looked at recently** and hand it over free. An owner running
six jobs does not open USASpending to check when their own contracts end. The hook exploits a gap in
attention, and attention is harder for a funded competitor to buy than data is.

### 2.4 What the hook must never do

- Assert intent. The record shows an end date. The office may extend, bridge, absorb the work into a
  vehicle, or stop buying. Say what the field says, per `AGENTS.md` rule 3.
- Manufacture a deadline. There is no deadline on a recompete hook, and that is a feature: it is what
  makes a second touch and a four-figure price compatible (offer-design §5.2).
- Read absence as a signal. A missing offer count is missing, not one. A missing certification record
  is missing, not lapsed.

---

## 3. Proof without payment

### 3.1 The constraint that decides the design

Every option below costs founder minutes or does not. `AGENTS.md` rule 1 requires Mike's approval on
anything that leaves, and a wrong number on a public page is a reputation gate failure. So the real
question is not "how much proof do we give away." It is **how much proof we can give away that
requires no human judgment**, because judgment is the resource that runs out at ten customers.

That constraint eliminates the obvious answer and produces a better one.

### 3.2 The four options, assessed

| Option | Founder cost per unit | What it proves | Copyability | Verdict |
|---|---|---|---|---|
| **A. Publish the full sample deliverables openly, no gate** | **Zero.** The ten samples exist, gates green, double-bannered (repo) | That our work is checkable. Does **not** prove we can do theirs | A competitor can read our template. They cannot read our gates, which are operational | **Do it this week.** Cost is already sunk |
| **B. Free partial specific to their pursuit** | **Zero if and only if it contains no synthesis.** See §3.3 | That we already did work on *their* record | Low. The value is the personalization, which costs compute per firm | **The conversion mechanism.** Recommended |
| **C. Public gallery of past deliverables** | Zero, but there are no past deliverables. Zero customers | Nothing yet | n/a | **Defer.** It is option A wearing a different label until somebody buys |
| **D. Teardown of a real solicitation, published** | **The binding cost. Unmeasured.** Public numbers need review | That we adjudicate, not just cite | High, and irrelevant: a vendor whose footer reads "never say no bid" will not publish refusals | **The compounding channel.** 1 to 2 a week, capped |

### 3.3 The design that makes B free

The free artifact contains **nothing but fields copied verbatim from an API response**, one per line,
each with a permalink and a retrieval timestamp. No prose, no synthesis, no ranking, no
recommendation. Spec and exact layout in `assets/02-landing-page.md`.

Three consequences fall straight out of that rule.

- It is **mechanically checkable**. A `gate_runner.py`-shaped test can assert that every printed value
  equals the value at the linked source. No human decides anything, so no human has to read it.
- It is **impossible to be wrong about in an interesting way**. The worst failure is a stale pull,
  which the printed timestamp already discloses.
- It **demonstrates the paid product by omission**. The free page shows the offer count next to the
  competition flag and does not say what that means. The gap between the two fields is visible and
  unresolved, and resolving it is what $1,500 buys. `assets/04-public-teardown.md` shows the resolved
  version on a real record.

### 3.4 What the evidence for this is, and how weak it is

Honest, because the prior passes were: **there is no published conversion data for any lead magnet in
the govcon niche.** offer-design §6 already established that and it has not changed.

The cross-industry direction, vendor-published aggregation, is that a free scoped audit converts at 5
to 15% opt-in and wins on the quality of what it produces, while generic ebooks sit near 3% with
about 12% read-through
([shno.co](https://www.shno.co/marketing-statistics/lead-magnet-conversion-statistics),
[digitalapplied](https://www.digitalapplied.com/blog/lead-magnet-conversion-benchmarks-2026-b2b-data-reference)).
Both sources tell you to score a magnet by how many opt-ins you would put on a sales call rather than
by opt-in rate. A free scoped audit is exactly the shape of option B.

The competitor evidence is stronger than the benchmark evidence. GovCon API runs six free
single-answer tools feeding a $19 to $79/mo product; PrimeRFP publishes an aggregate count free and
gates the named rows, and on its diligence page shows two figures and emails the rest; Fed-Spend runs
a free tier of ten searches with full results and argues explicitly that it is not a bait-and-switch
(offer-design §6, all observed). Three competitors independently converged on "show a real answer,
partially" and that is worth more than a benchmark table.

### 3.5 The published refusal count, and why I am not confident about it

`knowledge/research/competitive-assessment/REPORT.md` §8.3 recommends publishing the refusal count as
the single defensive action, on the argument that a competitor can copy a marketing line about telling
you not to bid in an afternoon and cannot copy a counter that goes up.

The argument is sound about **defensibility** and unproven about **demand**. Mike's standing
correction applies to it with full force: a refusal counter is an integrity feature, and integrity
features are hygiene. A busy owner does not buy because a vendor publishes how often it says no.

**How I would treat it.** Build the counter because it costs a database column and it is the cheapest
insurance against a funded competitor copying our positioning. Put it in the fold as a link, not as
the headline. Then test it as a headline against the end-date hook, and expect it to lose. §7.5
specifies that test. If it wins, that is a genuinely surprising result and it changes the whole page.

---

## 4. Channels, ranked by what an agent swarm makes cheaper

### 4.1 The arithmetic that reorders everything

1,484 firms. Three touches each, ever. Roughly 4,500 sends across the entire life of the current
pond. Against that:

- Best practice in 2026 is 20 to 30 sends per mailbox per day, and sending 1,000 a day needs 35 to 50
  mailboxes across 12 to 25 domains ([maildeck](https://maildeck.co/blog/cold-email-infrastructure-cost-2026/),
  vendor-published, observed 2026-08-26). **None of that applies.** One domain, one mailbox, 20 to 40
  a day, done in three months.
- Cold-email infrastructure runs $0.40 to $4.50 per inbox per month (same source). Our infrastructure
  bill is therefore roughly **$20 to $50 a month**, not a line item worth optimizing.
- Gmail requires spam complaints below 0.30% and recommends below 0.10%
  ([Gmail sender guidelines](https://support.google.com/a/answer/81126), observed 2026-08-26). At 40
  sends a day, three complaints in a week is already at the recommended ceiling. The three-touch cap
  is a deliverability control as much as a courtesy.

**Inference.** The agent swarm earns its keep by knowing more per name rather than by sending more
names. A solo operator with a spreadsheet can send 1,484 emails in a week. Nobody working alone can
compute a checked, cited, per-firm fact for 1,484 firms and then refuse to send where the fact fails
a gate. That inversion is the thesis of this section.

### 4.2 The ranking

Cost is cash. Time-to-first-customer assumes the counsel gate in §6.3 clears. Agent-swarm gain is my
judgment on a 0 to 10 scale of how much cheaper the channel gets per unit when agents run it.

| # | Channel | Cash cost | Time to first customer | Agent-swarm gain | Evidence strength | Gate |
|---|---|---|---|---|---|---|
| 1 | **Computed-fact outbound over the 1,484-firm census** | ~$50/mo | 3 to 8 weeks | **10** | Signal-based personalization at 15 to 25% reply vs 3.43% platform average (vendor-published, [Amplemarket](https://www.amplemarket.com/blog/cold-email-benchmarks), [InboxKit](https://www.inboxkit.com/learn/cold-email-reply-rate-benchmarks-2026)); no govcon-specific figure exists | **Counsel, narrowed. §6.3** |
| 2 | **The free one-page read, self-serve on a UEI** | Build once | Immediate once traffic exists | **9** | Three competitors run partial-answer free tools (offer-design §6, observed); free-audit benchmark (vendor-published) | Needs the landing page. `sop/MARKETING.md` Door 1 |
| 3 | **Published adjudicated teardowns, 1 to 2 a week** | ~$0 | 3 to 9 months | **7**, capped by founder review | Domains created 2026-01-24 and 2026-04-10 hold page-one slots (competitive-assessment §10.2); the intent query currently returns government PDFs | Founder review time. Measure on page one |
| 4 | **Warm referral from paid peers** (consultants, cert shops, bonding agents, GovCon CPAs) | $0 plus 15 to 20% terms | 4 to 10 weeks after one shipped file | **2** | Referral is the dominant lead source in govcon (Hinge, vendor-published, GTM §1.1) | One shipped sample and a written term |
| 5 | **Getting named in the AI answer** | A page of copy | 60 days to test | **4** | Thirteen vendors named across eleven buyer-intent searches, zero from the software tier; the five things the named ones have in common are entity, phone, address, founding year, references (competitive-assessment §9.3, §10.3) | Publish the five. Four are free |
| 6 | **Founder-led LinkedIn** | $0 | Unpredictable | **1** | High-growth govcon firms rank social networking second among techniques used (Hinge, vendor-published) | Mike-time only. No auto-post |
| 7 | **Live rooms** (NVSBE Dec 8-9 Cleveland; NVSBC VETS; NaVOBA Joint Forces Forum) | Travel | Months | **0** | VETS 26 drew more than 2,000 veteran-owned businesses, agencies and partner organizations, with NAICS-matched networking sessions ([NVSBC](https://nvsbc.org/events/), vendor-published, observed 2026-08-26); VA OSDBU lists NVSBE (repo) | Calendar. Register now, it is free |
| 8 | **APEX / SBDC as awareness** | $0 | Indirect | **1** | 95 centers, 300+ local offices, 600+ procurement professionals; 54,000 clients served in 2019 (vendor-published aggregations, observed 2026-08-26). They cannot endorse (SBDC and SBA non-endorsement language, repo) | Hand over free assets. Never pitch |
| 9 | **Per-NAICS newsletter** | ~$10/mo | Not an acquisition channel | **9 for production, 0 for list growth** | repo, `sop/MARKETING.md` Door 2 | Say out loud that it retains rather than acquires |
| 10 | **Programmatic entity pages** | ~$0 | Never | **10 for production, negative for outcome** | §4.5 | **Do not build** |
| 11 | **Paid ads** | n/a | n/a | n/a | Settled no (repo, growth-plan §2) | Do not revisit before repeat purchase is measured |

### 4.3 The three that compound, and why they are one thing

Channels 1, 2 and 3 are the same pipeline exposed at three levels of intimacy.

```
one contract record
        |
   +----+-------------------+------------------------+
   |                        |                        |
one line in an email    the free one-page read    the published teardown
(their fact, no verdict) (their fields, no verdict) (a stranger's record,
                                                     with a verdict)
```

Building all three costs barely more than building one, because the expensive part is the pull and
the gate, and both are shared. That is the specific thing an agent swarm does that a solo operator
cannot: three channels off one artifact, with no marginal headcount behind any of them.

Channels 4 through 8 are where this trade's money actually comes from and none of them gets cheaper
with agents. Keep all five, and be honest that they are Mike's five hours a week and will not scale
past it.

### 4.4 What the newsletter is for, stated plainly because the repo is ambiguous

`sop/MARKETING.md` puts the newsletter at the centre of the diagram. The arithmetic says it belongs
after the first touch, not before it. A newsletter grows a list from traffic, and we have no traffic.
It is a retention and permission asset, which is exactly what GTM §14.3 concluded about code watch,
and it should be resourced as one.

### 4.5 Programmatic entity pages: the test I ran and the answer

**Measured.** I searched a real contractor's legal name plus "federal contracts profile" on
2026-08-26. The results, in order: two HigherGov awardee pages for the same firm, g2xchange, Fed360,
a USASpending award page, a second g2x property, and readthegovcontract. The raw entity page is
saturated, and PrimeRFP publishes the same shape across 2.5M+ awardees (competitive-assessment §10.1).

Second measurement: a search for an archived VA sealed-bid solicitation number returned nothing
relevant at all, while a search for a live VA solicitation number returned HigherGov contract-opportunity
pages and mysetaside.com. So the record-level SERP is partly occupied and partly empty, and the part
that is empty is empty because those records are stale rather than because nobody is trying.

Add the policy risk. Google defines scaled content abuse as generating many pages primarily to
manipulate rankings, and names scraping feeds to generate many pages with little added value as a
central example
([Google Search Central](https://developers.google.com/search/docs/essentials/spam-policies), observed
2026-08-26). 1,484 auto-generated firm pages is that example.

**Conclusion.** Publish few pages with a verdict on each rather than many pages with a record on each.
The verdict is what makes the page not-scraped-content, and it is also the only thing on it a
competitor is structurally unwilling to copy. Template in `assets/04-public-teardown.md`.

---

## 5. The copy

Written, not described, in `assets/`. Four files.

| File | Contains |
|---|---|
| `assets/01-cold-email.md` | Form R opener at 114 words unmerged and 118 merged, counted with a script against a real public record; touch 2 and touch 3; five ranked subject lines with the banned list; send mechanics sized to 1,484 firms |
| `assets/02-landing-page.md` | Above-the-fold headline, subhead, UEI control, the identity strip, the published-price block, the one-paragraph "what am I buying" at 163 words, and the full spec for the free one-page read |
| `assets/03-objections.md` | "How do I know this is any good," "why you rather than a proposal shop since 2002," "why not the free SAM alerts," and the objection nobody says out loud |
| `assets/04-public-teardown.md` | The teardown template, a real worked specimen where the federal record contradicts itself, cadence, and the scaled-content policy limit |

**Three rules the copy follows and the reasoning behind each.**

1. **Every merged field is a verbatim API value with a printed retrieval timestamp.** Not a style
   choice. It is what lets an email go out without twenty minutes of founder reading per firm, and it
   answers the staleness complaint that dominates the only review corpus in this category
   (competitor-pain §2.2).
2. **The price is in the email and above the fold.** Of every services provider on page one of eleven
   buyer-intent searches, not one publishes a price, including SAS-GPS, which advertises "Transparent
   Pricing" behind a seven-field form (competitive-assessment §10.2, observed). This is free and
   nobody else does it.
3. **Anti-slop is a send gate, not a review pass.** No em dashes, no "I hope this finds you," no
   adjective stacks, no "not X but Y," no manufactured urgency. The existing rule in
   `brand/voice.md` stands: any sentence that could survive being said about an empty template is not
   selling anything. Every sentence in `assets/01` names a field or a number that could only come
   from that firm's record.

---

## 6. Three things that are blocking, and one that is smaller than it looks

### 6.1 The two claims that are now retired

Do not put either in copy again.

- ~~"We cite and they don't."~~ PrimeRFP names FPDS-NG, SAM.gov and USASpending, discloses a $100K
  award-level floor and the DoD reporting lag, and their figures reconcile against USASpending
  (competitive-assessment §0.9).
- ~~"A $500/yr subscription cannot give you a human."~~ HigherGov prints Live Analyst Support on the
  $500/yr Starter tier ([HigherGov pricing](https://www.highergov.com/pricing/), observed 2026-08-26).

What survives, in its narrow form: competitors already refuse when data is **missing**. What they
structurally cannot do is refuse when the data is **present and contradicts the recommendation**,
because that costs them the transaction. Citation without a gate is a bibliography.

### 6.2 The competitive set was wrong and the copy has been rewritten

The buyer looking for help does not encounter HigherGov, Sweetspot or PrimeRFP. Across eleven
buyer-intent searches the entire software tier was named zero times (competitive-assessment §9.3).
`assets/03-objections.md` was rewritten mid-session to argue against SAS-GPS and the proposal-shop
tier. The harder objection is not "why not use HigherGov." It is "why you rather than a
twenty-four-year-old SDVOSB with named testimonials and an A+ BBB record," and the honest answer
concedes most of it.

### 6.3 The contact question, narrowed

GTM §5.1 calls the contact-source ruling existential and it is, in the form it has been asked. The
question on the table has been: may we derive contractor contact fields from SAM's Entity API or the
DSBS POST at scale. SAM excludes POC email as FOUO, the DSBS route is an undocumented internal POST
with no located commercial-use authorization, and SAM's restricted-data language on D&B fields
describes prohibited use in words that exactly match prospecting (GTM §11.2).

**At 1,484 firms, there is a different question available.** An agent can visit each firm's own
website, record the contact address the firm publishes about itself, and log the URL and retrieval
timestamp per address. That is first-party published information, not a SAM field, not a D&B field,
and not a bulk extract. It fails closed where no address is published.

Two things make this tractable that would not be at 50,000 firms: the list is small enough to do
firm by firm, and every address carries its own provenance record, which is the same discipline the
deliverables already run under.

**The narrow question for counsel, in one sentence:** may we send a CAN-SPAM-compliant commercial
email to an address a firm publishes on its own public website, where we hold the source URL and
retrieval timestamp for that address and never touch SAM entity or D&B contact fields?

I am not a lawyer and none of this is advice. The question is smaller than the one currently open,
and getting it answered is the highest-value hour in this file.

### 6.4 What has not been established

- **No govcon-specific conversion data exists for any channel in this file.** Every reply-rate and
  lead-magnet figure quoted is cross-industry and vendor-published. Anyone quoting §4.2 must carry
  that caveat.
- **Founder review time per teardown is unmeasured.** The whole cadence in `assets/04` rests on it.
  Measure it on page one before promising a rate.
- **The 15 to 25% signal-based reply figure is from cold-email vendors selling signal-based tooling.**
  It is the direction, not the number, and our sample will be 40, which cannot distinguish 8% from
  20% anyway.
- **Whether anyone searches a solicitation number is unknown.** competitive-assessment §10.3 Test A
  is the right way to find out and this file does not duplicate it.
- **Reddit and LinkedIn remain unreachable**, as in every prior pass. Fourth consecutive report with
  no practitioner-forum sentiment. It needs a human with a browser.
- **The refusal counter's effect on conversion is untested and I expect it to be small.** §3.5.
- **SAS-GPS's named contract wins are checkable against USASpending and nobody has checked them.**
  Flagged in the sibling report and worth an hour, because if they check out that firm has the most
  substantiated track record in the competitive set and our copy should be more deferential still.

---

## 7. The test

### 7.1 The principle

The expensive mistake available right now is spending the 1,484-name list on untested copy. 40
exposures burns 2.7% of the universe; two batches burns 5.4%. So the test is sequenced so that the
cheapest disconfirming evidence arrives first, and the first two steps cost no list at all.

### 7.2 Step 0: count the hooks. Agent time, two days, $0 cash, no counsel gate

Run the §2.1 pull across all 1,484 firms. For each, record which hook class it carries: class 1 (own
contract ending 6 to 18 months out with option runway recorded), class 2 (concentration share above
some threshold), class 3 (a contestability gap on a named award), or none.

**This is the cheapest possible kill.** Sizing from the 6.4% rate measured on a small-dollar SDVOSB
sample and 12 to 15% on a large-dollar mixed sample (Measured, §0), expect somewhere between 100 and
250 firms with a class 1 hook. **Kill condition: fewer than 100 firms across the six NAICS carry a
class 1 hook.** If that fires, the census hook has no supply, and the product reverts to the
notice-triggered object on its 8-day clock, which is the existing V6 plan.

### 7.3 Step 1: build the contact list the safe way. Agent time, three days, $0

For the top 80 firms by hook strength, visit the firm's own website and record a published contact
address with its source URL and retrieval timestamp. Fail closed where none exists. Report the hit
rate. **A second, quieter kill lives here: if fewer than half of the 80 publish a usable address, the
own-website route is not a route and §6.3 goes back to counsel unchanged.**

### 7.4 Step 2: one counsel hour. Mike, one hour

The narrow question in §6.3. Everything after this depends on it.

### 7.5 Step 3: send 40. Two weeks, ~$50 cash, ~6 founder hours

**Send to ranks 41 to 80 by hook strength, not the top 40.** This is a deliberate trade against GTM
§8, which says to use the strongest artifacts on the first three customers. That advice was written
before anyone knew the list was 1,484 names. Testing copy on the second-best cohort keeps the best
cohort intact for the tuned second batch, and it costs a slightly weaker read of the ceiling.

- Three touches, `assets/01-cold-email.md`, no deadline because the object has none.
- The CTA is the free one-page read, not the sale. The sale is offered only after the free read is
  taken.
- Split the 40 evenly between two subject lines: `{pid} ends {end_date_short}` and the refusal-led
  variant `files I refused this month, and why yours might be one`. This is the §3.5 test of whether
  the refusal counter is a purchase driver or hygiene. **I expect the end-date line to win and the
  result to be worth knowing either way.**
- Log the reason for every no, and count "who are you" and "is this a scam" as their own category
  rather than as generic rejection (GTM §9.3).

### 7.6 What the numbers have to be

| Measure | Success | Kill |
|---|---|---|
| Reply rate on 40 | ≥6 replies (15%) | **<2 replies (5%). The hook is not a hook** |
| Free read taken, of repliers | ≥50% | **<10%. Giving away proof is not the conversion mechanism and §3 is wrong** |
| Free read → paid | ≥1 of the first 20 free reads | **0 paid after 80 exposures across two batches.** The repo's existing gate discipline |
| Own-website contact hit rate | ≥50% of 80 | <50%, see §7.3 |
| Founder minutes per free read | 0 | **Anything above 0 means the §3.3 no-synthesis rule leaked and the design failed** |

**The single most informative number, if only one is instrumented:** what fraction of firms who
receive their own computed contract end date reply at all. That is the hook test with everything else
stripped out. Below 5% and no amount of copy work fixes it.

### 7.7 What this test does not answer, and what does

It does not test whether the intent-query channel has volume, and it should not, because
competitive-assessment §10.3 Test A already specifies that experiment: publish one page targeting a
sources-sought help query with a complete, ungated sample and a published price, then measure
impressions rather than conversions for 30 days, with a kill at fewer than 100 impressions. Run both.
They cost nothing to each other and they fail in different directions.

---

## 8. Coordination

The sibling handoff convention is a GitHub issue on `redtrades/govcon-factory`.

**This session could not post it.** The `gh` CLI is not installed in this workspace and an
unauthenticated request to the GitHub API from the sandbox returns 404, so there was no authenticated
path to the issue tracker. `HANDOFF-COMMENT.md` in this directory is written ready to paste. Mike, or
the next session with `gh` available, should open the issue and cross-link the two sibling sessions
named in the brief: the Gartner market opportunity scan and the Adversarial competitor capability test
(`knowledge/research/competitive-assessment/`).

Per `AGENTS.md`, claim before touching the tree: `scripts/issue-claim.sh <N>`, then close with
`scripts/issue-complete.sh <N> --evidence "..."`.

---

## Sources

**Measured this session.** All against `https://api.usaspending.gov`, keyless, 2026-08-26.
`/api/v2/search/spending_by_award/` · `/api/v2/search/spending_by_award_count/` ·
`/api/v2/search/spending_by_category/recipient/` · `/api/v2/awards/{generated_internal_id}/`.
Filters and page counts are written out inline at §0.1, §0.3, §0.4 and §2.1 so every figure can be
re-run.

**Primary.**
[Google Search Central, spam policies for Google Web Search](https://developers.google.com/search/docs/essentials/spam-policies) ·
[Gmail email sender guidelines](https://support.google.com/a/answer/81126) ·
[GAO-10-833](https://www.gao.gov/products/gao-10-833).

**Observed, 2026-08-26.**
[HigherGov pricing](https://www.highergov.com/pricing/) ·
[SAS-GPS](https://sas-gps.com/) ·
[NVSBC events](https://nvsbc.org/events/) ·
[NaVOBA Joint Forces Forum](https://www.navoba.org/JFF).

**Vendor-published (direction, not decimals), all observed 2026-08-26.**
[Amplemarket 2026 cold email benchmarks](https://www.amplemarket.com/blog/cold-email-benchmarks) ·
[InboxKit reply-rate benchmarks 2026](https://www.inboxkit.com/learn/cold-email-reply-rate-benchmarks-2026) ·
[Instantly 2026 cold email benchmark report](https://instantly.ai/cold-email-benchmark-report-2026) ·
[Maildeck, cold email infrastructure cost 2026](https://maildeck.co/blog/cold-email-infrastructure-cost-2026/) ·
[shno.co lead magnet statistics](https://www.shno.co/marketing-statistics/lead-magnet-conversion-statistics) ·
[digitalapplied lead magnet benchmarks](https://www.digitalapplied.com/blog/lead-magnet-conversion-benchmarks-2026-b2b-data-reference) ·
[Norcal APEX, who we are](https://www.apexnorcal.org/about-us/about-us-who-we-are/) ·
[SupplierDiversity.com on APEX Accelerators](https://www.supplierdiversity.com/blog/apex-accelerators-free-government-contracting-help/).

**Internal, cited rather than re-derived.**
`AGENTS.md` · `sop/PLAN-V5.md` · `sop/MARKETING.md` · `sop/DATA.md` · `sop/SOP-DELIVERABLES.md` ·
`brand/offer.md`, `brand/customer.md`, `brand/voice.md` ·
`templates/outreach/email-1-opener-v5-draft.md`, `templates/outreach/footer-v5-draft.md` ·
`knowledge/research/gtm-playbook/REPORT.md` Parts I and II ·
`knowledge/research/offer-design/REPORT.md` §1, §5, §6, §8 ·
`knowledge/research/competitor-pain/REPORT.md` §2.1, §2.2, §2.5, §2.7 ·
`knowledge/research/competitive-assessment/REPORT.md` §0, §3.2, §8.3, §9.2.1, §9.3, §10 ·
`research/feasibility-review/REPORT.md` F1, F7, F10 ·
`research/council/2026-08-23-legal-sources-terra.md` · `samples/sample-set/`.
