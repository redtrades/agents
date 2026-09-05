# VA/SDVOSB intelligence business — improved plan

2026-08-21. Built from the three source documents in iCloud (`va-sdvosb-business-plan.pdf`, `va-sdvosb-financial-model.xlsx`, `market-snapshot-template.pdf`) plus the fable proposal, corrected against independent research. Full sourcing in `claim-ledger.md`; a standalone critique of the fable proposal is in `fable-critique.md`. This document is deliberately not in agreement with the plan where the evidence doesn't support it — see Weaknesses at the end.

## The three open questions

**1. Review interface: GitHub PRs, or a simple web review page?**

**Recommendation: build the simple web page.** The proposal's stated reason to prefer PRs — free training-data capture — is a false tradeoff. Logging before/after edit deltas as training signal is a database decision, not a Git decision; a purpose-built page writes the same diff to Postgres a PR merge would. What PRs actually cost here is per-customer navigation overhead (finding this week's draft among N open PRs, every week, forever) on the exact step that gates how many customers one founder can serve — see Unit economics below. GitHub Mobile's file editor turns out to be more capable than a knee-jerk "phones can't do this" assumption would suggest (in-app Markdown editing since 2022, confirmed working), so mobile friction alone doesn't decide this — but once the training-data justification is removed, there's no remaining reason to route the business's core weekly bottleneck through a tool built for diff review instead of a single-purpose approval queue.

*What would change this:* if subscriber count stays permanently low (under ~15), PR navigation overhead never really bites, and GitHub Mobile's editor is fine as-is — don't over-build. Also reconsider if Mike specifically wants versioned briefings living in Git for reasons unrelated to this business (grep-able history, existing habits).

**2. Postgres host: Neon or Supabase?**

**Recommendation: Neon now, revisit at the month 8–10 gate.** The review tool has exactly one user — the founder — so Supabase's bundled multi-user auth doesn't buy anything yet; a single hardcoded admin check works identically on either host. Supabase's advantage (auth + storage + edge functions) becomes real when the customer-facing web portal ships (month 10–14 per the plan, or sooner if the recommended review page proves the model early). Both are Postgres, so a later Neon→Supabase migration is not a rewrite. Front-loading Supabase now adds unused surface area for no current benefit.

*What would change this:* if the customer-facing portal timeline moves up significantly (e.g., a Snapshot buyer explicitly asks for self-serve login in month 2–3), start on Supabase immediately to avoid the migration.

**3. Billing route: API pay-per-token, or a Claude Max subscription?**

