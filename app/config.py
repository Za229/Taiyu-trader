import os
from dotenv import load_dotenv

load_dotenv()

EXCHANGE_ID = os.getenv("EXCHANGE_ID", "coindcx").lower()
DEFAULT_SYMBOL = os.getenv("DEFAULT_SYMBOL", "BTC/USDT")
DEFAULT_TIMEFRAME = os.getenv("DEFAULT_TIMEFRAME", "1m")
CANDLE_LIMIT = min(max(int(os.getenv("CANDLE_LIMIT", "100")), 25), 1000)
TRADING_MODE = os.getenv("TRADING_MODE", "paper").lower()
ENABLE_LIVE_TRADING = os.getenv("ENABLE_LIVE_TRADING", "false").lower() == "true"
LIVE_TRADING_ACK = os.getenv("LIVE_TRADING_ACK", "")
API_KEY = os.getenv("API_KEY", "")
API_SECRET = os.getenv("API_SECRET", "")
API_PASSWORD = os.getenv("API_PASSWORD", "")

def live_trading_gate_status() -> dict:
    checks = {
        "mode_is_live": TRADING_MODE == "live",
        "live_flag_enabled": ENABLE_LIVE_TRADING,
        "explicit_ack": LIVE_TRADING_ACK == "I_UNDERSTAND_REAL_MONEY_RISK",
        "api_credentials_present": bool(API_KEY and API_SECRET),
    }
    return {"enabled": all(checks.values()), "checks": checks}
