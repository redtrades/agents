# Proposed diff: `research/proposal-writing/PROPOSAL-RUBRIC.md`

Status: **proposal only. Not applied.** `PROPOSAL-RUBRIC.md` is unmodified.
Evidence: `REPORT.md` in this directory.
Route: per `AGENTS.md` rule 5, rubric edits go through `skills/rubric-improve/`, not a direct
rewrite. This file is the input to that, not a substitute for it.

Caveat carried forward from the report: **n=1**. One award, one agency, one NAICS, one dollar
band. Every change below is proposed because a real winner contradicted or bypassed a row built
from secondary research. That is a reason to add a scope condition to the row, not usually a
reason to delete it. Where deletion is proposed, it is said plainly.

---

## Summary of proposed changes

| # | Change | Type | Rubric location |
|---|---|---|---|
| 1 | Scope the whole rubric to UCF; add a non-UCF construction track | **Structural** | new §0.0, and §0.1 |
| 2 | Split the compliance matrix into internal artifact vs submitted content | Correction | §0.1 |
| 3 | Add a Forms and Instruments section, including bonding | **New section** | new §4A |
| 4 | Add an Out-of-Band Obligations section | **New section** | new §7 |
| 5 | Re-scope "unaddressed requirement equals not awardable" | Correction | §1 disqualifiers |
| 6 | Add "relevance by selection" alongside relevance by narrative | Addition | §3 |
| 7 | Mark the adjectival and confidence scales as agency-conditional | Correction | §1, §3 |
| 8 | Add scope conditions to the pricing volume rows | Correction | §4 |
| 9 | Add exceptions, exclusions and assumptions | Addition | §1 |
| 10 | Scale review depth to pursuit size and response window | Correction | §0.6 |
| 11 | Generalize the VetCert row to any asserted set-aside basis | Correction | §0.4 |
| 12 | Add a page-allowance-underuse note | Addition | §1 disqualifiers |

---

## 1. Scope the rubric, and add a non-UCF track

**Why.** The rubric's spine is Section L and Section M. FAR Part 36 construction solicitations
use SF1442 and have neither. The observed solicitation carried its instructions and evaluation
criteria as unlabeled free text inside a 57-page PDF. NAICS 236220 is on our own target list, so
this is not an exotic case.

**Proposed, as a new §0.0 inserted before the existing cross-cutting rules:**

```diff
+## 0.0 Scope and solicitation format
+
+This rubric was written from research on **Uniform Contract Format** solicitations
+(FAR 15.204-1), which carry lettered Section L instructions and Section M evaluation
+factors. Every row below assumes that shape unless marked otherwise.
+
+**It does not apply unmodified to FAR Part 36 construction solicitations.** Those use
+SF1442, have no lettered sections, commonly use two volumes rather than four, and place
+instructions and evaluation criteria as unlabeled free-text blocks inside the solicitation
+PDF. Where a row below says "Section L instruction" or "Section M factor," read it against
+a Part 36 solicitation as "the enumerated instruction bullets under each factor's
+instruction block" and "the stated evaluation factor," and expect no lettered anchor to
+extract against. **[GATE]** the pipeline must classify solicitation format (UCF vs SF1442
+vs other) before selecting a volume model, and fail closed rather than assume UCF.
+
+Rows tagged **[UCF-ONLY]** below have been observed not to apply on a Part 36 construction
+buy. They are retained because they are sourced, not because they are universal.
```

**And amend §0.1's opening clause:**

```diff
-1. **Section L/M compliance matrix is the spine of the whole proposal, not a technical-volume
-   artifact.**
+1. **The compliance matrix is the spine of the whole proposal, not a technical-volume
+   artifact.** On a UCF solicitation it is built from Section L instructions and Section M
+   factors. On a non-UCF solicitation (§0.0) it is built from the enumerated instruction
+   bullets under each stated factor, which is harder to extract and easier to under-count:
+   in the observed winner, six enumerated obligations were never answered.
```

---

## 2. The compliance matrix is an internal artifact, not submitted content

**Why.** The observed winner submitted no compliance matrix, and would have been spending a
five-page allowance on a table if it had. The rubric does not say to submit one, but the
factory's `package_rfp_response` renders it as §3 of the delivered document, which is the rubric
being read as though it did. Fix the rubric so the implementation has a clear instruction.

