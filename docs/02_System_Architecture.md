# 02_System_Architecture.md

# System Architecture

## Architectural Philosophy

The application follows a layered architecture with clear separation of
responsibilities. Each layer performs a single task and communicates
through domain models and services rather than directly depending on
implementation details.

------------------------------------------------------------------------

# Layered Architecture

``` text
Presentation Layer
    │
    ▼
Dashboard (PySide6)
    │
    ▼
Scanner / Controller Layer
    │
    ▼
Analysis Layer
    │
    ▼
Strategy Layer
    │
    ▼
Indicator Layer
    │
    ▼
Candle Layer
    │
    ▼
MarketDataStore
    │
    ▼
Tick Processing
    │
    ▼
WebSocket Client
    │
    ▼
Dhan Market Feed
```

------------------------------------------------------------------------

# Component Responsibilities

## WebSocket Layer

Responsibilities:

-   Connect to Dhan Market Feed
-   Subscribe to securities
-   Receive live ticks
-   Handle reconnects
-   Forward ticks to the processing pipeline

This layer never performs business logic.

------------------------------------------------------------------------

## Tick Processor

Responsibilities:

-   Validate incoming ticks
-   Normalize values
-   Update runtime market state
-   Trigger downstream processing

------------------------------------------------------------------------

## MarketDataStore

The MarketDataStore is the runtime source of truth.

It maintains:

-   Latest tick
-   Active candle
-   Completed candles
-   Latest indicators
-   Active signals
-   Ranking information

Every major module reads from or writes to this shared state.

------------------------------------------------------------------------

## Candle Engine

Consumes live ticks and creates completed OHLC candles.

Each completed candle triggers:

1.  SQLite persistence
2.  Indicator calculation
3.  Strategy evaluation

------------------------------------------------------------------------

## Indicator Engine

Calculates technical indicators from completed candles.

Current indicator families include:

-   Trend
-   Momentum
-   Volume
-   Volatility

Indicators are stored in both memory and SQLite.

------------------------------------------------------------------------

## Strategy Engine

Each strategy evaluates the latest market state independently.

Examples include:

-   EMA Alignment
-   Pullback
-   Trend Continuation
-   Opening Range Breakout

Strategies generate candidate BUY or SELL signals.

------------------------------------------------------------------------

## Analysis Engine

The analysis layer verifies candidate signals using multiple
confirmations.

Typical checks include:

-   Trend confirmation
-   Momentum confirmation
-   Volume confirmation
-   Volatility confirmation

Only validated opportunities continue to scoring.

------------------------------------------------------------------------

## Dynamic Scoring

Each validated signal receives a confidence score based on weighted
factors.

Higher scores indicate stronger trading opportunities.

------------------------------------------------------------------------

## Ranking Engine

Ranks all active signals.

Sorting is primarily driven by:

-   Confidence
-   Score
-   Signal quality

The dashboard always displays ranked opportunities.

------------------------------------------------------------------------

## Dashboard

The PySide6 dashboard is responsible only for presentation.

It:

-   Displays BUY table
-   Displays SELL table
-   Refreshes incrementally
-   Preserves sorting
-   Shows detailed signal information

Business logic is intentionally excluded.

------------------------------------------------------------------------

## Alert Engine

Responsible for:

-   Detecting new signals
-   Preventing duplicate alerts
-   Formatting alert messages

------------------------------------------------------------------------

## SQLite Layer

Persists:

-   Candles
-   Indicators
-   Signals
-   Alerts

This enables historical analysis and future backtesting.

------------------------------------------------------------------------

# Dependency Flow

``` text
WebSocket
   ↓
Tick Processor
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
```

------------------------------------------------------------------------

# Key Architectural Benefits

-   Modular implementation
-   Clear separation of concerns
-   Easy unit testing
-   Thread-safe runtime state
-   Replaceable strategy modules
-   Backtesting-ready persistence
-   Future extensibility without major redesign

------------------------------------------------------------------------

# Next Document

The next document explains the complete runtime execution flow from
application startup until a BUY or SELL signal appears on the dashboard.
