"""
Scanner Engine

Runs all enabled scanners and collects trading signals.
"""

from __future__ import annotations

from src.indicators import IndicatorEngine
from src.models.indicator import IndicatorData
from src.scanners.breakout import BreakoutScanner
from src.scanners.trend import TrendScanner
from src.scanners.volume import VolumeScanner
from src.services.market_data import MarketData
from src.core.market_data_store import MarketDataStore
from src.services.watchlist import WatchlistService

class Scanner:
    """
    Executes all enabled scanners against the shared MarketData.
    """

    def __init__(
            self,
            market_data: MarketData,
            market_store: MarketDataStore,
            watchlist: WatchlistService,
    ) -> None:

        #
        # Shared MarketData instance.
        #
        self.market_data = market_data
        self.market_store = market_store
        self.watchlist = watchlist
        #
        # Scanners.
        #
        self.trend = TrendScanner()

        self.breakout = BreakoutScanner()

        self.volume = VolumeScanner()

        #
        # Shared Indicator Engine.
        #
        self.indicator_engine = IndicatorEngine()

        #
        # Latest calculated indicators.
        #
        self.latest_indicators: dict[
            str,
            IndicatorData,
        ] = {}

    # ------------------------------------------------------------------

    def scan(self):
        """
        Run all scanners and return trading signals.
        """

        #
        # Clear previous scan cache.
        #
        self.latest_indicators.clear()

        signals = []

        for symbol in self.market_data.get_symbols():

            candles = self.market_data.get_candles(symbol)

            #
            # Need sufficient candle history.
            #
            if len(candles) < 2:
                continue

            #
            # Calculate indicators once.
            #
            indicators = self.indicator_engine.calculate(
                symbol,
                candles,
            )
            #
            # Cache indicators for dashboard.
            #
            self.latest_indicators[symbol] = indicators
            #
            # Trend Scanner.
            #
            trend_signals = self.trend.scan(
                symbol,
                candles,
                indicators,
            )

            instrument = self.watchlist.get_instrument(symbol)

            if instrument is not None:
                for signal in trend_signals:
                    signal.security_id = instrument.security_id

            signals.extend(trend_signals)

            #
            # Breakout Scanner.
            #
            trend_signals = self.trend.scan(
                symbol,
                candles,
                indicators,
            )

            instrument = self.watchlist.get_instrument(symbol)

            if instrument is not None:
                for signal in trend_signals:
                    signal.security_id = instrument.security_id

            signals.extend(trend_signals)

            #
            # Volume Scanner.
            #
            volume_signals = self.volume.scan(
                symbol,
                candles,
            )

            if instrument is not None:
                for signal in volume_signals:
                    signal.security_id = instrument.security_id

            signals.extend(volume_signals)

        #
        # Update runtime signal store.
        #
        for signal in signals:
            self.market_store.update_signal(signal)

        return signals

    # ------------------------------------------------------------------

    def get_latest_indicators(
            self,
    ) -> dict[str, IndicatorData]:
        """
        Return the latest calculated indicators.
        """

        return self.latest_indicators