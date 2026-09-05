# KEY-DOCS — estate north star / control plane

**Date:** 2026-09-03 ET · **Board:** [agent-sdlc#117](https://github.com/redtrades/agent-sdlc/issues/117)  
**Ingest:** Doc Bot harvest + Codex `/Users/man/agent-reports/codex-north-star-docs-2026-09-04/KEY-DOCS.md`.  
**Rule:** museum/frozen = **EVIDENCE** only.

## Cold-start ≤8

1. `/Users/man/agent-knowledge-archive/00-start-here/START.md` — **CANON** door
2. `…/EVIDENCE-MODE.md` + `BRIEFING-CONTRACT.md` — **CANON**
3. `…/20260903-estate-structure-decision.md` — **CANON**
4. `…/INTENT-AGGREGATE.md` → `20260831-current-intent-decisions.md` — **CANON** (7,10,53,58)
5. `…/ANTI-PATTERNS.md` (+ `WHOLE-STORY.md`) — **CANON**
6. `/Users/man/agent-sdlc/docs/adr/0001-symphony-codex-mvp.md` + `/Users/man/agent-sdlc/AGENTS.md` — **CANON**
7. `/Users/man/agent-configs/AGENTS.md` + `rules/merge-authority.md` (+ `review-independence.md`) — **CANON**
8. MIKE-INTENT via `git -C /Users/man/agent-configs show 6850fa3:knowledge/MIKE-INTENT-DEBRIEF-2026-08-28.md` (**MISSING on disk**) → RCA → `DONE-LEDGER.md`

After: `cross-harness-agent-launch.md` + `govcon-reviewer-bot.md`. See `KEYWORDS.md`, `WORKSTREAMS.md`.

## KEY paths

| Path | Purpose | Tag |
|---|---|---|
| `…/START.md` | Cold-start SoT | CANON |
| `…/EVIDENCE-MODE.md` / `BRIEFING-CONTRACT.md` | Anti-poison | CANON |
| `…/ESTATE-STRUCTURE-DECISION-…` | Live vs museum | CANON |
| `…/INTENT-AGGREGATE` / `CURRENT-INTENT-…` | Decisions | CANON |
| `…/ANTI-PATTERNS` / `WHOLE-STORY` | Stop conditions | CANON |
| `…/DONE-LEDGER.md` | Done/not-done (lag) | CANON |
| `…/HISTORIC-INDEX` / `REPORTS-SINK` | Index / dumps | CANON |
| `…/MERGE-AUTHORITY-DECISION-…` | Class A/B | CANON |
| `/Users/man/agent-configs/rules/merge-authority.md` | Operative merge | CANON |
| `/Users/man/agent-configs/rules/review-independence.md` | Different-family | CANON |
| `/Users/man/agent-configs/AGENTS.md` | Policy → START | CANON |
| `~/.agents` / `~/.codex` AGENTS | Adapters | CANON |
| `/Users/man/agent-sdlc/AGENTS.md` + ADR 0001 | Impl | CANON |
| `…/runbooks/govcon-reviewer-bot.md` | App review | CANON |
| `…/runbooks/cross-harness-agent-launch.md` | Harness launch | CANON |
| git `6850fa3:knowledge/MIKE-INTENT-DEBRIEF-…` | Owner voice | CANON restore |
| `~/agent-reports/death-spiral-rca-2026-09-03/RCA.md` | RCA | EVIDENCE |
| `…/work/reports/estate-intent-inventory-…` | Inventory | EVIDENCE |
| `agent-platform/docs/START-HERE.md` | Museum poison | EVIDENCE |
| mesh/workspace/factory AGENTS | Museum bodies | EVIDENCE |

## Gaps (5-layer)

| Layer | Gap |
|---|---|
| Router | Banner≠body on museum AGENTS/START-HERE |
| Queue | DONE-LEDGER lag; weak WIP cap |
| Authority | ADR 0001 review≠App+family; D-001 tiered vs risk-adaptive |
| Discovery | graphify not installed |
| Skills-once | MIKE-INTENT missing on disk |
