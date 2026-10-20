#!/usr/bin/env python3
"""Mortgage affordability calculator for Canada/Alberta with a stress test.

Rates are always inputs. Program rules (stress-test buffer, insurance premium
tiers, land title fees) come from data/rules-ca-ab.json, which is dated and
sourced and must be re-verified before you rely on it.

Example:
    python3 scripts/affordability.py --price 665000 --down 66500 --rate 4.0 \
        --years 25 --insured --first-time --stress-auto --monthly-income 12500
"""
import argparse
import json
import math
import os
import sys

RULES_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "rules-ca-ab.json")


def load_rules(path=RULES_PATH):
    with open(path) as f:
        return json.load(f)


def monthly_rate(annual_pct: float, compounding: str) -> float:
    """Effective monthly rate. Canadian fixed mortgages compound semi-annually."""
    r = annual_pct / 100
    if compounding == "semi-annual":
        return (1 + r / 2) ** (1 / 6) - 1
    return r / 12


def monthly_payment(principal: float, annual_rate_pct: float, years: int,
                    compounding: str = "semi-annual") -> float:
    n = years * 12
    i = monthly_rate(annual_rate_pct, compounding)
    if i == 0:
        return principal / n
    return principal * i / (1 - (1 + i) ** -n)


def min_down_payment(price: float, rules: dict) -> float:
    m = rules["default_insurance"]["min_down_payment"]
    cap = m["first_tier_cap"]
    first = min(price, cap) * m["first_tier_pct"] / 100
    rest = max(price - cap, 0) * m["remainder_pct"] / 100
    return first + rest


def insurance_premium_pct(ltv_pct: float, years: int, surcharge_eligible: bool, rules: dict) -> float:
    """Premium as a percent of the loan; 0 when no insurance is needed (LTV <= 80)."""
    if ltv_pct <= 80:
        return 0.0
    ins = rules["default_insurance"]
    for tier in ins["premium_pct_by_ltv"]:
        if ltv_pct <= tier["max_ltv_pct"]:
            pct = tier["premium_pct"]
            if years > 25 and surcharge_eligible:
                pct += ins["amortization_30yr_surcharge_pct"]
            return pct
    raise ValueError("loan-to-value above 95% cannot be insured")


def land_title_fee(value: float, rules: dict) -> float:
    lt = rules["alberta_land_titles"]
    return lt["base_fee"] + math.ceil(value / 5000) * lt["per_5000_of_value"]


def analyse(price, down, rate, years, stress_rate=None, monthly_income=None,
            compounding="semi-annual", insured=False, first_time=False, rules=None,
            annual_fees=0.0):
    rules = rules or load_rules()
    if down >= price:
        raise ValueError("down payment must be less than price")
    loan = price - down
    ltv = loan / price * 100
    out = {"price": price, "down": down, "down_pct": down / price * 100,
           "loan": loan, "ltv_pct": ltv, "rate": rate, "years": years,
           "compounding": compounding, "premium": 0.0, "premium_pct": 0.0}

    if insured:
        minimum = min_down_payment(price, rules)
        if down < minimum:
            raise ValueError(f"down payment below the minimum of ${minimum:,.0f} for this price")
        if price > rules["default_insurance"]["insured_price_cap"]:
            raise ValueError("price above the insured-mortgage cap")
        out["premium_pct"] = insurance_premium_pct(ltv, years, first_time, rules)
        out["premium"] = loan * out["premium_pct"] / 100
    elif ltv > 80:
        raise ValueError("down payment under 20% requires --insured")

    mortgage = loan + out["premium"]
    out["mortgage"] = mortgage
    out["monthly_payment"] = monthly_payment(mortgage, rate, years, compounding)
    out["total_interest"] = out["monthly_payment"] * years * 12 - mortgage
    out["annual_fees"] = annual_fees
    out["monthly_with_fees"] = out["monthly_payment"] + annual_fees / 12
    out["title_fees"] = land_title_fee(price, rules) + land_title_fee(mortgage, rules)

    if stress_rate is not None:
        out["stress_rate"] = stress_rate
        out["stress_payment"] = monthly_payment(mortgage, stress_rate, years, compounding)
    if monthly_income:
        out["payment_to_income_pct"] = out["monthly_payment"] / monthly_income * 100
        if stress_rate is not None:
            out["stress_to_income_pct"] = out["stress_payment"] / monthly_income * 100
    return out


