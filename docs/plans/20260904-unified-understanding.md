# UNIFIED UNDERSTANDING  -  Locked Stone

**Date:** 2026-09-04  
**Authority:** agent-knowledge-archive + agent-sdlc DONE-LEDGER + CURRENT-INTENT-DECISIONS  
**Purpose:** One immutable vision for Phase 1+ execution (all agents, user, this session)  
**Do not re-derive.** Execute written decisions.

---

## NORTH STAR (Non-Negotiable)

### Founding Directive (Mike, Apr 2026)
> "I want to have the agnostic, genetic harness and plug-in-play brain and body so that any model can be implemented into the baseline or any of the other agents... Think of composable modular architecture, but for agentic swarms."

### The Dual Engine

#### Engine 1: AISDLC (Agent-Integrated Software Delivery Lifecycle)
**What:** Prove that agents can produce reviewed, production-ready code with deterministic gates, independent human oversight, and bounded autonomy.

**Lifecycle (non-negotiable contract):**
```
Issue (Intent) 
  → Tier-based complexity inference
  → Bounded work item + plan
  → Isolated attempt (Git worktree)
  → Deterministic verification (tests, checks, AST)
  → Independent exact-candidate review (different model family)
  → Approval or bounded grant (human or explicit, never self)
  → Expected-head merge (exact commit binding)
  → Receipt + recovery evidence
```

**Acceptance proves:** stable work identity, atomic ownership, isolation, recovery without dupes, verification to exact inputs, reviewer independence, approval binding, fail-closed behavior, exact-head promotion, measured quality/cost/latency/reliability/risk/attention/reversibility.

**Status:** Symphony + Codex MVP-0 merged. Fusion/Paperclip bakeoff deferred.

#### Engine 2: GovCon Factory (Federal Contracting Automation)
**What:** Turn RFP solicitations into:
- Compliance matrices (automated FAR/DFARS extraction)
- Fit/diagnostic artifacts (evidence-grounded, zero invented facts)
- Paid opportunity packets (~$8-10K/mo aspiration)
- Client-completable starters (not turnkey proposals)

**Status:** Decision 53 Rung 1 delivered (Z-TECH 18F3334 end-to-end artifact).

### Sequence (Owner, 2026-09-03)
**AISDLC proof first → then GovCon production.** Vertical slices (thin E2E paths), not platform-first.

---

## ESTATE (Canonical Non-Negotiable Structure)

| Role | Repository | Status |
|---|---|---|
| **Canon decisions** | `agent-knowledge-archive/00-start-here/` | Frozen, evidence-only |
| **Operative policy** | `agent-configs` | LIVE (rules, hooks, AGENTS.md, skills) |
| **AISDLC trial** | `agent-sdlc` (Symphony + Codex) | LIVE (implementation) |
| **Runtime adapters** | `~/.agents`, `~/.claude`, `~/.codex`, `~/.hermes`, etc. | Generated, operative |
| **Historical evidence** | `agent-platform`, `agent-mesh`, `agent-workspace`, `govcon-factory` | Frozen (read-only, no new work) |
| **Deliverables** | `~/agent-reports/` | Not Git (output sink) |

### What This Means
- **Frozen repos are evidence, not instructions.** Never restart platform/mesh/workspace as the solution.
- **agent-configs is your operative system.** All rule changes, skill updates, AGENTS.md edits, hooks  -  operative.
- **agent-knowledge-archive records decisions once.** Don't re-litigate; execute.
- **agent-sdlc is the trial space.** Compose, verify, promote from here.

---

## DEATH SPIRAL ANTI-PATTERNS (Do Not Repeat)

1. **Recursive meta-work**  -  rules about rules about repos with no product goal
2. **Re-deciding intent**  -  new issues instead of executing written decisions (Decisions 1-58 exist; stop inventing)
3. **No single SoT**  -  each session reads different START/AGENTS subsets
4. **Briefing against demoted trees**  -  treating frozen platform/mesh as governing
5. **Routing delivery into unmaintained repos**  -  live board starves while work goes elsewhere
6. **Unbounded concurrent writers**  -  no WIP cap on governing files; parallel conflicting edits
7. **"While I'm here" scope creep**  -  no stopping condition or acceptance test
8. **Meta-work without acceptance**  -  consolidation/planning/research never ends
9. **Generator ≈ Judge**  -  same model family reviewing own work defeats independence
10. **Filing diagnoses instead of fixing**  -  RCA/handoff/path-forward documents instead of merging the board item
11. **Worktree/branch sprawl**  -  inventing parallel layouts (*-wt, *-worktrees)
12. **Mass-delete ~/.agents or rewrite skills**  -  as a "fix" for spiral symptoms
13. **Recreate Apps/PATs**  -  instead of wiring existing `govcon-reviewer-bot`
14. **Treating PLAN-V\* as live**  -  frozen SOPs as if they govern after estate freeze
15. **Marathon sessions**  -  drift accumulation without 5-line handoff + hard stop

