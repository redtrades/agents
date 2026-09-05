# Inert platform projection foundation

This directory contains Slice 0–1 source artifacts for one deliberately inert
projection seam. It is not a runtime configuration directory and it does not
activate Codex, discover a loader, install an instruction file, or edit any
runtime home.

`platform/` is a logical source boundary only. It has no `__init__.py`; the
implementation package is named `agentmesh_platform` under `platform/src/` so it
cannot shadow Python's standard-library `platform` module.

## `codex-agents-md@v1`

The adapter validates a strict JSON manifest, resolves its typed instruction
module graph, and writes a deterministic managed `AGENTS.md`-style projection
only underneath an explicit system-temporary allowed root. It is invoked directly:

```sh
python3 platform/projections/codex_agents_md.py \
  --manifest platform/fixtures/codex-agents-md.v1.manifest.json \
  --target generated/AGENTS.md \
  --allowed-root "$(mktemp -d)" \
  --receipt receipts/codex-agents-md.json \
  --rollback-dir rollback
```

All three output arguments are either relative to `--allowed-root` or absolute
paths that still resolve below it. The root must already exist below the host
system's temporary directory. Target, receipt, and rollback paths must be
pairwise disjoint: no path may equal, contain, or be contained by another. The
adapter opens that root once and performs
directory traversal, reads, temporary-file creation, replacement, rollback, and
deletion relative to the anchored directory descriptor with no-follow semantics.
Lexical traversal, pre-existing symlinks, a symlink swapped in after validation,
paths outside the root, and known live runtime locations are rejected without an
outside-root write. The adapter never writes to `~/.codex`, `~/.claude`,
`~/.hermes`, `~/.buzz`, or another runtime/configuration location.

The manifest schema is `codex-agents-md-manifest@v1`; it has only:

- `schema_version`, `target`, `target_context_budget`, and `modules`.

Each module has a stable `id` and `semantic_key`, `type`, relative `source_path`,
source `sha256`, dependencies, precedence, activation trigger, supported targets,
per-module context budget, provenance, license, and rollback reference. Unknown
or missing fields fail closed. Per-module context budgets count exact UTF-8 source
bytes. The target context budget counts the complete rendered projection,
including managed metadata, markers, and preserved user-zone bytes. The resolver
rejects source hash mismatch/missing sources, duplicate IDs or meanings,
cycles/missing dependencies, target/precedence conflicts, and per-module,
aggregate-source, or rendered-target budget violations.

Managed output carries the adapter, manifest hash, graph hash, and deterministic
projection-body hash. It has explicit user-zone markers. A user-zone edit is
preserved byte-for-byte and gets a refreshed receipt; a managed-region edit or
ambiguous marker layout fails closed rather than being overwritten. An unchanged
second run changes neither projection nor receipt bytes.

Before a valid managed projection is replaced after a manifest/source transition,
the adapter writes its full prior bytes to a SHA-256-named rollback file below the
allowed root. If that rollback write fails, the projection stays unchanged. Every
target/receipt publish first durably writes a deterministic prepared-transaction
journal under the rollback directory. A later invocation either recognizes the
complete next pair or restores the complete prior pair before proceeding, so an
abrupt stop after either file replacement does not strand an unrecoverable split
generation. The journal is removed only after both exact next hashes verify. The
receipt is deterministic and records the adapter, inactive/unverified status,
manifest/graph/source hashes, exact target, prior/output/managed/user-zone hashes,
and rollback path/hash when applicable.

## Fixtures and boundary

`fixtures/modules/inert-codex-projection.md` is the one representative source
module. `fixtures/codex-loader-0.146.0.json` records only a versioned loader
evidence contract for Codex CLI `0.146.0`. It explicitly says activation is
`unverified`; file presence and projection success are not runtime-discovery or
activation evidence.

Run the focused contract suite with:

```sh
python3 -m unittest discover -s platform/tests -p 'test_*.py' -v
```

This foundation intentionally does not define leases, checkpoints, CI, memory,
service control, runtime activation, or any control-attempt schema.
