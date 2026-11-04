# User situations — validation pilot

These situations define the first observable workflow. IDs are stable so interview notes, events, and test results can refer to the same behavior.

## US-01 — Select an instrument

**Given:** a participant opens the pilot landing page.

**When:** they choose EUR/JPY, a stock/index instrument, or a commodities/crypto instrument.

**Then:** the selected instrument and asset category are recorded, and the next step explains the required inputs.

## US-02 — Submit market inputs

**Given:** an instrument is selected.

**When:** the participant uploads or connects the available calendar, chart, price-data, news, and manual-context inputs.

**Then:** the interface shows which inputs were received, which are missing, and whether the brief can be generated without silently substituting data.

## US-03 — Receive the decision and risk brief

**Given:** the minimum required inputs are available.

**When:** the participant requests analysis.

**Then:** the brief identifies the instrument and analysis time, separates evidence from interpretation, presents scenarios, and states invalidation conditions and risk warnings.

## US-04 — Inspect uncertainty and hidden risks

**Given:** a brief has been generated.

**When:** the participant opens a source, risk, or uncertainty detail.

**Then:** the relevant input or source context is visible, missing information is labelled, and no unsupported certainty is added.

## US-05 — Ask a follow-up question

**Given:** a participant disagrees with or does not understand part of the brief.

**When:** they ask a follow-up question tied to the selected instrument and session.

**Then:** the response remains tied to the supplied evidence, identifies uncertainty where relevant, and does not change the original record without showing what changed.

## US-06 — Compare a second workflow

**Given:** the participant has completed one workflow.

**When:** they run a stock/index or commodities/crypto workflow.

**Then:** the same core structure is used, instrument-specific risks are visible, and the results can be compared without claiming that one category is better from a single participant.

## Acceptance checklist

- Each situation can be completed on a laptop and a phone-sized screen.
- Empty, incomplete-input, and failed-analysis states are explicit.
- The selected instrument and analysis time remain visible throughout the result.
- The result contains evidence context, scenarios, invalidation conditions, and risk warnings.
- Follow-up questions cannot silently introduce unsupported market facts.
