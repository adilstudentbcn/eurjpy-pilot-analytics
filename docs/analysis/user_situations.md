# User situations — validation pilot

These situations define the first observable workflow. IDs are stable so interview notes, events, and test results can refer to the same behavior.

## US-01 — Set up the MT4 workflow and select an instrument

**Given:** a participant opens the pilot landing page and chooses a subscription plan.

**When:** they create an account or log in, copy the license key, download the Expert Advisor,
attach it to MetaTrader 4, and select EUR/JPY, a stock/index instrument, or a commodities/crypto
instrument on an MT4 chart.

**Then:** the license and plan are visible in the dashboard, the EA can connect to the server,
and the selected instrument and asset category are included in the analysis request.

## US-02 — Submit market inputs

**Given:** an instrument is selected.

**When:** the EA submits the chart and account context: license key, account number, broker server,
symbol, timeframe, bid/ask, ATR, and chart summary. Calendar and news are fetched server-side.

**Then:** the server validates the license, account binding, quota, and required fields, and
returns explicit errors instead of silently substituting missing data.

## US-03 — Receive the decision and risk brief

**Given:** the minimum required inputs are available.

**When:** the participant requests analysis from the EA.

**Then:** the brief identifies the instrument and analysis time, separates evidence from interpretation, presents scenarios, and states invalidation conditions and risk warnings.

## US-04 — Inspect uncertainty and hidden risks

**Given:** a brief has been generated.

**When:** the participant inspects the risk, confidence, grounded status, calendar/news status,
or dashboard usage after an analysis.

**Then:** the relevant input or source context is visible, missing information is labelled, and no unsupported certainty is added.

## US-05 — Ask a follow-up question

**Given:** a participant disagrees with or does not understand part of the brief.

**When:** they ask a follow-up question tied to the selected instrument and analysis session.

**Then:** the response remains tied to the supplied evidence, identifies uncertainty where relevant, and does not change the original record without showing what changed.

## US-06 — Compare a second workflow

**Given:** the participant has completed one workflow.

**When:** they run a stock/index or commodities/crypto workflow.

**Then:** the same core structure is used, instrument-specific risks are visible, and the results can be compared without claiming that one category is better from a single participant.

## Acceptance checklist

- The account/dashboard steps can be completed in a browser; the analysis step runs in MetaTrader 4.
- Empty, incomplete-input, and failed-analysis states are explicit.
- The selected instrument and analysis time remain visible throughout the result.
- The result contains evidence context, scenarios, invalidation conditions, and risk warnings.
- Follow-up questions cannot silently introduce unsupported market facts.
- The old image/CSV upload prototype is not part of the current workflow.
