"""
Reusable filters shared by trading strategies.
"""

from __future__ import annotations

from src.core.market_data_store import StockState


class StrategyFilters:

    #
    # Default thresholds
    #
    MIN_ADX = 20.0

    # ---------------------------------------------------------

    @staticmethod
    def has_indicator_data(
        stock: StockState,
    ) -> bool:

        indicator = stock.indicator
        tick = stock.tick

        return (
            indicator is not None
            and tick is not None
        )

    # ---------------------------------------------------------

    @classmethod
    def adx_bullish(
        cls,
        stock: StockState,
    ) -> bool:

        indicator = stock.indicator

        return (
            indicator.adx14 is not None
            and indicator.adx14 >= cls.MIN_ADX
        )

    # ---------------------------------------------------------

    @classmethod
    def adx_bearish(
        cls,
        stock: StockState,
    ) -> bool:

        indicator = stock.indicator

        return (
            indicator.adx14 is not None
            and indicator.adx14 >= cls.MIN_ADX
        )

    # ---------------------------------------------------------

    @staticmethod
    def above_vwap(
        stock: StockState,
    ) -> bool:

        indicator = stock.indicator
        tick = stock.tick

        return (
            indicator.vwap is not None
            and tick.ltp > indicator.vwap
        )

    # ---------------------------------------------------------

    @staticmethod
    def below_vwap(
        stock: StockState,
    ) -> bool:

        indicator = stock.indicator
        tick = stock.tick

        return (
            indicator.vwap is not None
            and tick.ltp < indicator.vwap
        )