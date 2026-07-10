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

        self._window.update_buy_table(
            self._build_rows(
                self._market_store.get_buy_signals()
            )
        )

        self._window.update_sell_table(
            self._build_rows(
                self._market_store.get_sell_signals()
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