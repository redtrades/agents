# Local agent commit identity

`tools/identity/configure_git_identity.py` establishes deterministic Git
**attribution** for one agent run. It does not create a commit, change a global
Git setting, configure a signing key, enable GPG/SSH signing, or establish a
cryptographic identity.

## Use

Run it only for the intended existing Git worktree/repository:

```sh
python3 tools/identity/configure_git_identity.py \
  --repo /path/to/worktree \
  --persona reviewer-bot \
  --run-id run-20260828-01 \
  --model gpt-5.6-terra
```

The helper validates all inputs before invoking Git, enables Git's
`extensions.worktreeConfig`, and writes these two values through
`git -C <repo> config --worktree`:

```text
user.name  = Agent reviewer-bot
user.email = agent+reviewer-bot.run-20260828-01@agents.invalid
```

`agents.invalid` is an intentionally non-delivery domain. It keeps the author
address separate from Mike's email identities and avoids using an address that
could be linked to him by GitHub. Each linked worktree therefore keeps its own
persona instead of overwriting its siblings. The helper never calls
`git config --global` and does not write author identity into the shared
repository config.

Accepted values are deliberately narrow:

- persona: lowercase letter followed by up to 31 lowercase letters, digits, or
  hyphens;
- run ID: lowercase letter/digit followed by 7–63 lowercase letters, digits, or
  hyphens;
- optional model: a single-line identifier made from letters, digits, `.`, `_`,
  `+`, `:`, `/`, or `-`.

Unsafe, path-like, whitespace-containing, or multiline values fail before any
worktree-local Git identity key is written.

## Required commit trailers

Every agent-authored commit using this identity must include these trailers:

```text
Agent-Actor: agent/<persona>
Agent-Run-ID: <run-id>
```

When known, include this additional trailer:

```text
Agent-Model: <model-id>
```

For the example above:

```text
Agent-Actor: agent/reviewer-bot
Agent-Run-ID: run-20260828-01
Agent-Model: gpt-5.6-terra
```

The helper emits these exact trailer lines in its deterministic JSON report so a
caller can add them to a commit message. It does not make the commit itself.

## Attribution is not a signature

`user.name`, `user.email`, and trailers identify a claimed actor and run for
review/audit. They are not cryptographic proof of who made a commit. This helper
does not set `commit.gpgsign`, `user.signingkey`, SSH signing configuration, or a
signature verification policy. Any signature requirement must be configured and
verified as a separate approved control.

## Exact-range admission

Attribution becomes an admission decision only when every commit in an explicit
`base..head` range passes the executable gate:

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

The validator refuses to run unless Python isolated and no-site modes (`-I -S`)
are active. Its bootstrap check imports only the built-in `sys` module before
enforcing those conditions, so sibling, startup, and site-customization modules
cannot execute first during a direct invocation. These checks are defense in depth,
not execution provenance: the validator cannot attest its own memory image,
interpreter, executable digests, or direct-file invocation. The trusted outer
CI/controller must select and attest the exact Python and Git executables and
digests, the `python -I -S /absolute/accepted/validator` argv, and the prohibition
on `-c`, `exec`, `runpy`, or equivalent in-memory loading. The validator only
requires the supplied Git path to resolve to an absolute file.

The controller supplies lowercase, full 40-hex commit object IDs; `HEAD`, branch
or tag names, abbreviations, uppercase IDs, and revision expressions are invalid.
The validator resolves both objects and requires each resolved ID to equal its
requested ID exactly. It then requires the base to be an ancestor of the head
and enumerates the complete range in deterministic reverse topological order.

The single-line, key-sorted JSON receipt is portable. It records exact base and
head, controller-supplied expected actor and run, actual and expected validator
file SHA-256 and Git blob identity, the ordered commit set, each commit's tree and
parents, whether its tree differs from its first parent, raw author and committer
identity, parsed identity trailers, and any violations. Its `execution` field is
always `{"attestation":"external-required","self_attested":false}`; it never
claims direct-file or memory-image provenance from self-observation. It deliberately
excludes executable, repository, and worktree paths. A controller puts executable
digests, exact argv, and local paths in its separately signed outer receipt.
Identical objects checked with the same on-disk validator and expectations in
another linked worktree or clone produce byte-identical portable receipt output.

