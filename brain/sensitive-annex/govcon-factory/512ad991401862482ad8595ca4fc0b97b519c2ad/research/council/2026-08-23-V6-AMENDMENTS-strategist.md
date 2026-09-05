# Proposed amendments to PLAN-V6 — strategist seat

**Status: PROPOSALS. Nothing here has been applied.** `sop/PLAN-V6.md` is on `origin/main` and is the live plan. No agent should edit it without Mike's word.

**Author:** IdeaPlans (claude-opus-5) · 2026-08-23 · branch `council/2026-08-23-research`
**Why this file exists:** my amendment list was living in Buzz messages. A thread is not documentation, and "the strategist recommended X" is only actionable if X is somewhere a cold session can open. Same defect the copy seat fixed in `2026-08-23-copy-review-write.md` §7.

Ordered by consequence-if-ignored, not by size.

## Strategist seat — the four files, and what is in which

| File | What it is |
|---|---|
| `2026-08-23-V6-AMENDMENTS-strategist.md` | **Start here.** Six proposed V6 amendments, ordered by consequence-if-ignored, with `file:line` evidence |
| `2026-08-23-strategist-claude-opus-5.md` | The seat brief. Bannered — it amends V5, which `origin/main` superseded with V6 |
| `2026-08-23-strategist-appendix-claude-opus-5.md` | Economics (three break-even floors), test power, release capacity, the failure classes, my correction log |
| `2026-08-23-market-scan-claude-opus-5.md` | Live competitor pages, retrieved 2026-08-23 |

**Other seats' primary sources this seat cites** — cite the file, not the seat:

| For | Open |
|---|---|
| Receipts, window distributions, the funnel, the 23% packet, extraction economics, the `skills/` sweep | `2026-08-23-runtime-receipts-research.md` |
| Willingness-to-pay bands, APEX, the unprecedented-purchase finding | `2026-08-23-willingness-to-pay-research.md` |
| Copy defects, failure classes, §7 the V6 §1 replacement sentence, §8 source index | `2026-08-23-copy-review-write.md` |
| Skeptic seat — **the 81-line working-tree version is canonical, not the 115-line remote** | `2026-08-23-skeptic-grok-4.6.md` |
| GTM seat | `2026-08-23-gtm-gpt-5.6-sol.md` |
| Factory seat | `2026-08-23-factory-gpt-5.6-codex.md` |

---

## 1. `sop/PLAYBOOK.md` line 3 still reads "Companion to `sop/PLAN-V5.md`", and V6 has no companion playbook

**Why first.** V6 §2 adds a quality floor (Covered+Partial < ~50% → no $699 pitch). Whether it can fire depends on which pipeline an agent follows:

- `sop/PLAYBOOK.md` Loop 1 step 4 writes `requirements.json` **during ingest**, before Make/Route — gate computable.
- `skills/` puts extraction at Production step 2, downstream of `order-intake` ("turn a sale into a buildable order") — gate uncomputable.

**V6 names no winner, and the pipeline that makes its own gate work is pinned to the superseded plan.** So an agent reading V6 and asking *how does the swarm run* is sent to V5's companion or to `skills/`. If it lands on `skills/`, the gate does not error — **it silently does not run and the thin-map packet ships with the price in it, which is the failure the gate was added to prevent.**

**Fix:** one line in V6 naming PLAYBOOK as its companion; one line in PLAYBOOK pointing at V6. Found by grok; sharpened by Write. My original framing ("the gate is uncomputable") was wrong and is withdrawn.

## 2. `skills/` still implements V3 — file a BOARD task

`skills/order-intake/SKILL.md:8-33` is Production step 1 of 5 and demands confirmed `[CLIENT PROVIDES]` items at **$450/$750**; `skills/deliverable-draft/SKILL.md:17` consumes them as a required drafting input; `outcome-track` records against PLAN-V3 gates; `notice-triage:34` still says *"sell as normal"* under a policy Mike has since set; five skills carry Market Snapshot as live scope.

**An agent handed V6 today will block on customer intake and quote $450.** V6 §2 says customer input is not required to start. No counterpart on main, purely mechanical, needs no counsel ruling and no measurement. **Blocking pair: `order-intake` and `deliverable-draft`.**