```diff
 1. **The compliance matrix is the spine...**
+
+   **Where it lives.** The matrix is a *working and review* artifact, not proposal content,
+   unless the solicitation's own instructions require a cross-reference table. Submit it only
+   when asked. Page allowances are for evidence. In the one real winner reviewed
+   (`knowledge/research/winning-proposal-teardown/REPORT.md` §2.3) no matrix was submitted in
+   either volume. **[GATE]** the matrix exists and every instruction maps to a section;
+   **[GATE]** it is *not* rendered into the deliverable unless the solicitation requires it.
```

---

## 3. New section: Forms and Instruments (including bonding)

**Why.** This is the largest omission in the rubric. The observed winning price volume was
roughly 93% forms and instruments. The bid guarantee, a surety-executed bond at ten percent with
the original couriered post-close, was the hardest gate in the pursuit and the rubric never
mentions bonding. Amendment acknowledgment is a stated non-responsiveness trigger and is not
mentioned either.

**Proposed new §4A, immediately after the Pricing section:**

```diff
+## 4A. Forms and Instruments volume/section
+
+**Why this section exists:** in the one real winner reviewed, the volume nominally titled
+"Price Proposal" contained one dollar figure and four forms. Treating that volume as a
+pricing narrative (§4) misreads what it is. On fixed-price construction and on many
+simplified acquisitions, the priced volume is a **forms and instruments package with a
+number in it**. This section covers the package. §4 covers the number.
+
+### Required content elements
+
+| Element | Source | Tag |
+|---|---|---|
+| The solicitation's own offer form, completed and signed in every block it directs (SF1442 blocks 14–20c on construction; SF33/SF1449 analogues elsewhere) | teardown §4.2 | [GATE] every directed block non-empty |
+| Priced schedule matching the solicitation's own CLIN structure exactly, including unit of measure | teardown §4 | [GATE] |
+| **Amendment acknowledgment**, every amendment, by number and date | teardown §5.6 item 3 | [GATE] count of acknowledged amendments equals count published on SAM.gov. Independently fatal: solicitations routinely state that failure to acknowledge renders an offer non-responsive. The observed winner left this block blank. |
+| **Bid guarantee / bond**, where required: correct form, correct percentage, executed by a surety, scanned into the volume, **and** the original delivered by the stated method to the stated address by the stated post-close deadline | teardown §0.3, §4.2, §5.6 item 1 | [GATE] presence and percentage; the underlying bonding capacity is not gateable and is a **go/no-go qualification input**, not a proposal task |
+| Representations and certifications **as posted in SAM for this offeror**, not the blank FAR provision text | teardown §2.5 | [GATE] the artifact is the offeror's SAM export, not an unfilled provision |
+| Subcontracting-limitation certification, completed on the line applicable to **this** NAICS and contract type, with the statutory floor met | teardown §2.5, §5.6 item 4 | [GATE] correct line selected by NAICS; percentage meets the floor |
+| Title page carrying every element the instructions enumerate, plus the FAR 52.215-1(c)(2) first-page information and the statement of extent of agreement with the solicitation's terms | teardown §2.5 | [GATE] element-by-element checklist |
+
+### Common disqualifiers
+
+| Disqualifier | Tag |
+|---|---|
+| Any unacknowledged amendment | [GATE] |
+| Bond absent, wrong percentage, unexecuted, or original not delivered by the stated deadline | [GATE] presence; [JUDGMENT] on recovery if the deadline is missed |
+| Certification completed on the wrong line, or self-performance below the statutory floor | [GATE] |
+| Blank provision text submitted in place of the offeror's own completed representations | [GATE] |
+
+### Qualification gate, upstream of everything
+
+**[GATE]** If the solicitation requires a bid guarantee or performance and payment bonds and
+the offeror has no bonding line, the pursuit is not enterable. This check belongs at triage,
+before any drafting work is done, not at proposal review.
```

---

## 4. New section: Out-of-Band Obligations

**Why.** The observed winner discharged an entire six-page evaluation factor by getting three
third parties to file a form with the contracting officer before close. Nothing about that is
proposal content, and missing it is fatal. The rubric has no concept of an obligation due
somewhere other than the proposal submission.

