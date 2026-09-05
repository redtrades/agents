# Pipeline vs winner: a live end-to-end replay

Status: uncommitted working note. Not SOP. Not approved.
Date: 2026-08-27.
Companions: `REPORT.md` (the teardown), `PROPOSED-RUBRIC-DIFF.md`, `ISSUE-DRAFT.md`.

We pulled the real solicitation from SAM.gov by its own identifier, ran
`python3 -m factory.runner` against it end to end, and diffed the output against the offer that
actually won. This is the first time the factory has been measured against a known-good outcome
rather than against its own gates.

**Result in one line: the pipeline passed 36 of 37 gate checks and produced a document that
could not be submitted, matched to a firm that was not eligible to bid.**

Same PII rules as `REPORT.md`. No proposal or solicitation PDFs entered the repo. Scrub pass at
§8.

---

## 1. Retrieval from SAM.gov

### 1.1 Which route worked

I had only the solicitation number from the SF1442 package. The pipeline's entry point
(`factory.notice_fetch.parse_notice_id`) requires a 32-character hex notice ID and rejects
anything else, so the first step was resolving one to the other. That is itself a finding: **a
user who has a solicitation number, which is what appears on every solicitation document, cannot
enter our pipeline.**

| Route | Result |
|---|---|
| `api.sam.gov/opportunities/v2/search` | **404.** Endpoint gone. |
| `sam.gov/api/prod/opps/v2/opportunities/search` | **401 UNAUTHORIZED.** Now requires a key. |
| `sam.gov/api/prod/opps/v1/search` | **404.** |
| `sam.gov/api/prod/sgs/v1/search/` | **200. This is the one that worked.** Keyless. Resolves a solicitation number to a notice ID. Requires `Accept: application/hal+json`; sending plain `application/json` returns 406. |
| `sam.gov/api/prod/opps/v2/opportunities/<id>` (notice detail, what `notice_fetch` uses) | **200 keyless on an archived notice.** |
| `sam.gov/api/prod/opps/v3/opportunities/<id>/resources` (attachment listing) | **200 keyless. All five attachments listed and downloadable.** |
| Daily CSV archive | Not needed. |

**Answer to "can our ingest reach historical solicitations at all": yes, fully.** The notice is
archived (`archived: true`, `isActive: false`, auto-archived 15 days after close) and both the
detail record and every attachment byte are still served without a key, two years after award.
Past awards are usable as ground truth, and we should be building a regression corpus from them.

Two caveats worth recording. The search endpoint we depend on to resolve a solicitation number
is undocumented, is the one the SAM.gov web UI calls, and is content-negotiation-fussy. The
documented public search API now wants a key. So the resolution path is real but fragile, and
the pipeline does not implement it at all today.

### 1.2 What the record contained

- Notice type `o` = Solicitation, NAICS 236220, set-aside code `SBA`
  (Total Small Business Set-Aside, FAR 19.5), a building alteration/repair PSC, place of
  performance DC.
- **`modifications.count: 0`.** No amendments were ever issued.
- Five attachments, 803 KB total: the 57-page solicitation, a past-performance questionnaire
  form, the subcontracting-limitations form, a Davis-Bacon wage determination, and the space
  drawings.
- The notice description body is **two sentences**. The entire scope, every instruction, every
  evaluation factor and every page limit lives in the attachments.

**This corrects `REPORT.md`.** The teardown flagged the winner's blank amendment-acknowledgment
block as a compliance defect. There were no amendments. The blank block was correct. That
correction is now recorded in `REPORT.md` §2.5 rather than silently removed, because it is a
clean example of a wrong inference from the proposal alone that only the authoritative source
could overturn. It is also the argument for doing this replay at all.

---

## 2. The run

```
python3 -m factory.runner --notice <32-hex-id> --deliverable rfp-response-starter
```

All eight stages executed. Nothing crashed. Nothing was fixed mid-run.

| Stage | Gate checks | Result |
|---|---|---|
| ingest | 3 | PASS |
| normalize | 5 | PASS |
| triage | 5 | PASS |
| match | 6 | PASS |
| extract_attachments | 4 | PASS. 5 of 5 attachments fetched, all marked valid, 20 requirements extracted |
| assemble | 6 | PASS |
| synthesize | 4 | PASS |
| package | 4 | **3 PASS, 1 FAIL** |
| **Total** | **37** | **36 pass, 1 fail** |

