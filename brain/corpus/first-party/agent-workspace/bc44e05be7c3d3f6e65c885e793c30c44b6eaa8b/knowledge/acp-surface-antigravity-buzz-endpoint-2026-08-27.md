# ACP control surface, Antigravity, and whether Antigravity can back Buzz

2026-08-27. Read-only investigation. **Nothing was applied.** No file under
`~/.hermes`, `~/.omlx`, `~/Library/LaunchAgents`, `~/.config/opencode` or
`~/agent-mesh` was modified. No GPU work was started. No secret value appears
anywhere in this file.

## Ownership boundary observed

`~/agent-mesh` owns the live Hermes and omlx surface (its own `AGENTS.md`
"no new daemon/scheduler/database next to an existing one", and
`~/agent-workspace/knowledge/opencode-config-providers-rootcause-2026-08-27.md`
which established the same ruling for `~/.config/opencode` local-provider
blocks). Everything below is a proposal against those files, not a change to
them. I read `~/agent-mesh/AGENTS.md`, `DECISIONS.md` (D-001..D-026),
`WORKLOG.md` and `HANDOFF.md` first.

**What agent-mesh already decided that constrains this answer:**

| Decision | Effect here |
|---|---|
| D-012 | No auto-trading anywhere. Not touched by this work. |
| D-016, D-017, D-023 | Hermes root and bots are pinned to local `omlx` `qwen3.8-oq4e`. Any new provider is additive, never a default swap. |
| D-022 | Agent-mesh operational sources only; GovCon is non-governing. |
| D-026 | Local oQ4e + TurboQuant KV4 + Lightning MTP is the measured production champion. A hosted backend is a supplement to that, not a replacement. |
| `AGENTS.md` hard line | Secrets live in `~/.hermes/.env`, Keychain, or `~/.config/<tool>`, referenced by name only. Any Antigravity key must follow that. |

Agent-mesh has **not** done ACP or Antigravity work. `grep -ril "antigravity"`
across `~/agent-mesh` returns only four research files that mention Antigravity
in passing (skill-portability matrices and the mined OpenClaw v1 digest), and
its only ACP mention is `research/research-harnesses-councils.md` line 74, which
correctly distinguishes Zed's Agent Client Protocol from IBM's ACP that merged
into A2A. Its worklog carries future-dated entries; I trusted file mtimes
throughout (`WORKLOG.md` mtime 2026-08-27 02:48, `DECISIONS.md` 2026-08-27
01:30, `HANDOFF.md` 2026-08-27 00:25).

**An agent-mesh benchmark session may be live.** I ran no inference, no
`hermes` command, and no `curl` against `:8300`. Every "verify with" line below
is a command for you to run, not something I ran.

---

# Answer in three lines

1. **ACP gives you sessions, prompts, streaming, permissions, and model
   selection. It does not give you profiles, toolsets, or provider
   registration.** Model selection over ACP is real and Buzz uses it, but it is
   an *unstable* protocol method, and the model string can only name providers
   that already exist in the target profile's `config.yaml`.
2. **The Antigravity skill on your disk is real but stale.** It describes `agy`
   as a subprocess with no JSON output. Google's current docs document
   `--output-format json|stream-json`, a `--input-format stream-json`
   bidirectional session, a Python SDK, and a hosted Antigravity agent on the
   Gemini Interactions API. The skill predates all of that.
3. **Antigravity cannot become a custom endpoint for Buzz on your
   subscription, and can become one on the Gemini API only if you write a
   translation shim.** Google publishes no endpoint for the subscription rail
   and states there is no bring-your-own-endpoint. More decisively, the
   Antigravity terms name third-party tools accessing the Service through its
   OAuth session as a **breach of agreement with account termination as the
   stated remedy**, and they name OpenClaw as the example. Every `agy`-wrapping
   proxy on GitHub is that pattern. The hosted Antigravity agent on the Gemini
   Interactions API *is* legitimately reachable, but it speaks
   `POST /v1beta/interactions`, not `/v1/chat/completions`, so no config-only
   path exists in any of the five harnesses.

---

# Q1. What ACP actually gives you

## Provenance of this section

Every claim here is from code on this machine, not from the website.

| Thing | Path |
|---|---|
| ACP SDK Hermes actually runs | `~/.hermes/hermes-agent/venv/lib/python3.11/site-packages/acp/` |
| SDK version | `agent-client-protocol` **0.9.0** (`…/agent_client_protocol-0.9.0.dist-info/METADATA`) |
| Schema it was generated from | `acp/meta.py` header: `Schema ref: refs/tags/v0.11.2` |
| Wire protocol version | `acp/meta.py`: `PROTOCOL_VERSION = 1` |
| Method registry | `acp/meta.py` `AGENT_METHODS` / `CLIENT_METHODS` |
| Stable-vs-unstable routing | `acp/agent/router.py` `build_agent_router()` |
| Hermes implementation | `~/.hermes/hermes-agent/acp_adapter/` (`server.py` 113,390 bytes, `session.py`, `tools.py`, `permissions.py`, `auth.py`, `edit_approval.py`, `events.py`, `entry.py`) |
| Entrypoints | `pyproject.toml` `[project.scripts]`: `hermes-acp = "acp_adapter.entry:main"`; also `hermes acp` (`hermes_cli/main.py`, `_AGENT_COMMANDS = {None, "chat", "acp", "rl"}`) |

Public spec cross-check: <https://agentclientprotocol.com/protocol/schema>
(accessed 2026-08-27). The published page documents `authenticate`,
`initialize`, `logout`, `session/cancel`, `session/close`, `session/delete`,
`session/list`, `session/load`, `session/new`, `session/prompt`,
`session/resume`, `session/set_config_option`, `session/set_mode`,
`elicitation/*`, `fs/*`, `session/request_permission`, `session/update`,
`terminal/*`, `$/cancel_request`. Note the difference: **the published page has
no `session/set_model` section, but the SDK on disk has it in `AGENT_METHODS`.**
That is consistent with it being unstable, and it is the one place where
vendor doc and local code disagree. Local code wins for "what Hermes will
answer today".

## The complete method surface

**Client calls these on Hermes (agent methods):**

| Method | Stable? | Hermes handler |
|---|---|---|
| `initialize` | stable | `server.py:1295` |
| `authenticate` | stable | `server.py:1329` |
| `session/new` | stable | `server.py:1591` |
| `session/load` | stable | `server.py:1612` |
| `session/list` | stable | `server.py:1737` |
| `session/prompt` | stable | `server.py:1784` |
| `session/cancel` (notification) | stable | `server.py:1696` |
| `session/set_mode` | stable | `server.py:2604` |
| `session/set_config_option` | stable | `server.py:2620` |
| `session/set_model` | **unstable** | `server.py:2570` |
| `session/fork` | **unstable** | `server.py:1717` |
| `session/resume` | **unstable** | `server.py:1660` |
| `session/close` | **unstable** | not implemented by Hermes |

Unstable methods are only routed when the server is built with
`use_unstable_protocol=True` (`acp/agent/router.py`, `unstable=True` on those
four routes). Hermes sets it:
`acp_adapter/entry.py` → `asyncio.run(acp.run_agent(agent, use_unstable_protocol=True))`.
So on your box, model switching, fork and resume are live.

**Hermes calls these back on the client (client methods):**
`session/update` (streaming), `session/request_permission`,
`fs/read_text_file`, `fs/write_text_file`, `terminal/create`, `terminal/output`,
`terminal/wait_for_exit`, `terminal/kill`, `terminal/release`.

**Extension channel:** `router.handle_extension_request` dispatches any method
whose name starts with `_` to `agent.ext_method(name, payload)`. This is how
Buzz's mid-turn steering is meant to work: `_session/steering`, documented in
`~/.hermes/skills/autonomous-ai-agents/hermes-buzz-integration/SKILL.md`
(section "A. Mid-turn mentions cancel"), which specifies
`initialize` returning `_meta.steering.supported: true` and a result of
`{outcome: "injected"|"startedNewTurn"}`.

## What Hermes advertises at handshake

From `server.py:1295` `initialize()`:

- `agent_info`: name `hermes-agent`, version = installed Hermes version
- `agent_capabilities.load_session = True`
- `prompt_capabilities.image = True`
- `session_capabilities`: `fork`, `list`, `resume`
- `auth_methods` from `acp_adapter/auth.py` `build_auth_methods()`:
  - an `AuthMethodAgent` whose id is the *currently resolved runtime provider*
    (on this box that resolves from `~/.hermes/config.yaml` `model.provider: omlx`)
  - always a `TerminalAuthMethod` with id `hermes-setup`, `args: ["--setup"]`,
    which shells out to `hermes model` for interactive setup

