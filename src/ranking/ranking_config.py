"""
Ranking configuration.
"""

from dataclasses import dataclass


@dataclass(slots=True)
class RankingConfig:

    #
    # Minimum acceptable score.
    #
    minimum_score: float = 40.0

    #
    # Maximum BUY signals.
    #
    max_buy_signals: int = 10

    #
    # Maximum SELL signals.
    #
    max_sell_signals: int = 10