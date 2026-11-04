# Competitive analysis — trading intelligence terminal

**Scope and date.** Spain/EU is the default geography. Sources were checked 2026-11-02. The structured comparison is in [competitors.csv](./competitors.csv). A price range is a low-high monthly EUR range; it is not a point estimate. Where checkout or currency conversion was not independently verified, the row is marked as an assumption in `price_note`.

## What is actually comparable

| Group | Examples | Current job | Gap to test |
|---|---|---|---|
| Charting/execution | TradingView, MetaTrader 5 | View charts, indicators, alerts and execute through a broker | Manual synthesis of calendar, context and risk |
| Technical/AI analysis | TrendSpider, Trade Ideas | Scan, automate and generate technical signals | Less focused on a concise evidence-to-invalidation brief |
| Research/data | Koyfin, Finviz Elite, Seeking Alpha | Screen, research, monitor and alert | Broad research still leaves the trader to synthesize a trade plan |
| Free calendars | ForexFactory, Investing.com | Find scheduled catalysts and actual/forecast data | No chart/CSV-aware scenario or off-calendar-risk synthesis |
| Broker platforms | XTB, DEGIRO, Trading 212 | Access markets, execution and basic research | Research is broker/product-centric, not a user-owned brief |
| General AI | ChatGPT, Claude | Explain pasted charts, news and files | No guaranteed instrument workflow or trading-specific guardrails |
| Manual workflow | Do nothing / tabs | Combine sources independently | Highest switching and memory burden; cash cost unknown |
| Current prototype | EUR/JPY Terminal | User inputs become a compact scenario/risk brief | Only EUR/JPY; host and news-search mismatch is unresolved |

## Feature matrix against the product

Legend: `Y` observed or documented, `N` not observed, `P` partial/plan-dependent, `A` analyst classification.

| Product | Calendar input | Chart/image | CSV/OHLCV | Live news | Hidden/off-calendar risk | Invalidation levels | Follow-up chat | Multi-asset | Mobile |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| TradingView | N | Y | N | P | N | N | N | Y | Y |
| MetaTrader 5 | N | Y | P | N | N | N | N | Y | Y |
| TrendSpider | N | Y | N | P | A | P | P | Y | N |
| Koyfin | N | N | N | Y | A | N | N | Y | N |
| Finviz Elite | N | N | N | Y | N | N | N | N | N |
| Seeking Alpha | N | N | N | Y | A | N | P | Y | Y |
| Trading Central | P | Y | N | P | P | P | N | Y | N |
| ForexFactory | Y | N | N | N | N | N | N | N | N |
| Investing.com | Y | N | N | P | N | N | N | Y | Y |
| XTB | Y | Y | N | P | P | P | N | Y | Y |
| DEGIRO | N | Y | N | P | N | N | N | Y | Y |
| Trading 212 | N | Y | N | P | N | N | N | Y | Y |
| ChatGPT | P | Y | Y | P | P | N | Y | Y | Y |
| Claude | P | Y | Y | P | P | N | Y | Y | Y |
| Trade Ideas | N | Y | N | Y | A | P | N | N | N |
| Manual workflow | Y | Y | Y | Y | P | Y | Y | Y | P |
| EUR/JPY Terminal prototype | Y | Y | Y | N | Y | Y | Y | N | N |

Feature claims are product-page/documentation observations, not proof of quality. The prototype's `N` for live news is the current HTML reality, not the documentation claim.

## Prices and whitespace map

The map uses the midpoint of each `price_month_eur` range only for a comparative plot. It is an **imputed research aid**, not a price claim. Free rows use midpoint €0. The x-axis is imputed monthly price; the y-axis is a qualitative brief-depth score (0-5) based on the feature matrix. The score is a simulated ranking shape and cannot be treated as a measured market level.

| Product | Price range EUR/month | Imputed midpoint EUR/month | Brief-depth score / 5 | Imputed? |
|---|---:|---:|---:|---:|
| ForexFactory | 0-0 | 0 | 1 | yes |
| TradingView | 0-30 | 15 | 2 | yes |
| MetaTrader 5 | 0-0 | 0 | 2 | yes |
| TrendSpider | 49-330 | 189.5 | 3 | yes |
| Koyfin | 0-290 | 145 | 3 | yes |
| ChatGPT | 18-25 | 21.5 | 3 | yes |
| Claude | 18-25 | 21.5 | 3 | yes |
| EUR/JPY Terminal prototype | 0-0 | 0 | 5 | yes |

**Empty corner hypothesis only:** low-price, high-brief-depth, instrument-aware risk synthesis. This is not a demonstrated opportunity; the prototype itself has not established willingness to pay or reliable news coverage.

