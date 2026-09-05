# Automated Obsidian Second-Brain Pipelines — Research Digest

**Date:** 2026-08-26 · **Scope:** auto-classify/tag/link an ~8k-file mixed markdown corpus (skills, prompts, research digests, news briefs, entity notes) with Obsidian as the human-visible layer. Local-first, free.
**Verification:** every plugin/project below was checked for 2025–2026 activity; dead or unverifiable items are flagged as such.

---

## Summary (10 lines)

1. **Bases is the new center of gravity**: core plugin since Obsidian 1.9 (public Aug 2025), `.base` files over YAML properties; table/cards at 1.9, list/map at 1.10. It replaces most Dataview tables — and Dataview is now explicitly maintenance-mode (author building Datacore).
2. **Architecture consensus 2026**: shallow stable folders + controlled type tags + frontmatter properties for machine queries, MOCs (LYT-style) for human navigation; PARA alone buries knowledge in Archive — use it only as the top-level skeleton.
3. **LLM plugins all run local now**: Smart Connections v4 (local transformers.js embedder by default), Copilot V4 (BYOK OpenAI-compatible endpoints incl. Ollama/LM Studio → works with omlx), Khoj self-hosted (Ollama/OpenAI-compatible backend).
4. **MLX does support embeddings** — but via separate packages (`mlx-embeddings`, `mlx-community/bge-m3-mlx-*`, OpenAI-compat servers like `aperepel/mlx-serve-embeddings`), not necessarily through Mike's existing omlx chat route.
5. **Recommended single embedder: bge-m3** (1024-dim, MIT, 8192-token ctx) served by a `llama-server --embedding` sidecar with `/v1/embeddings` — one endpoint every tool can share; keep Smart Connections' internal micro-model as its own in-app index rather than trying to unify vector stores in v1.
6. **Auto-classification**: two-tier — embedding kNN/SetFit-style zero-shot against a controlled vocabulary first (HF docs: outperforms bart-large-mnli zero-shot, ~67× faster), local LLM fallback only for low-confidence docs.
7. **Dedupe/near-dupe**: sha256 exact pass then `datasketch` MinHashLSH (v2.0, active) on normalized text (frontmatter/wikilinks stripped).
8. **Graph hygiene is a scheduled job**, not a plugin: weekly orphan sweep, cluster→MOC-candidate generation with *human approval*, naming conventions (stable kebab-case slugs, aliases for renames), tag taxonomy file as source of truth.
9. **Dendron's sunset is the cautionary tale**: enforced hierarchy + schemas scaled well but died with its tool — keep everything plain markdown and let links/MOCs emerge.
10. **wheat.ws/obsidian-scripts could not be verified** (domain unreachable, no index hits) — substitute verified equivalents below.

---

## 1. Vault architecture patterns (2026)

### Three competing patterns, one synthesis

| Pattern | Primitive | Strength | Failure mode |
|---|---|---|---|
| **PARA** (Tiago Forte) | 4 folders by actionability (Projects/Areas/Resources/Archives) | Trivial onboarding; sorts *where things live* | "Archive black hole": finished-project notes become unfindable [S1] |
| **LYT / MOCs** (Nick Milo) | Maps of Content — index notes that curate links; Home note on top | Emergent structure; a note lives in many MOCs; AI-friendly entry point (one MOC = whole topic landscape) [S2][S3] | Needs curation discipline |
| **Entity-graph** (person/org/topic/product notes) | Atomic entity pages + typed wikilinks; Karpathy's "LLM builds the wiki" pattern revived this in 2025–26 [S4][S5] | Graph view becomes genuinely navigable; retrieval walks links instead of chunk-RAG | Entity sprawl without governance |

The 2026 practitioner consensus (and the right call for agent-written corpora): **PARA-shaped top folders + LYT-style MOC layer + entity-graph inside Resources/topics**. Folders answer "where does this file live" (shallow, ≤2 levels deep — deep folders are where notes go to die [S6]); tags/frontmatter answer "what is this"; wikilinks/MOCs answer "how does this connect." A March 2026 comparison found LYT the most AI-compatible of the three because a MOC gives an agent the whole topic map in one read [S3]; dsebastien's LYT notes make the same point about MOCs as navigational hubs distinct from folders/tags [S2].

