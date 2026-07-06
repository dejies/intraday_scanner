"""
Stock model.
"""

from dataclasses import dataclass

from src.core.constants import Exchange


@dataclass(slots=True)
class Stock:
    """
    Represents a tradable stock.
    """

    security_id: str

    symbol: str

    exchange: Exchange

    name: str

    enabled: bool = True