The single failure: `format`, on `deadline 2024-08-15: restated=True, future=False`. The pipeline
fail-closed because the response date is in the past. That is correct behaviour for a live run
and a pure artifact of replaying history. It is the only thing that stopped this artifact from
being marked deliverable.

Outputs produced before the halt: `package/DELIVERABLE.md` (126 lines, 17.7 KB) and
`package/DELIVERY-NOTE.md`, plus full stage envelopes and a trace.

---

## 3. Defects observed, recorded not fixed

Ordered by severity.

### 3.1 It matched an ineligible firm, and no gate noticed

The deliverable is headed "Prepared for" a **multi-billion-dollar national general contractor**,
one of the largest builders in the United States. The other top matches are the same: large
national and regional GCs, and a joint venture.

The solicitation is a **Total Small Business Set-Aside with a $45M size standard**. None of these
firms is remotely eligible.

The set-aside is not missing from our data. `normalize/notices.json` carries
`set_aside: "SBA"` and `set_aside_code: "SBA"`, correctly parsed. The match stage simply never
consults it. Grepping the codebase, **no size-standard or set-aside eligibility filter exists
anywhere in `factory/` or `domains/`**; a sibling stage records `size_standard: "N/A (needs SBA
size standards pull)"`, so the absence is known but unenforced.

This is the worst defect in the run. Everything downstream is personalized to a firm that
cannot bid, and the deliverable would have been emailed to them under the routing rules in
`AGENTS.md` ("List 3: awards match this notice, build packet, then email").

### 3.2 The single most important requirement came out as gibberish

REQ-002 as extracted and printed in the deliverable:

> "THE CONTRACTOR MUST FURNISH ANY REQUIRED PERFORMANCE AND PAYMENT 12b. CALENDAR DAYS"

The word **BONDS** was dropped. The SF1442's two-column form layout scrambled during PDF text
extraction, the noun was lost, and a form-field label was spliced in. The bid guarantee and
payment bond requirement, which `REPORT.md` identifies as the hardest gate in the entire pursuit
and the thing that decides who can bid at all, reached the customer as an unparseable fragment.
The volume router then saw the word "PAYMENT" and filed it under Pricing.

REQ-001 is scrambled the same way: "begin performance within 5 60 calendar days and complete it
within calendar days after receiving." Two form columns interleaved.

### 3.3 Extraction found 20 requirements in a 57-page solicitation

The Factor 1 instruction block alone contains roughly fourteen enumerated obligations. The
extractor captured the single top-level sentence ("provide a detailed summary for three (3)
projects...") and **none of the sub-bullets**: not sustainable design, not the safety record, not
local market conditions, not critical-material procurement, not utility coordination, not
closeout approach.

Those are exactly the six instructions the winner ignored. `REPORT.md` §7 item 2 proposed an
instruction-level enumerator and said it "would have listed exactly the six the winner missed."
**That claim is now measurably wrong about the current state:** today's extractor would have
listed none of them. The proposed change stands, but the distance to it is larger than the
teardown implied, and that correction belongs on the record.

Requirements are also truncated mid-sentence at roughly 130 characters, so several read as
fragments ("the Contractor shall have full use of the").

### 3.4 A silent extraction failure marked valid

The space drawings PDF yielded **47 characters** of text: a title and the note "For refernce
only." It is a vector or scanned drawing with no text layer and we have no OCR. It was marked
`valid: true` with `error: null`.

The construction drawings, which you cannot price a renovation without, disappeared without a
warning anywhere in the deliverable or the delivery note.

### 3.5 Four of five attachments were parsed and then discarded

| Attachment | Text extracted | Reached the deliverable |
|---|---|---|
| 57-page solicitation | 226,867 chars | Partially, as 20 truncated requirements |
| Davis-Bacon wage determination | 22,838 chars | **No.** Never mentioned |
| Past-performance questionnaire form | 2,511 chars | **No.** Never mentioned |
| Subcontracting-limitations form | 1,352 chars | **No.** Never mentioned |
| Space drawings | 47 chars (failed) | **No** |

The wage determination sets the mandatory labor rates that drive the price. The questionnaire is
the form the references must complete, which is how the winner discharged an entire evaluation
factor. The subcontracting form is a required Volume II submittal. All three were downloaded,
parsed successfully, and dropped on the floor. Attachment filenames are captured in
`attachments.json` and never rendered.

### 3.6 Volume routing is close to random

Fifteen of twenty requirements went to Technical, including three copies of the submission
deadline mechanics (not a volume), the past-performance instructions, and the Volume II
forms-and-certifications instruction. Past Performance received exactly one requirement. The
`Management` volume, which does not exist in this solicitation, received two, because the
keyword regex matched the word "schedule" in "submit a proposed schedule" and "update the panel
schedule" (an electrical panel).

### 3.7 The gaps section asks the client for things the document already states

Every one of the 20 requirements is dumped into "Gaps (you, 10 minutes)" under the heading
"require contractor-proprietary information." Including:

> "[REQ-012] Proposal due date is August 15, 2024 by 1:00 PM ET... [CLIENT PROVIDES: Provide
> specific verification or narrative for Proposal due date is August 15, 2024 by 1:00 PM ET...]"

