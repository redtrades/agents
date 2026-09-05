# INTENT.md — Canonical Direction for OpenClaw

**Last updated:** 2026-04-29 (Intelligence Mesh v2.5 — Autonomy Dial + Goal-First Triage + OpenShell Safety Plane + SwarmClaw V2 Control Plane).
**Status:** CANONICAL. This doc + ADR-003/004/005/006/009/010/011/014 are the current truth.
**Commander:** Mike Ninov.
**Amendment protocol:** §18.

> **Recent amendments since 2026-04-25:** DR082-DR095 promoted (see CLAUDE.md cache anchor section); BOOTSTRAP.md generator landed via PR #1497 + §2.5 Decisions Log via PR #1498; W21 Reconciliation Auditor live (4-hour cron, `ai.openclaw.w21-reconcile`, plist + DR095); Round-1 reconciliation pivot merged via PR #1463; SwarmClaw v1 M1 + M2 in active build (PR #1487 + #1500); Hygiene cleanup PR #1497 + #1502 closed 7 stale PRs and amended DR092 to make user-domain `launchctl bootstrap` revocable.

> **Historical aspirations, preserved for reference only:** ADR-001, ADR-002, BUILD.md v2, and all prior plans / handovers / research / CTX entries. These informed Round 1 but are no longer canonical. When INTENT.md disagrees with any of them, INTENT.md wins.

---

## 0. How to read this document

- INTENT.md is the Mike-authored direction doc. It is the single source of truth for *what we're building*.
- ADR-004/005/006/009/010/011 operationalize this intent — topology, MVP scope, model routing, taxonomy, hardware, composability.
- If a CTX / DR / skill / manifest / ADR-001 / ADR-002 / BUILD.md disagrees with INTENT.md, **INTENT.md wins** until Mike amends it (§18).
- Amendments only via `type: intent-amendment` PR Mike approves.

---

## 0.5 Naming convention — Issue-as-spine (v6)

**Universal pointer:** GitHub Issue ID (e.g. `#1408`). Every concept — strategic, tactical, intent, decision, rule, event — is a GH Issue on Project #9. Metadata that previously lived in compound labels migrates to **Issue type labels + Project #9 fields**.

**Issue type labels:**

| Label | Replaces | Example |
|---|---|---|
| `type:initiative` | Track A/B/C/D | `[Initiative] Track A — Personal force-multiplier` |
| `type:epic` | MVP-##, WS-NAME | `[Epic] MVP-01 Morning Brief`, `[Epic] WS-18 Repo Auditor` |
| `type:story` | (new) | user-visible deliverable beneath an epic |
| `type:task` | (new) | atomic work item |
| `type:question` | Round Q | `[Question] Phase-1.Q10 Pivot criteria for MVP-01` |
| `type:adr` | ADR-### | links to `docs/agent-system/decisions/ADR-NNN.md` |
| `type:rule` | DR### | links to `.agents/memory/semantic.jsonl` entry |
| `type:event` | CTX-### | links to `.agents/memory/context.jsonl` entry |
| `type:commitment` | AC-### | links to `.agents/memory/dispatch-agent-comms.jsonl` entry |
| `type:antipattern` | AP-### | links to `.agents/memory/semantic.jsonl` AP entry |

**Project #9 fields** (replace standalone labels):

- **Iteration** — Sprint-0, Sprint-1, Sprint-2, …
- **Milestone** — Phase-1, Phase-2, … (GH-native milestones)
- **Priority** — P0 / P1 / P2 / P3
- **Agent** — prime / forge / scout / sentinel / operator / mike
- **Status** — Backlog / Ready / In Progress / Review / Done / Blocked

**Cross-cutting labels (kept):** `track:<a/b/c/d>` (initiative linkage), `area:<name>` (e.g. `area:morning-brief`, `area:harness`).

**Title / branch / PR / commit format:**

- Title: `[<type>] <verb-led description>`
- Branch: `<type>/<gh-id>-<slug>` — e.g. `feat/1408-launchd-installer`
- PR title: `<type>(<scope>): <subject> (closes #<gh-id>)`
- Commit trailer: `Refs: #<gh-id>` (in addition to `[via dispatch-...]`)
- Doc cross-ref: `gh_issue: <id>` in CTX/DR/ADR frontmatter

**Killed (per "cleanest break"):**

- `mvp:01..04`, `ws:harness`, `ws:vector` — superseded by `type:epic` + Issue title
- `q:1..11` — superseded by `type:question`
- `round:1..3` — superseded by Project #9 Iteration
- `phase:1..2` — superseded by Project #9 Milestone
- Compound `MVP-##-X.Y.Z` coordinate — retired entirely

Single-letter `A/B/C/D` reserved for tracks (initiatives) only.