`authenticate()` only accepts a `method_id` matching either `hermes-setup` or
the detected provider; anything else returns `None`.

## Capability-by-capability

### Model selection: yes, with a real constraint

`set_session_model(model_id, session_id)` (`server.py:2570`):

1. `_resolve_model_selection` (`server.py:980`) calls
   `hermes_cli.models.parse_model_input` (`models.py:2780`), then
   `detect_provider_for_model` as a fallback.
2. `parse_model_input` accepts `provider:model`, and specifically
   `custom:<name>:<model>` triples, returning provider `custom:<name>`
   (`models.py:2813-2824`). The left side is only treated as a provider if it is
   in `_KNOWN_PROVIDER_NAMES` or `_configured_custom_provider_ids()`.
3. The session's agent is rebuilt via `session_manager._make_agent(...)`. If the
   provider changed, `base_url` and `api_mode` are deliberately dropped so they
   are re-resolved for the new provider (`server.py:2586-2588`).

The picker list ACP clients see comes from
`hermes_cli.inventory.build_models_payload` with `explicit_only=True`,
`include_unconfigured=False` (`server.py` `_build_model_state`). That is the
same inventory `hermes model`, the TUI and the dashboard use. Entries are
encoded `provider:model` and named `"<Provider label> · <model id>"`.

**The constraint:** ACP can only *select among* providers that already exist in
the profile's `config.yaml`. There is no ACP method to add a provider, a
base URL, or a key. Adding a backend is always a config write plus a restart of
whatever launched `hermes-acp`.

### Profile selection: no

`grep -n "profile\|PROFILE" ~/.hermes/hermes-agent/acp_adapter/*.py` returns
**zero matches**. Profile is resolved entirely at process launch:

- `hermes_cli/main.py:586` scans argv broadly for `-p` / `--profile` /
  `--profile=`, before subcommand dispatch, so `hermes -p prime acp` works.
- Otherwise `HERMES_HOME` decides (`hermes_constants.py:114` `get_hermes_home()`:
  context-local override → `HERMES_HOME` env → `~/.hermes`).

So orchestrating "which profile" means controlling the spawn (argv or
`HERMES_HOME`), which for Buzz means the harness definition's `command`/`args`/
`env`, not anything sent over the wire. The Buzz integration skill says the same
thing from the other side: "path ① Desktop ACP typically uses the **default**
profile (`~/.hermes`) … unless hermes-acp is launched with `HERMES_HOME`
override" (`hermes-buzz-integration/references/model-routing.md`, step 7).

### Tool availability: not an ACP operation, with one exception

- Toolsets are fixed when the session's agent is built:
  `_expand_acp_enabled_toolsets(["hermes-acp"], mcp_server_names=…)`
  (`acp_adapter/session.py:140`, used at `session.py:637` and
  `server.py:1167`). Every enabled `mcp_servers` entry in `config.yaml`
  becomes a `mcp-<name>` toolset.
- **Exception:** a client may pass MCP servers on `session/new`, and Hermes
  registers them for that session (`server.py:1126`
  `_register_session_mcp_servers`, with a late-refresh scheduler at
  `server.py:1197`). That is the one tool-surface knob ACP genuinely exposes.
- `/tools`, `/model`, `/context`, `/compress`, `/reset`, `/steer`, `/queue`,
  `/version`, `/help` are Hermes-side text commands surfaced to the client as
  `AvailableCommand` (`server.py:2224`, `_handle_slash_command` at
  `server.py:2268`). They arrive inside a `session/prompt` as text. They are a
  human affordance that happens to be scriptable, not protocol operations.

### Session lifecycle: full

`session/new`, `session/load` (with history replay, `server.py:1493`
`_replay_session_history`), `session/list`, `session/fork`, `session/resume`
(resumes without replaying history), `session/cancel`. Sessions persist to the
per-profile `state.db`.

### Streaming: full

Agent-to-client `session/update` notifications carry message chunks, thought
chunks, tool-call starts and updates, plus Hermes extras: `UsageUpdate` for
native context usage (`_build_usage_update` / `_send_usage_update`,
`server.py:999`/`1032`) and session-info updates (`server.py:1071`).

### Permissions and approvals: full, and mapped carefully

`acp_adapter/permissions.py`:

- Hermes asks the client via `session/request_permission` with a synthesized
  `perm-check-N` tool call.
- Option ids map to Hermes approval strings:
  `allow_once`→`once`, `allow_session`→`session`, `allow_always`→`always`,
  `deny`/`deny_always`→`deny`.
- ACP has no session-scoped kind, so "Allow for session" is sent with
  `kind: allow_always` and the semantics ride on the option id.
- 60 s default timeout returns the string `"timeout"`, deliberately distinct
  from a user deny.
- Where Hermes will re-ask every time anyway (`allow_session=False`, or a Smart
  DENY override), the option list collapses to allow-once/deny so the editor
  cannot offer a scope Hermes would discard.

