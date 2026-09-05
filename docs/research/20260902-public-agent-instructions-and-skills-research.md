# Public agent instructions and coding-skill patterns

Date: 2026-09-02
Scope: Primary-source review of public agent-instruction files and reusable
coding-agent skill repositories, with a source-only reconciliation against
`runtimes/codex/AGENTS.md`.

This is research and a set of proposals, not an installation or runtime change.
Repository star counts are a point-in-time popularity signal observed through
the GitHub API on 2026-09-02; they are not evidence of quality or local fit.

## Identity and attribution findings

| Subject | Primary evidence | Observed | Proposed disposition |
|---|---|---|---|
| "Andrew Karpathy" | [`karpathy` GitHub profile](https://github.com/karpathy); [`karpathy/autoresearch/README.md`](https://github.com/karpathy/autoresearch/blob/master/README.md#L7-L15); [`program.md`](https://github.com/karpathy/autoresearch/blob/master/program.md) | The public profile displays **Andrej Karpathy**, not Andrew. No `AGENTS.md` or `CLAUDE.md` was located in his owned repositories. `autoresearch` explicitly identifies `program.md` as agent instructions and a "super lightweight skill." It restricts writes to one file, freezes the evaluator, fixes the time budget and metric, establishes a baseline first, and records keep/discard results. It also prefers a deletion or an equally effective simpler implementation. | Treat "Andrew" as unresolved spelling ambiguity, with Andrej Karpathy as the likely intended person rather than silently correcting the name. Adapt the narrow authority surface, fixed evaluator, baseline, and keep/discard evidence pattern. Do not import its indefinite loop or destructive reset procedure. |
| Boris Cherny | [`bcherny` GitHub profile](https://github.com/bcherny); [`bcherny/openclaw`](https://github.com/bcherny/openclaw); [its `AGENTS.md` history](https://github.com/bcherny/openclaw/commits/main/AGENTS.md) | The profile identifies Boris Cherny and says "Claude Code @ Anthropic." No first-party personal `AGENTS.md`, `CLAUDE.md`, equivalent prompt, or relevant gist was located. The apparent counterexample, `bcherny/openclaw/AGENTS.md`, is inherited from an upstream fork: the fork was observed zero commits ahead and the file history is authored upstream. Third-party reconstructions therefore do not establish Cherny's personal configuration or use. | Keep this finding explicitly unresolved. Do not attribute any public instruction bundle or coding style to Cherny until a first-party repository artifact is available. |

## Public repository evidence

| Repository and exact source paths | Popularity snapshot | Observed source pattern | Proposed use for a Basic MVP | Overengineering risk |
|---|---:|---|---|---|
| [`DietrichGebert/ponytail`](https://github.com/DietrichGebert/ponytail): [`AGENTS.md`](https://github.com/DietrichGebert/ponytail/blob/main/AGENTS.md), [`skills/ponytail/SKILL.md`](https://github.com/DietrichGebert/ponytail/blob/main/skills/ponytail/SKILL.md), [`benchmarks/`](https://github.com/DietrichGebert/ponytail/tree/main/benchmarks) | 120,863 stars | This resolves "ponytail" in this context. Its decision ladder asks whether work is needed, then prefers existing code, standard-library and native features, already-installed dependencies, a one-line solution, and finally the minimum new code. It explicitly protects understanding, trust-boundary validation, data-loss handling, security, accessibility, and one runnable check for non-trivial logic. | Adapt only the decision ladder plus its safety and verification exceptions as a short repository-owned instruction. | **High if installed wholesale.** The complete project adds always-on hooks, modes, commands, multi-harness adapters, status integration, and benchmark machinery that a Basic MVP does not need. |
| [`karpathy/autoresearch`](https://github.com/karpathy/autoresearch): [`README.md`](https://github.com/karpathy/autoresearch/blob/master/README.md), [`program.md`](https://github.com/karpathy/autoresearch/blob/master/program.md) | 95,111 stars | Task-specific agent program with one mutable file, immutable evaluation, one metric, fixed budget, baseline-first execution, compact result logging, and keep/discard decisions. | Adapt as a task-packet pattern for bounded experiments, not as a general global instruction file. | **Low in its native narrow domain; high if generalized.** The endless loop and reset behavior conflict with bounded authority and destructive-action controls. |
| [`multica-ai/andrej-karpathy-skills`](https://github.com/multica-ai/andrej-karpathy-skills): [`CLAUDE.md`](https://github.com/multica-ai/andrej-karpathy-skills/blob/main/CLAUDE.md), [`skills/karpathy-guidelines/SKILL.md`](https://github.com/multica-ai/andrej-karpathy-skills/blob/main/skills/karpathy-guidelines/SKILL.md), [`README.md`](https://github.com/multica-ai/andrej-karpathy-skills/blob/main/README.md), [initial commit](https://github.com/multica-ai/andrej-karpathy-skills/commit/8462496b34419f20b32778610571ac723e91f94c) | 209,578 stars | This is explicitly **Karpathy-inspired**, not Karpathy-authored. The README says it is derived from Andrej Karpathy's observations; the initial commit is authored by Jiayuan Zhang (`forrestchang`) and co-credits Claude Opus 4.5. `CLAUDE.md` and the nearly identical skill encode four rules: surface assumptions and tradeoffs, use minimum non-speculative code, make surgical task-traceable edits, and define verifiable success criteria. The two behavior files were observed at 2,357 and 2,518 bytes. | Treat it as a compact third-party synthesis and use it only as corroboration for rules already independently supported. If wording is later adapted, preserve the current contract's stronger safety floor and attribution. | **Low token cost, low MVP need.** The content is compact, but importing it would duplicate the existing work-mode, scope, simplicity, and verification rules. Its blanket "no error handling for impossible scenarios" statement is unsafe if the agent merely assumes a case is impossible. |
| [`affaan-m/ECC`](https://github.com/affaan-m/ECC): [`AGENTS.md`](https://github.com/affaan-m/ECC/blob/main/AGENTS.md), [`CLAUDE.md`](https://github.com/affaan-m/ECC/blob/main/CLAUDE.md), [`.codex/AGENTS.md`](https://github.com/affaan-m/ECC/blob/main/.codex/AGENTS.md), [`coding-standards/SKILL.md`](https://github.com/affaan-m/ECC/blob/main/.agents/skills/coding-standards/SKILL.md), [`strategic-compact/SKILL.md`](https://github.com/affaan-m/ECC/blob/main/.agents/skills/strategic-compact/SKILL.md), [`AGENTS.md` history](https://github.com/affaan-m/ECC/commits/main/AGENTS.md) | 246,083 stars | These are first-party **ECC project** instructions maintained in the repository, not evidence of Andrej Karpathy's, Boris Cherny's, or even one maintainer's personal global configuration. Commit history includes Affaan Mustafa and other contributors. The root `AGENTS.md` mandates agent-first delegation, TDD with 80% coverage, proactive review, broad security checks, immutability, planning, and a multi-stage workflow. `CLAUDE.md` is repository-contributor guidance; `.codex/AGENTS.md` is a Codex-specific supplement. The coding skill includes KISS/YAGNI but is 12,842 bytes; strategic compaction is 6,570 bytes and adds hook/config guidance. The root `AGENTS.md` and `CLAUDE.md` were observed at 8,805 and 3,936 bytes. | Extract no wholesale instruction bundle. At most, use its progressive-disclosure separation - short always-loaded rules, on-demand skills, and hooks outside model context - as corroboration for the repository's existing layering. | **Very high for Basic MVP.** The repository advertises 68 agents, 286 skills, 94 command shims, hooks, memory, continuous learning, security scanning, MCP configuration, multiple installers, and multi-harness adapters. Its mandatory delegation, planning, TDD, review, and coverage floor directly conflict with the current Basic MVP exception. |
| [`addyosmani/agent-skills`](https://github.com/addyosmani/agent-skills): [`code-simplification/SKILL.md`](https://github.com/addyosmani/agent-skills/blob/main/skills/code-simplification/SKILL.md), [`incremental-implementation/SKILL.md`](https://github.com/addyosmani/agent-skills/blob/main/skills/incremental-implementation/SKILL.md), [`AGENTS.md`](https://github.com/addyosmani/agent-skills/blob/main/AGENTS.md) | 91,636 stars | Behavior-preserving simplification, project-convention matching, recently-changed-scope discipline, thin vertical slices, naive-correct-first implementation, and explicit anti-overengineering examples. Its repository instruction maps most work through a mandatory multi-skill lifecycle. | Adapt the scope, vertical-slice, and simplicity checks selectively. | **Medium to high wholesale.** The full catalog and mandatory DEFINE-to-SHIP lifecycle add ceremony beyond a basic local change. |
| [`obra/superpowers`](https://github.com/obra/superpowers): [`test-driven-development/SKILL.md`](https://github.com/obra/superpowers/blob/main/skills/test-driven-development/SKILL.md), [`verification-before-completion/SKILL.md`](https://github.com/obra/superpowers/blob/main/skills/verification-before-completion/SKILL.md), [`CLAUDE.md`](https://github.com/obra/superpowers/blob/main/CLAUDE.md) | 280,729 stars | Test-first red/green proof, minimum implementation, one problem per PR, explicit human approval of the complete diff, and behavior-level evaluation for skill changes. Its `AGENTS.md` points to `CLAUDE.md`, avoiding two independently maintained instruction bodies. | Reuse focused verification and one-problem scope where the task risk warrants them. | **Medium wholesale.** Automatically invoking a full process skill stack for every code change conflicts with Basic MVP routing. |
| [`EveryInc/compound-engineering-plugin`](https://github.com/EveryInc/compound-engineering-plugin): [`ce-simplify-code/SKILL.md`](https://github.com/EveryInc/compound-engineering-plugin/blob/main/skills/ce-simplify-code/SKILL.md), [`ce-simplify-code` guide](https://github.com/EveryInc/compound-engineering-plugin/blob/main/docs/guides/ce-simplify-code.md) | 24,779 stars | Simplifies settled recent code, preserves exact outputs, errors, side effects, ordering, and safety checks, then runs verification matched to blast radius. The skill dispatches three reviewer agents before applying worthwhile findings. | Adapt the settled-diff boundary, behavior preservation, and blast-radius verification statements. | **High for Basic MVP.** Three parallel reviewers and the surrounding lifecycle are disproportionate for a small reversible change. |
| [`vercel-labs/skills`](https://github.com/vercel-labs/skills): [`src/skill-lock.ts`](https://github.com/vercel-labs/skills/blob/main/src/skill-lock.ts), [`src/source-parser.ts`](https://github.com/vercel-labs/skills/blob/main/src/source-parser.ts), [`AGENTS.md`](https://github.com/vercel-labs/skills/blob/main/AGENTS.md) | 30,232 stars | Skill lock entries record source, source type and URL, ref, subpath, complete-folder tree hash, timestamps, and optional plugin identity. | Adapt these fields later for admitted-capability provenance and update detection. | **High for this routing change.** A package installer and lock implementation do not improve the Basic MVP's code-writing behavior directly. |
| [`anthropics/skills`](https://github.com/anthropics/skills): [`template/SKILL.md`](https://github.com/anthropics/skills/blob/main/template/SKILL.md), [`README.md`](https://github.com/anthropics/skills/blob/main/README.md#L63-L90) | 173,184 stars | Minimal skill package shape: a folder containing `SKILL.md`, YAML frontmatter with `name` and a trigger-oriented `description`, followed by instructions. The repository says its examples are demonstrations and that licensing varies by skill. | Use only as a packaging and progressive-disclosure reference for future approved skills. | **Medium wholesale.** The broad document, design, API, and application catalog is unrelated to a narrow routing MVP. |
| [`wshobson/agents`](https://github.com/wshobson/agents): [`AGENTS.md`](https://github.com/wshobson/agents/blob/main/AGENTS.md), [`README.md`](https://github.com/wshobson/agents/blob/main/README.md) | 39,352 stars | Its `AGENTS.md` is intentionally a short map into detailed documentation and on-demand skills. The repository reports 94 plugins, 202 agents, 183 skills, 105 commands, 16 orchestrators, generators, and adapters for several harnesses. | Adapt the short-map/progressive-disclosure principle only. | **Very high wholesale.** It is a multi-harness marketplace and orchestration system, not a Basic MVP instruction patch. |

## Runtime adapters

This section distinguishes native discovery from proposed adapters. Paths and
behavior were checked against current official documentation and source on
2026-09-02. No live runtime configuration was changed.

| Runtime or standard | Observed discovery and controls | Does one global `AGENTS.md` reach it automatically? | Proposed Basic MVP adapter |
|---|---|---|---|
| **Codex** | OpenAI documents global discovery at `$CODEX_HOME/AGENTS.override.md`, otherwise `$CODEX_HOME/AGENTS.md`; `CODEX_HOME` defaults to `~/.codex`. Project discovery then walks from the project root toward the working directory, taking at most one instruction file per directory. [Official Codex guidance](https://developers.openai.com/codex/guides/agents-md) | **Yes, at Codex's own global path.** `~/.codex/AGENTS.md` is native global guidance for Codex, not a cross-runtime standard location. | Keep `runtimes/codex/AGENTS.md` as the source artifact and let the approved installer place it at the Codex-supported destination. |
| **Claude Code** | Claude Code's user-wide instruction file is `~/.claude/CLAUDE.md`; project locations are `./CLAUDE.md` and `./.claude/CLAUDE.md`. Anthropic explicitly says Claude Code reads `CLAUDE.md`, not `AGENTS.md`, and documents either a `CLAUDE.md` `@AGENTS.md` import or a symlink. Imports may be relative or absolute and recurse up to four hops. [Official memory/instructions documentation](https://code.claude.com/docs/en/memory) | **No.** A file named `AGENTS.md` outside a project is not Claude Code's native user instruction source. | Add a tiny `~/.claude/CLAUDE.md` adapter that imports the installed canonical file, or use a symlink when no Claude-specific text is needed. Treat this as a runtime adapter, not a second maintained instruction body. Cowork sessions are an exception: Anthropic says they skip user-scope imports or links that resolve outside the session working directory. |
| **Claude Code skills** | Personal skills live at `~/.claude/skills/<skill-name>/SKILL.md`; project skills live at `.claude/skills/<skill-name>/SKILL.md`. Normally descriptions enter startup context and the full body loads only when invoked. `disable-model-invocation: true` removes the description from Claude's context and makes the full skill manual-only. `skillOverrides` supports `on`, `name-only`, `user-invocable-only`, and `off`; the `/skills` menu writes the setting to `.claude/settings.local.json`. [Official skills documentation](https://code.claude.com/docs/en/skills) | Not applicable to `AGENTS.md`; skill discovery is a separate path and loading contract. | Link or copy only admitted skills. For side-effecting or operator-timed procedures, prefer `disable-model-invocation: true`; use `name-only` or `off` when even description tokens or automatic availability are not justified. |
| **Hermes Agent instructions** | Hermes reserves `$HERMES_HOME/SOUL.md` (normally `~/.hermes/SOUL.md`) for global instance identity. It treats `.hermes.md`/`HERMES.md`, `AGENTS.override.md`/`AGENTS.md`, and `CLAUDE.md` as **project** context. In a Git repository, the `AGENTS.md` chain runs from Git root to working directory; outside Git, only the working directory is checked, so an `AGENTS.md` in `$HOME` is not a general inherited default. [Official context-file docs at source revision `afc3d9d`](https://github.com/NousResearch/hermes-agent/blob/afc3d9d34c9c3b01fa2e1332d2c66a5b5fabae3f/website/docs/user-guide/features/context-files.md) [Official personality/global-scope docs](https://github.com/NousResearch/hermes-agent/blob/afc3d9d34c9c3b01fa2e1332d2c66a5b5fabae3f/website/docs/user-guide/features/personality.md) | **No.** Hermes has no documented user-global `AGENTS.md` discovery path. `SOUL.md` and the manual `agent.system_prompt` setting in `~/.hermes/config.yaml` are Hermes-specific global mechanisms; neither imports a global `AGENTS.md` automatically. The manual prompt is also conditional: the official docs say it applies only when no personality is selected. | Generate a small Hermes-owned global adapter from the canonical contract, rather than relying on filename coincidence. Keep project facts in project `AGENTS.md`; do not repurpose `SOUL.md` as a repository runbook. |
| **Hermes Agent skills** | Hermes' profile-local skill source is `$HERMES_HOME/skills/` (normally `~/.hermes/skills/`). `skills.external_dirs` in `~/.hermes/config.yaml` adds shared directories such as `~/.agents/skills`; local names win collisions. The current source builds the prompt skill index only when at least one skills tool is present. `agent.disabled_toolsets` is applied as a global subtraction after platform tool configuration, and the `skills` toolset contains `skills_list`, `skill_view`, and `skill_manage`. [Official skills docs](https://github.com/NousResearch/hermes-agent/blob/afc3d9d34c9c3b01fa2e1332d2c66a5b5fabae3f/website/docs/user-guide/features/skills.md) [Global-disable docs](https://github.com/NousResearch/hermes-agent/blob/afc3d9d34c9c3b01fa2e1332d2c66a5b5fabae3f/website/docs/user-guide/configuration.md#global-toolset-disable) [Prompt gate](https://github.com/NousResearch/hermes-agent/blob/afc3d9d34c9c3b01fa2e1332d2c66a5b5fabae3f/agent/system_prompt.py#L619-L648) [Toolset definition](https://github.com/NousResearch/hermes-agent/blob/afc3d9d34c9c3b01fa2e1332d2c66a5b5fabae3f/toolsets.py#L176-L180) | Not applicable to global `AGENTS.md`. With the observed `agent.disabled_toolsets: [skills]`, configuring `skills.external_dirs` alone does **not** expose the skill tools or prompt index to the model. | If Hermes skill use is approved, first make the configuration internally consistent by removing `skills` from the global disable list, then point `skills.external_dirs` at only the admitted shared skill directory. This is proposed configuration, not a change made by this report. |
| **AGENTS.md open format** | The stewarded site defines AGENTS.md as a predictable Markdown file for project instructions, says to place it at the repository root, and supports nested files whose closest scope takes precedence. It specifies no user-global filesystem path. [Official repository README at revision `6ae2272`](https://github.com/agentsmd/agents.md/blob/6ae22720966e9cca6b2c2dd0780fb7265a87a46c/README.md) [Official site source for root and nested scope](https://github.com/agentsmd/agents.md/blob/6ae22720966e9cca6b2c2dd0780fb7265a87a46c/components/HowToUseSection.tsx) | **No cross-runtime guarantee.** The observed scope is repository guidance; global discovery and adapter behavior are runtime implementation details. | Use one canonical content source, but install the smallest explicit adapter each runtime documents. Do not treat format portability as automatic global activation. |

### Runtime-adapter reconciliation

- **Already adopted in source:** the current `runtimes/codex/AGENTS.md` is a
  concise global-behavior artifact suited to Codex's native global path, and it
  already separates stable defaults from repository instructions and skills.
- **Still proposed:** a minimal Claude `CLAUDE.md` import or symlink; a
  Hermes-specific global wrapper; selective runtime skill links; and, only if
  Hermes skills are approved, reconciling `agent.disabled_toolsets: [skills]`
  with `skills.external_dirs`.
- **Rejected for the Basic MVP:** assuming `~/.codex/AGENTS.md` is a universal
  location, copying the whole contract into multiple independently maintained
  files, putting repository runbooks in Hermes `SOUL.md`, or enabling every
  shared skill merely because a runtime can discover the directory.

## Reconciliation with `runtimes/codex/AGENTS.md`

This section compares repository source. It does not claim that the source file
is installed or active in any live Codex runtime.

### Already represented in the source contract

- **Small, layered global guidance.** The contract says it is a compact set of
  durable defaults rather than a system map or runbook. This already captures
  the strongest part of the short-map pattern in `wshobson/agents` and the
  single-source intent visible in `obra/superpowers`.
- **Basic MVP routing.** Lines 30-44 select the smallest runnable end-to-end
  slice, reuse the existing code and platform, require one focused check, and
  explicitly exclude speculative extensibility, multi-agent review, formal
  review, and release ceremony. This already rejects the heaviest parts of
  ECC and Addy Osmani's lifecycles, Superpowers' mandatory TDD path, and
  EveryInc's three-reviewer simplification pass for routine MVP work.
- **Assumptions, scope, and verification.** The contract's instruction-order,
  work-mode, safety, and evidence sections already cover the useful core of
  `multica-ai/andrej-karpathy-skills`: do not silently override instructions,
  diagnose before fixing, preserve unrelated work, label uncertainty, and
  verify proportionally. Its concise synthesis corroborates this direction but
  does not establish that Andrej Karpathy authored or used these exact rules.
- **Non-negotiable safety.** Lines 45-46 preserve security boundaries,
  trust-boundary validation, accessibility, and data-loss protection. That is
  compatible with Ponytail's explicit exceptions to minimalism.
- **Evidence and exactness.** Lines 63-71 distinguish observed, inferred,
  proposed, and unverified claims; require deterministic checks before model
  judgment; and bind review and promotion evidence to the exact candidate.
  These cover the core verification lesson from Superpowers and the evidence
  discipline behind Karpathy's fixed evaluator.
- **Approval before material architecture.** Lines 73-79 already stop new
  frameworks, dependencies, schemas, infrastructure, and security boundaries
  at an evidence-and-approval gate.

### Still proposed, not adopted by this report

- Add a compact reuse ladder for code-writing decisions: not needed, already in
  the repository, standard library, native platform, installed dependency,
  then minimum new code. The existing contract says "reuse" but does not encode
  this ordered decision aid.
- Keep task-specific experiment packets capable of naming one writable surface,
  immutable evaluation inputs, a baseline, a bounded budget, and a compact
  keep/discard record. This belongs in a procedure or task packet, not the
  global contract.
- Add immutable source/ref/subpath/tree-hash evidence when capability admission
  is implemented. This belongs in provenance records, not global prose.
- Package any later approved procedure as an on-demand `SKILL.md` with minimal
  trigger metadata rather than expanding the always-loaded global file.
- Preserve progressive disclosure: stable behavior in the short global file,
  task procedures in on-demand skills, and deterministic enforcement in hooks.
  ECC supports this separation, but its full installation is not proposed.

### Rejected or deferred for Basic MVP routing

- Installing Ponytail's full always-on plugin, hooks, modes, statusline, or
  benchmark harness.
- Importing a public skills marketplace or catalog wholesale.
- Installing ECC's agent, command, hook, memory, MCP, or multi-harness runtime;
  adopting its mandatory 80% coverage, proactive delegation, planning, and
  review floor for Basic MVP work.
- Mandatory TDD, planning, brainstorming, worktrees, or formal review solely
  because a Basic MVP task changes code.
- Three-reviewer simplification passes for small reversible changes.
- Karpathy's indefinite loop and automated reset behavior outside its narrow
  experimental branch contract.
- Any instruction attributed to Boris Cherny without first-party repository
  evidence.
- Treating `multica-ai/andrej-karpathy-skills` as an Andrej Karpathy-authored
  instruction file, or duplicating its four principles in always-loaded
  context when equivalent rules already exist.

## Compact proposal

If a later change is approved, the smallest evidence-supported addition would
be a short ordered reuse/minimal-code ladder inside the Basic MVP section or its
`lean-build` procedure. It should preserve the safety floor already present,
require the existing focused verification, and stop there. The repository does
not need another controller, catalog, plugin runtime, reviewer swarm, or global
lifecycle to obtain that behavior.

## Method and limits

- Read the named repositories' current default-branch files and GitHub metadata
  directly; no secondary article was used as evidence.
- Confirmed `affaan-m/ECC` and `multica-ai/andrej-karpathy-skills` are in the
  authenticated user's GitHub starred list: the first-party GitHub API
  `GET /user/starred/{owner}/{repo}` returned HTTP 204 for each on 2026-09-02.
- Used repository file and commit history to distinguish ECC's maintained
  project instructions from the Multica repository's third-party synthesis.
  The latter repository's own README and initial commit identify its derivation
  and non-Karpathy authorship.
- Queried GitHub code search for `AGENTS.md`, `CLAUDE.md`, related instruction
  paths, and public gists under the named personal accounts. An unsuccessful
  search supports only "not located," not proof that a private or unindexed
  file does not exist.
- Checked commit history and fork relationship before excluding
  `bcherny/openclaw/AGENTS.md` as personal authorship evidence.
- Inspected `runtimes/codex/AGENTS.md` directly for the reconciliation. No live
  runtime configuration was inspected or changed.
