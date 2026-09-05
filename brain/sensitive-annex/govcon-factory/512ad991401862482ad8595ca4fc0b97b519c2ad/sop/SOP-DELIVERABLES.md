# SOP-DELIVERABLES — agent procedure for producing capture deliverables

2026-08-22 draft, approved and revised 2026-08-22 (incorporates the ten cheap-win amendments from `report-enhancements/REPORT.md` §7 — MS-1..MS-6 and SS-1..SS-4). **Revised again 2026-08-22** (feasibility red-team, `research/feasibility-review/REPORT.md`, applied via `rubric-improve`): §1.3/§2.3/§2.4 G4 letterhead handling (PROPOSAL-0008, tag P8-1), §2.5/§3.5 register + inference-strength checklist items (PROPOSAL-0008, tag P8-2), §3.3 obligated-vs-ceiling label (PROPOSAL-0008, tag P8-3), §2.1/§2.6 notice-shape flag (PROPOSAL-0007, tag P7), §2.4 G3 degradation rule (PROPOSAL-0011, tag P11). This is the **canonical** copy; the original at `~/agent-reports/sdvosb-business/SOP-DELIVERABLES.md` is a pointer stub. Implements PLAN-V3 §6 (pipeline/gates) and §5 (review-time targets). Rubric sourced from `sample-response/RUBRIC-NOTES.md` (first real build, notice 36C77626Q0261); content standards sourced from the Part 1 research in §0 below. **Status: APPROVED — frozen. Further changes require a new dated revision, noted here and cross-linked from `rubric-improve`.**

An agent session with this file, the data-source credentials, and a notice_id must be able to produce a reviewable deliverable with zero re-derivation. If you find yourself researching "what should a sources sought response contain," stop — it's in §2.3. If a step is ambiguous, that's a defect in this SOP: flag it in the delivery note, don't improvise silently.

---

## 0. Content research basis (Part 1 findings — why the templates look the way they do)

### 0.1 What contracting officers use Sources Sought responses for

