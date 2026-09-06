---
name: compliance-matrix
description: Builds and audits Shipley-style Requirements Traceability Matrices. Use when verifying proposal volume alignment against Section M evaluation factors or auditing orphan instructions.
---

# Compliance Matrix Skill

Use this skill to audit proposal compliance against RFP Section L instructions and Section M evaluation factors.

## Quick Start

Audit an existing RTM artifact for orphan instructions or unmapped requirements:

```bash
python3 tools/govcon/shredder.py audit --rtm <path/to/rtm.json>
```

To enforce strict validation where any orphan instruction triggers a non-zero exit code:

```bash
python3 tools/govcon/shredder.py parse --rfp <path/to/solicitation.txt> --strict
```

## Compliance Matrix Standards

1. **Section M Dominance:** The proposal outline must follow Section M scoring criteria, not contractor internal preference. Evaluators score strictly against Section M.
2. **100% Traceability:** Every Section L instruction must map to an explicit proposal volume and section.
3. **Orphan Elimination:** Any Section L instruction that lacks an associated Section M factor must be addressed in an un-scored compliance section to avoid disqualification.
