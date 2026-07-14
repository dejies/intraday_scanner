"""
Represents the result produced by a trading strategy.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(slots=True)
class StrategyResult:
    """
    Standard result returned by every strategy.
    """

    #
    # Strategy information
    #
    strategy: str

    #
    # BUY / SELL
    #
    signal: str

    #
    # Signal confidence (0-100)
    #
    confidence: float

    #
    # Human-readable explanation
    #
    reason: str

    #
    # Trigger price
    #
    price: float

    #
    # Optional stop loss
    #
    stop_loss: Optional[float] = None

    #
    # Optional target
    #
    target: Optional[float] = None

    #
    # Whether the signal is valid
    #
    valid: bool = True