"""
Scanner Engine

Runs all enabled scanners and collects trading signals.
"""

from __future__ import annotations

from src.services.market_data import MarketData

from src.scanners.trend import TrendScanner
from src.scanners.breakout import BreakoutScanner
from src.scanners.volume import VolumeScanner
from src.scanners.reversal import ReversalScanner
from src.scanners.vwap import VWAPScanner


class Scanner:

    def __init__(self):

        self.market_data = MarketData()

        self.trend = TrendScanner()

        self.breakout = BreakoutScanner()

        self.volume = VolumeScanner()

        self.reversal = ReversalScanner()

        self.vwap = VWAPScanner()

    def scan(self):

        signals = []

        for symbol in self.market_data.get_symbols():

            candles = self.market_data.get_candles(symbol)

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

            signals.extend(
                self.reversal.scan(symbol, candles)
            )

            signals.extend(
                self.vwap.scan(symbol, candles)
            )

        return signals