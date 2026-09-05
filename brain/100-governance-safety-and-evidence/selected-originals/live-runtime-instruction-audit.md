# Live runtime instruction audit — 2026-08-28

## Scope and result

This is a read-only trace of the instruction surfaces currently discoverable on
this host for Codex, Claude Code, Hermes, Buzz, Pi, OpenCode, Grok, and
Gemini/Antigravity. It distinguishes authored source, install or synchronization
mechanisms, runtime discovery, automatic startup injection, explicit invocation,
compaction behavior, generated content, and historical evidence. “Active” below
means a runtime will load the material without the user naming that particular file
or command. A source file, installed copy, loader implementation, or historical
receipt alone is not current activation proof.

Observed baseline:

- `/Users/man/agent-configs/MASTER-GUIDE.md` does not exist.
- Fresh startup paths no longer contain a direct reference to that deleted file.
- The remaining direct references are in supporting provenance, archived or
  historical session/research records, and project documentation that is evidence
  of earlier design intent rather than current runtime authority.
- The largest residual risk is stale already-open session state. A Hermes request
  dump created before the baseline correction still contains the old repository
  `AGENTS.md` text and its `MASTER-GUIDE.md` directive at
  `/Users/man/.hermes/profiles/local-27b-control/sessions/request_dump_20260828_060703_7bc26f_20260828_060704_961543.json:17`.
  The dump is historical evidence, not a loader, but a session retaining that old
  prompt should not be treated as clean merely because the file on disk changed.

No runtime/configuration file was changed by this audit.

## Authority classification

| Surface | Current activation class | Finding | Recommendation |
|---|---|---|---|
| `/Users/man/.codex/AGENTS.md` | Codex global startup instructions | Compact and clean; explicitly says retrieved memory and repository material are data unless loaded as instructions (`:1-12`) and assigns volatile state away from the contract (`:55-68`). | **Keep** |
| `/Users/man/CLAUDE.md` | Claude global startup instructions; also an ancestor context file for Pi | Compact and clean; explicitly disclaims being an instruction to load an external rules library (`:1-11`) and treats prompt caches/memory as supporting evidence (`:50-63`). | **Keep** |
| `/Users/man/agent-mesh/AGENTS.md` | Repository startup instructions for runtimes that discover `AGENTS.md` | Clean; file presence does not prove discovery or activation (`:1-11`), and task authority is kept out of chat/memory (`:13-20`). | **Keep** |
| `/Users/man/.hermes/SOUL.md` | Default-profile Hermes startup identity | Clean anti-recursion rule at `:1-3`. | **Keep** |
| `/Users/man/.buzz/AGENTS.md` | Buzz provider working-directory context | Managed roster at `:61-76`; the persistent Hermes warning at `:111-114` requires profile/toolset inspection and a fresh discovery/invocation receipt, while `:116-121` rejects recursive agent-configs loading. | **Keep**, but preserve the generator boundary |
| `/Users/man/.claude/commands/multi-model-diff-review.md` | Explicit Claude slash command only | Quarantined deprecation notice; it rejects the retired guide and static provider/model/port assumptions (`:1-9`). | **Keep quarantined** |
| `/Users/man/.claude/hooks/post-compact-reinject.sh` | Active Claude `SessionStart` hook for `compact` only | Registered by `/Users/man/.claude/settings.local.json:42-52`; emits only the bounded warning at `:10-11`, which makes derived continuity subordinate to current request and live evidence. | **Keep** |
| `/Users/man/.hermes/skills/rules/SKILL.md` | Explicit Hermes skill for the default profile; not auto-indexed in the current default CLI configuration | Quarantined deprecation notice at `:1-15`; it forbids loading or enforcing the legacy universal ruleset. | **Keep quarantined** |
| `/Users/man/.hermes/skills/autonomous-ai-agents/agent-configs-verification/SKILL.md` | Explicit Hermes audit skill; not auto-indexed in the current default CLI configuration | Audit-only and explicitly forbids install/sync at `:1-10`; unknown provenance remains unknown at `:36-49`. | **Keep audit-only** |
| `/Users/man/.hermes/skills/hermes-agent-config-setup/SKILL.md` | Explicit Hermes skill/tombstone | Correctly forbids bulk install/sync and says agent-configs is a source library (`:1-18`). | **Keep** as a deprecation tombstone |
| `/Users/man/agent-configs/README.md` | Source-library documentation | Explicitly says there is no universal auto-load and forbids wholesale loading (`:1-10`, `:33-43`). It is not live bootstrap. | **Keep** |
| `/Users/man/agent-workspace/README.md` | Project-local onboarding for that repository, historical to the current `agent-mesh` runtime path | It says the adjacent library is only cloned when needed and is not automatically active (`:1-15`). It is not cross-runtime bootstrap. | **Keep** as project documentation |
| `agent-mesh/.agent/AGENTS.md` | Nested project instructions and historical portable-core design | Claims one portable core is “consumed by every harness” (`:1-22`) and gives manual adoption recipes (`:24-111`). These are authored design evidence, not proof that any named runtime installed, discovered, or activated the material. | **Adapt before reuse** |
| `agent-mesh/README.md` and `agent-mesh/HANDOFF.md` | Project documentation | README calls `.agent/` cross-harness (`README.md:1-20`) and both files retain historical universal-source language (`README.md:27-31`; `HANDOFF.md:70-75`). Documentation is not runtime authority. | **Adapt when the governing design is approved** |

