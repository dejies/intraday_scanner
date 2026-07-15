"""
Evidence model used by the confidence engine.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class EvidenceType(Enum):

    EMA_ALIGNMENT = "EMA_ALIGNMENT"

    RSI_BULLISH = "RSI_BULLISH"
    RSI_BEARISH = "RSI_BEARISH"

    MACD_BULLISH = "MACD_BULLISH"
    MACD_BEARISH = "MACD_BEARISH"

    ADX_STRONG = "ADX_STRONG"

    ABOVE_VWAP = "ABOVE_VWAP"
    BELOW_VWAP = "BELOW_VWAP"

    ORB_BREAKOUT = "ORB_BREAKOUT"

    GAP_CONTINUATION = "GAP_CONTINUATION"

    PULLBACK = "PULLBACK"


@dataclass(slots=True)
class SignalEvidence:

    strategy: str

    signal: str

    evidence: EvidenceType

    description: str