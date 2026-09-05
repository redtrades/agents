# Plan evolution review — how the plan got here, where it is still weak, what to cut

2026-08-23. Mandate: assess how the business plan evolved V2 → V3 → V4 → post-red-team, find where the current plan is weakest, and name what a sharper operator would cut. Evidence over opinion; every claim about the plan cites file:line. Complements `research/swarm-retrospective/REPORT.md` (process); this file is about the *decisions*. Findings that warrant action are filed as `proposals/PROPOSAL-0013..0017.md` (0012 is taken on `origin/main`).

**State of the record, first, because it is itself a finding.** This working tree (branch `council/2026-08-23-research`) carries PLAN-V5 as the operating plan (`AGENTS.md:3`, `CLAUDE.md:3`). `origin/main` carries **PLAN-V6**, accepted by Mike (commit `3451098`, "Accepts PROPOSAL-0012") — and even on main, `CLAUDE.md` still points at V5 and `sop/PLAYBOOK.md:3` still says "Companion to `sop/PLAN-V5.md`". A V7 draft exists on this branch (`research/council/2026-08-23-PLAN-V7-DRAFT-strategist.md`, explicitly not accepted). This report treats V5 as the in-tree current plan and V6 as the accepted plan, and flags where V6 already closes a gap so nothing below re-litigates settled ground.

---

## 1. The decision trace — what reversed, what it cost, what survived

Six plan generations in three days of calendar time: V2 (08-21, `sop/plan-history/PLAN-V2.md`), V3 (08-22), V4 (08-22), red-team revisions (08-22), V5 (08-23), V6 (08-23, origin/main), V7 draft (08-23, unaccepted). Zero customer contact across all of them (`BOARD.md:36-38` — Done: none; `sop/financial-model/SUMMARY-v5.md:30` — "None of these are measurements").

### 1.1 Pricing logic: outcome-ROI → time-substitution → per-decision → one $699 SKU

- **V2** found the original crux: the source plan priced a $5,000 subscription on a win-rate claim no document supported. The MECE pass showed all evidence pointed at coverage/time value, none at outcome value (`sop/plan-history/PLAN-V2.md:27,33`), and re-anchored $5,000 to time-substitution arithmetic (`PLAN-V2.md:68-76`).
- **V3** dropped the subscription entirely: "Buyers pay for coverage and time, never win-rate claims… a per-decision deliverables factory" (`sop/PLAN-V3.md:13`), with the $450/$750/$1,500 ladder (`PLAN-V3.md:17`) and the ~$1,000/founder-review-hour governing rule (`PLAN-V3.md:32`).
- **V5** collapsed the ladder to a single $699 packet plus free reports, explicitly retiring the two-SKU story (`sop/PLAN-V5.md:138-142`, `AGENTS.md:14`) and replacing the hourly rule with the 20-minute packet rule (`PLAN-V5.md:140`).

**Improvement? Yes, monotonically — in honesty, not in evidence.** Each step deleted a number nobody could defend: first the win-rate claim, then the subscription that depended on it, then the ladder whose repeat-purchase assumption was never measured. What triggered each step: V2's was internal logic (the gap statement, `PLAN-V2.md:13`); V3's was Mike's section-by-section review plus real notice data (`PLAN-V3.md:7`); V5's was Mike restating the business in his own words (`PLAN-V5.md:4-5`). Note what *never* triggered a pricing change: a customer. Prices remain "set, not validated" from the first ledger correction (`proposals/PROPOSAL-0009.md:17`, `sop/financial-model/SUMMARY.md:49`) through v5 (`SUMMARY-v5.md:30`).

### 1.2 Snapshot-first (V2) → deliverables factory (V3) → the packet (V5)

V2's most durable move was promoting the per-decision deliverable from lead magnet to primary revenue vehicle, *because it required no unproven number* (`PLAN-V2.md:52,78,98`). V3 made that the whole company (`PLAN-V3.md:13`). V5 then declared the V3 *packaging* — "$450 Sources Sought response and a $750 Market Snapshot" — to be "one agent generation's packaging of an older crux, not Mike's idea" (`PLAN-V5.md:13`) and merged both SKUs into the one packet.

