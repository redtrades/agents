# Consolidation scope

## In scope

- Inventory the complete first-party repository and historical documentation
  estate.
- Copy intent-bearing documents, key research, architecture history, audits,
  decisions, postmortems, and meaningful milestone versions.
- Preserve exact provenance to the original repository, path, revision, and
  content hash where available.
- Build the approved hybrid taxonomy with concise reading packs and an exact
  source corpus.
- Reconcile historical intent with current owner decisions and retain unresolved
  conflicts explicitly.
- Keep sensitive material separated and exclude secrets, runtime state, and case
  material.

## Out of scope

- Fixing or extending `agent-platform`.
- DocOps, CI, GitOps, SDLC controls, enforcement hooks, or compliance machinery.
- Selecting or deploying orchestration, memory, observability, or agent-runtime
  infrastructure.
- Adopting legacy code, skills, prompts, configurations, or runtime wiring.
- Rebuilding the platform before the archive and current intent are understood.

## Output

The output is a private, navigable historical knowledge repository that lets a
future agent understand the current intent quickly, inspect the relevant domain
history when necessary, and trace every material conclusion back to source.
