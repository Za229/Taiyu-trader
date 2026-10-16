import unittest
import pandas as pd
from app.strategy import build_signal

class StrategyTests(unittest.TestCase):
    def test_insufficient_candles_returns_wait(self):
        candles = pd.DataFrame({"close": [100.0] * 10, "timestamp": pd.date_range("2025-01-01", periods=10, tz="UTC")})
        result = build_signal(candles)
        self.assertEqual(result["signal"], "WAIT")
        self.assertIsNone(result["entry"])

    def test_flat_market_does_not_claim_buy_or_sell(self):
        candles = pd.DataFrame({"close": [100.0] * 40, "timestamp": pd.date_range("2025-01-01", periods=40, tz="UTC")})
        result = build_signal(candles)
        self.assertEqual(result["signal"], "WAIT")
        self.assertIn("reason", result)

if __name__ == "__main__":
    unittest.main()
