# HISTORIC-INDEX — estate roots → role → status

**Canon cold-start:** [START.md](START.md) (`/Users/man/agent-knowledge-archive/00-start-here/START.md`).  
**Hybrid policy:** physical canon here; everything else stays put with HISTORIC/freeze banners + links here.
**Evidence-mode:** [EVIDENCE-MODE.md](EVIDENCE-MODE.md) · **Briefs:** [BRIEFING-CONTRACT.md](BRIEFING-CONTRACT.md).  
**Reports sink:** [REPORTS-SINK.md](REPORTS-SINK.md).

| Root | Role | AGENTS / README | Status |
| --- | --- | --- | --- |
| `agent-knowledge-archive` | **canon** (live) | `00-start-here/START.md` | Active default branch `codex/archive-foundation` |
| `agent-configs` | **policy** (live) | `AGENTS.md` → generates `~/.agents`, `~/.codex`, `~/.claude`, `~/.hermes` | Active (`main`) |
| `agent-sdlc` | **impl** (live AISDLC) | `AGENTS.md` | Active (`main`) |
| `govcon-corpus` | **impl** (live GovCon evidence) | `AGENTS.md` | Active; no CMP private in public PRs |
| `agent-platform` + `agent-mesh` + `agent-workspace` | **SAME-ATTEMPT family** (museum) | each has freeze/`AGENTS.md` stub | Sibling superseded skins of one attempt — **not** three roles; HISTORIC/freeze; not cold-start |
| `govcon-factory` | **frozen** (museum) | `AGENTS.md` | Freeze banner; harvest-only |
| `~/agent-reports/` | **reports** (historic dump) | local `AGENTS.md` / [REPORTS-SINK.md](REPORTS-SINK.md) | Not a git repo; dumps ≠ canon; `credentials/` OK for secrets outside git |
| `~/.agents` / `~/.codex` / `~/.claude` / `~/.hermes` | **adapters** | `AGENTS.md` / `CLAUDE.md` / `SOUL.md` | Generated from `agent-configs`; CANON block → archive START |

Worktree sprawl (`*-wt`, `*-worktrees`, `~/.codex/worktrees`, `~/.worktrees`) is **not** an authority surface — see [CLEANUP-CANDIDATES.md](CLEANUP-CANDIDATES.md) (index only; no delete).
