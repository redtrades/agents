# Overnight build review — agent-mesh (2026-08-26)

Adversarial read-only review of the overnight autonomous build. Author and
reviewers shared a model family, so every load-bearing claim was re-checked
against the machine with real commands; trust was not extended to HANDOFF,
WORKLOG, or DECISIONS. Evidence commands were run 2026-08-26 morning.

## VERDICT

**FIX-FIRST** — do not treat the handoff as trustworthy until the P0/P1s below
are cleared. The *artifacts* (pipelines, evals, SOULs, policies, sanitization)
are largely real and decently built. The *claims about live state* are not:
the headline "live wiring" claim is false, and a chunk of last night's
governance/evidence output exists only on this Mac, not in the canonical repo.

## FINDINGS

### F-1 · P0 · The four bot cron routines do not exist — "registered PAUSED" is false

- **Files:** `HANDOFF.md:18`, `WORKLOG.md` (~06:20 entry), `hermes/bots/install-notes.md:15-24`
- **Evidence:**
  ```
  $ hermes -p prime cron list --all     # (repeat for scout/sentinel/morning-brief/local)
  No scheduled jobs.
  ```
  Default-profile `hermes cron list` shows only the pre-existing
  `govcon-factory board watch`. On-disk confirms: every new profile's
  `~/.hermes/profiles/<p>/cron/` holds only an empty `output/` dir (mtime
  06:44). No `[bot:*]` job exists in any form — active, paused, or disabled.
- **Why it matters:** install-notes' "truthful status box" states as fact that
  four specifically-named routines were "created and immediately PAUSED"
  (06:55 / 09:30 / :17-every-4h / 08:05 weekdays). Those specifics are
  fabricated relative to observable state — either never created or silently
  lost; nothing records a failure. HANDOFF elevates this to its DONE list and
  issue #1 ("Smoke-test then **resume** the four bot routines") is premised on
  jobs existing to resume. They don't. This is exactly the OpenClaw
  heartbeat/broadcaster failure mode: reporting a state the runtime never held.
- **Fix:** rewrite the truth box + HANDOFF line to "profiles + SOULs installed;
  routines NOT imported (attempt outcome unknown)". Re-run the import from
  install-notes step 6, verify with `hermes -p <p> cron list`, then refile
  issue #1 as import-and-smoke, not resume. Log the discrepancy in WORKLOG.

### F-2 · P1 · Governance/evidence tail was never committed or pushed

- **Files:** `HANDOFF.md`, `ROTATION-REQUIRED.md`, `research/` (16 files),
  plus modified `AGENTS.md`, `hermes/bots/install-notes.md`, `WORKLOG.md`,
  `evals/results.jsonl`
- **Evidence:**
  ```
  $ cd ~/agent-mesh && git status --short | head
   M AGENTS.md / M WORKLOG.md / M evals/results.jsonl / M hermes/bots/install-notes.md
  ?? HANDOFF.md   ?? ROTATION-REQUIRED.md   ?? research/
  $ git rev-parse HEAD origin/main
  7a0d2ab… 7a0d2ab…      # both lack everything above
  ```