**Verdict: the crux survived every rewrite; the packaging churned three times.** The churn was not free: 18 skill directories, five polished SS-response samples, four deliverable templates, and financial models v1–v3 were all built around SKUs that are now retired (`PLAN-V5.md:15-17`), and the cleanup is still open work (`BOARD.md:28` TASK-0019; `templates/outreach/email-1-opener.md:20` still sells "flat $450"). The lesson V5 itself drew — the repo taught later agents the wrong company (`PLAN-V5.md:9-19`) — is the correct diagnosis, and §2.2 below shows it recurred within hours of V6.

### 1.3 Universe re-derivation (red-team F1 → PROPOSAL-0001) — the model case

The repo simultaneously carried ~1,500, 4,000–8,000, and ~27–38K as the addressable universe, none derived (`research/feasibility-review/REPORT.md:32`). The red-team replaced the firm denominator with the one that actually binds a notice-tied product: **~250–400 viable Sources Sought moments/yr** across the 6 NAICS (`REPORT.md:36-38`), showed Optimistic Y2 exceeds that supply at 100% capture (`REPORT.md:39`), and the fix was applied with commits (`proposals/PROPOSAL-0001.md:41-43`) and propagated into v5 (`SUMMARY-v5.md:58`) and the council's ceiling judgment (`research/council/2026-08-23-SYNTHESIS.md:37`).

**Verdict: unambiguous improvement, and the process working as designed** — data the pipeline already had, an outside reviewer forcing the derivation, a proposal with a commit trail. This is the pattern the other reversals should be measured against. It also demoted the entire Optimistic scenario from "upside" to "requires leaving the pond" — a real strategic consequence, not a bookkeeping fix (`SUMMARY-v5.md:58`).

### 1.4 Wedge rewrite (red-team F3 → PROPOSAL-0003) — right correction, still unproven

The V3 wedge ("only finished document under $500") was falsified by external evidence: Sweetspot and SamSearch already shipped SS/RFI drafting (`research/feasibility-review/REPORT.md:61-65`). PROPOSAL-0003 restated the wedge as *verified + accountable + zero-effort* and expanded the kill-test to the AI-SaaS leg (`proposals/PROPOSAL-0003.md:17-18`, applied `PLAN-V3.md:28`).

**Verdict: improvement, but the corrected wedge is still a hypothesis, and the ground is still moving.** The 0002a recon found the repo's competitor facts stale again within days — SamSearch "$99/mo" is dead, HigherGov Starter is $500/yr *with* a generator, "they only sell search is false" (`research/kill-test/REPORT.md:22,19,25`) — and concluded the 30-second difference "is articulable… not proven" (`kill-test/REPORT.md:38-42`), with high pitch-kill risk on thin packets (`kill-test/REPORT.md:44-46`). Two structural takeaways: (a) the bake-off (0002b) is still the single cheapest unrun test in the repo; (b) competitor claims decay in days, and nothing gates stale claims out of customer-facing copy — `templates/outreach/objection-ai-saas.md:10-18` still says "$99/mo" and "submission-ready" today (→ PROPOSAL-0017).

### 1.5 Delegated review + outreach ramp + growth system (V4) — scaling before evidence

V4 replaced the founder-review ceiling with a delegation ladder (`sop/PLAN-V4.md:49-55`), ramped outreach 15→200/wk (`PLAN-V4.md:59-69`), and wrapped a multi-channel growth funnel around outbound (`PLAN-V4.md:22-45`). To its credit, V4 §0 firewalled all of it behind the kill-gates (`PLAN-V4.md:11`).

**Verdict: mostly scope that a session produced, not scope the business needed.** The tell is what V5 kept: nothing. No delegation ladder, no 50→200/wk table, no digest→mini-snapshot funnel with working targets — V5's steady state is Mike at ~5 hrs/wk and "someone else takes first pass" appears only as an Optimistic-scenario note (`SUMMARY-v5.md:46`). The second feasibility pass said it directly: "V4 is a scaling document written before a single email left the building… The business is over-specified and under-validated. That is the governing fact" (`research/feasibility-final/REPORT.md:11-13`). What V4 contributed that survived: the repo-is-the-company governance (`PLAN-V4.md:15-18` → `AGENTS.md:62-68`), the kill-gate supremacy clause (`PLAN-V4.md:11`), and the earned-autonomy principle (`PLAN-V4.md:74` → `PLAN-V5.md:111` "Send is the last thing that goes autonomous"). Those were worth one page, not a plan version. The growth system's useful residue is MARKETING.md's doors — reframed as doors into one funnel with the discipline "change the packet, not the number of channels" (`sop/MARKETING.md:162`).

