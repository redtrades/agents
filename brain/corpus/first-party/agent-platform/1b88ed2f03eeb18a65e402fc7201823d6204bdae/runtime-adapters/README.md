# Runtime Adapters

This directory is the dependency-free runtime-adapter foundation promoted into the
canonical `agent-platform` source by issue #16. The independently reviewed legacy
candidate and live Buzz/Hermes sources are migration evidence, not platform
authority.

It implements one concise typed contract, deterministic dry-run projections for
Buzz and Hermes, projection receipts, and a separate activation-evidence receipt.
It does **not** edit runtime homes, install files, restart processes, or claim that
rendered bytes were discovered or loaded.

## What it projects

- Buzz transport base: a fragment that must be composed with the exact
  version-matched native base before binding the resulting full file to
  `BUZZ_ACP_BASE_PROMPT_FILE`. The inspected seam replaces the native base; it
  does not append to it.
- Buzz nest context: a source-template fragment for
  `nest_agents.md` plus `NEST_AGENTS_VERSION` regeneration. It is not a live
  `AGENTS.md` user-zone override. Later admission must prove exactly one valid
  BEGIN/END marker pair because malformed marker drift is not fail-closed in the
  inspected source generator.
- Hermes identity: a candidate for the exact selected profile's
  `$HERMES_HOME/SOUL.md`.
- Hermes project context: an owner-merged fragment for the deliberately selected
  project-context family, normally repository-owned `AGENTS.md`. It is not a
  generated `HERMES.md`, which would take precedence and mask `AGENTS.md`.

## Commands

From the repository root:

```sh
PYTHONPATH=runtime-adapters python3 -m runtime_adapters.cli validate \
  runtime-adapters/fixtures/canonical-contract.json

PYTHONPATH=runtime-adapters python3 -m runtime_adapters.cli project \
  runtime-adapters/fixtures/canonical-contract.json --runtime buzz

PYTHONPATH=runtime-adapters python3 -m runtime_adapters.cli activation-template \
  runtime-adapters/fixtures/canonical-contract.json --runtime hermes

PYTHONPATH=runtime-adapters python3 -m runtime_adapters.cli validate-activation \
  runtime-adapters/fixtures/activation-not-observed.json
```

All commands are read-only. Projection and receipt JSON is written only to
stdout; the CLI has no filesystem-output, deploy, install, or activation command.

## Evidence states

Activation receipts report only the highest demonstrated state:

```text
projected -> discovered -> loaded -> activated -> behaviorally_verified
```

An `activated` receipt requires the exact deployed-file hashes and composition
inputs for every projected fragment, installed runtime identity, a fresh effective
prompt hash, selected context, no higher-precedence conflict, and passing
discovery, loaded-content, invocation, denial, and restart probes. All positive
probes must bind to the same activation attempt and effective prompt, with
monotonic UTC RFC3339 date-time timestamps ending in `Z`. Hermes also requires
selected profile/effective home, `skip_context_files=false`, and a fresh or
inapplicable prompt cache. Buzz requires selected harness/provider workdir and a
valid nest marker pair. A behaviorally verified receipt additionally requires a
passing behavior probe.

All observed runtime, profile-home, provider-workdir, and deployed-file paths must
be absolute. Hermes and Buzz loader-specific settings are required from the
`loaded` state onward, so a receipt cannot claim loaded content while disabling a
projected surface.

## Verification

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover \
  -s runtime-adapters/tests -t runtime-adapters -v
```

The canonical fixture's `source_revision` and rollback references bind the clean
`agent-platform` base revision from which issue #16 was implemented. Any future
contract change must rebind its revision and provenance and regenerate every
reviewed hash before promotion.
