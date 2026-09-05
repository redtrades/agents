# Open-Source Prior Art — Federal Contract-Intelligence Pipeline

**Date:** 2026-08-22 · **Method:** cloned and read actual source (not READMEs) for 16 repos; walked every entry of makegov/awesome-procurement-data; six targeted GitHub searches beyond the list. Context: PLAN-V3.md (deliverables factory) and govconapi-exploration/REPORT.md (data stack).

## Verdict table

| Repo | What it is | License | Last commit | Verdict |
|---|---|---|---|---|
| **GSA/srt-fbo-scraper** | Production SAM ingest + attachment→text pipeline | **CC0** | 2026-04 | **FORK/BORROW** |
| **beeindustriesmail-tech/samgov-screen** | Recompete contestability from USASpending (offers-received) | MIT | 2026-08 | **FORK/BORROW** |
| **groundtruthtools/us-gov-data-mcp** | Expiring-contract detection incl. missing-filter workaround | MIT | 2026-08 | **FORK/BORROW** |
| **makegov/procurement-tools** | UEI validation, UEI→USASpending hash, pydantic entity models | Apache-2.0 | 2024-05 | **BORROW** |
| **chakmarebel/federal-proposal-copilot** | Shipley-aligned Claude Code proposal workflow + compliance matrix templates | MIT | 2026-08 | **BORROW** (templates/rubrics) |
| **CSISdefense/Lookup-Tables** | NAICS / contracting-office / agency lookup CSVs | CC0 | 2026-08 | **ADOPT** (data) |
| CJud25/GovConRadar | DoD cyber/IT recompete ETL+BI, runway estimation, data quarantine | MIT | 2026-07 | REFERENCE |
| blencorp/capture-mcp-server | MCP over SAM+USASpending+Tango, 32★, join tools | MIT | 2026-08 | REFERENCE |
| 0bsolescence/capturecommons | Full watch→triage→shred→draft capture platform w/ provenance gates | **AGPL-3.0** | 2026-08 | REFERENCE ONLY — no code lift |
| riderr/govcon-pipeline | SDVOSB firm's own Sources Sought pipeline, 9-dim LLM scoring | **none** | 2026-05 | REFERENCE ONLY — no code lift |
| PHiZou/recompete-radar | dbt marts for recompete candidates over USASpending | MIT (README) | 2026-08 | REFERENCE |
| pretorin-ai/govbizops | SAM v2 client + SQLite store + Playwright fallback + GPT analyzer | MIT | 2026-03 | REFERENCE |
| MindPetal/sam-search | Daily NAICS poll → MS Teams via GitHub Actions | MIT | 2026-07 | REFERENCE |
| Diego-Arrechea/sam-scraper | Undocumented sam.gov internal API wrapper | MIT | 2024-02 (dead) | REFERENCE (endpoint docs only) |
| HigherGov/API, HigherGov/mcp | Competitor's public API docs | none | 2026-08 | REFERENCE (kill-test prep) |
| dherincx92/fpds | Async FPDS ATOM parser, well built | MIT | 2026-01 | SKIP — ATOM feed retiring FY2026 |
| jpleger/pysam | SAM client on deprecated v1 endpoint | MIT | 2023 | SKIP |
| coforma/usa-spending-bot | Slack bot tracking award recipients (TS) | MIT | 2024 | SKIP |
| abreulastra/sam-bd-pipeline | SAM→Google Sheets BD pipeline | empty LICENSE file | 2026-08 | SKIP |
| ecoffie/govcon-tools | Static-JS expiring-contracts explorer | none | 2026-01 | SKIP |
| nasa/889-Compliance-SAM-Tool, mheadd/SamDotNet, jankaltenegger/SAM.gov-Webscraper, DGill/AcquisitionInnovation | Misc from curated list | various | 2022–2024 | SKIP |

License rule applied: CC0/MIT/Apache-2.0 are safe for commercial borrow. AGPL and no-license repos are read-for-approach only — no copied code, no copied prompts.

---

## The four named repos (code-level findings)

### GSA/srt-fbo-scraper — FORK/BORROW (CC0, the best license possible)
GSA's production Section 508 solicitation-review ingester. Actively maintained (dependency bump Apr 2026), tested (18 test files), Postgres + alembic migrations. The valuable parts are exactly the fiddly ones we'd otherwise debug for a week:

- `get_opps.py` — paginated v2 search loop with `requests_retry_session`, proper `totalRecords`/offset handling, an injectable `opportunity_filter_function`, and attachment download (`get_docs`) that handles the real-world mess: `beta.sam.gov`→`sam.gov` URL rewrites in stale resourceLinks, Content-Disposition filename extraction with `+`→space unquoting, and ENAMETOOLONG filename shortening.
- `get_doc_text.py` — text extraction with the mismatch fallback chain learned in production: `.doc` that's really RTF → rename and retry; `.docx` that's really PDF (BadZipfile) → rename and pdftotext; scanned-PDF TypeError → empty string, never crash. Uses textract (aging); keep the case logic, swap the extractor.
- `sam_utils.py` — notice-type code mapping, NAICS/sol-type filters, `schematize_opp` normalization.

CC0 = public domain; no attribution required, commercial use unrestricted. This is the single highest-value borrow found.

### pretorin-ai/govbizops — REFERENCE (MIT)
Small, clean, tested SAM v2 client + SQLAlchemy store + per-NAICS dedup collector, an OpenAI (gpt-4o-mini) "solicitation analyzer" that drafts responses, and a Playwright scraper fallback for when the API description fetch fails. Nothing here beats srt-fbo-scraper's equivalents, and the analyzer is a naive single-prompt draft (no gates, no provenance) — the opposite of the PLAN-V3 factory. Two ideas worth keeping: the v1→v2 description-URL rewrite (SAM returns v1 URLs in some payloads) and the browser-scrape fallback as a last resort for deleted/superseded content. Pushes into their own "Pretorin CRM"; a company's internal tool published, not a library.

### MindPetal/sam-search — REFERENCE (MIT, actively maintained)
275-line script + generated OpenAPI client: GitHub Actions daily cron, per-NAICS query loop over yesterday's postings, Adaptive Card formatting, 28KB Teams message chunking. Competent but everything is Teams-shaped. The transferable part is the ops pattern — config.yaml NAICS list + scheduled zero-infra runner — which matches what Week 1 needs for the digest, but that's an afternoon's code, not a dependency.

### Diego-Arrechea/sam-scraper — REFERENCE, endpoint documentation only (MIT, dead since Feb 2024)
Low quality: hardcoded `q="construction"` in the search method (!), Spanish variable names, a broken `download_resource` missing `self`, no tests. Its only value is documenting sam.gov's **undocumented internal endpoints** that need no API key: `sam.gov/api/prod/sgs/v1/search/`, `/api/prod/opps/v2/opportunities/{id}`, `/api/prod/opps/v3/opportunities/{id}/resources`, and `/api/prod/opps/v3/opportunities/resources/files/{id}/download`. ToS-gray; keep as an emergency fallback map only. Note the attachment-download endpoint is the same one govconapi's attachment URLs resolve to — already verified working in the data-stack report.

---

## awesome-procurement-data — full walk (20 entries, list last updated 2023-11)

**Official APIs (8):** SAM Entity Extracts, SAM Opportunities, USASpending, FPDS ATOM (retiring — already excluded in PLAN-V3), SBIR, FAR-in-XML (GSA repo), Acquisition Gateway (access-restricted). One genuinely new find for us: **CALC API** (open.gsa.gov/api/dx-calc-api) — GSA professional-services labor rates. Free labor-rate comparables are a cheap enrichment for the $750 Market Snapshot (price-context section) that no plan document currently mentions.

