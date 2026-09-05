# agent-configs

The source library for reusable agent rules, skills, hooks, prompt templates, and
role definitions. Content here is evidence or a distribution candidate until a
specific runtime adapter installs it and behavioral checks prove discovery,
permissions, and activation.

Created 2026-08-24 and split out of `agent-workspace` and `govcon-factory`.
This README maps the library. Repository instructions remain repository-local;
volatile runtime state belongs in generated status, not in this repository map.

## Layout

```
rules/     Enforced or strongly-held behavioral rules — not project code,
           not aspirational wishlist. Each file names what it governs and,
           where one exists, its enforcement mechanism.
skills/    Claude Code Skills meant to be used from any project (SKILL.md
           + supporting files, same shape Claude Code expects under
           .claude/skills/<name>/).
hooks/     PreToolUse/PostToolUse/etc. hook scripts + their config, meant
           to be installed into ~/.claude/hooks/ (hooks must live there to
           be picked up by Claude Code — this dir is the source of truth
           they're copied FROM, not a location Claude Code reads directly).
prompts/   Reusable prompt/command templates (the shape of
           .claude/commands/*.md) — orchestration patterns, workflow
           loops, not project-specific content.
roles/     Agent role/persona definitions — boundaries, tool scope,
           reporting contract for a named role (e.g. "verifier," "lead,"
           "worker") independent of which project it's deployed in.
```

## How consumers use this library

There is no universal auto-load mechanism. A consumer selects a specific asset,
records its source revision and license, adapts it to the runtime's native format,
and proves discovery, invocation, permission boundaries, and context cost before
promotion. Do not bulk-load this repository, copy it wholesale into prompts, or
assume symlink/file presence means adoption.

Runtime-local installations may be copies, symlinks, generated adapters, or native
packages depending on the loader. Every installed asset must retain provenance and
must be updated deliberately rather than by an unreviewed global sync.

## Provenance

Every rule/skill/hook/prompt/role either originated here or names its
source (a disler/IndyDevDan repo + license, another project it was
extracted from, or "Mike, `<date>`" for things that started as direct
instruction). Nothing here is unattributed.