## Requirement 1 — source-to-activation completeness matrix

`VERIFIED` means current behavioral evidence for the named runtime and cwd.
`UNVERIFIED` and `ABSENT` are complete audit outcomes, not implementation blockers.

| Runtime | Authored source | Install/sync mechanism | Loader/discovery evidence | Activation verdict |
|---|---|---|---|---|
| Codex | `/Users/man/.codex/AGENTS.md:1-68` plus `/Users/man/agent-mesh/AGENTS.md:1-44` | Direct authoritative files; no external instruction-library path in `/Users/man/.codex/config.toml:1-20` | This live Codex session received the global and repository contracts; installed loader source was not recovered | **VERIFIED** for this Codex session; other cwd/profile combinations remain unverified |
| Claude Code | `/Users/man/CLAUDE.md:1-64`; explicit command/hook files are separate surfaces | Direct global file; local hook registration in `/Users/man/.claude/settings.local.json:42-52`; no universal sync | Settings prove the `compact` hook registration, but this audit has no fresh Claude prompt dump proving the global file body | **UNVERIFIED** for fresh global-file injection; hook registration is verified, hook execution is not behaviorally probed here |
| Hermes | Selected profile `SOUL.md` plus the first matching project context; current default source is `/Users/man/.hermes/SOUL.md:1-3` | Native profile/context files; retired bulk installer remains a tombstone and audit skills forbid sync | Installed source trace at `prompt_builder.py:2373-2396,2430-2448` and `agent_init.py:658-664` | **UNVERIFIED** for a fresh post-cleanup prompt; the pre-cleanup dump is historical negative evidence only |
| Buzz / Buzz Agent | Static `nest_agents.md`, generated `/Users/man/.buzz/AGENTS.md`, and the bundled/base prompt layers | `nest.rs` owns template refresh and roster projection; optional base-prompt file override is separate | Source checkout proves expected composition, but it is older than installed Buzz 0.5.19 | **UNVERIFIED** for the installed 0.5.19 effective provider prompt; design and file boundaries are verified |
| Pi | Reuses ancestor `/Users/man/CLAUDE.md` and repository `AGENTS.md`; no Pi-specific context file exists | No separate sync; `/Users/man/.pi/agent` and project `.pi` context are absent | Installed `resource-loader.js`, `system-prompt.js`, and `agent-session.js` trace discovery/composition | **UNVERIFIED** behaviorally for a fresh `agent-mesh` launch |
| OpenCode | Provider-only base config plus explicitly selected named agents under `/Users/man/.config/opencode/agents/` | Named-agent copies exist; no canonical sync/provenance mechanism was verified | `opencode debug config` resolves named agents; readable ancestor-loader source was not recovered | **UNVERIFIED** for automatic `AGENTS.md`/`CLAUDE.md`; named-agent presence is verified, activation is selection-dependent |
| Grok | Repository `AGENTS.md`/compatible names and any scoped Grok rules | Native project discovery; no separate agent-mesh synchronization mechanism observed | Current `grok inspect --json` identifies one project instruction for the exact audit worktree | **VERIFIED discovery** under Grok 1.0.5; fresh behavioral obedience is **UNVERIFIED**; historical prompt-context capture proves earlier Buzz loading only |
| Gemini / Antigravity | No `GEMINI.md` or project `.gemini` instruction source found in `agent-mesh`; Antigravity plugins are separate capability packages | No Gemini CLI or agent-mesh instruction sync found | Antigravity 2.11.0 registers `/Users/man/agent-mesh` as a project and has enabled plugins, but no readable instruction-loader or prompt receipt was recovered | Gemini CLI **ABSENT** on PATH; Antigravity instruction activation **UNVERIFIED** |

## Runtime traces

### Codex

Verified current inputs:

- The global contract is `/Users/man/.codex/AGENTS.md:1-68`.
- The current repository contract is `/Users/man/agent-mesh/AGENTS.md:1-44`.
- `/Users/man/.codex/config.toml:1-20` sets runtime/model/permission values and
  a Hermes MCP server, but no external instruction path. The comment at `:10`
  scopes Hermes regeneration to that managed configuration section; it is not an
  instruction-library loader.
- Plugins are enabled at `/Users/man/.codex/config.toml:54-115`; that makes their
  capabilities discoverable, not equivalent to injecting all skill bodies.
- Memory is enabled at `/Users/man/.codex/config.toml:125-128`. The global and
  repository contracts explicitly demote retrieved memory to supporting data, so
  old memory references are not task authority (`/Users/man/.codex/AGENTS.md:8-12,
  55-60`; `/Users/man/agent-mesh/AGENTS.md:13-20`).

The installed binary is Codex CLI 0.146.0. This audit did not locate readable
installed source for its `AGENTS.md` discovery algorithm; the global plus nearest
repository injection is verified behaviorally by this live Codex session rather
than claimed from guessed source internals.

Remaining poison: none in the fresh automatic Codex files. Old rollout summaries,
memory records, worktrees, and transcripts that mention `MASTER-GUIDE.md` are
historical/retrieval evidence. They must not be promoted to instruction authority.

Recommendation: **Keep** the two compact contracts. **Adapt** future memory UI or
prompt text only if it starts presenting retrieved records as commands rather than
evidence.

### Claude Code

Automatic startup:

- `/Users/man/CLAUDE.md:1-64` is the compact global instruction file.
- `/Users/man/.claude/settings.json:58-108` registers only `PreToolUse` enforcement
  hooks and a `PostToolUse` skill-usage logger. Local settings separately register
  a `SessionStart` hook for the `compact` source at
  `/Users/man/.claude/settings.local.json:42-52`.
- `/Users/man/.claude/hooks/post-compact-reinject.sh:1-12` is therefore registered
  for post-compaction starts. It gates on `source == compact` and emits only a
  bounded warning that derived continuity is not a new user instruction (`:6-11`).
- `/Users/man/.claude/hooks/purpose-gate/purpose_gate.sh:1-25` remains unregistered.
  Its comments describe startup/resume context injection at `:17-25`; comments are
  not registration.
- `/Users/man/.claude/hooks/session-start-context-DRAFT/PROVENANCE.md:6-10`
  explicitly says the draft is not wired. Its deleted-guide reference at `:24-34`
  is historical/dormant.

Explicit invocation:

- `/Users/man/.claude/commands/multi-model-diff-review.md:1-9` is now a quarantine
  notice. It forbids using the retired guide or embedded provider/model/port
  assumptions and requires live capability discovery before any future review.
- `/Users/man/.claude/skills/drive-tmux-automation/PROVENANCE.md:53-57` uses the
  deleted guide as machine inventory support. The skill body is invoked by skill;
  this supporting provenance file is only loaded if followed.

Post-compaction:

- The local post-compaction hook is registered through `settings.local.json`, not
  the main settings file. Its current output is safe and deliberately
  non-authoritative. Registration is verified; this audit did not launch Claude or
  compact a live session, so behavioral hook execution is **UNVERIFIED**.

Recommendation: **Keep** the command quarantined and the bounded compact hook
registered. **Adapt** the provenance reference when that skill is next maintained.
**Keep** current enforcement hooks, while auditing their rules independently for
drift because behavioral controls are not instruction contracts. Fresh Claude
global-file injection and compact-hook execution remain explicit **UNVERIFIED**
behavioral outcomes.

### Hermes

Automatic startup loader:

- `/Users/man/.hermes/hermes-agent/agent/prompt_builder.py:2373-2396` defines the
  project-context priority: `.hermes.md/HERMES.md`, then a merged `AGENTS.md`
  chain, then cwd-only `CLAUDE.md`, then Cursor rules. Only the first matching
  project context type is loaded; `SOUL.md` is independent.
- The actual composition is at
  `/Users/man/.hermes/hermes-agent/agent/prompt_builder.py:2430-2448`.
- `/Users/man/.hermes/hermes-agent/agent/agent_init.py:658-664` confirms that
  `SOUL.md`, `.hermes.md`, `AGENTS.md`, `CLAUDE.md`, and Cursor rules are the
  context-file set skipped by batch/data-generation mode.
- In `agent-mesh`, fresh default/profile runs therefore choose
  `/Users/man/agent-mesh/AGENTS.md`, not `/Users/man/CLAUDE.md`, and add the
  selected profile's `SOUL.md`.
- In the Buzz nest, Hermes chooses `/Users/man/.buzz/AGENTS.md` and the selected
  profile's `SOUL.md`.

Skills and explicit invocation:

- Progressive disclosure is explicit at
  `/Users/man/.hermes/hermes-agent/tools/skills_tool.py:9-12,52-66`: metadata is
  listed and full instructions load through `skill_view`.
- Skill discovery scans project, active-profile, and external directories at
  `/Users/man/.hermes/hermes-agent/tools/skills_tool.py:687-725,744-794`.
- A skill catalog is placed in the system prompt only when skills tools are
  available (`/Users/man/.hermes/hermes-agent/agent/system_prompt.py:524-553`).
- The current default config disables the `skills` toolset at
  `/Users/man/.hermes/config.yaml:1-5` and omits it from the CLI platform set at
  `:16-22`. Consequently the default automatic prompt does **not** currently
  include the default profile's skill catalog.
- Those files remain explicitly reachable when the selected profile exposes skill
  commands: Hermes states skills can be invoked by
  `/skill-name`, `skills_list`, or `skill_view` at
  `/Users/man/.hermes/hermes-agent/cli.py:14324-14335` and
  `/Users/man/.hermes/hermes-agent/agent/skill_commands.py:577-588`. The installed
  files are no longer operating instructions for universal adoption:
  `rules/SKILL.md:1-15` is quarantined,
  `agent-configs-verification/SKILL.md:1-10` is audit-only, and
  `hermes-agent-config-setup/SKILL.md:1-18` is a deprecation tombstone.
- The `cloud-coordinator` profile enables skills in
  `/Users/man/.hermes/profiles/cloud-coordinator/config.yaml:1-4,29-35`, but its
  profile-local skills are the bounded gstack set, not the default profile's
  `rules` or agent-configs skills. Profile isolation matters; do not infer the
  default skill directory applies to every profile.

Generated cache:

- `/Users/man/.hermes/.skills_prompt_snapshot.json:2737-2740` caches the old
  “configure universal rules” description even though the live setup skill is now
  a tombstone; it also indexes `rules` at `:3789-3792` and the verification skill
  at `:1242-1245`.
