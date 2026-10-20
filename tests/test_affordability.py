import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
from affordability import (analyse, insurance_premium_pct, land_title_fee,
                           load_rules, min_down_payment, monthly_payment)

RULES = load_rules()


class PaymentTests(unittest.TestCase):
    def test_monthly_compounding_textbook(self):
        # 300,000 at 6% over 30 years, monthly compounding: ~1,798.65
        self.assertAlmostEqual(monthly_payment(300_000, 6, 30, "monthly"), 1798.65, places=2)

    def test_semi_annual_is_cheaper_than_monthly(self):
        self.assertLess(monthly_payment(500_000, 5, 25, "semi-annual"),
                        monthly_payment(500_000, 5, 25, "monthly"))

    def test_zero_rate(self):
        self.assertAlmostEqual(monthly_payment(120_000, 0, 10, "monthly"), 1000.0)


class RulesTests(unittest.TestCase):
    def test_min_down_payment_tiered(self):
        self.assertAlmostEqual(min_down_payment(500_000, RULES), 25_000)
        self.assertAlmostEqual(min_down_payment(665_000, RULES), 41_500)

    def test_premium_tiers(self):
        self.assertEqual(insurance_premium_pct(90, 25, False, RULES), 3.10)
        self.assertEqual(insurance_premium_pct(95, 25, False, RULES), 4.00)
        self.assertEqual(insurance_premium_pct(80, 25, False, RULES), 0.0)

    def test_30yr_surcharge_only_when_eligible(self):
        self.assertAlmostEqual(insurance_premium_pct(90, 30, True, RULES), 3.30)
        self.assertEqual(insurance_premium_pct(90, 30, False, RULES), 3.10)

    def test_land_title_fee(self):
        # 50 base + 5 per 5,000 -> 1,000,000 = 50 + 200*5 = 1,050 (matches the cited example)
        self.assertEqual(land_title_fee(1_000_000, RULES), 1050)


class AnalyseTests(unittest.TestCase):
    def test_insured_adds_premium_to_mortgage(self):
        r = analyse(665_000, 66_500, 4.0, 25, insured=True, rules=RULES)
        self.assertAlmostEqual(r["premium"], 598_500 * 0.031)
        self.assertAlmostEqual(r["mortgage"], 598_500 + r["premium"])

    def test_under_20_percent_requires_insured(self):
        with self.assertRaises(ValueError):
            analyse(665_000, 66_500, 4.0, 25, rules=RULES)

    def test_below_minimum_down_payment(self):
        with self.assertRaises(ValueError):
            analyse(665_000, 20_000, 4.0, 25, insured=True, rules=RULES)

    def test_stress_payment_higher(self):
        r = analyse(700_000, 150_000, 4.0, 25, stress_rate=6.0, insured=True, rules=RULES)
        self.assertGreater(r["stress_payment"], r["monthly_payment"])

    def test_association_fee_added_monthly(self):
        r = analyse(665_000, 66_500, 4.0, 25, insured=True, rules=RULES, annual_fees=498.02)
        self.assertAlmostEqual(r["monthly_with_fees"], r["monthly_payment"] + 498.02 / 12)

    def test_down_payment_too_large(self):
        with self.assertRaises(ValueError):
            analyse(500_000, 500_000, 4.0, 25, rules=RULES)

    def test_income_ratio(self):
        r = analyse(500_000, 100_000, 5.0, 25, monthly_income=10_000, rules=RULES)
        self.assertAlmostEqual(r["payment_to_income_pct"], r["monthly_payment"] / 100, places=6)


if __name__ == "__main__":
    unittest.main()
