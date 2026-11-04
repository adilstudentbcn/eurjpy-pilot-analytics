# Evidence synthesis — multi-market trading intelligence terminal

## Shared hypothesis

The current hypothesis is:

> A concise, instrument-aware decision and risk brief can create more value for part-time and multi-asset traders than another standalone chart or alert tool.

The evidence is mixed-purpose and mostly indirect. It can guide the next research choice, but it does not yet validate the trading product.

## Weak supervision

The notebook combined 400 App Store reviews and 911 Hacker News comments: **1,311 texts** total.

Five transparent labeling functions looked for:

- recurring unmet need
- paying for a workaround but still missing something
- switching or searching for alternatives
- feature requests
- praise without a reported problem

At least one function labelled 25% of texts. Among labelled texts, 83% were positive for an unmet/paid-for job. This is a label-model result about selected texts, not a share of buyers. The labeling functions are correlated and majority accuracy is not independent validation.

## Triangulation

Five sources ranked remote workers ahead of students:

| Source | Main bias | Remote workers ahead? |
|---|---|---|
| Hacker News conversations | Tech-heavy, vocal posters; few older users | Yes |
| App Store reviews | Review extremes; iPhone users in the US | Yes |
| Ritmo behaviour | Existing habit-app users only | Yes |
| Eurostat spending | Measures health/fitness-app subscriptions, not trading software | Yes |
| Journey simulation | Depends on explicit assumptions | Yes |

This is useful directional agreement because the biases differ, but it is not proof that remote or part-time traders are the best launch niche. The sources are not fully independent: the Ritmo, review, and simulation evidence all relate to habit products.

## Bayesian synthesis

The notebook demonstration joined:

- indirect Ritmo premium conversion evidence
- a broad prior for how a coach might differ from Ritmo
- a **placeholder** fake-door count of 9/400

| Estimate | P5 | P50 | P95 |
|---|---:|---:|---:|
| Indirect Ritmo × delta prior | 0.97% | 6.18% | 11.39% |
| Placeholder fake door alone | 1.36% | 2.41% | 3.88% |
| Synthesis using both | 1.36% | 2.41% | 3.88% |

The placeholder was included only to demonstrate the model. It is not a real trading-product experiment and must be replaced with actual visitors and pre-orders before it informs launch decisions.

## Dempster–Shafer viability view

The class demonstration assigned subjective mass to viability, non-viability, and ignorance:

- Conversations: viable 0.30, unknown 0.70
- Eurostat budget: viable 0.20, not viable 0.05, unknown 0.75
- Ritmo bridge: viable 0.40, not viable 0.10, unknown 0.50
- Placeholder fake door: viable 0.15, not viable 0.45, unknown 0.40

The combined result is not a probability of success. It keeps ignorance visible. The notebook showed that double-counting conversations increases belief from 0.43 to 0.60 without adding information, demonstrating why related sources must not be multiplied as independent evidence.

## Current conclusion

- **Evidence supports:** a research direction around concise guidance, recovery from missed sessions, alerts, and reducing manual synthesis.
- **Evidence does not support:** a trading-market size, a trading conversion rate, a winning instrument category, or a final price.
- **Main unknown:** whether active traders will upload/connect data, trust the brief, return for multiple sessions, and pay.
- **Next evidence:** a trading-specific fake-door test and interviews across forex, stocks/indices, commodities, crypto, and multi-asset traders.
