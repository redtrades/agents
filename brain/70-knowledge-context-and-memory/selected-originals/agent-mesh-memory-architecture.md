# Memory architecture — five tiers

One memory system under many harnesses. Each tier has one owner, one
retention policy, and one write path. Tiers below are ordered by
volatility: fast and raw at the bottom of the number scale, curated and
stable at the top.

```
L0 KERNEL      identity + invariants        always loaded, frozen per session
L1 SESSION     raw transcripts              ephemeral capture, never deleted
L2 LEDGERS     git-canonical events         append-only, supersede-not-mutate
L3 STORE       semantic recall              search-first gate, verbatim chunks
L4 VAULT       human-curated wiki           draft->canonical promotion
```

Reads flow up (a session consults L0 automatically, everything else on
demand). Writes flow down: curation at L4 cites evidence that lives in
L3/L2; nothing curated exists without a verbatim ancestor.

## L0 — Kernel markdown

Identity, invariants, workflow law: CLAUDE.md-class files per harness,
SOUL.md-class files per bot, AGENTS.md as the cross-harness entry.

- Budget: hard cap around 200 lines. Imperative anchors at the top;
  prohibited-action framing over passive description.
- Static-first: byte-stable within a session, rendered once at boot,
  frozen for the session (see `prompts/cache-stable-layout.md`).
- Hard invariants are never prose-only. Anything that must survive
  compaction, injection, or a model's bad day is also wired as a gate:
  blocked tool calls cannot be summarized away.
- Session-scoped pointers (current goal, active claim) do not live in
  L0; they live one tier down where they can change safely.

## L1 — Session JSONL

Raw transcripts of every session, exactly as captured: immutable,
mined freely, deleted never.

- This is evidence, not context. Nothing loads L1 wholesale into a
  prompt; mining hooks (session end, pre-compaction) extract into L3
  synchronously so compaction never eats the only copy.
- Retention: forever, cheaply. Verbatim dated chunks are the single
  biggest recall lever; storage is cheaper than the details you did not
  keep.

## L2 — Git-canonical ledgers

Append-only JSONL under version control: the event spine every agent
reads and only the orchestrator writes. Corrections are new entries
carrying `supersedes`; history is never edited.

### Common envelope

Every entry carries the envelope fields plus its type-specific payload:

```json
{"id": "CTX-<n>", "ts": "<iso8601>", "session": "<session-id>",
 "actor": "<agent-id>", "event": "<type>",
 "ref": "<issue|pr|path|commit>", "payload_hash": "<sha256 of payload>"}
```

- `id`: allocated from the ledger itself (max scan + 1), collision-safe
  across branches by convention of appending before push.
- `ref`: pointer discipline — points at committed bytes, never at
  intentions.
- `payload_hash`: lets an auditor verify the referenced artifact still
  says what the ledger claimed.

### context.jsonl — episodic work ledger

Envelope plus: `stream`, `status`, `title`, `detail`, `blocked_on`,
`next_step`. Event types include: workstream, decision, milestone,
brief-generated, open-flag, config-change, audit-finding, drift-detected,
destructive-intercept, handover, retro, supersede. One entry per major
turn; a handover entry closes every session.

### semantic.jsonl — durable rules

```json
{"id": "SR-CAN-<n>", "category": "<routing|verification|communication|
 execution|research|identity|economy>", "rule": "<imperative>",
 "rationale": "<why>", "actor": "<author-session>",
 "provenance": "<where this rule came from>"}
```

Rules are few and load-bearing. A rule nobody violates is a candidate
for deletion; a rule violated twice earns enforcement (hook or gate),
not repetition.

### Companion ledgers

| Ledger | Purpose | Key fields |
|---|---|---|
| claims.jsonl | work claims/leases | id, agent_id, branch, task, claimed_at, expires_at, state |
| active-watch.jsonl | running-process registry | name, status, owner_pid, last_heartbeat_ts |
| decisions.jsonl | chose-X-over-Y records | decision, because, ref, supersedes |
| failure-log.jsonl | reflexion entries | approach, error, lesson; read before next spawn |
| agent-comms.jsonl | inter-agent commitments | from, to, subject, outcome; written before spawn returns |

