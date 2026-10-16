# Taiyu-trader — Crypto Signal Dashboard

A starter crypto market dashboard using CoinDCX public candle API and an EMA 9/21 + RSI strategy.

> **Safety first:** the app runs in paper mode. It displays informational signals only and does not submit real orders. Crypto trading is risky; signals do not guarantee returns.

## Included
- FastAPI API and dashboard
- Public OHLCV market data from a CCXT-supported exchange
- EMA 9/21 and RSI-based BUY / SELL / WAIT signals
- Illustrative stop-loss/take-profit levels
- Dockerfile and GitHub Actions checks
- Paper-mode environment template and cloud deployment notes

## Run locally
1. Install Python 3.11 or newer.
2. `python -m venv .venv` and activate it.
3. `pip install -r requirements.txt`
4. Copy `.env.example` to `.env` and review settings.
5. Run `uvicorn app.main:app --host 0.0.0.0 --port 8000`
6. Visit `http://127.0.0.1:8000`

## API endpoints
- `GET /api/health`
- `GET /api/market?symbol=BTC/USDT&timeframe=5m`
- `GET /api/signal?symbol=BTC/USDT&timeframe=5m`
- `POST /api/trading/start` (deliberately refuses actual order execution)

## Exchange
Public candles are fetched from CoinDCX's documented REST endpoint. The dashboard currently supports `BTC/USDT`, `ETH/USDT`, `SOL/USDT`, and `BNB/USDT` selections; confirm each pair is available on CoinDCX. CoinDCX candle intervals supported by the app are `1m`, `15m`, `1h`, and `1d`.

## Live execution status
**Not implemented.** The trading-start endpoint intentionally returns an error instead of placing orders. Before any exchange execution is added, implement and test exchange-specific sandbox support, order idempotency, partial-fill/reconciliation handling, position sizing, daily loss limits, and an emergency stop.

Never commit API keys. If exchange keys are added in the future, keep them in the host's secret environment settings, disable withdrawals, and grant only the minimum permissions needed.

## Deploy
See [CLOUD_DEPLOY.md](CLOUD_DEPLOY.md). This project includes a Dockerfile; a cloud provider account and deployment configuration are still required.

## Tests
`python -m compileall -q app tests`
`python -m unittest discover -s tests -v`