Modes (`server.py:682` `_session_modes`): Hermes advertises three session modes
mapped onto edit-approval policy (Default, "Ask before edits"; Accept Edits;
Don't Ask), with a comment explaining the choice: Zed renders `config_options`
in the slot where the model picker lives, so Hermes uses modes instead to keep
both visible.

`set_config_option` (`server.py:2620`) accepts anything, but only the
edit-approval-policy config id does something; every other id is stored on the
session and otherwise ignored.

## Automate vs human-in-a-UI

| Behavior | Over ACP? | How to automate instead |
|---|---|---|
| Start / list / fork / resume / cancel sessions | Yes | ACP |
| Send prompts, stream results | Yes | ACP |
| Switch model, including `custom:<provider>:<model>` | Yes (unstable) | ACP |
| Approve or deny a tool call | Yes | ACP client implements `session/request_permission` |
| Switch edit-approval posture | Yes | `session/set_mode` |
| Add MCP servers for one session | Yes | `session/new` `mcpServers` |
| **Switch profile** | No | spawn with `-p <name>` or `HERMES_HOME` |
| **Register a provider / base URL / key** | No | edit `config.yaml` (or `hermes config set`), then restart the ACP process |
| **Enable or disable toolsets** | No | `config.yaml`, or `/tools` text command |
| **Reasoning effort, thinking budget, context length, compaction** | No | `config.yaml`, or `/compress` text command |
| **Cron routines, skills install, gateway, WebUI** | No | `hermes cron`, `hermes gateway`, config |

Everything in the "No" rows is file plus process control, which is still
scriptable. The point is that it is not reachable from an ACP client at
runtime, so a Buzz-side or Zed-side UI cannot drive it.

---

# Q2. Antigravity

## The skill on your disk

**Path:** `/Users/man/.hermes/skills/autonomous-ai-agents/antigravity-cli/SKILL.md`
(9,485 bytes, mtime **2026-08-16 07:37**), plus
`references/cli-docs.md` (2,140 bytes, same mtime). It sits in the
`autonomous-ai-agents` skill family alongside `claude-code`, `codex`,
`opencode`, `hermes-agent`, `hermes-buzz-integration`, `hermes-local-models`.

**Frontmatter:** `name: antigravity-cli`, `version: 0.2.0`,
`author: Tony Simons (asimons81), Hermes Agent`, `license: MIT`,
tags `[Coding-Agent, Antigravity, CLI, Auth, Plugins, Sandbox]`.

**What it actually does:** nothing. It is a reference-and-procedure document. Its
own words, line 18-19: it "does not wrap a network API, so there is nothing to
authenticate from Hermes itself." It tells
the agent to run `agy` through the Hermes `terminal` tool and read
`~/.gemini/antigravity-cli/` files with `read_file`. Its "Orchestration
boundary" section is explicit that `agy` is a worker execution backend or third
opinion, "NOT a first-class orchestration primitive", and should not go on a
kanban board.

There is no Antigravity entry in `~/.agents/skills/` beyond a passing mention in
`using-superpowers/references/antigravity-tools.md`.

**Where the skill is now wrong.** Compared against
<https://antigravity.google/docs/cli/headless> (accessed 2026-08-27):

| Skill says (2026-08-16) | Google docs say (2026-08-27) |
|---|---|
| "there is **no `--output-format json`** and no result envelope with `session_id` / cost / turn count" | `--output-format` accepts `text`, `json`, `stream-json`. The `json` envelope carries `conversation_id`, `status`, `response`, `error`, `duration_seconds`, `num_turns`, `structured_output`, `json_schema`, `usage{input_tokens,output_tokens,thinking_tokens,cache_read_tokens,total_tokens}` |
| "There is **no `--max-turns`**" | Still true. Bounding is `--print-timeout`, default `5m`. Skill correct here. |
| Model picked with display strings, e.g. `--model 'Gemini 3.1 Pro (High)'` | `agy models` lists slugs: `gemini-3.7-flash-high`, `gemini-3.1-pro-high`, `claude-sonnet-4-6`, … and `--model` takes the slug. Unknown model exits non-zero rather than falling back. |
| no mention | `--input-format stream-json` holds one process open and takes NDJSON `{"event":"user","message":{"content":"…"}}` on stdin, emitting one `result` per turn. Requires `--output-format stream-json`. |
| no mention | `--json-schema`, `--effort low|medium|high`, `--agent <name>` |

Two independent local documents also disagree with each other:
`~/agent-reports/google-subscription-antigravity/google-subscription-antigravity-2026-08-20.md`
(mtime 2026-08-20) already asserted `--output-format json` exists, contradicting
the 2026-08-16 skill. The 2026-08-20 report is the one that matches today's
vendor docs. **The skill should be updated or its stale lines struck.**

## What Antigravity is, as of 2026-08-27

There are now **four** separate things wearing the name. Conflating them is the
main way to get this wrong.

| # | Surface | Version in docs nav | Auth | Reachable endpoint? |
|---|---|---|---|---|
| 1 | Antigravity 2.0 desktop / IDE | v2.11.0 | Google account, AI plan quota | No |
| 2 | Antigravity CLI `agy` | v1.1.21, then v1.1.22 minutes later | OS keyring, else browser Google sign-in | No (subprocess only) |
| 3 | Antigravity SDK (Python `google-antigravity`) | v0.1.14, then v0.1.15 | `GEMINI_API_KEY`, or Vertex via `GOOGLE_GENAI_USE_VERTEXAI` + project/location + ADC | It is a local runtime harness that calls the Gemini API |
| 4 | Antigravity agent on the Gemini **Interactions API** | agent id `antigravity-preview-05-2026` | Gemini API key | **Yes** |

The version numbers moved between two fetches minutes apart on 2026-08-27
(CLI 1.1.21 → 1.1.22, SDK 0.1.14 → 0.1.15). Treat every version here as a
snapshot, not a fact with a shelf life.

Sources, all accessed 2026-08-27:
<https://antigravity.google/docs/cli/headless>,
<https://antigravity.google/docs/plans/>,
<https://antigravity.google/docs/sdk/overview/>,
<https://ai.google.dev/gemini-api/docs/antigravity-agent> (page footer: "Last
updated 2026-08-26 UTC"),
<https://ai.google.dev/gemini-api/docs/interactions>.

### Does it expose an API or endpoint we can reach?

**On the subscription: no, and Google says so.** From
<https://antigravity.google/docs/plans/> under "Other": "There is currently no
support for: Bring-your-own-key or bring-your-own-endpoint for additional rate
limits. Organizational tiers via contract." That cuts both ways. You cannot feed
Antigravity your own key, and Google publishes no endpoint for pointing your own
tools at the subscription-funded harness.

**On the Gemini API: yes.** The Antigravity agent is a first-class agent on the
Interactions API, agent id `antigravity-preview-05-2026`, listed alongside
`deep-research-preview-04-2026` in the Interactions API "Supported models &
agents" table. It is described as "a general-purpose managed agent on the Gemini
API. A single API call gives you an agent that reasons, executes code, manages
files, and browses the web inside your own secure Linux sandbox, hosted by
Google. It is powered by Gemini 3.7 Flash and uses the same harness as the
Antigravity IDE."

That last clause is the interesting one: same harness, different billing rail.

**What the Interactions API is not.** It is not `POST /v1/chat/completions`. It
is `interactions.create` with `agent`, `input`, `agent_config`, `tools`,
`environment`, `previous_interaction_id`, `background`, `store`. Access is via
`google-genai` (Python ≥ 2.3.0) or `@google/genai` (JS ≥ 2.3.0). Documented
limitations that matter for a harness integration:

- `temperature`, `top_p`, `top_k`, `stop_sequences`, `max_output_tokens` all
  return **400**.
- No structured outputs on the Antigravity agent.
- Function calling is **stateful only**: you must use `previous_interaction_id`;
  reconstructing history stateless is not supported.
- `background=True` requires `store=True`.
- Only text and image input.

### Terms around data and training

All three documents below were fetched and read on **2026-08-27**.

#### Which terms apply to which rail

`https://antigravity.google/terms` opens by scoping itself out of the API rail:
"If you are accessing the Service through Gemini Enterprise (Google Cloud),
Gemini Enterprise for Business or a Google Workspace subscription on the Google
Cloud Pre-GA Offering Terms, **or with a Gemini Enterprise Agent Platform API
Key**, then you are subject to the terms of use accepted or signed by your
administrator … and the terms below do not apply to you."

So the split is clean and it is written down:

- `agy` and the IDE on a consumer Google account → **Antigravity Additional
  Terms**.
- The Antigravity agent on the Interactions API via an API key → **Gemini API
  Additional Terms**.

#### Antigravity Additional Terms (consumer rail)

<https://antigravity.google/terms>, accessed 2026-08-27. Relevant clauses,
quoted:

- **§3 (collection):** "we record and store your user data, interaction data
  pertaining to your usage of the Service, related metadata connected to the
  Service, and any feedback you provide ('Interactions')". Deletion is by
  emailing `antigravity-support@google.com`, and until you do, "such
  Interactions will be used in accordance with the terms of this Agreement".
- **§5 (training and human review):** "We use Interactions to evaluate, develop,
  and improve Google and Alphabet research, products, services and machine
  learning technologies … **Google employees and contractors may access, view,
  review and use Interactions.** If you don't want your Interactions used in this
  way, navigate to settings to change your preference on how such data is used."
  There is no Free / Pro / Ultra distinction anywhere in the document. The
  opt-out is a pointer to an unnamed setting; the 2026-08-20 local report found
  the only findable toggle is "Enable Telemetry" under Advanced Settings and
  that its scope is unconfirmed. That gap is still open.
- **§4 (agents):** "You are solely responsible for: (a) the actions and tasks
  performed by an AI Agent … (d) exercising judgment and supervision when and if
  an AI Agent is used in production environments."
- **§6 (third-party access):** see the next section. This is the clause that
  decides Q3.
- **§8:** selecting a third-party model as the main agent model subjects you to
  that vendor's terms, Anthropic's commercial terms named explicitly.

#### The clause that settles the proxy question

Antigravity Additional Terms **§6**, quoted in full because paraphrasing it
would soften it:

> "You must not abuse, harm, interfere with, or disrupt the Service. This
> includes, but is not limited to, using the Service in connection with products
> not provided by us. **Using third party software, tools, or services to access
> the Service (e.g. using OpenClaw with Antigravity OAuth) is a breach of this
> Agreement.** Such actions may be grounds for suspension or termination of your
> account."

Google names OpenClaw specifically. Every `agy`-wrapping OpenAI-compat proxy in
the wild works by borrowing the Antigravity OAuth session, which is exactly the
described pattern. This is not a gray area and not a "risk to weigh". It is a
named breach with account termination as the stated consequence.

The sanctioned path is narrower and it survives §6: running Google's own `agy`
binary, non-interactively, the way Google's own headless docs describe for CI
and cron. That is using the Service through a product Google provides. §6's
first sentence ("in connection with products not provided by us") is broad
enough that a very literal reading could reach even that, but Google publishes
the CI recipe itself on
<https://antigravity.google/docs/cli/headless>, so the narrow reading is the
supportable one. Worth knowing the ambiguity exists rather than pretending it
does not.

#### Gemini API Additional Terms (API rail)

<https://ai.google.dev/gemini-api/terms>, effective 2026-03-23, page last
updated 2026-04-28 UTC, accessed 2026-08-27.

**Unpaid Services** (which includes "the unpaid quota on Gemini API"):

> "Google uses the content you submit to the Services and any generated
> responses to provide, improve, and develop Google products and services and
> machine learning technologies … human reviewers may read, annotate, and
> process your API input and output … **Do not submit sensitive, confidential,
> or personal information to the Unpaid Services.**"

**Paid Services:**

> "Google doesn't use your prompts (including associated system instructions,
> cached content, and files such as images, videos, or documents) or responses
> to improve our products, and will process your prompts and responses in
> accordance with the Data Processing Addendum for Products Where Google is a
> Data Processor. For Paid Services, Google logs prompts and responses for a
> limited period of time, solely for detecting and preventing violations of the
> Prohibited Use Policy … and any required legal or regulatory disclosures."

