# Constitution

Five rules. Each has exactly one enforcer that physically rejects a violation
at commit time — not a convention, not a reminder in a prompt. If a rule here
has no enforcer, it doesn't belong in this file; move it to a wishlist
instead of pretending it's binding.

Rationale for five: an earlier retrospective on this workspace found 65
codified rules with exactly one actually enforced. Five enforced beats
sixty-five aspirational. These five were drawn directly from failures
observed in one day of real work (see `git log --follow CONSTITUTION.md` for
amendments and why).

---

### 1. No claim of done without evidence

A task cannot move to `state: done` without a non-empty `evidence:` field
naming the concrete thing that proves it — a command and its output, a file
path and line range, a commit hash, a URL. "I did it" is not evidence.
"Ran `pytest tests/`, 42 passed" is.

**Enforcer:** `scripts/hooks/checks/01-done-needs-evidence.sh`
(git pre-commit hook)

---

### 2. Every assertion traces to a source or is removed

Claims recorded in `knowledge/` must carry a `source:` — a file path, a URL,
or a commit hash. An unsourced claim does not get softened with a hedge
word ("likely", "seems", "probably") and left in place; it gets deleted.
Hedging is how false claims survive review. Deletion is not.

**Enforcer:** `scripts/hooks/checks/02-claims-need-source.sh`
(git pre-commit hook)

---

### 3. A withdrawn instruction is marked withdrawn in place

Nothing under `tasks/` or in this file's rule list is ever deleted or
silently renamed out from under an owner. To retire it, its `state` moves
to `withdrawn` with a `withdrawn_reason`, in the same file, in the same
place. History shows what was true and when it stopped being true. This
directly targets today's failure: an agent found itself writing to a folder
that had been renamed out from under it, with no trace of the rename.

**Enforcer:** `scripts/hooks/checks/03-no-silent-withdrawal.sh`
(git pre-commit hook — blocks deletion/rename of tracked task files;
requires `withdrawn_reason` when `state: withdrawn`)

---

### 4. No shared artifact is edited without a commit

`BOARD.md` is a generated summary of `tasks/*.md`, not a place to hand-edit
status. It is only ever produced by `scripts/generate-board.sh`, and a
commit that changes it must match what that script would generate right
now. This directly targets today's failure: a document asserted it had
been re-synced when it had not — the words said "synced," the content
disagreed, and nothing caught it before a human trusted the words.

**Enforcer:** `scripts/hooks/checks/04-board-must-be-regenerated.sh`
(git pre-commit hook — regenerates BOARD.md into a temp file and diffs it
against the staged version)

---

### 5. Anything reserved for a human stays blank

Fields named `human_decision` in a task file are for a human to fill in and
for nothing else to touch. An agent commit — identified by a committer
identity of the form `agent:<name>` — that sets a `human_decision` field to
anything other than `null` is rejected outright, regardless of how
confident the agent was.

**Enforcer:** `scripts/hooks/checks/05-human-fields-stay-blank.sh`
(git pre-commit hook — checks committer identity against changed
`human_decision` fields)

---

## Amendment process

Amending this file follows rule 3: an old rule doesn't disappear, it moves
to a "Withdrawn" section below with a reason and the commit that replaced
it. New rules require a working enforcer in the same commit — no rule
without a mechanism.

## Withdrawn

(none yet)
