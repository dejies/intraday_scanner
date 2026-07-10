"""
Main Dashboard Window.
"""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QLabel,
    QHBoxLayout,
    QHeaderView,
    QMainWindow,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
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

    SYMBOL_COLUMN = 0
    CONFIDENCE_COLUMN = 5

    def __init__(self) -> None:

        super().__init__()

        self.setWindowTitle(
            "Indian Intraday Scanner"
        )

        self.resize(
            1400,
            900,
        )

        #
        # Remember current sorting for both tables.
        # Default = Confidence DESC
        #
        self._buy_sort_column = self.CONFIDENCE_COLUMN
        self._buy_sort_order = Qt.DescendingOrder

        self._sell_sort_column = self.CONFIDENCE_COLUMN
        self._sell_sort_order = Qt.DescendingOrder

        self._build_ui()

        #
        # Apply default sorting.
        #
        self.buy_table.sortByColumn(
            self.CONFIDENCE_COLUMN,
            Qt.DescendingOrder,
        )

        self.sell_table.sortByColumn(
            self.CONFIDENCE_COLUMN,
            Qt.DescendingOrder,
        )

        #
        # Listen for user sorting.
        #
        self.buy_table.horizontalHeader().sortIndicatorChanged.connect(
            self._buy_sort_changed
        )

        self.sell_table.horizontalHeader().sortIndicatorChanged.connect(
            self._sell_sort_changed
        )

    # ------------------------------------------------------------------

    def _build_ui(self) -> None:

        central = QWidget()

        self.setCentralWidget(
            central
        )

        layout = QVBoxLayout(
            central
        )

        #
        # Status
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
        # BUY
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
        # SELL
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

        table.setSortingEnabled(
            True
        )

        return table

    # ------------------------------------------------------------------

    def _buy_sort_changed(
        self,
        column: int,
        order: Qt.SortOrder,
    ) -> None:

        self._buy_sort_column = column
        self._buy_sort_order = order

    # ------------------------------------------------------------------

    def _sell_sort_changed(
        self,
        column: int,
        order: Qt.SortOrder,
    ) -> None:

        self._sell_sort_column = column
        self._sell_sort_order = order

    # ------------------------------------------------------------------

    @staticmethod
    def _selected_symbol(
        table: QTableWidget,
    ) -> str | None:

        row = table.currentRow()

        if row < 0:
            return None

        item = table.item(
            row,
            DashboardWindow.SYMBOL_COLUMN,
        )

        if item is None:
            return None

        return item.text()

    # ------------------------------------------------------------------

    @staticmethod
    def _restore_selection(
        table: QTableWidget,
        symbol: str | None,
    ) -> None:

        if symbol is None:
            return

        for row in range(
            table.rowCount()
        ):

            item = table.item(
                row,
                DashboardWindow.SYMBOL_COLUMN,
            )

            if (
                item is not None
                and item.text() == symbol
            ):
                table.selectRow(
                    row
                )
                return

    # ------------------------------------------------------------------

    @staticmethod
    def _find_row(
        table: QTableWidget,
        symbol: str,
    ) -> int:

        for row in range(
            table.rowCount()
        ):

            item = table.item(
                row,
                DashboardWindow.SYMBOL_COLUMN,
            )

            if (
                item is not None
                and item.text() == symbol
            ):
                return row

        return -1

    # ------------------------------------------------------------------

    @staticmethod
    def _set_cell(
        table: QTableWidget,
        row: int,
        column: int,
        value: str,
    ) -> None:

        value = str(value)

        item = table.item(
            row,
            column,
        )

        if item is None:

            item = QTableWidgetItem(
                value
            )

            item.setTextAlignment(
                Qt.AlignCenter
            )

            table.setItem(
                row,
                column,
                item,
            )

            return

        if item.text() != value:
            item.setText(
                value
            )

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
            table=self.buy_table,
            rows=rows,
            sort_column=self._buy_sort_column,
            sort_order=self._buy_sort_order,
        )

    # ------------------------------------------------------------------

    def update_sell_table(
        self,
        rows: list[list[str]],
    ) -> None:

        self._update_table(
            table=self.sell_table,
            rows=rows,
            sort_column=self._sell_sort_column,
            sort_order=self._sell_sort_order,
        )

    # ------------------------------------------------------------------

    @classmethod
    def _update_table(
        cls,
        table: QTableWidget,
        rows: list[list[str]],
        sort_column: int,
        sort_order: Qt.SortOrder,
    ) -> None:

        selected_symbol = cls._selected_symbol(
            table
        )

        #
        # Disable sorting while updating.
        #
        table.setSortingEnabled(
            False
        )

        #
        # Remove duplicate symbols from incoming data.
        #
        unique_rows: dict[str, list[str]] = {}

        for row in rows:

            if not row:
                continue

            symbol = str(
                row[
                    cls.SYMBOL_COLUMN
                ]
            )

            unique_rows[
                symbol
            ] = row

        #
        # Remove symbols that disappeared.
        #
        existing_symbols = []

        for row in range(
            table.rowCount()
        ):

            item = table.item(
                row,
                cls.SYMBOL_COLUMN,
            )

            if item is not None:
                existing_symbols.append(
                    item.text()
                )

        for symbol in reversed(
            existing_symbols
        ):

            if symbol not in unique_rows:

                row = cls._find_row(
                    table,
                    symbol,
                )

                if row >= 0:
                    table.removeRow(
                        row
                    )

        #
        # Update existing rows / insert new rows.
        #
        for symbol, row_data in unique_rows.items():

            row = cls._find_row(
                table,
                symbol,
            )

            if row < 0:

                row = table.rowCount()

                table.insertRow(
                    row
                )

            for column, value in enumerate(
                row_data
            ):

                cls._set_cell(
                    table,
                    row,
                    column,
                    value,
                )

        #
        # Restore sorting.
        #
        table.setSortingEnabled(
            True
        )

        table.sortByColumn(
            sort_column,
            sort_order,
        )

        #
        # Restore previous selection.
        #
        cls._restore_selection(
            table,
            selected_symbol,
        )