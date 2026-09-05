# PLAYBOOK — how the swarm runs

2026-08-23. Companion to `sop/PLAN-V5.md`. An agent session that is *making* something starts here. Citation and fail-closed rules: `sop/SOP-DELIVERABLES.md`. Access patterns: `recipes/` via `sop/DATA.md`.

Human still approves every send and every paid file (AGENTS.md rule 1).

---

## Loops

```
INGEST  →  MAKE  →  ROUTE  →  (Mike) SEND / SHIP
                ↘ review agent checks files
```

Do not start MAKE without INGEST files on disk for that notice and firm. Do not ROUTE a firm you did not score. Do not SEND from a list-1 dump.

---

## Loop 1 — Ingest

**Done when:** `orders/<notice_id>/notice-raw/` has the notice JSON, attachment text, and `requirements.json`; `data/` has the award and cert pulls this MAKE will cite.

### Steps

1. Pull open notices. Filter `due_after=today`. Do not use `active_only` as the deadline filter (it keeps expired items). Recipe: `recipes/govconapi.md` or SAM fallback `recipes/sam-gov.md`.
2. Drop disqualifiers (read the description, not just the type): sole-source intent, MAC/vehicle-holders-only, product catalog, anticipated 8(a) when we are not serving that cert. Classifier notes live in `skills/notice-triage/SKILL.md`.
3. Download attachments. If a slot is nameless or zero-byte, treat as missing (superseded-attachment trap). Text-extract; if image-PDF, OCR; if empty, flag.
4. Write `requirements.json`: every numbered ask, quoted. Completion: each ask has an `id` and `text` copied from the source file, not paraphrased from memory.
5. For each candidate firm (see Route for how they got here), pull:
   - USASpending awards by UEI (`recipes/usaspending.md`) — paginate to `hasNext=false`.
   - SBS profile (`recipes/sbs-search.md`) — cert dates, small-under-NAICS, contact, bonding flags.
   - Exclusions by UEI (`recipes/sam-gov.md`).
6. Persist every pull as JSON in `data/`. A number that is not in a file does not exist.

**Industry-report ingest** (no single notice): last-90-day notices + awards for one NAICS. Same sources. Write to `reports/naics/<code>/data/`.

---

## Loop 2 — Make

Two artifacts. Shared spine, different cover.

### 2A. Industry report

Template: `templates/deliverables/industry-report.md`.

Must contain, all cited:

- NAICS, window, retrieval date
- Open-now count and trailing-90-day count
- Award dollars and top recipients (UEI + permalink)
- Competition roll-up: % competed, median offers, % single-offer
- What is open this week (table)
- One paragraph: what a firm in this code should actually watch

Must not contain: bid advice, pWin, CPARS, “you should bid.”

**Done when:** every count has pagination proof in `data/`; every dollar is a floored prefix of a source value; sample banner on if it has not been sold or approved as a public magnet.

### 2B. Opportunity packet

Template: `templates/deliverables/opportunity-packet.md`. Built **before** the firm replies. One packet per (notice, UEI).

Sections, in order:

1. Opportunity slice (from the notice + 2A).
2. Requirements map: each `requirements.json` row → their awards → Covered / Partial / Not in public record. Each Covered cell has a PIID and a USASpending permalink.
3. Submission draft in their SAM legal name, filled only on Covered rows. Identity, certs, POC, past performance come from files. Intent sentence is drafted as a default they can delete.
4. Gaps page: every Not-in-public-record row, one line each, written so they can fill it in 10 minutes.
5. Internal compliance matrix (not submitted).

**Refuse the draft (ship 1+2+4 only) when** more than half the asks are approach/price/people questions. Say so in the delivery note.

**Done when:** a review agent (different pass, preferably different model) has checked every dollar, PIID, date, and count against `data/` and `notice-raw/`. Tone review is Mike's. File review is the swarm's.

Local Qwen: lookups and tool picks only. Frontier: requirements JSON, draft prose, map adjudication.

---

## Loop 3 — Route

Score each firm for a notice. Default inputs: NAICS overlap, at least one relevant award in 36 months, cert active past the deadline, exclusions clean, not vehicle-blocked if the notice is vehicle-gated.

| Score band | List | Action |
|---|---|---|
| Listed the NAICS only | 1 | No email. Eligible for public page / newsletter if they opt in later. |
| Award in the NAICS, weak scope match | 2 | Industry report / newsletter. No packet email. |
| Scope + geo + vehicle + cert | 3 | Build packet. Queue matched email. |

**If list 3 for one notice exceeds 40 firms, the matcher is too loose.** Tighten scope (same activity, same work-type words, same state or obvious travel) and rescore. Do not send 40 “personalized” packets that are the same PDF.

Newly certified, no awards: list 2 at most. They get the free report and the newsletter, not a fake draft.

---

## Loop 4 — Send / ship (human gated)

1. Draft the matched email from `templates/outreach/email-packet.md`. The opener names **one real PIID**. If you cannot, the firm is not list 3.
2. CAN-SPAM footer on. Physical address on. Opt-out on.
3. Drop in Mike's approval queue. Never auto-send.
4. On paid: Stripe invoice, prepaid for first packet. Attach the packet PDF. Log the outcome in the pipeline log.
5. Add the buyer to the newsletter for that NAICS and offer code-watch.

Industry-report public magnets and newsletter issues also need Mike's approve-send. Batch-approve is fine. Silent publish is not.

---

## Daily / weekly cadence (once ingest is a job)

**Daily (agents)**

- Poll notices in the active NAICS set.
- Refresh list-3 queues for notices with 10–20 days left.
- Rebuild any packet whose notice changed (amendment / new attachment). G5 freshness: notice-tied data ≤5 days.

**Weekly (agents + one Mike block)**

- Compile newsletter from the same tables.
- Two LinkedIn drafts (data only). Mike rewrites and posts.
- One free-report refresh for the codes on the landing page.

**Monthly**

- Re-pull SBS universe snapshot (S4 canary). If the payload shape moved, stop Route and file a proposal.
- Recount viable notices. Update the saturation line in the financial assumptions if it moved a lot.

---

## Review agent checklist

Run as a separate pass. Output a GATE-REPORT, fail closed.

- Every `$` in the packet is a floored prefix of a value in `data/`.
- Every PIID exists in `data/` and the permalink resolves to that PIID.
- Every count either has pagination exhaustion recorded or is not claimed as complete.
- Cert exit date > notice deadline (or flagged).
- Exclusions pull exists and is clean, or the packet does not ship.
- Draft contains no CPARS, no price-to-win, no “winning proposal.”
- Gaps page lists every uncovered requirement.
- Sample banner present unless this is a paid, approved ship.

G1 (every notice ask pointed at a section) is still hand unless `gates/gate_runner.py` has been extended. Do not claim G1 ran if it did not.

---

## What not to build in a session

- A new skill directory for a step that is already a heading in this file.
- A full technical proposal volume.
- Auto-send.
- A “Core subscription” product.

If MAKE is blocked on a missing recipe, write the pull into `recipes/` and `sop/DATA.md`. Do not invent an endpoint.
