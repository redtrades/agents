# Proposal rubric: full-RFP proposal volumes

2026-08-25. Sourced from `research/proposal-writing/REPORT.md` (read that file for citation
detail and source-quality caveats: every claim below is sourced there; this file states the
rubric plainly for direct consumption, cross-references only). This is the proposal-volume
analog of `sop/SOP-DELIVERABLES.md`'s §2.3/§2.4 (Sources Sought template + gates) and §3.3/§3.4
(Market Snapshot template + gates), same discipline, different deliverable: a **full RFP
proposal response**, not a market-research reply or a capture-intelligence brief.

**Relationship to `sop/SOP-DELIVERABLES.md`:** that SOP is APPROVED/frozen for its two existing
deliverables (§0 header) and is not amended by this file. This rubric does not modify
SOP-DELIVERABLES.md's gates, templates, or citation contract; it is new, additive reference
material for a deliverable type the SOP does not yet cover. Section 1.2's citation-format
contract, §1.3's `[CLIENT PROVIDES]` marker convention, and the fail-closed/no-claim-without-a-
file rules (`AGENTS.md` rules 2–4) all carry over unchanged and are assumed throughout below.

**Intended consumer:** the factory's RFP-response-starter deliverable module (issue #80). Per
`runs/20260825T015239Z-446b40/RETROSPECTIVE.md`, that module today extracts attachment-derived
requirements correctly but discards them before synthesis (§2 of that retrospective), has no
pricing-volume capability, and has no `.xlsx`/spreadsheet attachment extractor. This rubric is
written so each row below can become either (a) a mechanical gate check in
`factory/gates/registry.py`-style code, or (b) a named judgment item routed to founder review,
mirroring the SOP's existing G1–G5 / human-judgment split, not inventing a new pattern.

**Format:** each volume section has three tables: Required Content Elements, What Evaluators
Actually Score, Common Disqualifiers, each row tagged **[GATE]** (a script can mechanically
check it, following the pattern of `sop/SOP-DELIVERABLES.md` §2.4/§3.4) or **[JUDGMENT]** (needs
human or LLM-with-human-review judgment, following §2.5/§3.5's pattern). A row can be partially
gateable, tagged **[GATE+JUDGMENT]**, when a script can check presence/format but a human must
judge quality or fit.

---

## 0. Cross-cutting rules (apply to every volume)

1. **Section L/M compliance matrix is the spine of the whole proposal, not a technical-volume
   artifact.** Every Section L instruction and every Section M evaluation factor/subfactor gets
   one row with a section pointer and an owner; the proposal's own section order should mirror
   Section M's scoring sequence, not the offeror's internal logic (FAR 15.305(a) binds the
   agency to evaluate "solely on the factors... specified in the solicitation";
   `REPORT.md` §2, §1). **[GATE]** presence of every L/M row mapped to a document section,
   directly extends `sop/SOP-DELIVERABLES.md` §2.4 G1's existing compliance-matrix gate pattern.
2. **Register**: compliance-anchored, not capability-marketing, more so than a sources-sought
   response, because a proposal is evaluated against stated, scored criteria, not read as
   general market-research evidence (`sop/SOP-DELIVERABLES.md` §2.5 item 7's register check:
   "would any sentence read as marketing rather than evidence to a CO?", which applies here with even
   less tolerance, since a proposal evaluator scores every sentence against a factor). Never name
   a competitor; unattributed "ghosting" only, evidence-backed, never unsupported negative
   language (`REPORT.md` §1, APMP). **[JUDGMENT]**
3. **Precision-of-statement is a protest-defense feature.** The GAO sustain pattern (`REPORT.md`
   §4) traces every reviewed sustain to an evaluator's inability to point at proposal text
   supporting a rating: ambiguous staffing-month statements, SIN-category confusion, and
   cross-section bleed are exactly what gets exploited. Every factual claim (dates, durations,
   dollar figures, certifications) must be stated once, unambiguously, and consistently across
   every volume that references it. **[GATE+JUDGMENT]**: cross-volume consistency (e.g.,
   staffing hours in Management matching priced labor categories in Pricing) is mechanically
   checkable; whether a sentence is *ambiguous enough to be misread* is judgment.
4. **SDVOSB/VOSB certification assertions must track the current VetCert regime, not
   self-certification-era language.** Certification is a single SBA-administered program (13 CFR
   Part 128) since January 1, 2023, valid 3 years, with a 90-day pre-expiration recertification
   window and a 30-day post-expiration grace/reinstatement window (`REPORT.md` §0.5). A proposal
   must cite VetCert certification status and dates, never "self-certified" language (obsolete
   since 2024) or the old VA-only CVE framing. **[GATE]** cert-status assertion present, dated,
   and not using retired terminology.
5. **Executive Summary is not a separately-scored volume** (verified against sources, not
   assumed, `REPORT.md` §5). Treat it as a short cross-volume framing section, not a fifth
   scored factor; do not gate it the way Technical/Management/Past-Performance/Pricing are
   gated below. Required only where Section L calls for one; content: solution overview,
   stated differentiators, explicit tie to the RFP's own stated requirements/evaluation factors
   (`REPORT.md` §0.1). **[JUDGMENT]** (quality only; presence is a simple **[GATE]** check against
   whether Section L requires it).
6. **Color-team-equivalent review checkpoints**, adapted from Shipley (`REPORT.md` §1) to this
   factory's pipeline: a **Pink-equivalent** check (compliance-matrix + narrative-completeness
   pass, ~mid-draft) and a **Red-equivalent** check (independent, evaluator-perspective scoring
   against the actual Section M language, run by a reviewer who did not draft the section) before
   anything reaches Mike's final review. **[JUDGMENT]**, but the *inputs* to each review
   (compliance matrix, Section M text, win themes) are **[GATE]**-checkable for presence.

