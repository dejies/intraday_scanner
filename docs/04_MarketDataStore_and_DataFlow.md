# 04_MarketDataStore_and_DataFlow.md

# MarketDataStore and Data Flow

## Overview

The `MarketDataStore` is the central runtime repository of the
application. It acts as the single source of truth for all live market
information, allowing every module to work from a consistent in-memory
state.

Rather than each component maintaining its own copy of market data, all
runtime information flows through the MarketDataStore.

------------------------------------------------------------------------

# Responsibilities

The MarketDataStore is responsible for maintaining:

-   Latest market tick for each subscribed security
-   Current in-progress candle
-   Recently completed candles
-   Latest calculated indicators
-   Active BUY/SELL signals
-   Ranked opportunities
-   Runtime metadata required by downstream components

It does **not** calculate indicators, evaluate strategies, or update the
UI directly.

------------------------------------------------------------------------

# Why a Central Store?

Without a shared runtime store:

-   Each module would duplicate state.
-   Synchronization would become difficult.
-   Components could observe inconsistent market data.
-   Thread-safety would be harder to maintain.

Using a single shared store ensures every module works with the same
snapshot of the market.

------------------------------------------------------------------------

# Data Flow

``` text
WebSocket Tick
      │
      ▼
Tick Processor
      │
      ▼
MarketDataStore
 ┌────────┼─────────┐
 ▼        ▼         ▼
Dashboard Candle   Scanner
          │
          ▼
Indicator Engine
          │
          ▼
Strategy Engine
          │
          ▼
Analysis & Ranking
```

------------------------------------------------------------------------

# Typical Lifecycle

1.  A live tick arrives from the Dhan WebSocket.
2.  The Tick Processor validates and normalizes it.
3.  The latest tick is written to the MarketDataStore.
4.  The Candle Builder updates the current OHLC candle.
5.  On candle completion, indicators are recalculated.
6.  Strategies evaluate the latest market state.
7.  Ranked signals are written back into the store.
8.  The Dashboard reads the updated state and refreshes incrementally.

------------------------------------------------------------------------

# Information Stored

Typical runtime objects include:

  Category    Purpose
  ----------- --------------------------------------
  Tick        Latest price and volume
  Candle      Current and historical OHLC data
  Indicator   EMA, RSI, MACD, ADX, ATR, VWAP, RVOL
  Signal      Active BUY or SELL recommendation
  Ranking     Confidence and priority information

------------------------------------------------------------------------

# Interaction with Major Modules

## WebSocket Client

Writes incoming market ticks.

## Candle Builder

Reads live ticks and updates active candles.

## Indicator Engine

Reads completed candles and stores calculated indicators.

## Strategy Engine

Reads indicators and publishes candidate signals.

## Analysis Engine

Consumes candidate signals and stores validated results.

## Ranking Engine

Updates ranked opportunities.

## Dashboard

Reads only. It never owns business data.

------------------------------------------------------------------------

# Thread Safety

The application processes live market data continuously while the
dashboard refreshes independently.

The MarketDataStore provides a controlled location for shared runtime
state, reducing the risk of inconsistent reads and writes across
components.

------------------------------------------------------------------------

# Benefits

-   Single source of truth
-   Reduced duplication
-   Easier debugging
-   Simpler testing
-   Cleaner module boundaries
-   Scalable architecture

------------------------------------------------------------------------

# Next Document

The next document explains the Candle Engine, including how ticks are
aggregated into one-minute OHLC candles and how completed candles
trigger downstream processing.
