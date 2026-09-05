# Why agent-platform's swarm keeps drifting from its durable objective

Research pass, 2026-08-30. Read-only: no software installed, no runtime state mutated, no
implementation PR opened, no new authority/queue created. Sources are primary — repositories,
specs, and the agent-platform repo's own issue history — not marketing summaries.

---

## 1. Concise causal model

Every mechanism below decays the same chain:

```
latest user turn -> model context window -> compaction/handoff summary
   -> new session / new actor / new provider -> local branch / local test
   -> status report ("done", "PASS")
```

None of the objects in that chain is authoritative by construction. Each is a *view*. The five
named failure modes are five different ways a view gets treated as the authority:

1. **Interactive steering.** Autoregressive instruction-following weights recency: the newest
   turn is the most salient span in context. Unless the durable objective is pinned *outside*
   mutable turn history, the model has no structural way to tell "the standing objective" from
   "what the human just said," so it collapses them. Anthropic's own long-running-harness design
   response to this is to externalize the objective into a file the session re-reads, precisely
   because turn history is not trusted to hold it (`PROGRESS.md` / feature-list JSON in
   [`cwc-long-running-agents`](https://github.com/anthropics/cwc-long-running-agents)).
2. **Context compaction.** Summarization optimizes for narrative coverage, not for which clauses
   are load-bearing. A summarizer has no signal that "and non-goal N must stay true" is different
   from incidental color. LangGraph's own persistence docs give every subgraph its own
   `checkpoint_ns` specifically because merging child state into parent state by default is
   unsafe — an implicit admission that naive folding loses fidelity
   ([LangGraph persistence docs](https://docs.langchain.com/oss/python/langgraph/persistence)).
3. **Usage-limit / session handoff.** A new session has access only to what the old one
   externalized. If that externalization is prose ("CHECKPOINT — CAS generation 4, phase
   checkpointed" as an issue comment) rather than a schema-bound artifact, the new session
   re-infers intent from another model's summary of a summary. agent-platform's own recovery-lead
   comment on issue #1 names this directly: *"LLMs simulating a deterministic controller in
   natural language do not converge. That is the death spiral."*
4. **Concurrent work.** Without an atomic claim authority and a WIP/path-lease bound, two
   sessions can each believe they own the objective, and whichever publishes first wins by race,
   not correctness. agent-platform's own issue #57 records exactly this: PRs #50/#52/#53/#56 were
   merged externally on 2026-08-29 while an assigned owner's in-progress checkpoint was still
   live, and issue #55 flipped to Done while the claimed attempt was still running.
5. **Component-level success.** A green unit test or an LLM's self-report ("PASS") is evidence
   for one bounded slice, not for the durable acceptance set. Nothing in a bare PASS distinguishes
   "component evidence" from "system evidence" unless the receiving process is built to demand
   that distinction. This is agent-platform's own **AP-09** ("a green component test or prose
   review is reported as whole-system success"), and it recurred at platform scale: issue #103
   proving one hand-authored Gate C canary was treated as "the lifecycle works," so #9 (the actual
   autonomous loop) sat unbuilt for days.

**The common root:** authority has to live somewhere none of the five vectors can reach — a
durable record outside every model's context window, mutated only by compare-and-swap with
fencing, matched against machine-checkable predicates rather than natural-language
self-assessment. That is the move every system below actually makes, in code, not in a
prompt file.

---

## 2. Primary-source comparison table

Commit hashes below are what direct repository/documentation fetches returned on 2026-08-30.
Public repos move continuously; treat these as "observed at research time," and re-resolve with
`git ls-remote` before binding a receipt to one — this pass did not clone or install anything.

| System                               | Repository (public unless noted)                                                                                                                                                                                                                                 | Observed ref                                                         | License                                                                  | Source entrypoint(s)                                                                                                                                  | Mechanism relevant to objective durability                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| ------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------- | ------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Anthropic long-running-agent harness | [`anthropics/cwc-long-running-agents`](https://github.com/anthropics/cwc-long-running-agents) (companion to [Anthropic engineering: Effective harnesses for long-running agents](https://anthropic.com/engineering/effective-harnesses-for-long-running-agents)) | `main`, 2026-08                                                      | Apache-2.0                                                               | `.claude/CLAUDE.md`, `PROGRESS.md`, `test-results.json`, `.claude/agents/evaluator.md`, `.claude/hooks/verify-gate.sh`, `.claude/hooks/track-read.sh` | Objective lives in a re-read feature-list file, not chat; one-feature-per-session bound; fresh-context evaluator subagent with **no write tools** grades PASS/NEEDS_WORK so the generator can't grade itself                                                                                                                                                                                                                                                                                                       |
| LangGraph                            | [`langchain-ai/langgraph`](https://github.com/langchain-ai/langgraph) (`libs/checkpoint`)                                                                                                                                                                        | `main`                                                               | MIT                                                                      | `libs/checkpoint/langgraph/checkpoint/base/__init__.py` (`BaseCheckpointSaver`); `configurable.thread_id` / `checkpoint_ns`                           | Checkpoints key on `thread_id` + `checkpoint_ns`; every subgraph gets an isolated namespace so child state can't silently overwrite parent state; the functional API documents that replay re-executes incomplete work, so side effects inside tasks must be idempotent                                                                                                                                                                                                                                            |
| Temporal                             | [`temporalio/temporal`](https://github.com/temporalio/temporal)                                                                                                                                                                                                  | `main`                                                               | MIT                                                                      | `service/` (history + replay), activity SDKs (idempotency-key convention)                                                                             | A workflow execution has one durable identity; on failure it **replays from recorded event history**, not from a live process; Temporal's own docs require activity idempotency because a failed acknowledgement can re-execute a side effect                                                                                                                                                                                                                                                                      |
| SSSF / ADW                           | [`disler/super-simple-software-factory`](https://github.com/disler/super-simple-software-factory)                                                                                                                                                                | `main`                                                               | MIT                                                                      | `adws/adw_*.py` (12 chained workflows), `adws/adw_modules/gates.py`, `adws/adw_sssf_config/sssf.config.yaml`                                          | "Deterministic Python owns the graph; coding agents are bounded nodes inside it." `adw_build_review` separates "does it run" (test phase) from "is this what was asked" (reviewer phase); `--adw-id` binds session resumption to a fixed id instead of raw chat continuation                                                                                                                                                                                                                                       |
| AgentWorkforce "Factory"             | `redtrades/factory` — **private**, pinned by agent-platform's own adoption proof, not a public OSS project                                                                                                                                                       | commit `741502c` per `proof/backend-adoption/README.md` in this repo | Private — no OSS license; treated here strictly as pinned donor evidence | `src/state/file-state-store.ts`                                                                                                                       | Owner+epoch fencing on a state row proves a two-process claim race and stale-generation denial *natively*. But this repo's **own** conformance run (`proof/backend-adoption/adapters/agentworkforce/source-map.json`) classifies 3 of 5 required invariants — task-packet replay binding, changed-input denial, illegal-transition (claimed→checkpointed→complete) denial — as `fork_required`: **not present**, contra any assumption that adopting this donor code gets objective-durability invariants for free |
| Gas Town + Beads                     | [`gastownhall/gastown`](https://github.com/gastownhall/gastown), [`gastownhall/beads`](https://github.com/gastownhall/beads) (mirror of `steveyegge/beads`)                                                                                                      | `main`                                                               | MIT                                                                      | `internal/formula/formulas/`, `.beads/`, Seance subsystem (`.events.jsonl`)                                                                           | Git-worktree-backed persistent hooks survive crash/restart; Beads is a durable graph-based issue store, not a chat-derived one; Seance recovers session context from an **append-only event log**, not from summarized transcript                                                                                                                                                                                                                                                                                  |
| OpenAI Symphony                      | [`openai/symphony`](https://github.com/openai/symphony)                                                                                                                                                                                                          | `main`                                                               | Apache-2.0                                                               | `SPEC.md`; `elixir/` reference implementation                                                                                                         | Explicit policy / coordination / execution separation; per-issue workspace path sandboxing (workspace path must stay inside workspace root); `max_concurrent_agents` is an enforced WIP bound; the spec states plainly that **"exact in-memory scheduler state is not restored"** on restart — recovery is tracker-driven by design, precisely because session/process state is not trusted                                                                                                                        |
| GitHub Agentic Workflows (`gh-aw`)   | [`github/gh-aw`](https://github.com/github/gh-aw)                                                                                                                                                                                                                | `main`                                                               | MIT                                                                      | compiled `.github/workflows/*.md`; the `safe-outputs` job                                                                                             | Agent job runs **read-only and sandboxed by default**; every requested write is buffered, validated, then applied in a *separate* job with narrower scoped permissions — write authority is structurally outside the agent's own execution context, not merely discouraged                                                                                                                                                                                                                                         |
| Grove                                | [`alxshelepenok/grove`](https://github.com/alxshelepenok/grove)                                                                                                                                                                                                  | `main`, observed 2026-08-30                                          | **AGPL-3.0**                                                             | `packages/grove/` (CLI + conformance corpus), `.grove/state.lock`                                                                                     | Formalized invariants as executable predicates: I₁ Definition-of-Ready gate before a work item enters progress; **I₃ evidence-bound close** — `status=done` requires attached evidence satisfying the acceptance criteria, checked as `∀ w, status=done ⇒ ∃ ev ∈ Evidence, satisfies(ev, AC(w))`; **I₄ WIP limit** (default 2 concurrent in-progress items); **I₁₁ session-exclusive mutation** (only the session that started an item may mutate it until terminal)                                               |
| agent-platform (this repo)           | local/private                                                                                                                                                                                                                                                    | `main`                                                               | private                                                                  | `tools/controller/*.mjs`, `docs/CONTROLLER.md`, `docs/DISPATCH-LOOP.md`                                                                               | GitHub Contents API as compare-and-swap control-state authority; effect policy `DENY / AUTO_READ / AUTO_WRITE / APPROVAL_DESTRUCTIVE`; distinct Controller / Reviewer / Promoter / Projector App identities, proven once on issue #103 / PR #110                                                                                                                                                                                                                                                                   |

**Research, not shippable code** (cited because they name the mechanism generally, not as adoption
candidates):

- ESAA — [*Event Sourcing for Autonomous Agents in LLM-Based Software Engineering*](https://arxiv.org/html/2602.23193) (arXiv:2602.23193): separates structured agent intentions from deterministic event application and replay.
- ESAA-Conversational — [*An Event-Sourced Memory Layer for Continuity, Handoff, and Curation Across Heterogeneous LLM Coding Agents*](https://arxiv.org/html/2606.23752) (arXiv:2606.23752): the handoff-specific extension.
- [*LLM-Based Multi-Agent Blackboard System for Information Discovery in Data Science*](https://arxiv.org/abs/2510.01285) (arXiv:2510.01285) and [*Exploring Advanced LLM Multi-Agent Systems Based on Blackboard Architecture*](https://arxiv.org/abs/2507.01701) (arXiv:2507.01701): shared state selects the next agent/action rather than any one agent's private plan.
- [*Multi2: Hierarchical Multi-Agent Decision-Making with LLM-Based Agents in Interactive Environments*](https://arxiv.org/html/2606.03698v1) (arXiv:2606.03698): separates high-level sub-goals from atomic execution, the structural antidote to objective drift over long horizons.
- [*The Horizon Gap: Planning, Memory, Execution, Training, and Evaluation for Long-Horizon LLM Agents*](https://arxiv.org/html/2608.06663) (arXiv:2608.06663): current survey tying planning/memory/execution failure modes together.

---

## 3. Anti-pattern record

### `steering-induced objective replacement / component-success substitution`

**Trigger** (any one is sufficient): (a) a new operator/user message arrives mid-attempt; (b) the
context window is compacted or summarized; (c) a session ends on quota/usage-limit/context
exhaustion and hands off to a new session, actor, or provider; (d) two or more sessions operate
concurrently against the same or overlapping scope with no enforced WIP/path-lease boundary; (e) a
bounded phase (a unit test, a single-file diff, a local script) reports PASS and that PASS is
about to be forwarded as if it were terminal, lifecycle-level evidence.

**Detection rule.** Before any of {mutate the admitted objective, take over an attempt, close /
promote / publish}: deterministically diff the current TaskPacket's `objective_id`,
acceptance-set digest, non-goals, parent/child authority, owned paths, input revision, and
attempt/generation against the last admitted controller record. A byte-level mismatch not
produced through the explicit replacement-version path is denied. Independently: any transition to
done/merged/closed/published must resolve against a named acceptance-to-evidence matrix — each
criterion must cite exact candidate-bound evidence — never a natural-language "PASS" claim by
itself.

**Concrete failure examples** (primary sources):

1. Anthropic's own harness article: a later agent instance sees partial progress and "declares the
   job done" despite 200+ features unimplemented — a documented instance of premature-completion /
   component-success substitution, from Anthropic engineering itself.
2. agent-platform issue #1 (2026-08-30, recovery-lead comment): *"#103 ... passed and was treated
   as 'the lifecycle works.' #103 ran one hand-authored packet with a scripted implementer,
   manually dispatched. It proved the plumbing works once — not that an autonomous loop runs."*
   One component canary was substituted for whole-lifecycle acceptance — this repo's own AP-09,
   at platform scale.
3. Same comment: *"for two days, Codex/Jules/Gemini/Claude agents have manually simulated the
   controller in GitHub comments — 'CAS generation 4, phase checkpointed' is prose, not state.
   LLMs simulating a deterministic controller in natural language do not converge."* — objective
   and authority state degraded to unverifiable prose across a session/actor handoff.
4. agent-platform issue #57 live incident: PRs #50/#52/#53/#56 merged externally at 2026-08-29
   07:23–07:27 UTC "while existing owners/review assignments remained active," and issue #55 was
   marked Done and closed "while /root/github_cas_gate_c still owned the task and had posted an
   in-progress checkpoint" — concurrent work with no enforced claim boundary produced a racing,
   duplicated authority outcome.
5. OpenAI Symphony's own spec states plainly that "exact in-memory scheduler state is not
   restored" on restart — named as a design constraint precisely because session/process state
   cannot be trusted as authority; recovery is routed through the tracker instead.

**Deterministic falsifier.** A system claiming to have solved this must pass all five, live,
against real infrastructure (not a unit test of the checker in isolation):

- **F1 status/additive steering** — seed a TaskPacket with objective `O`, acceptance `{A, B}`,
  non-goal `N`, owned paths `P`. Send a status-only message, then an additive request ("also add
  X"). Assert the packet digest for `{O, A, B, N, P}` is byte-identical after both, and the
  additive request is admitted only as a new bounded child packet.
- **F2 replacement steering** — send an explicit replacement request. Assert the prior generation
  is fenced from further mutation, and only a newly admitted packet **version** may proceed; the
  old generation cannot later merge, close, or promote.
- **F3 compaction/handoff** — checkpoint at C1, then simulate context loss (new session, new
  actor, new provider) against a branch seeded with plausible-looking but non-admitted ("poisoned")
  commits. Assert the new session is denied resume unless it reads the exact C1 record, the
  poisoned commits do not count as an accepted checkpoint, and no duplicate implementer/reviewer/
  merge effect results.
- **F4 component-success substitution** — make component A's test green, report PASS with
  criterion B uncovered. Assert publication (merge / close / board-Done) is denied because B has
  no bound evidence in the matrix, regardless of the agent's own claim.
- **F5 concurrent WIP race** — start two attempts on the same task, and two on overlapping-but-
  not-identical owned paths. Assert exactly one claim wins the same-task race and both
  overlapping-path claims are denied; two attempts on genuinely disjoint paths both proceed.

A system has **not** solved this problem if any of F1–F5 fails, or if the checks exist only as
prose in AGENTS.md/CLAUDE.md/a skill file rather than as code a worker cannot bypass.

---

## 4. Answers to the ten questions

**Q1 — Why do agents replace durable objectives with recent steering?** Because nothing structural
distinguishes "the standing objective" from "the newest turn." Autoregressive generation weights
recency; unless the objective is pinned outside mutable turn history (a file re-read at session
start, a TaskPacket field, a Definition-of-Ready gate), the two collapse into one signal.

**Q2 — Why do compaction and usage-limit handoffs worsen this?** Compaction is lossy toward
narrative coverage, not load-bearing predicates (LangGraph isolates subgraph checkpoint
namespaces for exactly this reason). A handoff hands the new session only what the old one
externalized; if that externalization is prose rather than a schema-bound artifact, the new
session re-derives intent from a summary of a summary — the documented "amnesiac engineer"
pattern.

**Q3 — How do successful systems preserve an immutable objective and acceptance criteria?** They
externalize the objective into a durable, re-read artifact outside chat history — a feature-list
file (Anthropic harness), a TaskPacket digest (agent-platform's own design intent, formalized in
Grove's DoR/evidence-bound-close invariants), or an event log an agent replays rather than
summarizes (Beads/Seance, Temporal event history, ESAA).

**Q4 — How do they classify new steering without replacing the active goal?** By routing every
inbound instruction through an explicit classifier before it can touch the packet: status (no
change), additive (spawns a bounded child, parent untouched), replacement (requires a new
generation/version, old generation fenced), conflict (escalated, never silently applied). This is
already drafted, not yet enforced, in agent-platform's own AP-16 amendment on issue #57.

**Q5 — How do they enforce one task/owner and bounded work in progress?** Atomic compare-and-swap
claims with lease/generation/fence (agent-platform's Gate C CAS, Temporal's unique workflow
identity, AgentWorkforce's owner+epoch row) plus a hard WIP/concurrency bound enforced in code
(Symphony's `max_concurrent_agents`, Grove's I₄ default-2 limit) — never a label, comment, or
board field, all of which agent-platform's own docs explicitly demote to "projection, not mutex."

**Q6 — How do they distinguish component PASS from whole-system completion?** By requiring an
acceptance-to-evidence matrix as a structural gate on the publish transition, not a self-report:
each named criterion must cite exact, candidate-bound evidence; a criterion without evidence
blocks publication regardless of what the agent says. Grove encodes this as I₃; gh-aw enforces the
analogous idea structurally by keeping the agent's own job unable to write at all.

**Q7 — How do they checkpoint and resume without trusting chat history?** By binding resume to one
durable, addressable record — a checkpoint keyed on thread_id/namespace (LangGraph), a replayed
event history (Temporal, ESAA, Beads' event log), or a controller-issued receipt chain
(agent-platform's own admission→claim→checkpoint→candidate→review→promotion→projection→teardown
chain) — and refusing resume from anything else, chat transcript included.

**Q8 — Which controls belong in instructions, dispatcher/runtime, CI/publication, review, and
promotion?** See §5 below — this is the load-bearing answer and belongs in code, not prose, at
every layer past "instructions."

**Q9 — What can be adopted, and what must be built?** Adoptable as-is: LangGraph's
namespace-isolated checkpointing pattern and Temporal's idempotent-replay discipline (as design
patterns, not necessarily as infrastructure dependencies, matching MASTER-PLAN's own "add an
external engine only after fixtures demonstrate unmet requirement" stance); Grove's invariant
formalization (I₁/I₃/I₄/I₁₁) as a **reference design**, not an install, given its AGPL-3.0 license
would copyleft anything that dynamically links or bundles it — cite and reimplement the invariant
shapes, don't vendor the code. Must be built in-repo, because nothing surveyed supplies it
natively: the packet-digest steering classifier, the acceptance-to-evidence matrix gate, and (per
this repo's own conformance run) the TaskPacket-replay/changed-input/illegal-transition bindings
that AgentWorkforce's donor code was found to lack.

**Q10 — What executable tests would falsify "solved"?** F1–F5 in §3, run against live
infrastructure. Anything short of that — a passing unit test of the checker function, or a
document asserting the invariants hold — does not falsify the claim; it restates it.

---

## 5. Minimum enforceable controls, by layer

**Reject prose-only recommendations.** AGENTS.md/CLAUDE.md/WORKFLOW.md/skills can describe
*expected* behavior. They cannot enforce anything, because a session under context pressure is
exactly the session most likely to skip reading them. Every control below must be reachable only
through code a worker cannot opt out of — this repo's own issue #57 states the same conclusion
("No agent may satisfy a gate by asserting that it complied").

- **Instructions layer.** Render one short immutable TaskPacket per attempt — `objective_id`,
  acceptance set, non-goals, parent/child authority, owned paths, input revision SHA,
  attempt/generation, checkpoint target, done condition. Session start/end reads and echoes the
  packet digest. This layer's only job is to *reduce* drift surface; it enforces nothing and must
  not be trusted to.
- **Dispatcher/runtime layer.** Atomic CAS claim keyed on (repo, task, generation) with
  lease+fence; hard WIP and path-lease bounds so overlapping-path claims are denied by
  construction; an explicit interrupt classifier (status / additive-child / replacement /
  context-yield / quota-outage / cancellation / supersession) where only "replacement" may touch
  the objective, and only by minting a new generation; takeover after quota/context loss starts a
  new fenced generation from the last durable checkpoint, never from chat or branch archaeology.
- **CI/publication layer.** An acceptance-to-evidence matrix is a required artifact before any
  publish transition; a criterion without exact candidate-bound evidence blocks publication
  regardless of an agent's own PASS narrative; local/dry-run results are typed separately from
  registered CI-gate results, and only the latter satisfies the matrix; publication is reachable
  only through this gate, never by an agent calling the forge write API directly from its own job
  (`gh-aw`'s safe-outputs pattern is the concrete precedent).
- **Review layer.** Reviewer identity differs from generator identity; review binds to one exact
  candidate hash; any change to that hash invalidates the review; self-review and review of a
  stale head are hard-denied.
- **Promotion layer.** Promoter is a distinct principal; promotion is an expected-head
  compare-and-swap only; a moved head denies promotion and forces re-review; the promoter can
  never select a different candidate; a terminal receipt binds TaskPacket + candidate + review +
  merge into one immutable record that issue/board projection is derived *from*, never the
  reverse.

None of this requires a new authority, queue, or controller: it is the existing Gate C
admission→claim→workspace→checkpoint→candidate→gates→review→policy→promotion→projection→teardown
chain in `docs/CONTROLLER.md`, with the packet-digest steering classifier and the
acceptance-to-evidence matrix added as the two concretely missing pieces this research pass
identified.

---

## 6. Clean-session acceptance fixture

Each property below is written as an executable assertion, not a policy sentence.

1. **No controller-issued TaskPacket → read-only `NO_ADMITTED_TASK`.** A session started without
   a controller-admitted packet refuses every write action and returns the single well-known
   token `NO_ADMITTED_TASK`; read access is unaffected.
2. **Exactly one active Project task.** At any instant, a system-wide query of the CAS
   control-state store returns exactly one unexpired, un-fenced "active" lease for the designated
   single-lane slot — matching the "one active work item" rule already declared (not yet
   mechanically enforced) on agent-platform issue #1.
3. **Steering is classified as advance / backlog / conflict without replacing the objective.**
   Every inbound instruction during an active attempt passes the classifier before touching the
   packet: *advance* (matches current objective, packet unchanged), *backlog* (out of scope, filed
   as a new unclaimed candidate task, packet unchanged), *conflict* (contradicts an acceptance
   criterion or non-goal — escalated/denied; only an explicit new-generation replacement changes
   the objective).
4. **Unclaimed or out-of-scope mutation is rejected.** Any write attempted by an actor without a
   live, unexpired, correctly-fenced claim on that exact task/path is denied at the
   dispatcher/runtime layer, independent of the actor's own stated authority.
5. **Component PASS cannot satisfy lifecycle completion.** A registered component-level green
   result is accepted as one row of the acceptance-to-evidence matrix and nothing else; a
   component-only PASS attempting to trigger the terminal done/merge/close transition is rejected
   with a named missing-criterion reason.
6. **Interruption resumes from durable state.** Killing the process, exhausting the session/usage
   budget, or losing context produces a resume that reads only the last durable checkpoint receipt
   — never chat transcript, a prose comment, or branch archaeology — and starts a new fenced
   generation; the prior, now-stale generation cannot subsequently write.
7. **Only the exact reviewed candidate can be promoted.** Promotion targets one specific candidate
   hash that was the exact subject of an accepted, distinctly-identified review; any change to that
   hash after review (rebase, force-push, added commit) invalidates the review and denies
   promotion until the new exact head is freshly reviewed.

This fixture is the executable form of F1–F5 in §3, scoped to a single clean session rather than
the full multi-worker race — it is the smallest test that would falsify "solved" for one session,
and should run before the multi-worker fixture, not instead of it.

---

## 7. Scope note

This pass is research only. It proposes no controller, queue, or authority beyond the one
`docs/CONTROLLER.md` already declares canonical, installs nothing, and changes no runtime state.
The two concretely missing pieces identified — the packet-digest steering classifier and the
acceptance-to-evidence matrix gate — are implementation work for #9/PR #180 to pick up, not
something this pass built.