**Proposed new §7, renumbering the existing §7 mapping table to §8:**

```diff
+## 7. Out-of-band obligations
+
+Things that must happen, on a deadline, **somewhere other than the proposal document**.
+Every one of these is fatal if missed and invisible to a document-completeness check.
+
+| Obligation | Typical timing | Tag |
+|---|---|---|
+| Past-performance questionnaires submitted **by the references themselves** directly to the contracting officer | before proposal close; the references control it, the offeror does not | [GATE] tracked with a per-reference send date and confirmation; [JUDGMENT] reference selection and chasing |
+| Bond original delivered by traceable courier to a physical address | commonly a fixed number of business days **after** close | [GATE] |
+| Question / RFI cutoff | commonly days before close | [GATE] date extracted; [JUDGMENT] whether to ask |
+| Mandatory or effectively-mandatory pre-award site visit and field verification | fixed date before close | [GATE] date extracted; attendance is a physical act, not automatable |
+| SAM registration active and representations current as of the offer date | continuous | [GATE] |
+
+**Product note:** in the observed winner, past performance was **entirely** discharged this
+way. One sentence in the volume pointed at questionnaires third parties had already filed.
+A pipeline that generates documents and nothing else cannot see any of this, and the
+consequences of missing it exceed the consequences of a weak narrative.
```

---

## 5. Re-scope "unaddressed requirement equals not awardable"

**Why.** The rubric's §1 disqualifier row states that any unaddressed mandatory requirement is a
deficiency rendering the proposal not awardable. The observed winner left at least six
enumerated instructions completely unanswered and was awarded. The row is not wrong as a
statement of the definition. It is wrong as a prediction of behavior.

```diff
-| Deficiency = "does not meet requirements... Proposal is not awardable" (VA guide's own definition): any unaddressed mandatory requirement | `REPORT.md` §3 | [GATE] every Section L technical requirement has a mapped, present answer |
+| Deficiency = "does not meet requirements... Proposal is not awardable" (VA guide's own definition): any unaddressed mandatory requirement | `REPORT.md` §3 | [GATE] every technical instruction has a mapped, present answer. **Scope condition, evidence-based:** this is the definition, not reliably the practice. In the one real winner reviewed (teardown §3.2), six enumerated instructions were unanswered and the award was still made, on a sub-$250K best-value construction buy where technical factors converged and price decided. Treat completeness as **insurance that scales with competition and dollar value**, not as a bright line. Report unanswered instructions to the client as risk, ranked, rather than as automatic disqualification. |
```

**And add a companion row to "what evaluators actually score":**

```diff
+| **Where completeness actually binds.** Completeness matters most where the field is large, the technical factors genuinely discriminate, or a disappointed offeror is likely to protest. It matters least on small, price-converged buys with short response windows. Same instruction, different consequence. | teardown §3.2, §5.2 | [JUDGMENT] |
```

---

## 6. Relevance by selection, not only by narrative

**Why.** This is the most transferable technique found. The observed winner wrote zero relevance
sentences and instead chose three projects that sit on the solicitation's own published
relevancy tiers, in the same metropolitan area, with the same trade mix. The rubric assumes
relevance is argued in prose.

```diff
-| Recency and relevance stated explicitly against the *current* solicitation's own scope/magnitude/complexity, not a generic "similar work" claim | FAR 15.305(a)(2); `REPORT.md` §2, §3 | [JUDGMENT] |
+| Recency and relevance established against the *current* solicitation's own scope/magnitude/complexity. **Two mechanisms, and the second is the stronger one.** (a) *By narrative*: an explicit relevance argument per project. (b) ***By selection*: choosing projects that land on the solicitation's own published relevancy tiers, in the same geography, with the same trade or labor mix, so the evaluator can apply the ladder without help.** In the one real winner reviewed (teardown §3.3), mechanism (b) was used exclusively and mechanism (a) was entirely absent. | FAR 15.305(a)(2); teardown §3.3 | [JUDGMENT] on the choice; **[GATE]** that the chosen set is scored against the solicitation's own stated tiers and the scoring is shown to the client |
```

**And add a required element:**

```diff
+| A **reference-selection rationale**, internal, showing which candidate projects were considered and why these were chosen against the solicitation's own tiers. Not submitted; it is the record of the judgment. | teardown §3.3 | [GATE] present in the review note |
```

