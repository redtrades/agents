# Outreach Playbook — SDVOSB Sources Sought Cold Email

2026-08-22. Supports PLAN-V3 §7 (sales) and Week 1–2 validation gates. Part 1: what converts + 3 templates + workflow/tooling. Part 2: skills shortlist.

---

## Part 1A — What actually converts (2026 data)

### The numbers that matter

- Average cold email reply rate is ~3.4%; top-10% campaigns clear ~10.7%. The single biggest separator: emails referencing a **specific, timely buying signal** hit 15–25% reply rates — ~5x baseline ([Instantly benchmark report](https://instantly.ai/cold-email-benchmark-report-2026), [Cleverly](https://www.cleverly.co/blog/cold-email-statistics)). A Sources Sought notice closing in 12 days that matches the firm's NAICS **is** that signal. The whole strategy rides on this one fact.
- **Length:** 50–80 words beats longer email by ~65% on replies; every sentence past 80 words lowers reply probability (Lavender, 300K+ emails: [best length](https://lavender.ai/blog/best-length-cold-email), [benchmark report](https://lavender.ai/blog/the-cold-email-benchmark-report)). Average read time is ~9 seconds. Must be readable on a phone without scrolling ([30MPC](https://www.30mpc.com/newsletter/the-data-backed-cold-email-formula-the-exact-words-length)).
- **Subject lines:** 3–6 words, sentence case or lowercase, specific not clever. Mobile truncates ~60 characters. Naming the concrete thing ("APG plumbing sources sought") outperforms curiosity bait. Personalized subjects lift opens ~26–31%.
- **Structure** (Lavender/30MPC consensus): Trigger → so-what → value → one ask. 30MPC's key refinement: don't just state the trigger, **segue it to the problem** — trigger alone reads robotic ([4 questions framework](https://www.30mpc.com/newsletter/4-questions-to-write-painfully-triggering-cold-emails)).
- **CTA:** one CTA only — a second CTA cuts replies ~37%. Low-friction interest-based asks ("Worth a look?", "Want the outline?") beat calendar asks ("got 30 minutes?"). For a $450 product, never ask for a meeting — ask for permission to send the thing.

### Follow-up cadence

3–5 follow-ups roughly doubles reply rate vs. a single send (8.3% vs 4.1%); 60–70% of positive replies come from touches 1–3; past ~7 touches you're buying spam complaints, not replies ([Unify](https://www.unifygtm.com/explore/how-many-follow-ups-cold-email), [Modern Inbound](https://moderninbound.com/blog/cold-email-sequencing-how-many-touches-is-too-many)).

**But the notice deadline overrides generic cadence.** With a 10–20 day close window, the sequence must finish before the deadline — that's the point. Recommended: **3 touches, compressed**:

| Touch | Timing | Angle |
|---|---|---|
| Email 1 | Day 0 (notice has 10–16 days left) | Deadline + match + offer |
| Email 2 | Day 3–4 | New information (a specific insight from the notice), not "bumping this" |
| Email 3 | Deadline minus 4–5 days | Last-call, explicit cutoff (you need 2–3 days to draft), then stop |

Each follow-up must add something new. After touch 3: stop; recycle the firm into the next matching notice (a fresh notice = a fresh sequence, not a stale thread).

### Deliverability — new domain setup

Non-negotiable before email #1 (also protects the digest drip later):

1. **Dedicated sending domain** (per PLAN-V3), e.g. a variant of the main brand — never the main domain. One mailbox is plenty at 10–20/week.
2. **SPF + DKIM + DMARC before any send.** Start DMARC at `p=none` with reports, move to `p=quarantine` after 2–4 clean weeks. From-domain must align with DKIM/SPF domain ([Google/Yahoo requirements](https://powerdmarc.com/google-and-yahoo-email-authentication-requirements/), [MXScan checklist](https://mxscan.me/google-yahoo-email-requirements-2026)). Compliant senders average ~89% inbox placement; non-compliant see 22–34% routed to spam ([Redsift](https://redsift.com/guides/bulk-email-sender-requirements)).
3. **Warm-up: 3–4 weeks minimum** for a brand-new domain ([Mailivery guide](https://mailivery.io/blog/email-warmup-guide)). Week 1–2: no cold email at all — real correspondence only (sign up for newsletters, email people who reply, reply back). Ramp: ~5/day → 15/day → 30/day. At Mike's target volume he never exceeds warm-up-safe levels, which is a real advantage. Skip automated warm-up networks (bot pools) — Google actively detects them and the risk/benefit is bad at this volume. **This puts domain purchase in Week 1 on the critical path** — the plan's sequencing already reflects this.
4. **Volume discipline:** 10–20/week is far below the 5,000/day bulk-sender threshold, but keep spam complaints <0.3% and honor the one-click/reply opt-out anyway.

### CAN-SPAM (no B2B exemption)

Per the [FTC compliance guide](https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business), every email needs: accurate From/Reply-To identifying the real sender; a non-deceptive subject line; a valid **physical postal address** (a registered agent or virtual mailbox address is acceptable); a clear **opt-out** that costs nothing and requires nothing beyond a reply or one click, honored within **10 business days** and functional for 30+ days after send. Penalties run to ~$53K per violating email, so the footer lives in the template from email one (PLAN-V3 risk #3). A genuine 1:1 prospecting email arguably falls outside "commercial bulk," but comply anyway — the footer costs two lines.

---

## Part 1B — The three templates

Grounded in the real notice structure from `govconapi-exploration/raw/notice_detail_b719.json` (Aberdeen Proving Ground plumbing repair, Sources Sought, NAICS 236220, posted 08-21, closes 08-25). Merge fields in `{braces}` map 1:1 to govconapi fields; `{firm_*}` fields come from DSBS/USASpending enrichment. Filter matches to notices with **10–20 days left** so the 3-touch cadence fits.

**Footer (all three emails, required):**

```
—
Mike Ninov · [Company name], a service-disabled veteran-owned small business
[Physical mailing address]
Not interested in notes like this? Reply "no thanks" and I won't email again.
```

### Email 1 — deadline-tied opener (Day 0)

**Subject:** `{agency_short} {keyword} sources sought — closes {deadline_short}`
*Example: "Army plumbing sources sought — closes Sep 8"*

```
{first_name} — {agency_short} posted a Sources Sought that looks like
{firm_name}'s lane: {notice_title_short} ({solicitation_number}, NAICS
{naics}, closes {deadline_date}).

{one_line_match_reason — e.g. "Your {award_year} {agency} contract
{award_number} is exactly the past performance they're asking about."}

Responses to these shape the set-aside decision; firms that skip them
are invisible when the RFP drops.

I draft complete Sources Sought responses for SDVOSBs — every claim
cited to your actual award records — flat $450, 3 business days,
veteran-owned. You review everything before it goes in.

Want the notice link and a one-page outline?
```

~75 words merged. The `{one_line_match_reason}` is the personalization that earns the 5x — it must cite a real award (USASpending lookup), never a generic compliment. If no specific award matches, the firm doesn't get the email.

### Email 2 — follow-up with new information (Day 3–4)

**Subject:** reply in-thread (`Re:`) — threading beats a new subject for follow-up 1.

```
{first_name} — one detail from the {solicitation_number} notice worth
knowing: {specific_notice_insight — e.g. "it's currently marked Total
Small Business, and the responses they get decide whether it tightens
to SDVOSB" / "the draft PWS is attached to the notice, which usually
means the requirement is further along than most sources sought"}.

A response is 2–4 pages: capabilities matched to the requirement,
past performance, socioeconomic status. I handle the drafting and
citations; you review and submit. $450 flat.

Still time before {deadline_date} — want the outline?
```

~65 words. The insight comes from the notice detail (set-aside type, attachments, sole-source language, PoP) — the pipeline already pulls all of it.

### Email 3 — last call (deadline minus 4–5 days)

**Subject:** `{solicitation_number} — need to start by {start_by_date}`

```
{first_name} — last note on this. {notice_title_short} closes
{deadline_date}; to deliver a reviewed draft in time I'd need to start
by {start_by_date}.

If it's not a fit for {firm_name}, no reply needed — I won't follow up
again on this one. If another notice in {naics} matches you down the
line, would a heads-up be useful?

Either way: responding to sources sought notices is the cheapest
visibility in federal contracting, and most firms skip it.
```

~65 words. The explicit "I won't follow up again" is both a courtesy and a proven reply-driver; the secondary question converts dead deadlines into digest-list opt-ins (feeds PLAN-V3's drip channel).

---

## Part 1C — Workflow & tooling

### The pattern

```
TRIGGER   Daily poll: govconapi sources-sought, 5 target NAICS, due_after=today,
          10–20 days to deadline (remember: not `active_only`)
   ↓
ENRICH    DSBS → certified SDVOSBs matching NAICS + state; contact name/email
          USASpending → firm's actual awards for {one_line_match_reason}
          Exclusions check (already in pipeline)
   ↓
DRAFT     Template merge → Claude personalization pass → gates:
          (a) match_reason cites a real award ID  (b) ≤ ~90 words body
          (c) CAN-SPAM footer present  (d) anti-slop pass
   ↓
APPROVE   Drafts land in Mike's queue; he edits/kills/approves each one.
          Never auto-send. (Gmail is already connected here — Claude can
          write directly to Gmail drafts, Mike hits send from his phone.)
   ↓
SEND      Manual send from the warmed dedicated-domain mailbox
   ↓
TRACK     One CSV/sheet: firm, notice_id, touch#, sent_date, reply, outcome.
          Replies checked daily; "no thanks" → suppression list same day
          (10-business-day legal max, same-day actual). Suppression list is
          checked at the ENRICH step forever.
```

### Tooling verdict: skip the platforms, at least for now

| Option | Cost | Fit at 10–20/week |
|---|---|---|
| [Instantly](https://instantly.ai/blog/instantly-vs-smartlead-lemlist-2026/) Growth | $47/mo | Built for multi-inbox scale sending, warm-up networks, 1,000+ contacts. Wrong shape: its value is rotation and volume, which Mike doesn't need; its warm-up pools are a deliverability risk, not a benefit. |
| [Smartlead](https://sparkle.io/blog/smartlead-vs-instantly/) Base | $39/mo | Same story, $8 cheaper, better API. The API matters only if sending is automated — which the plan explicitly forbids (Mike approves every send). |
| **Google Workspace on the dedicated domain + Gmail drafts + CSV tracker** | **~$7/mo** | **Recommended.** Human-sent 1:1 mail from a normally-used mailbox is the best deliverability profile that exists. Pipeline writes drafts via the Gmail connector; Mike sends; replies tracked in the sheet. Zero new vendors. |

Reconsider Smartlead only if volume passes ~50/week sustained or the digest drip needs real list management — and the digest is better served by a proper newsletter tool (Buttondown/Loops, ~$0–30/mo) than a cold-email platform anyway.

---

## Part 2 — Claude skills shortlist

Already installed and sufficient: docx/pdf/xlsx, anti-slop, skill-creator, internal-comms, doc-coauthoring, research-before-build. Verdicts on what's out there:

| Item | What it is | Verdict |
|---|---|---|
| [coldoutboundskills](https://github.com/growthenginenowoslawski/coldoutboundskills) (GrowthEngineX, 564★, 28 skills) | Full cold-email stack: ICP, copywriting, deliverability, Smartlead/Prospeo/Zapmail automation | **Adapt 3, skip 25.** Worth stealing: `email-deliverability-audit` (SPF/DKIM/DMARC diagnostic), `spam-word-checker`, `positive-reply-scoring` (the right metric). Skip everything infrastructure/list-building — it assumes 20 domains + 40 inboxes + purchased leads; Mike's leads come from DSBS and he sends from one mailbox. |
| [louisblythe/Sales-Skills](https://github.com/louisblythe/Sales-Skills) (122 skills) | Generic sales frameworks + AI-SDR bot skills | **Skip.** Prose-only frameworks (no scripts/gates), aimed at autonomous SDR bots and generic B2B. The templates above already encode the applicable email craft. |
| [anthropics/skills](https://github.com/anthropics/skills) (official) | Document skills + examples | **Already have** the relevant ones (docx/pdf/xlsx). Watch the repo for new verification-type skills. |
| Fact-checker–style skills (various, per [awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills)) | Verify claims in documents via web search, propose corrections | **Skip installs; build native.** PLAN-V3 §6 already commits to native gates (compliance/provenance/format/freshness) with rubrics frozen from real deliverables. A generic fact-checker is weaker than a provenance gate that demands an award ID per claim. Use **skill-creator** (installed) to build the gate skills — that's the highest-leverage skill action available. |
| CRM skills (HubSpot/Pipedrive etc., via awesome lists) | CRM automation | **Skip.** At 10–20 emails/week a CSV + Gmail labels is the CRM. Revisit if the ladder produces repeat buyers worth pipeline-managing. |
| Web-research skills (Firecrawl etc.) | Scraping/crawling | **Skip.** All required data comes from structured APIs (govconapi/SAM/USASpending/DSBS). Scraping adds fragility, not coverage. |

**Net recommendation:** two custom skills, built with skill-creator, beat everything installable: (1) `ss-outreach-draft` — takes a notice_id + firm UEI, runs the enrich→merge→gate→Gmail-draft flow above; (2) `ss-response-gates` — the deliverable-side compliance/provenance gate contract from PLAN-V3. Fold the three adapted coldoutboundskills checklists into them rather than installing the repo.

---

## Sources

Cold email data: [Instantly 2026 benchmarks](https://instantly.ai/cold-email-benchmark-report-2026) · [Lavender benchmark report](https://lavender.ai/blog/the-cold-email-benchmark-report) · [Lavender on length](https://lavender.ai/blog/best-length-cold-email) · [30MPC data-backed formula](https://www.30mpc.com/newsletter/the-data-backed-cold-email-formula-the-exact-words-length) · [30MPC triggering emails](https://www.30mpc.com/newsletter/4-questions-to-write-painfully-triggering-cold-emails) · [Cleverly statistics](https://www.cleverly.co/blog/cold-email-statistics) · [Unify on follow-ups](https://www.unifygtm.com/explore/how-many-follow-ups-cold-email) · [Modern Inbound on touches](https://moderninbound.com/blog/cold-email-sequencing-how-many-touches-is-too-many). Deliverability: [PowerDMARC](https://powerdmarc.com/google-and-yahoo-email-authentication-requirements/) · [MXScan](https://mxscan.me/google-yahoo-email-requirements-2026) · [Redsift](https://redsift.com/guides/bulk-email-sender-requirements) · [Mailivery warm-up guide](https://mailivery.io/blog/email-warmup-guide). Legal: [FTC CAN-SPAM compliance guide](https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business). Tooling: [Instantly vs Smartlead](https://sparkle.io/blog/smartlead-vs-instantly/). Skills: [coldoutboundskills](https://github.com/growthenginenowoslawski/coldoutboundskills) · [Sales-Skills](https://github.com/louisblythe/Sales-Skills) · [ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills).
