# State of the Art: Memory + Context Management for Personal AI Agents (2026)

**Researched:** 2026-08-26. Scope: durable cross-harness memory for Mike's stack (NousResearch hermes-agent local, Claude Code, opencode; diagnostic agent swarm). Existing assets: mempalace fork (`redtrades/mempalace`, upstream `MemPalace/mempalace`), gbrain (`~/.gbrain` PGLite), retired Mem0 usage, prior 5-tier pipeline (session JSONL → git-canonical ledgers (`context.jsonl`/`semantic.jsonl`) → vector/graph store behind a mandatory search-before-synthesis MCP gate).

> Caveat up front: GitHub star counts below vary widely between sources because they were captured at different dates by different publications. Treat them as magnitude, not fact. All activity claims were verified against 2026-dated sources.

---

## 1. Landscape survey

| Project | Stars (approx., source-dependent) | Architecture (extraction → storage → retrieval) | Local-first viability | License | MCP |
|---|---|---|---|---|---|
| **Mem0** | ~47k–63k | LLM extracts atomic facts on each turn → vector (+paid graph) store, ADD/UPDATE/DELETE/NOOP dedup pass → multi-signal retrieval (semantic + BM25 + entity overlap), ~6.8k tokens/query | Partial: core SDK self-hosts; **graph memory is paid Pro ($249/mo)**; cloud-first gravity | Apache 2.0 (core) | Yes |
| **MemPalace** (Mike's fork upstream) | ~54k–58k (per AI/TLDR, rohitraj.tech) | **Verbatim capture, zero extraction lossiness**: transcripts mined as-is → "palace" of wings (people/projects) / rooms (topics) / drawers (content) on SQLite + pluggable vector backend → scoped semantic search + temporal entity KG with validity windows | **Excellent: offline default, no API key or LLM anywhere in the retrieval path** | Reported MIT, fully open ([rohitraj.tech](https://rohitraj.tech/en/notes/open-source-ai-agent-memory-mem0-vs-zep-letta-2026)) | Yes — 36–44 tools; hooks for Claude Code/Codex/Cursor/Antigravity |
| **Zep / Graphiti** | Graphiti ~27k–29k | Episodes ingested → temporal knowledge graph; every edge carries `valid_at`/`invalid_at` windows; contradictions invalidate rather than delete → graph queries answer "what was true when" | Weak for platform: **Graphiti OSS is open; the full Zep product stepped back from self-hosting (SaaS ~$25/mo+)** | Apache 2.0 (Graphiti) | Yes (Zep Cloud / embed Graphiti) |
| **Letta (MemGPT)** | ~24k | Agent-owned tiered memory (core blocks in-context = RAM, recall = searchable history, archival = vector disk); agent pages its own memory via tools → **sleep-time agents / "Dreaming"** consolidate in background; Feb 2026 **Context Repositories**: git-backed MemFS with subagent worktree merges | Excellent: fully self-hostable, model-agnostic | Apache 2.0 | Server + tool surface |
| **cognee** | ~28k–30k | Ingest any format → ECL pipelines (Extract-Cognify-Load) build self-hosted KG (Kuzu/Neo4j) + vectors (LanceDB/pgvector) → hybrid graph+vector recall via 4-verb API (`remember`/`recall`/`forget`/`improve`) | Good: pip/Docker, runs local, any LLM incl. Ollama; cloud optional | Apache 2.0 | Yes (`cognee/cognee-mcp`; Claude Code plugin) |
| **Basic Memory** | ~3k (site-claimed), 57k dl/mo | Humans + AI co-write plain Markdown notes with wikilinks → observations/relations parsed into a knowledge-graph + FTS/semantic index on SQLite/Postgres → `build_context` traversal + hybrid search | **Excellent: files are the database**, Obsidian-native, optional paid cloud sync | Open source (local free); Cloud $15/mo | Yes (stdio/https, all major clients) |
| **Memobase** | n/a (product) | Deterministic HTTP hooks capture turns → server-side vault (Postgres RLS) with background dedupe/merge/distillation → hybrid vector+BM25+graph recall, `reconstruct_context` snapshots | **No: hosted-only today** ("self-custody options on the roadmap"; explicitly not zero-knowledge) | Proprietary service | Yes (MCP-native) |
| **memoripy** | tiny | Short/long-term stores, decay/reinforcement, spreading activation over concept graphs | Fine technically, but **stale: PyPI v0.1.2, no 2026 activity found** | MIT | No |
| **Claude-native (CLAUDE.md + Auto Memory + memory tool)** | n/a | You write CLAUDE.md (rules); Claude writes Auto Memory (`~/.claude/projects/<repo>/memory/`, `MEMORY.md` index capped at 200 lines/25KB + topic files read on demand); API `memory_20250818` tool (GA) = client-implemented `/memories` file ops → loaded at session start, not vector-searched | Excellent (it's just your filesystem) | n/a | memory tool is client-side contract |
| **Karpathy-style LLM-wiki vault** | pattern (gist Apr 2026) | Raw sources immutable → **LLM compiles & maintains interlinked Markdown wiki** (entity/concept/source pages, index.md, log.md, AGENTS.md schema) → index-first navigation, optionally qmd/local BM25+vector search | Excellent: plain files + git; Obsidian front-end | pattern; impls MIT (llm-wiki-plugin, MirkoSon/llm-wiki-vault, KHOAAI template) | optional (qmd MCP; plugin ships one) |
| **gbrain-class PGLite brains** | gbrain ~14k | Markdown brain-repo is system of record → every `put_page` regex-extracts typed graph edges (**zero LLM calls**) into embedded Postgres 17/PGLite + pgvector → hybrid HNSW+BM25+RRF+reranker, 74 MCP tools, seven frozen memory verbs (`recall`/`remember`/`synthesize`/`context_pack`/`delta`…) | Excellent: `~/.gbrain/brain.pglite`, no server; Supabase migration past ~50k pages | MIT | Yes (stdio + HTTP/OAuth) |

### Prose notes

- **Mem0** is the bolt-on default: widest integration surface, fastest to adopt, cheapest per turn (~120ms, ~280 injected tokens in one June 2026 hands-on benchmark, 84% recall vs Zep's 91% at ~2x cost)[hamzashabbir.dev](https://hamzashabbir.dev/article/agent-memory-mem0-vs-letta-vs-zep-vs-langmem-benchmark-2026). But its most accurate mode (graph) is paywalled, and its published numbers are contested (§2).
- **MemPalace** is the strongest *local-first* entrant: verbatim storage with **no summarization step before search** ([ai-tldr.dev](https://ai-tldr.dev/tools/mempalace/)), a temporal entity KG with validity windows backed by local SQLite (v3.6.0), pluggable backends (ChromaDB default; sqlite_exact bundled; Qdrant/pgvector/Milvus opt-in), and an active 2026 release cadence — **v3.8.0 shipped Aug 2026** with lean hub-proxied MCP sessions (~17MB, sized for 50-agent fleets), wakeable-agent `logstream watch` coordination across machines, single-writer palace ownership, and a secure multi-host `mempalace serve` ([releases](https://github.com/MemPalace/mempalace/releases)). It ships transcript parsers + lifecycle hooks (stop/preCompact/sessionStart) for Claude Code, Codex, Cursor, Gemini CLI/Antigravity — and an open PR (#1684) for a **native Hermes memory provider** implementing Hermes' `MemoryProvider` ABC with session backfill.
- **Zep/Graphiti** remains the reference design for temporal correctness: validity windows on every fact beat flat vector stores on "what changed when" questions (a 15-point LongMemEval edge over Mem0 in one comparison) [blog.appxlab.io](https://blog.appxlab.io/2026/04/13/ai-agent-memory-frameworks/). But the product is SaaS-first now; self-hosters get the Graphiti engine, not the platform [rohitraj.tech](https://rohitraj.tech/en/notes/open-source-ai-agent-memory-mem0-vs-zep-letta-2026).
- **Letta** matured the MemGPT idea: memory blocks the agent edits itself, sleep-time background consolidation (arXiv:2504.13171 — ~5x less test-time compute for equal accuracy), and in Feb 2026 **Context Repositories** — the agent's context lives as a git repo; subagents get worktrees and merge learned context through normal git conflict resolution; a sleep-time process reviews history and commits memory updates ([letta.com/blog/context-repositories](https://www.letta.com/blog/context-repositories/)). Cost: it wants to be your runtime; hardest to bolt on [digitalapplied.com](https://www.digitalapplied.com/blog/open-source-agent-memory-mem0-letta-zep-compared).
- **cognee** is the serious open-source graph-memory platform (30.2k stars verified on GitHub, Apache 2.0, v1.4.0 July 17 2026): local Kuzu+LanceDB by default, MCP server with a deliberately minimal `remember/recall/forget` surface. Heavier than vectors; graphs cost latency/tokens ([dev.to review](https://dev.to/andrew-ooo/cognee-review-open-source-ai-memory-for-agents-2cei)).
- **Basic Memory** proves the "Markdown is the DB" thesis at product quality: same `.md` files edited by human (Obsidian) and AI (MCP), with a derived graph/search index. Best when the human wants to read what the agent knows.
- **Memobase** pivoted to a hosted cross-vendor vault ("tell Claude today, ChatGPT knows tomorrow") — architecturally interesting (deterministic hooks + Postgres RLS + background distillation) but fails a local-first constraint outright [memobase.ai/docs](https://memobase.ai/docs/). **memoripy** is a neat decay/spreading-activation demo that hasn't moved since v0.1.2 — not a 2026 option.
- **Claude-native patterns**: Claude Code now has two first-party systems — CLAUDE.md you write, and **Auto Memory** Claude writes itself (index + topic files, capped startup load, per-repo scope, no semantic search) [code.claude.com/docs/en/memory](https://code.claude.com/docs/en/memory). The API-level `memory_20250818` tool is GA: the model issues `/memories` file operations, your code implements them; Anthropic auto-injects a protocol telling the model to assume its context can reset at any moment [platform.claude.com cookbook](https://platform.claude.com/cookbook/tool-use-context-engineering-context-engineering-tools).
- **LLM-wiki vaults** (Karpathy gist, April 2026): the agent doesn't retrieve from raw docs — it *compiles* them once into a maintained wiki and answers from compiled pages. Works to ~100 sources on index navigation alone; practitioners add union-with-full-text-search past that ([karpathy gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f), [praneybehl/llm-wiki-plugin](https://github.com/praneybehl/llm-wiki-plugin)). The ecosystem converged on guardrails: draft→canonical promotion, contradiction detection, size limits, re-read-before-edit.
- **gbrain** (Garry Tan, released Apr 5 2026, MIT) is the PGLite-class brain Mike already runs: markdown repo as source of truth, deterministic typed-graph extraction (no LLM calls), hybrid retrieval measured at BrainBench P@5 49.1% / R@5 97.9% (+31.4 pts P@5 over graph-disabled variant), built explicitly for OpenClaw/**Hermes** deployments; production instance cited at 146k pages, 66 cron jobs ([vectorize.io](https://vectorize.io/articles/what-is-gbrain), [marktechpost tutorial](https://www.marktechpost.com/2026/05/22/a-step-by-step-coding-tutorial-to-implement-gbrain-the-self-wiring-memory-layer-built-by-y-combinators-garry-tan-for-ai-agents/)). v0.45.x adds ambient-recall verbs (`context_pack`, `delta`) and mountable team brains.

---

## 2. What's actually winning

### The benchmark picture is broken — treat all vendor scores as upper bounds

Three suites anchor 2026 comparisons: **LoCoMo** (1,540 Qs, multi-session dialogue), **LongMemEval** (500 Qs: knowledge updates, temporal reasoning, abstention), **BEAM** (1M/10M-token contexts) [AgenticWire](https://www.agenticwire.news/article/mem0-zep-letta-agent-memory), [mem0.ai/blog](https://mem0.ai/blog/ai-memory-benchmarks-in-2026).

The headline dispute: Mem0 self-reports **94.4 on LongMemEval** (Apr 14, 2026 announcement); the one independent reproduction measured **49.0 pre-April** and **73.8 post-April** on the same hosted system — still ~20 points below claim. An audit of `mem0ai/memory-benchmarks` commit history found 14 dataset-specific equivalence rules mapping 1:1 to public question IDs, a hidden CoT block, a "lean toward yes" judge instruction, and a one-directional gold-override clause [maximem.ai](https://www.maximem.ai/blog/state-of-ai-memory-2026-claimed-vs-observed). Zep published a rebuttal ("Is Mem0 Really SOTA in Agent Memory?") claiming three implementation errors in Mem0's Zep eval, with corrected LoCoMo 75.14 vs Mem0-graph ~68 — inverting the result [aibootstrapperacademy.com](https://aibootstrapperacademy.com/blog/mem0-vs-zep-vs-letta-ai-agent-memory-guide). Every headline score is vendor-run on its own harness [digitalapplied.com](https://www.digitalapplied.com/blog/open-source-agent-memory-mem0-letta-zep-compared).

What survives scrutiny (reproducible/open-harness numbers):

| System | Benchmark | Score | Source |
|---|---|---|---|
| Full-context baseline | LoCoMo | 72.9% | mem0 paper Table 1, via [Omi repo](https://github.com/BasedHardware/omi-memory-benchmarks) |
| Mem0 (paper, reproducible config) | LoCoMo | 66.9% | same |
| Letta (filesystem) | LoCoMo | 74.0% | Letta blog, via Omi repo |
| Zep (corrected replication) | LoCoMo | 58.4% | Omi repo |
| **Omi (verbatim chunk indexing)** | LoCoMo | **86.6%** | own harness, results committed |
| Hindsight (local) | LoCoMo | 92.0% | [agentmemorybenchmark.ai](https://agentmemorybenchmark.ai/dataset/locomo) |

**The single most transferable finding of 2026**: Omi went from ~51% → 86.6% on LoCoMo almost entirely by adding **verbatim, dated, overlapping chunks of raw transcripts** to an index that previously held only summaries. Exact details (dates, names, numbers) are semantically unfindable after lossy summarization; ingestion cost was embeddings-only, ~$0.01/user/month [BasedHardware/omi-memory-benchmarks](https://github.com/BasedHardware/omi-memory-benchmarks). This independently validates the verbatim-capture bet both MemPalace and gbrain make, and it validates keeping raw session logs forever.

Research-side, two signals matter for a diagnostic swarm:

- **LoCoMo-Plus** (ACL 2026) shows *all* current memory systems — Mem0, SeCom, A-Mem included — collapse on "cognitive memory": retaining implicit constraints under cue-trigger disconnect drops GPT-4o-system averages from ~57 (factual) to ~15–42. Beyond-factual consistency is an open problem; don't expect any store to solve it [aclanthology.org/2026.acl-long.1150](https://aclanthology.org/2026.acl-long.1150.pdf).
- **E-mem** (June 2026) argues extraction/compression pipelines cause "destructive de-contextualization" and gets SOTA on LoCoMo multi-hop by reconstructing uncompressed episodic contexts via hierarchical agents (+8.86 F1 over GAM, −70% token cost) [alphaxiv](https://www.alphaxiv.org/overview/2601.21714). **TiMem** shows temporal-hierarchical consolidation (raw observations → progressively abstracted personas) reaching 75.3 LoCoMo / 76.88 LongMemEval-S while halving recalled length [arxiv.gg/abs/2601.02845](https://arxiv.gg/abs/2601.02845). Direction of travel: **layered consolidation on top of preserved episodic raw material**, not replacement of it.

### Practitioner consensus (agentic memory, mid-2026)

1. **Split episodic from semantic** — conversation logs and durable facts have different retention/recall profiles; treat them as separate stores [callsphere.ai](https://callsphere.ai/blog/td30-fw-mem0-vs-zep-vs-letta-2026-honest-comparison-guide).
2. **Verbatim beats summaries as the retrieval substrate**; summaries belong in a curated layer above (Omi result; MemPalace design; Karpathy compile-once pattern).
3. **Decay aggressively** — memory that never expires accumulates noise; recall improves when forgetting is biased toward (callsphere; MemPalace ships Ebbinghaus decay on graph edges).
4. **Temporal validity windows are table stakes** for anything whose facts change (Zep's design copied into MemPalace v3.6+ and gbrain's supersession).
5. **Run your own golden-set evals** — the only trustworthy benchmark is the one you run on your own conversations with a neutral judge (universal conclusion of the 2026 comparison pieces).
6. **Extraction pipelines are not winning outright** — the honest split: extraction (Mem0) wins ease/latency; verbatim+structure wins recall fidelity; agent-managed tiers (Letta) win autonomy; graphs win time-aware questions. Hybrid tiered designs are where the field is converging.

---

## 3. Context engineering SOTA

### Compaction: three levers, sorted by what you can afford to lose

Anthropic now ships first-party API primitives [platform.claude.com cookbook](https://platform.claude.com/cookbook/tool-use-context-engineering-context-engineering-tools):

- **Tool-result clearing** (`clear_tool_uses_20250919`, trigger default 100K tokens, keeps last 3 uses): evicts re-fetchable tool outputs, keeps the call record. Lossless-for-re-fetchable, cheapest lever. Also `clear_thinking_20251015` for reasoning blocks.
- **Compaction** (`compact_20260112`, Jan 2026, default trigger 150K): whole-transcript summary, continues from it. Measured behavior: preserves 3/3 high-level facts, **0/3 obscure specifics** — the details that later turn out to matter are exactly what dies. Custom `instructions` let you name what must survive.
- **Memory tool** (`memory_20250818`, GA): file-backed `/memories` outside the window; the only lever where a fact survives a context reset.

Reported eval deltas: context editing alone +29% on agentic search; +39% with memory added; 84% token reduction over a 100-turn run [dreaming.press](https://dreaming.press/posts/context-editing-vs-compaction-for-long-running-agents.html). Playbook order: **Write (to memory) what you can't lose → Select just-in-time → Compress what remains → Isolate into subagents only when work genuinely forks** [dreaming.press playbook](https://dreaming.press/posts/context-engineering-playbook-write-select-compress-isolate.html). Isolation dissent worth knowing: Cognition's "Don't Build Multi-Agents" — isolate work, not decisions; keep writes single-threaded.

### Just-in-time retrieval vs always-loaded memory

Anthropic's canonical position: shift from pre-loading retrieved context to **just-in-time strategies** — lightweight identifiers (paths, queries, links) resolved at runtime via tools, mirroring how humans use indexes rather than memory [anthropic.com/engineering/effective-context-engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents). Claude Code itself is the hybrid exemplar: CLAUDE.md dropped in up front, glob/grep navigate everything else. Production memory systems converge on **bounded always-loaded index + lazy bodies**: Hermes caps `MEMORY.md` at ~2,200 chars and `USER.md` at ~1,375 chars; Codex injects a 5K-token `memory_summary.md` and greps the handbook on demand; Claude Code loads 200 lines/25KB of index and Reads topic files when judged relevant [nicolasbustamante.com](https://nicolasbustamante.com/blog/agent-memory-engineering). Known failure mode: when the index outgrows its cap, pointers scroll out of the loaded window and their topic files become effectively invisible [vectorize.io claude-code-memory](https://vectorize.io/articles/claude-code-memory).

### Instruction-drift mitigation for marathon sessions

Documented failure taxonomy from the Claude Code issue tracker [#44166](https://github.com/anthropics/claude-code/issues/44166), [#68636](https://github.com/anthropics/claude-code/issues/68636), [#48959](https://github.com/anthropics/claude-code/issues/48959):

- `.claude/rules/` files are **re-injected fresh each turn** (compaction-exempt); root CLAUDE.md and auto-memory are compressed like ordinary messages. Moving critical invariants into rules files is the working native workaround.
- Drift persists even when content survives: the post-compaction summary restates rules in its own words *before* CLAUDE.md re-loads, and wins on positional weight — a positioning problem, not a preservation problem (#48959). Mitigations that practitioners report working: **imperative anchors at the top** (`ALWAYS`/`NEVER`/prohibited-actions framing, which pattern-match instruction-following rather than relying on positional authority), injecting immutable-rule blocks into the compaction prompt itself, PreCompact/SubagentStart hooks re-injecting rules as system reminders, and behavioral digests (extract corrections once, store verbatim, re-inject append-only — e.g., cozempic).
- Consensus contract: **soft conventions → instruction layers (auditable, occasionally missed, recoverable); hard invariants (security boundaries, approval gates) → tool/permission gates outside the prompt entirely.** A blocked tool call cannot be summarized away.

### Static-first, prompt-cache-friendly layout

Prompt caching is prefix matching; one changed byte invalidates everything after it. Claude Code's own lessons [claude.com/blog](https://claude.com/blog/lessons-from-building-claude-code-prompt-caching-is-everything):

1. Ordering: static system prompt + tools (globally cached) → CLAUDE.md (project-cached) → session context → messages last.
2. Never add/remove tools mid-session (use state-transition messages or `defer_loading` stubs instead); never change models mid-session.
3. Forked operations (compaction, summarization) must reuse the parent's exact prefix — Claude Code appends the compaction prompt as a user message to the identical prefix instead of a separate call.
4. Kill timestamps/shuffled tool order/nondeterministic JSON in the prefix.

Cache mechanics as of Aug 2026: ≤4 breakpoints, 5-min TTL refreshed on hit, 1-hour opt-in at 2x write cost, reads at 0.1x; minimum cacheable prefixes 512–4,096 tokens depending on model [mnemoverse.com](https://mnemoverse.com/docs/library/prompt-cache-stable-prefix). **hermes-agent is the reference implementation of this discipline**: file-backed memory is snapshotted once at session start and frozen (`format_for_system_prompt()` returns the snapshot, never live state), mid-session writes hit disk but become prompt-visible only next boot, the rendered prefix is persisted in SessionDB so eviction/restart replays identical bytes against a warm cache, and a four-block sliding window of `cache_control` breakpoints covers system + last three messages. The cautionary tale: the Honcho integration rewrote a system-prompt layer every N turns → 100% cache miss, ~20K-token full prefill per turn (hermes-agent issue 13631) [bryanyzhu/agentic-ai-system-course](https://github.com/bryanyzhu/agentic-ai-system-course/blob/main/course/04-prompts-context-cache.md), [mnemoverse](https://mnemoverse.com/docs/library/prompt-cache-stable-prefix).

### Memory-write discipline: mid-turn vs session-end

Three shipped models, each coherent [nicolasbustamante.com](https://nicolasbustamante.com/blog/agent-memory-engineering):

- **Synchronous mid-turn** (Claude Code, Hermes): user-visible corrections land immediately, user can object; prompt stays frozen (freshness deferred to next session). Right default for interactive harnesses.
- **Deferred batch/offline consolidation** (Codex): after ≥6h idle, a small model extracts structured memories from the rollout, then a stronger model consolidates the canonical handbook inside a git-baselined memory folder. Right default for cloud/background rollouts; recency lag is the price.
- **Sleep-time agents** (Letta, Letta 0.7.0+ / "Dreaming"): a second agent owns memory-editing tools and continuously revises learned context between active tasks; configurable cadence (after N steps or at compaction) [docs.letta.com sleeptime](https://docs.letta.com/guides/agents/architectures/sleeptime). Research backing: amortized sleep-time compute cuts test-time compute ~5x at equal accuracy [arXiv:2504.13171](https://arxiv.org/html/2504.13171v1).

Structural invariant everyone converges on: **bounded always-loaded budget, unbounded body content** (index in prompt, bodies on demand), plus cheap verification-on-read (age stamps) to catch stale paths/facts.

---

## 4. Recommendation

Opinionated, tuned to: three harnesses (hermes-agent, Claude Code, opencode), a diagnostic agent swarm, hard local-first constraint, existing mempalace fork + gbrain + prior Mem0 exit.

### Target architecture — four layers, one owner each

```
T0 KERNEL (always-loaded, frozen per session)
  SOUL.md / CLAUDE.md / AGENTS.md — identity, invariants, workflow law. ≤200 lines,
  imperative anchors + prohibited-action framing. Hard invariants ALSO wired as
  PreToolUse hooks (block, don't ask). Byte-stable within a session (cache discipline).

T1 EPISODIC LEDGER (append-only, verbatim, git-canonical) ← KEEP YOUR EXISTING DESIGN
  Session JSONLs stay exactly as they are: immutable raw evidence, mined-but-never-deleted.
  Evidence: verbatim dated chunks were the single biggest recall lever in 2026 (Omi
  ~51%→86.6% LoCoMo). Wire capture via MemPalace hooks (stop/preCompact mines the
  transcript synchronously before compaction eats it) instead of bespoke glue.

T2 SEMANTIC STORE + SEARCH-FIRST GATE (single OSS store: MemPalace)
  Scoped search (wings=projects/people) + SQLite temporal KG with validity windows +
  verbatim drawers. The mandatory search-before-synthesis MCP gate STAYS — enforce it in
  T0 text AND structurally (session-start hook injects recall; swarm workers get scoped
  search stubs). Pluggable backends let you point it at pgvector/Qdrant if you want one
  vector infra shared across machines.

T3 VAULT/WIKI (curated distillates, human-readable, git-tracked)
  Karpathy llm-wiki layout: raw/ (immutable sources) → research/ (draft, status:draft)
  → articles/ (canonical, explicit consolidate promotion), index.md + log.md, AGENTS.md
  schema. Decisions/ADRs/diagnoses live here — NOT in the vector store. Obsidian as UI;
  add qmd or the llm-wiki-plugin's local BM25+FastEmbed RRF search only past ~100 pages
  of index strain. Union index+full-text results; additive-only so recall never regresses.
```

### Which single OSS store: **MemPalace**

Rationale against the field, given the constraints:

- vs **Mem0**: Mike already exited; graph accuracy is paywalled Pro, cloud gravity, contested self-reported benchmarks (49.0 independent vs 94.4 claimed on LongMemEval). No reason to return.
- vs **Zep**: best-in-class temporal semantics but the product is SaaS-first; Graphiti alone means running graph infra yourself. MemPalace ships the same validity-window semantics on local SQLite.
- vs **Letta**: wrong shape — it wants to own the runtime; Mike has three runtimes and needs a layer beneath them.
- vs **cognee**: credible alternative if he wanted heavy document-graph synthesis, but heavier ops and its recall is graph-shaped; the diagnostic-swarm workload is transcript-scoped recall, which is MemPalace's home turf.
- vs **gbrain**: closest competitor and already installed. But MemPalace wins on the specific 2026 features a *swarm* needs: verbatim multi-harness transcript mining with parsers for Claude Code/Codex/Gemini/Continue/Pi, lifecycle hooks on every harness family, hub-proxied MCP sessions sized for 50-agent fleets, and **logstream coordination** — append-only cross-machine event layer with wait/ack handoffs so agents delegate without a human relay (v3.7.0/v3.8.0, Aug 2026). Its Hermes provider PR (#1684) implements the exact `MemoryProvider` ABC hermes-agent scans for; landing it in his fork is a weekend, not a project. Upstream is the most actively shipping local-first project surveyed (five releases across Jun–Aug 2026).
- **gbrain is not deleted — it's demoted.** Its markdown-brain-repo is exactly a T3 vault with opinions; its typed graph is deterministic and good. Keep it read-only as a secondary brain (`gbrain mounts` exists for this) or export its pages (plain markdown, `gbrain export`) into the wiki and retire the second write path. Two live write-paths for memory guarantees drift — the one thing a cross-harness memory layer must not have.

### Migration from the 5-tier pipeline

1. **Session JSONL → unchanged.** Still the canonical episodic ledger; now also the input to `mempalace mine --mode convos` (idempotent, append-only, resumable) driven by stop/preCompact hooks per harness.
2. **context.jsonl → replaced** by T0 kernel files (per harness: CLAUDE.md / AGENTS.md / Hermes MEMORY.md+USER.md) with bounded budgets and frozen-at-session-start semantics — matching hermes-agent's native snapshot model so no harness fights the cache.
3. **semantic.jsonl (hand-curated ledgers) → promoted to T3 wiki articles** with explicit draft→canonical promotion; git history preserved. Machine-derived facts move to MemPalace drawers/KG, not prose ledgers.
4. **Vector/graph store + mandatory search gate → collapsed into MemPalace.** Keep the gate; strengthen it: kernel rule ("no synthesis without a scoped search citation"), session-start recall injection, and for opencode/hermes the store's own MCP tools. Backfill: replay historical JSONLs through the miner once; verify drawer counts per wing before deleting anything.
5. **Add offline consolidation (new tier, Codex/Letta-proven):** a nightly/sleep-time job (local omlx model fits — non-blocking work per routing discipline) that reads the day's ledger deltas, updates KG validity windows, proposes wiki drafts (`status: draft` only), and prunes decayed graph edges. Mid-turn writes remain synchronous-and-small (corrections to kernel/store); heavy synthesis happens between sessions.
6. **Eval harness before feature work:** freeze 50–100 golden probes from real past sessions (temporal + multi-hop weighted), neutral judge, run against the store on every upgrade — the direct lesson of the 2026 benchmark-audit mess.

### Non-goals / traps flagged by the evidence

- Don't chase vendor leaderboard deltas; the reproducible spread is enormous (94.4 claimed vs 73.8/49.0 observed) and the audit showed prompt-engineered judges, not better memory.
- Don't put dynamic memory or timestamps in any cached prefix (hermes-agent issue 13631: 100% miss).
- Don't rely on prose for hard invariants — hooks and permission gates survive compaction; instructions don't.
- Don't expect cross-session *cognitive* consistency (implicit constraints) from any store — LoCoMo-Plus shows it's unsolved; compensate with explicit constraint surfacing in T0/T3.
- PGLite gotcha if gbrain stays on macOS 26: embedded WASM engine crashes on Apple Silicon macOS 26.x — use Homebrew Postgres+pgvector per its docs.

---

## SOURCES

- [Agent Memory in 2026: Mem0 vs Letta vs Zep vs LangMem benchmarked — hamzashabbir.dev](https://hamzashabbir.dev/article/agent-memory-mem0-vs-letta-vs-zep-vs-langmem-benchmark-2026)
- [Open-source AI agent memory incl. MemPalace scoreboard — rohitraj.tech](https://rohitraj.tech/en/notes/open-source-ai-agent-memory-mem0-vs-zep-letta-2026)
- [Mem0 vs Zep vs Letta: vendor-score provenance table — digitalapplied.com](https://www.digitalapplied.com/blog/open-source-agent-memory-mem0-letta-zep-compared)
- [Mem0 vs Zep vs Letta architectures + Zep rebuttal — aibootstrapperacademy.com](https://aibootstrapperacademy.com/blog/mem0-vs-zep-vs-letta-ai-agent-memory-guide)
- [Benchmark landscape: LoCoMo/LongMemEval/BEAM + provenance — AgenticWire](https://www.agenticwire.news/article/mem0-zep-letta-agent-memory)
- [AI Memory Benchmarks 2026 — mem0.ai](https://mem0.ai/blog/ai-memory-benchmarks-in-2026)
- [The state of AI memory 2026: claimed vs observed (audit) — maximem.ai](https://www.maximem.ai/blog/state-of-ai-memory-2026-claimed-vs-observed)
- [Framework comparison tables + pricing traps — blog.appxlab.io](https://blog.appxlab.io/2026/04/13/ai-agent-memory-frameworks/)
- [Production practices for memory stacks — callsphere.ai](https://callsphere.ai/blog/td30-fw-mem0-vs-zep-vs-letta-2026-honest-comparison-guide)
- [Omi long-term memory benchmarks (verbatim-chunk finding) — github.com/BasedHardware/omi-memory-benchmarks](https://github.com/BasedHardware/omi-memory-benchmarks)
- [LoCoMo dataset — Snap Research](https://snap-research.github.io/locomo/)
- [LoCoMo-Plus (ACL 2026) cognitive-memory gap — aclanthology.org](https://aclanthology.org/2026.acl-long.1150.pdf)
- [TiMem temporal-hierarchical consolidation — arxiv.gg/abs/2601.02845](https://arxiv.gg/abs/2601.02845)
- [E-mem episodic context reconstruction — alphaxiv.org](https://www.alphaxiv.org/overview/2601.21714)
- [Agent Memory Benchmark leaderboard — agentmemorybenchmark.ai](https://agentmemorybenchmark.ai/dataset/locomo)
- [MemPalace releases v3.4–v3.8.0 — github.com/MemPalace/mempalace/releases](https://github.com/MemPalace/mempalace/releases)
- [MemPalace overview (verbatim, backends, 44 MCP tools) — ai-tldr.dev](https://ai-tldr.dev/tools/mempalace/)
- [MemPalace Hermes memory-provider PR #1684 — github.com/MemPalace/mempalace/pull/1684](https://github.com/MemPalace/mempalace/pull/1684)
- [cognee GitHub (30.2k stars, Apache 2.0) — github.com/topoteretes/cognee](https://github.com/topoteretes/cognee)
- [Cognee review (v1.4.0 Jul 2026) — dev.to](https://dev.to/andrew-ooo/cognee-review-open-source-ai-memory-for-agents-2cei)
- [Basic Memory — basicmemory.com / docs.basicmemory.com / github.com/basicmachines-co/basic-memory](https://github.com/basicmachines-co/basic-memory)
- [Memobase docs (hosted vault, RLS, not zero-knowledge) — memobase.ai/docs](https://memobase.ai/docs/)
- [memoripy (v0.1.2, stale) — github.com/caspianmoon/memoripy](https://github.com/caspianmoon/memoripy)
- [Claude Code memory docs (CLAUDE.md, Auto Memory, compaction survival) — code.claude.com/docs/en/memory](https://code.claude.com/docs/en/memory)
- [Claude Code memory limits analysis — vectorize.io/articles/claude-code-memory](https://vectorize.io/articles/claude-code-memory)
- [CLAUDE.md compaction exemption issues — anthropics/claude-code #44166](https://github.com/anthropics/claude-code/issues/44166), [#68636](https://github.com/anthropics/claude-code/issues/68636), [#48959](https://github.com/anthropics/claude-code/issues/48959)
- [Context engineering cookbook (compaction/clearing/memory primitives) — platform.claude.com](https://platform.claude.com/cookbook/tool-use-context-engineering-context-engineering-tools)
- [Effective context engineering for AI agents — anthropic.com/engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- [Lessons from building Claude Code: prompt caching — claude.com/blog](https://claude.com/blog/lessons-from-building-claude-code-prompt-caching-is-everything)
- [Write/Select/Compress/Isolate playbook — dreaming.press](https://dreaming.press/posts/context-engineering-playbook-write-select-compress-isolate.html)
- [Editing vs compaction vs memory tool — dreaming.press](https://dreaming.press/posts/context-editing-vs-compaction-for-long-running-agents.html)
- [Stable-prefix contract + cache-breaker catalog — mnemoverse.com](https://mnemoverse.com/docs/library/prompt-cache-stable-prefix)
- [Prompt-cache chapter incl. hermes-agent snapshot/SessionDB design — bryanyzhu/agentic-ai-system-course](https://github.com/bryanyzhu/agentic-ai-system-course/blob/main/course/04-prompts-context-cache.md)
- [Agent Memory Engineering (Hermes/Codex/Claude Code write-discipline comparison) — nicolasbustamante.com](https://nicolasbustamante.com/blog/agent-memory-engineering)
- [Context Repositories (git-backed MemFS) — letta.com/blog/context-repositories](https://www.letta.com/blog/context-repositories/)
- [Letta sleep-time agents — letta.com/blog/sleep-time-compute](https://www.letta.com/blog/sleep-time-compute/) and [docs.letta.com sleeptime](https://docs.letta.com/guides/agents/architectures/sleeptime)
- [Sleep-time compute paper — arXiv:2504.13171](https://arxiv.org/html/2504.13171v1)
- [Karpathy llm-wiki gist (Apr 2026) — gist.github.com/karpathy/442a6bf555914893e9891c11519de94f](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
- [LLM Wiki plugin (local hybrid search impl) — github.com/praneybehl/llm-wiki-plugin](https://github.com/praneybehl/llm-wiki-plugin)
- [llm-wiki-vault (.brain persistence layer) — github.com/MirkoSon/llm-wiki-vault](https://github.com/MirkoSon/llm-wiki-vault)
- [Karpathy pattern guide — mindstudio.ai](https://www.mindstudio.ai/blog/karpathy-llm-wiki-knowledge-base-pattern) and [openknowledge.ai](https://openknowledge.ai/docs/workflows/karpathy-llm-wiki)
- [GBrain overview — vectorize.io/articles/what-is-gbrain](https://vectorize.io/articles/what-is-gbrain)
- [GBrain implementation tutorial (BrainBench, 74 MCP tools) — marktechpost.com](https://www.marktechpost.com/2026/05/22/a-step-by-step-coding-tutorial-to-implement-gbrain-the-self-wiring-memory-layer-built-by-y-combinators-garry-tan-for-ai-agents/)
- [GBrain CLAUDE.md/architecture (memory verbs, mounts, storage tiering) — github.com/garrytan/gbrain](https://github.com/garrytan/gbrain/blob/HEAD/CLAUDE.md)
- [Context engineering practical guide — sourcegraph.com/blog/context-engineering](https://sourcegraph.com/blog/context-engineering)
