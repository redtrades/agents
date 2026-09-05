# Autonomous Provider-Neutral AI Software Engineering Swarm: Research & Architecture

**Document Version:** 1.0.0  
**Status:** Read-only architecture brief & research report  
**Access / Evaluation Date:** 2026-08-29  
**Target Repository:** `agent-platform`

---

## Executive Summary & Recommendation

**Recommendation:** **Compose two or more projects and build only a thin missing control layer.**

```text
+---------------------------------------------------------------------------------------+
|                                 PLATFORM GOVERNANCE                                   |
|   GitHub Issues (Work Queue) <---> Project Board (View) <---> SQLite / Git Receipts   |
+---------------------------------------------------------------------------------------+
                                           |
                                           v
+---------------------------------------------------------------------------------------+
|                       THIN DETERMINISTIC CONTROL SPINE (Python)                       |
|   • Symphony-style Polling Loop         • SQLite CAS Leases with Fencing Tokens       |
|   • Beads-style Task Dependency Graph   • Expected-Head CAS Promoter (Fail-Closed)    |
|   • 4-Outcome Policy Engine (AUTO_READ / AUTO_WRITE / APPROVAL_DESTRUCTIVE / DENY)    |
+---------------------------------------------------------------------------------------+
                                           |
                   +-----------------------+-----------------------+
                   |                                               |
                   v                                               v
+------------------------------------+           +------------------------------------+
|         GENERATOR RUNTIME          |           |        INDEPENDENT REVIEWER        |
|  • OpenHands SDK / Headless Engine |           |  • Dedicated Verifier Process      |
|  • Local CLI (Claude/Codex/Hermes) |           |  • Distinct Model / Seed Principal |
|  • Google Jules Async Cloud Worker |           |  • Read-Only Inspection Tools      |
|  • Model Context Protocol (MCP)    |           |  • Signed Review Evidence Hash     |
+------------------------------------+           +------------------------------------+
```