We print the deadline, then ask the client to supply the deadline. The delivery note calls this
"Gaps Requiring Client Input (24 items)." A ten-minute promise against 24 items, most of which
are not gaps.

### 3.8 Wrong-deliverable boilerplate

The gaps table asks for "SDVOSB certification entrance/exit dates" and reports a count of
"SDVOSB set-aside actions this activity has awarded." This is a plain small-business set-aside
with no SDVOSB dimension. The magnitude gap says the value band is "not stated in the notice
text," but the solicitation attachment states a FAR 36.204(b) range explicitly; the magnitude
regex only ever ran against the two-sentence notice description, not the attachment text.

The compliance matrix section cites "the notice's actual Section L/M instructions" on a
solicitation that has no Section L and no Section M, as `REPORT.md` §2.1 predicted.

---

## 4. Structural diff against the winner

### 4.1 Artifact-level

| Bucket | Count | Items |
|---|---|---|
| **A. We produced it, the winner also had it** | **1 of 13** | A restatement of scope requirements, in fragmentary form. The winner's trade-scope section covered the same ground correctly and completely. |
| **B. The winner had it, we produced nothing** | **11 of 13** | Compliant title page (7 required elements); the FAR 52.215-1(c)(2)(iii) agreement statement; three selected reference projects; per-project scope narratives; the trade-bucket scope echo; the exclusions block; the completed offer form; the priced CLIN schedule; the SAM representations printout; the executed bid bond; the subcontracting certification. |
| **C. We produced it, the winner did not include it and did not need it** | **4 items** | A submitted compliance matrix; a Management volume; a Requirements Map table; a 24-item gaps table that largely restates the requirements map. |

### 4.2 Volume by volume

| | Winner | Our output |
|---|---|---|
| Volume I, Factor 1 (5 pp allowed) | ~4 pp: three projects, scope narratives, status, safety, values, POCs | A `[CLIENT PROVIDES]` placeholder |
| Volume I, Factor 2 (6 pp allowed) | 1 sentence, plus questionnaires filed out of band | A `[CLIENT PROVIDES]` placeholder; the questionnaire form we downloaded is never mentioned |
| Volume I, unrequested trade-scope section | ~2 pp | Nothing comparable; 20 truncated fragments |
| Volume II, price | 1 number, twice | A `[CLIENT PROVIDES]` placeholder |
| Volume II, forms and instruments | 13 pp, 4 instruments | **Zero.** No form is generated, referenced, or listed |
| Volume structure | 2 volumes, matching the solicitation | 4 volumes, one of which does not exist |
| Compliance matrix | Not submitted (correct) | Submitted as §3 |

### 4.3 Required submittal items present versus absent

Counting the discrete items the solicitation directs an offeror to submit:

| Category | Required | Present in our output | Absent |
|---|---|---|---|
| Volume I content items | 4 | 0 | 4 |
| Volume II forms and instruments | 6 | 0 | 6 |
| Title-page elements | 7 | 2 (solicitation number, title) | 5 |
| Out-of-band obligations | 4 | 0 | 4 |
| **Total** | **21** | **2** | **19** |

**Two of twenty-one.** And neither of the two is a form.

### 4.4 Page accounting

The winner submitted 22 pages, roughly 6 of them authored prose and 13 of them forms and
instruments. Our `DELIVERABLE.md` is 17.7 KB, which renders to roughly 6 to 7 pages, of which
essentially all is tabular restatement of the same 20 extracted strings. Those 20 strings appear
**three times** across our two files: once in the Requirements Map, once in the Compliance
Matrix, once in the Gaps table, and again in the delivery note. Deduplicated, the informational
content is under one page.

---

## 5. What a customer would actually have received

**Direct answer: a five-to-seven page markdown file, addressed to the wrong company, listing
twenty truncated fragments of the solicitation three times over, with a placeholder where each
of the four volumes should be, and no forms at all. To get from that to something submittable
they would have had to do essentially the entire job themselves.**

