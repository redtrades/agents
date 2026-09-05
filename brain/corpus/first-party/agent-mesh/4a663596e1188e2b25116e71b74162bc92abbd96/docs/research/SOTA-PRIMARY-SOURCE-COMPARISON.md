# Primary-source SOTA comparison for the provider-neutral SDLC MVP

**Checked:** 2026-08-28T20:06:03Z
**Scope:** 21 candidate families: 17 named agent/workflow repositories plus
SLSA, in-toto, Sigstore, and OpenTelemetry.
**Status:** read-only upstream research and proposed reuse boundaries; no
implementation authority.

## Evidence contract

- **Observed upstream** means a property visible in a file at the exact full
  commit SHA linked below, an official release, or the repository's official
  issue/security surface.
- **Officially documented** means the project says it; it is not automatically
  a behavioral or security proof.
- **Local evidence** means an existing `agent-mesh` artifact reports a local
  run or state. It is not evidence about every version or environment.
- **Inference** is an architectural conclusion drawn from the observed facts.
- **Proposed** is a fit decision for the current MVP, not an upstream fact.
- **Unknown** means this pass found no primary-source proof. Unknowns fail
  closed; they are not silently converted into capabilities.

Repository popularity and recency are included only as weak screening signals.
Stars, forks, a recent push, a large issue count, or an upstream use claim do
**not** prove reliability, security, operational adoption, or fit. No external
adoption study was used because this pass was deliberately primary-source-only.

## Intent and local boundary

The MVP under review is the existing thin delivery contract:

```text
Issue intent -> atomic attempt/resource lease -> isolated worktree
  -> transition checkpoint -> exact candidate SHA + artifact hashes
  -> deterministic gates -> fresh independent exact-candidate review
  -> human-controlled promotion
```

**Observed local evidence:** the current first-principles brief says GitHub
Issues are the human task graph, Git refs/commits and content hashes identify
state and evidence, and no database, daemon, or workflow engine is required for
the MVP. It also reports that the local SSSF adaptation executed typed phases,
deterministic gates, and SQLite traces, but that claimed provider neutrality did
not hold. See
[`sdlc-mvp-first-principles-2026-08-28.md`](./sdlc-mvp-first-principles-2026-08-28.md)
and
[`AGENT-PLATFORM-APPROVAL-BRIEF-2026-08-28.md`](./AGENT-PLATFORM-APPROVAL-BRIEF-2026-08-28.md).

**Fit rule:** a candidate may supply a pattern, schema, or adapter lesson. It
does not displace GitHub Issues as intent, Git CAS as ownership, the exact Git
SHA as candidate identity, independent exact-candidate review, or owner-held
promotion authority unless a later approved brief explicitly changes that.

## Pinned repository receipt

`S/F/O` is the checked GitHub API snapshot of stars/forks/open issues. It is a
popularity and maintenance-queue signal only. `Push` is the repository's
`pushed_at`, not proof that the cited component changed or that a release is
safe. License is the pinned license file, not only GitHub's classifier.

