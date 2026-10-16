# Cloud deployment (safe starter)

This service can be deployed as a Docker web service on a cloud host that supports Docker (for example, Render, Railway, Fly.io, or a VPS). Provider settings change over time; use the provider's current Docker deployment instructions.

## Suggested steps
1. Upload this project to the GitHub repository.
2. Create a Docker web service from the repository. Use the included `Dockerfile`; the app listens on port `8000`. Configure the host to expose that port or inject its expected `PORT` as needed.
3. Set environment variables from `.env.example` in the cloud provider dashboard. Keep `TRADING_MODE=paper`, `ENABLE_LIVE_TRADING=false`, and leave `LIVE_TRADING_ACK` blank.
4. Open `/api/health` and `/` to verify service health and dashboard. Check logs for market-data connectivity.
5. Run sandbox/testnet trials and review orders, duplicate-order protection, retries, precision/minimum order sizes, rate limits, partial fills, and kill-switch behavior before implementing any real order execution.

## Important deployment note
The current starter intentionally does **not** implement actual order placement. The `/api/trading/start` endpoint refuses to run live orders, even if the configuration gate is satisfied. Cloud deployment does not make it a live trading bot by itself.

## Secrets
Use the cloud provider's encrypted environment-variable/secret settings. Use exchange API keys with withdrawals disabled and only the minimum required trading permissions. Never put keys in browser JavaScript, source code, logs, GitHub commits, or screenshots.
