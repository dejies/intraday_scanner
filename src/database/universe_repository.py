"""
Repository responsible for universe persistence.

Responsibilities
----------------
- Create universe table
- Save stocks
- Load stocks
- Clear table

Knows NOTHING about
NSE download
Scanner
Dashboard
"""

from __future__ import annotations

import time

from src.database import SQLiteManager
from src.database.schema import TABLES
from src.services.universe.models import UniverseStock


class UniverseRepository:

    TABLE_NAME = "universe"

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

    # ---------------------------------------------------------

    def save_all(
        self,
        stocks: list[UniverseStock],
    ):

        sql = f"""
        INSERT OR REPLACE INTO {self.TABLE_NAME}
        (
            symbol,
            company_name,
            security_id,
            exchange_segment,
            index_name,
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
                stock.exchange_segment,
                stock.index_name,
                now,
            )

            for stock in stocks
        ]

        self._sqlite.executemany(
            sql,
            rows,
        )

    # ---------------------------------------------------------

    def load_all(
        self,
    ) -> list[UniverseStock]:

        rows = self._sqlite.query(
            f"""
            SELECT *

            FROM {self.TABLE_NAME}

            ORDER BY symbol
            """
        )

        return [
            self._row_to_stock(row)
            for row in rows
        ]

    # ---------------------------------------------------------

    def count(
        self,
    ) -> int:

        rows = self._sqlite.query(
            f"""
            SELECT COUNT(*) count

            FROM {self.TABLE_NAME}
            """
        )

        return rows[0]["count"]

    # ---------------------------------------------------------

    def exists(
        self,
        symbol: str,
    ) -> bool:

        rows = self._sqlite.query(
            f"""
            SELECT 1

            FROM {self.TABLE_NAME}

            WHERE symbol=?

            LIMIT 1
            """,
            (
                symbol,
            ),
        )

        return bool(rows)

    # ---------------------------------------------------------

    def delete_all(
        self,
    ):

        self._sqlite.execute(
            f"""
            DELETE FROM {self.TABLE_NAME}
            """
        )

    # ---------------------------------------------------------

    @staticmethod
    def _row_to_stock(
        row,
    ) -> UniverseStock:

        return UniverseStock(
            symbol=row["symbol"],
            company_name=row["company_name"],
            security_id=row["security_id"],
            exchange_segment=row["exchange_segment"],
            index_name=row["index_name"],
        )