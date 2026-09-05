# Extended Reference Details

## Source-Specific Traps

### Zscaler ZIA / SWG

- Custom URL categories often split into separate IP, domain, and URL lists. Count the generated lists, not just source categories.
- ZIA locations with IPs are useful as source IP lists; they are not automatically [Gateway DNS locations](https://developers.cloudflare.com/cloudflare-one/networks/resolvers-and-proxies/dns/locations/) for DNS policy scoping.
- GRE tunnel source IPs can inform policy conditions, but the transport migration is a separate WARP Connector or Cloudflare WAN workstream.
- CAUTION/warn behavior has no exact Gateway equivalent. Treat it as an explicit customer decision, not a silent allow/block choice.
- DLP engines and custom regex usually require manual Cloudflare DLP profile recreation. Placeholder policies must not be enabled as if DLP is complete.
- Network application groups and unsupported protocols are partial mappings. Review them before enablement.
- If SCIM is unavailable, identity-scoped source rules become overly broad unless you add an enforceable alternative such as user/email lists. Check [Gateway identity selectors](https://developers.cloudflare.com/cloudflare-one/traffic-policies/identity-selectors/) before creating those rules.

### Zscaler ZPA / Private Access

- ZPA app segments, server groups, and connector groups do not map 1:1. Cloudflare separates Access apps, tunnel routes, DNS, and policies.
- Creating tunnels through the API does not complete connector deployment. Plan cloudflared installation, authentication, and origin reachability separately.
- Create one Cloudflare Tunnel per ZPA connector group regardless of connector runtime status (AUTHENTICATED, DISCONNECTED, or disabled). Status is operational, not architectural. Tag disconnected or legacy groups in the tunnel description and let the customer decide what to decommission after validation.
- Each ZPA connector instance within a group maps to one cloudflared replica running against that tunnel's token. Match replica count to connector instance count per group to preserve the same topology. A single tunnel token supports multiple simultaneous cloudflared processes. Recommend installing replicas within the same data center but on different hosts or subnets.
- For each connector group, identify all server groups linked to it and all app segments assigned to those server groups. IP addresses and CIDRs in those app segments become CIDR routes on the corresponding tunnel; domain names become hostname routes on the same tunnel. Prefer one CIDR route per subnet over per-host /32 routes where a broad subnet covers all app segment IPs.
- ZPA bypass means split-tunnel bypass in Cloudflare, not an Access `bypass` decision. Bypass rules map to WARP [Split Tunnel](https://developers.cloudflare.com/cloudflare-one/team-and-resources/devices/cloudflare-one-client/configure/route-traffic/split-tunnels/) exclude entries. This is a manual configuration step with no API automation - the customer must add bypassed domains and IPs to the device profile split tunnel exclude list through the dashboard.
- Agentless/browser apps may become separate public-hostname Access apps per domain. WARP private apps remain private-destination apps.
- The default Cloudflare Access application destination limit is 5 hostnames per app. For ZPA migrations with large app segments, contact the Cloudflare account team to request an increase (up to 50) before implementation. Confirm the limit is active on the account before creating apps - without it, large segments must be split into multiple apps with identical policies, significantly increasing object count.
- IP-anchored apps require an explicit egress decision before migration: preserve source IP through customer egress, use Cloudflare [dedicated egress](https://developers.cloudflare.com/cloudflare-one/traffic-policies/egress-policies/) where available, or accept that the target service must be updated to allow new source IPs. This is a customer decision that blocks implementation if unresolved.
- Resolver policies can be account-wide. Be careful with overlapping private DNS namespaces across sites or virtual networks; retrieve [resolver policy](https://developers.cloudflare.com/cloudflare-one/traffic-policies/resolver-policies/) docs before making DNS changes.
- Each ZPA access policy rule maps to a Cloudflare reusable Access policy. Create all reusable policies before attaching them to Access apps. In default-deny Gateway Network environments, additionally create a Network allow rule with selector "Self-hosted Access App with Private Address is Present" (wirefilter: `any(access.private_app[*] in {"*"})`) at higher precedence than any broad L4 block rules - without it, Gateway blocks private app traffic before Access policy evaluation occurs.
- In combined ZIA and ZPA migrations, Gateway Network rules can accidentally block Access private-app traffic. The Gateway Network allow rule above is the fix - place it at higher precedence (lower number) than ZIA-migrated block rules. Add and validate this rule before enabling broad L4 blocks.

### Palo Alto / Prisma / NGFW

- One Palo Alto rule can produce multiple Cloudflare resources. Preserve rule intent, not rule count.
- App-ID, URL category, zone, HIP, schedule, and decryption behavior rarely translate exactly. Mark partial mappings rather than forcing false equivalence.
- Export address/service objects and groups with rules. Missing object exports cause silent-looking drops unless explicitly detected.
- Broad `any` destination/service rules and very broad CIDRs require manual review. Do not auto-create broad catchalls.
- HIP/device checks require Cloudflare [device posture](https://developers.cloudflare.com/cloudflare-one/reusable-components/posture-checks/) integrations before enforcement.
