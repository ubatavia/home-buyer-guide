#!/usr/bin/env python3
"""Mortgage payment calculator with an optional stress test.

All rates are inputs. Nothing here hardcodes a rate or program rule, because
those change. Look up the current figures and pass them in.

Example:
    python3 scripts/affordability.py --price 750000 --down 100000 \
        --rate 4.5 --years 25 --stress-rate 6.5
"""
import argparse
import sys


def monthly_payment(principal: float, annual_rate_pct: float, years: int) -> float:
    """Standard amortized payment, monthly compounding."""
    n = years * 12
    r = annual_rate_pct / 100 / 12
    if r == 0:
        return principal / n
    return principal * r / (1 - (1 + r) ** -n)


def analyse(price, down, rate, years, stress_rate=None, monthly_income=None):
    if down >= price:
        raise ValueError("down payment must be less than price")
    principal = price - down
    pay = monthly_payment(principal, rate, years)
    out = {
        "price": price,
        "down": down,
        "down_pct": down / price * 100,
        "principal": principal,
        "monthly_payment": pay,
        "total_interest": pay * years * 12 - principal,
    }
    if stress_rate is not None:
        out["stress_rate"] = stress_rate
        out["stress_payment"] = monthly_payment(principal, stress_rate, years)
    if monthly_income:
        out["payment_to_income_pct"] = pay / monthly_income * 100
        if stress_rate is not None:
            out["stress_payment_to_income_pct"] = out["stress_payment"] / monthly_income * 100
    return out


def render(r: dict) -> str:
    lines = [
        "INPUTS",
        f"  Price:            ${r['price']:,.0f}",
        f"  Down payment:     ${r['down']:,.0f} ({r['down_pct']:.1f}%)",
        f"  Mortgage amount:  ${r['principal']:,.0f}",
        "",
        "RESULT",
        f"  Monthly payment:  ${r['monthly_payment']:,.2f}",
        f"  Total interest:   ${r['total_interest']:,.0f}",
    ]
    if "stress_payment" in r:
        lines.append(f"  At stress rate {r['stress_rate']}%: ${r['stress_payment']:,.2f}/mo")
    else:
        lines.append("  Stress test:      skipped (pass --stress-rate with the current qualifying rate)")
    if "payment_to_income_pct" in r:
        lines.append(f"  Payment / gross monthly income: {r['payment_to_income_pct']:.1f}%")
    lines += ["", "Excludes: mortgage default insurance, property tax, heat, closing costs.",
              "Not financial advice. Confirm with a licensed mortgage professional."]
    return "\n".join(lines)


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--price", type=float, required=True)
    p.add_argument("--down", type=float, required=True)
    p.add_argument("--rate", type=float, required=True, help="annual contract rate, percent")
    p.add_argument("--years", type=int, default=25, help="amortization in years")
    p.add_argument("--stress-rate", type=float, help="qualifying rate for the stress test, percent")
    p.add_argument("--monthly-income", type=float, help="gross monthly household income")
    a = p.parse_args(argv)
    try:
        print(render(analyse(a.price, a.down, a.rate, a.years, a.stress_rate, a.monthly_income)))
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
