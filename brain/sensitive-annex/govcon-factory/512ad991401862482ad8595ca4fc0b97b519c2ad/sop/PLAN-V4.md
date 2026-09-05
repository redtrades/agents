# PLAN-V4 — integrated operating plan

**Superseded as the operating plan by `sop/PLAN-V5.md` (2026-08-23).** Kept as history. Do not implement from this file.

2026-08-22. Superseded PLAN-V3 as the operating plan; PLAN-V3 stays in place — its §1–§6 decisions (crux/positioning, product ladder, buyer, wedge, pricing rule, data & pipeline stack) and §9 risks **stand unchanged and are incorporated by reference**. V4 folds in everything decided after V3 was written: repo governance, the growth system (`research/growth-plan/REPORT.md`), delegated review, the outreach ramp, model routing (`research/local-model-eval/`), and the autonomy design principle. Decisions and sequencing only; rationale lives in the referenced reports.

**2026-08-22 revision** (feasibility red-team, `research/feasibility-review/REPORT.md`, applied via `rubric-improve`): §4 saturation restated on viable notices (PROPOSAL-0001), §4 sending-infrastructure gap closed (PROPOSAL-0006), §2 growth channels extended (PROPOSAL-0005, see `research/growth-plan/REPORT.md` addendum).

## 0. The discipline that outranks everything below

PLAN-V3 §8's 30-day kill-gates are unchanged and remain the most valuable thing in the plan. **Nothing in V4 — no growth channel, no delegation setup, no scaling work — delays the first 10 deadline-tied outreach emails or the HigherGov/VetBiz wedge kill-test.** Reply→paid conversion is still THE untested number; everything else in this plan is contingent on it. If the 30-day gates fail (0/10 twice on responses), V4's scaling sections are void and the reassessment is of thesis B itself, not of channel mix.

## 1. Governance — the repo is the company

- **Canonical record: `github.com/redtrades/govcon-factory` (private).** Every agent from any harness (Claude Code, Codex, Grok CLI, Hermes) reads/writes here; `AGENTS.md` is the entrypoint; the five operating rules there are binding. No business content goes to `~/agent-reports/` anymore.
- **Work moves through the task board** (`tasks/*.md` + generated `BOARD.md`): commit-based claims, evidence-mandatory completion, hook-enforced freshness. Growth channels are already tasked (TASK-0006–0010); new work gets a task file, not a side-thread.
- **The factory improves itself through `proposals/`**: any agent or Mike files against any part of the flow; `rubric-improve` processes; no agent accepts its own proposal. Review catches during `package-deliver` auto-generate proposals — every founder correction becomes a permanent fix candidate.
- **Three-tier mirrors, distinct jobs**: GitHub (canonical, agents), iCloud (offline file mirror, never edited), Google Drive (human-readable for Mike). Only GitHub is authoritative.

## 2. Growth system — the compounding layer around outbound

Full evidence and channel-by-channel verdicts: `research/growth-plan/REPORT.md`. The funnel:

```
LinkedIn (Mike) / SEO cornerstone / APEX-OSDBU / outreach email 3 / pSEO (later)
        → DIGEST subscriber → free MINI-SNAPSHOT → paid deliverable
        → ladder ($450 → $750 → $1,500) → Core subscription
```

**Start now (agent-time, not founder-time; none block the first 10 emails):**

1. **Digest as hub** (TASK-0007) — weekly, data-not-advice (new certifications × open notices per NAICS). Growth loops: mini-snapshot magnet, outreach email-3 opt-in, cross-promotion after 3–6 months of issues.
2. **Founder-led LinkedIn** (TASK-0008) — 2–3 posts/wk. Agents produce data + draft; Mike owns voice and the send (the rewrite is the authenticity; also keeps LinkedIn ToS-clean). Budget: 2–3 hrs/wk of Mike — the one real founder-time cost in this section.
3. **SEO cornerstone pages + mini-snapshot magnet** (TASK-0009, rides on TASK-0006 landing page) — 5–10 pages targeting the thin "sources sought response" SERP, plus one lead magnet: a free scoped-down section of the $750 Snapshot, pipeline-generated, gate-checked, batch-approved by Mike. Public pages carry the same provenance discipline as deliverables — a wrong number on a public page is a reputation gate failure.
4. **Community, low intensity** (TASK-0010) — APEX counselor intros (free assets only, never a pitch — counselors are structurally neutral), OSDBU/DAP event calendar, referral paragraph folded into the already-planned 5 consultant feed emails (their too-small leads have nowhere else to go).

