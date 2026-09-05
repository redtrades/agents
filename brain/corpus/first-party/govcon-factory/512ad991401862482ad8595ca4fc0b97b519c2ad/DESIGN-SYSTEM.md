# DESIGN-SYSTEM.md — govcon-factory public site

2026-08-25. Issue #144. Companion to `SITE-PLAN.md`. Governs `site/static/style.css` and every
template in `site/templates/`.

## 1. Stack decision

**Plain HTML/CSS, no build step, no framework.** The existing scaffold (`site/README.md`) is
deliberately framework-free — `specs/content-pipeline.md` §2 already flags Astro as "an allowed later
refactor" that "changes step 2 only." This issue does not take that refactor: introducing
Node/Astro/a component framework is a real toolchain change (new CI step, new thing for
`page_gates.py`/`verify_landing.py` to account for, new thing the next agent has to learn) and nothing
in this issue's scope needs it — three static pages and a shared stylesheet don't need componentized
build tooling. Design tokens (below) get us most of what a component library buys, without the
toolchain cost. Revisit Astro when A1/A2 scale-out (dozens–hundreds of generated pages) makes
hand-copying a template per archetype genuinely painful — not before.

**Component base: shadcn/ui's *token model and component anatomy*, not its React runtime.** shadcn/ui
(MIT license, github.com/shadcn-ui/ui) ships as copy-into-your-repo source, not an npm dependency —
its actual innovation for our purposes is the CSS-variable token contract (`--background`,
`--foreground`, `--primary`, `--muted`, `--border`, `--radius`, etc.) and a small set of well-tested
component *shapes* (button variants, card, badge, accordion, table). We port that token contract and
those shapes to plain CSS custom properties + vanilla HTML/CSS, skipping React/Radix/Tailwind
entirely. This is what "shadcn as component base" means in a zero-build static site.

## 2. Typography and color

**Brand fit check first:** `brand/voice.md` — "plain and specific," "evidence-first," "veteran-to-
veteran respect, no valor-milking," never "marketing register." The visual system has to read as
*documentary*, not *startup*. winacontract's dark-gradient hero + neon accent + glossy dashboard
mockup is the exact visual register we're avoiding — it's the SaaS-hype look paired with their
SaaS-hype copy. Ours should look like the thing it is: a cited government-data product, closer to a
well-typeset report than an app landing page.

**Typography:**
- **UI/body:** `-apple-system, "Segoe UI", Inter, system-ui, sans-serif` — the existing scaffold
  already uses `system-ui`; this issue adds Inter as a webfont-optional upgrade (system font stack
  first, Inter loads progressively if the network allows — no layout shift dependency on a CDN font
  loading, no self-hosted font server).
- **Cited data (dollar figures, PIIDs, dates, UEIs, counts):** `ui-monospace, "SF Mono", "Cascadia
  Code", monospace`. Every number on this site is a citation, per PG1 — giving cited figures a
  distinct, tabular typeface makes that provenance discipline *visible*, not just enforced at build
  time. This is the one deliberately distinctive typographic choice and it's functional, not
  decorative: it's the same instinct as `voice.md`'s "if there's no number with a file behind it, cut
  the sentence" — the type system makes the number-with-a-file visually different from prose.
- **Scale:** a restrained 5-step scale (0.875rem / 1rem / 1.25rem / 1.75rem / 2.5rem) — no
  hero-sized 5rem+ display type. The claim is the content, not the font size.

**Color — restrained, functional, low-saturation:**

| Token | Light value | Use |
|---|---|---|
| `--background` | `#fefefe` | Page background — near-white, not stark, closer to paper |
| `--foreground` | `#18181b` | Body text |
| `--muted` | `#6b6b6f` | Secondary text, captions, source lines |
| `--muted-bg` | `#f4f4f5` | Subtle section backgrounds, code/data blocks |
| `--border` | `#e4e4e7` | Hairline borders, table rules |
| `--primary` | `#1e3a5f` | Deep slate-navy — links, primary buttons, headings accent. Institutional, not techy. |
| `--primary-foreground` | `#fefefe` | Text on primary-colored surfaces |
| `--accent` | `#166534` | Reused from the existing skeleton's `--accent` (`#14532d`, adjusted +contrast) — success/covered state only, never decorative |
| `--warn` | `#92400e` | Sample/draft banners — unchanged from existing skeleton |
| `--status-covered` | `#166534` on `#f0fdf4` | Requirements-map "Covered" |
| `--status-partial` | `#92400e` on `#fffbeb` | Requirements-map "Partial" |
| `--status-gap` | `#991b1b` on `#fef2f2` | Requirements-map "Gap" |
| `--radius` | `6px` | shadcn's default corner radius — soft but not rounded-pill |

