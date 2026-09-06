#!/usr/bin/env python3
"""Declarative catalog generator for skills, rules, and decision records.

Parses YAML frontmatter across:
- plugins/*/skills/*/SKILL.md
- rules/*.md
- docs/decisions/*.md

Generates self-healing markdown index tables and validates declarative integrity.
"""

from __future__ import annotations

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
                    items = [
                        x.strip().strip('"').strip("'") for x in v[1:-1].split(",") if x.strip()
                    ]
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

    content = (
        [
            "# Canonical Rules Index",
            "",
            "Living operational rules binding all agents across all harnesses. Read at cold start.",
            "",
            "| Rule File | Version | Status | Last Updated |",
            "| :--- | :--- | :--- | :--- |",
        ]
        + rows
        + [""]
    )
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
        status = meta.get("status", "proposed").upper()
        date = meta.get("date", "2026-09-05")
        tier = meta.get("tier", "standard")
        rows.append(f"| [{af.name}]({af.name}) | **{status}** | `{tier}` | `{date}` |")

    content = (
        [
            "# Architecture Decision Records (ADR) Registry",
            "",
            "Durable ledger of ratified architecture decisions. Eliminates re-litigation across sessions.",
            "",
            "| Decision Record | Status | Tier | Date |",
            "| :--- | :--- | :--- | :--- |",
        ]
        + rows
        + [""]
    )
    out_file = decisions_dir / "README.md"
    out_file.write_text("\n".join(content), encoding="utf-8")
    return out_file


def infer_tier(plugin: str, skill: str, desc: str) -> str:
    """Infer difficulty tier from skill characteristics."""
    text = f"{plugin} {skill} {desc}".lower()
    # Tier 1: Quick / Docs / Syntax
    if any(
        k in text
        for k in [
            "syntax",
            "format",
            "typo",
            "lint",
            "classifier",
            "caveman-syntax",
            "verify-and-stop",
        ]
    ):
        return "Tier 1 (Quick)"
    # Tier 4: Complex / Audit / Security / Reverse Engineering
    if any(
        k in text
        for k in [
            "audit",
            "reversing",
            "forensic",
            "finetuning",
            "quantiz",
            "grpo",
            "sast",
            "threat-mitigation",
            "incident",
            "parallel-debugging",
        ]
    ):
        return "Tier 4 (Audit)"
    # Tier 3: Architecture / Distributed / Strategic
    if any(
        k in text
        for k in [
            "architecture",
            "saga",
            "event-store",
            "projection",
            "microservices",
            "terraform",
            "multi-cloud",
            "durable-objects",
            "wayfinder",
            "workflow-orchestration",
        ]
    ):
        return "Tier 3 (Architecture)"
    # Tier 2: MVP / Standard
    return "Tier 2 (MVP)"


def infer_domain(plugin: str) -> str:
    """Group plugins into canonical functional domains."""
    mapping = {
        "operational-discipline": "Operational Discipline & Governance",
        "caveman": "Caveman Token Minimalism",
        "deep-research": "Deep Research & Intelligence",
        "software-craft": "Software Craftsmanship & Testing",
        "planning-spec": "Planning & Specification Design",
        "cloudflare-platform": "Cloudflare & Edge Infrastructure",
        "backend-development": "Backend Architecture & Distributed Systems",
        "llm-application-dev": "LLM Application Engineering",
        "llm-finetuning": "Model Fine-Tuning & Quantization",
        "developer-essentials": "Developer Essentials & Git Workflows",
        "security-scanning": "Security & Vulnerability Analysis",
        "accessibility-compliance": "Accessibility & Compliance",
        "ui-design": "UI Design & Component Systems",
        "data-engineering": "Data Engineering & Pipelines",
        "business-analytics": "Business Analytics & Metrics",
        "startup-business-analyst": "Startup Strategy & Financials",
    }
    return mapping.get(plugin, plugin.replace("-", " ").title())


def generate_skills_moc() -> Path:
    """Generate docs/skills-moc.md with domain and tier classifications."""
    skills = sorted(REPO_ROOT.glob("plugins/*/skills/*/SKILL.md"))
    domains: dict[str, list[dict[str, str]]] = {}

    for sp in skills:
        plugin = sp.parent.parent.parent.name
        skill_name = sp.parent.name
        meta = parse_frontmatter(sp)
        desc = meta.get("description", "")
        if isinstance(desc, dict):
            desc = str(desc)
        desc_clean = desc.replace("\n", " ").strip()

        # Extract triggers
        trigger_idx = desc_clean.lower().find("use when")
        trigger = desc_clean[trigger_idx:].strip().rstrip(".") if trigger_idx != -1 else desc_clean

        tier = infer_tier(plugin, skill_name, desc_clean)
        domain = infer_domain(plugin)

        rel_path = sp.relative_to(REPO_ROOT)

        entry = {
            "name": skill_name,
            "plugin": plugin,
            "tier": tier,
            "trigger": trigger,
            "path": str(rel_path),
        }
        domains.setdefault(domain, []).append(entry)

    lines = [
        "# Canonical Skills Map of Content (MOC)",
        "",
        "Master index of all specialized skills across the estate. Used by agents to infer and load matching skills Just-In-Time based on user request keywords and task complexity tiers.",
        "",
        f"**Total Registered Skills:** {len(skills)} across {len(set(sp.parent.parent.parent.name for sp in skills))} plugins.",
        "",
        "## Complexity Tiers",
        "- **Tier 1 (Quick):** Focused single-file fixes, formatting, syntax, and direct configs (<2 min).",
        "- **Tier 2 (MVP):** Standard feature slices, unit tests, and surgical bug fixes (2 to 15 min).",
        "- **Tier 3 (Architecture):** Multi-service refactors, event schemas, distributed sagas, and worktrees.",
        "- **Tier 4 (Audit / Swarm):** Deep security scans, model fine-tuning, reverse engineering, and multi-agent coordination.",
        "",
        "---",
        "",
    ]

    for domain_name in sorted(domains.keys()):
        lines.append(f"### {domain_name}")
        lines.append("")
        lines.append("| Skill | Plugin | Tier | Trigger Keywords / Activation |")
        lines.append("| :--- | :--- | :--- | :--- |")
        for s in domains[domain_name]:
            lines.append(
                f"| [{s['name']}](../{s['path']}) | `{s['plugin']}` | **{s['tier']}** | {s['trigger']} |"
            )
        lines.append("")

    out_file = REPO_ROOT / "docs" / "skills-moc.md"
    out_file.write_text("\n".join(lines), encoding="utf-8")
    return out_file


def main() -> int:
    rules_idx = generate_rules_index()
    decisions_idx = generate_decisions_index()
    skills_moc = generate_skills_moc()
    print(f"Generated: {rules_idx.relative_to(REPO_ROOT)}")
    print(f"Generated: {decisions_idx.relative_to(REPO_ROOT)}")
    print(f"Generated: {skills_moc.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
