import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
from affordability import analyse, monthly_payment


class AffordabilityTests(unittest.TestCase):
    def test_known_payment(self):
        # 300,000 at 6% over 30 years is a standard textbook case: ~1,798.65
        self.assertAlmostEqual(monthly_payment(300_000, 6, 30), 1798.65, places=2)

    def test_zero_rate(self):
        self.assertAlmostEqual(monthly_payment(120_000, 0, 10), 1000.0)

    def test_stress_payment_higher(self):
        r = analyse(700_000, 100_000, 4.0, 25, stress_rate=6.0)
        self.assertGreater(r["stress_payment"], r["monthly_payment"])

    def test_down_payment_too_large(self):
        with self.assertRaises(ValueError):
            analyse(500_000, 500_000, 4.0, 25)

    def test_income_ratio(self):
        r = analyse(500_000, 100_000, 5.0, 25, monthly_income=10_000)
        self.assertAlmostEqual(r["payment_to_income_pct"], r["monthly_payment"] / 100, places=6)


if __name__ == "__main__":
    unittest.main()
