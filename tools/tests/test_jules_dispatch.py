"""Tests for tools/jules_dispatch.py."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest
from tools.jules_dispatch import (
    JulesDispatchError,
    extract_markdown_section,
    has_jules_label,
    parse_acceptance_criteria,
    parse_issue_payload,
    validate_and_build_packet,
)


def test_extract_markdown_section():
    content = (
        "## Overview\n"
        "Some introductory context.\n\n"
        "### Objective\n"
        "Build the cloud dispatch pipeline.\n\n"
        "### Acceptance Criteria\n"
        "1. Unit tests pass.\n"
        "2. Deterministic execution.\n\n"
        "### Next Steps\n"
        "Deploy to production.\n"
    )
    assert extract_markdown_section(content, "Objective") == "Build the cloud dispatch pipeline."
    assert "Unit tests pass." in extract_markdown_section(content, "Acceptance Criteria")
    assert extract_markdown_section(content, "NonExistent") == ""


def test_parse_acceptance_criteria_numbered():
    block = "1. First criterion.\n2. Second criterion with details.\n3. Third criterion.\n"
    items = parse_acceptance_criteria(block)
    assert len(items) == 3
    assert items[0] == "First criterion."
    assert items[1] == "Second criterion with details."
    assert items[2] == "Third criterion."


def test_parse_acceptance_criteria_bullets():
    block = "- Item A\n- Item B\n* Item C\n"
    items = parse_acceptance_criteria(block)
    assert len(items) == 3
    assert items == ("Item A", "Item B", "Item C")


def test_parse_acceptance_criteria_fallback():
    block = "All unit tests must pass without regressions."
    items = parse_acceptance_criteria(block)
    assert len(items) == 1
    assert items[0] == block


def test_has_jules_label():
    assert has_jules_label(["jules"]) is True
    assert has_jules_label(["jules:cloud"]) is True
    assert has_jules_label(["Jules", "area:swarm"]) is True
    assert has_jules_label(["JULES:CLOUD"]) is True
    assert has_jules_label(["bug", "enhancement"]) is False
    assert has_jules_label([]) is False


def test_validate_and_build_packet_success():
    body = (
        "### Objective\n"
        "Implement Jules async dispatch.\n\n"
        "### Acceptance Criteria\n"
        "1. Create dispatch script.\n"
        "2. Verify with test suite.\n"
    )
    packet = validate_and_build_packet(
        issue_number=42,
        title="feat: automated cloud task",
        body=body,
        repository="redtrades/agents",
        labels=["jules", "area:swarm-sdlc"],
    )
    assert packet.task_id == "jules-task-42"
    assert packet.issue_number == 42
    assert packet.branch_name == "jules/issue-42"
    assert packet.objective == "Implement Jules async dispatch."
    assert len(packet.acceptance_criteria) == 2
    assert packet.acceptance_criteria[0] == "Create dispatch script."
    assert "https://github.com/redtrades/agents/issues/42" in packet.target_url
    assert "## Operating Instructions" in packet.prompt


def test_validate_and_build_packet_missing_label():
    body = "### Objective\nTest.\n\n### Acceptance Criteria\n1. Done.\n"
    with pytest.raises(JulesDispatchError) as exc_info:
        validate_and_build_packet(
            issue_number=10,
            title="Some task",
            body=body,
            repository="redtrades/agents",
            labels=["bug"],
        )
    assert exc_info.value.code == "missing_jules_label"


def test_validate_and_build_packet_missing_objective():
    body = "### Background\nTest.\n\n### Acceptance Criteria\n1. Done.\n"
    with pytest.raises(JulesDispatchError) as exc_info:
        validate_and_build_packet(
            issue_number=10,
            title="Some task",
            body=body,
            repository="redtrades/agents",
            labels=["jules"],
        )
    assert exc_info.value.code == "missing_objective"


def test_validate_and_build_packet_missing_criteria():
    body = "### Objective\nBuild something.\n\n### Context\nNone.\n"
    with pytest.raises(JulesDispatchError) as exc_info:
        validate_and_build_packet(
            issue_number=10,
            title="Some task",
            body=body,
            repository="redtrades/agents",
            labels=["jules"],
        )
    assert exc_info.value.code == "missing_acceptance_criteria"


def test_validate_and_build_packet_unbounded_body():
    body = "### Objective\nLarge.\n\n### Acceptance Criteria\n1. Done.\n" + ("x" * 13000)
    with pytest.raises(JulesDispatchError) as exc_info:
        validate_and_build_packet(
            issue_number=10,
            title="Some task",
            body=body,
            repository="redtrades/agents",
            labels=["jules"],
        )
    assert exc_info.value.code == "unbounded_body"


def test_parse_issue_payload_dict():
    raw_payload = {
        "issue": {
            "number": 7,
            "title": "Autonomous refactor",
            "body": "### Objective\nRefactor adapters.\n\n### Acceptance Criteria\n- Prune old code\n- Pass tests",
            "html_url": "https://github.com/redtrades/agents/issues/7",
            "labels": [{"name": "jules:cloud"}, {"name": "enhancement"}],
        },
        "repository": {"full_name": "redtrades/agents"},
    }
    packet = parse_issue_payload(raw_payload)
    assert packet.issue_number == 7
    assert packet.branch_name == "jules/issue-7"
    assert len(packet.acceptance_criteria) == 2


def test_cli_validate_stdin(tmp_path: Path):
    payload = {
        "number": 99,
        "title": "CLI Test Task",
        "body": "### Objective\nVerify CLI.\n\n### Acceptance Criteria\n1. Run validate command.\n",
        "html_url": "https://github.com/redtrades/agents/issues/99",
        "labels": ["jules"],
    }
    proc = subprocess.run(
        [sys.executable, "tools/jules_dispatch.py", "validate", "--format-packet"],
        input=json.dumps(payload),
        text=True,
        capture_output=True,
        check=True,
    )
    result = json.loads(proc.stdout)
    assert result["task_id"] == "jules-task-99"
    assert result["branch_name"] == "jules/issue-99"
