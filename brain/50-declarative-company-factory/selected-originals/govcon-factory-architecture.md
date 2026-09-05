# Factory architecture — stages as pure transforms

**Status: IMPLEMENTED (skeleton + one live proof run).** Code lives in `factory/`;
domain-zero config lives in `domains/govcon/`. This spec is the contract the code
implements — if they disagree, fix the code or dated-revise this file, don't let
them drift silently.

Design principle agreed with Mike: build **one concrete deterministic pipeline
end-to-end first**, then extract the generic core from the working instance —
not the other way around. This document already looks generic because the
govcon pipeline turned out to generalize cleanly, not because genericism was
designed in up front.

Everything downstream of this file inherits the operating rules already in force
for this repo: `AGENTS.md` (fail closed, no claim without a file, nothing ships
without Mike), `sop/SOP-DELIVERABLES.md` (the provenance/citation contract this
architecture mechanizes), and `research/swarm-retrospective/REPORT.md` (the
tuning rules this spec is required to satisfy — see §6).

---

## 1. Core idea

A pipeline is a sequence of **stages**. Each stage is a pure transform:

```
Envelope(s) in  →  stage function  →  Envelope out
```

Agents operate **only inside stages** (today: the `synthesize` stage; `package`
will grow one). Everything *between* stages is typed data plus code — no stage
reads another stage's reasoning, only its validated output file. This is what
makes the pipeline auditable: replaying a run means re-reading files, not
re-running a conversation.

Every stage boundary is **schema-validated, then gated, then fail-closed** — a
stage's output is never trusted because the stage (agent or code) claims it's
correct; it's trusted because the envelope schema check and the declared gates
both passed against the actual bytes on disk. This directly encodes the
`research/local-model-eval/REPORT.md` finding: local-model `response_format`
does not enforce a grammar on this stack (`grammar-constrained decoding is
unavailable; output will not be schema-enforced`) — so gates validate
*after the fact*, structurally, regardless of what any model (local or
frontier) was asked to produce or claims to have produced.

## 2. The envelope

Every stage emits one JSON envelope (`factory/envelope.py`):

```json
{
  "schema_version": "1.0.0",
  "stage": "normalize",
  "run_id": "20260823T151900Z-1a2b3c",
  "inputs": [
    {"path": "ingest/raw/sam_opportunities_filtered.csv", "sha256": "…"},
    {"source_url": "https://s3.amazonaws.com/falextracts/...", "sha256": "…", "retrieved_at": "2026-08-23T15:19:00Z"}
  ],
  "outputs": [
    {"path": "normalize/notices.json", "sha256": "…"}
  ],
  "claims": [
    {
      "text": "normalized 149 Sources Sought notices in the 5 target NAICS",
      "type": "count",
      "value": 149,
      "source_refs": ["normalize/notices.json"],
      "recompute": {"method": "count_json_list", "file": "normalize/notices.json"}
    }
  ],
  "produced_by": {"kind": "code", "id": "factory.stages.normalize:run"},
  "timestamps": {"started": "2026-08-23T15:19:00Z", "finished": "2026-08-23T15:19:02Z"}
}
```

Two kinds of `inputs`/`outputs` refs:

- **`path`** — a file inside this run's directory, produced by an earlier stage
  in the same run. Hash is recomputed and compared at gate time.
- **`source_url`** — an external, out-of-repo source (an API pull, a bulk
  download). Hash is over the bytes as fetched; freshness is judged by
  `retrieved_at`, not by re-hashing a 237 MB file on every gate run.

