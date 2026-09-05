# SITE-PLAN.md — govcon-factory public website

2026-08-25. Issue #144. Companion to `sop/MARKETING.md` (the doors) and `specs/content-pipeline.md`
(the programmatic archetypes) — this file is the third leg: what actually ships as pages, in what
order, and why. If this disagrees with either of those on funnel mechanics, they win; this file is
the site-specific application.

Brand grounding: `brand/{company,customer,offer,voice}.md` (restored this issue from
`origin/rescue/pre-reset-main-2026-08-25` — see `brand/README.md`'s provenance note). Design
grounding: `DESIGN-SYSTEM.md` (same directory as this file).

---

## 1. What we're building against

**winacontract.com** is the direct comparable Mike named — a funded, polished SaaS competitor
selling contract discovery + AI proposal drafting as a $X/mo membership. Read live 2026-08-25.
Structure, distilled:

Nav → Hero (bold claim + live-looking product mockup, tabbed demo) → trust bar (client-count +
industry chips) → three feature sections (Find / Win / Grow, each with its own mockup) → data-source
coverage list → 60-second video → "the real problem" agitation copy → aspirational 6-month timeline
(Week 1 → Month 6) → big stat bar (9,809 live contracts, 4hrs, 6mo, win-rate) → testimonial carousel
→ "more than software" (built around you / restricted access / we sell the result) → partner/teaming
network → "is it a fit?" (explicit good-fit / bad-fit list) → SEO cornerstone article grid (6
explainers: SAM.gov registration, NAICS codes, capability statements, set-asides, etc.) → footer.

### What we take

- **The "is it a fit?" good-fit/bad-fit block.** Direct, no-nonsense self-qualification instead of
  vague "book a demo" universalism. This maps exactly onto `brand/customer.md`'s ICP ladder (list 1/2/3,
  good-fit/bad-fit) — we already have the real content for this, better sourced than theirs (ours
  cites specific thresholds: cert-exit > deadline + 12mo, ~50% fill floor, other-than-small
  disqualifiers).
- **The SEO cornerstone article grid.** Validates `specs/content-pipeline.md` archetype A3 — six
  short, plain-English explainers driving organic search, each linking back to product. We already
  planned this; seeing a funded competitor running the identical play is confirmation, not a new idea.
- **Data-source coverage as a trust signal.** A visible list of exactly which systems feed the
  product (SAM.gov, GSA eBuy, DLA, etc. for them; SAM.gov + USASpending.gov + SBA DSBS/VetCert for
  us) reads as credible specificity. We do this better: theirs is a bare list, ours is provenance —
  every page already carries "Data retrieved «date»" per PG1/PG5.
- **One clear primary action above the fold.** A single UEI box, one button. No feature-tour before
  the ask.

### What we deliberately avoid

- **"34% Win rate," "$8.4M pipeline" stat cards with no source.** Directly forbidden by
  `brand/offer.md`'s claims-to-avoid ("Win-rate, pWin, or ROI promises") and `brand/voice.md`'s rule
  that every statistic names its source population. Every number we publish traces to a snapshot
  (`data.json`) and a retrieval date — PG1 makes this a build failure, not a style choice, if violated.
- **"Picture six months from now" / Week 1 → Month 6 trajectory with a "send us your first win"
  testimonial ask.** This is an outcome promise ("your first award," "repeat wins") for a product
  that cannot control CO decisions. `brand/offer.md`: "Any guarantee of a set-aside outcome — we
  support the CO's rule-of-two memo; we don't control it." We never publish this shape of content.
- **Government agency logos (DoD/GSA/DHS/HHS/NASA) shown as trust marks.** Reads as implied agency
  endorsement. `specs/content-pipeline.md` PG7 (sample-ethics/endorsement gate) exists precisely to
  block this pattern — "no implied endorsement by any agency."
