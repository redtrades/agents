# Retail-Grade Trading Research Stack — TSLA / SPCX / QQQM + Options + Polymarket

**Prepared for Mike (ninov-trader context: personal options dashboard, IBKR + Cloudflare).**
**Date:** 2026-08-26. All projects/links verified live as of this date unless noted. FREE-TIER-FIRST throughout.

> **⚠️ Headline correction before anything else: SPCX is real now.** SpaceX completed the largest IPO in history on **June 12, 2026** and trades on Nasdaq under ticker **SPCX** — priced at $135/share, raised ~$75B at a ~$1.75–1.77T valuation, opened $150, closed day one ~$161 (+19%), intraday high $176.52 [S1][S2][S3]. Listed options followed ~3–5 business days later (~June 18–19, 2026) [S4]. So the dashboard's "SPCX" is a normal public underlying with listed options — not a proxy problem anymore. Section 0 covers what changed for the pre-IPO exposure vehicles he may still hold or reference.

---

## 0. SPCX reality check: what "SPCX" maps to in Aug 2026

| Item | Status |
|---|---|
| Underlying | SpaceX Class A on Nasdaq, ticker `SPCX`, IPO 2026-06-12, ~5% free float, Musk controls ~82.4% voting power [S2][S3] |
| Options | Listed ~June 18–19, 2026 per OCC/exchange approval norms for megacap IPOs; verify live chain via IBKR/CBOE before relying on it; expect elevated IV, wide spreads near listing [S4] |
| Index inclusion | FTSE Russell fast-track (~5 trading days); Nasdaq benchmark fast-entry rules adopted March 2026 [S2] |
| Valuation dispute | Morningstar publicly said SPCX was worth less than half the IPO price; several banks similar [S2] |
| Lock-up | Standard 90–180 days → insider unlock window lands roughly Sept–Dec 2026; plan around it in any short-premium strategy [S2][S4] |

**Legacy pre-IPO vehicles (what they were, and where they stand now):**

- **Destiny Tech100 (`DXYZ`)** — closed-end fund, SpaceX was its keystone position (~16–23% weight across 2025–26). The whole game was premium-to-NAV: NAV ran $6.92 (Jun '25) → $24.56 (Mar '26) while price swung $19.71–$72.87; premiums ranged from ~+21% to an insane +658%, sitting at **+40% to +74% as of late Aug 2026** ($34.43 vs stale NAV marks) [S5][S6][S7]. A **$1B at-the-market share program** filed May 2026 mechanically compresses any premium [S5]. Post-IPO its scarcity thesis is dead; treat any DXYZ holding as a premium-compression trade, not a SpaceX proxy.
- **ARK Venture Fund (`ARKVX`)** — interval fund; SpaceX **13.78%** weight as of Jun 30, 2026 (now marked public post-IPO), plus OpenAI/Anthropic/Stripe. Quarterly liquidity gates, ~2.75–3.49% fees, retail access mainly via SoFi/Titan/RIA channels at Schwab/Fidelity [S8][S9]. Fine as diversified venture exposure; wrong tool for trading a view.
- **Baron funds (BPTRX, BFGFX)** — mutual funds with long-held SpaceX stakes; no options, T+1 fund liquidity [S10].
- **Pre-IPO marketplaces (Hiive, Forge, EquityZen)** — accredited-only, $25k+ minimums; **moot for SpaceX since June 2026**, still the route for OpenAI/Anthropic/xAI-type names [S11].
- **Tokenized "pre-IPO" products** — OpenAI and Anthropic issued explicit warnings against Solana-based tokenized equity claims in May 2026. Avoid [S11].
- **LEAPS-on-proxy**: never really existed for SpaceX specifically (no clean listed proxy with options); now unnecessary. If Mike wants leveraged SPCX exposure, deep-ITM LEAPS on SPCX itself are the honest instrument once chains mature.

---

## 1. Free data APIs (2026 state)

