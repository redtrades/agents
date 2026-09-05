# Canonical Skills Map of Content (MOC)

Master index of all specialized skills across the estate. Used by agents to infer and load matching skills Just-In-Time based on user request keywords and task complexity tiers.

**Total Registered Skills:** 225 across 58 plugins.

## Complexity Tiers
- **Tier 1 (Quick):** Focused single-file fixes, formatting, syntax, and direct configs (<2 min).
- **Tier 2 (MVP):** Standard feature slices, unit tests, and surgical bug fixes (2 to 15 min).
- **Tier 3 (Architecture):** Multi-service refactors, event schemas, distributed sagas, and worktrees.
- **Tier 4 (Audit / Swarm):** Deep security scans, model fine-tuning, reverse engineering, and multi-agent coordination.

---

### Accessibility & Compliance

| Skill | Plugin | Tier | Trigger Keywords / Activation |
| :--- | :--- | :--- | :--- |
| [screen-reader-testing](../plugins/accessibility-compliance/skills/screen-reader-testing/SKILL.md) | `accessibility-compliance` | **Tier 2 (MVP)** | Use when validating screen reader compatibility, debugging accessibility issues, or ensuring assistive technology support |
| [wcag-audit-patterns](../plugins/accessibility-compliance/skills/wcag-audit-patterns/SKILL.md) | `accessibility-compliance` | **Tier 4 (Audit)** | Use when auditing websites for accessibility, fixing WCAG violations, or implementing accessible design patterns |

### Agent Teams

| Skill | Plugin | Tier | Trigger Keywords / Activation |
| :--- | :--- | :--- | :--- |
| [multi-reviewer-patterns](../plugins/agent-teams/skills/multi-reviewer-patterns/SKILL.md) | `agent-teams` | **Tier 2 (MVP)** | Use when working with multi reviewer patterns |
| [parallel-debugging](../plugins/agent-teams/skills/parallel-debugging/SKILL.md) | `agent-teams` | **Tier 4 (Audit)** | Use when working with parallel debugging |
| [parallel-feature-development](../plugins/agent-teams/skills/parallel-feature-development/SKILL.md) | `agent-teams` | **Tier 2 (MVP)** | Use when working with parallel feature development |
| [task-coordination-strategies](../plugins/agent-teams/skills/task-coordination-strategies/SKILL.md) | `agent-teams` | **Tier 2 (MVP)** | Use when working with task coordination strategies |
| [team-communication-protocols](../plugins/agent-teams/skills/team-communication-protocols/SKILL.md) | `agent-teams` | **Tier 2 (MVP)** | Use when working with team communication protocols |
| [team-composition-patterns](../plugins/agent-teams/skills/team-composition-patterns/SKILL.md) | `agent-teams` | **Tier 4 (Audit)** | Use when working with team composition patterns |

### Api Scaffolding

| Skill | Plugin | Tier | Trigger Keywords / Activation |
| :--- | :--- | :--- | :--- |
| [fastapi-templates](../plugins/api-scaffolding/skills/fastapi-templates/SKILL.md) | `api-scaffolding` | **Tier 2 (MVP)** | Use when building new FastAPI applications or setting up backend API projects |

### Avoid Ai Writing

| Skill | Plugin | Tier | Trigger Keywords / Activation |
| :--- | :--- | :--- | :--- |
| [avoid-ai-writing](../plugins/avoid-ai-writing/skills/avoid-ai-writing/SKILL.md) | `avoid-ai-writing` | **Tier 4 (Audit)** | Use when working with avoid ai writing |

### Backend Architecture & Distributed Systems

| Skill | Plugin | Tier | Trigger Keywords / Activation |
| :--- | :--- | :--- | :--- |
| [api-design-principles](../plugins/backend-development/skills/api-design-principles/SKILL.md) | `backend-development` | **Tier 2 (MVP)** | Use when designing new APIs, reviewing API specifications, or establishing API design standards |
| [architecture-patterns](../plugins/backend-development/skills/architecture-patterns/SKILL.md) | `backend-development` | **Tier 3 (Architecture)** | Use when working with architecture patterns |
| [cqrs-implementation](../plugins/backend-development/skills/cqrs-implementation/SKILL.md) | `backend-development` | **Tier 3 (Architecture)** | Use when separating read and write models, optimizing query performance, or building event-sourced systems |
| [event-store-design](../plugins/backend-development/skills/event-store-design/SKILL.md) | `backend-development` | **Tier 3 (Architecture)** | Use when building event sourcing infrastructure, choosing event store technologies, or implementing event persistence patterns |
| [microservices-patterns](../plugins/backend-development/skills/microservices-patterns/SKILL.md) | `backend-development` | **Tier 3 (Architecture)** | Use when building distributed systems, decomposing monoliths, or implementing microservices |
| [projection-patterns](../plugins/backend-development/skills/projection-patterns/SKILL.md) | `backend-development` | **Tier 3 (Architecture)** | Use when implementing CQRS read sides, building materialized views, or optimizing query performance in event-sourced systems |
| [saga-orchestration](../plugins/backend-development/skills/saga-orchestration/SKILL.md) | `backend-development` | **Tier 3 (Architecture)** | Use when working with saga orchestration |
| [temporal-python-testing](../plugins/backend-development/skills/temporal-python-testing/SKILL.md) | `backend-development` | **Tier 2 (MVP)** | Use when implementing Temporal workflow tests or debugging test failures |
| [workflow-orchestration-patterns](../plugins/backend-development/skills/workflow-orchestration-patterns/SKILL.md) | `backend-development` | **Tier 3 (Architecture)** | Use when building long-running processes, distributed transactions, or microservice orchestration |

### Before You Build

| Skill | Plugin | Tier | Trigger Keywords / Activation |
| :--- | :--- | :--- | :--- |
| [before-you-build](../plugins/before-you-build/skills/before-you-build/SKILL.md) | `before-you-build` | **Tier 2 (MVP)** | Use when working with before you build |

### Block No Verify

| Skill | Plugin | Tier | Trigger Keywords / Activation |
| :--- | :--- | :--- | :--- |
| [block-no-verify-hook](../plugins/block-no-verify/skills/block-no-verify-hook/SKILL.md) | `block-no-verify` | **Tier 2 (MVP)** | Use when setting up Claude Code projects that enforce commit quality gates |

### Blockchain Web3

| Skill | Plugin | Tier | Trigger Keywords / Activation |
| :--- | :--- | :--- | :--- |
| [defi-protocol-templates](../plugins/blockchain-web3/skills/defi-protocol-templates/SKILL.md) | `blockchain-web3` | **Tier 2 (MVP)** | Use when building decentralized finance applications or smart contract protocols |
| [nft-standards](../plugins/blockchain-web3/skills/nft-standards/SKILL.md) | `blockchain-web3` | **Tier 2 (MVP)** | Use when creating NFT contracts, building NFT marketplaces, or implementing digital asset systems |
| [solidity-security](../plugins/blockchain-web3/skills/solidity-security/SKILL.md) | `blockchain-web3` | **Tier 4 (Audit)** | Use when writing smart contracts, auditing existing contracts, or implementing security measures for blockchain applications |
| [web3-testing](../plugins/blockchain-web3/skills/web3-testing/SKILL.md) | `blockchain-web3` | **Tier 2 (MVP)** | Use when testing Solidity contracts, setting up blockchain test suites, or validating DeFi protocols |

### Brand Landingpage

| Skill | Plugin | Tier | Trigger Keywords / Activation |
| :--- | :--- | :--- | :--- |
| [brand-landingpage](../plugins/brand-landingpage/skills/brand-landingpage/SKILL.md) | `brand-landingpage` | **Tier 2 (MVP)** | > |

### Business Analytics & Metrics

| Skill | Plugin | Tier | Trigger Keywords / Activation |
| :--- | :--- | :--- | :--- |
| [data-storytelling](../plugins/business-analytics/skills/data-storytelling/SKILL.md) | `business-analytics` | **Tier 2 (MVP)** | Use when presenting analytics to stakeholders, creating data reports, or building executive presentations |
| [kpi-dashboard-design](../plugins/business-analytics/skills/kpi-dashboard-design/SKILL.md) | `business-analytics` | **Tier 2 (MVP)** | Use when working with kpi dashboard design |

