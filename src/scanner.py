"""
Scanner Engine

Runs all enabled scanners and collects trading signals.
"""

from __future__ import annotations

from src.services.market_data import MarketData

from src.scanners.trend import TrendScanner
from src.scanners.breakout import BreakoutScanner
from src.scanners.volume import VolumeScanner


class Scanner:
    """
    Executes all enabled scanners against the shared MarketData.
    """

    def __init__(
        self,
        market_data: MarketData,
    ) -> None:

        #
        # Shared MarketData instance.
        #
        self.market_data = market_data

        #
        # Scanners
        #
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

            #
            # Need sufficient candle history.
            #
            if len(candles) < 50:
                continue

            signals.extend(
                self.trend.scan(symbol, candles)
            )

            signals.extend(
                self.breakout.scan(symbol, candles)
            )

            signals.extend(
                self.volume.scan(symbol, candles)
            )

        return signals