def render(r: dict) -> str:
    L = [
        "INPUTS",
        f"  Price:               ${r['price']:>12,.0f}",
        f"  Down payment:        ${r['down']:>12,.0f}  ({r['down_pct']:.1f}%)",
        f"  Contract rate:       {r['rate']}%  ({r['compounding']} compounding, {r['years']}-yr amortization)",
        "",
        "MORTGAGE",
        f"  Loan before premium: ${r['loan']:>12,.0f}",
    ]
    if r["premium"]:
        L.append(f"  Default insurance:   ${r['premium']:>12,.0f}  ({r['premium_pct']:.2f}%, added to the mortgage)")
    L += [
        f"  Mortgage amount:     ${r['mortgage']:>12,.0f}",
        f"  Monthly payment:     ${r['monthly_payment']:>12,.2f}",
        f"  Total interest:      ${r['total_interest']:>12,.0f}",
    ]
    if r.get("annual_fees"):
        L.append(f"  + Association fee:   ${r['annual_fees']:>12,.2f}/yr -> ${r['monthly_with_fees']:,.2f}/mo together")
    if "stress_payment" in r:
        L.append(f"  Stress payment @ {r['stress_rate']:.2f}%: ${r['stress_payment']:,.2f}/mo")
    else:
        L.append("  Stress test:         skipped (pass --stress-rate or --stress-auto)")
    if "payment_to_income_pct" in r:
        L += ["", "AFFORDABILITY",
              f"  Payment / gross monthly income: {r['payment_to_income_pct']:.1f}%"]
        if "stress_to_income_pct" in r:
            L.append(f"  Stressed payment / income:      {r['stress_to_income_pct']:.1f}%")
    L += ["", "ONE-TIME COSTS (estimate)",
          f"  Alberta land title + mortgage registration: ${r['title_fees']:,.0f}",
          "",
          "Excludes property tax, utilities, legal fees, GST/rebates and closing adjustments.",
          "Rules come from data/rules-ca-ab.json. Verify before relying on them.",
          "Not financial advice. Confirm with a licensed mortgage professional."]
    return "\n".join(L)


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--price", type=float, required=True)
    p.add_argument("--down", type=float, required=True)
    p.add_argument("--rate", type=float, required=True, help="annual contract rate, percent")
    p.add_argument("--years", type=int, default=25, help="amortization in years")
    p.add_argument("--compounding", choices=["semi-annual", "monthly"], default="semi-annual")
    p.add_argument("--insured", action="store_true", help="add default-insurance premium (needed under 20%% down)")
    p.add_argument("--first-time", action="store_true", help="first-time buyer or new build (30-yr surcharge applies)")
    p.add_argument("--stress-rate", type=float, help="qualifying rate, percent")
    p.add_argument("--stress-auto", action="store_true",
                   help="derive the qualifying rate from data/rules-ca-ab.json")
    p.add_argument("--annual-fees", type=float, default=0.0, help="community/residents' association fee per year")
    p.add_argument("--monthly-income", type=float, help="gross monthly household income")
    a = p.parse_args(argv)
    try:
        rules = load_rules()
        stress = a.stress_rate
        if a.stress_auto:
            s = rules["stress_test"]
            stress = max(a.rate + s["buffer_pct"], s["floor_pct"])
        print(render(analyse(a.price, a.down, a.rate, a.years, stress, a.monthly_income,
                             a.compounding, a.insured, a.first_time, rules, a.annual_fees)))
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
