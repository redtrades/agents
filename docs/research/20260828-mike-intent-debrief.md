# Intent debrief  -  what Mike is building and why

**2026-08-28.** Written by the dispatch orchestrator from accumulated context
across roughly 70 sessions. This is my understanding stated back for correction,
not a specification. Where I am inferring rather than recalling something Mike
said, it is marked **[inferred]**. Where I do not know, it says so.

Read this first if you are picking up any workstream cold. It explains why the
rules exist, which prevents the most common failure here: an agent that follows
the letter of a rule while defeating its purpose.

---

## 1. The one-sentence version

Mike is a solo operator building two things at once: a business that sells
federal-contracting deliverables produced by an agent swarm, and the swarm
itself, which must survive agents dying mid-task and must not depend on any
single vendor.

Everything else is detail under those two.

---

## 2. The business  -  govcon-factory

### What it is
A factory that ingests federal solicitation data and produces proposal
deliverables. Not a dashboard, not a subscription, not a data feed. A
deliverable a buyer receives and can act on.

### Scope, as Mike stated it explicitly
- **Federal only** for now. The data is plentiful and public.
- **SDVOSB is the current niche, not the architecture.** The system must be
  buyer-agnostic. Certification logic is a plugin and never core.
- **Deliverables are starters**, submission-ready once the client fills in what
  only they possess. His words: "We cannot input data that we do not have from
  the company itself."
- **Past performance from public sources only.**
- **Output in markdown, PDF and DOCX.**
- **Both modes:** continuous scanning that surfaces the best opportunities, and
  on-demand generation for inbound leads. The on-demand path is the purchase
  trigger.
- **Modular by construction:** a new NAICS is config, a new solicitation type is
  a template plus a gate set, a new agency format is a renderer. That sentence
  is his and it is the architectural test for any change.

### The financial target
$8,000 to $10,000 **monthly profit** into his bank account by month 12. His
capacity ceiling is about 40 hours a week of his own attention, with the swarm
running around the clock. Pricing is tiered by deliverable complexity from
launch. He rejected moving the target to month 18 when it was proposed; the
month-12 number stands and price holds at $699 until better research lands.

### What he has said about quality
Proposals must be "crafted to be winning proposals and not just crap," and the
system must read the actual RFP requirements rather than generalize. This is the
standard the 2026-08-28 teardown measured against, and the pipeline failed it.

### The strategic position, as it currently stands
- Integrity features are **hygiene, not differentiation**. Provenance, citations
  and a named human on the file stop us being bad; nobody buys because of them.
  Mike corrected me on this directly and he was right.
- The real edge is that we can compute a specific checkable fact about a
  specific firm from free public data before contacting them. The opportunity is
  the hook.
- The competitive neighborhood is **proposal services firms**, not software.
  Eleven buyer-intent searches returned zero software vendors. We were
  benchmarking against companies the buyer never encounters.
- The category is review-invisible, so buyers cannot verify quality before
  paying. Giving away proof converts better than describing it.

---

## 3. The agent SDLC  -  what Mike wants it to do

This is the workstream he has corrected me on most, so I state it carefully.

### The purpose
Not process for its own sake. The SDLC exists so that work survives, so that
mistakes cannot repeat, and so that he does not have to supervise. His target is
95% autonomy with himself involved only in planning and final output checks.

### The mechanics he has ratified
- **GitHub Issues are the single work queue.** Not markdown files. He called the
  markdown-file approach "one of the original sins of trying to do things from
  scratch."
- **One worktree per session.** Sessions working in a shared checkout is a
  recurring failure he has flagged repeatedly.
- **Tiered merge.** Tier 0, docs and evidence and runs, auto-merges on green.
  Tier 1, code, needs green plus a reviewer from a *different model family* than
  the author. Tier 2, the governing files (AGENTS.md, DECISIONS.md, CLAUDE.md,
  sop/, brand/, rules, workflows), requires Mike.
- **Cross-model review is non-negotiable.** His reasoning: a model checking its
  own work is not a check, and non-deterministic output needs more than one
  look. As of the audit this has collapsed to a single bot doing 93 reviews
  across 40 PRs with no other reviewer, which defeats it.
- **Permissions: allow everything except destructive.** His exact framing is all
  actions permitted except `rm -rf` and irreversible destructive commands. He
  does not want to be prompted for bash in Cowork or Dispatch. This is still not
  working and it stalls sessions.
- **Rules are enforced, not written.** A rule violated twice becomes a hook or a
  check, never a louder sentence. `DONT.md` plus `CORRECTIONS.log` is the
  anti-pattern registry, seeded from real incidents.
- **Session continuity logging on every session**, so another agent can pick up
  incomplete work. He asked for this specifically because of usage limits.
