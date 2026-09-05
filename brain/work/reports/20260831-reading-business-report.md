# Business reading-pack report

Date: 2026-08-31
Status: completed synthesis lane; current decisions are distinguished from historical evidence.

## Files created

Seven self-contained reading packs were created under the assigned paths:

| Pack | Reading files | Byte-preserved selected originals |
| --- | ---: | ---: |
| `10-intent-and-north-star/` | 4 | 2 |
| `20-personal-operator-os/` | 4 | 3 |
| `50-declarative-company-factory/` | 4 | 3 |
| `60-business-domains/govcon/` | 4 | 3 |
| `60-business-domains/intelligence-and-news/` | 4 | 3 |
| `60-business-domains/idea-and-market-discovery/` | 4 | 2 |
| `60-business-domains/trading-and-research/` | 4 | 3 |

Each pack has `README.md`, `CURRENT-HISTORICAL-SYNTHESIS.md`,
`DECISIONS-AND-CONFLICTS.md`, `SOURCE-GUIDE.md`, and a three-to-four-file
`selected-originals/` set (two to four retained files after the case-material
screen). No future infrastructure or platform implementation
has been selected as a current build. The normal GovCon pack only points to the
restricted annex; it does not reproduce its plan, financial, GTM, outreach, or
council details.

## Default reading paths

Every pack uses the same short path:

1. `README.md`
2. `CURRENT-HISTORICAL-SYNTHESIS.md`
3. `DECISIONS-AND-CONFLICTS.md`
4. `SOURCE-GUIDE.md` only when deeper provenance is needed.

## Source corpus used

- Current owner decisions: `00-start-here/20260831-current-intent-decisions.md` and `00-start-here/CONSOLIDATION-SCOPE.md`.
- OpenClaw historical intent, first-principles architecture, and postmortems under `corpus/first-party/openclaw/govcon-factory/512ad991401862482ad8595ca4fc0b97b519c2ad/knowledge/archive/openclaw/`.
- Whole-estate reconstruction: `corpus/first-party/agent-platform/WORKING-TREE-2026-08-31/research/WHOLE-ESTATE-FIRST-PRINCIPLES-VISION-2026-08-30.md`.
- GovCon decisions, factory contract, and failure history under `corpus/first-party/govcon-factory/512ad991401862482ad8595ca4fc0b97b519c2ad/`.
- Agent-mesh intent, idea-factory, intake, GovCon-overlap, and trading research under `corpus/first-party/agent-mesh/4a663596e1188e2b25116e71b74162bc92abbd96/`.
- Sensitive-boundary inventory: `work/reports/20260831-govcon-openclaw-corpus-report.md` and `manifests/fragments/govcon-openclaw.tsv`.

## Historical ranked clarification questions

This list records the gaps found during the original reading pass. Current
intent decisions 43-58 now govern: the AISDLC first slice is selected, later
portfolio sequencing remains evidence-gated, the GovCon offer is reopened, the
integrated operator outcome and shared company contract are resolved, and
trading is parked.

1. **Which two or more paired/portfolio vertical slices should be validated first, and what outcome/metric decides their order?** This was open during the reading pass. Decision 58 later selects an AISDLC software fixture and bounded GovCon-derived acceptance workload as the first proof; later portfolio order remains evidence-gated. Sources: `00-start-here/20260831-current-intent-decisions.md`; `00-start-here/20260831-aisdlc-architecture-decision.md`; `corpus/first-party/govcon-factory/512ad991401862482ad8595ca4fc0b97b519c2ad/DECISIONS.md:47-52`.
2. **Is the historical GovCon commercial shape still a live hypothesis, or must its offer, price, exclusivity, and customer-contact assumptions be reopened before any validation slice?** The archive preserves a single-packet position and a temporary exclusivity default, but the reboot requires formal conflict resolution and defers business investment. Sources: `00-start-here/20260831-current-intent-decisions.md:32-34,115-121`; `corpus/first-party/govcon-factory/512ad991401862482ad8595ca4fc0b97b519c2ad/DECISIONS.md:26-31,145-150`.
3. **What is the first operator-OS outcome to test: decision support, a concise intelligence brief, or a research artifact, and what interruption threshold makes a proactive surface worthwhile?** Current intent commits to proactivity but does not select the first outcome or threshold. Source: `00-start-here/20260831-current-intent-decisions.md:77-87,115-121`.
4. **What is the smallest declarative company contract that must be shared before domain extensions diverge?** The current direction names a small stable core and typed extensions, but it does not name the minimal required fields or the boundary between definition and imperative process. Sources: `00-start-here/20260831-current-intent-decisions.md:52-61`; `corpus/first-party/agent-platform/WORKING-TREE-2026-08-31/research/WHOLE-ESTATE-FIRST-PRINCIPLES-VISION-2026-08-30.md:60-67,164-199`.
5. **What research-only trading artifact, if any, has an approved hypothesis, data-entitlement boundary, and usefulness metric?** The history supports read-only deterministic research and explicitly bars auto-execution, but no current experiment is defined. Sources: `00-start-here/20260831-current-intent-decisions.md:38-50,115-121`; `corpus/first-party/agent-mesh/4a663596e1188e2b25116e71b74162bc92abbd96/research/research-trading-polymarket.md:87-92,125-143`.
