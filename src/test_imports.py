"""
Smoke test for Milestone 6 - Part 1

Verifies:
1. IndicatorType enum
2. IndicatorRecord model
3. SQLite schema creation
4. Indicators table exists
5. Index exists
"""

from datetime import datetime
import sqlite3
from database.schema import TABLES, INDEXES

from models.indicator_record import (
    IndicatorRecord,
    IndicatorType,
)
from database.sqlite_manager import SQLiteManager


def verify_indicator_model():
    print("Testing IndicatorRecord...")

    record = IndicatorRecord(
        security_id=1333,
        timeframe="1m",
        indicator=IndicatorType.EMA_20,
        candle_time=datetime.now(),
        value=2456.78,
    )

    assert record.security_id == 1333
    assert record.timeframe == "1m"
    assert record.indicator == IndicatorType.EMA_20
    assert record.value == 2456.78

    print("✓ IndicatorRecord OK")


def verify_database_schema():

    print("Testing SQLite schema...")

    db = SQLiteManager("src/data/test.db")



    #
    # Verify indicators table
    #
    rows = db.query(
        """
        SELECT name
        FROM sqlite_master
        WHERE type='table'
        AND name='indicators'
        """
    )

    assert len(rows) == 1

    print("✓ indicators table exists")

    #
    # Verify lookup index
    #
    rows = db.query(
        """
        SELECT name
        FROM sqlite_master
        WHERE type='index'
        AND name='idx_indicator_lookup'
        """
    )

    assert len(rows) == 1

    print("✓ indicator index exists")

    db.close()


def main():

    print("=" * 60)
    print("Milestone 6 - Part 1 Smoke Test")
    print("=" * 60)

    verify_indicator_model()
    verify_database_schema()

    print()
    print("=" * 60)
    print("✓ ALL TESTS PASSED")
    print("=" * 60)


if __name__ == "__main__":
    main()