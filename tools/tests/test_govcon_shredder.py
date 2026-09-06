import json
import subprocess
import sys

# Sample synthetic FAR Part 15 RFP for testing
SAMPLE_RFP_TEXT = """
SOLICITATION NO: 36C10B26R0042
TITLE: Enterprise Cloud Hosting and Modernization Services
AGENCY: Department of Veterans Affairs
SET-ASIDE: Service-Disabled Veteran-Owned Small Business (SDVOSB)

SECTION C - DESCRIPTION/SPECIFICATIONS/WORK STATEMENT

C.1 Scope of Work
The Contractor shall provide comprehensive cloud migration and maintenance services for VA medical center applications.
The Contractor must ensure 99.99% system availability during operational hours.
The Contractor will participate in bi-weekly technical sprint reviews with the Contracting Officer's Representative (COR).

C.2 Security Requirements
C.2.1 The Contractor shall maintain FedRAMP High authorization across all proposed hosting infrastructure.
C.2.2 The Contractor must report any suspected cybersecurity incident within one hour of detection.

SECTION L - INSTRUCTIONS, CONDITIONS, AND NOTICES TO OFFERORS

L.1 General Proposal Submission Instructions
L.1.1 Proposals shall consist of four separate volumes: Volume I Technical, Volume II Management, Volume III Past Performance, Volume IV Cost/Price.
L.1.2 Volume I Technical approach shall not exceed 50 pages excluding executive summary.

L.2 Technical Proposal Instructions
L.2.1 The Offeror shall describe its technical approach to meeting all requirements specified in Section C.1.
L.2.2 The Offeror must provide a detailed architecture diagram illustrating FedRAMP High compliance per Section C.2.1.
L.2.3 The Offeror shall submit a comprehensive Quality Control Plan (QCP).

L.3 Management and Staffing Instructions
L.3.1 The Offeror shall provide resumes and signed letters of commitment for all proposed Key Personnel.
L.3.2 The Offeror must demonstrate an active SBA VetCert SDVOSB certification status.

L.4 Past Performance Instructions
L.4.1 The Offeror shall submit three past performance references of similar size, scope, and complexity completed within the past three years.

SECTION M - EVALUATION FACTORS FOR AWARD

M.1 Basis for Award
The Government will award a contract resulting from this solicitation to the responsible offeror whose offer conforms to the solicitation and represents the Best Value to the Government using Tradeoff Process.

M.2 Evaluation Factors
Factor 1 - Technical Approach
The Government will evaluate the offeror's technical approach to meeting PWS Section C requirements and the feasibility of the proposed cloud architecture.

Factor 2 - Management and Staffing
The Government will evaluate the qualifications and experience of proposed Key Personnel and the realism of the staffing plan.

Factor 3 - Past Performance
The Government will evaluate the recency, relevance, and performance quality of submitted references.

Factor 4 - Cost/Price
Price will be evaluated for reasonableness and price realism. Technical and Management factors combined are significantly more important than Cost/Price.
"""


def test_shredder_imports():
    """Verify shredder module and core classes can be imported."""
    from tools.govcon.shredder import RFPShredder, ShredderResult

    assert RFPShredder is not None
    assert ShredderResult is not None


def test_section_splitting():
    """Verify Section C, L, and M are split accurately from solicitation text."""
    from tools.govcon.shredder import RFPShredder

    shredder = RFPShredder()
    sections = shredder.split_sections(SAMPLE_RFP_TEXT)

    assert "SECTION C" in sections
    assert "SECTION L" in sections
    assert "SECTION M" in sections

    assert "Scope of Work" in sections["SECTION C"]
    assert "General Proposal Submission Instructions" in sections["SECTION L"]
    assert "Evaluation Factors" in sections["SECTION M"]


