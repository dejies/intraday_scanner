"""
Console Dashboard

Displays ranked trading signals.
"""

from __future__ import annotations

from datetime import datetime

from src.models.indicator import IndicatorData
from src.models.signal import Signal


class Dashboard:
    """
    Console dashboard for the intraday scanner.
    """

    WIDTH = 120

    def display(
            self,
            signals: list[Signal],
            indicators: dict[str, IndicatorData],
            connected: bool,
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
            f"{'RVOL':>12}"
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

            indicator = indicators.get(signal.symbol)
            #
            # Default values.
            #
            ema20 = "--"
            ema50 = "--"
            rsi = "--"
            vwap = "--"
            rvol = "--"

            if indicator is not None:

                if indicator.ema20 is not None:
                    ema20 = f"{indicator.ema20:.2f}"

                if indicator.ema50 is not None:
                    ema50 = f"{indicator.ema50:.2f}"

                if indicator.rsi14 is not None:
                    rsi = f"{indicator.rsi14:.2f}"

                if indicator.vwap is not None:
                    vwap = f"{indicator.vwap:.2f}"

                if indicator.relative_volume is not None:
                    rvol = f"{indicator.relative_volume:.2f}x"

            print(
                f"{signal.symbol:<12}"
                f"{signal.price:>10.2f}"
                f"{ema20:>10}"
                f"{ema50:>10}"
                f"{rsi:>8}"
                f"{vwap:>10}"
                f"{rvol:>12}"
                f"{signal.signal.value:>10}"
                f"{str(signal.confidence) + '%':>10}"
            )

        print("=" * self.WIDTH)