---

## 1. Technical Volume

### Required content elements

| Element | Source | Tag |
|---|---|---|
| Technical approach/methodology addressing the SOW/PWS/SOO point by point | `REPORT.md` §0.1, §5 (OCIWins) | [GATE] presence per compliance-matrix row |
| Solution architecture, tools, processes proposed | `REPORT.md` §0.1 | [JUDGMENT] |
| Risk identification + mitigation approach tied to *this* contract's specific risks, not generic boilerplate | `REPORT.md` §0.1; VA guide's risk-rating framework, `REPORT.md` §3 | [JUDGMENT] |
| Every enumerated Section L technical-volume instruction answered in the section it's assigned to | FAR 15.305(a); `REPORT.md` §2 | [GATE] |
| Personnel qualifications and facilities where the RFP requests them (VA guide names these as technical-factor subfactors) | `REPORT.md` §3 (VA Source Selection Guide p.9) | [GATE] presence / [JUDGMENT] quality |

### What evaluators actually score

| What's scored | Source | Tag |
|---|---|---|
| Strength = "merit or exceeds specified... requirements in a way that will be advantageous... during contract performance" (VA guide's own definition, p.12), not just meeting the requirement | `REPORT.md` §3 | [JUDGMENT] |
| Adjectival rating keyed to strength/weakness/deficiency balance: Outstanding → Good → Acceptable → Marginal → Unacceptable, per the VA's own Table 1/2 definitions | `REPORT.md` §3 (VA guide p.14-15) | [JUDGMENT] (rating is the evaluator's; a self-check against the same rubric is [GATE+JUDGMENT]) |
| Risk (Low/Moderate/High) tied to schedule/cost/performance disruption potential of the *proposed approach itself*, evaluated either combined with the technical rating or separately | `REPORT.md` §3 (VA guide p.15-16, Table 3) | [JUDGMENT] |
| Precision of factual claims (dates, durations, quantities): evaluators rate what the text actually says, and misstatement is a GAO-sustained protest ground when it favors an awardee incorrectly | `REPORT.md` §4 (*Emissary LLC*, B-422388.3/.4) | [GATE] internal consistency check / [JUDGMENT] clarity |

### Common disqualifiers

