from src.services.universe.providers.base_provider import (
    MarketUniverseProvider,
)


class UniverseManager:

    def __init__(
        self,
        providers: list[MarketUniverseProvider],
    ):

        self._providers = providers

    def load(self):

        stocks = {}

        for provider in self._providers:

            for stock in provider.load():

                stocks[stock.symbol] = stock

        return list(stocks.values())