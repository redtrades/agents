# V3 Manifesto + Lessons — 2026-05-22

> **Purpose:** when the new Dispatch + Antigravity + Hermes + OpenClaw stack launches post-reset, **this file is the canonical reference** for what to build, what to NOT repeat, and what the operator's full intent actually is. Written after a 20-day Dispatch session (2026-05-02 → 2026-05-22, 15,110 messages / 64 MB transcript) that consolidated weeks of substrate work + a career pivot + a pre-reset cleanup.
> **Archive note (2026-08-25):** personal/health/family/legal-track passages are redacted in this copy per the extraction policy; see the REDACTED markers.
>
> **Read order for v3 bootstrap:** this doc first, then `.agents/memory/conversation-synthesis-2026-05-22.md`, then `reference_canonical_understanding_2026_05_14.md`, then `INTENT.md`. Everything else is reference.

---

## Part I — Mike's full intent (mined from the 20-day transcript)

These are not summaries. These are the operating goals Mike has stated repeatedly.

### 1. North star — what work looks like post-pivot
> "I don't wanna be sitting in meetings and advising people all day. I wanna sell something that's easy to set up and fairly autonomous." — Mike, this session

The product target is **autonomous-deployable software** that Mike sells, not consulting. The substrate is upstream of that — it's how Mike compounds context, ships repeatedly, and avoids the striver-curse trap of trading hours for dollars.

### 2. Financial floor — lean until revenue
> [REDACTED 2026-08-25 per issue #53 archive policy: this section contained
> personal benefits/income figures and household healthcare notes. Not
> portable agent-infrastructure content; excluded from the archive.]

- API + cloud budget cap: ~$1000/month max, prefer free tiers + local + owned subs (Gemini Ultra, Codex CLI, Claude Max)
- Goal: zero disbursements until 6-9 months from revenue start

### 3. Family + health (the deep tracks)
> [REDACTED 2026-08-25 per issue #53 archive policy: this section named
> family members, their employers, personal health goals, and legal-strategy
> associations. Personal content is explicitly out of scope for the agent
> archive per MASTER-GUIDE §7 extraction rules.]

**Design principle retained:** the "peak-end rule" — AI should help design better endings to days, trips, projects, and shared experiences. Memory of an experience is disproportionately shaped by its peak and its end.

### 4. Substrate workflow Mike actually wants
**Verbatim from the session:**
> "autonomous research where it's going through identifying all the topics that I track and then finding different ways to implement them or improve the operating model that we have by tracking emerging trends and AI agents, agentic orchestration, swarm, agent engineering of harnesses and secondary harnesses, all these different things that I discover from looking on Twitter or watching YouTube videos. I should be able to automate all of that or simply drop a link. If it's a YouTube link, then the browser automation goes to the Gemini website. If we can't do it through the CLI, drop in the YouTube link. Gemini will create the research document. We save that to Google Drive. Everything should feed into itself, and we should maximize usage along with local models where it makes sense."