| # | Candidate and exact revision | Push / latest official release | S/F/O | Pinned license |
|---:|---|---|---:|---|
| 1 | [`disler/super-simple-software-factory@de31374882e7a4e3e5b7bb9bd09e69dc2f779356`](https://github.com/disler/super-simple-software-factory/tree/de31374882e7a4e3e5b7bb9bd09e69dc2f779356) | 2026-08-04; no GitHub release | 757/189/13 | [MIT](https://github.com/disler/super-simple-software-factory/blob/de31374882e7a4e3e5b7bb9bd09e69dc2f779356/LICENSE) |
| 2 | [`disler/fusion-harness@01a348202482cad0e7d3c34eada180f711aaddd7`](https://github.com/disler/fusion-harness/tree/01a348202482cad0e7d3c34eada180f711aaddd7) | 2026-08-23; no GitHub release | 462/92/7 | [MIT](https://github.com/disler/fusion-harness/blob/01a348202482cad0e7d3c34eada180f711aaddd7/LICENSE) |
| 3 | [`disler/the-verifier-agent@aa18d68bcf886fb2a061ca5a76c6d2e1f3516501`](https://github.com/disler/the-verifier-agent/tree/aa18d68bcf886fb2a061ca5a76c6d2e1f3516501) | 2026-05-03; no GitHub release | 159/46/0 | [MIT](https://github.com/disler/the-verifier-agent/blob/aa18d68bcf886fb2a061ca5a76c6d2e1f3516501/LICENSE) |
| 4 | [`github/gh-aw@7c9958c9abde37967bbefe16da92fb551139bee2`](https://github.com/github/gh-aw/tree/7c9958c9abde37967bbefe16da92fb551139bee2) | 2026-08-28; [`v0.86.2`, 2026-08-11](https://github.com/github/gh-aw/releases/tag/v0.86.2) | 5,027/512/320 | [MIT](https://github.com/github/gh-aw/blob/7c9958c9abde37967bbefe16da92fb551139bee2/LICENSE) |
| 5 | [`OpenHands/OpenHands@d573456dc69332736250d265ca22b358f5aa7e30`](https://github.com/OpenHands/OpenHands/tree/d573456dc69332736250d265ca22b358f5aa7e30) | 2026-08-28; [`v1.16.0`, 2026-08-27](https://github.com/OpenHands/OpenHands/releases/tag/v1.16.0) | 85,455/11,177/605 | [MIT](https://github.com/OpenHands/OpenHands/blob/d573456dc69332736250d265ca22b358f5aa7e30/LICENSE) |
| 6 | [`gastownhall/beads@71377f276968b452ee607177637970a4ff888584`](https://github.com/gastownhall/beads/tree/71377f276968b452ee607177637970a4ff888584) | 2026-08-28; [`v1.2.2`, 2026-08-15](https://github.com/gastownhall/beads/releases/tag/v1.2.2) | 26,684/1,801/802 | [MIT](https://github.com/gastownhall/beads/blob/71377f276968b452ee607177637970a4ff888584/LICENSE) |
| 7 | [`gastownhall/gastown@649b832b7672bc7a2dbef26f5983aba6198b819b`](https://github.com/gastownhall/gastown/tree/649b832b7672bc7a2dbef26f5983aba6198b819b) | 2026-08-19; [`v1.2.1`, 2026-06-06](https://github.com/gastownhall/gastown/releases/tag/v1.2.1) | 17,824/1,641/444 | [MIT](https://github.com/gastownhall/gastown/blob/649b832b7672bc7a2dbef26f5983aba6198b819b/LICENSE) |
| 8 | [`garrytan/gstack@b5a951e62398abc8aea5beed429cc2617184fcc1`](https://github.com/garrytan/gstack/tree/b5a951e62398abc8aea5beed429cc2617184fcc1) | 2026-08-28; no GitHub release | 130,207/19,580/809 | [MIT](https://github.com/garrytan/gstack/blob/b5a951e62398abc8aea5beed429cc2617184fcc1/LICENSE) |
| 9 | [`first-fluke/oh-my-agent@ca736256275e4dc8c15a1fe967eb8c8d1df5fddc`](https://github.com/first-fluke/oh-my-agent/tree/ca736256275e4dc8c15a1fe967eb8c8d1df5fddc) | 2026-08-28; [`cli-v12.8.0`, 2026-08-28](https://github.com/first-fluke/oh-my-agent/releases/tag/cli-v12.8.0) | 1,254/148/1 | [MIT](https://github.com/first-fluke/oh-my-agent/blob/ca736256275e4dc8c15a1fe967eb8c8d1df5fddc/LICENSE) |
| 10 | [`temporalio/temporal@5ed21eb39b8b46031666c59afc51ea3f87ad8fd0`](https://github.com/temporalio/temporal/tree/5ed21eb39b8b46031666c59afc51ea3f87ad8fd0) | 2026-08-28; [`v1.31.2`, 2026-07-08](https://github.com/temporalio/temporal/releases/tag/v1.31.2) | 22,585/1,844/932 | [MIT](https://github.com/temporalio/temporal/blob/5ed21eb39b8b46031666c59afc51ea3f87ad8fd0/LICENSE) |
| 11 | [`cline/cline@1fbcfab05dccad23c12ef75ce45f99d711a82fb7`](https://github.com/cline/cline/tree/1fbcfab05dccad23c12ef75ce45f99d711a82fb7) | 2026-08-28; [`desktop-v0.0.20`, 2026-08-28](https://github.com/cline/cline/releases/tag/desktop-v0.0.20) | 67,077/7,240/1,134 | [Apache-2.0](https://github.com/cline/cline/blob/1fbcfab05dccad23c12ef75ce45f99d711a82fb7/LICENSE) |
| 12 | [`aaif-goose/goose@ef0924a0a03e1231340b28b9a76975729896daa5`](https://github.com/aaif-goose/goose/tree/ef0924a0a03e1231340b28b9a76975729896daa5) | 2026-08-28; [`v1.48.0`, 2026-08-27](https://github.com/aaif-goose/goose/releases/tag/v1.48.0) | 53,617/6,131/221 | [Apache-2.0](https://github.com/aaif-goose/goose/blob/ef0924a0a03e1231340b28b9a76975729896daa5/LICENSE) |
| 13 | [`github/spec-kit@684670871fc81a0510ad0c9f0522a5e02d3043c9`](https://github.com/github/spec-kit/tree/684670871fc81a0510ad0c9f0522a5e02d3043c9) | 2026-08-28; [`v1.0.1`, 2026-08-21](https://github.com/github/spec-kit/releases/tag/v1.0.1) | 132,034/11,864/336 | [MIT](https://github.com/github/spec-kit/blob/684670871fc81a0510ad0c9f0522a5e02d3043c9/LICENSE) |
| 14 | [`daystar7777/agent-work-mem@45d683c4b3f1766244a780e2542a8209219e839f`](https://github.com/daystar7777/agent-work-mem/tree/45d683c4b3f1766244a780e2542a8209219e839f) | 2026-05-10; no GitHub release | 16/4/0 | [MIT](https://github.com/daystar7777/agent-work-mem/blob/45d683c4b3f1766244a780e2542a8209219e839f/LICENSE) |
| 15 | [`Spe1977/cli-collaboration@5954dfd309d574e20bb8abbbc1afae75a96fc8cf`](https://github.com/Spe1977/cli-collaboration/tree/5954dfd309d574e20bb8abbbc1afae75a96fc8cf) | 2026-07-21; [`v2.5.0`, 2026-07-21](https://github.com/Spe1977/cli-collaboration/releases/tag/v2.5.0) | 3/0/0 | [MIT](https://github.com/Spe1977/cli-collaboration/blob/5954dfd309d574e20bb8abbbc1afae75a96fc8cf/LICENSE) |
| 16 | [`OpenMOSS/claude-codex-handoff@baab7913a38bbf114c41c23e6e6bf748b2bf165b`](https://github.com/OpenMOSS/claude-codex-handoff/tree/baab7913a38bbf114c41c23e6e6bf748b2bf165b) | 2026-07-04; no GitHub release | 35/1/0 | [MIT](https://github.com/OpenMOSS/claude-codex-handoff/blob/baab7913a38bbf114c41c23e6e6bf748b2bf165b/LICENSE) |
| 17 | [`AniruddhaHumane/handoff@384a7e5ccaebe63dd95915dd300184066dee4ec9`](https://github.com/AniruddhaHumane/handoff/tree/384a7e5ccaebe63dd95915dd300184066dee4ec9) | 2026-06-22; no GitHub release | 0/0/1 | [MIT](https://github.com/AniruddhaHumane/handoff/blob/384a7e5ccaebe63dd95915dd300184066dee4ec9/LICENSE) |

The earlier local metadata receipt pinned OpenHands at
`226a6d2e68ebd5c86e4f275a0f33ca25f1ee0878`. Upstream advanced during the
same-day research window; the fresher revision above supersedes that row. No
other exact SHA changed between the receipt and this check.

## Candidate findings

### 1. disler/super-simple-software-factory — **Adapt**

- **Observed architecture:** deterministic Python owns named human, agent, and
  code phases; Pydantic-style typed JSON envelopes cross phase seams; gates run
  after agent output; the same session is corrected rather than cold-restarted;
  events stream into a WAL SQLite trace while raw JSONL/files remain the
  rebuildable record. The default runtime is Pi, configuration is YAML, and the
  optional visualizer is Vue/Vite/Bun. [Pinned README](https://github.com/disler/super-simple-software-factory/blob/de31374882e7a4e3e5b7bb9bd09e69dc2f779356/README.md).
- **Explicit limits/failures:** the README says v1 runs Pi only and that
  `claude_code` is schema-valid but stubbed; provider credentials are not
  preflighted and may fail partway through a chain; `--force` overwrites all
  stamped files, including prompts/config; sessions and SQLite are gitignored.
- **Maturity/adoption signal:** no GitHub release; the main branch is a skill,
  while the project's own example branch carries demos/traces. That is useful
  implementation evidence, not independent production adoption.
- **Reusable mechanism:** code-owned phase graph, explicit code phases, typed
  envelopes, postcondition gates, correction-in-place, raw evidence plus a
  queryable mirror.
- **Fit boundary (inference):** adapt the phase/envelope/gate concepts inside
  the existing authority contract. Do not stamp its task database or runtime
  ownership model into every consumer repo, and do not call it provider-neutral
  until each adapter passes behavioral probes.

### 2. disler/fusion-harness — **Adapt**

- **Observed architecture:** a TypeScript Pi extension runs 2–5 model slots,
  requires one architect and one primary builder, validates a collaboration DAG,
  executes dependency-ready read tasks concurrently, and serializes write tasks
  behind a canonical-CWD atomic writer lease. It keeps per-slot sessions only
  for the lifetime of the app process and stores run evidence under
  `/tmp/fusion-harness-*`. [Pinned README](https://github.com/disler/fusion-harness/blob/01a348202482cad0e7d3c34eada180f711aaddd7/README.md).
- **Dependencies/stack:** Node/TypeScript, Pi, YAML, `just`, `jq`, `uv`, tmux,
  and provider credentials; the README reports 34 deterministic tests.
- **Explicit limits/failures:** quitting Pi discards every slot transcript;
  child models registered only through another extension are rejected;
  `/fh-collaborate` forbids child worktree commands; the writer lease is scoped
  to a canonical working directory, not a distributed Git ownership lease.
- **Maturity/adoption signal:** no official release and no external deployment
  receipt reviewed. Checked-in tests and run artifacts are stronger than a
  prompt-only demo but do not prove crash recovery or distributed safety.
- **Reusable mechanism:** independent proposals, validated DAG, dependency-ready
  scheduling, one write token, red-first acceptance gate, bounded validation
  loop, exact ACK/evidence panels.
- **Fit boundary:** use these mechanisms inside one admitted attempt. Git CAS and
  resource leases remain authoritative across processes/machines; durable Git
  checkpoints, not Pi slot memory or `/tmp`, carry recovery.

### 3. disler/the-verifier-agent — **Adapt**

- **Observed architecture:** a builder Pi emits lifecycle ticks over a Unix
  socket; an input-locked verifier reads the builder's session JSONL, runs
  deterministic read-only checks, and may inject corrective follow-ups for at
  most three loops before human escalation. [Pinned README and known limits](https://github.com/disler/the-verifier-agent/blob/aa18d68bcf886fb2a061ca5a76c6d2e1f3516501/README.md).
- **Dependencies/stack:** TypeScript/Node 20+, Pi, tmux, Unix sockets, JSONL;
  macOS/Linux, with Windows-native untested.
- **Explicit limits/failures:** one verifier per builder; no late attach across
  processes; read-only is a tool surface, not a sandbox; verifier and builder
  share the same user/filesystem and provider environment; a transcript is its
  observation source.
- **Maturity/adoption signal:** no release and no independent operational
  adoption evidence reviewed.
- **Reusable mechanism:** decompose claims into atomic checks, distinguish
  verified/partial/failed, surface unverifiable gaps, cap feedback loops, and
  escalate rather than self-approve.
- **Fit boundary:** retain a different actor/model context and exact candidate
  receipts. The reviewer should inspect Git state and artifacts directly; the
  generator's transcript may be supporting context, never review authority.

### 4. github/gh-aw — **Keep** for the CI-side safety pattern

- **Observed architecture:** Markdown plus YAML frontmatter is compiled into a
  standard GitHub Actions lock workflow. Deterministic Actions remain the build,
  test, and deployment layer; reasoning tasks run in a read-only sandbox by
  default; configured writes are buffered, validated, and applied later by
  scoped `safe-outputs` jobs. Engines include Copilot, Claude Code, Codex,
  Gemini, and Pi. [Pinned README](https://github.com/github/gh-aw/blob/7c9958c9abde37967bbefe16da92fb551139bee2/README.md) and [security policy](https://github.com/github/gh-aw/blob/7c9958c9abde37967bbefe16da92fb551139bee2/SECURITY.md).
- **Dependencies/stack:** Go CLI/compiler plus generated GitHub Actions YAML,
  JavaScript/Node tooling, schemas, linters, and container actions.
- **Explicit limits/failures:** controls are configurable and authors must
  review permissions, tools, network, and generated files; upstream explicitly
  warns that careful supervision is still required. Releases `0.68.4` through
  `0.71.3` were retired for a billing bug.
- **Maturity/adoption signal:** GitHub-owned, tagged releases, active issues and
  CI; this supports maintenance confidence but does not prove every workflow or
  engine is safe.
- **Reusable mechanism:** compile human-readable source to deterministic locked
  workflow, default read-only execution, move mutations into separately scoped
  jobs, and preserve deterministic CI beside agent judgment.
- **Fit boundary:** use only after the local exact-candidate receipt exists. It
  is a CI/promotion adapter, not the local attempt lease, checkpoint store, or
  human merge authorization.

### 5. OpenHands/OpenHands (Agent Canvas) — **Defer**

- **Observed architecture:** the repository is now the beta Agent Canvas
  frontend/control center. It selects among local, remote, Docker, VM, cloud,
  OpenHands, or ACP-compatible backends. The canonical Agent Server/API and
  conversations live in `software-agent-sdk`; a TypeScript client connects the
  UI; a separate automation repository owns schedules, webhooks, history, and
  dispatch. [Pinned README and repository boundaries](https://github.com/OpenHands/OpenHands/blob/d573456dc69332736250d265ca22b358f5aa7e30/README.md), [pinned package manifest](https://github.com/OpenHands/OpenHands/blob/d573456dc69332736250d265ca22b358f5aa7e30/package.json).
- **Dependencies/stack:** Node 22, TypeScript, React 19, React Router, Vite,
  Socket.IO client, Electron, optional Docker, and external Python agent/automation
  services.
- **Explicit limits/failures:** the project labels itself beta. The no-sandbox
  launcher gives the agent full filesystem access; even the Docker path exposes
  the mounted projects directory. The product boundary spans four repositories.
- **Maturity/adoption signal:** packaged release, npm/Docker surfaces, extensive
  test tooling and a large public community; still explicitly beta.
- **Reusable mechanism:** provider/backend registry, ACP seam, separate UI,
  agent-server, client, and automation ownership, plus explicit sandbox warning.
- **Fit boundary:** defer the control-center/service stack until the thin Git
  contract proves demand for a long-lived UI/API. Evaluate the Agent Server as
  an adapter, not as execution authority.

### 6. gastownhall/beads — **Adapt**

- **Observed architecture:** a Go CLI stores structured issues in a
  version-controlled Dolt database, supports formulas/dependencies and explicit
  tracker synchronization. Security documentation says sync is user-initiated,
  external issue content is untrusted and sanitized/size-limited, and issue IDs
  and SQL inputs are validated. [Pinned tree](https://github.com/gastownhall/beads/tree/71377f276968b452ee607177637970a4ff888584) and [security model](https://github.com/gastownhall/beads/blob/71377f276968b452ee607177637970a4ff888584/SECURITY.md).
- **Dependencies/stack:** Go, Dolt/versioned SQL, Cobra; tracker adapters.
- **Explicit limits/failures:** Dolt sends usage metrics by default unless
  disabled; tokens placed in beads config are plaintext; issue data is
  plaintext with no built-in encryption/access control; audit is Git/Dolt
  history; documentation says it is for development/internal use, not secret
  management.
- **Maturity/adoption signal:** post-1.0 release and security support statement;
  active queue. No proof reviewed that its sync is conflict-free for this exact
  GitHub/source-authority model.
- **Reusable mechanism:** structured dependency graph, deterministic tracker
  boundary, JSON output that separates metadata from free text, explicit
  prompt-injection treatment, and versioned history.
- **Fit boundary:** do not add Dolt or a second issue authority to the MVP.
  Adapt its untrusted-input and deterministic-sync rules to the GitHub Issue
  projection; revisit storage only if measured scale makes Git refs/manifests
  insufficient.

### 7. gastownhall/gastown — **Reject** as the MVP control plane

- **Observed architecture:** a Go/tmux workspace manager coordinates a Mayor,
  project rigs, persistent identities, ephemeral workers, Git-worktree hooks,
  Beads convoys/formulas, watchdog tiers, a daemon, scheduler, escalation, and
  session discovery from event logs. [Pinned README](https://github.com/gastownhall/gastown/blob/649b832b7672bc7a2dbef26f5983aba6198b819b/README.md).
- **Dependencies/stack:** Go 1.26+, Dolt, Beads, SQLite CLI, ICU/CGO, tmux,
  shell integration, optional Docker Compose, and coding-agent CLIs.
- **Explicit limits/failures:** upstream calls it experimental; workers share
  filesystem access, execute shell as the user, and can push remotes. Full mode
  starts Dolt, daemon, Deacon, Mayor, Witnesses, and Refineries. Native Windows
  has material toolchain limits. [Pinned security scope](https://github.com/gastownhall/gastown/blob/649b832b7672bc7a2dbef26f5983aba6198b819b/SECURITY.md).
- **Maturity/adoption signal:** official releases and active community, but the
  security policy's experimental label and broad host authority dominate fit.
- **Reusable mechanism:** capacity governor, explicit stalled-worker escalation,
  teardown roles, dependency-aware convoys, and persistent identity separate
  from ephemeral sessions.
- **Fit boundary:** these ideas can inform later operations, but installing Gas
  Town would duplicate the issue/task state, add long-lived services, and
  broaden shell/remote authority beyond the smallest coherent MVP.

### 8. garrytan/gstack — **Quarantine**

- **Observed architecture:** a large skill/process distribution generates
  runtime-specific skill projections, supplies review/QA/security/release roles,
  browser automation, local JSONL state, worktree execution for some flows,
  deterministic static tests and paid E2E/model-judge tiers. The architecture
  records explicit command side-effect classes, atomic partial-eval writes,
  hash-chained egress receipts, and several known non-goals. [Pinned README](https://github.com/garrytan/gstack/blob/b5a951e62398abc8aea5beed429cc2617184fcc1/README.md) and [architecture](https://github.com/garrytan/gstack/blob/b5a951e62398abc8aea5beed429cc2617184fcc1/ARCHITECTURE.md).
- **Dependencies/stack:** Bun/TypeScript, Claude Code first, generated skills for
  multiple hosts, Chromium/Playwright, optional local ONNX classifier, GitHub
  CLI, and numerous host/service integrations.
- **Explicit limits/failures:** team mode performs automatic update checks;
  `/ship` and `/land-and-deploy` intentionally push/merge/deploy; an egress
  receipt is forensic rather than an exfiltration control and some user-facing
  sinks fail open if receipt writing fails; no multi-user server; several
  platform-specific credential limitations.
- **Maturity/adoption signal:** very high popularity and extensive checked-in
  tests, but no GitHub release and many upstream claims are self-reported.
- **Reusable mechanism:** generated-skill drift test, thin preamble runtime,
  side-effect classification, egress receipt caveats, explicit test tiers,
  independent second-opinion review, and failure-first investigation.
- **Fit boundary:** audit and selectively extract narrow patterns only. Do not
  install or auto-update the bundle, import deployment commands, or accept its
  mutable home state as platform authority without separate approval and local
  activation receipts.

### 9. first-fluke/oh-my-agent — **Quarantine**

- **Observed architecture:** `.agents/` is presented as a source tree projected
  into multiple runtime layouts; the Bun CLI installs workflows, rules, hooks,
  model routing, orchestration, and dashboards. It includes staged workflows,
  fresh reviewer sessions, trigger tests, and a broad role/skill catalog.
  [Pinned README](https://github.com/first-fluke/oh-my-agent/blob/ca736256275e4dc8c15a1fe967eb8c8d1df5fddc/README.md).
- **Dependencies/stack:** Bun/TypeScript, `uv`, Serena, runtime-specific hooks,
  CLI adapters, web UI, and many optional vendor integrations.
- **Explicit limits/failures:** `oma-config.yaml` is code-equivalent: configured
  binary paths, arguments, flags, and environment variables execute as the
  current user. Backup migrations may retain user-edited content. [Pinned
  security warning](https://github.com/first-fluke/oh-my-agent/blob/ca736256275e4dc8c15a1fe967eb8c8d1df5fddc/SECURITY.md).
- **Maturity/adoption signal:** frequent tagged CLI releases and CI/eval claims;
  compatibility and trigger-accuracy statements remain upstream claims until
  locally reproduced per runtime/version.
- **Reusable mechanism:** canonical source plus runtime projections, selective
  two-layer loading, fresh-context review, explicit trigger fixtures, and
  honest degradation when providers are unavailable.
- **Fit boundary:** no bulk installation or config execution. Evaluate one
  projection/trigger mechanism at a time in disposable homes, with source hash,
  loader probe, denial test, and rollback receipt.

### 10. temporalio/temporal — **Defer**

- **Observed architecture:** a durable-execution server persists workflow
  history and coordinates language-specific workers/activities, handling
  intermittent failures and retries. The server is Go; workflows live in SDKs;
  production deployment adds persistence, namespaces, visibility, and worker
  operations. [Pinned README](https://github.com/temporalio/temporal/blob/5ed21eb39b8b46031666c59afc51ea3f87ad8fd0/README.md) and [architecture index](https://github.com/temporalio/temporal/tree/5ed21eb39b8b46031666c59afc51ea3f87ad8fd0/docs/architecture).
- **Maturity/adoption signal:** the official README calls it mature, it has a
  long tagged release stream, tests, proposals, multiple SDKs, and active
  maintenance. Those are strong project signals, still not a fit proof.
- **Explicit limits/failures:** operationally it is a server platform, not a
  file-only library; workflow code must obey deterministic-replay constraints;
  activities, workers, persistence, upgrades, and visibility create an
  operations surface the MVP intentionally avoids.
- **Reusable mechanism:** durable history, retry/timeout semantics, explicit
  workflow/activity split, and replay-safe state transitions.
- **Fit boundary:** defer until measured requirements exceed Git checkpoints
  and CI—for example multi-day timers, high-volume external effects, or durable
  compensation. Do not add Temporal to solve context loss that Git already
  solves.

### 11. cline/cline — **Defer**

- **Observed architecture:** a Bun/Node monorepo exposes a shared SDK/agent core
  through CLI, VS Code, desktop, and a separately owned Kanban service. The
  README documents project checkpoints, terminal execution, rules/skills,
  provider abstraction, MCP, teams, schedules, and connector-backed sessions.
  [Pinned README](https://github.com/cline/cline/blob/1fbcfab05dccad23c12ef75ce45f99d711a82fb7/README.md).
- **Dependencies/stack:** Bun 1.3, Node 22, TypeScript SDK packages, a local hub
  daemon, VS Code, and optional Tauri/Rust/Next desktop.
- **Explicit limits/failures:** agent commands run directly as the user; the
  repository documents rebuild/restart requirements between SDK edits, known
  test drift, daemon behavior, and heavy GUI/Tauri prerequisites. Only the most
  recent minor is actively security-patched. [Pinned contributor/runtime
  caveats](https://github.com/cline/cline/blob/1fbcfab05dccad23c12ef75ce45f99d711a82fb7/AGENTS.md), [security policy](https://github.com/cline/cline/blob/1fbcfab05dccad23c12ef75ce45f99d711a82fb7/SECURITY.md).
- **Maturity/adoption signal:** large installed product surface, active release
  stream and issue queue; the latest repository release tag is desktop-specific.
- **Reusable mechanism:** shared agent core behind several clients, explicit
  diff/revert checkpoints, worktree-per-card concept, persistent team state,
  and provider/tool extension seams.
- **Fit boundary:** treat Cline as a runtime adapter target. Do not import its hub,
  Kanban, checkpoint, schedule, or connector state as cross-runtime authority.

### 12. aaif-goose/goose — **Adapt**

- **Observed architecture:** a Rust workspace provides native desktop, CLI, and
  API surfaces, supports many providers, ACP-based subscription providers, and
  MCP extensions. The manifest pins ACP and OpenTelemetry dependencies.
  [Pinned README](https://github.com/aaif-goose/goose/blob/ef0924a0a03e1231340b28b9a76975729896daa5/README.md), [workspace manifest](https://github.com/aaif-goose/goose/blob/ef0924a0a03e1231340b28b9a76975729896daa5/Cargo.toml).
- **Maturity/adoption signal:** AAIF/Linux Foundation governance, active tagged
  releases, CI and cross-platform packaging; no claim that this proves a
  particular provider/extension combination works.
- **Explicit limits/failures:** official security guidance says local developer
  agents can execute code and act on the machine, prompt injection may override
  the user's task, only reviewed extensions should be connected, and sensitive
  actions need human confirmation. [Pinned security policy](https://github.com/aaif-goose/goose/blob/ef0924a0a03e1231340b28b9a76975729896daa5/SECURITY.md).
- **Reusable mechanism:** provider/ACP/MCP boundaries, custom distributions,
  Rust typed interfaces, and explicit human-confirmation/security posture.
- **Fit boundary:** use as an external runtime and adapter reference. Platform
  authorization, leases, exact candidate receipts, and promotion stay outside
  Goose; extension capability discovery must be probed, not assumed.

### 13. github/spec-kit — **Adapt**

- **Observed architecture:** a Python CLI and versioned templates generate a
  feature spec, plan, tasks, checks, and project constitution across supported
  coding agents. The documented flow creates numbered feature branches and
  derives tasks from plan/contracts/data models; templates force clarification,
  testability, and checklists. [Pinned README](https://github.com/github/spec-kit/blob/684670871fc81a0510ad0c9f0522a5e02d3043c9/README.md), [methodology](https://github.com/github/spec-kit/blob/684670871fc81a0510ad0c9f0522a5e02d3043c9/spec-driven.md).
- **Dependencies/stack:** Python 3.11+, `uv`/`pipx`, Git, Jinja-like templates,
  per-agent integrations and shell/PowerShell scripts.
- **Explicit limits/failures:** the README labels major goals experimental;
  supported-agent integration issues are expected; commands perform branch and
  file mutations; the methodology's claim that specifications become source of
  truth conflicts with this MVP's authority order if taken literally.
- **Maturity/adoption signal:** `v1.0.1`, GitHub ownership, tests and large
  popularity; no evidence that generated artifacts stay correct after arbitrary
  brownfield change without human review.
- **Reusable mechanism:** intent -> clarification -> spec -> plan -> task graph,
  explicit constitution, testable acceptance criteria, templates as validators,
  and dependency/parallel annotations.
- **Fit boundary:** adapt artifact shapes and validation questions. Git and
  observed behavior remain executable truth; generated specs are reviewed intent,
  not self-enforcing authority. Branch creation remains behind admission.

### 14. daystar7777/agent-work-mem — **Reject** as execution authority

- **Observed architecture:** plain Markdown under `AIMemory/` provides an index,
  project overview, append-only hot log, archive/cold tiers, and handoff files;
  optional tmux delivers pointers. The protocol proposes atomic small appends,
  optional `flock`, and per-session logs on cloud-synced storage. [Pinned README](https://github.com/daystar7777/agent-work-mem/blob/45d683c4b3f1766244a780e2542a8209219e839f/README.md), [protocol](https://github.com/daystar7777/agent-work-mem/blob/45d683c4b3f1766244a780e2542a8209219e839f/PROTOCOL.md).
- **Dependencies/stack:** Markdown and agent compliance; optional shell/tmux/
  `flock`; no daemon/database.
- **Explicit limits/failures:** correctness depends on agents reading and
  appending the protocol; `flock` is host-local; cloud sync has conflict-copy
  races; logs and handoffs are prose and do not bind exact Git/artifact state;
  the repository has no release or visible test/CI surface at the pinned root.
- **Maturity/adoption signal:** README self-labels stable v2, but the release and
  verification evidence needed to support that label was not found.
- **Reusable mechanism:** tiered context, explicit rejected-path/next-action
  handoff fields, and the warning that transport is not truth.
- **Fit boundary:** do not make `AIMemory` or a universal worklog mandatory.
  Required recovery state belongs in typed Git checkpoints and hashed receipts;
  prose memory stays optional supporting context.

### 15. Spe1977/cli-collaboration — **Adapt**

- **Observed architecture:** `AGENT_HANDOFF.md` carries explicit task, files,
  red test, reserved zones, and stop condition; Bash/Python guardrails parse
  ownership, report drift/conflicts, and run fixtures across macOS/Linux. The
  repository documents six semantic eval scenarios and release gates.
  [Pinned README](https://github.com/Spe1977/cli-collaboration/blob/5954dfd309d574e20bb8abbbc1afae75a96fc8cf/README.md).
- **Dependencies/stack:** Markdown skill, Bash, Python 3, runtime adapters and
  GitHub Actions.
- **Explicit limits/failures:** its own README says scripts are guardrails and
  do not replace judgment; `AGENT_HANDOFF.md` has one active writer and locking
  is deferred; native Windows is unsupported; activation differs per runtime
  and can require explicit prompting.
- **Maturity/adoption signal:** `v2.5.0`, documented CI/fixtures and a very small
  public adoption surface; upstream's local verification claims were not rerun.
- **Reusable mechanism:** explicit file ownership/reserved/frozen zones, stop
  conditions, dirty-worktree preservation, conflict checker, and negative tests
  against destructive cleanup.
- **Fit boundary:** adapt fields and checks into typed admission/checkpoint
  contracts. A Markdown owner line is not the atomic attempt lease, and runtime
  activation requires current loader probes.

### 16. OpenMOSS/claude-codex-handoff — **Adapt**

- **Observed architecture:** two append-only directional JSONL streams, locked
  sender sequence assignment, per-session cursors, atomic claim files with
  expiry/renewal, idempotent replay checks, fsync + atomic rename, side-effects-
  before-cursor ordering, notes, archive compaction, read-only doctor, and
  bounded cron/heartbeat polling. [Pinned README](https://github.com/OpenMOSS/claude-codex-handoff/blob/baab7913a38bbf114c41c23e6e6bf748b2bf165b/README.md), [protocol v1.12](https://github.com/OpenMOSS/claude-codex-handoff/blob/baab7913a38bbf114c41c23e6e6bf748b2bf165b/PROTOCOL.md).
- **Dependencies/stack:** Python stdlib helpers, Bash/PowerShell setup, JSONL,
  filesystem locks, Claude cron and Codex heartbeat.
- **Explicit limits/failures:** two named sides, local/project filesystem,
  timer-driven latency, six-hour default leases, and no remote distributed
  consensus. The protocol correctly treats inbound messages as untrusted
  requests and says stale liveness is not failure proof.
- **Maturity/adoption signal:** no release and small public usage surface; the
  protocol is unusually detailed, but no crash/concurrency test matrix or
  hostile-filesystem result was found in this pass.
- **Reusable mechanism:** atomic claim creation, renew/expiry/takeover audit,
  per-session cursors, replay idempotency, terminal messages that are not ACKed
  again, fail-closed authorization checks, bounded wake gate, and doctor.
- **Fit boundary:** adapt these algorithms to the existing Git CAS attempt and
  checkpoint model; generalize identities beyond Claude/Codex; remote Git ref
  ownership remains authoritative. Do not start timers or install the kit as
  part of this research.

### 17. AniruddhaHumane/handoff — **Reject** as execution authority

- **Observed architecture:** two installed skills write per-agent
  `snapshot.json`/`summary.md` and merge one or more snapshots into a current
  resume brief, using the newest as primary. The project is intentionally a
  shell installer plus skills, not a Python runtime. [Pinned README](https://github.com/AniruddhaHumane/handoff/blob/384a7e5ccaebe63dd95915dd300184066dee4ec9/README.md).
- **Dependencies/stack:** shell installer, symlink or copy into Codex/Claude
  skill homes, plain JSON/Markdown files.
- **Explicit limits/failures:** it intentionally cannot preserve hidden model
  state; snapshots are usually local/uncommitted; no atomic ownership,
  candidate-hash binding, signing, conflict algorithm, or behavioral tests were
  found at the pinned root. Newest timestamp is not necessarily most
  authoritative or correct.
- **Maturity/adoption signal:** no release, zero-star snapshot, and one open
  issue; this is insufficient to infer operational maturity.
- **Reusable mechanism:** concise summary, next action, open tasks, decisions,
  blockers, touched/read-first files, verification state, confidence, and
  uncertainty.
- **Fit boundary:** use those fields only inside the typed Git checkpoint.
  Reject installed snapshot skills as a second state authority.

## Standards and ecosystem mechanisms

### 18. SLSA — **Keep** the provenance vocabulary; do not claim a level

- **Pinned sources:** [`slsa-framework/slsa@1686afeba11a456e470235ecf50cfc0d2f9ecbc3`](https://github.com/slsa-framework/slsa/tree/1686afeba11a456e470235ecf50cfc0d2f9ecbc3), pushed 2026-08-09 (1,916/290/174; no GitHub release). The specification is under [Community Specification License 1.0, with documented Apache-2.0 treatment for pre-existing portions](https://github.com/slsa-framework/slsa/blob/1686afeba11a456e470235ecf50cfc0d2f9ecbc3/LICENSE.md).
- **Observed concept:** an attestation is authenticated machine-readable
  metadata whose Statement binds `subject` artifacts to a typed `predicate`;
  explicit metadata separates meaning from the signature. SLSA provenance
  describes where/how an artifact was produced and treats external parameters
  as untrusted downstream inputs. [Attestation model](https://github.com/slsa-framework/slsa/blob/1686afeba11a456e470235ecf50cfc0d2f9ecbc3/spec/attestation-model.md), [build provenance](https://github.com/slsa-framework/slsa/blob/1686afeba11a456e470235ecf50cfc0d2f9ecbc3/spec/build-provenance.md).
- **Explicit limits:** storage/lookup is marked TBD in the model; provenance is
  only as trustworthy as its builder/attester and verification policy; the
  framework's levels concern supply-chain controls, not agent quality or review
  correctness.
- **Fit boundary:** keep subject digest, builder/adapter identity, external
  parameters, resolved dependencies, byproducts, and verification policy in the
  receipt vocabulary. Do not advertise a SLSA Build Level for an agent run
  without a conforming builder, threat model, and independent verification.

### 19. in-toto — **Adapt** Statement/attestation structure

- **Pinned sources:** [`in-toto/attestation@2dcd055e9f72e746687c306e35f4e59720ff45be`](https://github.com/in-toto/attestation/tree/2dcd055e9f72e746687c306e35f4e59720ff45be), pushed 2026-08-24, [`v1.2.0`](https://github.com/in-toto/attestation/releases/tag/v1.2.0), [Apache-2.0](https://github.com/in-toto/attestation/blob/2dcd055e9f72e746687c306e35f4e59720ff45be/LICENSE); and [`in-toto/in-toto@e352b43ad7cb8915d84c36d791aa61346152a0a3`](https://github.com/in-toto/in-toto/tree/e352b43ad7cb8915d84c36d791aa61346152a0a3), pushed 2026-08-27, [`v3.1.0`](https://github.com/in-toto/in-toto/releases/tag/v3.1.0), [Apache-2.0](https://github.com/in-toto/in-toto/blob/e352b43ad7cb8915d84c36d791aa61346152a0a3/LICENSE).
- **Observed concept:** the attestation repository defines versioned Statement,
  ResourceDescriptor and predicate schemas/protobufs across languages. The
  reference implementation models a signed software-supply-chain layout and
  link metadata for steps/inspections. [Attestation README](https://github.com/in-toto/attestation/blob/2dcd055e9f72e746687c306e35f4e59720ff45be/README.md), [reference model](https://github.com/in-toto/in-toto/blob/e352b43ad7cb8915d84c36d791aa61346152a0a3/doc/source/model.md).
- **Explicit limits:** generic schemas do not define the semantics of an agent
  acceptance predicate, nor do signatures prove the claim is true. Key,
  identity, policy, storage, and verification lifecycle remain separate.
- **Fit boundary:** adapt a versioned `agent-candidate` predicate carried in an
  in-toto-style Statement: subject exact Git/artifact digests; predicate exact
  inputs, adapter/model/effort when observable, gates, review, boundaries, and
  unknowns. Defer DSSE/signing until a threat model selects identities and keys.

### 20. Sigstore — **Defer** signing and transparency integration

- **Pinned sources:** [`sigstore/docs@842c30981f1bf5061fe0d370512db4de8cdf3b33`](https://github.com/sigstore/docs/tree/842c30981f1bf5061fe0d370512db4de8cdf3b33), pushed 2026-08-25, [MIT docs license](https://github.com/sigstore/docs/blob/842c30981f1bf5061fe0d370512db4de8cdf3b33/LICENSE); [`sigstore/cosign@58aae9e112fa1de80594eed34667e920ac4d4a3b`](https://github.com/sigstore/cosign/tree/58aae9e112fa1de80594eed34667e920ac4d4a3b), pushed 2026-08-24, [`v3.1.3`](https://github.com/sigstore/cosign/releases/tag/v3.1.3), [Apache-2.0](https://github.com/sigstore/cosign/blob/58aae9e112fa1de80594eed34667e920ac4d4a3b/LICENSE).
- **Observed concept:** keyless signing uses an OIDC identity, Fulcio
  short-lived certificate, Rekor transparency log, certificate transparency,
  and TUF-distributed trust roots. Cosign signs/verifies artifacts and
  attestations. [Security overview](https://github.com/sigstore/docs/blob/842c30981f1bf5061fe0d370512db4de8cdf3b33/content/en/about/security.md), [threat model](https://github.com/sigstore/docs/blob/842c30981f1bf5061fe0d370512db4de8cdf3b33/content/en/about/threat-model.md).
- **Explicit limits:** Sigstore proves control of an identity, not whether that
  identity should be trusted or whether an attested claim is correct. Its own
  threat model requires an external policy, discusses OIDC/Fulcio/Rekor/root
  compromise, and recommends monitoring and 2FA. Public transparency may expose
  identity/artifact metadata inappropriate for private work.
- **Fit boundary:** first make unsigned local receipts deterministic and bind
  them to exact subjects. Add Cosign only when CI promotion needs cryptographic
  identity/non-repudiation and the owner approves identity provider, public vs
  private log, trust roots, revocation, retention, and verifier policy.

### 21. OpenTelemetry — **Adapt** stable trace primitives; quarantine GenAI names

- **Pinned core:** [`opentelemetry-specification@8057bf6d5cf0ab10891b9e6f7b928cded76ab2f7`](https://github.com/open-telemetry/opentelemetry-specification/tree/8057bf6d5cf0ab10891b9e6f7b928cded76ab2f7), pushed 2026-08-27, [`v1.60.0`](https://github.com/open-telemetry/opentelemetry-specification/releases/tag/v1.60.0), [Apache-2.0](https://github.com/open-telemetry/opentelemetry-specification/blob/8057bf6d5cf0ab10891b9e6f7b928cded76ab2f7/LICENSE).
- **Pinned GenAI source:** the core semantic-conventions repository at
  [`106c389363c43729a25cde2e37e4df670d54d3cb`](https://github.com/open-telemetry/semantic-conventions/tree/106c389363c43729a25cde2e37e4df670d54d3cb)
  says GenAI conventions moved and are no longer maintained there. The current
  source is [`semantic-conventions-genai@67dff024110be5bd9f318006e733f4078e0f4c97`](https://github.com/open-telemetry/semantic-conventions-genai/tree/67dff024110be5bd9f318006e733f4078e0f4c97), pushed 2026-08-27, no release, [Apache-2.0](https://github.com/open-telemetry/semantic-conventions-genai/blob/67dff024110be5bd9f318006e733f4078e0f4c97/LICENSE).
- **Observed concept:** stable OTel trace primitives form a DAG of spans with
  trace/span IDs, parent-child relationships, links, attributes, events, status,
  context propagation, SDK/exporter separation, and collector processing.
  [Core overview](https://github.com/open-telemetry/opentelemetry-specification/blob/8057bf6d5cf0ab10891b9e6f7b928cded76ab2f7/specification/overview.md).
- **GenAI status and limits:** the dedicated GenAI documents label the entire
  convention **Development**, including agent creation/invocation, workflow,
  plan, tool, memory, retrieval, model operations, token/cache usage, MCP and
  provider names. They explicitly warn that input/output messages, system
  instructions, prompt variables, and tool definitions may contain sensitive
  information. [GenAI index](https://github.com/open-telemetry/semantic-conventions-genai/blob/67dff024110be5bd9f318006e733f4078e0f4c97/docs/gen-ai/README.md), [agent spans](https://github.com/open-telemetry/semantic-conventions-genai/blob/67dff024110be5bd9f318006e733f4078e0f4c97/docs/gen-ai/gen-ai-agent-spans.md).
- **Fit boundary:** adapt stable trace IDs, parent/link semantics, timestamps,
  status/error class, and OTLP export as an optional mirror. Freeze a small
  versioned project namespace for agent fields until GenAI conventions stabilize.
  Default-deny prompt/content/tool-argument export; prefer hashes, sizes, counts,
  opaque IDs, and redacted error classes. Telemetry is observability, never the
  task lease, receipt authority, or acceptance result.

## Compact disposition matrix

| Candidate | Disposition | What survives the boundary |
|---|---|---|
| `disler/super-simple-software-factory` | **Adapt** | Code-owned phases, typed envelopes, deterministic gates, correction loop, trace mirror |
| `disler/fusion-harness` | **Adapt** | Independent proposals, validated DAG, dependency readiness, one write token, red-first gate |
| `disler/the-verifier-agent` | **Adapt** | Atomic claim decomposition, confidence/gap reporting, bounded correction, human escalation |
| `github/gh-aw` | **Keep** | Compiled locked workflows, read-only default, validated safe outputs, scoped mutation jobs |
| `OpenHands/OpenHands` | **Defer** | ACP/backend boundary and multi-repository service ownership, only after MVP demand |
| `gastownhall/beads` | **Adapt** | Structured dependency data, untrusted issue boundary, deterministic explicit sync |
| `gastownhall/gastown` | **Reject** | Do not adopt control plane; only retain capacity/escalation/teardown lessons |
| `garrytan/gstack` | **Quarantine** | Selectively audit projection, side-effect, egress-receipt and eval-tier patterns |
| `first-fluke/oh-my-agent` | **Quarantine** | One projection/trigger mechanism at a time in disposable runtime homes |
| `temporalio/temporal` | **Defer** | Durable workflows only after measured long-running/external-effect need |
| `cline/cline` | **Defer** | Treat as an external runtime; evaluate SDK/checkpoint/worktree interfaces later |
| `aaif-goose/goose` | **Adapt** | ACP/provider/MCP adapter seams and explicit confirmation/security posture |
| `github/spec-kit` | **Adapt** | Clarification, spec/plan/task artifact shapes, constitution and testable acceptance |
| `daystar7777/agent-work-mem` | **Reject** | Keep only optional handoff/context fields; no Markdown execution authority |
| `Spe1977/cli-collaboration` | **Adapt** | Ownership/reserved zones, stop conditions, conflict checks, destructive negative tests |
| `OpenMOSS/claude-codex-handoff` | **Adapt** | Atomic claims, renewal/takeover, cursors, idempotency, bounded polling and doctor |
| `AniruddhaHumane/handoff` | **Reject** | Fold concise snapshot fields into typed checkpoint; no second authority |
| SLSA | **Keep** | Subject/builder/input/dependency/byproduct/provenance vocabulary; no level claim |
| in-toto | **Adapt** | Versioned Statement plus agent-candidate predicate; signing later |
| Sigstore | **Defer** | Identity-backed signatures/transparency only after threat/policy decision |
| OpenTelemetry | **Adapt** | Stable trace primitives and optional OTLP mirror; GenAI names version-pinned/development |

## Reconciled SOTA lessons for the current architecture

1. **The durable seam is an exact subject plus typed evidence, not a chat.**
   SLSA/in-toto, SSSF, gh-aw, OpenMOSS, and the stronger handoff projects all
   converge on explicit subjects, structured messages, deterministic code,
   and inspectable evidence. The MVP should bind every gate/review to exact Git
   and artifact digests.
2. **Isolation, scheduling, and ownership are different controls.** Worktrees
   isolate bytes; DAGs order dependencies; a write token serializes one process;
   only a compare-and-swap attempt/resource lease establishes cross-process
   ownership. No candidate justifies collapsing these concepts.
3. **Deterministic code precedes model judgment.** SSSF, fusion, gh-aw, Spec Kit,
   and gstack all encode deterministic steps around reasoning. A model should
   not rediscover test commands, self-assert acceptance, or perform promotion.
4. **A fresh reviewer must see the exact candidate, not merely the generator's
   story.** The verifier pattern is useful, but transcript observation alone is
   weaker than direct Git/artifact inspection. Review invalidates on any subject
   change.
5. **Provider neutrality is behavioral.** A common schema, copied skill, ACP
   claim, or projection is not activation proof. Each adapter needs current
   loader, tool, identity, model/effort, cancellation, checkpoint, and denial
   probes.
6. **Long-lived platforms are not free durability.** Temporal, OpenHands, Gas
   Town, Cline, Beads/Dolt, dashboards and daemons solve real higher-scale
   problems while adding operations, security, migration, and second-authority
   risks. The present Git/CI slice should earn those dependencies through
   measured failure.
7. **Observability is a mirror.** SQLite and OTel improve diagnosis, but neither
   owns state. Raw immutable artifacts, Git checkpoints, and receipts must allow
   the mirror to be rebuilt.
8. **Content telemetry is a security boundary.** OTel GenAI content fields,
   external issue text, browser content, handoff messages, MCP results, and
   runtime transcripts are all potentially sensitive or adversarial. Hash and
   classify by default; export content only through explicit policy.

## Unresolved unknowns and pre-implementation proof gates

1. No independent operational adoption evidence was admitted by the
   primary-source-only scope. Packaging, releases, owner, stars and issue
   activity remain signals, not proof.
2. The exact behavior of each candidate under abrupt kill, network partition,
   stale lease, clock skew, disk-full, fsync failure, concurrent checkout, and
   remote Git race was not reproduced locally.
3. Dependency-license, SBOM, vulnerability and transitive-maintainer review was
   not performed; pinned top-level licenses do not clear code import.
4. SSSF's current Pi-only adapter, Fusion's app-lifetime sessions, verifier
   transcript coupling, and OpenMOSS's two-side filesystem design have not been
   generalized or proven against Codex, Claude, Hermes, Buzz, OpenCode and Pi.
5. `gh-aw` engine behavior, sandbox boundaries, safe-output validation and
   billing for the intended private repositories have not been tested; retired
   billing-bug releases show why an exact supported version is required.
6. OpenHands' Agent Canvas/API/automation compatibility matrix and auth model
   across self-hosted backends remain unverified; the repository is beta.
7. Beads/Dolt telemetry-disable behavior, credential retention, tracker conflict
   rules, repository growth and migration/rollback are untested locally.
8. No candidate's marketing/provider-neutral compatibility matrix is accepted
   without current runtime discovery and denial probes.
9. The agent receipt predicate is proposed, not registered with in-toto/SLSA;
   canonical JSON, extension/version policy, and verifier behavior need design
   and deterministic fixtures.
10. Sigstore identity provider, public/private transparency, TUF root, revocation,
    retention and offline verification policy are undecided.
11. OpenTelemetry GenAI semantic conventions are Development and recently moved
    repositories; a version-pinned compatibility layer and redaction policy are
    required before exporting those fields.
12. GitHub Issues/refs availability, offline handoff, claim expiry/takeover and
    one-transition checkpoint freshness still need fault-injection acceptance
    tests in the current repository.

## Approval boundary

This comparison supports the existing thin Git/CI architecture and narrows
reuse to patterns and schemas. It does not authorize installs, runtime/config
changes, dependency additions, scaffolding, product-file edits, commits, pushes,
PRs, deployment, or promotion. Any implementation should remain blocked until
the consolidated brief is explicitly approved for its current scope.

APPROVAL STATUS: awaiting user confirmation
