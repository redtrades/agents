# Research catalog — every corpus across the entire history

One catalog of every research artifact ever produced for this system, with
pointers and one-line takeaways. Read a file before contradicting a decision
it backed (rule from `agent-mesh/research/INDEX.md`).

## A. OpenClaw-era research (v1/v2/v3 mining, 2026-08-26 digests of pre-2026-08 material)

| Corpus | Pointer | Takeaway |
|---|---|---|
| v1 mining digest | `~/agent-mesh/research/mine-v1-digest.md` | OpenClaw v1 constitution, personas, ledgers, research mapped; Prime is the only complete persona survivor; JUDGE_RUBRIC ≥32/40 gated all self-improvement. |
| v2/v3 mining digest | `~/agent-mesh/research/mine-v2v3-digest.md` | 92 intel scans (version-velocity signal); reference-grade skill templates; v3 courtroom topology with generator≠judge proof + `proposal.schema.yaml`. |
| backup/config digest | `~/agent-mesh/research/mine-backup-config-digest.md` | Declarative control plane (7-primitive roster, tier routing, PaC budgets); bimodal skills; 16-job cron schema; eval golden-set format. |
| govcon overlap map | `~/agent-mesh/research/govcon-overlap-map.md` | Factory friction map; SAM delta→notices.db→FTS5 as top upgrade; council gate advisory; cache-stable prompts ~90% input cut; memory admissible only as cited inputs. |
| V1 swarm constitution + ledgers | `~/Library/Mobile Documents/com~apple~CloudDocs/09-Archive/OpenClaw-System-History/openclaw-v1-1534commits-2026-04-05-to-05-23/` (AGENTS.md, CLAUDE.md, `.agents/` era files) | 138 Decision Rules, JSONL append-only ledgers, COP.json, Slack #prime, AAIF AGENTS.md standard, three-tier swarm + Autonomy Dial + Landlock sandbox sim. |
| Vault-era concepts | `.../09-Archive/Ovault-Recovered/OPENCLAW_CONCEPTS.md`, `OPENCLAW_ARCHITECTURE.md`, `AGENTS.md` | documentation-by-default, memory tiers, token discipline, runtime guardrails of the OpenClaw home system. |
| disler / IndyDevDan corpus | `~/agent-configs/` provenance headers + `~/agent-reports/disler-agentic-engineering-findings-2026-08-28.md` + `~/agent-configs/archive/max-your-cc-sub/` | external prompt-engineering corpus mined into rules/skills with attribution (`SOURCE.md` discipline). |

## B. The overnight research wave (2026-08-26, 12 parallel agents; canonical copy = `~/agent-mesh/research/`, INDEX.md carries exec summaries)