| Source | Cost | What you get | Limits | Licensing / caveats |
|---|---|---|---|---|
| **IBKR TWS/Gateway API** (he has this) | $0 base; OPRA non-pro ~$1.50/mo top-of-book, ~$5/mo full streaming; US Securities Snapshot & Futures bundle ~$10/mo non-pro, waived ≥$30/mo commissions | Real-time US equities + full option chains + model greeks; free 15-min delayed snapshots without subscriptions; regulatory snapshots $0.01/req (150/day non-pro cap) [S12][S13] | Market-data "lines" quota; pacing rules; needs TWS/Gateway process running | Non-pro use only, no redistribution; greeks require both underlying + option subscription |
| **yfinance** | Free | Daily/intraday bars, option chains (snapshot), fundamentals | No published limit but aggressive loops get `YFRateLimitError`; geo-dependent blocks reported 2025–26; Chrome-impersonation workarounds circulate [S14][S15] | Unofficial scrape of Yahoo endpoints — ToS-gray, schema drift risk. Research only; cache everything; never sole source of truth |
| **Alpaca Market Data** | Free tier $0 | IEX real-time stocks (partial-volume feed), SIP data delayed 15-min via REST, crypto real-time, **US options indicative (OPRA delayed)**, option chains + greeks, 7yr history | 200 API calls/min; websocket limited to 30 symbols; real-time SIP + OPRA needs $99/mo Algo Trader Plus [S16][S17] | Personal/non-commercial; IEX ≈ 2–3% of volume — fine for EOD-ish research, not microstructure |
| **Polygon.io (rebranded Massive.com)** | Basic $0 | Stocks/options/forex/crypto REST; aggregates OHLCV; historical trades+quotes (tick-level even on free!) | **5 req/min hard cap**, 15-min delayed, ~2yr history; options = separate asset-class subscription (paid); WebSocket gated [S18][S19] | Free tier is personal-use sandbox; rebrand confirmed mid-2026, keys/API unchanged |
| **Tradier Brokerage API** | Free **with brokerage account** | Real-time US equities + options quotes, full option chains **with greeks/IV courtesy of ORATS**, historical bars, streaming | Sandbox = delayed; production real-time requires funded account; greeks refresh hourly [S20][S21] | Account-holder use; good second chain source to cross-check IBKR |
| **CBOE delayed quotes JSON** | Free | Full option chains w/ bid/ask/IV/OI/greeks, 15-min delayed: `https://cdn.cboe.com/api/global/delayed_quotes/options/{TICKER}.json` (indices need `_SPX` style prefix) [S22] | Unofficial endpoint; CBOE's page states automated extraction is prohibited and IPs get blocked [S23] | **Do not build a nightly scraper on it** — ToS explicitly forbids auto-extraction. Use manually for spot-checks; keep licensed sources primary |
| **Databento** | No permanent free tier; **$125 one-time credits** (expire 6 months) | Institutional OPRA historical options, equities, futures; pay-per-GB historical | Usage-based billing after credits; live data needs $199/mo Standard [S24] | Clean licensing; best "graduate to" option for serious options history |
| **Polymarket Gamma + CLOB APIs** | Free, no auth for reads | Markets metadata (gamma), order books/prices/trades (CLOB REST + WS) [S25][S26] | Public rate limits undocumented — be polite; high-volume traders must complete KYC/business verification per geoblock policy [S27] | Global platform geo-blocks US IPs/wallets — read-only data pulls from US for research are the gray-but-common pattern; see §4 |
| **Kalshi API** | Free market data (account for trading) | CFTC-regulated probabilities: Fed/CPI/elections; official docs + clients | Rate-limited tiers | Fully legal for US residents; cleanest *legal* prediction-market data source for him |

**Practical stack recommendation:** IBKR Gateway as primary (already paid/set up), Alpaca free + yfinance as redundant cross-checks, Tradier if he ever opens a second account for ORATS greeks. Store every pull (parquet/sqlite) — your own accumulating archive becomes the backtest dataset that free tiers won't give you retroactively.

---

## 2. Backtesting OSS — liveness verified 2026-08-26

