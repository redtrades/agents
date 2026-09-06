#!/usr/bin/env python3
"""
GBrain Deterministic Context Compiler
Wraps `gbrain compile-context` to compile deterministic, sensitivity-scanned,
token-budgeted context files for Claude Code and generic agent harnesses.
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

GBRAIN_BIN = os.environ.get("GBRAIN_BIN", "/Users/man/.bun/bin/gbrain")
DEFAULT_CLAUDE_BUDGET = 1200
DEFAULT_GENERIC_BUDGET = 800


def find_gbrain_bin() -> str | None:
    """Resolve gbrain executable location."""
    if os.path.isfile(GBRAIN_BIN) and os.access(GBRAIN_BIN, os.X_OK):
        return GBRAIN_BIN
    resolved = shutil.which("gbrain")
    if resolved:
        return resolved
    return None


def run_compile_target(
    gbrain_path: str,
    target: str,
    budget: int,
    out_path: Path,
    check: bool = False,
) -> tuple[int, str]:
    """Compile or check a single context target."""
    cmd = [
        gbrain_path,
        "compile-context",
        "--target",
        target,
        "--budget",
        str(budget),
        "--out",
        str(out_path),
    ]
    if check:
        cmd.append("--check")

    try:
        proc = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            check=False,
        )
        return proc.returncode, proc.stdout
    except Exception as exc:
        return 2, f"Execution failed: {exc}"


def compile_all_contexts(
    repo_root: Path,
    check: bool = False,
    budget_claude: int = DEFAULT_CLAUDE_BUDGET,
    budget_generic: int = DEFAULT_GENERIC_BUDGET,
) -> int:
    """Compile or verify all configured context targets."""
    gbrain_path = find_gbrain_bin()
    if not gbrain_path:
        print("WARNING: gbrain binary not found on PATH. Skipping context compilation.")
        return 0

    claude_out = repo_root / ".claude" / "gbrain-context.md"
    claude_out.parent.mkdir(parents=True, exist_ok=True)

    generic_out = repo_root / ".gbrain" / "compiled-context.md"
    generic_out.parent.mkdir(parents=True, exist_ok=True)

    targets = [
        ("claude-code", budget_claude, claude_out),
        ("openclaw", budget_generic, generic_out),
    ]

    overall_code = 0
    for target_name, budget, out_path in targets:
        ret, output = run_compile_target(gbrain_path, target_name, budget, out_path, check=check)
        filtered_lines = [line for line in output.splitlines() if not line.startswith("UPGRADE_AVAILABLE")]
        clean_output = "\n".join(filtered_lines).strip()
        if clean_output:
            print(clean_output)

        if ret != 0:
            overall_code = ret

    return overall_code


def main() -> int:
    parser = argparse.ArgumentParser(description="Compile deterministic GBrain context files.")
    parser.add_argument("--check", action="store_true", help="Verify freshness against existing digests.")
    parser.add_argument("--repo-root", type=str, default=".", help="Target repository root.")
    parser.add_argument("--budget-claude", type=int, default=DEFAULT_CLAUDE_BUDGET, help="Token budget for Claude.")
    parser.add_argument("--budget-generic", type=int, default=DEFAULT_GENERIC_BUDGET, help="Token budget for generic.")

    args = parser.parse_args()
    repo_root = Path(args.repo_root).resolve()
    return compile_all_contexts(
        repo_root=repo_root,
        check=args.check,
        budget_claude=args.budget_claude,
        budget_generic=args.budget_generic,
    )


if __name__ == "__main__":
    sys.exit(main())