**Kill these immediately if observed. They indicate control-plane failure, not technical complexity.**

---

## GOVERNANCE DECISIONS (Decision ID System)

### Decision 10: Bounded Autonomy
- Reversible internal work → autonomous
- Consequential / destructive / security / spending → requires grant or approval

### Decisions 43-52: Experiment Portfolio
- Isolated variants, fixed/held-out eval, independent selection
- Candidate cannot rewrite canon, alter policy, or promote itself
- Promotion evidence is risk-tiered: fixed tests → baseline improvement → no regression → independent-model review
- Agents may admit bounded low-risk experiments within owner-set caps

### Decision 53: GovCon Staged Ladder (Reopened)
- Fit/diagnostic entry → paid evidence-grounded packet → proposals later (not now)
- Durable principles survive: buyer-actionable deliverables, no invented facts, traceable evidence, human review
- Trading/market research parked

### Decision 58: AISDLC First Implementation (Ratified 2026-09-03)
- **Symphony + Codex MVP-0** (per agent-sdlc `docs/adr/0001-symphony-codex-mvp.md`)
- Fusion / Paperclip bakeoff deferred until working issue-to-merge loop exists
- Neutral lifecycle contract + acceptance suite still bind whatever control plane is used

### Merge Authority (2026-09-03): Risk-Adaptive, Not Path-Based

**Class A (agent may merge):** on green checks + independent different-model review
- Documentation, evidence, reports, run artifacts
- Code that passes checks + review
- Low-risk governing: additive prose transcribing owner directive, extraction, dups, reverts, typos, new judgment rules

**Class B (owner merges):**
- Enforced mechanisms (merge authority itself, permission posture, allow/deny lists, hooks, gates, checks)
- New/altered standing constraints not direct transcription of owner directive
- Security/trust/credentials/schema/data-loss guards
- Structural changes to master guide or lifecycle
- **Unsure → escalate to Class B**

**Conditions:** PR body names class + reason. Cross-family reviewer confirms class call. Revertable in one commit. One-line evidence record.

---

## WHAT'S DONE (as of 2026-09-04)

