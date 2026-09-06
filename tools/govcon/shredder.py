#!/usr/bin/env python3
"""
GovCon RFP Document Shredder and Compliance Matrix Generator
Parses FAR Part 15 solicitation documents (Section C, L, and M) into
discrete requirements and generates a bidirectional Requirements
Traceability Matrix (RTM) in JSON and CSV formats.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

MODAL_VERBS = ["shall", "must", "will", "required", "provide", "submit", "should"]


@dataclass
class Requirement:
    req_id: str
    section: str
    paragraph_ref: str
    text: str
    modal_verb: str
    category: str


@dataclass
class TraceabilityRow:
    req_id: str
    section: str
    paragraph_ref: str
    text: str
    modal_verb: str
    category: str
    target_volume: str
    eval_factor: str | None
    proposal_section_ref: str
    compliance_status: str


@dataclass
class ComplianceAudit:
    orphan_instructions: list[Requirement] = field(default_factory=list)
    unmapped_factors: list[str] = field(default_factory=list)
    summary: dict[str, Any] = field(default_factory=dict)


@dataclass
class ShredderResult:
    metadata: dict[str, Any]
    sections: dict[str, str]
    requirements: list[Requirement]
    traceability_matrix: list[TraceabilityRow]
    audit: ComplianceAudit


class RFPShredder:
    """Deterministic parser and matrix generator for federal RFP solicitations."""

    def __init__(self) -> None:
        self.section_pattern = re.compile(
            r"(?m)^(SECTION\s+[A-M]|Section\s+[A-M])\b[^\n]*",
            re.IGNORECASE,
        )
        self.para_pattern = re.compile(
            r"^([A-M]\.\d+(?:\.\d+)*|\d+\.\d+(?:\.\d+)*)\s+(.*)$",
            re.MULTILINE,
        )

    def split_sections(self, text: str) -> dict[str, str]:
        """Split solicitation text into mapped sections."""
        matches = list(self.section_pattern.finditer(text))
        sections: dict[str, str] = {}

        if not matches:
            sections["SECTION C"] = text
            return sections

        for i, match in enumerate(matches):
            header_raw = match.group(0).strip()
            # Normalize header key: SECTION C, SECTION L, SECTION M
            sec_match = re.search(r"SECTION\s+([A-M])", header_raw, re.IGNORECASE)
            key = f"SECTION {sec_match.group(1).upper()}" if sec_match else header_raw

            start_idx = match.end()
            end_idx = matches[i + 1].start() if i + 1 < len(matches) else len(text)
            body = text[start_idx:end_idx].strip()
            sections[key] = body

        return sections

    def extract_requirements(self, text: str) -> list[Requirement]:
        """Extract individual requirements from all recognized sections."""
        sections = self.split_sections(text)
        requirements: list[Requirement] = []

        counter = {"C": 1, "L": 1, "M": 1, "OTHER": 1}

        for sec_name, sec_body in sections.items():
            prefix = "OTHER"
            sec_match = re.search(r"SECTION\s+([A-M])", sec_name, re.IGNORECASE)
            if sec_match:
                prefix = sec_match.group(1).upper()
            elif " C" in sec_name:
                prefix = "C"
            elif " L" in sec_name:
                prefix = "L"
            elif " M" in sec_name:
                prefix = "M"

            lines = sec_body.split("\n")
            current_ref = f"{prefix}.1"

            for raw_line in lines:
                line = raw_line.strip()
                if not line:
                    continue

                # Check if line begins with a paragraph number
                p_match = re.match(r"^([A-M]\.\d+(?:\.\d+)*|\d+\.\d+(?:\.\d+)*)\s*(.*)$", line)
                if p_match:
                    current_ref = p_match.group(1)
                    content = p_match.group(2).strip()
                else:
                    content = line

                # Check for sentences or clauses containing modal verbs
                sentences = re.split(r"(?<=[.?!])\s+", content) if content else [content]
                for sentence in sentences:
                    sentence_clean = sentence.strip()
                    if not sentence_clean:
                        continue

                    lower = sentence_clean.lower()
                    detected_verb = None
                    for verb in MODAL_VERBS:
                        # Match whole word
                        if re.search(rf"\b{verb}\b", lower):
                            detected_verb = verb
                            break

                    # In Section L and M, also capture instructions even without classic modal
                    if not detected_verb:
                        if prefix == "L" and any(
                            k in lower
                            for k in ["describe", "instructions", "pages", "format", "proposals"]
                        ):
                            detected_verb = "provide"
                        elif prefix == "M" and any(
                            k in lower for k in ["evaluate", "factor", "basis for award", "rating"]
                        ):
                            detected_verb = "evaluate"

                    if detected_verb:
                        req_num = counter[prefix]
                        counter[prefix] += 1
                        req_id = f"REQ-{prefix}-{req_num:03d}"

                        category = "MANDATORY"
                        if detected_verb in ["should"]:
                            category = "OPTIONAL"
                        elif prefix == "L":
                            category = "INSTRUCTION"
                        elif prefix == "M":
                            category = "EVALUATION"

                        requirements.append(
                            Requirement(
                                req_id=req_id,
                                section=sec_name,
                                paragraph_ref=current_ref,
                                text=sentence_clean,
                                modal_verb=detected_verb,
                                category=category,
                            )
                        )

        return requirements

    def _determine_target_volume(self, req: Requirement) -> str:
        """Heuristic volume routing based on content and paragraph reference."""
        text = req.text.lower()
        ref = req.paragraph_ref.lower()

        if re.search(r"\b(past\s+performance|references?|cpars)\b", text) or "l.4" in ref:
            return "Volume III Past Performance"
        if (
            re.search(
                r"\b(management|staffing|personnel|resumes?|commitments?|vetcert|sdvosb|quality\s+control|qcp)\b",
                text,
            )
            or "l.3" in ref
        ):
            return "Volume II Management"
        if re.search(r"\b(costs?|prices?|pricing|clins?)\b", text) or "l.5" in ref:
            return "Volume IV Cost/Price"
        if re.search(r"\b(administrative|sf\s*1449|sf\s*33|representations)\b", text):
            return "Volume V Administrative"

        # Default for Section C and technical instructions
        return "Volume I Technical"

    def _map_eval_factor(self, target_volume: str, section_m_text: str) -> str | None:
        """Map target volume to corresponding Section M factor."""
        sec_m_lower = section_m_text.lower()

        if target_volume == "Volume I Technical":
            match = re.search(r"(Factor\s+1[^\n\.]*)", section_m_text, re.IGNORECASE)
            if match and "technical" in match.group(1).lower():
                return match.group(1).strip()
            if "technical" in sec_m_lower:
                return "Factor 1 - Technical Approach"

        elif target_volume == "Volume II Management":
            match = re.search(r"(Factor\s+2[^\n\.]*)", section_m_text, re.IGNORECASE)
            if match and (
                "management" in match.group(1).lower() or "staffing" in match.group(1).lower()
            ):
                return match.group(1).strip()
            if "management" in sec_m_lower or "staffing" in sec_m_lower:
                return "Factor 2 - Management and Staffing"

        elif target_volume == "Volume III Past Performance":
            match = re.search(r"(Factor\s+3[^\n\.]*)", section_m_text, re.IGNORECASE)
            if match and "past performance" in match.group(1).lower():
                return match.group(1).strip()
            if "past performance" in sec_m_lower:
                return "Factor 3 - Past Performance"

        elif target_volume == "Volume IV Cost/Price":
            match = re.search(r"(Factor\s+4[^\n\.]*)", section_m_text, re.IGNORECASE)
            if match and ("cost" in match.group(1).lower() or "price" in match.group(1).lower()):
                return match.group(1).strip()
            if "cost" in sec_m_lower or "price" in sec_m_lower:
                return "Factor 4 - Cost/Price"

        return None

    def process(self, text: str) -> ShredderResult:
        """Run full shredding and bidirectional traceability matrix construction."""
        sections = self.split_sections(text)
        requirements = self.extract_requirements(text)
        section_m_text = sections.get("SECTION M", "")

        matrix_rows: list[TraceabilityRow] = []
        orphan_instructions: list[Requirement] = []

        # Parse solicitation metadata if present
        metadata: dict[str, Any] = {
            "title": "Federal Solicitation",
            "shred_timestamp": datetime.now(UTC).isoformat(),
            "total_requirements": len(requirements),
        }
        sol_match = re.search(r"SOLICITATION\s+(?:NO|NUMBER)?:\s*([^\n]+)", text, re.IGNORECASE)
        if sol_match:
            metadata["solicitation_number"] = sol_match.group(1).strip()
        title_match = re.search(r"TITLE:\s*([^\n]+)", text, re.IGNORECASE)
        if title_match:
            metadata["title"] = title_match.group(1).strip()
        agency_match = re.search(r"AGENCY:\s*([^\n]+)", text, re.IGNORECASE)
        if agency_match:
            metadata["agency"] = agency_match.group(1).strip()

        for req in requirements:
            target_vol = self._determine_target_volume(req)
            eval_factor = self._map_eval_factor(target_vol, section_m_text)

            # Suggest proposal response section
            proposal_sec = f"{target_vol} > Section {req.paragraph_ref}"

            compliance_status = "Compliant"
            if "resumes" in req.text.lower() or "reference" in req.text.lower():
                compliance_status = "Requires Client Input"

            # Check if Section L instruction lacks an evaluation factor
            if req.section == "SECTION L" and eval_factor is None:
                orphan_instructions.append(req)

            matrix_rows.append(
                TraceabilityRow(
                    req_id=req.req_id,
                    section=req.section,
                    paragraph_ref=req.paragraph_ref,
                    text=req.text,
                    modal_verb=req.modal_verb,
                    category=req.category,
                    target_volume=target_vol,
                    eval_factor=eval_factor,
                    proposal_section_ref=proposal_sec,
                    compliance_status=compliance_status,
                )
            )

        audit = ComplianceAudit(
            orphan_instructions=orphan_instructions,
            summary={
                "total_requirements": len(requirements),
                "total_mapped_rows": len(matrix_rows),
                "orphan_instructions_count": len(orphan_instructions),
            },
        )

        return ShredderResult(
            metadata=metadata,
            sections=sections,
            requirements=requirements,
            traceability_matrix=matrix_rows,
            audit=audit,
        )

    def export_json(self, result: ShredderResult, output_path: Path | str) -> None:
        """Export full shredder result to formatted JSON."""
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        payload = {
            "metadata": result.metadata,
            "sections": list(result.sections.keys()),
            "requirements": [asdict(r) for r in result.requirements],
            "traceability_matrix": [asdict(r) for r in result.traceability_matrix],
            "audit": {
                "orphan_instructions": [asdict(r) for r in result.audit.orphan_instructions],
                "unmapped_factors": result.audit.unmapped_factors,
                "summary": result.audit.summary,
            },
        }

        with open(path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)

    def export_csv(self, result: ShredderResult, output_path: Path | str) -> None:
        """Export flattened Requirements Traceability Matrix to CSV."""
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        headers = [
            "Requirement_ID",
            "Section",
            "Paragraph_Ref",
            "Requirement_Text",
            "Modal_Verb",
            "Category",
            "Target_Volume",
            "Section_M_Factor",
            "Proposal_Section_Ref",
            "Compliance_Status",
        ]

        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            for row in result.traceability_matrix:
                writer.writerow(
                    [
                        row.req_id,
                        row.section,
                        row.paragraph_ref,
                        row.text,
                        row.modal_verb,
                        row.category,
                        row.target_volume,
                        row.eval_factor or "UNMAPPED",
                        row.proposal_section_ref,
                        row.compliance_status,
                    ]
                )


def parse_cli(argv: list[str] | None = None) -> int:
    """CLI entrypoint for GovCon RFP shredding and auditing."""
    parser = argparse.ArgumentParser(
        description="GovCon RFP Shredder and Compliance Matrix Generator",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Parse subcommand
    parse_cmd = subparsers.add_parser("parse", help="Parse solicitation and generate RTM")
    parse_cmd.add_argument("--rfp", required=True, help="Path to raw RFP text/markdown file")
    parse_cmd.add_argument(
        "--output-dir", default="output", help="Directory for generated RTM files"
    )
    parse_cmd.add_argument("--json", action="store_true", help="Generate rtm.json")
    parse_cmd.add_argument("--csv", action="store_true", help="Generate RTM.csv")
    parse_cmd.add_argument(
        "--strict", action="store_true", help="Fail if any orphan instructions exist"
    )

    # Audit subcommand
    audit_cmd = subparsers.add_parser("audit", help="Audit generated RTM for compliance gaps")
    audit_cmd.add_argument("--rtm", required=True, help="Path to rtm.json")

    args = parser.parse_args(argv)

    if args.command == "parse":
        rfp_path = Path(args.rfp)
        if not rfp_path.exists():
            print(f"Error: RFP file not found at {rfp_path}", file=sys.stderr)
            return 1

        content = rfp_path.read_text(encoding="utf-8")
        shredder = RFPShredder()
        result = shredder.process(content)

        out_dir = Path(args.output_dir)
        out_dir.mkdir(parents=True, exist_ok=True)

        json_dest = out_dir / "rtm.json"
        csv_dest = out_dir / "RTM.csv"

        # By default or if requested, emit both
        if args.json or not (args.json or args.csv):
            shredder.export_json(result, json_dest)
            print(f"Saved structured JSON: {json_dest}")

        if args.csv or not (args.json or args.csv):
            shredder.export_csv(result, csv_dest)
            print(f"Saved tabular CSV: {csv_dest}")

        print("\nShredding Complete:")
        print(f"  Sections Parsed: {len(result.sections)}")
        print(f"  Total Requirements: {len(result.requirements)}")
        print(f"  Traceability Matrix Rows: {len(result.traceability_matrix)}")
        print(f"  Orphan Instructions: {len(result.audit.orphan_instructions)}")

        if args.strict and result.audit.orphan_instructions:
            print(
                f"\nSTRICT FAILURE: {len(result.audit.orphan_instructions)} orphan instructions detected.",
                file=sys.stderr,
            )
            return 2

        return 0

    if args.command == "audit":
        rtm_path = Path(args.rtm)
        if not rtm_path.exists():
            print(f"Error: RTM file not found at {rtm_path}", file=sys.stderr)
            return 1

        with open(rtm_path, encoding="utf-8") as f:
            data = json.load(f)

        orphans = data.get("audit", {}).get("orphan_instructions", [])
        total = data.get("metadata", {}).get("total_requirements", 0)

        print(f"RTM Audit Report for {rtm_path.name}:")
        print(f"  Total Requirements: {total}")
        print(f"  Orphan Instructions: {len(orphans)}")

        if orphans:
            print("\nFlagged Orphan Instructions:")
            for o in orphans:
                print(f"  - [{o.get('req_id')}] ({o.get('paragraph_ref')}): {o.get('text')}")
            return 2

        print("\nAll instructions mapped to evaluation criteria.")
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(parse_cli())
