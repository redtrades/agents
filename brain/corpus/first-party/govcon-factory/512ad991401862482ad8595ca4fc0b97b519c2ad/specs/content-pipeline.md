# Content pipeline — agent-driven programmatic content/SEO

**Status: DESIGN (skeleton).** Nothing in this spec is live. Implementation is tracked in
[issue #139](https://github.com/redtrades/govcon-factory/issues/139); the near-term
cornerstone/mini-snapshot subset is [issue #138](https://github.com/redtrades/govcon-factory/issues/138)
(which this spec extends, not replaces). Sequencing authority: `research/growth-plan/REPORT.md`
§1 (programmatic SEO), §6 (free tier), §8 (start-now vs. wait triggers). Stack decisions
(SQLite, Cloudflare Pages, Buttondown) were made in `research/stack-selection/REPORT.md` —
this spec does not reopen them.

The one-sentence version: **the same pipeline data that produces paid deliverables renders
public pages, under the same provenance discipline, with Mike approving each page template
once and the factory regenerating pages from data thereafter.** A public page with a wrong
number is a reputation-gate failure (growth plan §8) — so pages go through gates like
deliverables do, and fail closed.

---

## 1. Page archetypes

Five archetypes. Each is one template file in `site/templates/`, one URL pattern, one data
contract, one regeneration cadence. A page ships only if its gates pass (§5); a page that
fails gates is simply not emitted (or its previous good version is kept — never a stale-data
page silently presented as fresh).

| # | Archetype | URL pattern | Data inputs | Cadence | Min unique data points (PG3) | CTA |
|---|---|---|---|---|---|---|
| A1 | Per-NAICS market page — "Sources Sought activity in NAICS «code»" | `/naics/<code>/` | S1 open notices, S3 award history roll-up (later), notice-level facts (agency, set-aside, deadlines) | Daily (with ingest) | ≥ 10 | Digest signup + mini-snapshot request |
| A2 | Per-agency buyer page — "How «agency» uses Sources Sought in «NAICS list»" | `/agency/<slug>/` | S1 notices grouped by agency, S9 forecast entries, S3 award patterns (later) | Weekly | ≥ 10 | Digest signup |
| A3 | Per-notice-type educational cornerstone (e.g. "How to respond to a Sources Sought notice", "SDVOSB rule of two", recompete explainers) | `/guides/<slug>/` | Hand-written prose + live data callouts pulled from A1 data + annotated sample from `samples/` (sample-ethics rules, SOP §1.3) | Prose: on edit. Data callouts: weekly | ≥ 3 live data callouts | Digest signup + product page |
| A4 | Weekly digest web version (public archive of each Buttondown issue) | `/digest/<yyyy-mm-dd>/` + `/digest/` index | The already-approved digest issue (TASK-0007 output) — no new claims, ever | Weekly, after Mike approves the send | n/a — inherits issue's approval | Digest signup |
| A5 | Free mini-snapshot magnet page (the landing + request form for growth plan §6) | `/free-snapshot/` (+ per-NAICS variants `/free-snapshot/<code>/` later) | A1 aggregates as teaser numbers; the generated snapshot itself is **emailed, not published** and goes through Mike's approval queue per AGENTS.md rule 1 | Teaser numbers: daily | ≥ 5 | The form itself |

Deliberately not in scope (growth plan §8 wait-triggers): recompete pages (needs
`recompete-detect` shipped), notice-alert product, per-firm pages (sample-ethics risk —
uninvited public pages about real firms is exactly what SOP §1.3 restricts; revisit only
with anonymization or opt-in).

Archetype count discipline: A1 starts with the 5 target NAICS (PLAN-V3 §3) only — 5 pages,
not 1,000. Scale-out across all NAICS/agencies is the "programmatic SEO at scale" item that
waits for its trigger (§8 below).

## 2. Data flow

```
S1–S9 ingest (notice-ingest, firm-ingest, …)
        │  recipes/*.md access patterns; raw JSON persisted
        ▼
SQLite store  (db/pipeline.db — the store TASK-0005/daily-ingest builds; FTS5 later)
        │  content-generate skill:
        │    1. per-archetype query → data snapshot JSON (frozen input, one per page)
        ▼
site/data/<page-path>/data.json     ← page-level provenance ground truth (≙ order data/)
        │    2. template render (Python string templating; no framework build step)
        ▼
site/pages/<page-path>/index.html   ← candidate page, not yet publishable
        │    3. page gates (site/gates/page_gates.py) — fail closed per page
        ▼
gate-green pages only → sitemap.xml, robots.txt, index updates regenerated
        │  site-publish skill:
        ▼
Cloudflare Pages deploy (wrangler pages deploy site/pages/ or git integration — TASK-0006's
landing-site project; this site is the same Pages project, same domain)
        │
        ▼
post-deploy verify: fetch N random published URLs, diff against local render
```

Key properties:

- **Frozen data snapshot per page.** The render never reads the live DB directly at
  template-fill time; it reads the snapshot JSON emitted for that page in that run. This is
  the exact analogue of a deliverable's `data/` directory (SOP §1.4): every figure on the
  page must exist verbatim in that page's `data.json`, so gates can regex-sweep page vs.
  snapshot exactly like `gate_runner.py` G2 sweeps deliverable vs. `data/`.
- **Per-page fail-closed.** One page failing gates blocks that page, not the site. A failed
  regeneration leaves the previous gate-green version live **only if** it still passes PG5
  freshness; otherwise the page is unpublished (removed from sitemap + 404/redirect to the
  archetype index). Silence beats staleness.
- **No framework build yet.** Plain HTML emitted by the render script, one shared CSS file.
  Astro (or similar) is an allowed later refactor — it changes step 2 only; the
  snapshot/gates/deploy contract is framework-agnostic on purpose.

## 3. Freshness & regeneration cadence

| Archetype | Regenerated | Staleness limit (PG5) | On stale |
|---|---|---|---|
| A1 per-NAICS | Nightly, after `notice-ingest` completes green | 48 h since underlying ingest run | Unpublish page (see §2); never serve counts older than 48 h |
| A2 per-agency | Weekly (Mon, after weekend ingest) | 10 days | Unpublish |
| A3 cornerstones | Data callouts weekly; prose only on edited-and-approved change | Callouts 10 days | Strip callouts to prose-only version (prose has no perishable claims) |
| A4 digest archive | On each approved send | Never stale (dated historical artifact — page states its date) | n/a |
| A5 magnet teaser | Nightly with A1 | 48 h | Fall back to form without teaser numbers |

Every data-bearing page displays its retrieval date ("Data retrieved YYYY-MM-DD") — the
freshness claim is itself a page fact that PG1 checks against the snapshot.

## 4. Internal linking & SEO mechanics

**Linking scheme (hub-and-spoke, generated, never hand-maintained):**

- A3 cornerstones are the hubs: each links to every A1 NAICS page and to `/free-snapshot/`.
- A1 pages link: sibling NAICS pages (all 5), the agency pages (A2) for their top agencies,
  the relevant cornerstone, and the CTA pair. A2 links back to the A1 pages it draws from.
- A4 digest issues link to the A1 pages for each NAICS mentioned; `/digest/` index links all.
- Every page carries breadcrumbs (Home → section → page) matching `BreadcrumbList` schema.
- Rule: links are emitted from the same data snapshot as the page (an A1 page's "top
  agencies" links must match the agencies actually shown on the page).

**Per-page SEO surface (all generated at render, per archetype):**

- `<title>` + meta description from archetype-specific templates with live numbers where
  the numbers are gate-checked (e.g. `Sources Sought in NAICS 236220 — 24 open notices |
  «site»`). A number in a title is a claim; PG1 applies.
- Canonical URL; `og:`/`twitter:` cards; `robots` per-page: **`noindex` until the page's
  gates have passed on 2 consecutive regenerations** (protects against a bad first render
  getting indexed), then index-follow.
- JSON-LD: A1/A2 → `Dataset` (+ `Organization` publisher); A3 → `Article` (+ `FAQPage` where
  the guide has a Q&A section); A4 → `Article` with `datePublished`; A5 → `WebPage`.
- `sitemap.xml` regenerated on every publish from the set of currently gate-green pages
  only; `lastmod` = data retrieval date. Submitted to GSC once (TASK-0009 covers the
  console setup); after that, deploys just update the file.

## 5. Quality gates (adapted from SOP-DELIVERABLES §2.4/§3.4 — the deliverable SOP is the parent)

Implemented in `site/gates/page_gates.py` (stub today). Same posture as `gates/gate_runner.py`:
one line per check, fail closed, a gate that can't run (missing snapshot, API error at verify
time) is a FAIL, never a skip. Output: `GATE-REPORT.json` per site build, listing every page,
every gate, offending string + file on failure — same evidence shape as a deliverable's
`GATE-REPORT.md`.

| Gate | Check | Adapted from |
|---|---|---|
| **PG1 Provenance** | Every number, date, count, agency name, notice ID, and dollar figure in the rendered HTML (including `<title>`, meta, JSON-LD) exists verbatim in that page's `data.json`. Dollar figures truncated (floored) so the page figure is a verbatim prefix of the source value. Each data section carries a source line with retrieval date per SOP §1.2 formats | G2 Provenance |
| **PG2 Count exhaustion** | Any claim of the form "N notices/firms/awards" requires pagination-exhaustion proof in the snapshot (`has_next: false` or all pages pulled). Otherwise the claim must be **scoped** ("N notices posted between X and Y" covering only what the snapshot fully contains) or the gate fails. See the worked example — this gate has already caught a real case | G2 count rule |
| **PG3 Thin content** | Page ships only with ≥ N unique data points (per-archetype N in §1 table). A "data point" = a distinct fact traceable to the snapshot, not a template word. Below N → page not emitted; no filler prose to fake substance | Anti-doorway; growth plan §1 caution |
| **PG4 Duplication** | Rendered text (template boilerplate stripped) must differ from every sibling page of the same archetype by a similarity threshold; two NAICS with near-identical data produce one page + a redirect, not twins | Anti-doorway |
| **PG5 Freshness** | Snapshot age within the archetype's staleness limit (§3); the on-page "retrieved" date matches the snapshot's actual retrieval timestamp | G5 Freshness |
| **PG6 Forbidden sources** | **CPARS is never cited, implied, or estimated — grep for CPARS/past-performance-rating language, hard fail** (SOP §3.4 G3 / AGENTS.md rule 3). No non-public data, no client data, no credential-derived content on any public page | G3 CPARS rule |
| **PG7 Sample ethics / endorsement** | Real firm names on a public page only under SOP §1.3 demo rules (banner/anonymize) or with written permission; no implied endorsement by any agency; notice quotes attributed to the notice | SOP §1.3 |

Human gates that never mechanize: template approval (§6), anything that leaves by email
(mini-snapshot copies — Mike's approval queue, AGENTS.md rule 1), and the first-publish
review of each new page URL at autonomy level L0/L1 (§7).

## 6. How agents run it

| Stage | Skill | Does |
|---|---|---|
| Data | existing `notice-ingest` / `firm-ingest` (+ TASK-0005 ingester) | Keep the SQLite store current; the content pipeline adds **no new ingestion** — if a page wants data the pipeline doesn't ingest, that's a pipeline feature first |
| Generate + gate | `skills/content-generate/` | Query → snapshot → render → run `page_gates.py` → emit gate-green pages + build `GATE-REPORT.json`. Never deploys |
| Publish | `skills/site-publish/` | Regenerate sitemap/robots from gate-green set, deploy to Cloudflare Pages, post-deploy verify, log the publish in `status/`. Never edits content |
| Feedback | existing `rubric-improve` / `proposals/` | A wrong number that reaches production = incident: file a proposal against the gate that should have caught it, fix the gate before regenerating |

**Human touchpoints (the contract with Mike):**

1. **Template approval, once per archetype version.** Mike reviews each archetype template
   + one rendered example and approves it explicitly. Approval is recorded in the template
   header comment (`approved: <date> by mike, template-version: N`). After that, pages
   auto-generate from data with no per-page review — that's the entire economics of the
   channel. Any template change bumps the version and requires re-approval; data changing
   under an approved template does not.
2. **First deploy of the site, and any new archetype's first deploy** — publish actions,
   AGENTS.md rule 1.
3. **Every emailed mini-snapshot** — approval queue, batch-approve daily. Publishing a page
   is template-gated; emailing a document is always per-item.
4. Cornerstone (A3) **prose** edits — reviewed like deliverable prose.

**Earned-autonomy progression** (promotion by evidence, demotion instantly on incident):

| Level | Behavior | Promote when |
|---|---|---|
| L0 | Every rendered page reviewed by Mike before deploy | Template approved + 2 consecutive all-green builds |
| L1 | Auto-generate under approved templates; Mike spot-checks a sample per batch; deploy still Mike-triggered | 4 weeks at L1, zero gate-escapes (wrong fact found post-render) |
| L2 | Auto-deploy on all-green gates; post-deploy diff report to Mike (what changed, which pages added/pulled) | 8 weeks at L2, zero production incidents, PG gates extended to cover every incident class seen |
| L3 | Fully scheduled (nightly/weekly per §3) incl. unpublish-on-stale; Mike sees the diff report only | — (terminal) |

Any production incident (wrong figure live, CPARS-adjacent language, endorsement complaint)
drops the pipeline to L0 for that archetype until the gate gap is fixed via a proposal.

## 7. Scope triggers (from growth plan §8 — restated so this spec can't be used to jump the gun)

- **Now (with TASK-0009):** A3 cornerstones (5–10 pages), A5 magnet, A1 for the 5 target
  NAICS as the "live data" those pages cite.
- **After daily ingest is stable AND the TASK-0002 kill-test passes AND cornerstones index
  cleanly:** A1/A2 scale-out (more NAICS, all buyer agencies) — the actual "programmatic
  SEO at scale" play. This is TASK-0011's done-definition territory.
- **Never on this spec's authority:** paid ads, per-firm pages, notice alerts — each has its
  own trigger row in the growth plan.

## 8. Worked example

`site/templates/naics-market.html` (A1 template, **not yet Mike-approved** — approval header
says so) rendered with real 236220 data from
`research/govconapi-exploration/raw/sources_sought_5naics_open.json` by
`site/scripts/render_naics.py` → `site/pages/naics/236220/index.html` +
`site/pages/naics/236220/data.json`. It demonstrates PG2 concretely: the raw pull is page 1
of 314 with `has_next: true`, so the page scopes every count to "notices posted 2026-08-07
→ 2026-08-21 (the window this snapshot fully contains)" rather than claiming a NAICS-wide
total. See `site/README.md` for the file-by-file map.
