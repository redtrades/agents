# Winning proposal teardown

Status: uncommitted working note. Not SOP. Not approved.
Date: 2026-08-27.
Companion file: `PROPOSED-RUBRIC-DIFF.md` in this directory (a proposal against
`research/proposal-writing/PROPOSAL-RUBRIC.md`, not an edit to it).

---

## 0. Sources, identification, and redaction discipline

### 0.1 What was read

Three PDFs, all added to Google Drive on the morning of 2026-08-27. The synced copies under
`~/Library/CloudStorage/GoogleDrive-<account>/My Drive/` are Drive stream placeholders, not
materialized bytes: every local read returned `OSError 35, Resource deadlock avoided`, while
other files in the same directory read normally. Content was therefore retrieved through the
Drive connector by file ID.

| Drive file ID | Filename shape (solicitation number redacted) | What the document actually is |
|---|---|---|
| `11uR3OBSF1sAIlX8u_YDesNdQIfx6f1yX` | `S02 [SOL-NUM]_F.pdf` | **The solicitation, not a proposal.** A 57-page SF1442 construction solicitation package: cover form, CLIN schedule, Statement of Work, special contract requirements, FAR clause block, submission instructions, evaluation factors, representations and certifications. This is the "SO2" Mike referred to. "S02" is a filename prefix, not a solicitation number and not a separate document type. |
| `171Inf05cgxHxDBfk8jcqvCzQE0KmtYsK` | `VOLUME I - Technical Proposal for [PROJECT] [SOL-NUM].pdf` | **Volume I of the winning offer.** 7 pages including cover and table of contents. Contains Factor 1 (Project Experience), Factor 2 (Past Performance), and a third section the solicitation did not request. |
| `1nSsmFXO41DZy8uTnT8kuoZgHZYugssVP` | `VOLUME II - Price Proposal for [PROJECT] [SOL-NUM] (1).pdf` | **Volume II of the winning offer.** 15 pages. Contains no price narrative. See §4, which is the headline of this report. |

All three IDs Mike sent match the three documents analyzed here. There is no fourth document,
and nothing with a similar name was read by mistake. The "two-volume proposal set" is Volumes I
and II above; the third file is the government's own solicitation, which is what makes the
teardown possible, because it lets every element of the offer be checked against what was asked
for.

### 0.2 Redaction discipline, applied from the first read

Nothing identifying appears anywhere below or in any file written to this repo. Specifically
excluded by construction, not by cleanup: the offeror's legal name, trade name, address, web
domain, principal and officer names, UEI, CAGE, EIN, and phone; the solicitation number; the
agency name and the contracting officer's and site POC's names, emails and phone numbers; the
named reference POCs, their employers and their contact details; the named subcontractor; the
offered price; the dollar value of any of the three reference projects; the project names and
room numbers of the reference projects; and the specific building address and suite numbers.
The offeror is called **[OFFEROR]** throughout. No PDF was copied into the repo. There are no
extended quotations: short fragments below are held to a few words each, quoted for compliance
analysis where the exact wording is the point.

An explicit scrub pass and its results are recorded in §9.

### 0.3 The pursuit, abstracted

A federal agency headquarters interior office renovation. NAICS 236220 (Commercial and
Institutional Building Construction), which is already one of this factory's target codes.
Small business set-aside. Firm fixed price. One CLIN. Sixty calendar days from notice to proceed
to final punch list. Best value tradeoff under FAR 15.101-1, award intended without discussions.
Two evaluated technical factors weighted equally with each other and, combined, approximately
equal to price, with an explicit statement that price decides as technical merit converges.

Two facts about the pursuit shape everything else:

- **The response window was six calendar days**, issue to close, including a weekend, with the
  question cutoff two days before close.
- **A bid guarantee was mandatory**, at ten percent of the offered price, executed on SF24 by a
  surety, scanned into Volume II, with the original hard copy couriered to the contracting
  officer within five business days.

Six days and a surety-executed bond are the real competitive filter. They are also both entirely
outside anything a document-generation pipeline can supply.

### 0.4 Standing caveat

This is n=1. One award, one agency, one NAICS, one dollar band, one point in time. There is no
visibility into the competing offers, the independent government estimate, or the source
selection decision document. Everything below is a description of what one winner did. It is not
evidence of what causes winning. Treat every finding as a hypothesis with one supporting
observation, and treat the rubric rows it contradicts as rows to question rather than rows to
delete.

---

## 1. Shape of the submission

| Volume | Factor | Pages allowed | Pages used | Allowance consumed |
|---|---|---|---|---|
| I | Factor 1, Project Experience | 5 | ~4 | ~80% |
| I | Factor 2, Past Performance | 6 (excl. CPARS) | ~0.1 (one sentence) | ~2% |
| I | Unrequested third section | n/a | ~2 | n/a |
| II | Factor 3, Price | 40 | ~1 (one number, stated twice) | ~2.5% |
| II | Forms, certifications, bond | not page-limited | ~13 | n/a |

Both volumes together are 22 pages, and roughly 13 of those are forms, scanned bond pages, and
copied FAR provision text. The narrative the offeror actually authored is about six pages.

The offeror was given 51 pages of allowance across the three factors and used about five. This
is not an oversight pattern. It is a consistent judgment that at this band, additional pages
were not worth writing.

