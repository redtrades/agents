# Claim ledger — VA/SDVOSB intelligence business

2026-08-21. Consolidated from four independent research passes (competitor pricing, SDVOSB/VA policy, USASpending/SAM.gov ToS, Anthropic billing/compliance, GitHub mobile). Confidence follows the acp-harness-comparison convention: VERIFIED (independently re-fetched, matches), PLAUSIBLE (single-sourced or gist-only), CONFLICTING (sources disagree — reported, not resolved).

## Competitor pricing & positioning

| # | Claim | Source | Confidence |
|---|---|---|---|
| 1 | GovWin IQ publishes no price list; third-party estimator blogs disagree with each other — one gives $13K–$119K/yr (avg ~$29K), another implies ~$2,400/seat/yr base | civiciq.com, fed-spend.com, itqlick.com | CONFLICTING |
| 2 | The business plan's "$15K–$40K+/yr" GovWin figure is directionally plausible but not independently verifiable against a vendor-published number | same as #1 | PLAUSIBLE |
| 3 | GovWin has no dedicated SDVOSB/VA product module — its "SDVOSB" content is a free editorial trends report, not a filtered product tier | iq.govwin.com, deltek.com | VERIFIED |
| 4 | GovTribe tiers (vendor's own docs): Launch $1,500/yr, Launch Plus $1,900/yr, Growth $5,000/yr, Growth Plus $6,000/yr — no VA/SDVOSB-specific tier | govtribe.com/user-guide | VERIFIED |
| 5 | No major incumbent (GovWin, GovTribe, HigherGov, BGOV, GovSpend, Fedmine, Unison) offers a dedicated SDVOSB/veteran-owned product line | aggregate vendor-site check | VERIFIED |
| 6 | **VetBiz Network** (vetbiznetwork.org — private, for-profit, distinct from the free government vetbiz.va.gov portal) already sells SAM.gov-feed-plus-AI-matching for veteran-owned businesses at $49/mo ("Tactical Operations," ~$588/yr) and $149/mo ("Strategic Command," ~$1,788/yr) | vetbiznetwork.org, fetched directly | VERIFIED |
| 7 | Free/near-free substitutes exist: SAM.gov saved searches with email alerts, and USASpending.gov custom reports, both filterable by NAICS/set-aside | secondary summary, not primary docs | PLAUSIBLE |

**Implication:** the $5,000/yr price point is not undefended territory — VetBiz Network already serves veteran-owned businesses at 3–10x lower cost. The wedge has to be analytical depth (named incumbent, vulnerability signal, recompete date, buying-office concentration) that a feed-matching tool doesn't attempt, not "cheaper than GovWin" alone. **Action before launch:** do a direct feature comparison against VetBiz Network's actual output, not just its price.

## SDVOSB/VA policy landscape

| # | Claim | Source | Date | Confidence |
|---|---|---|---|---|
| 8 | VA's Rule of Two (mandatory SDVOSB/VOSB set-aside, 38 U.S.C. §8127, *Kingdomware*) remains in force; no repeal | statute + case law, secondary summaries | ongoing | VERIFIED |
| 9 | A 2026 House procurement bill trends toward *codifying* Rule of Two further, not weakening it | Federal News Network | Jun 2026 | PLAUSIBLE (paywalled; snippet-only) |
| 10 | White House/OFPP+SBA explicitly reaffirmed preserving small-business set-aside requirements alongside EO 14240's procurement-consolidation push | whitehouse.gov | Sep 2025 | VERIFIED |
| 11 | VA no longer runs its own CVE verification; SBA's VetCert has been sole certifier since Jan 2023 | va.gov/OSDBU | updated Aug 2025 | VERIFIED |
| 12 | VetCert had a real backlog (up to ~2,700 pending, processing time rose to 81 days by end of 2024); SBA self-reports it cleared to zero, ~12-day average, by Nov 2025 | sba.gov press releases | Nov 2025 | VERIFIED (self-reported, not independently audited) |
| 13 | Fraud crackdown is real but currently centered on the adjacent 8(a) program (1,000+ firms suspended Jan 2026), not SDVOSB/VOSB directly | sba.gov | Jan 2026 | VERIFIED, scope caveat noted |
| 14 | VA prime-contract SDVOSB obligations: FY2024 $10.2B (23% of prime $), FY2025 $10.1B (21.68%) | va.gov/osdbu (FY24, primary); social post (FY25, secondary) | FY24–25 | VERIFIED (FY24) / PLAUSIBLE (FY25) |
| 15 | Implied total VA prime spend ≈ $44–47B/yr, backing out the SDVOSB percentage — supports the plan's "$40B+" figure | derived from #14 | — | PLAUSIBLE (arithmetic inference) |
| 16 | A third-party aggregator (plainspending.com) shows internally inconsistent VA totals ($155B vs $298B in two fetches) — do not use as a source | plainspending.com | — | CONFLICTING, excluded |
| 17 | Registered SDVOSB/VOSB firm count (plan estimates 25,000–35,000): no authoritative current headcount found; partial data (10,400 approved in VetCert's first year, +17,000 in FY2024 alone) is directionally consistent but not a confirmed live total | sba.gov, fsuvboc.com | 2024 | UNVERIFIED / PLAUSIBLE |

**Implication:** nothing here should raise the plan's risk assessment — if anything the legal foundation looks more durable than a plan written a year ago might assume, and VetCert's operational friction (the thing most likely to actually block a prospective customer) has genuinely improved. Watch item: whether the 8(a) fraud-crackdown scrutiny extends to SDVOSB/VOSB verification.

## USASpending.gov / SAM.gov terms of use (business-model risk)

| # | Claim | Source | Confidence |
|---|---|---|---|
| 18 | USASpending's API and underlying data are released under CC0 1.0 — explicitly permits commercial use, resale, and redistribution | github.com/fedspendingtransparency/usaspending-api/LICENSE | VERIFIED |
| 19 | Federal government works are public domain by default (17 U.S.C. §105); CC0 makes this explicit for reuse purposes | law.cornell.edu, resources.data.gov | VERIFIED |
| 20 | USASpending's paginated search endpoints hit a practical ceiling around ~10,000 records/query — not the "50K row cap" the fable proposal cited; the real fix is the same either way (use the async bulk-download endpoint, not paginated search, for nightly deltas) | govconapi.com, github.com/fedspendingtransparency/usaspending-api | CONFLICTING on the exact number; VERIFIED on the underlying architectural requirement |
| 21 | **SAM.gov's Terms of Use restrict data use to "the purpose of the work required by the U.S. Federal Government" and bar use "for commercial purposes not covered by this Agreement"** — scope for plain API-key users (vs. System Account/bulk-extract users) is not clearly disclaimed | sam.gov/about/terms-of-use | VERIFIED (text), CONFLICTING on scope |
| 22 | **D&B-sourced SAM.gov entity data is explicitly barred from commercial resale**, including "D&B Open Data" (name/address/ZIP), which additionally bars bulk sharing | sam.gov/about/terms-of-use | VERIFIED |
| 23 | SAM.gov Opportunities API (contract notices) requires a key, has tiered rate limits (10–10,000 req/day by account type); no explicit commercial-use restriction in the endpoint docs themselves, but the site-wide ToU still applies | open.gsa.gov | VERIFIED (limits) / unresolved (commercial scope) |
| 24 | Automated scraping is explicitly prohibited (grounds for Login.gov account termination) — does not clearly extend to authorized API polling, but nightly ingestion must go through the documented API only, never HTML scraping | sam.gov/about/terms-of-use | VERIFIED |
| 25 | No public record found of SAM.gov/USASpending enforcement action against a commercial product; several comparable products (GovTribe, HigherGov, GovConAPI) operate on this same data combination without documented incident | absence-of-evidence search | PLAUSIBLE |

**Implication — this is the one genuine legal/business risk in the plan, not a technical detail.** USASpending is clean. SAM.gov's entity data (the D&B-sourced fields — company names, addresses, size status linked to D&B numbers) is explicitly barred from commercial resale. A product that ingests SAM.gov entity records and resells synthesized profiles of them is the highest-exposure part of this architecture. **Mitigation, buildable without redesigning the pipeline:** source recipient/entity identity primarily from USASpending's own award records (CC0, already carries recipient name/UEI/address), and use SAM.gov calls narrowly for opportunity notices and non-bulk, non-resold lookups. Get counsel to confirm the Data Use Agreement clause's scope for API-key (non-System-Account) users before launch — this is cheap to check and expensive to guess wrong on.

## Anthropic billing & compliance (the two claims Mike flagged specifically)

| # | Claim | Source | Confidence |
|---|---|---|---|
| 26 | **FALSE, as of today.** Anthropic announced separate monthly Agent SDK credit pools ($20/$100/$200 matching Pro/Max 5x/Max 20x) effective June 15, 2026 — then paused the rollout on the same day. Current state: Agent SDK / `claude -p` / third-party usage still draws from the plan's normal interactive limits | support.claude.com/en/articles/15036540 | VERIFIED |
| 27 | **Substantively TRUE**, though "effective 2026-04-04" overstates precision. Anthropic's Consumer Terms of Service bar automated/non-human access (except via API key) and bar reselling or building competing products on top of the consumer Services. Anthropic's own public statement (via The Register, Apr 2026) says third-party/commercial tool use on subscription credentials "isn't permitted under our Terms of Service." April 4, 2026 appears to be when *enforcement* (billing/technical) tightened, not a new clause's effective date — the underlying ToS language predates it | anthropic.com/legal/terms; theregister.com/2026/04/06 | VERIFIED (substance) / PLAUSIBLE (exact date framing) |
| 28 | No official Anthropic document uses the literal phrase "Agent SDK" inside the Consumer ToS text itself — the SDK carve-out (announced, then paused) lives in Help Center/support docs and secondary reporting, not the ToS | multiple, cross-checked | VERIFIED (absence confirmed) |

**Implication — this changes the plan's billing architecture, not just a footnote.** A nightly multi-customer pipeline run on a personal Claude Pro/Max subscription's OAuth credentials is (a) not cheaper than believed — the separate SDK credit pool doesn't currently exist — and (b) not compliant — automated, resale-adjacent use of consumer credentials is barred by Anthropic's own Consumer ToS, independent of the credit-pool question. **The only compliant and viable route is the standard pay-per-token Anthropic API under the Commercial Terms of Service.** This is actually what the business plan document itself already specifies ("Claude API with model orchestration") — it's Fable's open question #3 that introduced the subscription option as if it were live and cheaper. It isn't either.

Current API pricing (Anthropic first-party, per docs.claude.com, cached 2026-06-24): Claude Haiku 4.5 — $1/$5 per MTok in/out. Claude Sonnet 5 — $3/$15 per MTok standard ($2/$10 intro pricing through 2026-08-31, expiring in ~10 days from today). Use standard pricing for planning; the intro rate is not durable.

## GitHub Mobile — review-interface feasibility

| # | Claim | Source | Confidence |
|---|---|---|---|
| 29 | GitHub Mobile (iOS since 2022, Android in beta) supports direct in-app editing of a file — including Markdown — inside an open PR: whole-file plain-text edit, not diff-aware | github.blog changelog, GitHub community discussion #40852 | VERIFIED |
| 30 | The in-app editor cannot edit multiple files in one commit, has no rich-text/markdown toolbar | github.blog, community #40852 | VERIFIED |
| 31 | GitHub Mobile does **not** support one-tap "commit suggestion" (applying a reviewer-proposed inline text replacement) — open, unresolved feature request since Oct 2024 | community discussion #141743 | VERIFIED (gap confirmed, no fix found through Aug 2026) |
| 32 | github.dev (the mobile web editor fallback) has a documented, unresolved failure mode on mobile Safari/Chrome ("stuck at Setting up your web editor") | GitHub community discussion #74779 | VERIFIED (specific failure mode; not proof it's universally broken) |
| 33 | General mobile-browser use of github.com is anecdotally described by developers as built around desktop assumptions (keyboard shortcuts, cursor precision) | dev.to opinion piece | PLAUSIBLE (single source) |

**Implication:** for exactly this task shape — open one drafted markdown briefing per customer, tweak wording, approve — GitHub Mobile's file editor is more workable than a naive "GitHub PRs are desktop-only" assumption would suggest. The real gap is anything requiring diff-precise edits, multi-file changes, or applying a suggested change — none of which this review step needs if each customer's briefing is a single file. The stronger objection to GitHub-PRs-as-review-UI is not mobile friction per se; it's navigation overhead (finding the right PR among N open ones, per-customer, every week) and the false premise that PRs are required to capture training data (see fable-critique.md).