**Utilities (8):**
- **makegov/procurement-tools (Apache-2.0)** — the list curator's own library. BORROW three small pieces: `uei.py` (full UEI checksum validation per GSA spec, ported from GSA-TTS/uei-js — needed the moment UEI joins become load-bearing), `usaspending.py` (the non-obvious UEI→USASpending recipient-hash conversion: `md5("uei-"+UEI)` as UUID + `-P`/`-C` suffix — this is how you build direct USASpending profile links per matched firm), and the pydantic SAM entity models. Dormant since 2024-05 but the pieces are small and stable; vendor them in, don't depend.
- dherincx92/fpds — well-engineered async ATOM parser, but built on the feed GSA is killing in FY2026. SKIP.
- pysam (v1 endpoint, dead), SamDotNet (C#), NASA 889 tool (889-specific entity checks), PSC Selection Tool / FSCPSC / Pulse Part9 (hosted services, not code). SKIP.

**Data science (4):** **CSISdefense/Lookup-Tables (CC0, still updated Aug 2026)** — clean crosswalk CSVs for NAICS, PSC, contracting offices, agency hierarchies; ADOPT as static data for normalizing agency names in Snapshots (cite CSIS per their request). usa-spending-bot (recipient-tracking Slack bot, TS) and the rest: SKIP.

Notably absent from the list: anything touching DSBS/SBS, VetCert, or contact data. The curated ecosystem stops at opportunities + spending.

---

## Broader search — who has already built this

### Recompete / expiring-contract detection (the crowded corner, all 2026)
- **beeindustriesmail-tech/samgov-screen (MIT, Aug 2026)** — FORK/BORROW. Four stdlib-only scripts that are exactly the Market Snapshot's competitive section: `recompete.py` (NAICS → awards ending in N months → per-award detail fetch for `number_of_offers_received`, `extent_competed`, `type_set_aside` → contestability ranking: "1 offer = wired, 5+ = contestable") and `expiring.py` (same, inverted: one company's own expiring contracts — a ready-made outreach hook: "your X contract ends Dec 31"). Encodes two hard-won facts: the search API has **no period-of-performance-end filter** (window applied client-side over paginated results) and offers-received lives only in the per-award detail endpoint (one HTTP call per award — cap it).
- **groundtruthtools/us-gov-data-mcp (MIT, Aug 2026)** — FORK/BORROW `core/expiry.py`: pure, tested functions that solve the same missing-filter problem differently — the API *can* sort by End Date but junk dates (2000…2108) bury today in the middle, so it **binary-searches pages to find the today-boundary in ~10 requests** instead of walking thousands. Also documents the 50,000-row offset-pagination cap (HTTP 422 past page 500). Cleanest detection code found anywhere.
- **CJud25/GovConRadar (MIT, Jul 2026)** — REFERENCE. The most serious end-to-end recompete product: 238K-award USASpending snapshot, recompete-window estimation, pursuit scoring vs. a company profile, FPDS termination evidence to stop dead contracts riding the pipeline as live leads, 118 data-integrity checks, and a quarantine discipline ("records the data can't stand behind are quarantined, not dressed up as leads") that matches the provenance-gate philosophy exactly. DoD-cyber-specific and heavy; read `scripts/validate_data.py` and the runway logic before building Detect, don't adopt.
- PHiZou/recompete-radar (MIT) — dbt staging/mart SQL over USASpending bulk (`mart_recompete_candidates.sql`); REFERENCE if the feed ever moves to warehouse-scale. MarboCreatives/recompete-radar is Canadian data — skip.

### Capture platforms (the philosophical twins)
- **0bsolescence/capturecommons (AGPL-3.0, active Aug 2026)** — the closest thing to PLAN-V3 in the open: watch (SAM + Grants.gov) → evidence-linked go/no-go triage → shredder (compliance matrix + Pink Team) → drafts where "every claim cites a source or is flagged as unsupported." FastAPI + pgvector + provider-abstracted LLM. It is aimed at grants-heavy nonprofits/tribal/municipal self-hosters, free. **AGPL: no code or prompt text may be lifted into a commercial closed product** — reference architecture only. Strategic read: it validates the provenance-gated approach and is simultaneously the free alternative a price-sensitive SDVOSB could be pointed to; the factory's answer is "finished, verified document delivered to you" vs. "software you must run."
- **riderr/govcon-pipeline (no license, May 2026)** — an SDVOSB IT firm running Mike's exact play for themselves: SAM Sources Sought → hard filters → 9-dimension LLM scoring (NAICS fit 20, set-aside match 20, scope 15, stage 10 with Sources Sought highest, value fit, competition, incumbent, agency relationship, geo) → HubSpot deals + a capture-strategy agent, Claude or local Ollama. Unlicensed = all rights reserved: reimplement, don't copy. The rubric dimensions are the best free prior art for the bid/no-bid scoring the outreach matcher needs — and evidence the target buyer builds this in-house when they can code.
- **blencorp/capture-mcp-server (MIT, 32★, Aug 2026)** — best-maintained repo in the space. TS MCP server: SAM entities/opportunities/exclusions, USASpending, and join tools (`get_entity_and_awards`, `get_opportunity_spending_context` — the same joins the Snapshot performs). Queue-based per-API rate limiting. Wrong language for our stack; REFERENCE for query shapes, and a sign MCP-wrapped govcon data is commoditizing fast (also: govtoolspro-mcp-server, mindy-mcp, gov-contracts-mcp, samgov-mcp — all 2026).
- **chakmarebel/federal-proposal-copilot (MIT, Aug 2026)** — BORROW. A Claude Code-native, Shipley-aligned proposal factory with compliance-matrix and color-team-review templates, voice-pair prose calibration, md→docx/xlsx tools, and a leak-scan script. Not a pipeline (no ingest), but its `templates/` and `reference/methodology/` are ready-made seed material for the compliance and format gates — MIT, and already structured for the same runtime we're building on.