- The snapshot is **not currently valid**: the runtime requires an exact manifest
  match at `/Users/man/.hermes/hermes-agent/agent/prompt_builder.py:1570-1585`, and
  the current setup and verification skill mtimes/sizes no longer match their
  snapshot manifest entries. A cold prompt build will rescan and replace the
  snapshot (`:1832-1869`). Do not hand-edit this generated file.

Post-compaction:

- No separate Hermes local post-compaction instruction hook was found. The system
  prompt, context files, and any explicitly loaded skill remain the relevant
  sources. Hermes compaction contains skill-reload markers, so a bad skill that was
  explicitly loaded may remain relevant across compaction; that does not turn the
  entire catalog into authority.

Recommendation: **Keep** `rules` quarantined, the verification skill audit-only,
and the setup skill as a deprecation tombstone. Let a normal rescan regenerate the
cache from those corrected sources; do not hand-edit generated cache state. Start
a fresh session after the baseline cleanup and receipt the selected profile,
toolsets, project context, and prompt. The pre-cleanup request dump is historical
negative evidence, not proof of current activation, so fresh Hermes activation is
explicitly **UNVERIFIED**.

### Buzz

Buzz itself generates context and chooses the provider process working directory;
the provider performs native instruction discovery.

- `/Users/man/.buzz/REPOS/buzz/desktop/src-tauri/src/managed_agents/nest.rs:38-56`
  identifies `nest_agents.md` as the embedded template and defines the managed
  markers/version. The source template version is now 6 at `:46-53`, while the
  live `/Users/man/.buzz/.nest-agents-version:1` still records 5. This is observed
  source/live projection drift, not evidence that installed Buzz has refreshed it.
- The authoritative static template is
  `/Users/man/.buzz/REPOS/buzz/desktop/src-tauri/src/managed_agents/nest_agents.md:1-62`.
  It contains no `MASTER-GUIDE.md` or agent-configs dependency.
- `/Users/man/.buzz/REPOS/buzz/desktop/src-tauri/src/managed_agents/nest.rs:143-156,
  190-207` creates the file and documents refresh/preservation behavior.
- Version refresh replaces only content above the managed marker and preserves the
  existing marker and suffix (`/Users/man/.buzz/REPOS/buzz/desktop/src-tauri/src/
  managed_agents/nest.rs:412-466`).
- Roster regeneration replaces only the BEGIN/END managed region and preserves the
  suffix (`/Users/man/.buzz/REPOS/buzz/desktop/src-tauri/src/managed_agents/
  nest.rs:630-687`). Thus direct edits inside the managed roster do not persist;
  the persistent warning at `/Users/man/.buzz/AGENTS.md:111-114` requires selected
  Hermes profile/toolset inspection and a fresh activation receipt, and the
  workspace rule at `:116-121` rejects recursive agent-configs loading.
- Buzz creates the nest before restoring agents
  (`/Users/man/.buzz/REPOS/buzz/desktop/src-tauri/src/lib.rs:444-450`) and selects
  `/Users/man/.buzz` as the default provider working directory
  (`/Users/man/.buzz/REPOS/buzz/desktop/src-tauri/src/managed_agents/mod.rs:82-106`).
  Backend and ACP processes inherit it at
  `/Users/man/.buzz/REPOS/buzz/desktop/src-tauri/src/managed_agents/backend.rs:85-88`
  and `/Users/man/.buzz/REPOS/buzz/desktop/src-tauri/src/managed_agents/runtime.rs:568-570`.
- Hermes is invoked through `hermes-acp` with no profile argument in the preset at
  `/Users/man/.buzz/REPOS/buzz/desktop/src-tauri/src/managed_agents/discovery/
  presets.rs:152-159`; absent another saved-agent override, that uses the default
  Hermes profile and its currently disabled skills toolset.

Recommendation: **Keep** the template, managed roster, and corrected suffix. Make
future static edits in `nest_agents.md` plus a template-version bump; make roster
changes through Buzz data; keep user workspace guidance below `END BUZZ MANAGED`.
Do not call version-6 source active while the live marker remains 5; require the
installed 0.5.19 regeneration and provider-prompt receipts.

### Pi

Automatic startup:

- Pi 0.84.1 considers, in order, `AGENTS.override.md`, `AGENTS.md`, and
  `CLAUDE.md` in each directory (`/Users/man/.local/lib/node_modules/
  @earendil-works/pi-coding-agent/dist/core/resource-loader.js:31-50`).
- It loads an agent-directory global context and then walks every cwd ancestor to
  the filesystem root, de-duplicating and handling linked-worktree shadowing
  (`/Users/man/.local/lib/node_modules/@earendil-works/pi-coding-agent/dist/core/
  resource-loader.js:81-107`).
- The loader injects those files unless context files are disabled and separately
  discovers system/append prompt files (`:370-399`).
- The constructed prompt appends every context file and skill metadata at
  `/Users/man/.local/lib/node_modules/@earendil-works/pi-coding-agent/dist/core/
  system-prompt.js:18-31,94-107`, using the resources gathered at
  `/Users/man/.local/lib/node_modules/@earendil-works/pi-coding-agent/dist/core/
  agent-session.js:724-739`.

Skills:

- Pi puts only invocable skill metadata in the prompt; full bodies are read on
  demand (`/Users/man/.local/lib/node_modules/@earendil-works/pi-coding-agent/
  dist/core/skills.js:249-277`). Default skill roots are the agent directory and
  cwd `.pi/skills` (`:329-334`).
