import pandas as pd

def build_signal(candles: pd.DataFrame) -> dict:
    if len(candles) < 25:
        return {"signal": "WAIT", "reason": "Need at least 25 candles", "entry": None, "stop_loss": None, "take_profit": None}
    df = candles.copy()
    df["ema_fast"] = df["close"].ewm(span=9, adjust=False).mean()
    df["ema_slow"] = df["close"].ewm(span=21, adjust=False).mean()
    delta = df["close"].diff()
    gain = delta.clip(lower=0).ewm(alpha=1/14, adjust=False).mean()
    loss = (-delta.clip(upper=0)).ewm(alpha=1/14, adjust=False).mean()
    rs = gain / loss.replace(0, float("nan"))
    df["rsi"] = 100 - (100 / (1 + rs))
    last, prev = df.iloc[-1], df.iloc[-2]
    price = float(last["close"])
    rsi = float(last["rsi"]) if pd.notna(last["rsi"]) else 50.0
    crossed_up = prev["ema_fast"] <= prev["ema_slow"] and last["ema_fast"] > last["ema_slow"]
    crossed_down = prev["ema_fast"] >= prev["ema_slow"] and last["ema_fast"] < last["ema_slow"]
    signal, reason = "WAIT", "No EMA crossover; wait for confirmation"
    if crossed_up and 45 <= rsi <= 68:
        signal, reason = "BUY", "EMA 9 crossed above EMA 21 and RSI is not overbought"
    elif crossed_down and 32 <= rsi <= 55:
        signal, reason = "SELL", "EMA 9 crossed below EMA 21 and RSI is not deeply oversold"
    stop = price * 0.99 if signal == "BUY" else price * 1.01 if signal == "SELL" else None
    target = price * 1.02 if signal == "BUY" else price * 0.98 if signal == "SELL" else None
    return {
        "signal": signal, "reason": reason, "entry": round(price, 8),
        "stop_loss": round(stop, 8) if stop else None,
        "take_profit": round(target, 8) if target else None,
        "ema_fast": round(float(last["ema_fast"]), 8),
        "ema_slow": round(float(last["ema_slow"]), 8),
        "rsi": round(rsi, 2), "candle_time": last["timestamp"].isoformat(),
    }
