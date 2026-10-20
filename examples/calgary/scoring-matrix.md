# Scoring matrix (illustrative weights)

Weights are placeholders. Set your own in `docs/framework.md`.
Scores come only from what the research files support; everything else is `insufficient data`, and nothing here is a recommendation.

| Criterion | Weight | Jayman BUILT @ Glacier Ridge | Cedarglen @ Glacier Ridge |
|---|---|---|---|
| All-in price (computed vs $720K target, $825K ceiling) | 35% | 5 | 5 |
| Single-income affordability (from financial-analyst) | 25% | needs analysis | needs analysis |
| Build quality | 20% | insufficient data | insufficient data |
| Community feel | 10% | insufficient data | insufficient data |
| Deposit structure | 10% | insufficient data | insufficient data |

**Confidence:** both options are web-only and `data_confidence: low`, so the one scored row is tentative. The demo's point is that the matrix says what it does not know instead of filling in the gaps.

Price rule from `docs/framework.md`: 5 at or below the target price, 1 at the ceiling, linear between. Both starting prices are under the $720K target, so both score 5. This is a poor discriminator on its own; it only becomes useful once real quotes and the affordability scenario are in.
