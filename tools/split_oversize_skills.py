#!/usr/bin/env python3
"""Refactor the 9 oversize skills into MOC SKILL.md (<8 KB) and references/details.md."""

from pathlib import Path
import re

REPO_ROOT = Path(__file__).resolve().parent.parent

def refactor_screen_reader_testing():
    p = REPO_ROOT / "plugins/accessibility-compliance/skills/screen-reader-testing"
    skill_file = p / "SKILL.md"
    content = skill_file.read_text()
    
    # Split before "## VoiceOver (macOS)"
    marker = "## VoiceOver (macOS)"
    idx = content.find(marker)
    if idx == -1:
        return
    head = content[:idx].rstrip()
    tail = content[idx:].lstrip()
    
    pointer = (
        "\n\n## Platform Testing Guides & Checklists\n\n"
        "Comprehensive guides for VoiceOver, NVDA, JAWS, and TalkBack, along with test scripts "
        "and checklists, live in `references/details.md`. Read that file when executing specific tests.\n"
    )
    
    new_skill = head + pointer
    refs_dir = p / "references"
    refs_dir.mkdir(parents=True, exist_ok=True)
    (refs_dir / "details.md").write_text("# Screen Reader Testing: Platform Guides & Checklists\n\n" + tail)
    skill_file.write_text(new_skill)
    print("Refactored screen-reader-testing:", len(new_skill.encode()))

def refactor_code_review_excellence():
    p = REPO_ROOT / "plugins/developer-essentials/skills/code-review-excellence"
    skill_file = p / "SKILL.md"
    content = skill_file.read_text()
    
    # Split before "## Review Techniques"
    marker = "## Review Techniques"
    idx = content.find(marker)
    if idx == -1:
        return
    head = content[:idx].rstrip()
    tail = content[idx:].lstrip()
    
    pointer = (
        "\n\n## Review Techniques, Checklists & Templates\n\n"
        "Detailed review checklists (security, performance, testing), language-specific patterns, "
        "and comment templates live in `references/details.md`. Read that file during thorough code reviews.\n"
    )
    
    new_skill = head + pointer
    refs_dir = p / "references"
    refs_dir.mkdir(parents=True, exist_ok=True)
    (refs_dir / "details.md").write_text("# Code Review Excellence: Detailed Checklists & Templates\n\n" + tail)
    skill_file.write_text(new_skill)
    print("Refactored code-review-excellence:", len(new_skill.encode()))

def refactor_debugging_strategies():
    p = REPO_ROOT / "plugins/developer-essentials/skills/debugging-strategies"
    skill_file = p / "SKILL.md"
    content = skill_file.read_text()
    
    # Split before "## Advanced Debugging Techniques"
    marker = "## Advanced Debugging Techniques"
    idx = content.find(marker)
    if idx == -1:
        return
    head = content[:idx].rstrip()
    tail = content[idx:].lstrip()
    
    pointer = (
        "\n\n## Advanced Techniques & Bug Patterns\n\n"
        "Detailed playbooks for flaky bugs, memory leaks, concurrency issues, production debugging, "
        "and checklists live in `references/details.md`. Read that file when performing root cause analysis.\n"
    )
    
    new_skill = head + pointer
    refs_dir = p / "references"
    refs_dir.mkdir(parents=True, exist_ok=True)
    (refs_dir / "details.md").write_text("# Debugging Strategies: Advanced Techniques & Playbooks\n\n" + tail)
    skill_file.write_text(new_skill)
    print("Refactored debugging-strategies:", len(new_skill.encode()))

def refactor_architecture_decision_records():
    p = REPO_ROOT / "plugins/documentation-generation/skills/architecture-decision-records"
    skill_file = p / "SKILL.md"
    content = skill_file.read_text()
    
    # Split before "## Templates"
    marker = "## Templates"
    idx = content.find(marker)
    if idx == -1:
        return
    head = content[:idx].rstrip()
    tail = content[idx:].lstrip()
    
    pointer = (
        "\n\n## ADR Templates & Review Checklists\n\n"
        "Complete markdown templates (MADR, Michael Nygard, Y-Statements, RFC style) and review checklists "
        "live in `references/details.md`. Read that file when authoring or reviewing an ADR.\n"
    )
    
    new_skill = head + pointer
    refs_dir = p / "references"
    refs_dir.mkdir(parents=True, exist_ok=True)
    (refs_dir / "details.md").write_text("# Architecture Decision Records: Templates & Checklists\n\n" + tail)
    skill_file.write_text(new_skill)
    print("Refactored architecture-decision-records:", len(new_skill.encode()))

def refactor_protocol_reverse_engineering():
    p = REPO_ROOT / "plugins/reverse-engineering/skills/protocol-reverse-engineering"
    skill_file = p / "SKILL.md"
    content = skill_file.read_text()
    
    # Split before "## Binary Protocol Analysis"
    marker = "## Binary Protocol Analysis"
    idx = content.find(marker)
    if idx == -1:
        return
    head = content[:idx].rstrip()
    tail = content[idx:].lstrip()
    
    # Ensure nav-tier section exists
    if "## When to Use" not in head and "## Overview" not in head:
        head = head.replace(
            "# Protocol Reverse Engineering\n",
            "# Protocol Reverse Engineering\n\n## Overview\n\nComprehensive techniques for capturing, analyzing, and documenting network protocols for security research, interoperability, and debugging.\n\n## When to Use\n\n- Analyzing network traffic and unknown protocols\n- Understanding proprietary protocols for interoperability\n- Debugging network communication issues\n"
        )
    
    pointer = (
        "\n\n## Binary Analysis, Encryption & Documentation Templates\n\n"
        "Detailed workflows for binary structure identification, entropy analysis, state machine mapping, "
        "and protocol documentation templates live in `references/details.md`.\n"
    )
    
    new_skill = head + pointer
    refs_dir = p / "references"
    refs_dir.mkdir(parents=True, exist_ok=True)
    (refs_dir / "details.md").write_text("# Protocol Reverse Engineering: Deep Analysis & Templates\n\n" + tail)
    skill_file.write_text(new_skill)
    print("Refactored protocol-reverse-engineering:", len(new_skill.encode()))

