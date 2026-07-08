"""
Application configuration.

Loads configuration from the .env file and exposes a single immutable
Settings object for the entire application.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

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

    dhan_base_url: str
    dhan_market_feed_url: str
    dhan_instrument_master_url: str

    api_timeout: int
    retry_count: int
    retry_delay: float

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

    instrument_master_file: Path

    # -------------------------------------------------------------------------
    # Indicators
    # -------------------------------------------------------------------------

    ema_short: int
    ema_long: int

    rsi_period: int

    macd_fast: int
    macd_slow: int
    macd_signal: int


# -----------------------------------------------------------------------------
# Loader
# -----------------------------------------------------------------------------


def load_settings() -> Settings:
    """
    Load application settings from .env.
    """

    watchlist_file = Path(
        os.getenv(
            "WATCHLIST_FILE",
            DATA_DIR / "watchlist.csv",
        )
    )

    instrument_master_file = Path(
        os.getenv(
            "INSTRUMENT_MASTER_FILE",
            DATA_DIR / "dhan_instruments.csv",
        )
    )

    return Settings(

        # ---------------------------------------------------------------------
        # Dhan
        # ---------------------------------------------------------------------

        dhan_client_id=os.getenv(
            "DHAN_CLIENT_ID",
            "",
        ).strip(),

        dhan_access_token=os.getenv(
            "DHAN_ACCESS_TOKEN",
            "",
        ).strip(),

        dhan_base_url=os.getenv(
            "DHAN_BASE_URL",
            "https://api.dhan.co",
        ).strip(),

        dhan_market_feed_url=os.getenv(
            "DHAN_MARKET_FEED_URL",
            "wss://api-feed.dhan.co",
        ).strip(),

        dhan_instrument_master_url=os.getenv(
            "DHAN_INSTRUMENT_MASTER_URL",
            "https://images.dhan.co/api-data/api-scrip-master.csv",
        ).strip(),

        api_timeout=max(
            5,
            int(
                os.getenv(
                    "API_TIMEOUT",
                    "30",
                )
            ),
        ),

        retry_count=max(
            0,
            int(
                os.getenv(
                    "RETRY_COUNT",
                    "3",
                )
            ),
        ),

        retry_delay=max(
            0.1,
            float(
                os.getenv(
                    "RETRY_DELAY",
                    "0.5",
                )
            ),
        ),

        # ---------------------------------------------------------------------
        # Telegram
        # ---------------------------------------------------------------------

        telegram_bot_token=os.getenv(
            "TELEGRAM_BOT_TOKEN",
            "",
        ).strip(),

        telegram_chat_id=os.getenv(
            "TELEGRAM_CHAT_ID",
            "",
        ).strip(),

        # ---------------------------------------------------------------------
        # Logging
        # ---------------------------------------------------------------------

        log_level=os.getenv(
            "LOG_LEVEL",
            "INFO",
        ).upper(),

        # ---------------------------------------------------------------------
        # Scanner
        # ---------------------------------------------------------------------

        scan_interval=max(
            1,
            int(
                os.getenv(
                    "SCAN_INTERVAL",
                    "1",
                )
            ),
        ),

        max_candles=max(
            50,
            int(
                os.getenv(
                    "MAX_CANDLES",
                    "200",
                )
            ),
        ),

        # ---------------------------------------------------------------------
        # Files
        # ---------------------------------------------------------------------

        watchlist_file=watchlist_file,

        instrument_master_file=instrument_master_file,

        # ---------------------------------------------------------------------
        # Indicators
        # ---------------------------------------------------------------------

        ema_short=max(
            1,
            int(
                os.getenv(
                    "EMA_SHORT",
                    "20",
                )
            ),
        ),

        ema_long=max(
            2,
            int(
                os.getenv(
                    "EMA_LONG",
                    "50",
                )
            ),
        ),

        rsi_period=max(
            2,
            int(
                os.getenv(
                    "RSI_PERIOD",
                    "14",
                )
            ),
        ),

        macd_fast=max(
            1,
            int(
                os.getenv(
                    "MACD_FAST",
                    "12",
                )
            ),
        ),

        macd_slow=max(
            2,
            int(
                os.getenv(
                    "MACD_SLOW",
                    "26",
                )
            ),
        ),

        macd_signal=max(
            1,
            int(
                os.getenv(
                    "MACD_SIGNAL",
                    "9",
                )
            ),
        ),
    )


settings = load_settings()