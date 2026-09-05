# Agent factory program — migration evidence

**Superseded destination, 2026-08-28:** the clean canonical platform repository is
`/Users/man/agent-platform` / `redtrades/agent-platform`. This directory is the
entry point for research, salvage, and migration evidence only.

Existing repositories, runtime homes, reports, prompts, skills, and prior designs
are evidence until they pass the current architecture's admission and promotion
gates.

## Intent

Read [`INTENT.md`](./INTENT.md) for the durable objective and boundaries.

## Current architecture package

1. [`architecture/AGENT-PLATFORM-APPROVAL-BRIEF.md`](./architecture/AGENT-PLATFORM-APPROVAL-BRIEF.md)
2. [`architecture/SDLC-MVP-FIRST-PRINCIPLES.md`](./architecture/SDLC-MVP-FIRST-PRINCIPLES.md)
3. [`research/SOTA-PRIMARY-SOURCE-COMPARISON.md`](./research/SOTA-PRIMARY-SOURCE-COMPARISON.md)
4. [`research/LIVE-RUNTIME-INSTRUCTION-AUDIT.md`](./research/LIVE-RUNTIME-INSTRUCTION-AUDIT.md)

## Consolidation and preservation

- [`migration/LEGACY-SOURCE-CATALOG.md`](./migration/LEGACY-SOURCE-CATALOG.md)
- [`migration/WORKSPACE-CONSOLIDATION-MANIFEST.md`](./migration/WORKSPACE-CONSOLIDATION-MANIFEST.md)
- [`migration/INHERITED-COMPONENT-DISPOSITION-MANIFEST.md`](./migration/INHERITED-COMPONENT-DISPOSITION-MANIFEST.md)

## Authority boundary

- `agent-platform` is the single source repository for the agent platform.
- `agent-mesh` is a migration/reference and benchmark-history source.
- Product factories remain separate consumers.
- Runtime homes remain runtime-local and become adapter targets, not source.
- Large generated evidence belongs in an external immutable artifact/archive
  hierarchy, not in Git worktrees.
- A legacy path is not deleted merely because it appears in this catalog.
  Preservation, extraction, and retirement are separate steps.
