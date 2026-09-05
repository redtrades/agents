---
name: lean-build
description: Build feature work with high overbuilding risk. Use for new behavior, product slices, or integrations where repository reuse, strict scope, and an explicit stop condition matter Use when implementing new features with high risk of overengineering.
---
# Lean build

Build the smallest complete feature that fits the existing system.

- Derive observable acceptance and explicit non-goals from request and repository.
- Trace entry point through layers owning invariants.
- Deliver coherent end-to-end path across responsible layers; never force work into one file, direct expression, or local patch.
- Reuse fitting seam. Refactor when patching duplicates behavior, weakens ownership, or hides root cause.
- Omit modes, providers, config, extensibility, and polish unless acceptance needs them.
- Add surface, dependency, service, config, or migration only for lifecycle design or acceptance; state material tradeoff.
- Keep work runnable; preserve existing safety and data-loss guards.

Exercise path. Run focused proof. Stop when acceptance passes. Report only material omissions and trigger.

<!-- agent-configs generated source-sha256: 52ff17eaf7fa3471f98cdb064b91d485e90e7abfa635fd30607a91d1b8fff9b2 -->
