---
name: rfp-shredder
description: Deconstructs federal RFP solicitations into discrete requirements and generates a Requirements Traceability Matrix. Use when parsing FAR solicitations, extracting Section C/L/M clauses, or preparing proposal outlines.
---

# RFP Shredder Skill

Use this skill to parse federal solicitation documents into structured requirements.

## Quick Start

Run the shredder CLI against any text or markdown RFP file:

```bash
python3 tools/govcon/shredder.py parse --rfp <path/to/solicitation.txt> --output-dir <output/dir> --json --csv
```

Or via Makefile:

```bash
make shred-rfp RFP=<path/to/solicitation.txt>
```

## How It Works

1. **Section Segmentation:** Identifies Section C (PWS/SOW), Section L (Instructions), and Section M (Evaluation Factors) using Uniform Contract Format boundaries.
2. **Clause Extraction:** Sweeps sentences for mandatory modal verbs (`shall`, `must`, `will`, `required`) and assigns unique IDs (`REQ-C-001`, `REQ-L-001`).
3. **Traceability Matrix:** Maps instructions to target volumes and evaluation factors. Emits `rtm.json` and `RTM.csv`.

## Output Artifacts

- `rtm.json`: Complete structured data model with metadata, sections, requirements, and compliance audit.
- `RTM.csv`: Tabular spreadsheet format ready for import into Excel or Google Sheets for proposal team assignment.
