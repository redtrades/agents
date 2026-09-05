# Provenance

Source: `disler/max-your-cc-sub`, `examples/` directory. License: MIT,
verbatim (`Copyright (c) 2026 IndyDevDan`, confirmed by reading the
`LICENSE` file directly). Copied **verbatim**, no modifications — MIT
permits this and the scripts are self-contained, heavily-commented
reference examples not meant to be edited to fit in.

Copied 2026-08-24:

| File | What it does |
|---|---|
| `01_oauth_cli.py` | Runs `claude -p` under `CLAUDE_CODE_OAUTH_TOKEN` (subscription billing), captures the stream-json event feed, extracts `system/init.apiKeySource` and `rate_limit_event.rateLimitType` as forensic proof of which billing path was used. Scrubs `ANTHROPIC_API_KEY`/`ANTHROPIC_AUTH_TOKEN` from the subprocess env first, since Claude Code's documented credential precedence puts both of those ABOVE the OAuth token — if either is set, the OAuth token is silently ignored. |
| `02_oauth_sdk.py` | Same OAuth-subscription check, via the Claude Agent SDK (Python) instead of the CLI subprocess. |
| `03_api_key_cli.py` | Same check, but under `ANTHROPIC_API_KEY` (Console API billing) via the CLI. |
| `04_api_key_sdk.py` | Same check, API-key path, via the Agent SDK. |
| `_compare_signals.py` | Runs both an OAuth and an API-key example, diffs the two captured signal sets side-by-side. |

Pure Python 3.11+ stdlib (PEP 723 inline deps, `uv run` resolves them —
`01`/`03` declare `dependencies = []`; `02`/`04` likely pull in the Claude
Agent SDK package, check each file's script header before running).
Tested by the source repo on macOS and Linux per its own README; nothing
platform-specific found on inspection (no shell-outs beyond invoking
`claude` itself). No secrets, no `.env` file, no credentials of any kind
in the copied files — they read `CLAUDE_CODE_OAUTH_TOKEN`/
`ANTHROPIC_API_KEY` from the environment at runtime, they don't embed any
value. Confirmed via a repo-wide secret-pattern scan (API-key-shaped
strings, AWS keys, GitHub tokens, private-key blocks) across all five
2026-08-24 disler-import clones — no hits.

**Not runnable as-is without credentials of your own** (`CLAUDE_CODE_OAUTH_TOKEN`
via `claude setup-token`, or `ANTHROPIC_API_KEY` from the Console) — these
are diagnostic scripts, staged here for reference/reuse, not wired into
anything. See `configs/claude-subscription-compliance-notes.md` for why
this is relevant to Mike specifically.
