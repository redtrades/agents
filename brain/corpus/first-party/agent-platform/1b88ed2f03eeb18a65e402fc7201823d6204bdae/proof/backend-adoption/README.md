# Backend adoption proof

This proof evaluates the minimum hard-control seam selected in issue #22. It is
not another lifecycle controller.

The executable AgentWorkforce subject is:

- repository: `https://github.com/redtrades/factory`
- pull request: `https://github.com/redtrades/factory/pull/1`
- commit: `741502c3d4e759e2a12bc59ec6459dfa87cb8dc7`
- tree: `d7aa7d39d8ab6c65c2b4b95dc7f45da8c91b5013`

The conformance adapter runs the compiled module from that exact clean checkout
and records source/tree, module/runtime manifest, lockfile, proof artifact and
program bytes, plus the single Node/npm installation used to execute it. It
exercises same-attempt replay, changed-input denial, a two-process claim race,
stale-generation denial (including the direct generic, canonical migration, and
aliased-seed paths), and illegal-transition denial.

Run the neutral tests:

```sh
node --test proof/backend-adoption/tests/contract/fixture.test.mjs
```

Run the AgentWorkforce proof after building the pinned fork:

```sh
AWF_CONFORMANCE_MODULE=/absolute/path/to/redtrades-factory/dist/index.js \
AWF_CONFORMANCE_EXPECTED_COMMIT=741502c3d4e759e2a12bc59ec6459dfa87cb8dc7 \
AWF_CONFORMANCE_EXPECTED_TREE=d7aa7d39d8ab6c65c2b4b95dc7f45da8c91b5013 \
  node --test proof/backend-adoption/tests/contract/agentworkforce-conformance.test.mjs
```

Passing this bounded proof does not establish the complete issue #27 lifecycle.
It establishes only that the selected fork supplies the task-packet, fencing,
restart, and transition seam required to replace PR #47's temporary fixture.
