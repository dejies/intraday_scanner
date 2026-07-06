# PROJECT_DEVELOPER_GUIDE.md

## Intraday Scanner -- Developer Guide

> **Purpose:** This document is the single source of truth for
> developers and AI assistants (Claude, ChatGPT, Gemini, Copilot, etc.)
> working on this project.

------------------------------------------------------------------------

# 1. Project Overview

## Project Name

**Intraday Scanner**

## Objective

A lightweight Python application for scanning the Indian stock market in
real time using the DhanHQ API.

The scanner is intended for **manual intraday trading**. It generates
trading signals based on technical indicators and predefined strategies.

**Version:** 1.0

**Architecture Status:** **LOCKED**

------------------------------------------------------------------------

# 2. Design Philosophy

-   Keep the project simple.
-   Avoid over-engineering.
-   One responsibility per module.
-   Readability is more important than cleverness.
-   Prefer modifying existing files over creating new ones.
-   No unnecessary architectural patterns.
-   Suitable for personal use and future enhancements.

------------------------------------------------------------------------

# 3. Locked Project Structure

``` text
src/
│
├── core/
│   ├── config.py
│   ├── constants.py
│   ├── exceptions.py
│   └── logger.py
│
├── models/
│   ├── candle.py
│   ├── signal.py
│   └── stock.py
│
├── services/
│   ├── base_service.py
│   ├── dhan_context.py
│   ├── market_data.py
│   ├── notifier.py
│   ├── watchlist.py
│   └── websocket_client.py
│
├── scanners/
│   ├── trend.py
│   ├── breakout.py
│   └── volume.py
│
├── indicators.py
├── scanner.py
├── ranking.py
├── dashboard.py
└── main.py
```

> **Do not add new folders or modules without explicit approval.**

------------------------------------------------------------------------

# 4. Module Responsibilities

## core/config.py

**Purpose** - Load application configuration. - Read `.env`. - Validate
mandatory settings.

**Inputs** - Environment variables

**Outputs** - Settings object

**Must NOT** - Connect to Dhan - Perform business logic

------------------------------------------------------------------------

## core/logger.py

**Purpose** - Configure logging.

**Responsibilities** - Console logging - File logging - Log formatting

**Must NOT** - Contain business logic

------------------------------------------------------------------------

## core/constants.py

**Purpose** - Store project constants.

Examples: - Strategy names - Signal types - Default periods - Threshold
values

------------------------------------------------------------------------

## core/exceptions.py

**Purpose** - Store custom exceptions.

Examples: - ConfigurationError - DhanConnectionError - WatchlistError

------------------------------------------------------------------------

## models/stock.py

Represents one stock.

Fields: - Symbol - Exchange - Security ID - Enabled

Business logic is **not allowed**.

------------------------------------------------------------------------

## models/candle.py

Represents one OHLCV candle.

Fields: - Timestamp - Open - High - Low - Close - Volume

Business logic is **not allowed**.

------------------------------------------------------------------------

## models/signal.py

Represents one trading signal.

Fields: - Symbol - Strategy - BUY / SELL - Price - Confidence -
Timestamp - Message

------------------------------------------------------------------------

## services/base_service.py

Common parent class.

Provides: - Logger - Configuration - Shared initialization

------------------------------------------------------------------------

## services/watchlist.py

Purpose: - Load watchlist CSV - Validate entries - Return enabled stocks

Must NOT: - Connect to Dhan - Generate signals

------------------------------------------------------------------------

## services/market_data.py

Purpose: - Store completed candle data - Return candle history -
Thread-safe access

Acts as the application's in-memory market cache.

Must NOT: - Calculate indicators - Generate signals - Connect to Dhan

------------------------------------------------------------------------

## services/dhan_context.py

Purpose: - Authenticate with Dhan - Create and maintain Dhan context

Must NOT: - Generate trading signals

------------------------------------------------------------------------

## services/websocket_client.py

Purpose: - Connect to Dhan WebSocket - Subscribe to watchlist - Receive
live ticks

