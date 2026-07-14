"""
Executes all enabled trading strategies.
"""

from __future__ import annotations

from typing import Iterable

from src.core.market_data_store import StockState
from src.strategies.base_strategy import BaseStrategy
from src.strategies.strategy_result import StrategyResult


class StrategyManager:

    def __init__(self):

        self._strategies: list[BaseStrategy] = []

    # ---------------------------------------------------------

    def register(
        self,
        strategy: BaseStrategy,
    ) -> None:

        self._strategies.append(strategy)

    # ---------------------------------------------------------

    def register_all(
        self,
        strategies: Iterable[BaseStrategy],
    ) -> None:

        self._strategies.extend(strategies)

    # ---------------------------------------------------------

    def clear(self) -> None:

        self._strategies.clear()

    # ---------------------------------------------------------

    @property
    def strategies(self) -> tuple[BaseStrategy, ...]:

        return tuple(self._strategies)

    # ---------------------------------------------------------

    def evaluate(
        self,
        stock: StockState,
    ) -> list[StrategyResult]:

        results: list[StrategyResult] = []

        for strategy in self._strategies:

            result = strategy.evaluate(stock)

            if result is not None and result.valid:
                results.append(result)

        return results