from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from app import config
from app.market import fetch_candles
from app.strategy import build_signal

app = FastAPI(title="Taiyu-trader", version="0.2.0")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/", response_class=HTMLResponse)
def home():
    with open("app/static/index.html", encoding="utf-8") as f:
        return f.read()

@app.get("/api/health")
def health():
    return {"status": "ok", "exchange": "CoinDCX",
            "trading_mode": config.TRADING_MODE,
            "live_trading": config.live_trading_gate_status()}

@app.get("/api/market")
def market(symbol: str = Query(default=config.DEFAULT_SYMBOL, min_length=3, max_length=30),
           timeframe: str = Query(default=config.DEFAULT_TIMEFRAME, min_length=2, max_length=5)):
    try:
        df = fetch_candles(symbol, timeframe)
        return {"symbol": symbol.upper(), "timeframe": timeframe,
                "candles": [{"time": r.timestamp.isoformat(), "open": float(r.open),
                             "high": float(r.high), "low": float(r.low),
                             "close": float(r.close), "volume": float(r.volume)}
                            for r in df.tail(60).itertuples(index=False)],
                "last_price": float(df.iloc[-1]["close"])}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"CoinDCX market data unavailable: {type(e).__name__}: {e}")

@app.get("/api/signal")
def signal(symbol: str = Query(default=config.DEFAULT_SYMBOL, min_length=3, max_length=30),
           timeframe: str = Query(default=config.DEFAULT_TIMEFRAME, min_length=2, max_length=5)):
    try:
        df = fetch_candles(symbol, timeframe)
        return {"symbol": symbol.upper(), "timeframe": timeframe, **build_signal(df),
                "mode": config.TRADING_MODE, "orders_enabled": False,
                "note": "Informational signal only; automatic order execution is not implemented."}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"CoinDCX signal calculation failed: {type(e).__name__}: {e}")

@app.post("/api/trading/start")
def start_trading():
    raise HTTPException(status_code=403, detail="Trading is paper-only. Real order execution is not implemented; this endpoint cannot place orders.")
