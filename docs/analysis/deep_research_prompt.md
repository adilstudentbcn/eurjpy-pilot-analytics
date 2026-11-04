# Deep-research prompt — trading-product validation

## Objective

Replace the weakest assumptions in the Day 9 niche estimate with checked evidence for a multi-market trading intelligence product. EUR/JPY is the validated prototype; compare forex, stocks/indices, commodities, crypto, and part-time multi-asset traders.

## Questions

1. What share of active retail traders use a paid charting, research, alert, or trading-journal product?
2. What monthly price ranges are publicly observed for comparable products in each category?
3. Which workflows are underserved: off-calendar catalyst detection, scenario planning, invalidation/risk levels, data aggregation, or follow-up explanation?
4. Which acquisition channels reach each group, and what evidence supports that claim?

## Evidence rules

- Open two independent sources for every market or price figure.
- Record URL, publisher, publication date, access date, population definition, geography, and unit.
- Do not use a provider's total market figure as a trader count without a documented bridge.
- Keep estimates as ranges.
- Mark unverified numbers as `assumption`; only move them to `research` after checking the original sources.
- Do not use simulated personas as market levels.
- Separate active traders from investors, account holders, and social-media followers.

## Required output

Return a table with:

`input, low, high, unit, kind, source_1, source_2, access_date, definition, bias_or_gap`

End with the single input that most reduces uncertainty and the proposed next measurement method.
