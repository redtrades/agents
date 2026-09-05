# Coordination issue draft: redtrades/govcon-factory

Not posted. The in-app browser is not signed in to GitHub and the repo is private; `gh` is not
available in this session's sandbox. Entering credentials is out of scope, so the body is staged
here instead.

**To post, from the repo root:**

```sh
gh issue create \
  --repo redtrades/govcon-factory \
  --title "Winning-proposal teardown: retarget the RFP starter from prose scaffolding to compliance mechanics and forms" \
  --body-file knowledge/research/winning-proposal-teardown/ISSUE-DRAFT.md \
  --label ready
```

That posts this whole file including these instructions. If you would rather post only the body,
everything below the horizontal rule is the issue.

This body has been through the same scripted PII scrub as `REPORT.md` and
`PROPOSED-RUBRIC-DIFF.md`.

---

## Context

First teardown of real winning proposals rather than research. One award: a two-volume offer
plus the solicitation that produced it. Full analysis in
`knowledge/research/winning-proposal-teardown/REPORT.md` (uncommitted). Proposed rubric changes
in `PROPOSED-RUBRIC-DIFF.md` in the same directory, as a proposal, not an edit.

Pursuit shape, abstracted: federal HQ interior office renovation, NAICS 236220 (one of our own
target codes), small business set-aside, firm fixed price, single CLIN, 60-day performance,
best-value tradeoff, award without discussions. **Six calendar day response window.** Mandatory
surety-executed bid guarantee.

Standing caveat: **n=1**. This is what one winner did, not what causes winning.

## Headline finding

**The winning price volume contains no pricing narrative.** No cost breakdown, no basis of
estimate, no labor categories, no rates, no hours, no material takeoff, no subcontractor quotes,
no overhead, no fee. Forty pages were allowed for the price factor. About one was used, and the
used page is a form.

The volume is: cover page, signed offer form with a lump sum, single-line CLIN schedule with the
same lump sum, five pages of copied blank FAR provision text, a scanned wet-signed surety bond,
and a one-page subcontracting certification.

**It is a forms and instruments package with a number in it, roughly 93% forms and 7% number.
We currently build 0% of the forms.**

This directly contradicts `sop/PLAN-V5.md` line 52, which says a technical or price volume is
out of reach because it needs people, rates, and an approach we do not have. The winning price
volume needed no rates and no approach. The winning technical volume named no people.

## Other findings that change what we build

1. **The solicitation has no Section L and no Section M.** FAR Part 36 construction uses SF1442
   with unlabeled free-text instruction blocks. `PROPOSAL-RUBRIC.md` §0.1 makes the L/M matrix
   the spine of everything, and `package_rfp_response` hard-codes four volumes. Both are wrong
   for a code we target.
2. **The winner left six enumerated instructions completely unanswered** (sustainable design,
   critical-material procurement, local market conditions, utility coordination, closeout
   approach, quantified safety record) plus contract numbers for all three references, and was
   awarded. Our rubric says any unaddressed mandatory requirement is not awardable. Re-scope it
   to risk, ranked, rather than a bright line.
3. **An entire six-page past-performance factor was discharged in one sentence** pointing at
   questionnaires that third-party references filed directly with the contracting officer. That
   is a workflow with a deadline, not a document. We have no concept of an obligation due
   somewhere other than the proposal email.
4. **Relevance was argued by selection, not by prose.** Zero relevance sentences. Three projects
   chosen to sit on the solicitation's own published relevancy tiers, same metro, same trade
   mix. This is computable and is the most transferable technique found.
5. **No compliance matrix was submitted.** We render ours as §3 of the delivered document. It
   belongs in the review note.
6. **The bid guarantee is the real filter** and the rubric never mentions bonding. Ten percent,
   surety-executed, scanned in, original couriered post-close, inside a six-day window.
7. **Sloppiness survived.** Both volumes carry a PDF header from a prior solicitation's
   document. Subcontracting certification on the wrong line. Blank provision text submitted in
   place of the offeror's own SAM representations. All under a stated rule that omissions render
   an offer non-responsive. (The blank amendment-acknowledgment block, flagged in an earlier
   draft, was **not** a defect: SAM.gov reports zero amendments.)

8. **We ran the real pipeline against this solicitation.** See `PIPELINE-VS-WINNER.md`. It
   fetched the notice and all five attachments keyless from an archived record, ran all eight
   stages, passed 36 of 37 gate checks, and produced an output that could not be submitted. The
   one failure was the response deadline being in the past. Every content gate passed. Details
   and the gate-design argument are in that file, and it is the stronger result.

