"""
Repository responsible for universe persistence.

Responsibilities
----------------
- Create universe tables
- Save stocks
- Save memberships
- Load universe
- Clear tables
"""

from __future__ import annotations

import time

from src.database import SQLiteManager
from src.database.schema import TABLES

from src.services.universe.models import (
    MarketUniverse,
    UniverseMembership,
    UniverseStock,
)


class UniverseRepository:

    # ---------------------------------------------------------

    def __init__(
        self,
        sqlite: SQLiteManager,
    ):
        self._sqlite = sqlite
        self._create_schema()

    # ---------------------------------------------------------

    def _create_schema(self):

        self._sqlite.execute(TABLES[1])
        self._sqlite.execute(TABLES[2])
        self._sqlite.execute(TABLES[4])

    # ---------------------------------------------------------

    def save_stocks(
        self,
        stocks: list[UniverseStock],
    ):

        sql = """
        INSERT OR REPLACE INTO universe
        (
            symbol,
            company_name,
            security_id,
            exchange,
            segment,
            updated_at
        )

        VALUES
        (
            ?,?,?,?,?,?
        )
        """

        now = int(time.time())

        rows = [

            (
                stock.symbol,
                stock.company_name,
                stock.security_id,
                stock.exchange,
                stock.segment,
                now,
            )

            for stock in stocks
        ]

        self._sqlite.executemany(
            sql,
            rows,
        )

    # ---------------------------------------------------------

    def save_memberships(
        self,
        memberships: list[UniverseMembership],
    ):

        sql = """
        INSERT OR REPLACE INTO universe_indices
        (
            symbol,
            index_name
        )

        VALUES
        (
            ?,?
        )
        """

        rows = [

            (
                membership.symbol,
                membership.index_name,
            )

            for membership in memberships
        ]

        self._sqlite.executemany(
            sql,
            rows,
        )

    # ---------------------------------------------------------

    def load_universe(
        self,
    ) -> MarketUniverse:

        universe = MarketUniverse()

        #
        # Stocks
        #

        rows = self._sqlite.query(
            """
            SELECT *

            FROM universe
            """
        )

        for row in rows:

            universe.add_stock(

                UniverseStock(

                    symbol=row["symbol"],

                    company_name=row["company_name"],

                    security_id=row["security_id"],

                    exchange=row["exchange"],

                    segment=row["segment"],
                )
            )

        #
        # Memberships
        #

        rows = self._sqlite.query(
            """
            SELECT *

            FROM universe_indices
            """
        )

        for row in rows:

            universe.add_membership(

                UniverseMembership(

                    symbol=row["symbol"],

                    index_name=row["index_name"],
                )
            )

        return universe

    # ---------------------------------------------------------

    def delete_all(self):

        self._sqlite.execute(
            "DELETE FROM universe_indices"
        )

        self._sqlite.execute(
            "DELETE FROM universe"
        )

    # ---------------------------------------------------------

    def count(self):

        rows = self._sqlite.query(
            """
            SELECT COUNT(*) cnt

            FROM universe
            """
        )

        return rows[0]["cnt"]