### Caveman Token Minimalism

| Skill | Plugin | Tier | Trigger Keywords / Activation |
| :--- | :--- | :--- | :--- |
| [cavecrew](../plugins/caveman/skills/cavecrew/SKILL.md) | `caveman` | **Tier 2 (MVP)** | Use when running multi-agent coordination with terse telegraphic messaging |
| [caveman-compress](../plugins/caveman/skills/caveman-compress/SKILL.md) | `caveman` | **Tier 1 (Quick)** | Use when compressing prompt footprints, context logs, and conversational memory |
| [caveman-learn](../plugins/caveman/skills/caveman-learn/SKILL.md) | `caveman` | **Tier 2 (MVP)** | Use when the user runs "caveman learn", asks to lower their agent's token cost, wants to trim a heavy CLAUDE.md, or wants to offload context they re-paste every session into cavemem |
| [caveman-syntax](../plugins/caveman/skills/caveman-syntax/SKILL.md) | `caveman` | **Tier 1 (Quick)** | Use when user says "caveman mode", "talk like caveman", "use caveman", "less tokens",   "be brief", or invokes /caveman. Also auto-triggers when token efficiency is requested |

### Cicd Automation

| Skill | Plugin | Tier | Trigger Keywords / Activation |
| :--- | :--- | :--- | :--- |
| [deployment-pipeline-design](../plugins/cicd-automation/skills/deployment-pipeline-design/SKILL.md) | `cicd-automation` | **Tier 2 (MVP)** | Use when working with deployment pipeline design |
| [github-actions-templates](../plugins/cicd-automation/skills/github-actions-templates/SKILL.md) | `cicd-automation` | **Tier 2 (MVP)** | Use when setting up CI/CD with GitHub Actions, automating development workflows, or creating reusable workflow templates |
| [gitlab-ci-patterns](../plugins/cicd-automation/skills/gitlab-ci-patterns/SKILL.md) | `cicd-automation` | **Tier 2 (MVP)** | Use when implementing GitLab CI/CD, optimizing pipeline performance, or setting up automated testing and deployment |
| [secrets-management](../plugins/cicd-automation/skills/secrets-management/SKILL.md) | `cicd-automation` | **Tier 2 (MVP)** | Use when handling sensitive credentials, rotating secrets, or securing CI/CD environments |

### Cloud Infrastructure

| Skill | Plugin | Tier | Trigger Keywords / Activation |
| :--- | :--- | :--- | :--- |
| [cost-optimization](../plugins/cloud-infrastructure/skills/cost-optimization/SKILL.md) | `cloud-infrastructure` | **Tier 2 (MVP)** | Use when reducing cloud expenses, analyzing infrastructure costs, or implementing cost governance policies |
| [hybrid-cloud-networking](../plugins/cloud-infrastructure/skills/hybrid-cloud-networking/SKILL.md) | `cloud-infrastructure` | **Tier 3 (Architecture)** | Use when building hybrid cloud architectures, connecting data centers to cloud, or implementing secure cross-premises networking |
| [istio-traffic-management](../plugins/cloud-infrastructure/skills/istio-traffic-management/SKILL.md) | `cloud-infrastructure` | **Tier 2 (MVP)** | Use when implementing service mesh traffic policies, progressive delivery, or resilience patterns |
| [linkerd-patterns](../plugins/cloud-infrastructure/skills/linkerd-patterns/SKILL.md) | `cloud-infrastructure` | **Tier 2 (MVP)** | Use when setting up Linkerd, configuring traffic policies, or implementing zero-trust networking with minimal overhead |
| [mtls-configuration](../plugins/cloud-infrastructure/skills/mtls-configuration/SKILL.md) | `cloud-infrastructure` | **Tier 2 (MVP)** | Use when implementing zero-trust networking, certificate management, or securing internal service communication |
| [multi-cloud-architecture](../plugins/cloud-infrastructure/skills/multi-cloud-architecture/SKILL.md) | `cloud-infrastructure` | **Tier 3 (Architecture)** | Use when building multi-cloud systems, avoiding vendor lock-in, or leveraging best-of-breed services from multiple providers |
| [service-mesh-observability](../plugins/cloud-infrastructure/skills/service-mesh-observability/SKILL.md) | `cloud-infrastructure` | **Tier 2 (MVP)** | Use when setting up mesh monitoring, debugging latency issues, or implementing SLOs for service communication |
| [terraform-module-library](../plugins/cloud-infrastructure/skills/terraform-module-library/SKILL.md) | `cloud-infrastructure` | **Tier 3 (Architecture)** | Use when creating infrastructure modules, standardizing cloud provisioning, or implementing reusable IaC components |

### Cloudflare & Edge Infrastructure

| Skill | Plugin | Tier | Trigger Keywords / Activation |
| :--- | :--- | :--- | :--- |
| [cloudflare](../plugins/cloudflare-platform/skills/cloudflare/SKILL.md) | `cloudflare-platform` | **Tier 3 (Architecture)** | Use when designing and deploying serverless applications on Cloudflare Workers |
| [cloudflare-email-service](../plugins/cloudflare-platform/skills/cloudflare-email-service/SKILL.md) | `cloudflare-platform` | **Tier 2 (MVP)** | Use when building email sending (Workers binding or REST API), email routing, Agents SDK email handling, or integrating email into any app  -  Workers, Node.js, Python, Go, etc. Also use for email deliverability, SPF/DKIM/DMARC, wrangler email setup, MCP email tools, or when a coding agent needs to send emails. Even for simple requests like "add email to my Worker"  -  this skill has critical config details |
| [cloudflare-one](../plugins/cloudflare-platform/skills/cloudflare-one/SKILL.md) | `cloudflare-platform` | **Tier 2 (MVP)** | Use when designing, configuring, troubleshooting, or reviewing Cloudflare One deployments. Retrieval-first: use current Cloudflare docs/API schemas instead of embedded product docs |
| [cloudflare-one-migrations](../plugins/cloudflare-platform/skills/cloudflare-one-migrations/SKILL.md) | `cloudflare-platform` | **Tier 2 (MVP)** | Use when migrating network infrastructure to Cloudflare One |
| [durable-objects](../plugins/cloudflare-platform/skills/durable-objects/SKILL.md) | `cloudflare-platform` | **Tier 3 (Architecture)** | Use when building stateful coordination (chat rooms, multiplayer games, booking systems), implementing RPC methods, SQLite storage, alarms, WebSockets, or reviewing DO code for best practices. Covers Workers integration, wrangler config, and testing with Vitest. Biases towards retrieval from Cloudflare docs over pre-trained knowledge |
| [sandbox-next](../plugins/cloudflare-platform/skills/sandbox-next/SKILL.md) | `cloudflare-platform` | **Tier 2 (MVP)** | Use when building or changing Cloudflare Sandbox apps on @cloudflare/sandbox@next (Sandbox SDK 1.0 preview) - code execution, AI runners, interpreters, CI-like jobs, terminals, files, mounts, tunnels, preview URLs, lifecycle, or errors. Not for the default stable package (use sandbox-stable) or for porting stable to @next (use sandbox-migrate-to-next) |
| [sandbox-stable](../plugins/cloudflare-platform/skills/sandbox-stable/SKILL.md) | `cloudflare-platform` | **Tier 2 (MVP)** | Use when building or changing Cloudflare Sandbox apps on the current stable @cloudflare/sandbox package (default npm tag) - commands, sessions, files, ports, tunnels, terminals, bridge, production, or deprecated-API cleanup while staying on stable. Not for @cloudflare/sandbox@next (use sandbox-next) or for porting to 1.0 (use sandbox-migrate-to-next) |
| [turnstile-spin](../plugins/cloudflare-platform/skills/turnstile-spin/SKILL.md) | `cloudflare-platform` | **Tier 2 (MVP)** | Use when configuring Cloudflare Turnstile bot detection widgets and verification |
| [workers-best-practices](../plugins/cloudflare-platform/skills/workers-best-practices/SKILL.md) | `cloudflare-platform` | **Tier 2 (MVP)** | Use when reviewing or writing production Cloudflare Workers code |
| [wrangler](../plugins/cloudflare-platform/skills/wrangler/SKILL.md) | `cloudflare-platform` | **Tier 1 (Quick)** | Use when managing, configuring, and deploying Cloudflare resources via Wrangler CLI |

