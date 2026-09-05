# Architecture teardown structure

Use this structure when researching a system or factory for weaknesses and
improvements. Read it only when the task is a teardown, not a general research
question.

## 1. Diagnosis  -  what is weak, missing, or risky

- Specific, observable weaknesses ("no CLI for run inspection", "zero run
  comparison tooling").
- Grouped by category: operational, quality, security, performance.
- Each weakness: current state + the risk it creates + a concrete example from
  code, logs, or run artifacts.

## 2. Proposals  -  concrete improvements with repo paths

- Exact file paths to create or modify (`factory/cli.py`, `factory/gates/registry.py`).
- How the change works, what it affects.
- Before/after code or config snippets where relevant.

## 3. Prioritization  -  impact / effort

Table: Priority, Item, Impact, Effort, Dependencies.
- Priority: P0 (critical/foundational), P1 (high value), P2 (strategic).
- Impact and Effort: High / Medium / Low.

## 4. Risks / dependencies  -  what could block or break

- Technical risks (idempotency, notification spam, data loss).
- Dependency risks (what must be done first).
- A mitigation per risk.

## 5. Implementation roadmap

- Time-boxed phases ("Week 1", "Week 2").
- What each phase accomplishes; dependencies between phases; parallelizable work.

## 6. Appendices

- Current run-artifact inventory (what files a successful run produces).
- Registry references (each gate's purpose and where it applies).
- Diagrams, tables, contextual material.
