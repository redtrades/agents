# Plan: Add scripts/count-tasks.sh

## Task

Add a new, self-contained script `scripts/count-tasks.sh` that, with no arguments, prints the number of `.md` files **directly under `tasks/`** (not recursive) as a single integer and nothing else. Include a one-line usage comment at the top of the file. Make the script executable. Do not modify any existing file.

## Repo facts (verified)

- Repo root: `/Users/man/agent-workspace` (a git repo).
- `scripts/` exists; `count-tasks.sh` does **not** exist there yet — creating it adds a file, which is allowed.
- `tasks/` currently contains exactly one top-level `.md` file: `TASK-0001.md`, and no subdirectories — so the expected output right now is `1`.
- Existing scripts use `#!/bin/bash` with usage comments in the header (e.g. `scripts/check-stale-claims.sh`) — match that style.
- `specs/` does not exist yet; it will be created to hold this plan's copy.

## Steps

### 1. Create `scripts/count-tasks.sh`

New file, exact content:

```bash
#!/usr/bin/env bash
# Usage: scripts/count-tasks.sh — prints the number of .md files directly under tasks/ (not recursive).
set -euo pipefail

cd "$(git rev-parse --show-toplevel)"

count=0
for f in tasks/*.md; do
  [ -f "$f" ] && count=$((count + 1))
done
printf '%d\n' "$count"
```

Notes on the implementation:

- `#!/usr/bin/env bash` keeps it self-contained; `set -euo pipefail` matches the existing `scripts/` convention.
- `cd "$(git rev-parse --show-toplevel)"` makes it work from any cwd, matching how sibling scripts locate the repo root.
- The glob `tasks/*.md` is inherently non-recursive and only matches top-level entries; the `[ -f "$f" ]` guard skips a subdirectory named `*.md` and also handles the no-match case (under default shell options, an unmatched glob stays literal), so an empty `tasks/` correctly prints `0` instead of erroring.
- The script is a `&&` compound at the top level; under `set -e` the loop's final guard failure does not abort the script (compound commands at loop top level are exempt), so reaching `printf` is safe.
- `printf '%d\n'` emits exactly one line: the integer plus a trailing newline — "nothing else".

### 2. Make it executable

```sh
chmod +x scripts/count-tasks.sh
```

### 3. Verify

From the repo root:

1. `scripts/count-tasks.sh` → exit 0, stdout is exactly `1` (one line: `1`), nothing on stderr.
2. Run it from a different cwd (e.g. `cd knowledge && ../scripts/count-tasks.sh`) → still `1`, proving the `git rev-parse` cd works.
3. Negative test that recursion is excluded: `mkdir -p tasks/tmpverify && touch tasks/tmpverify/NOTCOUNTED.md`, rerun → still `1`, then `rm -rf tasks/tmpverify` to restore the exact prior state.
4. Zero test: `mv tasks/TASK-0001.md /tmp/ && scripts/count-tasks.sh` → prints `0`, then `mv /tmp/TASK-0001.md tasks/` to restore.
5. Final state check: `ls -l scripts/count-tasks.sh` shows the executable bit (`-rwxr-xr-x`), `git status --porcelain` shows only `scripts/count-tasks.sh` (new file) plus this spec — no modified existing files.

If any check fails, fix the script and re-run until all pass; do not loosen the checks.

## Out of scope / constraints

- No arguments are supported (the script takes none); no flags, no options.
- No changes to `tasks/`, `scripts/lib.sh`, the `justfile`, or any other existing file.
- No new dependencies; bash builtins + `printf` only.
