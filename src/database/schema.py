"""
Database schema definitions.
"""

# ----------------------------------------------------------------------
# Tables
# ----------------------------------------------------------------------

TABLES = [
    """
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
    );
    """,
"""
CREATE TABLE IF NOT EXISTS universe
(
    symbol              TEXT PRIMARY KEY,

    company_name        TEXT NOT NULL,

    security_id         TEXT,

    exchange_segment    TEXT,

    index_name          TEXT NOT NULL,

    updated_at          INTEGER NOT NULL
)
""",
"""
CREATE TABLE IF NOT EXISTS universe_metadata
(
    key     TEXT PRIMARY KEY,
    value   TEXT NOT NULL
)
""",
    """
    CREATE TABLE IF NOT EXISTS indicators
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT,

        security_id INTEGER NOT NULL,

        timeframe TEXT NOT NULL,

        indicator TEXT NOT NULL,

        candle_time TEXT NOT NULL,

        value REAL NOT NULL,

        UNIQUE
        (
            security_id,
            timeframe,
            indicator,
            candle_time
        )
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS universe_indices
    (
        symbol TEXT NOT NULL,
    
        index_name TEXT NOT NULL,
    
        PRIMARY KEY(symbol, index_name)
    )
    """,
]

# ----------------------------------------------------------------------
# Indexes
# ----------------------------------------------------------------------

INDEXES = [
    """
    CREATE INDEX IF NOT EXISTS idx_security_interval
    ON candles
    (
        security_id,
        interval
    );
    """,
    """
    CREATE INDEX IF NOT EXISTS idx_candle_time
    ON candles
    (
        candle_time
    );
    """,
    """
    CREATE INDEX IF NOT EXISTS idx_indicator_lookup
    ON indicators
    (
        security_id,
        timeframe,
        indicator,
        candle_time
    );
    """,
]