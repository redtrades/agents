# Local Agent Commit Identity

Source: agent-platform#COMMIT-IDENTITY.md

## Overview

`tools/identity/configure_git_identity.py` establishes **deterministic Git attribution** for one agent run.

**Important Clarifications**:
- Does NOT create commits (only configures environment)
- Does NOT change global Git settings
- Does NOT configure signing keys or GPG/SSH signing
- Does NOT establish cryptographic identity
- **Attribution is not a signature** — it's an audit trail for review

## Worktree-Local Configuration

### Usage

Run only for the intended existing Git worktree/repository:

```sh
python3 tools/identity/configure_git_identity.py \
  --repo /path/to/worktree \
  --persona reviewer-bot \
  --run-id run-20260828-01 \
  --model gpt-5.6-terra
```

### What It Does

Enables Git's `extensions.worktreeConfig` and writes two values through `git -C <repo> config --worktree`:

```text
user.name  = Agent <persona>
user.email = agent+<persona>.run-<run-id>@agents.invalid
```

**Isolation**: Each linked worktree keeps its own persona instead of overwriting siblings.

**Domain**: `agents.invalid` is intentionally non-delivery domain; keeps author address separate from Mike's email identities and prevents linking to him by GitHub.

### Constraints

Never calls `git config --global` and does not write author identity into shared repository config.

## Input Validation

Accepted values are deliberately narrow (defense in depth):

| Input | Pattern | Examples | Rejects |
|-------|---------|----------|---------|
| **persona** | lowercase letter + up to 31 lowercase letters/digits/hyphens | `reviewer-bot`, `implementer-v1` | uppercase, spaces, whitespace, symbols |
| **run ID** | lowercase letter/digit + 7-63 lowercase letters/digits/hyphens | `run-20260828-01`, `pass-1` | uppercase, spaces, paths, multiline |
| **model** (optional) | single-line identifier: letters, digits, `.`, `_`, `+`, `:`, `/`, `-` | `gpt-5.6-terra`, `freellmapi/auto:notrain` | spaces, newlines, shell metacharacters |

**Fail Rule**: Unsafe, path-like, whitespace-containing, or multiline values fail BEFORE any worktree-local Git config is written.

## Required Commit Trailers

Every agent-authored commit using this identity must include these trailers:

```text
Agent-Actor: agent/<persona>
Agent-Run-ID: <run-id>
Agent-Model: <model-id>  # optional but recommended
```

### Example

```text
Fix gate ordering and add DFL-020 enforcement

Gate order now ensures lease is released before worktree removal.
DFL-020 identity validation runs at attempt admission.

Agent-Actor: agent/reviewer-bot
Agent-Run-ID: run-20260828-01
Agent-Model: gpt-5.6-terra
```

### Trailer Parsing

- Git's `git interpret-trailers --parse` is the source of truth
- Trailer-looking body text is NOT sufficient (must be in final block)
- Parser runs outside repository discovery
- System, global, local, and caller-injected Git config are excluded
- Stable locale enforced

**Rule**: Repository or environment trailer aliases cannot reinterpret immutable commit message.

Every agent commit, material or empty, must have exactly one adjacent final-block sequence.

## Attribution vs. Signature

**Attribution is NOT cryptographic proof**:
- `user.name` and `user.email` are claimed, not verified
- Trailers identify claimed actor and run for review/audit only
- Anyone with repository access can commit under any name

**This helper does NOT set**:
- `commit.gpgsign`
- `user.signingkey`
- SSH signing configuration
- Signature verification policy

**Additional Control Needed**: Any signature requirement must be configured and verified as a separate approved control (GPG, SSH, etc.).

## Exact-Range Admission (DFL-020)

**Context**: Commits must be admitted to the delivery pipeline. Attribution becomes an admission decision only when every commit in explicit `base..head` range passes an executable gate.

### The Validator

```sh
/absolute/locked/python3 -I -S /absolute/accepted/validate_commit_range.py \
  --repo /path/to/worktree \
  --base <full-base-commit> \
  --head <full-head-commit> \
  --expected-actor agent/<persona> \
  --expected-run-id <run-id> \
  --expected-validator-sha256 <accepted-file-sha256> \
  --expected-validator-git-blob <accepted-git-blob> \
  --git-executable /absolute/locked/git
```

### Bootstrap Defense in Depth

Validator enforces:
- Python isolated mode (`-I`) and no-site mode (`-S`)
- Only built-in `sys` module imported before enforcement
- Sibling, startup, and site-customization modules cannot execute first
- **These are defense in depth, not execution provenance**

