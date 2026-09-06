#!/usr/bin/env python3
"""Mechanical triage scanner for historic agent repositories.

Token-efficient scanner that indexes documentation, decisions, and tools across
historic attempts without invoking LLM tokens.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

HISTORIC_REPOS = [
    Path("/Users/man/agent-platform"),
    Path("/Users/man/agent-mesh"),
    Path("/Users/man/agent-workspace"),
    Path("/Users/man/agent-sdlc"),
    Path("/Users/man/agent-configs"),
]

TARGET_AGENTS = Path("/Users/man/agents")
TARGET_BRAIN = Path("/Users/man/Brain")

IGNORE_DIRS = {
    ".git",
    "node_modules",
    ".venv",
    "venv",
    "__pycache__",
    "dist",
    "build",
    ".codex",
    ".opencode",
    ".antigravity",
    ".cursor",
}


def file_hash(path: Path) -> str:
    h = hashlib.sha256()
    try:
        with open(path, "rb") as f:
            while chunk := f.read(65536):
                h.update(chunk)
        return h.hexdigest()
    except Exception:
        return ""


def main() -> None:
    print("=== Mechanical Estate Triage Scanner ===")

    # 1. Index hashes in target repos (agents and Brain)
    target_hashes: set[str] = set()
    for root in (TARGET_AGENTS, TARGET_BRAIN):
        if not root.is_dir():
            continue
        for p in root.rglob("*"):
            if p.is_file() and not any(part in IGNORE_DIRS for part in p.parts):
                h = file_hash(p)
                if h:
                    target_hashes.add(h)

    print(f"Indexed {len(target_hashes)} unique file hashes in agents/ and Brain/")

    # 2. Scan historic repositories
    manifest = {
        "decisions": [],
        "rules": [],
        "tools": [],
        "post_mortems": [],
        "other_markdown": [],
    }

    stats = {"scanned": 0, "already_preserved": 0, "unique_candidates": 0}

    for repo in HISTORIC_REPOS:
        if not repo.is_dir():
            print(f"Skipping missing repo: {repo}")
            continue

        print(f"Scanning {repo.name}...")
        for p in repo.rglob("*"):
            if not p.is_file() or any(part in IGNORE_DIRS for part in p.parts):
                continue

            stats["scanned"] += 1
            h = file_hash(p)
            if h in target_hashes:
                stats["already_preserved"] += 1
                continue

            stats["unique_candidates"] += 1
            rel = str(p.relative_to(repo))
            name_lower = p.name.lower()

            entry = {
                "repo": repo.name,
                "path": rel,
                "size_bytes": p.stat().st_size,
                "ext": p.suffix,
            }

            if "adr" in name_lower or "decision" in name_lower:
                manifest["decisions"].append(entry)
            elif "rule" in name_lower or "constitution" in name_lower or "operating" in name_lower:
                manifest["rules"].append(entry)
            elif (
                "postmortem" in name_lower
                or "rca" in name_lower
                or "incident" in name_lower
                or "spiral" in name_lower
            ):
                manifest["post_mortems"].append(entry)
            elif p.suffix in (".py", ".sh", ".ts", ".mjs"):
                manifest["tools"].append(entry)
            elif p.suffix == ".md":
                manifest["other_markdown"].append(entry)

    print("\n=== Triage Results ===")
    print(f"Total Files Scanned:       {stats['scanned']}")
    print(f"Already Preserved:         {stats['already_preserved']}")
    print(f"Unique Candidate Assets:   {stats['unique_candidates']}")
    print(f"  - Decisions/ADRs:        {len(manifest['decisions'])}")
    print(f"  - Rules & Policies:      {len(manifest['rules'])}")
    print(f"  - Post-Mortems & RCAs:   {len(manifest['post_mortems'])}")
    print(f"  - Reusable Tools/Scripts:{len(manifest['tools'])}")
    print(f"  - Other Markdown Docs:   {len(manifest['other_markdown'])}")

    out_dir = TARGET_AGENTS / "docs/research"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "20260905-historic-estate-triage.json"
    with open(out_file, "w") as f:
        json.dump(manifest, f, indent=2)
    print(f"\nManifest saved to: {out_file.relative_to(TARGET_AGENTS)}")


if __name__ == "__main__":
    main()
