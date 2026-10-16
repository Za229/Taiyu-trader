import unittest

from app.market import SUPPORTED_INTERVALS, symbol_to_pair, validate_symbol


class CoinDCXMarketTests(unittest.TestCase):
    def test_usdt_pair_format(self):
        self.assertEqual(symbol_to_pair("BTC/USDT"), "B-BTC_USDT")

    def test_inr_pair_format(self):
        self.assertEqual(symbol_to_pair("BTC/INR"), "I-BTC_INR")

    def test_symbol_is_normalized(self):
        self.assertEqual(validate_symbol("btc/usdt"), "BTC/USDT")

    def test_rejects_bad_symbol(self):
        with self.assertRaises(ValueError):
            symbol_to_pair("BTCUSDT")

    def test_only_documented_intervals_are_enabled(self):
        self.assertEqual(SUPPORTED_INTERVALS, {"1m", "15m", "1h", "1d"})


if __name__ == "__main__":
    unittest.main()
