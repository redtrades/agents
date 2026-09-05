# Swarm retrospective — 2026-08-22/23 build-out

Written by the dispatch orchestrator from complete session context (~26 sessions). Purpose: identify where the swarm got off track, which sessions performed best, and concrete tuning changes. Honest scoring, including of the orchestrator.

## Where we got off track

| # | Miss | Cost | Root cause | Fix |
|---|------|------|------------|-----|
| 1 | Orchestrator summarized Cowork dispatch sessions when Mike meant Claude Code sessions | one cycle | ambiguous "sessions" not clarified | ask scope on ambiguous nouns, or check both |
| 2 | First history task tried to mount ~/.claude (protected) and stalled asking Mike to copy files | one task | wrong tool for protected host paths | rule: host-protected paths → code session, never a mount request (now in memory) |
| 3 | Early strategy messages too long/detailed; Mike corrected twice | friction, re-work | orchestrator verbosity | format locked: one decision per message, options/trade-offs/rec (in memory) |
| 4 | Financial model v1 shipped with assumption misses Mike immediately rejected ($200-400/mo opex, $150-250/hr founder rate, hard review ceiling, outreach cap treated as permanent) | full rebuild ×2 | modeling before grounding assumptions with the owner | before any modeling task: elicit the user's cost reality and which constraints are choices vs physics. The slider widget landed better than any spreadsheet — lead with drivers, not workbooks |
| 5 | Financial lineage confusion: real v2 workbook diverged from SUMMARY.md labels; canonical summary attributed v1 numbers to v2 ($72.0K vs actual $136.9K) | wrong numbers quotable for hours | two sessions writing the same artifact family without version stamps | single-writer per artifact family; version stamp inside every file; byte-compare on dedupe (this is what caught it) |
| 6 | Drive mirror: xlsx corrupted via base64 MCP upload (flailed before the synced-folder workaround); manifest hardcoded ~/agent-reports paths that broke after dedup | rework, latent breakage | binary-over-MCP untested; absolute paths in a manifest | binaries via synced folder; manifests use repo-relative paths (consolidation session caught and fixed) |
| 7 | Usage-limit wave killed 4 sessions mid-flight; two later reported "failed" that had actually completed | status ambiguity | platform limit + unclear terminal state | STATUS handoff doc + scheduled resume worked — keep as the standard limit-wave protocol |
| 8 | Hermes ESTOP set 08-18 (by Mike's own benchmark run) survived undocumented and initially looked like a system fault | confusion in live test; Mike spotted it externally | stop-flags with reason but no owner/expiry | any ESTOP-class flag gets owner + expiry + auto-reminder |
| 9 | Live test first ran raw omlx instead of Hermes (the production harness), and the first Hermes prompts assumed shared context — no data attached. Mike caught the missing attachment from outside | invalid first arm; human caught what a gate should have | tested the convenient path, not the production path; no inputs-present check on agent→agent dispatch | test the production path first; add an inputs-present gate to any agent→agent handoff |
| 10 | Config-headroom check queued mid-task into the running eval session got absorbed/delayed behind the live test | Mike had to re-ask | scope appended to a busy session | follow-ups become discrete tasks/board entries, never appended scope |
| 11 | Growth-plan cowork task left .tmpboard/ artifact and couldn't commit from the sandbox mount | minor cleanup | cowork sandbox vs host git friction | rule now standing: cowork tasks write, code sessions commit |

## Best performers — and the behaviors to clone

1. **Snapshot batch builder** (best overall): ran a negative-control test against its own gate, discovered the naive numeric sweep passes corrupted counts, and invented the count-recomputation rule — an agent strengthening the verification system mid-task. Also produced the deliberate NO-BID sample for credibility.
2. **Response batch builder**: gate discipline exemplar — G3 rejected the best-story firm in 3/5 orders (cert windows, size standard) rather than shipping the better narrative; verified all 19 permalinks live; logged deviations honestly.
3. **Local-model eval session**: best debugging thread — root-caused failures to server capability (grammar fallback found in server logs), discovered the thinking_budget fix, found the Hermes passthrough gap, distinguished config from capability throughout. Weakness: absorbed appended scope (see miss #10).
4. **Consolidation/mirrors session**: respected another session's file lock per CLAUDE.md rules, later verified it stale via lsof before acting; caught the v1/v2 divergence by byte-compare instead of blind-deduping; proactively fixed the Drive manifest paths.
5. **Feasibility red-team**: found the denominator arithmetic error every prior session (and the orchestrator) missed; filed findings as proposals instead of prose.
6. **Financial modeler**: independent full recomputation in Python caught a calibration error (optimistic subs above the plan's own ceiling) before shipping.
7. **Proposal processor**: refused self-acceptance, deferred xlsx edits it couldn't do safely as TASK-0012 instead of faking them, escalated the two human-judgment calls with options/recommendation instead of deciding.

Common thread in every top performer: **they verified their own work by an independent method and were honest about what they couldn't do.** The weakest moments all involved assuming (shared context, path stability, binary transport, "the model must be the problem").

## Orchestrator self-score

Got right: parallel decomposition, kill-test discipline held against enthusiasm, pushback role (sales-before-infrastructure; the sample-first compromise), limit-wave recovery, memory hygiene. Got wrong: misses #1, #3, #4 (assumption-heavy modeling brief), #10 were mine. The financial v1 brief should have asked Mike three grounding questions first — that rework was avoidable.

## Tuning changes (actionable)

1. AGENTS.md addition: any artifact with numbers requires an independent verification method (recomputation, negative control, or live refetch) before it's declared done. The two batch sessions proved the pattern; make it law.
2. Inputs-present gate on agent→agent dispatch: the dispatching side must verify the receiving agent can actually reach every referenced input (file attached, path readable) before the turn ends.
3. Single-writer + in-file version stamps for versioned artifact families (plans, models, SOPs).
4. Standing split: cowork tasks research and write; code sessions commit, push, and touch host services.
5. Session-end hygiene checklist (extend cleanup-after-work): release locks, delete temp dirs, read or kill background jobs, report anything left running.
6. Stop-flags (ESTOP etc.) require owner + expiry + reason; anything past expiry gets surfaced automatically.
7. Follow-up scope goes to the board as new tasks, never appended to running sessions.
8. Orchestrator briefs for modeling/estimation tasks must include grounding questions answered by Mike first (his costs, his rates, which constraints are his choices).
9. Production-path-first rule for capability tests: evaluate through the harness production will use, not the most convenient API.