### Conductor

| Skill | Plugin | Tier | Trigger Keywords / Activation |
| :--- | :--- | :--- | :--- |
| [context-driven-development](../plugins/conductor/skills/context-driven-development/SKILL.md) | `conductor` | **Tier 2 (MVP)** | >- |
| [track-management](../plugins/conductor/skills/track-management/SKILL.md) | `conductor` | **Tier 2 (MVP)** | Use when working with track management |
| [workflow-patterns](../plugins/conductor/skills/workflow-patterns/SKILL.md) | `conductor` | **Tier 2 (MVP)** | Use when working with workflow patterns |

### Context Management

| Skill | Plugin | Tier | Trigger Keywords / Activation |
| :--- | :--- | :--- | :--- |
| [continuation-protocol](../plugins/context-management/skills/continuation-protocol/SKILL.md) | `context-management` | **Tier 2 (MVP)** | Use whenever executing multi-step tasks, before handoffs, or when approaching token exhaustion and rate limits |

### Data Engineering & Pipelines

| Skill | Plugin | Tier | Trigger Keywords / Activation |
| :--- | :--- | :--- | :--- |
| [airflow-dag-patterns](../plugins/data-engineering/skills/airflow-dag-patterns/SKILL.md) | `data-engineering` | **Tier 2 (MVP)** | Use when creating data pipelines, orchestrating workflows, or scheduling batch jobs |
| [data-quality-frameworks](../plugins/data-engineering/skills/data-quality-frameworks/SKILL.md) | `data-engineering` | **Tier 2 (MVP)** | Use when building data quality pipelines, implementing validation rules, or establishing data contracts |
| [dbt-transformation-patterns](../plugins/data-engineering/skills/dbt-transformation-patterns/SKILL.md) | `data-engineering` | **Tier 1 (Quick)** | Use when building data transformations, creating data models, or implementing analytics engineering best practices |
| [spark-optimization](../plugins/data-engineering/skills/spark-optimization/SKILL.md) | `data-engineering` | **Tier 2 (MVP)** | Use when improving Spark performance, debugging slow jobs, or scaling data processing pipelines |

### Database Design

| Skill | Plugin | Tier | Trigger Keywords / Activation |
| :--- | :--- | :--- | :--- |
| [postgresql-table-design](../plugins/database-design/skills/postgresql-table-design/SKILL.md) | `database-design` | **Tier 2 (MVP)** | Use when working with postgresql table design |

### Deep Research & Intelligence

| Skill | Plugin | Tier | Trigger Keywords / Activation |
| :--- | :--- | :--- | :--- |
| [last30days](../plugins/deep-research/skills/last30days/SKILL.md) | `deep-research` | **Tier 2 (MVP)** | Use when researching recent community discussions, reactions, and news over the last 30 days |
| [research](../plugins/deep-research/skills/research/SKILL.md) | `deep-research` | **Tier 2 (MVP)** | Use when the task is "find out" rather than "what do you already know"  -  current events, tooling or version facts, prior-art surveys, API or spec behavior, or any claim that moves faster than the training cutoff. Not for questions answerable from the codebase in front of you |
| [wayfinder](../plugins/deep-research/skills/wayfinder/SKILL.md) | `deep-research` | **Tier 3 (Architecture)** | Use when breaking down large architectural multi-session initiatives into roadmap maps |

### Developer Essentials & Git Workflows

| Skill | Plugin | Tier | Trigger Keywords / Activation |
| :--- | :--- | :--- | :--- |
| [auth-implementation-patterns](../plugins/developer-essentials/skills/auth-implementation-patterns/SKILL.md) | `developer-essentials` | **Tier 2 (MVP)** | Use when implementing auth systems, securing APIs, or debugging security issues |
| [bazel-build-optimization](../plugins/developer-essentials/skills/bazel-build-optimization/SKILL.md) | `developer-essentials` | **Tier 2 (MVP)** | Use when configuring Bazel, implementing remote execution, or optimizing build performance for enterprise codebases |
| [code-review-excellence](../plugins/developer-essentials/skills/code-review-excellence/SKILL.md) | `developer-essentials` | **Tier 2 (MVP)** | Use when reviewing pull requests, establishing review standards, or mentoring developers |
| [debugging-strategies](../plugins/developer-essentials/skills/debugging-strategies/SKILL.md) | `developer-essentials` | **Tier 2 (MVP)** | Use when investigating bugs, performance issues, or unexpected behavior |
| [e2e-testing-patterns](../plugins/developer-essentials/skills/e2e-testing-patterns/SKILL.md) | `developer-essentials` | **Tier 2 (MVP)** | Use when implementing E2E tests, debugging flaky tests, or establishing testing standards |
| [error-handling-patterns](../plugins/developer-essentials/skills/error-handling-patterns/SKILL.md) | `developer-essentials` | **Tier 2 (MVP)** | Use when implementing error handling, designing APIs, or improving application reliability |
| [git-advanced-workflows](../plugins/developer-essentials/skills/git-advanced-workflows/SKILL.md) | `developer-essentials` | **Tier 2 (MVP)** | Use when managing complex Git histories, collaborating on feature branches, or troubleshooting repository issues |
| [monorepo-management](../plugins/developer-essentials/skills/monorepo-management/SKILL.md) | `developer-essentials` | **Tier 2 (MVP)** | Use when setting up monorepos, optimizing builds, or managing shared dependencies |
| [nx-workspace-patterns](../plugins/developer-essentials/skills/nx-workspace-patterns/SKILL.md) | `developer-essentials` | **Tier 2 (MVP)** | Use when setting up Nx, configuring project boundaries, optimizing build caching, or implementing affected commands |
| [sql-optimization-patterns](../plugins/developer-essentials/skills/sql-optimization-patterns/SKILL.md) | `developer-essentials` | **Tier 2 (MVP)** | Use when debugging slow queries, designing database schemas, or optimizing application performance |
| [turborepo-caching](../plugins/developer-essentials/skills/turborepo-caching/SKILL.md) | `developer-essentials` | **Tier 2 (MVP)** | Use when setting up Turborepo, optimizing build pipelines, or implementing distributed caching |

### Dgx Spark Ops

| Skill | Plugin | Tier | Trigger Keywords / Activation |
| :--- | :--- | :--- | :--- |
| [spark-environment-setup](../plugins/dgx-spark-ops/skills/spark-environment-setup/SKILL.md) | `dgx-spark-ops` | **Tier 2 (MVP)** | Use when installing PyTorch/Unsloth/TRL/vLLM on DGX Spark, hitting libcudart or wheel-ABI errors on aarch64, or choosing between NGC containers and bare pip installs |
| [spark-memory-thermal-ops](../plugins/dgx-spark-ops/skills/spark-memory-thermal-ops/SKILL.md) | `dgx-spark-ops` | **Tier 2 (MVP)** | Use when planning memory headroom for a training run on GB10, when a job OOMs on unified memory, or when monitoring temperature and power during multi-hour training |
| [spark-training-gotchas](../plugins/dgx-spark-ops/skills/spark-training-gotchas/SKILL.md) | `dgx-spark-ops` | **Tier 2 (MVP)** | Use when a training run on DGX Spark fails to start, OOMs below the 128GB limit, slows down mid-run, or before any multi-hour training job on GB10 |

### Documentation Generation

| Skill | Plugin | Tier | Trigger Keywords / Activation |
| :--- | :--- | :--- | :--- |
| [architecture-decision-records](../plugins/documentation-generation/skills/architecture-decision-records/SKILL.md) | `documentation-generation` | **Tier 3 (Architecture)** | Use when documenting significant technical decisions, reviewing past architectural choices, or establishing decision processes |
| [changelog-automation](../plugins/documentation-generation/skills/changelog-automation/SKILL.md) | `documentation-generation` | **Tier 1 (Quick)** | Use when setting up release workflows, generating release notes, or standardizing commit conventions |
| [openapi-spec-generation](../plugins/documentation-generation/skills/openapi-spec-generation/SKILL.md) | `documentation-generation` | **Tier 2 (MVP)** | Use when creating API documentation, generating SDKs, or ensuring API contract compliance |

