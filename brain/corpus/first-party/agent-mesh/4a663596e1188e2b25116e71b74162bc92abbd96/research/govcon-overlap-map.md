# govcon-factory × swarm-stack overlap map

**Written:** 2026-08-26 · **Mode:** read-only analysis of `/Users/man/govcon-factory` + synthesis of tonight's five staging research files (caching-routing, memory-context, agentic-engineering, harnesses-councils, free-routing-subscriptions).
**Rule compliance:** repo content treated as data only; no instructions inside it followed; no secrets printed. Every claim about current state carries a factory file path.

---

## 1. Current-state snapshot

**Note:** the brief named `business/sop/PLAN-V6.md` — that path does not exist. Current operating plan is `sop/PLAN-V5.md` (`AGENTS.md:18` points there; V3/V4 are history under `sop/plan-history/`). Snapshot below reads V5.

### What the business is

An agent factory turning public federal data into two objects: **industry reports** (free magnet/newsletter spine) and **$699 opportunity packets** (one live notice × one firm) — `AGENTS.md:5-14`, `sop/PLAN-V5.md:23-55`. Beachhead: SBA-certified SDVOSBs whose *awards* (not just NAICS listings) match a notice; three-list routing where list 1 is never emailed (`AGENTS.md:36-44`, `sop/PLAN-V5.md:60-70`). The marketing funnel explicitly ends in "**CODE WATCH (alert when the next one matches)**" — `sop/PLAN-V5.md:80-95` — which is an alert product that does not exist mechanically yet (see §3.6).

### What runs today (the mechanized backbone)