def test_requirement_extraction():
    """Verify discrete requirements are extracted with modal verbs and unique IDs."""
    from tools.govcon.shredder import RFPShredder

    shredder = RFPShredder()
    reqs = shredder.extract_requirements(SAMPLE_RFP_TEXT)

    assert len(reqs) > 0

    # Verify ID conventions
    c_reqs = [r for r in reqs if r.section == "SECTION C"]
    l_reqs = [r for r in reqs if r.section == "SECTION L"]

    assert len(c_reqs) >= 4
    assert len(l_reqs) >= 5

    assert any(r.req_id.startswith("REQ-C-") for r in c_reqs)
    assert any(r.req_id.startswith("REQ-L-") for r in l_reqs)

    # Verify modal verb detection
    shall_reqs = [r for r in reqs if r.modal_verb == "shall"]
    must_reqs = [r for r in reqs if r.modal_verb == "must"]

    assert len(shall_reqs) >= 4
    assert len(must_reqs) >= 2


def test_traceability_matrix_generation():
    """Verify bidirectional mapping between Section L, M, and C into target volumes."""
    from tools.govcon.shredder import RFPShredder

    shredder = RFPShredder()
    result = shredder.process(SAMPLE_RFP_TEXT)

    assert result is not None
    assert len(result.traceability_matrix) > 0

    # Verify Volume assignments
    vol1_rows = [
        row for row in result.traceability_matrix if row.target_volume == "Volume I Technical"
    ]
    vol2_rows = [
        row for row in result.traceability_matrix if row.target_volume == "Volume II Management"
    ]
    vol3_rows = [
        row
        for row in result.traceability_matrix
        if row.target_volume == "Volume III Past Performance"
    ]

    assert len(vol1_rows) >= 2
    assert len(vol2_rows) >= 1
    assert len(vol3_rows) >= 1

    # Check mapping to Section M factors
    mapped_to_m = [row for row in result.traceability_matrix if row.eval_factor is not None]
    assert len(mapped_to_m) > 0


def test_export_json_and_csv(tmp_path):
    """Verify serialization to rtm.json and RTM.csv."""
    from tools.govcon.shredder import RFPShredder

    shredder = RFPShredder()
    result = shredder.process(SAMPLE_RFP_TEXT)

    json_file = tmp_path / "rtm.json"
    csv_file = tmp_path / "RTM.csv"

    shredder.export_json(result, json_file)
    shredder.export_csv(result, csv_file)

    assert json_file.exists()
    assert csv_file.exists()

    # Validate JSON content
    with open(json_file, encoding="utf-8") as f:
        data = json.load(f)
        assert "metadata" in data
        assert "requirements" in data
        assert "traceability_matrix" in data
        assert data["metadata"]["total_requirements"] == len(result.requirements)

    # Validate CSV content
    with open(csv_file, encoding="utf-8") as f:
        lines = f.readlines()
        assert len(lines) > 1
        headers = lines[0].strip().split(",")
        assert "Requirement_ID" in headers
        assert "Section" in headers
        assert "Target_Volume" in headers
        assert "Section_M_Factor" in headers


def test_orphan_detection():
    """Verify that unmapped instructions or factors are flagged in compliance audit."""
    from tools.govcon.shredder import RFPShredder

    unbalanced_rfp = """
SECTION L - INSTRUCTIONS
L.1 The Offeror shall provide an unreferenced special cybersecurity plan not evaluated in Section M.

SECTION M - EVALUATION FACTORS
M.1 Factor 1 - Past Performance
Evaluation of past performance only.
"""
    shredder = RFPShredder()
    result = shredder.process(unbalanced_rfp)

    assert len(result.audit.orphan_instructions) > 0
    assert (
        "L.1" in result.audit.orphan_instructions[0].paragraph_ref
        or "cybersecurity" in result.audit.orphan_instructions[0].text.lower()
    )


def test_cli_execution(tmp_path):
    """Verify CLI interface runs end-to-end with exit code 0."""
    rfp_path = tmp_path / "test_rfp.txt"
    rfp_path.write_text(SAMPLE_RFP_TEXT, encoding="utf-8")
    out_dir = tmp_path / "output"

    cmd = [
        sys.executable,
        "tools/govcon/shredder.py",
        "parse",
        "--rfp",
        str(rfp_path),
        "--output-dir",
        str(out_dir),
        "--json",
        "--csv",
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    assert proc.returncode == 0, f"CLI failed: {proc.stderr}"
    assert "Shredding Complete" in proc.stdout or "RTM generated" in proc.stdout
    assert (out_dir / "rtm.json").exists()
    assert (out_dir / "RTM.csv").exists()