| File | Takeaway (from INDEX.md; full text cited) |
|---|---|
| `research-hermes-ecosystem.md` | Hermes = NousResearch/hermes-agent; bots=profiles; routines=cron `[bot:]` with bot-chat delivery; real proactivity (gateway tick, /heartbeat, /loop); Mem0-class external memory incl. MemPalace path. |
| `research-memory-context.md` | Vendor benchmarks unreliable; keep verbatim dated chunks (Omi 51%→86.6% lesson); MemPalace as single semantic store; gbrain demoted to secondary/export; keep search-before-synthesis gate. |
| `research-caching-routing.md` | DR066 static-first caching holds everywhere 2026; DR086 four-tier routing ≈ LiteLLM config; Claude Code auto-compact ~95% hardcoded → proactive discipline needed; FreeLLMAPI proxy must be byte-transparent or caching dies. |
| `research-agentic-engineering.md` | AGENTS.md won; skills port via name+description; evaluator-before-generator settled; councils non-monotonic — start 3 cap 5; **GEPA+ACE practical pair** (see `GENETIC-SWARM.md` §5); artifact-or-nothing heartbeats + L2 autonomy ceiling. |
| `research-harnesses-councils.md` | Best trio: opencode (openai-compatible config), pi (cheap stateless judge), Claude Code (heavy code); git/files blackboard as comms bus; Hermes message_agent = signaling only; Buzz = human I/O, never coordination. |
| `research-free-routing-subscriptions.md` | GitHub Models retired 7/30; Cerebras killed always-free; Gemini free shrank; Groq best no-train workhorse; Max-arbitrage closed by Anthropic — legitimate maximization = lease-queued sessions; stealth models = rotation policy. |
| `research-proactive-agents.md` | Two-tier design: deterministic triggers decide whether/what, LLM writes prose about survivors; build-first 8 bots ranked with Morning Brief as aggregation spine; skip-on-missed-window doctrine. |
| `research-trading-polymarket.md` | SPCX IPO'd Jun 2026; no free options history → snapshot own chains; arb-bot NOT viable solo; prediction-market probabilities as sentiment features IS viable; no-auto-trading line. |
| `research-x-intake.md` | X Owned Reads ~$0.001/bookmark — cheapest reliable path; archive excludes bookmarks; Nitter class dead (C&D Aug 24 2026); hybrid Shortcuts+API ranked #1. |
| `research-idea-factory-gtm.md` | Sourcing automatable from free APIs (HN Algolia, app-review RSS, pytrends); base rates brutal → portfolio throughput + pre-committed kill thresholds; margin in B2B niches/bundles/catalogs. |
| `research-swarmclaw-command-center.md` | SwarmClaw = mobile PWA control plane (Deck/Board/Timeline/Feed + Watch/Assist/Auto dial), died of unwatched failures; v1 = static snapshot+HTML over existing stores; self-host Langfuse/Phoenix viable later. |
| `research-obsidian-vault.md` | Bases > Dataview; frontmatter standard type/status/source/topics/tags/aliases/up/related; bge-m3 llama-server sidecar embeddings; kNN classify + MinHash dedupe; weekly MOC sweep human-approved. |
| Staging provenance | Produced overnight 2026-08-26 by 12 agents in ephemeral `/var/folders/.../opencode/agentmesh/staging/` — `~/agent-mesh/research/` is the canonical copy (INDEX.md §Provenance). |

## C. Apple Silicon / model-program research (2026-08-26 → 2026-08-28)

