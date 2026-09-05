# DECISIONS — agent-configs

A new significant decision gets an entry here in the same PR that makes
it, not a follow-up. Format matches `govcon-factory/DECISIONS.md`. Read
this before re-litigating anything that looks settled.

### D-001: Merge authority is tiered, not uniformly reserved to Mike

- **Date:** 2026-08-25
- **Decision:** `MASTER-GUIDE.md` §2 point 4 and §8 amended from a flat
  "Mike merges every PR, even low-stakes ones" rule to a tiered policy:
  **Tier 0** (docs/evidence/runs — research writeups, dated reports,
  log/evidence files, non-governing documentation) auto-merges on CI
  green, no reviewer-bot approval required. **Tier 1** (code — scripts,
  hooks, pipeline/application code, skill implementations) auto-merges
  on CI green **and** reviewer-bot approval. **Tier 2** (governing docs —
  plans, SOPs, gate thresholds, `MASTER-GUIDE.md` itself, `DONT.md`, any
  file under `rules/`) still requires Mike to merge personally,
  regardless of CI/bot status — no agent merges this tier, ever.
- **Provenance:** Mike's explicit ruling, 2026-08-25 — quote: "delegate
  merges" — given in response to the guide's reserved-merge rule being
  surfaced to him with the conflict explained (the reserved-merge rule
  blocked routine low-stakes merges from ever proceeding without him,
  which didn't scale as PR volume grew). This supersedes the prior
  reserved-merge clause in §8 and the §2 point 3 blocked-delegation
  signal from 2026-08-24 (an attempt to delegate merge authority to a
  subagent was blocked by the session's own auto-mode classifier). That
  signal is retained in §2 point 3 as history, not deleted — it's now
  annotated as resolved by this owner ruling, reached through the proper
  channel: surfaced to Mike → conflict explained → he explicitly ruled.
  It was not silently routed around.
- **Alternatives considered and rejected:** Leaving the flat rule in
  place and having agents route every merge through Mike regardless of
  stakes — rejected per his own ruling; the reserved-merge rule was
  originally a reasonable default under uncertainty, but scaling PR
  volume made it a bottleneck disproportionate to the actual risk of
  Tier 0/1 changes. Silently reinterpreting the blocked-delegation
  classifier signal as stale without surfacing it — rejected: the signal
  was a real, deliberate guardrail (MASTER-GUIDE.md §2 point 3, written
  the day it was hit), and overriding it required his explicit sign-off,
  not an agent's own judgment call that it no longer applied.
- **Status:** active. This PR amends the policy only — it does not itself
  exercise Tier 0/1 delegated-merge authority; Mike merges this PR
  personally as the final Tier-2 act that activates the new policy
  (`MASTER-GUIDE.md` is itself Tier 2).
- **Source:** `MASTER-GUIDE.md` §2 point 3/4, §8; Mike's 2026-08-25
  ruling ("delegate merges").
