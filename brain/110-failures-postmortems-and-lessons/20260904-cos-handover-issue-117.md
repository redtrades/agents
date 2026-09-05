## CoS session handover (2026-09-04 ~23:38 ET) — usage ~95%

### Intent / north star
Harness-agnostic multi-agent swarm control plane: any agent (any CLI) picks up mid-task using the same START/AGENTS/skills; GitHub issues = queue/resume; independent App review + exact-head merge; discovery via graphify later; skills once. Long-term skins (Fusion/Optio/OpenHands) are NOT the plane. GovCon product parked until more AISDLC proofs.

### Control plane (5 layers) — ADR on this issue
1. Router — ~/.agents → archive 00-start-here/START.md
2. Queue+resume — agent-sdlc issues (#117 board)
3. Authority — govcon-reviewer-bot App + CI harness-agnostic (#125)
4. Discovery — KEY-DOCS/KEYWORDS; graphify spike #128 later; gbrain revive-later
5. Skills once — agent-configs adapters

### Where canon lives
- Archive branch: codex/archive-foundation (no main)
- Cold start: /Users/man/agent-knowledge-archive/00-start-here/START.md
- NEW: KEY-DOCS.md, KEYWORDS.md, WORKSTREAMS.md (archive PR #7 merged)
- Policy: redtrades/agent-configs
- Implementation: redtrades/agent-sdlc
- Board: this issue #117
- Scratch reports: ~/agent-reports/ (not canon)

### Live vs museum
Live: archive, agent-configs, agent-sdlc, govcon-corpus(+CMP)
Museum/evidence: agent-platform, agent-mesh, agent-workspace, govcon-factory freeze gap

### Completed this session (high signal)
- Canon/cold-start: START pack, stubs, archive on foundation locally
- App wiring + Goal B canary #119→#120 earlier; Jules smokes: #123→#124 tree, #126→#127 blob, #129→#130 tag, #131→#132 branch, #133→#134 release-latest
- CI #125 harness-agnostic PRs→main
- Worktree prune ~139→34 (report ~/agent-reports/worktree-prune-2026-09-04/)
- Harness smoke: claude/codex/agy PASS; opencode→openrouter/openrouter/auto PASS
- Doc Bot created; KEY-DOCS pack merged archive PR #7
- Codex KEY-DOCS draft: ~/agent-reports/codex-north-star-docs-2026-09-04/KEY-DOCS.md
- Open PRs held: sdlc #116 #86 #71 #18; configs hygiene leftovers

### In flight / parked
- Jules #135 formatGitHubMilestoneRef OPEN (babysit)
- Cleanup (branches/worktrees/CLI fan-out) PARKED per Mike
- GovCon #121 PARKED
- Graphify spike #128 later
- Pointer FAILs (configs AGENTS template, Hermes SOUL, museum skills path) parked
- MIKE-INTENT still missing on disk (restore configs git 6850fa3)

### Operating rules for next CoS
- Token-efficient; dispatch Coder for Jules; Doc Bot for docs
- Merge docs without re-asking; App APPROVE for code
- WIP: Jules proofs only; do not re-open cleanup/CLI fan-out unless Mike says
- Update Mike after major teammate results