| File | Pointer | Takeaway |
|---|---|---|
| Apple Silicon inference engines | `~/agent-mesh/research/APPLE-SILICON-INFERENCE-ENGINES.md` | Comparative eval: oMLX vs mlx-lm vs vMLX vs llama.cpp; launch configs and tradeoffs. |
| M1 Max roofline microarchitecture | `.../M1-MAX-ROOFLINE-MICROARCHITECTURE.md` | First-principles roofline: 400 GB/s, 21.8 TFLOPS; bottleneck decomposition. |
| Metal kernels prefill bottleneck | `.../METAL-KERNELS-PREFILL-BOTTLENECK.md` | FP16 vs BF16 SIMD emulation, TurboQuant KV4 attention sinks, MTP dispatch overhead. |
| Prefix-cache internals GDN | `.../PREFIX-CACHE-INTERNALS-GDN.md` | OMLX 2-tier cache, block Merkle token hashing (block_size=2048), GDN recurrent-state serialization (rht_int8), 96.9% hit rate. |
| HuggingFace SOTA models 2026 | `.../HUGGINGFACE-SOTA-MODELS-2026.md` | DeepSeek-Coder-V2-Lite MoE, Qwen2.5-Coder 7B/14B, Qwen3.8-27B, Qwen3.5-2B for Apple Silicon. |
| oQ4e series (5 files) | `~/agent-mesh/research/omlx-qwen38-oq4e-*.md` | T0 install/setup/verify/desktop/ideal-config receipts of the 27B OMLX control. |
| Flash-Next apple-silicon evidence | `.../qwen38-flash-next-apple-silicon-evidence-2026-08-27.md` | X/article evidence confirms IQ4 M64 feasibility on M1 Max; keep merged llama.cpp, 30-min soak, defer Q4/OMLX/concurrency until single-slot gates pass. |
| Model architecture + experiment | `~/agent-mesh/hermes/QWEN-38-27B-OQ4E-CONTROL-ARCHITECTURE.md`, `hermes/qwen38-flash-next-experiment.yaml`, `hermes/benchmark-results-2026-08-27.md`, `hermes/OMLX-M1MAX-OPTIMIZATION-GUIDE.md`, `hermes/OMLX-HERMES-OPTIMIZATION.md`, `hermes/MASTER-PERMUTATIONS-MATRIX.md`, `hermes/OPTIMAL-STACK-DELIVERABLE-2026-08-27.md`, `hermes/LOCAL-EVIDENCE-RECONCILIATION-2026-08-27.md` | The identity-correction chain (D-032/D-035) lives here; exact model = `qwen4_exp` (125B main / 6B active + 51B n-gram + 4B MTP), AtomicChat IQ4_XS-M64. Note: D-030's cited `QWEN-38-FLASH-NEXT-ARCHITECTURE.md` was renamed per D-032 to the `-CONTROL-` file (chronology preserved in DECISIONS/WORKLOG; only the CONTROL file exists on disk — verified 2026-08-30). |
| Raw benchmark evidence | `~/agent-reports/qwen38-flash-next/` (~985 MiB; immutable receipts; SHAs quoted in HANDOFF/WORKLOG tail) | Local-only; archive by hash per ESTATE-LEDGER, never git-import wholesale. |
| Older model-era reports | `~/agent-reports/` folders: `2026-08-19-benchmark-findings-preserved`, `writing-model-evaluation`, `mlx-engine-shootout`, `mlx-serving-landscape`, `vmlx-config-search`, `omlx-*` series, `concurrent-serving-apple-silicon`, `freellmapi-*`, `ox-alpha-setup`, `2026-08-24-superqwen-benchmark` | Predecessor benchmark/serving evaluations across the estate. |

## D. Platform / architecture research inside `agent-platform`