### Documentation Standards

| Skill | Plugin | Tier | Trigger Keywords / Activation |
| :--- | :--- | :--- | :--- |
| [grounded-vault](../plugins/documentation-standards/skills/grounded-vault/SKILL.md) | `documentation-standards` | **Tier 2 (MVP)** | Use when maintaining a durable Markdown knowledge store that agents compile from sources, when every number or quote in a wiki page must trace back to an immutable source, or when compiled pages need cheap drift detection against the code they describe. Teaches the raw/wiki/archive layout, per-claim provenance links, and git fingerprints for zero-token staleness checks |
| [hads](../plugins/documentation-standards/skills/hads/SKILL.md) | `documentation-standards` | **Tier 1 (Quick)** | Use when writing technical documentation that needs to be readable by both humans and AI models, converting existing docs to HADS format, validating a HADS document, or optimizing documentation for token-efficient AI consumption |

### Dotnet Contribution

| Skill | Plugin | Tier | Trigger Keywords / Activation |
| :--- | :--- | :--- | :--- |
| [dotnet-backend-patterns](../plugins/dotnet-contribution/skills/dotnet-backend-patterns/SKILL.md) | `dotnet-contribution` | **Tier 3 (Architecture)** | Use when developing .NET backends, reviewing C# code, or designing API architectures |

### File Conversion

| Skill | Plugin | Tier | Trigger Keywords / Activation |
| :--- | :--- | :--- | :--- |
| [file-conversion](../plugins/file-conversion/skills/file-conversion/SKILL.md) | `file-conversion` | **Tier 1 (Quick)** | Use when the user needs a file converted to a different format |

### Framework Migration

| Skill | Plugin | Tier | Trigger Keywords / Activation |
| :--- | :--- | :--- | :--- |
| [angular-migration](../plugins/framework-migration/skills/angular-migration/SKILL.md) | `framework-migration` | **Tier 2 (MVP)** | Use when upgrading AngularJS applications, planning framework migrations, or modernizing legacy Angular code |
| [database-migration](../plugins/framework-migration/skills/database-migration/SKILL.md) | `framework-migration` | **Tier 1 (Quick)** | Use when migrating databases, changing schemas, performing data transformations, or implementing zero-downtime deployment strategies |
| [dependency-upgrade](../plugins/framework-migration/skills/dependency-upgrade/SKILL.md) | `framework-migration` | **Tier 2 (MVP)** | Use when upgrading framework versions, updating major dependencies, or managing breaking changes in libraries |
| [react-modernization](../plugins/framework-migration/skills/react-modernization/SKILL.md) | `framework-migration` | **Tier 2 (MVP)** | Use when modernizing React codebases, migrating to React Hooks, or upgrading to latest React versions |

### Frontend Mobile Development

| Skill | Plugin | Tier | Trigger Keywords / Activation |
| :--- | :--- | :--- | :--- |
| [nextjs-app-router-patterns](../plugins/frontend-mobile-development/skills/nextjs-app-router-patterns/SKILL.md) | `frontend-mobile-development` | **Tier 2 (MVP)** | Use when building Next.js applications, implementing SSR/SSG, or optimizing React Server Components |
| [react-native-architecture](../plugins/frontend-mobile-development/skills/react-native-architecture/SKILL.md) | `frontend-mobile-development` | **Tier 3 (Architecture)** | Use when developing mobile apps, implementing native integrations, or architecting React Native projects |
| [react-state-management](../plugins/frontend-mobile-development/skills/react-state-management/SKILL.md) | `frontend-mobile-development` | **Tier 2 (MVP)** | Use when setting up global state, managing server state, or choosing between state management solutions |
| [tailwind-design-system](../plugins/frontend-mobile-development/skills/tailwind-design-system/SKILL.md) | `frontend-mobile-development` | **Tier 2 (MVP)** | Use when creating component libraries, implementing design systems, or standardizing UI patterns |

### Game Development

| Skill | Plugin | Tier | Trigger Keywords / Activation |
| :--- | :--- | :--- | :--- |
| [godot-gdscript-patterns](../plugins/game-development/skills/godot-gdscript-patterns/SKILL.md) | `game-development` | **Tier 2 (MVP)** | Use when building Godot games, implementing game systems, or learning GDScript best practices |
| [unity-ecs-patterns](../plugins/game-development/skills/unity-ecs-patterns/SKILL.md) | `game-development` | **Tier 2 (MVP)** | Use when building data-oriented games, optimizing performance, or working with large entity counts |

### Hermes Tweet

| Skill | Plugin | Tier | Trigger Keywords / Activation |
| :--- | :--- | :--- | :--- |
| [hermes-tweet](../plugins/hermes-tweet/skills/hermes-tweet/SKILL.md) | `hermes-tweet` | **Tier 4 (Audit)** | Use when working with hermes tweet |

### Hr Legal Compliance

| Skill | Plugin | Tier | Trigger Keywords / Activation |
| :--- | :--- | :--- | :--- |
| [employment-contract-templates](../plugins/hr-legal-compliance/skills/employment-contract-templates/SKILL.md) | `hr-legal-compliance` | **Tier 2 (MVP)** | Use when drafting employment agreements, creating HR policies, or standardizing employment documentation |
| [gdpr-data-handling](../plugins/hr-legal-compliance/skills/gdpr-data-handling/SKILL.md) | `hr-legal-compliance` | **Tier 2 (MVP)** | Use when building systems that process EU personal data, implementing privacy controls, or conducting GDPR compliance reviews |

### Incident Response

| Skill | Plugin | Tier | Trigger Keywords / Activation |
| :--- | :--- | :--- | :--- |
| [incident-runbook-templates](../plugins/incident-response/skills/incident-runbook-templates/SKILL.md) | `incident-response` | **Tier 4 (Audit)** | Use when working with incident runbook templates |
| [on-call-handoff-patterns](../plugins/incident-response/skills/on-call-handoff-patterns/SKILL.md) | `incident-response` | **Tier 4 (Audit)** | Use when working with on call handoff patterns |
| [postmortem-writing](../plugins/incident-response/skills/postmortem-writing/SKILL.md) | `incident-response` | **Tier 4 (Audit)** | Use when conducting incident reviews, writing postmortem documents, or improving incident response processes |

### Javascript Typescript

| Skill | Plugin | Tier | Trigger Keywords / Activation |
| :--- | :--- | :--- | :--- |
| [javascript-testing-patterns](../plugins/javascript-typescript/skills/javascript-testing-patterns/SKILL.md) | `javascript-typescript` | **Tier 2 (MVP)** | Use when writing JavaScript/TypeScript tests, setting up test infrastructure, or implementing TDD/BDD workflows |
| [modern-javascript-patterns](../plugins/javascript-typescript/skills/modern-javascript-patterns/SKILL.md) | `javascript-typescript` | **Tier 2 (MVP)** | Use when refactoring legacy code, implementing modern patterns, or optimizing JavaScript applications |
| [nodejs-backend-patterns](../plugins/javascript-typescript/skills/nodejs-backend-patterns/SKILL.md) | `javascript-typescript` | **Tier 3 (Architecture)** | Use when creating Node.js servers, REST APIs, GraphQL backends, or microservices architectures |
| [typescript-advanced-types](../plugins/javascript-typescript/skills/typescript-advanced-types/SKILL.md) | `javascript-typescript` | **Tier 2 (MVP)** | Use when implementing complex type logic, creating reusable type utilities, or ensuring compile-time type safety in TypeScript projects |

### Kubernetes Operations

