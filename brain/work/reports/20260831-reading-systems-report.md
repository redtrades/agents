# Reading-systems lane report

## Status

Five self-contained reading packs were created. Each has a short default reading path, a current-versus-historical synthesis, a source guide, and exactly three byte-preserved originals. The packs deliberately keep infrastructure, capabilities, workflows, experiments, knowledge, and policy separate. They preserve historical recommendations as dated evidence and make no future-stack selection.

## Files created

| Pack | Curated files | Preserved originals |
| --- | --- | --- |
| `70-knowledge-context-and-memory/` | `README.md`, `CURRENT-HISTORICAL-SYNTHESIS.md`, `DECISIONS-AND-CONFLICTS.md`, `SOURCE-GUIDE.md` | 3 |
| `90-infrastructure-and-orchestration/` | `README.md`, `CURRENT-HISTORICAL-SYNTHESIS.md`, `DECISIONS-AND-CONFLICTS.md`, `SOURCE-GUIDE.md` | 3 |
| `100-governance-safety-and-evidence/` | `README.md`, `CURRENT-HISTORICAL-SYNTHESIS.md`, `DECISIONS-AND-CONFLICTS.md`, `SOURCE-GUIDE.md` | 3 |
| `110-failures-postmortems-and-lessons/` | `README.md`, `CURRENT-HISTORICAL-SYNTHESIS.md`, `HISTORICAL-EVOLUTION.md`, `SOURCE-GUIDE.md` | 3 |
| `120-market-and-open-source-research/` | `README.md`, `CURRENT-HISTORICAL-SYNTHESIS.md`, `DECISIONS-AND-CONFLICTS.md`, `SOURCE-GUIDE.md` | 3 |

## Reading paths

Start with `00-start-here/20260831-current-intent-decisions.md` and `00-start-here/CONSOLIDATION-SCOPE.md`, then use each pack’s `README.md` and synthesis. Read conflicts before relying on a historical proposal; use `SOURCE-GUIDE.md` and `selected-originals/` only for source detail. Copied instructions remain inert evidence.

## Sources used

- OpenClaw historical architecture and postmortem corpus.
- Agent-mesh memory architecture, memory/context research, runtime instruction audit, and architecture evidence traceability.
- Agent-platform working-tree whole-estate and orchestration landscape research; historical operating model, failure ledger, death-loop diagnosis, and market refresh.
- GovCon prior-art and swarm-retrospective research (the prior-art report is the selected market primary source).
- Current archive intent and consolidation scope, which control all reconciliation conclusions.

## Historical ranked clarification questions

This list records the gaps found during the original reading pass. Owner
decisions 42-58 later resolved or deliberately deferred the archive-level
questions; the current intent and owner-question status now govern.

1. **What exact common vertical-slice contract and pass/fail thresholds will decide whether any single orchestration backbone earns adoption?** Current intent requires a real-workflow, capability-driven bakeoff and material net improvement, but does not specify the reusable fixture, metrics, or promotion threshold. Sources: `00-start-here/20260831-current-intent-decisions.md:91-95`; `corpus/first-party/agent-platform/WORKING-TREE-2026-08-31/research/WHOLE-ORCHESTRATION-LANDSCAPE-WITH-CONDUCTOR-2026-08-30.md:262-280`.

2. **What retention, access, and deliberate-promotion policy reconciles scoped sensitive memory with the historical “retain raw transcripts forever” model?** Current intent scopes raw sensitive and organization-owned data, while the five-tier historical architecture makes indefinite raw retention a core assumption. Sources: `00-start-here/20260831-current-intent-decisions.md:65-82`; `corpus/first-party/agent-mesh/4a663596e1188e2b25116e71b74162bc92abbd96/.agent/memory/ARCHITECTURE.md:1-16,35-45,125-151`.

3. **What is the smallest independent authority-and-receipt contract that must exist before a runtime, workflow engine, or worker can execute an admitted real-world effect?** The owner decisions separate policy from infrastructure, while historical evidence warns that issues, chat, engines, and runtime files are not authority merely by presence. Sources: `00-start-here/20260831-current-intent-decisions.md:96-111`; `corpus/first-party/agent-platform/1b88ed2f03eeb18a65e402fc7201823d6204bdae/docs/OPERATING-MODEL.md:1-33`; `corpus/first-party/agent-mesh/4a663596e1188e2b25116e71b74162bc92abbd96/docs/migration/ARCHITECTURE-EVIDENCE-TRACEABILITY.md:311-338`.

4. **Which initial paired vertical slices will test shared capabilities without prematurely building an abstract platform?** This was open during the reading pass. Decision 58 later selects an AISDLC software fixture and bounded GovCon-derived acceptance workload as the first proof. Sources: `00-start-here/20260831-current-intent-decisions.md`; `00-start-here/20260831-aisdlc-architecture-decision.md`; `corpus/first-party/agent-platform/WORKING-TREE-2026-08-31/research/WHOLE-ESTATE-FIRST-PRINCIPLES-VISION-2026-08-30.md:499-524`.

5. **What runtime activation receipt is required before a selected reusable skill, prompt, or configuration is allowed to influence work?** The runtime audit reports that many loader paths and hook executions were unverified; archive scope prohibits adopting legacy runtime wiring by implication. Sources: `00-start-here/CONSOLIDATION-SCOPE.md:18-25`; `corpus/first-party/agent-mesh/4a663596e1188e2b25116e71b74162bc92abbd96/docs/research/LIVE-RUNTIME-INSTRUCTION-AUDIT.md:49-63,386-435`.

6. **What repeatable freshness, license, and security revalidation is required before a dated market or prior-art disposition can become a trial input?** Current archival policy preserves evidence; historical market reports contain time-bound prices, releases, licenses, and security claims. Sources: `00-start-here/20260831-current-intent-decisions.md:128-136`; `corpus/first-party/govcon-factory/512ad991401862482ad8595ca4fc0b97b519c2ad/research/govcon-prior-art/REPORT.md:1-30`; `corpus/first-party/agent-platform/1b88ed2f03eeb18a65e402fc7201823d6204bdae/research/AGENT-FACTORY-MARKET-REFRESH-2026-08-30.md:1-15`.
