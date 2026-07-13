"""
Dashboard Controller.

Connects MarketDataStore to the DashboardWindow.
"""

from __future__ import annotations

from PySide6.QtCore import QObject, QTimer

from src.core.market_data_store import MarketDataStore
from src.dashboard.dashboard_window import DashboardWindow
from datetime import datetime

class DashboardController(QObject):
    """
    Updates the dashboard periodically.
    """

    def __init__(
            self,
            window: DashboardWindow,
            market_store: MarketDataStore,
    ) -> None:

        super().__init__()

        self._window = window
        self._market_store = market_store

        self._timer = QTimer(self)

        self._timer.setInterval(1000)

        self._timer.timeout.connect(
            self.refresh
        )

    # ------------------------------------------------------------------

    def start(self) -> None:
        """
        Start automatic dashboard refresh.
        """

        self.refresh()

        self._timer.start()

    # ------------------------------------------------------------------

    def refresh(self) -> None:
        """
        Refresh dashboard.
        """

        status = self._market_store.get_market_status()

        self._window.update_status(
            market_status=status.market_state.name,
            connected=status.connection_state.name == "CONNECTED",
            watching=self._market_store.stock_count(),
            current_datetime=datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        )

        buy_stocks = self._market_store.get_buy_signals()
        sell_stocks = self._market_store.get_sell_signals()

        #
        # Cache technical indicators for the inspection window
        #
        self._window.set_stock_details(
            self._build_stock_details(
                buy_stocks,
                sell_stocks,
            )
        )

        self._window.update_buy_table(
            self._build_rows(
                buy_stocks
            )
        )

        self._window.update_sell_table(
            self._build_rows(
                sell_stocks
            )
        )

    # ------------------------------------------------------------------

    @staticmethod
    def _build_rows(
            stocks,
    ) -> list[list[str]]:
        """
        Convert StockState objects into table rows.
        """

        rows = []

        for stock in stocks:

            tick = stock.tick

            signal = stock.active_signal

            rows.append([
                stock.instrument.symbol,
                f"{tick.ltp:.2f}" if tick else "-",
                f"{tick.ltp:.2f}" if tick else "-",
                f"{signal.signal_price:.2f}" if signal else "-",
                signal.strategy if signal else "-",
                f"{signal.confidence:.1f}" if signal else "-",
            ])

        return rows

    # ------------------------------------------------------------------

    @staticmethod
    def _build_stock_details(
            buy_stocks,
            sell_stocks,
    ) -> dict[str, dict]:
        """
        Build stock details for the inspection window.
        """

        details: dict[str, dict] = {}

        for stock in list(buy_stocks) + list(sell_stocks):
            tick = stock.tick
            indicator = stock.indicator
            print(
                stock.instrument.symbol,
                indicator,
            )

            signal = stock.active_signal

            details[stock.instrument.symbol] = {

                "symbol": stock.instrument.symbol,

                #
                # Price
                #
                "ltp": (
                    round(float(tick.ltp), 2)
                    if tick
                    else "-"
                ),

                #
                # Trend
                #
                "ema9": (
                    round(indicator.ema9, 2)
                    if indicator and indicator.ema9 is not None
                    else "-"
                ),

                "ema20": (
                    round(indicator.ema20, 2)
                    if indicator and indicator.ema20 is not None
                    else "-"
                ),

                "ema50": (
                    round(indicator.ema50, 2)
                    if indicator and indicator.ema50 is not None
                    else "-"
                ),

                "ema200": (
                    round(indicator.ema200, 2)
                    if indicator and indicator.ema200 is not None
                    else "-"
                ),

                #
                # Momentum
                #
                "rsi14": (
                    round(indicator.rsi14, 2)
                    if indicator and indicator.rsi14 is not None
                    else "-"
                ),

                "macd": (
                    round(indicator.macd, 4)
                    if indicator and indicator.macd is not None
                    else "-"
                ),

                "macd_signal": (
                    round(indicator.macd_signal, 4)
                    if indicator and indicator.macd_signal is not None
                    else "-"
                ),

                "macd_histogram": (
                    round(indicator.macd_histogram, 4)
                    if indicator and indicator.macd_histogram is not None
                    else "-"
                ),

                #
                # Trend Strength
                #
                "adx14": (
                    round(indicator.adx14, 2)
                    if indicator and indicator.adx14 is not None
                    else "-"
                ),

                #
                # Intraday
                #
                "vwap": (
                    round(indicator.vwap, 2)
                    if indicator and indicator.vwap is not None
                    else "-"
                ),

                #
                # Volume
                #
                "relative_volume": (
                    round(indicator.relative_volume, 2)
                    if indicator and indicator.relative_volume is not None
                    else "-"
                ),

                #
                # Signal
                #
                "signal": (
                    signal.strategy
                    if signal
                    else "-"
                ),

                "confidence": (
                    round(signal.confidence, 1)
                    if signal
                    else "-"
                ),
            }

        return details