**What makes it "Paid"** is stated precisely, and it is not about spending
money: "Your access to Gemini API is a 'Paid Service' **only when accessing the
API through a Cloud Project associated with an active billing account**." So the
protection is a billing-account property, not a per-request one. Attach billing
to the project or you are on the Unpaid terms regardless of volume.

**Regional carve-out:** "If you're in the European Economic Area, Switzerland,
or the United Kingdom, the terms under 'How Google uses Your Data' in 'Paid
Services' apply to all Services". A US project does not get that, which is why
the billing-account step is load-bearing here.

**Also relevant, and new since the 2026-08-20 local report**, an "Agentic
Services" section:

> "When using agentic services, including the Computer Use API, you are solely
> responsible for the actions and tasks performed by the service … **You will
> not automatically bypass any requests for human confirmation.**"

That last sentence is a direct constraint on unattended agentic loops. It does
not forbid headless runs, but it does sit awkwardly next to
`--dangerously-skip-permissions` and next to any shim that auto-approves tool
calls on the caller's behalf. Design the shim to preserve confirmations rather
than swallow them.

#### Retention on the API rail

<https://ai.google.dev/gemini-api/docs/interactions>, accessed 2026-08-27:

- `store=true` is the default. Paid tier retains interactions **55 days**; free
  tier **1 day**.
- `store=false` is available per request, but it is incompatible with
  `background` execution and blocks `previous_interaction_id`.
- Paid-tier projects can configure retention to 7 / 14 / 28 / 55 days in AI
  Studio, and can delete interactions programmatically.
- Paid-tier `store=true` requests are viewable in the AI Studio Logs page.

#### The practical split

| | `agy` on the subscription | Interactions API, billed project |
|---|---|---|
| Governing document | Antigravity Additional Terms | Gemini API Additional Terms |
| Used to train | Yes (§5), no tier distinction | No, on Paid |
| Human review | Yes (§5), employees and contractors | Only abuse-detection logging |
| Opt-out | "navigate to settings", unnamed, unconfirmed | Not needed on Paid |
| Third-party proxying | **Named breach (§6)** | Not applicable, it is a public API |
| Retention | not specified; deletion by email request | 55 days default, configurable to 7 |

The 2026-08-20 local report recorded from local files that this machine's
Antigravity auth is `consumer`, not Workspace, which is what puts you on the
left column for `agy` and rules out the Workspace carve-out.

### Free and preview tiers, with limits

From <https://antigravity.google/docs/plans/> (accessed 2026-08-27):

- **All plans**: Gemini 3.1 Pro / 3.5 Flash and other offered models as the core
  agent model, unlimited Tab completions, and "access to all product features,
  such as the Scheduled Tasks and the CLI".
- **Google AI Ultra**: highest quota, refreshed every five hours, highest weekly
  rate limits, access to third-party models.
- **Google AI Pro**: high quota, refreshed every five hours until the weekly
  limit is reached.
- **Not on Pro or Ultra**: "Meaningful quota, refreshed weekly. Weekly rate
  limit."
- Limits are "correlated with the amount of work done by the agent", so prompt
  count is not the unit. And: "Usage limits for this service are subject to
  modification."
- Overage is purchased AI credits, gated by an "AI Credit Overages" setting with
  values Never / Always.

From <https://ai.google.dev/gemini-api/docs/antigravity-agent> (accessed
2026-08-27):

- The Antigravity agent is **in preview**, available "for both free tier and
  paid tier projects". "Free tier projects include a free rate limit and usage
  quota." The doc does not publish the numeric free quota.
- Pricing is pay-as-you-go on underlying Gemini model tokens plus tools. Google's
  own estimates: research and synthesis $0.30-$1.00, document generation
  $0.30-$1.30, process design $0.25-$0.80, data processing $0.70-$3.25, and
  "complex agentic workflows with many tool calls can accumulate 3-5 million
  tokens in a single interaction, with costs up to ~$5".
- "Environment compute (CPU, memory, sandbox execution) is not billed during the
  preview period."
- Budget control: `agent_config.max_total_tokens`, best-effort, returns
  `status: "incomplete"` when hit, resumable by referencing the original
  `interaction id` and `environment_id`.

### Known reliability issues

Two open GitHub issues on `google-antigravity/antigravity-cli` surfaced in
search: **#76** (`agy --print` silently drops stdout on a non-TTY: pipe,
subprocess, or redirect, completing a full model round trip and exiting 0 with
no output) and **#318** (`agy -p` hangs indefinitely in non-TTY headless
environments). **I did not fetch these issue pages directly.** This is a search
summary, and the two issues describe contradictory symptoms, so at least one may
be version-specific or already fixed. If you drive `agy` from a subprocess, test
that exact shape first. The 2026-08-20 local report independently flagged a
related failure mode: quota exhaustion returning a successful empty response
rather than an error.

---

# Q3. Can Antigravity become a custom endpoint for Buzz?

## First, the chain Buzz actually uses

This is all from source on this machine, in
`~/.buzz/REPOS/buzz` (checkout HEAD `631b05c883f58e9533e9038b4669ebdfb1d9cf27`,
"feat: ship Buzz Term (#4347)", **2026-08-03**, which is older than your
installed Buzz.app, so treat it as indicative rather than current) and
`~/.hermes`:

```
Buzz Desktop agent record  managed-agents.json  "model": "custom:omlx:qwen3.8-oq4e"
        │
        ▼  desktop/src-tauri/src/managed_agents/runtime.rs:767
   command.env("BUZZ_ACP_MODEL", model)
        │
        ▼  crates/buzz-acp/src/config.rs:423   #[arg(long, env = "BUZZ_ACP_MODEL")]
   buzz-acp --model <string>
        │
        ▼  crates/buzz-acp/src/acp.rs:735  +  pool.rs:158
   session/set_model   (applied after every session_new_full)
        │
        ▼  acp_adapter/server.py:2570
   HermesACPAgent.set_session_model
        │
        ▼  hermes_cli/models.py:2780  parse_model_input
   provider = "custom:omlx"  |  model = "qwen3.8-oq4e"
        │
        ▼  hermes_cli/runtime_provider.py  resolve_runtime_provider
   providers.<name>.base_url  in  $HERMES_HOME/config.yaml
        │
        ▼
   OpenAI-compatible POST /v1/chat/completions
```

Two things fall out of this immediately.

**One:** Buzz does drive model selection over ACP, using the *unstable*
`session/set_model`. Note that `KnownAcpRuntime.supports_acp_model_switching` is
documented in `discovery/runtime_metadata.rs:36-39` as "Currently unused" because
"env var injection runs unconditionally regardless of this value", and Hermes is
registered as a **Preset**, not a tier-1 compiled runtime
(`discovery/presets.rs:153`: `id: "hermes"`, `command: "hermes-acp"`,
`args: &[]`). Presets carry `model_env_var: None`. So for Hermes the model
travels as `BUZZ_ACP_MODEL` into `buzz-acp`, which then issues
`session/set_model`. A model change still needs Stop → Start in Desktop for the
env var to be re-read, which matches what the local Buzz skill has been saying.

**Two:** whatever Buzz reaches, it reaches **through a Hermes provider entry**.
Buzz has no concept of a base URL. So "make Antigravity an endpoint for Buzz"
is really "make Antigravity a Hermes provider", plus a Buzz-side model string.

The only other route is registering Antigravity as its own Buzz **harness**,
sibling to Hermes rather than behind it. Buzz's loader
(`desktop/src-tauri/src/managed_agents/custom_harnesses.rs`) reads
`<app-data>/custom_harnesses/*.json` with exactly these fields:
`id` (must match `[a-z0-9_][a-z0-9_-]*`), `label`, `command`, `args`, `env`,
optional `installInstructionsUrl` / `installHint`. No install commands, no
avatar URL, both stripped for security. The requirement is that `command` speaks
**ACP JSON-RPC over stdio**.

## The verdict

### Subscription-backed Antigravity as a Buzz endpoint: no. Two independent reasons.

**Reason one, capability.** Google publishes no endpoint and states there is no
bring-your-own-endpoint (<https://antigravity.google/docs/plans/>, accessed
2026-08-27). The subscription-funded harness is reachable only as the `agy`
process on this machine.

