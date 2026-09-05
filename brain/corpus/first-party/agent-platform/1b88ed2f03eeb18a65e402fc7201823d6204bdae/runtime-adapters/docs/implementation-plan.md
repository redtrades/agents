# Buzz and Hermes Runtime Adapter Foundation Implementation Plan

> **For agentic workers:** keep all file ownership in the primary task; read-only
> loader audits and exact-candidate review may be delegated. Do not deploy,
> install, restart, activate a runtime, or write outside `runtime-adapters/`.

**Goal:** Build deterministic validation and dry-run projection of one canonical
instruction contract into Buzz and Hermes native surfaces, with projection and
activation evidence kept distinct.

**Architecture:** A dependency-free Python package loads a strict JSON contract,
validates its module graph, renders target-specific Markdown into a canonical JSON
bundle, and validates the resulting receipt. Activation receipts use a separate
schema and stronger semantic gates that projection code cannot satisfy by itself.

**Tech Stack:** Python 3 standard library, JSON Schema documents as portable
contracts, `unittest`, SHA-256.

## Global Constraints

- Own and modify only `runtime-adapters/`.
- Read Buzz and Hermes runtime/source state only; never expose secret values.
- This repository is the permanent canonical destination; issue #16 is the bounded
  import authority and legacy repositories are migration evidence only.
- No runtime edits, installs, restarts, deployment, merge, or activation claims.
- Commit, push, and PR evidence are authorized only for the issue #16 candidate.
- Keep repository `AGENTS.md` files repository-owned.
- A projection receipt is not an activation receipt.

---

### Task 1: Strict canonical contract validation

**Files:**

- Create: `runtime-adapters/runtime_adapters/errors.py`
- Create: `runtime-adapters/runtime_adapters/contract.py`
- Create: `runtime-adapters/schemas/canonical-contract.schema.json`
- Create: `runtime-adapters/fixtures/canonical-contract.json`
- Test: `runtime-adapters/tests/test_contract.py`

**Interfaces:**

- Produces: `load_contract(path: Path) -> dict[str, object]`
- Produces: `validate_contract(contract: Mapping[str, object]) -> None`
- Produces: `contract_hash(contract) -> str` and `module_graph_hash(contract) -> str`

- [ ] Write tests for a valid fixture, hash mismatch, unknown dependency, target
      mismatch, budget overflow, and dependency cycle.
- [ ] Run the focused tests and verify they fail because the package is absent.
- [ ] Implement the smallest strict validator and canonical hashing helpers.
- [ ] Run the focused tests and verify they pass.

### Task 2: Deterministic Buzz and Hermes projections

**Files:**

- Create: `runtime-adapters/runtime_adapters/projector.py`
- Create: `runtime-adapters/runtime_adapters/__init__.py`
- Create: `runtime-adapters/schemas/projection-receipt.schema.json`
- Create: `runtime-adapters/fixtures/expected-projection-hashes.json`
- Test: `runtime-adapters/tests/test_projector.py`

**Interfaces:**

- Consumes: validated canonical contract mappings and graph hashes from Task 1.
- Produces: `project_contract(contract, runtime: str) -> dict[str, object]`
- Produces: `validate_projection_bundle(bundle) -> None`

- [ ] Write tests asserting hand-derived artifact paths, module ordering, receipt
      flags, and exact repeated-call equality for each runtime.
- [ ] Run the focused tests and verify they fail because projection is absent.
- [ ] Implement dependency-ordered surface rendering and canonical bundle output.
- [ ] Generate and inspect small golden bundles, then make focused tests pass.

### Task 3: Activation receipt evidence gate

**Files:**

- Create: `runtime-adapters/runtime_adapters/receipts.py`
- Create: `runtime-adapters/schemas/activation-receipt.schema.json`
- Create: `runtime-adapters/fixtures/activation-not-observed.json`
- Test: `runtime-adapters/tests/test_receipts.py`

**Interfaces:**

- Produces: `activation_receipt_template(bundle) -> dict[str, object]`
- Produces: `validate_activation_receipt(receipt) -> None`

- [ ] Write tests proving `not_observed` is valid and `activated` fails unless
      deployment, runtime identity, exact hashes, loader evidence, and all five
      pre-behavior probes are present and passing.
- [ ] Run the focused tests and verify expected failures.
- [ ] Implement the template and semantic activation validator.
- [ ] Run the focused tests and verify they pass.

### Task 4: Read-only CLI and operator documentation

**Files:**

- Create: `runtime-adapters/runtime_adapters/cli.py`
- Create: `runtime-adapters/README.md`
- Create: `runtime-adapters/tests/test_cli.py`
- Create: `runtime-adapters/tests/__init__.py`

**Interfaces:**

- Consumes all earlier pure functions.
- Produces CLI commands `validate`, `project`, `activation-template`, and
  `validate-activation`.

- [x] Write subprocess tests for successful validation, stdout-only projection,
      absence of a filesystem-output option, and rejected invalid activation
      claims.
- [ ] Run the focused CLI tests and verify expected failures.
- [ ] Implement argument parsing with no deploy/activate/runtime-home command.
- [ ] Run all tests twice and compare projection output hashes.
- [ ] Compile package sources, scan artifacts for secret-like literals, inspect
      `git diff -- runtime-adapters`, and remove only task-created debris.