Concretely, the customer still has to:

1. Notice that the deliverable is addressed to a different firm, and that the firm named is not
   eligible for the set-aside they are bidding.
2. Read the 57-page solicitation themselves, because 20 truncated fragments is not the
   requirement set. In particular they must find the fourteen enumerated Factor 1 obligations we
   never extracted.
3. Discover the bid bond requirement on their own, because ours reads as a broken sentence with
   the word "bonds" missing, and arrange a surety-executed SF24 at ten percent.
4. Discover, download and complete the past-performance questionnaire, then get three references
   to file it with the contracting officer before close. We downloaded that form and never told
   them it exists.
5. Discover and complete the subcontracting-limitations certification, and work out which line
   applies to their NAICS. Same: downloaded, never surfaced.
6. Find the wage determination and price against it. Same.
7. Obtain the drawings in a usable form, since our extraction returned 47 characters.
8. Rebuild the volume structure from four to two, and delete the Management volume we invented.
9. Delete the compliance matrix before submitting, since submitting it would burn a five-page
   allowance.
10. Select three past-performance projects against the relevancy ladder, which is the technique
    that actually won and which we do not attempt.
11. Complete the offer form, the CLIN schedule, the title page's seven elements and the
    agreement statement.
12. Set the price.

Of those twelve, items 2, 3, 4, 5, 6, 8, 9 and 11 are things `REPORT.md` classifies as
derivable from public sources today or with work we have not done. **Eight of the twelve remaining
tasks are ours to do and we did none of them.** Only 3 (partly), 10 (partly) and 12 are genuinely
the customer's alone.

The honest summary: the deliverable saves the customer roughly the time it takes to skim a
solicitation's headline metadata, and costs them the time to read it, verify it, discard the
wrong parts, and notice what is missing. Net value against a six-day response window is at or
below zero.

---

## 6. Where our earlier claims break

### 6.1 The 42 of 42 gate pass

`CHANGELOG.md` records "Full fresh pipeline run, all 9 stages OK, `gate_final/GATE-REPORT.json`
**42/42 checks, all_green**." That run was the **Sources Sought packet** pipeline, which has nine
stages including a terminal `gate_final` stage running the SOP G1 to G5 `gate_runner`.

The RFP-response-starter pipeline has **eight** stages and **no `gate_final` stage at all**. Its
package stage runs four gates, and the delivery note explicitly records that the `value` and
`eligibility` gates are "not run on this deliverable."

So the 42 of 42 number does not transfer. It was earned on a different deliverable, a different
solicitation type, and a strictly larger gate set. Any external use of that number as evidence
about the RFP starter is unsupported.

### 6.2 This is a gate design failure, stated as such

**36 of 37 gate checks passed on an unsubmittable artifact matched to an ineligible firm. The
one failure was a date comparison. That is a gate design failure, not a tuning problem.**

The mechanism is visible in the code. `domains/govcon/gates.py::gate_compliance` is documented as
"Every requirement in requirements.json has a resolved pointer in DELIVERABLE.md," and it is
implemented as:

```python
for r in requirements:
    req_id = r.get("id", "")
    if req_id in deliv_text:   # substring check
```

It tests whether the literal string `REQ-001` appears in a file that the same stage wrote by
looping over the same requirements list. **It is tautological. It cannot fail unless the renderer
is broken.** It passed while routing fifteen of twenty requirements to the wrong volume, while
one of them was gibberish, and while a volume that does not exist was invented.

`gate_format` is the same shape: banners present, timezone restated, POC email echoed, deadline
restated. Every check is "did the renderer render." The only check that reaches outside the
document is `deadline is in the future,` and that is the only one that failed.

Generalizing across the whole registry: `schema`, `inputs_present`, `provenance`,
`count_recomputation`, `single_writer`, `freshness`, `compliance`, `format`. Every one is an
**internal-consistency** check. Not one is a **correspondence** check against the solicitation.

> Our gates verify that the artifact is internally consistent and honestly provenanced. They do
> not verify that it is correct. An artifact can be perfectly self-consistent, fully traceable,
> and completely wrong, and ours was.

The specific correspondence checks that would have caught this run, none of which exist:

