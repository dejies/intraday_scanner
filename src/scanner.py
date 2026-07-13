"""
Scanner Engine

Runs all enabled scanners and collects trading signals.
"""

from __future__ import annotations

from src.scanners.breakout import BreakoutScanner
from src.scanners.trend import TrendScanner
from src.scanners.volume import VolumeScanner
from src.services.market_data import MarketData
from src.core.market_data_store import MarketDataStore
from src.services.watchlist import WatchlistService


class Scanner:
    """
    Executes all enabled scanners.
    """

    def __init__(
        self,
        market_data: MarketData,
        market_store: MarketDataStore,
        watchlist: WatchlistService,
    ) -> None:

        self.market_data = market_data
        self.market_store = market_store
        self.watchlist = watchlist

        self.trend = TrendScanner()
        self.breakout = BreakoutScanner()
        self.volume = VolumeScanner()

    # ------------------------------------------------------------------

    def scan(self):
        """
        Run all scanners and return trading signals.
        """

        signals = []

        for symbol in self.market_data.get_symbols():

            candles = self.market_data.get_candles(symbol)

            if len(candles) < 2:
                continue

            instrument = self.watchlist.get_instrument(symbol)

            if instrument is None:
                continue

            indicators = self.market_store.get_indicator_data(
                instrument.security_id,
            )

            if indicators is None:
                continue

            #
            # Trend Scanner
            #
            trend_signals = self.trend.scan(
                symbol,
                candles,
                indicators,
            )

            for signal in trend_signals:
                signal.security_id = instrument.security_id

            signals.extend(trend_signals)

            #
            # Breakout Scanner
            #
            breakout_signals = self.breakout.scan(
                symbol,
                candles,
            )

            for signal in breakout_signals:
                signal.security_id = instrument.security_id

            signals.extend(breakout_signals)

            #
            # Volume Scanner
            #
            volume_signals = self.volume.scan(
                symbol,
                candles,
            )

            for signal in volume_signals:
                signal.security_id = instrument.security_id

            signals.extend(volume_signals)

        for signal in signals:
            self.market_store.update_signal(signal)

        return signals