**Settled, not open: pay-per-token API under the Commercial Terms of Service.** The proposal's premise — that Claude plans now include a separate Agent SDK credit pool that doesn't touch interactive limits — is false as of today: Anthropic announced this for June 15, 2026 and paused it the same day, per its own support documentation. Independent of that, Anthropic's Consumer Terms of Service bar automated, resale-adjacent use of subscription credentials outright, and enforcement of exactly this tightened in April 2026. Running a multi-customer nightly pipeline on a personal Pro/Max subscription's OAuth token is both currently non-functional as described and non-compliant. This also turns out not to matter for cost — see Unit economics: LLM spend is a rounding error either way, so there was never a real economic tradeoff here, just a compliance one. (The business plan document itself already specifies "Claude API with model orchestration" — this corrects the proposal's open question, not the underlying plan.)

*What would change this:* nothing foreseeable — the blocking issue is a Terms-of-Service resale prohibition, not a missing feature Anthropic might ship later.

---

## The business, restated

**What it is.** A subscription intelligence service that converts free, public federal procurement data (USASpending, SAM.gov opportunity notices) into a weekly, per-customer briefing for SDVOSB/VOSB contractors pursuing VA work: what's coming up for recompete in their lane, which incumbent is vulnerable and why, which VA offices actually buy what they sell. Agents produce the draft; the founder's edit is the product's actual scarce ingredient.

**Who it's for.** Owner or BD director at a certified SDVOSB/VOSB firm, $1M–$50M revenue, 2–4 priority NAICS codes, currently either paying $15K–$40K+/yr for GovWin IQ and getting more coverage than they need, or burning 5–15 hours/week manually watching SAM.gov and getting less than they need. This buyer segment is real and underserved specifically at the VA-only, SDVOSB-only depth this product promises — no major incumbent (GovWin, GovTribe, HigherGov, BGOV, GovSpend) builds a dedicated SDVOSB product line.

**Pricing.** $750 one-time Market Snapshot (lead magnet, converts to Core), $5,000/yr Core (the business), $8,500/yr Pro (multi-NAICS expansion). The $5,000 anchor still works against GovWin's $15K–$40K+ ceiling. It does **not** work in isolation against the newly-identified competitor below — see Weaknesses.

**The wedge.** Not "cheaper than GovWin." GovWin's own SDVOSB content is a free editorial report bolted onto a general tool — it has never built VA-specific, recompete-dated, incumbent-named analysis, and probably won't, because that depth doesn't scale to its enterprise-generalist customer base. The wedge is: analyst-depth intelligence (named incumbent, vulnerability signal, dated recompete window, buying-office concentration), priced for a $1–50M firm's actual budget, sourced with a citation on every claim.

**The moat, in order of durability.**
1. **The proprietary relevance dataset** — every edit, threshold tune, and customer "useful" vote, accumulated by NAICS and contract type. The public data is free; two years of filtered judgment about what actually matters is not. This is the one asset a funded competitor genuinely cannot buy or rebuild quickly.
2. **Provenance-first generation** (a source `award_id` on every claim) — a real accuracy guarantee, not just an engineering discipline, and one GovWin's analyst-written product structurally can't match with the same rigor.
3. **Owned audience** — the free digest list and LinkedIn following.
4. Niche trust and switching costs from a customer's configured watchlist.

**Path to first revenue.** Unchanged from the plan and still sound: ship Ingest+Detect in weeks 1–2 (proves the data pipeline works, costs nothing to validate), Synthesize + review loop in weeks 3–4 (first real briefing, sent manually — this is also when founder-review-time-per-customer should start being measured for real, not assumed), Distribution + Stripe in weeks 5–6. Cash break-even at 3 Core customers holds; the LLM cost floor is low enough that it was never really at risk (see below) — the real gate on this timeline is whether the review step's per-customer time comes in anywhere near what's assumed.

**What kills it, honestly:**
- **Review time doesn't scale the way the plan assumes** — this is the single biggest structural risk, detailed below.
- **A cheaper, already-live competitor exists at the exact customer segment**, undiscussed anywhere in the source documents — also detailed below.
- **SAM.gov's entity data has a real, unaddressed commercial-resale restriction** in its Terms of Use — a legal risk currently invisible to the plan, which treats SAM.gov and USASpending as interchangeably safe.
- Founder-single-point-of-failure remains real; the plan's own mitigation (runbooks, 30-day guarantee) is reasonable but doesn't change that this is fundamentally a solo-judgment business until proven otherwise.
- GovWin, or anyone else, launching a genuinely cheap VA-specific tier would compress the wedge fast — low-medium likelihood per the original plan, unchanged by this research.

---

## Unit economics — the numbers the plan doesn't state

**LLM cost per customer per week: not the bottleneck.** At current Anthropic API pricing (Haiku 4.5: $1/$5 per MTok in/out; Sonnet 5: $3/$15 per MTok standard, not the $2/$10 intro rate expiring 2026-08-31), a realistic weekly pipeline run per customer — Haiku classifying ~20–30 candidate events (~16K in / 3K out tokens) plus Sonnet drafting one cited briefing (~12K in / 4K out tokens) — costs roughly **$0.13/week, or ~$7/year**. Even at a generous 5x buffer for retries, richer context, and multiple draft passes, that's ~$35/year — still well under the financial model's own $60/yr marginal-cost assumption and far under the plan's $2/week ceiling. **Compute was never the risk in this business. Founder time is.**

**Founder review time — this is the actual ceiling, and the plan states it wrong.** Every version of the plan gives review time as a flat weekly constant ("30–45 min," KPI ceiling "60 min") that holds from 3 subscribers to 63. That can't be right: every customer gets an individually personalized draft, and review means individually judging it. The real model is a fixed weekly baseline (skim pipeline health, scan the free digest — call it 15 min) plus a marginal per-customer edit time that has to be measured, not assumed. Estimating 3–6 minutes per customer (skim draft, spot-check top citations, adjust framing, decide whether to override anything) as a placeholder pending real pilot data:

| Marginal time/customer | Founder review budget/week | Customer ceiling |
|---|---|---|
| 3 min | 3 hrs | ~57 |
| 3 min | 5 hrs | ~97 |
| 5 min | 3 hrs | ~35 |
| 5 min | 5 hrs | ~58 |
| 6 min | 5 hrs | ~48 |

The plan's own month-24 base-case target — 63 subscribers — sits right at the edge of sustainable under a middling assumption (~4–5 min/customer, ~5 hrs/week dedicated). That's not necessarily wrong, but it is currently a coincidence, not a designed-for number: nothing in the plan measures or budgets for this. **Action:** instrument actual per-customer review time starting the week-3–4 pilot, not the total weekly minutes the KPI dashboard currently tracks. If real per-customer time comes in above ~6 minutes, either the growth targets past ~40–50 subscribers need revising downward, or review needs to stop being solo-founder-only — which breaks the plan's core "90%+ margin, no payroll" claim, since a part-time reviewer's hours are the one cost that scales with revenue instead of staying flat.

---

## Weaknesses to sit with

1. **A direct, already-live competitor exists at the target customer segment and the plan doesn't know it.** VetBiz Network (vetbiznetwork.org — private, unrelated to the free government vetbiz.va.gov portal) sells SAM.gov-feed-plus-AI-matching to veteran-owned businesses at $49–149/month ($588–$1,788/yr), 3–10x under the proposed $5,000 Core price. Before finalizing pricing, get an actual sample of VetBiz's output and compare it against what the Market Snapshot template promises — if VetBiz already delivers "material-change alerts on your NAICS," the wedge has to be sharper than price, and the pitch needs an explicit answer to "why not the $49/month tool" that doesn't currently exist anywhere in the source documents.
2. **SAM.gov's entity data carries an explicit commercial-resale restriction** that the plan's risk table doesn't surface (it lists SAM.gov only under generic "API changes" risk). This is fixable without redesigning the pipeline — source recipient identity from USASpending's CC0 award records instead — but it needs to happen before launch, not after a legal letter.
3. **Review time is asserted, not modeled**, as detailed above — the plan's central scaling assumption is currently a guess dressed as a constant.
4. **The proposal's billing-cost tradeoff was never real.** Whether via subscription or API, LLM spend rounds to noise against $5,000 ACV. The open question spent real analysis on a decision that doesn't move the numbers either way — the actual constraint, review time, got a fixed-constant placeholder instead of the same scrutiny.