Exit behavior is stable:

- `0`: logical validation of the exact range passed; this is never admission by
  itself, which also requires the trusted controller's signed outer execution
  attestation;
- `1`: the validator identity differs from the controller's accepted identity,
  or Git objects resolved but the range violates identity policy or ancestry;
- `2`: CLI input or repository inspection failed, including an unresolved object,
  non-exact object input, non-isolated Python, site-enabled execution, invalid
  absolute Git path, nonempty graft overlay, shallow history, or path that is not
  a Git worktree.

The gate invokes `git interpret-trailers --parse`; trailer-looking body text is
not sufficient. It runs that parser outside repository discovery with system,
global, local, and caller-injected Git configuration excluded and a stable
locale. A repository or environment trailer alias therefore cannot reinterpret
the immutable commit message. Every agent commit, material or empty, must have
exactly one adjacent final-block sequence in this order:

```text
Agent-Actor: agent/<persona>
Agent-Run-ID: <run-id>
Agent-Model: <model-id>  # optional
```

Blank-line-split, reordered, duplicated, multiline, conflicting, or unknown
`Agent-*` fields fail. The actor and run must also agree with both raw commit
identities, which must be identical and use the worktree-local shape established
by this helper:

```text
Agent <persona> <agent+<persona>.<run-id>@agents.invalid>
```

This binding is claimed attribution, not cryptographic authentication. A later
valid empty commit cannot repair a malformed earlier commit because the entire
range is always checked.

Ordinary human commits may omit all `Agent-*` trailers. Human-authored merge
commits are handled the same way and are reported as `human-merge`; their merged
side commits remain individually present in the checked range. A human commit
that carries an agent claim, a partially agent-shaped raw identity, or an agent
commit whose author and committer disagree fails closed. Every agent-authored
commit in one candidate range must also match the controller-supplied expected
actor and run. Ordinary human commits may coexist in that range, but a second
agent actor or run requires a separately claimed range. Current worktree Git
configuration is never promotion authority.

Every repository operation uses the controller-pinned absolute Git executable
with both `--no-replace-objects` and `GIT_NO_REPLACE_OBJECTS=1`. The subprocess
environment is rebuilt from a fixed allowlist without caller `PATH` or Git config
injection. Replacement refs therefore cannot pair an original object ID with
replacement commit, tree, parent, or message bytes. Because legacy graft files
cannot be disabled as uniformly, any nonempty graft overlay is rejected before
range inspection. Shallow repositories are also rejected: the gate does not
claim complete `base..head` evidence when the object store declares truncated
history.

## Validator bootstrap and pinning

Issue #21 is a one-time manually reviewed bootstrap. Its candidate validator
cannot authorize its own admission. The candidate requires fresh independent
exact-history and implementation review followed by the repository's existing
promotion controls.

After that bootstrap is accepted, a controller must load the validator from
accepted authority, calculate and supply its exact on-disk file SHA-256 and Git
blob, and compare those evidence fields in the portable receipt. The validator
denies an on-disk byte mismatch before object inspection, but this is not proof of
the executing memory image. The trusted controller alone attests the locked Python
and Git executable digests, exact direct-file argv, accepted validator digest, and
absence of an in-memory loader in a separately signed outer receipt. A Python 3.9
`-I -S -c` parent can rewrite `sys.argv[0]` and `__file__`; no in-process heuristic
is treated as a substitute for that outer attestation.

## Verification boundary

The focused tests use temporary repositories and an isolated synthetic global
Git config. They prove worktree configuration is deterministic, linked worktrees
retain distinct identities, global config bytes remain unchanged, unsafe
persona/run values are rejected, and no signing setting is enabled. They do not
modify the live `agent-platform` repository's identity.

The range-gate tests create real material, empty, expected-identity mismatch,
human, and merge commits. They prove portable byte equality across a linked
worktree and clone, config-poison resistance, exact object input, ignored replace
refs, rejected grafts and shallow histories, isolated import behavior, and
runs without site/startup customization, explicitly self-unattested forged
in-memory execution, and tampered on-disk validator rejection. They also preserve exact regression
ranges for the malformed published histories from PRs #14, #17, #18, and #19
when those objects are present locally. The validator reads Git objects only: it
installs no hook, rewrites no history, and changes no Git configuration.
