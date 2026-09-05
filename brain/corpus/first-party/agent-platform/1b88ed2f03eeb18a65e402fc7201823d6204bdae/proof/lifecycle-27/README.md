# Lifecycle 27 real-backend fixture

This directory is the first executable assembly point for issue #27. Its
GitHub-hosted workflow checks out, builds, and executes the canonical
`redtrades/factory` backend at
`741502c3d4e759e2a12bc59ec6459dfa87cb8dc7` (tree
`d7aa7d39d8ab6c65c2b4b95dc7f45da8c91b5013`).

The fixture exercises the failures that previously broke multi-agent work:

- two workers racing for one claim;
- stale-generation writes;
- interruption and idempotent resume;
- self-review;
- changed-head promotion;
- failed verification followed by correction in the same attempt; and
- cleanup without deleting durable authority.

The workflow contract is the backend-neutral
`task-packet-authority/v1` seam: claim, checkpoint, complete, and read. The
Factory source commit, tree, lockfile, compiled module, and toolchain are bound
as source-receipt evidence rather than becoming lifecycle contract fields. The
fixture keeps no durable lifecycle state of its own.

The fixture imports `bindAgentWorkforceAuthority` from
`proof/backend-adoption/adapters/agentworkforce/authority.mjs`, the canonical
shared authority module published by PR #48 at
`487c2b7cb36725335cd856be0fdd57069decb02f`. PR #47 defines neither a Factory
loader nor a native state-store wrapper, so it cannot drift into a second
controller.

A GitHub compare-and-swap authority adapter can replace the Factory adapter at
that seam only if it preserves the same claim and receipt contract plus the
exact source-binding evidence. It must not add a second controller or ledger.

Run the unit proof locally:

```sh
LIFECYCLE_27_FACTORY_ROOT=/absolute/path/to/clean/redtrades-factory \
  python3 proof/lifecycle-27/test_real_backend_fixture.py
```

The GitHub workflow writes `lifecycle-receipt.json` and uploads it as the run
artifact. A green run proves this bounded real-backend fixture, not the
complete production lifecycle or automatic GitHub promotion.
