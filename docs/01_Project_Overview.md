# 01_Project_Overview.md

# Project Overview

## Purpose

The Indian Intraday Scanner is a modular, real-time stock scanning
application built for the Indian equity market. It continuously consumes
live market data from the Dhan WebSocket API, constructs OHLC candles,
computes technical indicators, evaluates trading strategies, scores
opportunities, ranks BUY/SELL signals, and presents them through a
PySide6 desktop dashboard.

The application is designed as a decision-support system rather than an
automated trading bot.

------------------------------------------------------------------------

# Project Goals

-   Receive live market ticks with minimal latency.
-   Maintain an in-memory market state for all subscribed securities.
-   Build one-minute OHLC candles.
-   Persist historical candles and indicators into SQLite.
-   Calculate multiple technical indicators.
-   Detect high-probability BUY and SELL opportunities.
-   Assign confidence scores using multiple confirmations.
-   Rank signals based on overall quality.
-   Display opportunities in a live desktop dashboard.
-   Generate alerts while preventing duplicates.
-   Provide a foundation for future backtesting.

------------------------------------------------------------------------

# Major Modules

  Module             Responsibility
  ------------------ ----------------------------------------------
  WebSocket          Receive live market ticks
  Tick Processor     Validate and normalize ticks
  MarketDataStore    Runtime source of truth
  Candle Engine      Build OHLC candles
  Indicator Engine   Compute EMA, RSI, MACD, ADX, ATR, VWAP, RVOL
  Strategy Engine    Detect trading setups
  Analysis Engine    Validate strategy output
  Dynamic Scoring    Calculate confidence score
  Ranking Engine     Prioritize opportunities
  Dashboard          Present BUY/SELL candidates
  Alert Engine       Notify new trading signals
  SQLite             Persist historical information

------------------------------------------------------------------------

# Design Principles

## Single Responsibility

Each package has one clearly defined responsibility.

## Loose Coupling

Modules communicate through domain models rather than direct
implementation details.

## Thread Safety

Market data processing and UI updates remain isolated while sharing
state safely through the MarketDataStore.

## Repository Pattern

All database access is encapsulated inside repository classes.

------------------------------------------------------------------------

# End-to-End Workflow

1.  Application starts.
2.  Configuration is loaded.
3.  SQLite is initialized.
4.  Dashboard starts.
5.  WebSocket subscribes to market feed.
6.  Live ticks update MarketDataStore.
7.  Candle Builder produces completed candles.
8.  Indicator Engine recalculates indicators.
9.  Strategy Engine evaluates opportunities.
10. Analysis Engine validates signals.
11. Dynamic Scoring assigns confidence.
12. Ranking Engine sorts candidates.
13. Dashboard refreshes BUY/SELL tables.
14. Alert Engine generates notifications.
15. Results are persisted for historical analysis.

------------------------------------------------------------------------

# Next Document

The next document (**02_System_Architecture.md**) explains the internal
architecture, package relationships, runtime components, and interaction
diagrams.