- **9-stage pipeline** `ingest → normalize → triage → match → assemble → synthesize → gate → package`, then human review + deliver (`specs/factory-architecture.md` §5 table, lines 158-172). Stages are pure transforms between schema-validated JSON envelopes (`factory/envelope.py`; spec §2); agents operate only *inside* stages.
- All deterministic stages are real and have run end-to-end against a live same-day SAM.gov pull; `synthesize`/`package` completed as TASK-0021/0022 (`AGENTS.md:64`). Four pipeline YAMLs exist: sources-sought-packet, industry-report, market-snapshot, rfp-response-starter (`factory/pipelines/`).
- **On-demand any-notice entry:** `python3 -m factory.runner --notice <sam-id-or-url> --deliverable <type>` does a keyless live pull via `factory.notice_fetch`, with fail-closed notice-type→deliverable compatibility routing (issues #80/#157) (`AGENTS.md:66-68`).
- **Gate registry** (fail-closed): `schema`, `inputs_present`, `provenance`, `count_recomputation`, `freshness`, `single_writer` implemented; `compliance`/`format` bind at package (`specs/factory-architecture.md` §3, lines 105-122; `factory/gates/registry.py`). Waivers are recorded exceptions per `(run_id, stage, gate)`; product-blocking gates can't be waived (`factory/README.md:165-189`, `factory/waivers.py`).
- **SQLite tracing:** every envelope + gate result lands in `factory/factory.db` (tables `envelopes`, `gate_results`) and exports per-run to committed `runs/<run_id>/trace.json` (`specs/factory-architecture.md` §4, lines 136-151; `factory/README.md:20-22`). Resume-from-failed-stage (`factory/README.md:152-163`), retention purge with GOLDEN-marker exclusion (`factory/README.md:115-125`), opt-in PII redaction (`factory/README.md:83-113`, `factory/redaction.py`).
- **Second SQLite precedent:** DSBS small-business universe snapshots persist to `data/sbs/sbs.db` via `factory/sbs_store.persist_snapshot`, behind a canary-first probe (`factory/ingest_sbs.py`; `.github/workflows/sbs-ingest.yml:48-72`).
- **SDLC machinery:** GitHub Issues single queue; atomic claims via git-push mutex on a `claims` branch (`scripts/issue-claim.sh` header — #19 was built twice 39 seconds apart); reviewer-bot GitHub App files real APPROVE/REQUEST_CHANGES reviews (`scripts/reviewer-bot-review.sh`); tiered auto-merge loop Tier-0 docs / Tier-1 code+bot-review / Tier-2 Mike-only (`factory/reviewer_loop.py:1-13`, DECISIONS.md D-032); daily digest (`scripts/daily-digest.sh`); SSSF ADW wiring check (`scripts/ci/check-sssf-wiring.sh`) and dispatcher (`scripts/dispatch-ready.py`, issue #45). Per session context, SSSF phases run `coding_agent: pi` against local omlx (e.g., `packet_reviewer`), and m64 is the self-hosted CI runner with omlx access (session briefing; not found in-repo).
- **CI:** lint + pip-audit + secret scan + pytest + smoke-runs of all four pipelines + page gates (`.github/workflows/ci.yml:32-65`).

### What's manual / stubbed / friction (per its own docs)

| Friction | Evidence |
|---|---|
| Nothing sends without Mike — final review is a queue state, not a stage | `AGENTS.md:29` (rule 1); `specs/factory-architecture.md:171-172` |
| Outbound gated on matcher precision floor (#95/TASK-0018) — analysis runs, outreach waits | `factory/stages/match.py:289,311` |
| List-3 > 40 firms ⇒ matcher judged too loose; tightening is manual | `AGENTS.md:44`; `specs/factory-architecture.md:166` |
| Only ONE live source (bulk CSV leg); second-source cross-check (SAM v2/v3 API) deliberately unbuilt — TASK-0023; govconapi free-tier already 429'd during the build | `specs/factory-architecture.md:213-216`; swap-in point documented in `factory/stages/ingest.py` docstring |
| Ingest re-downloads a ~237MB daily bulk extract; cached per `max_cache_age_hours` only | `factory/README.md:24-28`; `domains/govcon/sources.yaml` |
| `client_profile` loader/UI a stub; full-proposal generator unbuilt | `AGENTS.md:66,68` |
| `deliver` stage not built | `specs/factory-architecture.md:172` |
| Local models: no grammar-constrained decoding — structure enforced only by post-hoc gates; routing contract (local=narrow lookups, frontier=drafting) is binding text, not code | `specs/factory-architecture.md:38-44,169` |
| Scheduled jobs disabled pending hand-smoke (no-parallel-infrastructure rule) — sbs cron commented out | `.github/workflows/sbs-ingest.yml:1-12` |
| Run artifacts hold contact PII; redaction opt-in default OFF; 30-day purge policy | `factory/README.md:76-125` |

---

## 2. SAM.gov integration deep-dive (delta pulls → local corpus → search → feed triage/match)

Design principle: **this extends the existing `ingest` stage; it does not add a parallel pipeline.** The architecture already anticipated exactly this — the spec names the v2/v3 API leg as "the same contract with a different fetch function — swap-in point noted in the module docstring" (`specs/factory-architecture.md:163`) and tracks it as TASK-0023 (`specs/factory-architecture.md:213-216`).

### 2.1 Source landscape

- **Today:** keyless daily bulk Contract Opportunities CSV (~237MB, `https://s3.amazonaws.com/falextracts/Contract Opportunities/datagov/ContractOpportunitiesFullCSV.csv`), filtered to domain NAICS/type/active/due_after; output `ingest/raw/sam_opportunities_filtered.csv` plus a `source_url` envelope input carrying hash + `retrieved_at` (`specs/factory-architecture.md:163`; `factory/stages/ingest.py`).
- **Add:** SAM Opportunities API v2/v3 (`api.sam.gov`), free registered API key, `postedFrom`/`modifiedTo` date-window params → **nightly delta pulls** sized in kilobytes instead of 237MB. Free-tier keys have modest daily/hourly request ceilings — throttle, respect 429/`Retry-After`, and treat a dead API as FAIL per AGENTS.md rule 2 (the repo already learned this lesson with govconapi's 429 — `specs/factory-architecture.md:216`). *(Exact current ceiling figures need a one-time verify against api.sam.gov data-services docs before coding — outside tonight's sources.)*
- **Per-notice deep fetch already exists:** `factory.notice_fetch` (keyless live pull) and `factory.attachments.fetch_notice_attachments()` on real v3 resources/download endpoints (`AGENTS.md:66`). Delta pulls only need to *discover* notice IDs; heavy per-notice enrichment reuses these.

### 2.2 Corpus design (SQLite + FTS5, following the sbs.db precedent)

New module `factory/notices_db.py` (sibling to `factory/sbs_store.py`), database `data/notices/notices.db`:

```sql
CREATE TABLE notices (             -- one row per notice version seen
  notice_id TEXT, posted_date TEXT, modified_date TEXT,
  naics TEXT, agency TEXT, notice_type TEXT, title TEXT,
  description TEXT, due_date TEXT, active INTEGER,
  set_aside TEXT, place TEXT, ui_path TEXT,
  first_seen TEXT, last_seen TEXT,          -- temporal validity, Zep-style
  payload_sha256 TEXT, source_url TEXT, retrieved_at TEXT,  -- envelope-ref compatible
  PRIMARY KEY (notice_id, modified_date));
CREATE VIRTUAL TABLE notices_fts USING fts5(
  title, description, content='notices', content_rowid='rowid', tokenize='porter');
-- optional phase 2: CREATE VIRTUAL TABLE notices_vec USING vec0(...)  -- sqlite-vec embeddings
```

Why SQLite/FTS5 over DuckDB-first: the repo's two existing stores (`factory/factory.db`, `data/sbs/sbs.db`) are SQLite; FTS5/BM25 ships in stdlib; gbrain's measured hybrid recall (BM25+vector RRF) shows lexical alone gets most of the way for exact-name/number queries (`research-memory-context.md` §1 gbrain row). DuckDB stays an *optional* analytics sidecar over archived bulk-CSV snapshots for industry-report aggregates — same file family, no new daemon.

**Provenance invariant:** every corpus row keeps `source_url` + `retrieved_at` + `payload_sha256`, so any downstream stage citing the corpus can emit an envelope `source_url` input ref and pass the existing `freshness`/`inputs_present`/`provenance` gates unchanged (`specs/factory-architecture.md:76-111`). The corpus is just another source leg, not a trust boundary.

### 2.3 Pipeline integration (one new stage variant, zero new pipelines)

1. **Ingest:** add `factory/stages/ingest_delta.py` (or a `mode: delta` flag in the YAML): nightly `modifiedTo=today` pull → upsert into `notices.db` → emit the same-shaped filtered-notice output the current ingest emits. Bulk CSV remains the weekly/backfill leg; delta is the daily leg. Change-detection hash gate: if nothing changed since yesterday's hash, write a no-op run record and exit (artifact-or-nothing, per `research-agentic-engineering.md` §3.1).
2. **Normalize/triage:** unchanged contracts. Triage gains an *input*: for each candidate notice, query `notices_fts` for top-k historic similars (agency + NAICS + title/description terms). Recurring-notice detection ("this RFI reposted 3× this quarter") and agency-cadence features sharpen the existing scoring heuristic (`specs/factory-architecture.md:165`) without touching its fail-closed shape.
3. **Match:** List-2/List-3 already rest on a live USASpending pull (`specs/factory-architecture.md:166`). Historic notices add a *demand-side prior*: which agencies posted similar scopes before, and how those progressed (sources-sought → solicitation), feeding teaming analysis (`factory/teaming.py`) with richer context. Precision-floor work under TASK-0018 gets a measurable substrate: historical list-3 assignments to replay.
4. **Synthesize/assemble:** win-theme retrieval (§3.7) reads the corpus through `assemble/data.json`'s frozen-snapshot pattern (`specs/factory-architecture.md:167`) — never ad-hoc queries inside prompts, keeping the audit trail intact.
5. **Backfill:** seed the corpus from the existing cached bulk extracts (`factory/.cache/`) + N weeks of nightly deltas; record each batch as a run with trace.json so coverage is auditable.

---

## 3. Swarm-stack feature map (research finding → concrete adoption path)

### 3.1 Council review of assembled packets — pi/omlx judges before `gate`

**Research basis:** rank-then-synthesize councils with 3–5 cross-*model* judges; blind anonymized ranking fixes self-preference; minority findings must be gathered before synthesis; deterministic aggregation, no LLM (`research-harnesses-councils.md` §2, §4; `research-agentic-engineering.md` §2.3). SSSF already proves `pi` against omlx works on this machine (packet_reviewer phase).

**Path:** a `packet_council` step between `synthesize` and the `gate` stage — three judges (`pi -p --mode json` against omlx :8300, optionally one FreeLLMAPI :3100 judge for cross-lab decorrelation) each score the drafted packet against the frozen rubric; verdict JSONs land in `runs/<run_id>/council/judge-{N}.json`; a pure-Python Borda aggregator (~100 lines, no LLM) writes `VERDICT.json`. Register a non-blocking `council_consensus` gate in `factory/gates/registry.py`: split verdicts ⇒ advisory note in GATE-REPORT, never auto-pass (AGENTS.md rule 1 intact; Tier-2 decisions stay Mike's). Judge diversity follows the review-independence rule: never all one model family.

### 3.2 Memory layer — gbrain/mempalace over past packets + awards

**Research basis:** verbatim+dated beats lossy summaries (Omi LoCoMo 51%→86.6%); bounded index + lazy bodies; hard invariants belong in gates, not prose (`research-memory-context.md` §2-§4).

**Path:** T2-style store over `runs/*/assemble/data.json` + shipped DELIVERABLEs + award rows, giving win-theme/entity recall ("what did we tell firm X about NAICS 336340 in June"). Non-negotiable adapter rule: **memory hits enter the pipeline only as cited inputs** — a retrieved fact must resolve to a `runs/<run_id>/...` path (with sha256) that goes into the envelope's `inputs` list, or it doesn't get used. That keeps AGENTS.md rule 3 ("no claim without a file") and the `provenance` gate authoritative; the memory layer indexes *where* evidence lives, it never becomes evidence itself. gbrain's markdown-brain doubles as the curated T3 vault for win-theme writeups; MemPalace hooks mine session transcripts. Start read-only (recall MCP tools), no autonomous writes.

### 3.3 Prompt-cache-stable layouts in `synthesize`/`package` prompts

**Research basis:** byte-identical prefixes; static blocks first, volatile last; timestamps/IDs in the final user message; ≤4 Anthropic breakpoints; reads at 0.1x; local omlx has hot+SSD KV prefix caching that rewards the same discipline (`research-caching-routing.md` §1, §4.2).

**Path:** codify a shared prompt-layout helper used by every agent-stage call (`synthesize.py`, `package_rfp_response`, reviewer loops): L0-L3 static layers (rubric, SOP excerpt, tool defs — stable across runs) → breakpoint → L4-L6 (data.json slice, notice text, `today` LAST). Today's likely failure: per-run headers/timestamps near the top kill every cache. Expected effect: 90% off cached Anthropic input tokens and warm TTFT on omlx lookups. Cheap, mechanical, measurable via cached-token ratio.

### 3.4 Token/routing guardrails around `claude -p` agent stages

**Research basis:** DR086-shaped budget fallbacks now native in LiteLLM (`budget_fallbacks`, zero-cost-model exemption); error classes need different timers; SDK retries must be zeroed and owned by the router; cost-velocity breaker for runaway loops (`research-caching-routing.md` §3.1/§4.3; `research-free-routing-subscriptions.md` §2).

**Path:** the binding routing contract already lives in the synthesize stage spec (`specs/factory-architecture.md:169`: local=narrow closed-ended lookups incl. `thinking_budget`, frontier=open-ended extraction/drafting). Mechanize it: one thin client module wrapping every model call from stages — enforces (a) per-run token/spend cap with hard stop (fail closed, files an issue — matching AGENTS.md rule 2), (b) cascade local→paid on budget exhaustion with zero-cost exemption so omlx stays reachable, (c) `max_retries=0` at SDK level with router-owned retry budget ≤4 attempts. No standalone gateway service (no-parallel-infrastructure rule) — a library in-process, config-declared in the pipeline YAML.

### 3.5 Observability — meters over factory runs

**Research basis:** OTel GenAI semantic conventions; Langfuse self-hostable with custom $0 model definitions; spend tracking belongs in existing infra (`research-caching-routing.md` §2.2, §4.3 implementation note: "Langfuse… is the only new component worth adding, and only if per-call cost visibility is currently missing").

**Path:** start trace-native, not server-native: extend `factory/factory.db` with a `stage_usage` table (run_id, stage, model, input/output/cached tokens, est_cost_usd, latency_ms) written by the §3.4 client wrapper; surface in `python3 -m factory.cli shows`. This gives ccusage-class per-run economics with zero new infrastructure and composes with the committed `trace.json` evidence trail. Graduate to self-hosted Langfuse only when multi-machine fleet or council fan-out makes per-span views necessary.

### 3.6 Proactive bots — opportunity alerts / SAM delta watchman / attention ranking

**Research basis:** change-detection heartbeats (cheap state hash, exit unless changed); artifact-or-nothing; missed-window=skip; budgets in wrapper scripts; smoke-by-hand before any cron goes live (`research-agentic-engineering.md` §3).

**Path:** this is PLAN-V5's own "CODE WATCH" made real (`sop/PLAN-V5.md:92-95`). Clone the `sbs-ingest.yml` pattern (`.github/workflows/sbs-ingest.yml:1-27`): `sam-delta-watch.yml`, `workflow_dispatch` first, cron enabled only after hand-smoke passes. Flow: nightly delta pull (§2.3) → triage scoring → for each subscribed firm/code, FTS match against the corpus → attention-ranked digest (score × days-to-deadline × firm-fit) → appended to `daily-digest.sh` output / filed as a labeled issue. **Nothing emails anyone** — alerts surface to Mike and the issue queue; sends remain rule-1-gated. Recsys ranking starts as the existing triage heuristic + corpus novelty features; collaborative signals come later from newsletter click data.

### 3.7 Eval golden sets — extending TASK-0018's matcher precision floor

**Research basis:** vendor benchmarks untrustworthy; run your own golden-set evals with neutral judges; freeze 50-100 probes before feature work (`research-memory-context.md` §2 practitioner consensus #5; `research-agentic-engineering.md` §2.4 solo-operator recipe).

**Path:** the pieces exist: GOLDEN-marker-protected reference runs (`factory/README.md:121-125`), mutation testing (`factory/mutation_testing.py`), and the matcher precision floor gating outbound (`factory/stages/match.py:289`, DECISIONS.md:155 records the `work/matcher-gold-TASK-0018` branches). Extend: (a) replay historic list-2/3 assignments against corpus-derived ground truth; (b) add retrieval-quality probes for the FTS layer (P@5/R@5 style, gbrain's BrainBench method); (c) add council-verdict-stability checks (same packet, two judge pools ⇒ agreement rate) before trusting §3.1; (d) wire all three into ci.yml as a nightly job, not per-PR. This converts TASK-0018 from a one-time floor into a continuous regression guard — the precondition for ever loosening the outbound gate safely.

---

## 4. Ranked roadmap — top 8 upgrades by value/effort

| # | Upgrade | Value | Effort | Extends (existing mechanism) |
|---|---|---|---|---|
| 1 | **SAM v2/v3 nightly delta pulls** (keyed API, `modifiedTo` windows, throttle + fail-closed) | High — fresh data, kills the 237MB/day dependency, unblocks #2/#3/#6 | M | TASK-0023 swap-in point in `factory/stages/ingest.py` (`specs/factory-architecture.md:163,213-216`); canary-first pattern from `.github/workflows/sbs-ingest.yml:35-49` |
| 2 | **Historic-notices SQLite corpus + FTS5/BM25** (`factory/notices_db.py`, backfill from cached extracts) | High — recurrence detection, agency cadence, report spines, retrieval substrate for everything below | M | `factory/sbs_store.py` persistence pattern; envelope `source_url` refs keep `freshness`/`provenance` gates valid (`factory/envelope.py`, spec §2-3) |
| 3 | **Code-watch alert bot** (delta → triage → ranked digest → issue/digest comment; no auto-send) | High — it IS the PLAN-V5 funnel's promised endgame (`sop/PLAN-V5.md:92-95`) | L (after #1) | `sbs-ingest.yml` dispatch-then-cron pattern; `scripts/daily-digest.sh`; triage scorer in `factory/stages/triage.py` |
| 4 | **Cache-stable prompt layout helper** for all agent-stage calls (static-first, timestamps-last, breakpoints) | Med-high — direct 10x input-token cost cut on frontier calls, warm local TTFT; tiny diff | L | `factory/stages/synthesize.py`, `factory/stages/package_rfp_response.py`; layout spec in `research-caching-routing.md` §4.2 |
| 5 | **Golden-set expansion + retrieval eval**, wired nightly (matcher replay, FTS P@5/R@5, council stability) | Med-high — de-risks every other item; the path to relaxing TASK-0018's outbound gate with evidence | L-M | GOLDEN markers (`factory/README.md:121-125`); `factory/mutation_testing.py`; matcher gold branches (DECISIONS.md:155) |
| 6 | **Council adjudication before `gate`** (3× pi/omlx blind judges + deterministic Borda → advisory `council_consensus` gate) | Med — catches draft defects pre-Mike, cuts his review load without touching rule 1 | M | Gate registry extension point (`factory/gates/registry.py`, `factory/README.md:137-142`); reviewer-loop tiering (`factory/reviewer_loop.py`); SSSF pi+omlx precedent |
| 7 | **Trace-native token/cost observability** (`stage_usage` table + `cli shows` economics) | Med — makes #4's savings and every run's cost visible; zero new infra | L | `factory/factory.db` tables (`specs/factory-architecture.md:136-140`); `factory/cli.py shows`; future Langfuse only if needed |
| 8 | **Win-theme memory layer** (gbrain/mempalace index over past packets/awards; cited-inputs-only adapter) | Med — compounds with corpus history; differentiator for packet quality | M-H | `assemble/data.json` frozen-snapshot discipline (`specs/factory-architecture.md:167`); provenance gate as the enforcement boundary |

Sequencing logic: 1→2→3 form one dependency chain (the SAM-data flywheel); 4 and 7 are independent quick wins; 5 should land before 6 is trusted and before 3's ranking is tuned; 8 last because it needs accumulated history from 1-2 to be useful.

**Anti-recommendations honored from the research:** no parallel pipeline for delta pulls (swap-in point already reserved); no standing gateway/observability server at solo scale; no stealth/free-pool dependency anywhere in the send path (fail closed instead — `research-free-routing-subscriptions.md` §5.1); Ralph-style unattended build loops contraindicated for anything near deliverables (`research-agentic-engineering.md` §5.2).

---

STATUS: analysis complete
STATE: deliverable written to staging/govcon-overlap-map.md (current-state snapshot w/ file-path citations, SAM delta→FTS corpus design extending ingest, 7-feature swarm map, ranked 8-item roadmap)
NEXT: Mike picks roadmap items; #1 (TASK-0023 delta pulls) + #4 (cache-stable prompts) are the recommended first PRs
BLOCKED-ON: none (read-only session; no repo changes made)
