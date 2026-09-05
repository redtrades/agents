# Exclusions

| Excluded material | Reason | Custodian or safe pointer |
| --- | --- | --- |
| Credentials, tokens, keys, cookies, and account exports | Secret-bearing material is never archived. | Original account owner / secret manager. |
| Executable skills, prompts, hooks, workflows, and runtime configuration | A historical file must not become active by archive presence. | Source repository at the commit in `REPOSITORY-INVENTORY.md`. |
| TDIU, P&T, SSDI, provider, claimant, and VA case material | Personal case material stays outside this archive. | Original protected case location. |
| OpenClaw runtime state, schedulers, catalogs, and full backups | Sealed reference evidence; bulk import would be unsafe and misleading. | iCloud paths in `SOURCE-INVENTORY.tsv`. |
| Forks/external prior art | Retain retrieval pointers only; preserve upstream provenance and license context. | Fork entries in `REPOSITORY-INVENTORY.md`. |
| Unrelated trading, boilerplate, and infrastructure projects | Outside the agent-history scope. | Original GitHub repository. |
| Untracked local material without a document-level review | No commit can be honestly attributed. | Original local path, marked `WORKING-TREE-ONLY`. |

No excluded source has been copied by this task.
