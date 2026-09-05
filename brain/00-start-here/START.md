# START — cold-start canon

**Parent:** [redtrades/agent-sdlc#117](https://github.com/redtrades/agent-sdlc/issues/117)  
**Status:** active · 2026-09-03  
**Do not** re-derive intent from subject packs, frozen repos, or new "path forward" issues.

**Also required:** [EVIDENCE-MODE.md](EVIDENCE-MODE.md) (frozen = evidence only) · [BRIEFING-CONTRACT.md](BRIEFING-CONTRACT.md) (every brief opens here).

## North star (both goals)

1. **AISDLC** — Issues → verify → independent review → exact-head merge (`agent-sdlc`).
2. **GovCon** — one buyer-actionable federal deliverable E2E (~$8–10k/mo aspiration).

**Sequence (owner):** AISDLC proof first, then GovCon. Vertical slices, not platform-first.

**Goal B canary:** done — [#119](https://github.com/redtrades/agent-sdlc/issues/119) / [PR #120](https://github.com/redtrades/agent-sdlc/pull/120) (Codex author + Claude ship + `govcon-reviewer-bot` APPROVE).

**Decision 53:** staged ladder recorded (fit/diagnostic → paid evidence-grounded packet; proposals later). [#121](https://github.com/redtrades/agent-sdlc/issues/121) **parked** this pass (doc spiral only; no Symphony/Herdr; no GovCon product).

**Independent review:** `govcon-reviewer-bot` App **and** different model family than the author.

Compact north star: [INTENT-AGGREGATE.md](INTENT-AGGREGATE.md). Anti-patterns: [ANTI-PATTERNS.md](ANTI-PATTERNS.md).

## Live / museum map

| Layer | Where |
| --- | --- |
| **Live** | **Canon** this repo `00-start-here/` · **Policy** `agent-configs` → `~/.agents` / `~/.claude` / `~/.codex` / `~/.hermes` · **Impl** `agent-sdlc` (AISDLC) · `govcon-corpus` (+ cmp private) |
| **Museum (SAME-ATTEMPT family)** | `agent-platform` + `agent-mesh` + `agent-workspace` — sibling superseded skins of one attempt, **not** three roles |
| **Museum (other frozen)** | `govcon-factory` (harvest-only) |
| **Adjacent (not on either goal's critical path)** | `agent-x` (X-feed digests for agent consumption), `universal-record-engine` (URE V5 product). Own repos; do not fold into AISDLC/GovCon work or cold-start from them. |
| **Reports (historic dump)** | `~/agent-reports/` — [REPORTS-SINK.md](REPORTS-SINK.md) (not canon; not a git repo). No new dated folders (`agent-configs/rules/hygiene.md`). |

Index of roots: [HISTORIC-INDEX.md](HISTORIC-INDEX.md). Worktree piles: [CLEANUP-CANDIDATES.md](CLEANUP-CANDIDATES.md).

## Ordered read list (≤8)

1. [20260903-estate-structure-decision.md](20260903-estate-structure-decision.md)
2. [INTENT-AGGREGATE.md](INTENT-AGGREGATE.md) → [20260831-current-intent-decisions.md](20260831-current-intent-decisions.md) (esp. 7, 10, 53, 58)
3. [ANTI-PATTERNS.md](ANTI-PATTERNS.md) + [WHOLE-STORY.md](WHOLE-STORY.md) (short)
4. `agent-sdlc` `AGENTS.md` + ADR 0001 + **`docs/runbooks/cross-harness-agent-launch.md`** (how any harness — Codex, Claude, Hermes, OpenCode, OpenHands, Buzz, Grok/Antigravity CLI, Jules — runs the SDLC: one issue → one owner → isolated workspace → verify → different-family review → exact-head merge)
5. `agent-configs` `AGENTS.md` ("How to work" section) + merge-authority rule
6. MIKE-INTENT-DEBRIEF (`agent-configs` git `6850fa3:knowledge/MIKE-INTENT-DEBRIEF-2026-08-28.md` if missing on disk)
7. death-spiral RCA — [`110-failures-postmortems-and-lessons/selected-originals/20260903-death-spiral-rca.md`](../110-failures-postmortems-and-lessons/selected-originals/20260903-death-spiral-rca.md)
8. GovCon only: `govcon-corpus` CANONICAL MVP + Decision 53 ladder — **not** PLAN-V5

Then: [DONE-LEDGER.md](DONE-LEDGER.md). Inventory: [20260903-estate-intent-inventory.md](../work/reports/20260903-estate-intent-inventory.md).

## DO NOT cold-start here

- `agent-platform` (incl. `docs/START-HERE.md`) as governing instructions
- `agent-mesh` / `agent-workspace` (SAME-ATTEMPT siblings of platform), worktree sprawl (`*-wt`, `*-worktrees`)
- `govcon-factory` SOPs / PLAN-V* as **product authority**
- Archive subject packs / OpenClaw lineage beyond escalation
- `OVERALL-INTENT-…-2026-09-02.md`, death-loop diagnoses, mesh `HANDOFF.md`
- Fusion/Paperclip bakeoff as the active build plan
- Mass-delete `~/.agents`, rewrite all skills, or recreate Apps (wire existing `govcon-reviewer-bot`)

## Pointers

- Done vs not-done: [DONE-LEDGER.md](DONE-LEDGER.md)
- Historic roots → roles: [HISTORIC-INDEX.md](HISTORIC-INDEX.md)
- Reports dump sink: [REPORTS-SINK.md](REPORTS-SINK.md)
- Worktree index (no delete): [CLEANUP-CANDIDATES.md](CLEANUP-CANDIDATES.md)
- Board: [agent-sdlc#117](https://github.com/redtrades/agent-sdlc/issues/117)
