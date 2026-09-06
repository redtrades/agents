#!/usr/bin/env python3
"""Standardized issue dispatch payload parser and validator for GitHub Jules App.

Validates that an issue candidate carries structured sections (Objective,
Acceptance Criteria, Bounded Scope), valid trigger labels (jules, jules:cloud),
and bounded scope before dispatching to cloud execution.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from typing import Any

VALID_LABELS = {"jules", "jules:cloud"}
EXCLUDED_LABELS = {"type:epic", "type:program", "state:blocked"}

SECTION_HEADER_RE = re.compile(
    r"^(?:#+\s*|(?:\*\*)?)(Objective|Acceptance Criteria|Bounded Scope|Scope)(?:\*\*)?:?\s*$",
    re.IGNORECASE | re.MULTILINE,
)


def parse_issue_sections(body: str) -> dict[str, str]:
    """Parse structured markdown sections from an issue body."""
    sections: dict[str, str] = {}
    if not body:
        return sections

    lines = body.splitlines()
    current_section: str | None = None
    current_content: list[str] = []

    for line in lines:
        stripped = line.strip()
        # Check header match
        header_match = re.match(
            r"^(?:#+\s*|(?:\*\*)?)(Objective|Acceptance Criteria|Bounded Scope|Scope)(?:\*\*)?:?\s*$",
            stripped,
            re.IGNORECASE,
        )
        if header_match:
            if current_section:
                sections[current_section] = "\n".join(current_content).strip()
            sec_name = header_match.group(1).title()
            if sec_name.lower() == "scope":
                sec_name = "Bounded Scope"
            current_section = sec_name
            current_content = []
        elif current_section is not None:
            current_content.append(line)

    if current_section and current_content:
        sections[current_section] = "\n".join(current_content).strip()

    return sections


def validate_dispatch_candidate(
    body: str,
    labels: list[str] | None = None,
    allow_comment_trigger: bool = False,
) -> dict[str, Any]:
    """Validate issue body and labels for Jules cloud dispatch.

    Returns a dict with 'valid' (bool), 'reasons' (list[str]), and 'sections' (dict).
    """
    reasons: list[str] = []
    labels_set = {b.lower().strip() for b in (labels or [])}

    # Label validation
    if not allow_comment_trigger:
        has_valid_label = bool(labels_set.intersection(VALID_LABELS))
        if not has_valid_label:
            reasons.append(f"Issue lacks required label ({', '.join(sorted(VALID_LABELS))})")

    # Excluded label check
    blocking_labels = labels_set.intersection(EXCLUDED_LABELS)
    if blocking_labels:
        reasons.append(f"Issue carries blocking label(s): {', '.join(sorted(blocking_labels))}")

    sections = parse_issue_sections(body)

    # Section completeness checks
    objective = sections.get("Objective", "").strip()
    if not objective:
        reasons.append("Missing or empty required section: Objective")

    criteria = sections.get("Acceptance Criteria", "").strip()
    if not criteria:
        reasons.append("Missing or empty required section: Acceptance Criteria")

    bounded_scope = sections.get("Bounded Scope", "").strip()
    if not bounded_scope:
        reasons.append("Missing or empty required section: Bounded Scope")
    elif "unbounded" in bounded_scope.lower() or "entire repo" in bounded_scope.lower():
        reasons.append("Bounded Scope explicitly indicates unbounded work")

    valid = len(reasons) == 0
    return {
        "valid": valid,
        "reasons": reasons,
        "sections": {
            "objective": objective,
            "acceptance_criteria": criteria,
            "bounded_scope": bounded_scope,
        },
    }


def main() -> int:
    """CLI entrypoint for issue dispatch validation."""
    parser = argparse.ArgumentParser(description="Validate GitHub issue payload for Jules dispatch")
    parser.add_argument("--body", help="Issue body string")
    parser.add_argument("--body-file", help="Path to file containing issue body")
    parser.add_argument(
        "--labels",
        help="Comma-separated labels associated with the issue",
        default="",
    )
    parser.add_argument(
        "--allow-comment-trigger",
        action="store_true",
        help="Allow dispatch triggered by issue comment",
    )

    args = parser.parse_args()

    body = args.body or ""
    if args.body_file:
        with open(args.body_file, encoding="utf-8") as f:
            body = f.read()
    elif not body and not sys.stdin.isatty():
        body = sys.stdin.read()

    labels_list = [lbl.strip() for lbl in args.labels.split(",") if lbl.strip()]

    result = validate_dispatch_candidate(
        body=body,
        labels=labels_list,
        allow_comment_trigger=args.allow_comment_trigger,
    )

    print(json.dumps(result, indent=2))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    sys.exit(main())