### Frontmatter schema people actually standardize on

Converged fields across the sources:

```yaml
---
type: digest            # controlled vocab: skill|prompt|digest|brief|person|org|product|topic|daily
status: processed       # inbox|processed|moc-candidate|archived
source: "https://..."   # or repo://path for retired-repo imports
created: 2026-08-26
updated: 2026-08-26
topics: [embeddings, obsidian]   # CONTROLLED vocabulary (machine-written)
tags: [whatever]                 # loose discovery tags (human/liberal)
aliases: ["BGE-M3"]              # alternate names → stable wikilinks
up:                              # parent MOCs (LYT convention)
  - "[[Embeddings MOC]]"
related:
  - "[[llama.cpp]]"
---
```

Evidence: LYT practitioners standardize on `up:` / `collection:` / `related:` / `says:` so cards auto-surface in MOCs [S3]; the obsidian-llm-wiki plugins write exactly `tags/type/aliases/sources(/relations)` on every generated page so Dataview/Bases work out of the box [S4][S5]; typed-relations frontmatter (`contradicts`, `supports`, `is-a`, `depends_on`) is the emerging extension for semantic graph queries [S5]. Obsidian's native Properties UI (since 1.4) makes YAML-first metadata human-editable [S7].

### Folder taxonomy for agent-written notes

Recommendation for Mike's corpus shape (validated against [S6][S8]):

```
00_inbox/            # nightly digests land here raw
10_skills/
20_prompts/
30_digests/YYYY/     # only place a date-based level is justified
40_topics/           # topic notes (concept/product)
50_entities/people|orgs/
60_daily/            # optional
90_archive/          # retired-repo imports that classify < threshold
_meta/               # taxonomy.md, dashboards (.base), pipeline state
```

Rules of thumb from the sources: never >2–3 folder levels [S6]; don't mirror folders in tags (double bookkeeping) [S6]; put structural tags in frontmatter, not inline scatter [S8]; keep core structural tags under ~50 total [S8].

---

## 2. Automation toolchain

### Inside Obsidian (human-visible layer)

| Tool | State (verified) | Role in this system |
|---|---|---|
| **Bases** (core) | Shipped public in 1.9.x Aug 2025; `.base` YAML format; table/cards views (1.9), list/map (1.10); data stays plain markdown+YAML [S9][S10] | Human dashboards: digests-by-topic table, inbox triage view, status boards. No community-plugin risk — it's core. |
| **Dataview** | Author confirmed maintenance mode, successor **Datacore** in progress (npm 0.1.24 May 2025; still power-user stage) [S11][S12] | Legacy only. Don't build new dependencies on dataviewjs. |
| **Templater** | Very active: v2.25.0 released 2026-08-05; steady monthly releases through 2025–26 [S13] | Note templates per `type`; frontmatter scaffolding on manual captures. |
| **Smart Connections v4** | Active (4.5.3, Jun 2026). Local embeddings by default via transformers.js (`TaylorAI/bge-micro-v2` class models); optional Ollama adapter; Pro split moved API-model routing to paid tier; new **Connections-in-Bases** (`score_connection`, `list_connections`) renders similarity columns inside .base tables [S14][S15][S16] | The in-app link-suggestion surface. Zero-setup, fully offline default path. |
| **Copilot for Obsidian** | V4 (2026): ground-up rewrite around agents — runs opencode/Claude Code/Codex natively in the vault; free tier fully usable with BYOK incl. any OpenAI-compatible local endpoint (Ollama/LM Studio/custom) + local Miyo search index [S17][S18] | Optional chat/QA over the vault pointing at omlx as custom provider. Not needed for the pipeline itself. |
| **Khoj** (self-hosted) | Active; Docker/pip server + Obsidian sync client; supports Ollama/OpenAI-compatible backends (`OPENAI_BASE_URL`); default local embed model; pgvector index [S19][S20] | Optional second-layer RAG/search over the vault if Mike wants query-side recall beyond Obsidian. Skip for v1 — redundant with Smart Connections. |

