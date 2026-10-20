# Framework

Shared method for the project. Your own figures live in `PRIVATE-FINANCES.md` and `PROJECT-GUIDE.md` (both gitignored); this file holds only the method.

**Legend:** ✅ Confirmed · ❓ Needs input · ⚠️ Recently-changed rule — verify with a professional before relying on it

## Research output schema

Every file in `builders/` and `communities/` must start with this exact frontmatter. Fill what's known, leave the rest `null`, never delete a field. Identical fields every time is what makes parallel research comparable and scoreable. Narrative sections follow, with the same headers every time.

### Community files (`communities/<slug>.md`)

```yaml
---
type: community
name: ""
slug: ""
last_updated: YYYY-MM-DD
price_starting: null            # lowest price for a home matching your fixed requirements
price_range: [null, null]
sqft_range_available: [null, null]
builders_present: []
schools: []
commute_minutes: null
community_fee_annual: null
transit_access: none|partial|full
future_development_notes: ""
data_confidence: low|medium|high   # how much is source-verified vs inferred
sources:
  - {field: "price_range", url: "", date: "YYYY-MM-DD"}
---

## Overview & Location
## Schools (detail)
## Parks & Amenities
## Future Development / Risks
## Open Questions
```

### Builder files (`builders/<slug>.md`)

```yaml
---
type: builder
name: ""
slug: ""
last_updated: YYYY-MM-DD
price_starting: null
price_range: [null, null]
matching_floorplans: []
sqft_range_offered: [null, null]
deposit_structure: ""
build_timeline_months: null
warranty_provider: ""
superintendent_quality: unknown|poor|mixed|good|excellent
subcontractor_quality: unknown|poor|mixed|good|excellent
build_quality_reputation: unknown|poor|mixed|good|excellent
social_signal_summary: ""
data_confidence: low|medium|high
sources:
  - {field: "", url: "", date: ""}
---

## Overview
## Pricing & Included Features
## Matching Floorplans
## Upgrade Options & Pricing
## Build Quality & Trades
## Reputation / Reviews / Social Signals
## Open Questions
```

`data_confidence` and `sources` are required. A file with unsourced numbers is `data_confidence: low`. First-hand data (show-home visits, quotes from sales staff) is high confidence and outranks website figures.

Mark quality fields `unknown` when evidence is thin, `mixed` when reports conflict (and explain in the narrative). Don't guess.

## Scoring method

A hybrid approach: formulas where the data supports them, judgment (1–5, read from the narrative) elsewhere.

**Computed criteria**
- *All-in price*: 5 at or below your target price, 1 at your ceiling, linear between. Missing price → "insufficient data".
- *Affordability scenarios*: taken from the financial-analyst's output, never estimated by the scorer.

**Subjective criteria** (1–5): community feel, build quality, kitchen, layout features you care about, deposit structure, energy package, long-term resale.

**Weights** — set these to match your priorities; they must sum to 100%.

| Criterion | Weight |
|---|---|
| All-in price | % |
| Affordability scenarios | % |
| Build quality | % |
| _your criteria…_ | % |

Contribution = score × weight. Sum for the ranking. Revisit as priorities shift.

## Programs & rules log

Record what changed, when it was confirmed and the source. These go stale, so the financial-analyst must re-verify before using any of them in a live calculation.

- Down-payment/withdrawal program limits
- Stress-test qualifying rate
- Insured-mortgage price cap and amortization rules
- First-time buyer rebates and tax rules
- Land title / transfer fees in your jurisdiction

## Open questions

Running list. Add when something is unresolved, remove when it's answered.
