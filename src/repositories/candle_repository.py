"""
Repository responsible for candle persistence.

Responsibilities
----------------
- Create candle table
- Create indexes
- Insert candles
- Update candles
- Upsert candles
- Query candles

This repository knows NOTHING about
MarketDataStore or WebSocket.
"""

from __future__ import annotations

from typing import Iterable

from src.database import SQLiteManager
from datetime import datetime, timezone
from src.models import Candle, CandleInterval
from src.database.schema import (
    CANDLE_INDEXES,
    CANDLE_TABLE_SQL,
)
from decimal import Decimal


class CandleRepository:

    TABLE_NAME = "candles"

    def __init__(self, sqlite: SQLiteManager):
        self._sqlite = sqlite
        self._create_table()

    # ---------------------------------------------------------

    def _create_table(self):
        self._sqlite.execute(CANDLE_TABLE_SQL)

        for index_sql in CANDLE_INDEXES:
            self._sqlite.execute(index_sql)

    # ---------------------------------------------------------

    def _create_indexes(self):

        self._sqlite.execute(
            f"""
            CREATE INDEX IF NOT EXISTS
            idx_security_interval
            ON {self.TABLE_NAME}
            (
                security_id,
                interval
            )
            """
        )

        self._sqlite.execute(
            f"""
            CREATE INDEX IF NOT EXISTS
            idx_candle_time
            ON {self.TABLE_NAME}
            (
                candle_time
            )
            """
        )

    # ---------------------------------------------------------

    def upsert(self, candle: Candle):
        sql = f"""
        INSERT INTO {self.TABLE_NAME}
        (
            security_id,
            interval,
            candle_time,
            open,
            high,
            low,
            close,
            volume
        )
        VALUES
        (
            ?,?,?,?,?,?,?,?
        )

        ON CONFLICT
        (
            security_id,
            interval,
            candle_time
        )

        DO UPDATE SET

            high=excluded.high,
            low=excluded.low,
            close=excluded.close,
            volume=excluded.volume
        """

        self._sqlite.execute(
            sql,
            (
                candle.security_id,
                candle.interval.value,
                self._to_epoch_ms(candle.candle_time),
                float(candle.open),
                float(candle.high),
                float(candle.low),
                float(candle.close),
                candle.volume,
            ),
        )

    # ---------------------------------------------------------

    def insert_many(self, candles: list[Candle]):
        sql = f"""
        INSERT INTO {self.TABLE_NAME}
        (
            security_id,
            interval,
            candle_time,
            open,
            high,
            low,
            close,
            volume
        )
        VALUES
        (
            ?,?,?,?,?,?,?,?
        )
        """

        rows = [
            (
                candle.security_id,
                candle.interval.value,
                self._to_epoch_ms(candle.candle_time),
                float(candle.open),
                float(candle.high),
                float(candle.low),
                float(candle.close),
                candle.volume,
            )
            for candle in candles
        ]

        self._sqlite.executemany(sql, rows)

    # ---------------------------------------------------------

    def latest(
        self,
        security_id,
        interval,
    ):

        sql = f"""
        SELECT *

        FROM {self.TABLE_NAME}

        WHERE

            security_id=?
            AND interval=?

        ORDER BY candle_time DESC

        LIMIT 1
        """

        rows = self._sqlite.query(
            sql,
            (
                security_id,
                interval.value,
            ),
        )

        if not rows:
            return None

        return self._row_to_candle(rows[0])

    # ---------------------------------------------------------

    def history(
            self,
            security_id,
            interval,
            limit=100,
    ):

        sql = f"""
        SELECT *

        FROM {self.TABLE_NAME}

        WHERE

            security_id=?
            AND interval=?

        ORDER BY candle_time DESC

        LIMIT ?
        """

        rows = self._sqlite.query(
            sql,
            (
                security_id,
                interval.value,
                limit,
            ),
        )

        return [self._row_to_candle(row) for row in rows]

    # ---------------------------------------------------------

    def delete_all(self):

        self._sqlite.execute(
            f"DELETE FROM {self.TABLE_NAME}"
        )

    @staticmethod
    def _to_epoch_ms(dt: datetime) -> int:
        return int(dt.astimezone(timezone.utc).timestamp() * 1000)

    @staticmethod
    def _from_epoch_ms(epoch_ms: int) -> datetime:
        return datetime.fromtimestamp(epoch_ms / 1000, tz=timezone.utc)

    def _row_to_candle(self, row) -> Candle:
        return Candle(
            security_id=row["security_id"],
            interval=CandleInterval(row["interval"]),
            candle_time=self._from_epoch_ms(row["candle_time"]),
            open=Decimal(str(row["open"])),
            high=Decimal(str(row["high"])),
            low=Decimal(str(row["low"])),
            close=Decimal(str(row["close"])),
            volume=row["volume"],
        )