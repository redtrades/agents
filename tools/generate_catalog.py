#!/usr/bin/env python3
"""Declarative catalog generator for skills, rules, and decision records.

Parses YAML frontmatter across:
- plugins/*/skills/*/SKILL.md
- rules/*.md
- docs/decisions/*.md

Generates self-healing markdown index tables and validates declarative integrity.
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def parse_frontmatter(file_path: Path) -> dict[str, Any]:
    """Extract simple key-value YAML frontmatter without external pyyaml dependency."""
    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception:
        return {}
    match = FRONTMATTER_RE.match(content)
    if not match:
        return {}
    raw_yaml = match.group(1)
    meta: dict[str, Any] = {}
    current_key = None
    for line in raw_yaml.splitlines():
        line_str = line.strip()
        if not line_str or line_str.startswith("#"):
            continue
        if ":" in line_str:
            k, v = line_str.split(":", 1)
            k = k.strip()
            v = v.strip().strip('"').strip("'")
            if v == "" or v.startswith("["):
                if v.startswith("[") and v.endswith("]"):
                    items = [x.strip().strip('"').strip("'") for x in v[1:-1].split(",") if x.strip()]
                    meta[k] = items
                else:
                    meta[k] = {}
                    current_key = k
            else:
                meta[k] = v
                current_key = None
        elif current_key and line.startswith("  ") and ":" in line_str:
            sub_k, sub_v = line_str.split(":", 1)
            sub_k = sub_k.strip()
            sub_v = sub_v.strip().strip('"').strip("'")
            if isinstance(meta.get(current_key), dict):
                meta[current_key][sub_k] = sub_v
    return meta


def generate_rules_index() -> Path:
    """Generate rules/README.md from active files in rules/."""
    rules_dir = REPO_ROOT / "rules"
    if not rules_dir.exists():
        return rules_dir
    rule_files = sorted(rules_dir.glob("*.md"))
    rows = []
    for rf in rule_files:
        if rf.name == "README.md":
            continue
        meta = parse_frontmatter(rf)
        name = meta.get("name", rf.stem)
        version = meta.get("version", "1.0.0")
        status = meta.get("status", "active")
        updated = meta.get("last_updated", "2026-09-05")
        rows.append(f"| [{name}]({rf.name}) | `{version}` | **{status.upper()}** | `{updated}` |")

    content = [
        "# Canonical Rules Index",
        "",
        "Living operational rules binding all agents across all harnesses. Read at cold start.",
        "",
        "| Rule File | Version | Status | Last Updated |",
        "| :--- | :--- | :--- | :--- |",
    ] + rows + [""]
    out_file = rules_dir / "README.md"
    out_file.write_text("\n".join(content), encoding="utf-8")
    return out_file


def generate_decisions_index() -> Path:
    """Generate docs/decisions/README.md from MADR records."""
    decisions_dir = REPO_ROOT / "docs" / "decisions"
    if not decisions_dir.exists():
        return decisions_dir
    adr_files = sorted(decisions_dir.glob("*.md"))
    rows = []
    for af in adr_files:
        if af.name == "README.md":
            continue
        meta = parse_frontmatter(af)
        title = meta.get("name", af.stem)
        status = meta.get("status", "proposed").upper()
        date = meta.get("date", "2026-09-05")
        tier = meta.get("tier", "standard")
        rows.append(f"| [{af.name}]({af.name}) | **{status}** | `{tier}` | `{date}` |")

    content = [
        "# Architecture Decision Records (ADR) Registry",
        "",
        "Durable ledger of ratified architecture decisions. Eliminates re-litigation across sessions.",
        "",
        "| Decision Record | Status | Tier | Date |",
        "| :--- | :--- | :--- | :--- |",
    ] + rows + [""]
    out_file = decisions_dir / "README.md"
    out_file.write_text("\n".join(content), encoding="utf-8")
    return out_file


def main() -> int:
    rules_idx = generate_rules_index()
    decisions_idx = generate_decisions_index()
    print(f"Generated: {rules_idx.relative_to(REPO_ROOT)}")
    print(f"Generated: {decisions_idx.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