---

## 2. Structure and compliance

### 2.1 The solicitation has no Section L and no Section M

This is the single most important structural finding, and it invalidates the spine of the
current rubric for an entire class of pursuits.

`PROPOSAL-RUBRIC.md` §0.1 makes the Section L/M compliance matrix "the spine of the whole
proposal" and requires the proposal's section order to mirror "Section M's scoring sequence."
That is the Uniform Contract Format under FAR 15.204-1. **Construction acquisitions under FAR
Part 36 use SF1442 and do not have lettered UCF sections at all.** This solicitation's
instructions and evaluation criteria are free text blocks buried inside a 57-page PDF, under
headings like "Instructions, conditions, and notices to offerors" and "Evaluation factors for
award," with no letter designation and no cross-reference scheme. There is nothing named
"Section L" to extract and nothing named "Section M" to mirror.

The factory's requirements extractor and the starter's compliance matrix both assume the UCF
shape. Against a 236220 buy, which is a code we target, that assumption produces a matrix keyed
to sections that do not exist.

### 2.2 Section order did mirror factor order, then stopped

Volume I's table of contents runs Factor 1, Factor 2, and then a third section titled as a
technical approach to the scope of work. The first two mirror the solicitation's factor
sequence, which supports the rubric's ordering principle. The third is unrequested: the
solicitation has no technical approach factor. So the winner both followed the evaluation order
and appended content outside it, in the same document.

### 2.3 There was no compliance matrix

Neither volume contains a compliance matrix, a cross-reference table, or a requirement-to-page
map. Not a reduced one. None.

This matters for the product. The current starter emits the compliance matrix as **§3 of the
delivered document**, which frames it as submitted content. No offeror at this band would submit
it, and a matrix in a 5-page-limited factor would consume allowance that should hold evidence.
The matrix is a correct and valuable artifact. It belongs in the review note, not the proposal.

### 2.4 Cross-volume references

There are none in either direction. Volume I never points at Volume II and Volume II never
points at Volume I. The only shared content is the cover page, which is duplicated nearly
verbatim across both volumes with only the volume number and table of contents changed.

The rubric's cross-volume numeric reconciliation gates (§1 precision, §2 staffing-to-pricing,
§4 consistency) have nothing to reconcile here. There are no hours in either volume, no labor
categories, no rates, and exactly one dollar figure in the entire submission. The reconciliation
gates are structurally unreachable on a single-CLIN fixed-price construction buy.

### 2.5 Where the precision budget went

The winner was meticulous about exactly two things and careless about everything else.

Meticulous: the cover page. It carries all seven elements the submission instructions
enumerate, plus the FAR 52.215-1(c)(2)(iii) statement of the extent of agreement with the
solicitation's terms, placed on the first page of both volumes exactly as instructed. The forms
package in Volume II is complete in structure and the bond is properly executed and scanned.

Careless: the PDF page header of **both** volumes carries the document title of a **different,
earlier solicitation's technical volume**, including that other solicitation's number and, on
Volume II, the words "Volume I." The winning price volume is headed with the title of a prior
pursuit's technical volume. The offeror duplicated a previous proposal's working document,
edited the body, and never touched the header. It did not cost them the award.

Three further defects survived award:

- ~~The SF1442 amendment acknowledgment block was left blank, on a solicitation that states in
  terms that failure to acknowledge an amendment renders a proposal non-responsive.~~
  **CORRECTED 2026-08-27 by the live SAM.gov pull** (see `PIPELINE-VS-WINNER.md` §1): the notice
  record reports `modifications.count: 0`. No amendments were ever issued, so the blank block was
  correct and this was not a defect. Recorded rather than deleted, because it is a good example
  of a wrong inference drawn from the proposal alone that only the authoritative source could
  overturn.
- The subcontracting-limitation certification was filled on the wrong line. The line for general
  construction, which is the applicable one for this NAICS and carries a fifteen percent self
  performance floor, was marked not applicable. A percentage was entered against the special
  trade contractor line instead.
- Where the instructions call for a printed copy of the offeror's own representations and
  certifications as posted in SAM, Volume II instead contains five pages of the blank FAR
  provision text with the checkboxes unmarked.

All of this sat under a stated rule that an omitted item renders the offer non-responsive. The
gap between what a solicitation says it will reject and what it actually rejects is wide at this
dollar band, and any product that sells compliance completeness has to be honest that
completeness buys insurance, not points.

---

## 3. What the winner did in the technical volume

### 3.1 Factor 1 carried content that was not project experience

The factor is titled Project Experience, but its instruction block enumerates roughly fourteen
distinct obligations, only about six of which concern past projects. The rest are forward
looking approach questions: understanding of the project and its challenges, response to
emergency situations, approach to obtaining critical construction materials, understanding of
local market conditions including labor and project labor agreements and weather, coordination
of temporary and permanent utility services, and approach to punch list, final acceptance and
closeout. Plus sustainable design and a quantified safety record.

**The factor title is misleading and an outline built from factor titles will be wrong.** A
compliance outline has to be built from the enumerated instruction bullets, not from the factor
headings. This is a concrete, mechanical requirement on the extractor.

### 3.2 Six enumerated instructions went entirely unanswered