**Trigger-gated (do not start early):**

| Deferred | Trigger |
|---|---|
| Programmatic SEO (per-NAICS / per-agency / recompete pages) | Daily ingest stable + wedge kill-test passed + cornerstone pages indexing cleanly |
| Paid ads (LinkedIn Document Ads first; Google never at current tickets) | Digest→paid conversion measured positive, or Core/feed is the advertised product |
| Conference booth ($1,750+) / referral tooling / notice-alert product | Revenue covers 3× / digest >1K subs / mini-snapshot demand proven |

Funnel working targets (external benchmark → ours; measure and replace within 90 days): digest page 10% visitor→sub · 15% sub→mini-snapshot in first 3 issues · 5–10% mini-snapshot→paid in 60 days · 25% repeat in 6 months (hypothesis). These are **working targets, not measurements** — the financial model v3 carries the same labels.

## 3. Delegated review — removing the founder ceiling

V3 priced everything against Mike's 5 review-hrs/wk. V4 replaces that ceiling with a delegation ladder:

- **Months 1–3: founder reviews everything.** This is the measurement period — stopwatch data (SOP §2.6), rubric extraction, gate hardening. Non-negotiable: the rubrics that make delegation safe come from these reviews.
- **From month 3–4: delegated reviewers take first-pass review** — contract reviewers (GovCon-literate, ~$40–60/hr) and/or agent reviewers as gate coverage matures. Preconditions: stopwatch data exists, gates mechanized for the deliverable class (G1-matrix + Snapshot gates, TASK-0004), and a written review rubric per deliverable type.
- **Founder drops to spot-checks** (~20% of units initially, declining with reviewer track record) **plus every catch files a proposal** — delegation runs through the same self-improvement loop as everything else.
- The **~$1,000/founder-review-hour governing rule** (V3 §5) survives as a margin rule: delegated review cost is a direct cost per unit; a deliverable class whose price can't cover reviewer cost + spot-check time at target margin gets repriced or cut, same as before.
- Rule 1 (nothing ships without Mike's explicit approval) **is not repealed by delegation** — it is satisfied per §5's earned-autonomy ladder: approval migrates from per-item to per-batch to standing-approval-per-class as gate history accumulates, and ship authority stays with Mike until a class has earned standing approval.

## 4. Outreach ramp — 15 → 50 → 100–200/wk

V3's 10–20/wk cap was a founder-review-capacity number, not a market number. With delegated review and gate maturity, the cap moves:

| Phase | Volume | Gate to advance |
|---|---|---|
| Validation (M1–3) | ~15/wk, every email notice-matched, Mike approves each send | 30-day kill-gates pass; reply + reply→paid measured |
| Scale-up (M3–6) | ~50/wk | Delegated review live; deliverability clean (bounce <2%, spam complaints ~0); reply rate holds ≥⅔ of validation level |
| Full ramp (M6+) | 100–200/wk | List precision holds at volume (reply-rate dilution monitored monthly); second sending domain warmed; NAICS set widened per `research/naics-selection/` if match supply thins |

Standing constraints: every email stays notice-matched (the match is the pitch — volume never buys generic spray), CAN-SPAM discipline from email one. Saturation *(revised 2026-08-22, PROPOSAL-0001)*: the certified-firm pool (~36,265 total, ~38.5K firm-code slots across the 6 target NAICS) is not the binding constraint — **viable Sources Sought notice supply is** (~250–400 sellable notice-moments/yr across the 6 codes, `sop/PLAN-V3.md` §3). Firm-side saturation is still a Year-2 monitoring item; notice-side saturation binds the Optimistic scenario much sooner and requires NAICS widening or multiple clients per notice (`sop/financial-model/SUMMARY.md` saturation caveat, PROPOSAL-0002). Expect reply rates to dilute as volume rises; the financial model carries this explicitly rather than assuming validation-level rates at full ramp.

**Sending infrastructure *(added 2026-08-22, PROPOSAL-0006):*** stack-selection §1 sized manual Gmail-on-primary-domain for the 10–20/wk world; this table's 100–200/wk ramp was never reconciled against it. At the **Scale-up (M3–6) trigger — 50/wk** — outreach moves to a **separate sending domain**, warmed from M1 in parallel (cheap, no reason to wait), using GMass or equivalent; the primary domain (which also sends deliverables, invoices, and the digest) never carries cold-email volume above validation level. Add the domain + tool cost line to the financial model. Measure bounce rate on the first DSBS-sourced batch (contact freshness is unmeasured); a >10% bounce rate triggers list-hygiene work before any ramp past validation.

## 5. Model routing & autonomy

- **Routing (validated 2026-08-22, `research/local-model-eval/`):** local Qwen (omlx) runs extraction, structuring, and agentic tool-calling stages — tool-calling passed grounded multi-turn tests (correct tool selection, well-formed calls). Frontier models handle final customer-facing prose and gate adjudication. Effect: LLM cost per deliverable trends toward the $1–2 floor and the pipeline's agentic middle runs at zero marginal API cost. Remaining eval stages (3–5, config headroom) finish opportunistically; routing decision does not block on them.
- **Autonomy design principle: the organization is built to run ≥95% autonomously**, with the human loop concentrated at exactly three points: send approval, deliverable review (→ spot-checks per §3), and calls. Autonomy is **earned, never assumed**: a pipeline stage or deliverable class graduates (per-item approval → batch approval → standing approval) only on accumulated gate history, and any gate failure or founder catch demotes it a rung. Fail-closed (rule 2) applies at every rung.

## 6. Sequencing

| Window | Critical path | Also running (agent-time) |
|---|---|---|
| **M1** | V3 §8 week-1/2 unchanged: SAM key, DSBS ingester, domain warm-up, first 10 emails, wedge kill-test, 5 feed emails | Landing page + cornerstone pages, digest scaffold, LinkedIn drafts, board/proposals live |
| **M2–3** | Deliver, stopwatch every review, ladder follow-ons; 30-day go/no-go | Digest weekly cadence, mini-snapshot magnet live, APEX intros, gate mechanization (TASK-0004) |
| **M3–4** | Delegated review onboarded (§3 preconditions); outreach → 50/wk | Reply-dilution monitoring; Core upsell to any 2–3-time buyer |
| **M6+** | Outreach → 100–200/wk as gates allow; pSEO if triggers met | Paid-ads decision only if digest→paid measured positive |
| **Y2** | Channel mix rebalance toward inbound as SEO compounds (month-6 indexing inflection) | Saturation monitoring; Capture Brief ($1,500–2,500 premium) revisited per `research/report-enhancements/` |

## 7. Economics

Financial model v3 (`sop/financial-model/sdvosb-financial-model-v3.xlsx` + `SUMMARY.md`) models this integrated plan: BASE and OPTIMISTIC only (v2 retains the conservative case), outbound per the §4 ramp with reply-rate dilution, inbound phased in per §2's working targets, delegated review as a direct cost, founder time at **$60/hr below the cash line** (revised from v2's $150–250/hr convention), revenue split by source (outbound / inbound / feed / subscription) so the channel mix is visible across 24 months. Working-target assumptions are labeled as such in the workbook — none of them are measurements until the funnel produces data.

*(Added 2026-08-22, PROPOSAL-0006/0009):* the model's Base reply-rate assumption (15%→8% across the ramp) sits well above typical cold-B2B single-digit rates; the ramp gates should be robust to a measured 4–5% rate. `sop/financial-model/SUMMARY.md` carries a pessimistic reply-rate note pending the workbook update (TASK-0012).