## 3. V6 §1's competitor sentence is false

Carried verbatim from V5: *"Comparable is not HigherGov (a login) and not a four-figure consultant."*

Procurement Sciences acquired HigherGov (May 2026); its Proposal Generator drafts Sources Sought from a firm's linked Federal Profile, entry plan ~$500/yr. **Drafted replacement with every claim's basis and limit tabled: `2026-08-23-copy-review-write.md` §7.1.** Two cautions carried in it: the ~$500 tier and the generator are documented on separate pages and must not be bundled; the Virginia/Arizona waits are two accelerators of ~90 and are not a national claim.

## 4. Gate 0 should not block a supervised fill-rate packet

V6 §8 puts counsel (TASK-0019), benefits (TASK-0020), matcher gold-set (TASK-0018) and the kill-test (TASK-0002) in front of TASK-0017. **A supervised packet built to measure fill rate and release minutes is not a commercial send.** It needs no counsel ruling, no key and no spend, and it is the one measurement every seat independently reached. Found by grok.

## 5. `sop/DATA.md` S1 — ingest is keyless and free

V6 §6 is **byte-identical to V5 §6** (a section nobody opened) and still lists *"govconapi Pro or SAM free"*. The SAM bulk extract returns 82,921 notices with full `Description` text, refreshed daily, **no credential**; ~56K tokens/day to read every new Sources Sought federal-wide. Receipts: `2026-08-23-runtime-receipts-research.md`.

**Also for DATA.md S1:** dedupe on `Sol#`, not `NoticeId` — 1,029 open rows carry 847 unique solicitations, one appearing fifteen times. Cache value = latest-posted row; a new row for a known `Sol#` is a cache-invalidation event, not a duplicate.

## 6. Two internal contradictions in V6

- **§7 prices a consultant feed at $249/mo; §8 says "do not invent a third paid SKU."** Same file, two sections edited at different times. Strike the line or state the exception. (grok)
- **§7's "No Core subscription line until that product is defined"** is a conditional that becomes permission the moment anyone drafts a definition. Rewrite as an invariant. (Write)

---

## Evidence V6 does not have, and does not contradict

Recorded so an amender can use it without re-deriving it. Sources: `2026-08-23-runtime-receipts-research.md`, `2026-08-23-willingness-to-pay-research.md`, `2026-08-23-market-scan-claude-opus-5.md`.

- **Deadline compression, the product's core claim.** Use **days remaining**, not the window at posting: median **8**, **p25 = 3**, n=1,029 open. A quarter of open Sources Sought have three days or fewer. Against published new-client waits of 3-4 weeks (Arizona) and 30-60 days (Virginia) — those two accelerators only. **Every window figure must carry its population**: 11 (all, at posting, n=4,950) · 16 (open only, at posting, n=919) · 8 (open only, remaining). ±5 days apart.
- **Willingness to pay exists and $699 is premium-edge, not middle:** $85-300 marketplace, $300-800 consultant, $395 clearest buy-now comparable.
- **No purchase found anywhere precedes the buyer's decision to bid.** V6 §4's second on-ramp still sells before it. The thesis is unprecedented rather than disproven, and the 30-day test is its first measurement.
- **Notice inventory is not the constraint:** ~60-68 qualifying solicitations post per week, ~23 VA; 96 currently open clear every notice-side gate, 27 of them VA. V6's "6-8 notices" has roughly nine-fold headroom. The unmeasured term is strict list-3 yield, which TASK-0018's gold-set is the right place to measure.
- **The one live packet scored 1 Covered / 2 Partial / 9 Gaps = 23%**, which V6's ~50% floor correctly refuses. V6 chose that threshold without this measurement and the measurement supports it. Add one anti-gaming clause: at least one meaningful Covered row, and every Partial must name its exact missing element — a percentage floor is otherwise passable by inflating Partial.

## Standing dissent (grok, SKEPTIC seat)

Against the prebuild design V6 retains: teasers naming one real PIID, full draft on interest or payment — not unpaid full drafts across a batch. Recorded as a minority position, not resolved.
