# 11_Dashboard.md

# Dashboard

## Overview

The Dashboard is the presentation layer of the Intraday Scanner. It
displays the highest-ranked BUY and SELL opportunities in real time
while remaining completely independent of business logic.

The dashboard consumes ranked signals produced by upstream components
and presents them through an interactive PySide6 user interface.

------------------------------------------------------------------------

# Responsibilities

The Dashboard is responsible for:

-   Displaying BUY opportunities
-   Displaying SELL opportunities
-   Showing confidence scores
-   Presenting strategy information
-   Refreshing data incrementally
-   Preserving user sorting
-   Preserving row selection
-   Displaying stock details
-   Showing application status

The dashboard does **not** calculate indicators, evaluate strategies, or
rank signals.

------------------------------------------------------------------------

# Dashboard Architecture

``` text
                Ranking Engine
                       │
                       ▼
              Dashboard Controller
                       │
        ┌──────────────┼──────────────┐
        ▼              ▼              ▼
 BUY Table       SELL Table     Status Panel
        │              │
        └───────┬──────┘
                ▼
        Stock Details View
```

------------------------------------------------------------------------

# Dashboard Components

## BUY Table

Displays active BUY opportunities.

Typical columns include:

-   Symbol
-   Last Traded Price
-   Strategy
-   Confidence
-   Score
-   Timestamp

The table is sorted using ranked signals.

------------------------------------------------------------------------

## SELL Table

Displays active SELL opportunities.

Its structure mirrors the BUY table, allowing users to compare both
market directions independently.

------------------------------------------------------------------------

## Status Panel

The status section communicates application health.

Typical information includes:

-   Scanner running state
-   Market connection
-   Feed status
-   Last refresh time
-   Number of tracked securities

------------------------------------------------------------------------

## Stock Details View

When a user selects a row, detailed information can be displayed.

Typical information:

-   Symbol
-   LTP
-   EMA values
-   RSI
-   MACD
-   ADX
-   ATR
-   VWAP
-   Relative Volume
-   Confidence
-   Active Strategy
-   Analysis Facts

This enables users to understand why a signal qualified.

------------------------------------------------------------------------

# Refresh Strategy

The dashboard performs **incremental updates** instead of rebuilding
tables.

For every refresh cycle:

1.  Add newly ranked signals.
2.  Update changed rows.
3.  Remove expired rows.
4.  Preserve manual sorting.
5.  Preserve selected rows.

This approach minimizes UI flicker and improves responsiveness.

------------------------------------------------------------------------

# Runtime Flow

``` text
Ranking Engine
      │
      ▼
Dashboard Controller
      │
      ▼
Compare Existing Rows
      │
      ▼
Add / Update / Remove
      │
      ▼
Refresh Visible Tables
      │
      ▼
Update Status Panel
```

------------------------------------------------------------------------

# Interaction with Other Modules

## Reads From

-   Ranking Engine
-   MarketDataStore

## Displays

-   Ranked BUY signals
-   Ranked SELL signals
-   Indicator summary
-   Confidence information

The Dashboard never modifies trading logic.

------------------------------------------------------------------------

# Design Principles

-   Presentation only
-   Incremental UI updates
-   Separation from business logic
-   Fast refresh performance
-   Stable user experience

------------------------------------------------------------------------

# Benefits

-   Responsive desktop interface
-   Minimal redraw operations
-   Easy navigation of trading opportunities
-   Clear separation between analytics and presentation
-   Extensible for future visualizations

------------------------------------------------------------------------

# Next Document

The next document explains the Alert Engine, including duplicate
prevention, alert lifecycle, formatting, and interaction with ranked
signals.
