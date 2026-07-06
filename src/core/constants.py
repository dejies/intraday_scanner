"""
Application constants.

This module contains all application-wide constants and enumerations.
Configuration values that may change between environments should go in
config.py/.env, while fixed application constants belong here.
"""

from enum import StrEnum


# =============================================================================
# Application
# =============================================================================

APP_NAME = "Intraday Stock Market Scanner"
APP_VERSION = "1.0.0"


# =============================================================================
# Exchanges
# =============================================================================

class Exchange(StrEnum):
    NSE = "NSE"
    BSE = "BSE"


# =============================================================================
# Timeframes
# =============================================================================

class TimeFrame(StrEnum):
    ONE_MINUTE = "1m"
    FIVE_MINUTES = "5m"
    FIFTEEN_MINUTES = "15m"
    THIRTY_MINUTES = "30m"
    ONE_HOUR = "1h"
    ONE_DAY = "1d"


# =============================================================================
# Signal Types
# =============================================================================

class SignalType(StrEnum):
    BUY = "BUY"
    SELL = "SELL"
    HOLD = "HOLD"
    NONE = "NONE"


# =============================================================================
# Scanner Strategies
# =============================================================================

class Strategy(StrEnum):
    TREND = "TREND"
    BREAKOUT = "BREAKOUT"
    VOLUME = "VOLUME"
    VWAP = "VWAP"
    REVERSAL = "REVERSAL"


# =============================================================================
# Trend Direction
# =============================================================================

class Trend(StrEnum):
    BULLISH = "BULLISH"
    BEARISH = "BEARISH"
    SIDEWAYS = "SIDEWAYS"


# =============================================================================
# Scanner Status
# =============================================================================

class ScannerStatus(StrEnum):
    READY = "READY"
    RUNNING = "RUNNING"
    STOPPED = "STOPPED"
    ERROR = "ERROR"


# =============================================================================
# Logging
# =============================================================================

DEFAULT_LOG_FILE = "scanner.log"


# =============================================================================
# Market Timing (Indian Market)
# =============================================================================

MARKET_OPEN = "09:15"
MARKET_CLOSE = "15:30"


# =============================================================================
# Defaults
# =============================================================================

DEFAULT_WATCHLIST = "data/watchlist.csv"

DEFAULT_SCAN_INTERVAL = 60

DEFAULT_MAX_CANDLES = 200


# =============================================================================
# Technical Indicators
# =============================================================================

DEFAULT_EMA_SHORT = 20
DEFAULT_EMA_LONG = 50

DEFAULT_RSI_PERIOD = 14

DEFAULT_MACD_FAST = 12
DEFAULT_MACD_SLOW = 26
DEFAULT_MACD_SIGNAL = 9


# =============================================================================
# Dashboard
# =============================================================================

MAX_DASHBOARD_SIGNALS = 50


# =============================================================================
# Telegram
# =============================================================================

TELEGRAM_TIMEOUT = 10


# =============================================================================
# WebSocket
# =============================================================================

WEBSOCKET_RECONNECT_DELAY = 5

MAX_RECONNECT_ATTEMPTS = 10