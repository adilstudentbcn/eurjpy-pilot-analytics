# UX validation plan — trading intelligence terminal

## Objective

Find usability problems in the core trading workflow before interpreting behavior as demand. Simulated-persona findings are hypotheses and must not be used as market rates.

## Personas

Use four fictional personas:

1. **Part-time multi-asset trader:** laptop, limited monitoring time, switches instruments.
2. **EUR/JPY intraday trader:** phone and laptop, expects macro and geopolitical risk detail.
3. **Stock/index trader:** laptop, expects earnings and macro-event context.
4. **Cautious commodities/crypto trader:** phone, sensitive to volatility warnings and unsupported certainty.

Each persona must include a goal, device, available time, existing knowledge, at least two likely mistakes, and a reason they would abandon the workflow.

## Two critique runs

Run each persona twice from a fresh start. Show only the current prototype stage. Record:

- screen or step;
- action attempted;
- observed problem;
- severity from 1–4;
- usability heuristic;
- suggested change;
- whether the finding appeared in both runs.

## Triage rules

Accept no more than five changes in one wave. For every change, record:

- finding IDs covered;
- personas affected;
- ACCEPT, DEFER, or REJECT;
- reason tied to the product directive;
- screens and invariant checks to re-walk.

Reject requests that would:

- hide missing or uncertain evidence;
- imply guaranteed profitability;
- remove instrument-specific context;
- execute trades without explicit user control;
- broaden the product before the core workflow is usable.

## Re-walk after implementation

Repeat the same personas and steps after accepted changes. At least one re-walk must verify:

- selected instrument remains visible;
- source or input context remains inspectable;
- invalidation and risk warnings remain present;
- incomplete or failed input states remain explicit.

## Evidence boundary

The UX wave informs interface changes only. Demand, willingness to pay, retention, and market size require the real pilot and the event schema in [event_schema.md](./event_schema.md).
