# 14_Threading_and_Concurrency.md

# Threading and Concurrency

## Overview

The Intraday Scanner is a real-time application that simultaneously
receives market data, processes trading logic, updates the dashboard,
and persists data. To achieve this without blocking the user interface,
the application separates responsibilities across different execution
contexts while sharing runtime state through the `MarketDataStore`.

------------------------------------------------------------------------

# Objectives

The threading model is designed to:

-   Keep the UI responsive.
-   Process live market data with low latency.
-   Prevent race conditions.
-   Avoid blocking operations.
-   Isolate long-running tasks.
-   Provide predictable runtime behavior.

------------------------------------------------------------------------

# High-Level Thread Model

``` text
                   Main Application
                         │
        ┌────────────────┴────────────────┐
        │                                 │
        ▼                                 ▼
 Dashboard (UI Thread)         Market Feed Thread
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
        ┌───────────────┬────────────────┼────────────────┐
        ▼               ▼                ▼                ▼
 Candle Builder   Indicator Engine  Strategy Engine  Alert Engine
```

------------------------------------------------------------------------

# UI Thread

The main thread is dedicated to presentation.

Responsibilities:

-   Render dashboard
-   Handle user interaction
-   Refresh BUY table
-   Refresh SELL table
-   Display status
-   Show stock details

The UI thread should never perform heavy analytical work.

------------------------------------------------------------------------

# Market Feed Thread

The market feed executes independently.

Responsibilities:

-   Maintain WebSocket connection
-   Receive ticks
-   Handle reconnects
-   Forward validated ticks

This prevents network activity from blocking the UI.

------------------------------------------------------------------------

# Tick Processing

Each incoming tick follows the pipeline:

``` text
WebSocket
     │
     ▼
Tick Processor
     │
     ▼
MarketDataStore
```

The Tick Processor validates and normalizes incoming data before
updating shared runtime state.

------------------------------------------------------------------------

# Shared Runtime State

The `MarketDataStore` is the shared in-memory repository used by all
major modules.

It contains:

-   Latest tick
-   Active candle
-   Completed candles
-   Indicators
-   Active signals
-   Rankings

By centralizing runtime state, components operate on a consistent view
of the market.

------------------------------------------------------------------------

# Background Processing

After a candle is completed, downstream processing typically includes:

1.  Candle persistence
2.  Indicator calculation
3.  Strategy evaluation
4.  Analysis
5.  Dynamic scoring
6.  Ranking
7.  Alert generation

These operations are isolated from UI rendering.

------------------------------------------------------------------------

# Dashboard Refresh

The dashboard consumes processed results.

Refresh strategy:

-   Compare existing rows.
-   Add new rows.
-   Update changed values.
-   Remove obsolete rows.
-   Preserve user sorting.
-   Preserve row selection.

Incremental updates minimize redraw overhead.

------------------------------------------------------------------------

# Thread Safety Considerations

The application avoids inconsistent state by:

-   Maintaining a central MarketDataStore.
-   Separating UI and market processing.
-   Restricting responsibilities to dedicated modules.
-   Avoiding duplicated runtime state.

------------------------------------------------------------------------

# Benefits

-   Responsive user interface
-   Low-latency market processing
-   Modular execution flow
-   Easier debugging
-   Improved scalability
-   Cleaner separation of concerns

------------------------------------------------------------------------

# Runtime Sequence

``` text
Market Feed
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
Indicator Engine
      │
      ▼
Strategy Engine
      │
      ▼
Analysis Engine
      │
      ▼
Ranking Engine
      │
      ├────────► Dashboard
      │
      └────────► Alert Engine
```

------------------------------------------------------------------------

# Design Principles

-   Keep the UI lightweight.
-   Perform analytics outside the presentation layer.
-   Share runtime state through a single source of truth.
-   Maintain modular, thread-safe processing.

------------------------------------------------------------------------

# Next Document

The next document explains the complete end-to-end trade lifecycle,
tracing a single market tick from arrival to a BUY or SELL signal
appearing on the dashboard and being stored in the database.
