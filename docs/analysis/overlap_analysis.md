# Overlap analysis — qualified audience

## Method

Notebook Block 8b combines:

- `N`: Spain population by age band from Eurostat `demo_pjangroup`, 2024
- `B`: paid health/fitness-app subscription share from Eurostat `isoc_ec_ibgs`, 2025
- `A`: people who want to build a habit and struggle, an explicit assumption
- `q = P(A and B | age band)`, with Fréchet bounds

The independence estimate is `q = P(A)P(B)`. It is not presented as fact. A bridge estimate uses Ritmo paid rates among existing habit-app users, but this is not the same definition as Eurostat's paid health/fitness-app subscription measure.

## Results

| Age band | N | Assumed A | B | q low | q independent | q high | q bridge | Bridge valid? |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| 18–24 | 3,660,708 | 35% | 10.1% | 0.0% | 3.5% | 10.1% | 6.9% | Yes |
| 25–34 | 5,462,028 | 35% | 12.3% | 0.0% | 4.3% | 12.3% | 7.4% | Yes |
| 35–44 | 6,706,754 | 35% | 11.1% | 0.0% | 3.9% | 11.1% | 6.3% | Yes |
| 45–54 | 7,966,380 | 30% | 7.3% | 0.0% | 2.2% | 7.3% | 6.0% | Yes |
| 55–74 | 11,883,870 | 25% | 3.1% | 0.0% | 0.8% | 3.1% | 5.0% | **No** |

Summed qualified-audience bounds:

- Fréchet lower bound: **0**
- Independence estimate: **891,644**
- Fréchet upper bound: **2,735,044**
- Bridge estimate: **2,148,308**, but it violates the upper bound for 55–74

## Interpretation and limitations

The lower bound is zero because the assumed problem and budget rates do not force any overlap. The independence figure is only an assumption-based scenario. The bridge mismatch in the 55–74 group demonstrates that the two budget definitions are not aligned; it must not be used as a validated estimate.

This block is a class-method demonstration using habit-app data. It is **not** a qualified audience estimate for forex, stocks, indices, commodities, or crypto traders. A trading-specific bridge study must measure active trading, instrument focus, problem severity, and willingness to pay in the same respondents.
