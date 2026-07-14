"""
Base class for all trading strategies.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from src.core.market_data_store import StockState
from src.strategies.strategy_result import StrategyResult


class BaseStrategy(ABC):
    """
    Base class for all trading strategies.
    """

    def __init__(
        self,
        name: str,
    ):
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    @abstractmethod
    def evaluate(
        self,
        stock: StockState,
    ) -> StrategyResult | None:
        """
        Evaluate a stock and return a strategy result.

        Returns
        -------
        StrategyResult
            Valid trading signal.

        None
            No signal generated.
        """
        raise NotImplementedError