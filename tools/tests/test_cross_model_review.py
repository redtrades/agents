"""Tests for tools/cross_model_review.py."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest
from tools.cross_model_review import (
    ReviewError,
    audit_diff_content,
    run_review_audit,
    validate_peer_pairing,
)


def test_validate_peer_pairing_valid():
    validate_peer_pairing("jules", "claude")
    validate_peer_pairing("codex", "antigravity")
    validate_peer_pairing("hermes", "jules")


def test_validate_peer_pairing_self_review():
    with pytest.raises(ReviewError) as exc_info:
        validate_peer_pairing("claude", "claude")
    assert exc_info.value.code == "self_review_forbidden"


def test_validate_peer_pairing_empty():
    with pytest.raises(ReviewError) as exc_info:
        validate_peer_pairing("", "claude")
    assert exc_info.value.code == "empty_author"

    with pytest.raises(ReviewError) as exc_info:
        validate_peer_pairing("jules", "")
    assert exc_info.value.code == "empty_reviewer"


def test_validate_peer_pairing_unknown():
    with pytest.raises(ReviewError) as exc_info:
        validate_peer_pairing("unknown_bot", "claude")
    assert exc_info.value.code == "unknown_author"


def test_audit_diff_content_clean():
    diff_text = (
        "--- a/file.py\n"
        "+++ b/file.py\n"
        "@@ -1,3 +1,4 @@\n"
        " def add(a: int, b: int) -> int:\n"
        "+    # Return sum of numbers\n"
        "     return a + b\n"
    )
    findings = audit_diff_content(diff_text)
    assert len(findings) == 0


def test_audit_diff_content_em_dash():
    diff_text = (
        "--- a/docs.md\n"
        "+++ b/docs.md\n"
        "@@ -10,3 +10,4 @@\n"
        "+This is a feature \u2014 with an em dash.\n"
    )
    findings = audit_diff_content(diff_text)
    assert len(findings) == 1
    assert findings[0].file_path == "docs.md"
    assert "Em dash" in findings[0].message


def test_audit_diff_content_banned_phrase():
    diff_text = (
        "--- a/plan.md\n"
        "+++ b/plan.md\n"
        "@@ -1,2 +1,3 @@\n"
        "+This is a load-bearing architecture component.\n"
    )
    findings = audit_diff_content(diff_text)
    assert len(findings) == 1
    assert "load-bearing" in findings[0].message


def test_run_review_audit_pass():
    clean_diff = "--- a/src/app.py\n+++ b/src/app.py\n@@ -1,2 +1,3 @@\n+# Clean addition\n"
    receipt = run_review_audit(
        author="jules",
        reviewer="claude",
        diff_text=clean_diff,
        skip_tests=True,
    )
    assert receipt.verdict == "PASS"
    assert receipt.author == "jules"
    assert receipt.reviewer == "claude"
    assert len(receipt.findings) == 0


def test_run_review_audit_fail_on_slop():
    slop_diff = (
        "--- a/src/app.py\n+++ b/src/app.py\n@@ -1,2 +1,3 @@\n+# Here is a \u2014 forbidden dash\n"
    )
    receipt = run_review_audit(
        author="codex",
        reviewer="antigravity",
        diff_text=slop_diff,
        skip_tests=True,
    )
    assert receipt.verdict == "FAIL"
    assert len(receipt.findings) == 1
    assert receipt.checks["anti_slop_clean"] is False


def test_cli_audit_json(tmp_path: Path):
    clean_diff_file = tmp_path / "diff.patch"
    clean_diff_file.write_text("--- a/test.txt\n+++ b/test.txt\n@@ -1 +1,2 @@\n+clean line\n")
    proc = subprocess.run(
        [
            sys.executable,
            "tools/cross_model_review.py",
            "audit",
            "--author",
            "hermes",
            "--reviewer",
            "jules",
            "--diff-file",
            str(clean_diff_file),
            "--skip-tests",
            "--json",
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    data = json.loads(proc.stdout)
    assert data["verdict"] == "PASS"
    assert data["author"] == "hermes"
    assert data["reviewer"] == "jules"