## Content classification (the crux)

- **Bucket A, derivable today:** instruction inventory, page limits, evaluation structure,
  relevancy definitions, forms checklist, submission mechanics, bond mechanics, out-of-band
  deadlines, the trade-scope echo (about a third of the winner's authored technical content),
  the SOW's own stated quantities, solicitation defects.
- **Bucket B, needs work not done:** forms-fill engine, instruction-level completeness auditing,
  quantity schedule, reference-selection ranking, obligations tracker, SAM reps retrieval,
  non-UCF parsing.
- **Bucket C, only the company:** bonding capacity, the price, the exclusions decision,
  reference relationships, non-federal past performance, self-performance percentage, site
  visit, signatures, SAM currency.

**Honest answer: by decisiveness, Bucket C is close to all of it.** The bond decided who could
bid, the number decided who won, the three questionnaires decided the past performance factor.
None is touchable.

**The softening finding:** Bucket C is small and concentrated (one number, one bond, three phone
calls, one percentage, one signature). Bucket A/B is large and tedious (dozens of enumerated
instructions, deadlines scattered across a 57-page PDF, a forms checklist, a quantity list). Our
value is removing the tedium around the parts that win, in six days, without missing the thing
that makes you non-responsive.

## Proposed work, ranked by distance closed

Mechanical:

1. **Submission-mechanics extractor.** Close date/time/zone, destination, file format, size cap,
   filename rules, subject line, title-page elements, bond courier deadline and address,
   question cutoff, site visit. Best value-to-effort ratio in the list.
2. **Instruction-level enumerator** replacing the four-way keyword volume router. Would have
   listed exactly the six the winner missed. This is the compliance-completeness claim we sell.
3. **Two-volume SF1442 / Part 36 pipeline variant.** Stop hard-coding four volumes; delete the
   empty Management section.
4. **Forms and instruments pack.** Offer-form blocks, CLIN schedule, subcontracting
   certification with NAICS-correct line, SAM reps retrieval, amendment acknowledgment.
5. **Out-of-band obligations tracker** as a first-class object with dates and owners.
6. **Solicitation-defect detector**, output becomes the RFI question list.
7. **Quantity schedule extractor** for construction SOWs.
8. **Scope-echo generator.**
9. **Move the compliance matrix out of the deliverable** into the review note.
10. **Bonding-requirement flag at triage**, as go/no-go before any drafting.

Judgment, not automatable: the price, the exclusions, whether to RFI, how thin a narrative can
be, reference relationship management, bonding capacity.

**Suggested first two weeks: items 1 and 10.** Small, purely mechanical, they address the two
failure modes that actually kill a bid at this band, and both demo in under a minute.

## Offer questions raised, flagged not decided

1. **Amend `sop/PLAN-V5.md` line 52.** Proposed restatement: we can build the entire container
   and every page that is not the number, the bond, the signature, and the references. Route
   through `skills/rubric-improve/` per `AGENTS.md` rule 5.
2. **Per-pursuit pricing may be the wrong unit.** Nearly everything in Bucket A is
   *solicitation*-derived, identical for every offeror on that notice. Only reference selection,
   identity fill and the number vary by firm. That is a one-to-many object with a one-to-one
   price tag. A per-solicitation object plus a thin per-firm layer matches the cost structure
   better. This collides with the D-004 conflict decision (two firms, same notice: allow,
   disclose, firewall), which was framed as an awkward edge case. On this evidence it may be the
   natural product boundary.
3. **The 20-minute founder review rule survives only if the deliverable is retargeted.** A
   mechanics-and-forms pack reviews in well under 20 minutes. A four-volume narrative starter
   does not.

## What would settle the open questions

Next sample: one services buy and one construction buy above the simplified acquisition
threshold. That tests all four at once: whether completeness binds harder with a larger field,
whether our target codes actually publish the adjectival and confidence scales the rubric
imports, whether relevance-by-selection generalizes, and how often the priced volume is a forms
package rather than a breakdown.

## Handling note

Source documents are real proposals from a real company. They are not in this repo and must not
be. All three analysis files were written under PII constraint from the first keystroke and
verified by a scripted scrub (literal identifier list plus patterns for emails, phones, dollar
amounts, entity identifiers and solicitation numbers). The scrub caught two leaks, both raw
filenames containing the solicitation number, both removed. Detail in `REPORT.md` §9.
