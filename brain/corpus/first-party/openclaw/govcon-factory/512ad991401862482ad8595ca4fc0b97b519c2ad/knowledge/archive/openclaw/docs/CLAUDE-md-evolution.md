# CLAUDE.md — Evolution Over Time

The longitudinal "see it move" view of the OpenClaw constitution. `CLAUDE.changelog.md` records *what* changed per release in semver-row form; this document records *why* it changed — what failure mode each version was correcting and what evidence drove it — so future maintainers can see the trajectory, not just the diffs.

Read this when deciding whether a proposed CLAUDE.md change is in the spirit of where the file is heading, or when onboarding to why the constitution looks the way it does.

---

## Version table

| Version | Date | Bytes | Sections | Imperative kernel? | Headline | Commit |
|---|---|---|---|---|---|---|
| v3.0.0 | 2026-05-07 | 15,125 | 17 (§1–§17) | no | Slim rewrite — 63 KB bloat archived, DR catalog externalized | `97f73eb92` |
| v3.1.0 | 2026-05-16 | 16,255¹ | 17 (§1–§17) | no | Governance + changelog adopted (semver discipline) | uncommitted² |
| v3.2.0 | 2026-05-19 | 19,291 | 18 (§0–§17, +§2.5) | **yes** | Karpathy §0 imperative kernel + named failure modes | `c60e422ac`³ |

¹ The HEAD blob carried the v3.0 banner at 16,136 bytes; the v3.1.0 banner swap (+ pointer to the changelog) brought the working tree to 16,255. v3.1.0 never landed as its own commit.
² v3.1.0's banner edit and the entire `CLAUDE.changelog.md` were uncommitted/untracked working state. v3.2.0 is the commit that finally lands both. Governance-era sibling work (memory-governance upstream adoption) committed `c72b09bf2`, 2026-05-17.
³ v3.2.0's SHA is self-referential — see the PR / `git log -1 --format=%h -- CLAUDE.md` after merge.

---

## Diff highlights — the reasoning behind each version

### v3.0.0 — the slim treatment (2026-05-07)

**Failure it fixed:** the constitution had grown to 63 KB / 351 lines with a doubled "Hive Mind" header and the entire DR catalog inlined. Evidence: the file no longer fit comfortably in cache-anchored attention, and the inline DR catalog meant every constitution read paid for content that was canonical elsewhere (`semantic.jsonl`). Reconstructed from `97f73eb92` ("activate W1-E CLAUDE.md slim, 66KB→15KB") and the changelog's v3.0.0 row.

**What changed:** deduped the doubled header, moved the DR catalog out to `.agents/memory/semantic.jsonl` (constitution now cites pinned numbers only), archived the original as `CLAUDE.archive-2026-05-07.md` per DR135 (archive-as-lessons, never restore-as-is), and restructured into the §1–§17 layout. Net 63 KB → 15 KB.

**What it did *not* fix:** the file was now short, but still structured as *reference* — behavioral rules (assumptions, verify-before-assert, irreversible-stop) stayed buried mid-document behind DR-coded indirection. Length was solved; attention ordering was not.

### v3.1.0 — governance scaffolding (2026-05-16)

**Failure it fixed:** CLAUDE.md edits were happening without traceability — no version, no rationale trail, no enforced "every edit lands a row" discipline. Evidence: pre-v3.0 history existed only in git log with no semver tags; there was no single place to answer "what changed in the constitution and why." Reconstructed from the changelog v3.1.0 row + the Context-Governance v0 artifacts (`docs/memory-governance/*`, `scripts/hooks/memory-staleness-check.sh`, the weekly-consolidation scheduled task).

**What changed:** added the `v3.1.0 (governed)` banner + a pointer to the new `CLAUDE.changelog.md`, and placed the constitution under explicit governance — every future edit must produce a semver bump and a changelog row in the same PR. No semantic changes to §1–§17.

