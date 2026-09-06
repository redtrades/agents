"""Unit tests for tools/jules_dispatch.py."""

from __future__ import annotations

import unittest
from unittest.mock import patch

from tools.jules_dispatch import (
    main,
    parse_issue_sections,
    validate_dispatch_candidate,
)

SAMPLE_VALID_BODY = """
## Objective
Refactor authentication module to use JWT tokens.

## Acceptance Criteria
- All tests in test_auth.py pass.
- No plain text passwords stored.

## Bounded Scope
`src/auth/jwt.py`, `tests/test_auth.py`
"""

SAMPLE_UNBOUNDED_BODY = """
# Objective
Fix all bugs across the entire repo.

# Acceptance Criteria
- Repo is clean.

# Bounded Scope
Unbounded maintenance task across the entire repo.
"""


class TestJulesDispatch(unittest.TestCase):
    def test_parse_issue_sections_valid(self):
        sections = parse_issue_sections(SAMPLE_VALID_BODY)
        self.assertIn("Objective", sections)
        self.assertIn("Acceptance Criteria", sections)
        self.assertIn("Bounded Scope", sections)
        self.assertEqual(sections["Objective"], "Refactor authentication module to use JWT tokens.")

    def test_parse_issue_sections_empty(self):
        sections = parse_issue_sections("")
        self.assertEqual(sections, {})

    def test_validate_dispatch_candidate_valid_jules_label(self):
        res = validate_dispatch_candidate(SAMPLE_VALID_BODY, labels=["jules"])
        self.assertTrue(res["valid"])
        self.assertEqual(res["reasons"], [])
        self.assertEqual(
            res["sections"]["objective"],
            "Refactor authentication module to use JWT tokens.",
        )

    def test_validate_dispatch_candidate_valid_jules_cloud_label(self):
        res = validate_dispatch_candidate(SAMPLE_VALID_BODY, labels=["jules:cloud"])
        self.assertTrue(res["valid"])
        self.assertEqual(res["reasons"], [])

    def test_validate_dispatch_candidate_missing_label(self):
        res = validate_dispatch_candidate(SAMPLE_VALID_BODY, labels=["enhancement"])
        self.assertFalse(res["valid"])
        self.assertTrue(any("lacks required label" in r for r in res["reasons"]))

    def test_validate_dispatch_candidate_comment_trigger_without_label(self):
        res = validate_dispatch_candidate(
            SAMPLE_VALID_BODY, labels=["bug"], allow_comment_trigger=True
        )
        self.assertTrue(res["valid"])

    def test_validate_dispatch_candidate_blocking_label(self):
        res = validate_dispatch_candidate(SAMPLE_VALID_BODY, labels=["jules", "type:epic"])
        self.assertFalse(res["valid"])
        self.assertTrue(any("blocking label" in r for r in res["reasons"]))

    def test_validate_dispatch_candidate_missing_sections(self):
        incomplete_body = "## Objective\nJust an objective without criteria or scope."
        res = validate_dispatch_candidate(incomplete_body, labels=["jules"])
        self.assertFalse(res["valid"])
        self.assertTrue(any("Acceptance Criteria" in r for r in res["reasons"]))
        self.assertTrue(any("Bounded Scope" in r for r in res["reasons"]))

    def test_validate_dispatch_candidate_unbounded_scope(self):
        res = validate_dispatch_candidate(SAMPLE_UNBOUNDED_BODY, labels=["jules"])
        self.assertFalse(res["valid"])
        self.assertTrue(any("unbounded" in r.lower() for r in res["reasons"]))

    @patch("sys.argv", ["jules_dispatch.py", "--body", SAMPLE_VALID_BODY, "--labels", "jules"])
    def test_cli_main_success(self):
        with patch("sys.stdout"):
            exit_code = main()
            self.assertEqual(exit_code, 0)

    @patch("sys.argv", ["jules_dispatch.py", "--body", "invalid body", "--labels", "jules"])
    def test_cli_main_failure(self):
        with patch("sys.stdout"):
            exit_code = main()
            self.assertEqual(exit_code, 1)


if __name__ == "__main__":
    unittest.main()
