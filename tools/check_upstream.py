#!/usr/bin/env python3
"""Inspect upstream wshobson/agents for new plugins and skills (read-only).

Governed by DEC-20260905-18: Clean split sovereign repo with quarterly check.
Does not alter git remotes or working tree.
"""

import json
import os
import sys
import urllib.request

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLUGINS_DIR = os.path.join(REPO_ROOT, "plugins")
UPSTREAM_API = "https://api.github.com/repos/wshobson/agents/contents/plugins"


def main():
    print("Checking upstream (wshobson/agents) plugins...")
    local_plugins = set(os.listdir(PLUGINS_DIR))

    req = urllib.request.Request(
        UPSTREAM_API,
        headers={"User-Agent": "agents-upstream-checker", "Accept": "application/vnd.github.v3+json"},
    )

    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print(f"Failed to query upstream API: {e}", file=sys.stderr)
        return 1

    upstream_plugins = {item["name"] for item in data if item.get("type") == "dir"}

    new_upstream = sorted(upstream_plugins - local_plugins)
    our_exclusive = sorted(local_plugins - upstream_plugins)

    print(f"\nLocal plugins count: {len(local_plugins)}")
    print(f"Upstream plugins count: {len(upstream_plugins)}")

    if new_upstream:
        print(f"\nNew upstream plugins to evaluate ({len(new_upstream)}):")
        for p in new_upstream:
            print(f"  + {p}")
    else:
        print("\nNo new plugins found in upstream repository.")

    print(f"\nOur sovereign plugins not in upstream ({len(our_exclusive)}):")
    for p in our_exclusive:
        print(f"  * {p}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
