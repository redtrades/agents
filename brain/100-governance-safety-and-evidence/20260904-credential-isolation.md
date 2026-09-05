# Worker Credential Isolation

Source: agent-platform#WORKER-CREDENTIAL-ISOLATION.md

## Overview

Describes the worker credential boundary implemented in the local Gate C launcher (`tools/controller/run_gate_c.mjs`).

**Scope**: This is the **local launcher boundary**. Does not claim server-side branch protection or autonomous-safe forge.

**Issue**: #163 (reopened under #59/#24/#1)

## Implemented Launcher Boundary

`tools/controller/run_gate_c.mjs` is the shared local launch seam for Gate C implementer and reviewer subprocesses.

### Environment Isolation

Each agent phase receives:
- **New temporary `HOME`**: Isolated user directory
- **New temporary `TMPDIR`**: Isolated temp directory
- **New `GH_CONFIG_DIR`**: Isolated GitHub CLI config

Each agent phase receives NONE of:
- `GH_TOKEN`
- `GITHUB_TOKEN`
- `GATE_C_PROJECTOR_TOKEN`
- `CODEX_HOME`
- `SSH_AUTH_SOCK`
- Parent `GIT_ASKPASS`

### Git Configuration Isolation

Launcher also:
- Disables system and global Git configuration
- Clears Git credential helpers
- Disables terminal credential prompts
- Uses SSH command with no configuration file or agent identity

### Role Token Protection

Launcher **rejects** before generic passthrough:
- `AGENT_PLATFORM_CONTROLLER_TOKEN`
- `AGENT_PLATFORM_REVIEWER_TOKEN`
- `AGENT_PLATFORM_PROMOTER_TOKEN`
- `AGENT_PLATFORM_PROJECTOR_TOKEN`
- Equivalent role-secret fields

**Returned Evidence**: Receipt `agent-platform.worker-credential-isolation/v1` recorded in:
- Gate C implementer evidence
- Gate C reviewer evidence
- Hash-only command journal

**Rule**: Controller, reviewer, promoter, and projector credentials remain injectable only through their corresponding controller-owned runners (not worker environment).

## Scoped Provider Capability

### Binding Structure

Controller-derived OpenCode implementer and Codex reviewer bindings carry only the opaque reference:
```
secret://codex-provider
```

At `Execute Gate C` workflow step, controller may receive `GATE_C_FREELLMAPI_API_KEY` from repository secret store.

### Capability Mapping

Controller maps `GATE_C_FREELLMAPI_API_KEY` to `FREELLMAPI_API_KEY` **only** in child environment for exact agent phase AFTER validation:

- Provider reference matches provider identity
- Environment variable matches expected
- Implementer or reviewer phase matches
- Attempt ID matches
- Input revision matches
- FreeLLMAPI audience is `http://127.0.0.1:3100/v1` (exact)
- Route is `auto:notrain` (no other routes)
- Issued/expiry interval is bounded
- Capability object is unambiguous with no extra fields

### Denial Rules

Missing, malformed, stale, expired, wrong-attempt, wrong-provider, wrong-audience, or bootstrap-failed capabilities:
- **Deny before child command starts**
- Do not proceed with subprocess
- Record denial reason in receipt

### Secret Protection

The secret must be:
- Provisioned/rotated outside this repository
- NEVER placed in:
  - Task packet
  - Command-line argument
  - Prompt
  - TOML/configuration file
  - Receipt or artifact
  - Logs

**Fail-Closed Rule**: Run denies when scoped capability is absent/unavailable. This document does NOT infer current provider capacity from that fail-closed behavior.

## Adapter Bindings

### Implementer Adapter

Controller selects committed `tools/adapters/implementer/opencode.py` and constructs OpenCode command for exact candidate worktree:

```text
/opt/homebrew/bin/opencode run --pure --format json --agent build \
  --model freellmapi/auto:notrain --dir <worktree>
```

**Configuration**:
- Controller supplies `OPENCODE_CONFIG_CONTENT` for FreeLLMAPI audience only
- Does NOT load host OpenCode configuration or authentication directory
- Does NOT allow model selection outside `auto:notrain`

**Event Handling**: OpenCode events are telemetry only (not control).

**Adapter Validation**: Adapter independently derives:
- Base commit (validated)
- Candidate commit (validated)
- Commit count
- Clean state
- Owned-path result

**Result Type**: Typed phase result from Git derivation before returning.

### Reviewer Adapter

Controller selects committed `tools/adapters/reviewer/codex.py` and constructs Codex command with:

**Schema**: Committed JSON Schema at `tools/adapters/reviewer/child-review-result.schema.json`

**Constraints**:
```text
codex exec --ignore-user-config --ignore-rules --strict-config --ephemeral \
  -s read-only -a never -m auto:notrain \
  -c model_provider="freellmapi" \
  -c model_providers.freellmapi.base_url="http://127.0.0.1:3100/v1" \
  -c model_providers.freellmapi.wire_api="responses"
```

**Isolation**: Each child receives provider credential only as `FREELLMAPI_API_KEY`.

**Secret Leak Prevention**: If stdout or stderr contains credential value:
- Gate C replaces result with phase-specific fixed denial
- Records leak in receipt
- Terminates subprocess

