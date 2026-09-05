---
id: "PROPOSAL-NNNN"
title: "Short imperative title"
target: "rule/file this proposal promotes or amends"
proposer: "agent:<name> | human:mike"
status: "open"
date: "YYYY-MM-DD"
decision: null
---

## Insight

What recurring pattern prompted this. For an auto-filed promotion
proposal: name the `DONT.md` row and cite every matching
`log/CORRECTIONS.log` line (2+ required) that triggered filing.

## Proposed change

The literal change: new queue-check logic, a new PreToolUse/PostToolUse
hook, or a rule-file amendment. An auto-filed proposal may leave this as
a TODO for whoever accepts it — counting violations and citing evidence
is mechanical; designing the actual enforcer is a judgment call this
loop does not make for itself.

## Rationale

Why a mechanical enforcer (queue check / hook) instead of leaving this a
written-rule-only entry.

## Evidence

Concrete pointers: the `log/CORRECTIONS.log` lines, dates, sessions —
not "this keeps happening."

---

## Decision (filled in by whoever accepts or rejects this)

- **Outcome:** accept | reject
- **If accepted:** commit hash applying the change, referencing this
  proposal's id.
- **If rejected:** reason. Moves to `proposals/rejected/` unchanged
  except this section — a recorded outcome, not a deletion, so the next
  pass doesn't re-litigate it.

**An agent never accepts its own proposal.**
