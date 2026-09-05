# Architecture Specification: SOTA Swarm SDLC, Mandatory Research Protocol & Historic Archive Extraction

**Date:** 2026-09-05  
**Context:** Canonical architecture codifying the non-negotiable research protocol, swarm SDLC mechanics, and historic estate extraction into `/Users/man/agents`.  
**Authority:** Living architecture and implementation standard. Governed by Boris Cherny, Andrej Karpathy, and OpenClaw §0 invariants.

---

## 1. Executive Summary & Core Rule Ratification

This specification solidifies the engineering contract for `/Users/man/agents`:
1. **Mandatory A Priori Research & Counter-Points:** Research is not optional and must never require operator prompting. Before proposing architectures or non-trivial code, agents must automatically benchmark internal research and top GitHub repositories, surfacing explicit counter-points (CP1..CPN) with trade-offs.
2. **First-Principles Swarm SDLC:** Work is isolated in Git worktrees (`work/<task-id>`), anchored in GitHub Issues, offloaded to cloud/local compute by cost tier, and validated via cross-model review before production merge.
3. **Historic Estate Extraction:** Candidate tools from legacy `agent-*` repositories are selectively distilled via mechanical triage manifests into native `plugins/`. Unneeded legacy directories are packed to `~/archive/` and pruned to terminate estate sprawl.

---

## 2. Mandatory A Priori Research & SOTA Benchmarking Protocol

### 2.1 The 4-Stage Research Workflow
Whenever non-trivial architectural, structural, or refactoring tasks are requested, the agent must execute this workflow prior to proposing code:

1. **Stage 1: Internal Estate Cross-Reference**
   - Inspect `docs/research/` (e.g., `20260828-mike-intent-debrief.md`, `20260905-sota-patterns-and-anti-patterns.md`, `20260905-historic-estate-triage.json`).
   - Check past post-mortems in `CORRECTIONS.log` to identify documented failure modes and prevent repeat mistakes.
2. **Stage 2: External SOTA & Top GitHub Repository Benchmarking**
   - Query online sources, top starred repositories, and primary creator implementations (`karpathy/autoresearch`, `bcherny/openclaw`, `DietrichGebert/ponytail`, `affaan-m/ECC`, `obra/superpowers`, `Runfusion/Fusion`, `hatchet-dev/hatchet`, `conductor-oss/conductor`).
   - Inspect raw markdown/code directly; reject secondary summaries and hype.
3. **Stage 3: Anti-Wholesale Distillation & ROT Elimination**
   - Enforce the Anti-Wholesale Ingestion Law: extract durable principles and minimal runnable slices; discard redundant, obsolete, and trivial (ROT) complexity.
   - Apply the Ponytail YAGNI ladder: standard tools > top installed libraries > minimal bespoke code.
4. **Stage 4: Counter-Point Formulation (CP1..CPN)**
   - Formulate objective counter-points (`CP1..CPN`) challenging premature abstractions, over-engineering, and unverified assumptions.
   - Present findings with reference codes (`F1..FN`, `D1..DN`), comparison tables, and explicit recommendations.

---

## 3. First-Principles Swarm SDLC Architecture

### 3.1 Consensus Primitive: Git Worktrees
- **Isolation:** Agents never run parallel tasks in the primary checkout. Each active task provisions an isolated worktree under `work/<task-id>` linked to the central Git database.
- **Concurrency Ceiling:** Maximum 2 concurrent working trees globally across the machine to prevent Apple Silicon memory compression and disk thrashing.
- **Zero Data Loss:** Before pruning a worktree, uncommitted diffs are backed up to `backup/worktrees/<task-id>`.

### 3.2 Single Task Queue: GitHub Issues
- **Single Source of Truth:** GitHub Issues on `redtrades/agents` serve as the unified task queue.
- **Task Binding:** Every worktree, branch, and commit binds to an explicit issue (`feat/issue-<id>-<slug>`).
- **Elimination of Markdown Bureaucracy:** Task state files (`TASK.md`, `CONTINUATION.md`) exist for session cold-start recovery, while GitHub records assignment and delivery.

