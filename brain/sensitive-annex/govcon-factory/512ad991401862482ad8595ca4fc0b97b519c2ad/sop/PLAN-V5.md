# PLAN-V5 — the factory

2026-08-23. This is the operating plan. It supersedes PLAN-V3 and PLAN-V4 as the description of **what we sell and how we go to market**. Citation rules, gates, and sample provenance in `SOP-DELIVERABLES.md` still apply to anything that leaves the building. V3/V4 stay in `sop/` as history.

Mike's words, compressed: *write reports on a market or a specific opportunity, do outreach (and other doors) so people can get those reports, and include a draft submission mapped to their public record.*

---

## Why the repo made this hard to see

A cold agent reading `AGENTS.md` yesterday learned the wrong company.

1. **The entrypoint named the wrong products.** It said the business *is* a $450 Sources Sought response and a $750 Market Snapshot, sold by cold email. That was one agent generation's packaging of an older crux, not Mike's idea.
2. **Four plans disagreed.** V2 was a $5k subscription. V3 flipped to a per-decision document factory. V4 added scaling, digest, SEO, LinkedIn, and a financial model that assumed 20–35% reply→paid. None of them opened with “we write the report, then we find the people who want it.”
3. **Sixteen skills encoded the wrong pipeline.** Lead-gen assumed “find a notice, match a firm, sell a response.” There was no first-class object for an *industry* report, a newsletter storefront, a UEI lookup, or a packet built *before* the customer replies.
4. **Samples taught the wrong default.** Five polished SS responses sit in `samples/`. Agents copy what they can see. The report-plus-draft packet was never the artifact on disk.
5. **Process outgrew the sentence.** Board, proposals, three workbooks, two feasibility reviews. All useful. None restated the founder's idea in one place. Later agents (including the one that wrote the first feasibility pass) optimized the documents that existed, not the business in Mike's head.

V5 exists so that does not happen again. If a document in this repo disagrees with this file on *what we sell* or *who we email*, this file wins. File a proposal to change this file. Do not silently revert to the $450/$750 two-SKU story.

---

## 1. What this is

An **agent factory** that turns public federal data into:

- **Industry reports** (a NAICS, a window of time). Shared. Usually free.
- **Opportunity packets** (one live notice). Personalized. This is what people pay for.
- **A storefront** (landing page + newsletter + UEI lookup) so people can come get them.

SDVOSB is the **first pond**, not the fence. Same factory, different filter, later.

Comparable is not HigherGov (a login) and not a four-figure consultant. Comparable is: *someone already did the homework on this market or this bid, cited every number, and mapped your awards into a draft.*

---

## 2. The two paid-adjacent objects

### Industry report (usually free)

What is going on in one NAICS (or one agency × NAICS) over the last 90 days: notice flow, award dollars, who wins, how contested, what is open now. Built once. Sold to nobody on day one. Used as the magnet, the newsletter section, and the shared spine inside packets.

### Opportunity packet (paid) — **$699**

For one live Sources Sought, RFI, or pre-RFP notice, for one firm, built **before they reply**:

1. The relevant slice of the industry report.
2. Every requirement in the notice, mapped to that firm's **public** awards (covered / partial / not in public record).
3. A submission draft in their legal name, filled only where public data exists.
4. A one-page gaps list: the N items only they can add.

Not a “winning proposal.” Winning proposals are not public. Not a technical/price volume. Those need people, rates, and an approach we do not have. If the notice is a long “how would you” questionnaire, sell the report + map only. Do not fake the draft.

**Customer input is not required to start.** SAM, SBS, and USASpending already have name, UEI, certs, POC, and awards. They review, fill gaps if they want, submit themselves. We never submit for them.

---

## 3. Who it is for

**Beachhead:** SBA-certified SDVOSBs whose *awards* (not just their SAM NAICS list) match the work.

Three lists. Only the last two are audiences.

| List | What it is | Use |
|---|---|---|
| 1 | Firms that *list* the NAICS | Do not email. Noise. |
| 2 | Firms that *won a federal award* in that NAICS in 36 months | Industry report / newsletter |
| 3 | Firms whose awards match *this notice* (scope, geo, vehicle, cert live) | Packet email |

“A couple thousand orgs in the code” is list 1. Treating it as a send list is how the domain dies.

**Later (same factory):** other small-business certs; primes who need real SDVOSB teammates (a second storefront: “who has actually done this”).

---

## 4. How it reaches people (many doors, one factory)

Full play: `sop/MARKETING.md`. The system, not a single trick:

```
LinkedIn / partners / public NAICS pages / communities
                    ↓
           LANDING PAGE
        (free report + UEI lookup + signup)
                    ↓
              NEWSLETTER
           (their codes only)
                    ↓
        they click a live notice
                    ↓
           PAID PACKET ($699)
                    ↓
            CODE WATCH
        (alert when the next one matches)
```

**Second on-ramp:** matched outbound on a live notice, packet already built. Skips the middle. Pays the bills while the hub warms up.

**Do not** merge newly-certified drip, consultant pitches, and deadline packets into one template.

---

## 5. The swarm

Full play: `sop/PLAYBOOK.md`. Three loops.

1. **Ingest** — notices, awards, certs, exclusions, forecasts. Fail closed if a source is down.
2. **Make** — industry report, per-firm map, draft, gaps. A second agent checks numbers against files, not against tone.
3. **Route** — score the firm onto list 1/2/3. Below cutoff: no email. Above: queue.

Human 5–10%: kill bad drafts, approve sends, take payment, rare gap-fill. Send is the **last** thing that goes autonomous, not the first.

Local models: tool-calling and lookups only (`research/local-model-eval/`). Frontier: extract, draft, adjudicate. PLAN-V4's “local does extraction” line is retired.

---

## 6. Data

Index: `sop/DATA.md`. Recipes stay in `recipes/`.

| Need | Source |
|---|---|
| Open notices + attachments | govconapi and/or SAM.gov API (S1/S2) |
| Award history, offers, mods | USASpending (S3/S6) |
| Certs, contacts, bonding flags | SBA SBS / DSBS (S4) — fragile; snapshot it |
| Exclusions, R/Q | SAM.gov (S5/S8) |
| Protests | GAO search (S7) |
| Forecasts | VA VetBiz + acquisition.gov (S9) |

No customer interview is an input to Make. Credentials never enter git.

---

## 7. Money

Model: `sop/financial-model/SUMMARY-v5.md` + `sdvosb-financial-model-v5.xlsx`.

Headline: packet **$699**. Industry report free. Newsletter free. Consultant feed **$249/mo** as a side test. No “Core subscription” line until that product is defined.

Unit rule still holds: if founder review on a packet will not fit in ~20 minutes, the packet is too big or the gates are too weak. Reprice or cut. Do not “add Core” to paper over it.

The number that decides viability is **matched-email → paid packet**. Everything else is a door into that.

---

## 8. Validation (first 30 days)

Week 1

- Domain + DNS (sending). One-page site: UEI box, one free NAICS report, newsletter signup.
- One live notice. Build packets for list-3 firms only. If that list is >40, the matcher is wrong. Rebuild it.
- Kill-test: one packet vs a Sweetspot/SamSearch draft vs a HigherGov page. If Mike cannot say the difference in 30 seconds, rewrite the pitch.

Week 2–4

- Send the matched packet emails (Mike approves).
- Newsletter issue 1, only codes that already have a report.
- Five consultant feed emails (sample week).
- Two LinkedIn posts from factory numbers.
- Stopwatch every review.

Go / no-go

- **0 paid packets after two matched batches (and the packets were actually theirs):** the offer failed. Do not add Facebook ads. Change the packet or stop.
- **Any paid packet:** keep the factory, pour fuel on the site and newsletter.
- **Review >40 minutes with gates:** cut scope or raise price before adding volume.

---

## 9. Risks

1. Emailing list 1. Treat as an operational failure, not a growth tactic.
2. SBS contact use and SAM entity-data DUA — ask counsel once, covering outreach and any future feed.
3. CAN-SPAM on every commercial send.
4. Conflict: two firms buy a packet on the same notice. Default until Mike picks otherwise: **allow, disclose, firewall the drafts.** Task: `TASK-0013`.
5. Calling the draft a “winning proposal.” Don't.
6. SBS endpoint disappearing. Snapshot the universe; degrade, don't die (`recipes/sbs-search.md`).
7. Terms, E&O, prepaid $699 before the second paid order (`TASK-0014`).

---

## 10. What “done” looks like for an agent session

You can point at:

- This file for *what we are*.
- `sop/PLAYBOOK.md` for *how the swarm runs*.
- `sop/MARKETING.md` for *how it reaches people*.
- `sop/DATA.md` + `recipes/` for *where numbers come from*.
- `sop/SOP-DELIVERABLES.md` for *citation and gate rules*.
- `templates/` for *the files we fill*.

If you are about to invent a third paid SKU or a 16th skill, stop and read this file again.
