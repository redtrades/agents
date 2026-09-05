# OpenCode config / providers — breakage root cause + fix, 2026-08-27

Mike: "OpenCode not loading all the keys and providers he had before."
Diagnosed and fixed. Related: the parallel Hermes/omlx work in
`omlx-qwen38-oq4e-mcp-restore-and-rootcause-2026-08-27.md` — same writer
(`~/agent-mesh`), same class of failure, different file.

## File paths (the actual ones)

| Purpose | Path |
|---|---|
| OpenCode global config | `~/.config/opencode/opencode.json` |
| Credentials (API keys) | `~/.local/share/opencode/auth.json` (chmod 600) |
| Personas written by agent-mesh | `~/.config/opencode/agents/{prime,scout,sentinel,forge,operator}.md` |
| Pre-existing auto-backup | `~/.config/opencode/opencode.json.backup-20260826-152834` (holds the Aug-21 last-good config) |
| My timestamped backup before editing | `~/.config/opencode/opencode.json.backup-20260827-094811-prefix` |
| Project-local config (separate, not global) | `~/agent-reports/freellmapi-install/freellmapi/opencode.json` |
| OpenCode DB / logs | `~/.local/share/opencode/opencode.db`, `~/.local/share/opencode/log/opencode.log` |

`~/.config/opencode/` is **not** a git repo (has a `.gitignore` but no
`.git`). No version history for these files.

## Root cause

**`opencode.json` was schema-invalid.** The `omlx-local` provider's
`qwen3.8-oq4e` model entry had:

```json
"limit": { "context": 262144 }
```

OpenCode 1.18.20's config schema requires **both** `context` and `output`
whenever a `limit` object is present. Missing `output` →

```
Configuration is invalid at /Users/man/.config/opencode/opencode.json
↳ Missing key provider.omlx-local.models.qwen3.8-oq4e.limit.output
```