- `/Users/man/.pi/agent` currently has no context/prompt file and no installed
  skill body; `agent-mesh` has no project `.pi` directory. For an `agent-mesh`
  launch, the material local inputs are therefore `/Users/man/CLAUDE.md` at the
  home ancestor and `/Users/man/agent-mesh/AGENTS.md` at the repository ancestor.

Recommendation: **Keep** current state. Avoid adding a redundant
`/Users/man/.pi/agent/AGENTS.md` unless it has Pi-specific value, because Pi already
walks the home and repository ancestors. Loader implementation is verified, but no
fresh Pi process was launched; activation of those exact inputs is **UNVERIFIED**.

### OpenCode

Verified current configuration:

- OpenCode is 1.18.20.
- `/Users/man/.config/opencode/opencode.json:1-40` contains provider definitions
  only. There is no `instructions`, plugin, command, or external library path.
- `opencode debug config` resolves `/Users/man/.config/opencode/agents/*.md` as
  named agents. These are explicit agent selections, not the base configuration's
  global instruction field.
- `/Users/man/.config/opencode/agents/forge.md:1-14` and
  `/Users/man/.config/opencode/agents/prime.md:1-14` illustrate the named-agent
  form. The five named files `forge`, `prime`, `scout`, `sentinel`, and `operator`
  are exact-byte matches to the same-named authored files under
  `agent-mesh/.agent/agents/`, but no `SOURCE.md` provenance stub or automatic sync
  mechanism was found. Copy equality proves a current copy, not loader activation.
  No named agent contains a `MASTER-GUIDE.md` or agent-configs reference.

The installed Homebrew binary exposes `CLAUDE.md` strings but this audit did not
recover a readable, line-citable source implementation for its ancestor discovery.
Therefore automatic `AGENTS.md`/`CLAUDE.md` discovery is **unverified here**, not
assumed from historical logs. The verified negative is narrower: the resolved
OpenCode config has no explicit instruction-library loader.

Recommendation: **Keep** provider-only config. **Adapt** named agents only when a
user explicitly wants those workflows; do not treat named-agent presence as base
startup authority.

### Grok

Authored source and install/sync:

- Grok recognizes repository instruction files rather than requiring a copied
  global contract. Its bundled guide lists `Agents.md`, `Claude.md`, `CLAUDE.md`,
  `CLAUDE.local.md`, `AGENT.md`, and `AGENTS.md` at
  `/Users/man/.grok/docs/user-guide/12-project-rules.md:15-26` and documents home,
  repo-root-to-cwd, and cwd-only discovery at `:50-80`.
- No separate Grok-specific instruction projection or automatic sync from
  `agent-configs` or `.agent/` was observed. `/Users/man/.grok/config.toml:1-19`
  configures CLI/marketplace/UI/privacy surfaces, not a universal instruction path.

Current discovery receipt, captured read-only without prompt bodies:

- `grok --version` returned `grok 1.0.5 (5115b46bc909) [stable]`.
- From the exact audit worktree, `grok inspect --json` reported cwd and project root
  `/Users/man/worktrees/redtrades/agent-mesh/runtime-instruction-audit`, trusted
  project state, and one project instruction:
  `/Users/man/worktrees/redtrades/agent-mesh/runtime-instruction-audit/Agents.md`,
  scope `project`, type `agents_md`, 2,437 bytes, approximately 609 tokens. On this
  case-insensitive filesystem that resolves to the repository `AGENTS.md`.
- The same sanitized inspection reported only `/Users/man/.grok/config.toml` as a
  user config layer. Compatibility cells were reported separately and are not
  treated as proof that their source material was loaded.

Historical activation evidence:

- `/Users/man/.grok/sessions/%2FUsers%2Fman%2F.buzz/
  01a0371b-19a4-7a82-8b12-8f43ebce172d/prompt_context.json:6-14` records
  `/Users/man/.buzz/Agents.md` in `agents_md_files` for a 2026-08-25 session. The
  prompt body is deliberately not reproduced. This proves that historical session's
  capture, not current Buzz or agent-mesh behavior.

Verdict: current Grok project-instruction **discovery is VERIFIED** for the exact
worktree. This audit did not start a Grok task or test obedience to a sentinel
instruction, so behavioral activation is **UNVERIFIED**. Historical Buzz capture is
supporting evidence only.

### Gemini / Antigravity

Authored source and install/sync:

- `/Applications/Antigravity.app/Contents/Info.plist` reports installed version
  2.11.0.
- `/Users/man/.gemini/config/projects/
  670f9f22-5c0e-4c89-8817-1e6d6688ba28.json:2-15` registers `agent-mesh` with
  `file:///Users/man/agent-mesh` on default branch `main`.
- `/Users/man/.gemini/config/config.json:1-32` enables six Antigravity plugins and
  contains user settings, but no agent-mesh instruction projection or sync path.
- No `GEMINI.md` or project `.gemini` instruction file was found under
  `/Users/man/agent-mesh` or the audit worktree. Plugin skill bodies are installed
  capability packages, not proof of automatic project-instruction injection.

Discovery and activation:

- No `gemini` executable is present on PATH, so Gemini CLI is **ABSENT** for this
  audit. Antigravity project registration proves workspace metadata only.
- No readable line-citable Antigravity implementation for `AGENTS.md`, `CLAUDE.md`,
  or `GEMINI.md` discovery was recovered from the installed app, and no redacted
  prompt/context receipt was found for `agent-mesh`.
