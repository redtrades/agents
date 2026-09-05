# Claude subscription compliance notes

**Source:** `disler/max-your-cc-sub`. License: MIT (verbatim,
`Copyright (c) 2026 IndyDevDan`). This is a plain-language writeup of the
repo's compliance framing, not a copy of its README — see that repo (or
`configs/billing-path-detector/`) for the original wording and the
runnable diagnostic scripts. Written 2026-08-24. Informational/diagnostic
content, not a ToS violation itself — filed under `configs/`, not
`tos-flagged/`.

## The one rule, as the source repo states it

> Your Pro/Max subscription is for your own individual use — the moment
> your code routes someone else's request through your seat, stop using
> the subscription OAuth token and switch to an API key.

Two tripwires: **"your own individual use"** is the permission Anthropic
grants; **"someone else's request"** is what crosses the line. The
source repo cites Anthropic's own
[legal/compliance clarification](https://code.claude.com/docs/en/legal-and-compliance#authentication-and-credential-use)
(dated February 2026 per the repo) as the basis — a Consumer Terms of
Service matter, being actively enforced, not a hypothetical risk.

## The three-tier classification

- ✅ **Green (safe):** one human, one subscription, one beneficiary.
  Personal scripts, CI on your own individual repo using
  `CLAUDE_CODE_OAUTH_TOKEN` as a secret, Claude Code on a work laptop for
  work *you* author.
- ⚪ **Gray (controversial):** more than one human benefits from a single
  subscription, and Anthropic's own wording doesn't resolve it cleanly —
  agency/contractor work through a personal token, a Slack bot or daily
  report multiple people read, an internal team tool running on one
  dev's Pro/Max token. The repo's own advice for this tier: "grab an API
  key and stop guessing."
- ❌ **Red (bannable):** shipping a product on a personal OAuth token,
  multi-tenant SaaS logging users into Claude.ai on someone else's
  behalf, **pooling one subscription across a team**, reselling access,
  extracting tokens from `~/.claude/.credentials.json` or Keychain.

## Why this is relevant to Mike specifically

Mike's own memory has a diagnosed, named issue:
**shared-account session contention** —
`project_shared_account_session_contention` (2026-08-17): 10+ concurrent
Claude Code/Buzz/FleetView sessions on one Max account, causing OAuth
refresh races and session-limit hits. `agent-configs/MASTER-GUIDE.md` §4
separately documents that `claude -p` calls in the SSSF pipeline
intermittently break mid-run under 12+-concurrent-session contention,
attributing it to OAuth expiry rather than a code bug.

**This survey pass does not make a determination about which tier that
setup falls into** — that's explicitly Mike's call, same posture the
prior survey pass took ("flag the compliance angle to Mike rather than
silently act on it," per `disler-github-survey-2026-08-24.md`'s verdict
on this same repo). What this note adds, now that Mike has given a
blanket go-ahead to bring the material in: the actual diagnostic
mechanism is now staged and available, if/when he wants to run it against
his own setup rather than reason about it in the abstract.

## The diagnostic mechanism (now staged, not run)

`configs/billing-path-detector/` has the copied example scripts. The
technique: launch `claude -p` (or the SDK) with `--output-format
stream-json --include-hook-events`, capture the event feed, and read two
fields:

| Signal | OAuth (subscription) | API key |
|---|---|---|
| `system/init.apiKeySource` | `"none"` | `"ANTHROPIC_API_KEY"` |
| `rate_limit_event.rateLimitType` | `"five_hour"` (Pro/Max bucket) | *(event never emitted)* |

The `five_hour` rate-limit bucket is the decisive tell, per the source
repo: API keys are billed on RPM/TPM tiers and never emit that event —
seeing it is proof-positive of subscription billing, not an inference.

**One documented gotcha worth flagging before anyone runs this against a
real session:** Claude Code's credential precedence puts
`ANTHROPIC_API_KEY` and `ANTHROPIC_AUTH_TOKEN` *above*
`CLAUDE_CODE_OAUTH_TOKEN`. If a shell or `.env` has both a subscription
OAuth token and an API key set (plausible on a machine running multiple
tools/gateways — FreeLLMAPI's gateway, for instance, per
`agent-configs/MASTER-GUIDE.md` §4), a run believed to be subscription-
billed may silently be billed against the API key instead, with no error
— the scripts in `billing-path-detector/` exist specifically to catch
that silently-wrong assumption, not just to confirm a known-good one.

## What this note is not

Not legal advice, not a determination that Mike's setup is or isn't
compliant, not an instruction to change anything about the current
FreeLLMAPI/Hermes/SSSF credential wiring. Purely: here is the framework
Anthropic itself uses to draw the line, here is a working way to check
which line a given run actually crossed, and here is why it's on Mike's
radar already via a different, previously-diagnosed problem.
