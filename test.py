"""
Foundation test for Intraday Scanner V1.

This script verifies:

1. Configuration
2. Logger
3. Constants
4. Stock Model
5. Candle Model
6. Signal Model
7. Watchlist Service
8. MarketData Service
"""

from datetime import datetime

from src.core.config import settings
from src.core.logger import get_logger
from src.core.constants import (
    APP_NAME,
    APP_VERSION,
    Exchange,
    SignalType,
    Strategy,
)
from src.models.stock import Stock
from src.models.candle import Candle
from src.models.signal import Signal
from src.services.watchlist import WatchlistService
from src.services.market_data import MarketData


logger = get_logger("FoundationTest")


def separator(title: str) -> None:
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


def test_config() -> None:
    separator("CONFIG")

    print(settings)

    assert settings.max_candles > 0
    assert settings.scan_interval > 0

    print("✅ Configuration OK")


def test_constants() -> None:
    separator("CONSTANTS")

    print(APP_NAME)
    print(APP_VERSION)

    print(Exchange.NSE)
    print(SignalType.BUY)
    print(Strategy.TREND)

    print("✅ Constants OK")


def test_models() -> None:
    separator("MODELS")

    stock = Stock(
        security_id=2885,
        symbol="RELIANCE",
        exchange=Exchange.NSE,
        name="Reliance Industries",
    )

    candle = Candle(
        timestamp=datetime.now(),
        open=100,
        high=105,
        low=99,
        close=104,
        volume=100000,
    )

    signal = Signal(
        symbol="RELIANCE",
        strategy="TREND",
        signal="BUY",
        price=104,
        confidence=92,
        timestamp=datetime.now(),
        message="EMA20 crossed EMA50",
    )

    print(stock)
    print(candle)
    print(signal)

    print("✅ Models OK")


def test_watchlist() -> None:
    separator("WATCHLIST")

    watchlist = WatchlistService()

    stocks = watchlist.load()

    assert watchlist.count() > 0

    print(f"Loaded Stocks : {watchlist.count()}")

    print()

    for stock in stocks:
        print(stock)

    print()

    print("Symbols")

    print(watchlist.get_symbols())

    print()

    print("Security IDs")

    print(watchlist.get_security_ids())

    print("✅ Watchlist OK")


def test_market_data() -> None:
    separator("MARKET DATA")

    market = MarketData()

    candle1 = Candle(
        timestamp=datetime.now(),
        open=100,
        high=102,
        low=99,
        close=101,
        volume=1000,
    )

    candle2 = Candle(
        timestamp=datetime.now(),
        open=101,
        high=104,
        low=100,
        close=103,
        volume=1500,
    )

    market.add_candle("RELIANCE", candle1)
    market.add_candle("RELIANCE", candle2)

    assert market.symbol_count() == 1
    assert market.get_candle_count("RELIANCE") == 2

    print("Symbols :", market.get_symbols())

    print("Latest :", market.get_latest_candle("RELIANCE"))

    print("Previous :", market.get_previous_candle("RELIANCE"))

    print("All Candles")

    for candle in market.get_candles("RELIANCE"):
        print(candle)

    print("✅ MarketData OK")


def test_logger() -> None:
    separator("LOGGER")

    logger.info("Logger test")
    logger.warning("Warning test")
    logger.error("Error test")

    print("Check logs/scanner.log")

    print("✅ Logger OK")


def main() -> None:
    logger.info("Starting foundation tests...")

    test_config()

    test_constants()

    test_models()

    test_watchlist()

    test_market_data()

    test_logger()

    separator("RESULT")

    print("🎉 ALL FOUNDATION TESTS PASSED")

    logger.info("Foundation tests completed successfully.")


if __name__ == "__main__":
    main()