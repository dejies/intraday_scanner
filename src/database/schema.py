"""
Database schema definitions.
"""

CANDLE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS candles
(
    security_id    TEXT NOT NULL,
    interval       TEXT NOT NULL,
    candle_time    INTEGER NOT NULL,

    open           REAL NOT NULL,
    high           REAL NOT NULL,
    low            REAL NOT NULL,
    close          REAL NOT NULL,

    volume         INTEGER NOT NULL,

    PRIMARY KEY
    (
        security_id,
        interval,
        candle_time
    )
)
"""

CANDLE_INDEXES = [
    """
    CREATE INDEX IF NOT EXISTS idx_security_interval
    ON candles
    (
        security_id,
        interval
    )
    """,
    """
    CREATE INDEX IF NOT EXISTS idx_candle_time
    ON candles
    (
        candle_time
    )
    """,
]