"""Tests for tools/canary_runner.py."""

from __future__ import annotations

import json
import subprocess
import sys

from tools.canary_runner import (
    ALL_HARNESSES,
    probe_harness,
    run_canary_suite,
)


def test_all_harnesses_tuple():
    assert len(ALL_HARNESSES) == 5
    assert "claude" in ALL_HARNESSES
    assert "hermes" in ALL_HARNESSES


def test_probe_harness_missing():
    res = probe_harness("non_existent_binary_xyz_123")
    assert res.installed is False
    assert res.status == "SKIPPED"
    assert res.exit_code == -1


def test_probe_harness_installed():
    res = probe_harness("claude")
    if res.installed:
        assert res.status == "PASS"
        assert res.exit_code == 0
        assert res.duration_ms >= 0


def test_run_canary_suite_custom_harnesses():
    receipt = run_canary_suite(["claude", "hermes"])
    assert receipt.harnesses_tested == 2
    assert len(receipt.results) == 2
    assert receipt.overall_status in {"PASS", "FAIL"}


def test_cli_canary_json():
    proc = subprocess.run(
        [sys.executable, "tools/canary_runner.py", "--harnesses", "claude,hermes", "--json"],
        capture_output=True,
        text=True,
        check=True,
    )
    data = json.loads(proc.stdout)
    assert data["harnesses_tested"] == 2
    assert "overall_status" in data
    assert "results" in data
    assert len(data["results"]) == 2