Must NOT: - Calculate indicators - Rank signals - Display dashboard

------------------------------------------------------------------------

## services/notifier.py

Reserved for notifications.

Future: - Telegram - Email - Push notifications

------------------------------------------------------------------------

## indicators.py

Purpose: - Technical indicator calculations.

Implemented: - SMA - EMA - RSI - VWAP - Highest High - Lowest Low -
Average Volume

Input: - list\[Candle\]

Output: - Indicator values

Must NOT: - Generate BUY/SELL signals

------------------------------------------------------------------------

## scanner.py

Purpose: - Execute all scanners - Collect signals

Must NOT: - Implement indicator calculations directly

------------------------------------------------------------------------

## scanners/trend.py

BUY: - EMA20 \> EMA50 - Price \> VWAP - RSI \> 55

SELL: - EMA20 \< EMA50 - Price \< VWAP - RSI \< 45

------------------------------------------------------------------------

## scanners/breakout.py

BUY: - Close above previous 20-candle high - Volume \> 1.5 × average
volume

SELL: - Close below previous 20-candle low - Volume \> 1.5 × average
volume

------------------------------------------------------------------------

## scanners/volume.py

BUY: - Bullish candle - Volume \> 2 × average volume - Close \> previous
close

SELL: - Bearish candle - Volume \> 2 × average volume - Close \<
previous close

------------------------------------------------------------------------

## ranking.py

Purpose: - Remove duplicate signals - Sort by confidence

Input: - list\[Signal\]

Output: - Ranked list

------------------------------------------------------------------------

## dashboard.py

Purpose: - Display ranked signals

Responsibilities: - Format output - Print console dashboard

Must NOT: - Generate signals

------------------------------------------------------------------------

## main.py

Purpose: - Application entry point

Responsibilities: 1. Load configuration 2. Load watchlist 3.
Authenticate 4. Connect WebSocket 5. Update MarketData 6. Execute
scanner 7. Rank signals 8. Display dashboard

Business logic should remain in the appropriate modules.

------------------------------------------------------------------------

# 5. Data Flow

``` text
Watchlist
    │
    ▼
Dhan Authentication
    │
    ▼
WebSocket
    │
    ▼
MarketData
    │
    ▼
Indicators
    │
    ▼
Scanner
    │
    ▼
Trend / Breakout / Volume
    │
    ▼
Ranking
    │
    ▼
Dashboard
```

------------------------------------------------------------------------

# 6. Coding Standards

-   Python 3.12+
-   PEP 8
-   Type hints
-   Dataclasses where appropriate
-   Logger instead of print statements (except test files)
-   One responsibility per module
-   Reuse existing code
-   Avoid duplicate logic
-   Keep methods readable

------------------------------------------------------------------------

# 7. AI Development Rules

Before making changes:

1.  Read this document.
2.  Review the current implementation.
3.  Do not change the architecture.
4.  Do not rename files.
5.  Do not create new folders.
6.  Prefer modifying existing modules.
7.  Preserve coding style.
8.  Provide tests for new functionality.
9.  Ask before making structural changes.

------------------------------------------------------------------------

# 8. Current Project Status

  Module                 Status
  ---------------------- ---------
  Foundation             ✅
  Models                 ✅
  Services               ✅
  Indicators             ✅
  Trend Scanner          ✅
  Breakout Scanner       ✅
  Volume Scanner         ✅
  Ranking                ✅
  Dashboard              ✅
  WebSocket Connection   ✅
  Live Tick Processing   Pending
  Main Integration       Pending
  Notifications          Pending

------------------------------------------------------------------------

# 9. Future Enhancements

-   Telegram notifications
-   Historical data loading
-   SQLite storage
-   Backtesting
-   Multi-timeframe analysis
-   Strategy configuration
-   Performance analytics

------------------------------------------------------------------------

# 10. Final Notes

This architecture is intentionally simple.

The goal is to complete a reliable intraday scanner before introducing
additional features.

All future development should preserve the existing structure and extend
functionality incrementally.