**Reason two, and this is the one that closes the door: it is a named breach of
contract.** Third-party projects do exist that reverse-proxy an authenticated
`agy` session into an OpenAI-compatible server on localhost. The 2026-08-20
local report names `krmslmz/antigravity-cli`, `sandeshbagmare/antigravity-cli`,
`jackwener/open-antigravity`, `johnneerdael/antigravity-gateway`, typically on
`localhost:6012/v1/chat/completions`. Every one of them works by borrowing the
Antigravity OAuth session.

Antigravity Additional Terms §6 (<https://antigravity.google/terms>, accessed
2026-08-27): "Using third party software, tools, or services to access the
Service (e.g. using OpenClaw with Antigravity OAuth) is a breach of this
Agreement. Such actions may be grounds for suspension or termination of your
account."

Google names OpenClaw, which is the lineage of the system this stack replaced.
I did not evaluate any of those proxies and I am not recommending them. **Do not
wire one into Hermes, Buzz, FreeLLMAPI, or anything else.** The downside is not
a degraded response, it is losing the Google account the subscription is on.

### `agy` as an Antigravity Buzz harness: no, today

`agy` does not document an ACP mode. Its flag reference
(<https://antigravity.google/docs/cli/headless>) has no `--acp` and no `--stdio`.
Its programmatic surface is `--input-format stream-json` NDJSON over stdin,
which is a different protocol with a different event vocabulary
(`init` / `step_update` / `result`). Making Antigravity a Buzz harness therefore
requires writing an `agy-acp` adapter, the same shape as `codex-acp` or
`pi-acp`. That is a real project, not a config file.

If someone does build it, the Buzz side is then trivial:

```json
{
  "id": "antigravity",
  "label": "Antigravity",
  "command": "agy-acp",
  "args": [],
  "env": {}
}
```

dropped at `~/Library/Application Support/xyz.block.buzz.app/custom_harnesses/antigravity.json`.

### Interactions-API Antigravity as a Buzz endpoint: yes, with a shim you write

This is the only route that reaches a real, official, supported endpoint. It
needs one piece of new code because the protocols do not line up:

| | Interactions API | What every harness in your stack expects |
|---|---|---|
| Call | `interactions.create(agent=…, input=…)` | `POST {base_url}/chat/completions` |
| History | `previous_interaction_id`, server-side | full `messages[]` array per request |
| Tools | server-side agentic loop, own sandbox | `tools[]` + `tool_calls` returned to the caller |
| Sampling | `temperature`/`top_p`/`max_output_tokens` return 400 | routinely sent |
| Streaming | SSE over Interactions | OpenAI chunk stream |
| Discovery | not in models.dev | `GET {base_url}/models` |

I checked the last row on disk:
`~/.hermes/models_dev_cache.json` (4,341,400 bytes, mtime 2026-08-27 14:11)
contains **no** provider key and **no** model id matching `antigravity`. So
nothing in your stack will auto-discover it. Every registration is manual.

There is a second, deeper mismatch worth naming before anyone builds this. The
Antigravity agent *is itself an agent*: it plans, runs code in Google's sandbox,
edits files there, and browses. Putting it behind Hermes means Hermes' own
agentic loop wraps a second agentic loop that has its own filesystem. Hermes has
a bridge for exactly this shape at
`~/.hermes/hermes-agent/agent/acp_openai_bridge.py`, whose docstring says a CLI
"that is an autonomous agent with its own read/edit/execute tools must forward
only Hermes' agent-level tools, because re-offering the overlapping ones makes
Hermes re-run work the agent already finished". That bridge is currently
wired for exactly one provider, `copilot-acp`
(`agent/copilot_acp_client.py`, `api_mode="copilot_acp"`). **Treat Antigravity
as a delegation target, not as a chat model.**

## Is there one integration point that serves all five?

**No, not as your stack is configured today.** Here is the actual reachability
map, read from the config files on disk:

| Harness | Points at `:3100` (FreeLLMAPI) today? | Evidence |
|---|---|---|
| Hermes root | Yes | `~/.hermes/config.yaml` `providers.freellmapi` |
| Hermes, all 12 profiles | Yes | every `~/.hermes/profiles/*/config.yaml` has its own `providers.freellmapi` block |
| Buzz | Yes, transitively (it is Hermes) | via `custom:freellmapi:<model>` |
| OpenCode | **No** | `~/.config/opencode/opencode.json` has only `omlx-local` and `mlx-local`; cloud providers come from `auth.json` |
| Pi | **No** | `~/agent-reports/freellmapi-install/pi-config-backup/models.json.bak-20260820-160821` has `mesh`, `qwen-local`, `omlx` |

So **FreeLLMAPI at `:3100` is the closest thing to a single integration point,
and it covers Hermes and Buzz completely, but not OpenCode or Pi.** If you want
one place, the move is two-step: register the shim once in FreeLLMAPI, then
separately add a `freellmapi` provider block to OpenCode and Pi so that
everything downstream inherits future backends for free. That second step is
worth doing on its own merits, independent of Antigravity.

One important caveat about routing through `:3100`. Hermes' `freellmapi`
provider block sets `extra_headers: {X-Sensitivity: public}` in the root config
and in all 12 profile configs. The gateway's `resolvePool`
(`~/agent-reports/freellmapi-install/gateway/gateway.mjs`, Layer 2, around
line 438) maps `public` → the `full` pool and honors the caller's own `model`
without rewriting it. So **all Hermes traffic through the gateway is labeled
public and reaches the unrestricted pool by default**, with only the Layer 1
denylist and the Layer 3 PII backstop able to push it down to `notrain`. That is
a pre-existing property of your config, not something Antigravity introduces,
but it is exactly the property that decides whether adding a Google-backed model
to the `Default` profile is safe.

Also note the standing drift risk recorded in
`~/agent-reports/freellmapi-install/PROFILE-POLICY.md`: `notrain` is policy-
defined as **Groq, Requesty, Cloudflare, OVH only**, and
`catalog-sync`'s `ensureAllModelsInProfiles` has twice re-added every model to
every profile. A new custom endpoint could land in `notrain` on the next sync
even if you register it only in `Default`. Check drift after any registration.

---

# The wiring proposal

Feasible, with one piece of new code. Nothing below has been applied.

## How adding a backend actually goes wrong

Worth stating before the steps, because in this stack the failure modes have
cost more time than the wiring. Each of these is a real incident on this
machine, not a hypothetical.

**1. A partial config write invalidates the whole file and hides everything.**
On 2026-08-26 an automated writer added a `qwen3.8-oq4e` model block to
`~/.config/opencode/opencode.json` carrying `limit.context` but not
`limit.output`. OpenCode 1.18.20's schema requires **both** whenever a `limit`
object is present. The strict config path (`opencode models`, the TUI picker,
any fresh session's provider enumeration) aborts the entire config load on a
schema violation, so **all eight providers disappeared**, including six cloud
providers that live in `auth.json` and have no `provider` block at all. The
lenient serve path tolerated it, which is why it looked intermittent rather than
broken. One missing sub-key on one model in one provider took out every
provider. Full writeup:
`~/agent-workspace/knowledge/opencode-config-providers-rootcause-2026-08-27.md`.

The generalizable lesson: **`limit` is optional, but a partial `limit` is
fatal.** Omit the object entirely when you do not know the real numbers. The
sibling `qwen3.8` entry has no `limit` and is valid. Do not guess a `context`
and leave `output` for later.

**2. Config writers fight each other and last write wins silently.** The same
class of bug hit `~/.hermes/config.yaml` the same week, by a different
mechanism: a brute-force YAML rewrite dropped `mcp_servers` entries and left the
per-profile `~/.hermes/profiles/*/config.yaml` files empty, so
`hermes profile list` showed no model at all. The fix was to stop hand-editing
and use `hermes -p <profile> config set …`. Recorded in
`~/agent-mesh/WORKLOG.md` at 2026-08-27 ~19:00 and D-017.

**3. Catalog sync re-adds your model everywhere.** FreeLLMAPI's
`reinstateUpstreamRetiredCatalogModel()` re-enabled models in **every** profile
with no profile filter, twice bloating the curated `notrain`, `code` and
`business` pools to 271 of 274 models, making them functionally identical to
`Default`. The code path is fixed, but the failure is what makes the drift check
in Step 2 mandatory rather than optional. See
`~/agent-reports/freellmapi-install/PROFILE-POLICY.md`.

**4. A bare model id resolves against whatever provider is current.**
`parse_model_input` only treats the text before a colon as a provider if it
recognizes it. A Hugging Face repo id or a short card name therefore resolves
against the *current* provider, which is how a Buzz agent named after a local
MLX model ends up answering from a hosted provider, or 404ing on a repo lookup.
Always the provider-qualified triple.

So, three rules for everything below: **write complete objects or omit them,
write through the tool that owns the file, and re-check membership after any
sync.**

## Step 0. Decide the rail, because it decides the data posture

| Rail | Cost | Data posture | Verdict |
|---|---|---|---|
| `agy` on the AI Pro/Ultra subscription | already paid | Antigravity Terms §5: trains, employees and contractors may review, opt-out is an unnamed setting | Public, non-sensitive work only. Never claim-adjacent. Subprocess only, never proxied (§6). |
| Interactions API, project **with an active Cloud billing account** | pay-as-you-go, roughly $0.25 to $5 per task | Gemini API Paid Services: no training, abuse-detection logging only, 55-day retention configurable down to 7, `store=false` available | The only rail worth wiring into infrastructure |
| Interactions API, project **without** billing attached | free quota | Gemini API Unpaid Services: trains, human reviewers, and Google's own instruction is "Do not submit sensitive, confidential, or personal information" | Throwaway experiments only |

Note the second and third rows differ by **one billing-account setting**, not by
spend. Per the Gemini API Additional Terms, "Your access to Gemini API is a
'Paid Service' only when accessing the API through a Cloud Project associated
with an active billing account." Attaching billing is the single step that moves
you from the training-permitted column to the training-excluded one. Verify it
before the first real request, not after.

The rest of this proposal assumes the billed Interactions API rail.

## Step 1. Build the shim (the only new code)

### The upstream call it wraps

Verified from <https://ai.google.dev/gemini-api/docs/managed-agents-quickstart>
(page footer: last updated 2026-08-26 UTC, accessed 2026-08-27). This is the
whole upstream contract:

```sh
curl -X POST "https://generativelanguage.googleapis.com/v1beta/interactions" \
  -H "Content-Type: application/json" \
  -H "x-goog-api-key: $GEMINI_API_KEY" \
  -d '{
    "agent": "antigravity-preview-05-2026",
    "input": [{"type": "text", "text": "Reply with exactly: PONG"}],
    "environment": {"type": "remote"}
  }'
```

Response carries `id`, `environment_id`, `output_text`, and `steps`. Multi-turn
is two independent dimensions, which is the part that does not map cleanly onto
`messages[]`:

- **conversation** continues with `previous_interaction_id`
- **filesystem** continues with `environment: "<environment_id>"`

You can mix them: omit `previous_interaction_id` and keep `environment` for a
fresh conversation in the same workspace, or the reverse. Streaming is
`"stream": true` on the same endpoint, emitting step deltas with a `step.stop`
event carrying usage. Files the agent wrote come back as a tarball from
`GET https://generativelanguage.googleapis.com/v1beta/files/environment-$ENV_ID:download?alt=media`.

### The shim itself

A small local server exposing an OpenAI-compatible surface and translating to
`interactions.create`.

- Listen on **loopback only**, `127.0.0.1:8310` (pick any free port; `:8300` is
  omlx, `:3100` is FreeLLMAPI, `:9337` is Buzz mesh, `:11434` is the MLX local
  entry, `:8787` is Hermes WebUI, `:8765` is X intake).
- Implement `GET /v1/models` returning one entry,
  `antigravity-preview-05-2026`, and `POST /v1/chat/completions`.
- Map the last user message to `input`; map prior turns to
  `previous_interaction_id` held in a small in-process map keyed by a
  conversation id. Do not try to replay full history: the Interactions API
  requires stateful mode for function calling.
- Drop `temperature`, `top_p`, `top_k`, `stop_sequences`, `max_output_tokens`
  before forwarding. They 400.
- Set `agent_config.max_total_tokens` from a config value so a runaway agentic
  loop cannot spend $5 unattended. Surface `status: "incomplete"` as a finish
  reason the caller can see.
- Read the key from the environment. Per `~/agent-mesh/AGENTS.md`, the key
  belongs in `~/.hermes/.env` or Keychain and is referenced by variable name
  only. Suggested name: `GEMINI_API_KEY` (which is what the Antigravity SDK
  reads natively) or a dedicated `HERMES_CUSTOM_ANTIGRAVITY_API_KEY`.
- Run it under launchd, following the existing `com.mike.freellmapi-server`
  pattern, not a new supervisor. Agent-mesh's hard line is explicit about not
  standing up a second scheduler.

**Verify (not run in this session):**

```sh
curl -s http://127.0.0.1:8310/v1/models | jq -r '.data[].id'
# expect: antigravity-preview-05-2026

curl -s http://127.0.0.1:8310/v1/chat/completions \
  -H 'content-type: application/json' \
  -d '{"model":"antigravity-preview-05-2026","messages":[{"role":"user","content":"Reply with exactly: PONG"}]}' \
  | jq -r '.choices[0].message.content'
# expect: PONG
```

## Step 2. Register once in FreeLLMAPI (covers Hermes and Buzz)

FreeLLMAPI has a first-class custom-endpoint registration path. From
`~/agent-reports/freellmapi-install/freellmapi/server/src/routes/keys.ts:918`
(`keysRouter.post('/custom')`, mounted at `/api/keys` behind `requireAuth` per
`server/src/app.ts:226`) and
`server/src/services/custom-model-register.ts`:

```jsonc
// POST https://<freellmapi-host>/api/keys/custom     (auth required)
{
  "baseUrl": "http://127.0.0.1:8310/v1",
  "label": "Antigravity (Gemini Interactions API)",
  "apiKey": "<referenced by name only; never paste a value into a repo>",
  "models": [
    {
      "model": "antigravity-preview-05-2026",
      "displayName": "Antigravity Agent (preview)",
      "supportsTools": true,
      "supportsVision": true
    }
  ]
}
```

Notes from the source, not from docs:

- Keys are matched on `(base_url, secret)`, so a second key for a known endpoint
  **inserts** rather than overwrites (`custom-endpoint.ts` header comment).
- `baseUrl` passes through `rejectUnsafeBaseUrl` → `assessProviderUrl`
  (`keys.ts:773`). Confirm loopback is accepted before assuming this works.
- New custom models seed their routing ranks at the catalog median
  (`customModelSeed`), so the model gets explored rather than buried.
- There is a **credential-only** add path when the endpoint already has models
  registered (`keys.ts`, "#702").

**Then decide the pool deliberately.** Per
`~/agent-reports/freellmapi-install/PROFILE-POLICY.md`, `Default` is the
unrestricted pool reached only by `X-Sensitivity: public`; `notrain` is
Groq/Requesty/Cloudflare/OVH only. Leaving Antigravity in `Default` alone is
the conservative choice. Adding it to `notrain` would require re-confirming
Google's retention policy and updating three places together: that policy file,
the Layer 2 comment in `gateway.mjs`, and `CURATED_NOTRAIN_PLATFORMS` in
`server/src/services/model-state.ts`.

**Verify (not run in this session):**

```sh
# 1. It appears in the gateway's catalog
curl -s http://127.0.0.1:3100/v1/models | jq -r '.data[].id' | grep -i antigravity

# 2. Profile membership is what you intended, and nothing drifted
DB=~/agent-reports/freellmapi-install/freellmapi/server/data/freeapi.db
sqlite3 "$DB" "SELECT p.name, m.platform, m.model_id FROM profile_models pm
  JOIN models m ON m.id = pm.model_db_id JOIN profiles p ON p.id = pm.profile_id
  WHERE pm.enabled = 1 AND m.model_id LIKE 'antigravity%';"

# 3. notrain has not silently absorbed it
sqlite3 "$DB" "SELECT p.name, m.platform, COUNT(*) FROM profile_models pm
  JOIN models m ON m.id = pm.model_db_id JOIN profiles p ON p.id = pm.profile_id
  WHERE p.name IN ('notrain','code','business') AND pm.enabled = 1
  GROUP BY p.name, m.platform ORDER BY p.name, m.platform;"
# notrain should show only cloudflare/groq/ovh/requesty
```

## Step 3 (alternative to 2). Register directly as a Hermes provider

If you would rather not put it behind the gateway, the direct shape is a
`providers:` entry. The accepted key set is exact and comes from
`hermes_cli/config.py:1419` (`_KNOWN_KEYS` in
`_normalize_custom_provider_entry`): `provider`, `name`, `api`, `url`,
`base_url`, `api_key`, `key_env`, `api_key_env`, `key_cmd`, `api_mode`,
`transport`, `model`, `default_model`, `models`, `models_discovered`,
`context_length`, `rate_limit_delay`, `request_timeout_seconds`,
`stale_timeout_seconds`, `discover_models`, `extra_body`, `extra_headers`,
`ssl_ca_cert`, `ssl_verify`. Anything else logs "unknown config keys ignored".

```yaml
# $HERMES_HOME/config.yaml  ::  PROPOSED, do not apply without Mike's go-ahead
providers:
  antigravity:
    name: Antigravity Agent (Gemini Interactions API)
    api: http://127.0.0.1:8310/v1
    base_url: http://127.0.0.1:8310/v1
    api_mode: chat_completions
    transport: chat_completions
    default_model: antigravity-preview-05-2026
    key_env: HERMES_CUSTOM_ANTIGRAVITY_API_KEY   # name only, never a value
    discover_models: true
    models:
      antigravity-preview-05-2026:
        context_length: 131072   # placeholder: not published; measure it

model_overrides:
  antigravity:
    antigravity-preview-05-2026:
      supports_tools: true
      supports_vision: true
      supports_reasoning: false
      max_output_tokens: 8192
```

**This is per-profile, not global.** I confirmed there is no inheritance:
`get_hermes_home()` (`hermes_constants.py:114`) resolves to the profile
directory and `load_config()` reads `config.yaml` from there. Every one of
`~/.hermes/profiles/{coach,hermes-analyst,hermes-research,hermes-scout,local,morning-brief,prime,qwen38-oq4e-full,qwen38-oq4e-mid,qwen38-oq4e-short,scout,sentinel}/config.yaml`
already carries its own full copy of the `omlx` and `freellmapi` provider
blocks. Adding a provider to root reaches root sessions only. That is 13 edits
if you want it everywhere, which is a strong argument for Step 2 instead.

Two related observations while I was in those files, both worth a separate
decision and neither touched by me:

- The omlx `api_key` value is stored **in plaintext** in the root `config.yaml`
  and duplicated into every profile config. It is a local loopback key so the
  blast radius is small, but it contradicts the `AGENTS.md` "reference by name
  only" line, and `key_env` exists for exactly this.
- The root config's `model_overrides.omlx` contains both a correct
  `qwen3.8-oq4e` block and a malformed `qwen3:` → `8-oq4e:` nested block, which
  looks like a dotted-key splitter artifact of the kind
  `model-routing.md` warns about ("do not `hermes config set` nested keys whose
  path segments contain `.`"). Harmless but dead.

**Verify (not run in this session):**

```sh
hermes config get providers | grep -A6 antigravity
hermes -p prime chat --provider antigravity \
  --model antigravity-preview-05-2026 -q 'Reply with exactly: PONG'
```

## Step 4. Point Buzz at it

No Buzz config change beyond the model string. Set the Hermes agent's model in
Buzz Desktop to the provider-qualified triple, then Stop → Start:

```
custom:antigravity:antigravity-preview-05-2026
```

or, if you went the FreeLLMAPI route:

```
custom:freellmapi:<the id the gateway lists>
```

Owner-reviewed CLI path, when `BUZZ_PRIVATE_KEY` is available:

```sh
buzz agents draft-update \
  --channel <channel-uuid> \
  --agent-name hermes \
  --runtime hermes \
  --model 'custom:antigravity:antigravity-preview-05-2026'
```

Never a bare model id. `parse_model_input` resolves a bare string against the
*current* provider, which is how you get the "hosted provider answers a local
model name" failure the Buzz skill documents.

**Verify (not run in this session):**

```sh
python3 - <<'PY'
import json
from pathlib import Path
p = Path.home()/"Library/Application Support/xyz.block.buzz.app/agents/managed-agents.json"
for a in json.loads(p.read_text()):
    if a.get("runtime") == "hermes":
        print(a.get("name"), "model=", a.get("model"), "pubkey_set=", bool(a.get("pubkey")))
PY

ps -axo pid,ppid,command | grep -E 'buzz-acp|hermes-acp' | grep -v grep

rg -n 'set_model|steering_supported|ERROR' \
  "$HOME/Library/Application Support/xyz.block.buzz.app/agents/logs/"* | tail -20
```

## Step 5. OpenCode

Separate wiring. Schema is OpenCode's own, and it is strict: a `limit` object
must carry **both** `context` and `output`, which is exactly what broke your
providers on 2026-08-26 and was fixed on 2026-08-27
(`~/agent-workspace/knowledge/opencode-config-providers-rootcause-2026-08-27.md`).

```jsonc
// ~/.config/opencode/opencode.json  ::  PROPOSED
"antigravity": {
  "npm": "@ai-sdk/openai-compatible",
  "name": "Antigravity Agent (Interactions API)",
  "options": { "baseURL": "http://127.0.0.1:8310/v1", "apiKey": "{env:ANTIGRAVITY_SHIM_KEY}" },
  "models": {
    "antigravity-preview-05-2026": {
      "name": "Antigravity Agent (preview)",
      "limit": { "context": 131072, "output": 8192 }
    }
  }
}
```

Ownership note: `opencode.json`'s local-provider blocks are agent-mesh's
surface under the 2026-08-27 ruling. Propose, do not land.

**Verify (not run in this session):**

```sh
opencode models | grep -i antigravity
opencode run -m antigravity/antigravity-preview-05-2026 "reply with exactly: OPENCODE_OK"
```

## Step 6. Pi

Separate again. Shape taken from your own backup at
`~/agent-reports/freellmapi-install/pi-config-backup/models.json.bak-20260820-160821`.
Note `~/.config/pi` does not exist on this machine, so I could not confirm the
live path; find it with `pi --help` or by locating the file that backup was
taken from.

```jsonc
"antigravity": {
  "api": "openai-completions",
  "apiKey": "antigravity",
  "baseUrl": "http://127.0.0.1:8310/v1",
  "models": [{
    "contextWindow": 131072,
    "id": "antigravity-preview-05-2026",
    "input": ["text"],
    "maxTokens": 8192,
    "name": "Antigravity Agent (preview)",
    "reasoning": false
  }]
}
```

## Step 7. The honest alternative, if the shim is not worth it

Skip all of the above and use the sanctioned subprocess path. It is officially
supported, needs no new server, and costs nothing beyond the subscription you
already pay for. It is not an endpoint, so nothing in Hermes' provider model
applies. Hermes reaches it through the existing `terminal` tool, exactly as the
`antigravity-cli` skill already describes:

```sh
agy -p 'Review this diff for bugs and security issues' \
  --model gemini-3.1-pro-high \
  --output-format json \
  --print-timeout 15m
```

Correct the skill's stale lines first (see the table in Q2), then this is a
one-line change to how workers invoke it. This is the right answer for public,
non-sensitive second opinions. It is the wrong answer for anything that touches
VA or SSDI content, for the data reasons in Q2.

---

## Step 8. The option you did not ask about, which may beat both

While reading the quickstart I found something that fits your stack better than
either route above. Managed agents can be **saved server-side with your own
instructions and skills mounted from a git repo**
(<https://ai.google.dev/gemini-api/docs/managed-agents-quickstart>, "Save a
managed agent", accessed 2026-08-27):

```sh
curl -X POST "https://generativelanguage.googleapis.com/v1beta/agents" \
  -H "Content-Type: application/json" \
  -H "x-goog-api-key: $GEMINI_API_KEY" \
  -d '{
    "id": "scout-remote",
    "base_agent": "antigravity-preview-05-2026",
    "agent_config": {"type": "antigravity", "model": "gemini-3.7-flash"},
    "system_instruction": "<the SOUL.md content for that bot>",
    "base_environment": {
      "type": "remote",
      "sources": [
        {"type": "inline", "target": ".agents/AGENTS.md", "content": "<house rules>"},
        {"type": "repository", "source": "https://github.com/redtrades/agent-configs", "target": ".agents/skills"}
      ]
    }
  }'
```

Note the target paths: `.agents/AGENTS.md` and `.agents/skills`. That is the
same convention your local `~/.agents/skills` uses, which Hermes already reads
through `skills.external_dirs` in `config.yaml`. So the same skill corpus can
run locally on omlx and remotely in Google's sandbox without a second format.

Each invocation forks the base environment, so runs start clean. There are also
**triggers**: a cron schedule bound to an agent, environment and prompt, with
`max_consecutive_failures` (default 5) and `execution_timeout_seconds` (default
600), and every execution reuses the same environment so files persist between
runs (<https://ai.google.dev/gemini-api/docs/antigravity-agent>, "Triggers").

That is a second scheduler, which runs straight into the agent-mesh hard line
about not standing up a daemon or scheduler next to an existing one. Hermes
already has `hermes cron` and your four bot routines are registered there,
paused. If remote scheduling is ever wanted, the right shape is a Hermes cron
job that fires the interaction, not a Google-side trigger running in parallel
with Hermes' own. Flagging it as available, not recommending it.

This route sidesteps the whole shim problem for delegation-shaped work, because
you stop pretending Antigravity is a chat model and start treating it as what it
is: a remote worker you hand a task to. It does not help if what you actually
want is a model behind Buzz's picker.

# What I could not verify

Listed plainly rather than smoothed over.

| Claim | Why unverified | How to close it |
|---|---|---|
| `agy` non-TTY issues #76 and #318 | Search-result summary only; I did not fetch either issue page, and their symptoms contradict each other (one says silent empty output with exit 0, the other says an indefinite hang), so at least one is likely version-specific or fixed | Fetch both issues, or just test your exact subprocess shape |
| Whether `agy` is installed on this machine and at what version | I have no host shell, and a mount request for `~/.gemini` was refused. The 2026-08-20 report found **no** `agy` binary and `~/.gemini/antigravity-cli/` absent, with Antigravity.app v2.8.1 onboarded; docs now show the app at v2.11.0, so it has moved since | `command -v agy && agy --version && agy models` |
| Whether the Antigravity opt-out setting referenced in Terms §5 actually stops training, human review, both, or neither | The terms say "navigate to settings" without naming the setting. The 2026-08-20 report found only an "Enable Telemetry" toggle under Advanced Settings, with open unanswered forum threads about its scope | Ask Google support, or treat it as ineffective and keep sensitive content off that rail |
| Current Buzz.app version and whether its harness registry matches the source I read | The `~/.buzz/REPOS/buzz` checkout is HEAD `631b05c`, **2026-08-03**. `~/Library/Application Support/xyz.block.buzz.app` cannot be mounted (protected location) | `git -C ~/.buzz/REPOS/buzz pull`, and read the live `managed-agents.json` yourself |
| Live Buzz agent records, model strings, and logs | Same mount refusal | The `python3` snippet in Step 4 |
| Pi's live config path and current providers | `~/.config/pi` does not exist; I only had a 2026-08-20 backup under `agent-reports` | `pi --help`, then read the real file |
| Whether `assessProviderUrl` permits a loopback `baseUrl` | Read the call site (`keys.ts:773`) but not the implementation in `server/src/lib/` | Read `assessProviderUrl`, or just try the POST and read the 400 |
| Real context window and output ceiling for `antigravity-preview-05-2026` | Not published. The 131,072 / 8,192 figures above are **placeholders**. The docs do say context compaction triggers around 135k tokens | Measure, then set `context_length` from the measurement |
| Whether Antigravity's Interactions agent is usable at all as a chat-completions backend | This is the load-bearing design risk, not a fact gap. It is an agent with its own sandbox, not a model | Build the shim behind a feature flag and run one real Hermes turn before wiring anything else |

## Provenance key

- **Local code, read this session:** everything in Q1's method and handler
  tables, the `parse_model_input` and `_make_agent` behavior, the Buzz chain in
  Q3, the Buzz custom-harness schema, the Hermes `_KNOWN_KEYS` provider schema,
  the per-profile config independence, the FreeLLMAPI `POST /api/keys/custom`
  shape and pool routing, the OpenCode and Pi config shapes, and the absence of
  `antigravity` from `models_dev_cache.json`.
- **Vendor documentation, fetched 2026-08-27:** everything about `agy` flags and
  output formats, the four Antigravity surfaces and their versions, the plans
  and quota table, the no-BYO-endpoint statement, the Antigravity agent
  capabilities and pricing estimates, the Interactions API retention windows and
  limitations, the `POST /v1beta/interactions` REST shape, and **every quoted
  clause from both terms documents**.
- **Prior local reports, not re-verified this session:** the third-party proxy
  project names, the "Enable Telemetry is the only findable toggle" finding, and
  the 2026-08-20 machine-state snapshot (Antigravity.app v2.8.1 onboarded,
  `auth_method: consumer`, `useAiCredits: False`, no `agy` binary). Each is
  attributed inline.

Reading-access note: `~/.hermes`, `~/.buzz`, `~/.agents` and
`~/.config/opencode` were mounted and read in full earlier in this session, and
every claim attributed to them was taken then. Those mounts were dropped later
in the session, so I could not re-open them for a second pass. `~/.gemini` was
never grantable, and `~/Library/Application Support/xyz.block.buzz.app` is a
protected location that cannot be mounted at all, which is why the live Buzz
agent records are in the unverified table rather than quoted.

## Sources

Vendor documentation, all accessed 2026-08-27:

- Antigravity headless mode: <https://antigravity.google/docs/cli/headless>
- Antigravity plans and quota: <https://antigravity.google/docs/plans/>
- Antigravity SDK overview: <https://antigravity.google/docs/sdk/overview/>
- Antigravity agent on the Gemini API: <https://ai.google.dev/gemini-api/docs/antigravity-agent> (page footer: last updated 2026-08-26 UTC)
- Interactions API: <https://ai.google.dev/gemini-api/docs/interactions>
- Managed agents quickstart, source of the REST shape: <https://ai.google.dev/gemini-api/docs/managed-agents-quickstart> (page footer: last updated 2026-08-26 UTC)
- Antigravity Additional Terms of Service: <https://antigravity.google/terms>
- Gemini API Additional Terms of Service: <https://ai.google.dev/gemini-api/terms> (effective 2026-03-23, page footer: last updated 2026-04-28 UTC)
- Agent Client Protocol schema: <https://agentclientprotocol.com/protocol/schema>

Referenced but not read this session, listed so they are easy to close out:

- <https://github.com/google-antigravity/antigravity-cli/issues/76>
- <https://github.com/google-antigravity/antigravity-cli/issues/318>
- <https://antigravity.google/docs/cli/reference> (full flag reference)
- <https://ai.google.dev/gemini-api/docs/custom-agents> (saving a managed agent with your own `.agents/skills`)

Local files (paths, since they are not linkable):

- `~/.hermes/hermes-agent/acp_adapter/{entry,server,session,auth,permissions}.py`
- `~/.hermes/hermes-agent/venv/lib/python3.11/site-packages/acp/{meta.py,agent/router.py}`
- `~/.hermes/hermes-agent/hermes_cli/{main.py,models.py,config.py,auth.py,runtime_provider.py}`
- `~/.hermes/hermes-agent/hermes_constants.py`
- `~/.hermes/hermes-agent/plugins/model-providers/README.md`, `.../gemini/__init__.py`, `.../copilot-acp/__init__.py`
- `~/.hermes/hermes-agent/agent/acp_openai_bridge.py`
- `~/.hermes/config.yaml`, `~/.hermes/profiles/*/config.yaml`, `~/.hermes/models_dev_cache.json`
- `~/.hermes/skills/autonomous-ai-agents/antigravity-cli/SKILL.md`
- `~/.hermes/skills/autonomous-ai-agents/hermes-buzz-integration/SKILL.md` and `references/model-routing.md`
- `~/.buzz/REPOS/buzz/desktop/src-tauri/src/managed_agents/{runtime.rs,custom_harnesses.rs,discovery.rs,discovery/presets.rs,discovery/runtime_metadata.rs,config_bridge/{types.rs,reader.rs}}`
- `~/.buzz/REPOS/buzz/crates/buzz-acp/src/{config.rs,acp.rs,pool.rs}`
- `~/.config/opencode/opencode.json`
- `~/agent-reports/freellmapi-install/{PROFILE-POLICY.md,gateway/gateway.mjs,pi-config-backup/models.json.bak-20260820-160821}`
- `~/agent-reports/freellmapi-install/freellmapi/server/src/{app.ts,routes/keys.ts,services/{custom-endpoint.ts,custom-model-register.ts}}`
- `~/agent-reports/google-subscription-antigravity/google-subscription-antigravity-2026-08-20.md`
- `~/agent-reports/acp-harness-comparison/report.md`
- `~/agent-reports/freellmapi-evaluation/freellmapi-evaluation-2026-08-20.md`
- `~/agent-workspace/knowledge/{opencode-config-providers-rootcause-2026-08-27.md,freellmapi-gateway-403-removal-and-model-aliases-2026-08-24.md}`
- `~/agent-mesh/{AGENTS.md,DECISIONS.md,WORKLOG.md,HANDOFF.md}`