| Skill | Plugin | Tier | Trigger Keywords / Activation |
| :--- | :--- | :--- | :--- |
| [gitops-workflow](../plugins/kubernetes-operations/skills/gitops-workflow/SKILL.md) | `kubernetes-operations` | **Tier 2 (MVP)** | Use when implementing GitOps practices, automating Kubernetes deployments, or setting up declarative infrastructure management |
| [helm-chart-scaffolding](../plugins/kubernetes-operations/skills/helm-chart-scaffolding/SKILL.md) | `kubernetes-operations` | **Tier 2 (MVP)** | Use when creating Helm charts, packaging Kubernetes applications, or implementing templated deployments |
| [k8s-manifest-generator](../plugins/kubernetes-operations/skills/k8s-manifest-generator/SKILL.md) | `kubernetes-operations` | **Tier 2 (MVP)** | Use when generating Kubernetes YAML manifests, creating K8s resources, or implementing production-grade Kubernetes configurations |
| [k8s-security-policies](../plugins/kubernetes-operations/skills/k8s-security-policies/SKILL.md) | `kubernetes-operations` | **Tier 1 (Quick)** | Use when securing Kubernetes clusters, implementing network isolation, or enforcing pod security standards |

### LLM Application Engineering

| Skill | Plugin | Tier | Trigger Keywords / Activation |
| :--- | :--- | :--- | :--- |
| [embedding-strategies](../plugins/llm-application-dev/skills/embedding-strategies/SKILL.md) | `llm-application-dev` | **Tier 2 (MVP)** | Use when choosing embedding models, implementing chunking strategies, or optimizing embedding quality for specific domains |
| [hybrid-search-implementation](../plugins/llm-application-dev/skills/hybrid-search-implementation/SKILL.md) | `llm-application-dev` | **Tier 2 (MVP)** | Use when implementing RAG systems, building search engines, or when neither approach alone provides sufficient recall |
| [langchain-architecture](../plugins/llm-application-dev/skills/langchain-architecture/SKILL.md) | `llm-application-dev` | **Tier 3 (Architecture)** | Use when building LangChain applications, implementing AI agents, or creating complex LLM workflows |
| [llm-evaluation](../plugins/llm-application-dev/skills/llm-evaluation/SKILL.md) | `llm-application-dev` | **Tier 2 (MVP)** | Use when testing LLM performance, measuring AI application quality, or establishing evaluation frameworks |
| [prompt-engineering-patterns](../plugins/llm-application-dev/skills/prompt-engineering-patterns/SKILL.md) | `llm-application-dev` | **Tier 2 (MVP)** | Use when working with prompt engineering patterns |
| [rag-implementation](../plugins/llm-application-dev/skills/rag-implementation/SKILL.md) | `llm-application-dev` | **Tier 2 (MVP)** | Use when implementing knowledge-grounded AI, building document Q&A systems, or integrating LLMs with external knowledge bases |
| [similarity-search-patterns](../plugins/llm-application-dev/skills/similarity-search-patterns/SKILL.md) | `llm-application-dev` | **Tier 2 (MVP)** | Use when building semantic search, implementing nearest neighbor queries, or optimizing retrieval performance |
| [vector-index-tuning](../plugins/llm-application-dev/skills/vector-index-tuning/SKILL.md) | `llm-application-dev` | **Tier 4 (Audit)** | Use when tuning HNSW parameters, selecting quantization strategies, or scaling vector search infrastructure |

### Machine Learning Ops

| Skill | Plugin | Tier | Trigger Keywords / Activation |
| :--- | :--- | :--- | :--- |
| [ml-pipeline-workflow](../plugins/machine-learning-ops/skills/ml-pipeline-workflow/SKILL.md) | `machine-learning-ops` | **Tier 2 (MVP)** | Use when creating ML pipelines, implementing MLOps practices, or automating model training and deployment workflows |
| [recsys-pipeline-architect](../plugins/machine-learning-ops/skills/recsys-pipeline-architect/SKILL.md) | `machine-learning-ops` | **Tier 2 (MVP)** | Use when building any system that picks "the top K items for a (user, context)"  -  content feeds, search ranking, RAG rerankers, task prioritizers, notification triage, ad selection |

### Model Fine-Tuning & Quantization

| Skill | Plugin | Tier | Trigger Keywords / Activation |
| :--- | :--- | :--- | :--- |
| [checkpoint-promotion](../plugins/llm-finetuning/skills/checkpoint-promotion/SKILL.md) | `llm-finetuning` | **Tier 4 (Audit)** | Use when working with checkpoint promotion |
| [dataset-curation](../plugins/llm-finetuning/skills/dataset-curation/SKILL.md) | `llm-finetuning` | **Tier 1 (Quick)** | Use when converting raw data into training format, applying chat templates, configuring sequence packing, generating synthetic training data, or writing a dataset card before a run |
| [eval-harness-first](../plugins/llm-finetuning/skills/eval-harness-first/SKILL.md) | `llm-finetuning` | **Tier 4 (Audit)** | Use when starting a fine-tuning effort, when converting traces into an eval set, or when calibrating a judge against human labels |
| [finetuning-method-selection](../plugins/llm-finetuning/skills/finetuning-method-selection/SKILL.md) | `llm-finetuning` | **Tier 4 (Audit)** | Use when starting any fine-tuning effort, when unsure whether RAG or prompting would suffice, or when choosing between preference-optimization and reinforcement methods |
| [grpo-rlvr-training](../plugins/llm-finetuning/skills/grpo-rlvr-training/SKILL.md) | `llm-finetuning` | **Tier 4 (Audit)** | Use when task success is algorithmically checkable (math, code, tool calls, structured output), when designing GRPO reward functions, or when a GRPO run diverges or reward-hacks |
| [lora-qlora-recipes](../plugins/llm-finetuning/skills/lora-qlora-recipes/SKILL.md) | `llm-finetuning` | **Tier 4 (Audit)** | Use when writing or reviewing a LoRA/QLoRA training configuration, choosing rank/alpha/target modules, or deciding between LoRA, QLoRA, and full fine-tuning |
| [preference-optimization](../plugins/llm-finetuning/skills/preference-optimization/SKILL.md) | `llm-finetuning` | **Tier 4 (Audit)** | Use when preference pairs or thumbs-up/down feedback exist, when choosing between preference-optimization methods, or when a DPO run needs hyperparameters or debugging |
| [quantized-export](../plugins/llm-finetuning/skills/quantized-export/SKILL.md) | `llm-finetuning` | **Tier 1 (Quick)** | Use when working with quantized export |
| [trace-to-training-data](../plugins/llm-finetuning/skills/trace-to-training-data/SKILL.md) | `llm-finetuning` | **Tier 4 (Audit)** | Use when graded traces or failure examples exist and need to become training data, when applying rejection sampling to model outputs, or when building DPO pairs from passing and failing runs |
| [vision-sft](../plugins/llm-finetuning/skills/vision-sft/SKILL.md) | `llm-finetuning` | **Tier 4 (Audit)** | Use when adapting a VLM to a visual domain or task, configuring frozen-vision-tower LoRA, or debugging a VLM fine-tune that trains without learning |

### Observability Monitoring

| Skill | Plugin | Tier | Trigger Keywords / Activation |
| :--- | :--- | :--- | :--- |
| [distributed-tracing](../plugins/observability-monitoring/skills/distributed-tracing/SKILL.md) | `observability-monitoring` | **Tier 3 (Architecture)** | Use when debugging microservices, analyzing request flows, or implementing observability for distributed systems |
| [grafana-dashboards](../plugins/observability-monitoring/skills/grafana-dashboards/SKILL.md) | `observability-monitoring` | **Tier 2 (MVP)** | Use when building monitoring dashboards, visualizing metrics, or creating operational observability interfaces |
| [prometheus-configuration](../plugins/observability-monitoring/skills/prometheus-configuration/SKILL.md) | `observability-monitoring` | **Tier 2 (MVP)** | Use when implementing metrics collection, setting up monitoring infrastructure, or configuring alerting systems |
| [slo-implementation](../plugins/observability-monitoring/skills/slo-implementation/SKILL.md) | `observability-monitoring` | **Tier 2 (MVP)** | Use when establishing reliability targets, implementing SRE practices, or measuring service performance |

### Operational Discipline & Governance

