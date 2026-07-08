"""
Console Dashboard

Displays ranked trading signals.
"""

from __future__ import annotations

from datetime import datetime

from src.models.signal import Signal


class Dashboard:
    """
    Console dashboard for the intraday scanner.
    """

    WIDTH = 120

    def display(
        self,
        signals: list[Signal],
        connected: bool = True,
    ) -> None:
        """
        Display trading dashboard.
        """

        print()

        print("=" * self.WIDTH)

        print(
            f" Time : {datetime.now().strftime('%H:%M:%S')}"
            f"{' ' * 40}"
            f"Connected : {'YES' if connected else 'NO'}"
        )

        print("=" * self.WIDTH)

        header = (
            f"{'Symbol':<12}"
            f"{'LTP':>10}"
            f"{'EMA20':>10}"
            f"{'EMA50':>10}"
            f"{'RSI':>8}"
            f"{'VWAP':>10}"
            f"{'Volume':>12}"
            f"{'Signal':>10}"
            f"{'Conf':>10}"
        )

        print(header)

        print("-" * self.WIDTH)

        if not signals:

            print()
            print(" No trading signals available.")
            print()

            print("=" * self.WIDTH)

            return

        for signal in signals:

            print(
                f"{signal.symbol:<12}"
                f"{signal.price:>10.2f}"
                f"{'--':>10}"
                f"{'--':>10}"
                f"{'--':>8}"
                f"{'--':>10}"
                f"{'--':>12}"
                f"{signal.signal.value:>10}"
                f"{str(signal.confidence) + '%':>10}"
            )

        print("=" * self.WIDTH)