# Indian Intraday Scanner

# Documentation Index

This documentation is organized into independent guides that explain
every major component of the application.

  ----------------------------------------------------------------------------------------
  No.          Document                                   Description
  ------------ ------------------------------------------ --------------------------------
  0            README.md                                  Documentation index and project
                                                          summary

  1            01_Project_Overview.md                     Project goals, modules and
                                                          overall workflow

  2            02_System_Architecture.md                  Layered architecture and
                                                          component interactions

  3            03_Application_Runtime_Flow.md             Complete runtime execution flow

  4            04_MarketDataStore_and_DataFlow.md         Runtime data management and data
                                                          flow

  5            05_Candle_Engine.md                        Tick aggregation and OHLC candle
                                                          generation

  6            06_Indicator_Engine.md                     EMA, RSI, MACD, ADX, ATR, VWAP
                                                          and RVOL

  7            07_Strategy_Engine.md                      Strategy execution and signal
                                                          generation

  8            08_Analysis_and_Dynamic_Scoring.md         Signal validation and confidence
                                                          scoring

  9            09_Buy_Sell_Decision_Logic.md              Complete BUY/SELL decision
                                                          pipeline

  10           10_Ranking_Engine.md                       Signal prioritization and
                                                          ranking

  11           11_Dashboard.md                            Dashboard architecture and UI
                                                          flow

  12           12_Alert_Engine.md                         Alert generation and duplicate
                                                          prevention

  13           13_Database_and_Models.md                  Database layer, repositories and
                                                          domain models

  14           14_Threading_and_Concurrency.md            Thread model and runtime
                                                          concurrency

  15           15_End_to_End_Trade_Lifecycle.md           Tick-to-signal lifecycle
                                                          walkthrough

  16           16_Deployment_and_Future_Enhancements.md   Deployment, testing and future
                                                          roadmap
  ----------------------------------------------------------------------------------------

------------------------------------------------------------------------

# Project Summary

The Indian Intraday Scanner is a modular real-time stock scanning
application for the Indian equity market. It consumes live market data
from the Dhan WebSocket API, builds one-minute candles, calculates
technical indicators, evaluates trading strategies, validates and scores
opportunities, ranks BUY/SELL signals, displays them in a PySide6
dashboard, generates alerts, and stores historical data in SQLite.

## High-Level Processing Flow

``` text
Dhan Market Feed
        ↓
WebSocket Client
        ↓
Tick Processor
        ↓
MarketDataStore
        ↓
Candle Engine
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

## Core Features

-   Live Dhan WebSocket integration
-   One-minute OHLC Candle Builder
-   Technical Indicator Engine
-   Strategy Engine
-   Analysis & Dynamic Scoring
-   Ranking Engine
-   Real-time Dashboard
-   Alert Engine
-   SQLite persistence
-   Modular architecture
