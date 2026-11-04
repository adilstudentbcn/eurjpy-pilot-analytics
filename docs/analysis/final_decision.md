# Day 9 final decision and next research

## Class-method result

The notebook's final habit-app scenario ranked **remote workers at €7.99** first by P10:

- P10: €189,500
- P50: €418,500
- P90: €809,600

Sensitivity was highest for:

1. Reach share: Spearman absolute correlation 0.80
2. Habit-app adoption share: 0.57
3. Paid rate: 0.09
4. Price-screen share: 0.01

## What this does and does not mean

These are not forecasts for the multi-market trading product. They inherit habit-app populations, Ritmo conversion data, broad assumptions, and a simulated €7.99 response. The ranking is useful only as a demonstration that pessimistic-case ranking and sensitivity analysis are better than choosing the highest median.

## Provisional product decision

Do not launch based on the current revenue numbers. The evidence supports testing the product, not declaring product-market fit. The first test should use the validated EUR/JPY workflow and compare it with at least one stock/index and one commodities or crypto workflow.

## Next measurement

Run a trading-specific fake-door test with separate landing pages for:

1. Forex intraday traders — EUR/JPY first
2. Stock/index traders
3. Part-time multi-asset traders

Test €4.99, €9.99, and €19.99 monthly offers. Measure visits, instrument selection, input upload/connect intent, pre-orders, and qualified interviews. Replace the notebook placeholder fake-door counts with real observations and update the ledger.

## Day 10 productization additions

The Day 10 material adds a product-validation layer without changing the evidence conclusion:

- [trading_product_brief.md](./trading_product_brief.md) defines the working pilot target, promise, funnel, and out-of-scope items.
- [product_directive.md](./product_directive.md) freezes the pilot invariants against feature drift.
- [user_situations.md](./user_situations.md) defines six observable workflow situations with acceptance checks.
- [event_schema.md](./event_schema.md) defines privacy-conscious funnel events and data-quality rules.
- [ux_validation_plan.md](./ux_validation_plan.md) defines a two-run simulated UX critique and capped triage wave.

These documents are implementation and measurement hypotheses, not new market evidence. The first target remains provisional and must be tested with real trading users.

## Pilot materials

- [pilot_landing_copy.md](./pilot_landing_copy.md) contains neutral landing-page variants and qualification fields.
- [pilot_interview_script.md](./pilot_interview_script.md) contains the consent opening, workflow task, and debrief questions.
- [pilot_measurement_sheet.md](./pilot_measurement_sheet.md) provides the funnel, segment comparison, and interview evidence tables.
