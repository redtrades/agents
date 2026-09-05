# Cheap Intake Pipeline for X (Twitter) Bookmarks/Likes + Article Saving

**Researched:** 2026-08-26 · **Scope:** lowest-cost, free-tier-preferred avenues for getting Mike's daily X bookmarks/likes + saved articles into a local AI research/synthesis pipeline (topics → takeaways → summaries → tidbits surfaced through the day). All pricing verified against live sources on this date unless noted.

---

## 1. Official X API in 2026 — current state

### What changed
X killed subscription tiers for new developers. Since **February 6, 2026**, new developers get **pay-per-use credits only**: buy credits upfront in the Developer Console, get debited per resource fetched. The old Free / Basic ($200/mo) / Pro ($5,000/mo) ladder is closed to new signups; remaining Basic subscribers were auto-migrated starting June 1, 2026 ([postproxy.dev](https://postproxy.dev/blog/x-api-pricing-2026/), [api.sorsa.io](https://api.sorsa.io/blog/twitter-api-pricing-2026)). A final rate change landed **April 20, 2026** ([devcommunity.x.com announcement](https://devcommunity.x.com/t/x-api-pricing-update-owned-reads-now-0-001-other-changes-effective-april-20-2026/263025), via [blotato.com](https://www.blotato.com/blog/twitter-api-pricing)).

### Current rate card (verified on official docs, [docs.x.com/x-api/getting-started/pricing](https://docs.x.com/x-api/getting-started/pricing))
| Operation | Cost |
|---|---|
| Post read (standard) | $0.005/resource |
| User read | $0.010/resource |
| **Owned Reads — `GET /2/users/{id}/bookmarks`** | **$0.001/resource** |
| **Owned Reads — `GET /2/users/{id}/liked_tweets`** | **$0.001/resource** |
| Post create | $0.015/request ($0.20 if it contains a URL) |

**The critical fact for this project:** Owned Reads price your *own* app reading *your own* data at **$0.001/resource (1,000 resources = $1)**, and both the bookmarks endpoint and liked-tweets endpoint qualify when `{id}` matches the authenticated user who owns the developer app ([docs.x.com Owned Reads table](https://docs.x.com/x-api/getting-started/pricing)). Other details verified from the same page and the endpoint spec ([docs.x.com/x-api/users/get-bookmarks](https://docs.x.com/x-api/users/get-bookmarks)):

- Bookmarks endpoint: OAuth 2.0 user token, scopes `bookmark.read users.read tweet.read`, `max_results` up to **100 posts/page**, cursor pagination.
- All reads are **deduplicated within a 24-hour UTC window** (soft guarantee) — re-polling the same bookmarks same-day is mostly free.
- Pay-per-use caps at **3 million post reads/cycle** (irrelevant here); you can set a hard **spending limit** per billing cycle so runaway cost is impossible; auto-recharge is optional and off by default behavior-wise.
- No free tier for new signups — even `GET /2/users/me`-only access is gone. Minimum viable spend = whatever your first credit top-up is (small denominations accepted; no subscription).

### Realistic cost model for Mike
- 30–100 bookmarks/day → 900–3,000 owned reads/month → **$0.90–$3.00/month**, trending toward the low end because 24-hour dedup means incremental polling mostly bills only *new* bookmarks.
- One-time cost: developer-account setup (verified phone), Project + App creation, one OAuth 2.0 PKCE dance to mint a user token with offline refresh.
- **Verdict for a solo budget: genuinely viable now.** This is the first time since 2023 the official API has been the *cheapest reliable* path for self-data ingestion. Caveats: (a) pricing has changed repeatedly and can again — keep the spending limit set low; (b) a known platform ceiling means the bookmarks endpoints return roughly the **most recent ~800 bookmarks**, not the full history — reported by both [stashr.me](https://stashr.me/blog/export-x-bookmarks) ("both usually stall around the first 800") and [xarchive](https://github.com/sytelus/xarchive/) ("the API v2 caps at 800 with no folder support"). Design implication: **poll frequently (daily) rather than bulk-backfilling**; deep history must come from a one-time extension export (§2).

---

## 2. Unofficial / alternative avenues — honestly assessed

| Avenue | Mechanism | Cost | Reliability | ToS/legal risk |
|---|---|---|---|---|
| **Browser-extension bookmark exporters** ([xarchive](https://github.com/sytelus/xarchive/), [prinsss/twitter-web-exporter](https://github.com/prinsss/twitter-web-exporter), [displace-agency/x-bookmarks-exporter](https://github.com/displace-agency/x-bookmarks-exporter), several Chrome Web Store tools e.g. [X Bookmarks Exporter](https://chromewebstore.google.com/detail/x-bookmarks-exporter-expo/abgjpimjfnggkhnoehjndcociampccnm)) | Extension/userscript reads your logged-in `x.com/i/bookmarks` page (or replays internal GraphQL with your cookies), paginates, exports CSV/JSON/XLSX/MD locally | Free | Works today; ~3s/page pacing; hits the same ~800-recent practical wall; breaks whenever X ships GraphQL changes (endpoint IDs rotate) | Formally violates X automation rules (unofficial GraphQL access); practically low risk because it's your own data at human speed — **but see Nitter below: X's legal posture hardened sharply this week** |
| **Takeout-style archive export** | Settings → Your account → Download an archive of your data | Free | Snapshot only (~24h build); fine for one-time likes/posts backup | None — official channel |
| ⚠️ **But: the archive contains NO bookmarks** — posts, likes, DMs, followers only. Confirmed by [stashr.me](https://stashr.me/blog/download-twitter-archive), [marqly.com](https://www.marqly.com/blog/export-twitter-x-bookmarks), [xarchive](https://github.com/sytelus/xarchive/) ("the official data archive excludes bookmarks entirely"); one outlier guide claims otherwise ([ideacoach.io](https://ideacoach.io/guides/export-twitter-bookmarks)) but the specific-tool vendors that looked agree it's absent. Treat archive as useless for this project. | | | | |
| **RSS-Bridge / Nitter-class readers** | Self-hosted PHP bridge or alternative frontend generating RSS from X | Free (self-host) | **Effectively dead for X.** X Corp served cease-and-desist letters on Nitter instances and the repo **August 24, 2026**; nitter.net went offline Aug 25, development stopped ([TechCrunch](https://techcrunch.com/2026/08/25/x-sends-cease-and-desist-to-open-source-project-nitter-over-alleged-scraping/), [The Verge](https://www.theverge.com/tech/984819/nitter-which-let-you-read-x-posts-without-using-x-is-offline)). RSS-Bridge's TwitterV2 bridge now just wraps your own paid API bearer token anyway ([docs](https://rss-bridge.github.io/rss-bridge/Bridge_Specific/TwitterV2.html)); Nitter RSS feeds were already disabled/antibot-walled on nearly all instances ([rss-bridge issue #4871](https://github.com/RSS-Bridge/rss-bridge/issues/4871)) | **High** — active legal enforcement, cite-by-name takedowns. Avoid building anything on this class |
| **Read-later apps with X capture** | Share sheet / extension saves article or thread; app extracts full text server-side | See below | High — maintained parsers survive X UI churn because they parse at save-time, not poll-time | Low — they're sanctioned clients of their own services |
| — [Readwise Reader](https://readwise.io/read) | Saves articles, PDFs, newsletters, YouTube transcripts, **X/Twitter threads**; long-form X posts render cleanly ([App Store release notes](https://apps.apple.com/us/app/readwise-reader/id1567599761)); ships a **Readwise MCP server** exposing highlights + full text of all Reader docs to Claude/Cursor ([same source]) | **$9.99/mo annual ($119.88/yr)** or $12.99 monthly; **no permanent free tier** (30-day trial); Lite plan $5.59/mo has no Reader ([gleamr.io](https://gleamr.io/blog/readwise-reader-pricing-2026), [readless.app](https://www.readless.app/blog/readwise-reader-pricing-2026)) | Highest | None |
| — [Matter](https://web.getmatter.com/) | Save articles/threads/PDFs; transcribes YouTube/podcasts; **has a public API** (`docs.getmatter.com` items endpoint) | **Free tier: unlimited saves**, unlimited tags, full-text search; Premium $60/yr web ($79.99 via iOS IAP) adds TTS/highlights/newsletter sync ([toolchase.com](https://toolchase.com/tool/matter-app/), [gleamr.io](https://gleamr.io/blog/matter-app-pricing-2026)) | High; iOS-first (no Android) | None |
| — wallabag | Open-source read-later; **self-host free**, or wallabag.it hosted | €11/year hosted ([wallabag.it/en/pricing](https://wallabag.it/en/pricing/)); MIT licensed ([wallabag.org](https://wallabag.org/self-hosting/)) | Solid, mature; parsing quality below Readwise/Matter | None. Note: **Omnivore shut down in 2025** along with Pocket (July 8, 2025; data deleted Nov 12, 2025) — do not build on either ([readless.app Pocket-alternatives](https://www.readless.app/blog/pocket-alternatives-2026), [flownib.com](https://flownib.com/articles/2026-08-07/best-open-source-later-alternatives-in-2026-self-hosted-tool.html)) |
| **Email-to-self / newsletter-address workflows** | Forward or subscribe via a per-user address; Readwise Reader and Matter Premium both ingest newsletters into the library | $0 (plain forwarding) to included-in-subscription | High for newsletters; manual friction for per-article use | None |
| **iOS Shortcuts share-sheet → local endpoint** | Shortcut receives URL from share sheet, "Get Contents of URL" POSTs JSON to a small server | Free | **Works, but NOT to `localhost`** — iOS sandboxes each app; 127.0.0.1 from Shortcuts fails ([r/shortcuts](https://www.reddit.com/r/shortcuts/comments/1du6rh5/post_url_to_localhost_fails/)). Must target the Mac's **LAN IP** (e.g. `http://192.168.1.x:8765/intake`). Prior art: [Orange-Share](https://github.com/Yannis4444/Orange-Share), [ShareFall](https://github.com/noenic/ShareFall), linkding share-sheet flows ([MPU Talk](https://talk.macpowerusers.com/t/how-to-create-share-sheet-shortcut-using-urls/39578)). POST-from-shortcut mechanics documented at [routinehub.co](https://blog.routinehub.co/how-to-send-a-post-request-with-apple-shortcuts/) | None (your own LAN) |
| **Claude in Chrome / browser-agent capture** | Anthropic extension (beta, all paid Claude plans, Chrome-only desktop) reads the page in a sidebar, can act agentically, records repeatable workflows ([support.claude.com](https://support.claude.com/en/articles/12012173-get-started-with-claude-in-chrome), [claudeai.guide](https://claudeai.guide/use-cases/claude-for-chrome/)) | Included with paid plan (Pro $20/mo min) | Beta rough edges; prompt-injection risk acknowledged by Anthropic; per-site permissions default-on | None for personal use — but it's a capture *assist*, not an unattended intake pipe |

**Honest ranking of unofficial avenues:** read-later apps (Matter free / Readwise) > iOS Shortcuts→LAN endpoint > extension exports > takeout (useless for bookmarks) > RSS/Nitter class (**dead, legally hostile**).

---

## 3. Article full-text extraction (saved link → clean text for LLM synthesis)

| Tool | Type | Cost | Notes |
|---|---|---|---|
| **[trafilatura](https://trafilatura.readthedocs.io/)** (v2.x, Python) | Local library/CLI | Free | Best-in-class open-source main-content extractor: F ≈ 0.90 with fallbacks on its 990-doc benchmark updated **2026-08-04** ([evaluation docs](https://trafilatura.readthedocs.io/en/latest/evaluation.html)); wins external benchmarks (ScrapingHub, Bevendorff et al. 2023). Outputs plain text/Markdown/XML + metadata (title, author, date). No JS rendering — pair with cache of the original HTML or use jina for JS-heavy pages |
| **Jina Reader — `https://r.jina.ai/<url>`** | Hosted API | **Free without key at 20 RPM; free API key raises to 500 RPM**; 10M free tokens on signup; then ~$0.05/1M tokens ([jina.ai/reader](https://jina.ai/en-US/reader/), [augmentcode listing](https://www.augmentcode.com/mcp/reader)) | Server-side JS rendering → LLM-ready Markdown; handles PDFs natively. Ideal fallback for pages trafilatura can't parse. (Elastic acquired Jina Oct 2025 — service continuity currently fine.) |
| **Mozilla Readability** (Firefox Reader View engine) | JS lib / built into Firefox Reader Mode | Free | Best raw fidelity in a May 2026 50-page benchmark (88% within 5% of ground truth); fastest path inside browser extensions ([bulkmd.app benchmark](https://bulkmd.app/blog/readability-vs-trafilatura-extractors)) |

Recommended stack: **trafilatura primary (local, free, fast), r.jina.ai fallback (free key, 500 RPM) for JS-heavy/paywalled-lite failures.** Both slot behind one `extract(url) -> {title, text, byline, published}` interface.

---

## 4. Recommended intake design

### Architecture (lowest-friction daily flow)

```
[iPhone share sheet]                    [Mac, nightly]
 iOS Shortcut "Save to intake"          cron/launchd 07:00
   POST {url, tweet_id?, note}            │
        │                                 ▼
        ▼                        Official X API poll:
 http://<mac-LAN-IP>:8765/intake    GET /2/users/{id}/bookmarks
        │                           GET /2/users/{id}/liked_tweets
        ▼                           (Owned Reads @ $0.001; dedup 24h)
 ┌──────────────────────────────────────────────┐
 │ intake daemon (python stdlib http.server —   │
 │ no FastAPI dependency needed)                │
 │  append → normalize → dedupe                 │
 └──────────────┬───────────────────────────────┘
                ▼
      ~/intake/items.jsonl           (normalized store)
                ▼
      extraction stage (nightly batch):
        trafilatura → fallback r.jina.ai
        local qwen via omlx: topic classify +
        takeaway/summary (batch, thinking budget low)
                ▼
      vault notes + tidbits queue (scored)
```

Why this shape: share-sheet capture is zero-friction at the moment of reading (works from X app, Safari, anything); the nightly API sweep backstops anything Mike forgot to share and catches likes too; extraction/classification runs **local via omlx** which matches the machine's routing rule (local models for batch work, hosted for interactive/blocking). The ~800-bookmark recency ceiling makes *daily* polling mandatory — never bulk-only.

### Normalized schema — `items.jsonl` (one JSON object per line)

```json
{
  "id": "sha256(source + source_id)",          // stable identity
  "source": "x_bookmark | x_like | ios_share | ext_export",
  "source_id": "1893...",                      // tweet id or url hash
  "captured_at": "2026-08-26T09:14:03-04:00",
  "ingest_batch": "2026-08-27T07:00",
  "kind": "tweet | thread | article",
  "author": {"handle": "...", "name": "..."},
  "text": "tweet text or article excerpt",
  "canonical_url": "https://example.com/post", // unwound from t.co
  "urls": ["..."],
  "lang": "en",
  "metrics": {"likes": 0, "rt": 0, "bookmarks": 0},
  "dedupe_key": "https://example.com/post",    // canonical_url OR tweet id
  "status": "new | extracted | classified | vaulted | tidbit_queued | rejected",
  "extraction": {
    "extractor": "trafilatura | r.jina.ai | native",
    "title": "...",
    "full_text_path": "~/intake/fulltext/<id>.txt"
  },
  "synthesis": {
    "model": "omlx/qwen-local",
    "topics": ["ai-agents", "va-policy"],
    "takeaways": ["..."],
    "summary": "...",
    "tidbit_score": 0.82,
    "tidbit_reason": "contradicts standing assumption X"
  }
}
```

Dedupe rule: unique on `dedupe_key`; second occurrence merges `source` list instead of appending a row.

### Top-3 cheapest reliable paths, ranked

1. **Shortcuts→LAN endpoint + nightly Owned-Reads API poll** — **~$0–3/month total** (X credits only; everything else free/local). Most robust: official API for the firehose, share-sheet for intent-flagged saves. Setup cost: one evening (developer portal + PKCE token + ~80-line stdlib server).
2. **Zero-API variant: extension export + share-sheet** — **$0/month.** Daily/weekly `xarchive` JSON export dropped in a watched folder replaces the API sweep; share-sheet still flags priority saves. Slightly higher friction, zero vendor dependence, immune to future X price hikes. Good fallback if the developer-account approval annoys him.
3. **Readwise Reader + its MCP server** — **$119.88/year.** Least code: share any post/thread/article straight into Reader, then point Claude/agents at the Readwise MCP for full-text access; Ghostreader handles first-pass summaries. Choose this only if Mike values managed polish over ownership — it's the only option with a real recurring bill, and it keeps his corpus on someone else's servers (Pocket's 2025 shutdown is the cautionary tale).

---

## 5. Tidbits surfacing cadence

Patterns worth stealing, found in prior art:

- **One fixed daily anchor digest** — Readwise's Daily Review sends a single spaced-repetition email/day ([aisotools review](https://www.aisotools.com/blog/readwise-reader-review-2026)); predictability is the feature, not frequency.
- **Per-topic schedules with thresholds** — Readless Pro supports up to 3 independent delivery schedules (e.g. tech at 7am, finance at 5pm, Sunday recap) with sender filters and cross-source de-duplication so the same story doesn't hit twice ([readless.app](https://www.readless.app/blog/readwise-reader-pricing-2026)).
- **Quiet hours** — suppress all pushes overnight; batch anything accumulated for the morning anchor. Implement trivially: the tidbits queue drains only at scheduled windows; launchd calendar jobs at 07:00 / 12:30 / 17:30.

Concrete recommendation for Mike:

| Window | Behavior |
|---|---|
| 22:00–06:45 | Quiet hours — nothing delivered; queue accumulates |
| 07:00 | **Morning digest**: top 5–7 tidbits by score, grouped by topic, one line + link each (local model wrote them overnight) |
| Midday (12:30) | Optional top-up **only if** ≥3 items scored above a high threshold arrived since morning — otherwise silent |
| 17:30 | Optional end-of-day recap of articles fully extracted (titles + takeaways), no push if queue empty |
| Sunday | Weekly synthesis: topic clusters, recurring themes, what changed vs. last week |

Threshold logic mirrors Readless: per-topic counters reset after delivery; a topic fires early only when N high-score items accumulate between windows. Score = local-model tidbit_score (novelty/actionability/relevance to active projects), calibrated over the first weeks.

---

## SOURCES

- X API pricing & credits (official): https://docs.x.com/x-api/getting-started/pricing
- X API bookmarks endpoint spec (official): https://docs.x.com/x-api/users/get-bookmarks · overview: https://docs.x.com/x-api/posts/bookmarks/introduction
- April 20, 2026 rate-change announcement: https://devcommunity.x.com/t/x-api-pricing-update-owned-reads-now-0-001-other-changes-effective-april-20-2026/263025 (via https://www.blotato.com/blog/twitter-api-pricing)
- Pay-per-use transition & legacy-tier status: https://postproxy.dev/blog/x-api-pricing-2026/ · https://api.sorsa.io/blog/twitter-api-pricing-2026 · https://www.xpoz.ai/blog/guides/understanding-twitter-api-pricing-tiers-and-alternatives/
- Nitter cease-and-desist (Aug 24–25, 2026): https://techcrunch.com/2026/08/25/x-sends-cease-and-desist-to-open-source-project-nitter-over-alleged-scraping/ · https://www.theverge.com/tech/984819/nitter-which-let-you-read-x-posts-without-using-x-is-offline
- Nitter instance health / RSS disabled: https://status.d420.de/ · https://github.com/RSS-Bridge/rss-bridge/issues/4871 · https://rss-bridge.github.io/rss-bridge/Bridge_Specific/TwitterV2.html
- X archive excludes bookmarks: https://stashr.me/blog/download-twitter-archive · https://stashr.me/blog/export-x-bookmarks · https://www.marqly.com/blog/export-twitter-x-bookmarks · https://github.com/sytelus/xarchive/ (outlier claiming inclusion: https://ideacoach.io/guides/export-twitter-bookmarks)
- Export tooling: https://github.com/sytelus/xarchive/ · https://github.com/prinsss/twitter-web-exporter · https://github.com/displace-agency/x-bookmarks-exporter · https://chromewebstore.google.com/detail/x-bookmarks-exporter-expo/abgjpimjfnggkhnoehjndcociampccnm
- Readwise Reader pricing/X support/MCP: https://readwise.io/read · https://apps.apple.com/us/app/readwise-reader/id1567599761 · https://gleamr.io/blog/readwise-reader-pricing-2026 · https://www.readless.app/blog/readwise-reader-pricing-2026
- Matter pricing + API: https://web.getmatter.com/ · https://toolchase.com/tool/matter-app/ · https://gleamr.io/blog/matter-app-pricing-2026 · https://docs.getmatter.com/api/items/get
- wallabag: https://wallabag.org/self-hosting/ · https://wallabag.it/en/pricing/ · Pocket/Omnivore shutdown context: https://www.readless.app/blog/pocket-alternatives-2026 · https://flownib.com/articles/2026-08-07/best-open-source-later-alternatives-in-2026-self-hosted-tool.html
- Jina Reader rates/free tier: https://jina.ai/en-US/reader/ · https://www.augmentcode.com/mcp/reader · https://serp.fast/tools/jina-ai
- trafilatura benchmarks (updated 2026-08-04): https://trafilatura.readthedocs.io/en/latest/evaluation.html · https://github.com/adbar/trafilatura
- Readability comparison benchmark: https://bulkmd.app/blog/readability-vs-trafilatura-extractors
- iOS Shortcuts POST mechanics + localhost limitation: https://blog.routinehub.co/how-to-send-a-post-request-with-apple-shortcuts/ · https://www.reddit.com/r/shortcuts/comments/1du6rh5/post_url_to_localhost_fails/ · prior art: https://github.com/Yannis4444/Orange-Share · https://github.com/noenic/ShareFall · https://talk.macpowerusers.com/t/how-to-create-share-sheet-shortcut-using-urls/39578
- Claude in Chrome status: https://support.claude.com/en/articles/12012173-get-started-with-claude-in-chrome · https://claudeai.guide/use-cases/claude-for-chrome/ · https://code.claude.com/docs/en/chrome