One clean reversal inside this cluster: V4 §5 said local models run extraction (`PLAN-V4.md:73`); the live eval falsified it and V5 retired it explicitly (`PLAN-V5.md:113`). Evidence-triggered, cheap, correct.

### 1.6 Post-red-team disposition — 9 applied, 2 escalated, both still undecided

The red-team's 11 proposals were processed correctly: 9 accepted with commit hashes, 2 escalated as founder decisions with options and recommendations (`proposals/PROPOSAL-0002.md:49-53`, `PROPOSAL-0010.md:43-58`). But both escalations — the COI policy and the legal/ops pack — were still open on the board at V5 time (`BOARD.md:22-23`, TASK-0013/0014, owner mike) and had to be *defaulted* by V6 rather than decided (exclusive-per-notice, `origin/main:sop/PLAN-V6.md:62,196`; minimal terms in Gate 0, `PLAN-V6.md:165`). The proposal machinery moves at agent speed; founder decisions are the queue that backs up. That asymmetry is structural and worth designing around: escalations should ship with a default that takes effect on a date, which is exactly what V6 eventually did by hand.

### 1.7 Decisions that survived every review — the load-bearing set

These went through V2's crux pass, Mike's V3 review, the V4 integration, two feasibility reviews, and a multi-model council without reversing. Treat them as fixed points; a future session proposing to reopen one should carry unusual evidence.

| Decision | First stated | Last confirmed |
|---|---|---|
| Sell coverage/time; never claim win rates | `PLAN-V2.md:33` | `MARKETING.md:145-146`, V6 unchanged |
| Per-decision purchase at a live notice, not a subscription | `PLAN-V2.md:45,52` | `PLAN-V5.md:43-54`; "No Core until defined" `PLAN-V5.md:138` |
| Provenance-first, fail-closed, no claim without a file | `plan-history/fable-critique.md:10` | `AGENTS.md:29-31`, `PLAYBOOK.md:130-143` |
| USASpending-first; SAM entity-data resale is the legal risk | `plan-history/claim-ledger.md:40-49` | `PLAN-V5.md:174`, V6 Gate 0 counsel task |
| Kill-test before build; failure is a valid, cheap outcome | `PLAN-V2.md:104-110` | `PLAN-V4.md:11`, `PLAN-V5.md:162-166`, V6 Gate 0 |
| Founder review time is the binding constraint, priced per unit | `plan-history/report.md:58-68` | `PLAN-V3.md:32` → `PLAN-V5.md:140` |
| Pay-per-token API, never subscription credentials | `claim-ledger.md:55-59` | never reopened |
| Deterministic pipeline over agent frameworks | `fable-critique.md:7` | `PLAYBOOK.md` structure |
| List 1 is never a send list | `PLAN-V3.md:21` (implicit) | `AGENTS.md:36-44`, `PLAN-V5.md:70` |

The pattern across §1.1–1.6: **reversals triggered by evidence (data pulls, web verification, live evals, Mike's own words) were improvements; reversals and additions triggered by a session having room to elaborate (V4's scaling stack, the V3 SKU packaging) created cleanup debt that is still open.** The repo's own retrospective reached the same conclusion about sessions ("the weakest moments all involved assuming", `research/swarm-retrospective/REPORT.md:31`); this is the plan-level version.

---

## 2. Where the current plan is still weakest

Ordered by how much is resting on the weak point. Items V6 already closes are marked; they remain listed because the in-tree V5 lineage still carries them and the entrypoint drift (W2) means agents keep reading V5.

### W1 — Planning has replaced contact, and the repo knows it

