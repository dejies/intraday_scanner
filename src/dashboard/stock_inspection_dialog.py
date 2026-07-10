"""
Stock Inspection Dialog.
"""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QFormLayout,
    QFrame,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
)


class StockInspectionDialog(QDialog):
    """
    Displays technical indicators for a selected stock.
    """

    def __init__(
            self,
            stock: dict,
            parent=None,
    ) -> None:

        super().__init__(parent)

        self._stock = stock or {}

        self.setWindowTitle(
            self._stock.get(
                "symbol",
                "Stock Inspection",
            )
        )

        self.setModal(
            True
        )

        self.setFixedSize(
            450,
            650,
        )

        self._build_ui()

        self._load_data()

    # ------------------------------------------------------------------

    def _build_ui(
            self,
    ) -> None:

        root = QVBoxLayout(
            self
        )

        #
        # Header
        #
        header = QHBoxLayout()

        self.symbol_title = QLabel(
            "-"
        )

        self.signal_title = QLabel(
            "-"
        )

        header.addWidget(
            self.symbol_title
        )

        header.addStretch()

        header.addWidget(
            self.signal_title
        )

        root.addLayout(
            header
        )

        line = QFrame()

        line.setFrameShape(
            QFrame.HLine
        )

        root.addWidget(
            line
        )

        #
        # Price
        #
        price_group = QGroupBox(
            "Price"
        )

        self.price_layout = QFormLayout()

        self.symbol_value = QLabel()
        self.ltp_value = QLabel()

        self.price_layout.addRow(
            "Symbol",
            self.symbol_value,
        )

        self.price_layout.addRow(
            "LTP",
            self.ltp_value,
        )

        price_group.setLayout(
            self.price_layout
        )

        root.addWidget(
            price_group
        )

        #
        # Moving Averages
        #
        ma_group = QGroupBox(
            "Moving Averages"
        )

        self.ma_layout = QFormLayout()

        self.ema20_value = QLabel()
        self.ema50_value = QLabel()

        self.ma_layout.addRow(
            "EMA20",
            self.ema20_value,
        )

        self.ma_layout.addRow(
            "EMA50",
            self.ema50_value,
        )

        ma_group.setLayout(
            self.ma_layout
        )

        root.addWidget(
            ma_group
        )

        #
        # Momentum
        #
        momentum_group = QGroupBox(
            "Momentum"
        )

        self.momentum_layout = QFormLayout()

        self.rsi_value = QLabel()

        self.momentum_layout.addRow(
            "RSI",
            self.rsi_value,
        )

        momentum_group.setLayout(
            self.momentum_layout
        )

        root.addWidget(
            momentum_group
        )

        #
        # Volume
        #
        volume_group = QGroupBox(
            "Volume"
        )

        self.volume_layout = QFormLayout()

        self.vwap_value = QLabel()
        self.rvol_value = QLabel()

        self.volume_layout.addRow(
            "VWAP",
            self.vwap_value,
        )

        self.volume_layout.addRow(
            "RVOL",
            self.rvol_value,
        )

        volume_group.setLayout(
            self.volume_layout
        )

        root.addWidget(
            volume_group
        )

        #
        # Signal
        #
        signal_group = QGroupBox(
            "Signal"
        )

        self.signal_layout = QFormLayout()

        self.recommendation_value = QLabel()
        self.confidence_value = QLabel()

        self.signal_layout.addRow(
            "Recommendation",
            self.recommendation_value,
        )

        self.signal_layout.addRow(
            "Confidence",
            self.confidence_value,
        )

        signal_group.setLayout(
            self.signal_layout
        )

        root.addWidget(
            signal_group
        )

        root.addStretch()

        #
        # Close button
        #
        button_layout = QHBoxLayout()

        button_layout.addStretch()

        close_button = QPushButton(
            "Close"
        )

        close_button.clicked.connect(
            self.accept
        )

        button_layout.addWidget(
            close_button
        )

        root.addLayout(
            button_layout
        )

    # ------------------------------------------------------------------

    def _load_data(
            self,
    ) -> None:
        """
        Populate the dialog from the supplied stock dictionary.
        """

        symbol = self._stock.get(
            "symbol",
            "-"
        )

        signal = self._stock.get(
            "signal",
            "-"
        )

        confidence = self._stock.get(
            "confidence",
            "-"
        )

        #
        # Header
        #
        self.symbol_title.setText(
            str(symbol)
        )

        self.signal_title.setText(
            str(signal)
        )

        #
        # Price
        #
        self.symbol_value.setText(
            str(symbol)
        )

        self.ltp_value.setText(
            str(
                self._stock.get(
                    "ltp",
                    "-"
                )
            )
        )

        #
        # Moving Averages
        #
        self.ema20_value.setText(
            str(
                self._stock.get(
                    "ema20",
                    "-"
                )
            )
        )

        self.ema50_value.setText(
            str(
                self._stock.get(
                    "ema50",
                    "-"
                )
            )
        )

        #
        # Momentum
        #
        self.rsi_value.setText(
            str(
                self._stock.get(
                    "rsi",
                    "-"
                )
            )
        )

        #
        # Volume
        #
        self.vwap_value.setText(
            str(
                self._stock.get(
                    "vwap",
                    "-"
                )
            )
        )

        self.rvol_value.setText(
            str(
                self._stock.get(
                    "rvol",
                    "-"
                )
            )
        )

        #
        # Signal
        #
        self.recommendation_value.setText(
            str(signal)
        )

        self.confidence_value.setText(
            f"{confidence}%"
            if confidence != "-"
            else "-"
        )

    # ------------------------------------------------------------------

    def update_stock(
            self,
            stock: dict,
    ) -> None:
        """
        Update the dialog with new stock information.
        """

        self._stock = stock or {}

        self.setWindowTitle(
            self._stock.get(
                "symbol",
                "Stock Inspection",
            )
        )

        self._load_data()