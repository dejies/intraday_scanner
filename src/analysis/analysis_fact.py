"""
Facts produced by analyzers.

Analyzers NEVER assign scores.
They only report facts.

The ScoringEngine decides the weight
of each fact.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class AnalysisFactType(Enum):

    #
    # Trend
    #
    EMA_ALIGNMENT = "EMA_ALIGNMENT"

    EMA_BULLISH_ALIGNMENT="EMA_BULLISH_ALIGNMENT"

    EMA_BEARISH_ALIGNMENT="EMA_BEARISH_ALIGNMENT"
    
    ADX_STRONG = "ADX_STRONG"

    PRICE_ABOVE_EMA20 = "PRICE_ABOVE_EMA20"

    PRICE_BELOW_EMA20 = "PRICE_BELOW_EMA20"

    PRICE_NEAR_EMA20 = "PRICE_NEAR_EMA20"

    PRICE_NEAR_EMA50 = "PRICE_NEAR_EMA50"

    #
    # Momentum
    #
    RSI_BULLISH = "RSI_BULLISH"

    RSI_BEARISH = "RSI_BEARISH"

    MACD_BULLISH = "MACD_BULLISH"

    MACD_BEARISH = "MACD_BEARISH"

    #
    # Volume
    #
    ABOVE_VWAP = "ABOVE_VWAP"

    BELOW_VWAP = "BELOW_VWAP"

    RVOL_HIGH = "RVOL_HIGH"

    #
    # Session
    #
    ORB_BREAKOUT = "ORB_BREAKOUT"

    GAP_UP = "GAP_UP"

    GAP_DOWN = "GAP_DOWN"

    #
    # Pattern
    #
    PULLBACK = "PULLBACK"


@dataclass(slots=True)
class AnalysisFact:

    type: AnalysisFactType

    description: str

    value: float | None = None