| Skill | Plugin | Tier | Trigger Keywords / Activation |
| :--- | :--- | :--- | :--- |
| [investigate-first](../plugins/operational-discipline/skills/investigate-first/SKILL.md) | `operational-discipline` | **Tier 2 (MVP)** | Use when diagnosing ambiguous failures, regressions, or unknown bugs before touching code |
| [lean-build](../plugins/operational-discipline/skills/lean-build/SKILL.md) | `operational-discipline` | **Tier 2 (MVP)** | Use when implementing new features with high risk of overengineering |
| [operating-discipline](../plugins/operational-discipline/skills/operating-discipline/SKILL.md) | `operational-discipline` | **Tier 2 (MVP)** | Use when starting open-ended or measurable work, deciding whether to spawn a new session or ask a question, deciding whether to escalate, or giving a recommendation |
| [request-complexity-classifier](../plugins/operational-discipline/skills/request-complexity-classifier/SKILL.md) | `operational-discipline` | **Tier 1 (Quick)** | Use when classifying user prompts into difficulty tiers 1 through 4 |
| [using-superpowers](../plugins/operational-discipline/skills/using-superpowers/SKILL.md) | `operational-discipline` | **Tier 2 (MVP)** | Use when explicitly activating the Superpowers workflow and process skills |
| [verification-before-completion](../plugins/operational-discipline/skills/verification-before-completion/SKILL.md) | `operational-discipline` | **Tier 2 (MVP)** | Use when verifying tasks with deterministic tests and exit code 0 before declaring completion |
| [verify-and-stop](../plugins/operational-discipline/skills/verify-and-stop/SKILL.md) | `operational-discipline` | **Tier 1 (Quick)** | Use when proving existing work satisfies requirements without introducing scope creep |
| [verify-before-asserting](../plugins/operational-discipline/skills/verify-before-asserting/SKILL.md) | `operational-discipline` | **Tier 3 (Architecture)** | Use when verifying tech stack claims, tool availability, or machine state before asserting |
| [vision-before-committing](../plugins/operational-discipline/skills/vision-before-committing/SKILL.md) | `operational-discipline` | **Tier 2 (MVP)** | Use when considering "should I start", weighing a new direction, or deciding whether to take something on. Not for choosing among things already in motion, planning execution of a decided project, or fixing something that already exists |

### Payment Processing

| Skill | Plugin | Tier | Trigger Keywords / Activation |
| :--- | :--- | :--- | :--- |
| [billing-automation](../plugins/payment-processing/skills/billing-automation/SKILL.md) | `payment-processing` | **Tier 2 (MVP)** | Use when implementing subscription billing, automating invoicing, or managing recurring payment systems |
| [paypal-integration](../plugins/payment-processing/skills/paypal-integration/SKILL.md) | `payment-processing` | **Tier 2 (MVP)** | Use when implementing PayPal payments, processing online transactions, or building e-commerce checkout flows |
| [pci-compliance](../plugins/payment-processing/skills/pci-compliance/SKILL.md) | `payment-processing` | **Tier 2 (MVP)** | Use when securing payment processing, achieving PCI compliance, or implementing payment card security measures |
| [stripe-integration](../plugins/payment-processing/skills/stripe-integration/SKILL.md) | `payment-processing` | **Tier 2 (MVP)** | Use when integrating Stripe payments, building subscription systems, or implementing secure checkout flows |

### Planning & Specification Design

| Skill | Plugin | Tier | Trigger Keywords / Activation |
| :--- | :--- | :--- | :--- |
| [decompose-the-plan](../plugins/planning-spec/skills/decompose-the-plan/SKILL.md) | `planning-spec` | **Tier 2 (MVP)** | Use when breaking complex plans into independent subtasks |
| [grill-me](../plugins/planning-spec/skills/grill-me/SKILL.md) | `planning-spec` | **Tier 3 (Architecture)** | Use when interrogating requirements, trade-offs, and architecture through adversarial interview |
| [spec-design](../plugins/planning-spec/skills/spec-design/SKILL.md) | `planning-spec` | **Tier 2 (MVP)** | Use when authoring concise engineering implementation specifications from user requirements |
| [to-questionnaire](../plugins/planning-spec/skills/to-questionnaire/SKILL.md) | `planning-spec` | **Tier 2 (MVP)** | Use when generating structured questionnaires to clarify ambiguous requirements |
| [to-spec](../plugins/planning-spec/skills/to-spec/SKILL.md) | `planning-spec` | **Tier 2 (MVP)** | Use when converting conversations and loose requirements into structured specifications |
| [to-tickets](../plugins/planning-spec/skills/to-tickets/SKILL.md) | `planning-spec` | **Tier 2 (MVP)** | Use when decomposing specifications or plans into atomic GitHub issues |
| [visual-spec](../plugins/planning-spec/skills/visual-spec/SKILL.md) | `planning-spec` | **Tier 2 (MVP)** | Use when the user says "htmlvspec", wants a visual/illustrated HTML implementation plan, a browser-openable spec with per-section diagrams, or any HTML plan where images are required. argument-hint: "[user prompt] |
| [writing-plans](../plugins/planning-spec/skills/writing-plans/SKILL.md) | `planning-spec` | **Tier 2 (MVP)** | Use when you have a spec or requirements for a multi-step task, before touching code |

### Plugin Eval

| Skill | Plugin | Tier | Trigger Keywords / Activation |
| :--- | :--- | :--- | :--- |
| [evaluation-methodology](../plugins/plugin-eval/skills/evaluation-methodology/SKILL.md) | `plugin-eval` | **Tier 2 (MVP)** | Use when working with evaluation methodology |

### Pptx Deck Creation

| Skill | Plugin | Tier | Trigger Keywords / Activation |
| :--- | :--- | :--- | :--- |
| [pptx-deck-context](../plugins/pptx-deck-creation/skills/pptx-deck-context/SKILL.md) | `pptx-deck-creation` | **Tier 2 (MVP)** | Use when preparing the narrative, sources, and design context for a new editable PPTX deck |
| [pptx-quality-gates](../plugins/pptx-deck-creation/skills/pptx-quality-gates/SKILL.md) | `pptx-deck-creation` | **Tier 2 (MVP)** | Use when validating or repairing an editable PPTX deck for geometry, accessibility, native editability, source lineage, and OOXML package integrity |
| [pptx-reference-deck-analysis](../plugins/pptx-deck-creation/skills/pptx-reference-deck-analysis/SKILL.md) | `pptx-deck-creation` | **Tier 1 (Quick)** | Use when analyzing a reference PPTX for read-only structure, theme, typography, layout rhythm, diagnostics, derived template catalogs, or safe OOXML package inspection |
| [pptx-slide-specification](../plugins/pptx-deck-creation/skills/pptx-slide-specification/SKILL.md) | `pptx-deck-creation` | **Tier 2 (MVP)** | Use when authoring or repairing a coordinate-explicit JSON specification for an editable PPTX deck |
| [pptx-visual-assets](../plugins/pptx-deck-creation/skills/pptx-visual-assets/SKILL.md) | `pptx-deck-creation` | **Tier 2 (MVP)** | Use when selecting and placing approved supporting icons, images, SVGs, diagrams, or infographics in an editable PPTX deck |

### Protect Mcp

| Skill | Plugin | Tier | Trigger Keywords / Activation |
| :--- | :--- | :--- | :--- |
| [protect-mcp-setup](../plugins/protect-mcp/skills/protect-mcp-setup/SKILL.md) | `protect-mcp` | **Tier 4 (Audit)** | Use when setting up projects that need cryptographic audit trails, policy-gated tool execution, or compliance-ready evidence of agent actions |

### Python Development