---

## 7. Mark the adjectival and confidence scales as agency-conditional

**Why.** The rubric imports the Outstanding-to-Unacceptable adjectival scale, the
Low/Moderate/High risk rating, and the five-level performance-confidence scale from a single
agency's source selection guide. The observed solicitation states none of them. It states a
tradeoff, a four-level relevancy ladder, and nothing else.

```diff
-| Adjectival rating keyed to strength/weakness/deficiency balance: Outstanding → Good → Acceptable → Marginal → Unacceptable, per the VA's own Table 1/2 definitions |
+| Adjectival rating keyed to strength/weakness/deficiency balance: Outstanding → Good → Acceptable → Marginal → Unacceptable. **Agency-conditional.** These are one agency guide's tables, not a FAR requirement. The observed construction solicitation published no adjectival scale at all (teardown §5.2). **[GATE]** extract the solicitation's *own* stated rating methodology first; apply this table only if the solicitation states it or an equivalent. Do not build gates against a scale the solicitation does not use. |
```

Apply the same conditional framing to the §1 risk-rating row and the §3 performance-confidence
row.

**Retain unchanged:** the §3 four-level relevancy scale. The observed solicitation published
that ladder independently, with dollar thresholds. It is now confirmed from a primary
solicitation rather than a secondary guide, which is a strict upgrade in source quality.

---

## 8. Scope conditions on the pricing volume

**Why.** Three of the four headline rows in §4 are unreachable on a single-CLIN fixed-price
buy. See teardown §4.1.

```diff
+**Applicability, read this first.** Every row below assumes a solicitation that requires a
+*priced breakdown*. Many do not. On a firm-fixed-price construction or simplified acquisition
+with a single CLIN, the priced volume is one number plus forms (see §4A), and the rows below
+are not merely unmet, they are structurally unreachable: there are no lines to break out, no
+hours to reconcile, and unbalanced-pricing analysis is a comparison among line items that
+cannot be performed on one line item. **[GATE]** determine from the solicitation's own pricing
+instructions whether a breakdown is required before applying this section.
```

```diff
-| Line-item cost breakdown: labor category/rate/hours, materials, ODCs, indirect costs, profit/fee... |
+| Line-item cost breakdown: labor category/rate/hours, materials, ODCs, indirect costs, profit/fee... **Required only where the solicitation's pricing instructions ask for it.** The observed winner supplied one lump sum against a 40-page allowance and was awarded (teardown §4). |
```

```diff
-| **Unbalanced pricing** review: line items materially over/understated... |
+| **Unbalanced pricing** review: line items materially over/understated... **Not applicable to single-CLIN awards**, where the analysis has no comparands. Solicitations often retain the boilerplate anyway; do not treat retained boilerplate as an applicable requirement. |
```

**And add one genuinely new required element, which the rubric currently has nowhere:**

```diff
+| **Quantity schedule** derived from the solicitation's own stated dimensions and counts, supplied to the offeror's estimator as an input. This is not a price and must never be rendered as one. On construction SOWs the government commonly states its own takeoff (linear feet, square feet, unit counts, fixture types); capturing it is derivable work that assists pricing without performing it. | teardown §6.1, §6.2 | [GATE] presence where the SOW states quantities; [JUDGMENT] never on the price itself |
```

---

## 9. Exceptions, exclusions and assumptions

**Why.** The observed winner closed its technical section with a short exclusions list scoping
out three trades, one of which arguably conflicts with the SOW. Standard construction practice,
consequential, and the rubric has no row for it.

**Proposed addition to §1 required content elements:**

```diff
+| **Exceptions taken, exclusions, and assumptions**, stated explicitly and in one place if taken at all | teardown §3.5 | [GATE] if any exclusion appears anywhere in the proposal, it is consolidated and stated once; **[JUDGMENT]** whether to take an exception at all, which is a commercial risk decision no pipeline can make. Flag the tension: an exclusion allocates risk and protects margin, and simultaneously creates a responsiveness argument against the offer. The observed winner excluded a trade the SOW elsewhere requires engineering analysis for, and was still awarded. |
```

---

## 10. Scale review depth to pursuit size and response window