Against that instruction block, the winning volume contains nothing at all on:

1. Sustainable design principles and environmental program goals, named in the instruction with
   two certification schemes as examples. Zero words.
2. Approach to obtaining critical construction materials and ensuring timely delivery. Zero.
3. Understanding of local market conditions: material and labor availability, project labor
   agreements, weather impact. Zero.
4. Coordination of temporary and permanent utility services. Zero.
5. Approach to punch list, final acceptance and project closeout. Zero as an approach.
6. Quantified safety record. The instruction asks for numbers of lost time accidents and days.
   Each project got the same three-word phrase asserting no injuries or delays, with no figures.

Also missing, and separately required: contract numbers for all three reference projects, period
of performance dates as opposed to a completion month, project addresses for two of three, and
a description of the project team and each firm's role for two of three.

The rubric's §1 disqualifier row states that any unaddressed mandatory requirement is a
deficiency and renders a proposal not awardable. **This winner has at least six and was
awarded.** That row needs to be re-scoped rather than deleted, and §5 of the diff proposes how.

### 3.3 The relevance argument was made by selection, not by prose

The solicitation publishes a four-level relevancy ladder with explicit dollar thresholds and a
similarity definition. The winner never writes a single sentence arguing relevance. There is no
"similar in scope and complexity because" anywhere in the document.

What the winner did instead: chose three projects that straddle the ladder, one landing above
each of the top three tiers, all federal or federal-adjacent interior fit-out work in the same
metropolitan area as the place of performance, all recent, all with the same trade mix as the
Statement of Work (demolition, metal stud framing, drywall to a stated finish level, ceiling
grid, lay-in lighting, flooring, cove base). The evaluator can apply the ladder without help
because the projects were picked to sit on it.

**This is the most transferable technique in the entire document set.** At this band, project
choice does the work the rubric assumes narrative does. It is also computable: given a firm's
job list and a solicitation's own relevancy definitions, ranking which three to submit is a
scoring problem, not a writing problem.

### 3.4 The unrequested third section is a scope echo

The third section restates the government's own Statement of Work, reorganized from the
government's prose bullets into trade buckets: demolition, framing, drywall, painting, flooring,
cove base, ceiling, electrical, HVAC. It preserves the SOW's own quantities and specifications.
It adds essentially no information the government did not already write.

Its function is not to inform. It is to demonstrate that the offeror read and understood the
scope, in a form a construction evaluator recognizes immediately. It also lets the offeror
control the record of what it believes it is pricing.

**This section is roughly a third of the authored content in the winning technical volume, and
it is derivable from the solicitation alone.** That is the most encouraging finding in this
teardown for the product, and §6 treats it accordingly.

### 3.5 The exclusions block

The third section ends with a short list of scope the offeror excludes: sprinklers, asbestos
work, lead work. Three lines.

This is a commercial construction bidding convention, it allocates risk, and it is not neutral:
the Statement of Work elsewhere requires engineering analysis supporting the sprinkler needs of
the space. An exclusion is an exception taken to solicitation scope, which in a strict reading
is a responsiveness problem. It survived.

The rubric has no row for exceptions taken, exclusions, assumptions, or qualified offers. In
construction and in any fixed-price build, that is a standard and consequential element. It is
also pure judgment: what to exclude is a pricing and risk decision no pipeline can make.

### 3.6 Past performance was discharged by orchestration, not writing

Factor 2, with a six-page allowance, is one sentence stating that past performance
questionnaires were sent directly to the contracting office.

That is it. No references restated, no contract numbers, no CPARS identification by contract
number, no entity identifiers for the offeror or team members, all of which the instructions
require in this factor.

The work of Factor 2 happened outside the document: pick three reference POCs, get them the
questionnaire form, and get them to submit it to the contracting officer before close. Inside a
six-day window. That is relationship management under time pressure, and it is a workflow with
a deadline, not a document.

**The rubric assumes past performance is content the offeror writes. In this pursuit it was
content third parties submitted, and the offeror's job was to make that happen on time.** The
factory produces documents. It has no concept of an obligation that is due somewhere other than
the proposal email. That is a gap with real customer value, because missing it is fatal and
noticing it is trivial.

---

## 4. Volume II is the headline

**The winning price volume contains no pricing narrative, no cost breakdown, no basis of
estimate, no labor categories, no rates, no hours, no material takeoff, no subcontractor quotes,
no overhead and no fee line. It contains one dollar figure, stated twice, and four forms.**

Contents in order:

1. Cover page, duplicating Volume I's cover.
2. The signed SF1442, with the lump sum in the offer block.
3. The CLIN schedule, single line item, unit of measure "job," the same lump sum again.
4. Five pages of copied FAR annual representations and certifications provision text, blank.
5. The executed SF24 bid bond, scanned, wet-signed by two corporate officers. These scan pages
   are why the file is by far the largest of the three.
6. The subcontracting-limitation certification, one page.

Forty pages were allowed for the price factor. About one was used, and the used page is a form.

### 4.1 What this does to the rubric's pricing section

`PROPOSAL-RUBRIC.md` §4 is the most detailed section in the rubric and it is built on the VA
Source Selection Guide's cost-analysis element list: direct labor dollars, direct material,
indirect costs, other direct costs, facilities capital cost of money, profit and fee, with a
basis and assumptions for each priced line, reconciled against staffing hours in another volume.

