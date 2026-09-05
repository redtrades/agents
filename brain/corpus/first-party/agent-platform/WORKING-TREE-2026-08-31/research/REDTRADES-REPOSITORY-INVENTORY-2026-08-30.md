# Redtrades repository estate inventory

**Captured:** 2026-08-30 via the authenticated GitHub REST API  
**Account:** `redtrades`  
**Observed total:** 73 owned repositories: 18 active first-party repositories, 54 forks, and 1 archived first-party repository
**Purpose:** historical-intent and prior-art inventory; this is not an adoption list or governing architecture

## First-party product and platform lineage

These repositories contain direct product work or system intent and deserve source-level inspection when their capability is evaluated:

| Family | Repositories | Recovered role |
| --- | --- | --- |
| OpenClaw lineage | `openclaw`, `openclaw-v2`, `openclaw-v3`, `openclaw-backup`, `openclaw-config`, `workspace-main` | Original personal/company agent operating system, declarative Mind/Body/Brain design, workflows, role manifests, UI, knowledge, autonomy, and runtime evidence |
| Current agent lineage | `agent-platform`, `agent-mesh`, `agent-configs`, `agent-workspace` | Transactional authority; portable harness/runtime and research; genome/config library; execution coordination |
| Product factories | `govcon-factory`, `ninov-trader`, `polymarket-arb`, `tesla-swing`, `work-ops` | Domain factories showing that projects need their own sources, schemas, workflows, policies, evaluations, and outputs |
| Earlier products | `curate-and-share-now`, `v0-news-ai`, `webapp` | Research/news/curation product ancestry and user-facing product experiments |
| Infrastructure reference | `terraform-reference-architectures` | Earlier declarative infrastructure interest; useful context, not an agent-company definition |

`work-ops` is the one archived first-party repository in the account snapshot. Archive status does not make its content governing.

## Forked agent, runtime, orchestration, and skill prior art

These forks show the solution spaces repeatedly investigated. Fork presence proves interest or preserved source, not adoption, integration, maintenance, or runtime activation.

- Agent frameworks and swarms: `Fusion`, `claude-agents`, `agents`, `awesome_ai_agents`, `deepagents`, `Subagents`, `awesome-claude-agents`, `claude-flow`, `deep-agents-from-scratch`, `agency-agents`, `agentic-stack`, `social-media-agent`, `factory`.
- Harnesses and coding agents: `codex`, `anyclaude`, `shadow`, `claw-code`, `claude-code`, `openclaude`, `oh-my-codex`, `oh-my-claudecode`, `superpowers`, `gstack`.
- Runtime source/reference snapshots: `claw-cli-claude-code-source-code-v2.1.88`, `claude-code-source-code`, `claude-sessions`.
- Skills, prompts, and catalogs: `skills`, `awesome-openclaw-skills`, `awesome-claude-code`, `leaked-system-prompts`, `system-prompts-and-models-of-ai-tools`, `openai-cookbook`.
- Memory and evolution: `mempalace`, `hermes-agent-self-evolution`.
- Models, interfaces, and tooling: `free-llm-api-resources`, `VibeVoice`, `chrome-devtools-mcp`, `AI-Crash-Course`.

## Older learning and infrastructure forks

These repositories are part of the account but did not supply material evidence for the five-month agent-factory intent:

`airbnb-clone`, `do-article-templates`, `moderndiver-book`, `autoenv`, `python-patterns`, `mapboxgl-jupyter`, `ATM`, `machine_learning_examples`, `data-science-from-scratch`, `tutorialinux-hashistack`, `node-express-boilerplate`, `devops-exercises`, `terraform-guides`, `terraform-aws-ec2-instance`, and `fabric-samples`.

They remain useful biographical/context evidence—especially the Terraform and DevOps material—but are not candidates for wholesale import.

## What this estate says about the original intent

The repository pattern is consistent across time:

1. preserve and compare many agent harnesses rather than bind to one;
2. extract reusable roles, skills, prompts, and memory behavior;
3. use declarative infrastructure and Git-native artifacts;
4. operate several domain-specific product factories through one agent substrate;
5. add proactive monitoring, knowledge, evaluation, and self-evolution; and
6. expose the result through a command surface that minimizes operator queue work.

The estate also exposes the recurrent failure mode: many forks and partial first-party implementations were accumulated without a single capability ledger that said which upstream project owned each responsibility, which source revision was admitted, which adapter was active, and which custom substitute could be deleted.

## Disposition rule

- **Mine first-party lineage deeply** for intent, domain contracts, and verified unique behavior.
- **Evaluate maintained upstream projects at their current upstream revision**, not from an old fork.
- **Keep forks only as provenance pins or patch carriers** when they contain a deliberate delta.
- **Do not infer activation or product readiness from repository presence.**
- **Do not import an archive or fork wholesale.** Adopt a capability only through a named owner, exact revision, conformance tests, and a retirement target for overlapping custom code.