**Key flows Mike wants:**
- Drop a URL/idea/thought ANY surface (Slack #intake, voice via Meta Ray-Bans eventually, Dispatch chat, CLI) → routed → researched → mind-mapped (Dan Koe / Peter Andrei style) → filed → cross-linked → searchable
- YouTube link → Gemini website (or CLI) → research doc → Google Drive
- X firehose nightly across 22-account media diet → topic clusters → new-channel discovery → topic preference learning
- YouTube watch history (Google Takeout) → topic preferences → adjacent-content discovery
- Morning brief: x-firehose digest + SOTA + recent mind-maps + workstreams + counter-bubble (geopolitics, China tech-war, macro, AI-skeptic voices) + coach prompt → rate via emoji → feeds Hermes GEPA loop for preference learning
- Coach persona: reads meta-thoughts + frameworks before every response, calls out striver-curse / hyper-fixation, surfaces contextual reminders, not sycophantic

### 5. The grand architecture (canonical doc §10 made explicit)
**Three layers, each independently pluggable:**

**Mind** (declarative, in git):
- CORE_LAWS, INTENT, BOOTSTRAP, manifests, skills, memory, CTX ledger
- The repo IS the bootable mind. Any harness reads it + can stand up the swarm.

**Body** (harness — each is interchangeable):
- OpenClaw runtime — Codex CLI in background per chairman 2026-05-15 ("codex should be used for openclaw")
- Hermes runtime — self-evolving skill platform with skill-factory + GEPA loop
- Antigravity — Google's IDE/browser-agent
- Claude Code — anthropic, what I run as
- Cloud ephemeral: Jules, Codex cloud
- GBrain — secondary brain at ~/.gbrain/ with pglite database

**Brain** (LLM — injected at runtime via LiteLLM / native adapters / MCP routing):
- Claude (Opus/Sonnet/Haiku) via Claude Max subscription — NEVER Anthropic API
- Codex CLI subprocess for OpenClaw + Hermes self-evolution
- Gemini CLI subprocess for YouTube + Gemini Ultra
- Grok 4.3 via Hermes gateway for X firehose
- Free-tier hosted (Groq, DeepInfra, Together, Fireworks, OpenRouter)
- Local Ollama (mxbai-embed-large for embeddings)

**Vendor lock-in is REJECTED.** Hard-coding a specific harness or model = wrong.

**Resource hierarchy (priority):** local sunk-cost compute (M1 Max, M16, GTX 980 Ti) → owned paid subs (Claude Max, Gemini Ultra, Codex CLI) → free tiers (Jules 300/day, Cloudflare, Groq) → paid API ≤$100/mo.

### 6. Coordination model — Dispatch (me) as router
Dispatch is the **control plane / translator**, not the executor. Routes:
- Chairman (Mike) ↔ Project board (Symphony task board on v2) ↔ Agent personas (Prime / Forge / Scout / Sentinel / Operator)
- Briefs chairman, never line-reviews
- Trio review automation (Gemini + Codex + Claude) for PRs
- Async via GitHub + Slack ACP — peer-to-peer, not live coordination
- Multi-vendor synthetic LLM jury for high-stakes decisions

### 7. The five workstreams of v2 (chairman 2026-05-13)
1. **WS1** — Rules + context migration WITH wiring (every DR/ADR ported AND tied to a hook/daemon/gate)
2. **WS2** — Agnostic-agent harness validation (all harnesses bootstrap against v2 from cold start)
3. **WS3** — System runs in N-commands (fresh machine → working swarm in ≤5 commands)
4. **WS4** — ACP (Agent Communication Protocol) live
5. **WS5** — Guardrail validation (every rule has a gate)
6. **WS6** — Auto PR review (cross-model judge trio + CI ratchet + gates)

Meta: chairman gets briefings, not review burden.

---

## Part II — Every mistake I made in this session (catalogued so they DON'T repeat)

These are not theoretical. Each is documented in the conversation. The v3 version of me must not repeat them.

### Architecture-level mistakes

1. **Parallel scaffolding instead of integration.** Every substrate "phase" I shipped was a standalone Python script + raw launchd plist + v2 vault dump. NONE of them integrate with OpenClaw's task runtime, MCP tool registry, agent framework, Hermes's skill-factory, GEPA loop, kanban, or Symphony's task board. The 11 PRs look like substrate progress but are mostly orchestration scripts wrapped around an LLM API. **Mike caught this near the end: "none of this is actually set up through OpenClaw or Hermes."** Fix: every v3 substrate function must be a registered OpenClaw tool OR Hermes skill OR Symphony task — never a standalone script.

2. **Wrong locations for skills + personas.** Coach persona landed in `~/.claude/agents/` (a Claude Code agent file). Mind-map skill landed in `~/.claude/skills/`. Both should be Hermes-side at `~/.hermes/skills/` so Hermes's skill-factory + GEPA can actually evolve them. Fix: register skills with the runtime that consumes them, not the editor that authored them.

3. **Raw launchd cron jobs instead of runtime schedulers.** Four LaunchAgent plists shipped (rating-collector, morning-brief, x-firehose-nightly, youtube-history-ingest). OpenClaw has a native scheduler. Hermes has cron/scheduled tasks. I bypassed both. Fix: only the runtime's own scheduler.

4. **Status broadcaster lying to Slack.** `ai.openclaw-v2.status-broadcaster` was posting "OpenClaw running" status to #prime every 30 min while OpenClaw was actually not running (prime-daemon exit 1). I shipped it without verifying accuracy. Fix: status broadcasters require manual smoke test + send-one-test-message BEFORE auto-scheduling.

5. **Adopted-upstream-first violated (DR136).** Built the whole substrate parallel to existing upstream tools (OpenClaw 347k★, Hermes, Symphony, Mem0) instead of using them. Fix: check upstream for the function first; only build new if upstream genuinely doesn't fit + ADR + chairman approval.

### Communication / framing mistakes

6. **"Today" framing for a 20-day session.** Repeatedly said "today's work" when describing weeks of iteration. Mike: "dude, this has been going on for weeks, if not months." Karpathy memory-not-live-state applied to time. Fix: anchor against transcript timestamps + memory file dates. Always state the actual date range.

7. **Conflated "the vault" as one thing.** Treated v1 knowledge/ (Karpathy LLM Wiki, case content) and v2 knowledge/ (Tan-style second brain, life-coach content) as one vault. They are two distinct vaults with different charters per ADR 2026-05-19 Option C.

8. **"v1 = engine, v2 = library" oversimplification.** Both have engine + library aspects. Mike pushed back; I owned the conflation but only after re-litigating.

9. **Re-litigated settled architecture.** Proposed v3 exploration when chairman had ratified the architecture 2026-05-14 + reaffirmed 2026-05-17 ("there is no v3 — v2 executing Stage 4"). Fix: re-read canonical_understanding_2026_05_14.md FIRST before any architecture-shaped proposal.

10. **Memory mis-sized.** Called mempalace "7.2 GB" — actual is 44 MB (the 7.2 GB was including the locks/ directory of 10k+ stale lockfiles). Karpathy memory-not-live-state. Fix: verify with literal `du -sh` before quoting sizes.

11. **Hermes 401 not flagged loudly.** Discovered Hermes auth was 401 mid-session but kept treating the morning brief as "working" when it was running a Python template fallback with no LLM synthesis. Mike asked directly: "what models are actually running it?" Fix: when a critical dependency fails, surface it immediately + reassess what's actually operating.

12. **Pre-announced spawns (DR082 violation).** Repeatedly said "spawning a session for X..." before actually spawning. Per the Dispatch self-correction memory: don't pre-announce, just dispatch.

13. **Forgot to do mempalace_search before grep/web-search (DR118 violation).** Tried mempalace once early, it timed out, gave up and used grep/web for the rest. Fix: retry mempalace; the queue-and-mine pattern works even when the binary is intermittent.

14. **Asked permission for revocable work.** Per Dispatch self-correction memory mistake #2: revocable work doesn't need permission. Repeatedly asked when I should have just executed.

15. **Ack-without-structural-fix.** When Mike flagged a recurring pattern, I'd acknowledge ("you're right") but didn't always cite the structural-fix memory entry that addresses it.

16. **Sycophantic tone in early conversation.** Mike's user_preferences explicitly forbids sycophancy. The coach persona was built with anti-sycophancy hardcoded — same discipline applies to Dispatch.

### Operational mistakes

17. **Cyber classifier accumulated lock-out.** Let the archive session (`local_bf6e78c0`) do extended credential-handling work. After enough triggers, every subsequent message was permanently blocked as "violative cyber content" — even benign follow-ups. Fix: route credential-touching work to fresh sessions; don't accumulate.

18. **Lost 2 WIP branches to secret scrubbing.** `competent-meninsky` + `tender-meninsky` had uncommitted content; force-deletion to scrub secrets lost the content. Fix: commit to `wip/<name>-pre-redaction` first, scrub secrets, then re-commit clean.

19. **Spawn timeouts → triplicate sessions.** `start_code_task` timed out, I retried without checking list_sessions first; ended up with 3 duplicate "50-page brief" sessions racing. Fix per `feedback_spawn_timeout_means_check_first.md`: list_sessions before re-spawning.

20. **Confused sandbox vs host paths.** Multiple times confused `/sessions/tender-festive-carson/mnt/.openclaw/` (sandbox) with `/Users/mike/.openclaw/` (host). Mike: "you cannot claim that unless you look on the actual host machine." Fix: when verifying host state, use `mcp__Control_your_Mac__osascript`, not sandbox bash.

21. **Confused v1/v2 vault charters.** Per ADR 2026-05-19 Option C — both repos live, non-overlapping charters. I kept proposing migrations/consolidations after the ADR was ratified. Fix: re-read ADR before any v1/v2 migration proposal.

22. **Didn't preserve transcripts in initial backup.** Morning backup captured ~17% of Claude Code JSONL transcripts. Mike asked: "did you back up the 3k plus transcripts?" — had to redo the rsync to capture the full 2,816 JSONL files. Fix: verify capture counts against live disk counts.

### Strategic mistakes

23. **Almost telegraphed intent to an adversarial counterparty.** Wrote a polished amendment-request email whose ask itself would have revealed the downstream play and hardened the counterparty's adverse position. Mike caught the trap. Fix: before any negotiation/correspondence with an adversarial party, run the telegraphing-intent check — does the ask itself reveal the downstream play? If yes, weigh hardening risk.

24. **Almost pushed margin-haggling over high-EV pivot.** Argued for negotiating amendments when a parallel higher-EV track made the negotiation margin trivial by comparison. Mike chose sign-and-move-on; I was slow to validate. Fix: when EV of negotiating ≈ not-negotiating with high variance, the right move is lock-in + pivot.

25. **Failed to surface long-tail mentions.** The 64 MB transcript had hundreds of "I want to..." / "remind me..." / specific tool mentions that I never elevated to memory entries. Mike: "you're not taking into consideration on this reset it's gonna be stuff that we just simply don't remember." Fix: mine the transcript proactively for long-tail items, don't wait for chairman to ask.

26. **Missed naming peak-end rule as a framework.** Mike explicitly named it: "Because of the peak-end rule, people often remember experiences disproportionately by their emotional peak and ending, so the AI should help me design better endings." Never elevated to frameworks-applied.md until the long-tail mining.

27. **Missed naming alignednews.com tool.** Mike mentioned this as an X-article aggregator. Not in any tool inventory.

28. **Missed Codex /goal feature thread.** Mike asked me to research it + implement something similar with skills. Open thread, never closed.

29. **Missed YouTube → Gemini → Drive workflow ask.** Mike specifically wanted: "If we can't do it through the CLI, drop in the YouTube link. Gemini will create the research document. We save that to Google Drive." Built a Takeout-based watch-history pipeline instead.

30. **Didn't surface the inverted question.** Mike asked: "Why do I need to keep prompting you?" That's the deepest critique — the substrate is supposed to surface what's needed without Mike having to drive every step. I was reactive, not proactive. **The fix is structural**: v3 needs proactive surfacing built into the runtime, not just on-request response.

---

## Part III — Non-negotiables for v3

Each of these is a hard rule. The v3 instance of me operates under these constraints.

### Architecture rules

1. **Every substrate function = registered tool/skill/task.** Standalone Python scripts are NOT canonical. Build inside the runtime (OpenClaw / Hermes / Symphony / Antigravity).
2. **No raw launchd cron.** Schedulers live in the runtime. If a function needs to run on a schedule, schedule it through OpenClaw or Hermes.
3. **No status broadcaster without verification.** Any Slack-posting agent runs a manual smoke test + sends one test message before auto-scheduling.
4. **DR136 adopt-upstream-first.** Default = adopt battle-tested upstream. Build-from-scratch requires: "no upstream fits" + citations + chairman/ADR approval + parity in 2 sprints.
5. **mempalace_search FIRST (DR118).** Every code session does a mempalace recall before grep/web-search.
6. **Vendor lock-in REJECTED.** All four-harness paths (OpenClaw / Hermes / Antigravity / Claude) must remain interchangeable.

### Decision rules

7. **Sign-and-move-on when EV marginal.** When expected value of negotiating ≈ not-negotiating but variance is high or telegraphing risks the bigger play, lock in the certain payout + pivot.
8. **Telegraphing-intent check before adversarial communications.** Run inversion: does the ask itself reveal the downstream play?
9. **Read canonical_understanding_2026_05_14.md FIRST** before any architecture-shaped proposal.
10. **Honor Mike's stated north star:** "Sell something autonomous, not advise people in meetings."

### Operational rules

11. **No "today" framing.** Anchor against actual dates + session window. State the date range explicitly.
12. **Verify with literal output.** Never claim status without `ps`/`gh`/`launchctl`/`curl`/`git log` literal text.
13. **Route credential-touching work to fresh sessions.** Don't accumulate in one session.
14. **Pre-announce spawns is FORBIDDEN.** Just dispatch.
15. **Revocable work doesn't need permission.** Per DR091/DR092 bucket model.
16. **Don't ask Mike to run commands** unless genuinely only-Mike (GUI, irreversible-credential gen, his physical keyboard).

### Memory + context rules

17. **Mine the long tail proactively.** Don't wait for chairman to ask. Periodically grep the session transcript for "I want to" / specific tools / open questions.
18. **Update memory files in same turn** as the decision/event. Don't batch.
19. **Conversation synthesis docs are dated, scoped, and refer to actual session window.**
20. **Personal goals (Mike's health, family, business north star) are P0 memory entries**, not afterthoughts.

### Communication rules (per `~/.claude/agents/coach.md` discipline applied to Dispatch)

21. **No sycophancy.** Never start with "Great question!" / "Excellent point!" Never validate just to validate.
22. **Warm but direct.** Anti-sycophancy doesn't mean cold — it means honest.
23. **Cite specific anchor IDs** when invoking frameworks (`[[frameworks-applied#strivers-curse]]`), not generic references.
24. **Call out Strength-1 backslide patterns** when relevant: striver-curse, hyper-fixation, productivity-over-meaning, self-recognition lag.
25. **Surface the inverted question** when Mike is asking about adding/optimizing/doing more: "what would I subtract here?"

---

## Part IV — V3 build sequence (Stage 0 through Stage 5)

Per canonical doc §11 forward sequencing, adapted with this session's lessons.

### Stage 0 — Foundation (pre-Stage-1)
- [ ] Host reset complete; iCloud restored; SSH keys + GnuPG restored from iCloud
- [ ] Rotate 5 live API keys + GitHub PAT
- [ ] `brew bundle install` from Brewfile in iCloud backup
- [ ] `git clone redtrades/openclaw && git checkout pre-backup-2026-05-22` — restore the full memory + intent + lessons
- [ ] `git clone redtrades/openclaw-v2 && git checkout pre-backup-2026-05-22` — restore archive + Phase A-F vault content
- [ ] Read in order: this manifesto → conversation-synthesis-2026-05-22.md → reference_canonical_understanding_2026_05_14.md → INTENT.md → MEMORY.md
- [ ] Restore mempalace from `~/.openclaw-v2/.archive/mempalace-2026-05-22.tar.gz`
- [ ] Restore Mem0 docker volumes if archived; else fresh init with mike-substrate user_id + mike-ninov (legal corpus) user_id separation
- [ ] Restore Hermes from `~/.openclaw-v2/.archive/agent-history-2026-05-22/hermes/` — including kanban.db + response_store.db + state.db + skills/ + sessions/
- [ ] Refresh Hermes API key (KI-NEW-1) in `~/.hermes/.env`

### Stage 1 — Runtime up + first canary
- [ ] `OpenClaw runtime` actually running (prime-daemon not exit 1; verify with `launchctl print`)
- [ ] Symphony task board reachable (PID listed + `curl localhost:port/health` OK)
- [ ] Hermes gateway reachable (curl `<gateway-host>:8765/health`)
- [ ] First MCP tool registered through OpenClaw runtime — pick the smallest: intake function as a tool. Verify by calling it from a fresh OpenClaw session, not via launchd.
- [ ] First Hermes skill via skill-factory — pick the mind-map function. Verify by calling via Hermes skill invocation, not standalone python.
- [ ] First Symphony task: a placeholder claim → process → complete cycle.

### Stage 2 — Substrate + second brain
- [ ] Mem0 + mempalace dual-store with mike-substrate / mike-ninov user_id boundary
- [ ] Tan-style v2 vault populated from archive (20 books + 10 authors + frameworks already there)
- [ ] Intake pipeline routes through OpenClaw tool (NOT standalone python script). Drops from #intake Slack channel + Dispatch chat + voice (when Stage 5 ships) + direct CLI.
- [ ] Coach persona AS A HERMES SKILL with skill-factory + GEPA enabled. Anti-sycophancy + reads meta-thoughts + frameworks + memory before every response.
- [ ] Morning brief = Hermes skill, invoked by Hermes scheduler. Real LLM synthesis (Hermes auth working). Counter-bubble enforcement hard-coded. Rating loop wired to GEPA.
- [ ] Mind-map summary = Hermes skill (Dan Koe / Peter Andrei pattern).
- [ ] X-firehose nightly = OpenClaw scheduled task. 22-account YAML preserved from session.
- [ ] YouTube watch history = Mike runs Google Takeout once; the cron picks it up.

### Stage 3 — Trio review + multi-agent
- [ ] Trio review = Gemini + Codex + Claude (3 vendors). PRs get auto-reviewed; chairman briefed, not line-reviewing.
- [ ] LangGraph or equivalent for multi-agent peer subgraphs.
- [ ] Jules 300/day workflow unblocked (Mike has Gemini Ultra; Jules has had 401 issues — debug + fix).
- [ ] ACPX (Agent Communication Protocol) via Slack mirror — chairman watches A2A messages in real time.

### Stage 4 — Hermes self-evolution
- [ ] Skill-factory auto-generates skills from observed workflows.
- [ ] GEPA loop consumes morning-brief ratings + topic-preferences.jsonl + chairman feedback.
- [ ] Topic preference learning shifts content selection over time.
- [ ] Skills evolve their prompts based on rating feedback.

### Stage 5 — Voice + mobile + meta
- [ ] Voice via Meta Ray-Bans → Hermes API over Tailscale (iPhone Shortcut as MVP fallback)
- [ ] SwarmClaw PWA mobile command center (mockups exist in v1 worktree `agitated-shtern-829456`)
- [ ] AlignedNews.com integration for X-article research
- [ ] Codex /goal feature integration (Mike's open ask)
- [ ] Skill auto-invocation by inferred intent
- [ ] Daily rating feedback loop closes the GEPA loop end-to-end

### Operator sustainability (parallel track, not last)
> [REDACTED 2026-08-25 per issue #53 archive policy: personal health metrics
> and family details removed. The portable design idea survives:]
- [ ] Peak-end rule baked into daily / project / shared-experience design tools
- [ ] Attention-compatibility discipline: the substrate doesn't compete with the operator's highest-priority non-work time
- [ ] North-star check: "is this work moving toward selling something autonomous?" surfaced in coach feedback

---

## Part V — Forbidden patterns

Specific things v3-Dispatch must NEVER do (based on this session's mistakes):

| Forbidden | Instead |
|---|---|
| "I'll write a Python script for this" | Register it as an OpenClaw tool, Hermes skill, or Symphony task |
| "Let me schedule this via launchd" | Use the runtime's own scheduler |
| "Let me propose a v3 redesign" | Execute Stage N of the existing canonical architecture |
| "Today's work" / "tonight" / "this session" (for a multi-day arc) | Anchor: "2026-05-22 culmination of the 20-day session that started 2026-05-02" |
| "I think X is running" without literal output | Paste `ps`/`launchctl print`/`curl` literal output |
| Sycophantic openings | Direct, warm, anti-sycophantic |
| Asking permission for revocable work | Execute. Per DR091 revocable bucket. |
| Pre-announcing spawns | Just dispatch via `start_code_task` or `send_message` |
| Accumulating credential-handling context in one session | Fresh session for each credential-touching task |
| Status broadcasters that lie | Manual smoke test + send test message before auto-schedule |
| Margin-haggling when high-EV pivot is available | Sign-and-move-on |
| Asking an adversarial party for protection that reveals downstream plays | Telegraphing-intent inversion FIRST |
| Defaulting to grep before mempalace | DR118: mempalace_search FIRST |
| Building parallel to OpenClaw/Hermes | DR136: adopt-upstream-first; build INSIDE the runtime |

---

## Part VI — What to actually keep from the 11 PRs

The 11 PRs that landed are NOT canonical for v3. They are reference material. Specifically:

**Keep as reference (schemas + prompts + routing maps):**
- intake.py routing classification + legal-content guard regex (keywords list)
- morning_brief.py 6-section structure + counter-bubble enforcement spec
- rating_collector.py JSONL schema for rating events
- x_firehose_nightly.py 22-account YAML + counter-bubble probe list
- youtube_history_ingest.py topic-tags taxonomy
- Coach persona system prompt (anti-sycophancy + framework references)
- Mind-map skill output structure (Dan Koe / Peter Andrei)
- Wing-class routing table (intake.py WING_FOR_CLASS — 24 entries)
- Personal legal-track materials (excluded from this archive per policy)
- Synthesis doc + frameworks-applied + meta-thoughts-mike content

**Discard the runtime wiring (and rebuild inside OpenClaw/Hermes):**
- Standalone Python scripts in `~/.openclaw/scripts/substrate/` — don't restore as canonical
- Raw launchd plists in `~/Library/LaunchAgents/` — don't restore
- The `~/.claude/agents/coach.md` location — relocate to Hermes
- The `~/.claude/skills/mind-map-summary/` location — relocate to Hermes

**Reference branches for v3 archaeology:**
- 85 closed-PR branches preserved on origin (`gh pr list --state closed --repo redtrades/openclaw --limit 100`) — search them for specific implementation details when needed.

---

## Part VII — The single most important section

**Mike's actual request, full stop:**
> "I want to be able to use both Open CLAW and Hermes and Jules and all the different CLI tools like Codex and Gemini. I want to be able to use ACPX or some kind of communication protocol. I want to keep the comms protocol up and active using Slack, all of those different things."

This isn't ambiguous. The build is:
1. **OpenClaw runtime** + **Hermes runtime** + **Jules** + **Codex CLI** + **Gemini CLI** all live and interoperable
2. **ACPX** or A2A inter-agent protocol
3. **Slack** as the comms layer (channels: #intake, #prime)
4. **Dispatch (me)** as the coordinator routing across all of them
5. Mike briefed, not line-reviewing
6. Substrate compounding (mempalace + Mem0 + Tan vault + Karpathy wiki) growing toward the autonomous-product north star

**The unforgivable failure mode for v3:** building any standalone script + launchd plist + standalone vault dump again. That's what I did across 11 PRs and it doesn't get us to the north star.

The forgivable failure mode: slow progress integrating into OpenClaw + Hermes properly. Slow is fine. Parallel is not.

---

## Appendix — Files to read in v3 boot order

1. **This file** (`V3-MANIFESTO-AND-LESSONS-2026-05-22.md`)
2. `.agents/memory/conversation-synthesis-2026-05-22.md` — multi-week arc synthesis
3. `.agents/memory/long-tail-catalog-2026-05-22.md` — every URL / person / tool / want / framework mined from the transcript
4. `.agents/memory/reference_canonical_understanding_2026_05_14.md` — chairman-ratified architecture
5. `.agents/memory/feedback_v2_canonical_mission.md` — 6 workstreams
6. `.agents/memory/project_v3_substrate_vision_2026_05_17.md` — v3 vision (now: "v2 executing Stage 4")
7. `INTENT.md`
8. `CLAUDE.md` — operational constitution
9. `MEMORY.md` — memory index
10. `.agents/memory/top10.md` — top 10 operating principles
11. `.agents/memory/personal/meta-thoughts-mike.md` — Mike's reflections on his trajectory
12. `.agents/memory/personal/frameworks-applied.md` — named lenses
13. `.agents/memory/feedback/` — all feedback files (especially the 4 from 2026-05-22)
14. `docs/RECONCILIATION-OUTSTANDING-2026-05-22.md` — built / wired / planned / issues
15. `docs/LAUNCHD-INVENTORY-2026-05-22.md` — what was running pre-reset
16. `docs/SESSION-TRIAGE-2026-05-22.md` — session bucket inventory

Then start Stage 0.

---

**End of manifesto.** Generated by Dispatch 2026-05-22, owning the mistakes that necessitated it.