Against this winner:

- The line-item breakdown row is **falsified**. Not "thin," not "partially met." There are no
  lines to break out. The solicitation asked for a price for one CLIN and the winner gave one
  price for one CLIN.
- The basis and assumptions row is **ignored**. None supplied, none requested.
- The cross-volume reconciliation row is **unreachable**. No hours exist in the submission.
- The unbalanced pricing row is **structurally impossible**. Unbalanced pricing is a comparison
  among line items. With one line item there is nothing to compare. The solicitation reserves
  the right to check for it anyway, which is boilerplate the drafter did not prune.
- Price realism and price analysis remain live but they are evaluator-side activities against
  the independent government estimate and the competing offers. Nothing the offeror writes
  affects them, because the offeror writes nothing.

Roughly three of the four rows in the rubric's headline pricing table do not apply to a
single-CLIN fixed-price construction buy, which is the dominant shape at this dollar band in a
NAICS we target.

### 4.2 What Volume II actually demands, and why it matters commercially

Reframe it. Volume II is not a pricing document. It is a **forms and instruments package** with
a number in it. Its real requirements are:

| Element | Nature | Can the factory supply it |
|---|---|---|
| SF1442 blocks 14 through 20c, completed and signed | Form fill from firm identity + the offered number | Blocks yes, number no, signature no |
| CLIN schedule with the lump sum | Form fill | Same |
| Amendment acknowledgment | Requires knowing what amendments exist | **Yes, and this is a stated non-responsiveness trigger the winner left blank** |
| Representations and certifications as posted in SAM | Firm's administrative state, exportable from SAM | Retrievable given the firm's identifier |
| Executed SF24 bid guarantee at ten percent, plus courier of the original within five business days | Surety relationship and a hard external deadline | **No. This is the gate.** |
| Subcontracting-limitation certification with a self-performance percentage on the correct line | Firm's commercial plan, on a form whose applicable line is determined by the NAICS | Line selection yes, percentage no |
| The price | Estimating | No |

Three things are the whole ballgame: the bond, the number, and the three references filing on
time. Everything else in Volume II is form assembly against a known template, and form assembly
is exactly what a pipeline is good at and exactly what the current pipeline does not do.

### 4.3 The specific, actionable form of this finding

Do not read §4 as "pricing is impossible, drop it." Read it as:

> The winning price volume was 93% forms and 7% a number we cannot supply. We currently build
> 0% of the forms and 0% of the number. We should build the forms.

That is a bounded, mechanical engineering task with a clear definition of done, and it takes the
deliverable from "an outline of a volume" to "the volume, minus the number, minus the bond,
minus the signature." It also directly contradicts the premise in `sop/PLAN-V5.md` line 52 that
a price volume is out of reach because it needs rates and an approach. This one needed neither.

---

## 5. Rubric test, row by row

Verdicts: **CONFIRMED** (the winner did it), **IGNORED** (the winner did not do it and won
anyway), **UNREACHABLE** (the pursuit shape makes the row inapplicable), **NOT ANTICIPATED**
(the winner did something the rubric has no row for).

### 5.1 Cross-cutting rules, §0

| Rubric row | Verdict | Evidence |
|---|---|---|
| §0.1 L/M compliance matrix is the spine; order mirrors Section M | **UNREACHABLE + IGNORED** | No Section L or M exists in an SF1442 construction solicitation. No compliance matrix was submitted. Factor order was mirrored for the two real factors. |
| §0.2 Register: compliance-anchored, not marketing | **CONFIRMED, strongly** | Zero superlatives, zero capability marketing, zero competitor reference across 22 pages. The prose is flatly declarative scope description. This row is the rubric's cleanest win. |
| §0.3 Precision of statement as protest defense | **IGNORED** | Stale header from a different solicitation on both volumes, blank amendment block, certification on the wrong line, blank reps and certs. Awarded regardless. |
| §0.4 SDVOSB/VetCert assertions must track current regime | **UNREACHABLE** | Plain small business set-aside. No socioeconomic claim was made or needed. Row is over-specialized to one certification. |
| §0.5 Executive summary is not separately scored | **CONFIRMED** | None present, none requested. |
| §0.6 Pink-equivalent and Red-equivalent review checkpoints | **IGNORED** | A six-day window and a six-page authored volume. Evidence says no independent review occurred, since the stale header would not have survived one. |

### 5.2 Technical volume, §1

