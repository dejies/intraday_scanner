"""
Evidence contributed by a strategy.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class SignalEvidence:

    #
    # Strategy name
    #
    strategy: str

    #
    # BUY / SELL
    #
    signal: str

    #
    # Evidence description
    #
    reason: str

    #
    # Weight contributed
    #
    weight: float