### 3.3 Compute Right-Sizing & Selective Swarm Routing
- **Cloud Heavy-Lifting (GitHub Jules):** Routine refactoring, test suite generation, and dependency updates are dispatched asynchronously to Jules (cloud VMs), preserving local machine cycles.
- **Local Zero-Cost Workhorse (Apple Silicon MLX):** Qwen 2.5 Coder 14B (MLX Q4, 14 GB RAM, 38-48 tok/s) handles local syntax parsing, lint checks, and privacy-sensitive operations at exact $0 marginal cost.
- **Interactive Frontier (Claude Max / Codex):** High-judgment architectural planning, synthesis, and complex multi-file contract refactors are reserved for interactive frontier sessions.

### 3.4 Verification & Review Independence Gate
- **Deterministic Proof:** Tasks are gated by exit code 0 across the four repository gates (`make validate STRICT=1`, `make garden`, `npm test`, `make test`). Prose assertions are invalid.
- **Cross-Model Review:** Non-trivial code authored by one model family (e.g. Claude) must be verified by an independent model family (e.g. Codex or Grok). No model family reviews its own work alone.
- **Production Merge Authority:** Final merge authority for production branches belongs solely to Mike.

---

## 4. Historic Estate Extraction & Cold Archiving Pipeline

### 4.1 Mechanical Triage Standard
Extraction is governed by the 239 KB triage index in `docs/research/20260905-historic-estate-triage.json`. Candidates must demonstrate clear necessity and pass ROT filtering before promotion.

### 4.2 Candidate Extraction Clusters
1. **Cluster 1 (`agent-mesh`):**
   - Extract: Multi-agent evaluation benchmarks, latency measurement harnesses, and contract validation suites.
   - Destination: `plugins/plugin-eval/` and `tools/tests/`.
2. **Cluster 2 (`agent-configs`):**
   - Extract: Pre-commit git hooks, linting rules, and harness generation scripts.
   - Destination: `tools/` and `rules/`.
3. **Cluster 3 (`agent-platform`):**
   - Extract: Subprocess execution wrappers and tested utility recipes.
   - Destination: Makefile targets and native shell scripts under `tools/`.

### 4.3 Cold Archiving Protocol
Once candidate tools are extracted and verified:
1. Verify no active uncommitted work remains in the target directory.
2. Package the legacy repository to `~/archive/<repo>-backup-YYYYMMDD.tar.gz`.
3. Safely delete the legacy working directory from `~` to eliminate estate filesystem sprawl and prevent circular search loops.

---

## 5. Explicit Counter-Points (CP1..CPN)

| Code | Architectural Proposal | Counter-Point & Risk | Mitigating Decision |
| :--- | :--- | :--- | :--- |
| `CP1` | **Custom Swarm Daemon** (building background Python supervisors to monitor worktrees) | **Risk:** Daemon crashes, memory bloat, background port conflicts, and unrecoverable state loops. | **Mitigation:** Use native Make recipes (`make worktree-spawn`, `make worktree-clean`) and Git CLI. Lean agents, fat recipes. |
| `CP2` | **Bulk Ingestion of `agent-*`** (copying historic directories wholesale) | **Risk:** Imports 100+ dead symlinks, obsolete Python wrappers, and conflicting schemas. | **Mitigation:** Enforce Anti-Wholesale Ingestion Law. Extract only vetted assets via mechanical triage manifest. |
| `CP3` | **Single-Model Self-Approval** (authoring model verifies its own PR) | **Risk:** Confirmation bias; model fails to see its own hallucinations or subtle regression bugs. | **Mitigation:** Cross-model review gate. Different model family must run independent verification before production merge. |
| `CP4` | **Flat Uncoordinated Swarms** (spawning 5-10 agents in a single shared working tree) | **Risk:** Overlapping file writes, dirty git index corruption, and context-window competition. | **Mitigation:** Worktree isolation (1 worktree per session, max 2 concurrent globally). |