| Check | Would have caught |
|---|---|
| Matched firm eligible for the notice's set-aside | §3.1, the ineligible match |
| Every attachment with extracted text is either used or explicitly declared unused | §3.5, four dropped attachments |
| Attachment text length plausible against file size and page count | §3.4, the silent drawings failure |
| Requirement text is a well-formed sentence, not a form-column splice | §3.2, the mangled bond requirement |
| Extracted requirement count plausible against source document length | §3.3, 20 requirements from 57 pages |
| Volume model matches the solicitation's own stated volume structure | §3.6, the invented Management volume |
| Gap items are actually absent from the source text | §3.7, asking the client for the deadline |
| Socioeconomic boilerplate matches the notice's actual set-aside | §3.8 |

### 6.3 A smaller correction

`REPORT.md` §7 item 2 claimed an instruction-level enumerator "would have listed exactly the six
the winner missed." The current extractor captures none of those six. The proposed change is
unaffected but the starting point is worse than stated. Corrected in place there.

---

## 7. What this changes about priorities

`REPORT.md` §7 ranked ten mechanical changes. This run reorders the top of that list and adds
one item that outranks everything.

| New rank | Change | Why this run moved it |
|---|---|---|
| **0 (new)** | **Set-aside and size-standard eligibility filter in `match`, plus an `eligibility` gate that runs on every deliverable** | We matched a national GC to a small-business set-aside and shipped it. This is a correctness bug with a customer-facing failure mode, and the data to fix it is already in `normalize/notices.json`. |
| **1 (new)** | **Correspondence gates**, per the table in §6.2 | Our entire gate layer cannot detect being wrong. Until it can, every other quality claim is unfounded. |
| 2 (was 4) | Forms and instruments pack | Zero of six required instruments produced. Largest single content gap. |
| 3 (new) | **Attachment-use accounting**: every parsed attachment either used or declared unused, with extraction-quality thresholds | Four attachments parsed and dropped; one failed silently and was marked valid. |
| 4 (was 2) | Instruction-level enumerator | Confirmed necessary and further away than thought. |
| 5 (was 1) | Submission-mechanics extractor | Still high value, unchanged. |
| 6 (new) | **Solicitation-number to notice-ID resolution** at the CLI | A user with a solicitation number cannot enter the pipeline. One endpoint call. |
| 7 (was 3) | Two-volume SF1442 variant | Confirmed by the invented Management volume. |

Everything below that keeps its previous order.

One further item, cheap and valuable: **build a regression corpus from archived awards.** SAM.gov
serves closed notices and their attachments keyless and indefinitely. We can assemble a set of
solicitations with known winners and run the pipeline against them on every change. This run took
under a minute of compute. There is no reason it should have been the first one.

---

## 8. Scrub pass

Scripted scrub run over this file together with the other three in this directory: a literal
identifier list taken from the source documents, plus patterns for emails, phone numbers, dollar
amounts, and entity-identifier and solicitation-number shapes. **Result: clean, zero hits, zero
em dashes.**

Specific decisions for this file, since a live API pull surfaces material the PDFs did not:

- **The notice ID and solicitation number are not written here.** They appear in this session's
  commands and in the run directory under `runs/teardown-diff-01/`, which is machine output, not
  an analysis artifact. The run directory is untracked and should not be committed; it contains
  the contracting officer's name and email in `data.json` and in the generated deliverable.
- **The contracting officer's name, email and phone**, which the SAM.gov record exposes and our
  own deliverable prints in full, are excluded here.
- **The agency and sub-agency names** returned by the organization hierarchy are excluded.
- **The matched firm is described but not named.** It is a public company and not the winning
  offeror, so this is not strictly required, but naming a real company as the subject of a
  pipeline error serves no analytical purpose.
- **The wage determination number, the PSC code, attachment resource IDs and the
  place-of-performance postal code** are excluded. The PSC code was caught by the scripted pass
  after I had already written that it was excluded, which is the second time in this work that
  the leak came through incidental metadata rather than through analysis.
- **Requirement text quoted in §3.2 and §3.7** is the pipeline's own mangled output, not the
  offeror's work product. It contains no identifying information and the exact wording is the
  evidence, so it is quoted directly.

Nothing was copied into the repo from either the Drive PDFs or the SAM.gov attachments. The
attachment bytes live only in the sandbox run directory and in `/tmp`.

**Checked, no action needed:** `runs/teardown-diff-01/` sits inside the repo tree and contains
the contracting officer's name, email and phone in `data.json` and in the generated deliverable,
but `runs/` is already listed in `.gitignore` (line 10), so it cannot be committed accidentally.
Worth deleting the directory once you have read it, but nothing is at risk.