**What it did *not* fix:** governance now *recorded* changes but did not improve the file's *effectiveness*. The behavioral core was still mid-document and DR-indirected. And ironically, v3.1.0 itself never committed cleanly — the banner edit and changelog sat as uncommitted/untracked working state until v3.2.0, which is itself evidence that "governance exists" ≠ "governance is exercised."

### v3.2.0 — Karpathy §0 imperative kernel (2026-05-19)

**Failure it fixed:** the file was short (v3.0) and tracked (v3.1) but still structurally the opposite of what reduces model mistakes. Evidence: Brief 1 of `knowledge/research-briefs/2026-05-19-briefs.md` — Karpathy's late-Jan-2026 thread named three recurring Claude Code failure modes (silent wrong assumptions, over-complication, orthogonal damage); the packaged 4-rule single-file CLAUDE.md cut mistakes 41% → 11% (12 rules → ~3%). The mechanism: few rules, front-loaded, imperative, negative constraints, behavioral-not-procedural. OpenClaw's file had behavioral rules scattered across §2/§3/§9/§10 behind DR codes — late-document rules get dropped from attention.

**What changed:** added **§0 — Unbreakable Rules** (7 Always/Never one-liners, no DR codes inline) front-loaded above §1 so the behavioral kernel sits in cache-anchored attention; added **§2.5 — Karpathy failure modes** verbatim with good/bad examples; converted **§3** to pure imperative "Never …" constraints; inserted the **`--- REFERENCE (lookup, not behavior) ---`** divider before §15 so pointers/taxonomy/tracing fall below the high-attention region; added one explicit negative constraint each to §6 and §8. Net 16,255 → 19,291 bytes (+3,036). No DR pin numbers changed; no DR codes invented.

**Deliberate non-change:** did *not* cut to 4 KB. Hermes (local second opinion) pushed for 4–5 KB / 6–8 sections, but the swarm has irreducible governance surface (§6 GitHub-as-truth, §7 memory hygiene, §8 destructive gates, §9 three-bucket) that a generic 4-rule file can't carry. v3.2.0 captures most of the 41%→11% mechanism (front-load + imperative + negative constraints + demote reference) *without* discarding swarm-specific governance. This is the explicit trade-off recorded for future maintainers tempted to "just make it 4 rules."

---

## Pending v3.3+ candidates

A home for improvements identified but not yet executed, so they don't get lost:

- **§4 routing demotion** — Brief 1 flagged §4 (routing tables, model enums) as reference material that could move below the `--- REFERENCE ---` divider alongside §15–§17. Held back from v3.2.0 to keep that release scoped to the §0 kernel; revisit once the §0 ordering has been observed in practice.
- **Negative-constraint pass on §7** — §6 and §8 got an explicit "Never X" line in v3.2.0; §7 (memory hygiene) is still all-positive guidance and a strong candidate for the same treatment (e.g. "Never batch CTX appends across turns").
- **Good/bad examples beyond §2.5** — Hermes recommended one good/bad example per *critical* section, not just the Karpathy modes. §6 (Issue-before-branch) and §8 (one-step-destructive) are the next best candidates.
- **Empirical validation** — the 41%→11% figure is Karpathy's, on a generic single-file CLAUDE.md, not measured on the OpenClaw swarm. A v3.3 candidate is instrumenting the three failure modes (silent assumption / over-complication / orthogonal damage) as a tagged-incident counter so the next constitution change has *our* evidence, not borrowed evidence.
- **§0 attrition check** — track whether 7 rules is the right count. Karpathy's data suggests 4 rules → 11%, 12 rules → ~3%; if instrumentation shows §0 rules being dropped, the count or wording is wrong, not the concept.

When one of these is executed, move it out of this section and add the reasoning to "Diff highlights" under its version.

---

*Maintained alongside `CLAUDE.changelog.md` under the Context-Governance workstream. The changelog is the row-per-release ledger; this is the narrative. Update both in the same PR as any CLAUDE.md change.*