`claims` is the mechanism that ports `sop/SOP-DELIVERABLES.md` §1.2's "every
number traces to a file" rule into something gate-checkable for *any* domain,
not just a finished deliverable. A claim of `"type": "count"` **must** carry a
`recompute` block — this is the count-recomputation rule from the retrospective
(tuning change #1) made structural instead of aspirational: a stage cannot
assert a count without also telling the gate how to independently recompute it.

`produced_by.kind` is `"code"` for deterministic stages and `"agent"` (with
`id` = model/agent identifier) for agent stages. The schema gate does not treat
these differently — an agent-produced envelope is validated exactly as
strictly as a code-produced one, which is the point.

## 3. Gates (`factory/gates/registry.py`)

Contract: `gate(envelope: dict, ctx: GateContext) -> GateReport`, where
`GateReport = {"gate": name, "passed": bool, "lines": [...], "fails": [...]}`.
Every gate follows the posture already established in `gates/gate_runner.py`
and `site/gates/page_gates.py`: one line per check, fail closed — a gate that
cannot run (missing file, unreadable source, unimplemented check) is a
**FAIL**, never a skip (`AGENTS.md` rule 2).

| Gate | Checks | Status |
|---|---|---|
| `schema` | Envelope has every required key, every ref has the right shape, every claim has `source_refs` (and `recompute` if `type: count`) | **Implemented** |
| `inputs_present` | Every `path` input exists and its hash matches; every `source_url` input has a non-empty hash and `retrieved_at`. This is the retrospective's tuning change #2 (inputs-present gate on agent→agent / stage→stage dispatch), generalized to every stage boundary, not just agent handoffs | **Implemented** |
| `provenance` | Every dollar figure, date, ID, and count-type value named in a claim's `text` is verbatim-findable in the files the claim's `source_refs` point to. Dollar figures floor-truncated per `sop/SOP-DELIVERABLES.md` §1.2 | **Implemented** |
| `count_recomputation` | For every `type: count` claim, independently recompute the count via the claim's `recompute` method against the referenced file and compare to `value`. A count with no `recompute` block is a schema-gate failure before this gate even runs | **Implemented** |
| `freshness` | `source_url` inputs' `retrieved_at` within the stage's configured max age; `path` inputs inherit their producing stage's freshness (transitively — a stale grandparent input fails the child too) | **Implemented** |
| `single_writer` | Within one run, no two stages claim to have produced the same output path (queried from the trace DB, not from the current envelope alone) — the retrospective's tuning change #3, made mechanical rather than a naming convention | **Implemented** |
| `compliance` | Every requirement/question in a `requirements.json`-shaped input has a resolved pointer in the deliverable output | **Stub — binds at `package`, not before.** See `factory/gates/registry.py` docstring |
| `format` | Deliverable-level format rules (POCs present, deadline restated + future, banners, letterhead) per `sop/SOP-DELIVERABLES.md` §2.4/§3.4 G4 | **Stub — binds at `package`** |

`compliance` and `format` are real requirements of the finished deliverable
(SOP §2.4 G1/G4) but have nothing to check before prose exists — `synthesize`
and `package` are still stubs (§5), so these two gates fail closed with
`NOT_IMPLEMENTED` today, exactly like `site/gates/page_gates.py` does for PG1–PG7
before that pipeline had real renders to check. Wiring `synthesize`/`package`
is the trigger to make them real, ported from `gates/gate_runner.py`'s G1/G4
logic, not reinvented.

## 4. The runner (`factory/runner.py`)

`python factory/runner.py <pipeline.yaml> [--run-id ID]` executes a pipeline
spec's stages **synchronously**, in declared order. For each stage:

1. Build a `StageContext` (run dir, this stage's output dir, domain config,
   prior stages' envelopes, `today`).
2. Call the stage module's `run(ctx) -> envelope dict`.
3. Run the `schema` gate first, always, regardless of what the stage declares
   — an envelope that fails structural validation never reaches a
   domain-specific gate.
4. Run every gate the pipeline YAML declares for that stage.
5. Record the envelope and every gate result to `factory/factory.db`
   (SQLite) — table `envelopes` (run_id, stage, seq, path, status, ts) and
   table `gate_results` (run_id, stage, gate, passed, detail_json, ts). This
   is the durable trace; `runs/<run_id>/trace.json` is a git-friendly export
   of the same rows for a specific run, written at the end.
6. **Fail closed.** Any declared gate failing halts the pipeline — later
   stages do not run. The runner prints the failing gate's evidence lines and
   exits non-zero. Per `AGENTS.md`, a pipeline failure is a defect to fix or a
   filed GitHub issue, not something to route around (`skills/rubric-improve`),
   never a silent continue.

`factory/factory.db` is gitignored (a working index, not a source artifact);
`runs/<run_id>/` — envelopes, stage outputs, and `trace.json` — is committed
as the evidence a real run happened, per the retrospective's "verify your own
work by an independent method" pattern (tuning changes list, best-performer
common thread).

## 5. Stage contracts

Pipeline for domain pack zero (govcon sources-sought packet):

```
ingest → normalize → triage → match → assemble → synthesize → gate → package → [Mike review] → deliver
```

| Stage | Status | Contract |
|---|---|---|
| `ingest` | **Real** | Pull the SAM.gov bulk Contract Opportunities CSV extract (free, keyless, daily — `https://s3.amazonaws.com/falextracts/Contract Opportunities/datagov/ContractOpportunitiesFullCSV.csv`, ~237 MB, columns documented in `factory/stages/ingest.py`), cache it locally under `factory/.cache/` (gitignored — too large to commit, re-fetched when the cache exceeds `max_cache_age_hours`), filter to the domain's `notice_type` + `naics_codes` + `active=Yes` + `due_after=today`. Output: `ingest/raw/sam_opportunities_filtered.csv` (small, committed) + one `source_url` input ref recording the full extract's hash and retrieval time. This is the "SAM CSV" leg named in the brief; a `v2`/`v3` SAM Opportunities API leg (`recipes/sam-gov.md`) is the same contract with a different fetch function — swap-in point noted in the module docstring, not built until a second live source is actually needed (freshness/G5 re-fetch already exercises the v2 endpoint per-notice, see `stages/assemble.py`). |
| `normalize` | **Real** | Parse the filtered CSV into the domain's typed notice schema (`domains/govcon/schemas/notice.schema.json`): stable field names, ISO dates, NAICS as a string, POC list. One count claim (notices normalized), recomputed by counting the output list. |
| `triage` | **Real** | Per notice: disqualifier screen (regex trap list from `recipes/govconapi.md` — sole-source intent, vehicle-restricted language, imminent 8(a) set-aside), notice-shape classification (evidence-shaped / questionnaire-shaped / mixed, per SOP §2.1 item 7 / P7), and the candidate-scoring heuristic from `recipes/govconapi.md` "Candidate scoring" (days-to-deadline window, description length, `Section \d` presence, VA/set-aside leverage). Mechanical; final pick is still a human glance per the recipe's own text — this stage ranks, it does not choose. |
| `match` | **Real** | Firm↔notice tiering per `AGENTS.md` "Route, don't dump": **List 1** (firms that merely hold the NAICS — not an audience), **List 2** (firms with a completed award in that NAICS — from a live USASpending `spending_by_award` pull, free/keyless, per `recipes/usaspending.md`, pagination-exhausted), **List 3** (List 2 firms whose award description/PoP-state plausibly overlaps *this* notice — scope-shape heuristic, flagged for human confirmation, never auto-promoted to an audience). If List 3 exceeds 40 firms for one notice, the stage flags the matcher as too loose per `AGENTS.md` — volume is more notices, not a bigger dump. |
| `assemble` | **Real** | Combine one selected notice's `triage` + `match` output into the frozen `data.json` snapshot — the exact analogue of an order's `data/` directory (SOP §1.4) and a content-pipeline page's `data.json` (`specs/content-pipeline.md` §2). This is the artifact the `gate` stage and, later, `synthesize` both read — never the live upstream data again. |
| `gate` | **Real** | Re-run the full gate registry (§3) against every envelope produced so far in the run and write a consolidated `gate/GATE-REPORT.json` — same evidence shape as `GATE-REPORT.md` for a deliverable, generic across domains. This is the mandatory checkpoint before `package` may run. |
| `synthesize` | **Stub — exact contract, no implementation** | **Input:** `assemble/data.json` envelope. **Output:** an envelope with `produced_by.kind = "agent"`, outputs = extracted/drafted content (e.g. `synthesize/requirements.json`, `synthesize/draft_sections.json`), claims for every factual assertion with `source_refs` into `assemble/data.json`. **Model routing (from `research/local-model-eval/REPORT.md`, binding on this contract):** route narrow, closed-ended sub-calls (tool-calling / grounded lookup against already-scoped data) to local; route open-ended extraction, summarization, and drafting to frontier until a `thinking_budget_enabled` experiment or a prompt-decomposition change reopens that question — do not route stage-1-style "extract everything" calls to local based on this contract alone. **Never rely on `response_format`/grammar-constrained decoding for JSON safety** — this stack's `response_format` silently degrades to a prompt suggestion with zero decode-time enforcement (§1 above); the `schema` gate is what actually enforces structure, on either local or frontier output. Raises `NotImplementedError` today; implementing this is TASK-0021 (§7 below). |
| `package` | **Stub — exact contract, no implementation** | **Input:** `synthesize` envelope + `assemble/data.json`. **Output:** `DELIVERABLE.md` (or a public page, per `specs/content-pipeline.md`) + `DELIVERY-NOTE.md`, deterministic template render (`produced_by.kind = "code"`) — never re-invents content, only lays out what `synthesize` already produced and validated. This is where the `compliance` and `format` gates go from stub to real (ported from `gates/gate_runner.py` G1/G4). Raises `NotImplementedError` today; TASK-0022. |
| *(Mike review)* | **Human, never mechanized** | `AGENTS.md` rule 1 — nothing leaves without Mike's approval. Not a pipeline stage; a queue state after `package`. |
| `deliver` | **Not built** | Send/ship/publish, gated on human approval per above. Out of scope until `synthesize`/`package` are real. |

## 6. How this satisfies the retrospective's tuning rules

`research/swarm-retrospective/REPORT.md` "Tuning changes" §1–3 are requirements
on this architecture, not suggestions:

1. **"Any artifact with numbers requires an independent verification method
   before it's declared done."** → the `count_recomputation` gate structurally
   requires a `recompute` block on every count claim; the gate independently
   re-derives the number from the referenced file rather than trusting the
   claim's `value`.
2. **"Inputs-present gate on agent→agent dispatch."** → the `inputs_present`
   gate runs at every stage boundary (stage→stage is the general case; an
   agent stage like `synthesize` is just one instance), not only when an agent
   is involved — a code→code handoff with a missing/stale input fails exactly
   the same way.
3. **"Single-writer + in-file version stamps for versioned artifact
   families."** → the `single_writer` gate makes this mechanical: two stages
   in one run cannot both claim the same output path. `schema_version` inside
   every envelope is the in-file version stamp for the envelope format itself.

## 7. What's proven vs. what's next

`research/swarm-retrospective/REPORT.md`'s own rule (§1 above) applies to this
build: the claim "the deterministic stages work" is not credible from prose
alone. Evidence: `runs/<run_id>/trace.json` plus the committed stage outputs
under `runs/<run_id>/` for one live run against a same-day SAM.gov CSV pull,
through `assemble`, with `gate/GATE-REPORT.json` all-green. See that run
directory for the actual notice, counts, and gate lines — this document
doesn't restate numbers that live there, to avoid the exact stale-duplicate-
number failure mode `AGENTS.md` rule 3 exists to prevent.

Remaining work, tracked on the board:

- **TASK-0021** — implement `synthesize` against the contract in §5, starting
  with the narrow tool-calling sub-calls the local-model eval already found
  reliable (routing lookups against `assemble/data.json`), frontier for
  drafting.
- **TASK-0022** — implement `package`, and with it the real `compliance` and
  `format` gates (port from `gates/gate_runner.py`).
- **TASK-0023** — wire a second live source into `ingest` (SAM v2/v3
  Opportunities API, or govconapi once its rate limit resets — hit 429 on the
  free-tier key during this build, see the `ingest` module docstring) so
  `normalize` can cross-check the bulk-CSV leg against a second feed.
- Second domain proves the "config + templates, not code" claim in §0 —
  not attempted here; `domains/govcon/` is domain pack zero, not yet
  generalized against a second instance.
