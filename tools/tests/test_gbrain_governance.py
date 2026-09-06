"""Tests for GBrain memory grounding and governance rules."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock

from tools.compile_context import compile_all_contexts, find_gbrain_bin, run_compile_target
from tools.gbrain_mcp import LEAN_TOOLS, calculate_token_overhead


def test_gbrain_mcp_token_overhead():
    """Verify GBrain MCP tool schema stays well under 800-token ceiling."""
    overhead = calculate_token_overhead(LEAN_TOOLS)
    assert overhead <= 800
    assert overhead == 286


def test_operational_skills_contain_gbrain_directive():
    """Verify all core operational skills mandate GBrain memory grounding."""
    skills_to_check = [
        "plugins/deep-research/skills/research/SKILL.md",
        "plugins/deep-research/skills/wayfinder/SKILL.md",
        "plugins/operational-discipline/skills/investigate-first/SKILL.md",
        "plugins/operational-discipline/skills/operating-discipline/SKILL.md",
        "plugins/planning-spec/skills/writing-plans/SKILL.md",
        "plugins/software-craft/skills/diagnosing-bugs/SKILL.md",
        "plugins/context-management/skills/gbrain-memory/SKILL.md",
    ]
    repo_root = Path(__file__).resolve().parent.parent.parent
    for skill_rel in skills_to_check:
        skill_file = repo_root / skill_rel
        assert skill_file.exists(), f"Skill file {skill_rel} must exist"
        content = skill_file.read_text(encoding="utf-8")
        assert (
            "gbrain" in content.lower()
        ), f"Skill {skill_rel} must mandate GBrain grounding"


def test_repo_mcp_json_configured():
    """Verify repository root .mcp.json configures GBrain lean proxy."""
    repo_root = Path(__file__).resolve().parent.parent.parent
    mcp_json = repo_root / ".mcp.json"
    assert mcp_json.exists(), ".mcp.json must exist in repo root"
    data = json.loads(mcp_json.read_text(encoding="utf-8"))
    assert "mcpServers" in data
    assert "gbrain" in data["mcpServers"]
    gbrain_conf = data["mcpServers"]["gbrain"]
    assert "gbrain_mcp.py" in gbrain_conf.get("args", [""])[0]


def test_compile_context_runner_mock(monkeypatch, tmp_path: Path):
    """Verify run_compile_target handles commands and failures gracefully."""
    import subprocess

    mock_res = MagicMock(returncode=0, stdout="compile-context: up to date\n")
    monkeypatch.setattr(subprocess, "run", MagicMock(return_value=mock_res))

    code, out = run_compile_target(
        gbrain_path="/usr/local/bin/gbrain",
        target="claude-code",
        budget=1000,
        out_path=tmp_path / "context.md",
        check=True,
    )
    assert code == 0
    assert "up to date" in out


def test_compile_all_contexts_missing_binary(monkeypatch, tmp_path: Path):
    """Verify compile_all_contexts gracefully degrades when gbrain binary missing."""
    monkeypatch.setattr("tools.compile_context.find_gbrain_bin", lambda: None)
    ret = compile_all_contexts(repo_root=tmp_path)
    assert ret == 0
