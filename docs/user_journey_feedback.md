# Current workflow review and simulated user feedback

Date: 2026-11-05

## Does `STEPS-TO -SERVER.txt` match the current build?

**Mostly yes for the core architecture.** The document correctly describes:

- MT4 as a thin client that sends a license key, account details, symbol, timeframe, and
  chart summary.
- A server-owned prompt and AI key.
- Server-side license, account-binding, quota, calendar/news, and level validation.
- JSON returned to the EA for dashboard and chart rendering.
- Website, account, download, and payment surfaces around the analysis API.

The current [server.py](../mt4_ai_mvp/server.py) implements the local version of this core:
FastAPI, SQLite, demo licenses, `/analyze`, calendar/news fetches, a Gemini-or-mock path, and
HTML landing/login/dashboard/checkout-simulation pages.

## Differences from the planned production architecture

| Plan in `STEPS-TO -SERVER.txt` | Current local MVP |
|---|---|
| HTTPS hosted domain | Local `http://127.0.0.1/analyze` |
| Postgres | SQLite `mvp.db` |
| Stripe Checkout and signed webhook | Simulated checkout; no production webhook |
| Gemini or Claude for every run | Local mock when `GEMINI_API_KEY` is absent |
| User selects an instrument and supplies inputs | The MT4 EA sends symbol, timeframe, bid/ask, ATR, and chart summary to `/analyze`; there is no image/CSV upload flow |
| Persistent brief/session history | Usage is logged, but no user-facing brief session or follow-up thread |
| Source inspection and challenge/follow-up | Not exposed by the current API |
| Production rate limiting, monitoring, privacy/legal controls | Not yet implemented |

The architecture sketch in [architecture.md](architecture.md) should therefore be read as a
target model with a local implementation boundary, not as a claim that all production phases are
complete.

## Synthetic journey simulation

These are fictional usability predictions based on [personas.yaml](../personas.yaml), not
feedback from real participants. The API runs previously performed against the local server are
the observed integration results; the comments below are simulated reactions to those results.

### 1. Part-time multi-asset planner

**Journey:** Opens the landing page, chooses a plan, signs up or logs in, copies the license key
from the dashboard, downloads the EA, attaches it to an EUR/JPY H1 chart, and receives a BUY
result with entry, stop, target, invalidation, confidence, and warnings.

**Likely feedback:** “The output is quick and gives me a plan before work. I need the analysis
time and the actual calendar/news sources beside the result before I can trust it.”

**Likely action:** Saves the levels for review, but does not act directly from the brief until
the source context is visible.

**Friction:** The dashboard confirms the license and quota, but the end-to-end EA installation
and chart-display experience is not covered by the local API run.

### 2. EUR/JPY intraday specialist

**Journey:** Uses an active MT4 EUR/JPY M15 chart around an event window and receives a NEUTRAL
result with MEDIUM confidence and no levels.

**Likely feedback:** “Neutral is useful, but show me exactly why: calendar event, actual-versus-
forecast reaction, oil, Nikkei, volatility, intervention language, and the stale-data status.”

**Likely action:** Challenges the result and asks for the alternative scenario.

**Friction:** US-04 and US-05 are not complete: there is no source-detail view or follow-up
question tied to the same analysis.

### 3. Stock/index discretionary trader

**Journey:** Attaches the EA to an SPX500 H4 chart and receives a BUY result with levels.

**Likely feedback:** “The structure is reusable, but an FX-oriented calendar and prompt may not
understand earnings, index breadth, or a gap correctly. Show the instrument-specific evidence.”

**Likely action:** Compares the result with their own chart and rejects it if the catalyst context
is generic.

**Friction:** Multi-asset acceptance is structurally demonstrated, but not yet validated as
instrument-specific quality.

### 4. Volatility and catalyst monitor

**Journey:** Attaches the EA to an XAUUSD H1 chart and receives a NEUTRAL result during
consolidation.

**Likely feedback:** “I need the price timestamp, volatility regime, source freshness, and the
reason for neutral more than a generic headline.”

**Likely action:** Checks the source manually and waits for a new snapshot rather than treating
the result as an alert.

**Friction:** The current API returns `grounded=false` in mock mode, which is valuable honesty but
needs prominent user-facing treatment.

## Simulated failure journeys

| Situation | Current behavior | Simulated user reaction |
|---|---|---|
| Missing chart summary | HTTP 422 | Positive: the system refuses incomplete input instead of inventing data; the error should explain how to fix it. |
| Invalid license | HTTP 403 | Understandable, but the EA should show a recovery action such as “check key” or “open account page.” |
| Account limit reached | HTTP 403 | Confusing if presented as a generic analysis failure; explain bound accounts and plan limit. |
| Calendar/news unavailable | Response includes status fields | User needs the missing source and its effect on confidence shown beside the brief. |
| Mock AI active | `grounded=false` and mock warning | Correct for testing; must never look like live verified analysis. |
| No useful trade | NEUTRAL with zero levels | Good safety behavior; explain the conditions that would change the view. |

## Overall simulated verdict

**Core server workflow: promising for a closed technical beta.** The thin-client boundary,
license checks, quota, explicit neutral output, invalidation, and risk warnings are coherent.

**Not ready for a realistic user-simulation study of the full product promise.** The current flow
still lacks the EA installation/display test, source inspection, follow-up questions, persistent
analysis context, and screenshots of the dashboard and MT4 result.

The next highest-value test is to run the complete landing-page-to-MT4 journey and visibly show:
plan and license state, EA configuration, selected instrument and analysis time, source freshness,
grounded/mock status, scenarios with invalidation and warnings, and dashboard usage after analysis.
