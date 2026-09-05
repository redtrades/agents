# Portable role contracts

Issue [#35](https://github.com/redtrades/agent-platform/issues/35) defines the first provider-neutral role catalog. The catalog is platform data, not a queue, principal, model assignment, runtime installer, or promotion authority.

## Canonical objects

- `platform/roles/v1/catalog.json` is the source-pinned roster and the call-site binding from each role to one system prompt, one user prompt, and one typed output definition.
- `platform/roles/v1/task-packet.schema.json` defines one admitted unit of work. It binds issue/attempt identity, actor/run, input revision, fence, role-contract hash, the adapted ask/where/done/non-goals request, effect policy, owned paths, capabilities, skills, acceptance oracles, return schema, and artifact locators.
- `platform/roles/v1/role-output.schema.json` defines the typed claim envelopes returned by the roles.
- `.agents/roles/` is a portable behavioral prompt projection. These files are projected, but they are not discovered, loaded, activated, or behaviorally verified by any runtime in this change.

The `role_contract_sha256` is SHA-256 over the selected catalog role object serialized as canonical JSON (UTF-8, object keys sorted, separators `,` and `:` with no extra whitespace). A runtime adapter must verify that hash before invoking the role. Every output also binds the canonical SHA-256 of the full admitted task packet.

## Role roster

| Role | One purpose | Behavioral write declaration |
| --- | --- | --- |
| `orchestrator_dispatcher` | Select and explain an explicit chain without doing another role's work | none |
| `scout` | Locate exact evidence | none |
| `planner` | Produce an artifact-backed plan | plan artifacts only |
| `builder` | Make the smallest admitted change | packet-owned paths |
| `reviewer` | Judge the exact candidate against every criterion | none |
| `documenter` | Write only candidate-diff-backed documentation | packet-owned documentation paths |
| `independent_verifier` | Prove, disprove, or mark atomic claims unsure | none |

There is no `architect` role. Material architecture is an orchestrator cookbook concern that routes evidence to scouts, decisions to an artifact-backed plan, and implementation to the builder only after the issue authorizes the boundary change.

There is no `tester` role. Known tests, lint, builds, Git checks, and receipt checks are deterministic code phases. Test output may be adapted into a typed envelope for correction, but an agent does not rediscover or reinterpret a known exit status.

## Contract synchronization

The output contract is one synchronized triad:

1. The concrete definition under `role-output.schema.json#/$defs/...`.
2. The exact `Output schema:` identifier and JSON shape in the role's `user.md`.
3. The matching `output_schema` call-site binding in `catalog.json`.

The targeted test rejects a missing definition or drift among those three surfaces. System prompts hold stable identity and behavioral boundaries; user prompts hold task variables and the exact return shape. Large material travels through artifact locators, while the final JSON envelope remains a compact manifest of claims.

## Authority boundary

Roles are not security principals. Their prompts do not enforce filesystem, tool, network, lease, or promotion permissions. `behavioral_writes` records expected conduct so deterministic enforcement can detect drift; it is not a sandbox.

The external controller owns admission, leases, fencing, sequencing, bounded correction, effect classification, post-call write-scope checks, and evidence invalidation. The expected-head promoter is also a non-agent boundary. It may advance only the exact eligible candidate that passed current deterministic and independent-review gates. Eligible `AUTO_WRITE` promotion is automatic under `docs/OPERATING-MODEL.md`; only `APPROVAL_DESTRUCTIVE` requires a valid owner grant.

A changed candidate invalidates earlier test, review, and verification evidence. Reviewer and verifier envelopes therefore bind the candidate revision and must be regenerated after any byte change. Neither role repairs the work it judges.

## Donor provenance and adaptation

The adopted source pins are recorded in the catalog:

- `disler/super-simple-software-factory` at `de31374882e7a4e3e5b7bb9bd09e69dc2f779356`: one-role/one-purpose, stable system plus task-specific user prompt, typed artifact-backed envelopes, deterministic code phases, bounded corrections, post-call scope enforcement, and orchestrator cookbooks.
- `disler/the-verifier-agent` at `aa18d68bcf886fb2a061ca5a76c6d2e1f3516501`: atomic claim decomposition, evidence over assertion, `verified`/`failed`/`unsure`, explicit missing oracles, and concrete feedback.

This repository does not adopt the Pi/tmux/socket transport, shared dirty checkout execution, placeholder passing commands, broad bash as a permission boundary, wholesale stamping, or a second controller/queue. The stale research-note statement that every promotion remains owner-authorized is superseded by the governing effect policy described above.

## Deterministic fixture

Run:

```sh
python3 tests/roles/test_role_contracts.py
```

The fixture validates the catalog and positive task/output examples, rejects malformed packet cases, verifies prompt/schema/catalog synchronization, confirms donor pins, and checks that architecture/test work did not become invented roles. It proves repository contract consistency only. Runtime adapters must separately report projected, discovered, loaded, activated, and behaviorally verified state.
