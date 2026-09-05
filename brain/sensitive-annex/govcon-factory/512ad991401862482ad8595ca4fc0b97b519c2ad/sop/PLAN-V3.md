# PLAN-V3 — SDVOSB capture deliverables factory

**Superseded as the operating plan by `sop/PLAN-V5.md` (2026-08-23).** Kept as history. Do not implement from this file.

Canonical copy as of 2026-08-22; the original at `~/agent-reports/sdvosb-business/PLAN-V3.md` is a pointer stub.

2026-08-22. Supersedes PLAN-V2. Decisions from the section-by-section review with Mike; every factual input traces to a verified session report (opportunity-scan/2026-08-22-report.md, govconapi-exploration/REPORT.md, software-factory/2026-08-20-report.md). Decisions only — rationale lives in the transcripts.

**2026-08-22 revision** (feasibility red-team, `research/feasibility-review/REPORT.md`, applied via `rubric-improve`): §3 universe re-derived from S4/naics-selection data (PROPOSAL-0001); §4 wedge restated against the 2026 AI-drafting competitor set (PROPOSAL-0003); §9 item 1 extended to cover outreach DUA scope (PROPOSAL-0006).

## 1. Crux & positioning

Buyers pay for coverage and time, never win-rate claims. The business is **B: a per-decision deliverables factory** — agent-produced, veteran-owned, human-verified capture documents for SDVOSBs. **C (data feed)** runs in parallel (pipeline produces it anyway). **A (subscriptions)** is deferred to an upsell after a firm has bought 2–3 deliverables. Comparable is a four-figure consultant, not a $2,500 platform login.

## 2. Product line — the ladder

Order decided: **Sources Sought response ($450)** leads → **Market Snapshot ($750)** follow-on → **Compliance red-team ($1,500+)** opportunistic → Core subscription upsell later. Protest memo deferred until an attorney channel exists. Feed at $3–6K/yr per licensee, parallel track. One pipeline, one buyer, four price points; each rung offers the next.

## 3. Buyer & market

- **Paid outbound → notice-matched firms**: certified SDVOSBs whose NAICS + past performance match a notice closing in 10–20 days. The match is the pitch.
- **Free digest drip → newly VetCert-certified firms** (fresh public list monthly, ~12-day processing).
- **BD-staffed firms** are the graduation target for the Core upsell, not a cold target.
- Flow check *(revised 2026-08-22, PROPOSAL-0001)*: firms are the wrong denominator — the binding supply is **viable Sources Sought notices**, not the certified-firm pool. Derived from `research/naics-selection/REPORT.md`: ~820 SS/yr raw flow across the 6 target NAICS (SAM daily CSV, trailing 12 mo), of which BATCH-NOTES evidence puts only ~30–50% past content disqualifiers → **~250–400 sellable notice-moments/yr**. The certified-firm side: 36,265 SDVOSB-certified firms total; ~38.5K firm-code slots across the 6 target NAICS (~27.4K across 5; firms overlap codes, dedup pending the DSBS ingester, TASK-0005) — this replaces the underived "4,000–8,000" figure, which appears nowhere derived and doesn't match the two other firm-count guesses that had accumulated in this repo (`research/stack-selection/REPORT.md` §9's stray "~1,500 firms," also corrected this revision). Supports 10–20 precise emails/week indefinitely on the firm side; the notice-supply ceiling is the one that actually binds revenue at scale — see `sop/financial-model/SUMMARY.md` saturation caveat.

## 4. Competition & wedge

Platforms (HigherGov $500–2,500; VetBiz $49–149) sell search. AI proposal SaaS (SamSearch, GovDash, Sweetspot, GovEagle) sells drafting tools with ungated output. Consultants start at four figures. Fiverr is $90–250 boilerplate. **Wedge *(revised 2026-08-22, PROPOSAL-0003)*: not "the only finished document under $500" — that claim is false the moment a prospect has run a SamSearch or Sweetspot trial (both now ship dedicated Sources Sought/RFI drafting workflows, `research/feasibility-review/REPORT.md` F3). The wedge that survives: *verified + accountable + zero-effort service* — every claim cited to an award ID with fail-closed gates (absent from every AI-drafting tool surveyed), a human who signs the work, no tool for the client to drive.** Standing kill-test before the wedge goes in customer-facing copy: HigherGov Standard and VetBiz output, **plus a SamSearch and/or Sweetspot trial output**, side-by-side against one real deliverable (TASK-0002, expanded this revision) — pass condition: the difference is articulable to a non-expert in 30 seconds. Standing competitive-watch: expect HigherGov/SamSearch to ship one-click response generation within a quarter; monitor quarterly via `outcome-track`; keep differentiation investment in the service wrapper (gates, review, SLA, DSBS enrichment), never in drafting speed.

