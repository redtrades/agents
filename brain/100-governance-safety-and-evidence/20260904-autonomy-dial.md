# Autonomy Dial & Deterministic Loop Scheduling

Source: agent-platform#AUTONOMOUS-LOOP.md

## Loop Architecture

The autonomous loop combines existing deterministic components into a single restartable pass with a clock.

### Components (All Reused)

| Component | Status | Responsibility |
|-----------|--------|-----------------|
| `dispatch_eligibility.buildCandidates` | done, pure, tested | Pure translation from `gh issue list` to candidates |
| `dispatcher.dispatchOnce` | done, pure, tested | One bounded pass: order, gate, handoff |
| `github_contents_authority` (CAS) | adversarially tested | Claim/renew/complete + generation/fence |
| `gate_c` (claim→worktree→implementer→CI→review→promote→project→teardown) | proven once (#103/#110) | Complete delivery path |
| `run_dispatch.createGhIssueLister` | done | Live `gh issue list` |
| `run_dispatch.main()` | one-shot implemented | Entry point; proves live canary |
| `assemblePacket` | implemented | Per-issue packet assembly with bindings |

### Key Architectural Decisions

#### D1: Bounded Retry for Git Lock Races

**Anti-pattern** (Claude #55724, gascity #1181): `git worktree add/remove` and `git commit` across shared object stores hit `index.lock` / pack-lock contention.

**Rule**: Wrap Git operations in bounded retry in Gate C's git ops, not with a new tool.

#### D2: No Ambient Token in Worktree Environment

**Anti-pattern** (DFL-003): Agents work under broad credentials; changes escape intended authority.

**Rule**: Workers get `git` + worktree only. Never expose tokens with issue-mutate or merge scope in worker environment.

#### D3: Keep Expected-Head Promotion

**Anti-pattern** (DFL-009, AP-08): Candidate HEAD changes after review; promotion proceeds anyway.

**Rule**: Reviewer approval of SHA `S` promotes only if `HEAD == S`. Public SOTA is weaker; do not relax to match a framework.

#### D4: Shared-Host PAT Makes Independent Review Impossible

**Anti-pattern** (DFL-003, F3): One launcher credentials enable all workers; review cannot be independent.

**Rule**: Launcher holds claim credential. Workers never see issue-mutate tokens. Reviewer and Promoter are separate principals with separate credentials on the same host.

#### D5: Deterministic Teardown Order

**Anti-pattern** (Reapers #125): Cleanup order creates windows for orphaned state.

**Rule**: Release lease → remove worktree → ack checkpoint. Never reverse. Reapers read CAS lease, not PID or mtime.

#### F2: Bind Before Hydrating Worktree

**Anti-pattern** (AO #1034, Claude #60235): Worktree created first; resume dies.

**Rule**: `assemblePacket` pins `input_revision` to current `main` SHA and fixes attempt/branch/worktree names in the packet BEFORE Gate C hydrates the tree. This ensures resume can restart from the same state.

## One-Pass Loop Shape

```
run_dispatch.main(--config loop/config.json)
  ├─ createGhIssueLister → gh issue list (open + closed)
  ├─ buildCandidates → [{issue, ready, dependencies_met, priority}]
  ├─ read current control-state (which issues have live unexpired CAS claim)
  ├─ read open PRs (which issues have candidate PR)
  ├─ eligible = ready ∧ deps_met ∧ no live claim ∧ no open PR ∧ not epic
  ├─ order deterministically (priority, then issue number)
  ├─ capacity.evaluate (global / provider / harness / model concurrency)
  └─ for each admitted candidate, up to dispatch.max:
        assemblePacket(candidate) →
          ├─ input_revision = current origin/main SHA
          ├─ branch = agent/issue-<n>-<run_id>
          ├─ worktree = <worktree_root>/issue-<n>-<run_id>
          ├─ project.item_id = gh project item-list lookup
          └─ semantic packet with bindings
        runGateCConfig({control_state, receipt_path, packet})
          ├─ controller derives implementer_argv = opencode.py (immutable)
          ├─ controller derives exact child argv = opencode run ... --dir <worktree>
          ├─ controller derives reviewer_argv = codex.py (immutable)
          ├─ controller supplies scoped FreeLLMAPI capability
          └─ Gate C owns atomic claim, runs implementer, creates branch+PR
              → waits for exact-subject CI
              → routes reviewer (read-only)
              → only on PASS asks Promoter for expected-head merge
              → projects Done
              → tears down (lease → worktree → checkpoint)
```

## Scheduling & Cadence

### Cadence Mechanism

- **Tool**: `launchd` job `com.agent-platform.dispatch-loop` on self-hosted macOS runner
- **Interval**: `StartInterval 300s` (5-minute cadence)
- **Entry**: `node tools/controller/run_dispatch.mjs --config <abs path>`
- **Concurrency**: One pass at a time; `launchd` won't start second while one runs
- **Work bound**: `dispatch.max` bounds work per pass

**Why not GitHub schedule?** GitHub `schedule:` is unreliable at short intervals and not used for primary cadence.

### Restart & Interruption Handling

**Key Property**: The pass is stateless.

- A killed pass leaves at most one attempt mid-flight
- Next pass sees its live CAS claim (still fenced) and skips until lease expires or attempt completes
- Gate C's own resume path (`terminal checkpoint`, generation takeover) handles killed worker
- No loop state persisted outside CAS branch and per-attempt receipt

## Proof Gates (Issue #9 Completion Criteria)

All three gates must pass before autonomous loop is production-ready:

### Gate 1: Two-Contender Race (Live)

**Rule**: Two `run_dispatch` passes start within the same second against one ready issue.

**Expected Outcome**: Exactly one CAS claim wins; other pass skips with `already-leased`.

**Evidence**: Receipts retained for audit.

**Anti-pattern prevented** (DFL-010): Stale agent resume; two agents claim same work.

### Gate 2: Four-Worker Fixture (Live)

**Rule**: Four trivial seeded issues with `dispatch.max: 4` in one pass.

**Expected Outcome**: All four reach `state:done` with accepted candidate; zero duplicate ownership; zero lost state.

**Significance**: MASTER-PLAN Stage 1 completion.

**Anti-patterns prevented** (DFL-001, DFL-010): Unpushed work reported as delivered; lost state across parallel workers.

### Gate 3: Seeded Review Failure

**Rule**: One issue whose first candidate fails review.

**Expected Outcome**: Findings return to same attempt; later pass drains it after correction with no manual issue/PR movement.

**Anti-pattern prevented** (DFL-006): Review findings start new planning cycle instead of returning to same attempt.

## Code Bindings & Operator Capacity

### Controller is Deterministic Software

- Derives adapter paths from **immutable controller source**
- Never accepts worker-supplied adapter authority
- Current bindings:
  - **Implementer**: `tools/adapters/implementer/opencode.py` (OpenCode adapter)
  - **Reviewer**: `tools/adapters/reviewer/codex.py` (Codex adapter)
  - **Provider capability**: Opaque reference `secret://codex-provider`, resolved only for exact phase/attempt/input

### Parked Adapters (Available for Future Selection)

- `tools/adapters/implementer/hermes.py` with focused tests
- No Hermes executable, endpoint, model, readiness probe selected by `run_gate_c.mjs`

### Current Capacity Policy

**Policy**: External-provider dispatch is paused; root manually orchestrates separate Codex tasks.

**Non-evidence**: This policy neither makes Codex task authority nor proves other providers exhausted. Changing selected adapter is controller configuration/test change, not new queue/claim/promotion path.

## Non-Goals for This Phase

- Provider neutrality across ≥2 harnesses (Stage 2)
- Clean-host reconstruction (Stage 4)
- Product-factory slice (Stage 5)
- Full 20-task throughput measurement (Phase C)

**Scope**: This phase proves the loop **runs and is safe** on a small fixture (not full production throughput).

## State-of-the-Art Validation

Issue #181 surveyed primary sources: Paperclip, Beads/Gas Town, agent-orchestrator, Worktrunk, gh-aw, gh-issue-lease, safegit, Agency, OpenHands, Symphony, CMU CAID.

**Finding**: No maintained project supplies the missing operational layer. The star-heavy repos lose on:
- GitHub-as-mutex
- Reviewer-identity separation
- Promotion CAS (the exact primitives this repo already has)

**Build Decision**: Build, not adopt. Reuse three distinct GitHub Apps and `github_contents_authority.mjs` CAS proven in #59.