- No app or service was started.

Verdict: Antigravity 2.11.0 project and plugin configuration are **VERIFIED** as
stored local state. Gemini CLI is **ABSENT** and Antigravity instruction discovery
and activation are **UNVERIFIED**.

## Remaining risk ledger

1. **Keep quarantined — deprecated explicit command:**
   `/Users/man/.claude/commands/multi-model-diff-review.md:1-9`.
2. **Keep bounded — registered compact hook:**
   `/Users/man/.claude/settings.local.json:42-52` registers
   `/Users/man/.claude/hooks/post-compact-reinject.sh:1-12`; execution remains
   behaviorally unverified in this audit.
3. **Keep quarantined/audit-only — legacy Hermes skills:**
   `/Users/man/.hermes/skills/rules/SKILL.md:1-15`,
   `/Users/man/.hermes/skills/autonomous-ai-agents/agent-configs-verification/
   SKILL.md:1-10`, and
   `/Users/man/.hermes/skills/hermes-agent-config-setup/SKILL.md:1-18`.
4. **Adapt when touched — supporting provenance only:**
   `/Users/man/.claude/skills/drive-tmux-automation/PROVENANCE.md:53-57`.
5. **Classify before reuse — portable-core/universal-source claims:**
   `agent-mesh/.agent/AGENTS.md:1-22,24-111`, `agent-mesh/README.md:1-20,27-31`,
   and `agent-mesh/HANDOFF.md:70-75` are evidence of earlier architecture and
   adoption intent, not runtime authority or activation receipts.
6. **Reconcile projection drift — Buzz source version 6/live marker 5:**
   `/Users/man/.buzz/REPOS/buzz/desktop/src-tauri/src/managed_agents/nest.rs:46-53`
   versus `/Users/man/.buzz/.nest-agents-version:1`. Do not infer refresh.
7. **Quarantine operationally — pre-cleanup session state:** do not resume or
   trust sessions whose stored prompt contains the old guide directive; begin a
   fresh session and verify the resulting prompt/context list.
8. **Explicit unverified activation outcomes:** fresh Claude global injection and
   compact-hook execution, fresh Hermes prompt construction, installed Buzz 0.5.19
   effective provider prompt, Pi context injection, OpenCode automatic ancestor
   discovery, Grok behavioral obedience, and Antigravity instruction discovery all
   remain unverified. These are honest audit results, not permission to start the
   runtimes during this read-only pass.

## Minimum source-of-truth rule

Deleting `MASTER-GUIDE.md` is stable without replacing it when these sources stay
clean:

- runtime-global contracts: `/Users/man/.codex/AGENTS.md`,
  `/Users/man/CLAUDE.md`, and each active Hermes profile's `SOUL.md`;
- repository contract: `/Users/man/agent-mesh/AGENTS.md`;
- Buzz generator template:
  `/Users/man/.buzz/REPOS/buzz/desktop/src-tauri/src/managed_agents/nest_agents.md`
  plus its version in `nest.rs` for static-template changes;
- explicitly installed/invoked commands and skills, which must be audited
  individually rather than synchronized from `/Users/man/agent-configs`.

The existing `agent-mesh/.agent/` portable-core claims and manual adoption recipes
remain design evidence. They do not become the canonical source, installer, or sync
mechanism merely because their copies happen to match a runtime-local file. Keep,
Adapt, Defer, or Reject them in the approval design before any implementation.

There is no need to make either `/Users/man/agent-configs/README.md` or
`/Users/man/agent-workspace/README.md` a live bootstrap input. Both correctly
describe bounded source/onboarding roles and should remain documentation.

## Buzz configuration-readiness appendix

### Readiness verdict

The local evidence is sufficient to design a bounded Buzz configuration, but it
is **not** sufficient to declare Buzz properly configured. The installed app is
0.5.19, while the inspected source checkout is commit
`631b05c883f58e9533e9038b4669ebdfb1d9cf27` and declares 0.5.4 at
`/Users/man/.buzz/REPOS/buzz/desktop/src-tauri/Cargo.toml:10`. The checkout also
has an uncommitted change in `desktop/src-tauri/src/managed_agents/nest_agents.md`.
Source evidence therefore establishes the design and expected behavior, but an
installed-binary probe is still required at every activation seam.

### Bounded prompt-size measurement

Measured read-only on 2026-08-28 with `stat -f '%N\t%z bytes'` and SHA-256:

| File | Bytes | SHA-256 | Boundary |
|---|---:|---|---|
| `/Users/man/.buzz/REPOS/buzz/crates/buzz-acp/src/base_prompt.md` | 13,734 | `0ee7fd2ca8ed01ca514ef7089475531d5b979d98f0f68d9df84abfe2959449c5` | older source checkout; not the installed binary's effective prompt |
| `/Users/man/.buzz/AGENTS.md` | 6,351 | `8f78c58af451df649c9803a59f740577081b0e5b5ac3df56927d9bda5fcae5db` | live nest file only; excludes persona, memory, thread, and event context; source template is version 6 while live marker is 5 |

These sizes explain prompt-pressure risk but do not prove what installed Buzz
0.5.19 sends to a provider. That requires a redacted installed-binary prompt dump.

### Ownership and projection boundaries