### 1. Primary Recommendation
Compose:
1. **[OpenAI Symphony](https://github.com/openai/symphony)'s** architectural state machine and workspace lifecycle specification ([`SPEC.md`](https://github.com/openai/symphony/blob/main/SPEC.md)).
2. **[All-Hands-AI OpenHands SDK](https://github.com/OpenHands/software-agent-sdk)** for headless, sandboxed agent execution loops and container isolation.
3. **[Steve Yegge's Beads](https://github.com/gastownhall/beads)** task-graph and dependency data model.
4. **[Model Context Protocol (MCP)](https://github.com/modelcontextprotocol)** for standardized tool/context hydration.
5. **A Platform-Owned Thin Control Spine (~800 lines of deterministic Python)** providing the irreducible hard controls that no existing open-source tool implements out of the box:
   - Monotonically increasing generation fencing tokens (`fence_token = lease_id:generation`) on a local/remote SQLite compare-and-swap (CAS) ledger.
   - Genuine principal separation between the Generator worker and an adversarial Reviewer principal.
   - An expected-head compare-and-swap git promoter that safely lands reviewed changes on GitHub Free private repositories without requiring enterprise merge queues.
   - Immutable receipt generation binding task input SHA, candidate tree SHA, test logs, reviewer signature, and teardown state.

### 2. Strongest Challengers
* **[OpenHands](https://github.com/OpenHands/OpenHands) with `openhands-resolver`:** The most complete autonomous coding implementation. However, it is structured as a monolithic single-issue-to-PR batch pipeline. It lacks multi-worker atomic leases with generation fencing, provides no independent adversarial reviewer identity (the agent reviews its own work or waits for human review), and does not enforce expected-head CAS merges.
* **[OpenAI Symphony](https://github.com/openai/symphony) (and Kata Symphony):** The cleanest conceptual architecture for polling issue trackers, creating isolated worktree roots, and dispatching agent runners. However, it was released as an unmaintained engineering preview, relies on in-memory/process leases rather than monotonic cryptographic fencing tokens, lacks candidate receipt provenance, and defaults merge authority to human approval or unguarded PR merges.
* **[cliftonc/lastlight](https://github.com/cliftonc/lastlight):** A cohesive self-hosted software factory featuring Architect -> Executor -> Reviewer roles and SQLite persistence. However, its reviewer is an in-band prompt step within the same execution context rather than an independently authenticated principal, its state is not generation-fenced against network partitions/zombie processes, and it lacks expected-head promotion.

### 3. Why Build the Missing Control Layer?
No existing open-source project enforces the **fail-closed, 4-outcome effect policy** ([`docs/OPERATING-MODEL.md`](docs/OPERATING-MODEL.md)) across heterogeneous agent harnesses on a private repository without paid GitHub Enterprise merge queues. Commodity tools either:
- Rely on prompt-level self-discipline (hallucinated completions and self-merges).
- Require heavyweight SaaS/Enterprise infrastructure (Temporal, Kubernetes, LangSmith Platform).
- Fail to isolate the reviewer identity from the generator identity.

---

## B. Comprehensive Feature Matrix

### Evaluation Criteria Grades
* **PASS**: Officially verified in upstream source code / specification with direct links.
* **PARTIAL**: Partially implemented, requires significant custom glue, or documented with material operational gaps.
* **FAIL**: Absent, architectural anti-pattern, or explicitly unsupported.
* **UNKNOWN**: Unverifiable from public primary sources.

### Candidate Matrix

| Capability / Dimension | [OpenAI Symphony](https://github.com/openai/symphony) | [OpenHands SDK / Resolver](https://github.com/OpenHands/OpenHands) | [Last Light](https://github.com/cliftonc/lastlight) | [Paperclip](https://github.com/paperclipai/paperclip) | [SSSF & The Verifier](https://github.com/disler/super-simple-software-factory) | [GitHub Agentic Workflows (gh-aw)](https://github.com/github/gh-aw) | [Gas Town & Beads](https://github.com/gastownhall/gastown) | [Machinist](https://github.com/owainlewis/machinist) | [Google Jules API](https://jules.google.com) | [Hatchet / Restate](https://github.com/hatchet-dev/hatchet) | [Proposed Platform Spine](docs/ARCHITECTURE.md) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Atomic Task Claim** | PARTIAL | FAIL | PARTIAL | PARTIAL | FAIL | FAIL | PARTIAL | PARTIAL | PARTIAL | **PASS** | **PASS** |
| **Resource Locking** | **PASS** | FAIL | FAIL | FAIL | FAIL | FAIL | PARTIAL | FAIL | FAIL | **PASS** | **PASS** |
| **Fencing Generations** | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | PARTIAL | **PASS** |
| **Isolated Workspaces** | **PASS** | **PASS** | PARTIAL | PARTIAL | FAIL | **PASS** | PARTIAL | PARTIAL | **PASS** | PARTIAL | **PASS** |
| **Durable State** | PARTIAL | PARTIAL | **PASS** | **PASS** | FAIL | FAIL | **PASS** | PARTIAL | **PASS** | **PASS** | **PASS** |
| **Checkpoint / Resume** | PARTIAL | **PASS** | PARTIAL | PARTIAL | FAIL | FAIL | **PASS** | FAIL | **PASS** | **PASS** | **PASS** |
| **Crash Recovery** | **PASS** | PARTIAL | PARTIAL | PARTIAL | FAIL | FAIL | PARTIAL | FAIL | **PASS** | **PASS** | **PASS** |
| **Exact Input/Candidate Binding** | PARTIAL | PARTIAL | FAIL | FAIL | FAIL | PARTIAL | PARTIAL | PARTIAL | PARTIAL | FAIL | **PASS** |
| **Deterministic CI Evidence** | PARTIAL | **PASS** | **PASS** | PARTIAL | PARTIAL | **PASS** | PARTIAL | **PASS** | **PASS** | **PASS** | **PASS** |
| **Independent Reviewer Principal** | FAIL | FAIL | PARTIAL | FAIL | **PASS** | FAIL | PARTIAL | **PASS** | FAIL | FAIL | **PASS** |
| **Expected-Head Auto-Merge** | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | **PASS** |
| **Issue / Project Synchronization**| **PASS** | **PASS** | **PASS** | **PASS** | FAIL | **PASS** | PARTIAL | **PASS** | PARTIAL | PARTIAL | **PASS** |
| **Teardown / Rollback Receipts** | PARTIAL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | **PASS** |
| **Provider Neutrality** | **PASS** | **PASS** | **PASS** | **PASS** | PARTIAL | PARTIAL | **PASS** | PARTIAL | FAIL | **PASS** | **PASS** |
| **Harness Neutrality** | PARTIAL | PARTIAL | FAIL | FAIL | FAIL | FAIL | PARTIAL | FAIL | FAIL | **PASS** | **PASS** |
| **Declarative Clean-Host Rebuild** | **PASS** | PARTIAL | **PASS** | PARTIAL | **PASS** | **PASS** | **PASS** | **PASS** | **PASS** | PARTIAL | **PASS** |
| **API / Control-Plane Suitability** | **PASS** | **PASS** | PARTIAL | **PASS** | FAIL | PARTIAL | PARTIAL | PARTIAL | **PASS** | **PASS** | **PASS** |
| **Mobile / Command Suitability** | FAIL | PARTIAL | PARTIAL | **PASS** | FAIL | FAIL | FAIL | FAIL | PARTIAL | PARTIAL | **PASS** |
| **Maintenance Health** | PARTIAL | **PASS** | PARTIAL | **PASS** | PARTIAL | **PASS** | **PASS** | PARTIAL | **PASS** | **PASS** | **PASS** |
| **Open License (Commercial Reuse)**| **PASS** | **PASS** | **PASS** | **PASS** | **PASS** | **PASS** | **PASS** | **PASS** | FAIL | **PASS** | **PASS** |

### Verified Primary Source References for Key Passes
* **OpenAI Symphony Workspace Isolation & Tracker Polling:** [`openai/symphony/SPEC.md`](https://github.com/openai/symphony/blob/main/SPEC.md) & [Elixir Orchestrator](https://github.com/openai/symphony/tree/main/elixir).
* **OpenHands SDK Sandboxing & Headless Resolver:** [`OpenHands/software-agent-sdk`](https://github.com/OpenHands/software-agent-sdk) and [`OpenHands/OpenHands resolver`](https://github.com/OpenHands/OpenHands/tree/main/openhands/resolver).
* **Beads Task Graph & SQLite Memory:** [`gastownhall/beads`](https://github.com/gastownhall/beads).
* **The Verifier Independent Observer Pattern:** [`disler/the-verifier-agent`](https://github.com/disler/the-verifier-agent).
* **Machinist Proposer/Disposer State Machine:** [`owainlewis/machinist`](https://github.com/owainlewis/machinist).
* **Hatchet Durable Execution Engine:** [`hatchet-dev/hatchet`](https://github.com/hatchet-dev/hatchet).
* **Restate Durable Services:** [`restatedev/restate`](https://github.com/restatedev/restate).
* **GitHub Agentic Workflows Sandboxing & Compiling:** [`github/gh-aw`](https://github.com/github/gh-aw).
* **Google Jules Async Sessions API:** [Google Jules API v1alpha](https://jules.google.com).
* **Model Context Protocol Specification:** [Model Context Protocol](https://modelcontextprotocol.io).
* **Agent Client Protocol Registry & SDK:** [Agent Client Protocol](https://agentclientprotocol.com).

---

## C. Recommended Architecture

The platform architecture follows the **"Thin Controller, Thick Isolation, Replaceable Workers"** model. It reuses proven open-source components for execution, sandboxing, and protocols, while strictly owning the state machine, leases, and promotion gates.

```text
                                  +-----------------------+
                                  |     GitHub Issues     | <--- Intent & Acceptance Authority
                                  |    & Project Board    | <--- Human Observation Surface
                                  +-----------------------+
                                              |
                                     (1) Poll / Webhook
                                              v
+---------------------------------------------------------------------------------------------------+
| PLATFORM CONTROLLER DAEMON (Python 3.12 / SQLite)                                                 |
|                                                                                                   |
|  +-----------------------------------+               +-----------------------------------------+  |
|  |       LEASING & FENCING ENGINE    |               |          4-OUTCOME EFFECT POLICY        |  |
|  |  • CAS Lease with Monotonic Token |               |  • DENY: Stale token, invalid grant    |  |
|  |  • Resource lock (Path/Branch)    |               |  • AUTO_READ: Safe observation          |  |
|  |  • Lease Expiration & Heartbeat   |               |  • AUTO_WRITE: Valid lease & review pass|  |
|  +-----------------------------------+               |  • APPROVAL_DESTRUCTIVE: Unexpired grant|  |
|                  |                                   +-----------------------------------------+  |
|                  v                                                        ^                       |
|  +---------------------------------------------------------------------+  |                       |
|  | TASK PACKET GENERATOR (Immutable JSON Hash)                         |  |                       |
|  | {issue_id, base_sha, spec, acceptance_criteria, fence_token, budget}|  |                       |
|  +---------------------------------------------------------------------+  |                       |
|                  |                                                        |                       |
|                  +------------------------+                               |                       |
|                                           |                               |                       |
|                                           v                               |                       |
|                        +-------------------------------------+            |                       |
|                        |     EXPECTED-HEAD CAS PROMOTER      |------------+                       |
|                        |  • Validate Reviewer Receipt        |                                    |
|                        |  • Compare: Remote HEAD == Base SHA |                                    |
|                        |  • Atomic Push / Fast-Forward Merge |                                    |
|                        +-------------------------------------+                                    |
+---------------------------------------------------------------------------------------------------+
       |                                                               |
       | (2) Dispatch Packet                                           | (4) Dispatch Verification
       v                                                               v
+------------------------------------+                       +------------------------------------+
| GENERATOR PRINCIPAL                |                       | INDEPENDENT REVIEWER PRINCIPAL     |
| (Identity: bot-generator)          |                       | (Identity: bot-reviewer)           |
|                                    |                       |                                    |
| • Isolated Git Worktree / Docker   |                       | • Separate Process / Container     |
| • Harness Adapter:                 |                       | • Distinct Model & Clean Context   |
|   - OpenHands Headless SDK         |                       | • Read-Only Inspection Tools (MCP) |
|   - Claude Code / Codex / Hermes   |                       | • Deterministic Gate Runner (CI)   |
|   - Google Jules Async Cloud VM    |                       | • Signs Review Evidence Receipt    |
| • Produces: Candidate Commit SHA   |                       | • Emits: PASS / REVISE / REJECT    |
+------------------------------------+                       +------------------------------------+
       |                                                               |
       +----------------------------> [RECEIPT LEDGER] <---------------+
                               (SQLite + Local Evidence Store)
```

### 1. Adopted Components
* **Execution & Sandboxing:** **OpenHands SDK (`software-agent-sdk`)** for containerized, headless agent execution with standard bash/git tool definitions.
* **Tool & Context Interoperability:** **Model Context Protocol (MCP)** servers for filesystem, GitHub API, git tree inspection, and terminal access.
* **Task Graph Primitives:** **Steve Yegge’s Beads (`gastownhall/beads`)** JSON schema for tracking sub-issue dependency trees and status.
* **Cloud Asynchronous Offloading:** **Google Jules REST API (`v1alpha`)** adapter for long-running, VM-isolated background tasks via `X-Goog-Api-Key`.
* **Model Gateway (Optional):** **LiteLLM Proxy** for fallback routing, rate-limit retries, and token cost tracking across providers.

### 2. Narrowly Forked / Adapted Components
* **Symphony Reconciliation Engine:** Adapt the core state transitions of [`openai/symphony/SPEC.md`](https://github.com/openai/symphony/blob/main/SPEC.md) into an async Python loop without requiring the Elixir runtime.
* **The Verifier Sibling Pattern:** Adapt [`disler/the-verifier-agent`](https://github.com/disler/the-verifier-agent) into a clean, detached reviewer container that operates with read-only tools and independent model credentials.

### 3. Platform-Owned Control Code (Genuinely Unavoidable)
* **`atomic_lease.py`:** CAS leasing engine using SQLite `BEGIN IMMEDIATE` transactions with monotonic generation counters. Rejects any write or status update carrying an outdated generation.
* **`effect_controller.py`:** Implements the 4-outcome state machine ([`docs/OPERATING-MODEL.md`](docs/OPERATING-MODEL.md)) ensuring routine work drains automatically without human clicks, while destructive operations fail closed.
* **`promoter.py`:** Expected-head compare-and-swap git promoter. Executes atomic git pushes enforcing `expected_old_sha == remote_head_sha`, bypassing the limitations of GitHub Free private repositories.
* **`receipt_ledger.py`:** Cryptographic evidence accumulator that records JSON receipts binding `{task_packet_sha, base_commit_sha, candidate_commit_sha, test_evidence_sha, reviewer_signature, promoter_receipt_sha}`.

### 4. Authority and State Boundaries
* **Task Intent & Priority:** GitHub Issues and Subissues (Human & Factory consensus).
* **Task Mutex & Concurrency:** SQLite / Git CAS Lease Ledger (`agent_leases.db`).
* **Candidate Source Truth:** Git commit hashes and tree objects in the canonical repository.
* **Execution State:** Isolated ephemeral worktrees (`.worktrees/issue-<id>-gen-<n>`) or OpenHands Docker containers.
* **Promotion Authority:** Expected-Head CAS Promoter validating dual receipts (CI pass + Independent Reviewer pass).

### 5. Identity, CI, Secrets, and Rebuild
* **GitHub App Identities:**
  - `factory-worker[bot]`: Scoped permissions to create branches, push work commits, and read issues.
  - `factory-reviewer[bot]`: Scoped read-only access to repository contents and issue comments; post-review review receipts.
  - `factory-promoter[bot]`: Scoped write access to `main` for fast-forward expected-head CAS pushes.
* **CI Runners:** Local deterministic test execution within isolated worktrees (or GitHub Actions self-hosted runners using ephemeral sandboxes).
* **Secrets Boundary:** Credentials never enter Git. Stored in macOS Keychain or `.env.local` outside repository roots; injected into agent harnesses via opaque environment variables or 1Password CLI (`op run`).
* **Clean Rebuild:** Declarative single-script bootstrap (`./scripts/bootstrap.sh` or `make init`) installing Python virtual environments, Git hooks, local SQLite schemas, and MCP configurations in $< 60$ seconds.

---

## D. First Working Vertical Slice

The first vertical slice demonstrates the complete, unattended lifecycle on a single issue with zero routine human intervention, including deterministic chaos tests.

```text
+-----------------------------------------------------------------------------------------+
|                               VERTICAL SLICE SEQUENCE                                   |
+-----------------------------------------------------------------------------------------+

1. DISCOVERY:
   - Issue #42 in GitHub Project labeled 'ready'.
   - Controller polls issue, extracts requirements and acceptance criteria.

2. ATOMIC LEASE & GENERATION FENCING:
   - Worker A claims Issue #42.
   - SQLite CAS allocates Lease #101 with Fence Token: "lease-101:gen-1".
   - Competing Worker B attempts concurrent claim -> DENIED (Active Lease).

3. ISOLATED WORKSPACE HYDRATION:
   - Worktree created at `.worktrees/issue-42-gen1` pinned to current `main` HEAD (SHA-0).
   - Task packet JSON injected with immutable input hash.

4. IMPLEMENTATION & SEEDED BUG CORRECTION:
   - Worker A (Generator) generates code changes and candidate commit SHA-1.
   - Local CI deterministic tests run (linters, unit tests, security scans).
   - Reviewer Principal (Verifier) inspects candidate SHA-1 with read-only tools.
   - Seeded syntax error detected -> Reviewer emits REJECT receipt with exact diff findings.
   - Worker A consumes findings, repairs code, commits candidate SHA-2.
   - Reviewer re-evaluates SHA-2 -> Emits PASS with cryptographically signed receipt.

5. EXPECTED-HEAD CAS PROMOTION:
   - Promoter verifies dual receipts (CI PASS + Reviewer PASS).
   - Promoter checks remote `main` HEAD matches SHA-0.
   - Promoter executes atomic fast-forward push (`main` -> SHA-2).

6. ISSUE CLOSE & TEARDOWN RECEIPT:
   - Issue #42 closed automatically with linked receipt hash.
   - GitHub Project board updated to 'Done'.
   - Ephemeral worktree pruned and locked resources released.
```

### Chaos & Resilience Verifications in the Vertical Slice
1. **Competing Worker Race:** Worker B attempts an atomic claim on Issue #42 while Worker A holds Lease #101 Gen 1. The SQLite CAS transaction fails for Worker B with `DENY_LEASE_ACTIVE`.
2. **Seeded Failure & Automatic Correction:** Worker A introduces a deliberate lint/test violation in candidate `SHA-1`. Reviewer principal fails candidate `SHA-1`, returns exact line-numbered failure evidence. Worker A consumes findings, applies correction `SHA-2`, and passes re-verification without human prompt intervention.
3. **Stale-Generation Rejection (Zombie Worker):** Worker A is paused via `SIGSTOP` (simulating network partition or quota freeze). Lease expires. Worker B is leased Gen 2. Worker A wakes up and attempts to submit candidate for Gen 1. Controller rejects submission with `STALE_GENERATION_DENY`.
4. **Process Termination & Cold Resume:** Controller daemon is killed with `SIGKILL` mid-execution. Upon reboot, the daemon reads `agent_leases.db`, reconciles with the Git worktree status, detects the unexpired lease, and resumes execution seamlessly from the last recorded task packet without re-running passed stages or losing context.
5. **Zero Human Approval Proof:** The issue progresses from `ready` -> `in_progress` -> `review` -> `merged` -> `closed` with 0 human clicks or approvals.

---

## E. Five-Step Adoption Plan

```text
+-----------------------------------------------------------------------------------+
| STEP 1: Core State Machine & Atomic CAS Lease Engine (SQLite Ledger)              |
| Outcome: Multi-worker concurrency safety with monotonic generation fencing        |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
| STEP 2: Worktree Lifecycle & Task Packet Contract                                 |
| Outcome: Isolated workspace provisioning, hydration, and immutable input hashing  |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
| STEP 3: Dual-Principal Execution (Generator & Independent Reviewer)               |
| Outcome: OpenHands SDK / CLI harness + Detached Verifier with signed receipts     |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
| STEP 4: Expected-Head CAS Promotion & GitHub Integration                          |
| Outcome: Automated fast-forward merges, issue closing, and Project sync on Free tier|
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
| STEP 5: Cloud Worker Adapters (Google Jules API & Heterogeneous Models)           |
| Outcome: Asynchronous cloud offloading and provider-neutral routing               |
+-----------------------------------------------------------------------------------+
```

### Step 1: Core State Machine & Atomic CAS Lease Engine
* **Exact Outcome:** A standalone deterministic SQLite database schema and Python module providing atomic lease acquisition, heartbeats, lease stealing after TTL expiration, and monotonic fencing token verification.
* **Adopted Component:** Adapted from **OpenAI Symphony** leasing concepts and **Beads** SQLite primitives.
* **Smallest Necessary Changes:** Implement `atomic_lease.py` with `acquire_lease(issue_id, worker_id) -> (fence_token, lease_id)` and `verify_generation(lease_id, fence_token) -> bool`.
* **Deterministic Acceptance Test:** Two concurrent Python test processes attempt to claim the same issue ID simultaneously. Exactly one succeeds; the second receives `DENY`. Expired lease takeover increments generation from `1` to `2`.
* **Stop Condition:** Concurrency tests pass with zero duplicate leases across 100 iterations.
* **What Must NOT Be Built Yet:** Do not build webhooks, UI dashboards, or remote network databases.

### Step 2: Worktree Lifecycle & Task Packet Contract
* **Exact Outcome:** Ephemeral git worktree manager that creates isolated directories (`.worktrees/issue-<id>-gen-<n>`), injects the versioned `AGENTS.md` and task packet JSON, and deterministically tears them down upon completion.
* **Adopted Component:** Native Git worktrees (`git worktree add / remove / prune`).
* **Smallest Necessary Changes:** Implement `worktree_manager.py` that checks out the exact base commit SHA, isolates workspace state, and computes task packet input hashes.
* **Deterministic Acceptance Test:** Create worktree, make changes, verify host repository is completely unaffected, prune worktree, verify zero leftover locks.
* **Stop Condition:** Clean creation, hydration, and removal of 10 consecutive worktrees.
* **What Must NOT Be Built Yet:** Do not configure multi-machine shared network storage (NFS/EFS) or Kubernetes PVs.

### Step 3: Dual-Principal Execution (Generator & Independent Reviewer)
* **Exact Outcome:** Execution harness that runs a Generator agent in the worktree, captures candidate commit SHA, and immediately passes it to an independent Reviewer process (different model/seed) with read-only tools.
* **Adopted Component:** **OpenHands SDK (`software-agent-sdk`)** for worker execution; **The Verifier (`the-verifier-agent`)** pattern for independent review.
* **Smallest Necessary Changes:** Implement `harness_adapter.py` (running Generator) and `reviewer_adapter.py` (running Reviewer), returning a structured `ReviewReceipt(verdict=PASS|FAIL, findings=[...], signature=...)`.
* **Deterministic Acceptance Test:** Run an automated test where the generator produces a candidate with a seeded syntax error. The reviewer detects the error, rejects the candidate, and triggers a successful repair loop.
* **Stop Condition:** Automated generator-reviewer loop successfully fixes seeded bugs in test fixtures.
* **What Must NOT Be Built Yet:** Do not build semantic vector memory or dynamic agent-to-agent negotiations.

### Step 4: Expected-Head CAS Promotion & GitHub Integration
* **Exact Outcome:** Promoter that queries the remote GitHub `main` branch HEAD SHA, compares it against the candidate's recorded `base_commit_sha`, executes an atomic fast-forward push, closes the GitHub issue, and updates the Project board.
* **Adopted Component:** GitHub REST/GraphQL API via `gh` CLI / `httpx`.
* **Smallest Necessary Changes:** Implement `promoter.py` executing `git push origin candidate_sha:refs/heads/main` conditional on remote HEAD matching expected base. If base drifted, trigger automatic rebase and re-verification.
* **Deterministic Acceptance Test:** Simulate remote HEAD drift during review. Verify promoter detects mismatch, denies direct push, triggers clean rebase in worktree, re-runs deterministic checks, and successfully merges.
* **Stop Condition:** End-to-end Issue -> Worktree -> Review -> Auto-Merge -> Issue Close completes on live test repository.
* **What Must NOT Be Built Yet:** Do not purchase GitHub Enterprise or configure complex third-party merge queues.

### Step 5: Cloud Worker Adapters (Google Jules API & Heterogeneous Models)
* **Exact Outcome:** Pluggable harness adapters allowing tasks to be delegated asynchronously to Google Jules Cloud VMs or local CLI tools (Claude Code, Codex, Hermes, Pi).
* **Adopted Component:** **Google Jules REST API (`v1alpha`)** and **LiteLLM**.
* **Smallest Necessary Changes:** Implement `jules_adapter.py` creating sessions with `X-Goog-Api-Key`, monitoring activity completion, and importing the resultant PR/branch back into the local verification pipeline.
* **Deterministic Acceptance Test:** Dispatch a task packet to the Jules API, poll session to completion, pull candidate branch into local worktree, pass through Independent Reviewer, and merge via Expected-Head CAS promoter.
* **Stop Condition:** One task successfully completed via local OpenHands harness and one task completed via Google Jules API using identical task packet contracts.
* **What Must NOT Be Built Yet:** Do not build multi-tenant user authentication, billing, or custom Web UIs.

---

## F. Contrarian Conclusion

### 1. Are we overengineering this?
**No on hard transactional controls; Yes on infrastructure frameworks.**
- **Where we are not overengineering:** Monotonic generation fencing, atomic CAS leasing, separate reviewer identity, and expected-head merge promotion are **mathematically irreducible requirements**. Without them, concurrent AI agents corrupt git histories, overwrite newer work with stale revisions, hallucinate successful task completion, and create merge conflicts.
- **Where the industry overengineers:** Adopting heavyweight distributed orchestrators (Temporal, Kubernetes microVM fleets, LangSmith Platform, complex BPMN engines) or full multi-agent organizational role-playing hierarchies (CEO/Manager/Worker chat loops). For a solo-operated software factory, these add immense operational friction without solving the core transaction safety problem.

### 2. Which requirements belong in the first working lifecycle?
1. **GitHub Issues as the durable work queue.**
2. **SQLite atomic CAS lease ledger with monotonic generation fencing.**
3. **Isolated Git worktrees for every attempt.**
4. **Deterministic test/linter verification gates.**
5. **Independent Reviewer principal (separate process/model) emitting signed receipts.**
6. **Expected-head CAS promotion with automatic issue closing.**
7. **Cold crash recovery from local SQLite state.**

### 3. Which requirements should be deferred?
* **Distributed workflow engines (Temporal/Hatchet):** SQLite `BEGIN IMMEDIATE` + local daemon handles 10–50 concurrent tasks on a single machine easily.
* **Vector/Semantic Memory:** Git commit logs, issue descriptions, and `AGENTS.md` files in context provide 95% of required knowledge without retrieval drift.
* **Complex Web Dashboards / Mobile Command Centers:** GitHub Issues and GitHub Projects are already accessible on desktop and mobile.
* **Multi-tenant isolation / Enterprise RBAC:** Completely unnecessary for a solo developer or unified team.

### 4. What is the fastest credible path to a functioning swarm within days?
1. **Day 1:** Write `atomic_lease.py` (SQLite CAS ledger with monotonic fencing) and `worktree_manager.py` (git worktree isolation) in Python (~400 lines).
2. **Day 2:** Write `harness_adapter.py` integrating the **OpenHands SDK** (or local Claude Code / Codex subprocess CLI) and **The Verifier** pattern for dual-principal implementation and review (~300 lines).
3. **Day 3:** Write `promoter.py` and GitHub Issue poll/close loop using `gh` CLI (~250 lines).
4. **Day 4:** Add the **Google Jules API** async adapter for background cloud tasks.
5. **Day 5:** Run the end-to-end vertical slice across 10 test issues with seeded failure and crash scenarios.

This delivers a bulletproof, provider-neutral autonomous software engineering swarm within **one week**, entirely free of recurring platform software costs and immune to stale agent race conditions.