**Backward compatibility:** existing CTX/AC/AP/DR entries with v1–v5 compound labels are NOT mutated per DR046 (immutable history). New entries use `gh_issue:` field. The 21 seed Issues (#1408..#1428) are migrated in PR #1455: titles updated to `[<type>] …` form, `type:*` labels added, legacy `mvp:`, `ws:`, `q:`, `round:`, `phase:` labels stripped.

**Codified as DR081 (Issue-as-spine, supersedes DR078). Anchor rule from DR080 still applies.** Enforced by `scripts/audit/checks/issue_as_spine_compliance.py` (report-only until 2026-05-01). See [ADR-009](docs/agent-system/decisions/ADR-009-issue-as-spine-taxonomy.md) for full rationale + migration plan.

---

## 1. North star

**OpenClaw is a personal force-multiplier first, product path second.** Mike directs; the swarm executes, proposes, and compounds. The purpose is to turn Mike's attention into leverage — his research into durable knowledge, his code intent into shipped software, his meetings into structured artifacts, his evenings back into his family — and, separately and downstream, to become a product that other operators can adopt.

Round 1 ranking (2026-04-24): **A → C → B, no D.**

- **A (primary) — Personal force-multiplier.** Compound Mike's attention, memory, and decision velocity across research, coding, homelab, and communication.
- **C (secondary) — Product path.** Package the substrate so other single-operators can adopt it. Secondary — only pursued after A is reliably delivering daily value.
- **B (tertiary) — Agent-research platform.** W8 tournaments + GEPA + AI Scientist Loop are legitimate future capacity, but not the driver. They're in-scope when they serve A or C, not ends in themselves.
- **D (rejected) — Vendor lock-in.** No architecture that assumes Claude Code, Gemini CLI, or any single harness. Rejected explicitly.

Everything else in INTENT.md derives from this ranking.

---

## 2. Top 3 jobs (Round 1 Q2)

Ranked by marginal-value-per-week-to-Mike:

1. **Research + vault** — URL intake, signal scoring, knowledge filing, cross-referencing, entity extraction, Karpathy-style LLM Wiki. Sources: Aligned News, GitHub awesome-lists, RSS, X (via xAI native), YouTube transcripts, Otter.ai meetings. Output: morning brief + durable second brain.
2. **Coding** — PRs, patches, tests, refactors, migrations. Includes this repo's own rebuild, homelab tooling, and future SwarmClaw. Agents draft; Mike reviews.
3. **Swarm self-improvement** — the swarm gets more useful week-over-week by compounding its own learnings (CTX ledger, feedback memory dual-write, W18-style auditors, retros). Intentionally the third priority — it serves jobs 1 and 2, not the other way around.

Jobs deliberately NOT on the list right now: homelab infra ops (runs in background, not a primary driver), photo vault migration (operational, not strategic), product-facing SwarmClaw (deferred to C).

---

## 3. Interaction stack (Round 1 Q3)

Priority-ordered. Each tier adds surface area without replacing the previous.

1. **Slack** — primary, cross-device, async. Matches the Dispatch-orchestrator-to-workers model. Every material event lands as a DM to `U03N5L8TH` or in a relevant channel thread. ACPX pattern: agent-to-agent comms also flow through Slack threads so Mike can audit in real time.
2. **GitHub project board** — work-laptop DLP path. Work laptop can't export data; GitHub is the only interface. Agents draft markdown to the board; Mike pulls from work laptop.
3. **SwarmClaw PWA** — **The Control Plane** (M1 done 2026-04-26; v2 Intelligence Surface in active build). The primary governance layer for the swarm. Mike manages agent state, approvals, and attention from a single unified surface.
    - **Shared Autonomy Dial:** Global toggle (Watch / Assist / Auto) to manage risk and cognitive load. Default: Assist (HITL gates enabled).
    - **Attention Triage:** Goal-first hybrid UX. PWA prompts for active focus on startup to dampen noise and amplify relevant agent activity.
    - **Deep Explainability:** Surfaces instructions, rationale, context, and trade-offs for every ranked item or proposed action.
    - **Outcome Previews:** Visualizes "projected results" from OpenShell simulations before execution.
4. **Voice via Meta Ray-Bans** — long-term Jarvis. Vision-claw / open-glasses pattern. See §12 for prereqs.
5. **Typed chat at desk (Dispatch)** — ongoing baseline; not going away.

### Autonomy — Intelligence Mesh (v2.5) Shared Model

Replaces the old tiered-by-task model with a **Shared Autonomy Dial** integrated into the Control Plane:

- **Watch Mode:** Read-only; monitor agent reasoning and telemetry without intervening.
- **Assist Mode (Standard):** Agents propose paths (ADR-014 Rationale/Trade-offs); Mike approves or steers Bucket 2/3 actions via SwarmClaw/Slack.
- **Autonomous Mode:** Agents execute within pre-authorized budget and safety (OpenShell) policies.
- **Context-Aware Failover:** Autonomy automatically drops to Assist when the swarm detects low confidence or high-stakes ambiguity.

**Default permission posture:** Prime + OpenClaw + Slack agent surfaces operate at MAXIMAL permissions by default. Restrictions are explicit (HUMAN-IN-LOOP gates listed above). Codified as **DR083 (DR-MAXIMAL-PERMISSION-AGENT-FIRST)**. Prime specifically has full exec authority — distinct from Dispatch which is bound by DR001 separation-of-concerns. Codified as **DR085 (DR-PRIME-FULL-EXEC)**.

### Composable architecture — body / brain / mind

Mike verbatim 2026-04-24: *"I still want to have the agnostic, genetic harness and plug-in play brain and body so that any model can be implemented into the baseline or any of the other agents. This needs to be agnostic… Think of composable modular architecture, but for agentic swarms."*

- **Mind (declarative, in git):** CORE_LAWS, INTENT, BOOTSTRAP, manifests, skills, memory, CTX ledger. The bootable mind any harness reads.
- **Body (harness):** Claude Code CLI, Codex CLI, Gemini CLI, Jules cloud, Antigravity, OpenHarness, future harnesses. Translates Mind → native tool-use.
- **Brain (LLM):** Claude Opus/Sonnet/Haiku, Gemini Flash/Pro/Ultra, GPT-5.4/Codex, Qwen/Llama/DeepSeek local. Injected at runtime via LiteLLM / MCP / native adapters.

The SAME role manifest must bootstrap correctly as any (body × brain) pairing. Vendor-locked paths are rejected (the "no D" answer in §1).

See [ADR-004](docs/agent-system/decisions/ADR-004-baseline-5-on-demand-n-composable-architecture.md) for the operational detail.

---

## 4. Agent topology — baseline 5 + on-demand N + ephemeral cloud

Replaces ADR-001 §1's 5-agent lock and the historical 17-agent "always-on" framing from CTX-113/140.

### Tier 1 — Baseline (5, persistent, harness-agnostic)

| Agent | Role |
|---|---|
| **Prime** | Orchestrator; planning, delegation, full exec authority (DR085) |
| **Forge** | Code, PRs, tests |
| **Scout** | Research, URL intake, signal |
| **Sentinel** | Observability, security, drift |
| **Operator** | Infra, storage, cron |

Baseline MAY run via Claude Code on M1 Max (current convenience); MUST also run via Codex CLI / Gemini CLI / OpenHarness / Jules / any future harness that can clone the repo. Per **DR084 (DR-NODE-COMPOSABILITY)**, every baseline role has a primary substrate + at least one backup substrate; failover is config-swap, never code edit.

### Tier 2 — On-demand specialists (manifest blueprints, NOT always-on)

The 17 Gas Town manifests (`sisyphus`, `prometheus`, `judge`, `hephaestus-01..06`, `scout-01..08`) are **blueprints**, NOT always-on deployments. Spawn when work needs their specialization:

- `judge` — spawned when a tournament needs scoring.
- `hephaestus-05` (Knowledge Specialist) — spawned when research synthesis is requested.
- `prometheus` — spawned when adversarial planning review is needed.
- `scout-01..07` — spawned for parallel research sub-tasks.
- `scout-08` — spawned for local-inference-heavy work.

Spawn mechanisms: Claude Code Agent sub-tool (in-session), k8s Job/Knative (when cluster up), ephemeral cloud agent (Jules/Codex for skill-variant work). **Terminate on task completion.** Cost + coordination overhead scale with actual work, not roster size.

### Tier 3 — Ephemeral cloud agents

Jules, Claude Code CLI cloud, Codex CLI cloud, Antigravity (Gemini). Run in someone else's VM/container. Lifecycle:

1. User/Dispatch queues work → commits to GitHub project board.
2. Cloud VM spins up, pulls: deterministic container image (GHCR), repo state (git clone), role manifest (from `.agents/registry/manifests/`).
3. Cloud agent becomes worker for the specific task.
4. Works, communicates via Slack threads + commits to GitHub + writes CTX entries.
5. Terminates when task done.

**GitOps is the reconciliation layer.** Nix flake + OCI image + devcontainer.json guarantee env parity with local.

### Resolving the "framework says 8-10 agent ceiling" tension

Flat always-on topologies cap at 8-10 agents. Mike's model is NOT flat always-on — it's baseline 5 + ephemeral N. Ephemerals don't coordinate via live handshakes; they coordinate through GitHub + Slack asynchronously. Kubernetes runs 100+ pods for the same reason. Greenfield PR #1350 was right that "we don't need 22 running pods" — but wrong to delete the 17 manifests (those are blueprints, not stale code). **Baseline 5 + 17 blueprints + N cloud ephemerals = the correct roster.**

### 4.4 Agent identity tier (WS-AGENT-IDENTITY → Issue #1503)

Persistent identity across the swarm so commits, emails, Slack messages, and GH actions carry agent attribution distinct from `redtrades` (Mike). Operationalizes DR073 (`prime_access:`) at the credentials layer.

- **Tier 1 emails (5 baseline + witness)** on `ninov.io` via Cloudflare Email Routing → forward to Mike's primary inbox. Format: `prime@ninov.io`, `forge@ninov.io`, `scout@ninov.io`, `sentinel@ninov.io`, `operator@ninov.io`, `witness@ninov.io`.
- **Tier 2 emails (on-demand specialists)** per blueprint when spawned — `<blueprint>@ninov.io` (e.g. `judge@ninov.io`, `hephaestus-05@ninov.io`). Routed identically.
- **GPG key per agent** for commit signing. Co-author trailers (`Co-Authored-By: <Agent> <agent@ninov.io>`) on every agent-authored commit so `git log --author` filters correctly.
- **Optional GH bot accounts** (alternative path): one bot user per Tier 1 agent if Mike prefers commit-author distinct from co-author trailers. Trade-off documented in Issue #1503.
- **Email-as-signal loop:** Gmail filters route `to:agent@ninov.io` → label `openclaw/agent/<name>` → SwarmClaw poller reads via Gmail API → drops into action-signal ledger (§20). Closes the inbound side of the recsys spine.

Tracking: Issue #1503 `epic(WS-AGENT-IDENTITY)`. Land plan: Cloudflare Email Routing first (cheap, reversible); GPG keys second (per-agent setup script); GH bot accounts deferred until Mike picks A/B between co-author trailers vs distinct authors.

---

## 5. MVP — Phase 1 (Round 1 Q4 + Q9 metrics + Q10/Q11 pivot criteria)

Four MVPs are now in scope (Round 1 expanded Q4 from "two outputs" to "four sequenced deliverables"). MVP-01 + MVP-02 ship together as Phase 1; MVP-03 + MVP-04 follow as Track-C and substrate work.

> **Sprint 0 prerequisite:** WS-HARNESS (agnostic harness foundation, PR #1399, CTX-178) shipped 2026-04-24. WS-HARNESS is ongoing maintenance, not a one-off MVP — see §0.5 for the orthogonal Sprint/MVP/WS taxonomy and §16 for the sprint chain.

### MVP-01 — Morning Brief + Second-Brain Extraction (Sprint 2 deliverable)

Daily 07:00 ET (production cadence; plist fires 06:30 ET to allow ~30min synthesis pipeline). Scout + Prime produce a **rich** morning brief that includes:

- P0 / P1 / P2 tiered items (blockers / active / queued).
- Cross-references: items link to the relevant CTX entry, PR, file path, or vault note.
- **Karpathy LLM Wiki entity extraction** on overnight research intake — people, companies, technologies, papers, URLs. Entities land in the Obsidian-compatible second brain under `~/.openclaw/knowledge/entities/`.
- Delivered to Slack DM `U03N5L8TH`. Mobile-readable.

**DONE criteria (Round 1 Q9 — Opt B, 4 metrics):**
- [ ] Runs unattended for **7 consecutive mornings** without manual intervention.
- [ ] **≥80% of overnight intake items** land in the brief with a correct cross-reference.
- [ ] Mike can click an entity in a brief → land in the vault note for that entity (**100% click-through correctness**).
- [ ] **Under 800 chars** headline + collapsible detail (mobile-friendly).

### MVP-02 — Lean Meeting → Draft Pipeline (Sprint 3 deliverable)

Triggered by Otter.ai recording completion. Produces a **rich** meeting artifact:

- Actions (with owner + target date).
- Decisions (with rationale).
- Attendees.
- Draft emails (one per attendee requiring follow-up).

**DONE criteria (Round 1 Q9 — Opt C, 5 metrics, hallucination-first stricter):**
- [ ] End-to-end: Otter recording available → structured artifact + draft emails **within 10 min**.
- [ ] **≥80% of actions** have correct owner + reasonable target date.
- [ ] Draft emails sit in Mike's Gmail drafts with the right recipient + subject.
- [ ] **Hallucination check:** zero fabricated attendees, decisions, or action items across 7 consecutive meetings (sampling: Mike spot-checks 1 per meeting).
- [ ] DLP-safe path when the meeting is work-sensitive (local Ollama/vMLX only; see ADR-006 §DLP).

### MVP-03 — Track-C SwarmClaw "Vertex" prototype (Sprint 4 deliverable, gated)

Public-facing single-operator template. Externalize the substrate (manifests, harness, baseline 5, MVP-01/02 templates) for one external operator to adopt. **Gated behind Q12 stage-gates** — see §5.1 below.

**DONE criteria (Sprint 4 — preliminary):**
- [ ] One non-Mike user runs MVP-01 from a clean clone within 24 hours of repo handoff.
- [ ] Onboarding produces a working morning brief for that user's sources.
- [ ] Repo doesn't expose any of Mike's secrets / contacts / personal data.

### MVP-04 — Substrate re-evaluation (Sprint 5 deliverable)

After MVP-01/02/03 ship, **re-evaluate the harness + topology + routing decisions** with operating data. Specifically:

- Did baseline-5 actually serve A's daily value? Or did we need 7? Or 3?
- Did Tier-3 ephemerals actually solve the bursty workload pattern?
- Did the budget routing (§7) hold under real load?
- What did the on-demand specialists actually do?

**DONE criteria:**
- [ ] Quantified retro: every claim in INTENT.md §3/§4/§7/§8 either confirmed by 30 days of data or flagged for amendment.
- [ ] Resulting INTENT amendment PRs filed (or "no change needed" CTX).

### Deliberately NOT in MVP Phase 1

- SwarmClaw PWA (Phase 4 per §12).
- Voice/Ray-Bans interaction (Phase 4).
- k8s cluster rebuild + Flux reconcile (Phase 3; blocked by OrbStack rebuild).
- W8 Tournament runner + Research Synthesis (Phase 4/5 gates; awaiting Mike approval per prior INTENT versions, still pending).
- Cross-vendor auto-handoff via COMMANDER-HANDOFF.md (discipline remains; automation is §11).

See [ADR-005](docs/agent-system/decisions/ADR-005-mvp-phase-1-morning-brief-plus-lean-meetings.md) for implementation detail.

---

## 5.1 MVP pivot criteria (Round 1 Q10 / Q11 / Q12)

Each MVP has explicit pivot rules so we don't burn weeks on a deliverable that's failing silently.

### MVP-01 pivot — Q10 Opt B: metric-triggered + time-box

Pivot conditions (any of):

- **Metric:** 7-day rolling rate of "Mike opens brief on phone within 1 hr of delivery" drops below 50 %.
- **Metric:** ≥3 consecutive mornings missed (bug, infra, or zero-input).
- **Time-box:** Sprint 2 + 1 sprint of grace = max 4 sprints from kickoff to either DONE-met OR pivot.

On pivot: drop richness, ship a minimal "P0 only" morning brief; re-scope back to MVP-01 spec only after the minimal version is reliably delivered for 14 days.

### MVP-02 pivot — Q11 Opt C: hallucination-first stricter

Pivot conditions (any of):

- **Hallucination signal:** any meeting in a 7-day window contains a fabricated attendee, decision, or action item that Mike catches.
- **Latency:** end-to-end > 30 min for 3 consecutive meetings (10 min target × 3).
- **Owner-correctness:** owner-assignment accuracy drops below 60 % on a 5-meeting sample.

On pivot: drop draft-email generation; ship structured artifact only. Re-add drafts only after 14 days of zero-hallucination structured artifacts.

### MVP-03 (Track-C) pivot — Q12 Opt E: defer + stage-gate

Track C is **gated**, not in flight. Stage-gates in order:

1. **Gate-1 — Demand signal.** Mike or one external operator explicitly asks for the substrate to be templatable.
2. **Gate-2 — Substrate stability.** MVP-01 + MVP-02 both in DONE state for ≥30 days.
3. **Gate-3 — Capacity check.** Spend < 50 % of weekly budget on A; have headroom for C.

If any gate fails, file `WS-MARKET-RESEARCH` Issue (closes #TBD when filed) and re-evaluate at next monthly retro. Do not start Track-C work without all 3 gates green.

### MVP-04 pivot — none required

MVP-04 is the retro itself. Skipping it = not pivoting; just deferring the next iteration of INTENT.md. Acceptable up to one quarter post-MVP-01 ship.

---

## 6. Sources (Round 1 Q5)

What the Scout tier pulls from, in priority order:

| Source | Access path | Freshness | Notes |
|---|---|---|---|
| **Aligned News** | RSS / API | Hourly | Pre-curated signal from Mike's allowlist; high signal-to-noise |
| **GitHub awesome-* lists** | RSS of releases + scheduled scrape | Daily | awesome-claude-code, awesome-mcp-servers, awesome-claude-plugins, awesome-claude-skills |
| **RSS feeds** | Standard RSS | Configurable | Mike's subscribed feeds; lands in intake pipeline |
| **X (Twitter)** | xAI native API | Real-time | Uses xAI subscription, not scraping |
| **YouTube** | Transcripts via yt-dlp + LLM summary | On-demand | Queue from Slack: paste URL → Scout fetches transcript + summary |
| **Otter.ai** | Otter MCP / API | Post-meeting | Triggers MVP-02 pipeline |

Non-sources (intentionally off-list right now): Reddit, HN (available via /last30days skill on demand, not continuously), TikTok, Polymarket. Too noisy for the signal bar Mike wants.

---

## 7. Budget + model routing strategy (Round 1 Q6 + DR086)

**Subscriptions first.** Existing paid subscriptions are sunk cost; use them before burning anything marginal. Routing priority is now codified as **DR086 (DR-RESOURCE-ALLOCATION-PRIORITY)**:

> Route workloads in this order: (1) local sunk-cost compute, (2) paid subscriptions already owned, (3) generous free tiers, (4) paid API overflow up to $100/mo. Override only when higher-tier option is materially better.

### Tier 1 — Subscriptions (already paid)

| Service | Monthly | What it covers |
|---|---|---|
| **Claude Max** | $200 | Opus 4.7 / Sonnet 4.6 / Haiku 4.5 via Claude Code + Dispatch |
| **Gemini AI Ultra** | $124 | Gemini 2.5 Pro / Flash / Flash-Latest; includes AI Studio + Vertex quota |
| **Antigravity** | 25k credits | Gemini-powered autonomous workers |
| **xAI subscription** | (existing) | Grok-4 / Grok-4-fast native; X data access |
| **Codex OAuth (ChatGPT)** | (existing plan) | gpt-5.4 / gpt-5.5 / gpt-5.3-codex via Codex CLI |

### Tier 2 — Local compute (sunk cost)

- **M1 Max 64 GB** — primary; Ollama + vMLX.
- **M1 16 GB** — secondary Mac peer.
- **PC tower (i7-4790k + 32 GB DDR3 + GTX 980 Ti + 500 GB SSD + USB3 archives + DroboFS)** — Linux substrate / storage hub / GH runner / Ollama / nomic-embed / whisper.cpp. See §8 + ADR-010.
- **Raspberry Pi (existing)** — edge infra: DNS / observability collector. See §8.

Fully autonomous research + eval workloads run on Tier 2. Budget constraint = electricity + wall-clock, not tokens.

### Tier 3 — Free tiers (generous)

- **Gemini AI Studio** free tier — first stop for Prime / Scout exploratory work.
- **GitHub Models** — limited but useful for tail tasks.

### Tier 4 — Overflow ($100/month budget)

Cap on Tier 1 exhausted? Overflow spend goes to **xAI Grok** (primary overflow — Mike already has the subscription + xAI's pricing fits the budget best). Not Anthropic API, not OpenAI API key.

### Routing logic (summary; full detail in ADR-006)

- **Default primary per agent** is chosen by task + DLP + budget, not by vendor preference.
- **Prime:** `gemini-ai-studio/gemini-flash-latest` (free-tier-first) → `vertex-ai/gemini-2.5-pro` → `openai-codex/gpt-5.4` → `anthropic/claude-opus-4-7` last resort.
- **Forge / Scout / Sentinel / Operator:** Haiku/Sonnet-cheap-first, Gemini Flash free-tier for the tail, local Qwen/Ollama for DLP-sensitive paths.
- **DLP-sensitive path** (work-sensitive meetings, credentials, personal data): local Ollama / vMLX only. Never calls a cloud API.
- **Overflow spend** on Grok, not Anthropic/OpenAI API.

See [ADR-006](docs/agent-system/decisions/ADR-006-model-routing-strategy-subscription-tiered.md) for the full routing table + DLP policy.

---

## 7.1 Build / host / route decision matrix

For each WS / MVP, the canonical compute tier (per DR086 §7):

| Workstream / MVP | Compute tier | Default substrate | Backup substrate | DLP | Notes |
|---|---|---|---|---|---|
| MVP-01 Morning Brief | Tier 1 (sub) → Tier 3 (free) | Claude Max (Opus reasoning) + Gemini Flash free-tier (synthesis) | Local Ollama on M1 Max | non-DLP | xAI overflow if cap |
| MVP-02 Meeting Pipeline | Tier 1 / Tier 2 | Claude Sonnet + Otter MCP | Local Ollama (DLP) | conditional | DLP path forces Tier 2 only |
| MVP-03 Track-C Vertex | Tier 1 + Tier 3 | Gemini Vertex-AI | Claude Max | non-DLP | Gated per §5.1 |
| MVP-04 Substrate re-eval | All tiers | (analysis only, no inference) | n/a | n/a | Retro work |
| WS-HARNESS | Tier 1 + Tier 2 | Claude Max (Opus) | Codex CLI / Gemini CLI | non-DLP | Cross-vendor by design |
| WS-W18 Repo Auditor | Tier 2 + Tier 3 | Local Ollama qwen-coder | Claude Haiku | non-DLP | Hot-loop check |
| WS-W10 Intake | Tier 3 + Tier 1 | Gemini Flash free-tier | Haiku | non-DLP | High-volume |
| WS-VECTOR (future) | Tier 2 | M1 Max nomic-embed-text | PC tower nomic-embed | DLP | All embeddings local |
| WS-PHOTO-VAULT | Tier 2 | PC tower (storage hub) | M1 Max | DLP | Personal data |
| WS-PC-TOWER-BRINGUP | Tier 2 | PC tower itself | n/a | n/a | One-time bringup |
| WS-MARKET-RESEARCH | Tier 3 + Tier 1 | Gemini Flash | Claude Haiku | non-DLP | Spawned when Track-C Q12 fails Gate-1 |

**Override rule:** an agent may pick a higher-cost tier when the next-best tier is materially worse for the task (e.g. Opus reasoning vs Haiku for a high-stakes plan). The override goes in a CTX entry with `type: routing-override`.

---

## 8. Hardware (Round 1 Q13 — Opt C+E)

The OpenClaw compute fleet is multi-substrate by design (per DR084 — composability).

| Node | Spec | Role | Substrate |
|---|---|---|---|
| **M1 Max 64 GB** | macOS | Daily driver; primary harness host; Ollama + vMLX local inference | macOS |
| **M1 16 GB** | macOS | Mac peer; backup harness; iCloud bridge | macOS |
| **PC tower** | i7-4790k + 32 GB DDR3 + GTX 980 Ti + 500 GB SSD + USB3 archives + DroboFS | **Linux substrate + storage hub + GH runner + Ollama + nomic-embed + whisper.cpp** — Proxmox VE 8 hypervisor; ZFS pool serves NFS/SMB | Linux (Proxmox + Debian/Ubuntu VMs) |
| **Raspberry Pi** | (existing, low-power) | Edge infra: DNS / observability collector / ingress | Linux (Pi OS) |

**Key shifts vs prior INTENT (Round 1 Q13 Opt C+E):**

- The PC tower is **not** a desktop — it's a **Linux substrate + storage hub**. Proxmox hypervisor; Debian/Ubuntu VMs; ZFS for storage. It serves the Macs via NFS/SMB.
- The PC tower hosts a **self-hosted GH Actions runner** so CI workloads stop racing the M1 Max for compute.
- **Composability is enforced (DR084):** every role / agent / MVP runs on ≥2 substrates. Failover via config swap, not code edit.
- Storage media: 5 TB external + 24 TB pool + 2 TB SSD + 1 TB NVMe + DroboFS legacy → all federated via ZFS pool on the tower; NFS exports map to Mac mount points.
- See [ADR-010](docs/agent-system/decisions/ADR-010-pc-tower-topology.md) for the full PC tower bring-up plan and [ADR-011](docs/agent-system/decisions/ADR-011-node-composability.md) for the multi-substrate failover model.

---

## 8.1 Storage taxonomy (Round 1 Q14 — Opt D: hybrid per content type)

Different stores for different artefact types. No monolith.

| Content type | Store | Path / mount | Backup | Retention |
|---|---|---|---|---|
| Code (this repo) | git + GitHub | `~/.openclaw/` + `redtrades/openclaw` remote | GitHub mirror + iCloud rsync | git history |
| CTX / DR / AC ledgers | git (JSONL) | `.agents/memory/*.jsonl` | git + Cowork mirror | append-only forever |
| Research vault (entities, briefs, summaries) | Obsidian-compatible MD | `~/.openclaw/knowledge/` | git + iCloud + ZFS pool | forever |
| Meeting artifacts | MD + JSON in repo | `docs/meetings/<date>/` | git | forever |
| Otter recordings (raw) | Otter cloud | (vendor) | n/a (vendor) | vendor-managed |
| Photos | folder-per-person on ZFS | tower:/tank/photos/<person>/ | offsite + Apple Photos export | forever |
| Sessions / transcripts | rsync to 2TB external + git | per CTX-173/176/CTX-145 | offsite copy | indefinite |
| Secrets at rest | SOPS+age, in-repo | `manifests/secrets/*.sops.yaml` | git + 1Password vault | rotated |
| Secrets at runtime | 1Password CLI | `op run` | 1Password sync | live |
| Local model weights | Ollama / MLX cache | `~/.ollama/`, `~/.cache/mlx/` | regenerable | refresh quarterly |
| LLM observability traces | Langfuse self-host | K3s / on tower Postgres | ZFS snapshot | 90 days rolling |
| Build artifacts (OCI images) | GHCR | `ghcr.io/redtrades/openclaw/*` | regenerable | refresh per release |

**Rule:** if a piece of state isn't in this table, it doesn't get persisted — it's runtime cache and regenerable. Adding a row requires a CTX `type: storage-amendment` and INTENT amendment PR.

---

## 9. Slack — canonical channel layout (Round 1 Item 5 — 17 channels)

Five categories. Mike's user ID is `U03N5L8TH` for direct DMs.

### Ops (5)

| Channel | Purpose |
|---|---|
| `#dispatch` | Orchestrator updates, agent comms backbone |
| `#prime` | Prime-led decisions, morning brief deliveries |
| `#alerts` | Sentinel + Operator alerts (drift, security, infra) |
| `#bot-feedback` | Mike's feedback to bots; corrections, preferences |
| `#observability` | Langfuse summaries, OTel digest, metrics |

### Personal (3)

| Channel | Purpose |
|---|---|
| `#mike-private` | Mike's brain dump; personal scratchpad ingested by Scout |
| `#mike-tasks` | Mike's todo / capture |
| `#mike-mood` | Optional mood / energy log feeding morning brief context |

### Knowledge (4)

| Channel | Purpose |
|---|---|
| `#intake` | URL drops, paste-from-anywhere → Scout pipeline |
| `#research` | Research digests, awesome-list updates, daily curated |
| `#meetings` | Otter triggers, draft artifacts, follow-up emails |
| `#vault` | New entity entries, second-brain growth log |

### Professional (4)

| Channel | Purpose |
|---|---|
| `#work-bridge` | Work-laptop ↔ home bridge; GH-mediated DLP-safe artifacts |
| `#projects` | Active projects (per Project #9 milestones) |
| `#decisions` | Mike-approved decisions; ADR / CTX events |
| `#calendar` | Schedule events, time-blocking |

### Default (1)

| Channel | Purpose |
|---|---|
| `#general` | Catch-all; default if no channel routing matches |

**Routing rule (DR075 reaffirmed):** every agent manifest declares `slack_channels:` with a primary + fallback pair. Cross-channel comms use threads; never DM if a channel exists.

---

## 10. Composability extends to the compute fleet (DR-NODE-COMPOSABILITY → DR084)

> **Every role / agent / MVP runs on ≥2 substrates (primary + backup). Failover via config swap, never code edit.**

This is the operational extension of §3's "body / brain / mind" composability principle from the *agent layer* to the *compute layer*.

**Concrete consequences:**

- Every baseline-5 manifest declares `node_routing:` with primary + fallback substrates.
- Every MVP's compute tier (§7.1) names ≥2 substrates.
- An agent moved to a new substrate works without code change — only config / env / harness profile changes.
- The harness-profile mechanism (`config/litellm.yaml` × `OPENCLAW_PROFILE` env var, shipped in Sprint 0 PR #1399) is the canonical config-swap surface.

See [ADR-011](docs/agent-system/decisions/ADR-011-node-composability.md) for the full operating model.

---

## 11. Cross-vendor handoff automation (Round 1 Item 5 amendment)

`COMMANDER-HANDOFF.md` discipline (ADR-003) is the manual baseline. **Automation triggers** are now defined for the cases where Dispatch should propose a handoff without Mike asking:

### Auto-trigger conditions

1. **Budget cap.** Tier-1 subscription quota for the active vendor crosses 90 % of monthly budget → Dispatch proposes handoff to Tier-1 sibling (Gemini ↔ Claude ↔ Codex) with a Slack reaction approval gate.
2. **Capability mismatch.** Active task is a known weak-fit for the current vendor (e.g. very-long-context > 1 M tokens not on Opus 4.7 → handoff to Gemini 2.5 Pro 2M-context). Dispatch proposes; Mike reacts ✅ or ❌ in Slack.
3. **Scheduled rotation.** Weekly rotation cron (Mondays 04:00 local) on Commander-of-the-Watch role to surface any silent vendor lock. Dispatch proposes; auto-approve unless Mike reacts ❌ within 1 hour.

### Approval gate

- All three triggers post a single Slack message with: trigger reason, target vendor, ETA of handoff completion, ❌ to abort.
- Default = approve after 1 hr if no reaction. Mike retains override at any time.

### Post-handoff bookkeeping

- New CTX entry `type: commander-handoff` with `from_vendor` / `to_vendor` / `trigger` / `approver`.
- `COMMANDER-HANDOFF.md` updated with timestamp + new active orchestrator.
- New AC entry confirming handoff complete.

Out of scope for MVP Phase 1 — implement after MVP-01 + MVP-02 ship; the discipline is enough until then.

---

## 12. Phase 4 — Voice / Ray-Bans prereqs (Round 1 hybrid B+C)

Voice (Meta Ray-Bans, Vision-Claw / OpenGlasses) is **Phase 4**, not Phase 1. Two gates must be green before any Phase 4 work starts:

### Capability gates (B)

- [ ] STT pipeline (whisper.cpp on PC tower) sustains < 2 s end-to-end on 30 s clips.
- [ ] TTS pipeline produces Mike-tolerable voice within 1 s of LLM response.
- [ ] Wake-word detection on Ray-Bans audio path — < 5 % false-positive rate.

### Use-case gates (C)

- [ ] At least one daily Mike-driven use-case identified (e.g. "ask Prime mid-walk for today's morning brief headline" or "voice-add to morning brief queue").
- [ ] Equivalent text-only flow demonstrated in MVP-01 / MVP-02 first (we don't add voice on top of broken text).

**Round 3 candidates to evaluate** when the gates are within reach:

- **VisionClaw** — open-source Vision-Pro/Ray-Bans agent shell.
- **DarlingtonDeveloper/OpenGlass** — open-source Meta Ray-Bans capture stack.

Out of scope for MVP Phase 1; mentioned here so we don't accidentally close the door.

---

## 13. Operational gating — 3-bucket action rule (DR091 + DR092)

**Independent of DLP** — DLP (see §14) is about data-flow boundaries; this section is about action-gating: which decisions Dispatch may execute autonomously vs which require explicit Mike approval. Every routing decision goes through this gate before execution.

| Bucket | Default behavior | Examples (non-exhaustive) | Blocks? |
|---|---|---|---|
| **Revocable** | Execute the recommended path | close PR · merge after rebase · ship preview · port file · append ledger · run W18/W21 cycle · dual-write memory · render preview · **`launchctl bootstrap gui/$(id -u)` of repo-owned plists** (reverses via `launchctl bootout`) | **Never** — course-correct on next checkpoint |
| **Ambiguous** | Pick recommended path WITH rationale, then execute | 2+ paths with non-trivial trade-offs but not destructive (which library, file structure, ordering) | **Never** — roll back if Mike says so |
| **Irreversible** | STOP, surface explicit gate via Slack 🚨, wait for explicit "go" | force-push · delete · empty trash · secrets · DNS · tunnel · financial · account creation · **`system/0/...` system-domain launchd with sudo** · EFI / firmware | **Yes** |

**DR091** = `DR-DISPATCH-NON-BLOCKING-TWO-WAY` (operational stance — Dispatch keeps coordinating when Mike is offline; notifications fire in parallel but child sessions keep moving).
**DR092** = `DR-DISPATCH-ACTION-BUCKETS` (the enumerated table above; amended 2026-04-26 evening to clarify user-domain `launchctl` is revocable, not irreversible). Both promoted in PR #1497, amended in PR #1502.

**This is action gating, not data-flow gating.** DLP (§14) is its own concern — work-laptop-adjacent data routes to local Tier-2 substrate per §7 routing logic. The two policies compose: a DLP-flagged action that's revocable in this bucket but tries to leave the local fleet hits the §14 hard-fail before it executes.

---

## 14. DLP work-laptop bridge (DR-WORK-LAPTOP-DLP-BRIDGE → DR082)

Mike's work laptop is DLP-restricted: it cannot export data, cannot run local agents that touch the open internet from work-laptop side, cannot be a primary harness host.

**Canonical bridge:** **GH Projects + Issues + repo files**. Agents producing professional artifacts MUST commit them to the repo and link the artifact in a Project #9 Issue, so Mike can pull onto the work laptop without breaking DLP policy.

**Current restriction posture:**

- No current local-only inference restriction — Mike's home Macs are NOT under work-laptop DLP.
- Future placeholder: when DLP-local-only routing is needed (e.g. processing work-side meeting notes), the routing layer (§7.1 DLP column) will force Tier-2 only.

Codified as **DR082 (DR-WORK-LAPTOP-DLP-BRIDGE)**. Enforced by `gh_bridge.py` (every artifact-producing agent commits + Issue-links).

---

## 15. Mid-turn logging mandate (DR079 — DR-DISPATCH-LOGGING)

After every major turn that lands a decision, answers a Round question, changes a label, or shifts scope, the orchestrator MUST dispatch a code session to:

1. Append the appropriate CTX entry (`type: decision-resolution` or `intent-clarification`) with the Q##/MVP/DR reference.
2. Update the relevant DR / ADR / INTENT.md section.
3. Dual-write the rule to Cowork auto-memory per DR067.

Logging happens MID-TURN, not at session end. A turn is "major" if any of:

- Mike answered a Round Q
- A label or scope changed
- A pivot or kill decision landed
- A new DR is introduced
- A track / MVP / workstream gained or shed scope

The orchestrator (Dispatch) cannot itself execute these writes per DR001 — it dispatches a code session and confirms commit before treating the turn as logged.

Codified as DR079 (dispatch-logging-mandate). Rationale: Mike directive 2026-04-24 — *"from here on out you are required to always update your memory and also the repo ctx dr, etc after each major turn lands."* Caught when Q8 was answered + executed (Sprint 0 PR #1399) without a Q8-linked CTX entry; chain broke.

---

## 16. Sprint chain (Round 1 reconciliation 2026-04-25)

Sprints are time buckets, NOT MVPs (per §0.5 v6 + DR078). The chain is:

| Sprint | Iteration | Focus | Status | Tracking |
|---|---|---|---|---|
| **Sprint 0** | foundation | WS-HARNESS — agnostic harness foundation | **shipped** PR #1399 / CTX-178 / AC-081 | done |
| **Sprint 1** | Phase 1 setup | Critical foundation fixes; Round-1 reconciliation; INTENT-amendment cycle | **in flight** (this PR) | this PR |
| **Sprint 2** | Phase 1 | **MVP-01 Morning Brief** delivery | next | per §5 / ADR-005 |
| **Sprint 3** | Phase 1 | **MVP-02 Lean Meeting Pipeline** + WS-VECTOR (embedding pipeline for entity extraction) | queued | per §5 / ADR-005 |
| **Sprint 4** | Phase 2 | **MVP-03 Track-C Vertex** prototype (gated per §5.1 Q12) | gated | per §5.1 |
| **Sprint 5** | Phase 2 | **MVP-04 Substrate re-evaluation** retro | gated | per §5.1 |

Sprints can overlap (Sprint-2 and Sprint-1 reconciliation can run concurrently for non-overlapping files). Sprint boundaries are administrative; deliverable boundaries are MVPs.

---

## 17. What's explicitly out of scope for this PR (and for the next 2 weeks)

Listed so downstream agents don't re-ingest these as candidate work.

- Touching ADR-001 / ADR-002 content beyond adding the supersede banner.
- Reconciling Flux to a live cluster (OrbStack is wiped; PR #1389 has the repo-side fixes but no live apply).
- ~~Deleting the 17 Gas Town manifests — they're blueprints (§4 Tier 2).~~ **Superseded 2026-06-12:** 19 manifests archived to `_archive/agents-gastown-2026-06/` per swarm-decoration decision B (CTX-537, chairman-ratified 2026-06-12). Kept: prime, forge, scout, sentinel, operator, judge, coach.
- Re-litigating 5-vs-17-vs-22 agents — settled in §4.
- Opening new PRs against BUILD.md — it's reference now, not canonical. Future edits land in INTENT.md / ADRs.
- Merging other open PRs (#1373, #1375, #1380, #1386 draft, #1389 draft) — this PR doesn't close them; they get handled individually.
- Implementing §11 cross-vendor handoff automation (post-MVP-01 work).
- PC tower bring-up execution (covered by ADR-010; bring-up is its own WS).

---

## 18. Amendment protocol

INTENT.md is amended exactly one way:

1. Open a PR editing INTENT.md.
2. Append a CTX entry with `type: intent-amendment`, `status: pending-commander-decision`, referencing the PR.
3. Mike reviews the PR. On approval the CTX flips to `status: resolved`.
4. Merge → canonical. No amendment lands without Mike's explicit approval on the PR.

**Cannot amend via:**

- Direct-to-main push.
- Inline ADR / BUILD.md / manifest edits that contradict INTENT.md without a paired INTENT.md edit.
- Session-level "we've decided…" without a PR.

---

## 19. Commander model (operational)

- One orchestrator holds merge rights at a time. That orchestrator is **Commander of the watch**. Mike is always Commander-in-chief.
- Orchestrator-of-record rotates across harnesses (Claude Code, Codex, Gemini, Cursor, …) via `COMMANDER-HANDOFF.md`. Auto-trigger conditions in §11.
- Incoming harness reads INTENT.md + `COMMANDER-HANDOFF.md` + runs `ops/hooks/swarm-bootstrap.sh` before any action.
- **Single-file canonical bootstrap surface = `~/.openclaw/.agents/BOOTSTRAP.md`**, regenerated on every `swarm-bootstrap.sh` run. Any harness reads this file top-to-bottom and is operational — no other file required. Sections 1-10 + appendix A cover identity (3-bucket rule), timezone (DR093), Decisions Log (§2.5: ANSWERED/DEFERRED/OPEN — read this before re-asking), top priorities, live Project #9 snapshot, running sessions, recent CTX, all numbered DRs + top-N feedback, top 50 artifacts, blocked-on-Mike issues, how-to-act invocation rules, static rules. CI smoke test asserts all sections render. See **DR088** (DR-BOOTSTRAP-LOADS-FEEDBACK), **CTX-247** (BOOTSTRAP.md generator + Decisions Log), and PR #1497 + #1498 for the implementation.
- Prime has full exec authority (DR085) within the active orchestrator session — distinct from Dispatch which is bound by DR001 separation-of-concerns. Prime spawns code sessions for parallelization/specialization but is NOT required to.
- See [ADR-003](docs/agent-system/decisions/ADR-003-operating-model.md) for the full Commander + Intent + Worktree triad.

---

## 20. WS-RECSYS end-state framing (the swarm's compounding spine)

OpenClaw's compound-value-over-time mechanic is an **adaptive recommendation engine over Mike's attention surface**. Action signals (Slack reactions, SwarmClaw events, iMessage replies, morning-brief actions) accumulate; per-source weights persist; gradient updates re-rank what surfaces tomorrow. Mike verbatim 2026-04-26 (POV synthesis dialogue): *"like a social ranking or x algorithm where you surface things i like to read or implement based on my usage and feedback like netflix."*

**v1 shipped (PR #1493 / CTX-230, 2026-04-26):**

- **D1** Action-signal source-of-truth = **A now (Slack reactions) → C target (multi-source: + iMessage RedClaw eventual)**.
- **D2** Weight slicing = **B (per-source) → toward C (per-time-of-day eventual)**. Default weights: `slack-reaction:1.0`, `swarmclaw-event:0.7`, `imessage-reply:1.5`, `morning-brief-action:1.2` (`.agents/memory/interests.yaml` `weights_seed`).
- **D3** Cold-start = **A** — seed from INTENT.md + user_profile via `interests.yaml` high/medium/low buckets.

Files: `manifests/swarm/action-signals.schema.json` (JSON Schema draft-07) · `.agents/memory/action-signals.jsonl` (append-only ledger) · `scripts/recsys/append_signal.py` (writer) · `scripts/recsys/replay_signals.py` (idempotent replay) · `ops/listeners/prime_slack_dm.py` (`reaction_added` handler with emoji map).

**Deferred to v2** (per §2.5 Decisions Log of BOOTSTRAP.md): D4 decay function · D5 negative-signal weight · D6 model-pick-by-task-type · D7 failure-mode + reset path · multi-source ingestion beyond Slack reactions · per-time-of-day weight slicing.

**Operational underpinnings:** **DR086** (RUNTIME-STATE-FIRST — runtime state beats stale comments / memory; the recsys reads live action-signals not cached snapshots) + **DR087** (PUSH-FIRST-SIGNAL — long-running processes Slack-ping `#prime` on completion + append durable timing log; signal latency must be sub-second because the recsys's value compounds with signal velocity).

**Why this is the compounding spine:** every other workstream (W10 intake, MVP-01 morning brief, MVP-02 meeting pipeline, SwarmClaw §3, agent identity §4.4) is a SOURCE feeding signals into this engine OR a SURFACE consuming the engine's ranked output. Without it, the swarm is a collection of one-shot tools; with it, the swarm gets more useful week-over-week as Mike uses it. The engine itself is INTENT.md §2 job-3 (swarm self-improvement) made concrete.

References: `docs/pov/2026-04-26-master-pov.md` (master POV synthesis, recsys end-state grounding) · CTX-230 (action-signal schema v1 shipped) · CTX-225 (master POV merged via PR #1478) · Issue #1485 (D1-D7 question + Mike's answers) · PR #1493 (v1 implementation) · ADR-005 (MVP Phase 1 — both MVPs feed the engine).

---

## 21. File provenance

- Created: 2026-04-24 by PR `feat/round-1-intent-capture-2026-04-24` (#1392).
- Round-1 reconciliation: 2026-04-25 by PR `feat/round-1-intent-reconciliation-2026-04-25` (this PR).
- Supersedes: prior `INTENT.md` stub from PR #1385 (retained in git history).
- Amendment history: `git log --follow INTENT.md` + CTX entries of `type: intent-amendment`.
- Source material: `.agents/memory/user/user_intent_openclaw_architecture.md` (verbatim Mike quotes from 2026-04-24 Round 1 dialogue).
- If this file is ever deleted, restore from git + file a post-mortem CTX before doing anything else.

---

## 22. OpenShell Safety Plane (The "Monkey with a Knife" Sandbox)

Re-enabled in v2.5 as the deterministic foundation for autonomous execution. Every non-trivial agent action is simulated in an **OpenShell Landlock Sandbox** before being proposed or executed.

- **Outcome Previews:** Simulations produce a "Projected Result" (file diffs, API call previews) surfaced in SwarmClaw for Mike's approval.
- **Kernel-Level Guardrails:** Landlock LSM (Linux) and similar policy layers govern the agent process, preventing unauthorized network egress or credential leak even if the prompt is hijacked.
- **Safe-to-Try:** Enables Mike to move the Autonomy Dial to `Autonomous` with the confidence that the system's "blast radius" is technically constrained, not just probabilistically steered.

Codified as **ADR-014 (Safety Plane)**. Rationale: Reconciles the "high-velocity autonomy" ambition with Mike's "deterministic discovery" requirement.