- Buzz's fixed nest projection is `/Users/man/.buzz/AGENTS.md`. The embedded
  source template and its version/refresh algorithm are owned by
  `/Users/man/.buzz/REPOS/buzz/desktop/src-tauri/src/managed_agents/nest_agents.md:1-62`
  and `nest.rs:38-56,412-466`. The roster is a separate generated zone at
  `nest.rs:630-687`. Material below `END BUZZ MANAGED` is the persistent user
  zone; direct changes inside the roster are not persistent.
- Buzz's lowest-precedence agent defaults are stored in
  `/Users/man/Library/Application Support/xyz.block.buzz.app/agents/global-agent-config.json`.
  The source documents definition/persona/instance precedence, live resolution on
  next restart, and restricted storage at
  `/Users/man/.buzz/REPOS/buzz/desktop/src-tauri/src/managed_agents/global_config/mod.rs:1-23,36-72,177-207`.
  Current global values have no provider/model and prefer runtime `claude`; the
  required Claude ACP adapter is not present, so that preference is not presently
  runnable.
- The installed `/Applications/Buzz.app/Contents/MacOS/buzz-acp` 0.5.19 binary
  exposes `--base-prompt-file` and `BUZZ_ACP_BASE_PROMPT_FILE`. The corresponding
  inspected source declares the override at
  `/Users/man/.buzz/REPOS/buzz/crates/buzz-acp/src/config.rs:407-419` and reads it
  with a 1 MiB limit at `:879-893`. This is a direct-file **base-prompt** override,
  not an `AGENTS.md` suffix feature and not a provider configuration file.
- The base prompt is composed with the persona/system prompt, agent core, and
  channel canvas before `session/new` at
  `/Users/man/.buzz/REPOS/buzz/crates/buzz-acp/src/pool.rs:879-927`. Model and
  permission settings are separate ACP controls. The configured permission-mode
  default is `bypassPermissions` at
  `/Users/man/.buzz/REPOS/buzz/crates/buzz-acp/src/config.rs:421-444`; a safe
  deployment must set and behaviorally verify an explicit mode rather than rely
  on that default.

**Proposed canonical projection architecture:** keep one canonical module inside
the single agent-platform repository (currently `agent-mesh`) with two
intentionally different render targets. It renders a minimal Buzz base-prompt
projection, referenced through `BUZZ_ACP_BASE_PROMPT_FILE`, and a separate
nest-workspace projection through the fixed `nest_agents.md`/template-version
path into the static portion of `/Users/man/.buzz/AGENTS.md`. Both projections
carry source revision and content hash markers while preserving the roster and
user suffix. The repository module is canonical; runtime-local generated files
are projections, not sources of truth. This is **not** a copy of a universal
`AGENTS.md`. An activation receipt should record source revision, source and
projection hashes, installed Buzz/buzz-acp version, selected runtime/profile,
effective environment path, restart identity, and a behavioral prompt probe.

### ACP adapters and what is runnable now

The source catalog distinguishes `Available`, `AdapterMissing`, and
`NotInstalled` by command resolution at
`/Users/man/.buzz/REPOS/buzz/desktop/src-tauri/src/managed_agents/discovery/presets.rs:26-85`.
Its preset commands and arguments are at `:88-177`; built-in discovery is at
`/Users/man/.buzz/REPOS/buzz/desktop/src-tauri/src/managed_agents/discovery.rs:75-211`.

Observed PATH state on 2026-08-28:

| Runtime | Local command state | Configuration status |
|---|---|---|
| Buzz Agent | Bundled at `/Applications/Buzz.app/Contents/MacOS/buzz-agent` | **Partially verified**: binary present; no live session/model/tool probe |
| Goose | `/Users/man/.local/bin/goose` present | **Partially verified**: custom harness uses `goose acp`; no handshake/auth/model probe |
| OpenCode | `/opt/homebrew/bin/opencode` present | **Partially verified**: preset is `opencode acp`; no live Buzz handshake |
| Hermes | `/Users/man/.local/bin/hermes-acp` present | **Partially verified**: profile ownership is known; selected endpoint has not been proven through Buzz |
| Grok | `/Users/man/.grok/bin/grok` present | **Partially verified**: preset command exists; auth/session behavior untested |
| OpenClaw | `/Users/man/.local/bin/openclaw` present | **Partially verified**: gateway execution locus and credentials remain separate, as warned at `presets.rs:161-175` |
| Claude | `claude` exists, but `claude-agent-acp` and `claude-code-acp` are absent | **Not runnable through current Buzz catalog** |
| Codex | `codex` exists, but `codex-acp` is absent | **Not runnable through current Buzz catalog** |
| Devin, Cursor, OMP, Kimi, Amp | Required preset commands absent | **Not runnable** |

Presence is not readiness. The source can apply a requested model after session
creation (`pool.rs:879-884`), and installed `buzz-acp` exposes model, effort,
session-title, and permission controls, but per-adapter support and behavioral
effect remain unverified. Session IDs and turn counters live in in-memory maps at
`/Users/man/.buzz/REPOS/buzz/crates/buzz-acp/src/pool.rs:83-104`; the source
explicitly calls model switches runtime-only and gone after restart at `:292-297`.
Threads provide conversational continuity, not a durable ACP execution resume.

### Hermes and port 3100

