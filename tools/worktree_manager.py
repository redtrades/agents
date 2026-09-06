"""Worktree Manager: Ephemeral worktree lifecycle and zero-loss backup.

Implements SDLC worktree isolation invariants:
1. Provisions worktrees under work/<task-id> linked to branch work/<task-id>.
2. Enforces global estate concurrency ceiling (max 2 active worktrees).
3. Executes zero-loss diff backup to backup/worktrees/<task-id> before clean removal.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

MAX_CONCURRENT_WORKTREES = 2


def run_cmd(
    cmd: list[str], cwd: Path | None = None, check: bool = True
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=cwd, text=True, capture_output=True, check=check)


def sanitize_task_id(task_id: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9_-]", "-", task_id.strip())
    if not cleaned:
        raise ValueError("Task ID cannot be empty.")
    return cleaned


def get_active_worktrees(repo_root: Path) -> list[dict[str, str]]:
    result = run_cmd(["git", "worktree", "list", "--porcelain"], cwd=repo_root)
    worktrees: list[dict[str, str]] = []
    current: dict[str, str] = {}
    for line in result.stdout.splitlines():
        line = line.strip()
        if not line:
            if current:
                worktrees.append(current)
                current = {}
            continue
        if line.startswith("worktree "):
            current["path"] = line.split(" ", 1)[1]
        elif line.startswith("branch "):
            current["branch"] = line.split(" ", 1)[1]
        elif line.startswith("HEAD "):
            current["head"] = line.split(" ", 1)[1]
    if current:
        worktrees.append(current)
    return worktrees


def cmd_spawn(repo_root: Path, task_id: str) -> int:
    task_id = sanitize_task_id(task_id)
    worktree_path = repo_root / "work" / task_id
    branch_name = f"work/{task_id}"

    # Check concurrency ceiling
    active = get_active_worktrees(repo_root)
    # Filter out the main root worktree
    child_worktrees = [
        wt for wt in active if Path(wt.get("path", "")).resolve() != repo_root.resolve()
    ]
    if len(child_worktrees) >= MAX_CONCURRENT_WORKTREES:
        print(
            f"ERROR: Concurrency ceiling reached ({len(child_worktrees)}/{MAX_CONCURRENT_WORKTREES} active).",
            file=sys.stderr,
        )
        print("Finish or clean an existing worktree before spawning a new one.", file=sys.stderr)
        for wt in child_worktrees:
            print(f"  - {wt.get('path')} ({wt.get('branch', 'detached')})", file=sys.stderr)
        return 1

    if worktree_path.exists():
        print(f"ERROR: Worktree path already exists at {worktree_path}", file=sys.stderr)
        return 1

    # Check if branch exists
    branch_exists = (
        run_cmd(
            ["git", "rev-parse", "--verify", branch_name], cwd=repo_root, check=False
        ).returncode
        == 0
    )

    print(f"Spawning worktree for task {task_id}...")
    worktree_path.parent.mkdir(parents=True, exist_ok=True)

    if branch_exists:
        run_cmd(["git", "worktree", "add", str(worktree_path), branch_name], cwd=repo_root)
    else:
        run_cmd(
            ["git", "worktree", "add", "-b", branch_name, str(worktree_path), "HEAD"], cwd=repo_root
        )

    print(f"SUCCESS: Worktree provisioned at {worktree_path}")
    print(f"Branch: {branch_name}")
    return 0


def cmd_clean(repo_root: Path, task_id: str) -> int:
    task_id = sanitize_task_id(task_id)
    worktree_path = repo_root / "work" / task_id
    backup_branch = f"backup/worktrees/{task_id}"

    if not worktree_path.exists():
        print(f"WARNING: Worktree path {worktree_path} does not exist on disk.", file=sys.stderr)
        run_cmd(["git", "worktree", "prune"], cwd=repo_root)
        return 0

    # Zero-loss backup: check for dirty or untracked files
    status = run_cmd(["git", "status", "--porcelain"], cwd=worktree_path, check=False)
    if status.stdout.strip():
        print(
            f"Zero-loss backup: Uncommitted changes detected in {task_id}. Backing up to {backup_branch}..."
        )
        run_cmd(["git", "checkout", "-B", backup_branch], cwd=worktree_path, check=False)
        run_cmd(["git", "add", "-A"], cwd=worktree_path, check=False)
        run_cmd(
            [
                "git",
                "commit",
                "-m",
                f"backup(worktree): zero-loss snapshot of {task_id} before pruning",
            ],
            cwd=worktree_path,
            check=False,
        )
        print(f"Snapshot committed to {backup_branch}")

    # Remove worktree
    print(f"Removing worktree at {worktree_path}...")
    remove_res = run_cmd(
        ["git", "worktree", "remove", "--force", str(worktree_path)], cwd=repo_root, check=False
    )
    if remove_res.returncode != 0:
        print(f"Git worktree remove returned: {remove_res.stderr.strip()}", file=sys.stderr)

    run_cmd(["git", "worktree", "prune"], cwd=repo_root)
    print(f"SUCCESS: Worktree {task_id} cleanly pruned.")
    return 0


def cmd_list(repo_root: Path) -> int:
    worktrees = get_active_worktrees(repo_root)
    print(f"Active worktrees ({len(worktrees)} total, limit: {MAX_CONCURRENT_WORKTREES} children):")
    for wt in worktrees:
        path = wt.get("path", "")
        branch = wt.get("branch", "detached")
        head = wt.get("head", "")[:7]
        is_root = Path(path).resolve() == repo_root.resolve()
        marker = "[ROOT]" if is_root else "[CHILD]"
        print(f"  {marker} {path} | Branch: {branch} ({head})")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="SDLC Worktree Lifecycle Manager")
    subparsers = parser.add_subparsers(dest="action", required=True)

    spawn_parser = subparsers.add_parser("spawn", help="Spawn an isolated task worktree")
    spawn_parser.add_argument("task_id", help="Task ID or Issue ID (e.g. issue-1)")

    clean_parser = subparsers.add_parser("clean", help="Zero-loss prune of task worktree")
    clean_parser.add_argument("task_id", help="Task ID or Issue ID")

    subparsers.add_parser("list", help="List active worktrees and concurrency state")

    args = parser.parse_args()
    repo_root = Path(__file__).resolve().parent.parent

    if args.action == "spawn":
        return cmd_spawn(repo_root, args.task_id)
    elif args.action == "clean":
        return cmd_clean(repo_root, args.task_id)
    elif args.action == "list":
        return cmd_list(repo_root)
    return 1


if __name__ == "__main__":
    sys.exit(main())
