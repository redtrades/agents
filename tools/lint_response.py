#!/usr/bin/env python3
"""Deterministic response linter enforcing AGENTS.md and rules/communication.md.

Usage:
    python3 tools/lint_response.py <file>
    python3 tools/lint_response.py --text "some text to check"
    echo "some text" | python3 tools/lint_response.py
"""

import argparse
import sys

BANNED_CHARACTERS = [
    ("\u2014", "Em dash (use single hyphen, colon, or parentheses)"),
    ("\u2013", "En dash (use single hyphen, colon, or parentheses)"),
    (";", "Semicolon (banned under rules/communication.md Section 7)"),
]

BANNED_PHRASES = [
    "load-bearing",
    "worth stating plainly",
    "here's the honest truth",
    "the real tension",
    "carry the argument",
]

BANNED_OPENINGS = [
    "sure thing",
    "happy to help",
    "certainly",
    "of course",
    "great question",
    "i understand your",
]


def lint_text(text: str) -> list[str]:
    errors = []
    lines = text.splitlines()

    # Check banned openings on first non-empty line
    for line in lines:
        stripped = line.strip().lower()
        if stripped:
            for opening in BANNED_OPENINGS:
                if stripped.startswith(opening):
                    errors.append(f"Line 1: Banned conversational opening '{opening}'")
            break

    # Line-by-line checks
    for idx, line in enumerate(lines, start=1):
        for char, reason in BANNED_CHARACTERS:
            if char in line:
                col = line.find(char) + 1
                errors.append(f"Line {idx}:{col}: Banned character '{char}' -> {reason}")

        line_lower = line.lower()
        for phrase in BANNED_PHRASES:
            if phrase in line_lower:
                col = line_lower.find(phrase) + 1
                errors.append(f"Line {idx}:{col}: Banned exact phrase '{phrase}'")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Lint response against constitution rules.")
    parser.add_argument("file", nargs="?", help="File to lint")
    parser.add_argument("--text", help="Direct text string to lint")
    args = parser.parse_args()

    if args.text:
        content = args.text
    elif args.file:
        with open(args.file, encoding="utf-8") as f:
            content = f.read()
    elif not sys.stdin.isatty():
        content = sys.stdin.read()
    else:
        parser.print_help()
        return 1

    errors = lint_text(content)
    if errors:
        print(f"FAIL: {len(errors)} violation(s) detected:")
        for err in errors:
            print(f"  - {err}")
        return 1

    print("PASS: Response satisfies all constitution syntax and anti-slop rules.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
