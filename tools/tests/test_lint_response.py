"""Unit tests for response linter tool."""

from tools.lint_response import lint_text


def test_lint_clean_text():
    text = "Verdict: Everything passes cleanly (zero issues)."
    errors = lint_text(text)
    assert len(errors) == 0


def test_lint_detects_semicolon():
    text = "This is a test; it fails."
    errors = lint_text(text)
    assert len(errors) == 1
    assert "Semicolon" in errors[0]


def test_lint_detects_em_dash():
    text = "This is a test \u2014 it fails."
    errors = lint_text(text)
    assert len(errors) == 1
    assert "Em dash" in errors[0]


def test_lint_detects_banned_phrase():
    text = "This is a load-bearing component."
    errors = lint_text(text)
    assert len(errors) == 1
    assert "load-bearing" in errors[0]


def test_lint_detects_conversational_opening():
    text = "Certainly! I will execute this now."
    errors = lint_text(text)
    assert len(errors) == 1
    assert "banned conversational opening" in errors[0].lower()