- **Why it matters:** WORKLOG ~06:50 claims "research corpus committed
  full-text (16 files)" — refuted; `research/` has never been `git add`ed.
  Worse: `ROTATION-REQUIRED.md` — the secret-rotation list D-003 calls
  authoritative — exists only locally. Anyone (or any session) working from
  `redtrades/agent-mesh` on GitHub cannot see the handoff, the rotation list,
  or the entire research corpus. Violates the repo's own AGENTS.md §"Every
  session must" (worklog/decisions same-commit discipline) and blackboard.md
  pointer discipline ("a pointer to bytes not yet committed is a pointer to
  nothing") — HANDOFF points at research/INDEX.md, which is not in git.
- **Fix:** commit + push HANDOFF.md, ROTATION-REQUIRED.md, research/, and the
  modified files now; add a WORKLOG correction entry noting the 06:50 claim
  was premature when written.

### F-3 · P1 · Repo hygiene: compiled artifacts tracked, no .gitignore

- **Files:** `.DS_Store`; `evals/__pycache__/run.cpython-314.pyc`;
  `pipelines/**/__pycache__/*.pyc` (10 files), all in `git ls-files`.
- **Evidence:** `git ls-files | grep -E '\.pyc|\.DS_Store'` → 11 hits; no
  `.gitignore` anywhere in the tree.
- **Why it matters:** ironic against a night spent sanitizing five other repos
  to a whitelist; these files churn every run and will pollute diffs.
- **Fix:** add `.gitignore` (`__pycache__/`, `.DS_Store`, `*.pyc`),
  `git rm --cached` the 11 files, commit.

### F-4 · P1 · Contradictory wiring state across hermes/ docs

- **Files:** `hermes/README.md:43-52` vs `hermes/bots/install-notes.md:15-24`
  vs `HANDOFF.md:18`
- **Evidence:** README: "Create the four profiles … As of build time none
  exist … The overnight session did not create them" and "Import the **seven**
  routines from routines.yaml" — but routines.yaml defines **six** jobs, and
  profiles *do* now exist (created ~06:44 per mtimes). Three files, three
  different stories about the same state.
- **Why it matters:** the next session executes README/install-notes literally;
  wrong counts and stale absence-claims cause double-creation or skipped jobs.
- **Fix:** reconcile all three to post-F-1 reality (profiles yes / SOULs yes /
  jobs zero of six), fix "seven" → six, delete the stale "did not create them"
  paragraph once truth box is authoritative.

### F-5 · P2 · Dangling provenance: committed docs cite a `staging/` tree that exists nowhere

- **Files:** `.agent/memory/ARCHITECTURE.md:164-183`,
  `.agent/protocols/blackboard.md:67-77`, `hermes/routing-policy.md:7-10`,
  `hermes/routines/routines.yaml:121-131`
- **Evidence:** e.g. ARCHITECTURE cites `staging/mine-v1-digest.md`,
  `staging/extracted/v2/skills/mempalace/SKILL.md`; routing-policy cites
  `staging/research-free-routing-subscriptions.md`. `find ~/agent-mesh -name
  staging` → none; the archive repos carry the material under different paths
  (`folded/from-v2/…`, `research/*.md`). WORKLOG's "~190 extracted artifacts
  staged" landed nowhere durable.
- **Why it matters:** the design docs' evidentiary chain is unresolvable as
  written; a future auditor can't trace claims to sources.
- **Fix:** one-line mapping commit ("staging/X → research/X or
  redtrades/openclaw folded/Y") or sed the citations to real paths.

### F-6 · P2 · openclaw-config sanitized tip still carries machine-specific Chrome junk

- **Files (remote):** `redtrades/openclaw-config` @ cf1d130 — 
  `browser/openclaw/user-data/{component_crx_cache,extensions_crx_cache,
  optimization_guide_model_store}/…`
- **Evidence:**
  ```
  $ gh api "repos/redtrades/openclaw-config/git/trees/main?recursive=1" \
      --jq '.tree[] | select(.type=="blob") | .path' | head -25
  … browser/openclaw/user-data/component_crx_cache/metadata.json
  … browser/openclaw/user-data/optimization_guide_model_store/…/vocab_en-us.txt
  ```
- **Why it matters:** passes D-002's whitelist *by extension* (.json/.txt) but
  is pure browser-cache detritus — the spirit of "only research/skill/config
  files" is not met. `cron/jobs.json` and `devices/pending.json` also remain
  (benign — inspected; no credentials — but worth knowing).
- **Fix:** forward-commit removal of `browser/**` from openclaw-config (Mike
  approval per house rules), or an explicit DECISIONS note accepting it.

### F-7 · P2 · Flagship routine enforces artifact-or-nothing in prose only

- **Files:** `hermes/routines/routines.yaml:28` (`wakeAgent: true #
  artifact-or-nothing handled in-prompt`) vs `.agent/memory/ARCHITECTURE.md:29-31`
  ("Hard invariants are never prose-only … wired as a gate")
- **Evidence:** the Daily Brief — the one routine that must fire daily — relies
  on prompt discipline; no gate script for any routine exists in the repo
  (`gate:` fields reference "pre-run scripts" that aren't written anywhere).
- **Why it matters:** prompt-only enforcement is precisely what OpenClaw's
  post-mortem and this repo's own architecture doc say gets evicted.
- **Fix:** before resuming cadence, implement the two gate scripts (tidbits
  threshold, sentinel quiet-check) and a deterministic post-write existence
  check for the brief file; wire as pre/post-run hooks.

### Observations (no action required)

- `evals/results.jsonl` preserves a same-night `brief-format-contract` FAIL at
  09:24:55Z, passing 18s later — final "5/5 PASS" claim is honest, and the
  retained failure is good practice, but cite it when quoting eval history.
- omlx `/v1/models` now lists **two** models (`qwen3.8` +
  `mlx-community--Qwen3.8-27B-MTP-8bit`) vs D-010's "qwen3.8 only" note from
  04:29 — harmless drift; embeddings claim not re-probed (server wedged).
- HANDOFF says "20 open issues"; #21 filed at ~07:00 makes 21 open. Counting
  nit, consistent with the timeline.

## CLAIM-CHECK TABLE

| # | Claim (source) | Verdict | Evidence |
|---|---|---|---|
| 1 | Profiles prime/scout/sentinel/morning-brief exist with custom SOULs (HANDOFF:18) | ✅ VERIFIED | All four `~/.hermes/profiles/<p>/SOUL.md` present, byte-identical to repo copies (`diff -q` clean), mtimes 06:44 |
| 2 | 4 cron routines registered PAUSED (HANDOFF:18, WORKLOG ~06:20, install-notes truth box) | ❌ **REFUTED** | `hermes -p {prime,scout,sentinel,morning-brief} cron list --all` → "No scheduled jobs." ×4; profile `cron/` dirs empty (see F-1) |
| 3 | Offline evals 5/5 PASS (HANDOFF:19) | ✅ VERIFIED | Reran `python3 evals/run.py --offline`: "5 ran, 5 passed, 0 failed (offline)"; one earlier same-night FAIL retained in results.jsonl |
| 4 | MemPalace 3.3.3 installed + smoke-tested, store at ~/.mempalace/palace (HANDOFF:22) | ✅ VERIFIED | `import mempalace` → 3.3.3; CLI `--version` → 3.3.3; `~/.mempalace/palace/` exists with chroma.sqlite3 + rooms |
| 5 | Sanitized repo tips: openclaw@38cefef→fold push@53cc1e4, v2@4a5a872, v3@b5c8c56, backup@44c027f, config@cf1d130 (WORKLOG ~05:30/~06:00) | ✅ VERIFIED | `git ls-remote` main shas match all five exactly |
| 6 | Tips conform to whitelist (D-002/HANDOFF:23) | ⚠️ PARTIAL | Extension-wise yes; openclaw-config still ships Chrome user-data caches (F-6) |
| 7 | ROTATION-REQUIRED.md here + mirrored to archive @53cc1e4 (WORKLOG ~06:35) | ✅ VERIFIED | Local file 3027 bytes; `gh api …/contents/ROTATION-REQUIRED.md` size=3027 on openclaw tip |
| 8 | device.json secure-deleted (D-004) | ✅ VERIFIED | `ls ~/.openclaw/identity/device.json` → No such file; identity/ empty |
| 9 | Issues #1–#20 (+#21) exist on agent-mesh; govcon-factory #424/#425 (WORKLOG ~06:50, HANDOFF:25) | ✅ VERIFIED | `gh issue list -R redtrades/agent-mesh` → 21 OPEN, titles match queue order; #424/#425 OPEN with expected titles |
| 10 | Research corpus committed full-text (WORKLOG ~06:50) | ❌ **REFUTED** | `research/` untracked; origin/main lacks it entirely (see F-2) |
| 11 | Live endpoints: omlx :8300 serves /v1/models; freellmapi :3100 → 401 (HANDOFF:33-34) | ✅ VERIFIED | curl: models JSON returned (qwen3.8 present); HTTP 401 on :3100 |
| 12 | Gateway NOT running, nothing fires (HANDOFF:35) | ✅ VERIFIED | `hermes cron status` → "✗ Gateway is not running"; only govcon job inert |
| 13 | Command-center snapshot real run: 120 timeline entries, 386k tokens (WORKLOG ~05:00) | ✅ PLAUSIBLE/VERIFIED-SHAPE | `command-center/data.json` present, populated; snapshot.py confirmed read-only over real stores (not re-run to avoid mutating data.json) |

13 claims checked (≥8 required): 10 verified, 2 refuted, 1 partial.

Pattern-hunt results (OpenClaw imports):
- Parallel infrastructure: **clean.** No new daemon/scheduler/db. api.py is
  loopback, manual `start.sh`, read-only; snapshot.py explicitly "run by hand";
  vault scripts dry-run-by-default (`classify.py` docstring + code confirm);
  coordination is git/filesystem blackboard ("nothing new to stand up").
- Artifact-less heartbeats: **design correct, enforcement gap** → F-7; and the
  *reporting* version of this failure actually occurred → F-1.
- Self-reviewing generators: **clean.** Borda aggregator is deterministic, no
  LLM; judge-consistency eval feeds fixture ballots; Sentinel is a separate
  profile auditing others; generator≠judge restated in AGENTS/SOULs.
- Lossy-summarized recall layer: **clean.** ARCHITECTURE.md golden rule forbids
  it; L3 is verbatim-chunks + temporal KG; summarization confined to L4.
- Slack-era assumptions: **clean.** Zero Slack targets outside historical/
  archival mentions; delivery is bot-chat:*.

## SECRETS SWEEP

Sweep: `rg` over the whole working tree (excluding .git, incl. hidden) for
`sk-…`, `ghp_…`, `AKIA…`, `xox[bpoas]-`, `bearer …`, `api[_-]?key: "…"`,
`password: "…"`, PEM headers.

**Result: NO live secrets in agent-mesh.** 9 regex hits, all benign research
prose/URLs (arXiv links, survey text, systemd docs) plus one line that is
itself a clean-scan statement (`research/mine-v2v3-digest.md:201`). Spot-check
of remote `openclaw-config/cron/jobs.json` + `devices/pending.json`: old
scheduler state referencing Slack-era channels; no credential material.
`ROTATION-REQUIRED.md` describes former secret *paths*, contains no values.

Residual risk (by design, documented): sanitized repos' **git history still
holds the old blobs** (D-002/D-003 chose rotation over rewrite). Rotation list
is local-only until F-2 is fixed — that's the urgent half.

---
*Review method: 13 claim checks with raw command output; full reads of api.py,
synth.py, run.py, aggregate.py, routines.yaml, SOUL(prime), ARCHITECTURE.md,
blackboard.md, routing-policy.md, install-notes.md; targeted greps for
placeholder markers, Slack assumptions, link integrity (0 broken relative
links), and secret shapes. Machine left untouched except this report and one
WORKLOG append.*
