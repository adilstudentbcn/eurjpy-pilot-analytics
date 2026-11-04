# Feature: Pilot analytics (funnel summary and brief validation)

## Why
The validation pilot must measure qualified brief activation without inflating it, and every brief must
respect the product directive. Today both are checked by eye. (Seeds: docs/analysis/event_schema.md,
user_situations.md US-02..US-05, product_directive.md.)

## Who
The product owner reading pilot results, and the reviewer checking briefs before a participant sees them.

## User scenarios (Given / When / Then)

### S1 — Activation is not inflated (P1)
Given a session that delivered a brief but never selected an instrument or submitted an input,
when the funnel is summarised, then that session is not counted as activated.

### S2 — Sessions, not events (P1)
Given one session that fired `landing_viewed` three times, when the funnel is summarised,
then the landing stage counts 1 session and the summary reports 3 events.

### S3 — Rates show their denominator (P1)
Given no session reached `instrument_selected`, when conditional rates are computed,
then the rate for the next stage is `None`, never 0 and never a division error.

### S4 — A scenario must say what invalidates it (P1)
Given a brief with a scenario that has no invalidation condition, when it is validated,
then the violation `scenario_without_invalidation` is reported.

### S5 — Guarantee language is refused (P2)
Given a brief that says a trade is guaranteed, when it is validated, then `guarantee_language` is reported.

### S6 — Instrument and time are present (P2)
Given a brief with no instrument (or no analysis time), when validated, then `missing_instrument`
(or `missing_analysis_time`) is reported.

## Edge cases
Empty event list; events with missing common fields; a failure event for a session (never counted as
delivery); briefs with no scenarios; evidence items without a source.

## Functional requirements
- FR-001: `funnel_summary(events)` MUST count unique sessions per stage and report `n_events` separately.
- FR-002: It MUST count a session as activated only if it has `instrument_selected`, `input_submitted`
  and `brief_delivered`.
- FR-003: It MUST return each conditional rate as `None` when its denominator is 0.
- FR-004: It MUST report missing common fields (count per field) and the UTC date range.
- FR-005: `validate_brief(brief)` MUST return a list of violation codes (empty list = valid).
- FR-006: It MUST flag: `missing_instrument`, `missing_analysis_time`, `claim_without_source`,
  `scenario_without_invalidation`, `scenario_without_risk_warning`, `guarantee_language`.

## Success criteria
- SC-001: all S1-S6 have at least one passing test, written before the code.
- SC-002: mutation check (mutmut or by hand: three deliberate breaks) turns at least one test red each time.

## Out of scope
Conversion thresholds; market-size claims; reading screenshots; calling any AI model; executing trades.

## [NEEDS CLARIFICATION]
- Stage order for conditional rates: landing -> instrument -> input_submitted -> brief_requested ->
  brief_delivered. (Default applied; change by a dated entry in docs/decisions.md.)
