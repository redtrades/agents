# Unresolved source roots

Observed: 2026-08-31. These three roots remain unresolved and pointer-only. No
directory was copied. A later document-level review may select safe,
provenance-bound files without promoting runtime, secrets, personal-case
material, or untracked content. Roots with completed document-level capture are
recorded in `pointer-only/CAPTURED-SOURCE-ROOTS.md` and are no longer listed
here.

| Source root | Intended subject | Why pointer-only | Later document-level selection that would resolve it |
| --- | --- | --- | --- |
| /Users/man/.buzz/REPOS/buzz | Buzz prototype and coordination history | This is an external prior-art source with local uncommitted changes; directory-level copying could import runtime wiring or stale state. | Select named inert documents from a resolved commit or reviewed snapshot, retaining the external repository/ref and per-file hashes; leave runtime/configuration pointer-only. |
| /Users/man/agent-reports | Agent-generated research and delivery reports | No Git commit is resolved, so a directory copy cannot honestly establish source provenance. | Review individual reports, identify their producing source and date, preserve exact bytes and SHA-256, and record a stable source revision or WORKING-TREE-ONLY status. |
| /Users/man/Documents/Codex | Untracked candidate documents across Codex workspaces | The root is untracked and heterogeneous; path presence is not a committed source or document-level selection. | Name each candidate file, review sensitivity and relevance, capture exact bytes and SHA-256, and record its stable source revision or explicit WORKING-TREE-ONLY provenance. |
