# AGENTS.md — EUR/JPY brief pilot analytics

## Product directive (owned by the human; the agent never edits this section)

The terminal is for time-constrained part-time and multi-asset traders. It turns user-supplied market
inputs into a concise, instrument-aware decision and risk brief so they can plan a session without
manually assembling several tools. It keeps evidence, interpretation and uncertainty apart.

Must not change without the product owner (dated entry in docs/decisions.md):
1. Every brief is tied to the selected instrument and analysis time.
2. Every material claim has a source or input context; missing data is stated, never invented.
3. Every scenario has invalidation conditions and a risk warning.
4. The product supports a decision; it never presents a guaranteed trade and never executes one.
5. The user controls which inputs are submitted and can challenge the brief.

## This repo

Python package `pilot_analytics` (src/): turns pilot events into funnel summaries (event_schema in
docs/analysis/event_schema.md) and checks briefs against the invariants above. Spec: specs/001-pilot-analytics/spec.md.

## Commands

- Install: `pip install -e ".[dev]"`
- All tests: `pytest -q`      One test: `pytest tests/test_funnel.py::test_name -q`
- Lint/format: `ruff check --fix . && ruff format .`

## Tests (mandatory)

- Tests come first: one failing test, run it and SHOW the failure, then the minimum code, then refactor.
- Never edit, delete, skip, xfail or weaken anything under tests/ unless the task says so.
  If a test looks wrong, stop and say why.
- No special cases for test inputs. No new dependency without asking. No real network or LLM calls in tests.
- Done = `pytest -q` green + ruff clean, with the last output line pasted in your final message.

## Always on

1. Requirements and situations before code (spec first).
2. Run the tests yourself before "done"; no claim without command + output.
3. Every number carries source, date and kind (open/partial/research/assumption/simulated).
4. Unsure? Write the question with your default, apply it, log it in docs/decisions.md, continue.
5. One task per branch; small PRs; Conventional Commits with `Refs: #<issue>` and a Co-authored-by trailer.
6. No personal data, no keys, no broker identifiers, no financial data from participants.

## Read when

- analysing data or estimating a market -> rules/ANALYTICS_RULES.md (copy from the session-10 pack)
- planning, coding, testing, committing -> rules/DEVELOPMENT_RULES.md
- critiquing a screen with simulated users -> rules/USER_SIMULATION.md
