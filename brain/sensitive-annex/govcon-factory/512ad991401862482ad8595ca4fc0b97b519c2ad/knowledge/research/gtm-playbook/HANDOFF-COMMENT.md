# Handoff note for the code session

This research session had no `gh` binary and no GitHub token, so it could not post the coordination
comment itself. Paste the block below onto the relevant issue, then commit the new file. Nothing
else in the tree was touched.

**New, untracked:** `knowledge/research/gtm-playbook/REPORT.md` (plus this note).

---

```
GTM research pass complete (read-only). New file: knowledge/research/gtm-playbook/REPORT.md.
Not committed; this session had no gh/token. Please commit as-is or with a squash message like
"Add GTM playbook research (channels, pricing, close mechanics, 30/60/90, first-ten plan)".

What it adds that the repo did not already have:

1. FAR Subpart 3.4 / 52.203-5 primary text on contingent fees, with the practitioner reality
   (OST: "no one ever hears of proposal consultants who will agree to work for a success fee").
   Recommends a fourth objection block: "Can you do this on contingency?" No, and here is why.
2. A competitor's full live price ladder (Bidspeed marketplace, retrieved 2026-08-26):
   $125/$149 reports, $395 sources sought response, $595 bundle, $995 market research,
   $1,095-$2,995 advisory hour blocks. $699 sits between their response and their research package.
3. The reason fixed price is rare in this trade (consultants cannot estimate the effort) and why a
   gated factory can hold it. That is a positioning argument, not a discount.
4. Sales-cycle finding: sub-$5K B2B deals close in 7-21 days on one signature, and our notice window
   is shorter than that. No discovery call fits. Prepay after preview, never before.
5. Reputation risk the repo had not named: the SAM-registration scam ecosystem (GSA and BBB sources)
   means an unsolicited prebuilt artifact shares surface features with fraud at first read. Shapes
   touch 1 and is listed as one of the three highest-risk assumptions.
6. Retention: retainers fit capture, not proposal work (OST). Confirms MARKETING.md Door 9's
   event-billed code watch over a monthly subscription, with SMB churn benchmarks for the reason.

Two repo actions it flags, neither taken here:

- CORRECTION: research/growth-plan/REPORT.md section 4 says "NVSBE is gone." It is not. VA OSDBU
  lists NVSBE for Dec 8-9, 2026 in Cleveland (https://www.va.gov/osdbu/nvsbe/). sop/MARKETING.md
  Door 7 is the correct version. Suggest fixing the growth-plan line when that file is next touched.
- The counsel question on contractor-contact source/field/outreach use (TASK-0014 extension per the
  terra memo) is the day-1 gate in the 30/60/90. Nine of the ten first-customer slots depend on it
  directly or through referrals seeded by outbound.

Naming note: the commissioning brief used "submission-ready-starter proposal packages."
brand/offer.md retires "submission-ready" as a claim, so the report uses the repo vocabulary
(free industry report, $699 opportunity packet, code watch).

--- PART II ADDED 2026-08-26 (recurring revenue, ToS, wedge defensibility) ---

Same file, appended as Part II. Answers three sharpened questions from Mike.

7. DATA TERMS, with verbatim text pulled from sam.gov/about/terms-of-use. The redistribution
   question is now answered rather than open. Operative sentences: "If you want to share data
   publicly, only share data from public versions of APIs" and "You must use the public version of
   any API if you wish to display or disseminate the public-facing data." The terms route
   dissemination, they do not forbid it. The real restriction is the D&B carve-out, whose prohibited
   use is worded as "identifying, quantifying, segmenting and/or analyzing customers and prospective
   customers," which is prospecting, not publishing.
8. ACTIONABLE GATE: the D&B restriction is scoped to records with a last-updated/created/award date
   earlier than 4/4/2022, and those records carry D&B as the EVS Source field. Recommend a
   fail-closed gate on EVS Source + date before any entity record enters the matcher. Turns an open
   legal question into a mechanical filter with a log. Flagged for counsel because the "active
   registrations renew annually so they are all post-2022" step is my inference, not verified here.
9. THE FACT THAT SETTLES THE SUBSCRIPTION QUESTION: SAM.gov gives away saved-search email alerts
   for free with only a Login.gov account (GSA's own PDF, cited). A notification subscription is
   priced against zero and delivered by the authoritative source. Recurring revenue has to be sold
   on what happens after the notification.
10. THE WEDGE, HONESTLY: "notification plus an already-drafted response" is NOT a wedge. HigherGov's
    own docs describe a "one-click" Proposal Generator with a "Draft Sources Sought" option that
    uses the firm's public record and returns a draft in 3-5 minutes. GovTribe already sells
    saved-search alerts plus "scheduled or event-triggered GovTribe AI runs." Both halves exist at
    two vendors; combining them is a feature ticket. What survives: per-claim provenance with
    fail-closed gates, a named accountable human, and the refusal (fill floor, gaps page, "nothing
    to buy on this one"), each of which is off-model for an engagement-measured subscription.
11. REVENUE ARCHITECTURE: recommends per-deliverable core + free event-billed code watch, a capped
    standing capture retainer only after the first repeat buyer, and no data feed ever. Also
    recommends reframing the $249/mo consultant feed from "data feed" (ToS-exposed, competing with
    free alerts) to "gated qualified shortlist with a requirement map," or dropping it.
12. Adds a FOURTH high-risk assumption: that accountability is a purchase reason rather than a
    preference. The whole wedge now rests on buyers paying a premium over a $500/yr tool that
    one-click drafts a Sources Sought response.

Correction for anyone quoting GovTribe pricing: third-party blogs publish $1,350/$4,000/$1,800/$5,500.
GovTribe's own docs publish $1,500 Launch / $1,900 Launch Plus / $5,000 Growth / $6,000 Growth Plus,
plus credits at $0.09 PAYG. Use the vendor page.
```
