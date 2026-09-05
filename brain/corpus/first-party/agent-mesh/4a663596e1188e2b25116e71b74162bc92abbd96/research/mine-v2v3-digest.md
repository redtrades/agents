# Mine Digest — openclaw-v2 + openclaw-v3

READ-ONLY mining run · 2026-08-26 · sources: sparse clone `openclaw-v2` (intel/, skills/, services/, app/; single commit `f137d117` "pre-reset ingest+SOTA snapshot 2026-06-02 (#380)") and full clone `openclaw-v3` (single commit `0a586da` "init: openclaw v3 scaffold — courtroom architecture (#1)"). Observer rule observed throughout; nothing under `.archive/` was opened (no `.archive/` exists in this sparse checkout at all).

---

## 1. v2/intel/ — the daily SOTA scans (92 files)

Five parallel series over May 15 – Jun 2 2026 (claude starts 05-15; others 05-16). Format per file: title + scan timestamp → `## Top Findings` (top 3) → raw Atom/changelog excerpts per source. Produced by `skills/sota-scan/run.py` against a chairman-locked watch list.

### Series inventory (every scan)

**sota-claude-*** (19 scans, 20260515–20260602) — sources: anthropic-sdk-python releases, claude-code releases, anthropic-cookbook releases, anthropic.com/news.
| Date | Headline | Takeaway |
|---|---|---|
| 05-15→05-18 | sdk v0.102.0/v0.101.0 stable across days | No new signal; SDK quiet |
| 05-19 | sdk **v0.103.0** lands | Minor bump |
| 05-20→05-21 | sdk v0.103.1 | Patch |
| 05-22 | sdk **v0.104.0** | Minor bump; claude-code feed shows v2.1.139–142 in raw excerpts |
| 05-23 | _(no structured items extracted)_ | Feed-fetch failure day — all 5 series blank |
| 05-24→05-28 | sdk v0.104.1 steady-state | Quiet week |
| 05-29→06-02 | sdk **v0.105.x** (105.1→105.2) | Latest line at snapshot |
Takeaway: mechanical release-feed watch; value is the SDK/Claude-Code version timeline, not prose insight. Claude Code itself was shipping fast (2.1.139→142+ visible in feeds).

**sota-gemini-*** (18 scans, 20260516–20260602) — sources: google-gemini/generative-ai-python releases, cookbook releases, ai.google.dev changelog, deepmind blog.
Every single scan's top finding: **"Archived" — the generative-ai-python repo is deprecated/archived**, frozen at v0.8.2. Takeaway: the one genuinely durable fact in the intel corpus — Google moved off this SDK (to google-genai), and Mike's own v3 later depends on `google-genai`. DeepMind blog / Gemini changelog yielded no structured findings all month.

**sota-hermes-*** (18 scans, 20260516–20260602) — sources: NousResearch Hermes-Function-Calling, Hermes-3-Llama-3.1-8B, Nous-Hermes-2-Pro releases.
All scans identical: "Release notes from Hermes-Function-Calling", zero new releases during the window. Takeaway: Hermes (Nous) was static; note this "Hermes" (the model family) is distinct from the "Hermes" self-evolution agent Mike ran as a service/skill-factory.

**sota-openai-*** (18 scans, 20260516–20260602) — sources: openai-python, openai/codex, openai-agents-python releases, openai.com/news.
| Date range | codex line observed |
|---|---|
| 05-16→05-18 | 0.131.0-alpha.22 |
| 05-19 | 0.132.0-alpha.1 |
| 05-20 | rust-v0.133.0-alpha.1 |
| 05-21→05-22 | 0.133.0-alpha.4 |
| 05-23 | fetch-failure day |
| 05-24→05-26 | 0.134.0-alpha.3 |
| 05-27 | rust-v0.134.0-alpha.4 |
| 05-28 | python-v0.1.0b2 (agents-python?) |
| 05-29→06-02 | 0.136.0-alpha.x |
Takeaway: codex CLI was iterating at near-daily alpha cadence through May 2026 — relevant because Mike routed Hermes/OpenClaw LLM calls through Codex subscription auth.

