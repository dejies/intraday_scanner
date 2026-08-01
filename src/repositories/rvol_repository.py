from models.rvol_data import RVOLData


class RVOLRepository:
    """
    Repository responsible for persisting and retrieving
    Relative Volume (RVOL) data.

    The repository never performs RVOL calculations.
    It only interacts with SQLite.
    """

    def __init__(self, sqlite_manager):
        self._sqlite = sqlite_manager

    def save(self, rvol: RVOLData) -> None:
        """
        Insert or replace an RVOL record.
        """

        cursor = self._sqlite.connection.cursor()

        cursor.execute(
            """
            INSERT OR REPLACE INTO rvol (
                symbol,
                timestamp,
                current_volume,
                average_volume,
                rvol,
                classification
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                rvol.symbol,
                rvol.timestamp.isoformat(),
                rvol.current_volume,
                rvol.average_volume,
                rvol.rvol,
                rvol.classification,
            ),
        )

        self._sqlite.connection.commit()

    def get_latest(self, symbol: str):
        """
        Returns the latest RVOL record for a symbol.
        """

        cursor = self._sqlite.connection.cursor()

        cursor.execute(
            """
            SELECT
                symbol,
                timestamp,
                current_volume,
                average_volume,
                rvol,
                classification
            FROM rvol
            WHERE symbol=?
            ORDER BY timestamp DESC
            LIMIT 1
            """,
            (symbol,),
        )

        return cursor.fetchone()

    def get_history(self, symbol: str, limit: int = 20):
        """
        Returns historical RVOL records ordered newest first.
        """

        cursor = self._sqlite.connection.cursor()

        cursor.execute(
            """
            SELECT
                symbol,
                timestamp,
                current_volume,
                average_volume,
                rvol,
                classification
            FROM rvol
            WHERE symbol=?
            ORDER BY timestamp DESC
            LIMIT ?
            """,
            (symbol, limit),
        )

        return cursor.fetchall()