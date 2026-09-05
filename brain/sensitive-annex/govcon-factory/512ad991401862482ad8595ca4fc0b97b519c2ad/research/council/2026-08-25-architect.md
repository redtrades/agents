To provide a rigorous architectural analysis for the `govcon-factory` pipeline, I have reviewed the core execution logic in `factory/runner.py`, the data contract in `factory/envelope.py`, the gate implementation in `factory/gates/registry.py`, and the SAM.gov integration in `factory/stages/normalize.py` and `factory/stages/extract_attachments.py`.

The following report analyzes the "SSSF" (Synchronous Stage-Specific Fail-closed) framework and proposes improvements to transition from a prototype to a production-grade factory.

### 1. Diagnosis: Structural Weaknesses in SSSF

The current architecture is a robust "V0" that enforces high-trust data handling, but it contains several bottlenecks and coupling risks:

*   **Synchronous I/O Blocking:** Both `normalize` (SAM v2 cross-check) and `extract_attachments` (PDF fetching/extraction) execute API calls and CPU-bound text extraction in a serial loop. A pipeline run with 40 notices and 3 attachments each results in ~160 sequential network/CPU operations, causing massive latency.
*   **Tight Context Coupling:** Stages access prior data via `ctx.prior`, which contains full envelope dictionaries. This requires stages to manually "dig" into `prior["stage_name"]["outputs"]` to find paths. This creates a hard dependency on upstream naming conventions.
*   **SQLite Trace Contention:** While SQLite with WAL is efficient, the `runner.py` commits to the DB after every gate check and envelope creation. This is fine for single runs but will block concurrent pipeline executions (e.g., multi-notice parallel swarms).
*   **Envelope Rigidity:** The `envelope.py` schema is excellent for auditability but lacks a standard way to signal "partial success" or "item-level failure" within a batch. If 1 of 40 notices fails cross-check, the entire stage (and thus the pipeline) fails closed.
*   **Single-Threaded Extraction:** Attachment extraction (`factory/attachments.py`) is a heavy CPU task. Running this in the main thread blocks the runner from managing any other tasks.

---

### 2. Proposals: Architectural Evolution

#### P0: Parallelized Item Processing (The "Batch" Pattern)
**Target:** `factory/stages/normalize.py`, `factory/stages/extract_attachments.py`
Move away from serial loops. Implement `ThreadPoolExecutor` (for I/O-bound SAM API calls) and `ProcessPoolExecutor` (for CPU-bound PDF extraction).
*   **Proposed Path:** Create `factory/batch.py` to provide a standard `map_fail_closed` helper that handles parallel execution and aggregates results into a single envelope.

#### P1: Transition to Async-Native Runner
**Target:** `factory/runner.py`
Refactor the runner to be `asyncio` native. This allows the runner to manage "Watchers" (stages waiting on human approval) or "Listeners" (stages waiting on slow I/O) without blocking the entire OS process.
*   **Benefit:** Enables `TASK-0018` and `TASK-0015` (Human Gates) to exist as "pending" states in the DB rather than blocked terminal processes.

#### P1: Decoupled Gate Registry (Multi-Domain Support)
**Target:** `factory/gates/registry.py`
Currently, all gates (including domain-specific `compliance` and `value` gates) live in one file.
*   **Proposed Path:** Move domain-specific gates to `domains/<domain>/gates.py`. Refactor `run_gates` to accept a list of gate provider functions.

#### P2: Envelope Metadata & Payload Hints
**Target:** `factory/envelope.py`
Add an optional `payload_hints` key to the envelope `outputs`.
*   **Improvement:** Instead of stages searching for `selected_notice.json`, the upstream stage can flag `"primary_payload": "match/selected_notice.json"`. This reduces the "path-digging" logic in `_find_output`.

---

### 3. Prioritization & Impact

| Priority | Improvement | Impact | Effort |
| :--- | :--- | :--- | :--- |
| **P0** | **Parallel I/O & Extraction** | Reduce pipeline latency by 70-80% (O(N) -> O(1) for network). | Med |
| **P0** | **SAM v2 API Batching** | Critical for `normalize` stage stability at scale. | Low |
| **P1** | **Async Runner Refactor** | Necessary for human-in-the-loop (Mike review) scalability. | High |
| **P1** | **Domain-Specific Gate Separation** | Enables multi-domain expansion (beyond GovCon). | Med |
| **P2** | **Stage Retry Logic** | Resilience against transient SAM.gov 429/503 errors. | Low |

---

### 4. Risks & Dependencies

1.  **SAM.gov Rate Limits:** Moving to parallel API calls increases the risk of `429 Too Many Requests`. The `get_resilient_session` in `factory/util.py` must be enhanced with a global (per-run) rate-limiter or a more aggressive backoff strategy.
2.  **SQLite Locking:** Parallel runs will increase DB write contention. If moving to an async runner, `aiosqlite` is required to prevent blocking the event loop.
3.  **Memory Pressure:** Loading 40+ large PDF text blobs in parallel could spike memory usage. Stages should stream text to disk immediately after extraction rather than holding them all in the `envelope` dict.

---

### Concrete Architectural Changes (Repo Paths)

1.  **Modify `factory/runner.py`:** Wrap the stage loop in an `async` function and use `aiosqlite` for tracing.
2.  **Patch `factory/stages/normalize.py`:** Replace `for row in reader:` with a `ThreadPoolExecutor` for the `_fetch_sam_v2_notice` calls.
3.  **Patch `factory/stages/extract_attachments.py`:** Move extraction to a `ProcessPoolExecutor` to avoid GIL bottlenecks on PDF parsing.
4.  **Create `factory/gates/govcon.py`:** Move `gate_compliance`, `gate_format`, and `gate_value` out of the generic registry to prepare for `TASK-0022`.

The research file has been written to `research/council/2026-08-25-architect.md`.

---
**Summary of Work:**
- Analyzed `factory/` core and stages for bottlenecks.
- Diagnosed synchronous I/O and tight coupling as primary scalability risks.
- Proposed parallel processing, async runner transition, and domain-gate decoupling.
- Created `research/council/2026-08-25-architect.md` with detailed diagnosis and improvement paths.