| Skill | Plugin | Tier | Trigger Keywords / Activation |
| :--- | :--- | :--- | :--- |
| [async-python-patterns](../plugins/python-development/skills/async-python-patterns/SKILL.md) | `python-development` | **Tier 2 (MVP)** | Use when building async APIs, concurrent systems, or I/O-bound applications requiring non-blocking operations |
| [python-anti-patterns](../plugins/python-development/skills/python-anti-patterns/SKILL.md) | `python-development` | **Tier 2 (MVP)** | Use when working with python anti patterns |
| [python-background-jobs](../plugins/python-development/skills/python-background-jobs/SKILL.md) | `python-development` | **Tier 3 (Architecture)** | Use when implementing async task processing, job queues, long-running operations, or decoupling work from request/response cycles |
| [python-code-style](../plugins/python-development/skills/python-code-style/SKILL.md) | `python-development` | **Tier 1 (Quick)** | Use when writing new code, reviewing style, configuring linters, writing docstrings, or establishing project standards |
| [python-configuration](../plugins/python-development/skills/python-configuration/SKILL.md) | `python-development` | **Tier 2 (MVP)** | Use when externalizing config, setting up pydantic-settings, managing secrets, or implementing environment-specific behavior |
| [python-design-patterns](../plugins/python-development/skills/python-design-patterns/SKILL.md) | `python-development` | **Tier 2 (MVP)** | Use when working with python design patterns |
| [python-error-handling](../plugins/python-development/skills/python-error-handling/SKILL.md) | `python-development` | **Tier 2 (MVP)** | Use when implementing validation logic, designing exception strategies, handling batch processing failures, or building robust APIs |
| [python-observability](../plugins/python-development/skills/python-observability/SKILL.md) | `python-development` | **Tier 2 (MVP)** | Use when adding logging, implementing metrics collection, setting up tracing, or debugging production systems |
| [python-packaging](../plugins/python-development/skills/python-packaging/SKILL.md) | `python-development` | **Tier 2 (MVP)** | Use when packaging Python libraries, creating CLI tools, or distributing Python code |
| [python-performance-optimization](../plugins/python-development/skills/python-performance-optimization/SKILL.md) | `python-development` | **Tier 2 (MVP)** | Use when debugging slow Python code, optimizing bottlenecks, or improving application performance |
| [python-project-structure](../plugins/python-development/skills/python-project-structure/SKILL.md) | `python-development` | **Tier 3 (Architecture)** | Use when setting up new projects, organizing modules, defining public interfaces with __all__, or planning directory layouts |
| [python-resilience](../plugins/python-development/skills/python-resilience/SKILL.md) | `python-development` | **Tier 2 (MVP)** | Use when adding retry logic, implementing timeouts, building fault-tolerant services, or handling transient failures |
| [python-resource-management](../plugins/python-development/skills/python-resource-management/SKILL.md) | `python-development` | **Tier 2 (MVP)** | Use when managing connections, file handles, implementing cleanup logic, or building streaming responses with accumulated state |
| [python-testing-patterns](../plugins/python-development/skills/python-testing-patterns/SKILL.md) | `python-development` | **Tier 2 (MVP)** | Use when writing Python tests, setting up test suites, or implementing testing best practices |
| [python-type-safety](../plugins/python-development/skills/python-type-safety/SKILL.md) | `python-development` | **Tier 2 (MVP)** | Use when adding type annotations, implementing generic classes, defining structural interfaces, or configuring mypy/pyright |
| [uv-package-manager](../plugins/python-development/skills/uv-package-manager/SKILL.md) | `python-development` | **Tier 2 (MVP)** | Use when setting up Python projects, managing dependencies, or optimizing Python development workflows with uv |

### Quantitative Trading

| Skill | Plugin | Tier | Trigger Keywords / Activation |
| :--- | :--- | :--- | :--- |
| [backtesting-frameworks](../plugins/quantitative-trading/skills/backtesting-frameworks/SKILL.md) | `quantitative-trading` | **Tier 2 (MVP)** | Use when developing trading algorithms, validating strategies, or building backtesting infrastructure |
| [risk-metrics-calculation](../plugins/quantitative-trading/skills/risk-metrics-calculation/SKILL.md) | `quantitative-trading` | **Tier 2 (MVP)** | Use when measuring portfolio risk, implementing risk limits, or building risk monitoring systems |

### Reverse Engineering

| Skill | Plugin | Tier | Trigger Keywords / Activation |
| :--- | :--- | :--- | :--- |
| [anti-reversing-techniques](../plugins/reverse-engineering/skills/anti-reversing-techniques/SKILL.md) | `reverse-engineering` | **Tier 4 (Audit)** | Use when working with anti reversing techniques |
| [binary-analysis-patterns](../plugins/reverse-engineering/skills/binary-analysis-patterns/SKILL.md) | `reverse-engineering` | **Tier 2 (MVP)** | Use when analyzing executables, understanding compiled code, or performing static analysis on binaries |
| [memory-forensics](../plugins/reverse-engineering/skills/memory-forensics/SKILL.md) | `reverse-engineering` | **Tier 4 (Audit)** | Use when analyzing memory dumps, investigating incidents, or performing malware analysis from RAM captures |
| [protocol-reverse-engineering](../plugins/reverse-engineering/skills/protocol-reverse-engineering/SKILL.md) | `reverse-engineering` | **Tier 2 (MVP)** | Use when analyzing network traffic, understanding proprietary protocols, or debugging network communication |

### Review Agent Governance

| Skill | Plugin | Tier | Trigger Keywords / Activation |
| :--- | :--- | :--- | :--- |
| [review-agent-setup](../plugins/review-agent-governance/skills/review-agent-setup/SKILL.md) | `review-agent-governance` | **Tier 4 (Audit)** | Use when setting up a project where an agent may post PR reviews, comments, merges, or edit CI configuration, and you want a cryptographically auditable approval trail with Cedar-enforced gates |

### Security & Vulnerability Analysis

| Skill | Plugin | Tier | Trigger Keywords / Activation |
| :--- | :--- | :--- | :--- |
| [attack-tree-construction](../plugins/security-scanning/skills/attack-tree-construction/SKILL.md) | `security-scanning` | **Tier 2 (MVP)** | Use when mapping attack scenarios, identifying defense gaps, or communicating security risks to stakeholders |
| [sast-configuration](../plugins/security-scanning/skills/sast-configuration/SKILL.md) | `security-scanning` | **Tier 4 (Audit)** | Use when setting up security scanning, implementing DevSecOps practices, or automating code vulnerability detection |
| [security-requirement-extraction](../plugins/security-scanning/skills/security-requirement-extraction/SKILL.md) | `security-scanning` | **Tier 2 (MVP)** | Use when translating threats into actionable requirements, creating security user stories, or building security test cases |
| [stride-analysis-patterns](../plugins/security-scanning/skills/stride-analysis-patterns/SKILL.md) | `security-scanning` | **Tier 2 (MVP)** | Use when analyzing system security, conducting threat modeling sessions, or creating security documentation |
| [threat-mitigation-mapping](../plugins/security-scanning/skills/threat-mitigation-mapping/SKILL.md) | `security-scanning` | **Tier 4 (Audit)** | Use when prioritizing security investments, creating remediation plans, or validating control effectiveness |

### Shell Scripting

| Skill | Plugin | Tier | Trigger Keywords / Activation |
| :--- | :--- | :--- | :--- |
| [bash-defensive-patterns](../plugins/shell-scripting/skills/bash-defensive-patterns/SKILL.md) | `shell-scripting` | **Tier 2 (MVP)** | Use when writing robust shell scripts, CI/CD pipelines, or system utilities requiring fault tolerance and safety |
| [bats-testing-patterns](../plugins/shell-scripting/skills/bats-testing-patterns/SKILL.md) | `shell-scripting` | **Tier 2 (MVP)** | Use when writing tests for shell scripts, CI/CD pipelines, or requiring test-driven development of shell utilities |
| [shellcheck-configuration](../plugins/shell-scripting/skills/shellcheck-configuration/SKILL.md) | `shell-scripting` | **Tier 1 (Quick)** | Use when setting up linting infrastructure, fixing code issues, or ensuring script portability |

### Ship Mate

| Skill | Plugin | Tier | Trigger Keywords / Activation |
| :--- | :--- | :--- | :--- |
| [scan](../plugins/ship-mate/skills/scan/SKILL.md) | `ship-mate` | **Tier 2 (MVP)** | Use when bootstrapping a new agent-driven repo, refreshing project documentation after architectural changes, or running a delta scan to detect drift. Runs a full scan on first use and a smart delta scan on subsequent runs. Uses understand-anything + context-mode when available, falls back to native tools otherwise. Only updates AGENTS.md on detected architectural changes with human confirmation |