**Why.** §0.6 prescribes Pink-equivalent and Red-equivalent checkpoints. The observed pursuit
had a six calendar day window, weekend included, for a six-page authored submission, and the
evidence says no independent review occurred: a stale header from a prior solicitation survived
onto both volumes.

```diff
 6. **Color-team-equivalent review checkpoints**...
+
+   **Scaled to the pursuit.** Two full review passes presume a response window measured in
+   weeks. The observed winner had six calendar days from issue to close and produced roughly
+   six authored pages (teardown §0.3, §1). At that scale prescribe **one** pass, and spend it
+   on the mechanics: forms complete, amendments acknowledged, bond executed, page limits,
+   title-page elements, no stale content carried over from a prior pursuit's template. In the
+   observed winner the PDF headers of *both* volumes carried a prior solicitation's document
+   title, which a single mechanics pass would have caught. **[GATE]** review depth selected
+   from response-window length and pursuit value, and the selection recorded.
```

---

## 11. Generalize the certification row

**Why.** §0.4 is written entirely around SDVOSB and VetCert. The observed pursuit was a plain
small business set-aside with no socioeconomic claim, so the row was unreachable. The underlying
principle generalizes cleanly and is worth more generalized.

```diff
-4. **SDVOSB/VOSB certification assertions must track the current VetCert regime...**
+4. **Assert exactly the set-aside basis the solicitation invokes, no more and no less, using
+   current terminology.** Where the solicitation is a plain small business set-aside, the
+   assertion is size-standard compliance under the stated NAICS and nothing further; the
+   observed winner made no socioeconomic claim at all (teardown §5.1). Where a socioeconomic
+   set-aside is invoked, the assertion must track the current certification regime and be
+   dated. **SDVOSB/VOSB specifically:** a single SBA-administered program (13 CFR Part 128)
+   since 1 January 2023, valid 3 years, 90-day pre-expiration recertification window, 30-day
+   post-expiration grace; never "self-certified" language, never the retired VA-only CVE
+   framing. **[GATE]** the asserted basis matches the solicitation's stated set-aside; any
+   certification assertion is present, dated, and not using retired terminology.
```

---

## 12. Page-allowance underuse

**Why.** The rubric names exceeding page limits as a disqualifier, which is correct. The
observed failure mode was the opposite and by a wide margin: about five pages used of roughly
fifty-one allowed across three factors, including one sentence against a six-page allowance.

**Proposed addition to §1 common disqualifiers, as a note rather than a disqualifier:**

```diff
+| *Not a disqualifier, but worth a flag:* **substantial page-allowance underuse.** The observed winner used roughly five of about fifty-one allowed pages across three factors, including one sentence against a six-page past-performance allowance, and won (teardown §1). Underuse is sometimes correct and sometimes a missed opportunity to generate strengths. Surface the ratio to the client with the unanswered-instruction list from §5 above, and let them decide. Do not gate on it in either direction. | teardown §1, §3.2 | [JUDGMENT] |
```

---

## Rows proposed for deletion

None outright.

The closest candidate is the entire §2 Management Volume, every row of which was unreachable
against this pursuit. It should **not** be deleted: it is sourced, and it plainly applies to
larger services acquisitions, which is much of what the UCF research covered. It should instead
be marked **[UCF-ONLY]** per change 1, and the *implementation* should stop hard-coding a
four-volume model, which is an engineering fix rather than a rubric fix and is tracked in the
teardown's gap list (§7 item 3) rather than here.

---

## What a second and third winner would settle

Listed so the next teardown is cheaper and so nobody over-reads n=1.

1. Does the pattern hold above the simplified acquisition threshold, or does completeness start
   binding once the field is larger and protest risk is real? Change 5 hinges entirely on this.
2. Do services buys in our target codes actually publish the adjectival and confidence scales
   the rubric imports? Change 7 hinges on this.
3. Is relevance-by-selection general, or an artifact of a solicitation that happened to publish
   an unusually explicit relevancy ladder with dollar thresholds? Change 6 hinges on this.
4. How often is the priced volume a forms package rather than a breakdown? Changes 3 and 8 hinge
   on this, and it is the single highest-value question for the product.

A useful next sample would be one services buy and one construction buy above the simplified
acquisition threshold, which would test all four at once.
