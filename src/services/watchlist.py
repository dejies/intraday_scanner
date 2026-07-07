"""
Watchlist Service

Loads and manages the watchlist.
"""

from __future__ import annotations

import csv
from pathlib import Path

from src.core.constants import Exchange
from src.core.exceptions import WatchlistError
from src.models.stock import Stock
from src.services.base_service import BaseService


class WatchlistService(BaseService):
    """
    Loads and manages the stock watchlist.
    """

    def __init__(self) -> None:
        super().__init__()

        self._stocks: list[Stock] = []

        #
        # Fast lookup:
        # security_id -> symbol
        #
        self._security_lookup: dict[int, str] = {}

    # ------------------------------------------------------------------

    def load(self) -> None:
        """
        Load watchlist from CSV.
        """

        self.logger.info("Loading watchlist...")

        self._stocks.clear()
        self._security_lookup.clear()

        path = Path(self.settings.watchlist_file)

        if not path.exists():
            raise WatchlistError(
                f"Watchlist file not found: {path}"
            )

        try:

            with path.open(
                "r",
                newline="",
                encoding="utf-8",
            ) as file:

                reader = csv.DictReader(file)

                for row in reader:

                    stock = Stock(
                        security_id=str(
                            row["security_id"]
                        ).strip(),

                        symbol=row["symbol"]
                        .strip()
                        .upper(),

                        exchange=Exchange(
                            row["exchange"]
                            .strip()
                            .upper()
                        ),

                        #
                        # Optional column.
                        #
                        name=row.get(
                            "name",
                            row["symbol"],
                        ).strip(),

                        enabled=row["enabled"]
                        .strip()
                        .lower()
                        in (
                            "true",
                            "1",
                            "yes",
                            "y",
                        ),
                    )

                    if not stock.enabled:
                        continue

                    self._stocks.append(stock)

                    self._security_lookup[
                        int(stock.security_id)
                    ] = stock.symbol

            self.logger.info(
                "Loaded %d enabled stocks.",
                len(self._stocks),
            )

        except Exception as exc:

            raise WatchlistError(
                f"Unable to load watchlist: {exc}"
            ) from exc

    # ------------------------------------------------------------------

    def get_all(self) -> list[Stock]:
        """
        Return all enabled stocks.
        """

        return list(self._stocks)

    # ------------------------------------------------------------------

    def get_symbols(self) -> list[str]:
        """
        Return all symbols.
        """

        return [
            stock.symbol
            for stock in self._stocks
        ]

    # ------------------------------------------------------------------

    def get_symbol(
        self,
        security_id: int,
    ) -> str | None:
        """
        Return symbol for a security id.
        """

        return self._security_lookup.get(
            int(security_id)
        )

    # ------------------------------------------------------------------

    def get_stock(
        self,
        symbol: str,
    ) -> Stock | None:
        """
        Return Stock object for symbol.
        """

        symbol = symbol.upper()

        for stock in self._stocks:

            if stock.symbol == symbol:
                return stock

        return None

    # ------------------------------------------------------------------

    def has_symbol(
        self,
        symbol: str,
    ) -> bool:
        """
        Check whether symbol exists.
        """

        symbol = symbol.upper()

        return any(
            stock.symbol == symbol
            for stock in self._stocks
        )

    # ------------------------------------------------------------------

    def count(self) -> int:
        """
        Return number of enabled stocks.
        """

        return len(self._stocks)

    # ------------------------------------------------------------------

    def is_empty(self) -> bool:
        """
        Return True if watchlist is empty.
        """

        return len(self._stocks) == 0