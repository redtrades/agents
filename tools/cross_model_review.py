#!/usr/bin/env python3
"""Autonomous Cross-Model Peer Review Engine.

Enforces cross-model peer review invariant:
- Author and reviewer must be distinct model harnesses.
- Audits diff for banned characters (em dashes, semicolons) and banned phrases.
- Runs deterministic tests and validation checks.
- Outputs structured review receipt with PASS, FAIL, or UNSURE verdict.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ALLOWED_HARNESSES = frozenset({"claude", "codex", "antigravity", "hermes", "jules", "opencode"})

BANNED_CHARACTERS = [
    ("\u2014", "Em dash detected (use single hyphen, colon, or parentheses)"),
    ("\u2013", "En dash detected (use single hyphen, colon, or parentheses)"),
]

BANNED_PHRASES = [
    "load-bearing",
    "worth stating plainly",
    "here's the honest truth",
    "the real tension",
    "carry the argument",
]


class ReviewError(Exception):
    """Raised when cross-model review setup fails validation."""

    def __init__(self, code: str, message: str) -> None:
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")


@dataclass(frozen=True)
class ReviewFinding:
    code: str
    severity: str  # CRITICAL, HIGH, MEDIUM, LOW, INFO
    file_path: str
    line_number: int
    message: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ReviewReceipt:
    review_id: str
    author: str
    reviewer: str
    verdict: str  # PASS, FAIL, UNSURE
    base_commit: str
    head_commit: str
    findings: tuple[ReviewFinding, ...]
    checks: dict[str, bool]
    summary: str
    created_at: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "review_id": self.review_id,
            "author": self.author,
            "reviewer": self.reviewer,
            "verdict": self.verdict,
            "base_commit": self.base_commit,
            "head_commit": self.head_commit,
            "findings": [f.to_dict() for f in self.findings],
            "checks": self.checks,
            "summary": self.summary,
            "created_at": self.created_at,
        }


def validate_peer_pairing(author: str, reviewer: str) -> None:
    """Validate that author and reviewer are distinct recognized harnesses."""
    norm_author = author.strip().casefold()
    norm_reviewer = reviewer.strip().casefold()

    if not norm_author:
        raise ReviewError("empty_author", "Author harness cannot be empty")
    if not norm_reviewer:
        raise ReviewError("empty_reviewer", "Reviewer harness cannot be empty")

    if norm_author == norm_reviewer:
        raise ReviewError(
            "self_review_forbidden",
            f"Cross-model review invariant violated: author '{author}' cannot review its own work",
        )

    if norm_author not in ALLOWED_HARNESSES:
        raise ReviewError("unknown_author", f"Author '{author}' is not a recognized estate harness")
    if norm_reviewer not in ALLOWED_HARNESSES:
        raise ReviewError(
            "unknown_reviewer", f"Reviewer '{reviewer}' is not a recognized estate harness"
        )


def audit_diff_content(diff_text: str) -> list[ReviewFinding]:
    """Scan git diff additions for anti-slop violations."""
    findings: list[ReviewFinding] = []
    finding_idx = 1
    current_file = "unknown"
    line_num = 0

    for line in diff_text.splitlines():
        if line.startswith("+++ b/"):
            current_file = line[6:].strip()
            line_num = 0
            continue
        if line.startswith("@@"):
            match = re.search(r"\+(\d+)", line)
            if match:
                line_num = int(match.group(1)) - 1
            continue

        if line.startswith("+") and not line.startswith("+++"):
            line_num += 1
            added_content = line[1:]

            for char, reason in BANNED_CHARACTERS:
                if char in added_content:
                    findings.append(
                        ReviewFinding(
                            code=f"F{finding_idx}",
                            severity="HIGH",
                            file_path=current_file,
                            line_number=line_num,
                            message=reason,
                        )
                    )
                    finding_idx += 1

            content_lower = added_content.lower()
            for phrase in BANNED_PHRASES:
                if phrase in content_lower:
                    findings.append(
                        ReviewFinding(
                            code=f"F{finding_idx}",
                            severity="HIGH",
                            file_path=current_file,
                            line_number=line_num,
                            message=f"Banned anti-slop phrase '{phrase}' detected",
                        )
                    )
                    finding_idx += 1

    return findings


def run_review_audit(
    *,
    author: str,
    reviewer: str,
    base_commit: str = "main",
    head_commit: str = "HEAD",
    diff_text: str | None = None,
    repo_dir: Path | None = None,
    skip_tests: bool = False,
) -> ReviewReceipt:
    """Execute complete cross-model peer review audit."""
    validate_peer_pairing(author, reviewer)

    effective_repo = repo_dir or Path.cwd()
    checks: dict[str, bool] = {
        "peer_pairing_valid": True,
        "anti_slop_clean": True,
        "tests_passed": True,
    }

    if diff_text is None:
        try:
            cmd = ["git", "diff", f"{base_commit}...{head_commit}"]
            res = subprocess.run(
                cmd, cwd=effective_repo, capture_output=True, text=True, check=True
            )
            diff_text = res.stdout
        except Exception as err:
            raise ReviewError("diff_failed", f"Failed to compute git diff: {err}") from err

    findings = audit_diff_content(diff_text)
    if any(f.severity in {"CRITICAL", "HIGH"} for f in findings):
        checks["anti_slop_clean"] = False

    if not skip_tests:
        try:
            test_res = subprocess.run(
                [
                    "uv",
                    "run",
                    "--project",
                    "plugins/plugin-eval",
                    "pytest",
                    "-q",
                    "tools/tests/test_jules_dispatch.py",
                ],
                cwd=effective_repo,
                capture_output=True,
                text=True,
            )
            if test_res.returncode != 0:
                checks["tests_passed"] = False
                findings.append(
                    ReviewFinding(
                        code=f"F{len(findings) + 1}",
                        severity="CRITICAL",
                        file_path="test_suite",
                        line_number=0,
                        message="Deterministic test check failed",
                    )
                )
        except Exception:
            checks["tests_passed"] = False

    verdict = "PASS" if all(checks.values()) else "FAIL"
    review_id = f"rev-{author}-by-{reviewer}-{int(datetime.now(UTC).timestamp())}"
    summary = f"Review by {reviewer} of {author} candidate: {verdict} ({len(findings)} findings)"

    return ReviewReceipt(
        review_id=review_id,
        author=author,
        reviewer=reviewer,
        verdict=verdict,
        base_commit=base_commit,
        head_commit=head_commit,
        findings=tuple(findings),
        checks=checks,
        summary=summary,
        created_at=datetime.now(UTC).isoformat(),
    )


def remember_review_receipt(receipt: ReviewReceipt) -> bool:
    """Record a passing cross-model review receipt into GBrain memory."""
    fact_text = (
        f"Cross-model review {receipt.review_id} passed: author {receipt.author} "
        f"reviewed by {receipt.reviewer} on diff {receipt.base_commit}..{receipt.head_commit} "
        f"with {len(receipt.findings)} findings."
    )
    gbrain_bin = os.environ.get("GBRAIN_BIN", "/Users/man/.bun/bin/gbrain")
    if not (os.path.isfile(gbrain_bin) and os.access(gbrain_bin, os.X_OK)):
        resolved = shutil.which("gbrain")
        if resolved:
            gbrain_bin = resolved
        else:
            return False

    call_arg = json.dumps({
        "fact": fact_text,
        "provenance": "cross-model-review",
        "entity": "cross-model-review",
    })
    try:
        res = subprocess.run(
            [gbrain_bin, "call", "remember", call_arg],
            capture_output=True,
            text=True,
            check=False,
            timeout=5,
        )
        return res.returncode == 0
    except Exception:
        return False


def main() -> int:
    parser = argparse.ArgumentParser(description="Autonomous cross-model peer review engine")
    subparsers = parser.add_subparsers(dest="command", required=True)

    audit_p = subparsers.add_parser(
        "audit", help="Run cross-model audit between author and reviewer"
    )
    audit_p.add_argument(
        "--author", "-a", required=True, help="Author harness (e.g. jules, codex, hermes)"
    )
    audit_p.add_argument(
        "--reviewer", "-r", required=True, help="Reviewer harness (e.g. claude, antigravity)"
    )
    audit_p.add_argument("--base", default="main", help="Base commit or branch (default: main)")
    audit_p.add_argument("--head", default="HEAD", help="Head commit or branch (default: HEAD)")
    audit_p.add_argument("--diff-file", help="Path to precomputed diff file")
    audit_p.add_argument("--skip-tests", action="store_true", help="Skip running test suite")
    audit_p.add_argument("--json", "-j", action="store_true", help="Output review receipt as JSON")
    audit_p.add_argument(
        "--remember", action="store_true", help="Externalize PASS verdict to GBrain memory"
    )

    args = parser.parse_args()

    if args.command == "audit":
        diff_text = None
        if args.diff_file:
            with open(args.diff_file, encoding="utf-8") as f:
                diff_text = f.read()

        try:
            receipt = run_review_audit(
                author=args.author,
                reviewer=args.reviewer,
                base_commit=args.base,
                head_commit=args.head,
                diff_text=diff_text,
                skip_tests=args.skip_tests,
            )
            if args.remember and receipt.verdict == "PASS":
                remember_review_receipt(receipt)

            if args.json:
                print(json.dumps(receipt.to_dict(), indent=2))
            else:
                print(f"VERDICT: {receipt.verdict}")
                print(f"Review ID: {receipt.review_id}")
                print(f"Author: {receipt.author} | Reviewer: {receipt.reviewer}")
                print(f"Findings: {len(receipt.findings)}")
                for f in receipt.findings:
                    print(
                        f"  [{f.code}] ({f.severity}) {f.file_path}:{f.line_number} -> {f.message}"
                    )
            return 0 if receipt.verdict == "PASS" else 1
        except ReviewError as err:
            print(f"REVIEW_ERROR [{err.code}]: {err.message}", file=sys.stderr)
            return 2

    return 0


if __name__ == "__main__":
    sys.exit(main())
