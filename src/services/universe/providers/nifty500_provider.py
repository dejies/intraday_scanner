from __future__ import annotations

import csv
import io

from src.services.universe.clients import NSEHttpClient
from src.services.universe.models import (
    MarketUniverse,
    UniverseMembership,
    UniverseStock,
)
from src.services.universe.providers.base_provider import (
    MarketUniverseProvider,
)


class Nifty500Provider(MarketUniverseProvider):
    """
    Loads Nifty 500 constituents from NSE.
    """

    #
    # Replace this with the verified
    # official download URL.
    #
    DOWNLOAD_URL = "<NIFTY500_DOWNLOAD_URL>"

    def __init__(
        self,
        client: NSEHttpClient,
    ):
        self._client = client

    # ---------------------------------------------------------

    def load(self) -> MarketUniverse:

        csv_text = self._client.get_text(
            self.DOWNLOAD_URL
        )

        reader = csv.DictReader(
            io.StringIO(csv_text)
        )

        universe = MarketUniverse()

        for row in reader:

            symbol = (
                row.get("Symbol")
                or row.get("SYMBOL")
                or row.get("symbol")
            )

            if not symbol:
                continue

            symbol = symbol.strip().upper()

            company = (
                row.get("Company Name")
                or row.get("Company")
                or symbol
            ).strip()

            universe.add_stock(
                UniverseStock(
                    symbol=symbol,
                    company_name=company,
                )
            )

            universe.add_membership(
                UniverseMembership(
                    symbol=symbol,
                    index_name="NIFTY500",
                )
            )

        return universe