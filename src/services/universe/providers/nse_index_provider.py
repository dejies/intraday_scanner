import csv
import io

from services.universe.models import UniverseStock
from services.universe.providers.base_provider import (
    MarketUniverseProvider,
)


class NSEIndexProvider(MarketUniverseProvider):

    def __init__(
        self,
        client,
        index_name: str,
        download_url: str,
    ):

        self._client = client
        self._index_name = index_name
        self._download_url = download_url

    def load(self):

        csv_text = self._client.download(
            self._download_url
        )

        reader = csv.DictReader(
            io.StringIO(csv_text)
        )

        stocks = []

        for row in reader:

            symbol = (
                row.get("Symbol")
                or row.get("SYMBOL")
                or row.get("symbol")
            )

            if not symbol:
                continue

            company = (
                row.get("Company Name")
                or row.get("Company")
                or symbol
            )

            stocks.append(
                UniverseStock(
                    symbol=symbol.strip().upper(),
                    company_name=company.strip(),
                    index_name=self._index_name,
                )
            )

        return stocks