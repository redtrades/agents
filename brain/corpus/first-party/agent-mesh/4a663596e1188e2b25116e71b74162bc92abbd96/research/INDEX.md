# Research index — evidence base for every design decision here

Full cited digests, unedited (D-015). Each file ends with SOURCES.
Concise takeaways below; read the file before contradicting a decision.

| File | One-line takeaway |
|---|---|
| hermes-ecosystem | Hermes = NousResearch/hermes-agent v0.20.5; bots=profiles; routines=cron `[bot:]` w/ bot-chat delivery; proactivity real (gateway tick, /heartbeat, /loop); Mem0-class external memory providers incl. MemPalace path |
| memory-context | Vendor benchmarks unreliable; keep verbatim dated chunks (Omi 51%→86.6% lesson); adopt MemPalace as single semantic store; gbrain demoted to secondary/export; keep search-before-synthesis gate |
| caching-routing | DR066 static-first caching holds everywhere 2026; DR086 four-tier routing ≈ LiteLLM config; watchdogs sound; Claude Code auto-compact hardcoded ~95% so proactive/manual discipline needed; FreeLLMAPI proxy must be byte-transparent or kills caching |
| agentic-engineering | AGENTS.md won; skills port via name+description; evaluator-before-generator settled; councils non-monotonic — start 3 cap 5; GEPA+ACE practical pair; artifact-or-nothing heartbeats + L2 autonomy ceiling |
| harnesses-councils | Best trio: opencode (openai-compatible config), pi (cheap stateless judge), Claude Code (heavy code); git/files blackboard as comms bus; Hermes message_agent = signaling only; Buzz = human I/O, never coordination |
| free-routing-subscriptions | GitHub Models retired 7/30; Cerebras killed always-free; Gemini free shrank; Groq best no-train workhorse (8K TPM bind); Max-arbitrage closed by Anthropic — legitimate maximization = lease-queued sessions; stealth models = rotation policy |
| proactive-agents | Two-tier design everywhere: deterministic triggers decide whether/what, LLM writes prose about survivors; build-first 8 bots ranked w/ Morning Brief as aggregation spine; skip-on-missed-window doctrine |
| trading-polymarket | SPCX IPO'd Jun 2026 ($135, ~$1.75T) — normal underlying now; no free options history → snapshot own chains nightly; arb-bot verdict NOT viable solo; prediction-market probabilities as sentiment features IS viable; no-auto-trading line |
| x-intake | X API pay-per-use but Owned Reads \$0.001/bookmark — cheapest reliable path (~\$1-3/mo); archive excludes bookmarks; Nitter class dead (C&D Aug 24 2026); hybrid Shortcuts+API ranked #1 |
| idea-factory-gtm | Sourcing automatable from free APIs (HN Algolia, app-review RSS, pytrends); Reddit/G2 sampling-grade only; base rates brutal (median Gumroad seller \$72/mo) → portfolio throughput + pre-committed kill thresholds; margin in B2B niches/bundles/catalogs |
| swarmclaw-command-center | SwarmClaw = mobile PWA control plane (Deck/Board/Timeline/Feed + Watch/Assist/Auto dial), died of unwatched failures; v1 = static snapshot+HTML over existing stores; self-host Langfuse/Phoenix viable later |
| obsidian-vault | Bases > Dataview now; frontmatter standard type/status/source/topics/tags/aliases/up/related; bge-m3 llama-server sidecar for embeddings; kNN classify + MinHash dedupe; weekly MOC sweep human-approved |
| mine-v1-digest | v1 constitution/personas/ledgers/research mapped; Prime only complete persona survivor; JUDGE_RUBRIC ≥32/40 gated all self-improvement |
| mine-backup-config-digest | Declarative control plane (7-primitive roster, tier routing, PaC budgets); bimodal skills; 16-job cron schema; eval golden-set format |
| mine-v2v3-digest | 92 intel scans (version-velocity signal); reference-grade skill templates; v3 courtroom topology w/ generator≠judge proof + proposal.schema.yaml |
| govcon-overlap-map | Factory friction points + SAM delta→notices.db→FTS5 as top upgrade; council gate advisory; cache-stable prompts ~90% input cut; memory admissible only as cited inputs |
| omlx-qwen38-oq4e-installer-preflight-snapshot-2026-08-26 | T0 pre-execution snapshot and rollback reference for Qwen3.8-27B-oQ4e installer |
| omlx-qwen38-oq4e-setup-and-bench-2026-08-26 | T0 config setup closing max_tokens gaps and initial benchmark runs across 3 profile tiers (-t file baseline) |
| omlx-qwen38-oq4e-profile-verify-2026-08-26 | T0 verification of short/mid/full profile configs and concurrency safety checks |
| omlx-qwen38-oq4e-hermes-desktop-2026-08-26 | T0 desktop path latency investigation (full 18-tool schema / 28K token prompt vs isolated file tools) |
| omlx-qwen38-oq4e-ideal-config-2026-08-26 | T0 architectural retargeting note: long-context agentic coding target vs first-token sweep, lease protocol, and SDLC handoff |
| APPLE-SILICON-INFERENCE-ENGINES | Comprehensive comparative evaluation of oMLX, mlx-lm, vMLX, and llama.cpp; launch configs and architectural tradeoffs |
| M1-MAX-ROOFLINE-MICROARCHITECTURE | First-principles roofline and arithmetic intensity analysis on M1 Max (400 GB/s, 21.8 TFLOPS); microarchitecture bottleneck decomposition |
| PREFIX-CACHE-INTERNALS-GDN | OMLX 2-tier cache, block Merkle token hashing (block_size=2048), GDN recurrent state serialization (rht_int8), 96.9% hit rate |
| HUGGINGFACE-SOTA-MODELS-2026 | SOTA model comparative analysis (DeepSeek-Coder-V2-Lite MoE, Qwen2.5-Coder 7B/14B, Qwen3.8-27B, Qwen3.5-2B) for Apple Silicon |
| METAL-KERNELS-PREFILL-BOTTLENECK | Metal execution pipeline analysis, FP16 vs BF16 SIMD emulation, TurboQuant KV4 attention sinks, and MTP dispatch overhead |
| qwen38-flash-next-apple-silicon-evidence-2026-08-27 | Supplied X/article evidence confirms IQ4 M64 feasibility on M1 Max but not current explicit-lazy, cache, or restart semantics; keep merged llama.cpp, add a 30-minute soak, and defer Q4/OMLX/concurrency until single-slot gates pass |


## Provenance

Produced overnight 2026-08-26 by 12 parallel research/mining agents
(websearch + primary docs + local repo archaeology). Staging originals
in `/var/folders/.../opencode/agentmesh/staging/` (ephemeral) — this
directory is the canonical copy.
