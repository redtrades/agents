# Buzz and Hermes Runtime Adapter Foundation

**Status:** canonical issue #16 implementation candidate
**Date:** 2026-08-28
**Scope:** `runtime-adapters/` only in `agent-platform`; projection and validation
only

## Goal

Represent a small provider-neutral instruction contract once, then render only the
modules needed by Buzz and Hermes into deterministic, native-surface projection
bundles. A projection receipt proves what the adapter rendered. It never proves
that a runtime loaded or obeyed the result.

## Observed loader seams

This repository is the permanent platform source. Issue #16 imported an
independently reviewed legacy candidate; the runtime checkouts remain migration
evidence only. The adapter design is bound to read-only inspection of these source
states:

- Buzz source checkout commit `631b05c883f58e9533e9038b4669ebdfb1d9cf27`,
  declaring Buzz Desktop 0.5.4, with pre-existing local edits in both
  `nest.rs` and `nest_agents.md`. The current source
  exposes `BUZZ_ACP_BASE_PROMPT_FILE` as a whole replacement for the compiled
  transport base, not an append seam. Therefore the adapter emits only a fragment;
  later admission must compose it with the exact version-matched native base and
  hash the full result. Its nest
  generator refreshes static content above the managed marker and replaces only the
  managed roster when one valid marker pair exists. Missing/malformed markers are
  not fail-closed. Installed Buzz 0.5.19 exposes the base-prompt interface, but its
  full effective prompt remains unverified.
- Hermes source checkout commit `6da0ae1cf5a37898a046b644cf23f9fe67baba22`.
  Its prompt builder independently loads profile `SOUL.md`, then chooses the first
  project-context family found: `HERMES.md`, merged `AGENTS.md`, cwd-only
  `CLAUDE.md`, or Cursor rules.

The Hermes checkout was clean at the inspected commit. These source observations
describe loader mechanisms. They do not prove the
installed Buzz or Hermes process used a projection.

## Approaches considered

1. **Typed module graph with runtime-surface renderers (selected).** One JSON
   contract contains concise modules, dependencies, precedence, target surfaces,
   context budgets, and content hashes. Pure renderers select and order modules
   for each native surface. This gives deterministic output without turning a
   runtime home into authority.
2. **One universal Markdown prompt.** Simpler to copy, but duplicates large prompt
   bodies, conflates Buzz transport with nest context, and can suppress Hermes's
   repository-owned context precedence. Rejected.
3. **Separate canonical Buzz and Hermes configs.** Native-looking, but creates two
   sources of truth and makes drift reconciliation ambiguous. Rejected.

## Contract

Each module has:

- a stable ID and kind;
- concise content plus an independently recorded SHA-256;
- dependencies and integer precedence;
- a maximum character budget;
- provenance, license, and rollback reference;
- one or more `(runtime, surface)` targets.

Allowed initial surfaces are:

- Buzz: `transport_base_fragment`, `nest_static_template`;
- Hermes: `soul`, `project_context`.

Validation fails on unknown fields, duplicate IDs, missing dependencies, cycles,
invalid target/surface pairs, content-hash mismatch, or budget overflow.

## Projection flow

```text
canonical contract
  -> structural and semantic validation
  -> dependency-ordered target selection
  -> native-surface Markdown artifacts
  -> canonical JSON bundle
  -> projection receipt (projection_only, activation not_observed)
```

Buzz produces a transport-base fragment requiring version-matched native-base
composition and a separate static-template fragment for source integration plus a
version bump. It never emits a tiny file for direct use as the whole base, edits
managed markers, or claims regeneration occurred. Hermes produces `SOUL.md` and/or
an owner-merged project-context fragment. The latter must not overwrite or mask a
repository-owned `AGENTS.md`; later admission fails if a higher-precedence
`.hermes.md`/`HERMES.md` unexpectedly wins discovery.

Every generated artifact carries contract ID, source revision, module-graph hash,
and adapter version. Its byte hash lives in the receipt, avoiding a circular
self-hash. Canonical JSON serialization and stable module ordering make a second
identical projection byte-for-byte identical.

## Receipt boundary

A projection receipt records exact contract, graph, adapter, runtime target, and
artifact hashes. It is always `dry_run: true`, `claim: projection_only`, and
`activation_status: not_observed`.

An activation receipt is a different schema. An `activated` verdict requires:

- the exact projection-receipt hash;
- an applied deployment mechanism and one exact binding per projected fragment;
- installed runtime version, selected profile/toolsets/cwd, loader flags, and
  loader evidence;
- absolute runtime, effective-home/provider-workdir, and deployed-file paths;
- final deployed-file hashes plus composition-input hashes/evidence where a
  fragment is transformed or merged;
- one activation-attempt ID, monotonic UTC RFC3339 observation date-times ending
  in `Z`, and an effective
  prompt hash shared by passing discovery, loaded-content, invocation, denial, and
  restart probes.

Hermes activation also records effective profile home, `skip_context_files`,
`load_soul_identity`, prompt-cache state, and redacted effective-prompt evidence.
Buzz activation records selected harness/provider cwd and a valid nest marker pair.
Runtime-specific loader settings become mandatory at `loaded`, not only at
`activated`.

The dry-run CLI cannot deploy files or mint an `activated` receipt. It can validate
an externally captured activation receipt and can emit an explicitly
`not_observed` template for later evidence collection.

## Interfaces

- `load_contract(path) -> dict`
- `validate_contract(contract) -> None`
- `project_contract(contract, runtime) -> dict`
- `validate_projection_bundle(bundle) -> None`
- `validate_activation_receipt(receipt) -> None`
- CLI `validate`, `project`, `activation-template`, and `validate-activation`
  commands

The CLI reads files and writes only to stdout. It has no arbitrary filesystem
output, runtime-home discovery, runtime mutation, restart, or activation operation.

## Testing

Focused standard-library unit tests cover valid and invalid contracts, dependency
ordering, exact deterministic bundles for Buzz and Hermes, projection-only receipt
invariants, activated-receipt evidence gates, and CLI behavior. Golden fixtures
are hand-derived and small.
