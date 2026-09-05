# Decisions and conflicts

| Topic | Current decision | Historical evidence / conflict | Resolution state |
| --- | --- | --- | --- |
| Authority | Exact artifacts and structured records are authoritative. | The five-tier design also treats raw logs and Git ledgers as authoritative ancestors. | Compatible if derived recall stays non-authoritative. |
| Scope and retention | Global reusable learning may be promoted; sensitive and organization-owned material stays scoped by default. Canonical and source artifacts are retained; raw logs may be expired or compacted under sensitivity, value, legal-need, and domain-specific policy overlays. | Historical architecture says raw session logs are retained forever. | Resolved by owner decision 42; derived claims remain linked to retained sources and sanitized reusable knowledge is deliberately promoted. |
| Store | A future knowledge service is replaceable. | Agent-mesh recommends a named local-first store and a mandatory search gate. | Deferred; no store is selected here. |
| Curation | Domain writers maintain scoped syntheses; the global pool has one governed promotion boundary with delegated curators and independent quorum. Low-risk sanitized promotion may automate only inside explicit grants and thresholds. | Offline consolidation proposes wiki drafts and reviewed promotion. | Owner and enforcement contract resolved; store implementation remains deferred. |
| Supersession | New derived entries replace the current view while prior versions, sources, and lineage remain available. | Historical designs vary between append-only memory and rewritten wiki pages. | Current-view replacement plus retained history resolves the conflict. |
| Context | Current agents normally read current material; historical reasoning is escalation-only. | Historical designs describe a bounded kernel plus lazy retrieval. | Compatible as a design constraint, not active runtime law. |

The owner resolved the write boundary in current intent decision 51. The future store remains unselected; any implementation must preserve source links, append-only evidence, scoped writers, one global promotion boundary, and supersession history.