### Signed Audit Trails

| Skill | Plugin | Tier | Trigger Keywords / Activation |
| :--- | :--- | :--- | :--- |
| [signed-audit-trails-recipe](../plugins/signed-audit-trails/skills/signed-audit-trails-recipe/SKILL.md) | `signed-audit-trails` | **Tier 4 (Audit)** | Use when explaining, evaluating, or demonstrating the pattern before committing to the protect-mcp runtime hooks. Covers Cedar policy, Ed25519 receipts, offline verification, tamper detection, CI/CD integration, and SLSA composition |

### Skill Forge Essentials

| Skill | Plugin | Tier | Trigger Keywords / Activation |
| :--- | :--- | :--- | :--- |
| [ai-debt-detector](../plugins/skill-forge-essentials/skills/ai-debt-detector/SKILL.md) | `skill-forge-essentials` | **Tier 2 (MVP)** | >- |
| [session-guard](../plugins/skill-forge-essentials/skills/session-guard/SKILL.md) | `skill-forge-essentials` | **Tier 2 (MVP)** | >- |
| [visual-edit-precision](../plugins/skill-forge-essentials/skills/visual-edit-precision/SKILL.md) | `skill-forge-essentials` | **Tier 2 (MVP)** | >- |

### Social Publishing

| Skill | Plugin | Tier | Trigger Keywords / Activation |
| :--- | :--- | :--- | :--- |
| [social-publishing](../plugins/social-publishing/skills/social-publishing/SKILL.md) | `social-publishing` | **Tier 2 (MVP)** | > |

### Software Craftsmanship & Testing

| Skill | Plugin | Tier | Trigger Keywords / Activation |
| :--- | :--- | :--- | :--- |
| [diagnosing-bugs](../plugins/software-craft/skills/diagnosing-bugs/SKILL.md) | `software-craft` | **Tier 2 (MVP)** | Use when the user says "diagnose"/"debug this", or reports something broken/throwing/failing/slow |
| [resolving-merge-conflicts](../plugins/software-craft/skills/resolving-merge-conflicts/SKILL.md) | `software-craft` | **Tier 2 (MVP)** | Use when you need to resolve an in-progress git merge/rebase conflict |
| [safe-refactor](../plugins/software-craft/skills/safe-refactor/SKILL.md) | `software-craft` | **Tier 3 (Architecture)** | Use when restructuring code architecture while guaranteeing behavior preservation |
| [surgical-patch](../plugins/software-craft/skills/surgical-patch/SKILL.md) | `software-craft` | **Tier 2 (MVP)** | Use when regression proof, preserved surrounding behavior, and task-relevant tests matter |
| [systematic-debugging](../plugins/software-craft/skills/systematic-debugging/SKILL.md) | `software-craft` | **Tier 2 (MVP)** | Use when encountering any bug, test failure, or unexpected behavior, before proposing fixes |
| [test-driven-development](../plugins/software-craft/skills/test-driven-development/SKILL.md) | `software-craft` | **Tier 2 (MVP)** | Use when implementing any feature or bugfix, before writing implementation code |
| [using-git-worktrees](../plugins/software-craft/skills/using-git-worktrees/SKILL.md) | `software-craft` | **Tier 2 (MVP)** | Use when starting feature work that needs isolation from current workspace or before executing implementation plans - ensures an isolated workspace exists via native tools or git worktree fallback |

### Startup Strategy & Financials

| Skill | Plugin | Tier | Trigger Keywords / Activation |
| :--- | :--- | :--- | :--- |
| [competitive-landscape](../plugins/startup-business-analyst/skills/competitive-landscape/SKILL.md) | `startup-business-analyst` | **Tier 2 (MVP)** | Use when working with competitive landscape |
| [market-sizing-analysis](../plugins/startup-business-analyst/skills/market-sizing-analysis/SKILL.md) | `startup-business-analyst` | **Tier 2 (MVP)** | Use when working with market sizing analysis |
| [startup-financial-modeling](../plugins/startup-business-analyst/skills/startup-financial-modeling/SKILL.md) | `startup-business-analyst` | **Tier 3 (Architecture)** | Use when working with startup financial modeling |
| [startup-metrics-framework](../plugins/startup-business-analyst/skills/startup-metrics-framework/SKILL.md) | `startup-business-analyst` | **Tier 2 (MVP)** | Use when working with startup metrics framework |
| [team-composition-analysis](../plugins/startup-business-analyst/skills/team-composition-analysis/SKILL.md) | `startup-business-analyst` | **Tier 2 (MVP)** | Use when working with team composition analysis |

### Superself

| Skill | Plugin | Tier | Trigger Keywords / Activation |
| :--- | :--- | :--- | :--- |
| [superself](../plugins/superself/skills/superself/SKILL.md) | `superself` | **Tier 2 (MVP)** | Use when a project keeps its state in Superself (a `<!-- superself:begin` block in AGENTS.md or CLAUDE.md, or `self setup` resolves the directory to a registered project): read `self context` at session start, attach work to a work unit, report with evidence, and record confirmed decisions so the next session picks up where this one left off |

### Systems Programming

| Skill | Plugin | Tier | Trigger Keywords / Activation |
| :--- | :--- | :--- | :--- |
| [go-concurrency-patterns](../plugins/systems-programming/skills/go-concurrency-patterns/SKILL.md) | `systems-programming` | **Tier 2 (MVP)** | Use when building concurrent Go applications, implementing worker pools, or debugging race conditions |
| [memory-safety-patterns](../plugins/systems-programming/skills/memory-safety-patterns/SKILL.md) | `systems-programming` | **Tier 2 (MVP)** | Use when writing safe systems code, managing resources, or preventing memory bugs |
| [rust-async-patterns](../plugins/systems-programming/skills/rust-async-patterns/SKILL.md) | `systems-programming` | **Tier 2 (MVP)** | Use when building async Rust applications, implementing concurrent systems, or debugging async code |

### UI Design & Component Systems

| Skill | Plugin | Tier | Trigger Keywords / Activation |
| :--- | :--- | :--- | :--- |
| [accessibility-compliance](../plugins/ui-design/skills/accessibility-compliance/SKILL.md) | `ui-design` | **Tier 4 (Audit)** | Use when auditing accessibility, implementing ARIA patterns, building for screen readers, or ensuring inclusive user experiences |
| [design-system-patterns](../plugins/ui-design/skills/design-system-patterns/SKILL.md) | `ui-design` | **Tier 3 (Architecture)** | Use when creating design tokens, implementing theme switching, building component libraries, or establishing design system foundations |
| [interaction-design](../plugins/ui-design/skills/interaction-design/SKILL.md) | `ui-design` | **Tier 2 (MVP)** | Use when adding polish to UI interactions, implementing loading states, or creating delightful user experiences |
| [mobile-android-design](../plugins/ui-design/skills/mobile-android-design/SKILL.md) | `ui-design` | **Tier 2 (MVP)** | Use when designing Android interfaces, implementing Compose UI, or following Google's Material Design guidelines |
| [mobile-ios-design](../plugins/ui-design/skills/mobile-ios-design/SKILL.md) | `ui-design` | **Tier 2 (MVP)** | Use when designing iOS interfaces, implementing SwiftUI views, or ensuring apps follow Apple's design principles |
| [react-native-design](../plugins/ui-design/skills/react-native-design/SKILL.md) | `ui-design` | **Tier 2 (MVP)** | Use when building React Native apps, implementing navigation patterns, or creating performant animations |
| [responsive-design](../plugins/ui-design/skills/responsive-design/SKILL.md) | `ui-design` | **Tier 1 (Quick)** | Use when building adaptive interfaces, implementing fluid layouts, or creating component-level responsive behavior |
| [visual-design-foundations](../plugins/ui-design/skills/visual-design-foundations/SKILL.md) | `ui-design` | **Tier 1 (Quick)** | Use when establishing design tokens, building style guides, or improving visual hierarchy and consistency |
| [web-component-design](../plugins/ui-design/skills/web-component-design/SKILL.md) | `ui-design` | **Tier 3 (Architecture)** | Use when building UI component libraries, designing component APIs, or implementing frontend design systems |
