# 09_Buy_Sell_Decision_Logic.md

# BUY and SELL Decision Logic

## Overview

This document explains how a BUY or SELL recommendation is produced. The
decision process is intentionally layered to reduce false positives. No
single indicator generates a final signal on its own. Instead, multiple
technical confirmations are combined before a recommendation reaches the
dashboard.

------------------------------------------------------------------------

# Decision Pipeline

``` text
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
      │
      ▼
Dashboard
      │
      ▼
Alert Engine
```

------------------------------------------------------------------------

# BUY Decision Flow

A BUY opportunity generally follows these stages:

1.  Trend Identification
    -   Price trades above key moving averages.
    -   EMA alignment indicates an upward trend.
2.  Momentum Confirmation
    -   RSI supports bullish momentum.
    -   MACD confirms positive momentum.
3.  Trend Strength
    -   ADX indicates the trend is sufficiently strong.
4.  Volume Confirmation
    -   Relative Volume exceeds normal participation.
    -   Price remains above VWAP.
5.  Volatility Check
    -   ATR confirms meaningful price movement.
6.  Strategy Validation
    -   Strategy-specific entry rules are satisfied.
7.  Analysis Validation
    -   Multiple confirmations agree with the strategy.
8.  Confidence Calculation
    -   Dynamic Scoring assigns an overall confidence value.
9.  Ranking
    -   BUY candidates are ordered by confidence and quality.
10. Dashboard
    -   Qualified BUY opportunities are displayed.

------------------------------------------------------------------------

# SELL Decision Flow

SELL evaluation mirrors the BUY process.

Typical conditions include:

1.  Bearish EMA alignment.
2.  RSI weakening.
3.  MACD bearish confirmation.
4.  Strong ADX.
5.  Price below VWAP.
6.  Elevated Relative Volume.
7.  Strategy confirmation.
8.  Analysis validation.
9.  Confidence scoring.
10. Ranking and display.

------------------------------------------------------------------------

# Multi-Layer Validation

A signal must successfully pass several layers:

``` text
Indicators
      │
      ▼
Strategy Rules
      │
      ▼
Trend Check
      │
      ▼
Momentum Check
      │
      ▼
Volume Check
      │
      ▼
Volatility Check
      │
      ▼
Confidence Score
      │
      ▼
Ranked Signal
```

This layered approach helps reduce low-quality trading opportunities.

------------------------------------------------------------------------

# Confidence Influence

Confidence is not determined by a single indicator.

Typical contributors include:

  Confirmation              Influence
  ------------------------- -----------
  EMA Alignment             High
  RSI                       Medium
  MACD                      High
  ADX                       Medium
  ATR                       Medium
  VWAP                      Medium
  Relative Volume           High
  Strategy-specific rules   Variable

Higher agreement between confirmations results in higher confidence.

------------------------------------------------------------------------

# Signal Lifecycle

``` text
Market Tick
      │
      ▼
OHLC Candle
      │
      ▼
Indicators
      │
      ▼
Strategy Candidate
      │
      ▼
Analysis
      │
      ▼
Confidence Score
      │
      ▼
Ranking
      │
      ▼
Dashboard
      │
      ▼
Alert
      │
      ▼
SQLite History
```

------------------------------------------------------------------------

# Design Philosophy

The project intentionally separates:

-   Indicator calculation
-   Strategy detection
-   Signal validation
-   Confidence scoring
-   Ranking
-   Presentation

This separation keeps the application modular, testable, and easy to
extend.

------------------------------------------------------------------------

# Next Document

The next document describes the Ranking Engine, including how validated
BUY and SELL signals are prioritized before presentation.