| Disqualifier | Source | Tag |
|---|---|---|
| Deficiency = "does not meet requirements... Proposal is not awardable" (VA guide's own definition): any unaddressed mandatory requirement | `REPORT.md` §3 | [GATE] every Section L technical requirement has a mapped, present answer |
| Non-responsive sections that ignore the RFP's own language/terminology | `REPORT.md` §0.1 | [GATE+JUDGMENT] |
| Exceeding stated page limits without approval | `REPORT.md` §0.1 | [GATE] |
| Generic/boilerplate risk section with no tie to this contract's actual risk profile | `REPORT.md` §0.1, §3 | [JUDGMENT] |
| Missing signatures/certifications the technical volume requires | `REPORT.md` §0.1 | [GATE] |

---

## 2. Management Volume

### Required content elements

| Element | Source | Tag |
|---|---|---|
| Organizational structure / org chart | `REPORT.md` §0.1, §5 | [GATE] presence |
| Key personnel resumes/qualification summaries for every RFP-designated key position, meeting stated minimums (years, certs, clearance) | `REPORT.md` §5 (Hinz Consulting) | [GATE] every designated position has a named resume meeting the *stated* minimum thresholds |
| Staffing plan mapping labor categories to SOW tasks, with hours | `REPORT.md` §5 | [GATE+JUDGMENT] presence + cross-check against Pricing volume |
| PM methodology, QA/QC procedures, schedule/resource allocation | `REPORT.md` §0.1 | [JUDGMENT] |
| Risk-management approach (may be technical-factor or management-factor depending on the RFP's own factor structure; VA guide notes technical factor titles vary but the same rating tables apply) | `REPORT.md` §3 | [JUDGMENT] |
| Small-business participation plan/subcontracting plan where the RFP scores it as a stand-alone factor or subfactor | `REPORT.md` §3 (VA guide p.18) | [GATE] presence when required |

### What evaluators actually score

| What's scored | Source | Tag |
|---|---|---|
| Same Outstanding→Unacceptable adjectival scale applied to the management factor exactly as to technical (VA guide treats "technical" as a label covering any non-cost factor including management approach) | `REPORT.md` §3 | [JUDGMENT] |
| Key-personnel minimum-qualification match is a binary gate inside a judgment-scored volume; failing it is independently named as a common "unacceptable" trigger | `REPORT.md` §5 | [GATE] |
| Small-business evaluation ratings are either pass/fail (acceptable/unacceptable) or the full adjectival scale, per the RFP's own stated methodology (SST must pick one; VA guide p.18) | `REPORT.md` §3 | [GATE] which methodology the RFP specifies is present in the compliance matrix |

### Common disqualifiers

| Disqualifier | Source | Tag |
|---|---|---|
| A named key-personnel candidate who does not meet the RFP's stated minimum qualification | `REPORT.md` §5 | [GATE] |
| Staffing-plan hours that don't reconcile with the Pricing volume's labor-category hours | `REPORT.md` §5, §0.1 (cost-inconsistency-across-volumes disqualifier) | [GATE] cross-volume numeric reconciliation |
| Missing QA/QC or PM methodology where Section L requires it | `REPORT.md` §0.1 | [GATE] |

---

## 3. Past Performance Volume

### Required content elements

| Element | Source | Tag |
|---|---|---|
| Per-project: contract number, type, prime/sub role, value, period, customer, scope narrative; same standard already established in `sop/SOP-DELIVERABLES.md` §2.3's Sources Sought template, extended here to a scored proposal factor | `sop/SOP-DELIVERABLES.md` §2.3; `REPORT.md` §2 | [GATE] every field present + provenance-cited, exactly per SOP §1.2 |
| Recency and relevance stated explicitly against the *current* solicitation's own scope/magnitude/complexity, not a generic "similar work" claim | FAR 15.305(a)(2); `REPORT.md` §2, §3 | [JUDGMENT] |
| Certification/registration status current (VetCert dates) where cited as part of eligibility, not folded silently into past-performance narrative | `REPORT.md` §0.5 | [GATE] |
| Explicit acknowledgment when the offeror has thin/no directly relevant history: do not omit the section; state it plainly | FAR 15.305(a)(2) "may not be evaluated favorably or unfavorably"; `REPORT.md` §2, §3 | [GATE] section present even when evidence is weak, per `AGENTS.md` rule 5 (conservative reading, more gaps rather than invented claims) |

### What evaluators actually score

| What's scored | Source | Tag |
|---|---|---|
| **Relevancy**, on a 4-level scale: Very Relevant / Relevant / Somewhat Relevant / Not Relevant, keyed to scope, magnitude, and complexity match to *this* solicitation (VA guide's own Table 4 definitions) | `REPORT.md` §3 (VA guide p.16-17) | [JUDGMENT] (a scope-shape call, same as `sop/SOP-DELIVERABLES.md` §2.5 item 1's existing human-judgment item) |
| **Performance-confidence assessment**, a *separate* 5-level scale: Substantial / Satisfactory / Limited / No Confidence / **Unknown Confidence (Neutral)** when the record is too sparse to rate meaningfully | `REPORT.md` §3 (VA guide p.18, Table 5) | [JUDGMENT] |
| Sources evaluators actually pull from: PPIRS, FAPIIS, eSRS, direct interviews with PMs/COs/FDOs, DCMA, plus offeror-submitted references, not just what the offeror writes | `REPORT.md` §3 (VA guide p.17) | n/a (evaluator-side; informs how strong the offeror's own narrative needs to be, since the government cross-checks it against sources the offeror doesn't control) |
| No favorable-or-unfavorable penalty for a thin record: an honest "not relevant" self-assessment is not itself a disqualifier | FAR 15.305(a)(2) | [GATE] (the *presence* of an honest self-assessment, as distinct from its content) |

### Common disqualifiers

| Disqualifier | Source | Tag |
|---|---|---|
| Claiming "completed" on a project that is actually still ongoing, where the RFP requires completed-within-N-years: same failure mode `sop/SOP-DELIVERABLES.md` §2.3 already gates for Sources Sought, equally disqualifying in a scored proposal | `sop/SOP-DELIVERABLES.md` §2.4 G2 pagination/evidence rule | [GATE] |
| Missing contract number / unverifiable claim | `sop/SOP-DELIVERABLES.md` §1.2 | [GATE] |
| Overreaching relevance claims not supported by actual scope overlap ("one-to-one analogue" overreach, same register-check failure mode already named in `sop/SOP-DELIVERABLES.md` §2.5 item 2) | `sop/SOP-DELIVERABLES.md` §2.5 item 2 | [JUDGMENT] |

---

## 4. Pricing / Cost Volume

**Factory gap note:** per `runs/20260825T015239Z-446b40/RETROSPECTIVE.md` §2, this is the volume
the current pipeline has essentially no capability for: no pricing-attachment extraction
(`.xlsx` Schedule-of-Values files fail silently), no priced-volume synthesis path. Every row
below is a target for that gap, not a description of something already built.

### Required content elements

| Element | Source | Tag |
|---|---|---|
| Line-item cost breakdown: labor category/rate/hours, materials, ODCs, indirect costs, profit/fee, matching what a CO's cost-analysis review actually examines (Direct-Labor $, Direct Material, Indirect Costs, ODC, Facilities Capital Cost of Money, Profit/Fee) | `REPORT.md` §3 (VA guide p.13-14) | [GATE] presence of each line the RFP's own Section L pricing instructions require |
| Basis/assumptions for each priced line, sufficient to support a price- or cost-realism review | FAR 15.404-1 | [JUDGMENT] |
| Consistency with the Technical/Management volumes' proposed labor hours and approach | `REPORT.md` §5, §0.1 | [GATE] cross-volume numeric reconciliation, same as Management-volume row above |
| Explicit obligated-vs-ceiling-vs-outlaid labeling on any historical pricing-calibration figures cited (carrying over the existing SOP §3.3 P8-3 rule to a proposal context) | `sop/SOP-DELIVERABLES.md` §3.3 (P8-3) | [GATE] |

### What evaluators actually score

| What's scored | Source | Tag |
|---|---|---|
| Price/cost is evaluated in *every* source selection, but adjectival ratings are never used for cost/price: it's fair/reasonable or it isn't, a determination the CO makes, not a scored adjectival factor | `REPORT.md` §3 (VA guide p.13) | n/a (evaluator-side; means a pricing volume's job is defensibility, not "scoring well" the way technical does) |
| **Price analysis** (is the price too high?): comparison to prior prices paid, independent government estimate, competing quotes/published price lists, GSA prices | `REPORT.md` §2 (FAR 15.404-1) | [JUDGMENT] |
| **Cost realism analysis** (is the price too low relative to the offeror's own proposed technical/staffing approach?): required on cost-reimbursement contracts, permitted on some fixed-price cases | `REPORT.md` §2 (FAR 15.404-1) | [JUDGMENT] |
| **Unbalanced pricing** review: line items materially over/understated relative to the total, even if the total is acceptable; may (not must) cause rejection | `REPORT.md` §2 (Tillit Law) | [GATE] line-item variance check against a reasonableness band, flagged for [JUDGMENT] on rejection risk |

### Common disqualifiers

| Disqualifier | Source | Tag |
|---|---|---|
| Cost inconsistency between the Pricing volume and the Technical/Management narrative (independently named disqualifier) | `REPORT.md` §0.1 | [GATE] |
| A price so far below realistic cost that it fails cost-realism review, undermining the offeror's own demonstrated "understanding of the work" | `REPORT.md` §2 (FAR 15.404-1) | [JUDGMENT] |
| Missing a required pricing line/format Section L specifies (payment schedule, CLIN structure, etc.) | `REPORT.md` §0.1 | [GATE] |

---

## 5. Executive Summary (cross-cutting, not a scored volume)

Per `REPORT.md` §5: not separately scored under Section M in any source checked. Required only
where Section L calls for one.

| Element | Source | Tag |
|---|---|---|
| Solution overview tied explicitly to the RFP's own stated requirements/objectives | `REPORT.md` §0.1 | [JUDGMENT] |
| Stated differentiators/win themes, framed as customer benefit, not generic capability marketing (Shipley win-theme discipline) | `REPORT.md` §1 | [JUDGMENT] |
| No claim here that isn't substantiated in one of the scored volumes: an exec summary that promises something the technical/management volumes don't deliver is a consistency risk, same register-anchoring principle as §0.2/§0.3 above | `REPORT.md` §0.1, §2 (traceability principle from GAO sustains) | [GATE+JUDGMENT] |

---

## 6. Register/voice: concrete, not aspirational

Grounded in how this repo's existing deliverables are voiced (`sop/SOP-DELIVERABLES.md` §2.3–
§2.5, §3.3–§3.5) and how a proposal must differ:

- A **sources sought response** is market-research evidence submitted to help a CO write a
  set-aside determination; its register can lean toward demonstrating capability persuasively
  because there's no scored rubric on the other end (`sop/SOP-DELIVERABLES.md` §0.1). A
  **proposal volume** is scored line-by-line against Section M factors an evaluator applies
  mechanically (adjectival ratings, strength/weakness/deficiency counts), so voice must be
  **compliance-anchored first, persuasive second**: every claim should read as evidence an
  evaluator can point to and defend in a source selection decision document, not as marketing
  copy (`REPORT.md` §3, §4).
- Concretely: replace superlative claims ("the clear leader in...") with specific, cited
  capability statements, exactly the register-downgrade discipline `sop/SOP-DELIVERABLES.md`
  §2.5 item 7 already applies to sources-sought responses; apply it *more* strictly here, since
  a proposal evaluator is actively hunting for strengths/weaknesses/deficiencies to write down,
  not reading generally.
- Never name a competitor; ghost only, evidence-first (`REPORT.md` §1). This differs from a
  sources-sought response, where competitor mention is out of scope entirely
  (`sop/SOP-DELIVERABLES.md` §2.6 "Skip" line); a proposal's Technical/Management narrative can
  legitimately differentiate, but only in unnamed, benefit-framed terms.
- Section L formatting instructions always override house style (`REPORT.md` §1, APMP). This is
  a harder constraint than the sources-sought template's "mirror the notice's own structure"
  guidance (`sop/SOP-DELIVERABLES.md` §2.3); a proposal's format compliance is itself a scored
  or gating factor (FAR 15.204-1 Uniform Contract Format), not just good practice.

---

## 7. Mapping to `runs/20260825T015239Z-446b40/RETROSPECTIVE.md`'s gap list

For traceability, each retrospective-identified gap and the rubric section that targets it:

| Retrospective gap | RETROSPECTIVE.md § | Rubric section that targets it |
|---|---|---|
| Attachment-derived requirements extracted then discarded before synthesis | §2 | §0.1 (compliance-matrix-as-spine requires every extracted requirement to reach a document section, a synthesis-wiring fix, not new content, but this rubric assumes the wiring gap is closed) |
| No pricing-volume capability at all; `.xlsx` attachments fail silently | §2 | §4 (full Pricing Volume section, built to source the SOW's Schedule-of-Values once extraction exists) |
| Magnitude-extraction regex misses common phrasing | §6 | Not directly addressed here (an extraction-code fix, not a content-rubric gap), flagged for the factory engineering backlog, not this rubric |
| `DELIVERY-NOTE.md` doesn't reflect real gate results | §7 | Not addressed here: a rendering-pipeline defect, out of this rubric's scope (content/scoring, not pipeline plumbing) |

