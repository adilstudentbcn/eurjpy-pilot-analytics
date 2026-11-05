# EUR/JPY brief pilot analytics

Small Python package for the validation pilot of an MT4-connected trading assistant. The current
MVP uses a thin MetaTrader 4 Expert Advisor that sends user-controlled chart context to a local
FastAPI service, which returns an instrument-aware brief with scenarios, invalidation conditions,
and risks.

## What it does
- `funnel_summary(events)`: pilot funnel from raw events: unique sessions, conditional rates with visible
  denominators, activation rule, missing-field report.
- `calculate_funnel_dropoff(frame)`: step-by-step conversion rates for a DataFrame-like object.
- `validate_brief(brief)`: lists violations of the product directive's invariants 1-4.
- `generate_niche_brief(persona_data)`: formats a small persona brief as Markdown.
- `run_user_scenario(name)`: runs a deterministic local journey for the six pilot scenarios.

## What it does not do
No trade execution. No market-size or conversion claims (a pilot alone cannot make them). No personal
or financial data. No live data feed. It does not call any AI model.

## Run
    python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
    pip install -e ".[dev]"
    pytest -q

Run a user scenario from Python:

```python
from pilot_analytics import run_user_scenario

result = run_user_scenario("complete_activation")
print(result["funnel"]["activated_sessions"])
print(result["violations"])
```

Available scenarios: `complete_activation`, `orphan_delivery`, `missing_evidence`,
`missing_risk`, `guarantee_language`, and `repeat_session`.

The prompt-compatibility APIs do not require pandas. `calculate_funnel_dropoff` accepts a
DataFrame-like object exposing `iterrows()` with `stage` and `users` columns.

The earlier HTML upload prototype includes **Research mode: fictional participant**, based on
[`personas.yaml`](./personas.yaml), [`user_situations.md`](./docs/analysis/user_situations.md),
and [`pilot_interview_script.md`](./docs/analysis/pilot_interview_script.md). Select a persona,
start the six-step task, and use **Next step** to rehearse the workflow. These are synthetic
usability walkthroughs, not evidence from real users. It is not the current MT4 workflow.

The current local service is in [`mt4_ai_mvp/`](./mt4_ai_mvp/). Users choose a plan, obtain a
license key from the subscriber dashboard, download the EA, run it inside MT4, and inspect quota
and usage there. The image/CSV upload flow is retired.

## Docs
specs/001-pilot-analytics/spec.md · docs/adr/ · docs/analysis/ (niche, audience, competitors) · AGENTS.md