### AISDLC MVP-0/1/5
- ✅ Symphony + Codex bootstrap (merged)
- ✅ MVP lifecycle docs (#82, #80)
- ✅ Graphify discovery spike (#128, PR #166 merged)
- ✅ GovCon Decision 53 Rung 1 (#121, Z-TECH 18F3334 end-to-end artifact)
- ✅ Continuity canary (#108, PR #179 merged)
- ✅ Quota reconciliation (#109, PR #248 merged)
- ✅ Control plane dashboard + CLI (#160, port 4200)
- ✅ Cold-start path verified for all 7 harnesses

### Infrastructure
- ✅ Fusion engine running natively (port 4040) with runtime plugins
- ✅ FreeLLMAPI gateway (port 3100) routing free-tier models
- ✅ Estate frozen: agent-platform/mesh/workspace archived on GitHub
- ✅ Worktrees: ~250 → 9 (consolidated)
- ✅ Tests: 185 Node unit + 44 pytest tests passing

### Authority & Rules
- ✅ BOOTSTRAP_SHA tracking (f2b24a4+)
- ✅ 7 harness adapter files (regenerated 2026-09-04)
- ✅ AGENTS.md cold-start 8-item read list (all targets exist)

---

## OWNER-ONLY REMAINDER (Pending)

1. Merge PR #155 (Symphony as LaunchAgent persistence)
2. Install/load LaunchAgent (Keychain tokens needed)
3. Re-review control surface + bump BOOTSTRAP_SHA (if needed)
4. Quiet idle peer sessions on shared redtrades login
5. Deploy D-007 hook
6. Setup govcon-corpus remote
7. Archive default-branch rename

---

## WHAT PHASE 1 ACTUALLY IS

### NOT:
- Generic agent orchestration framework
- Dashboard/UI build
- Wholesale Fusion/OpenHands adoption
- Brute-force retry loops
- New orchestration layer on top of Symphony

### IS:
**Evidence-grounded decision infrastructure embedded into AISDLC contract itself.**

#### Four Critical Hooks (prevent death spirals)
1. **Tier detection**  -  auto-infer request complexity (Quick/MVP/Standard/Audit) → gate features/models
2. **WIP cap enforcement**  -  max 3 concurrent per tier, reject 4th → prevent unbounded concurrency
3. **Credential validation**  -  detect missing tokens (GITHUB_TOKEN, OPENROUTER_API_KEY, etc.) → fail-closed vs silent
4. **Terminal state tracking**  -  explicit "done" conditions per phase → prevent re-seeding loops

#### Extended AISDLC Schema (from consolidated findings)
- **Governance fields:** outcome (DENY/AUTO_READ/AUTO_WRITE/APPROVAL_DESTRUCTIVE), reviewer_principal, promotion_principal, exact_commit_binding
- **WIP fields:** wip_slot, failure_count, max_failures_before_halt
- **Credential fields:** required_credentials[], credentials_validated
- **Terminal state:** IN_PROGRESS/WAITING_REVIEW/WAITING_MERGE/DONE/BLOCKED + blocked_reason
- **Free-tier routing:** can_use_free_models, free_tier_provider_preference[], fallback_to_paid
- **Evidence:** tests_required, review_type, evidence_ledger, portable_evidence_receipts[]

#### 20 Unified Rule Files (from archive extraction)
**From agent-platform (9 files, extracted):**
1. operating-model-principles.md
2. autonomy-dial.md
3. dispatch-protocol.md
4. recovery-from-failures.md
5. review-protocol.md
6. ci-gates.md
7. commit-identity.md
8. credential-isolation.md
9. control-plane-patterns.md

**From knowledge archive (11 new files):**
10. anti-patterns-unified.md (10 patterns + controls)
11. rca-insights.md (5 RCA insights)
12. wip-cap-enforcement.md (mechanical max 3 concurrent)
13. credential-gap-detection.md (auto-fail on missing tokens)
14. terminal-state-definitions.md (explicit per-phase done conditions)
15. failure-counter-halt-logic.md (don't re-seed forever)
16. principal-separation-enforcement.md (distinct reviewer, promoter, implementer)
17. portable-evidence-receipts.md (JSON, no paths)
18. free-tier-routing.md (provider priority: FreeLLMAPI → Groq → omlx → Nous → paid)
19. lessons-from-failures.md (why each RCA happened, prevention)
20. governance-framework.md (unified decision-making authority)

---

## EXECUTION READINESS CHECKLIST

**All source materials audited:** ✅  
**All findings consolidated:** ✅  
**All rule files extracted:** ✅  
**AISDLC schema designed:** ✅  
**Timeline established:** ✅  
**Success criteria clear:** ✅  
**One immutable vision locked:** ✅  

---

## NEXT SESSION: PHASE 1 EXECUTION

**Start:** Immediately (no more research, no more planning meetings)

**Step 1:** Create 20 unified rule files in parallel (agent-configs/rules/)  
**Step 2:** Extend AISDLC schema (src/aisdlc.ts + schemas/)  
**Step 3:** Implement tier detection hook (auto-label issues)  
**Step 4:** Wire free-tier routing (check APIs, fallback chain)  
**Step 5:** Prepare Fusion + OpenHands integration stubs  
**Step 6:** Clean up dangling folders (quick wins: 50+ IDE configs, backups, caches)  
**Step 7:** Consolidate documentation (AGENTS.md, rules/INDEX.md)  
**Step 8:** Verification testing (6 core tests: tier/free-tier/WIP/cred/terminal/principal)  
**Step 9:** Document completion + Phase 4 kickoff  

**Timeline:** 3 days (parallel work, verified tests)  
**Owner approval gate:** None (already approved Decision 58 + estate structure)  
**Deliverable:** Phase 1 complete: all 20 rules + extended schema + 4 hooks + dangling cleanup + full test suite passing

---

**Status:** READY FOR EXECUTION  
**Blockers:** None  
**Clarity:** 100%  

All agents read this once before starting. No re-researching. No re-deciding. Execute.