- **Placeholder/fake testimonial carousel** ("Real member stories replace these as they come in" —
  their own copy admits the content isn't real yet, but it ships anyway). We do not publish a
  testimonial slot before we have a real, attributable one.
- **"By application," gated, cohort-review framing as manufactured exclusivity.** Our actual model is
  the opposite: self-serve UEI lookup, no gatekeeping, no waitlist theater. `brand/voice.md`: "Fake
  urgency... manufactured scarcity" is a listed anti-pattern.
  "winning is the point" (their own real hero-adjacent copy) — the "colon reveal" / fake-profound
  pattern by name, and it directly contradicts our house line: we sell coverage and a gaps list, not
  wins. Never write a sentence like it.
- **Animated SaaS-dashboard hero mockup (browser chrome, "LIVE" badge, tabbed feature demo).**
  Expensive to build, generic-reads-as-AI-native, and dishonest for our shape of product — we don't
  sell a dashboard, we sell one cited document. Our hero shows the actual thing: a live UEI box that
  produces a real (if teaser-scoped) result, and — on the product page — an actual redacted excerpt of
  a real gated sample from `samples/sample-set/`, not a mockup of one.

---

## 2. Sitemap

All routes match `specs/content-pipeline.md` §1's archetype table where one exists — this plan does
not invent new URL patterns for anything the spec already named.

| Route | Archetype | Status this issue | Purpose |
|---|---|---|---|
| `/` | Door 1 hub | **Extend** (exists, `site/pages/landing/`) | UEI box, free-report + newsletter capture, comparison, FAQ. Primary entry point. |
| `/packet/` | new (product page) | **New, this issue** | The $699 opportunity packet: what it is, what it isn't, sample excerpt, price, buy path. |
| `/digest/` | A4 | **New, this issue** (signup + archive shell; no issues to archive yet) | Newsletter signup + public archive of past Buttondown issues. |
| `/free-snapshot/` (+ `/free-snapshot/<code>/`) | A5 | Not this issue (TASK-0009) | Free industry-report magnet, email+NAICS gated. |
| `/naics/<code>/` | A1 | Not this issue (TASK-0011); one worked example exists (`/naics/236220/`) | Per-NAICS market page — programmatic, data-driven. |
| `/agency/<slug>/` | A2 | Not this issue (TASK-0011) | Per-agency buyer page. |
| `/guides/<slug>/` | A3 | Not this issue (TASK-0009); `/` and `/packet/` already link `/guides/sources-sought-response/` as a forward reference | SEO cornerstone explainers — this is where our version of winacontract's article grid lives. |
| `/about/` | new | Not this issue, flagged as a gap | Veteran-owned story, named owner, methodology. `brand/company.md` has the content; no page yet. |

**Scope discipline:** this issue builds `/`  (extend) + `/packet/` + `/digest/` and the design system
all three share. It does not build `/free-snapshot/`, `/naics/`, `/agency/`, `/guides/`, or `/about/`
— those are TASK-0009/TASK-0011/an-unfiled-about-page's work, tracked separately, so this PR stays
reviewable. The homepage's existing links to `/digest/` and `/free-snapshot/` were already forward
references before this issue; `/digest/` now resolves, `/free-snapshot/` still doesn't (expected —
out of scope, not a bug this PR should fix).

---

## 3. Funnel (mapped to the growth plan + MARKETING.md doors)

```
Awareness                    Digest signup              Free-report magnet         Paid trigger
──────────────────────────────────────────────────────────────────────────────────────────────
LinkedIn (Door 4)      ┐
Partner referral (D6)  ├──►  /digest/ signup       ┐
Organic search          │    (footer on every page,│
  → /guides/ (D8, A3)   │     + dedicated page)     │
  → /naics/<code> (A1)  ┘                           ├──► newsletter issue links a
                                                     │     live notice → /packet/
UEI curiosity (Door 1)  ──►  / (homepage)           │     (or the homepage UEI box's
  direct or from a link       UEI box → teaser match│      own "unlock the packet" CTA
                               result → CTA pair:    ┘      skips straight here)
                               "unlock the packet"
                               or "email me the PDF" ──►  /free-snapshot/ (A5, not
                                                            this issue) → nurture →
                                                            newsletter (loop back)
                                                                              │
                                                                              ▼
                                                                        /packet/  →  Stripe
                                                                        invoice/payment link
                                                                        (research/stack-selection
                                                                        §6 — not built this issue,
                                                                        page states price + "buy"
                                                                        is a mailto/contact action
                                                                        until Stripe is wired)
```

Matched outbound (Door 3) is a second on-ramp straight into `/packet/`'s buy step — it does not touch
the top of this funnel, per `sop/MARKETING.md`: "It does not replace the hub. A buyer from either door
lands on the newsletter."

---

## 4. Per-page purpose and CTA

### `/` — homepage (extend existing)

- **Purpose:** prove the mechanism (UEI → live award match → live notice match) in one interaction,
  for a visitor who showed up cold.
- **Primary CTA:** submit UEI.
- **Secondary CTA (post-lookup):** "unlock the packet ($699)" if a real list-3 match exists, else
  "email me the PDF" (free report) + digest signup.
