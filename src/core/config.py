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
    # Historical Data
    # -------------------------------------------------------------------------

    historical_lookback_days: int

    historical_interval: int

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

    # -------------------------------------------------------------------------
    # Confidence Scoring
    # -------------------------------------------------------------------------

    confidence_ema_weight: int
    confidence_vwap_weight: int
    confidence_rsi_weight: int
    confidence_rvol_weight: int
    confidence_ema_gap_weight: int

    # RSI

    rsi_buy_strong: int
    rsi_buy_medium: int
    rsi_buy_weak: int
    rsi_buy_min: int

    rsi_sell_strong: int
    rsi_sell_medium: int
    rsi_sell_weak: int
    rsi_sell_max: int

    # RVOL

    rvol_high: float
    rvol_medium: float
    rvol_normal: float
    rvol_low: float

    # EMA Gap

    ema_gap_strong: float
    ema_gap_medium: float
    ema_gap_normal: float
    ema_gap_weak: float
    ema_gap_min: float

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
            DATA_DIR / "dhan_instruments1.csv",
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
        # ---------------------------------------------------------------------
        # Confidence Scoring
        # ---------------------------------------------------------------------

        confidence_ema_weight=int(
            os.getenv(
                "CONFIDENCE_EMA_WEIGHT",
                "30",
            )
        ),

        confidence_vwap_weight=int(
            os.getenv(
                "CONFIDENCE_VWAP_WEIGHT",
                "20",
            )
        ),

        confidence_rsi_weight=int(
            os.getenv(
                "CONFIDENCE_RSI_WEIGHT",
                "20",
            )
        ),

        confidence_rvol_weight=int(
            os.getenv(
                "CONFIDENCE_RVOL_WEIGHT",
                "15",
            )
        ),

        confidence_ema_gap_weight=int(
            os.getenv(
                "CONFIDENCE_EMA_GAP_WEIGHT",
                "15",
            )
        ),

        #
        # RSI
        #

        rsi_buy_strong=int(os.getenv("RSI_BUY_STRONG", "65")),
        rsi_buy_medium=int(os.getenv("RSI_BUY_MEDIUM", "55")),
        rsi_buy_weak=int(os.getenv("RSI_BUY_WEAK", "50")),
        rsi_buy_min=int(os.getenv("RSI_BUY_MIN", "45")),

        rsi_sell_strong=int(os.getenv("RSI_SELL_STRONG", "35")),
        rsi_sell_medium=int(os.getenv("RSI_SELL_MEDIUM", "45")),
        rsi_sell_weak=int(os.getenv("RSI_SELL_WEAK", "50")),
        rsi_sell_max=int(os.getenv("RSI_SELL_MAX", "55")),

        #
        # RVOL
        #

        rvol_high=float(os.getenv("RVOL_HIGH", "2.0")),
        rvol_medium=float(os.getenv("RVOL_MEDIUM", "1.5")),
        rvol_normal=float(os.getenv("RVOL_NORMAL", "1.0")),
        rvol_low=float(os.getenv("RVOL_LOW", "0.7")),

        #
        # EMA Gap
        #

        ema_gap_strong=float(os.getenv("EMA_GAP_STRONG", "1.0")),
        ema_gap_medium=float(os.getenv("EMA_GAP_MEDIUM", "0.7")),
        ema_gap_normal=float(os.getenv("EMA_GAP_NORMAL", "0.5")),
        ema_gap_weak=float(os.getenv("EMA_GAP_WEAK", "0.3")),
        ema_gap_min=float(os.getenv("EMA_GAP_MIN", "0.1")),
        # ---------------------------------------------------------------------
        # Historical Data
        # ---------------------------------------------------------------------

        historical_lookback_days=max(
            1,
            int(
                os.getenv(
                    "HISTORICAL_LOOKBACK_DAYS",
                    "5",
                )
            ),
        ),

        historical_interval=max(
            1,
            int(
                os.getenv(
                    "HISTORICAL_INTERVAL",
                    "1",
                )
            ),
        ),
    )


settings = load_settings()