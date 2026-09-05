# Captured source roots

Observed: 2026-08-31. These mixed repository roots were not copied wholesale.
The archive instead captured the screened, document-level rows recorded in
`manifests/SOURCE-INVENTORY.tsv`. Runtime, configuration, executable, secret,
and personal-case material remains excluded.

| Source root | Captured evidence | Root-level handling |
| --- | --- | --- |
| `/Users/man/agent-mesh/research` | 26 screened research documents at source commit `4a663596e1188e2b25116e71b74162bc92abbd96` | Document-level capture resolved; the mixed root itself remains pointer-only. |
| `/Users/man/agent-workspace` | 22 screened historical documents at source commit `bc44e05be7c3d3f6e65c885e793c30c44b6eaa8b` | Document-level capture resolved; executable assets remain excluded. |
| `/Users/man/agent-configs` | 12 screened historical documents at source commit `6850fa3325c14d831bd1bdaa04d47dadd4c06d0c` | Document-level capture resolved; skills, prompts, hooks, and configuration remain pointer-only. |
| `/Users/man/govcon-factory` | 16 ordinary corpus documents and 41 separately routed GovCon documents at source commit `512ad991401862482ad8595ca4fc0b97b519c2ad` | Document-level capture resolved; code, runtime assets, identifiers, and personal-case material remain excluded. |

The counts above describe the current archive after the final personal-case
screen. Each captured file has a manifest checksum; the source-root pointer is
not a claim that every file under the original root was reviewed or copied.