### Gaps confirmed by absence
- **DSBS / SBA Small Business Search: zero working open-source scrapers or exporters on GitHub** (only a 2022 CSV snapshot). The SBS ingester must be written fresh — consistent with PLAN-V3 calling it "the fragile differentiator." The absence is the moat.
- **VetCert:** nothing. **Contact/outreach enrichment:** nothing beyond generic tools; no prior art to borrow, none needed given the DSBS-as-contact-source decision.
- **Sources Sought response generation as a product:** govbizops' naive draft and capturecommons' AGPL drafts are the only public attempts. Nobody ships gated, provenance-cited deliverables. The wedge survives this scan.

---

## What this changes about the Week-1 build plan

**Borrowed, not written (saves roughly 2–3 days of edge-case debugging):**

1. **SAM ingest + attachment pipeline** — port `get_opps.py`/`get_doc_text.py`/`sam_utils.py` logic from srt-fbo-scraper (CC0). Specifically keep: retry session + pagination, the beta.sam.gov rewrite, Content-Disposition filename handling, and the extension-mismatch fallback chain (swap textract for pymupdf/python-docx). This is the standing SAM.gov-API fallback PLAN-V3 §9.4 requires, prebuilt.
2. **Recompete/expiring detection** — lift samgov-screen's query shapes + contestability metric and us-gov-data-mcp's `expiry.py` (both MIT). The Market Snapshot's competitive section ("incumbent won with N offers last cycle") and the future Detect feed both drop from design problems to integration work. `expiring.py`'s per-company inversion is a new, cheap outreach angle: email a matched firm about *their own* expiring contract.
3. **Entity plumbing** — vendor `uei.py` + the UEI→recipient-hash converter from procurement-tools (Apache-2.0); gives valid UEI joins and direct USASpending profile links in every deliverable's citations.
4. **Gate seed material** — federal-proposal-copilot's compliance-matrix and review templates (MIT) seed the compliance/format gate rubrics, to be frozen against the first 2–3 real deliverables per PLAN-V3 §6.
5. **Static data** — CSIS Lookup-Tables (CC0) for agency/office name normalization; CALC API as a free labor-rate enrichment for Snapshots (new addition to the stack, costs nothing).

**Written fresh (no usable prior art):** the SBS/DSBS ingester (the moat), the VetCert-proxy firm matcher, the notice-to-firm outreach matcher, and the native gate contract (gate(envelope, run) → GateReport) — capturecommons and govcon-pipeline prove the concepts work but their licenses forbid lifting, which PLAN-V3's "reimplement natively" decision already anticipated.

**Strategic notes:** the recompete-radar corner got crowded in 2026 (four independent builds in three months) — Detect-feed differentiation must be SDVOSB-matching + provenance, not detection itself, which is now table stakes. CaptureCommons is the free-alternative objection to prep for. And riderr/govcon-pipeline is a reminder that BD-capable SDVOSBs build in-house — consistent with PLAN-V3 targeting non-BD-staffed firms first.
