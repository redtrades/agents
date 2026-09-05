"""Tests for tools/worktree_manager.py."""

from __future__ import annotations

import subprocess
from pathlib import Path

from tools.worktree_manager import sanitize_task_id, get_active_worktrees, MAX_CONCURRENT_WORKTREES


def test_sanitize_task_id():
    assert sanitize_task_id("issue-1") == "issue-1"
    assert sanitize_task_id("task/20260905") == "task-20260905"
    assert sanitize_task_id("feat#42!") == "feat-42-"


def test_get_active_worktrees(tmp_path: Path):
    # Initialize a temporary git repository
    subprocess.run(["git", "init"], cwd=tmp_path, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=tmp_path, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=tmp_path, check=True, capture_output=True)
    
    # Create an initial commit
    dummy_file = tmp_path / "README.md"
    dummy_file.write_text("# Test")
    subprocess.run(["git", "add", "README.md"], cwd=tmp_path, check=True, capture_output=True)
    subprocess.run(["git", "commit", "-m", "initial commit"], cwd=tmp_path, check=True, capture_output=True)

    active = get_active_worktrees(tmp_path)
    assert len(active) == 1
    assert Path(active[0]["path"]).resolve() == tmp_path.resolve()