## 5. Pricing & unit economics

Governing rule: **nothing ships under ~$1,000 per founder-review-hour.** Targets: response 10–15 min ($1,800–2,700/hr), Snapshot 20–30 min, red-team 45–90 min, feed zero. Two numbers to measure (not assume) in month one: actual review minutes with gates running (the ceiling — an engineering variable), and bid/no-bid decisions per firm per year (whether the ladder has repeat purchase). LLM cost is noise ($1–5/deliverable, less on local Qwen).

## 6. Data & pipeline

Stack (≤$39/mo, verified 08-22): govconapi Pro (discovery) + SAM.gov API free (historical walk-back, polling) + USASpending free (past performance) + SBA DSBS free (certified-firm universe + contacts — the fragile differentiator; VetCert has no API). Trap: filter `due_after=today`; `active_only` includes passed deadlines. Winning proposals unobtainable (FOIA Ex. 4) — original solicitation SOW is the template substitute; attachments download clean from SAM.

Factory: **reimplement SSSF's pattern natively** (gate(envelope, run) → GateReport, synchronous phases) on Claude Code/Hermes — do not run the SSSF dependency (frozen repo, pi-only, broken diff gate). Gates per deliverable: compliance (every notice requirement addressed), provenance (every claim carries an award/notice cite), format, freshness. Rubrics extracted from the first 2–3 real deliverables, then frozen into gates. Drafting: local Qwen for extraction/structuring, frontier model for final prose.

## 7. Sales & lead gen

Automated to the send button; Mike approves sends. Cold email from a dedicated warmed-up domain, 10–20/week max, every email built around a specific closing notice. Digest drip to newly certified firms, automated. LinkedIn manual only (ToS). Feed: five hand-written emails to named consultants with a sample week of Detect output.

## 8. Validation — 30 days, three gates

- **Week 1:** SAM key, DSBS ingester, sending-domain warm-up; first match batch; HigherGov/VetBiz side-by-side (run first — can kill the wedge cheapest).
- **Week 2:** 10 deadline-tied response emails + 5 consultant feed emails + digest list.
- **Weeks 3–4:** deliver, stopwatch every review, Snapshot follow-on to any buyer, red-team if a live proposal surfaces.

Go/no-go: 0/10 twice on responses = per-decision thesis fails, stop and reassess B. 0/5 on feed = shelve C. Review time >2× target with gates = reprice or cut scope.

## 9. Risks & compliance

1. SAM entity-data resale — ask GSA/counsel about DUA scope **before the feed sells** (days, cheap). *(Extended 2026-08-22, PROPOSAL-0006):* ask the same question about **marketing use of SBS/DSBS contact data** in the same conversation (marginal cost ~zero) — the outreach engine runs on scraped SBS contact emails from day one, and PLAN-V3 originally scoped this question to the feed only.
2. Practice-of-law — red-team/protest framed and disclaimed as research products; no legal conclusions.
3. CAN-SPAM — identity, physical address, opt-out in the template from email one.
4. govconapi vendor risk — SAM.gov API is the standing fallback for ingest.
5. API key single copy — `credentials/govconapi.env`; regenerate via sign-up form with same email; also store in password manager.

## Immediate next actions (greenlit)

1. SAM.gov API key + DSBS ingester + dedicated sending domain.
2. First lead batch: 10 firms matched to notices closing in 10–20 days, outreach drafts for Mike's approval.
3. HigherGov/VetBiz comparison kill-test.
4. Native gate-contract implementation, scoped to the Sources Sought deliverable first.