| Rubric row | Verdict | Evidence |
|---|---|---|
| Technical approach addressing the SOW point by point | **CONFIRMED, unexpected form** | Done as a trade-bucket scope echo, unrequested, roughly a third of authored content. |
| Solution architecture, tools, processes | **IGNORED** | Absent. |
| Risk identification and mitigation tied to this contract | **IGNORED** | No risk section of any kind. The rubric names a generic risk section as a disqualifier; the winner had none at all. |
| Every enumerated instruction answered in its assigned section | **IGNORED** | Six enumerated instructions unanswered, plus four missing required data fields. See §3.2. |
| Personnel qualifications and facilities | **UNREACHABLE** | Not requested. No named personnel appear anywhere in either volume. |
| Strength = exceeds requirement advantageously | **NO EVIDENCE** | Nothing in the volume is written to generate a strength. |
| Adjectival scale Outstanding to Unacceptable | **UNREACHABLE** | The solicitation states no adjectival scale. It states a tradeoff and a relevancy ladder. The rubric imported this apparatus from one agency's guide and it is not universal. |
| Risk rating Low/Moderate/High | **UNREACHABLE** | Not in the solicitation. |
| Deficiency renders proposal not awardable | **FALSIFIED** | Six unaddressed mandatory instructions, awarded. |
| Non-responsive sections ignoring the RFP's own language | **CONFIRMED, inversely** | The winner's strongest section works precisely because it mirrors the government's own language and quantities closely. |
| Exceeding page limits | **CONFIRMED as a real gate, wrong direction** | The observed failure mode is drastic underuse, not overrun. |
| Missing signatures/certifications the volume requires | **CONFIRMED** | This is one of the two things the winner was careful about. |

### 5.3 Management volume, §2

Every row is **UNREACHABLE**. There was no management volume, none was requested, and the
concepts do not appear: no org chart, no key personnel, no resumes, no clearances, no staffing
plan, no hours, no PM methodology, no QA/QC narrative, no subcontracting plan beyond the
one-page certification.

The rubric's four-volume model, and the starter's `VOLUMES` tuple that hard-codes Technical,
Management, Past Performance and Pricing, is a services and UCF assumption. Construction at this
band is two volumes. The starter currently emits an empty Management section with a placeholder
asking the client to confirm no management content is required, which is the deliverable
apologizing for a structure it should not have imposed.

### 5.4 Past performance, §3

| Rubric row | Verdict | Evidence |
|---|---|---|
| Per-project full field set, every field present and provenance-cited | **IGNORED** | No contract numbers at all, no prime or sub role, completion month rather than period of performance, two of three missing addresses. Both the rubric and the solicitation demanded contract numbers. The winner supplied none. |
| Recency and relevance stated explicitly against this solicitation | **IGNORED, and replaced by something better** | Not one relevance sentence. Relevance was established by which three projects were chosen. See §3.3. |
| Certification status current | **UNREACHABLE** | No certification claim. |
| Explicit acknowledgment when history is thin | **UNREACHABLE** | History was not thin. |
| Relevancy on a four-level scale keyed to scope, magnitude, complexity | **CONFIRMED** | The solicitation publishes exactly this ladder with dollar thresholds, independently of the VA guide the rubric cites. This is the rubric's second cleanest win, and it is now confirmed from a primary solicitation rather than a secondary guide. |
| Performance confidence on a separate five-level scale | **NOT PRESENT** | The solicitation states no confidence scale. |
| Evaluators pull from CPARS and direct reference contact | **CONFIRMED** | The solicitation says in terms that the CO will pull CPARS directly and may follow up with references. The winner relied on this entirely. |
| Claiming completed on an ongoing project | **CONFIRMED as a real risk** | All three were stated complete with a month. Unverifiable from the document, exactly the reason the row exists. |
| Missing contract number | **IGNORED and survived** | See above. |

### 5.5 Pricing, §4

Covered in full at §4 above. Summary: line-item breakdown **falsified**, basis and assumptions
**ignored**, cross-volume reconciliation **unreachable**, unbalanced pricing **structurally
impossible**, price analysis and realism **evaluator-side and unaffected by offeror content**.

### 5.6 What the rubric never anticipated

Ranked by how much it would have cost to miss.

1. **The bid guarantee.** A surety-executed bond at ten percent, scanned in, original couriered
   within five business days. No bonding line means no bid. The rubric does not mention bonding
   anywhere. This is the highest-consequence omission in the entire rubric.
2. **Out-of-band obligations with their own deadlines.** The reference questionnaires had to
   reach the contracting officer, from third parties, before close. The bond original had to be
   couriered post-close. Neither is content in the proposal. Both are fatal if missed.
3. **Amendment acknowledgment** as a named non-responsiveness trigger, with a specific form
   block to fill. (On this particular solicitation no amendments were issued, confirmed against
   SAM.gov; the rubric gap stands because the trigger is stated and generally applies.)
4. **The subcontracting-limitation certification**, a numeric self-certification whose
   applicable line is determined by the NAICS, with a statutory self-performance floor.
5. **Exceptions taken, exclusions, and qualified offers.** Standard in construction, consequential,
   and absent from the rubric.
6. **The mandatory pre-award site visit.** The Statement of Work directs field verification at
   the pre-award site visit in five separate places. Pricing the work without attending is
   guesswork. It is a physical act on a fixed date.
7. **Solicitation self-contradiction.** This solicitation misnumbers a factor when describing
   which volume carries it, and names the contracting officer two different ways. A bidder must
   decide whether to raise a question or absorb the ambiguity, against a question cutoff two days
   before close.
8. **Response windows measured in days, not weeks.** The rubric's review model presumes time
   that does not exist here.
9. **Non-UCF solicitation formats generally.** See §2.1.

---

## 6. Content classification: what we could generate, and what only the company has

This is the crux, so it is answered at the level of specific document elements rather than in
the abstract.

### 6.1 Bucket A: derivable from public sources today

Everything here comes from the solicitation PDF, which is public on SAM.gov, or from public
award data.

