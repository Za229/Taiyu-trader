from __future__ import annotations

import re
import requests
import pandas as pd
from app import config

COINDCX_CANDLES_URL = "https://api.coindcx.com/market_data/candles"
COINDCX_TICKER_URL = "https://api.coindcx.com/exchange/ticker"
COINDCX_MARKETS_URL = "https://api.coindcx.com/exchange/v1/markets"
SESSION = requests.Session()
SESSION.headers.update({"User-Agent": "Taiyu-trader/0.1 (public market data)"})

SUPPORTED_INTERVALS = {"1m", "15m", "1h", "1d"}
SYMBOL_RE = re.compile(r"^[A-Z0-9]{2,20}/(INR|USDT|BTC|ETH)$")

def validate_symbol(symbol: str) -> str:
    symbol = symbol.strip().upper()
    if not SYMBOL_RE.fullmatch(symbol):
        raise ValueError("Unsupported symbol format. Use a pair such as BTC/USDT or BTC/INR.")
    return symbol

def symbol_to_pair(symbol: str) -> str:
    """Convert dashboard symbols to CoinDCX's documented candle pair format."""
    symbol = validate_symbol(symbol)
    base, quote = symbol.split("/")
    source = "I" if quote == "INR" else "B"
    return f"{source}-{base}_{quote}"

def fetch_candles(symbol: str, timeframe: str, limit: int | None = None) -> pd.DataFrame:
    symbol = validate_symbol(symbol)
    if timeframe not in SUPPORTED_INTERVALS:
        raise ValueError(f"Unsupported CoinDCX candle interval. Use one of: {', '.join(sorted(SUPPORTED_INTERVALS))}")
    requested_limit = min(max(int(limit or config.CANDLE_LIMIT), 25), 1000)
    response = SESSION.get(
        COINDCX_CANDLES_URL,
        params={"pair": symbol_to_pair(symbol), "interval": timeframe, "limit": requested_limit},
        timeout=15,
    )
    response.raise_for_status()
    rows = response.json()
    if not isinstance(rows, list) or not rows:
        raise RuntimeError(f"CoinDCX returned no candles for {symbol} ({symbol_to_pair(symbol)})")
    df = pd.DataFrame(rows)
    required = {"time", "open", "high", "low", "close", "volume"}
    if not required.issubset(df.columns):
        raise RuntimeError("Unexpected CoinDCX candle response format")
    df = df.rename(columns={"time": "timestamp"})
    df["timestamp"] = pd.to_datetime(pd.to_numeric(df["timestamp"]), unit="ms", utc=True)
    for column in ["open", "high", "low", "close", "volume"]:
        df[column] = pd.to_numeric(df[column], errors="raise")
    # CoinDCX documents candle responses in descending time order; strategy needs ascending order.
    return df.sort_values("timestamp").drop_duplicates("timestamp").reset_index(drop=True)

def fetch_ticker(symbol: str) -> dict:
    symbol = validate_symbol(symbol)
    response = SESSION.get(COINDCX_TICKER_URL, timeout=15)
    response.raise_for_status()
    pair_name = symbol.replace("/", "")
    for ticker in response.json():
        if str(ticker.get("market", "")).upper() == pair_name:
            return ticker
    return {}
