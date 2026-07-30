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

This class knows NOTHING about repositories.
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
        self._database_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self._lock = threading.RLock()

        self._connection = sqlite3.connect(
            self._database_path,
            check_same_thread=False,
        )

        self._connection.row_factory = sqlite3.Row

        #
        # Tracks whether a manual transaction is active.
        #
        self._in_transaction = False

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

            #
            # Auto commit only if not inside
            # an explicit transaction.
            #
            if not self._in_transaction:
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

            cursor.executemany(
                sql,
                parameters,
            )

            if not self._in_transaction:
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
        """
        Begin an explicit transaction.
        """

        with self._lock:

            if self._in_transaction:
                raise RuntimeError(
                    "Transaction already active."
                )

            self._connection.execute("BEGIN")

            self._in_transaction = True

    # ------------------------------------------------------------------

    def commit(self):
        """
        Commit the current transaction.
        """

        with self._lock:

            if not self._in_transaction:
                return

            self._connection.commit()

            self._in_transaction = False

    # ------------------------------------------------------------------

    def rollback(self):
        """
        Roll back the current transaction.
        """

        with self._lock:

            if not self._in_transaction:
                return

            self._connection.rollback()

            self._in_transaction = False

    # ------------------------------------------------------------------

    @property
    def in_transaction(self) -> bool:
        """
        Returns True if an explicit transaction is active.
        """

        return self._in_transaction

    # ------------------------------------------------------------------

    def close(self):
        """
        Close the database connection.
        """

        with self._lock:

            #
            # Never leave an open transaction.
            #
            if self._in_transaction:
                self._connection.rollback()
                self._in_transaction = False

            self._connection.close()