- The full inventory of enumerated instructions per factor, including the six the winner missed.
- Page limits per factor, and what each limit excludes.
- The evaluation factor structure, relative weighting language, and the tradeoff statement.
- The recency, relevancy and similarity definitions with their dollar thresholds.
- The complete forms and instruments checklist: which standard forms, which blocks, which
  certifications, which attachments.
- Submission mechanics: close date and time and time zone, destination address, permitted file
  format, per-file size cap, prohibited filename characters, required email subject convention,
  required title-page elements, the required statement of agreement with terms and where it goes.
- The bond mechanics: percentage, form number, scan-into-volume requirement, courier deadline,
  physical mailing address, envelope marking requirements.
- Out-of-band deadlines: question cutoff, reference questionnaire deadline, bond original
  deadline, site visit timing.
- **The trade-bucket scope echo.** The winner's third section is a reorganization of the
  government's own Statement of Work. An LLM can produce it from the solicitation alone, and it
  was roughly a third of the authored technical content.
- The SOW's own stated quantities, which the government helpfully enumerates: linear feet of
  wall, square feet of flooring and carpet, counts of door frames, one window opening with
  dimensions, a wall patch with dimensions, ceiling grid module, fixture type.
- Solicitation defects: the factor misnumbering and the inconsistent POC naming are mechanically
  detectable and become the RFI questions.
- Applicable wage determination, from public sources, given place of performance and
  construction type.
- Candidate past-performance projects from federal award data, **with a caveat**: only one of the
  winner's three references would have surfaced cleanly. One was a subcontract under a private
  general contractor and appears in no federal award database. Public award data finds a subset
  of a firm's real experience, and the subset is smaller than we have been assuming.

### 6.2 Bucket B: derivable with work we have not done

- A forms-fill engine: SF1442 blocks, CLIN schedule, subcontracting certification with correct
  line selection by NAICS, all populated from a client profile plus the number the client
  supplies.
- Instruction-level completeness auditing: enumerate every imperative in every factor's
  instruction block and mark answered or unanswered. The current router classifies requirement
  sentences into volumes by keyword; it does not enumerate obligations or check them off.
- A quantity schedule extracted from the SOW's stated dimensions, handed to the client's
  estimator as an input. This assists the price without pretending to set it.
- Reference-selection ranking: score the firm's job list against the solicitation's own
  relevancy ladder and recommend which three to submit. This is the technique that won, and the
  scoring is computable once the firm supplies its job list.
- An out-of-band obligations tracker as a first-class object with dates and owners.
- SAM representations and certifications retrieval for the firm, to produce the printout the
  instructions ask for rather than the blank provision text the winner submitted.
- Attachment-set completeness: the solicitation references a technical exhibit and a
  questionnaire form as attachments. Detecting referenced-but-absent attachments is a small
  extension of the existing fetcher.
- Non-UCF solicitation parsing generally, for SF1442 and Part 36 formats.

### 6.3 Bucket C: genuinely requires the company

- **Bonding capacity and the executed bond.** Not derivable, not substitutable, months of lead
  time to establish, and the hardest filter in the pursuit.
- **The price.** One number embedding subcontractor quotes, self-perform rates, current material
  cost, an after-hours premium because all work had to occur outside occupied hours, no on-site
  dumpster and no parking, shared freight elevator scheduling, and the firm's own risk appetite.
- **The exclusions decision.** What to scope out is a commercial risk judgment.
- **Reference relationships.** Three POCs filing a questionnaire with a contracting officer
  inside six days is relationship capital, not a workflow you can buy.
- **Non-federal and subcontract past performance facts**, which do not appear in public data.
- **The self-performance percentage** certified under penalty on the subcontracting form.
- **Site visit attendance and field verification.**
- **Corporate signatures** on the offer form and the bond.
- **Active SAM registration and current representations**, which is administrative state, not
  public research.

### 6.4 The honest answer

By page count, Buckets A and B together could produce most of what was submitted: the cover
pages, the table of contents, the scope echo, the forms shells, and the structural frame of the
reference write-ups. Call it a majority of the paper.

By decisiveness, Bucket C is close to all of it. The bond decided who could bid. The number
decided who won among those who could. The three questionnaires decided the past performance
factor. None of the three is touchable.

**So yes, the majority of what makes these proposals win is company-specific. That is a finding
about the offer, not a gap to code around, and §8 treats it as one.**

But there is a second finding that softens it, and it is the one worth acting on. The
company-specific content is *small and concentrated*: one number, one bond, three phone calls,
one percentage, one signature. The non-company-specific content is *large and tedious*: dozens
of enumerated instructions, a forms checklist, a mechanics checklist, page limits, deadlines
scattered across a 57-page PDF, a scope echo, a quantity list. The value of the product is not
that it writes the parts that win. It is that it removes the tedium around the parts that win,
in a six-day window, without missing the thing that renders you non-responsive.

---

## 7. Gap list, ranked by distance closed

Distance closed means: how much of the gap between what the factory ships today and what was
actually submitted does this change eliminate.

### Mechanical

