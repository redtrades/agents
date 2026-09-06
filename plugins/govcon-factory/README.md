# GovCon Factory Plugin

Production-ready federal RFP document shredder, compliance matrix generator, and proposal volume starter deliverable tools.

## Architecture

This plugin implements deterministic FAR Part 15 solicitation decomposition and requirements traceability:

1. **RFP Shredder (`tools/govcon/shredder.py`):**
   - Splits Uniform Contract Format (UCF) solicitations into Section C (PWS/SOW), Section L (Instructions), and Section M (Evaluation Factors).
   - Extracts discrete requirements with modal verb classification (shall, must, will, required).
   - Generates bidirectional Requirements Traceability Matrices (RTM) in JSON (`rtm.json`) and tabular CSV (`RTM.csv`).
   - Audits orphan instructions and unscored factors.

2. **Agents:**
   - `rfp-shredder`: Expert agent for decomposing complex federal solicitations, amendments, and appendices.
   - `compliance-matrix-architect`: Specialist agent for constructing Shipley-compliant Section L/M compliance matrices.

3. **Skills:**
   - `rfp-shredder`: Invokes deterministic parsing and AST breakdown of RFP documents.
   - `compliance-matrix`: Validates proposal volume alignment against Section M evaluation factors.