**sota-openclaw-*** (18 scans, 20260516–20260602) — sources: openclaw/openclaw releases.atom + main CHANGELOG.md.
Daily-to-semidaily beta churn: 2026.5.16-beta.1/2 → beta.4/5/7 → 2026.5.18 → 5.19(+beta) → 5.20-beta → 5.21(-alpha/beta) → 5.22/5.24-beta → 5.25(-alpha/beta) → 5.26 → 5.27 → 5.28(-beta.1/2/4) → 5.29-alpha → 5.30-beta → 6.1(-alpha/beta) → 6.2-alpha. Takeaway: upstream OpenClaw released essentially every day; Mike's v2 tracked it via vendored pin (`skills/vendor/openclaw @ 0db0979`, upstream 2026.5.14). The vendored tree is a full copy of upstream incl. UI/gateway — hence its size.

### Recurring themes
1. **Mechanical density problem** — 92 scans, ~5,100 lines, almost entirely raw feed dumps; only ~1 real insight (Gemini SDK archived). The pipeline worked; the synthesis didn't.
2. **Version velocity as signal** — the only consistently useful data: anthropic-sdk-python 0.101→0.105.2, claude-code 2.1.139→142+, codex near-daily alphas, openclaw daily betas.
3. **Resilience gap** — every series failed identically on 2026-05-23 (`_(no structured items extracted)_`) with no retry/fallback.
4. **Still-relevant today**: the chairman-locked `sources.yaml` watch-list design (official / practitioners / frameworks / awesome-lists tiers, each source mapped to workstreams WS1–WS6, min-relevance ≥4/12 scoring); the practitioner roster (karpathy, simonw, swyx, jxnl, rasbt, lilianweng…); the WS1–WS6 workstream taxonomy itself.

---

## 2. v2/skills/ — the 13 skills

Top-level layout: 11 skill dirs + `adopted/` (4 vendored gbrain skills) + `proposed/` (3 generated proposals) = 13 units. Plus `RESOLVER.md` (routing table) and `vendor/` (upstream trees: gbrain, karpathy autoresearch, hermes ×2, openclaw, symphony, lean, finsvc-plugins — inventory-only, not mined).

