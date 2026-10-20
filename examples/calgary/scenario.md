# Affordability scenario (illustrative)

**This household is fictional.** The figures below are assumptions chosen for the demo.

| Input | Value | Basis |
|---|---|---|
| Purchase price | $665,000 | Jayman "from the $660,000s" Glacier Ridge laned home, e.g. the Brooklyn 20 (about 1,450 sq ft). Assumption within the band |
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

## Other options in the same community

The report compares three price points at 10% down, 25 years, 4.0% and the same income:

| Option | Assumed price | Mortgage incl. insurance | Monthly | At qualifying rate (6.00%) | Stressed payment / income |
|---|---|---|---|---|---|
| Paired, "low $500Ks" (Cedarglen band) | $520,000 | about $482,500 | about $2,538 | about $3,087 | 24.7% |
| Laned, "from $660Ks" (Jayman Brooklyn 20) | $665,000 | about $617,100 | about $3,246 | about $3,948 | 31.6% |
| Front drive, "low $700Ks" (Cedarglen, e.g. Carbon) | $725,000 | about $672,700 | about $3,539 | about $4,304 | 34.4% |

Regenerate with `python3 scripts/build_report.py examples/calgary demo/report.html`.
