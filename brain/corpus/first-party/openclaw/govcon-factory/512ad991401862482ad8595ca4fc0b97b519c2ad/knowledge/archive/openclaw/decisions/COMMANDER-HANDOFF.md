# COMMANDER-HANDOFF.md — State-of-the-swarm for the next Commander

**Last updated:** 2026-04-24
**Current Commander of the watch:** Claude Opus 4.7 (chief-of-staff session, worktree `suspicious-elgamal-9940b1`)
**Previous Commander:** sisyphus (Claude) — merged the greenfield refactor PR #1350 at `46d3f7de`, then antigravity pushed direct-to-main at `91e38e76`, `bb2ee375`
**Next Commander expectation:** The vendor Mike next directs. Read this, then INTENT.md, then run `ops/hooks/swarm-bootstrap.sh`, then check open PRs.

> Live doc — overwrite in place on every handoff. Past states are recoverable via `git log --follow COMMANDER-HANDOFF.md`.

---

## 1. What just happened (2026-04-22 → 2026-04-24)

- **2026-04-22:** 17-agent Gas Town topology + agnostic hive mind landed (CTX-140). Direct-to-main sisyphus commits; no PR.
- **2026-04-23:** Beads ingestion + bootstrap audit merged (#1346, #1348). Task board seeded.
- **2026-04-24 early:** Greenfield PR #1350 merged at `46d3f7de` — deleted 17 manifests citing ADR-001 (which was superseded). Parallel antigravity session pushed two direct-to-main fixes: `91e38e76` (v1-archive restore) and `bb2ee375` (semantic ledger V1→V2 merge).
- **2026-04-24 midday:** Mike directed chief-of-staff to restore the 17-agent intent, codify the operating model, and add guardrails. This PR is that work.

---

## 2. Active PRs (as of handoff)

| PR | Branch | State | Owner | Notes |
|---|---|---|---|---|
| **#1350** | (merged) | **merged at 46d3f7de** | sisyphus | Greenfield 22→5 refactor. Topology reverted by INTENT.md §2; placeholders restored in this PR. |
| **#1373** | (W18 permissions) | open | — | Allocator will tell it where to renumber. Do NOT touch in chief-of-staff PR. |
| **#1375** | (W19 semantic merge) | open | — | Superseded in part by `bb2ee375`. Do NOT touch. |
| **#1380** | (Codex) | open | codex | Left standing; do NOT touch. |
| **claude/admiring-driscoll-35802c** | (W20) | open | — | Do NOT touch. |
| **feat/chief-of-staff-operating-model-2026-04-24** | THIS PR | in-flight | chief-of-staff (Claude Opus 4.7) | See §4. |

---

## 3. Active sessions (as of handoff)

- **Dispatch orchestrator** — Opus 4.7 (1M). Primary long-running session.
- **chief-of-staff session** — Opus 4.7 in worktree `suspicious-elgamal-9940b1`. Holds merge rights until this PR lands or handoff fires.
- **Session A (local_02f9bbc2)** — Executing photo-vault plan per CTX-147. Status: pending Mike go-ahead per 48h staged-delete window.
- **witness-01 (launchd-python)** — out-of-band auditor, 15-min cadence. NOT a Claude session. Do not kill.

Assume any Claude Code session idle for >30 min is killable. Verify with `list_sessions` / `ps aux` before asserting any of the above is alive.

---

## 4. In-flight Mike decisions awaiting resolution

Listed in rough priority. None block the chief-of-staff PR landing.

1. **Placeholder vs. active for 17 recovered manifests.** Default: placeholder-unbootstrapped. Mike overrides per-agent.
2. **ADR-001 topology section vs. INTENT.md.** Proposal: INTENT.md supersedes until Mike reverses.
3. **`sisyphus` — alias or standalone.** Default: alias of `prime` in session-mode.
4. **W9 cloud-dispatch.** Mike: merge PR #1359; provision JULES_API_KEY + GEMINI_API_KEY; fire smoke Issue.
5. **W14 photo vault.** 48h staged-delete safety window per CTX-147 — Mike approves final delete.
6. **W18 restart Claude desktop.** Required for `dispatchTrustedCodeWorkspaces` changes per CTX-145.

---

## 5. Known traps for cross-vendor handoff

These are real, observed failure modes from 2026-04-22 → 2026-04-24. Do NOT repeat.

### 5.1 Direct-to-main pushes are an anti-pattern — including for "urgent" fixes

`91e38e76` and `bb2ee375` are live on main. They bypass review and CI and shatter the PR-audit trail. If your vendor (antigravity, a future vendor, or Claude in "just land it" mode) offers direct-to-main, **refuse** unless the Commander of the watch has pre-authorized that exact commit. The correct flow is: branch → PR → CI → squash-merge.

### 5.2 ADR / BUILD.md / INTENT.md precedence

- **INTENT.md** is the canonical direction doc.
- **ADR** records rationale for specific decisions and can go stale.
- **BUILD.md** records the rebuild contract and can go stale.

On conflict, INTENT.md wins. If the three disagree, the fix is an intent-amendment PR (§7 of INTENT.md), not a silent edit.

### 5.3 CTX entries aren't self-promoting to intent

A CTX entry with `status: resolved` resolves *that entry's topic*. It does **not** automatically become a rule for the next session. If a CTX ought to change INTENT.md, open an `intent-amendment` PR.

### 5.4 "Audit found placeholder unused → delete it" is wrong

Placeholders are **declared intent**. Absence of execution is not evidence of retirement. The greenfield PR deleted 17 manifests on this premise and we rebuilt them in this PR. See INTENT.md §5.

### 5.5 GitHub Issue ≠ resolution

An auditor who says "I'll file an Issue about this" and then lets the PR land **has not resolved the finding**. The options are: block the PR, or defer with a named `bootstrap_owner` and a target date recorded in the PR description. Issue-as-substitute loses the finding and accumulates drift.

### 5.6 Parallel conflicting IDs across branches

DR067 was minted simultaneously on three branches before chief-of-staff session saw them. Use `scripts/allocate_id.sh DR` (or `CTX`) **before** minting any new ID. The allocator reads main + every open PR branch.

---

## 6. Checklist for the next Commander

Run in order before taking any action on main:

- [ ] **Read this doc** (COMMANDER-HANDOFF.md) — start to finish.
- [ ] **Read INTENT.md** — start to finish. If anything surprises you, file `type: decision-request` CTX; do not act on the surprise.
- [ ] **Run `ops/hooks/swarm-bootstrap.sh`** — syncs the global pulse into ACTIVE_BRIEF.md. Verify it exits 0.
- [ ] **Run `gh pr list --state open`** — confirm which PRs are in flight. Do not auto-merge any that aren't yours.
- [ ] **Run `ps aux | grep -E "osxphotos|rsync|claude"`** — verify what's running locally before assuming state.
- [ ] **Check `.agents/memory/claims.jsonl`** — confirm your branch/worktree isn't claimed by another session.
- [ ] **Open a no-op PR** with a `type: commander-handoff` CTX entry acknowledging the watch. Only after that PR merges do you have implicit merge rights.

If any step errors, STOP and DM Mike (U03N5L8TH). Don't improvise around missing bootstrap state.

---

## 7. Hard don'ts

- Don't `git push origin main` directly. Ever.
- Don't delete manifests based on "looks unused." See INTENT.md §5.
- Don't edit ADR or BUILD.md in a way that contradicts INTENT.md without a paired INTENT.md amendment.
- Don't mint new DR / CTX IDs without running `scripts/allocate_id.sh` first.
- Don't assume the swarm is idle just because `list_sessions` is empty — witness-01 runs out-of-band.
