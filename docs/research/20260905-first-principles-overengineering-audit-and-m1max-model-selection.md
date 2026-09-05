# Systems Audit: Over-Engineering Traps, Zero-Amnesia Handoffs, and M1 Max Hardware Tuning (2026)

## Executive Summary

This audit critically examines the multi-agent estate from first principles to eliminate over-engineering, solve the "agent amnesia on usage exhaustion" failure mode, and right-size local inference models for an **Apple M1 Max with 64 GB unified memory**.

---

## 1. The Over-Engineering Audit: What We Are Over-Indexing On

### 1.1 The Multi-Control-Plane Trap
- **The Pitfall:** Attempting to operate Buzz (Nostr relay), Hatchet (PostgreSQL state engine), Fusion (Node/Vite DAG board), OpenHands (Docker daemon), and custom bash reapers simultaneously on a single machine.
- **The Consequence:**
  - Consumes all 64 GB of RAM with background daemon processes.
  - Generates cross-system state drift (a task is marked `done` in GitHub, `in-progress` in Fusion, and `pending` in Buzz).
  - Triggers the historic meta-work loop: spending more time debugging daemon synchronization than building software or closing GovCon deals.
- **The First-Principles Fix:**
  - **Single Source of Truth:** GitHub Issues and Pull Requests.
  - **Single Visual Glass:** Fusion on port 4040 acting purely as a lightweight viewer and telemetry dashboard over GitHub.
  - **Single Model Gateway:** LiteLLM Proxy on port 3100.
  - **Single Execution Protocol:** Agent Client Protocol (ACP) driving headless Goose or Hermes workers in temporary git worktrees.

---

## 2. Solving Agent Amnesia & Token Exhaustion Without Token Burn

### 2.1 Why Current Swarms Fail When Limits Hit
When an agent reaches an hourly quota, API rate limit (HTTP 429), or context window limit, its conversation trajectory is severed. Traditionally, restarting the task meant:
1. Spawning a new agent session.
2. Ingesting the entire codebase and prompt history from scratch.
3. Re-planning already decided architecture.
4. Burning tens of thousands of tokens only to run out of usage a second time.

### 2.2 The Zero-Loss Git-Backed Handoff Pattern (`CONTINUATION.md`)
Modern AI engineering eliminates this failure mode by externalizing state continuously to the filesystem and git, never relying on conversation memory across sessions:

1. **Incremental Git Checkpoints:**
   After every atomic tool execution or code change, the agent makes a local commit to `wip/issue-<id>`. Work is never left uncommitted in the working tree.
2. **The 5-Field `CONTINUATION.md` Protocol:**
   The agent continuously maintains a 50-line machine-readable file in `.agents/tasks/issue-<id>.json` (or `CONTINUATION.md`):
   ```yaml
   task_id: "SWARM-320"
   goal: "Add regression test guarding Failed task state in github-client"
   status: "in-progress"
   completed_steps:
     - step: "Preflight inspection"
       commit: "6111fe3"
     - step: "Write integration test for shouldAutoClose"
       commit: "a89d12e"
   interrupted_step: "Run full test suite npm test"
   modified_files:
     - "test/github-client.test.mjs"
   next_action: "Execute: npm test test/github-client.test.mjs"
   ```
3. **Cold-Start Resume Under 500 Tokens:**
   When a quota resets or an alternative model picks up the task, the new agent does not read previous conversation history. It reads **only** `CONTINUATION.md` and runs `git diff HEAD~1`. It resumes execution in under two seconds for less than 500 tokens.

---

## 3. Local Model Optimization: Apple M1 Max (64 GB Unified Memory)

### 3.1 The Memory Bandwidth Bottleneck
- **Hardware Profile:** The Apple M1 Max features 64 GB of unified memory with approximately 400 GB/s memory bandwidth.
- **Operating System Overhead:** macOS and resident developer tools (Docker, Chrome, IDEs, Fusion) require 14 to 18 GB of RAM, leaving approximately 46 to 50 GB for inference and disk cache.
- **The 32B Model Problem:**
  - A 32-billion parameter model (like Qwen 2.5 Coder 32B at 4-bit) requires ~20 GB for weights.
  - At long context windows (32k+ tokens), the KV cache requires an additional 10 to 14 GB.
  - Total allocation exceeds 34 GB, pushing total system memory to the edge of swapping.
  - Token generation speed on M1 Max drops to **12 to 14 tokens/second**, which feels sluggish for multi-step agent loops.

### 3.2 The Sweet-Spot Models for M1 Max 64GB (2026)

| Model | Weights Size (4-bit) | Total RAM + 32k KV Cache | M1 Max Speed | Coding Benchmark (HumanEval/SWE) | Best Role in Swarm |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Qwen 2.5 Coder 14B (MLX Q4_K_M)** | **~9 GB** | **~14 GB** | **38 to 48 tok/s** | **84.5% HumanEval** (matches GPT-4) | **Primary Local Workhorse:** Small code fixes, linter repairs, unit tests, fast repo cleanup. |
| **Qwen 2.5 Coder 7B (MLX Q8)** | **~7 GB** | **~10 GB** | **70 to 85 tok/s** | **78.2% HumanEval** | **Ultra-Fast AST & Lint Parser:** Formatting, docstring generation, syntax validation. |
| **Codestral 22B (MLX Q4)** | **~13 GB** | **~19 GB** | **24 to 28 tok/s** | **81.1% HumanEval** | **Alternative Multilingual Worker:** Strong Python/TS/Bash cross-language refactoring. |
| **DeepSeek-Coder-V2-Lite (16B MoE, 2.4B active)** | **~9 GB** | **~13 GB** | **55 to 65 tok/s** | **83.1% HumanEval** | **Low-Latency MoE Worker:** Rapid code synthesis with minimal memory pressure. |

- **Recommendation:** **Qwen 2.5 Coder 14B (MLX 4-bit)**. It runs at nearly 4x the speed of the 32B model, consumes only 14 GB total RAM, leaves 45 GB of free memory for system tasks, and easily solves routine code cleanups, test generation, and bug fixes.

---

## 4. Reconciling the Core Revenue Engine: GovCon Pipeline (`cmp1` / `govcon-corpus`)

All multi-agent engineering exists to accelerate the GovCon proposal engine ($8k to $10k/month revenue). The lean stack connects to GovCon without custom spaghetti code:

1. **RFP Solicitation Ingestion (Google Gemini 2.5 Flash Free Tier):**
   - 1M token context digests complete 250-page DoD/GSA solicitation packages (FAR/DFARS clauses, Sections C, L, and M) in a single pass for $0.00.
2. **Clause Shredding & Compliance Extraction (Local Qwen 2.5 Coder 14B):**
   - Runs locally on Apple Silicon to extract FAR/DFARS compliance matrices without leaking proprietary proposal strategies or past-performance data to external cloud APIs.
3. **Proposal Volume Generation (Claude Code Sonnet 3.7 / Opus 4.8):**
   - Reserved for drafting high-judgment Technical Approach (Section C) and Management volumes against the shredded compliance matrix.
4. **Deterministic Compliance Verification:**
   - Python static testing scripts (`pytest`) verify that every mandatory clause (e.g., DFARS 252.204-7012, NIST SP 800-171) is explicitly satisfied before proposal finalization.
