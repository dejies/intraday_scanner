# 15_End_to_End_Trade_Lifecycle.md

# End-to-End Trade Lifecycle

## Overview

This document describes the complete lifecycle of a trading opportunity,
beginning with a live market tick and ending with a ranked BUY or SELL
signal displayed on the dashboard and stored in the database.

Understanding this workflow helps developers trace data movement through
every major component of the application.

------------------------------------------------------------------------

# Complete Lifecycle

``` text
Dhan Market Feed
        │
        ▼
WebSocket Client
        │
        ▼
Tick Processor
        │
        ▼
MarketDataStore
        │
        ▼
Candle Builder
        │
        ▼
Completed Candle
        │
        ▼
Indicator Engine
        │
        ▼
Strategy Engine
        │
        ▼
Candidate Signal
        │
        ▼
Analysis Engine
        │
        ▼
Dynamic Scoring
        │
        ▼
Ranking Engine
      ┌─┴─────────────┐
      ▼               ▼
Dashboard      Alert Engine
      │               │
      └──────┬────────┘
             ▼
         SQLite Database
```

------------------------------------------------------------------------

# Step 1 -- Market Data Arrival

The lifecycle begins when the Dhan WebSocket delivers a live market
tick.

The WebSocket layer is responsible only for:

-   Receiving data
-   Maintaining connectivity
-   Forwarding ticks

No business logic is performed here.

------------------------------------------------------------------------

# Step 2 -- Tick Processing

Each incoming tick is:

-   Validated
-   Normalized
-   Converted into the application's internal model

The processed tick is then written to the MarketDataStore.

------------------------------------------------------------------------

# Step 3 -- Runtime State Update

The MarketDataStore immediately reflects the latest market state.

Updated information may include:

-   Latest price
-   Latest volume
-   Timestamp
-   Active candle reference

Every downstream component now observes the updated market state.

------------------------------------------------------------------------

# Step 4 -- Candle Construction

The Candle Engine updates the current one-minute OHLC candle.

If the minute changes:

1.  Finalize the candle.
2.  Persist it to SQLite.
3.  Trigger indicator calculations.

------------------------------------------------------------------------

# Step 5 -- Indicator Calculation

Using completed candles, the Indicator Engine calculates:

-   EMA
-   RSI
-   MACD
-   ADX
-   ATR
-   VWAP
-   Relative Volume

Calculated indicators are:

-   Stored in SQLite
-   Published to the MarketDataStore

------------------------------------------------------------------------

# Step 6 -- Strategy Evaluation

Each enabled strategy independently evaluates the latest market state.

Possible outcomes:

-   No opportunity
-   BUY candidate
-   SELL candidate

Only candidate signals are produced at this stage.

------------------------------------------------------------------------

# Step 7 -- Analysis

The Analysis Engine validates each candidate using multiple
confirmations.

Typical checks include:

-   Trend
-   Momentum
-   Volume
-   Volatility
-   Price location

Weak opportunities are discarded.

------------------------------------------------------------------------

# Step 8 -- Dynamic Scoring

Validated signals receive a confidence score.

Factors include:

-   EMA alignment
-   RSI
-   MACD
-   ADX
-   ATR
-   VWAP
-   Relative Volume
-   Strategy-specific rules

Higher confirmation produces higher confidence.

------------------------------------------------------------------------

# Step 9 -- Ranking

Signals are grouped into:

-   BUY
-   SELL

Each group is independently sorted so that the strongest opportunities
appear first.

------------------------------------------------------------------------

# Step 10 -- Dashboard Update

The Dashboard performs an incremental refresh.

Operations include:

-   Add new signals
-   Update existing signals
-   Remove expired signals
-   Preserve sorting
-   Preserve row selection

The user immediately sees the latest ranked opportunities.

------------------------------------------------------------------------

# Step 11 -- Alert Generation

The Alert Engine examines ranked signals.

If a signal has not previously been notified:

1.  Format alert
2.  Store alert
3.  Notify user

Duplicate alerts are intentionally suppressed.

------------------------------------------------------------------------

# Step 12 -- Persistence

Throughout the lifecycle, SQLite stores:

-   Completed candles
-   Indicators
-   Signals
-   Alerts

Historical information becomes available for future analysis and
backtesting.

------------------------------------------------------------------------

# Lifecycle Summary

``` text
Tick
 │
 ▼
MarketDataStore
 │
 ▼
Candle
 │
 ▼
Indicators
 │
 ▼
Strategies
 │
 ▼
Analysis
 │
 ▼
Confidence
 │
 ▼
Ranking
 │
 ├────────► Dashboard
 │
 ├────────► Alerts
 │
 └────────► SQLite
```

------------------------------------------------------------------------

# Architectural Benefits

-   Modular execution
-   Clear separation of responsibilities
-   Deterministic processing pipeline
-   Minimal coupling
-   High maintainability
-   Easy debugging
-   Future backtesting support

------------------------------------------------------------------------

# Next Document

The final document concludes the documentation set with deployment
guidance, extension points, coding conventions, and future enhancement
recommendations.
