"""
Repository responsible for indicator persistence.

Responsibilities
----------------
- Create indicator table
- Create indexes
- Insert indicator values
- Update indicator values
- Upsert indicator values
- Query indicator history

This repository knows NOTHING about
MarketDataStore, CandleService or Indicator Engines.
"""

from __future__ import annotations

from datetime import datetime
from typing import Iterable

from src.database import SQLiteManager
from src.models.indicator_record import (
    IndicatorRecord,
    IndicatorType,
)
from src.database.schema import (
    TABLES,
    INDEXES,
)


class IndicatorRepository:

    TABLE_NAME = "indicators"

    def __init__(self, sqlite: SQLiteManager):
        self._sqlite = sqlite
        self._create_schema()

    # ------------------------------------------------------------------

    def _create_schema(self):
        """
        Ensure required tables and indexes exist.
        """

        for sql in TABLES:
            self._sqlite.execute(sql)

        for sql in INDEXES:
            self._sqlite.execute(sql)

    # ------------------------------------------------------------------

    def upsert(
        self,
        indicator: IndicatorRecord,
    ):
        """
        Insert or update one indicator value.
        """

        sql = f"""
        INSERT INTO {self.TABLE_NAME}
        (
            security_id,
            timeframe,
            indicator,
            candle_time,
            value
        )
        VALUES
        (
            ?,?,?,?,?
        )

        ON CONFLICT
        (
            security_id,
            timeframe,
            indicator,
            candle_time
        )

        DO UPDATE SET

            value=excluded.value
        """

        self._sqlite.execute(
            sql,
            (
                indicator.security_id,
                indicator.timeframe,
                indicator.indicator.value,
                indicator.candle_time.isoformat(),
                float(indicator.value),
            ),
        )

    # ------------------------------------------------------------------

    def insert_many(
        self,
        indicators: Iterable[IndicatorRecord],
    ):
        """
        Bulk insert indicator values.
        """

        sql = f"""
        INSERT INTO {self.TABLE_NAME}
        (
            security_id,
            timeframe,
            indicator,
            candle_time,
            value
        )
        VALUES
        (
            ?,?,?,?,?
        )

        ON CONFLICT
        (
            security_id,
            timeframe,
            indicator,
            candle_time
        )

        DO UPDATE SET

            value=excluded.value
        """

        rows = [
            (
                record.security_id,
                record.timeframe,
                record.indicator.value,
                record.candle_time.isoformat(),
                float(record.value),
            )
            for record in indicators
        ]

        self._sqlite.executemany(sql, rows)

    # ------------------------------------------------------------------

    def latest(
        self,
        security_id: str,
        timeframe: str,
        indicator: IndicatorType,
    ) -> IndicatorRecord | None:
        """
        Return latest indicator value.
        """

        sql = f"""
        SELECT *

        FROM {self.TABLE_NAME}

        WHERE

            security_id=?
            AND timeframe=?
            AND indicator=?

        ORDER BY candle_time DESC

        LIMIT 1
        """

        rows = self._sqlite.query(
            sql,
            (
                security_id,
                timeframe,
                indicator.value,
            ),
        )

        if not rows:
            return None

        return self._row_to_record(rows[0])

    # ------------------------------------------------------------------

    def history(
        self,
        security_id: str,
        timeframe: str,
        indicator: IndicatorType,
        limit: int = 200,
    ) -> list[IndicatorRecord]:
        """
        Return indicator history ordered by candle time.
        """

        sql = f"""
        SELECT *

        FROM {self.TABLE_NAME}

        WHERE

            security_id=?
            AND timeframe=?
            AND indicator=?

        ORDER BY candle_time ASC

        LIMIT ?
        """

        rows = self._sqlite.query(
            sql,
            (
                security_id,
                timeframe,
                indicator.value,
                limit,
            ),
        )

        return [
            self._row_to_record(row)
            for row in rows
        ]

    # ------------------------------------------------------------------

    def delete(
        self,
        security_id: str,
        timeframe: str,
    ):
        """
        Delete all indicator values for a symbol/timeframe.
        """

        self._sqlite.execute(
            f"""
            DELETE

            FROM {self.TABLE_NAME}

            WHERE

                security_id=?
                AND timeframe=?
            """,
            (
                security_id,
                timeframe,
            ),
        )

    # ------------------------------------------------------------------

    def delete_all(self):
        """
        Delete every indicator record.
        """

        self._sqlite.execute(
            f"""
            DELETE FROM {self.TABLE_NAME}
            """
        )

    # ------------------------------------------------------------------

    @staticmethod
    def _row_to_record(
        row,
    ) -> IndicatorRecord:

        return IndicatorRecord(
            security_id=row["security_id"],
            timeframe=row["timeframe"],
            indicator=IndicatorType(row["indicator"]),
            candle_time=datetime.fromisoformat(
                row["candle_time"]
            ),
            value=float(row["value"]),
        )