**Key Limitation**: Validator cannot attest its own memory image, interpreter, executable digests, or direct-file invocation. **Trusted outer CI/controller must select and attest**:
- Exact Python executable
- Exact Git executable
- Digests of both
- Exact argv (`python -I -S /absolute/accepted/validator`)
- Prohibition on `-c`, `exec`, `runpy`, or in-memory loading
- Absolute file paths required (never resolve via PATH)

### Validation Rules

**Input Requirements**:
- Controller supplies **lowercase, full 40-hex commit object IDs** only
- `HEAD`, branch names, tag names, abbreviations, uppercase IDs, revision expressions are **INVALID**
- Validator resolves both objects and requires each ID to equal requested ID exactly

**Range Rules**:
- Base must be ancestor of head
- Complete range enumerated in **deterministic reverse topological order**
- Each commit checked for tree/parent/identity/trailers

**Identity Validation**:
- Raw author and committer identity extracted
- Parsed identity trailers extracted with `git interpret-trailers --parse`
- Exact matches required for:
  - `Agent-Actor: agent/<persona>`
  - `Agent-Run-ID: <run-id>`
  - `Agent-Model: <model-id>` (if present, validated; if absent, valid)

### Exit Codes

| Code | Meaning |
|------|---------|
| `0` | Logical validation passed; range is valid for admission |
| `1` | Validator identity differs from controller's accepted identity, OR range violates identity policy/ancestry |
| `2` | CLI input or repository inspection failed (unresolved object, invalid input, non-isolated Python, non-absolute paths, shallow history, etc.) |

**Non-admission by itself**: Exit 0 means logical validation passed; **controller's signed outer execution attestation is also required** for actual admission.

### Portable Receipt Output

Single-line, key-sorted JSON. Records:

- Exact base and head
- Controller-supplied expected actor and run
- Actual and expected validator file SHA-256 and Git blob identity
- Ordered commit set
- Each commit's tree and parents
- Whether tree differs from first parent
- Raw author and committer identity
- Parsed identity trailers
- Any violations

**Excluded by design**:
- Executable, repository, and worktree paths
- Local configuration
- Direct-file or memory-image provenance claims

**Portability**: Identical objects checked with same on-disk validator and expectations in another linked worktree or clone produce byte-identical portable receipt output.

**Execution Field**: Always `{"attestation":"external-required","self_attested":false}` (never claims direct-file or memory-image provenance from self-observation).

## Trailer-Specific Rules

### Required Trailers

Must appear in final block of commit message:

```text
Agent-Actor: agent/<persona>
Agent-Run-ID: <run-id>
```

### Optional Trailer

Recommended but not required:

```text
Agent-Model: <model-id>
```

### No Multiline Trailers

Trailers are single-line values only. Multiline content goes in body, not trailers.

## Key Decisions

1. **Worktree local**: Each worktree isolated; no global pollution
2. **Narrow input validation**: Defense in depth against injection
3. **External attestation required**: Validator cannot self-attest; controller must
4. **Exact object IDs**: No abbreviations or refspecs; prevents ambiguity
5. **Trailer-first parsing**: Git's parser is source of truth, not custom regex
6. **Portable receipt**: Same validator + inputs = same output anywhere
7. **Attribution audit trail**: Trailers are for review/audit; not cryptographic proof

## Integration Points

- **Admission**: Exact-range validator runs before issue admission
- **CI Gates**: Identity gates verify trailer presence and format
- **Review**: Reviewer checks commit metadata and trailers
- **Promotion**: Promoter requires passing identity validation receipt

## Common Patterns

### Pattern: Multiple Agents Same Worktree

```sh
# Implementer
python3 tools/identity/configure_git_identity.py \
  --repo $WORKTREE \
  --persona implementer \
  --run-id run-20260828-01

# Reviewer (if running locally)
python3 tools/identity/configure_git_identity.py \
  --repo $WORKTREE \
  --persona reviewer \
  --run-id run-20260828-01-rev
```

Each phase has its own persona and run-id; trailers distinguish them.

### Pattern: Cross-Run Recovery

If attempt is resumed in new run:

```text
Agent-Run-ID: run-20260828-01-attempt-2
```

Include attempt counter if needed; validator enforces exact match.

## Non-Goals

- This system does not provide cryptographic signing
- It does not prevent unauthorized commits (owner can always commit as anyone)
- It does not replace branch protection or server-side enforcement
- It does not establish model identity or prove model authorship
