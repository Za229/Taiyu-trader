import ccxt
import pandas as pd
from app import config

def make_exchange():
    exchange_cls = getattr(ccxt, config.EXCHANGE_ID, None)
    if exchange_cls is None:
        raise ValueError(f"Unsupported CCXT exchange id: {config.EXCHANGE_ID}")
    return exchange_cls({"enableRateLimit": True, "timeout": 15000})

def fetch_candles(symbol: str, timeframe: str, limit: int | None = None) -> pd.DataFrame:
    exchange = make_exchange()
    rows = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit or config.CANDLE_LIMIT)
    if not rows:
        raise RuntimeError("Exchange returned no candles")
    df = pd.DataFrame(rows, columns=["timestamp", "open", "high", "low", "close", "volume"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms", utc=True)
    return df