Five accepted plan versions plus a V7 draft; Done column: none (`BOARD.md:36-38`); every conversion driver untested (`SUMMARY-v5.md:30`); the kill-test's cheapest leg (0002b bake-off) unrun (`kill-test/REPORT.md:70`). The council wrote its own epitaph for this behavior: "Coherence is not demand. The repo's proven habit is writing plan N+1" (`SYNTHESIS.md:80`) — and the very next thing this branch produced was eight commits of PLAN-V7 drafting (git log `310bd68..f126287`). Nothing in the governance layer stops a session from writing V8. The plan's biggest open risk is not any assumption inside it; it is that plan-writing is the repo's lowest-friction activity and selling is its highest. → PROPOSAL-0013 (evidence-gated plan freeze).

### W2 — The version-pointer failure V5 was written to fix has already recurred

V5 §"Why the repo made this hard to see" is a five-point diagnosis of how a cold agent learns the wrong company (`PLAN-V5.md:9-19`). Within hours of V6's acceptance, the same failure re-materialized: on origin/main, `AGENTS.md:3` says V6 but `CLAUDE.md:3` says V5 and `PLAYBOOK.md:3` says "Companion to PLAN-V5"; on this branch, everything says V5; the 18 skills still implement V3 (order-intake quotes $450 — V7-draft defect 2); live outreach templates still sell the retired $450 SKU (`templates/outreach/email-1-opener.md:20`, `email-2-followup.md:16`) with corrected `-v5-draft` versions sitting *next to* them, unadopted. The fix is mechanical, not editorial: one canonical pointer, hook-enforced, and the stale copies quarantined — prose warnings have now failed twice. → PROPOSAL-0014, and TASK-0019 should be treated as send-blocking (V6 Gate 0 implies it but does not name it).

### W3 — Build-before-contact economics and the thin-packet failure (V6 partially closes)

V5 commits to building the packet **before** the firm replies (`PLAN-V5.md:45`, `PLAYBOOK.md:63`) but the v5 model charges LLM cost only on packets *sold* (`SUMMARY-v5.md:44`) — the council flagged that this omission can flip Conservative cash-negative (`SYNTHESIS.md:32`). Worse, V5 has no notice-quality gate before the pitch: the runtime-receipts exercise produced an honest, unsellable 1-Covered/9-Gap packet (`kill-test/REPORT.md:46`; `SYNTHESIS.md:31`). V6 adds the ≥50% fill floor and default exclusivity (`origin/main:sop/PLAN-V6.md:60-62`), and the synthesis resolves the prebuild question as map-before-contact, draft-after-interest (`SYNTHESIS.md:43`). What remains open even under V6: the pipeline that makes the floor computable pre-pitch is pinned to V5's PLAYBOOK ordering, and the skills layer would evaluate it *after* intake (V7-draft defect 1) — i.e., the gate exists on paper and cannot fire in the implemented pipeline. That is a W2-class problem wearing a W3 costume, and it is the strongest argument for PROPOSAL-0015 (retire the V3 skill layer rather than keep reconciling it).

### W4 — The in-tree kill gate cannot detect its own failure (V6 closes; carried here because V5 is what the tree teaches)

V5's no-go is "0 paid packets after two matched batches" (`PLAN-V5.md:164`) with batches of ~10–15 (`PLAN-V5.md:151`, `MARKETING.md:76`). At the model's own Base 3% email→paid (`SUMMARY-v5.md:24`), ~25 sends yields an expected 0.75 sales — 0/25 is fully consistent with the Base case being *true*. "Twelve emails is a coin flip at 3%" (`SYNTHESIS.md:70`). V6 replaces this with 80–100 sends across 6–8 notices and a reply-based kill condition (`PLAN-V6.md:182`). Nothing more to decide — but note the sequencing consequence nobody has priced: at ~250–400 viable notices/yr across 6 codes (`SUMMARY-v5.md:58`), 6–8 clean notices is plausibly 3–6 weeks of flow, so the *statistically valid* kill-test is a month-plus of calendar even executed perfectly. The 30-day validation window and the valid kill volume do not obviously fit each other, and no document reconciles them.

### W5 — Door 3's legality is a single point of failure for the whole demand test