def refactor_scan():
    p = REPO_ROOT / "plugins/ship-mate/skills/scan"
    skill_file = p / "SKILL.md"
    content = skill_file.read_text()
    
    marker = "## Step 4A: Generate AGENTS.md"
    idx = content.find(marker)
    if idx == -1:
        return
    head = content[:idx].rstrip()
    tail = content[idx:].lstrip()
    
    if "## When to Use" not in head and "## Overview" not in head:
        head = head.replace(
            "# Codebase Scanner\n",
            "# Codebase Scanner\n\n## Overview\n\nAutomated scanner that inspects the project codebase and produces accurate project documentation and AGENTS.md instructions.\n\n## When to Use\n\n- Bootstrapping a new agent-driven repository\n- Refreshing project documentation after architectural changes\n- Running a delta scan to detect code drift\n"
        )
    
    pointer = (
        "\n\n## Artifact Generation Templates\n\n"
        "Full generation templates for `project-doc.md` and repository `AGENTS.md` instructions, "
        "including architectural change detection patterns, live in `references/details.md`.\n"
    )
    
    new_skill = head + pointer
    refs_dir = p / "references"
    refs_dir.mkdir(parents=True, exist_ok=True)
    (refs_dir / "details.md").write_text("# Codebase Scanner: Generation Templates & Specifications\n\n" + tail)
    skill_file.write_text(new_skill)
    print("Refactored scan:", len(new_skill.encode()))

def refactor_signed_audit_trails():
    p = REPO_ROOT / "plugins/signed-audit-trails/skills/signed-audit-trails-recipe"
    skill_file = p / "SKILL.md"
    content = skill_file.read_text()
    
    # Split before "## How the cryptography works"
    marker = "## How the cryptography works"
    idx = content.find(marker)
    if idx == -1:
        return
    head = content[:idx].rstrip()
    tail = content[idx:].lstrip()
    
    head = head.replace("## When to use the pattern", "## When to Use This Pattern")
    
    pointer = (
        "\n\n## Cryptography, Policy Engine & CI/CD Integration\n\n"
        "Cryptographic verification details, Cedar policy specifications, SLSA provenance integration, "
        "and cross-implementation interop live in `references/details.md`.\n"
    )
    
    new_skill = head + pointer
    refs_dir = p / "references"
    refs_dir.mkdir(parents=True, exist_ok=True)
    (refs_dir / "details.md").write_text("# Signed Audit Trails: Cryptography & Architecture Reference\n\n" + tail)
    skill_file.write_text(new_skill)
    print("Refactored signed-audit-trails-recipe:", len(new_skill.encode()))

def refactor_competitive_landscape():
    p = REPO_ROOT / "plugins/startup-business-analyst/skills/competitive-landscape"
    skill_file = p / "SKILL.md"
    content = skill_file.read_text()
    
    # Split before "## Competitive Intelligence"
    marker = "## Competitive Intelligence"
    idx = content.find(marker)
    if idx == -1:
        return
    head = content[:idx].rstrip()
    tail = content[idx:].lstrip()
    
    pointer = (
        "\n\n## Competitive Intelligence, Pricing & Monitoring Playbooks\n\n"
        "Detailed playbooks for intelligence gathering, pricing tier analysis, go-to-market strategies, "
        "and continuous monitoring live in `references/details.md`.\n"
    )
    
    new_skill = head + pointer
    refs_dir = p / "references"
    refs_dir.mkdir(parents=True, exist_ok=True)
    (refs_dir / "details.md").write_text("# Competitive Landscape: Intelligence & Strategy Playbooks\n\n" + tail)
    skill_file.write_text(new_skill)
    print("Refactored competitive-landscape:", len(new_skill.encode()))

def refactor_startup_metrics_framework():
    p = REPO_ROOT / "plugins/startup-business-analyst/skills/startup-metrics-framework"
    skill_file = p / "SKILL.md"
    content = skill_file.read_text()
    
    # Split before "## Consumer/Mobile Metrics"
    marker = "## Consumer/Mobile Metrics"
    idx = content.find(marker)
    if idx == -1:
        return
    head = content[:idx].rstrip()
    tail = content[idx:].lstrip()
    
    pointer = (
        "\n\n## Consumer, B2B & Investor Metrics Frameworks\n\n"
        "Detailed formulas and tracking frameworks for Consumer/Mobile, B2B, stage-by-stage growth, "
        "and investor reporting live in `references/details.md`.\n"
    )
    
    new_skill = head + pointer
    refs_dir = p / "references"
    refs_dir.mkdir(parents=True, exist_ok=True)
    (refs_dir / "details.md").write_text("# Startup Metrics: Consumer, B2B & Investor Deep Dives\n\n" + tail)
    skill_file.write_text(new_skill)
    print("Refactored startup-metrics-framework:", len(new_skill.encode()))

if __name__ == "__main__":
    refactor_screen_reader_testing()
    refactor_code_review_excellence()
    refactor_debugging_strategies()
    refactor_architecture_decision_records()
    refactor_protocol_reverse_engineering()
    refactor_scan()
    refactor_signed_audit_trails()
    refactor_competitive_landscape()
    refactor_startup_metrics_framework()
