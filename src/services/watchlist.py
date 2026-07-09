"""
Watchlist Service

Loads and manages the application watchlist.

The watchlist contains only the symbols to monitor.
Instrument metadata is resolved using the Instrument Master.
"""

from __future__ import annotations

import csv
from pathlib import Path

from src.core.exceptions import WatchlistError
from src.models.instrument import Instrument
from src.services.base_service import BaseService
from src.services.instrument_master_service import (
    InstrumentMasterService,
)


class WatchlistService(BaseService):
    """
    Watchlist manager.

    Uses the Instrument Master as the single source of truth.
    """

    def __init__(
            self,
            instrument_master: InstrumentMasterService,
    ) -> None:

        super().__init__()

        self.instrument_master = instrument_master

        #
        # Loaded instruments.
        #
        self._instruments: list[Instrument] = []

        #
        # Fast lookups.
        #
        self._symbol_lookup: dict[str, Instrument] = {}

        self._security_lookup: dict[int, str] = {}

    # ------------------------------------------------------------------

    def load(self) -> None:
        """
        Load watchlist from CSV.

        Instrument information is resolved using the
        Instrument Master.
        """

        self.logger.info("Loading watchlist...")

        self._instruments.clear()
        self._symbol_lookup.clear()
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

                    enabled = (
                        row["enabled"]
                        .strip()
                        .lower()
                        in (
                            "true",
                            "1",
                            "yes",
                            "y",
                        )
                    )

                    if not enabled:
                        continue

                    symbol = (
                        row["symbol"]
                        .strip()
                        .upper()
                    )

                    instrument = (
                        self.instrument_master
                        .get_by_symbol(symbol)
                    )

                    if instrument is None:

                        self.logger.warning(
                            "Unknown symbol in watchlist: %s",
                            symbol,
                        )

                        continue

                    self._instruments.append(
                        instrument
                    )

                    self._symbol_lookup[
                        instrument.symbol
                    ] = instrument

                    self._security_lookup[
                        instrument.security_id
                    ] = instrument.symbol

            self.logger.info(
                "Loaded %d enabled instruments.",
                self.count(),
            )

        except Exception as exc:

            raise WatchlistError(
                f"Unable to load watchlist: {exc}"
            ) from exc

    # ------------------------------------------------------------------

    def get_all(
            self,
    ) -> list[Instrument]:
        """
        Return all enabled instruments.
        """

        return list(self._instruments)

    # ------------------------------------------------------------------

    def get_symbols(
            self,
    ) -> list[str]:
        """
        Return all enabled symbols.
        """

        return list(
            self._symbol_lookup.keys()
        )

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

    def get_instrument(
            self,
            symbol: str,
    ) -> Instrument | None:
        """
        Return Instrument by symbol.
        """

        return self._symbol_lookup.get(
            symbol.upper()
        )

    # ------------------------------------------------------------------

    def has_symbol(
            self,
            symbol: str,
    ) -> bool:
        """
        Check whether a symbol exists.
        """

        return (
            symbol.upper()
            in self._symbol_lookup
        )

    # ------------------------------------------------------------------

    def count(
            self,
    ) -> int:
        """
        Return number of enabled instruments.
        """

        return len(
            self._instruments
        )

    # ------------------------------------------------------------------

    def is_empty(
            self,
    ) -> bool:
        """
        Return True if watchlist is empty.
        """

        return not self._instruments