The validation plan's primary revenue motion — matched outbound that "pays the bills while the hub warms up" (`PLAN-V5.md:97`) — runs on SBS/DSBS contact data whose commercial use has an unasked counsel question (`PLAN-V5.md:174`; TASK-0018, owner mike, `BOARD.md:27`). The council was blunt: "Outbound is a legal branch, not the company" (`SYNTHESIS.md:33`), and its decision table says a counsel "no" flips validation to inbound — "a harder, more price-exposed test. Do not treat them as the same experiment" (`SYNTHESIS.md:44`). No document defines that inbound experiment: no denominator, no exposure count, no kill number for a concierge-UEI/newsletter-only validation. If counsel says no, the plan currently has a *feeling* about what to do next, not a test. → PROPOSAL-0016.

### W6 — Untested numbers the kill-test does not touch

The kill-test measures matched-email → paid. These v5-model drivers are outside its blast radius and carry real weight: newsletter growth 40 subs/mo Base from a standing start (`SUMMARY-v5.md:28` — the same top-quartile-as-Base pattern F7 flagged on the v3 digest, `feasibility-review/REPORT.md:122`, reduced but not evidenced); inbound packets ramping 1→6/mo (`SUMMARY-v5.md:25`); repeat purchase 2%/mo (`:26`); the $249/mo consultant feed with zero validation activity anywhere on the board (`SUMMARY-v5.md:27`; the five consultant emails of `PLAN-V5.md:158` remain unsent). None is dangerous alone; together they are most of the gap between Conservative ($3.6K Y2) and Base ($150K Y2) once outbound is measured (`SUMMARY-v5.md:37`). The model labels them honestly; the plan should also *sequence* them honestly — the feed test and inbound caps deserve the same measure-or-zero treatment PROPOSAL-0009 forced on Core.

### W7 — The 20-minute review rule is load-bearing and unmeasured

$699 ÷ 20 min is the unit-economics floor (`PLAN-V5.md:140`), review >40 min is a no-go trigger (`PLAN-V5.md:166`), and V6 tightens it to 30–40 (`PLAN-V6.md:184`) — but no real V5 packet has ever been stopwatched (TASK-0017 open; the stopwatch discipline exists, `PLAN-V5.md:160`, with nothing yet to time). The V2-era insight that review time was "asserted, not modeled" (`plan-history/report.md:76`) has been repaired in *structure* (per-unit rule instead of flat constant) but not yet in *data*. TASK-0017's stopwatch release is therefore not a formality; it is the first measurement of the number the price rests on.

---

## 3. What a sharper operator would cut, merge, or reorder

The MVP, per V5 §8 and the council's 7-day table: a sending domain, one industry report, packets for one gated notice, ~10–15 matched emails, newsletter issue 1, the bake-off kill-test (`PLAN-V5.md:148-160`; `SYNTHESIS.md:53-64`). Inventory against that:

**Skills — 18 directories, roughly 3 needed, several actively harmful.** `AGENTS.md:58` calls them "the V3 16-stage wrappers" (the count is 18 — even the description has drifted). The MVP touches maybe notice-triage, gate-run, and rubric-improve; PLAYBOOK.md is the real pipeline and covers the rest in 155 lines. Meanwhile order-intake teaches intake-before-draft and $450 (V7-draft defect 2) — the exact model V5 §2 forbids — and site-publish, content-generate, recompete-detect, outreach-cadence, lead-qualify, pipeline-log, outcome-track, firm-match, firm-ingest, notice-ingest, requirements-extract, deliverable-draft, package-deliver, outreach-draft encode a 16-stage decomposition of what PLAYBOOK does in three loops. This is scope that exists because sessions produced it. AGENTS.md's compromise ("use them when they match a PLAYBOOK step", `AGENTS.md:58`) asks every future agent to do a per-use reconciliation that two plan versions have already failed to do once. Cut: quarantine the directory, keep the three that earn their place. → PROPOSAL-0015.

