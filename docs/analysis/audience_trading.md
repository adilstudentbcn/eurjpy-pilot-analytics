# Audience analysis — discretionary retail traders

**Date:** 2026-11-02. **Geography:** Spain/EU unless stated otherwise. The correct current conclusion is **we do not know the active-trader number yet**.

## Definition and two routes

For this work, an **active trader** means an adult who reviewed or placed at least one discretionary trade in the selected asset category during the previous 90 days. Broker “client”, “funded account”, “customer”, “fund participant”, and “monthly active user” are not interchangeable. No public source located here supplies this exact Spain/EU definition.

### Route A — bottom-up scenario, not an estimate

Start with a Spain 18-74 population proxy of 39-41 million people (Eurostat/INE; [ledger rows L1 and L8](./ledger_trading.csv)). Multiply by an assumed 1-8% active-trading share and an assumed 10-50% tool-payer share. This produces 390,000-3,280,000 active-trader scenarios and 39,000-1,640,000 paying-tool scenarios. The ranges are intentionally wide and are `assumption`; they do not set a launch level. A €5-€50 observed comparable monthly price range creates only a simulated annual revenue ranking. No bridge to actual Spanish trader behaviour exists.

### Route B — top-down ceiling check

XTB reports 1.19-1.20 million active clients in 2025; flatexDEGIRO reports 3.5-3.6 million customers; Trading 212 reports 4.5-4.6 million global clients. These are useful ceilings, not Spain active-trader counts: they include countries, inactive or non-trading customers, investors, and potentially overlapping people. They cannot be summed. The 5.2-5.4 million Spanish retail-investor proxy from CNMV is also not a trading count. Route A and Route B therefore cannot be compared within 3x.

## Niche ranges and acquisition hypotheses

| Niche | Size range now | What they pay for today | Where they talk | How to reach |
|---|---|---|---|---|
| Forex intraday | Unknown; use 1-8% adult share only as a labelled scenario | Broker spread/commission, charting, calendar, education, occasional signals | ForexFactory, r/Forex, TradingView ideas, X, Discord/Telegram | EUR/JPY risk brief, transparent input audit, specialist communities |
| Stock/index | Unknown; broker ceilings are not stock-only | Broker access, charting, screeners, research/news, data | TradingView, r/Daytrading, X, broker communities | Earnings/index examples, search content, partner communities |
| Commodities/crypto | Unknown; no bridged Spain count | Exchange/broker fees, data, alerts, research, AI scanners | TradingView, Reddit, X, Telegram/Discord | Catalyst-risk examples and source-visible briefs |
| Part-time multi-asset | Unknown; overlap must be measured | One or more broker/chart/research/AI subscriptions plus time cost | TradingView, newsletters, finance communities | Time-saving workflow demo and waitlist |

## Trading overlap

Let **A** = active in the category and has missed or discovered a catalyst late; **B** = pays for at least one tool used in that workflow. The desired audience is A∩B.

With only marginal rates `a=P(A|niche)` and `b=P(B|niche)`, the Frechet bounds are `max(0,a+b-1) ≤ P(A∩B) ≤ min(a,b)`. Independence is a labelled assumption: `P(A∩B)=a*b`; it is not evidence and there is no bridge estimate. The survey must ask both behaviours of the same respondents so the overlap is observed rather than invented.

## Public conversations

The public routes are [r/Forex](https://www.reddit.com/r/Forex/), [r/Daytrading](https://www.reddit.com/r/Daytrading/), [ForexFactory](https://www.forexfactory.com/), [TradingView public ideas](https://www.tradingview.com/markets/currencies/ideas/), and public X search. Repeated topic hypotheses are: missed or revised economic-calendar events, unclear actual-versus-forecast reaction, broker/data latency, off-calendar geopolitical/intervention risk, too many tabs, generic AI answers, and distrust of unexplained levels.

Exact public quotes collected during this pass:

- ForexFactory: “old fashioned and dated looking website” — Trustpilot, accessed 2026-11-02.
- ForexFactory: “calendar destroyed me” — Trustpilot, accessed 2026-11-02.
- MetaTrader 5: “I would like to be added ‘Alarm notifications’” — App Store, accessed 2026-11-02.
- MetaTrader 5: “staring at a trade in the red” — App Store, accessed 2026-11-02.
- TrendSpider: “steep learning curve” — Warrior Trading review, accessed 2026-11-02.

Each quote is under 15 words and is one observed quote, not a prevalence estimate. Share of voice is **not known**: public communities are platform-biased, X search is volatile, and private Discord/Telegram, Spanish-language groups, lurkers, non-posters and lapsed users are missing.

## Personas

The four complete personas are in [personas.yaml](./personas.yaml). The non-cooperative case is explicit in each persona so the pilot tests whether the workflow can refuse unsafe or unsupported requests.

## 12-question bridge survey (design only)

Target: **200 consented answers per niche**; do not simulate responses. No names, contacts, broker IDs, balances, account numbers, P&L, positions or credentials.

1. Consent: “I understand this is research, may skip/stop, and no financial data is collected.” Yes / no (no ends survey).
2. Which niche did you actively trade or review in the last 90 days? Forex / stock-index / commodities-crypto / multi-asset / none.
3. How many days in the last 90 days did you review or place a trade in that niche? 0 / 1-4 / 5-19 / 20+.
4. Which instruments did you review? Category checkboxes only; no ticker, account or position.
5. In your last planning session, which sources did you use? Calendar / chart / broker / news / CSV-data tool / community / AI / other.
6. How often did you discover a relevant catalyst after planning? Never / rarely / sometimes / often / almost every session.
7. What happened? Select: missed event / off-calendar news / actual-versus-forecast surprise / price reaction unclear / data delay / other.
8. How much time did the last planning session take? Under 10 / 10-20 / 21-40 / 41-60 / over 60 minutes.
9. Which workflow tools did you pay for in the last 90 days? None / charting / news-research / broker add-on / AI / signals / other. Do not ask price or account details.
10. Which device do you use most? Desktop / laptop / tablet / phone.
11. Which output would be useful? Scenario / invalidation condition / source-linked risk list / follow-up chat / CSV summary / none.
12. What is the next acceptable test? Free prototype / paid trial / monthly plan research / interview only / none; optional open text: “What would make you stop using it?”

Record only anonymous survey ID, niche, consent, answers and collection date. Pre-register exclusions and report missingness, quotas and the exact wording.

## What I could not verify

1. A regulator-defined active-trader count for Spain or the EU.
2. Broker counts bridged to Spain, asset category and 90-day activity.
3. A public, random sample of Spanish/EU trader complaints.
4. Category-specific willingness to pay and tool-payer share.
5. Share of voice across public and private communities.
6. Whether the HTML prototype's Claude.ai host dependency is available to external pilot users.
