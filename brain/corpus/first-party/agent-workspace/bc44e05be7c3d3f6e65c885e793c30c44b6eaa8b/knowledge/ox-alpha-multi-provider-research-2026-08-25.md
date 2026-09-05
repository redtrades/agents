# Ox Alpha multi-provider maximization — research + partial wiring, 2026-08-25

Tracking issue: [redtrades/agent-configs#12](https://github.com/redtrades/agent-configs/issues/12), self-assigned.

Goal: use every provider that serves the free Ox Alpha stealth-preview model, not
just the OpenRouter path already wired (`~/agent-reports/ox-alpha-setup/ox-alpha-setup-2026-08-21.md`),
to maximize free token throughput before the free window closes.

## Bottom line

Four providers confirmed serving Ox Alpha free, via primary sources. One (OpenRouter)
was already wired 2026-08-21. The other three cannot be wired today — each requires
a new account, and creating accounts on Mike's behalf is a hard-prohibited action for
this agent. Everything short of that is done: endpoint, model-id-format, rate limits,
and retention terms are documented per provider, and a ready-to-run registration
recipe is below for whichever account Mike sets up first. A live gateway-config risk
unrelated to the new providers was also found while verifying the existing OpenRouter
entry — see "Finding: profile drift on the existing entry" below; not fixed, flagged only.

## Providers found (primary-sourced)

| Provider | Model ID | Endpoint | Confirmed via |
|---|---|---|---|
| **OpenRouter** (wired 2026-08-21) | `stealth/ox-alpha` | `openrouter.ai` OpenAI-compatible | openrouter.ai/stealth/ox-alpha (fetched live) |
| **OpenCode Zen** | `x-preview-f-free` | `https://opencode.ai/zen/v1/chat/completions` | opencode.ai/docs/zen/ (fetched live) |
| **Nous Portal** | unconfirmed exact string — see below | `https://inference-api.nousresearch.com/v1` | portal.nousresearch.com (browsed live: "Ox Alpha" listed FREE in both the promo rail and the full model table) + portal's own OpenAPI docs (fetched live) + [@NousResearch](https://x.com/NousResearch/status/2090899914700054780) |
| **Cline** | unconfirmed | `https://api.cline.bot/api/v1` (OpenAI-compatible) | [@cline](https://x.com/cline/status/2090854216399220985) ("Ox Alpha ... now free in Cline ... use /models to see it under Free options") + docs.cline.bot |

Two more names came up repeatedly across SEO/blogspam aggregator sites
(TokenRa, a generic "playground" claim) that I could not verify against any
primary source (official docs, official X account, or a working endpoint) —
treated as unconfirmed and excluded, per `verify-before-asserting`.

### Per-provider detail

**OpenCode Zen** — auth: create account at `opencode.ai/auth`, generate API key
(free signup, no payment method confirmed required for the free model
specifically — OpenCode's own page doesn't state one either way). Retention:
OpenCode's page claims "zero-retention policy, no training" — this directly
conflicts with OpenRouter's own page for the identical underlying model
("retained by the provider, not used for training"), a conflict already
flagged in the 2026-08-21 setup note. Given the model itself is an anonymous
stealth provider, OpenCode's zero-retention claim is unverifiable independent
of that anonymous provider's own conduct — per this task's instruction,
treated as retaining regardless of the claim: **Default profile only, never
`notrain`.** Rate limits: not published. Free-window evidence: OpenCode's own
Zen page says "for a limited time," no date; OpenCode's original launch post
(`x.com/opencode/status/2090544355824038300`) said "free for the next week"
from 2026-08-20 — the same ~2026-08-27 working assumption as the OpenRouter
path, not independently confirmed.

**Nous Portal** — auth: create account at `portal.nousresearch.com`, generate
API key (standard path). A second auth mode exists — x402 (Solana USDC
micropayments, no account) — irrelevant here since Ox Alpha is priced at $0.
Rate limits are the one provider here with a **published, concrete number**:
free-tier API keys get 50 RPM / 500,000 TPM (paid tiers get more; irrelevant
for a $0 model). Retention: not stated on the portal's public pages for
third-party-hosted models specifically; treat as retaining, Default-only, same
as the others. **Model ID unresolved**: probed the live API
(`inference-api.nousresearch.com/v1/chat/completions`) unauthenticated with
several candidate ids —
```
"ox-alpha"                 -> 404 "not found in configuration or OpenRouter catalog"
"stealth/ox-alpha"         -> 400 "Unknown model" (different error — likely the
                               right shape, but resolution needs a valid key)
"openrouter/stealth/ox-alpha", "opencode/ox-alpha", "x-preview-f-free",
"ox_alpha", "OxAlpha"      -> all 404 same as above
```
Best guess is `stealth/ox-alpha` (matches OpenRouter's own id, and the error
text explicitly mentions checking "our configuration or OpenRouter catalog,"
implying Nous proxies third-party models through the OpenRouter namespace).
Confirming this needs a real account key — didn't create one.

**Cline** — confirmed to exist only via Cline's own product account
(`app.cline.bot`) and its CLI (`npm i -g cline`, `/models`). `docs.cline.bot`'s
static model-reference page does not list Ox Alpha (it's evidently populated
into the live `/models` picker dynamically, not committed to the docs site).
Cline's OpenAI-compatible endpoint (`api.cline.bot/api/v1`) is documented for
general custom-provider use, but the exact model id Ox Alpha is registered
under in Cline's own catalog is unconfirmed without an account. Retention:
Cline's own privacy notice does not state whether Zero Data Retention applies
to their own routed traffic — explicitly "provider-dependent," which for an
anonymous stealth model means unverifiable — Default-only if wired.

## Accounts Mike must create (not created by this agent)

Creating accounts on Mike's behalf is on the hard-prohibited list regardless
of scope or instruction — listing only, per the task's own instruction:

1. **OpenCode** — `opencode.ai/auth`
2. **Nous Research / Nous Portal** — `portal.nousresearch.com`
3. **Cline** — `app.cline.bot`

Each needs: sign up, generate an API key, hand the key to whichever session
does the DB registration (or drop it somewhere this agent can read locally —
Mike's call, not specified here).

## Ready-to-run wiring recipe (once a key exists)

Follows the OpenRouter precedent in `ox-alpha-setup-2026-08-21.md` exactly —
SQLite catalog rows in `~/agent-reports/freellmapi-install/freellmapi/server/data/freeapi.db`,
Default profile (id 1) only, explicit denial from `notrain` (id 2):

```sql
-- 1. Register the key (once Mike hands it over) via the existing keys route/UI,
--    not by hand-inserting encrypted_key/iv/auth_tag (those fields are
--    encrypted by the running server, not something to construct by hand).
--    Use the dashboard's "Add API key" flow, platform = the new provider name,
--    exactly like every other key in api_keys today.

-- 2. Register the model (id/context/capability numbers per the provider table above):
INSERT INTO models (platform, model_id, display_name, intelligence_rank, speed_rank,
                     context_window, enabled, supports_vision, supports_tools, key_id)
VALUES ('<platform>', '<model_id>', 'Ox Alpha (stealth preview, free) — <platform>',
        1, 1, 1048576, 1, 1, 1, (SELECT id FROM api_keys WHERE platform='<platform>' LIMIT 1));

-- 3. Fallback chain (priority puts it in the auto-rotation the router already does —
--    see server/src/lib/fallback-loop.ts, no new mechanism needed):
INSERT INTO fallback_config (model_db_id, priority, enabled)
VALUES ((SELECT id FROM models WHERE platform='<platform>' AND model_id='<model_id>'), 1, 1);

-- 4. Default profile only:
INSERT INTO profile_models (profile_id, model_db_id, priority, enabled)
VALUES (1, (SELECT id FROM models WHERE platform='<platform>' AND model_id='<model_id>'), 1, 1);

-- 5. Explicitly disabled in notrain, matching the OpenRouter entry's pattern
--    (belt-and-suspenders against the profile-drift bug below):
INSERT INTO profile_models (profile_id, model_db_id, priority, enabled)
VALUES (2, (SELECT id FROM models WHERE platform='<platform>' AND model_id='<model_id>'), 999, 0);
```

Rotation/fallback: **no new mechanism needed.** FreeLLMAPI's router
(`server/src/lib/fallback-loop.ts`) already does per-key cooldown, per-model
failure benching (3 failures in 15 min → 10 min bench), and priority-ordered
fallback across every model in a profile — confirmed by reading the module,
not assumed (adopt-over-build check per `no-parallel-infrastructure.md`:
nothing new to build here, just add rows). Once two or more Ox Alpha entries
exist in the Default profile at the same priority tier, `auto:<profile>`
routing already spreads/falls-through across them on rate-limit or failure —
this is the existing behavior every other multi-key/multi-platform model in
the catalog already gets, not a new feature.

Usage/quota visibility: **no new infra needed either.** The gateway already
logs every request to `requests` (platform, model_id, tokens, latency,
status, timestamp) and tracks live remaining-quota where a provider exposes
it in response headers via `provider_quota_state`/`provider_quota_observations`.
A per-provider burn report is a `SELECT ... GROUP BY platform` away, e.g.:

```sql
SELECT platform, COUNT(*) AS calls, SUM(input_tokens) AS in_tok,
       SUM(output_tokens) AS out_tok, MAX(created_at) AS last_call
FROM requests WHERE model_id LIKE '%ox-alpha%' OR model_id = 'x-preview-f-free'
GROUP BY platform;
```

## Finding: profile drift on the existing OpenRouter entry (not fixed, flagged only)

While verifying sensitivity enforcement still holds for the existing
`stealth/ox-alpha` entry (id 348) before modeling new entries on it, live DB
state does not match the 2026-08-21 setup note's claim of "Default profile
only, explicitly not in notrain":

```
profile_id 1 (Default)   priority 333  enabled 1   <- matches the note
profile_id 2 (notrain)   priority 258  enabled 0   <- present but disabled, so not reachable
profile_id 3 (code)      priority 1    enabled 1   <- NOT in the note, live and reachable
profile_id 4 (business)  priority 258  enabled 1   <- NOT in the note, live and reachable
```

Two different explanations, not resolved here:

1. **Catalog-sync bloat** — already logged in
   [[project_freellmapi_profile_drift_2026_08_24]] memory: `ensureAllModelsInProfiles()`
   (`server/src/services/catalog-sync.ts`) sweeps every model into every
   profile on sync, contradicting the curated lists `gateway.mjs` documents
   in its own comments. This would explain the `business` membership.
2. **Deliberate design** — `gateway.mjs`'s own comment for the `code` pool
   reads: `"code" -> forced to auto:code (Ox Alpha only, profile "code")` —
   phrased as the pool's intended, documented backing model, not as an
   artifact of drift. If that comment reflects a real decision, `code`
   membership is correct and `business` is the actual anomaly.

Either way this is a pre-existing condition, not something this task
introduced, and not something I changed — code/business pools are for
`X-Sensitivity: code`/`business`-labeled traffic, a live routing decision
Mike or another session already made, and DONT.md's "curation when told to
adopt everything" / observer-rule both argue against silently rewriting
someone else's routing config on a hunch about which explanation is right.
**Flagging for Mike's call**, not resolved: the `business` profile
membership in particular sends Ox Alpha traffic into the pool documented as
reserved for "Mike's proprietary business content" — worth a deliberate
yes/no, not an assumption either way.

For the **new** entries prepared above, the same drift risk applies: the
next catalog-sync run may sweep them into `code`/`business` the same way,
regardless of the explicit Default-only/notrain-disabled rows inserted at
registration time. The mitigation used above (explicit disabled row in
`notrain`) doesn't cover `code`/`business` — worth deciding, when wiring for
real, whether to add the same explicit-disable rows for those two profiles
too, pending Mike's read on the finding above.

## Sensitivity enforcement — mechanism confirmed generic, not re-tested per-provider

`gateway.mjs`'s three-layer enforcement (hard denylist reroute, source-label
routing, PII backstop) operates purely on the `X-Sensitivity` header and
request-body pattern matching — it has no per-model or per-platform logic at
all (confirmed by reading the current file, not re-derived from the
2026-08-21 note). A request that resolves to `notrain`/`code`/`business` gets
its `model` field hard-rewritten to `auto:<pool>` before forwarding,
regardless of what the caller asked for — so a new provider's exposure is
entirely a function of which profiles its `profile_models` rows land in, not
of anything provider-specific. Given none of the three new providers can be
wired without a key, there's no live entry to run the per-provider denylist
test against yet; the mechanism itself needs no new testing since nothing
provider-specific was added to it. Re-run the one-request denylist test from
the 2026-08-21 note against each new provider once it's actually wired.

## Free-window expiry evidence, per provider

All four trace to the same root claim — OpenCode's 2026-08-20 launch post
saying "free for the next week" — repeated by every provider's own
announcement (Cline's and Nous Research's X posts both link back to the same
week-long framing, not an independently-set date). No provider's own docs
page states a hard cutoff. Treat 2026-08-27 as the working assumption across
all four, same caveat as the original OpenRouter setup: not a
provider-confirmed date, just Mike's stated week-long timeframe applied
uniformly. Re-check before then.
