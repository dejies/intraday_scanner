"""
Trading signal model.
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class Signal:
    """
    Represents a scanner signal.
    """

    symbol: str

    strategy: str

    signal: str

    price: float

    confidence: float

    timestamp: datetime

    message: str