The standard Buzz Hermes preset runs `hermes-acp` with no profile argument
(`presets.rs:152-159`). The saved custom harness
`/Users/man/Library/Application Support/xyz.block.buzz.app/custom_harnesses/hermes-local.json:1-9`
also supplies no arguments or environment and explicitly says it follows the
top-level default Hermes model. That default is currently
`http://127.0.0.1:8318/v1`, provider `custom`, at
`/Users/man/.hermes/config.yaml:10-22`.

Port 3100 belongs to the separate `cloud-coordinator` profile: both delegation
and model traffic select FreeLLMAPI there at
`/Users/man/.hermes/profiles/cloud-coordinator/config.yaml:5-11,23-41`. Buzz's
native relay mesh is a third, distinct path at `http://127.0.0.1:9337/v1`
(`/Users/man/.buzz/REPOS/buzz/desktop/src-tauri/src/managed_agents/relay_mesh.rs:1-4,25-36`).
Therefore “Buzz uses Hermes on :3100” is currently false for the preset/custom
harness as saved. A dedicated wrapper or proven profile-selection environment is
required before :3100 can be claimed, and its exact effective config must appear
in the activation receipt.

### Coordination capability versus missing execution authority

Buzz CLI supplies signed relay operations, messages/replies/threads, issues, and
issue assignment. It validates a private key and optional signed authorization
tag before dispatch at
`/Users/man/.buzz/REPOS/buzz/crates/buzz-cli/src/lib.rs:1899-1971`; message and
thread commands are defined at `:350-477`, and issues begin at `:1600`.

This is useful identity, conversation, and ownership metadata. It does **not**
establish an atomic task lease, compare-and-swap claim, durable heartbeat, or ACP
session checkpoint/resume contract. CLI exit code 5 is documented as a write
conflict at `:76`; it should not be relabeled as a task lease. Likewise, a local
agent-pool slot claim is process-local capacity control, not durable work
authority. Git/issue/checkpoint artifacts must remain the authoritative resume
seam until a real lease and checkpoint protocol is implemented and tested.

### Secrets, restart, rollback, and drift

- Global and managed stores are written mode 0600 (`global_config/mod.rs:20-23,
  194-207`); runtime definitions must use key references and redacted diagnostics,
  never copied secret values.
- Global values are picked up at next restart (`global_config/mod.rs:14-18`).
  Session state and model switches are not durable, so a restart is both an
  activation boundary and a continuity break.
- The local source checkout is older than the installed app and currently dirty.
  Its template is not, by itself, a rollback artifact for 0.5.19. Rollback must
  restore an exact versioned projection/config snapshot and clear the scoped
  override, followed by an idle-agent restart and receipt verification.
- Buzz Desktop was not running during this audit, so its native :9337 relay and
  UI-resolved runtime catalog were not live-probed. No service was started.

### Readiness matrix

| Surface | Status | Evidence still required |
|---|---|---|
| Fixed nest file and managed/user split | **Partially verified** | Reconcile source template version 6 with live marker 5, then run one 0.5.19 regeneration probe to prove installed behavior matches source |
| Direct Buzz base-prompt file override | **Ready (interface verified)** | Generated-file hash plus prompt-behavior receipt |
| Global/definition/persona ownership | **Ready (source verified)** | UI/API round-trip on installed 0.5.19 |
| Signed actors, issues, replies, threads | **Ready (interface verified)** | Relay-auth smoke with non-secret identity evidence |
| Runtime availability | **Partially verified** | Buzz UI/catalog result and ACP initialize/session-new probe per candidate |
| Model and permission semantics | **Partially verified** | Adapter capability report plus behavior tests for model selection and denied tool use |
| Hermes default versus :3100 routing | **Partially verified** | Explicit selected-profile config dump and request endpoint receipt |
| Atomic lease and durable execution resume | **Unverified/absent in inspected implementation** | Protocol, persistence, expiry/recovery, and contention tests |
| Restart and rollback | **Unverified operationally** | Exact-version backup, idle restart, rollback drill, and post-rollback receipt |
| No recursive/deleted-guide injection | **Partially verified** | Fresh 0.5.19 Buzz-to-provider prompt dump after projection activation |

### Smallest safe configuration sequence (proposed, not executed)

1. Freeze the exact installed Buzz/buzz-acp version and capture redacted current
   config hashes and runtime catalog; do not treat the older checkout as the
   installed binary's rollback image.
2. Create one canonical module inside the single agent-platform repository
   (currently `agent-mesh`) that renders separate minimal base-prompt and
   nest-workspace projections. Keep runtime-local outputs non-canonical, attach
   deterministic source-revision/hash markers, and reject any `MASTER-GUIDE.md`
   or wholesale agent-configs reference.
3. Set `BUZZ_ACP_BASE_PROMPT_FILE` only in the chosen Buzz agent's effective
   environment. Route nest-workspace changes through the authoritative template
   and version boundary, preserving roster and user zones.
4. Select one adapter only. Pin explicit provider/model/profile and an explicit
   least-privilege permission mode. If Hermes on :3100 is intended, use a proven
   profile-selection wrapper/environment rather than the current default preset.
5. Restart one idle agent. Record the activation receipt and prove cwd, prompt
   hashes, native instruction discovery, ACP model, permission behavior, and
   absence of recursive/deleted-guide loading.
6. Smoke signed identity, issue/thread/reply continuity, interruption, restart,
   and rollback. Expand to another adapter only after the first receipt and
   rollback drill pass.