### Headless pipeline (Python, outside Obsidian)

All verified maintained in 2025–2026 unless noted:

- **python-frontmatter** (eyeseast) — parse/normalize/write YAML frontmatter; v1.3.0 May 2026, py3.14-tested [S21].
- **trafilatura** (adbar) — main-content extraction for nightly web digests before they hit the inbox; actively maintained, and already used in 2026-era capture scripts of vault-automation projects [S22].
- **tiktoken** (openai) — token counting for chunk budgets before embedding; active [S23].
- **datasketch** (ekzhu) — MinHash/MinHashLSH near-dupe detection; v2.0 changed the default permutation scheme (`affine32`) fixing similarity over-estimation bias — rebuild persisted sketches after upgrade [S24].
- **Entity/link builders**: `wheat.ws/obsidian-scripts` — **UNVERIFIED** (site unreachable, no search footprint). Working substitutes verified instead:
  - **Ankush-Chander/obsidian-entity-linker** — links note titles/selections to Wikidata/Wikipedia/OpenAlex entities [S25].
  - **green-dalii/obsidian-llm-wiki** & **ignromanov/llm-obsidian-wiki** — 2026 implementations of Karpathy's LLM-as-librarian wiki pattern: ingest note → extract entities/concepts → generate interlinked wiki pages with provenance frontmatter; include lint/dedupe/orphan tooling [S4][S5]. The green-dalii variant deliberately avoids embeddings entirely (lex fast-path + keyword generation + Personalized PageRank over the wikilink graph) because most local providers lack `/v1/embeddings` [S4].
  - **Ar9av/obsidian-wiki cross-linker skill** — scoring rubric for inserting missing wikilinks (exact name match +4, shared tags +2, peripheral→hub +2 …) with conservative inline-linking rules [S26].

### Local embedding servers (the decision point)

| Server | Endpoint | Notes |
|---|---|---|
| **llama.cpp `llama-server`** | `--embedding --pooling mean` → OpenAI-compatible `/v1/embeddings`; reranking endpoint too [S27][S28] | Runs any GGUF embed model (bge-m3, bge-small-en-v1.5, nomic-embed, MiniLM, EmbeddingGemma). One binary, Metal-accelerated. |
| **Ollama** | `POST /api/embed`, batch input array, L2-normalized output, optional dimension truncation [S29][S30] | Easiest ops; `ollama pull bge-m3` / `nomic-embed-text`. |
| **fastembed** (qdrant) | In-process Python lib, ONNX Runtime CPU, no PyTorch deps; active release cadence into 2026 [S31] | Best when you want zero servers: `pip install fastembed`, BGE-small default, runs anywhere. |
| **MLX ecosystem** | `Blaizzy/mlx-embeddings` supports XLM-RoBERTa/BERT/ModernBERT/NomicBERT/Qwen3-embedding archs; `mlx-community` hosts bge-m3 fp16/6bit/8bit and Qwen3-Embedding conversions; `aperepel/mlx-serve-embeddings` wraps MLX embedders in an OpenAI-compatible API [S32][S33][S34][S35] | **Does MLX support embed models? Yes — but through dedicated packages, not necessarily through omlx's existing chat route** (mlx-lm is generation-focused). LM Studio notably fails to recognize some MLX embed conversions as embedding-type models (lmstudio bug #808, cited in [S35]) — expect rough edges outside llama.cpp/Ollama. |

---

## 3. Auto-classification approaches

### Topic tagging (zero-shot)

Three viable tiers, cheapest first:

1. **Embedding kNN against seed exemplars** — embed 5–10 hand-picked example notes per category once; classify newcomers by nearest-centroid/cosine. This is SetFit's zero-shot recipe: HF's own docs show templated-synthetic-example SetFit **outperforms** the transformers `bart-large-mnli` zero-shot pipeline while being **~67× faster**, using the same sentence-transformer body you already run for search [S36]. Reuses the pipeline's single embedder — no second model.
2. **NLI zero-shot classifier** — `MoritzLaurer/mDeBERTa-v3-base-xnli` family or browser-scale `Xenova/nli-deberta-v3-xsmall` via transformers.js; each label becomes an entailment hypothesis [S37][S38]. Better when categories have no exemplars yet; slower.
3. **Local LLM structured-output tagging** — prompt omlx with the controlled vocabulary + note excerpt, require JSON `{type, topics[], confidence}`. IBM's EMNLP study confirms LLMs are strong zero-shot topical classifiers but at much higher cost/latency [S39]. Reserve as fallback for docs where kNN confidence < threshold; write low-confidence docs to `_inbox/review-queue.md` instead of guessing.

**Governance rule (prevents tag soup):** the classifier may only emit labels from `_meta/taxonomy.md`. Unknown-but-repeated labels go to a proposal list a human merges weekly — exactly the controlled-vocabulary pattern used by the obsidian-wiki tag-taxonomy skill (canonical list + alias mapping + max-tags rule + migration renames) [S26].

### Clustering for MOC candidates

With one shared embedder, UMAP/HDBSCAN or simple agglomerative clustering over note vectors yields candidate clusters → draft MOC stubs. This is the same mechanism Vault Audit AI (zinverno/obsidian-ai-hub) ships: audit → thematic clustering → **MOC generation from saved clusters**, plus orphan detection [S40]. Generate drafts; never auto-publish MOCs.

### Dedupe / near-dupe

Two passes: (1) sha256 over normalized body for exact dupes; (2) `datasketch.MinHashLSH(threshold≈0.5, num_perm=128)` over word shingles after stripping frontmatter/wikilinks/code fences. Datasketch 2.0's benchmarks: precision/recall 0.92–1.0 in the dedupe shape (near-dupes at Jaccard 0.6–0.95), sub-millisecond LSH queries vs linear scan, ~100× faster at scale [S24]. Keep the newest file, fold older paths into `superseded_by:` frontmatter.

### Link suggestion

- In-app: Smart Connections' Connections view — chunked local embeddings, cosine similarity, drag-to-insert; algorithm details (chunk/block-level scoring, configurable ranking/rerank in Pro) documented [S14][S15][S16].
- Offline (pipeline writes suggestions, human accepts): score candidate links with the cross-linker rubric [S26], write top-N into `link_suggestions:` frontmatter or a per-note review section. Never inject body wikilinks unattended.

---

## 4. Graph hygiene

- **Orphan sweeps (weekly)**: Vinzent03/find-unlinked-files lists no-backlink files, broken links, empty files/folders; can archive instead of delete [S41]. Equivalent headless check is trivial in Python (parse `\[\[...\]\]` + frontmatter links, diff against filenames/aliases). Also sweep *orphan tags* (used once) during the same job [S8].
- **Hub-note generation (auto-MOC)**: cluster → draft MOC → human approve (see §3). Size caps borrowed from llm-obsidian-wiki's topology verifier: index ≤100 links, hub ≤15 members, split overgrown hubs [S5]. AutoMOC (dalcantara7) pulls missing linked/tagged mentions into an open MOC at cursor — good interactive complement [S42].
- **Naming conventions for stable wikilinks**:
  - Kebab-case slugs, no dates in entity/topic titles (dates belong in `created:`).
  - Disambiguate collisions by parenthetical type: `OpenAI (org)` vs `GPT-5 (product)`.
  - Every rename goes into `aliases:` — old wikilinks keep resolving; the cross-linker matches title *and* aliases when detecting unlinked mentions [S26].
  - Prefer shortest unambiguous link form `[[name]]`, not full paths [S26].