No gradients. No hero background imagery. The only saturated color on the page is the three-state
status system (Covered/Partial/Gap) — because that system *is the product*, so it's the one place
color is allowed to carry meaning beyond the primary/muted/border grayscale-plus-navy base.

## 3. Component inventory

Each ships as a CSS class block in `site/static/style.css` (token-driven, so a future Astro migration
can lift these 1:1 into components without a redesign) plus, where interaction is needed, a small
inline `<script>` (no dependency, matches the existing landing page's pattern).

| Component | Shape (from shadcn) | Used on | Notes |
|---|---|---|---|
| Button (primary/secondary) | `.btn-primary` / `.btn-secondary` | All 3 pages | Existing `.btn-primary` kept; add `.btn-secondary` (outline, `--border`) for the non-committal CTA (e.g. "not sure yet" on `/packet/`) |
| Card | `.card` | `/packet/` deliverable-contents list, `/digest/` archive items | shadcn's bordered-container-with-header shape; replaces ad-hoc `.cta`/`.stat` boxes with one consistent primitive |
| Badge | `.badge`, `.badge-covered/-partial/-gap` | Requirements-map excerpt on `/packet/`, NAICS/set-aside tags | Small pill, `--radius`, status-colored variants |
| Accordion | `.faq details/summary` (existing) | FAQ on `/` and `/packet/` | Native `<details>` — zero-JS, accessible by default, already shipped; keep it, it's the shadcn accordion's actual accessible base under the hood anyway |
| Status table | `.status-table` (new) | Requirements-map excerpt | Extends the existing `table`/`.comparison` styles with per-row status badges instead of a plain data table |
| Data citation line | `.source-line` (renamed from existing `.source`) | Every page, footer + inline data callouts | Monospace date/figure, muted color — the PG1 provenance line made visually consistent everywhere it appears |
| Nav | `.site-nav` (new) | All 3 pages | Currently only the homepage has a bare `<a href="/">Home</a>` breadcrumb. Adds a real, shared 3-link nav (Home / Packet / Digest) so the site reads as one thing, not three orphan pages |
| Footer | `.site-footer` (extends existing `.footer`) | All 3 pages | Shared identity/source block, currently only on homepage |

## 4. Reference sites — what's borrowed, what isn't

Per Mike's list, checked for licensing before use (verified live, 2026-08-25):

- **ui.shadcn.com** — token model + component anatomy, as above. MIT-style "open code" project; code
  is meant to be copied and modified.
- **transitions.dev** — free tier only (site has a paid "Pro" tier for premium effects; not
  subscribed, so only free-tier patterns are eligible). Used sparingly: a brief number pop-in for the
  UEI-lookup stat cards (the existing demo JS already swaps in numbers on submit — this issue adds a
  ~150ms fade/count-up so the swap doesn't feel like a jump-cut) and a skeleton-loader state for the
  same lookup while `demo-results` is pending. No page-transition animation, no scroll-triggered
  reveals — those read as "AI-native app," not "cited report."
- **rareui.com** — open-source (GitHub), reviewed for the segmented/OTP-style input pattern for the
  UEI field. Not used: our UEI field is a single free-text input with a regex `pattern` attribute
  (already shipped), and splitting it into segments would fight the copy-paste-a-UEI-from-SAM.gov use
  case, which is the actual task. Noted as considered-and-rejected rather than silently skipped.
- **beautifui.dev / beui.dev** — beautifui.dev: MIT-licensed primitives, but purpose-built for AI-chat
  interfaces (streaming text, approval cards, thinking indicators) — not the right register for a
  marketing/product site; not used. beui.dev did not resolve to distinguishable content separate from
  beautifui.dev during this review — flagged rather than guessed at.

## 5. Accessibility and performance baseline

- Semantic HTML first (`<nav>`, `<main>`, `<footer>`, `<details>`) — already the existing scaffold's
  practice, kept.
- Color contrast: `--primary` (#1e3a5f) on `--background` (#fefefe) = 10.9:1; `--muted` (#6b6b6f) on
  `--background` = 5.1:1 — both clear AA (body text needs ≥4.5:1) and AAA (≥7:1 for the primary pair).
- No custom font blocks first paint — system font stack renders immediately, Inter (if loaded) swaps
  via `font-display: swap`.
- Zero external script/style dependencies — everything in `site/static/style.css` and inline
  `<script>` blocks, matching the existing scaffold and the "nothing self-hosted, nothing
  third-party-dependent in a customer-facing path" stack decision's spirit (this is about page weight
  and dependency risk, not the hosting-location rule itself, but the same instinct applies).
