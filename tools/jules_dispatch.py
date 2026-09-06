#!/usr/bin/env python3
"""Jules Cloud Task Dispatcher and Validator.

Parses GitHub issues, validates required dispatch sections (Objective,
Acceptance Criteria), verifies label gating ('jules' or 'jules:cloud'),
and constructs deterministic task packets for cloud execution.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections.abc import Sequence
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from typing import Any

SAFE_TASK_ID = re.compile(r"^[A-Za-z0-9._:-]{1,128}$")
GITHUB_ISSUE_URL = re.compile(r"^https://github\.com/([^/\s]+/[^/\s]+)/issues/([1-9][0-9]*)$")
JULES_TRIGGER_LABELS = frozenset({"jules", "jules:cloud"})
MAX_BODY_LENGTH = 12000


class JulesDispatchError(Exception):
    """Raised when an issue fails Jules dispatch validation."""

    def __init__(self, code: str, message: str) -> None:
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")


@dataclass(frozen=True)
class JulesTaskPacket:
    task_id: str
    issue_number: int
    title: str
    repository: str
    target_url: str
    labels: tuple[str, ...]
    objective: str
    acceptance_criteria: tuple[str, ...]
    branch_name: str
    prompt: str
    created_at: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def extract_markdown_section(content: str, header: str) -> str:
    """Extract markdown section text under a header like '### Header' or '## Header'."""
    pattern = r"(?:^|\n)#{1,6}\s+" + re.escape(header) + r"\s*\n(.*?)(?=\n#{1,6}\s+|\Z)"
    match = re.search(pattern, content, flags=re.DOTALL | re.IGNORECASE)
    if not match:
        return ""
    return match.group(1).strip()


def parse_acceptance_criteria(criteria_block: str) -> tuple[str, ...]:
    """Parse numbered or bulleted list items from an acceptance criteria block."""
    lines = criteria_block.splitlines()
    items: list[str] = []
    current_item: list[str] = []

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        match = re.match(r"^(?:[0-9]+\.|\*|-)\s+(.*)$", stripped)
        if match:
            if current_item:
                items.append(" ".join(current_item))
                current_item = []
            current_item.append(match.group(1).strip())
        elif current_item:
            current_item.append(stripped)

    if current_item:
        items.append(" ".join(current_item))

    if not items and criteria_block.strip():
        items.append(criteria_block.strip())

    return tuple(items)


def has_jules_label(labels: Sequence[str]) -> bool:
    """Check if any label matches the Jules trigger set (case-insensitive)."""
    normalized = {lbl.strip().casefold() for lbl in labels if isinstance(lbl, str)}
    return bool(normalized & JULES_TRIGGER_LABELS)


def validate_and_build_packet(
    *,
    issue_number: int,
    title: str,
    body: str,
    repository: str,
    labels: Sequence[str],
    target_url: str = "",
) -> JulesTaskPacket:
    """Validate issue fields and produce an immutable Jules dispatch packet."""
    if not isinstance(title, str) or not title.strip():
        raise JulesDispatchError("empty_title", "Issue title cannot be empty")

    if not isinstance(body, str) or not body.strip():
        raise JulesDispatchError("empty_body", "Issue body cannot be empty")

    if len(body) > MAX_BODY_LENGTH:
        raise JulesDispatchError(
            "unbounded_body",
            f"Issue body exceeds maximum size of {MAX_BODY_LENGTH} characters",
        )

    if not has_jules_label(labels):
        raise JulesDispatchError(
            "missing_jules_label",
            "Issue lacks required Jules trigger label (must have 'jules' or 'jules:cloud')",
        )

    objective = extract_markdown_section(body, "Objective")
    if not objective:
        raise JulesDispatchError(
            "missing_objective",
            "Issue body missing required '### Objective' section",
        )

    criteria_text = extract_markdown_section(body, "Acceptance Criteria")
    if not criteria_text:
        raise JulesDispatchError(
            "missing_acceptance_criteria",
            "Issue body missing required '### Acceptance Criteria' section",
        )

    criteria = parse_acceptance_criteria(criteria_text)
    if not criteria:
        raise JulesDispatchError(
            "empty_acceptance_criteria",
            "Issue acceptance criteria list must contain at least one concrete item",
        )

    computed_url = target_url or f"https://github.com/{repository}/issues/{issue_number}"
    task_id = f"jules-task-{issue_number}"
    branch_name = f"jules/issue-{issue_number}"
    created_at = datetime.now(UTC).isoformat()

    prompt_lines = [
        f"# Task: {title.strip()} (Issue #{issue_number})",
        "",
        "## Objective",
        objective,
        "",
        "## Acceptance Criteria",
    ]
    for idx, item in enumerate(criteria, start=1):
        prompt_lines.append(f"{idx}. {item}")

    prompt_lines.extend(
        [
            "",
            "## Operating Instructions",
            "- Work in an isolated git branch.",
            "- Verify all changes deterministically before opening a pull request.",
            "- Adhere to anti-slop rules: zero em dashes and clean concise diffs.",
            f"- Target issue: {computed_url}",
        ]
    )

    prompt = "\n".join(prompt_lines)

    return JulesTaskPacket(
        task_id=task_id,
        issue_number=issue_number,
        title=title.strip(),
        repository=repository.strip(),
        target_url=computed_url,
        labels=tuple(labels),
        objective=objective,
        acceptance_criteria=criteria,
        branch_name=branch_name,
        prompt=prompt,
        created_at=created_at,
    )


def parse_issue_payload(data: dict[str, Any]) -> JulesTaskPacket:
    """Parse a GitHub issue JSON payload (from gh api or event webhook)."""
    issue_data = data.get("issue", data)
    issue_number = int(issue_data.get("number", 0))
    title = str(issue_data.get("title", ""))
    body = str(issue_data.get("body", ""))
    html_url = str(issue_data.get("html_url", ""))

    raw_labels = issue_data.get("labels", [])
    labels: list[str] = []
    for item in raw_labels:
        if isinstance(item, str):
            labels.append(item)
        elif isinstance(item, dict) and "name" in item:
            labels.append(str(item["name"]))

    repository = ""
    if "repository" in data and isinstance(data["repository"], dict):
        repository = data["repository"].get("full_name", "")
    elif html_url:
        match = GITHUB_ISSUE_URL.fullmatch(html_url)
        if match:
            repository = match.group(1)

    if not repository:
        repository = "redtrades/agents"

    return validate_and_build_packet(
        issue_number=issue_number,
        title=title,
        body=body,
        repository=repository,
        labels=labels,
        target_url=html_url,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Jules cloud task dispatcher and validator")
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate_p = subparsers.add_parser("validate", help="Validate issue payload from file or stdin")
    validate_p.add_argument(
        "--file", "-f", type=str, help="Path to issue JSON file (reads stdin if omitted)"
    )
    validate_p.add_argument(
        "--format-packet", action="store_true", help="Print structured dispatch packet JSON"
    )
    validate_p.add_argument(
        "--format-prompt", action="store_true", help="Print formatted Jules session prompt"
    )

    args = parser.parse_args()

    if args.command == "validate":
        if args.file:
            with open(args.file, encoding="utf-8") as f:
                raw = json.load(f)
        else:
            raw = json.load(sys.stdin)

        try:
            packet = parse_issue_payload(raw)
            if args.format_packet:
                print(json.dumps(packet.to_dict(), indent=2))
            elif args.format_prompt:
                print(packet.prompt)
            else:
                print(
                    f"VALID: Task {packet.task_id} ready for dispatch to branch {packet.branch_name}"
                )
            return 0
        except JulesDispatchError as err:
            print(f"DISPATCH_ERROR [{err.code}]: {err.message}", file=sys.stderr)
            return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