**Board — 19 tasks, ~9 on the critical path.** On-path: 0015 (domain), 0016 (report), 0017 (packets + stopwatch), 0002 (bake-off), 0001 (send queue, gated), 0018 (counsel), 0013/0014 (the two backed-up founder decisions), 0019 (copy replacement). Off-path but open: 0003 (Hermes bug — infrastructure), 0004 (gate mechanization — V6 says don't start, `PLAN-V6.md:187`), 0005 (full ingester — council demotes to snapshot/canary, `SYNTHESIS.md:64`), 0006-full/0007/0008/0010 (channel build-out — council: do not start, `SYNTHESIS.md:66`). One task is now pointed at a retired artifact: **TASK-0012 applies revisions to the v3 workbook** that v5 superseded and V6 explicitly says not to start (`BOARD.md:34`; `SUMMARY.md:3`; `PLAN-V6.md:187`). Close it; its four flagged changes are either done in v5 (burn restated, Core zeroed, Conservative restored — `SUMMARY-v5.md:44,16,54`) or moot. → PROPOSAL-0015.

**Templates — two generations coexisting.** Four live outreach templates sell the retired $450 SKU while their `-v5-draft` replacements sit adjacent (`templates/outreach/`). Until TASK-0019 lands, every day this persists is a day an agent can assemble a legally-footered, professionally-worded email for a product that no longer exists. Merge: adopt the drafts or delete the originals; do not keep both.

**Financial models — three workbooks, three summaries, one current.** The lineage confusion already burned a session (`swarm-retrospective/REPORT.md:13`; `SUMMARY-v2-standalone.md:1-10`). SUMMARY.md and SUMMARY-v2-standalone are correctly bannered as history; the remaining cut is TASK-0012 (above). Fine otherwise — the v5 model is the right size and admirably labeled (`SUMMARY-v5.md:30`).

**Content pipeline — 5 page archetypes, correctly caged.** `specs/content-pipeline.md` is the best-engineered spec in the repo (the red-team said the same, `feasibility-review/REPORT.md:152`) for a pSEO program that is rightly blocked (TASK-0011, `BOARD.md:33`). No action — but it is the standing example of the repo's failure shape: a production-grade spec for door 8 while door 3's first email is unsent.

**Council layer — 19 files, one deliverable.** The 08-23 council produced genuinely new evidence (runtime receipts, live competitor pricing, the willingness-to-pay scan) and one synthesis whose verdict was *amend-v5* — five decisions for Mike and a 7-day table (`SYNTHESIS.md:39-64`). It also produced a V6, V6-amendments, and a multi-commit V7 draft, i.e., the plan-N+1 habit at council scale. The synthesis's own closing line is the operating rule the repo needs enforced, not restated: "The synthesis is only useful if Mike picks the five rows above and someone claims TASK-0002 or TASK-0016" (`SYNTHESIS.md:80`).

**Reorder — one change.** The single highest-information-per-hour item in the entire repo is the 0002b bake-off: same live notice, HigherGov generator export vs. our packet, Mike stopwatch-judged (`kill-test/REPORT.md:72`). It requires one TASK-0017 packet and one trial signup, it can kill or confirm the wedge sentence before a single email is sent, and it has been "next" since 08-22. Everything else in the 7-day table survives contact with a bake-off result; nothing survives its absence.

---

## 4. Proposals filed

| ID | Title | Weak point |
|---|---|---|
| PROPOSAL-0013 | Evidence-gated plan freeze: no PLAN-V(N+1) until a gate number is measured | W1 |
| PROPOSAL-0014 | Mechanize the current-plan pointer; hook-fail stale references | W2 |
| PROPOSAL-0015 | Quarantine the V3 skill layer; prune the board to the validation path | W3, §3 |
| PROPOSAL-0016 | Pre-register the inbound fallback experiment (counsel-"no" branch) | W5 |
| PROPOSAL-0017 | Freshness discipline for competitor claims in customer-facing copy | §1.4 |

Numbering starts at 0013 because `origin/main` already carries PROPOSAL-0012 (accepted via the V6 cutover); filing a second 0012 on this branch would collide on merge.

Not filed, deliberately: anything the red-team's 11 proposals, PROPOSAL-0012/V6, or the unaccepted V7 draft already covers (kill math, gold-set, quality floor, COI default, counsel/benefits gates, PLAYBOOK re-pointing *content*). PROPOSAL-0014/0015 overlap two V7-draft *findings* but are filed as mechanical repo fixes that are correct whether or not V7 is ever accepted — a defect in the entrypoint should not have to wait on a plan decision to be fixed.