| # | Change | Where | Distance closed | Note |
|---|---|---|---|---|
| 1 | **Submission-mechanics extractor.** Close date/time/zone, destination, file format, size cap, filename rules, subject line, title-page elements, agreement statement, bond courier deadline and address, question cutoff, site visit. Emit as a one-page checklist. | new stage, or `synthesize.py` | **Highest.** Every item is a stated non-responsiveness trigger, every item is extractable, we extract none. | Best ratio of value to effort in this list. |
| 2 | **Instruction-level enumerator replacing the keyword volume router.** Parse each factor's instruction block into individually numbered obligations; mark each answered or unanswered. | `package_rfp_response._route_volume`, `synthesize._extract_requirements_from_text` | **High.** Would have listed exactly the six the winner missed. This is the compliance-completeness claim we sell. | The router is a four-way keyword classifier today. It cannot enumerate. |
| 3 | **Two-volume SF1442 / Part 36 pipeline variant.** Stop hard-coding four volumes. Detect non-UCF construction solicitations and switch the volume model. | `package_rfp_response.VOLUMES`, `notice_fetch.compatible_deliverables` | **High.** 236220 is one of our own target codes and the current shape is wrong for it. | Includes deleting the empty Management section. |
| 4 | **Forms and instruments pack.** SF1442 blocks, CLIN schedule, subcontracting certification with NAICS-correct line, SAM reps and certs retrieval, amendment acknowledgment. | new stage | **High.** This is 93% of the winning price volume. | See §4.3. |
| 5 | **Out-of-band obligations tracker** as a first-class object with dates and owners: reference questionnaires, bond original, SAM currency, site visit. | new stage | **High relative to effort.** Missing one is fatal; noticing them is trivial. | The factory has no concept of a deadline that is not the proposal deadline. |
| 6 | **Solicitation-defect detector.** Internal contradictions, factor misnumbering, referenced-but-absent attachments, inconsistent POC naming. Output becomes the RFI question list. | `extract_attachments`, `synthesize` | **Medium-high.** Visible, credible, and clients cannot easily do it themselves under time pressure. | This solicitation had at least two detectable defects. |
| 7 | **Quantity schedule extractor** for construction SOWs, from the government's own stated dimensions. | new stage | **Medium.** Feeds the estimator without pretending to estimate. | The SOW hands you the takeoff. |
| 8 | **Scope-echo generator.** Reorganize the SOW into trade buckets. | `synthesize` | **Medium.** Roughly a third of the winner's authored technical content, fully derivable. | Must be labeled as a draft the client confirms, since it becomes the record of what they priced. |
| 9 | **Move the compliance matrix out of the deliverable and into the review note.** | `package_rfp_response._render_deliverable` §3 | **Medium.** Corrects a framing error, cheap to do. | No offeror at this band submits one. |
| 10 | **Bonding-requirement flag.** Detect a bid guarantee requirement and surface it as a go/no-go at triage, before any drafting work happens. | `triage` | **Medium, high leverage.** Cheapest possible qualification of a pursuit. | Saves the client and us from working a pursuit they cannot enter. |

### Requiring judgment we cannot automate

| Item | Why it resists automation |
|---|---|
| The price | Estimating. Subcontractor quotes, live material cost, after-hours premium, risk appetite. |
| Exclusions and exceptions taken | A commercial risk allocation decision with responsiveness consequences. |
| Whether to raise an RFI or absorb an ambiguity | Reads the contracting officer and the calendar. |
| How thin a narrative can be for the band | This winner bet correctly. The bet is not derivable from the document. |
| Reference relationship management | Human, time-boxed, and the actual Factor 2 work. |
| Bonding capacity | A financial relationship. |

### One row that should probably shrink rather than grow

The rubric's adjectival-rating and confidence-scale apparatus, imported from a single agency's
source selection guide, did not appear in this solicitation at all. Before building gates around
it, check how many of our target NAICS actually publish those scales. On this evidence the
answer may be "the large services buys do, and the buys our customers can win do not."

---

## 8. What this says about the offer

### 8.1 A starter is the right product, aimed at the wrong two-thirds

The current starter generates narrative scaffolding: volume headers, a routed compliance matrix,
and `[CLIENT PROVIDES]` prose placeholders. Against this pursuit, most of that scaffolding was
for volumes that do not exist or factors discharged in one sentence.

What a bidder actually needed in six days was a mechanics checklist, a forms pack, an
instruction-completeness audit, a defect list, and a quantity schedule. All of it is Bucket A or
B. None of it is prose.

So keep the starter. Retarget it from prose scaffolding to compliance mechanics and forms. That
is a change of aim, not a change of product, and it moves the deliverable from something the
client reads to something the client uses.

### 8.2 PLAN-V5 line 52 needs amending

That line says: not a technical or price volume, because those need people, rates, and an
approach we do not have.

The winning price volume needed no rates and no approach. The winning technical volume named no
people. The line is right that we cannot supply the number, the bond, or the references. It is
wrong that a technical or price volume is out of reach as an artifact.

Proposed honest restatement: *we can build the entire container and every page that is not the
number, the bond, the signature, and the references.* That is a defensible claim, it is
verifiable against a real winner, and it is a better sales sentence than the current disclaimer.

This should go through `skills/rubric-improve/` as an SOP edit, not a silent rewrite, per
`AGENTS.md` rule 5. It is flagged here, not made here.

### 8.3 Per-pursuit pricing