### Cleanup on All Exits

All normal, failed, timed-out, malformed, bootstrap-failed, and missing-executable exits:
- Remove per-attempt temporary directory
- **Cleanup failure itself denies completion** (fail-closed)

## Admitted and Unadmitted Harnesses

### Current Bound Revision

Gate C's `createCommandRunner()` loads adapters from **immutable controller source**, not candidate worktree.

**Controller-derived defaults**:
- Implementer: OpenCode
- Reviewer: Codex

### Harness Status

| Harness | Status | Role |
|---------|--------|------|
| **OpenCode** | Admitted, wired | Implementer |
| **Codex** | Admitted, wired | Reviewer |
| **Hermes** | Parked, generic | Not launched; workflow-tested only |
| **Jules** | Remote adapter | Not launched; remote dispatch/review only |
| **Buzz** | Runtime contract | No candidate-worker launcher selected |
| **FreeLLMAPI** | Provider route | Replaceable; not task state authority |

**Immutability Rule**: Adapters loaded from controller source, never from candidate. Candidate cannot inject or select harness.

### Current Operator Capacity Policy

**Policy**: External provider dispatch is paused; root manually orchestrates separate Codex implementer and reviewer tasks.

**Non-Evidence**: This policy does NOT:
- Change committed adapter contracts
- Indicate other runtimes are exhausted
- Prove capacity constraints

**Future Selection**: A future selected launcher must use this isolation boundary or be denied until it has equivalent independently tested receipt.

## Exact Limitation (Not a Full Security Boundary)

This boundary prevents **documented ambient credential channels at launcher entry**.

**NOT a boundary against**:
- Arbitrary process with repository owner's macOS login
- Separately authorized cloud worker with equivalent access
- OS-level security compromise

**GitHub Free Limitations**: Free private repositories cannot enforce:
- Protected branches
- Rulesets
- Required reviews
- Required status checks

**See**: `docs/ARCHITECTURE.md` for platform constraints.

### Consequence

Platform must continue to report server-side direct-push and direct-merge prevention as:
- `unsupported`
- `not_enforced`

**Required for Autonomous Safety**:
- Separate OS account, OR
- VM/container boundary, OR
- Forge plan supporting repository enforcement

**Critical Rule**: This local boundary must NOT lift issue #1's promotion freeze or claim autonomous safety from local isolation alone.

## Reproduction & Testing

### Deterministic Unit Tests

```sh
node --test tests/controller/gate_c_cli.test.mjs
python3 tests/controller/test_gate_c_workflow.py
python3 -m unittest tests/adapters/test_opencode_implementer.py
python3 -m unittest tests/adapters/test_hermes_implementer.py
python3 -m unittest tests/adapters/test_codex_reviewer.py
```

**Coverage**:
- Injected fake capabilities and child commands
- Valid resolution and binding
- Exact active OpenCode and Codex bindings
- Absence of host-bound Hermes selection
- Parked Hermes adapter registration
- All required denial cases
- Output leak denial
- Cleanup across all exit types
- Concurrent distinct homes
- Workflow secret scoping
- Committed typed results

**Network**: Make no network request and do not read live credential.

### Bounded Live Denial Fixture

```sh
node tools/controller/worker_isolation_fixture.mjs \
  --repository "$PWD" \
  --candidate "$(git rev-parse HEAD)" \
  --receipt /absolute/external/worker-isolation-receipt.json
```

**Behavior**:
- Runs `gh auth status`
- Checks for Git credential helper
- Uses only `git push --dry-run`
- Writes secret-free PASS/DENY receipt
- Exits nonzero unless every worker operation is denied
- Never creates branch, merges, or alters repository state

**Falsifiers**:
- Secret credential appears in any log/output → FAIL
- Subprocess executes `git push` (not dry-run) → FAIL
- Subprocess successfully authenticates with leaked token → FAIL
- Cleanup does not remove temporary HOME → FAIL

## Key Rules

1. **Isolation First**: New HOME, TMPDIR, GH_CONFIG_DIR for each phase
2. **No Role Tokens in Worker**: Controller, reviewer, promoter secrets never in worker env
3. **Scoped Provider Capability**: Only opaque reference; validation before mapping
4. **Immutable Adapters**: From controller source, never from candidate worktree
5. **Artifact-First Validation**: Type-checked results, schema validation
6. **Cleanup Fail-Closed**: Cleanup failure denies completion
7. **Secret Protection**: Never in logs, configs, receipts, or artifacts
8. **Read-Only Review**: No write authority in reviewer subprocess
9. **Bounded Credentials**: Each phase gets only necessary creds for its role
10. **Concurrent Isolation**: Multiple phases with distinct homes prevent bleed-through

## Integration with Delivery Pipeline

- **Controller**: Validates capability, constructs argv, isolates environment
- **Implementer**: Receives isolated HOME + provider capability; produces candidate
- **Reviewer**: Receives isolated HOME + provider capability; returns typed verdict
- **Promoter**: Receives controller-owned credentials; performs merge
- **Cleanup**: Releases temporary directories; validates no orphaned state

No single subprocess has authority across roles.
