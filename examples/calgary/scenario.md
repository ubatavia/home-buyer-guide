# Affordability scenario (illustrative)

**The household is fictional.** Income, down payment and contract rate are assumptions for the demo. The prices are builders' Glacier Ridge starting prices (not quotes), with GST added to Jayman's so the comparison is like for like.

| Input | Value | Basis |
|---|---|---|
| Purchase price | $725,000 | Cedarglen Windsor, starting at $725,000 in Glacier Ridge including lot and GST (2,238 sq ft) |
| Down payment | $72,500 (10%) | Assumed. Minimum for this price is $53,750 |
| Contract rate | 4.0% | Assumption. Sources put 5-year fixed near 4% in spring 2026; get a live quote |
| Amortization | 25 years | Assumed |
| Gross household income | $150,000/yr ($12,500/mo) | Assumed |
| Residents' Association fee | $498.02/yr | Glacier Ridge Residents' Association, 2026, single-family, GST included; mandatory, registered on title |

Run it:

```bash
python3 scripts/affordability.py --price 725000 --down 72500 --rate 4.0 --years 25 \
  --insured --first-time --stress-auto --monthly-income 12500 --annual-fees 498.02
```

## Same-size plans compared

All at 10% down, 25 years, 4.0%, $150K income, qualifying rate 6.00% (greater of contract rate + 2% or 5.25%). Jayman prices include 5% GST.

| Option | Price | $ per sq ft | Mortgage incl. insurance | Monthly | At qualifying rate | Stressed payment / income |
|---|---|---|---|---|---|---|
| Jayman Brooklyn 20 (1,450 sq ft) | $546,000 | $377 | $506,633 | $2,665 | $3,241 | 25.9% |
| **Cedarglen Windsor (2,238 sq ft)** | **$725,000** | **$324** | **$672,728** | **$3,539** | **$4,304** | **34.4%** |
| **Jayman Karma 24 (2,261 sq ft)** | **$787,500** | **$348** | **$730,721** | **$3,844** | **$4,675** | **37.4%** |
| Jayman Holly 24 (2,436 sq ft) | $808,500 | $332 | $750,207 | $3,946 | $4,800 | 38.4% |

The Windsor and Karma are the closest pair. The Windsor works out to roughly $305 a month less, before the association fee ($41.50 a month), property tax and utilities. A lender applies its own debt-service limits, so these are screening numbers only.

Regenerate with `python3 scripts/build_report.py examples/calgary demo/report.html`.

**Not included:** property tax, utilities, legal fees, and the First-Time Home Buyers' GST rebate. If you qualify, the rebate can change Jayman's effective price relative to Cedarglen's GST-included price. Confirm eligibility with the builder and your lawyer.