Two observations, one uncomfortable and one useful.

**Uncomfortable.** This was a sub-six-figure award. A per-pursuit fee at the current level is a
meaningful fraction of a percent of contract value, spent *before* knowing whether you win.
Contractors at this band bid many and win few. A per-pursuit fee has to survive a low hit rate,
which pushes it toward commodity pricing and pushes the deliverable toward something producible
in minutes. That is consistent with the twenty-minute founder review rule in PLAN-V5, but only
if the deliverable is the retargeted one in §8.1. A four-volume narrative starter does not fit
in twenty minutes of review. A mechanics-and-forms pack does, comfortably.

**Useful.** Look at what §6.1 actually contains. Nearly all of it is *solicitation*-derived, not
*firm*-derived. The instruction inventory, the mechanics checklist, the forms list, the page
limits, the deadlines, the defect list, the quantity schedule, the scope echo: every one of
those is **identical for every offeror bidding that solicitation**. Only the reference selection,
the identity fields, and the number vary by firm.

That is a one-to-many object wearing a one-to-one price tag. Per-pursuit-per-firm pricing forces
re-derivation of shared work for every buyer on the same notice, which is the worst possible
cost structure: the marginal cost of the second buyer is near zero and we currently charge as
though it were the first.

The natural shape suggested by this teardown is a **per-solicitation object** covering everything
in §6.1, plus a thin per-firm layer covering reference ranking and identity fill. That collides
head-on with the existing conflict decision in PLAN-V5 that two firms buying on the same notice
is an awkward edge case to be allowed, disclosed and firewalled. On this evidence it is not an
edge case. It is the natural product boundary, and the firewall concern applies only to the thin
per-firm layer, not to the solicitation-derived bulk.

That is a strategy question, not an engineering one, and it is flagged rather than decided.

### 8.4 The one thing that should change first

Rank order for the next two weeks, given all of the above: build the submission-mechanics
extractor (§7 item 1) and the bonding flag (§7 item 10). Together they are small, they are
purely mechanical, they address the two failure modes that actually kill a bid at this band
(missing a stated non-responsiveness trigger, and working a pursuit you cannot enter), and they
are demonstrable to a prospect in under a minute.

---

## 9. Scrub pass

An explicit scrub pass was run over every file written for this work: this report and
`PROPOSED-RUBRIC-DIFF.md`. Both were written under the constraint from the first keystroke
rather than sanitized afterward, so the pass was intended as verification. It was run as a
scripted check over both files, testing a list of literal identifiers taken from the source
documents plus structural patterns for emails, phone numbers, dollar amounts, and
entity-identifier and solicitation-number shapes.

**The scrub found and removed two real leaks, both in this file, both the same mistake.** The
file-ID map in §0.1 originally reproduced the three raw Drive filenames verbatim, and two of
those filenames embed the solicitation number. They now read `[SOL-NUM]` and `[PROJECT]`. The
map still does its job, which is to let Mike confirm which document each ID is.

Worth recording as a process note: the leak came in through *metadata*, not through analysis.
Every judgment call in the body was made cleanly. What slipped was a filename pasted for
traceability. That is the failure mode to watch for, and it is a direct argument for the
scripted pass rather than a careful reread.

`PROPOSED-RUBRIC-DIFF.md` was clean on the first pass. Both files contain zero em dashes, per
the house constraint.

Checked for and confirmed absent from both files:

- Company legal name, trade name, web domain, street address, city and postal code.
- Officer and employee names and titles, in any form.
- UEI, CAGE code, EIN, DUNS.
- The offered price, and the dollar value of any of the three reference projects.
- The solicitation number, the amendment identifier, and the internal requisition number.
- The agency name, sub-component name, building address, room and suite numbers.
- Contracting officer, site point of contact, and finance office names, emails and phone numbers.
- Reference point-of-contact names, employers, emails and phone numbers, for all three projects.
- The named subcontractor.
- Reference project names and titles, and the specific room identifiers within them.
- Contract numbers of any kind.
- Product manufacturer and specific product line named in the flooring specification.

Removed or never written during drafting, listed for completeness:

- All personally identifying fields above, which appear in the source documents and were held in
  working context only.
- Dollar figures. Where a dollar comparison carries analytical weight, it is expressed
  structurally instead, for example "the three references straddle the solicitation's own
  relevancy tiers, one above each of the top three" rather than the values.
- The stale solicitation number visible in both volumes' PDF headers. The *fact* of the stale
  header is a finding and is reported; the number is not.
- Verbatim passages. No quotation in this report exceeds a few words, and the source PDFs
  contain the offeror's copyrighted work product, so technique and structure are described
  rather than reproduced.

No source PDF was copied into the repository. The Drive file IDs in §0.1 are retained
deliberately, at Mike's explicit request, so he can confirm which documents were read. They are
access-controlled Drive identifiers for his own files, not identifying information about the
offeror.

One residual to flag rather than hide: §0.3 names the NAICS code and describes the pursuit type,
period of performance and set-aside status. That combination is public solicitation metadata and
is necessary for the analysis to be checkable. It does not identify the offeror, and without the
solicitation number it does not resolve to a specific award. If Mike wants that tightened
further, the NAICS is the only line that would need to go, and losing it would cost the report
its connection to our own target-code list.