| Project | Last push | Stars | Fit for agent-driven nightly local batch |
|---|---|---|---|
| **nautilus_trader** | **2026-08-26 (today)** | 27.8k | Production-grade Rust-core event engine; overkill for nightly batch, right choice if anything ever goes live [S28] |
| **QuantConnect LEAN** | 2026-08-25 | 21.4k | Local Docker engine free; native multi-leg **options strategy support**; catch = realistic options history needs paid QC data or self-imported data [S29] |
| **vectorbt** (OSS core) | 2026-08-02 | 8.8k | Best for vectorized parameter sweeps on TSLA/QQQM price series (signals, exits); not options-aware; PRO tier is paid [S30] |
| **backtesting.py** | 2026-08-05 | 8.9k | Revived and active again; simplest single-asset bar backtester; great for quick strategy sanity checks [S31] |
| **zipline-reloaded** | 2026-01-06 | 1.9k | Alive but slow-cadence; daily-bar factor research style; no options; lowest priority here [S32] |
| **py_vollib** | 2026-05-29 | 426 | Black-Scholes pricing, greeks, implied vol ("Let's Be Rational"); pair with py_vollib_vectorized for speed; the standard OSS greeks layer [S33] |

**Honest gap:** there is **no good free source of historical options-chain data**. Polygon/Massive options aggregates are paid; CBOE DataShop/ORATS/HistoricalOptionData are paid; Databento OPRA is usage-based. Therefore the viable architecture is:

**Minimal viable options harness (build, don't buy):**
1. **Start snapshotting tonight** — each evening pull TSLA/SPCX/QQQM (+ SPY/QQQ for reference) chains from IBKR into parquet: strike, expiry, bid/ask/last, IV, OI, volume, greeks. In 90 days you own a proprietary research dataset.
2. **Pricing math:** py_vollib for BSM greeks/IV everywhere — deterministic code, never LLM arithmetic.
3. **Strategy P&L engine:** replay stored snapshots; for strategies predating your archive, approximate fills by pricing historical strikes off the underlying path + fixed IV surface (state assumptions loudly).
4. **Underlying-level studies:** vectorbt/backtesting.py for entry-timing signals (IV-rank filters, moving-average regime, expected-move math: `EM = S × IV × √(dte/365)`).
5. **Optional rigor:** LEAN in local Docker if he wants event-driven multi-leg simulation with slippage models — worth it once Phase 2 stabilizes.

---

## 3. Options-strategy suggestion engines

**The practitioner mapping (price-target + IV-regime → candidates):** standard, codable logic:

| Directional view | IV regime | Favored structures |
|---|---|---|
| Bullish, target above spot | IV low/rising | Long calls / bull-call debit spreads |
| Bullish, happy to own lower | IV high | Cash-secured puts / wheel; bull-put credit spreads |
| Neutral, range-bound | IV high (IVR > ~50) | Iron condors; covered calls if long shares |
| Bearish/modest pullback | IV high | Bear-call credit spreads (defined risk) |
| Any, event binary (earnings, launch, lockup) | — | Default: no short premium through the event unless explicitly accepted |

Rules that make it mechanical: short strikes near ~30Δ ≈ 1σ; expected move formula above for target plausibility; sell premium when IV rank high, buy when low; defined-risk-only for a solo retail book.

**Existing OSS screeners:** no dominant mature project exists. Examples of the pattern (small personal repos, inspect don't trust): `Ja-Ta/options-income-screener` (CC/CSP screening with IV-rank + scoring + LLM-written summaries over Polygon/Massive data), `aboutdomtime/condor-lab` (iron condor research), `sbauwow/schwagent` (wheel/condors + LLM review on Schwab API) [S34][S35][S36]. Treat these as design references; his ninov-trader repo is the right home for a thin screener over his own chain snapshots.

**What an LLM-agent layer can responsibly do (and not):**
- ✅ CAN: normalize inputs ("target 340 on TSLA by Dec"), compute expected moves/greeks/IV-rank **via deterministic code**, filter candidate structures against rules, draft rationale + payoff diagrams for the nightly brief, enforce checklists, log everything.
- ❌ CANNOT: be trusted with pricing arithmetic, invent probabilities, size positions beyond hard-coded caps, override max-loss limits, or place orders. Every numeric output must come from code; the LLM narrates and filters only.

**Risk guardrails (hard-coded, non-negotiable):**
- Risk ≤ 1–2% of account equity per idea; max-loss defined at entry for every structure; **no naked short options**; no short gamma through earnings/catalysts (SPCX lockup expiry ~Sept–Dec 2026 counts); position count cap; human approves every trade; all recommendations READ-ONLY until Mike says otherwise.

---

## 4. Polymarket reality check

**Access (the part most articles get wrong):** two venues, one brand:
- **Polymarket Global** (polymarket.com): USDC/Polygon, wallet-based — **geo-blocked for US IPs since the Jan 2022 CFTC settlement**; VPN access violates ToS, risks fund freezes (wallet-level analysis active), forfeits federal recourse [S37][S38].
- **Polymarket US (QCX LLC)**: CFTC-designated contract market, launched **Dec 3, 2025**; fiat via approved FCMs; full KYC + SSN; waitlist removed ~May 13–14, 2026; accessible in 40+ states (**Nevada is the only court-ordered ban currently in force**) [S37][S38][S39].

**Fees (changed materially in early 2026 — re-verify quarterly):**
- Dynamic **taker fees rolled out by category**: politics/finance coefficient ~0.04 (peak ≈1¢/share at 50¢); sports ~0–2% (NCAA men's basketball added a 2%-of-winnings fee Feb 18, 2026); 15-min crypto markets highest (~up to 1.8–3%); **geopolitics/world events fee-free** [S40][S41].
- **Maker orders free** + daily rebate pool (funded 100% by taker fees); tiered taker rebates; gasless via relayer; collateral moved to pUSD after the **CLOB V2** cutover [S40][S42].

**API/tooling status (verified today):**
- `py-clob-client` is **ARCHIVED and non-functional against V2 production** — README says migrate [S43].
- Interim: `py-clob-client-v2` [S44]. Recommended: unified official SDK **`Polymarket/py-sdk`** (`pip install polymarket-client`, stable 0.3.0 released 2026-08-04) covering gamma/data/CLOB/WebSockets [S45].
- Docs: gamma markets API + CLOB endpoints at docs.polymarket.com; order books readable with zero auth [S25][S26].

**Arbitrage bots — the evidence, honestly:**
- Real money WAS extracted: IMDEA Networks study documented **$39.59M arbitrage Apr 2024–Apr 2025** (negRisk rebalancing: $28.99M over just 662 ops, avg $43.8k; single-condition: $10.58M over 7,051 ops) [S46].
- But the window is closing fast: avg opportunity duration compressed **12.3s (2024) → ~2.7s (2026)**, ~73% captured by sub-100ms bots; an on-chain audit of 95M transactions found only **0.51% of wallets profited >$1k**; Kalshi-side research (300k contracts) shows average traders **−20% pre-fee**, with makers positive and takers negative [S47][S48][S49].
- Structural solo-operator killers: non-atomic multi-leg fills, thin depth beyond top-of-book, oracle manipulation incidents (March 2025 UMA whale case), category-specific fees, and — for Mike specifically — the US geoblock making the global venue off-limits anyway; Polymarket US/Kalshi have different stacks and their own fee schedules [S46][S50][S51].

> **Verdict: an automated arb bot is NOT a viable income strategy for a solo operator in Aug 2026.** The latency war is lost, fees bite at exactly the spreads left behind, execution is non-atomic, and lawful US access routes don't include the deep global books. Anyone selling a "Polymarket arb bot" is selling the 2024 window.

**What IS worth building — prediction markets as a data signal:**
- Calibration is genuinely good: Kalshi paper over **2.24M resolved markets** (2021–mid-2026) evaluates calibration by time-to-resolution; a Feb 2026 Federal Reserve paper finds Kalshi outperforms surveys/derivatives on economic releases; companion work shows Polymarket beating analysts on earnings reactions [S52][S53].
- Price discovery is real and leading: SSRN study (Ng/Peng/Tao/Zhou, rev. Apr 2026) finds liquid prediction markets outperform polls, Polymarket leads Kalshi in discovery during high activity, and large-trade order imbalance predicts subsequent returns [S54].
- Build: nightly pull of Fed-decision / CPI / Tesla-relevant / macro-event probabilities (via `py-sdk` public reads or Kalshi's API), store as time series, append to the brief as sentiment/probability features next to IV and price action. Zero trading, zero KYC-for-trading needed, fully defensible.

---

## 5. Recommended build plan (phased, free-tier-first)

**Phase 1 — Nightly data pull + brief (week 1–2, $0 marginal cost)**
- IBKR Gateway (paper or live) as primary quote/chain source for TSLA, SPCX, QQQM, SPY, QQQ + VIX; yfinance + Alpaca free as cross-checks; log divergences.
- Persist everything to parquet/sqlite (this becomes the options research dataset — irreplaceable later).
- Emit a markdown/JSON nightly brief to the Cloudflare dashboard: close, IV rank, expected moves, upcoming catalysts (earnings, **SPCX lockup expiry window**), top OI strikes.
- Acceptance: runs headless via cron/launchd, survives a Yahoo outage (fallbacks), zero manual steps.

**Phase 2 — Backtest lab + strategy suggester (weeks 3–8)**
- vectorbt/backtesting.py for underlying-signal studies; custom harness over stored chain snapshots + py_vollib greeks for options P&L; optional LEAN-in-Docker later for multi-leg rigor.
- Strategy suggester implementing §3 mapping: inputs = symbol + price target + horizon; outputs = ranked READ-ONLY candidates with expected move, POP estimate, max loss, IV-regime rationale — all numbers from deterministic code, LLM only writes the narrative.
- Guardrails hard-coded per §3; every suggestion labeled "NOT ADVICE — requires human approval."

**Phase 3 — Prediction-market signal reader (weeks 6+, parallelizable)**
- `pip install polymarket-client` (official py-sdk) read-only public data, or Kalshi API for fully-domestic coverage; map relevant markets (Fed funds, CPI, TSLA-named markets if any) to his tickers; append probability time-series to the nightly brief.
- Explicitly detection-only: no wallets funded, no keys, no orders.

### 🚫 NO-AUTO-TRADING LINE
Nothing in Phases 1–3 places, cancels, or modifies a single order on any venue — equities, options, or prediction markets. IBKR credentials stay used only for market data + manual workflows. Any future auto-execution (even paper) is a separate, explicit, written approval from Mike before a line of order-placement code is written.

---

## SOURCES

- [S1] TechJournal — SPCX largest-IPO debut FAQ: https://techjournal.org/spacex-stock-spcx-nasdaq-debut-largest-ipo
- [S2] Wikipedia — Initial public offering of SpaceX: https://en.wikipedia.org/wiki/Initial_public_offering_of_SpaceX
- [S3] IPO Club — SpaceX post-IPO status, $135/$75B/day-one $161: https://www.ipo.club/deals/spacex ; ThinkMarkets day-one recap: https://www.thinkmarkets.com/en/trading-academy/market-events/spacex-ipo-results-spcx-first-day-trading-2026/
- [S4] OptionLeo — SPCX options listing timing (~June 18–19, 2026) + first-week risk: https://www.optionleo.com/blog/spacex-options-launch-date
- [S5] TruthsandNews — DXYZ analysis Jun 2026 (NAV $24.56, premium ~53%, $1B ATM, holdings table): https://truthsandnews.com/markets/dxyz-stock-analysis-june-2026-destiny-tech100-spacex-ipo-proxy
- [S6] CEFConnect — DXYZ price $34.43 vs NAV $19.97 (+73.5%), premium history: https://www.cefconnect.com/fund/DXYZ ; CEFdata profile: https://cefdata.com/funds/dxyz
- [S7] ts2.tech — DXYZ look-through SpaceX exposure math + premium risk: https://ts2.tech/en/destiny-tech100-dxyz-stock-surges-on-spacex-ipo-buzz-what-happened-this-week-premium-to-nav-reality-check-and-week-ahead-watchlist-updated-dec-12-2025
- [S8] ARK Funds — ARKVX portfolio (SpaceX 13.78%, went public June 2026): https://www.ark-funds.com/portfolio ; Q2 2026 update: https://www.ark-funds.com/articles/venture-fund/ark-venture-2nd-quarter-2026-update
- [S9] NAI500 — ARKVX structure, fees 3.49%, SoFi/Titan/Schwab/Fidelity access: https://nai500.com/blog/2026/04/spacex-openai-and-anthropic-are-going-public-soon-and-ark-venture-fund-arkvx-is-getting-in-early
- [S10] Forbes/Shulman — How to buy SpaceX stock in 2026 (Baron funds, CEF premium risk): https://www.forbes.com/sites/joelshulman/2025/11/25/how-to-buy-spacex-stock-in-2026
- [S11] Allocations — non-accredited pre-IPO exposure guide (Hiive/Forge/EquityZen accredited-only; tokenized-product warnings; DXYZ/ARKVX tradeoffs): https://www.allocations.com/insights/how-non-accredited-investors-can-get-pre-ipo-exposure-(spacex-openai-anthropic)-in-2026
- [S12] IBKR market-data pricing: https://www.interactivebrokers.com/en/pricing/market-data-pricing.php
- [S13] IBKR Campus — market data subscriptions/API (regulatory snapshots, lines, OPRA notes): https://ibkrcampus.com/campus/ibkr-api-page/market-data-subscriptions/ ; Brokerchampion IBKR data guide (bundle costs/waivers): https://brokerchampion.com/interactive-brokers-market-data
- [S14] yfinance PyPI (v1.6.0, Aug 2026): https://pypi.org/project/yfinance/ ; docs: https://ranaroussi.github.io/yfinance/index.html
- [S15] yfinance rate-limit issue thread (YFRateLimitError, geo effects, impersonation workaround): https://github.com/ranaroussi/yfinance/issues/2411 ; edgeful 2026 alternatives overview: https://www.edgeful.com/blog/posts/yahoo-finance-api-alternatives
- [S16] Alpaca data plans (Free $0 IEX, 200 calls/min, options indicative, WS 30 symbols): https://alpaca.markets/data
- [S17] Alpaca support — IEX vs SIP feeds: https://alpaca.markets/support/data-provider-alpaca
- [S18] Polygon/Massive pricing guides 2026 (free tier 5 req/min, 15-min delay, options separate): https://tradingtoolshub.com/blog/polygonio-pricing-guide-2026-all-plans-costs-hidden-fees/ ; https://apicostcalc.com/polygon.html (rebrand note)
- [S19] Polygon rate-limit spec (Basic hard cap 5/min, HTTP 429): https://github.com/api-evangelist/polygon-io/blob/main/rate-limits/polygon-io-rate-limits.yml
- [S20] Tradier getting started (free account + tokens, sandbox): https://docs.tradier.com/docs/getting-started
- [S21] Tradier market data (real-time w/ account; sandbox delayed; ORATS greeks hourly): https://docs.tradier.com/docs/market-data ; options chains endpoint: https://docs.tradier.com/reference/brokerage-api-markets-get-options-chains
- [S22] CBOE delayed-quotes JSON endpoints + schema (incl. `_SPX` prefix convention): https://github.com/rik3k/cboe-options-data-pipeline
- [S23] CBOE delayed quotes API page — anti-automated-extraction notice: https://www.cboe.com/delayed_quotes/api
- [S24] Databento pricing ($125 credits, usage-based, $199 Standard for live): https://databento.com/pricing
- [S25] Polymarket docs — CLOB endpoints: https://docs.polymarket.com/developers/CLOB ; gamma markets API: https://docs.polymarket.com/developers/gamma-markets-api/get-markets
- [S26] Polymarket docs — fees (category taker fees, maker rebates, geopolitics fee-free): https://docs.polymarket.com/trading/fees
- [S27] Polymarket geoblock/KYC-for-API-traders policy: https://docs.polymarket.com/api-reference/geoblock (context: https://www.datawallet.com/crypto/polymarket-restricted-countries)
- [S28] nautilus_trader repo (pushed 2026-08-26): https://github.com/nautechsystems/nautilus_trader
- [S29] QuantConnect LEAN repo (pushed 2026-08-25): https://github.com/QuantConnect/Lean
- [S30] vectorbt repo (pushed 2026-08-02): https://github.com/polakowo/vectorbt
- [S31] backtesting.py repo (pushed 2026-08-05): https://github.com/kernc/backtesting.py
- [S32] zipline-reloaded repo (pushed 2026-01-06): https://github.com/stefan-jansen/zipline-reloaded
- [S33] py_vollib repo (pushed 2026-05-29): https://github.com/vollib/py_vollib
- [S34] Ja-Ta/options-income-screener (CC/CSP screener pattern): https://github.com/Ja-Ta/options-income-screener
- [S35] aboutdomtime/condor-lab (iron condor research): https://github.com/aboutdomtime/condor-lab
- [S36] sbauwow/schwagent (wheel/condors + LLM review): https://github.com/sbauwow/schwagent
- [S37] DropStab — Is Polymarket Legal 2026 (two-entity table, state-by-state, Nevada ban, May 2026 waitlist removal): https://news.dropstab.com/research/is-polymarket-legal
- [S38] Tech-Insider — Polymarket US legality (Dec 3 2025 launch, QCX LLC, KYC specs, VPN risks): https://tech-insider.org/prediction-markets/is-polymarket-legal-in-the-usa/
- [S39] Polymarket US docs — what is Polymarket US (DCM/DCO): https://docs.polymarket.us/getting-started/what-is-polymarket-us
- [S40] Predictefy — Polymarket fees 2026 (taker rollout, coefficients, maker rebates, pUSD): https://blog.predictefy.com/polymarket-fees
- [S41] Zenhodl — fee schedule detail (sports ~0%, NCAA winnings fee Feb 18 2026): https://zenhodl.net/blog/polymarket-fees-explained-maker-taker-clob
- [S42] Polymarket docs — CLOB V2 migration (new contracts, wiped orders, new SDK packages): https://docs.polymarket.com/v2-migration
- [S43] py-clob-client ARCHIVED notice → migrate: https://github.com/Polymarket/py-clob-client
- [S44] py-clob-client-v2 (interim): https://github.com/Polymarket/py-clob-client-v2
- [S45] Polymarket/py-sdk — unified SDK (`pip install polymarket-client`, v0.3.0 Aug 2026): https://github.com/Polymarket/py-sdk
- [S46] IMDEA Networks arb extraction figures (as summarized in FlexiWay/prediction-market-arbitrage README incl. negRisk $28.99M/662 ops, oracle-attack case): https://github.com/FlexiWay/prediction-market-arbitrage
- [S47] DigitechBytes — 95M-tx audit, 0.51% profitable wallets, opportunity compression 12.3s→2.7s: https://digitechbytes.com/emerging-consumer-tech-explained/are-polymarket-trading-bots-actually-profitable-the-math-behind-2026-s-predictio/
- [S48] PolyBot arbitrage risk guide (execution/depth/rules failure modes): https://polybot.trading/blog/polymarket-arbitrage-bot-related-markets-guide
- [S49] Laika Labs — CEPR Kalshi study (avg trader −20% pre-fee; makers positive; longshot bias): https://laikalabs.ai/prediction-markets/kalshi-prediction-market-trading-strategies
- [S50] QuantVPS — cross-market arb case studies (0xalberto $764/day single-market; multi-market losses; Talarico Kalshi-vs-Polymarket divergence): https://www.quantvps.com/blog/cross-market-arbitrage-polymarket
- [S51] Gizmodo — Polymarket geoblocking enforcement/wallet freezing: https://gizmodo.com/best-vpn/polymarket
- [S52] Kalshi Research — calibration paper (2,243,741 resolved markets): https://kalshi.com/research/publications/calibration
- [S53] Forbes — Fed paper (Kalshi vs surveys) + Polymarket-beats-analysts study coverage: https://www.forbes.com/sites/jasonbrett/2026/02/23/kalshi-polymarket-offer-evolution-of-predictions-for-fed-wall-street/
- [S54] Ng, Peng, Tao, Zhou — Price Discovery and Trading in Modern Prediction Markets (SSRN 5331995, rev. Apr 2026): https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5331995

*Not financial advice. Fee schedules, tiers, and regulatory status change frequently — re-verify before acting.*
