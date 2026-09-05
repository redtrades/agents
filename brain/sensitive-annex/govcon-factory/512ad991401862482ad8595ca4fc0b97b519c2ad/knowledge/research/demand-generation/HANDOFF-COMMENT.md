# Handoff comment, ready to paste as a GitHub issue on `redtrades/govcon-factory`

**Suggested title:** Demand generation research pass: the hook is their own contract's end date, and the pond is 1,484 firms

**Suggested labels:** `research`, `needs-mike`

**Cross-link:** the Adversarial competitor capability test (`knowledge/research/competitive-assessment/`) and the Gartner market opportunity scan, per the commissioning brief.

---

## What landed

`knowledge/research/demand-generation/REPORT.md` plus four copy assets in
`knowledge/research/demand-generation/assets/`. Uncommitted. Read-only pass; nothing else in the tree
was changed.

Commissioned after Mike's correction that provenance, fail-closed gates and a named human are hygiene
rather than purchase drivers. The file treats this as a demand and proof problem and does not write
another competitor comparison.

## The five findings that change what we do

1. **The pond is 1,484 firms.** Distinct prime recipients of SDVOSB set-aside awards across the six
   target NAICS in 36 months, measured against USASpending, paginated to `hasNext=false`. Adding VOSB
   set-asides makes it 1,503. Every volume-based outbound tactic in the standard playbook is
   irrelevant here and several are actively harmful. Our entire lifetime send volume at three touches
   is about 4,500 emails.
2. **The strongest hook is the firm's own contract and its end date, not a recompete we found for
   them.** Two keyless API calls, 1.3 seconds, return the PIID, end date, potential end date, offers
   received, competition flag, set-aside, office and UEI. A fact about their own money requires them
   to believe nothing about our judgment, and it does not share a silhouette with the registration
   scams GSA and BBB warn about. Ranked table at REPORT §2.2.
3. **The contestability signal re-derives, and it is stronger at our buyer's dollar band.** 34.9% of
   awards labelled FULL AND OPEN COMPETITION in a 577-award $150K-$5M sample drew exactly one offer.
   That independently reproduces the vendor-measured 37% figure `offer-design` flagged for
   re-derivation. **The cost: the offer field is missing 32.6% of the time at the small band against
   11.8% above it.** The hook must fail closed on a missing offer count.
4. **Give away the buyer's own record, and design it so it consumes zero founder minutes.** The free
   artifact contains nothing but verbatim API fields with permalinks and timestamps. No prose, no
   synthesis, no ranking. That makes it mechanically checkable, so no human has to read it, which is
   the constraint that decides whether we can do it at all. REPORT §3.3.
5. **Only three of eleven channels get cheaper with an agent swarm, and they are one artifact.** The
   computed per-firm fact, the free one-page read, and the published adjudicated teardown come off the
   same pull and the same gate. Referral, events, LinkedIn and partnerships are this trade's dominant
   channels and every one is founder-hour bound. Say so rather than pretending otherwise.

## The unblock worth an hour of Mike's time

**The contact question is smaller than the repo has been treating it.** The open counsel gate asks
whether we may derive contacts from SAM entity records or the DSBS POST at scale. At 1,484 firms
there is a narrower question available:

> May we send a CAN-SPAM-compliant commercial email to an address a firm publishes on its own public
> website, where we hold the source URL and retrieval timestamp for that address, and never touch SAM
> entity or D&B contact fields?

An agent can work 1,484 websites firm by firm and fail closed where no address is published. Not
legal advice, and it is a different and much smaller question than the one currently open. REPORT §6.3.

## Two claims retired, from the sibling assessment

Neither appears anywhere in the assets, and neither should appear again in copy.

- "We cite and they don't." PrimeRFP's figures reconcile against USASpending and their methodology
  disclosure is better than we assumed.
- "A $500/yr subscription cannot give you a human." HigherGov prints Live Analyst Support on the
  Starter tier.

What survives, narrowly: competitors refuse when data is **missing**. They cannot refuse when data is
**present and contradicts the recommendation**, because that costs them the transaction.
`assets/04-public-teardown.md` carries a real specimen where the federal record contradicts itself
(competition flag says full and open, set-aside field says 8(a) sole source, offers received = 1).

## What the assets are

| File | Contains |
|---|---|
| `assets/01-cold-email.md` | Form R opener, 114 words unmerged and 118 merged, counted with a script against a real public record. Touches 2 and 3. Five ranked subject lines plus a banned list. Send mechanics sized to 1,484 firms |
| `assets/02-landing-page.md` | Above the fold, the identity strip, the published-price block, the 163-word "what am I buying," and the full spec for the free one-page read |
| `assets/03-objections.md` | Rewritten mid-session against SAS-GPS and the proposal-shop tier rather than the software tier. Concedes their track record by name and argues the four surviving edges |
| `assets/04-public-teardown.md` | The teardown template, a worked specimen, cadence, and the scaled-content policy limit that caps it at 1 to 2 a week |

## The test, and it does not start by sending anything

1. **Step 0, agent time, $0, no counsel gate.** Count hooks across all 1,484 firms. **Kill: fewer
   than 100 carry a class 1 hook**, and the product reverts to the notice-triggered object.
2. **Step 1, agent time, $0.** Build a contact list for the top 80 from firms' own websites. **Kill:
   under 50% hit rate.**
3. **Step 2.** One counsel hour on the §6.3 question.
4. **Step 3, ~$50 and ~6 founder hours.** Send 40, three touches, CTA is the free read rather than
   the sale. **Send to ranks 41 to 80, not the top 40**, because the list is finite and the best
   cohort should meet the tuned copy.
5. Split the 40 between the end-date subject and a refusal-led subject, to test whether the published
   refusal count is a purchase driver or hygiene. I expect hygiene, and Mike's standing correction is
   the reason.

**Single most informative number:** what fraction of firms who receive their own computed contract end
date reply at all. Below 5% and no amount of copy work fixes it.

## Blocked on Mike

- The narrow counsel question above.
- Footer company name and physical postal address, still unfilled across every outreach template.
- Sending domain with SPF, DKIM, DMARC.
- Four of the five business-legitimacy items on the landing page (entity, phone, address, founding
  year). The fifth, an attributable customer reference, does not exist and must not be simulated.

## Honest limits

No govcon-specific conversion data exists for any channel in the file; every reply-rate and lead-magnet
figure is cross-industry and vendor-published. Founder review time per teardown is unmeasured and the
whole publishing cadence rests on it. The samples behind the contestability figures are sorted, not
random, and were built with opposite sort orders so the bias runs both ways. Reddit and LinkedIn were
unreachable again, fourth consecutive pass.

## Coordination note

This session could not open the issue itself: `gh` is not installed in the workspace and an
unauthenticated GitHub API request from the sandbox returns 404. Same limitation the
competitive-assessment session hit.
