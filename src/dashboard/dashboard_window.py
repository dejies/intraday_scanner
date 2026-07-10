"""
Main Dashboard Window.
"""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QLabel,
    QMainWindow,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
    QHBoxLayout,
    QHeaderView,
)


class DashboardWindow(QMainWindow):
    """
    Main application dashboard.
    """

    BUY_COLUMNS = (
        "Symbol",
        "LTP",
        "Current",
        "Signal",
        "Strategy",
        "Confidence",
    )

    SELL_COLUMNS = BUY_COLUMNS

    def __init__(self) -> None:

        super().__init__()

        self.setWindowTitle(
            "Indian Intraday Scanner"
        )

        self.resize(
            1400,
            900,
        )

        self._build_ui()

    # ------------------------------------------------------------------

    def _build_ui(self) -> None:

        central = QWidget()

        self.setCentralWidget(
            central
        )

        layout = QVBoxLayout(central)

        #
        # Status Bar
        #
        status_layout = QHBoxLayout()

        self.market_label = QLabel(
            "Market : CLOSED"
        )

        self.connection_label = QLabel(
            "Connection : DISCONNECTED"
        )

        self.watching_label = QLabel(
            "Watching : 0"
        )

        self.datetime_label = QLabel(
            "-"
        )

        status_layout.addWidget(
            self.market_label
        )

        status_layout.addSpacing(20)

        status_layout.addWidget(
            self.connection_label
        )

        status_layout.addSpacing(20)

        status_layout.addWidget(
            self.watching_label
        )

        status_layout.addSpacing(20)

        status_layout.addWidget(
            self.datetime_label
        )

        status_layout.addStretch()

        layout.addLayout(
            status_layout
        )

        #
        # BUY Section
        #
        layout.addWidget(
            QLabel("BUY Signals")
        )

        self.buy_table = self._create_table(
            self.BUY_COLUMNS
        )

        layout.addWidget(
            self.buy_table
        )

        #
        # SELL Section
        #
        layout.addWidget(
            QLabel("SELL Signals")
        )

        self.sell_table = self._create_table(
            self.SELL_COLUMNS
        )

        layout.addWidget(
            self.sell_table
        )

    # ------------------------------------------------------------------

    def _create_table(
            self,
            columns: tuple[str, ...],
    ) -> QTableWidget:

        table = QTableWidget()

        table.setColumnCount(
            len(columns)
        )

        table.setHorizontalHeaderLabels(
            columns
        )

        table.verticalHeader().setVisible(
            False
        )

        table.setEditTriggers(
            QTableWidget.NoEditTriggers
        )

        table.setSelectionBehavior(
            QTableWidget.SelectRows
        )

        table.setSelectionMode(
            QTableWidget.SingleSelection
        )

        table.setAlternatingRowColors(
            True
        )

        table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        return table

    # ------------------------------------------------------------------

    def update_status(
            self,
            market_status: str,
            connected: bool,
            watching: int,
            current_datetime: str,
    ) -> None:

        self.market_label.setText(
            f"Market : {market_status}"
        )

        self.connection_label.setText(
            "Connection : CONNECTED"
            if connected
            else "Connection : DISCONNECTED"
        )

        self.watching_label.setText(
            f"Watching : {watching}"
        )

        self.datetime_label.setText(
            current_datetime
        )

    # ------------------------------------------------------------------

    def update_buy_table(
            self,
            rows: list[list[str]],
    ) -> None:

        self._update_table(
            self.buy_table,
            rows,
        )

    # ------------------------------------------------------------------

    def update_sell_table(
            self,
            rows: list[list[str]],
    ) -> None:

        self._update_table(
            self.sell_table,
            rows,
        )

    # ------------------------------------------------------------------

    @staticmethod
    def _update_table(
            table: QTableWidget,
            rows: list[list[str]],
    ) -> None:

        table.setRowCount(
            len(rows)
        )

        for row_index, row in enumerate(rows):

            for column_index, value in enumerate(row):

                item = QTableWidgetItem(
                    str(value)
                )

                item.setTextAlignment(
                    Qt.AlignCenter
                )

                table.setItem(
                    row_index,
                    column_index,
                    item,
                )