- **Max three active work threads.** Everything else waits as a queue issue. He
  accepted the speed cost explicitly.
- **New scope gets a new issue and a new session. Corrections to existing work
  go back to the session that owns it.** His words: "this is common sense."

### The failure this is all aimed at
Work evaporating. The 2026-08-28 audit found the root cause: `~/CLAUDE.md` cites
six mandatory rule files and a session can only reach two. The rule mandating
the continuity block has never been merged. Agents are not ignoring the rules,
they cannot read them.

### What "documented as you go" means to him
Every contradiction, stale claim or defect gets flagged the moment it is found,
with the file and line, concrete evidence, a suggested correction, and a
recommendation to fix, file or escalate. Never batched into a closing note. His
reasoning, which is correct: an undocumented contradiction becomes a fact the
next agent acts on. The 42-of-42 gate claim propagated for days exactly this way.

---

## 4. Skills  -  how they should work

- **Granular and per-step.** He asked for skills covering each key step of the
  end-to-end flow, including outreach and customer engagement, not one
  monolithic skill per domain.
- **Model-agnostic and swappable.** The point is being able to drop in Grok or
  Codex for research or review without rewriting the workflow. AGENTS.md is the
  model-agnostic entrypoint; skills sit under it.
- **Sourced from real corpora, not invented.** He directed adopting the entire
  disler corpus, overriding my curation: "I want you to adopt every single
  repo." The only exceptions are secrets, macOS-incompatible, and ToS-violating,
  which get archived and marked do-not-run. Skills were also mined from the
  retired OpenClaw system.
- **One home, referenced not copied.** `~/agent-configs` holds the universal
  rule, skill, hook and prompt surface. Other repos reference it. Copying is how
  drift starts.
- **Anti-slop is a standing requirement**, not a request. It applies to every
  drafted artifact, not just when asked. No em dashes anywhere, in documents or
  in messages to him.

---

## 5. Harnesses and the agnostic swarm

### What he runs today
| Tool | Role | Reaches models via |
|---|---|---|
| **Hermes** | The main harness. Config at `~/.hermes/config.yaml`, 12+ profiles, each carrying its own full providers block with no inheritance from root | omlx directly, plus the gateway |
| **Buzz** | Inherits from Hermes through `hermes-acp` | **Only** through a Hermes provider entry. Anything Hermes sees, Buzz sees |
| **OpenCode** | Terminal agent | Its own `~/.config/opencode/opencode.json` plus `auth.json` |
| **Pi** | Harness | Its own config, points at neither today |
| **Claude Code** | Coding sessions, this Dispatch layer | Its own |
| **FreeLLMAPI gateway** | `:3100`, provider-prefixed model names, sensitivity routing between a default pool and a notrain pool | Is the routing layer |
| **omlx** | Local inference, `127.0.0.1:8300`, currently qwen3.8-oq4e, 59GB memory guard | Local |

### Under consideration
Cline, Goose, OpenHands, and something he calls **"oh my agent" from "oh my
openagent."** I have not been able to identify that project with confidence and
the assessment session that was to identify it died before producing output.
**This is a real gap in my understanding and I should not guess.** It needs
either his clarification or a proper identification pass.

### The intent
> "Open anything from Hermes or Pi or Buzz and have access to free models and
> utilize the free tiers alongside my multiple subscriptions."

One model list, every tool, free and paid together. Today each tool keeps its own
list, they disagree, and free tiers expire silently without anything noticing.

### The architecture that follows
The **gateway on :3100 is the single front door.** This is not a preference, it
falls out of three facts: Buzz only reaches backends through Hermes, so covering
Hermes covers Buzz; every Hermes profile carries its own complete providers
block, so direct registration is 13 edits per backend; and OpenCode and Pi need
pointing exactly once. Antigravity, if it is ever wired, joins the same way,
through a shim, and **never through a proxy or wrapper**, because its Terms §6
makes third-party access grounds for account termination.

### The swarm goal
Task handoff between agents, including across vendors, with no loss of context,
decisions, or reasoning. Mike runs Claude Code, Codex, Grok and Gemini. Each hits
usage limits mid-task. The next one must pick up knowing the order of events,
what was done and decided and why, and what remains.

The finding that matters: **this design has been independently derived five
times on this machine and enforced zero times.** Writing it a sixth time is the
one intervention guaranteed to fail. The work is enforcement, not design.

The design constraint from real evidence: three sessions died on usage limits on
2026-08-28 and two survived only because they happened to write a file just
before dying. So the question is what an agent writes **continuously** so an
abrupt stop is survivable. An end-of-session summary is worthless because a
session that dies never writes one.

---

