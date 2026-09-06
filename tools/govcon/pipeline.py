#!/usr/bin/env python3
"""
GovCon Multi-Agent Proposal Starter Pipeline and Volume Assembler
Consumes structured Requirements Traceability Matrices (rtm.json) and
assembles complete, Shipley-compliant proposal starter volumes (Volumes I-V)
with strict factual grounding, client placeholders, and Jules cloud task manifests.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class ProposalPackage:
    master_path: Path
    volume_paths: dict[str, Path]
    jules_tasks_path: Path | None = None


class ProposalPipeline:
    """Multi-agent proposal volume assembler and drafting orchestrator."""

    def __init__(self) -> None:
        pass

    def assemble(self, rtm_data: dict[str, Any], output_dir: Path | str) -> ProposalPackage:
        """Assemble all proposal volumes and master overview document from RTM data."""
        out = Path(output_dir)
        out.mkdir(parents=True, exist_ok=True)

        meta = rtm_data.get("metadata", {})
        title = meta.get("title", "Federal Proposal")
        sol_no = meta.get("solicitation_number", "SOLICITATION-TBD")
        agency = meta.get("agency", "Federal Agency")
        reqs = rtm_data.get("requirements", [])
        matrix = rtm_data.get("traceability_matrix", [])

        # 1. Master Package Document
        master_content = self._render_master_package(title, sol_no, agency, matrix)
        master_path = out / "PROPOSAL_PACKAGE.md"
        master_path.write_text(master_content, encoding="utf-8")

        # 2. Volume I: Technical Approach
        vol1_content = self._render_volume_i(title, sol_no, reqs, matrix)
        vol1_path = out / "Volume_I_Technical.md"
        vol1_path.write_text(vol1_content, encoding="utf-8")

        # 3. Volume II: Management Approach
        vol2_content = self._render_volume_ii(title, sol_no, reqs, matrix)
        vol2_path = out / "Volume_II_Management.md"
        vol2_path.write_text(vol2_content, encoding="utf-8")

        # 4. Volume III: Past Performance
        vol3_content = self._render_volume_iii(title, sol_no, reqs, matrix)
        vol3_path = out / "Volume_III_Past_Performance.md"
        vol3_path.write_text(vol3_content, encoding="utf-8")

        # 5. Volume IV: Cost / Price
        vol4_content = self._render_volume_iv(title, sol_no, reqs, matrix)
        vol4_path = out / "Volume_IV_Cost_Price.md"
        vol4_path.write_text(vol4_content, encoding="utf-8")

        # 6. Volume V: Administrative
        vol5_content = self._render_volume_v(title, sol_no, reqs, matrix)
        vol5_path = out / "Volume_V_Administrative.md"
        vol5_path.write_text(vol5_content, encoding="utf-8")

        return ProposalPackage(
            master_path=master_path,
            volume_paths={
                "Volume I": vol1_path,
                "Volume II": vol2_path,
                "Volume III": vol3_path,
                "Volume IV": vol4_path,
                "Volume V": vol5_path,
            },
        )

    def generate_jules_tasks(self, rtm_data: dict[str, Any]) -> list[dict[str, Any]]:
        """Generate structured task specifications for asynchronous cloud drafting."""
        meta = rtm_data.get("metadata", {})
        sol_no = meta.get("solicitation_number", "SOLICITATION")
        matrix = rtm_data.get("traceability_matrix", [])

        tasks = []

        # Task 1: Volume I Technical narrative
        vol1_reqs = [r for r in matrix if r.get("target_volume") == "Volume I Technical"]
        if vol1_reqs:
            tasks.append(
                {
                    "title": f"govcon(volume-i): draft technical approach narrative for {sol_no}",
                    "objective": "Draft technical methodology responding point by point to Section C scope requirements.",
                    "acceptance_criteria": [
                        "Address all Section C tasks enumerated in compliance matrix",
                        "Embed architectural diagrams and security compliance details",
                        "Include risk mitigation matrix with likelihood and severity ratings",
                        "Do not invent offeror past performance or client-specific certifications",
                    ],
                    "labels": ["jules", "jules:cloud", "area:govcon-factory"],
                    "target_requirements": [r.get("req_id") for r in vol1_reqs],
                }
            )

        # Task 2: Volume II Management & Staffing narrative
        vol2_reqs = [r for r in matrix if r.get("target_volume") == "Volume II Management"]
        tasks.append(
            {
                "title": f"govcon(volume-ii): draft staffing and management plan for {sol_no}",
                "objective": "Draft management volume narrative including staffing plan and VetCert compliance.",
                "acceptance_criteria": [
                    "Map key personnel qualifications to solicitation requirements",
                    "Include organizational breakdown structure (OBS)",
                    "Embed SBA VetCert SDVOSB status assertions per 13 CFR Part 128",
                    "Flag all offeror-specific details with [CLIENT PROVIDES] tags",
                ],
                "labels": ["jules", "jules:cloud", "area:govcon-factory"],
                "target_requirements": [r.get("req_id") for r in vol2_reqs],
            }
        )

        # Task 3: Volume IV Cost / Price Basis of Estimate
        tasks.append(
            {
                "title": f"govcon(volume-iv): draft basis of estimate and price realism narrative for {sol_no}",
                "objective": "Draft pricing volume narrative addressing CLIN schedule and price realism.",
                "acceptance_criteria": [
                    "Detail labor categories, mapping to technical volume staffing hours",
                    "Justify cost realism and reasonableness per FAR 15.404-1",
                    "Avoid unbalanced pricing risks",
                    "Leave actual hourly dollar figures for client population with [CLIENT PROVIDES: ...]",
                ],
                "labels": ["jules", "jules:cloud", "area:govcon-factory"],
                "target_requirements": [],
            }
        )

        return tasks

    def _render_master_package(
        self, title: str, sol_no: str, agency: str, matrix: list[dict[str, Any]]
    ) -> str:
        """Render master proposal package summary."""
        lines = [
            f"# Proposal Package: {title}",
            "",
            f"- **Solicitation:** {sol_no}",
            f"- **Agency:** {agency}",
            "- **Status:** Starter Deliverable Assembled",
            "- **Methodology:** Shipley Associates compliant / FAR Part 15 aligned",
            "",
            "## Proposal Structure",
            "",
            "1. **Volume I: Technical Approach** (`Volume_I_Technical.md`)",
            "2. **Volume II: Management Approach** (`Volume_II_Management.md`)",
            "3. **Volume III: Past Performance** (`Volume_III_Past_Performance.md`)",
            "4. **Volume IV: Cost / Price** (`Volume_IV_Cost_Price.md`)",
            "5. **Volume V: Administrative** (`Volume_V_Administrative.md`)",
            "",
            "## Master Requirements Traceability Matrix (RTM)",
            "",
            "| Req ID | Section | Ref | Requirement Text | Target Volume | Evaluated Factor | Status |",
            "|---|---|---|---|---|---|---|",
        ]

        for r in matrix:
            req_id = r.get("req_id", "")
            sec = r.get("section", "")
            pref = r.get("paragraph_ref", "")
            text_trunc = (
                r.get("text", "")[:60] + "..." if len(r.get("text", "")) > 60 else r.get("text", "")
            )
            vol = r.get("target_volume", "")
            factor = r.get("eval_factor", "UNMAPPED")
            status = r.get("compliance_status", "Compliant")
            lines.append(
                f"| {req_id} | {sec} | {pref} | {text_trunc} | {vol} | {factor} | {status} |"
            )

        lines.append("")
        return "\n".join(lines)

    def _render_volume_i(
        self, title: str, sol_no: str, reqs: list[dict[str, Any]], matrix: list[dict[str, Any]]
    ) -> str:
        """Render Volume I Technical Approach."""
        c_reqs = [r for r in reqs if r.get("section") == "SECTION C"]
        l_reqs = [r for r in matrix if r.get("target_volume") == "Volume I Technical"]

        lines = [
            f"# Volume I: Technical Approach: {title}",
            f"**Solicitation:** {sol_no}",
            "",
            "## 1. Executive Summary",
            "This volume articulates our comprehensive, low-risk technical approach to fulfilling the Government's mission objectives. Our solution couples proven commercial modern technologies with rigorous federal compliance.",
            "",
            "## 2. Evaluation Factor Alignment: Factor 1 - Technical Approach",
            "The technical approach directly mirrors the scoring factors specified in Section M:",
            "",
        ]

        for r in l_reqs:
            lines.extend(
                [
                    f"### Instruction {r.get('req_id')} ({r.get('paragraph_ref')})",
                    f"> **Requirement:** {r.get('text')}",
                    f"> **Mapped Factor:** {r.get('eval_factor')}",
                    "",
                    "**Proposed Technical Methodology:**",
                    "Our team addresses this requirement through an automated, resilient implementation strategy designed to exceed baseline performance metrics.",
                    "",
                ]
            )

        lines.extend(
            [
                "## 3. Work Scope Execution (Section C / PWS Tasks)",
                "Detailed response to enumerated performance tasks:",
                "",
            ]
        )

        for r in c_reqs:
            lines.extend(
                [
                    f"### {r.get('req_id')} ({r.get('paragraph_ref')})",
                    f"- **PWS Requirement:** {r.get('text')}",
                    f"- **Modal Standard:** {str(r.get('modal_verb') or 'SHALL').upper()}",
                    "- **Technical Solution:** [CLIENT PROVIDES: Specific Architecture Component / Tooling]",
                    "- **Value Proposition & Strength:** Exceeds baseline performance by integrating continuous automated verification.",
                    "",
                ]
            )

        lines.extend(
            [
                "## 4. Risk Identification & Mitigation Matrix",
                "",
                "| Risk ID | Description | Likelihood | Impact | Mitigation Strategy |",
                "|---|---|---|---|---|",
                "| RISK-01 | Cloud migration schedule compression | Low | Moderate | Parallelized workload waves and automated rollbacks |",
                "| RISK-02 | FedRAMP High boundary synchronization | Very Low | High | Pre-authorized GovCloud boundary and automated CSP compliance scanning |",
                "",
                "## 5. Quality Control Plan (QCP)",
                "Our QCP enforces deterministic, zero-defect delivery across all contractual milestones.",
                "",
            ]
        )

        return "\n".join(lines)

    def _render_volume_ii(
        self, title: str, sol_no: str, reqs: list[dict[str, Any]], matrix: list[dict[str, Any]]
    ) -> str:
        """Render Volume II Management Approach."""
        l_reqs = [r for r in matrix if r.get("target_volume") == "Volume II Management"]

        lines = [
            f"# Volume II: Management Approach & Key Personnel: {title}",
            f"**Solicitation:** {sol_no}",
            "",
            "## 1. Management Methodology",
            "Our program management structure establishes clear lines of authority, single-point accountability, and transparent communication with the Contracting Officer's Representative (COR).",
            "",
            "## 2. Evaluation Factor Alignment: Factor 2 - Management and Staffing",
            "",
        ]

        for r in l_reqs:
            lines.extend(
                [
                    f"### Instruction {r.get('req_id')} ({r.get('paragraph_ref')})",
                    f"> **Requirement:** {r.get('text')}",
                    "",
                    "- **Staffing Approach:** [CLIENT PROVIDES: Offeror Staffing Roster and Labor Pool]",
                    "- **Key Personnel:** [CLIENT PROVIDES: Resumes and Signed Letters of Commitment]",
                    "",
                ]
            )

        lines.extend(
            [
                "## 3. Small Business & SDVOSB Compliance",
                "Our firm maintains active, verified SBA VetCert certification under 13 CFR Part 128:",
                "- **Certification Regime:** SBA VetCert (valid 3-year term)",
                "- **Certification Date:** [CLIENT PROVIDES: Active VetCert Date]",
                "- **Work Share Commitment:** At least 51% of the cost of contract performance will be performed by the prime contractor.",
                "",
            ]
        )

        return "\n".join(lines)

    def _render_volume_iii(
        self, title: str, sol_no: str, reqs: list[dict[str, Any]], matrix: list[dict[str, Any]]
    ) -> str:
        """Render Volume III Past Performance."""
        lines = [
            f"# Volume III: Past Performance: {title}",
            f"**Solicitation:** {sol_no}",
            "",
            "## 1. Overview & Relevancy Statement",
            "In accordance with FAR 15.305(a)(2), the following references demonstrate recent (<3 years) and highly relevant performance of similar size, scope, and technical complexity.",
            "",
            "## 2. Past Performance Citations",
            "",
            "### Reference 1",
            "- **Customer Agency / Client Name:** [CLIENT PROVIDES: Customer Agency / Client Name]",
            "- **Contract Number & Value:** [CLIENT PROVIDES: Contract Number & Value]",
            "- **Period of Performance:** [CLIENT PROVIDES: Dates within past 3 years]",
            "- **Relevancy Determination:** Highly Relevant: scope directly aligns with cloud migration and high-availability operations.",
            "- **CPARS Performance Rating:** [CLIENT PROVIDES: Exceptional / Very Good rating]",
            "- **Client Point of Contact:** [CLIENT PROVIDES: COR/CO Name, Phone, Email]",
            "",
            "### Reference 2",
            "- **Customer Agency / Client Name:** [CLIENT PROVIDES: Customer Agency / Client Name]",
            "- **Contract Number & Value:** [CLIENT PROVIDES: Contract Number & Value]",
            "- **Period of Performance:** [CLIENT PROVIDES: Dates within past 3 years]",
            "- **Relevancy Determination:** Relevant: managed services and security operations.",
            "- **CPARS Performance Rating:** [CLIENT PROVIDES: Exceptional / Very Good rating]",
            "- **Client Point of Contact:** [CLIENT PROVIDES: COR/CO Name, Phone, Email]",
            "",
            "### Reference 3",
            "- **Customer Agency / Client Name:** [CLIENT PROVIDES: Customer Agency / Client Name]",
            "- **Contract Number & Value:** [CLIENT PROVIDES: Contract Number & Value]",
            "- **Period of Performance:** [CLIENT PROVIDES: Dates within past 3 years]",
            "- **Relevancy Determination:** Relevant: federal infrastructure engineering.",
            "- **CPARS Performance Rating:** [CLIENT PROVIDES: Exceptional / Very Good rating]",
            "- **Client Point of Contact:** [CLIENT PROVIDES: COR/CO Name, Phone, Email]",
            "",
        ]

        return "\n".join(lines)

    def _render_volume_iv(
        self, title: str, sol_no: str, reqs: list[dict[str, Any]], matrix: list[dict[str, Any]]
    ) -> str:
        """Render Volume IV Cost / Price."""
        lines = [
            f"# Volume IV: Cost / Price Proposal: {title}",
            f"**Solicitation:** {sol_no}",
            "",
            "## 1. Basis of Estimate (BOE) Narrative",
            "Our price proposal presents fully burdened, competitive rates formulated using historical labor accounting data. Our pricing is evaluated for price reasonableness and cost realism in accordance with FAR 15.404-1.",
            "",
            "## 2. Contract Line Item Number (CLIN) Pricing Schedule",
            "",
            "| CLIN | Description | Qty | Unit | Unit Price | Extended Amount |",
            "|---|---|---|---|---|---|",
            "| 0001 | Cloud Migration Core Engineering | 12 | MO | [CLIENT PROVIDES: Monthly Rate] | [CLIENT PROVIDES: Total] |",
            "| 0002 | FedRAMP High Security Operations | 12 | MO | [CLIENT PROVIDES: Monthly Rate] | [CLIENT PROVIDES: Total] |",
            "| 0003 | Program Management and Transition | 1 | JB | [CLIENT PROVIDES: Fixed Amount] | [CLIENT PROVIDES: Total] |",
            "",
            "## 3. Labor Categories & Loaded Rates",
            "",
            "| Labor Category | Standard Hours | Loaded Hourly Rate | Total |",
            "|---|---|---|---|",
            "| Lead Cloud Architect | 1920 | [CLIENT PROVIDES: Loaded Hourly Rate] | [CLIENT PROVIDES: Total] |",
            "| Senior Security Engineer | 1920 | [CLIENT PROVIDES: Loaded Hourly Rate] | [CLIENT PROVIDES: Total] |",
            "| DevOps Systems Engineer | 1920 | [CLIENT PROVIDES: Loaded Hourly Rate] | [CLIENT PROVIDES: Total] |",
            "",
            "## 4. Price Realism Justification",
            "Our labor rates align with current Bureau of Labor Statistics (BLS) and GSA MAS wage indices, eliminating any risk of unbalanced pricing or understaffing during contract execution.",
            "",
        ]

        return "\n".join(lines)

    def _render_volume_v(
        self, title: str, sol_no: str, reqs: list[dict[str, Any]], matrix: list[dict[str, Any]]
    ) -> str:
        """Render Volume V Administrative / Reps & Certs."""
        lines = [
            f"# Volume V: Administrative / Representations & Certifications: {title}",
            f"**Solicitation:** {sol_no}",
            "",
            "## 1. Standard Form Execution",
            "- Executed Standard Form 33 / SF 1449: [CLIENT PROVIDES: Signed SF Form]",
            "- Amendments Acknowledged: Amendments 0001 through 000X acknowledged and attached.",
            "",
            "## 2. Organizational Conflict of Interest (OCI) Statement",
            "The offeror certifies that no unfair competitive advantage or impaired objectivity exists regarding this procurement.",
            "",
            "## 3. System for Award Management (SAM.gov) Compliance",
            "- **Unique Entity Identifier (UEI):** [CLIENT PROVIDES: 12-character UEI]",
            "- **CAGE Code:** [CLIENT PROVIDES: 5-character CAGE]",
            "- **Registration Expiration Date:** [CLIENT PROVIDES: Active SAM Expiration Date]",
            "",
        ]

        return "\n".join(lines)


def parse_cli(argv: list[str] | None = None) -> int:
    """CLI entrypoint for GovCon proposal volume assembly."""
    parser = argparse.ArgumentParser(
        description="GovCon Proposal Volume Starter Assembler",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    assemble_cmd = subparsers.add_parser(
        "assemble", help="Assemble proposal volumes from RTM matrix"
    )
    assemble_cmd.add_argument("--rtm", required=True, help="Path to rtm.json")
    assemble_cmd.add_argument(
        "--output-dir", default="proposal", help="Output directory for volumes"
    )
    assemble_cmd.add_argument(
        "--jules", action="store_true", help="Generate async Jules cloud tasks JSON"
    )

    args = parser.parse_args(argv)

    if args.command == "assemble":
        rtm_path = Path(args.rtm)
        if not rtm_path.exists():
            print(f"Error: RTM file not found at {rtm_path}", file=sys.stderr)
            return 1

        with open(rtm_path, encoding="utf-8") as f:
            rtm_data = json.load(f)

        pipeline = ProposalPipeline()
        out_dir = Path(args.output_dir)
        package = pipeline.assemble(rtm_data, output_dir=out_dir)

        print("\nProposal Package Assembled:")
        print(f"  Master Document: {package.master_path}")
        for name, p in package.volume_paths.items():
            print(f"  {name}: {p}")

        if args.jules:
            tasks = pipeline.generate_jules_tasks(rtm_data)
            jules_path = out_dir / "jules_tasks.json"
            with open(jules_path, "w", encoding="utf-8") as f:
                json.dump({"tasks": tasks}, f, indent=2)
            print(f"  Jules Cloud Tasks: {jules_path} ({len(tasks)} tasks generated)")

        return 0

    return 0


if __name__ == "__main__":
    sys.exit(parse_cli())
