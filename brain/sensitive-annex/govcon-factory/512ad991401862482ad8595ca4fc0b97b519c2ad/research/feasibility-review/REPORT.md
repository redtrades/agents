# Feasibility review — outside red-team of the whole business before launch

2026-08-22. Mandate: skeptical outside reviewer; find what's wrong or missing, not summarize what's there. Scope reviewed: PLAN-V4 (+V3 by incorporation), SOP-DELIVERABLES, financial model v3 (SUMMARY + assumptions posture), the five-order sample set, growth-plan REPORT, content-pipeline spec, stack-selection REPORT, outreach templates, prior-art and NAICS-selection reports. External evidence gathered by web research this date; every external claim links. Material findings are filed as `proposals/PROPOSAL-0001..0010.md` for the feedback loop.

---

## VERDICT: **GO-WITH-CHANGES**

The core thesis survives red-teaming: the buyer moment is real (rule-of-two mechanics are correctly understood and better-sourced than most competitors' marketing), the sample deliverables are genuinely above the public standard, unit economics at $450/10–15-min-review are sound, fixed burn is a rounding error, and — decisively — the 30-day kill-gates already control the one assumption (reply→paid) that everything hinges on. Nothing found here says "don't run the kill-test."

What does **not** survive unmodified:

1. **The market is sized by the wrong denominator.** The business is notice-tied, so the binding constraint is *viable notices per year* (~250–400 sellable notice-moments/yr in the 6 target NAICS by this review's derivation, not the 4,000–8,000-firm universe the plan cites — a number that appears nowhere derived and contradicts two other universe figures in this same repo). Base-case Y1–Y2 fits inside the real ceiling; the Optimistic scenario does not without NAICS widening *and* selling multiple clients per notice.
2. **Selling to multiple clients on the same notice is an unaddressed conflict of interest** — and it is also the only way the Optimistic math closes. This needs a written policy before the first two orders on one notice arrive, not after.
3. **AI drafting of sources sought responses is already commoditized** (Sweetspot ships a dedicated RFI-response workflow; Rogue drafts sources sought responses; SamSearch Pro ~$99/mo includes proposal generation). The wedge as stated ("the only offer that is a finished document under $500") is behind the market by roughly a year. The wedge that actually survives is *verification + accountability + service delivery*, and the kill-test must be run against the AI SaaS tools, not only HigherGov/VetBiz search output.
4. A short list of **launch blockers that cost days, not weeks**: client services agreement/liability terms, E&O insurance, a conflict policy, a founder-absence protocol, and an honest triage rule for questionnaire-shaped notices where the $450 deliverable is mostly `[CLIENT PROVIDES]`.

Proceed to the 30-day validation exactly as planned, with the changes below. If the kill-gates pass, the changes marked P1 must be done before scaling past validation volume.

---

## Findings, ranked by severity

Severity: **S1** = threatens viability or creates unbounded downside; **S2** = materially changes the plan's numbers or sequencing; **S3** = fix-when-touched.

---

### F1 · S1 — Market sizing uses the wrong denominator, and the repo carries three inconsistent universe numbers

**The claim under review** (PLAN-V3 §3): "~4,000–8,000 serviceable certified firms; 99 open Sources Sought in the 5 target NAICS… supports 10–20 precise emails/week indefinitely."

**What the repo's own data says.** `research/naics-selection/REPORT.md` (same date) measured: 36,265 SDVOSB-certified firms total; ~38.5K firm-code slots across the 6-code set (~27.4K across 5, overlap not deduped); ~120–126 open Sources Sought across the 6 codes; **~820 Sources Sought/yr of flow** (trailing-12 SAM CSV). Meanwhile `research/stack-selection/REPORT.md` §9 says "the entire addressable pipeline is ~1,500 firms." So the repo simultaneously carries **~1,500, 4,000–8,000, and ~27–38K** as the universe, none with a derivation. The financial model's saturation analysis (SUMMARY.md) keys off 4,000–8,000 — a number that appears to be inherited from PLAN-V2-era reasoning, not from the S4 data the pipeline can now pull.

**The deeper problem: firms are the wrong denominator anyway.** The product is notice-tied — an order exists only when (a) a viable Sources Sought notice is open, (b) in a target NAICS, (c) a certified firm plausibly matches it, (d) the notice isn't disqualified on content. A better estimate from the repo's own evidence:

- Flow: **~820 SS/yr** in the 6 target NAICS (naics-selection, SAM daily CSV, trailing 12 mo). Government-wide ~1,052 open at a point in time; at a ~30-day average window that implies ~12–13K/yr government-wide — so the 6-code set is ~6–7% of federal SS flow.
- Viability haircut: BATCH-NOTES documents that content disqualifiers **dominate** (sole-source intents, MAC/vehicle-restricted, product-catalog RFIs, anticipated 8(a)); the batch read ~20 notices per NAICS to find 1 viable in-window demo candidate, and in 2 of 5 NAICS there were zero viable in-window candidates that week. A generous attachability estimate is **30–50%** of raw flow → **~250–400 sellable notice-moments/yr** across the 6 codes.
- Revenue ceiling, response product, one client per notice: 250–400 × $450 = **$112K–$180K/yr** at 100% capture — which no one gets. At a strong 10–20% capture of viable moments: **$11K–36K/yr** from responses alone in the current NAICS set. The ladder (Snapshot $750 attaches to any named requirement, not just SS; red-team; Core) and NAICS widening are therefore not upside — they are **required** for the Base case, and the plan should say so explicitly.
- Cross-check against the model: Base Y2 outbound $83.5K ≈ ~150 deliverables/yr — feasible only with Snapshot-heavy mix or NAICS widening. Optimistic Y2 outbound **$465K ≈ ~850 deliverables/yr exceeds the entire viable-notice supply of the 6-code set** even at 100% capture, unless multiple clients are sold per notice (see F2). SUMMARY.md's saturation caveat gestures at this via firm-count; the notice-count version is tighter and bites earlier.

**Response-behavior evidence (asked for, honestly thin).** No systematic public dataset counts SS responses. Point evidence from GAO protest records: agencies receiving [two responses](https://smallgovcon.com/gaobidprotests/gao-small-business-rule-of-two-must-be-based-on-accurate-market-research/), [four small + one large](https://blog.theodorewatson.com/gao-bid-protest-tips-for-challenging-set-aside-decisions/) — single digits is the observable norm. The "most firms skip them" claim used in outreach copy traces to vendors selling response services/tools ([USFCR](https://blogs.usfcr.com/sources-sought-response-strategy), [SamSearch](https://samsearch.co/guides/sources-sought)) — directionally credible, motivated sources. Two implications: (a) low response counts genuinely support the rule-of-two pitch; (b) as free AI drafting spreads (F3), response counts per notice will rise and the marginal value of *another* response falls. The kill-test measures willingness-to-pay now; re-measure yearly.

**Change required (P1):** derive the serviceable universe from S4 data (dedup firms across the 6 codes, count firms with ≥1 relevant federal award — the actually-matchable subset), publish the derivation, and restate the model's saturation math on *viable notices* as the second axis. → `PROPOSAL-0001`.

---

### F2 · S1 — No conflict-of-interest policy for multiple clients on one notice

Nothing in SOP-DELIVERABLES, PLAN-V3/V4, or the outreach playbook addresses the obvious situation: two SDVOSBs matched to the same notice both say yes. The factory would then be drafting *competing* capability responses from the same data, with the same "we make the CO's rule-of-two memo easy" pitch — while each client believes the response is their edge. Worse: the Snapshot names competitors; a client could buy a Snapshot on a notice where another client is in the competitive-field table, drafted by the same shop.

This is simultaneously (a) the plan's only path to the Optimistic revenue numbers (F1 arithmetic), (b) a reputational landmine in a community that is small, veteran-tight, and talks (r/GovernmentContracting alone is [41K+ members](https://www.weekendmvp.app/ideas/government-contract-finder)), and (c) a genuine service-quality question — a response's job is to make *this firm* count toward the two; two identically-structured responses from one factory arguably help the set-aside but dilute each client's differentiation.

Options with different revenue consequences: exclusive-per-notice (first paid order locks the notice; cleanest, lowest ceiling), capped-with-disclosure (max N clients/notice, all told "we may serve other respondents on this notice; your data is firewalled"), or laissez-faire (undisclosed; indefensible when discovered). Interaction with the rule of two is real: serving 2–3 responses on one notice *increases* the set-aside odds for everyone — there's an honest version of the disclosure that is actually a selling point. But it must be chosen and written down **before** the first collision, because the first collision is also the first time the outreach engine works well. → `PROPOSAL-0002`.

---

### F3 · S1 — The drafting wedge is already commoditized; the kill-test is aimed at last year's competitors

PLAN-V3 §4's standing kill-test compares against **HigherGov Standard and VetBiz** — search products. The sharper 2026 comparison is AI drafting:

- **Sweetspot** ships a dedicated workflow page — ["How to Respond to Federal RFIs and Sources Sought Notices Using AI"](https://www.sweetspot.so/govcon-workflows/responding-federal-rfis/) — generating a draft response "in under ten minutes" by mapping the org library to each RFI question.
- **Rogue** "drafts responses to Sources Sought, RFIs, and RFPs" ([GovDash's own market survey](https://www.govdash.com/blog/best-ai-capture-management-platforms-federal-contractors)).
- **SamSearch** Pro (~[$99/mo](https://www.saasworthy.com/product/samsearch-co/pricing), now demo-gated per [their pricing page](https://samsearch.co/pricing)) includes an AI proposal generator/editor, and their [sources sought guide](https://samsearch.co/guides/sources-sought) is a top SERP result — they own the educational funnel for this exact query.
- Fiverr sells capability statements at [$5](https://www.fiverr.com/emily_w888/write-a-winning-government-contract-proposal-rfp-response-capability-statement)–[$105](https://www.fiverr.com/chandoneaddis/create-a-professional-capability-statement) and bundles "RFP response" gigs at the same tier.
- Notably, **no competitor was found selling per-response Sources Sought drafting as a fixed-price productized service** — consultancies fold it into retainers (ProposalHelper's fixed-price model is undisclosed; [Winvale](https://winvale.com/govt-contract-consulting/consulting-services/proposal-support/), [Hudson](https://hudson-bidwriters.com/sources-sought/) quote per engagement), Upwork freelancers sell it hourly. The niche is open — but read both ways: the absence of a $450 productized competitor is *also* weak evidence that nobody has made the price point work at volume.

Consequences:

1. **The wedge sentence must change.** "The only offer that is a finished document + under $500" is false the moment a prospect has a SamSearch trial. The surviving wedge is: *finished and verified* (provenance gates — genuinely absent from every tool surveyed, confirmed independently by the prior-art scan: "Nobody ships gated, provenance-cited deliverables"), *accountable* (a human you can call, veteran-owned), and *zero-effort* (the SaaS tools all require the customer to drive). The buyer who can't or won't drive a tool is the durable segment — which is exactly PLAN-V3's no-BD-staff segment, so the strategy holds but the copy and kill-test don't.
2. **Kill-test scope must add one leg:** same notice, run through SamSearch/Sweetspot free trial, side-by-side against the factory deliverable. If Mike can't articulate the visible difference in 30 seconds to a non-expert, the wedge copy isn't ready.
3. **Replication speed if it works:** HigherGov (data superset, engineering team) could ship "generate a response" per notice within a quarter; SamSearch already has the SERP and the generator. What they will not replicate quickly is per-claim provenance with fail-closed gates + human review + service SLA — it's operationally expensive and off-model for SaaS. Defensibility is the *service wrapper*, DSBS contact enrichment (fragile, see F9), and the veteran identity. Price is not defensible; expect anchor erosion toward "$99/mo unlimited."
4. **AI-response flooding is a demand-side risk**: agencies are already adding [AI-disclosure language and quality scrutiny](https://www.goveagle.com/blog/can-government-detect-ai); if COs start receiving 30 templated AI responses per notice, the *paid, verified, specific* response gains relative value — but the outreach line "firms that skip them are invisible" weakens as fewer firms skip. Watch response-count drift via outcome-track.

→ `PROPOSAL-0003` (wedge + kill-test), `PROPOSAL-0004` (objection handling in outreach).

---

### F4 · S2 — Growth plan misses the channels where this buyer demonstrably already is

The growth plan is right that paid ads are wrong and right about LinkedIn + newsletter + SEO. But its channel scan omitted the largest observable attention pools for small/new government contractors:

- **YouTube**: GovCon Giants — [53K+ YouTube subscribers, 250K+ podcast listens, 24K LinkedIn](https://govcongiants.libsyn.com/) — is the #1 education channel for exactly the newly-certified, no-BD-staff segment. Neil McDonnell (already cited in the plan) runs daily LinkedIn Lives. The plan cites McDonnell but never asks *where else the same audience aggregates*: it's YouTube and podcasts.
- **Podcast guesting**: GovCon Giants, FedBiz'5 ([which has a whole episode on "should I respond to a sources sought"](https://fedbizaccess.com/fedbiz5-podcast-episode-42-should-my-small-business-respond-to-a-sources-sought-or-rfi/)), The How of Business, etc. A service-disabled-veteran founder with live data ("we watched 820 sources sought this year; here's how many got <3 responses") is a bookable guest. One guest slot ≈ months of cornerstone SEO at current volumes, at zero cash cost and ~2 hrs founder time.
- **Reddit**: [r/GovernmentContracting, 41K+ members](https://www.weekendmvp.app/ideas/govcon-contract-finder) trading SAM.gov war stories; r/smallbusiness threads on whether GovCon consultants are worth it. Answer-don't-pitch presence is free and reaches buyers mid-question.
- **Facebook groups**: "U.S. Government Contracting Made Easy" (9,200+ members) and peers — skew exactly toward the non-BD-staffed owner the plan targets.
- **Webinars/speaking at APEX/SBA/OSDBU events**: the plan uses APEX only for counselor referrals; counselors also *book speakers* for free training sessions. A data-driven "what happens to sources sought in your NAICS" session is neutral enough for a counselor to host.

None of this changes the funnel architecture (everything still lands on digest → mini-snapshot → paid); it changes the awareness layer's expected yield and reduces the plan's dependence on 6–12-month SEO compounding. Founder-time cost is the constraint — YouTube-as-channel (producing) is expensive, but *guesting* and community presence are cheap. → `PROPOSAL-0005`.

---

### F5 · S2 — Outreach ramp contradicts the stack it runs on, and the reply benchmark is far above cold-email base rates

- **Stack contradiction**: stack-selection §1 (written for the 10–20/wk world, "customer ceiling ~45–58") picked *manual Gmail on the primary Google Workspace domain*, GMass only past ~40–50/wk. PLAN-V4 §4 ramps to **100–200/wk**. Nobody reconciled these. 200 cold emails/wk through the primary business domain risks the domain's deliverability (the same domain that sends deliverables, invoices, and the digest); Google's bulk-sender spam-complaint thresholds (0.3%) are easy to trip on scraped-contact cold outreach. The "second sending domain warmed" line in V4 is the right instinct but has no owner, no task, and no tooling decision behind it.
- **Reply-rate benchmark**: the model's Base assumes 15%→8% reply across the ramp, labeled "benchmark, not ours" for *signal-triggered* cold email. Typical cold B2B reply rates are low single digits; 15–25% is the top decile of hyper-personalized sends. The notice-match personalization genuinely is strong, and DSBS emails are owner-direct (good), but they are also registration-record addresses of unknown freshness (bounce risk unmeasured). The model dilutes rates with volume but starts from an optimistic anchor; a Base that starts at 5–8% and dilutes to 3–4% would cut outbound revenue roughly in half. The kill-gates will produce the real number within 60 days — the model should carry a pessimistic-reply sensitivity row now so nobody is surprised by what "passing" the kill-test at a 4% reply rate implies.
- **CAN-SPAM/DSBS use**: PLAN-V3 §9 flags SAM data-use questions *for the feed* but not for outreach itself. Marketing to SBS/DSBS-listed contacts is common industry practice, but the same DUA/counsel question being asked for the feed should explicitly cover outreach use of scraped SBS contact data. Cheap to ask at the same time. → `PROPOSAL-0006`.

---

### F6 · S2 — Sample critique: strong compliance discipline, but three content weaknesses the SOP doesn't catch

Reviewed as a skeptical CO / BD professional: `236220-response`, `561210-response`, `541512-snapshot`.

**What genuinely lands** (credit where due): notice-mirrored structure, per-requirement compliance matrix, contract-numbered past performance with element-by-element relevance mapping, intent/price-plausibility/set-aside closing block, verbatim-provenance citations. This beats every public template surveyed ([GovCon Giants](https://govcongiants.com/guides/sources-sought), [USFCR](https://blogs.usfcr.com/sources-sought-response-strategy), the [GSA pre-award guide](https://www.gsa.gov/system/files/Pre-Award%20Notices%20-%20508%20-%2008272021.pdf)) and most consultant work product. A CO could write the set-aside memo from the 236220 sample directly.

**Weakness 1 — the `[CLIENT PROVIDES]` density problem (worst in 561210).** The WV BPA sample contains ~15 `[CLIENT PROVIDES]` markers, and they cover most of what the notice actually asks: serviceable locations, licensing evidence, pricing-approach feedback, BPA participation confirmation, all four subcontracting answers, Industry Day RSVP. What the factory contributed is the header, the eligibility screen, and the past-performance table — real value, but on this notice-shape the client writes the substance and pays $450 for scaffolding. A BD pro would notice; a repeat buyer would resent it. The SOP has no triage rule distinguishing *evidence-shaped* notices (where the USASpending record IS the response — 236220 is the showcase) from *questionnaire-shaped* notices (where it isn't). Fix: a pre-sale classification in notice-triage with either a price tier or a scope-honest pitch ("we do the evidence sections; you answer the operational questions — here's the intake"). → `PROPOSAL-0007`.

**Weakness 2 — no branding/visual identity path.** A capability response conventionally goes out on the firm's letterhead with its logo and marks — it's a marketing document to a future customer. The SOP's output is markdown→PDF with no letterhead handling, no `[CLIENT PROVIDES: logo/letterhead]` in the canonical intake list, and no format-gate check for it. Generic-looking output is a §0.1 discount trigger ("generic capability statement") in visual form, and it's the first thing a client's own reviewer will notice. Small fix, belongs in §2.3 and G4. → `PROPOSAL-0008`.

**Weakness 3 — tone and inference edges a CO would discount.** (a) 236220: "JRCS is the incumbent-experienced choice for exactly this scope" — marketing register in a market-research reply; the SOP's own §0.1 warns against reading as marketing. (b) 541512-snapshot §2: rule-of-two math counts SDVOSBs with *any* DHA 541512 award as plausibly capable, then §3 admits none has dental-PACS work — the §2 read should be hedged to match §3's honesty. (c) The snapshot's largest-award figures are obligation amounts on vehicle task orders; a sophisticated reader distinguishes ceiling vs. obligated vs. outlaid — one clarifying word in the table header. All are review-checklist items, not gate failures — which is the point: the human-judgment checklist (§2.5/§3.5) currently doesn't name *tone/register drift* as a check item, and it's exactly the failure mode an LLM drafting pipeline will produce at scale. → folded into `PROPOSAL-0008`.

Also worth recording: the 541512 snapshot was built against a notice due 5 days out — real orders on that timeline collide with the 3-business-day outreach SLA and Mike's review batching. No SLA/turnaround policy exists anywhere (see F10).

---

### F7 · S2 — Financial model: arithmetic verified, assumptions not; three labels overstate

The 2,688-cell independent recomputation is real rigor — about *formula integrity*. It says nothing about assumption plausibility, and three specific labels overstate:

1. **"Measured/validated: prices"** (SUMMARY honest-assumptions ledger). Prices are *set*, not validated — zero units have sold. The whole ledger's credibility rests on label discipline; this one breaks it.
2. **Core subscription revenue is modeled ($29.5K Base Y2, 18% of revenue) for a product that is defined nowhere.** No scope, no price, no deliverable cadence exists in any document. Modeling revenue for an unspecified product is a placeholder wearing a number.
3. **Digest growth (40–100 subs/mo Base from a standing start)** carries 24% of Y2 Base revenue through the inbound funnel. McDonnell's 25K took years of daily content with a huge following; Buttondown-from-zero at 40–100/mo sustained for 24 months is a top-quartile outcome being used as Base. The 90-day measure-and-replace commitment is the right control — but the model should also carry an inbound-fails-entirely row, since v2's conservative case predates the inbound funnel and no current sheet shows "outbound-only" v3 economics.

Missing cost lines: E&O insurance (~[$700–1,500/yr](https://www.insureon.com/small-business-insurance/errors-omissions/cost) for a small professional-services firm), one-time legal review of client terms (~$1–3K), chargeback/refund reserve, second-domain + sending-tool cost at ramp (F5). Individually trivial; collectively they're the difference between "fixed burn ~$17/mo" as stated and the real ~$150–250/mo steady state. → `PROPOSAL-0009`.

---

### F8 · S2 — Advice-adjacent liability with no legal wrapper

The Snapshot ships a **bid/no-bid recommendation** ("PROPOSED — founder judgment required" labels it internally, but the client receives a recommendation). A client who no-bids on the Snapshot's advice and watches a competitor win — or bids and loses expensively — is a plausible complainant. Today there is: no client services agreement, no limitation-of-liability clause, no disclaimer that deliverables are research products not professional advice, no E&O policy, no refund policy. Stack-selection §7 contemplates "order-form terms PDF… worth a one-time review by a lawyer" — that's the hook, but nothing tasks it and nothing in the SOP requires terms-acceptance before order intake. PLAN-V3 §9.2 covers practice-of-law framing for red-team/protest products but is silent on the Snapshot's recommendation and the response product. This is a P1 blocker: cheap (a few hundred dollars of insurance + one lawyer session), unbounded if skipped. → `PROPOSAL-0010`.

---

### F9 · S2 — The moat is a single undocumented scrape endpoint with no fallback

The DSBS/SBS ingester is called "the fragile differentiator" (PLAN-V3 §6) and the prior-art scan confirmed "the absence is the moat" — zero open-source SBS scrapers exist. Red-team reading: the moat is **one undocumented POST endpoint** (`/_api/v2/search`, payload reverse-engineered from a JS bundle, states-filter already broken, "verify quarterly") that SBA can alter, auth-gate, or captcha at any moment, silently. Because no open-source community uses it, there is also no early-warning network — breakage is discovered when the pipeline fails. Everything downstream depends on it: firm universe, cert dates, *contact emails* (the outreach engine's fuel), per-NAICS small flags (a G3 gate input — and gates fail closed, so an SBS outage stops all production).

Mitigations, none currently planned: (a) periodic full-universe snapshots per target NAICS (the response is unpaginated — one POST per code) archived in the repo's SQLite store, so an outage degrades freshness rather than existence; (b) a documented manual fallback (the public SBS website UI + SAM entity API covers cert-status-at-order-time for single firms); (c) a monitoring canary that runs the payload daily and alarms on schema drift *before* an order needs it. Cheap, and turns a cliff into a slope. Also note govconapi free tier is 25 req/day with a single-copy key — §9.5 covers the key, nothing covers govconapi silently changing response shapes; the SAM fallback recipe exists, good. → `PROPOSAL-0011`.

---

### F10 · S3 — Key-man risk is total, and the plan's own autonomy design makes it explicit

By design (correctly, for trust), **every send and every ship requires Mike**. Therefore any founder interruption — illness, VA appointments, a two-week emergency — halts 100% of revenue motion and breaks the 3-business-day SLA already promised in `templates/outreach/email-1-opener.md`. There is no absence protocol: what happens to in-flight orders, who tells the client, whether the SLA has a stated exception. Delegated review (V4 §3) eventually softens this but starts M3–4 at the earliest and covers review, not send/ship authority. Cheap fixes now: an SLA with an honest buffer ("3 business days, or notified upfront"), a canned delay-notice template, a documented pause procedure (stop outreach sends first, they create future obligations), and credentials escrow (already partially handled via password manager per §9.5). → folded into `PROPOSAL-0010`.

Payment friction, for completeness, is **largely solved** — stack-selection §6's Stripe-Invoicing-with-ACH-default matches GovCon AP culture (Net-30, invoice-and-ACH) and this review found no gap beyond: state a prepay-vs-Net-30 policy per product (a $450 first-time order should be prepaid; Net-30 is for repeat/Core), and a refund/kill-fee policy for orders cancelled after data-pull but before draft.

---

### F11 · S3 — Smaller items

- **Content-pipeline spec** is the best-engineered document in the repo (frozen snapshots, per-page fail-closed, noindex-until-2-green-builds, PG2 already caught a real case). Two nits: (a) A1 pages promise 48h freshness on a *daily ingest that doesn't exist yet* (TASK-0005) — the spec correctly sequences this but the cornerstone pages (TASK-0009, "start now") cite A1 live-data callouts, creating a hidden dependency on daily ingest earlier than the trigger table implies. (b) No analytics decision exists anywhere (measuring the §7 funnel targets requires *some* analytics on Pages + Buttondown + Stripe — pick the tool before launch or the 90-day measure-and-replace commitment is unmeasurable).
- **Local-model routing** (V4 §5): eval validated extraction/structuring/tool-calling, and customer-facing prose stays frontier — sound. Risk accepted knowingly; no change.
- **Governance**: the proposals/board/gates system is unusually good discipline for a solo shop. One honest observation: it is also a lot of process surface for zero revenue — the repo currently contains more governance than customers. The kill-gate discipline (§0) is the correct antidote; hold to it.
- **AI-disclosure trend** ([GovEagle, May 2026](https://www.goveagle.com/blog/can-government-detect-ai)): agencies adding AI-disclosure/human-review language to solicitations. Low risk for market-research responses today; add a standing line to outcome-track to watch for SS notices that request AI disclosure, and be ready to answer honestly (human-reviewed, provenance-verified) — it's a wedge *advantage* if it arrives.

---

## What would change the verdict

**To NO-GO:** kill-gates fail as defined (0/10 twice); or the SamSearch/Sweetspot side-by-side shows no articulable difference; or counsel says SBS-contact outreach violates data-use terms.

**To unqualified GO:** kill-gates pass, conflict policy + legal wrapper shipped, universe re-derived with the model's saturation restated on viable notices, and the wedge copy rewritten against the 2026 competitor set.

---

## Proposal index (filed this review)

| ID | Title | Target | Severity |
|---|---|---|---|
| PROPOSAL-0001 | Derive the serviceable universe from S4 data; restate saturation on viable notices | `sop/PLAN-V3.md` §3 / financial model | S1 |
| PROPOSAL-0002 | Adopt a conflict-of-interest policy for multiple clients per notice | `sop/SOP-DELIVERABLES.md` / order-intake | S1 |
| PROPOSAL-0003 | Rewedge against AI-drafting SaaS; expand the kill-test | `sop/PLAN-V3.md` §4 / TASK-0002 | S1 |
| PROPOSAL-0004 | Add "why not $99/mo AI SaaS" objection handling to outreach | `templates/outreach/` | S2 |
| PROPOSAL-0005 | Add YouTube/podcast-guesting/Reddit/FB-groups/webinars to growth channels | `research/growth-plan/REPORT.md` | S2 |
| PROPOSAL-0006 | Reconcile outreach ramp with sending infrastructure; extend DUA question to outreach | `sop/PLAN-V4.md` §4 / stack | S2 |
| PROPOSAL-0007 | Notice-shape triage: evidence-shaped vs questionnaire-shaped; scope-honest pricing | `skills/notice-triage/` + SOP §2 | S2 |
| PROPOSAL-0008 | Letterhead/branding path + tone-register review item | SOP §2.3/§2.5/G4 | S2 |
| PROPOSAL-0009 | Fix model labels (prices not validated; define Core before modeling it); add missing cost lines + outbound-only sensitivity | `sop/financial-model/` | S2 |
| PROPOSAL-0010 | Launch legal/ops pack: client terms, liability cap, E&O, refund/SLA/absence policy | new `ops/` + order-intake | S1 |
| PROPOSAL-0011 | DSBS fallback: universe snapshots, canary, manual degradation path | `recipes/sbs-search.md` | S2 |

---

## External sources

Market/response behavior: [SmallGovCon — rule-of-two market research](https://smallgovcon.com/gaobidprotests/gao-small-business-rule-of-two-must-be-based-on-accurate-market-research/) · [Watson — set-aside protest tips](https://blog.theodorewatson.com/gao-bid-protest-tips-for-challenging-set-aside-decisions/) · [Crowell — rule-of-two sustain](https://www.crowell.com/en/insights/client-alerts/et-two-gao-recent-sustain-on-the-rule-of-two-reminds-agencies-of-the-importance-of-accurate-market-research) · [USFCR response strategy](https://blogs.usfcr.com/sources-sought-response-strategy) · [SamSearch SS guide](https://samsearch.co/guides/sources-sought) · [GSA pre-award notices guide](https://www.gsa.gov/system/files/Pre-Award%20Notices%20-%20508%20-%2008272021.pdf).
Competitors: [Sweetspot RFI workflow](https://www.sweetspot.so/govcon-workflows/responding-federal-rfis/) · [GovDash AI capture platforms survey](https://www.govdash.com/blog/best-ai-capture-management-platforms-federal-contractors) · [SamSearch pricing](https://samsearch.co/pricing) · [SaaSworthy SamSearch pricing](https://www.saasworthy.com/product/samsearch-co/pricing) · [GovEagle AI-detection](https://www.goveagle.com/blog/can-government-detect-ai) · Fiverr gigs ([$105](https://www.fiverr.com/chandoneaddis/create-a-professional-capability-statement), [$5](https://www.fiverr.com/emily_w888/write-a-winning-government-contract-proposal-rfp-response-capability-statement)) · [Winvale proposal support](https://winvale.com/govt-contract-consulting/consulting-services/proposal-support/) · [Hudson Bid Writers](https://hudson-bidwriters.com/sources-sought/) · [Upwork proposal writers](https://www.upwork.com/hire/proposal-writers/).
Channels: [GovCon Giants podcast/YouTube stats](https://govcongiants.libsyn.com/) · [FedBiz'5 ep. 42](https://fedbizaccess.com/fedbiz5-podcast-episode-42-should-my-small-business-respond-to-a-sources-sought-or-rfi/) · [community sizes (r/GovernmentContracting 41K+, FB groups 9K+)](https://www.weekendmvp.app/ideas/government-contract-finder).
Ops: [Insureon E&O cost](https://www.insureon.com/small-business-insurance/errors-omissions/cost) · [MoneyGeek E&O cost 2026](https://www.moneygeek.com/insurance/business/e-o-cost/).