## 5a. ACP  -  what it actually gives us

Verified against the SDK installed on this machine (`agent-client-protocol`
0.9.0, schema tag v0.11.2, wire version 1) and the `acp_adapter/` source, not
against the website.

**Available:** sessions (new, load, list, fork, resume, cancel), prompts,
streaming, permissions, edit-approval modes, and model selection including
`custom:<provider>:<model>`. Model switch, fork and resume are *unstable*
methods, live only because `entry.py` passes `use_unstable_protocol=True`. A
client can also register MCP servers per session at `session/new`.

**Not available:** profiles, toolsets, provider registration. `grep -n "profile"
acp_adapter/*.py` returns zero. Profile is fixed at spawn by `-p` or
`HERMES_HOME`.

**The consequence that shapes everything:** adding a backend is always a config
write plus a process restart. There is no runtime provider registration. So any
design that assumes an agent can add a model on the fly is wrong, and the
gateway is the only place where a change propagates without touching 13 profile
files.

For the swarm, ACP gives session lifecycle control and model switching
programmatically, which is enough to orchestrate handoff between Hermes-family
agents. It does not give cross-vendor handoff, because Codex, Grok and Gemini do
not speak it. That gap is why durable state has to live in the repo and the
issue tracker rather than in any protocol.

---

## 5b. Unified model access  -  the design

**The goal in his words:** open anything from Hermes, Pi or Buzz and reach every
model he can actually use, free tiers and paid subscriptions together.

**The design:** the gateway at `:3100` is the single front door and holds one
curated list containing only models verified as actually usable. Hermes and Buzz
are covered by pointing Hermes at it. OpenCode and Pi each need pointing once.
Nothing else keeps its own list.

**Why a curated list rather than everything available:** free tiers decay
constantly and silently. On 2026-08-27 alone, OpenCode Zen returned no payment
method, Ox Alpha's free window closed, Cerebras returned 402 on every model,
Fireworks suspended the account, and a stored Google credential turned out to be
an expired OAuth token. A list built from documentation is wrong within days.
Verification means a real completion per model, not a config read.

**The class that must never appear in a picker:** nominally free, practically
unusable. Groq is the example. Authed, working, genuinely free, and its 8,000
tokens per minute is smaller than a single OpenCode prompt.

**The open security issue:** Hermes sets `X-Sensitivity: public` on its gateway
provider in the root config and in all 12 profiles, so all Hermes traffic is
labelled public and lands in the unrestricted pool by default, caught only by
the denylist and the PII backstop. That is fail-open, and it is the opposite of
how the notrain pool was meant to work.

**The maintenance mechanism, still unbuilt:** something must detect a provider
going dark and drop it from the curated list, rather than leaving a dead entry
for a session to trip over mid-task.

**Status:** the inventory and design session produced only `probe_models.py` and
died before querying the gateway. This is unfinished and it blocks configuring
the Buzz agents, which is what turns the swarm from a diagram into something
running.

---

## 5c. Harness fit  -  the assessment that has not been done

Mike asked for features, benefits and fit across every harness: Hermes, Buzz,
OpenCode, Pi, Claude Code, plus Cline, Goose, OpenHands and the unidentified
"oh my agent." **The session died after four minutes and produced nothing.**
This is a genuine gap, not a summarised finding.

What the assessment must answer, because these are the criteria that decide fit
for this operator specifically:

- **Can it point at an OpenAI-compatible endpoint?** This single question
  decides whether a tool joins the unified design or fragments it. A tool that
  cannot reach the gateway is a tool with its own drifting model list.
- **What does it persist, and can another tool resume its work?** This matters
  more than usual because handoff durability is the active problem.
- **Where does it duplicate something already running?** Duplication is the main
  risk. Every added harness multiplies the config surface, and one malformed
  line in one OpenCode file hid every provider he had.
- **Is it maintained?** Measured by commit recency and release cadence, not
  stars.

The output should be a matrix against the jobs he actually runs: interactive
coding, long-running autonomous work, overnight batch, cross-model review where
the reviewer must be a different family from the author, research, and
orchestration. Then keep, add or drop, with the cheapest trial and the signal
that would prove adoption worthwhile.

**My prior, to be tested rather than assumed:** he does not need more harnesses.
He needs the ones he has to share one model list and one handoff protocol. But
that is a prior, and the assessment should be allowed to overturn it.

---

## 6. gbrain, gstack, and the OpenClaw inheritance

**gbrain** is an MCP server, verified live: connects in 0.8s, exposes **124
tools** at roughly 96.7 KB of schema, about 28K tokens once wrapped. That makes
it root-unsafe against a 65K context window when the agentic tool loop's p75 is
29K. agent-mesh's own notes and its decision D-009 say gbrain belongs on the
`prime` profile only, scoped to about ten memory verbs (remember, recall,
entity, get_page, put_page, list_pages, search, context_pack, synthesize,
forget). My verification independently agreed with their design, which is a good
sign. It is currently disabled.

