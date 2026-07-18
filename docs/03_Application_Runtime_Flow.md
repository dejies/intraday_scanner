# 03_Application_Runtime_Flow.md

# Application Runtime Flow

## Overview

This document explains how the application executes from startup until a
BUY or SELL signal is displayed on the dashboard.

The runtime is event-driven. Every stage is triggered by the completion
of the previous stage.

------------------------------------------------------------------------

# Startup Sequence

``` text
Application Start
        │
        ▼
Load Configuration
        │
        ▼
Initialize SQLite
        │
        ▼
Create Repositories
        │
        ▼
Create Services
        │
        ▼
Initialize MarketDataStore
        │
        ▼
Create Dashboard
        │
        ▼
Start WebSocket Client
        │
        ▼
Subscribe to Securities
        │
        ▼
Wait for Market Data
```

------------------------------------------------------------------------

# Tick Processing Pipeline

Every market tick follows the same execution path.

``` text
Market Tick
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
Dashboard Tick Update
     │
     ▼
Candle Builder
```

The tick processor validates incoming data before updating the runtime
state.

------------------------------------------------------------------------

# Candle Building

The Candle Builder continuously updates the current one-minute candle.

For every incoming tick:

1.  Update Open (first tick only)
2.  Update High
3.  Update Low
4.  Update Close
5.  Update Volume

When the minute changes:

-   Finalize the candle
-   Store in SQLite
-   Publish completed candle

------------------------------------------------------------------------

# Indicator Calculation Flow

Each completed candle triggers indicator recalculation.

``` text
Completed Candle
      │
      ▼
EMA
RSI
MACD
ADX
ATR
VWAP
RVOL
      │
      ▼
Indicator Repository
      │
      ▼
MarketDataStore
```

Only completed candles are used for calculations, preventing unstable
indicator values.

------------------------------------------------------------------------

# Strategy Evaluation

After indicators are updated, every enabled strategy is evaluated
independently.

Typical workflow:

1.  Read latest indicators
2.  Check entry conditions
3.  Generate BUY or SELL candidate
4.  Store candidate signal

Multiple strategies may produce signals simultaneously.

------------------------------------------------------------------------

# Analysis Stage

Candidate signals are not shown immediately.

The Analysis Engine validates them using additional confirmations such
as:

-   Trend strength
-   Momentum
-   Volume participation
-   Volatility
-   Price position

Signals failing validation are discarded.

------------------------------------------------------------------------

# Dynamic Scoring

Validated signals receive a confidence score.

Typical scoring factors include:

-   EMA alignment
-   RSI position
-   MACD agreement
-   ADX strength
-   VWAP confirmation
-   Relative Volume
-   ATR
-   Strategy-specific bonuses

The final score represents overall signal quality.

------------------------------------------------------------------------

# Ranking

All active signals are sorted.

Priority order:

1.  Confidence
2.  Score
3.  Strategy quality

Only the highest-ranked opportunities appear at the top of the
dashboard.

------------------------------------------------------------------------

# Dashboard Refresh

The dashboard performs incremental updates.

It:

-   Adds new rows
-   Updates existing rows
-   Removes expired signals
-   Preserves user sorting
-   Preserves row selection

The entire table is never rebuilt unless necessary.

------------------------------------------------------------------------

# Alert Generation

Whenever a new qualified signal appears:

1.  Check duplicate history
2.  Format alert
3.  Persist alert
4.  Display notification

Duplicate alerts are intentionally suppressed.

------------------------------------------------------------------------

# Persistence

Throughout runtime, SQLite stores:

-   Candles
-   Indicators
-   Signals
-   Alerts

Historical data remains available for future analysis and backtesting.

------------------------------------------------------------------------

# End-to-End Execution Summary

``` text
Application
   ↓
WebSocket
   ↓
Tick
   ↓
MarketDataStore
   ↓
Candle Builder
   ↓
Indicator Engine
   ↓
Strategy Engine
   ↓
Analysis Engine
   ↓
Dynamic Scoring
   ↓
Ranking Engine
   ↓
Dashboard
   ↓
Alert Engine
   ↓
SQLite
```

------------------------------------------------------------------------

# Next Document

The next document focuses exclusively on the **MarketDataStore**,
explaining how runtime state is managed and shared safely between all
major components.
