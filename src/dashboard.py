"""
Console Dashboard

Displays ranked trading signals.
"""

from __future__ import annotations

from datetime import datetime

from src.models.signal import Signal


class Dashboard:

    def display(
        self,
        signals: list[Signal],
    ) -> None:
        """
        Display ranked signals.
        """

        print()
        print("=" * 100)
        print("               INTRADAY STOCK SCANNER")
        print("=" * 100)
        print(
            f"Time : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        print(f"Signals Found : {len(signals)}")
        print("=" * 100)

        if not signals:
            print("No trading signals found.")
            print("=" * 100)
            return

        header = (
            f"{'Symbol':<12}"
            f"{'Signal':<8}"
            f"{'Strategy':<12}"
            f"{'Price':>12}"
            f"{'Confidence':>12}"
            f"   Message"
        )

        print(header)
        print("-" * 100)

        for signal in signals:

            print(
                f"{signal.symbol:<12}"
                f"{signal.signal.value:<8}"
                f"{signal.strategy.value:<12}"
                f"{signal.price:>12.2f}"
                f"{signal.confidence:>12}%"
                f"   {signal.message}"
            )

        print("=" * 100)