"""
Application configuration.

Loads configuration from the .env file and exposes a single immutable
Settings object for the entire application.
"""

from dataclasses import dataclass
from pathlib import Path
import os

from dotenv import load_dotenv

# -----------------------------------------------------------------------------
# Project Paths
# -----------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

ENV_FILE = PROJECT_ROOT / ".env"

DATA_DIR = PROJECT_ROOT / "data"

LOG_DIR = PROJECT_ROOT / "logs"

load_dotenv(ENV_FILE)


# -----------------------------------------------------------------------------
# Settings
# -----------------------------------------------------------------------------

@dataclass(frozen=True, slots=True)
class Settings:
    """Application settings."""

    # -------------------------------------------------------------------------
    # Dhan
    # -------------------------------------------------------------------------

    dhan_client_id: str
    dhan_access_token: str

    # -------------------------------------------------------------------------
    # Telegram
    # -------------------------------------------------------------------------

    telegram_bot_token: str
    telegram_chat_id: str

    # -------------------------------------------------------------------------
    # Logging
    # -------------------------------------------------------------------------

    log_level: str

    # -------------------------------------------------------------------------
    # Scanner
    # -------------------------------------------------------------------------

    scan_interval: int
    max_candles: int

    # -------------------------------------------------------------------------
    # Files
    # -------------------------------------------------------------------------

    watchlist_file: Path

    # -------------------------------------------------------------------------
    # Indicators
    # -------------------------------------------------------------------------

    ema_short: int
    ema_long: int

    rsi_period: int

    macd_fast: int
    macd_slow: int
    macd_signal: int


def load_settings() -> Settings:
    """Load application settings from environment variables."""

    watchlist_file = Path(
        os.getenv(
            "WATCHLIST_FILE",
            DATA_DIR / "watchlist.csv"
        )
    )

    return Settings(

        # Dhan
        dhan_client_id=os.getenv("DHAN_CLIENT_ID", "").strip(),
        dhan_access_token=os.getenv("DHAN_ACCESS_TOKEN", "").strip(),

        # Telegram
        telegram_bot_token=os.getenv("TELEGRAM_BOT_TOKEN", "").strip(),
        telegram_chat_id=os.getenv("TELEGRAM_CHAT_ID", "").strip(),

        # Logging
        log_level=os.getenv("LOG_LEVEL", "INFO").upper(),

        # Scanner
        scan_interval=max(
            1,
            int(os.getenv("SCAN_INTERVAL", "60"))
        ),

        max_candles=max(
            50,
            int(os.getenv("MAX_CANDLES", "200"))
        ),

        # Files
        watchlist_file=watchlist_file,

        # Indicators
        ema_short=int(os.getenv("EMA_SHORT", "20")),
        ema_long=int(os.getenv("EMA_LONG", "50")),

        rsi_period=int(os.getenv("RSI_PERIOD", "14")),

        macd_fast=int(os.getenv("MACD_FAST", "12")),
        macd_slow=int(os.getenv("MACD_SLOW", "26")),
        macd_signal=int(os.getenv("MACD_SIGNAL", "9")),
    )


settings = load_settings()