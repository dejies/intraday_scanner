"""
Watchlist service.

Loads and manages the application's watchlist.
"""

from __future__ import annotations

import csv
from pathlib import Path

from src.core.constants import Exchange
from src.models.stock import Stock
from src.services.base_service import BaseService


class WatchlistService(BaseService):
    """
    Loads and manages the application watchlist.
    """

    def __init__(self) -> None:
        super().__init__()
        self._stocks: list[Stock] = []

    def load(self) -> list[Stock]:
        """
        Load stocks from the configured watchlist CSV.

        Returns
        -------
        list[Stock]
            List of enabled stocks.
        """

        self.logger.info("Loading watchlist...")

        self._stocks.clear()

        file_path: Path = self.settings.watchlist_file

        if not file_path.exists():
            self.logger.error("Watchlist file not found: %s", file_path)
            raise FileNotFoundError(file_path)

        symbols: set[str] = set()

        with file_path.open(
            mode="r",
            newline="",
            encoding="utf-8",
        ) as csv_file:

            reader = csv.DictReader(csv_file)

            for row in reader:

                enabled = (
                    row.get("enabled", "true")
                    .strip()
                    .lower()
                    == "true"
                )

                if not enabled:
                    continue

                symbol = row["symbol"].strip().upper()

                if symbol in symbols:
                    self.logger.warning(
                        "Duplicate symbol '%s' found. Skipping.",
                        symbol,
                    )
                    continue

                symbols.add(symbol)

                stock = Stock(
                    security_id=row["security_id"].strip(),
                    symbol=symbol,
                    exchange=Exchange(
                        row["exchange"].strip().upper()
                    ),
                    name=row["name"].strip(),
                    enabled=True,
                )

                self._stocks.append(stock)

        self.logger.info(
            "Loaded %d enabled stocks.",
            len(self._stocks),
        )

        return self._stocks

    def get_all(self) -> list[Stock]:
        """
        Return all loaded stocks.
        """
        return self._stocks

    def get_symbols(self) -> list[str]:
        """
        Return all symbols.
        """
        return [stock.symbol for stock in self._stocks]

    def get_security_ids(self) -> list[str]:
        """
        Return all Dhan security IDs.
        """
        return [stock.security_id for stock in self._stocks]

    def get_stock(self, symbol: str) -> Stock | None:
        """
        Find a stock by symbol.
        """
        symbol = symbol.upper()

        for stock in self._stocks:
            if stock.symbol == symbol:
                return stock

        return None

    def count(self) -> int:
        """
        Return number of loaded stocks.
        """
        return len(self._stocks)

    def is_loaded(self) -> bool:
        """
        Return True if the watchlist has been loaded.
        """
        return bool(self._stocks)