## L3 — Semantic store

Machine-recall layer: scoped semantic search over verbatim material
plus a temporal entity knowledge graph. One store, one write path
(mine-based ingestion from L1/L2); agents query through MCP tools and
write nothing here directly.

- **Search-first gate:** no synthesis without a prior scoped search.
  The kernel states it; session-start hooks reinforce it by injecting a
  fresh recall. A synthesized answer with zero citations behind it is
  treated as a guess.
- **Verbatim drawers:** content kept word-for-word with timestamps.
  Summarization happens above this tier or not at all.
- **Temporal KG:** entities carry validity windows (`valid_at`,
  `invalid_at`). New facts contradicting old ones invalidate rather
  than delete: the graph answers "what was true when", which flat
  vector stores cannot.
- **Decay:** edges and facts expire on schedules; forgetting is part of
  recall quality. Consolidation prunes decayed structure offline.
- Golden-set probes (temporal and multi-hop questions against real past
  sessions) run before trusting any upgrade to this tier.

## L4 — Vault wiki

The human-readable distillate: entity pages, maps of content, research
notes, decisions, postmortems. Plain markdown with wikilinks, opened in
any editor, useful even if every tool dies.

- Shape: shallow stable folders (two levels deep, no deeper), a MOC
  layer for navigation, atomic entity pages inside topics. Folders say
  where a file lives; frontmatter says what it is; wikilinks and MOCs
  say how it connects.
- Frontmatter conventions: `type`, `tags`, `aliases`, `up` (parent
  MOCs), `created`. Renames go into `aliases` so old links resolve.
- Promotion: drafts carry `status: draft`; canonical pages exist only
  after review. Decisions and ADRs land here as first-class pages, not
  in vector stores.
- Hygiene is a scheduled job, not a plugin prayer: orphan sweeps,
  cluster-to-MOC candidates generated for human approval, hub size caps
  (an index holds at most ~100 links).
- The vault models the system too: pages for agents, protocols, tiers —
  introspection keeps the mesh navigable to its own operators.

## Ownership map

| Tier | Writer | Written when |
|---|---|---|
| L0 | Human-approved PRs | rarely, via review |
| L1 | Harness hooks | every session, automatically |
| L2 | Orchestrator sessions | same turn as each meaningful action |
| L3 | Miner jobs from L1/L2 | continuously, offline |
| L4 | Reviewed consolidation + humans | nightly proposals, manual promotion |

## Golden rule

Keep verbatim dated chunks in the recall layers (L1, L3). Never lossy-
summarize what you may need to recall: exact dates, names, numbers, and
error strings are semantically unfindable after summarization, and
summarization-based pipelines measurably lose precisely the specifics
that later matter. Curation adds summaries on top of verbatim material;
it never replaces it. Raw transcripts are mined freely and deleted
never.

## Provenance

- `staging/mine-v1-digest.md` (16 JSONL ledgers with observed field
  schemas: context.jsonl CTX fields and ~100 event types, semantic.jsonl
  SR-CAN categories, claims/active-watch/anti-patterns/comms ledgers,
  DR046 immutable history, DR079 mid-turn logging, ID allocation)
- `staging/research-memory-context.md` (five-layer target architecture;
  Omi verbatim-chunk golden rule LoCoMo ~51 -> 86.6; Zep/Graphiti
  validity windows; MemPalace wings/rooms/drawers verbatim design and
  search-first MCP gate; Karpathy llm-wiki vault layout; bounded index
  + lazy bodies consensus)
- `staging/extracted/v2/skills/mempalace/SKILL.md` (tier model, DR102
  query-first mandate, when-to-write rules) via
  `staging/mine-v2v3-digest.md`
- `staging/research-obsidian-vault.md` (PARA-shaped shallow folders +
  MOC layer + entity graph consensus; frontmatter conventions; Dendron
  sunset lessons: plain markdown survives tool death; scheduled graph
  hygiene)
- `staging/mine-backup-config-digest.md` (MEMORY_SYSTEM.md tiering
  model, markdown-as-canonical-source-of-truth policy)
