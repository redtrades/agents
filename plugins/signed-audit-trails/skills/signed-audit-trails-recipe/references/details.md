# Signed Audit Trails: Cryptography & Architecture Reference

## How the cryptography works

Three invariants make receipts verifiable offline across any conformant
implementation:

1. **JCS canonicalization (RFC 8785)** before signing. Keys sorted,
   whitespace minimized, strings NFC-normalized. Two independent
   implementations produce byte-identical signing payloads for the same
   receipt content.
2. **Ed25519 signatures (RFC 8032)** over the canonical bytes.
   Deterministic, fixed-size, no nonce dependency.
3. **Hash chain linkage.** Each receipt's `parent_receipt_hash` is the
   SHA-256 of the predecessor's canonical form. Insertions, deletions, and
   reorderings break later receipts.

For the formal wire format see
[draft-farley-acta-signed-receipts](https://datatracker.ietf.org/doc/draft-farley-acta-signed-receipts/).

## Cross-implementation interop

The receipt format has four independent implementations today:

| Implementation | Language | Use case |
|----------------|----------|----------|
| [protect-mcp](https://www.npmjs.com/package/protect-mcp) | TypeScript | Claude Code, Cursor, MCP hosts |
| [protect-mcp-adk](https://pypi.org/project/protect-mcp-adk/) | Python | Google Agent Development Kit |
| [sb-runtime](https://github.com/ScopeBlind/sb-runtime) | Rust | OS-level sandbox (Landlock + seccomp) |
| APS governance hook | Python | CrewAI, LangChain |

A receipt produced by any of them verifies against
[`@veritasacta/verify`](https://www.npmjs.com/package/@veritasacta/verify).
The auditor does not need to trust the operator's tooling choice: the format
is the contract.

## CI/CD integration

Gate merges on receipt chain verification so no build lands with a broken
evidence chain:

```yaml
# .github/workflows/verify-receipts.yml
name: Verify Decision Receipts
on: [push, pull_request]

jobs:
  verify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '20' }
      - name: Run governed agent
        run: python scripts/run_agent.py > receipts.jsonl
      - name: Verify receipt chain
        run: npx @veritasacta/verify receipts.jsonl
```

Archive the receipts as an artifact so the chain survives beyond the job run:

```yaml
      - name: Upload receipts
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: decision-receipts
          path: receipts/
```

## Composition with SLSA provenance for agent-built software

When Claude Code builds and releases software (running `npm install`,
`npm build`, `npm publish` as tool calls), the receipt chain is the
per-step build log. SLSA Provenance v1 has an extension point for this: the
`byproducts` field can reference the receipt chain alongside the build
attestation.

The [agent-commit build type](https://refs.arewm.com/agent-commit/v0.2)
documents the pattern using the ResourceDescriptor shape:

```json
{
  "name": "decision-receipts",
  "digest": { "sha256": "..." },
  "uri": "oci://registry/org/build-xyz/receipts:sha256-...",
  "annotations": {
    "predicateType": "https://veritasacta.com/attestation/decision-receipt/v0.1",
    "signerRole": "supervisor-hook"
  }
}
```

The SLSA provenance is signed by the builder identity; the receipt
attestation is signed by the supervisor-hook identity. Two trust domains,
cross-referenced at the byproduct layer. See
[slsa-framework/slsa#1594](https://github.com/slsa-framework/slsa/issues/1594)
for the composition discussion.

## Common pitfalls

**Private key in version control.** The generated `./protect-mcp.key` must
not be committed. The examples above add it to `.gitignore`. If a key is
accidentally committed, rotate immediately (delete the key file and let the
hook regenerate on next run).

**Hook command quoting.** The hooks receive `$TOOL_NAME` and `$TOOL_INPUT`
as environment variables. Keep the quoting `"$TOOL_INPUT"` so inputs with
spaces or special characters pass through intact.

**Receipts directory in CI.** If Claude Code runs in CI, upload receipts as
an artifact at the end of the job or the chain is lost at job end.

**Policy is missing.** The example `PreToolUse` hook uses
`--fail-on-missing-policy false` so an absent `./protect.cedar` does not
break Claude Code out of the box. Remove this flag in production so a
missing policy is treated as a hard failure.

## Related in this marketplace

- [`protect-mcp`](../../protect-mcp/) — the runtime hook implementation
  (use this plugin in production)
- [`review-agent-governance`](../../review-agent-governance/) — require
  human approval before review-surface actions; composes with protect-mcp

## References

- [`draft-farley-acta-signed-receipts`](https://datatracker.ietf.org/doc/draft-farley-acta-signed-receipts/) — IETF draft, receipt wire format
- [RFC 8032](https://datatracker.ietf.org/doc/html/rfc8032) — Ed25519
- [RFC 8785](https://datatracker.ietf.org/doc/html/rfc8785) — JCS
- [Cedar policy language](https://docs.cedarpolicy.com/)
- [protect-mcp on npm](https://www.npmjs.com/package/protect-mcp)
- [@veritasacta/verify on npm](https://www.npmjs.com/package/@veritasacta/verify)
- [in-toto/attestation#549](https://github.com/in-toto/attestation/pull/549) — Decision Receipt predicate proposal
- [agent-commit build type](https://refs.arewm.com/agent-commit/v0.2) — SLSA provenance for agent-produced commits
- [Microsoft Agent Governance Toolkit](https://github.com/microsoft/agent-governance-toolkit) (`examples/protect-mcp-governed/`)
- [AWS Cedar for Agents](https://github.com/cedar-policy/cedar-for-agents)
