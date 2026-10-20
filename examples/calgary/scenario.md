# Affordability scenario (illustrative)

**This household is fictional.** The figures below are assumptions chosen for the demo.

| Input | Value | Basis |
|---|---|---|
| Purchase price | $665,000 | Jayman "from the $660,000s" Glacier Ridge laned home (assumption within the band) |
| Down payment | $66,500 (10%) | Assumed. Minimum for this price is $41,500 |
| Contract rate | 4.0% | Assumption. Sources put 5-year fixed near 4% in spring 2026; get a live quote |
| Amortization | 25 years | Assumed |
| Gross household income | $150,000/yr ($12,500/mo) | Assumed |

Run it:

```bash
python3 scripts/affordability.py --price 665000 --down 66500 --rate 4.0 --years 25 \
  --insured --first-time --stress-auto --monthly-income 12500
```

Result at the time of writing: mortgage payment about $3,246/month, or about $3,948/month at the 6.00% qualifying rate (the greater of contract rate + 2% or 5.25%), which is 31.6% of gross monthly income before property tax and utilities. A lender will apply its own debt-service limits, so this is a screening number only.

**Not included:** property tax, utilities, legal fees, and the First-Time Home Buyers' GST rebate. Jayman's price already states it includes GST, so check with the builder how a rebate would be handled.