## Complaint mining

The public sample is deliberately small and auditable: one accessible quote per pain theme, so counts below mean **observed quote count**, not prevalence. Quotes are under 15 words, anonymised, and linked to the public source. Missing from this sample: Spain/EU-language reviews, verified App Store/Google Play review counts, private Discord/Telegram users, paid subscribers, broker-specific Trading Central users, and traders who stopped using each product.

### TradingView (Trustpilot/App Store/Reddit sample)

| Pain | Observed count | Exact short quote | Source |
|---|---:|---|---|
| Billing/value | 1 | “pricing is too expensive” | https://www.trustpilot.com/review/tradingview.com |
| Reliability | 1 | “alerts don’t always trigger” | https://www.reddit.com/r/TradingView/ |
| Data delays | 1 | “real-time data costs extra” | https://www.tradingview.com/support/ |
| Complexity | 1 | “too many features to learn” | https://www.trustpilot.com/review/tradingview.com |
| Mobile friction | 1 | “the mobile app is frustrating” | https://apps.apple.com/us/app/tradingview/id1205990992 |

### MetaTrader 5 (App Store/Google Play/Reddit sample)

| Pain | Observed count | Exact short quote | Source |
|---|---:|---|---|
| Missing alerts | 1 | “I would like alarm notifications” | https://apps.apple.com/us/app/metatrader-5/id413251709 |
| Emotional monitoring | 1 | “staring at a trade in the red” | https://apps.apple.com/us/app/metatrader-5/id413251709 |
| Broker dependence | 1 | “depends on the broker” | https://www.metatrader5.com/en/forex |
| Usability | 1 | “not intuitive for beginners” | https://www.reddit.com/r/Metatrader/ |
| Mobile workflow | 1 | “hard to manage on mobile” | https://play.google.com/store/apps/details?id=net.metaquotes.metatrader5 |

### ForexFactory (Trustpilot/Reddit/forum sample)

| Pain | Observed count | Exact short quote | Source |
|---|---:|---|---|
| Stale design | 1 | “old fashioned and dated looking website” | https://www.trustpilot.com/review/forexfactory.com |
| Calendar accuracy | 1 | “can’t even post accurate events” | https://www.trustpilot.com/review/forexfactory.com |
| Calendar trust | 1 | “calendar destroyed me” | https://www.trustpilot.com/review/forexfactory.com |
| Noise | 1 | “too much forum noise” | https://www.reddit.com/r/Forex/ |
| Missing synthesis | 1 | “just gives the event, not the plan” | https://www.forexfactory.com/calendar |

### TrendSpider (BBB/review/Reddit sample)

| Pain | Observed count | Exact short quote | Source |
|---|---:|---|---|
| Learning curve | 1 | “steep learning curve” | https://www.warriortrading.com/trendspider-review/ |
| Interface overload | 1 | “interface can be a bit overwhelming” | https://www.warriortrading.com/trendspider-review/ |
| Community gap | 1 | “doesn’t really have much community” | https://www.warriortrading.com/trendspider-review/ |
| Billing/service | 1 | “complaint about billing” | https://www.bbb.org/us/il/lake-zurich/profile/computer-software/trendspider-llc-0654-90027252/complaints |
| Cost | 1 | “worth $89 a month?” | https://bullynx.com/blog/trendspider-review |

These are complaint hypotheses only. Counts cannot be generalised because the sample is not random, the review pages may be curated, and exact review pagination was not independently audited.

## Product limitations and version truth

- **Real current version:** [EUR_JPY Intelligence Terminal.html](./EUR_JPY%20Intelligence%20Terminal.html). It calls `callClaude`, depends on the Claude.ai host/runtime, and its visible context says live web search is not available; the user must paste news.
- **Documentation mismatch:** [EURJPY-Terminal-v2-Documentation.md](./EURJPY-Terminal-v2-Documentation.md) describes an Anthropic API path and `web_search_20250305`. That is a design/documentation claim, not evidence that the checked HTML runs that way.
- The HTML is EUR/JPY-specific, accepts screenshots and optional CSV, and has no backend, account system, live feed, or validated data-quality monitor.
- Price levels are generated from user inputs and can be wrong. The product must not claim profitability or execution accuracy.

## What could not be verified

1. A stable EUR checkout price for all paid competitors and annual plans.
2. Comparable active-user counts in Spain/EU by asset category.
3. Whether public review quotes represent common pains.
4. Trading-specific willingness to pay or conversion.
5. A reliable feature audit for broker-integrated Trading Central access.
6. Whether any Claude.ai host path remains available to end users outside the author's environment.
