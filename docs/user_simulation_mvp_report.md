# User simulation report: MT4 AI MVP

Date: 2026-11-05

## Method

The scenarios were mapped from [user_situations.md](analysis/user_situations.md) and the
personas in [personas.yaml](../personas.yaml). The live local endpoint used by the MT4 EA was:

`POST http://127.0.0.1/analyze`

All chart values and broker identifiers below were simulated. No participant, personal, or
broker data was used. The server was already running, and the responses indicate that its
current AI path is grounded=false; therefore the results are an MVP integration test, not
validated market advice. The direct API runs tested the EA-to-server contract, not the complete
landing-page, subscription, download, and MT4 display journey.

## Simulated users

| Persona | Situation | Simulated need and risk |
|---|---|---|
| Part-time multi-asset planner | EUR/JPY H1 session preparation | Has limited monitoring time and needs a concise plan with invalidation. |
| EUR/JPY intraday specialist | EUR/JPY M15 event-window check | Needs structure-aware levels and JPY-specific risk context; rejects stale or fabricated data. |
| Stock/index discretionary trader | SPX500 H4 comparison workflow | Needs the same evidence/scenario structure for a non-FX instrument. |
| Volatility and catalyst monitor | XAUUSD H1 comparison workflow | Needs explicit uncertainty and volatility-aware risk warnings. |

## Executed journeys

| User | Simulated input | Result | Observed outcome |
|---|---|---|---|
| Part-time multi-asset planner | EURJPY, H1, bid 185.420, ATR 0.180 | PASS, quota 1/25 | BUY, MEDIUM confidence; entry 185.420, stop 184.920, invalidation 184.800; calendar available, grounded=false. |
| EUR/JPY intraday specialist | EURJPY, M15, bid 185.420, ATR 0.090 | PASS, quota 2/25 | NEUTRAL, MEDIUM confidence; no price levels; calendar available, grounded=false. |
| Stock/index discretionary trader | SPX500, H4, bid 5800.0, ATR 35.0 | PASS, quota 3/25 | BUY, MEDIUM confidence; entry 5800.0, stop 5770.0, invalidation 5760.0; calendar available, grounded=false. |
| Volatility and catalyst monitor | XAUUSD, H1, bid 2740.50, ATR 18.0 | PASS, quota 4/25 | NEUTRAL, MEDIUM confidence; no price levels; calendar available, grounded=false. |

## Error and boundary checks

- Missing `tech_summary`: HTTP 422. The API rejects incomplete input rather than silently
  substituting it.
- Invalid license key: HTTP 403. The API rejects unauthorized analysis.
- Account binding: the first run for a second account was HTTP 403 because the existing demo
  license had already reached its two-account limit. Retrying the two personas on the
  already-bound simulated account succeeded. This is a real MVP constraint, not a user
  failure.

## Scenario coverage

- **US-01 Select an instrument:** partially covered by submitting EURJPY, SPX500, and XAUUSD;
  the MT4 chart-selection interaction was not observed.
- **US-02 Submit market inputs:** covered at the EA/API boundary by successful submissions and
  the 422 incomplete-input check. Image/CSV upload is not part of this workflow.
- **US-03 Receive decision and risk brief:** covered. Responses included instrument-specific
  signal, confidence, entry/stop/invalidation where applicable, and warnings.
- **US-04 Inspect uncertainty and hidden risks:** partially covered. The API returns confidence,
  hidden-risk text, warnings, calendar status, and grounded status, but it has no source-detail
  or expandable evidence endpoint.
- **US-05 Ask a follow-up question:** not supported by this MVP endpoint. There is no
  follow-up-question route or session identifier in the API response.
- **US-06 Compare a second workflow:** covered by SPX500 and XAUUSD submissions using the same
  core request/response shape. This validates structural reuse, not comparative trading
  performance.

## Findings

1. The endpoint can accept simulated users across FX, index, and commodity symbols and returns a
   risk-shaped result without allowing incomplete requests.
2. The response exposes `grounded=false`, which should remain visible to users; these outputs
   must not be presented as live, source-verified analysis.
3. Instrument selection is accepted, but the same endpoint contract does not yet provide the
   richer pilot workflow: source inspection, persistent session context, or follow-up questions.
4. The account-binding limit can block a new simulated user before analysis. A future user
   simulation harness should provision isolated demo licenses or reuse a documented test account.
5. A complete visual simulation still needs screenshots and observations for landing, plan choice,
   login/signup, dashboard/license key, EA download/configuration, MT4 result, and post-analysis
   usage display.
