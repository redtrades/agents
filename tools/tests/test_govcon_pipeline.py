import json
import subprocess
import sys

# Sample RTM payload for pipeline tests
SAMPLE_RTM_PAYLOAD = {
    "metadata": {
        "title": "Enterprise Cloud Hosting and Modernization",
        "solicitation_number": "36C10B26R0042",
        "agency": "Department of Veterans Affairs",
        "total_requirements": 5,
    },
    "sections": ["SECTION C", "SECTION L", "SECTION M"],
    "requirements": [
        {
            "req_id": "REQ-C-001",
            "section": "SECTION C",
            "paragraph_ref": "C.1",
            "text": "The Contractor shall provide comprehensive cloud migration services.",
            "modal_verb": "shall",
            "category": "MANDATORY",
        },
        {
            "req_id": "REQ-C-002",
            "section": "SECTION C",
            "paragraph_ref": "C.2.1",
            "text": "The Contractor shall maintain FedRAMP High authorization.",
            "modal_verb": "shall",
            "category": "MANDATORY",
        },
        {
            "req_id": "REQ-L-001",
            "section": "SECTION L",
            "paragraph_ref": "L.2.1",
            "text": "The Offeror shall describe technical approach meeting Section C.1.",
            "modal_verb": "shall",
            "category": "INSTRUCTION",
        },
        {
            "req_id": "REQ-L-002",
            "section": "SECTION L",
            "paragraph_ref": "L.3.1",
            "text": "The Offeror shall provide resumes for Key Personnel.",
            "modal_verb": "shall",
            "category": "INSTRUCTION",
        },
        {
            "req_id": "REQ-L-003",
            "section": "SECTION L",
            "paragraph_ref": "L.4.1",
            "text": "The Offeror shall submit three past performance references.",
            "modal_verb": "shall",
            "category": "INSTRUCTION",
        },
    ],
    "traceability_matrix": [
        {
            "req_id": "REQ-L-001",
            "section": "SECTION L",
            "paragraph_ref": "L.2.1",
            "text": "The Offeror shall describe technical approach meeting Section C.1.",
            "modal_verb": "shall",
            "category": "INSTRUCTION",
            "target_volume": "Volume I Technical",
            "eval_factor": "Factor 1 - Technical Approach",
            "proposal_section_ref": "Volume I Technical > Section L.2.1",
            "compliance_status": "Compliant",
        },
        {
            "req_id": "REQ-L-002",
            "section": "SECTION L",
            "paragraph_ref": "L.3.1",
            "text": "The Offeror shall provide resumes for Key Personnel.",
            "modal_verb": "shall",
            "category": "INSTRUCTION",
            "target_volume": "Volume II Management",
            "eval_factor": "Factor 2 - Management and Staffing",
            "proposal_section_ref": "Volume II Management > Section L.3.1",
            "compliance_status": "Requires Client Input",
        },
        {
            "req_id": "REQ-L-003",
            "section": "SECTION L",
            "paragraph_ref": "L.4.1",
            "text": "The Offeror shall submit three past performance references.",
            "modal_verb": "shall",
            "category": "INSTRUCTION",
            "target_volume": "Volume III Past Performance",
            "eval_factor": "Factor 3 - Past Performance",
            "proposal_section_ref": "Volume III Past Performance > Section L.4.1",
            "compliance_status": "Requires Client Input",
        },
    ],
    "audit": {
        "orphan_instructions": [],
        "unmapped_factors": [],
        "summary": {
            "total_requirements": 5,
            "total_mapped_rows": 3,
            "orphan_instructions_count": 0,
        },
    },
}


def test_pipeline_imports():
    """Verify proposal pipeline module and core classes can be imported."""
    from tools.govcon.pipeline import ProposalPackage, ProposalPipeline

    assert ProposalPipeline is not None
    assert ProposalPackage is not None