| File | Takeaway |
|---|---|
| `agent-platform/research/SELF-HOSTED-PLATFORM-COMPARISON.md` | Read-only decision brief (access 2026-08-28): which self-hostable systems could join later without taking source/acceptance/promotion/durable-policy authority; preserves the historic baseline (git+worktrees+portable procedures+immutable artifacts+local receipts as the initial seam) and defers Temporal/LangGraph/OpenTelemetry-Phoenix/vector-memory until measured failure. Authority map table (§2) is the boundary contract. |
| `agent-platform/docs/AUTONOMOUS-LOOP.md` | Phase-B spec: the clocked control loop wiring dispatcher+eligibility+CAS+gate_c into one restartable pass; names what's missing (CLI main, assemblePacket, real implementer/reviewer adapters, cadence, live fixtures). Anchor issue #9. |
| `agent-platform/docs/DISPATCH-LOOP.md` | Dispatch half: modules, eligibility, capacity, dry-run guard; observed readiness RED→PASS. |
| `agent-platform/docs/GITHUB-FREE-PRIVATE-BOUNDARY.md` | What GitHub Free private repos can/cannot enforce (no crypto CI trust, no branch-protection-style promotion mutex) — the reason Contents-API CAS is the shared authority. |
| `agent-platform/docs/DELIVERY-FAILURE-LEDGER.md` | DFL-001..020 / AP-01..027 — sole canonical anti-pattern register (also the distilled research of every era's failures). |
| `agent-platform/objective-drift-research.md` + untracked working notes | Drift research (2026-08-30 working set; not yet committed — treat as candidate). |
| Issue #185 research task | "Research: Temporal and LangGraph as durable execution substrate for objective continuity" — the open successor of the SELF-HOSTED comparison; state observed 2026-08-30. |
| `agent-platform/proofs/gate-c-live-{69,81,86,103}.txt` | Live-proof receipts for the four Gate C runs. |

## E. Product-factory and business corpora (`govcon-factory` + `agent-reports`)

- `~/govcon-factory/research/` + `~/govcon-factory/knowledge/research/`:
  winning-proposal-teardown (INDEX cited by 23 issues that never existed on
  main — the cautionary tale recorded in `agent-platform/docs/START-HERE.md`
  §Entry contract #4), gtm-playbook, offer-design, demand-generation,
  analyst-landscape, competitive-assessment, competitor-pain, naics-selection,
  kill-test, feasibility-final/-review, growth-plan, council, local-model-eval,
  govcon-prior-art, govconapi-exploration, e2e-validation.
- `~/agent-reports/`: `opportunity-scan.md`, `outreach-playbook.md`,
  `sdvosb-business/`, `video-reviews/`, `typed-failure-states/`,
  `avo-supervisor/`, `agent-memory/`, `claude-academy-reference/`,
  `google-subscription-antigravity/`, `hermes-provider-routing-20260829/`,
  `issue40-routing/`, `sssf-provider-options/`, `worktrees/`,
  `2026-08-22-dispatch-log.md`, `BACKLOG-2026-08-28.md`,
  `WORKSTREAM-PROMPTS-2026-08-28.md`.
- `~/agent-configs/knowledge/MIKE-INTENT-DEBRIEF-2026-08-28.md` — the
  accumulated-context intent model (two simultaneous projects; failure modes;
  why the rules exist).
- `~/agent-workspace/model-eval-qwen3.8-flash-next-glm-5.3.md` — matched model
  eval.

## F. External / fork prior art (GitHub `redtrades/*` forks — pointers only)

| Fork | Why it matters here |
|---|---|
| `redtrades/agentic-stack` | The public "one brain, many harnesses" portable `.agent/` pattern — same thesis agent-mesh built internally (adapters for Claude Code/Cursor/Windsurf/OpenCode/OpenClaw/Hermes/DIY Python). |
| `redtrades/hermes-agent-self-evolution` | DSPy + GEPA evolutionary self-improvement for Hermes — the concrete "genetic" optimizer implementation. Pointer: `GENETIC-SWARM.md` §5; upstream https://github.com/GEPA-ai/GEPA, https://dspy.ai/api/optimizers/GEPA/overview/ |
| `redtrades/awesome-openclaw-skills` | 5,400+ filtered OpenClaw skills registry (skill corpus scale). |
| `redtrades/claude-flow` | v2 alpha swarm intelligence/orchestration patterns. |
| `redtrades/superpowers`, `oh-my-claudecode`, `oh-my-codex` | Skills frameworks + multi-agent orchestration prior art (hook/prompt/role ecosystems the five config types mirror). |
| `redtrades/deepagents`, `deep-agents-from-scratch`, `Subagents`, `claude-agents`, `awesome-claude-agents`, `agency-agents`, `agents`, `agent-academy`, `shadow`, `awesome_ai_agents`, `system-prompts-and-models-of-ai-tools`, `chrome-devtools-mcp`, `codex`, `claude-code`, `social-media-agent` | Surveyed agent-framework/subagent prior art behind the design corpus. |

## G. Triage / ops artifacts (point-in-time, 2026-08-30)

`~/agent-platform-audit-2026-08-30.md` (P1/P2 worktree audit),
`agent-platform/QUEUE-*.md`, `CLAIM-QUEUE-TRIAGE*.md`, `STATUS-*.md`,
`TERMINAL-CLEANUP-SEQUENCE-NOTE.md`, `rebase-*-receipt.md`,
`triage-result-2026-08-30.json`, `worktree-reaper-report-2026-08-30.json` —
live transition evidence for the 2026-08-30 queue reconciliation; all
untracked working notes (candidate material, not governing).
