"""
Thread-safe SQLite manager.

Responsibilities
----------------
- Open SQLite database
- Create database if missing
- Execute SQL
- Execute many
- Transactions
- Thread-safe access

This class knows NOTHING about candles.
"""

from __future__ import annotations

import sqlite3
import threading
from pathlib import Path
from typing import Iterable, Optional


class SQLiteManager:
    """
    Thread-safe SQLite wrapper.
    """

    def __init__(self, database_path: str):
        self._database_path = Path(database_path)
        self._database_path.parent.mkdir(parents=True, exist_ok=True)

        self._lock = threading.RLock()

        self._connection = sqlite3.connect(
            self._database_path,
            check_same_thread=False
        )

        self._connection.row_factory = sqlite3.Row

        self._enable_pragmas()

    # ------------------------------------------------------------------

    def _enable_pragmas(self):
        """
        Configure SQLite for better performance.
        """

        with self._lock:
            cursor = self._connection.cursor()

            cursor.execute("PRAGMA journal_mode=WAL")
            cursor.execute("PRAGMA synchronous=NORMAL")
            cursor.execute("PRAGMA temp_store=MEMORY")
            cursor.execute("PRAGMA foreign_keys=ON")

            self._connection.commit()

    # ------------------------------------------------------------------

    def execute(
        self,
        sql: str,
        parameters: Optional[tuple] = None,
    ):
        """
        Execute a single SQL statement.
        """

        with self._lock:
            cursor = self._connection.cursor()

            if parameters:
                cursor.execute(sql, parameters)
            else:
                cursor.execute(sql)

            self._connection.commit()

            return cursor

    # ------------------------------------------------------------------

    def executemany(
        self,
        sql: str,
        parameters: Iterable[tuple],
    ):
        """
        Execute many SQL statements.
        """

        with self._lock:
            cursor = self._connection.cursor()

            cursor.executemany(sql, parameters)

            self._connection.commit()

            return cursor

    # ------------------------------------------------------------------

    def query(
        self,
        sql: str,
        parameters: Optional[tuple] = None,
    ):
        """
        Execute SELECT query.
        """

        with self._lock:
            cursor = self._connection.cursor()

            if parameters:
                cursor.execute(sql, parameters)
            else:
                cursor.execute(sql)

            return cursor.fetchall()

    # ------------------------------------------------------------------

    def begin(self):
        with self._lock:
            self._connection.execute("BEGIN")

    # ------------------------------------------------------------------

    def commit(self):
        with self._lock:
            self._connection.commit()

    # ------------------------------------------------------------------

    def rollback(self):
        with self._lock:
            self._connection.rollback()

    # ------------------------------------------------------------------

    def close(self):
        with self._lock:
            self._connection.close()