- **Changes this issue:** apply the design system (currently unstyled skeleton); add site-wide
  nav/footer linking `/`, `/packet/`, `/digest/`; fix the stale `PLAN-V6` header comment → `PLAN-V5`
  (V6 doesn't exist on current `main` — see `brand/README.md` provenance note); no copy rewrite — the
  existing draft already passes an anti-slop detect pass (evidence-dense, sourced, no hedges/hype
  found) and was written against the same voice file this issue restored.

### `/packet/` — the $699 opportunity packet (new, this issue)

- **Purpose:** answer "what exactly am I buying" for a visitor who already believes the mechanism
  (arrived from the homepage CTA, a newsletter notice link, or matched outbound) and is deciding
  whether to pay.
- **Primary CTA:** buy this notice's packet (mailto/contact until Stripe Invoicing is wired — page
  says so plainly, does not fake a checkout button).
- **Secondary CTA:** "not sure yet" → digest signup (nurture instead of losing the visitor).
- **Content:** exact deliverable contents (requirements map, 3 past-project cites, intent statement,
  gaps page), one real redacted excerpt from `samples/sample-set/` (sample-bannered per SOP §1.3), the
  exclusivity default (one packet per notice), price logic from `brand/offer.md` ("It's one notice,
  not a subscription..."), and the same FAQ objection-handling register as the homepage (Fiverr, APEX,
  "is it submission-ready") — reused verbatim where the objection is identical, not re-invented in a
  slightly different voice.

### `/digest/` — newsletter signup + archive (new, this issue)

- **Purpose:** capture list-2 firms (won an award in-NAICS, not yet notice-matched) into the nurture
  loop; serve as the public archive once issues exist (A4).
- **Primary CTA:** subscribe (NAICS-code checkboxes per `sop/MARKETING.md` Door 2).
- **Content:** what a weekly issue contains (3 numbers, 1 live notice line, two links) stated plainly
  so signup isn't a blind commitment; archive section present but empty-state ("first issue ships once
  a NAICS has a real report behind it" — matches TASK-0007's own stated gate, not a fabricated "coming
  soon").

---

## 5. Programmatic NAICS pages (A1) — design implications, not build (out of scope this issue)

`specs/content-pipeline.md` §1 already specs A1 fully (data contract, cadence, gates, CTA). This
issue's only obligation to A1 is that the design system (`DESIGN-SYSTEM.md`) ship *reusable* tokens
and components — the stat card, the status table (Covered/Partial/Gap), the source-citation line
component — so that when TASK-0011 builds `render_naics.py`'s real output, it inherits the same visual
system instead of the current bare `site/pages/naics/236220/` skeleton. Verified: the design system's
component list (`DESIGN-SYSTEM.md` §3) covers every element the existing `naics-market.html` worked
example uses.

---

## 6. What's explicitly not decided here

- **Domain name.** Every template still says `EXAMPLE-DOMAIN-TBD` — TASK-0015 (sending domain + DNS),
  needs-mike.
- **Stripe wiring.** `/packet/`'s buy CTA is a contact action, not a live checkout, until
  `research/stack-selection/REPORT.md` §6 is implemented — separate task, not this issue.
- **Cloudflare Pages deploy.** Built and preview-able locally this issue; publishing is Mike's click
  (customer-facing action, `~/CLAUDE.md` explicit-permission category + the stack decision's own
  "nothing self-hosted... customer-facing" framing extends to "nothing goes live without the approval
  step a paid deliverable already gets").
- **The backend for the UEI-lookup form.** Right now `/lookup` and `/subscribe` are honestly-labeled
  client-side demos (skeleton loader → hardcoded results). Wiring the real thing raised a question
  worth flagging rather than deciding unilaterally: `research/stack-selection/REPORT.md` §5
  (2026-08-22) named Cloudflare **Pages**; Cloudflare's own docs, checked live 2026-08-25, now say
  plainly "Are you sure you want to use Pages? ... Start new projects with Workers" — Pages still
  works but isn't where they're investing. Practically, a Worker with static assets can serve this
  exact `site/pages/` output as-is (no rebuild needed either way) and add `/lookup`/`/subscribe` as
  real routes in the same deployment. More relevant to this codebase specifically: Cloudflare now has
  Python Workers (`compatibility_flags: ["python_workers"]`) with a documented pattern for serving a
  static frontend *and* Python API routes from one Worker — a much more direct reuse path for the
  existing `factory/` Python lookup/matching logic than reimplementing it in JS. This changes a
  standing decision (`research/stack-selection/REPORT.md`), so it's Mike's call, not something this
  PR acts on. Recommended next step if he wants to pursue it: a short spike confirming the Python
  Workers path can actually run the existing SAM.gov/USASpending code before committing either way.
