# Estate intent vs drift inventory (compact)

**Date:** 2026-09-03 (America/New_York)  
**Promoted from:** CoS box scratch + [agent-sdlc#117](https://github.com/redtrades/agent-sdlc/issues/117)  
**Canon pointer:** [00-start-here/START.md](../../00-start-here/START.md)

---

## North star (both goals)

**(A)** GovCon buyer-actionable federal deliverables (~$8–10k/mo) · **(B)** AISDLC Issues → verify → independent review → exact-head merge.  
**Sequence:** AISDLC proof first, then GovCon. Vertical slices, not platform-first. Active: **archive + agent-configs + agent-sdlc**. Frozen: platform, mesh, workspace, govcon-factory. Decision **53** deferred. Independent review = `govcon-reviewer-bot` App **and** different model family than author.

---

## Top 10 conflicts

| # | Conflict |
| --- | --- |
| 1 | Fusion (decision 58) vs Symphony+Codex (estate / ADR 0001) — bakeoff deferred |
| 2 | `agent-platform` freeze banner vs body still "canonical" |
| 3 | `govcon-factory` never freeze-bannered; PLAN-V5 still live-looking vs decision 53 |
| 4 | Decision 53 reopens wedge; factory/debrief still treat V5 / $699 as settled |
| 5 | Local archive checkout drift (stale branch missing estate-structure) |
| 6 | Two reboots: platform Aug-29 vs archive Aug-31 — both readable as authority |
| 7 | Intent re-litigated as issues (`#97` class) despite written canon |
| 8 | Competing overall plans (`OVERALL-INTENT-…-2026-09-02`) vs approved estate structure |
| 9 | GovCon code home: `govcon-corpus` vs factory SOPs vs CMP private plane |
| 10 | Meta path-forward vs RCA: ship product, not another diagnosis |

---

## Canonical ≤8 (cold-start)

1. archive `20260903-estate-structure-decision.md`
2. archive `20260831-current-intent-decisions.md`
3. `WHOLE-STORY.md` + `READING-PATHS.md`
4. `agent-sdlc` ADR 0001 + `AGENTS.md`
5. `agent-configs` AGENTS.md + merge-authority
6. MIKE-INTENT-DEBRIEF (configs git `6850fa3`)
7. death-spiral RCA 2026-09-03
8. GovCon: `govcon-corpus` CANONICAL MVP + decision 53 caveat — **not** PLAN-V5

**Historic / DO NOT cold-start:** platform START-HERE, mesh/workspace, factory PLAN-V* as product authority, subject packs beyond escalation, Fusion bakeoff as active plan.

---

## Done / not-done (summary)

- **AISDLC:** partial (budget/failover/docs/canaries) · **missing** owner-forcing full autonomous issue→merge · related open: #114 #115 #108 #3 #17
- **GovCon:** code/corpus exist · **missing** decision 53 choice (deferred) + one buyer-received deliverable · factory freeze gap

Full checkboxes: [DONE-LEDGER.md](../../00-start-here/DONE-LEDGER.md).

---

## Anti-patterns (≤8)

1. Recursive meta-work with no product goal  
2. Re-deciding intent via new issues  
3. No single SoT across AGENTS files  
4. Routing to frozen / demoted repos  
5. Unbounded writers on governing files  
6. "While I'm here" scope creep  
7. Same-family / generator≈judge review  
8. Another diagnosis instead of board finish  

---

## Authority map

```
canon:     agent-knowledge-archive/00-start-here/
policy:    agent-configs  →  generated ~/.agents ~/.claude ~/.codex ~/.hermes
implement: agent-sdlc (AISDLC) | govcon-corpus (+ cmp private) for GovCon slice
frozen:    agent-platform, agent-mesh, agent-workspace, govcon-factory
reports:   ~/agent-reports/
```

**Do not:** mass-delete `~/.agents`, rewrite all skills, recreate Apps before wiring existing `govcon-reviewer-bot`.