- A sources sought notice is a **FAR Part 10 market-research tool**, not a solicitation. The CO's output is a set-aside determination, not an award. Responses are the primary evidence for the **rule of two**: FAR 19.502-2 requires a small-business set-aside when the CO has a *reasonable expectation* that (1) offers will be received from **two or more responsible** small businesses and (2) award will be made at a **fair market price**. For VA, 38 U.S.C. §8127(d) (mandatory per *Kingdomware*, 2016) applies the same two-part test to SDVOSB/VOSB first — the Vets First priority. ([FAR 19.502-2](https://www.acquisition.gov/far/19.502-2); [Kingdomware coverage](https://smallgovcon.com/tag/38-usc-8127/); [rule-of-two cheat sheet](https://governmentcontractsnavigator.com/2021/07/29/rule-of-two-cheat-sheet/))
- **What makes a response "count" toward the two:** the responding firm must read as (a) *responsible and capable* — demonstrated same-or-similar completed work as **prime**, not aspiration; (b) *eligible* — certified in the relevant program (SBA VetCert for SDVOSB), small under the assigned NAICS, SAM-active, not excluded; (c) *likely to submit an offer* — an explicit statement of interest/intent to propose is what converts "capable firm exists" into "expect an offer"; (d) *plausibly priced* — evidence the firm performs at the notice's magnitude band supports the fair-market-price prong. A capability response that needs a teaming partner for core scope, cites only subcontractor roles, or is generic marketing does **not** reliably count. ([SamSearch sources sought guide](https://samsearch.co/blog/sources-sought); [SECNAV small business PDF](https://www.secnav.navy.mil/smallbusiness/Documents/SSN%20Why%20We%20Use%20Them_22Sept2020_FINAL.pdf); [Watson on SDVOSB market research](https://blog.theodorewatson.com/sdvosb-small-business-set-aside-government-market-research/))
- **CO-authored guidance** (Longo, Army ACC, ["The Notice I Never Knew"](https://asc.army.mil/web/news-the-notice-i-never-knew/)): responses are actually read and legally matter — GAO sustained protests where agencies ignored capability statements (*Career Systems Development*, B-416021.2) or executed sole-source J&As before reading responses (*Barnes Aerospace*, B-298864.2). But a sources sought is not a solicitation, so no evaluation letters issue and non-selection is not protestable (*AeroSage*, B-415893). Practical consequence: the response's only job is to make the CO's set-aside memo easy to write.
- **Common disqualifiers / discount triggers** (consistent across CO and practitioner sources): late submission; wrong format or ignored submission instructions; generic capability statement not mapped to the described scope; treating the response as a proposal (pricing, volumes); missing or lapsed certification; no contract numbers on past performance; past performance that violates a stated constraint (e.g. "completed within 10 years" — an ongoing project fails); missing a specifically requested item (e.g. bonding letter of intent for construction). ([USFCR](https://blogs.usfcr.com/sources-sought-response-strategy); [GovConToday](https://govcontoday.com/blog/how-to-respond-sources-sought))
- **Length norm:** obey any stated page limit; absent one, 2–5 pages. Concision is itself a credibility signal.

### 0.2 What capture/BD professionals put in a bid/no-bid brief (Market Snapshot basis)

Shipley-style capture practice structures the go/no-go around five factors, each evidence-backed: **customer relationship/incumbency**, **capability & past-performance fit**, **competitive position** (who else will bid), **price viability** (funding/magnitude vs. our cost position), **strategic fit**. pWin is re-estimated as intelligence improves. ([Shipley process guide](https://www.goveagle.com/blog/complete-shipley-process-guide); [pWin guide](https://www.goveagle.com/blog/what-is-pwin-probability-of-win-guide); [12-criteria scorecard](https://bidclarity.ai/resources/bid-no-bid-decision-framework.html))

Evidence base practitioners use: FPDS/USASpending award history for **pricing calibration** (obligated amounts on similar scope = the de facto price band) and **incumbent identification**; incumbents win ~70–75% of recompetes, so incumbency is the heaviest-weighted signal; contestability improves when the incumbent has outgrown its size status, lost certification, had performance gaps, or when the requirement is new (no incumbent). ([Fed-Spend competitive intelligence](https://fed-spend.com/blog/federal-contract-competitive-intelligence-guide); [recompete analysis](https://fed-spend.com/blog/what-does-recompete-mean-government-contracting); [USFCR award tracking](https://blogs.usfcr.com/competitive-intelligence-federal-contracting))

### 0.3 Cross-check vs. SAMPLE-RESPONSE.md — gaps both directions

Sample already meets or exceeds the researched standard on: per-requirement compliance matrix, cert dates + eligibility window, contract-numbered past performance with relevance narrative, self-performed effort, DUNS-retirement handling, concision, provenance citations (which no public guidance even asks for — that's the wedge).

**Gaps in the sample the template below fixes:**

1. **No explicit intent-to-submit-an-offer statement.** The rule of two counts *expected offers*, not capable firms. One sentence, now mandatory in the template (§2.3, section "Interest & Intent").
2. **No explicit magnitude-band/price-plausibility line.** Fair-market-price is the second prong; the template adds one sentence tying the firm's completed-project value range to the notice's magnitude (evidence already in the data pull).
3. **No set-aside recommendation sentence.** Practitioner standard is to explicitly state the certification category and (where true) awareness that the rule of two can be met. The sample gestures at this in Section 2; the template makes it a fixed closing element.

**Things the sample does that public guidance omits (keep — do not "simplify" toward the generic standard):** provenance cites on every claim, the internal compliance matrix, `[CLIENT PROVIDES]` intake markers, sample-ethics double banner, aggregate-count verification.

---

## 1. Shared infrastructure (both deliverables)

### 1.1 Data sources & exact access patterns

| # | Source | Access | Used for | Key fields |
|---|--------|--------|----------|-----------|
| S1 | **govconapi** (Pro, key in `credentials/govconapi.env`; free tier = 25 req/day — budget calls) | `GET /opportunities/search` with `notice_type=Sources Sought`, `naics_multiple=`, `due_after=<today>`, `due_before=`, `has_attachments=true` in **one** call | Notice discovery + detail | `notice_id`, `title`, `notice_type`, `agency`, `naics`, `psc`, `posted_date`, `response_deadline`, `sam_url`, `description_text`, `contact_name`, `contact_email`, `contact_phone` |
| S2 | govconapi attachments | attachments endpoint per `notice_id`; URLs are direct SAM links, no auth | Full requirement text (SOW/synopsis) | attachment URL list → download → text-extract |
| S3 | **USASpending** (free, keyless, full FPDS history 2007+) | `POST /api/v2/search/spending_by_award/` filtered by recipient UEI, or by `naics_code` + awarding sub-agency + PoP state | Past performance, competitor awards, pricing history | `Award ID`, `Recipient Name`, `Award Amount`, `Total Outlays`, `Description`, `Start Date`, `End Date`, `Awarding Agency`, `Awarding Sub Agency`, `Place of Performance State Code`, `naics_code`, `Contract Award Type`, `generated_internal_id` (→ permalink `usaspending.gov/award/<generated_internal_id>`, e.g. `CONT_AWD_36E77619C0074_3600_-NONE-_-NONE-`) |
| S4 | **SBA Small Business Search (SBS/DSBS)** — undocumented, scrape-tier, verify quarterly | `POST /_api/v2/search`; payload = the zustand `filters` object from localStorage key `filters-store-v1.67`; SDVOSB filter value `"9,10"`; response = full hit array, **no pagination** | Certified-firm universe, cert entrance/exit dates, bonding, contacts, capabilities narrative | UEI, CAGE, contact name/email/phone, bonding per-contract/aggregate, cert dates, capabilities text |
| S5 | **SAM.gov APIs** (free api.data.gov key) | Get Opportunities API; Exclusions API by UEI; daily CSV (keyless) as fallback | Exclusions screening; govconapi fallback; historical solicitation walk-back | exclusion records keyed on UEI |
| S6 | **USASpending award detail / transactions** (free, keyless) | `GET /api/v2/awards/<generated_internal_id>/` + `/api/v2/transactions/` by award | Competition fields, modification history, burn rate, parent IDV | `extent_competed`, `number_of_offers_received`, `type_of_set_aside`, transaction list (mod #, date, amount, description), `total_outlays` vs obligated, parent award id/name |
| S7 | **GAO bid-protest search** (public; scrape-tier, no API) | gao.gov/legal/bid-protests/search by protester name / agency / solicitation number | Protest screen on incumbents, competitors, and the requirement's lineage | B-number, parties, date, disposition, decision link. **Caveat in every use: most dismissals and withdrawals are never published — findings are a lower bound** |
| S8 | **SAM.gov Responsibility/Qualification (formerly FAPIIS)** (public with signed-in SAM account) | SAM.gov entity record → Responsibility/Qualification section | Integrity screen: terminations for default/cause, non-responsibility determinations, defective pricing, admin agreements | record type, date, agency |
| S9 | **Agency procurement forecasts** (public planning data) | VA: vetbiz.va.gov/forecast; other agencies via acquisition.gov/procurement-forecasts directory | Pre-RFP corroboration: forecast line for the requirement/program | est. value band, target FY/quarter, anticipated set-aside. **Always caveated: planning data, not a commitment** |

Known traps (all hit or verified in prior sessions): `active_only` on govconapi includes passed deadlines — always filter `due_after=today`. SAM sometimes deletes superseded attachment files — an error JSON can come back under a `.pdf` filename; check magic bytes/content before parsing. True deadlines can move inside Q&A attachments without the notice field updating — parse attachments for date strings near "response"/"due". USASpending pages at 100 rows — see gate G2's pagination rule. FPDS ATOM feed is retired; never use it.

Full endpoint shapes, payloads, and gotchas for S1–S9 are in `recipes/` — see `recipes/govconapi.md`, `recipes/sam-gov.md`, `recipes/usaspending.md`, `recipes/sbs-search.md`, `recipes/protest-integrity-forecast.md`.

### 1.2 Citation format (the provenance contract)

Every factual claim in a deliverable carries an inline cite that a reviewer can resolve in one click or one file-open:

- **Award facts:** contract number + `usaspending.gov/award/<generated_internal_id>` — e.g. `36E77619C0074 · usaspending.gov/award/CONT_AWD_36E77619C0074_3600_-NONE-_-NONE-`.
- **Certification/entity facts:** `(Source: SBA Small Business Search certification record, retrieved YYYY-MM-DD)`.
- **Notice facts:** SAM notice number + govconapi `notice_id` — e.g. `SAM.gov notice 9f1681711a8d43fcb448645068de35a9` for 36C77626Q0261.
- **Exclusions:** `no UEI-keyed SAM exclusion for <UEI> (YYYY-MM-DD); name-level principal screening pending` (name-level screening is a human step).
- **Protest records:** GAO B-number + decision/docket URL — e.g. `B-416021.2 · gao.gov/products/b-416021.2`.
- **R/Q (FAPIIS) records:** `(Source: SAM.gov Responsibility/Qualification record for <UEI>, retrieved YYYY-MM-DD)`; empty screens follow the exclusions-line pattern.
- **Forecast entries:** `(«Agency» Forecast of Contracting Opportunities, entry «id/title», retrieved YYYY-MM-DD — planning data)`.
- **Dollar figures:** truncate (floor) to whole dollars so the document figure is a verbatim prefix of the source value (BATCH-NOTES rule, adopted — half-up rounding caused 10 false gate-fails in the first batch).

Every number that appears in prose must exist verbatim in a file under the deliverable's `data/` directory. If it isn't in `data/`, it doesn't go in the document.

### 1.3 Client-input markers and sample-ethics rules

- Anything the factory cannot source from public data is written as **`[CLIENT PROVIDES: <specific item>]`** — never guessed, never left as a silent blank. The canonical list from the first build: surety letter of intent, COR reference names/phones, self-performed $ split, street address, A/E partner selection. *(P8-1, added 2026-08-22, PROPOSAL-0008):* **logo/letterhead** — a capability response conventionally ships on the firm's letterhead; request it at intake as `[CLIENT PROVIDES: logo/letterhead]`, with a plain-header fallback (firm name, address, UEI/CAGE in a clean text block — no generic clip-art) when the client has none, confirmed in the delivery note either way. The set of markers in a finished deliverable **is** the client intake form for that order.
- **Demo artifacts about real firms** (uninvited use of a firm's public record): double `⚠ SAMPLE / DEMONSTRATION DOCUMENT` banner (top and bottom), "not reviewed or authorized" line, public-data-only sourcing, and if shown publicly, consider anonymizing ("a Connecticut SDVOSB, UEI on file"). Never submit; never imply endorsement.
- **Paid deliverables:** no banner; client supplies the `[CLIENT PROVIDES]` items via intake before drafting completes.

### 1.4 Working directory layout per deliverable

```
<order-dir>/
  DELIVERABLE.md          # the document (converted to PDF at ship time for responses)
  data/                   # every API pull, verbatim JSON — the provenance ground truth
  notice-raw/             # notice JSON + downloaded attachments + extracted text
  GATE-REPORT.md          # output of §2.4/§3.4 gates, pass/fail per gate with evidence
  DELIVERY-NOTE.md        # review checklist state + open flags for Mike
```

---

## 2. Deliverable: Sources Sought Response ($450 · review target 10–15 min)

### 2.1 Inputs

Required to start: `notice_id` (govconapi) and client firm UEI. Everything else is derived.

*Upstream candidate scoring (RUBRIC-NOTES mech #5 — used when selecting which notice to build against, e.g. for demos or outreach targeting):* filter S1 results to 10–25 days out + `has_attachments=true`, then rank by `description_text` length, presence of enumerated requirement sections (regex `Section \d`), and VA/set-aside leverage (`agency` contains "VETERANS" or set-aside language in description). Mostly mechanical; final pick is a human glance.

1. **Notice detail** (S1) → all notice fields above; persist as `notice-raw/notice.json`.
2. **Notice attachments** (S2) → download all; extract text; persist raw + `notice-raw/attachment_text.txt`. The attachment usually contains the enumerated requirement sections (as in 36C77626Q0261: Sections 1–4 + cover page + submission rules).
3. **Firm profile** (S4) → UEI, CAGE, cert type + entrance/exit dates, bonding capacity, contacts, capabilities narrative → `data/firm_sbs.json`.
4. **Firm award history** (S3, by UEI) → **all pages** → `data/awards_p1.json`, `data/awards_p2.json`, … until `has_next=false` or a page returns fewer than `limit` rows.
5. **Exclusions** (S5 or govconapi) by UEI → `data/exclusions.json`.
6. **Client intake** (paid orders): the `[CLIENT PROVIDES]` list from §1.3, plus confirmation of POC and intent to bid.
7. **Notice-shape classification** *(P7, added 2026-08-22, PROPOSAL-0007):* `notice-triage` tags the notice evidence-shaped / questionnaire-shaped / mixed (`skills/notice-triage/SKILL.md` step 4). Carry the tag into `DELIVERY-NOTE.md` — a questionnaire-shaped notice is a scope-honesty flag for the founder review (§2.6), not a hard stop; no pricing-tier policy exists yet for this classification (open question, tracked outside this SOP revision).

### 2.2 Pipeline (in order; do not reorder)

1. **Eligibility pre-check** (gate G3 logic, run first — kills the order before drafting): cert active; cert exit date beyond anticipated award window (parse "planned for advertising <months>" from notice text; default window = response deadline + 12 months if unstated); SAM active; exclusions empty; small under the notice's NAICS size standard. Any hard fail → stop, report, do not draft.
2. **Requirement extraction:** parse notice + attachment text into an enumerated requirement list. Sources: explicit `Section N:` blocks; cover-page sentence ("include a cover page, which includes, at a minimum: …"); submission-rule sentences (format, deadline, POC(s), page limit, "no phone calls"). Output: `notice-raw/requirements.json` — one row per requirement with quoted source text.
3. **Evidence selection:** from the full award history, select ≤ the notice's project cap (default 3) satisfying **all stated constraints** (completed-within-N-years means `End Date` in window AND project actually closed — an ongoing period of performance fails even if relevance is high); prefer scope-shape similarity > dollar size, geography match, and incumbency at the requiring activity (see §2.5 judgment item 1 — the agent proposes, the human decides).
4. **Draft** per the template in §2.3. Local model for extraction/structuring; frontier model for final prose (PLAN-V3 §6).
5. **Self-run all gates** (§2.4) → `GATE-REPORT.md`. Fix and re-run until all mechanical gates pass.
6. **Write `DELIVERY-NOTE.md`:** the §2.6 checklist pre-filled with pointers (award rows, judgment items flagged, `[CLIENT PROVIDES]` count), plus any SOP-ambiguity flags.
7. **Hand to Mike.** Never ship, send, or publish without human approval.

### 2.3 Content template

Mirror the notice's own structure — the document's section order is the notice's requirement order, so the CO can check compliance by reading top to bottom. Fixed elements regardless of notice structure:

| Element | Must contain | Source |
|---|---|---|
| **Header block** | Notice number, title, project number, NAICS, magnitude band; CO/CS names + emails; response deadline with timezone; submission format line. *(P8-1)* Rendered on the client's letterhead/logo per §1.3 intake, or the plain-header fallback when none was provided — never generic/unbranded when a letterhead exists | notice fields |
| **Cover page** | Every identifier the notice's cover-page sentence lists: name, address, UEI, CAGE, DUNS-line ("DUNS retired April 2022; UEI is successor" — never blank, never fake), socio-economic status with certifying body, POC name/phone/email | S4 + intake |
| **Company identification** | Established year, HQ, geographic footprint, SAM status w/ cite; **contract-vehicle holdings relevant to the anticipated acquisition route** (FSS/MAC/IDIQ contract numbers from the firm's award history parent-IDV fields; confirm via intake — `[CLIENT PROVIDES: vehicle list confirmation]`) *(SS-2)* | S4 (+ S3 parent-IDV fields) |
| **Size & certifications** | Small under NAICS + size standard; cert type, entrance date, **current-through date**; explicit tie to the set-aside statute in play (VA: 38 U.S.C. §8127 Vets First) | S4 |
| **Bonding** (construction notices) | Published per-contract/aggregate capacity vs. the notice's minimum, with comparison spelled out; `[CLIENT PROVIDES: surety letter of intent]` | S4 + intake |
| **Past performance** | Per project: contract number, contract type, prime/sub role, delivery method, value, period, customer, USASpending verification link, and a relevance paragraph mapping the project's scope to the notice's scope **element by element**. Respect project caps and completed-within rules. Aggregate context line (e.g. "186 federal awards, 180 VA") only with pagination-exhausted counts | S3 |
| **Self-performed effort** (when asked) | Trades self-performed with direct-hire crews; `[CLIENT PROVIDES: $ and %]`; subcontracted specialty trades honestly attributed | S4 narrative + intake |
| **Answers to specific questions** | Every enumerated question restated and answered individually | notice text |
| **Interest & Intent** *(gap fix #1–3, extended by SS-1)* | Fixed sentences, adapted: (1) intent — "«Firm» intends to submit a proposal in response to the anticipated solicitation." (2) price plausibility — "«Firm»'s completed projects of this type range $«lo»–$«hi», within the stated magnitude of construction." (3) set-aside support — "This response is offered to support a[n] «SDVOSB» set-aside determination under «authority»." (4) **activity precedent, when N>0** *(SS-1)* — "«Activity» has awarded «N» SDVOSB set-aside actions under NAICS «code» in the last three fiscal years, including «contract» ($«amt», «permalink»)." Omit when N=0. (5) **OPTIONAL, founder-gated per order** *(SS-4)* — rule-of-two awareness: "Public certification and award records indicate at least two certified SDVOSBs, including «Firm», have completed same-or-similar work for «agency»." Ships only when the founder approves it in the delivery-note review (§2.5 item 6) — default omit | S3-derived + firm cert |
| **Compliance matrix** (internal QC page, marked "not part of submission") | Every `requirements.json` row → section pointer | pipeline step 2 |
| **Provenance footer** | Data sources with retrieval dates, UEI, exclusions-screen line, (samples: second banner) | §1.2 |

**Drafting rule — hot-button vocabulary** *(SS-3)*: where truthful, capability narratives reuse the notice/SOW's own priority terminology verbatim (program names, standards, constraint phrases). G1 soft check: the five most frequent distinctive noun-phrases in the SOW each appear in the response or are flagged N/A in the compliance matrix.

Length: obey stated page limit; absent one, 2–5 pages excluding the internal matrix. No pricing, no proposal volumes, no key-personnel résumés unless the notice asks.

### 2.4 Mechanical gates (fail closed; every failure lists the offending string + file)

- **G1 Compliance.** Every row in `requirements.json` has a section pointer in the document; every enumerated notice question has a restated answer. Unmapped requirement → FAIL. (RUBRIC-NOTES mech #1.)
- **G2 Provenance.** Regex sweep of the document for `\$[\d,.]+`, dates, contract/award IDs, UEIs, and bare counts ("N awards", "N projects", "N years"): each match must equal a value present in `data/` or `notice-raw/`. **Pagination rule (RUBRIC-NOTES judgment #6, now mechanical):** any COUNT-type claim additionally requires proof of exhaustion — last page's `has_next=false` or row-count < page limit — recorded in the gate report. A count matching a truncated file is a FAIL, not a pass. (First build's "100 awards" error — true figure 186 — is the canonical catch.)
- **G3 Eligibility.** Booleans, all must pass: cert active now; cert exit date > anticipated award window end (e.g. exit 2027-04-28 vs. advertising Sep–Oct 2026 → pass); SAM registration Active; zero UEI-keyed exclusions; small under NAICS size standard. Also: intent-to-bid sentence present (G3b) — without it the response may not count toward the rule of two. **G3c** *(SS-1)*: activity-precedent sentence present when the Snapshot-style set-aside pull shows N>0 for this activity+NAICS (data must be in `data/`); absent otherwise. **G3d — SBS degradation rule** *(P11, added 2026-08-22, PROPOSAL-0011):* if the S4 (SBS/DSBS) API is down, this gate does not silently pass or silently fail-soft — it may accept **manual-fallback evidence** in its place (per `recipes/sbs-search.md`'s documented fallback: cert status from the public SBS website UI, screenshot persisted to `data/`, plus SAM entity API for registration status), provided the fallback evidence is present and a flag is recorded in `DELIVERY-NOTE.md` noting the API was down and manual evidence was substituted. Absent that documented substitution, a missing S4 API file is a hard FAIL per rule 2 (fail closed) — this is a narrow, written exception, not a general license to skip the check.
- **G4 Format.** Submission format honored (PDF-only when stated); all notice POC emails present in header (dual-POC notices → both); deadline restated with timezone and still in the future at gate time; page limit respected **when stated** — the gate must handle both cases (36C77626Q0261 had none; the Tacoma RFI in the same candidate set capped at 5 pages); every `[CLIENT PROVIDES]` enumerated in the delivery note; sample banners present iff demo artifact. **(P8-1, added 2026-08-22, PROPOSAL-0008):** letterhead present per §2.3, or the plain-header fallback explicitly confirmed in the delivery note — an unbranded document when the client supplied a letterhead is a FAIL.
- **G5 Freshness.** Every `retrieved:` date within 5 days of delivery; notice re-fetched at gate time (deadline unchanged, notice not superseded); attachments re-verified (content-type check — SAM deletes superseded files); attachment text re-scanned for deadline-moving Q&A language.

### 2.5 Human judgment (never automate; from RUBRIC-NOTES)

1. **Client–notice match / evidence selection** — scope-shape over dollar size, geography, incumbency signals. Agent proposes a ranked shortlist with reasons; human picks. (This is the product's IP.)
2. **Honest-relevance line** — "one-to-one analogue" claims vs. overreach (CT-scanner-room ≈ MRI site prep is defensible; claiming RF-shielding self-perform is not). Human reads every relevance paragraph.
3. **Notice-rule edge cases** — retired-DUNS-style anachronisms, project-cap interpretations (e.g. follow-on award folded into Project 2's narrative to respect a 3-project cap). Agent flags each with its reasoning; human ratifies.
4. **Sample-ethics call** — whether a demo about a real firm is appropriate for the intended audience.
5. **Anything the gates flagged but couldn't decide.**
6. **Rule-of-two awareness sentence** *(SS-4, Interest & Intent #5)* — include or omit per order; default omit.
7. **Register check** *(P8-2, added 2026-08-22, PROPOSAL-0008)* — would any sentence read as marketing rather than market-research evidence to a CO? (E.g. "the incumbent-experienced choice for exactly this scope" — a real drift caught in the 236220 sample, `research/feasibility-review/REPORT.md` F6-W3.) Downgrade superlatives to evidence statements. This is exactly the failure mode an LLM drafting pipeline produces systematically at scale, not a one-off — read every sentence, not just the relevance paragraphs already covered by item 2.

### 2.6 Human review checklist (target 10–15 min; stopwatch every review — PLAN-V3 §5)

Pre-condition: `GATE-REPORT.md` all-green. If any gate is red, bounce back to the agent — do not review around a failed gate.

1. ☐ Open GATE-REPORT — confirm all-green, skim the G2 evidence lines for the 3 largest dollar figures. *(~2 min)*
2. ☐ Project selection: agree with the ≤3 chosen projects vs. the ranked shortlist? Any ongoing project slipped in as "completed"? *(~3 min)*
3. ☐ Read the relevance paragraphs only — any claim you wouldn't defend on a call with the CO? Includes the register check (§2.5 item 7) — any sentence reading as marketing rather than evidence? *(~3–4 min, P8-2)*
4. ☐ Edge-case flags in DELIVERY-NOTE — ratify or fix each. *(~2 min)*
5. ☐ `[CLIENT PROVIDES]` list complete and matches intake? Interest & Intent section present and true for this client? *(~1 min)*
6. ☐ Skim header + cover page against the notice PDF once. *(~2 min)*
7. ☐ Log stopwatch time in the delivery note.

**Premium for responses:** none recommended. The response is priced on compliance + evidence discipline; intelligence upsells belong in the Snapshot/capture rungs. **Skip:** competitor ghosting inside a sources sought response (inappropriate in a market-research reply and would read as marketing — a §0.1 discount trigger).

---

## 3. Deliverable: Market Snapshot ($750 · review target 20–33 min)

### 3.1 Inputs

Required to start: `notice_id` (or a named target requirement) and the client firm UEI (the snapshot is *for* someone — competitive position is relative).

1. **Notice detail + attachments** (S1/S2) as §2.1 → `notice-raw/`.
2. **Comparable-award pull** (S3): `spending_by_award` filtered `naics_code` = notice NAICS + `Awarding Sub Agency` = notice's contracting activity + PoP state(s) of the requirement, last 5 FY. All pages. → `data/comparable_awards_p*.json`. (Pattern proven in `data/va_sdvosb_236220_ne_awards.json`.)
3. **Requiring-activity award pull** (S3): same filter narrowed to the facility/station if identifiable from the notice (e.g. Station 523) → incumbent evidence.
4. **Certified competitor field** (S4): SBS search, SDVOSB filter `"9,10"`, notice NAICS + relevant state(s) → `data/competitor_firms.json`; join to S3 by UEI for each firm's relevant-award count.
5. **Client firm history** (S3 by UEI, all pages) for the positioning section.
6. **Award-detail enrichment** *(MS-2)* (S6): for every incumbent-candidate award and the top-N comparable awards, fetch award detail + transactions → `data/award_detail_<piid>.json`, `data/transactions_<piid>.json`.
7. **Protest screen** *(MS-3)* (S7): search GAO by (a) incumbent + top-3 competitor firm names, (b) the predecessor solicitation number if identified → `data/gao_protests.json` (empty result = record the search terms + date).
8. **Integrity screen** *(MS-4)* (S8): R/Q section for incumbent + named competitors → `data/rq_screen.json`.
9. **Forecast cross-ref** *(MS-5)* (S9): agency forecast queried for the requirement/program keywords + NAICS → `data/forecast_check.json` (hit or bounded miss).

### 3.2 Pipeline

1. Pull inputs 1–9; persist everything to `data/`.
2. Compute the mechanical aggregates: comparable-award count, median/quartile `Award Amount`, award-type mix, top recipients by award count and dollars, count of certified SDVOSBs in NAICS+geo, subset with ≥1 relevant award.
3. Identify incumbent candidates: recipients with active or recent awards at the requiring activity whose `Description` overlaps the notice scope. **Incumbency assertion requires an award-row cite; "no incumbent identified" is the honest default**, stated with the search bounds used.
4. Draft per §3.3 template.
5. Run gates (§3.4) → `GATE-REPORT.md`.
6. Delivery note with §3.6 checklist pre-filled; the bid/no-bid recommendation is drafted **as a proposal for Mike's judgment**, clearly labeled.

### 3.3 Content template

| Section | Must contain | Source |
|---|---|---|
| **1. Opportunity summary** | Notice facts table: number, title, agency + contracting activity, NAICS + size standard, PSC, set-aside status *as posted*, magnitude/est. value, posted date, response deadline, anticipated advertising window, attachment inventory | notice fields |
| **2. Set-aside posture & rule-of-two math** | Current set-aside marking; the governing authority (VA → 38 U.S.C. §8127 Vets First; else FAR 19.502-2); count of certified SDVOSBs in NAICS+geo and how many have relevant completed awards — i.e., whether the CO can plausibly find two; what that means for how the requirement will likely be competed. **Competition-history roll-up** *(MS-1)*: from the comparable pull, % competed vs. sole-source, median `number_of_offers_received`, % single-offer awards, set-aside-type mix (S6). State what the activity's own competition behavior implies for how this buy will be run | S4 + S3 join (+ S6) |
| **3. Competitive field** | Table, one row per plausible bidder: firm, UEI, city/state, cert status + expiry, relevant-award count, largest relevant award ($ + contract number + permalink). Ranked by demonstrated relevance. Client firm's row highlighted in place — that *is* the positioning statement | S4 + S3 |
| **4. Incumbent analysis** | Named incumbent(s) with award cites, contract end dates, and whether this is a recompete or new requirement; if recompete: incumbent's current size/cert status (small→large or cert lapse = contestability); base rate context (incumbents win ~70–75% of recompetes) with the §0.2 sourcing. **Incumbent health block** *(MS-2)* per named incumbent award: modification count and classification (option-exercise / scope-growth / descope / corrective / bridge, from transaction descriptions), burn rate (`total_outlays` ÷ obligated, with both figures), and a one-line health verdict (healthy / mixed / vulnerable) tied to the classified mods. **Protest-screen result** *(MS-3)* and **R/Q-screen result** *(MS-4)* with links or bounded-empty lines. A termination for default/cause found in R/Q is always surfaced in the section lede | S3 requiring-activity pull (+ S6, S7, S8) |
| **5. Pricing history** | Comparable completed awards: count, median, quartiles, min–max; the notice's magnitude band vs. that distribution; 3–5 named exemplar awards with numbers + permalinks. No price recommendation — calibration only. **Award-type/vehicle detail** *(MS-6)*: parent IDVs carrying the comparable dollars, share of dollars through each, and whether the client holds access (client history parent-award join + `[CLIENT PROVIDES]` confirmation). Flag vehicle-gated markets explicitly. *(P8-3, added 2026-08-22, PROPOSAL-0008)* Label every dollar-figure table/column explicitly as **obligated amount** — a sophisticated reader distinguishes ceiling vs. obligated vs. outlaid, and the current tables don't say which figure they show | S3 comparable pull (+ S6) |
| **6. Contestability signals** | Checklist with evidence per item: new vs. recompete; incumbent weakness signals — **mod-history classification + burn rate + protest screen + R/Q screen (S6–S8)** — cite the specific rows; "none found" requires the §3.4 G3 bounds statement; requirement maturity (attachments/draft SOW present = further along); this activity's set-aside track record in the NAICS; timeline pressure; any Q&A/amendment activity | notice + S3, S6–S8 |
| **7. Bid/no-bid scorecard** | The five capture factors (§0.2): incumbency/customer relationship, capability & PP fit, competitive position, price viability, strategic fit. Each scored ▲/●/▼ with a one-line evidence cite. **Recommendation drafted, labeled "PROPOSED — founder judgment required"** | all above |
| **8. Recommended actions** | Dated next steps keyed to the notice deadline (respond-by date, intake items needed, follow-on solicitation monitoring). **Forecast line** *(MS-5)*: if the requirement or successor appears in the agency forecast, list it with target quarter as a follow-on watch item; if absent, note the absence and its implication (unplanned/urgent buy) | notice (+ S9) |
| **Provenance footer** | As §1.2 | — |

### 3.4 Mechanical gates

- **G1 Compliance (snapshot variant).** All 8 sections present; every scorecard factor has an evidence cite; recommendation carries the "PROPOSED" label.
- **G2 Provenance.** As §2.4 G2, including the pagination-exhaustion rule — snapshot aggregates (medians, counts, "N certified firms") are exactly the claims the rule exists for. Every named competitor row must carry a UEI resolvable in `data/competitor_firms.json`; every exemplar award a permalink. *(MS-1..MS-6)* Mod classifications must trace to transaction descriptions in `data/transactions_*.json`; burn-rate ratios must recompute from the two cited figures. Forecast values cite the forecast entry (S9) with retrieval date.
- **G3 Scope honesty.** Incumbency claims have award-row cites; absence claims ("no incumbent identified") state search bounds (filters + FY range + retrieval date). Base-rate claims (70–75%) cite §0.2 sources, not invented precision. Protest and R/Q "none found" claims state search terms, screens run, and retrieval date, plus the unpublished-dismissals caveat for GAO results. Health verdicts (healthy/mixed/vulnerable) must be supported by ≥2 classified data points or downgraded to "insufficient signal." **CPARS is never cited, implied, or estimated — competitor performance claims rest only on S6–S8 evidence.**
- **G4 Format.** Tables render; client row highlighted; no pricing *recommendation* language (calibration only — pricing advice is out of scope and drifts toward consulting liability).
- **G5 Freshness.** As §2.4 G5; additionally re-check the notice's set-aside marking at gate time — it can change during the response window and Section 2 hinges on it. Forecast and R/Q retrievals within 14 days of delivery (slower-moving sources; notice-tied sources keep the 5-day rule).

### 3.5 Human judgment

1. **The bid/no-bid recommendation itself.** The scorecard is mechanical; the call is not. Founder-only.
2. **Competitor-relevance ranking** — same scope-shape problem as §2.5(1); reading award descriptions is the method.
3. **Incumbent inference** — an award at the same facility is a signal, not proof; human decides how hard to state it.
4. **Strategic-fit scoring** — depends on client context the pipeline doesn't have.
5. **Inference-strength check** *(P8-2, added 2026-08-22, PROPOSAL-0008)* — does every capability/incumbency read match the strength of its evidence? (The 541512-snapshot catch: §2's rule-of-two math counted any DHA-541512 SDVOSB as plausibly capable, then §3 conceded none has dental-PACS work — §2's read should be hedged to match §3's honesty, not the other way around, `research/feasibility-review/REPORT.md` F6-W3.) Same failure mode as the response product's register check (§2.5 item 7): an LLM drafting pipeline produces inference-strength drift systematically, not as a one-off.

### 3.6 Human review checklist (target 22–33 min)

1. ☐ GATE-REPORT all-green; spot-check G2 on the median and the firm count. *(~3 min)*
2. ☐ Read competitive-field table: ranking sane? anyone obviously missing/misranked? *(~5 min)*
3. ☐ Incumbent section: is the strength of claim proportional to the evidence? Sanity-check the mod-history/burn-rate health verdict. *(~4–7 min)*
4. ☐ Scorecard: adjust scores; write/approve the recommendation. *(~7 min)*
5. ☐ Skim pricing section for accidental recommendation language. *(~2 min)*
6. ☐ Log stopwatch time.

**Premium tier:** MS-7 (teaming/subaward map), MS-8 (hot buttons/win themes/ghost themes), MS-9 (weighted pWin score), MS-10 (CALC+ labor-rate calibration), and MS-11 ("who buys this here" CO names) are real premium-tier material — a "Capture Brief" rung between Snapshot and red-team, est. $1,500–2,500, 45–60 min founder review. Not part of this SOP; see `report-enhancements/REPORT.md` §5 (PLAN-V4 candidate) and flag to `rubric-improve` when the ladder is ready for a third rung.

---

## 4. Operating rules for any agent session using this SOP

1. **Never ship without human approval.** All deliverables land in Mike's queue with GATE-REPORT + DELIVERY-NOTE.
2. **Fail closed.** A gate that can't run (API down, file missing) is a FAIL, not a skip.
3. **No claim without a file.** If a fact isn't in `data/` or `notice-raw/`, it doesn't appear in the deliverable — including "background knowledge" about agencies or firms.
4. **Budget API calls.** The efficient candidate-pull is one govconapi search with `due_after` + `due_before` + `has_attachments`; USASpending is free and keyless — push volume there.
5. **Log review time** on every deliverable — it's the month-one metric that decides pricing (PLAN-V3 §5).
6. **When this SOP is ambiguous,** note the ambiguity in DELIVERY-NOTE and choose the conservative reading (fewer claims, more `[CLIENT PROVIDES]`, lower-confidence language). SOP fixes ship as dated revisions after Mike approves — see `skills/rubric-improve/SKILL.md`.

## 5. Sources (Part 1 research)

Official/CO-authored: [FAR 19.502-2](https://www.acquisition.gov/far/19.502-2) · [eCFR 48 CFR 19.502-2](https://www.ecfr.gov/current/title-48/chapter-1/subchapter-D/part-19/subpart-19.5/section-19.502-2) · [Longo, "The Notice I Never Knew" (Army ACC)](https://asc.army.mil/web/news-the-notice-i-never-knew/) · [SECNAV Small Business: Sources Sought — Why We Use Them (PDF)](https://www.secnav.navy.mil/smallbusiness/Documents/SSN%20Why%20We%20Use%20Them_22Sept2020_FINAL.pdf) · [SBA set-aside guidance for contracting officials](https://sba.gov/partners/contracting-officials/small-business-procurement/set-aside-procurement) · [VAAR 808.405-70](https://www.acquisition.gov/vaar/808.405-70-set-aside-procedures-va-and-gsa-federal-supply-schedules.). Rule of two / VA: [SmallGovCon on 38 U.S.C. 8127](https://smallgovcon.com/tag/38-usc-8127/) · [Rule of Two cheat sheet](https://governmentcontractsnavigator.com/2021/07/29/rule-of-two-cheat-sheet/) · [Crowell on rule-of-two market research sustains](https://www.governmentcontractslegalforum.com/2024/09/articles/government-contracts/et-two-gaorecent-sustain-on-the-rule-of-two-reminds-agencies-of-the-importance-of-accurate-market-research/) · [Watson: SDVOSB set-asides & market research](https://blog.theodorewatson.com/sdvosb-small-business-set-aside-government-market-research/). Practitioner (responses): [SamSearch sources sought guide](https://samsearch.co/blog/sources-sought) · [USFCR response strategy](https://blogs.usfcr.com/sources-sought-response-strategy) · [GovConToday guide](https://govcontoday.com/blog/how-to-respond-sources-sought). Capture/bid-no-bid: [GovEagle Shipley process guide](https://www.goveagle.com/blog/complete-shipley-process-guide) · [GovEagle pWin guide](https://www.goveagle.com/blog/what-is-pwin-probability-of-win-guide) · [BidClarity 12-criteria scorecard](https://bidclarity.ai/resources/bid-no-bid-decision-framework.html) · [Fed-Spend competitive-intelligence guide](https://fed-spend.com/blog/federal-contract-competitive-intelligence-guide) · [Fed-Spend recompete analysis](https://fed-spend.com/blog/what-does-recompete-mean-government-contracting) · [USFCR competitive intelligence](https://blogs.usfcr.com/competitive-intelligence-federal-contracting).

Cheap-win enhancement sourcing (2026-08-22 revision): [Deltek — AI & UX in GovWin IQ](https://www.deltek.com/resources/articles/govwin-ai-ux-innovation/) · [Fed-Spend — pWin Verdict Engine](https://fed-spend.com/blog/pwin-verdict-engine-win-probability-guide-2026) · [FAR 42.1503](https://www.acquisition.gov/far/42.1503) (CPARS non-public, FOIA-exempt) · [FAR 9.104-6](https://www.acquisition.gov/far/9.104-6) · [GAO protest search](https://www.gao.gov/legal/bid-protests/search) · [FPDS — Extent Competed](https://www.fpds.gov/help/Extent_Competed.htm) · [GAO-10-833 — single-offer competition](https://www.gao.gov/assets/a308886.html) · [VA VetBiz forecast](https://www.vetbiz.va.gov/forecast/) · [acquisition.gov — procurement forecasts](https://www.acquisition.gov/procurement-forecasts). Full list: `report-enhancements/REPORT.md` §8 (source copy retained at `~/agent-reports/sdvosb-business/report-enhancements/REPORT.md`).

Internal: `PLAN-V3.md` §§5–6 · `sample-response/RUBRIC-NOTES.md` (all seven judgment items + three mechanical-gate sources incorporated above) · `sample-response/SAMPLE-RESPONSE.md` (canonical example: citations, matrix, markers) · `sample-set/BATCH-NOTES.md` (five-order batch run; dollar-truncation and DSBS-ingester findings incorporated above) · `report-enhancements/REPORT.md` (source of this revision's ten cheap-win amendments, §7) · `govconapi-exploration/REPORT.md` (API surfaces, traps, budgets) — these source documents remain at `~/agent-reports/sdvosb-business/`.
