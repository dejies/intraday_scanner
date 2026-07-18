# 05_Candle_Engine.md

# Candle Engine

## Overview

The Candle Engine is responsible for converting the continuous stream of
live market ticks into structured OHLC (Open, High, Low, Close) candles.
These candles become the foundation for all technical indicator
calculations and trading decisions.

Unlike ticks, which arrive irregularly and in high volume, candles
provide a standardized representation of price action over a fixed time
interval.

------------------------------------------------------------------------

# Responsibilities

The Candle Engine performs the following tasks:

-   Receive validated ticks
-   Maintain the active one-minute candle
-   Update Open, High, Low, Close values
-   Aggregate traded volume
-   Detect candle completion
-   Persist completed candles
-   Trigger downstream indicator calculations

------------------------------------------------------------------------

# Why Candles?

Technical indicators such as EMA, RSI, MACD, and ADX rely on completed
OHLC candles rather than raw tick data.

Using completed candles provides:

-   Stable calculations
-   Noise reduction
-   Consistent analysis intervals
-   Standardized historical records

------------------------------------------------------------------------

# Candle Lifecycle

``` text
Live Tick
    │
    ▼
Locate Current Minute
    │
    ▼
Existing Candle?
 ┌───────┴────────┐
 │                │
Yes              No
 │                │
 ▼                ▼
Update OHLC   Create Candle
 │                │
 └───────┬────────┘
         ▼
Minute Changed?
     │
 ┌───┴────┐
 │        │
No       Yes
 │        │
 ▼        ▼
Wait   Finalize Candle
            │
            ▼
Persist SQLite
            │
            ▼
Indicator Engine
```

------------------------------------------------------------------------

# OHLC Construction

For every incoming tick:

## Open

The first traded price received for the minute.

## High

The highest traded price observed during the minute.

## Low

The lowest traded price observed during the minute.

## Close

The most recent traded price.

## Volume

The cumulative traded volume for that candle.

------------------------------------------------------------------------

# Minute Transition

When a tick belongs to a new minute:

1.  Finalize the existing candle.
2.  Store it in SQLite.
3.  Publish the completed candle.
4.  Create a fresh candle for the new minute.

This guarantees that only completed candles are used for downstream
analysis.

------------------------------------------------------------------------

# Interaction with Other Modules

## Tick Processor

Supplies validated market ticks.

## MarketDataStore

Stores the active and completed candles.

## Indicator Engine

Receives each completed candle and recalculates technical indicators.

## SQLite Repository

Persists completed candle history.

------------------------------------------------------------------------

# Persistence

Each completed candle is written to the database with fields such as:

-   Security ID
-   Timestamp
-   Open
-   High
-   Low
-   Close
-   Volume

Historical candles form the basis for indicator calculations and future
backtesting.

------------------------------------------------------------------------

# Benefits

-   Converts noisy tick streams into meaningful price data.
-   Produces standardized market history.
-   Enables reliable indicator computation.
-   Decouples live market feed from analytical logic.
-   Supports historical replay and testing.

------------------------------------------------------------------------

# Runtime Sequence

``` text
Market Tick
     │
     ▼
Tick Processor
     │
     ▼
Candle Builder
     │
     ▼
Update Active Candle
     │
     ▼
Minute Complete?
     │
 ┌───┴────┐
 │        │
No       Yes
 │        │
 ▼        ▼
Continue Finalize Candle
            │
            ▼
SQLite
            │
            ▼
Indicator Engine
```

------------------------------------------------------------------------

# Design Considerations

-   Uses completed candles rather than partial candles for calculations.
-   Keeps candle creation isolated from business logic.
-   Avoids duplicate candle generation.
-   Supports future expansion to additional timeframes.

------------------------------------------------------------------------

# Next Document

The next document explains the Indicator Engine, covering the
calculation and role of EMA, RSI, MACD, ADX, ATR, VWAP, Relative Volume,
and how these indicators influence BUY and SELL decisions.
