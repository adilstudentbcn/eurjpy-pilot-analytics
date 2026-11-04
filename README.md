# EUR/JPY brief pilot analytics

Small Python package for the validation pilot of a browser trading assistant that turns calendar
screenshots, a chart and optional price data into an instrument-aware brief with scenarios,
invalidation conditions and risks.

## What it does
- `funnel_summary(events)`: pilot funnel from raw events: unique sessions, conditional rates with visible
  denominators, activation rule, missing-field report.
- `validate_brief(brief)`: lists violations of the product directive's invariants 1-4.

## What it does not do
No trade execution. No market-size or conversion claims (a pilot alone cannot make them). No personal
or financial data. No live data feed. It does not call any AI model.

## Run
    python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
    pip install -e ".[dev]"
    pytest -q

## Docs
specs/001-pilot-analytics/spec.md · docs/adr/ · docs/analysis/ (niche, audience, competitors) · AGENTS.md
