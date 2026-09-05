# INTENT-AGGREGATE — compact north star

**Canon entry:** [START.md](START.md) · **Parent:** [agent-sdlc#117](https://github.com/redtrades/agent-sdlc/issues/117)  
**Sources (cite, do not paste):** [20260831-current-intent-decisions.md](20260831-current-intent-decisions.md); `agent-configs` `6850fa3:knowledge/MIKE-INTENT-DEBRIEF-2026-08-28.md`; [20260903-estate-structure-decision.md](20260903-estate-structure-decision.md).

## Both goals (neither optional)

| Goal | Meaning |
| --- | --- |
| **AISDLC** | Solo-operator software delivery that survives agent death: Issues → verify → independent review → exact-head merge. Proof lives in `agent-sdlc`. |
| **GovCon** | Buyer-received federal deliverable E2E (fit/diagnostic → paid evidence-grounded packet per Decision 53 ladder). Aspiration ~$8–10k/mo profit; starters the client completes with private data. |

**Owner sequence (2026-09-03):** AISDLC proof first, then GovCon. AISDLC is **proof / forcing test**, not a product to sell. GovCon is the commercial deliverable.

## How to build

- **Vertical slices**, not platform-first. One thin end-to-end path before expanding surface.
- **Bounded autonomy** (decision 10): reversible internal work may proceed; consequential external / destructive / security / spend needs grants.
- **Independent review:** existing `govcon-reviewer-bot` App **and** different model family than the author (Goal B canary #119 / PR #120 done).
- **Composable adoption:** commodity OSS/services where they fit; build only differentiated contracts (decisions 17–18).
- **Experiments ≠ self-promotion** (11–14): isolated variants, held-out eval, governed promotion; candidates cannot rewrite canon.

## Estate roles (summary)

- Canon: this archive `00-start-here/`
- Operative policy: `agent-configs` → harness adapters
- Implementation: `agent-sdlc` · GovCon evidence plane: `govcon-corpus` (+ cmp private)
- Frozen evidence: `agent-platform`, `agent-mesh`, `agent-workspace`, `govcon-factory`

## Decision 53 (recorded; product exec parked)

Staged ladder: fit/diagnostic entry → paid evidence-grounded opportunity packet; proposal production later on demonstrated demand + client evidence. [#121](https://github.com/redtrades/agent-sdlc/issues/121) parked during doc-spiral stop.

## Stop conditions

Do not re-litigate intent via new issues. Execute written decisions. See [ANTI-PATTERNS.md](ANTI-PATTERNS.md) and [DONE-LEDGER.md](DONE-LEDGER.md).