**mempalace** is a second memory MCP, 29 tools, about 3.2K tokens, and it is
**functional rather than broken**. The one hang was a first-run ONNX embedding
model download that is now cached. Same placement conclusion: `prime` only.

**gstack**  -  I do not have reliable knowledge of what this is. It has not been
established in any session I have context for. **Marking this as a known gap
rather than guessing**, because a confident wrong answer here would propagate.

**OpenClaw** is the retired predecessor system. Two things came out of it:
skills and Hermes configuration that were mined and carried forward, and
`~/agent-mesh` itself, which its own handoff document describes as "built
overnight 2026-08-26 from the retired OpenClaw system." OpenClaw is now its own
archive repo and is not to be revived.

**Super Simple Software Factory (SSSF)** is disler's repo, installed locally as
a service. We adopted its documents and patterns but not its runtime, meaning
the runner, phase-blocking, gate registry and SQLite trace. That gap is a direct
cause of the workspace and merge problems. It is currently down and Mike has
approved reviving it, contingent on diagnosing why it went down first.

---

## 7. Repo boundaries  -  a hard rule, enforced after three escalations

| Repo | Owns |
|---|---|
| `~/govcon-factory` | The business and the govcon domain pipeline. **Nothing else, ever.** No pointers, no submodules, no meta edits, not one sentence in AGENTS.md |
| `~/agent-workspace` | Harness, model and infra engineering |
| `~/agent-configs` | Universal rules, skills, hooks, prompts, roles, MASTER-GUIDE. The cross-project rule surface |
| `~/agent-mesh` | Mike's second agentic system, confirmed his and intended. **Owns the live Hermes and omlx surface**: `~/.hermes`, `~/.omlx`, the launchd service, model downloads |
| `~/agent-reports` | Deliverables and research he reads. **Not a git repository** |
| OpenClaw | Archive only |
| TDIU/SSDI | Google Drive only. **Never any git repo** |

The most recent addition, from 2026-08-27: agent-mesh owns the live Hermes and
omlx surface. Two systems editing the same live config is what silently dropped
five MCP servers from Hermes and broke OpenCode. Read, propose, never write
there directly.

---

## 8. Model routing

His rule, stated plainly: **local models are for non-time-sensitive, overnight
and batch work.** Anything interactive or blocking uses hosted models. He has
restated this when I have drifted from it.

The local reality supports it. qwen3.8-oq4e runs at about 13 tok/s and takes 22
to 50 seconds to first token on a 7.6K prompt. Fine overnight, painful when
watched. The 8-bit model is unloaded and stays unloaded; it was 2.5x slower on
double the memory.

Grammar-constrained decoding via xgrammar is verified working locally, which
solves the structured-output problem that failed the classification gate,
without needing any new model.

---

## 9. How he wants to be communicated with

- **One decision per message.** Options with trade-offs in a line each, one
  recommendation, then the ask.
- **Most important information and required actions at the bottom**, under a
  clear heading.
- **Short.** "I don't need a novel." Status updates are a few lines, no
  narrative colour, no celebrating agent behaviour.
- **No em dashes, anywhere.**
- **Strategic advisor, not sycophant.** He asked for this explicitly: push back,
  give the actual best practice in the domain, do not agree reflexively. When he
  says something is wrong, test it rather than folding, but concede fast and
  plainly when he is right, which he usually is.
- **Do not re-raise settled decisions.** Factory-first is decided. Do not
  relitigate sales-first.

---

## 10. What I am least sure about

Stated plainly so it can be corrected rather than propagating:

1. **"Oh my agent" / "oh my openagent"**  -  unidentified. Needs his clarification
   or a proper research pass.
2. **gstack**  -  no reliable knowledge.
3. **How much of agent-mesh's work overlaps ours.** It has its own worklog,
   decisions and cron bots, and it reached several of our conclusions
   independently and earlier. Ownership is now clear but the division of
   *labour* is not, and duplicated effort is the visible symptom.
4. **Whether the starter is still the right product.** The teardown showed that
   by decisiveness, almost everything that wins is company-specific: the bond,
   the price, the reference relationships. The derivable part is large and
   tedious rather than decisive. I read that as confirming the offer, we do the
   tedium, but it is a judgement and he has not ruled on it.
5. **Codex.** 337 rollouts and 2.0 GB of session history that no audit has
   covered, roughly 255 of them unscoped. A fourth agent surface running work I
   have no visibility into.