| # | Skill | Purpose | Structure quality |
|---|---|---|---|
| 1 | **morning-brief** | Daily 07:00 ET digest: sweeps `knowledge/0-inbox/`, scores signals, adds live PR/session/board/stack sections, writes dated draft, optionally posts Slack #prime / files GH Issue on Project #10 | **Excellent** — full contract (flags table, output list, 10-step protocol, failure-mode table, harness mode w/ JSON-per-stage stdout, idempotent overwrite) |
| 2 | **autoresearch** | Nightly research queue processor: reads `research-queue.json`, WebSearch+WebFetch synthesis per topic → structured frontmatter files in `knowledge/0-inbox/`; owns the canonical signal-scoring formula | **Excellent** — same rigor; queue schema documented, atomic write-back, dry-run/--reset-done CLIs |
| 3 | **sota-scan** | Daily 06:00 ET SOTA sweep of locked source list → scores vs WS1–WS6 (0–2 each, ≥4/12 to include) → files `[event] SOTA digest YYYY-MM-DD` Issue on Project #10 | **Good** — clear scoring model + invocation; thinner than morning-brief; has DR136 SOTA-EVAL gate doc justifying build-from-scratch |
| 4 | **mempalace** | Semantic memory tier #4 of 5 (context → BOOTSTRAP → .agents/memory git-tracked → mempalace vector+graph → Obsidian vault); DR102 query-first mandate; mine-based ingestion; MCP + CLI surfaces; compliance enforced by WS-RECONCILE C20 miss-logging | **Good** — crisp tier model + when-to-query/write; references `~/.mempalace/palace` (912+ drawers) |
| 5 | **url-intake** | Slack #intake poller → fetch → classify (article/repo/doc/video) → 3–5 sentence summary → `knowledge/0-inbox/YYYY-MM-DD-<slug>.md`; CF Browser Rendering fallback; daemon mode | **Good** — classification table + failure modes; superseded-in-waiting by services/intake-pipeline |
| 6 | **stack-diagnostics** | Health probe (processes/disk/launchd/GitHub API) → JSON contract consumed by morning-brief; warn@80%/critical@90% disk thresholds; --fail-on-critical for alerting | **Good** — explicit output schema + consumer interface |
| 7 | **coding-recursive** | Multi-agent coding team (Planner/Researcher/Implementer/Tester/Reviewer/Reflector) w/ quality gates; Reflector persists learnings via commit_transaction to gbrain canonical | **Fair** — role definitions solid but no YAML frontmatter, no CLI/contract section |
| 8 | **gbrain-router** | Strategic-review router: CEO-challenge / office-hours / investigate(5-whys) / retro prompts keyed off trigger words; default synthesizes all four | **Fair** — good prompt craft, no tooling/protocol depth |
| 9 | **long-horizon-durability** | CRH pattern (Checkpoint-Resume-Handoff): checkpoint every 20 turns/15min, handoff brief at turn 80, hard stop 100 (DR014); goal_alignment drift score (>0.7 continue / <0.5 STOP); never resume from raw session JSONL | **Good** — concrete turn-budget table + resume checklist; most scripts still "TO BE WRITTEN" |
| 10 | **trading** | WS7 TSLA wheel/LEAP/swing: Karpathy-autoresearch-pattern loop — fixed backtest.py harness, agent-editable signals/ (rsi, iv_rank, news_sentiment, macro_rates; pure `score(ticker,date)->float`), append-only hypothesis_log; paper_trades tracker CSV + add/report CLIs; composite Sharpe/Calmar/MaxDD score w/ −inf MaxDD floor >20% | **Good** — README carries the loop contract; SOTA-EVAL.md is the self-flagged canonical DR136 violation (rebuilt what vendor/ already had) |
| 11 | **skill-discover** | Capability-gap meta-skill: search-before-build protocol (local → archive → GitHub/MCP registry → docs.anthropic.com), relevance 1–5 scoring, proposal file template, Slack DM notification | **Good** — tight protocol |
| 12 | **adopted/** — brain-ops, citation-doctor, news-ingest, twitter-ingest | Wave-1 ports from garrytan/gbrain (MIT, upstream SHAs pinned in headers): brain read-enrich-write cycle, citation audit/fix, news → brain pages, tweet → people pages | **Excellent provenance hygiene** — Migrated-from comments, SPDX, upstream_sha fields |
| 13 | **proposed/** — ops-auto-execute-misflagged-chairman-keyboard, symphony-p2-smoke-test, url-intake-to-vault-file | Machine-generated proposals (Hermes skill-factory / sub-agents) awaiting review; status: proposed, source trace paths recorded | **Mixed by design** — raw generation output kept out of the live namespace |

### SKILL.md structures captured

**morning-brief/SKILL.md** (the exemplar, 225 lines): YAML frontmatter `{name, version, description, triggers[], tools[], invokes[] (cross-skill deps), schedule {cron, launchd_plist}}` → purpose para → "Data Sources" table (source → command/API → draft section) incl. a literal GraphQL query → **Contract**: input flags table + numbered outputs (draft file w/ frontmatter keys, optional Slack, optional Issue, CTX jsonl append shape) → **Protocol** 10 numbered steps → scoring formula block (`source_reputation × recency_decay × topic_overlap(Jaccard) × entity_novelty × 100/30`) → non-interactive harness mode (JSON-per-stage stdout contract) → **Failure Modes table** → example invocations → implementation pointers → schedule → references. Notable discipline: "canonical source" cross-references to avoid duplicate formulas; scorer config versioning (`scoring_config_version: v1`).

**sota-scan/SKILL.md** (66 lines): frontmatter `{name, description, triggers, tools, invokes, schedule{cron, output: GH issue + project node ID}}` → Invocation (dry-run/date flags) → Output contract (issue title format, labels, inclusion threshold) → Workstream scoring table WS1–WS6. Companion `sources.yaml` (chairman-locked 2026-05-14: 5 official, 14 practitioners, 8 frameworks, 3 awesome-lists, each tagged to workstreams; scoring block `{min_relevance_for_digest: 4, max_findings_per_digest: 10, lookback_hours: 24}`) + `synthesize.md` + `run.py`.

**mempalace/SKILL.md** (104 lines): frontmatter `{name, description, triggers (incl. natural phrases like "has this been decided"), type, dr: DR102}` → 5-tier memory table → palace location/wings → When to query (DR102 MUST-query-first list) → When to write (mine pipeline only, no direct writes) → MCP tool priority order (`mempalace_search/list_wings/list_rooms/get_taxonomy/traverse`) → CLI fallback (`search/status/wake-up` ~600–900 tokens) → 3 concrete use cases → enforcer (C20 miss logging to `dispatch-mempalace-misses.jsonl`).

Common pattern worth preserving: **frontmatter contract → input/output contract → numbered protocol → failure-modes table → cross-references instead of duplication**. Every scheduled skill declares both cron AND launchd plist. Everything appends CTX JSONL in the same turn.

---

## 3. v2/services/ + app/ — inventory (archival record)

### services/ (17 services; production workflow layer; root README indexes them)

| Service | What it did | Tech | Wiring |
|---|---|---|---|
| **intake-pipeline** | Slack #intake URL → r.jina.ai markdown → Haiku classify → `knowledge/0-inbox/` | Python stub+SPEC | 15-min Slack poll; primary vault write path; downstream: daily-brief, aligned-news |
| **daily-brief** | 07:00 ET overnight synthesis (PRs, sessions, vault drops, Project #10 columns, prior SOTA digest) → mobile-readable brief | Python stub+SPEC | Cron 12:00 UTC; consumes intake + sota outputs; successor to skills/morning-brief |
| **aligned-news** | Cross-references SOTA scan + vault clusters vs chairman interests → ranked top-3 "signal that matters" | Python stub+SPEC | 08:00 ET after daily-brief; reuses its vault-drop list |
| **dispatch-tracker** | Watches `.agents/dispatches/<session>/todos.jsonl`, mirrors TodoWrite transitions → GitHub Issues + Project #10 state machine (Backlog→Ready→In Progress↔Blocked→Review→Done); dashboard.html viewer | Python (tracker.py, symphony_client.py), launchd, watchdog FS events | Companion to trio-review; shared file-watch→JSONL→side-effect pattern |
| **trio-review** | Cross-model PR review: 3 reviewer postures (strict/practical/skeptical) → aggregate → auto-merge on consensus, escalate on disagreement | Python (run/reviewers/aggregator/github_io), pytest | Poll/webhook PR events; the M1 meta-layer piece; direct ancestor of v3's judge idea |
| **observable-validator** | Enforces "every dispatch has a Verification observable": pre-dispatch refusal (exit 3) if brief lacks runnable check; retro_score for in-flight briefs | Python (validator/parser/runner/retro_score), pytest | M2 meta-layer; pairs w/ trio (M1) and autofix (M3) |
| **autofix** | Deterministic CI-failure classifier (lint/format vs test/security); security NEVER auto-fixed (DR091/092 revocable bucket) | Python (classifier/fixers/run), pytest, workflow.yml | M3; unblocks lane between trio review and validation |
| **knowledge-bridge** | Stage 2C glue: Obsidian vault (canonical, Pattern A chairman-locked 2026-05-14) ↔ Mem0 (derived projection); entity extraction (4-tier); nightly "dreaming" consolidation; agent facts materialize to `_agent-drafts/` for review | Python (bridge FSEvents watcher, entity_extract, dreaming), pytest | Writes flow Obsidian → Mem0 only |
| **mem0** | Self-hosted semantic memory: mem0 server + Qdrant vectors + Postgres 16 metadata (port 8432 remap), optional Ollama local-LLM embedding (DR086 local-first) | Docker Compose, healthcheck/mem0-startup shell | Backs knowledge-bridge + mempalace tier |
| **autorag-index** | Vault → R2 sync → Cloudflare AutoRAG managed RAG (qwen3-embedding) w/ Vectorize 768d fallback (@cf/baai) | Python (sync_to_r2, query), CF free tier | Query surface over knowledge vault |
| **url-to-md** | Any URL → clean markdown via CF Browser Rendering + R2 cache; #intake Slack poller variant | Python (fetch_md, intake_webhook) | Fetch primitive behind intake flows |
| **slack-bot** | Socket-mode receiver: slack_bolt App, event handlers, slash commands, queue writer; launchd plist `com.openclaw.slack-bot` | Python, slack_bolt | Pairs w/ app/slack-openclaw-bot manifest; token at `~/.config/openclaw/slack-bot-token` (path reference only) |
| **hermes** | Self-evolution serve daemon: observes Symphony Project #10 "In Progress" tasks → codex CLI backend generates skill proposals → `skills/proposed/` | Python package (serve.py), launchd | Feeds skills/proposed/; auth via ChatGPT Plus→Codex routing |
| **litellm** | Free-tier-first LLM router: Groq→DeepInfra→Together→Fireworks→OpenRouter→CF Workers AI | LiteLLM proxy, docker-compose, env-key only | Model access chokepoint pre-v3 (v3 replaced it with cli_router) |
| **rating-loop** | Chairman feedback capture on briefs (Slack reactions 👍👎📌🚫 → 1–5 ratings) → `chairman-preferences.jsonl` rollups → Hermes GEPA tunes content weighting | Python (rating_store, brief_footer, slack_webhook) | Closes loop on daily-brief/aligned-news output |
| **status-broadcaster** | Session state + launchctl daemon status → compact table to #prime via persona-signed post.py | Python | Push-first DR087 signal |
| **cross-source-fanout** | Seed-and-fanout discovery — STUB ONLY ("awaiting PR #333 merge") | Python stub | Never implemented before snapshot |
| **sota-scanner** | macOS scheduling wrapper for the sota scan (LaunchAgent + crontab snippets, install.sh) | Shell/plists | DR136 SOTA-EVAL chose launchd over cron/GHA |

Daily pipeline (ET): 06:00 sota-scan → 07:00 daily-brief → 08:00 aligned-news, with 15-min intake polls underneath.

### app/ (user-facing products & integrations)

| App | What | Tech/State |
|---|---|---|
| **ninov-io** | Stripe-compliant static landing site for ninov.io | Cloudflare Pages + wrangler; deploy blocked pending chairman-created CF API token (documented path `~/.config/cloudflare/ninov-io-token`) |
| **slack-openclaw-bot** | Slack app manifest + install/token runbook (redtrades workspace, free tier) | manifest.yml v2.1; runtime lives in services/slack-bot |
| **finance** | TSLA wheel/LEAP/swing Excel workbooks (CSV blocks: Trade Log ↔ paper_trades tracker.csv must stay in sync, LEAP sensitivity @ Sep 2027, IV-regime ladder) | CSV + Claude-for-Excel sidebar workflow |
| **workers-ai-router** | CF Worker with AI binding | TypeScript, wrangler 3, src/index.ts |
| **symphony-task-board** | Symphony spec → GitHub Projects #10 mapping (Unclaimed/Claimed/Running/Released/Done → Todo/In Progress/Done) | config.yml |
| **openclaw-runtime** | Upstream openclaw runtime config (JSON5, no secrets; auth-profiles.json explicitly NOT committed) | Auth routing directive: Claude Max quota reserved for Dispatch+trio; Gemini free tier primary → Vertex fallback → Ollama offline |
| **gbrain-obsidian-bridge** | Vendor adoption config for gbrain↔Obsidian sync (iCloud inbox path) | config.yml only |
| **hermes-skill-factory** | Upstream skill-factory wired to propose-mode over synthesized event traces | config.yml + events/*.jsonl + codex reauth helper |
| **swarmclaw** | Future SwarmClaw PWA intelligence surface | Not scaffolded; planned Turborepo+Next.js 15+Tailwind 4+Serwist (Issue #138, ADR-014) |

How they wired together: Slack (#intake, #prime, DMs) ⇄ slack-bot/socket layer ⇄ dispatch sessions writing todos.jsonl ⇄ dispatch-tracker → GitHub Projects #10 ⇄ trio-review/autofix/observable-validator guarding PR flow ⇄ knowledge vault (Obsidian canonical) fed by intake-pipeline/autoresearch/url-to-md ⇄ memory planes (mem0+mempalace+autorag) ⇄ briefing plane (daily-brief→aligned-news→rating-loop→GEPA tuning). Scheduling uniformly launchd/cron; LLM access via litellm free-tier router or subscription CLIs.

---

## 4. v2 root — concepts explained

**OPENCLAW.md (constitution, v3.0-v2, 2026-05-12).** Declares v2 a *fresh bootstrap, not a fork*: anything from v1 not migrated by Phase 2 close is "deprecated by omission". Survivors of the v1→v2 break: `scripts/commit_transaction.py` (atomic-write primitive, v1 PR #1982), `scripts/invariant_check.py` (3-state guard, PR #1984), L2 git-hook enforcement of DR080/090/099 (PR #1764) — plus adopted-from-upstream gbrain artifacts (vendor/gbrain submodule, RESOLVER.md, AGENTS.md). §16 lists deliberate exclusions (CTX ledger restarts at 001, semantic.jsonl rebuilt from 30 core DRs, no archive copies). Doctrine highlights: C4 complexity ladder (simple→direct … open-ended→MoA fan-out), A2 autonomy buckets (IN-LOOP for irreversible/credentials/hardware, ON-LOOP default for internal work, OUT-OF-LOOP for housekeeping), three-bucket action model (Revocable execute-never-block / Ambiguous pick-with-rationale / Irreversible STOP-for-chairman), adopt-upstream-first (DR136) with build-plan gate (S1 archive query → S2 INTENT-alignment → S3 SOTA scan → S4 adopt/rebuild/restore), maximal-exec permission posture with human gates only on irreversible actions, never execute trades. Six-agent swarm: prime (orchestrate) / forge (code) / scout (research) / sentinel (health) / operator (ops) / witness-01 (out-of-band audit).

**commit_transaction primitive.** The canonical write path: all meaningful state changes go through an atomic multi-store commit transaction instead of bare `git commit`, paired with `invariant_check.py` run BEFORE any new-writes session as a 3-state drift guard (repo ↔ board/memory ↔ CTX ledger). Same-turn ledger writes (DR090) are the discipline it enforces: every commit/decision/status change hits GH Issue + Project board + PR + CTX + claims.jsonl in one turn. Runbook referenced at `docs/runbooks/commit-transaction.md` (**not present in this sparse checkout** — neither `scripts/` nor `docs/` were included; the primitive survives here only as documentation). Recursive-validation flourish: the bootstrap commit itself was the primitive's first use on the new substrate.

**gbrain-canonical design.** Adoption of Garry Tan's thin-harness-fat-skills pattern via pinned submodule: agent-system doc, resolver routing (`skills/RESOLVER.md`: read gbrain resolver first → OpenClaw override rows win conflicts), canonical memory at `.agents/memory/` (append-only JSONL, corrections by supersede never mutation), Obsidian vault as human-canonical knowledge (Pattern A: Obsidian source-of-truth, Mem0/mempalace as derived projections, agent writes quarantined to `_agent-drafts/` pending chairman review). Fork rule: modify a gbrain skill >20% LoC → fork into `skills/adopted/`; otherwise ride upstream.

---

## 5. v3 — architecture walkthrough

One-commit scaffold (`#1`), clean-room Python 3.12/LangGraph. Tagline: **"a multi-agent system where the generator is never the judge."**

### Prime orchestrator pattern
- `prime/orchestrator.py`: 12-line entrypoint — `run(task)` builds the graph and invokes with a fresh thread_id.
- `prime/graph.py`: LangGraph StateGraph, MemorySaver checkpointer. Nodes: `receive` (writes `spec.yaml` — "nothing is real until it is on disk") → `plan` (LLM picks fanout as YAML; falls back to DEFAULT_FANOUT = two scouts) → `fanout` (ThreadPoolExecutor parallel specialists) → `collect` (dump scored proposals, compute divergence) → conditional edge: divergence >20% ⇒ `debate_loop` (max 1 round: Hermes critiques each artifact, scouts revise once) → `judge` → `synthesize` (winner-as-spine brief w/ Sources) → `land` (gate-check ALLOW/ASK/DENY, append-ledger event, Mem0/local memory write).
- Every stage persists an artifact to `agent_os/cases/<case-id>/`: `spec.yaml`, `plan.yaml`, `proposals/*.yaml`, `verdict.yaml`, `artifact.md` — Git-auditable courtroom transcripts.
- `prime/system_prompt.md` is Prime's character: sole write authority; evidence-or-it-didn't-happen; name-the-failure-mode; the gate is law (never route around ASK/DENY); greenfield (never read legacy `~/.openclaw*` trees — enforced in code too); "There is no pile of numbered rules — the architecture is the rule."

### Specialist/judge topology
- `swarm/specialist.py`: one shared core — load rubric → build prompt → complete → parse scored artifact. Specialists are GENERATORS and never score peers; vendor errors become schema-valid zero-confidence proposals so the courtroom runs on survivors. Roles mirror v2's taxonomy: scout (×2 aliases: grok contrarian / gemini long-context), forge (code), sentinel (health), operator (data moves) — each with a rubric yaml (mandate + scoring axes + emit contract).
- `swarm/judge.py`: evaluates structured artifacts (never raw answers, never its own). `pick_judge_alias()` selects a family matching NO generator — tested invariant; degraded mode still refuses generator families; unparseable verdicts fall back to highest-confidence proposal with `confidence: None` (signaling "no real judge read").
- `swarm/synthesizer.py`: lands the final Markdown brief using winner as spine, grafting corroborating evidence.

### MCP critic role
- `mcp/hermes_critic.py`: Hermes demoted from v2's autonomous service to a **critic at the tool boundary** — given one proposal, returns `{weakness, missing_evidence, risk}` YAML; used by debate_loop; also exposed as FastMCP stdio tool. It critiques, never synthesizes. (Known wart documented inline: local `mcp` package shadows pip SDK for serving.)

### Supporting layers
- `runtime/cli_router.py`: ONE chokepoint `complete(prompt, role)` over OAuth-subscription CLIs (claude/codex/grok) + Gemini AI-Studio SDK — replaces v2's litellm proxy; no per-token API keys; ROLES→vendor and VENDOR_FAMILY maps power the cross-family gate; gemini uses flash for free-tier quota.
- `runtime/gate.py`: deterministic ALLOW/ASK/DENY replacing v2's DR-rule piles — DENY on legacy-tree writes + destructive regexes (rm -rf /, force-push, drop table, fork bomb, mkfs/dd); ASK on commit/push/network/delete/spend; code-as-policy.
- `runtime/ledger.py`: append-only JSONL audit spine. `runtime/memory.py`: Mem0 w/ graceful local-JSONL degradation, same API.
- `agent_os/rubrics/*.yaml`: per-role scoring axes (scout: grounded/contrarian/recency/falsifiable; forge: correctness/tested/surgical/reversible; operator: safe/idempotent/reversible; sentinel: measured/actionable/blast_radius; judge: evidence_quality/failure_honesty/testability/calibration).
- Routines: nightly_audit Cloud routine + launchd heartbeat running `python -m prime` daily. CI: ruff + pytest on uv. PR template requires courtroom trace (case id, generator families, judge family ≠ generators) and a "no code copied from legacy trees" checkbox.

### proposal.schema.yaml (full)
```yaml
$schema: "openclaw/v3/proposal"
type: object
required: [claim, evidence, failure_mode, test, confidence]
properties:
  claim:        # string — the specialist's answer, stated plainly
  evidence:     # array[string] — citations / URLs / file:line / test results
  failure_mode: # string — what would invalidate this claim
  test:         # string — command/URL/query a third party can run
  confidence:   # number 0.0–1.0 — self-estimate used ONLY for divergence detection,
                #   never as the verdict
  role:  {type: string}   # optional runtime metadata for routing/audit
  model: {type: string}
```
Runtime twin: pydantic `Proposal` in `runtime/proposal.py` with lenient coercion (evidence flattening, confidence clamping, `(unspecified)` placeholders) because live models emit loose YAML.

### Golden test case format
`tests/golden/<role>/case{1..5}.yaml` — 20 cases, each exactly one minimal valid proposal (role/model/claim/evidence/failure_mode/test/confidence ≈0.62), e.g. scout case1: "SWE-bench Verified is the current SWE benchmark standard", test "open https://www.swebench.com". Consumed by `test_proposal_schema.py` to prove schema validity across realistic per-role shapes; `test_graph.py` runs the whole courtroom offline via a patched `fake_complete` chokepoint and asserts end-to-end artifact writing, `judge_family ∉ generator_families`, fallback preserves cross-family, and divergence triggers exactly one debate round.

### What "generator is never the judge" meant operationally
1. Structural: specialists emit artifacts; scoring happens in a separate graph node whose model alias is chosen at runtime such that `VENDOR_FAMILY[judge] ∩ {families of generators} = ∅` — asserted in tests and recorded in every `verdict.yaml` (`judge_family`, `generator_families` fields).
2. Informational: judges see labeled proposals with **families withheld** ("judge on merit").
3. No voting: disagreement (confidence spread >20%) routes to a bounded critique-and-revise round rather than majority vote; only the judge ranks.
4. Failure honesty: judges score failure-mode candor and testability, not just correctness; a claim without a runnable third-party test "is a draft".
5. Degradation keeps the invariant: even the fallback path refuses to let a generator family judge, and marks its own verdict `confidence: None`.

It operationalizes v2's `trio-review` (3-postiture cross-model PR review) into a general-purpose evaluation substrate — and echoes Mike's standing rule that a reviewer is never the authoring model.

---

## 6. Secret flags (paths by name only; NO values printed)

No live credentials found in either checkout. All regex hits for token shapes were documentation placeholders (`xoxb-...`) or upstream vendor code. Specific credential-path references (flag-by-name):

- **openclaw-v2**
  - `~/.config/openclaw/slack-bot-token` — Slack bot token store (chmod 600 instructed) — services/slack-bot README
  - `~/.config/cloudflare/ninov-io-token` — CF Pages deploy token, PENDING chairman creation — app/ninov-io README
  - `~/.hermes/auth.json` (stale Codex refresh token flagged in-tree) + `~/.codex/auth.json` import path — app/hermes-skill-factory config
  - `auth-profiles.json` — explicitly excluded from commits (openclaw-runtime config comment)
  - `services/mem0/.env.example` — template only
  - `services/litellm/config.yaml` — all keys via `os.environ/*`, clean
  - Slack IDs hardcoded throughout (channel `C0AQ1R1UK5W` #intake/#prime, `C0AQDLBHZ6C` #prime, DM `U03N5L8TH`) — identifiers, not secrets, but identify Mike's workspace
  - `.gitleaks.toml` present at root (good hygiene)
  - `skills/vendor/**` — huge upstream trees containing token-shaped strings in tests/docs/redaction code; treated as third-party content, not Mike's secrets
- **openclaw-v3**
  - `secrets.env.example` — placeholder template only (`sk-ant-...` etc.), instructs age-encryption for prod
  - `tests/conftest.py` — fake keys (`test-anthropic`), safe
- **`.archive/`**: not present anywhere in the sparse v2 checkout — nothing opened, per instruction; the leaked-credentials zone presumably lives outside the sparse cone.

---

## 7. What makes v2 / v3 worth preserving

**v2** (snapshot of a real operating system, not just code):
1. The **SKILL.md authoring discipline** — frontmatter contract/triggers/schedule → IO contract → numbered protocol → failure-mode table → cross-reference-don't-duplicate. morning-brief + autoresearch are reference-grade templates.
2. **Governance patterns** that survived into everything after: three-bucket action model (revocable/ambiguous/irreversible), adopt-upstream-first gate with written SOTA-EVAL justifications (including honest failure records like trading's DR136 violation), SOTA-EVAL as a build-gate artifact class.
3. **Memory architecture**: 5-tier model, Pattern A canonical-vs-projection split, append-only CTX ledgers, commit_transaction/invariant_check as atomic-write + drift-guard primitives.
4. **The full operating stack record**: 17 services + 9 apps showing how a solo operator wired Slack→intake→vault→RAG→brief→feedback-loop→review-gates, all on free tiers and launchd.
5. The **intel corpus** as a lesson: automated scanning without synthesis yields version timelines, not insight — plus the genuinely durable datum (Gemini generative-ai-python archived) and the chairman-locked watch-list/scoring design.
6. Honest archaeology: proposed/ machine-generated skills kept quarantined; retroactive violation memos; stub services marked as stubs.

**v3** (small, complete, load-bearing):
1. A working reference implementation of **generator≠judge** with the invariant enforced in code, preserved under degradation, asserted in offline tests, and audited per-case on disk.
2. The **scored-artifact schema** (claim/evidence/failure_mode/test/confidence) — a portable unit of currency for any eval or review pipeline; confidence explicitly demoted to divergence-signal, never verdict.
3. **Policy-as-code** gate replacing constitution sprawl (ALLOW/ASK/DENY + greenfield denial of legacy trees), and the principle "behavior in code, character in system_prompt, evaluation in tests."
4. The **subscription-CLI router** pattern (OAuth CLIs + one free API, no per-token keys) with family-based routing — directly reusable.
5. Bounded-disagreement design: debate triggered by measured divergence, capped rounds, survivors-only continuation on vendor failure.
6. Direct lineage: v2 trio-review → v3 courtroom; v2 six-agent taxonomy → v3 rubrics; v2 OPENCLAW.md rules → v3 gate.py. Together the two repos document one continuous design argument about machine reviewability.
