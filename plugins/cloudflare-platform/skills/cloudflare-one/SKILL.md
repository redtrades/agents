---
name: cloudflare-one
description: "Guides Cloudflare One Zero Trust and SASE work across Access, Gateway, WARP, Tunnel, Cloudflare WAN, DLP, CASB, device posture, and identity. Use when designing, configuring, troubleshooting, or reviewing Cloudflare One deployments. Retrieval-first: use current Cloudflare docs/API schemas instead of embedded product docs."
---
# Cloudflare One

## Overview

Before citing limits, settings, API fields, category IDs, or exact UI paths, retrieve current information from the [Cloudflare One docs](https://developers.cloudflare.com/cloudflare-one/), the Cloudflare docs MCP server, or the Cloudflare API schema.
## Workflow

1. Classify the ask: architecture, configuration, troubleshooting, migration, or review.
2. Gather context: account ID, users/sites/apps, identity provider, SCIM/group sync, device management, traffic path, compliance constraints, and rollout blast radius.
3. Retrieve only the current docs needed for the products involved: Access, Gateway, WARP/device client, Tunnel/Mesh, Cloudflare WAN, DLP, CASB, device posture, or identity.
4. If account access is available, inspect existing resources before proposing or making changes: Access apps/policies/groups/IdPs, Gateway rules/lists/categories, device profiles/posture checks, tunnels/routes, DNS/resolver settings, and locations/sites.
5. Propose the change set with prerequisites, validation, and rollback. For risky changes, stage disabled or scoped to a pilot group/site unless the user explicitly asks otherwise.
## Output Defaults

- Designs: current assumptions, target architecture, product responsibilities, rollout phases, validation, and open decisions.
- Configuration work: prerequisites, exact resources to inspect/create/change, test cases, and rollback.
- Troubleshooting: traffic path, likely failure point, evidence to collect, and next test.
## Validation Prompts

- Access: test authorized, unauthorized, posture-failing, service-token, and multi-IdP flows when applicable; inspect logs and policy precedence.
- Private network access: verify route lookup, tunnel health, origin reachability, split tunnel behavior, DNS resolution, and end-to-end access from a device client test device.
- Gateway: verify rule type, action, traffic expression, precedence/evaluation phase, referenced lists, and Gateway settings before enabling broadly.
- TLS/DLP: test Do Not Inspect exceptions and root CA trust before enabling inspection; test DLP with known samples and monitor false positives before blocking.
- CASB/risk: confirm integration health, credential expiry, asset discovery, scan timing, finding instances, and risk-score signal latency before declaring remediation complete.
- Cloudflare WAN: verify tunnel health, route priority/ownership, traffic flow, firewall expression syntax, and connector/appliance telemetry where applicable.
## API Safety

- Use fully qualified MCP tool names when MCP tools are available.
- Never guess category IDs, application IDs, wirefilter fields, or API request bodies. Retrieve the current schema/docs and existing account objects.
- Do not enable broad production policies without explicit approval.

## Extended Reference & Deep Mechanics

For complete implementations, edge cases, and detailed recipes, see [references/details.md](references/details.md).