On the strict config path (`opencode models`, the TUI model picker, any
fresh session's provider enumeration) this **aborts the whole config load** —
so every provider disappears, including the six unrelated cloud providers
that live in `auth.json` and need no `provider` block at all. That is the
"lost all my providers" symptom. (The lenient TUI/serve path tolerated it:
`opencode.log` shows `openrouter/auto` still answering at 02:24 Aug 27, which
is why it looked intermittent.)

### Not the cause
- **No duplicate-key / dropped-entry corruption** in either file. Unlike
  `~/.hermes/config.yaml`, `opencode.json` is JSON, has no duplicate keys,
  no dropped providers; `auth.json` is intact with all 6 entries, valid,
  no dupes. Checked explicitly — this is *not* the YAML last-key-wins shape.
- **Not a version upgrade.** OpenCode 1.18.20 installed Aug 22 10:20, never
  changed. The `output` requirement predates the bad edit.
- **Not rotated/expired keys** at the config level — keys are present and
  well-formed. (Some providers' *accounts* have lapsed — see verification.)

## Is agent-mesh the writer? — Yes.

`~/agent-mesh` (repo `redtrades/agent-mesh`, the overnight OpenClaw-successor
build Mike has confirmed as his and intended) writes `~/.config/opencode/`:

- Its `.agent/AGENTS.md` §opencode: *"Providers are configured in
  `opencode.json` with an OpenAI-compatible provider block per endpoint …
  this folder never records them"* — i.e. it treats `opencode.json` provider
  blocks as live machine state it configures and deliberately does not
  version.
- WORKLOG 2026-08-27 ~15:15: *"ported .agent/ personas to both harnesses
  (5 personas × 2 targets = 10 files); closed #17"* → the
  `~/.config/opencode/agents/*.md` files, mtime **2026-08-26 15:28:20**.
- The auto-backup `opencode.json.backup-20260826-152834` was made at that
  same moment (agent-mesh's backup-before-write fingerprint, cf.
  `config.yaml.backup-YYYYMMDD-HHMMSS-*`).
- `opencode.json` itself was then edited **2026-08-26 15:39** (pre-fix
  mtime) — 11 min later — adding the `qwen3.8-oq4e` block with
  `context: 262144`. This mirrors **exactly** the change agent-mesh recorded
  making to `~/.hermes/config.yaml` the same afternoon
  (DECISIONS D-017 / WORKLOG ~16:40: *"context_length 131072→262144 for
  qwen3.8-oq4e to match native window"*). Same intent, same session, same
  day, propagated to the OpenCode config — just without the `output` sibling
  key OpenCode's schema needs.

So: **same writer as the Hermes corruption (`~/agent-mesh`), same class**
(an automated writer extending a live config and leaving it structurally
invalid), but a **different mechanism** — a targeted JSON model-add missing
a required sub-key, not a duplicate top-level key.

## Ownership

`opencode.json`'s **local-provider blocks** (`omlx-local` → :8300,
`mlx-local` → :11434) and `~/.config/opencode/agents/` are **agent-mesh's
surface** — it configures them by design and its AGENTS.md says so. Under
the ruling that agent-mesh owns the live Hermes/omlx surface, these count.

The **six cloud credentials in `auth.json`** (OpenCode Zen, OpenRouter,
Cerebras, Google, Fireworks AI, Groq — a multi-provider free-routing setup,
cf. `research-free-routing-subscriptions.md`) are broader than omlx and not
obviously agent-mesh-exclusive, but they were only *invisible* because of
agent-mesh's invalid `opencode.json` edit — `auth.json` itself was never
touched by this bug.

### What I did about ownership
Applied the **minimal fix agent-mesh would keep**: added the missing
`"output": 65536` to the existing `limit` block — completing agent-mesh's
own edit rather than reverting its `262144` intent. `65536` matches Mike's
existing convention in `freellmapi/opencode.json`
(`"limit": {"context": 1048576, "output": 65536}`). agent-mesh's next
normalize pass has no reason to strip a schema-required key, so this
survives.

**Follow-up for agent-mesh's SDLC (not done here — needs a worktree+PR into
`redtrades/agent-mesh` per its AGENTS.md, or Mike's say-so):** whatever
agent-mesh routine/script emits the `opencode.json` provider block should
emit a complete `limit` (`context` **and** `output`), or omit `limit`
entirely (it's optional — the sibling `qwen3.8` entry has none and is
valid). File against agent-mesh alongside its config-writer-coordination
issue.

## Change made

`~/.config/opencode/opencode.json`, `provider.omlx-local.models.qwen3.8-oq4e.limit`:

```diff
   "limit": {
-    "context": 262144
+    "context": 262144,
+    "output": 65536
   }
```

Backup first: `opencode.json.backup-20260827-094811-prefix`. Nothing else
touched. `auth.json` not modified.

## Per-provider verification (real completions, not just config parse)

After the fix, `opencode models` enumerates all 8 providers and
`opencode run -m openrouter/openai/gpt-4o-mini "…"` returns `OPENCODE_OK`
end-to-end. Then each provider probed directly:

| Provider (auth.json key name) | Result | Detail |
|---|---|---|
| **openrouter** | ✅ **works** | `opencode run` → `OPENCODE_OK`; direct → "Pong!". Key valid. |
| **omlx-local** (:8300) | ✅ **works** | Direct `/v1/chat/completions` `qwen3.8-oq4e` → "…Final: pong". Server up, model resident. (opencode→omlx path is just slow: oq4e cold load ~50–120s per the bench notes.) |
| **groq** | ⚠️ **wired & authed; free-tier TPM too small for opencode** | Direct tiny-prompt probe `openai/gpt-oss-20b` → HTTP 200. Through `opencode run`: `Request too large … TPM Limit 8000, Requested 32491` — opencode's agent system prompt (~32–49k tok) exceeds groq's free 8000 tok/min. Provider correctly wired; needs a paid Groq tier to be usable as an opencode agent model (fine for tiny/API calls). Also `llama-3.1-8b-instant` / `llama-3.3-70b-versatile` now 404 — use `openai/gpt-oss-20b|120b`, `qwen/qwen3.6-27b`. |
| **opencode-zen** | ⚠️ **key valid, account blocked** | 401 `No payment method. Add a payment method here: opencode.ai/workspace/wrk_01M0XX24ZW0BR454DZAS7ZRH6W/billing`. The `x-preview-f-free` model (Ox Alpha on Zen) now returns `Model … is not supported` — **the free preview window closed** (expected per the Ox Alpha notes, ~2026-08-27). This is provider-side, not a config bug. To use Zen now Mike must add a payment method. |
| **cerebras** | ⚠️ **key valid, billing required** | 402 `Payment required to access this resource. Visit your billing tab.` on every model. Free quota exhausted/ended. Provider-side. |
| **fireworks-ai** | ❌ **account suspended** | 412 `Account redtrades is suspended, possibly due to reaching the monthly spending limit or failure to pay past invoices` → fireworks.ai/account/billing. Provider-side. |
| **google** | ❔ **inconclusive — likely stale token** | Every call (v1beta key-param, OpenAI-compat bearer, `x-goog-api-key`, curl) times out reading the response though TCP:443 connects. The stored key is `AQ.Ab8RN6…` — a Google **OAuth2 access token** (hourly expiry), not an `AIza…` API key; almost certainly expired. Re-auth: `opencode auth login google` with a real Gemini API key. (Read timeout may also be this session's egress; Mike should retry locally.) |
| **mlx-local** (:11434) | ❌ **backend not running** | `nothing listening on 11434`. Config entry valid; the MLX server (Qwen3.6-35B-A3B) is just not up. Also `omlx-local`'s bare `qwen3.8` model id no longer exists on :8300 (now `qwen3.8-oq4e` + ~12 renamed checkpoints agent-mesh pulled) — that one model entry is stale but harmless. |

### Summary
- **Genuinely fixed by the config change:** openrouter (full end-to-end via
  `opencode run`), omlx-local (direct API confirmed; opencode→omlx round
  trip stalls only under current omlx load — 3 active reqs, 2.8 tok/s —
  which is agent-mesh's surface, not this config), and the *visibility* of
  all 8 (picker + `opencode models` work again).
- **Wired correctly but free-tier quota blocks real use:** groq (8000
  TPM < opencode's prompt).
- **Key valid, needs a live-account action from Mike, not a config fix:**
  opencode-zen (add payment method; the free Ox Alpha / `x-preview-f-free`
  window has closed), cerebras (billing), fireworks-ai (account suspended).
- **Needs re-auth:** google (stored value is an expired `AQ.` OAuth token,
  not an `AIza` key — `opencode auth login google`).
- **Needs the backend started:** mlx-local (:11434, nothing listening).

**Only one thing was actually broken in config: the missing `limit.output`.**
Everything else is provider-account state or a dead local backend — i.e.
the providers whose "free window simply expired" (Zen/Ox Alpha, Cerebras
free quota) vs. real breakage (the invalid JSON).

## How verified

```
opencode --version                     # 1.18.20
opencode models 2>&1 | head            # pre-fix: "Configuration is invalid … Missing key … limit.output"
# (apply fix)
opencode models | sed 's#/.*##' | sort -u   # cerebras fireworks-ai google groq mlx-local omlx-local opencode openrouter
opencode auth list                     # 6 credentials: Zen, OpenRouter, Cerebras, Google, Fireworks, Groq
opencode run -m openrouter/openai/gpt-4o-mini "reply with exactly: OPENCODE_OK"   # -> OPENCODE_OK
python3 scratchpad/probe2.py / probe3.py   # per-provider direct completions (table above)
curl -sS http://127.0.0.1:8300/v1/models   # omlx up, qwen3.8-oq4e present
lsof -nP -iTCP:11434 -sTCP:LISTEN       # (nothing) -> mlx-local backend down
```

No secret values printed anywhere; keys referred to by `auth.json` key
name and location only.