def test_volume_assembly(tmp_path):
    """Verify proposal volumes are assembled from RTM data with factual placeholders."""
    from tools.govcon.pipeline import ProposalPipeline

    pipeline = ProposalPipeline()
    package = pipeline.assemble(SAMPLE_RTM_PAYLOAD, output_dir=tmp_path)

    assert package is not None
    assert (tmp_path / "PROPOSAL_PACKAGE.md").exists()
    assert (tmp_path / "Volume_I_Technical.md").exists()
    assert (tmp_path / "Volume_II_Management.md").exists()
    assert (tmp_path / "Volume_III_Past_Performance.md").exists()
    assert (tmp_path / "Volume_IV_Cost_Price.md").exists()
    assert (tmp_path / "Volume_V_Administrative.md").exists()

    # Check Volume I Technical content
    vol1_text = (tmp_path / "Volume_I_Technical.md").read_text(encoding="utf-8")
    assert "Volume I: Technical Approach" in vol1_text
    assert "REQ-L-001" in vol1_text
    assert "Factor 1 - Technical Approach" in vol1_text
    assert "FedRAMP High" in vol1_text or "cloud migration" in vol1_text

    # Check Volume II Management content
    vol2_text = (tmp_path / "Volume_II_Management.md").read_text(encoding="utf-8")
    assert "Volume II: Management Approach" in vol2_text
    assert "REQ-L-002" in vol2_text
    assert "[CLIENT PROVIDES:" in vol2_text
    assert "VetCert" in vol2_text or "SDVOSB" in vol2_text

    # Check Volume III Past Performance content
    vol3_text = (tmp_path / "Volume_III_Past_Performance.md").read_text(encoding="utf-8")
    assert "Volume III: Past Performance" in vol3_text
    assert "[CLIENT PROVIDES:" in vol3_text
    assert "Reference 1" in vol3_text


def test_client_provides_markers_present(tmp_path):
    """Verify offeror-specific sections never invent past performance or rates."""
    from tools.govcon.pipeline import ProposalPipeline

    pipeline = ProposalPipeline()
    pipeline.assemble(SAMPLE_RTM_PAYLOAD, output_dir=tmp_path)

    vol3_text = (tmp_path / "Volume_III_Past_Performance.md").read_text(encoding="utf-8")
    assert "[CLIENT PROVIDES: Customer Agency / Client Name]" in vol3_text
    assert "[CLIENT PROVIDES: Contract Number & Value]" in vol3_text

    vol4_text = (tmp_path / "Volume_IV_Cost_Price.md").read_text(encoding="utf-8")
    assert "[CLIENT PROVIDES: Loaded Hourly Rate]" in vol4_text or "[CLIENT PROVIDES:" in vol4_text


def test_jules_tasks_generation(tmp_path):
    """Verify asynchronous Jules cloud drafting tasks are generated."""
    from tools.govcon.pipeline import ProposalPipeline

    pipeline = ProposalPipeline()
    tasks = pipeline.generate_jules_tasks(SAMPLE_RTM_PAYLOAD)

    assert len(tasks) > 0
    first_task = tasks[0]
    assert "title" in first_task
    assert "objective" in first_task
    assert "acceptance_criteria" in first_task
    assert "labels" in first_task
    assert "jules" in first_task["labels"]


def test_cli_assemble_command(tmp_path):
    """Verify CLI interface runs proposal assembly end-to-end with exit code 0."""
    rtm_path = tmp_path / "test_rtm.json"
    with open(rtm_path, "w", encoding="utf-8") as f:
        json.dump(SAMPLE_RTM_PAYLOAD, f, indent=2)

    out_dir = tmp_path / "proposal_output"

    cmd = [
        sys.executable,
        "tools/govcon/pipeline.py",
        "assemble",
        "--rtm",
        str(rtm_path),
        "--output-dir",
        str(out_dir),
        "--jules",
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    assert proc.returncode == 0, f"CLI failed: {proc.stderr}"
    assert "Proposal Package Assembled" in proc.stdout
    assert (out_dir / "PROPOSAL_PACKAGE.md").exists()
    assert (out_dir / "jules_tasks.json").exists()
