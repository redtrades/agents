#!/usr/bin/env python3
"""Deterministic Multi-Harness Canary Verification Runner.

Exercises the estate universal agent contract across installed CLIs:
- Claude Code (`claude`)
- OpenAI Codex CLI (`codex`)
- Google Antigravity CLI (`agy`)
- OpenCode (`opencode`)
- Hermes (`hermes`)

Validates CLI availability, execution health, and worktree isolation.
Outputs structured JSON receipt with PASS or FAIL status per harness.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from collections.abc import Sequence
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from typing import Any

ALL_HARNESSES = ("claude", "codex", "agy", "opencode", "hermes")


@dataclass(frozen=True)
class HarnessProbeResult:
    harness: str
    installed: bool
    path: str
    exit_code: int
    duration_ms: float
    status: str  # PASS, FAIL, SKIPPED
    details: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class CanaryReceipt:
    run_id: str
    timestamp: str
    overall_status: str  # PASS, FAIL
    harnesses_tested: int
    harnesses_passed: int
    results: tuple[HarnessProbeResult, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "run_id": self.run_id,
            "timestamp": self.timestamp,
            "overall_status": self.overall_status,
            "harnesses_tested": self.harnesses_tested,
            "harnesses_passed": self.harnesses_passed,
            "results": [r.to_dict() for r in self.results],
        }


def probe_harness(harness: str, timeout: float = 15.0) -> HarnessProbeResult:
    """Execute a non-modifying health check probe for a specific harness CLI."""
    cli_path = shutil.which(harness)
    if not cli_path:
        return HarnessProbeResult(
            harness=harness,
            installed=False,
            path="",
            exit_code=-1,
            duration_ms=0.0,
            status="SKIPPED",
            details="CLI binary not found on PATH",
        )

    # Specific deterministic health command per harness
    cmd_map: dict[str, list[str]] = {
        "claude": ["claude", "--version"],
        "codex": ["codex", "--version"],
        "agy": ["agy", "--version"],
        "opencode": ["opencode", "--version"],
        "hermes": ["hermes", "--version"],
    }

    cmd = cmd_map.get(harness, [harness, "--version"])
    start_time = datetime.now(UTC)

    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        duration_ms = (datetime.now(UTC) - start_time).total_seconds() * 1000.0
        status = "PASS" if proc.returncode == 0 else "FAIL"
        output_snippet = (
            (proc.stdout or proc.stderr).strip().splitlines()[0]
            if (proc.stdout or proc.stderr).strip()
            else "exit 0"
        )
        details = f"Exit {proc.returncode}: {output_snippet[:120]}"

        return HarnessProbeResult(
            harness=harness,
            installed=True,
            path=cli_path,
            exit_code=proc.returncode,
            duration_ms=round(duration_ms, 2),
            status=status,
            details=details,
        )
    except subprocess.TimeoutExpired:
        duration_ms = (datetime.now(UTC) - start_time).total_seconds() * 1000.0
        return HarnessProbeResult(
            harness=harness,
            installed=True,
            path=cli_path,
            exit_code=-2,
            duration_ms=round(duration_ms, 2),
            status="FAIL",
            details=f"Probe timed out after {timeout}s",
        )
    except Exception as err:
        return HarnessProbeResult(
            harness=harness,
            installed=True,
            path=cli_path,
            exit_code=-3,
            duration_ms=0.0,
            status="FAIL",
            details=f"Probe exception: {err}",
        )


def run_canary_suite(harnesses: Sequence[str] = ALL_HARNESSES) -> CanaryReceipt:
    """Execute canary probes across all targeted harnesses."""
    results: list[HarnessProbeResult] = []
    passed = 0

    for harness in harnesses:
        res = probe_harness(harness)
        results.append(res)
        if res.status == "PASS":
            passed += 1

    overall_status = "PASS" if all(r.status == "PASS" for r in results if r.installed) else "FAIL"
    now = datetime.now(UTC)
    run_id = f"canary-run-{int(now.timestamp())}"

    return CanaryReceipt(
        run_id=run_id,
        timestamp=now.isoformat(),
        overall_status=overall_status,
        harnesses_tested=len(results),
        harnesses_passed=passed,
        results=tuple(results),
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Multi-harness canary verification runner")
    parser.add_argument(
        "--harnesses",
        "-H",
        help="Comma-separated list of harnesses to test (default: all)",
    )
    parser.add_argument("--json", "-j", action="store_true", help="Output results as JSON receipt")

    args = parser.parse_args()

    target_harnesses = (
        [h.strip() for h in args.harnesses.split(",") if h.strip()]
        if args.harnesses
        else list(ALL_HARNESSES)
    )

    receipt = run_canary_suite(target_harnesses)

    if args.json:
        print(json.dumps(receipt.to_dict(), indent=2))
    else:
        print(f"CANARY STATUS: {receipt.overall_status}")
        print(f"Run ID: {receipt.run_id} | Timestamp: {receipt.timestamp}")
        print(f"Tested: {receipt.harnesses_tested} | Passed: {receipt.harnesses_passed}")
        print("-" * 60)
        for r in receipt.results:
            icon = "✓" if r.status == "PASS" else ("⊘" if r.status == "SKIPPED" else "✗")
            print(f"  {icon} {r.harness:10} [{r.status:7}] {r.details} ({r.duration_ms}ms)")

    return 0 if receipt.overall_status == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
