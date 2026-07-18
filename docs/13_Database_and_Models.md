# 13_Database_and_Models.md

# Database and Domain Models

## Overview

The persistence layer stores historical and runtime-derived information
in SQLite while exposing a clean Repository API to the rest of the
application. Business logic never interacts with SQL directly; instead,
repositories encapsulate all database operations.

------------------------------------------------------------------------

# Responsibilities

The database layer is responsible for:

-   Persisting completed candles
-   Persisting calculated indicators
-   Persisting generated signals
-   Persisting alert history
-   Providing historical data for indicator calculations
-   Supporting future backtesting

------------------------------------------------------------------------

# Architecture

``` text
Business Layer
      │
      ▼
Repositories
      │
      ▼
SQLite Manager
      │
      ▼
SQLite Database
```

Repositories act as the only gateway between business logic and
persistent storage.

------------------------------------------------------------------------

# Repository Pattern

Each repository owns a specific data type.

Typical repositories include:

-   Candle Repository
-   Indicator Repository
-   Signal Repository
-   Alert Repository

Responsibilities:

-   Insert records
-   Read records
-   Update records (where applicable)
-   Hide SQL implementation details

------------------------------------------------------------------------

# Domain Models

Domain models represent business objects used throughout the
application.

Typical models include:

  Model           Purpose
  --------------- ------------------------------
  Tick            Latest market update
  Candle          OHLC market data
  Indicator       Technical indicator values
  Signal          BUY / SELL candidate
  Ranked Signal   Signal with ranking metadata
  Alert           User notification

These models travel between modules without exposing persistence
details.

------------------------------------------------------------------------

# Persistence Flow

``` text
Runtime Object
      │
      ▼
Repository
      │
      ▼
SQLite Manager
      │
      ▼
SQLite Database
```

Reading data follows the reverse path.

------------------------------------------------------------------------

# Candle Persistence

Completed candles are stored with information such as:

-   Security ID
-   Timestamp
-   Open
-   High
-   Low
-   Close
-   Volume

Historical candles are later reused for indicator calculations.

------------------------------------------------------------------------

# Indicator Persistence

Each completed indicator calculation is stored.

Typical values include:

-   EMA
-   RSI
-   MACD
-   ADX
-   ATR
-   VWAP
-   Relative Volume

Persisting indicators enables historical analysis and simplifies
debugging.

------------------------------------------------------------------------

# Signal Persistence

Signals may include:

-   Security ID
-   Signal type
-   Strategy
-   Signal price
-   Confidence
-   Timestamp
-   Analysis facts

These records provide a history of generated opportunities.

------------------------------------------------------------------------

# Alert Persistence

Alerts are stored to:

-   Prevent duplicates
-   Maintain notification history
-   Support auditing
-   Enable future reporting

------------------------------------------------------------------------

# SQLite Manager

The SQLite Manager centralizes:

-   Connection management
-   Transaction handling
-   Database initialization
-   Schema creation

Repositories reuse this manager instead of opening independent
connections.

------------------------------------------------------------------------

# Benefits of the Repository Pattern

-   SQL isolated from business logic
-   Easier testing
-   Cleaner architecture
-   Future database portability
-   Consistent data access

------------------------------------------------------------------------

# Module Interaction

``` text
Candle Engine
      │
      ▼
Candle Repository
      │
      ▼
SQLite

Indicator Engine
      │
      ▼
Indicator Repository
      │
      ▼
SQLite

Alert Engine
      │
      ▼
Alert Repository
      │
      ▼
SQLite
```

------------------------------------------------------------------------

# Design Principles

-   Separation of persistence and business logic
-   Strong domain model boundaries
-   Repository abstraction
-   Reusable database manager
-   Historical data retention

------------------------------------------------------------------------

# Next Document

The next document explains threading and concurrency, including how the
application safely processes live market data while keeping the
dashboard responsive.
