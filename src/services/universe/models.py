from __future__ import annotations

from dataclasses import dataclass, field


# ----------------------------------------------------------------------
# Individual stock
# ----------------------------------------------------------------------

@dataclass(slots=True, frozen=True)
class UniverseStock:
    """
    Represents one tradable stock in the market universe.

    This model contains only stock metadata.
    It does NOT contain index membership.
    """

    symbol: str

    company_name: str

    security_id: str | None = None

    exchange_segment: str | None = None


# ----------------------------------------------------------------------
# Stock -> Index relationship
# ----------------------------------------------------------------------

@dataclass(slots=True, frozen=True)
class UniverseMembership:
    """
    Represents membership of a stock in an index.
    """

    symbol: str

    index_name: str


# ----------------------------------------------------------------------
# Provider result
# ----------------------------------------------------------------------

@dataclass(slots=True)
class MarketUniverse:
    """
    Complete market universe returned by providers
    and loaded from the repository.
    """

    stocks: dict[str, UniverseStock] = field(default_factory=dict)

    memberships: set[UniverseMembership] = field(default_factory=set)

    # ---------------------------------------------------------

    def add_stock(
        self,
        stock: UniverseStock,
    ) -> None:

        self.stocks[stock.symbol] = stock

    # ---------------------------------------------------------

    def add_membership(
        self,
        membership: UniverseMembership,
    ) -> None:

        self.memberships.add(membership)

    # ---------------------------------------------------------

    def contains(
        self,
        symbol: str,
    ) -> bool:

        return symbol in self.stocks

    # ---------------------------------------------------------

    def get(
        self,
        symbol: str,
    ) -> UniverseStock | None:

        return self.stocks.get(symbol)

    # ---------------------------------------------------------

    def symbols(self) -> set[str]:

        return set(self.stocks.keys())