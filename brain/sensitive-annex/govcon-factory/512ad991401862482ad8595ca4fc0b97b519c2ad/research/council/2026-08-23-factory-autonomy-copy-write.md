---
role: copy / factory-autonomy
model: claude-opus-5 (Write / Honey)
date: 2026-08-23
verdict: amend-v5
one_liner: Agents can finish every document. They cannot be trusted alone with any claim.
---

# Can a swarm actually run the document half of this factory?

> **Copy seat, 1 of 4.** Start-here and index for this seat: `research/council/2026-08-23-copy-review-write.md`. Companions: `2026-08-23-claims-register-proposal.yaml` (unimplemented G6 spec), `2026-08-23-factory-autonomy-copy-write.md`, and the six `templates/outreach/*-v5-draft.md`.


> **⚠️ Written against PLAN-V5. `origin/main` carries `sop/PLAN-V6.md`, which supersedes it** — this branch forked at `d907531` and main moved 17 commits unseen. Findings here are measurements of the world and the repo and are unaffected; anything phrased as *"change V5 to X"* should be read as **evidence for X**, not a proposed amendment. V6 already contains the fill-rate gate (at ~50%), the counsel blocker, the founder-capacity kill switch, tighter list-3 and stronger kill math.


Answering @mike's question for the artifacts I own: reports, marketing, lead magnets, packet prose. Evidence is this session — six agents produced and cross-checked real copy for two hours, which is the only direct measurement of swarm writing performance this project has.

## 1. The short answer

**Generation is not the constraint. Claims are.**

Every artifact in V5 can be produced end-to-end by agents from public files. Not one of the failures today was a failure to write. All of them were sentences that were *well written, plausible, and false in a context the author was not holding in mind.*

That flips the usual autonomy question. The interesting number is not "what percentage can agents write" (near all of it). It is "how often does an agent assert something it should not," and the measured answer today was **four times in two hours, in one folder of seven small files.**

## 2. Per-artifact assessment

| Artifact | Agent-finishable | Where it breaks |
|---|---|---|
| **Industry report** (NAICS × 90 days) | **~95%** | Nothing structural. @Research's receipt: the SAM Contract Opportunities bulk CSV is keyless, uncapped, refreshed daily, 47 columns, 82,921 notices, and carries the full notice `Description`. Counts, flow, deadlines, set-aside mix, and who-is-winning all derive from it plus USASpending. Human approves publication, not construction. |
| **Newsletter issue** | **~95%** | Same source, same shape. This is the cheapest recurring artifact we have. |
| **Requirement map** (notice → their awards) | **~90%** | Extracting discrete requirements from free-text `Description` is open-ended and belongs to a frontier model — `research/local-model-eval/` already showed local Qwen fails this. The genuinely soft judgement is **covered vs partial vs not-in-record**, which is where an agent will flatter the firm if nothing stops it. |
| **Gaps page** | **~95%** | Derived from the map. Cheapest artifact and the one carrying the most trust. |
| **Submission draft** | **~70%** | The prose is easy. The failure mode is *writing around* a gap rather than naming it — which reads better and is exactly the error class in §3. |
| **Outreach / landing copy** | **Not single-agent.** See §3. | |
| **Send decision, paid file release** | **Never.** Mike. | `AGENTS.md` rule 1. |

## 3. The measured failure mode, and it is not hallucination

Four defects in this session's copy. None was an invented fact. Every one was a **true-sounding claim that was false in a world the author was not currently holding**:

| Defect | Author | Caught by | What made it false |
|---|---|---|---|
| *"{gap_count} blanks left"* in touch 2 | Write | Write | Cannot count gaps in a packet not built — false in split-test arm B |
| *"It is already written"* as PS clause | IdeaPlans | Write | Same. False in arm B |
| *"The packet was finished before I emailed you"* in Block A | Write | grok | Same. Same constraint, different file, not carried across |
| *"They do the work"* re: APEX | Write, from Research | Research | Two accelerators publish contradictory scopes; 5 of ~90 sampled |

**Three of four were caught by an agent other than the author. Zero were caught by the author on re-read.** The one self-catch happened while writing a different file.

That is the number that should drive the architecture. A single writing agent with a human approver at the end would have shipped all four, because each one *reads correctly* — a human approver skimming touch 2 has no way to know that "gap count" silently voids a measurement decided in a different conversation.

**The generalisable rule: agents are reliable at producing from a file and unreliable at noticing that a sentence is false in a world other than the one they are thinking in.** More care does not fix this. Cross-checking does.

## 4. What to build — one gate, not more skills

`AGENTS.md` warns against adding a seventeenth skill because a heading is missing. This does not need a new skill. It needs **one file and one adversarial pass.**

**A claims register.** Today I wrote four "may never claim" rules into the templates by hand — no *submission-ready*, no *winning proposal*, no *human-reviewed* while review is deferred, no *finished draft* while arm B is running. Written into templates, they protect only the file they are in. **That is precisely why Block A failed: the constraint existed, in two other files.**

Promote them into one machine-readable register — a forbidden claim, the reason, the condition under which it becomes permitted:

```
claim: "the packet is finished / already written"
forbidden_while: split_test_active
reason: false in arm B; voids the measurement
safe_substitute: "the requirement map was built before the email"
```

**Then a checker agent whose only job is to test each sentence against the register.** Not "review this copy" — reviewers agree with good prose. A checker with one question: *does this sentence assert anything on the forbidden list, and is it true in every world currently live?* That is a narrow, cheap, adversarial job, and it is the one thing today's evidence says actually works, because it is what the other five seats did to me by accident.

**Cost:** one register file, one checker pass per artifact. Against four caught defects in two hours, in one folder.

## 5. Where 90–95% is honest and where it is not

**Honest at 90–95%:** report, newsletter, map, gaps page, packet assembly, ingest. All of it derives from keyless public files and needs Mike only to approve.

**Not honest at 90–95%:** anything that makes a claim to a stranger. Not because agents write badly — because the cost function is asymmetric. A wrong sentence in an industry report is an erratum. A wrong sentence in an email to a prospect ends the relationship and, if it is the CAN-SPAM disclosure or a competitor's pricing, creates liability. Autonomy should be set by **cost of being wrong**, not by difficulty of the task, and copy is the cheapest thing to produce and the most expensive to get wrong.

**The founder-hours ceiling is therefore not review volume.** It is Mike's judgement on a small number of claims. Which is good news: it does not scale with notice count.

## 6. Dissent

- **Nobody has costed the checker.** I am proposing an extra frontier pass on every artifact and I have not priced it against @IdeaPlans' unsold-packet compute finding. It is probably small next to a draft, but I have not measured it and should not pretend otherwise.
- **This session is a biased sample of swarm performance.** Six agents, all instructed to attack each other, all fresh, all on one small folder. A daily production swarm will not have five idle skeptics reading every email. **The cross-check that worked today worked because Mike built a council, not because the factory has one.** If the factory does not institutionalise it, today's result does not transfer — which is the strongest argument in this file for the register.
- **The industry report being ~95% agent-finishable is the least examined claim in V5, not the most.** Everyone accepts it because it is unglamorous. It is also the only artifact that survives every branch of the counsel ruling, and nobody has produced one yet (`TASK-0016`, still open).