- **Tag taxonomy governance**: isolate structural namespaces (`type/`, `status/`, `source/`) so queries never pollute [S43]; liberal topic tags are fine — multiple redundant tags create multiple rediscovery paths, and chaos beats scarcity because it self-regulates and gets cleaned in quarterly reviews [S44]. Machine-written tags = controlled vocabulary only; human tags = free. Don't replicate folder structure in tags [S6].
- **Dendron sunset lessons** (verified: README states "maintenance only, active development has ceased", discussion #3890) [S45]: Dendron proved hierarchy+schemas scale to 10k+ notes, but coupling organization to one editor's extension API killed it. Lessons adopted here: (1) all structure must survive app death → plain markdown + YAML only; (2) prefer emergent links/MOCs over enforced trees; (3) schemas belong in a linter, not in storage format.

---

## 5. Recommended v1 pipeline for Mike

Opinionated. Nightly cron + one weekly job. Everything local, $0.

```
nightly:
  0. INTAKE      nightly digest scrape → trafilatura extract → _00_inbox/YYYY-MM-DD-slug.md
                 retired-repo import: copy tree → _90_archive/<repo>/ untouched
  1. NORMALIZE   python-frontmatter: enforce schema keys, ISO dates, kebab-case slug,
                 aliases merge, strip stale fields; write back atomically
  2. DEDUPE      sha256 exact → datasketch MinHashLSH (thr 0.5) near-dupes;
                 mark losers superseded_by: [[winner]]; log, don't delete
  3. CLASSIFY    embed via sidecar → kNN vs seed exemplars per category (SetFit-style);
                 confidence ≥ τ: write type+topics from taxonomy
                 else: omlx LLM structured-tagging attempt → else review queue
  4. PLACE       move by type → 10_skills/… 30_digests/YYYY/ 50_entities/…
                 status: inbox→processed; never move files humans edited that day
  5. LINK-SUGGEST top-5 cosine neighbors (same embedder) scored w/ cross-linker rubric
                 → write link_suggestions: frontmatter only
weekly:
  6. HYGIENE     orphan report, broken-link report, single-use tag report → one digest note
  7. MOC SWEEP   cluster week's new notes → draft MOC diffs appended to review queue;
                 apply last week's APPROVED MOC changes
```

**Which single embedder:** adopt **bge-m3 served by a llama.cpp sidecar** — `llama-server -m bge-m3-Q8_0.gguf --embedding --pooling mean --port 8081` exposing `/v1/embeddings` [S27][S33]. Reasons: MIT license, 1024-dim, 8192-token context (digest-length chunks without splitting), multilingual headroom, GGUF availability, and one OpenAI-shaped endpoint Copilot (custom BYOK provider), Khoj, and the Python pipeline can all target. MLX *can* serve embeddings faster on Apple Silicon (~prefill-bound gains per third-party benchmarks [S34]) and mlx-community has bge-m3-MLX conversions [S33] — worth a phase-2 swap via `aperepel/mlx-serve-embeddings` [S35] **if** Mike's omlx lacks an embeddings route (test: `curl http://localhost:<omlx>/v1/embeddings -d '{"model":"...","input":"ping"}'`). Until that curl succeeds, the llama.cpp sidecar is the boring, correct choice. Do **not** try to make Smart Connections reuse your vector store — leave its built-in micro-model indexing the vault independently [S14]; duplicate indexes at 8k files cost seconds, not dollars.

**In-Obsidian stack for v1:** enable core Bases (dashboards: inbox triage, digests-by-topic, status board) + Templater (capture templates) + Smart Connections (in-app related-notes) + find-unlinked-files (weekly hygiene click-through). Optional later: Copilot V4 pointed at omlx for vault QA; Khoj only if he wants phone/web query access.

**What stays manual (deliberately):**
- Approving MOC creation/edits and entity-page promotion from review queue.
- Taxonomy changes (add/merge/rename canonical tags) — the pipeline proposes, Mike disposes.
- All deletes/archives (rule: pipeline only marks `superseded_by`/`status: archived`).
- Accepting injected body wikilinks — suggestions stay in frontmatter until touched.
- Final placement judgment calls for ambiguous notes (review queue, ≤ handful/day expected).

---

## SOURCES

- [S1] PARA overview & critique (actionability, Archive burial) — https://www.apragmaticmind.com/blog/para-method
- [S2] LYT / MOC definitions (dsebastien notes) — https://notes.dsebastien.net/10+Meta/99+AI+Assistant/Wikis/PKM/AI+Wiki+-+PKM+-+Linking+Your+Thinking
- [S3] LYT vs PARA vs Zettelkasten with AI, `up:/collection:/related:/says:` schema — https://yu-wenhao.com/en/blog/lyt-framework-guide/
- [S4] green-dalii/obsidian-llm-wiki (Karpathy-pattern wiki builder, PPR retrieval, no-embeddings rationale) — https://github.com/green-dalii/obsidian-llm-wiki ; Karpathy gist: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
- [S5] ignromanov/llm-obsidian-wiki (typed relations, hub caps, capture scripts incl. trafilatura) — https://github.com/ignromanov/llm-obsidian-wiki
- [S6] Tags vs folders; shallow stable folders; no folder-mirroring in tags — https://danholloran.me/posts/tags-vs-folders-in-obsidian-how-to-organize-your-vault
- [S7] Obsidian Bases intro (properties/YAML backing) — https://www.mintlify.com/obsidianmd/obsidian-help/bases/introduction
- [S8] Broad-folders/specific-tags method; nested tags; ≤50 structural tags — https://notes-automate.com/posts/understanding-the-difference-between-folders-and-tags-obsidian/
- [S9] Obsidian 1.9.10 Desktop public — Bases announcement — https://obsidian.md/changelog/2025-08-18-desktop-v1.9.10/
- [S10] Bases views table (table/cards 1.9; list/map 1.10) — https://github.com/obsidianmd/obsidian-help/blob/029ba842/en/Bases/Views.md
- [S11] Dataview maintenance-mode confirmation (issue #749 thread) — https://github.com/blacksmithgu/obsidian-dataview/issues/749
- [S12] Datacore WIP successor — https://github.com/blacksmithgu/datacore (npm: https://registry.npmjs.org/@blacksmithgu/datacore)
- [S13] Templater changelog/releases (2.25.0, 2026-08-05) — https://github.com/SilentVoid13/Templater/blob/master/CHANGELOG.md ; https://github.com/silentvoid13/Templater/releases/tag/2.25.0
- [S14] Smart Connections README (v4, local default, Pro split, Connections-in-Bases, 4.5.3 Jun 2026) — https://github.com/brianpetro/obsidian-smart-connections/
- [S15] Smart Connections site (local-first retrieval boundary) — https://smartconnections.app/smart-connections/
- [S16] Smart Connections embedding internals (transformers.js, TaylorAI/bge-micro-v2, Ollama adapter) — https://deepwiki.com/brianpetro/obsidian-smart-connections/3.1-embedding-models
- [S17] Copilot for Obsidian README (V4, agents, BYOK/local, Miyo) — https://github.com/logancyang/obsidian-copilot
- [S18] Copilot local setup doc (Ollama/LM Studio endpoints, local embeddings) — https://github.com/logancyang/obsidian-copilot/blob/master/local_copilot.md
- [S19] Khoj self-host setup (Obsidian client, OPENAI_BASE_URL→Ollama/vLLM/LM Studio) — https://docs.khoj.dev/get-started/setup/
- [S20] Khoj repo & Ollama integration — https://github.com/khoj-ai/khoj/ ; https://docs.khoj.dev/advanced/ollama
- [S21] python-frontmatter v1.3.0 (2026-05-20) — https://github.com/eyeseast/python-frontmatter/releases/tag/v1.3.0
- [S22] trafilatura — https://github.com/adbar/trafilatura (activity corroborated via S5 capture scripts)
- [S23] tiktoken — https://github.com/openai/tiktoken
- [S24] datasketch 2.0 (MinHashLSH benchmarks, affine32 scheme change) — https://github.com/ekzhu/datasketch/ ; https://ekzhu.com/datasketch/lsh.html
- [S25] obsidian-entity-linker (Wikidata/Wikipedia/OpenAlex) — https://github.com/Ankush-Chander/obsidian-entity-linker
- [S26] Cross-linker scoring rubric + tag-taxonomy controlled vocabulary — https://github.com/Ar9av/obsidian-wiki/blob/main/.skills/cross-linker/SKILL.md ; https://github.com/Ar9av/obsidian-wiki/blob/8089bc7318d1e8d8339ae2fbd155a359ddec2eb5/.skills/tag-taxonomy/SKILL.md
- [S27] llama.cpp embeddings guide (`--embeddings`, pooling, /v1/embeddings) — https://mintlify.wiki/ggml-org/llama.cpp/inference/embeddings
- [S28] llama-server README (OpenAI-compat routes, rerank PR #9510) — https://github.com/ggml-org/llama.cpp/blob/00fa7cb2/tools/server/README.md
- [S29] Ollama /api/embed spec (batch, dimensions, truncation) — https://docs.ollama.com/api/embed
- [S30] Ollama embeddings capability page (L2-normalized) — https://docs.ollama.com/capabilities/embeddings
- [S31] fastembed (ONNX CPU, releases) — https://github.com/qdrant/fastembed ; https://github.com/qdrant/fastembed/releases
- [S32] mlx-embeddings (supported archs incl. NomicBERT, Qwen3) — https://github.com/Blaizzy/mlx-embeddings
- [S33] mlx-community bge-m3 conversions (fp16/8bit/6bit; oMLX-endpoint compatibility note) — https://huggingface.co/mlx-community/bge-m3-mlx-fp16
- [S34] Apple-Silicon embedder benchmark (MLX vs llama.cpp throughput; nomic/bge-m3/Qwen3) — https://contracollective.com/blog/local-embeddings-apple-silicon-nomic-bge-qwen3-m5-max-2026 *(third-party benchmark; treat numbers as indicative)* ; also https://mlxcommunity.com/t/embeddings-on-apple-silicon-bge-vs-nomic-vs-jina-on-mlx-15
- [S35] aperepel/mlx-serve-embeddings (OpenAI-compat MLX server; LM Studio MLX-embed bug #808) — https://github.com/aperepel/mlx-serve-embeddings
- [S36] SetFit zero-shot (beats bart-large-mnli, ~67× faster) — https://huggingface.co/docs/setfit/main/en/how_to/zero_shot ; tutorial: https://huggingface.co/docs/setfit/main/tutorials/zero_shot
- [S37] mDeBERTa-v3 NLI zero-shot classifiers — https://huggingface.co/rohithbojja/FT-mDeBERTa-v3-base-mnli-xnli (base: MoritzLaurer/mDeBERTa-v3-base-mnli-xnli)
- [S38] transformers.js in-browser zero-shot (Xenova/nli-deberta-v3-xsmall) — https://github.com/kbipul/zero-shot-tagger
- [S39] IBM, "Zero-shot Topical Text Classification with LLMs" (EMNLP 2023 findings) — https://github.com/IBM/zero-shot-topical-text-classification
- [S40] zinverno/obsidian-ai-hub (Vault Audit AI: clustering → MOC generation, orphan detection) — https://github.com/zinverno/obsidian-ai-hub
- [S41] Find orphaned files and broken links (Vinzent03) — https://github.com/Vinzent03/find-unlinked-files
- [S42] AutoMOC (linked/tagged mention import) — https://github.com/dalcantara7/obsidian-auto-moc
- [S43] Type-tag namespace isolation (`type/book` pattern) — https://www.dsebastien.net/the-tag-system-that-finally-made-sense-for-me-from-perfectionism-paralysis-to-discovery-freedom/
- [S44] Liberal topic tagging / emergence-over-planning counterpoint — same as S43 (intentional tension with S26/S8; resolved in §4 governance rule)
- [S45] Dendron end-of-development — https://github.com/dendronhq/dendron/discussions/3890 ; README banner: https://github.com/dendronhq/dendron/blob/master/README.md
