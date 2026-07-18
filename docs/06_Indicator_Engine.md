# 06_Indicator_Engine.md

# Indicator Engine

## Overview

The Indicator Engine transforms completed OHLC candles into technical
indicators that quantify trend, momentum, volatility, and volume. These
indicators are the primary inputs for the Strategy Engine and Analysis
Engine.

The engine recalculates indicators whenever a new candle is completed.
It never uses partially formed candles, ensuring stable and repeatable
calculations.

------------------------------------------------------------------------

# Responsibilities

The Indicator Engine is responsible for:

-   Reading completed candles
-   Calculating technical indicators
-   Persisting indicator values
-   Updating the MarketDataStore
-   Supplying indicator data to downstream modules

------------------------------------------------------------------------

# Indicator Categories

  -----------------------------------------------------------------------
  Category               Indicators                  Purpose
  ---------------------- --------------------------- --------------------
  Trend                  EMA 9, EMA 20, EMA 50, EMA  Determine market
                         200                         direction

  Momentum               RSI, MACD                   Measure
                                                     buying/selling
                                                     strength

  Trend Strength         ADX                         Evaluate strength of
                                                     current trend

  Volatility             ATR                         Measure price
                                                     movement range

  Volume                 VWAP, Relative Volume       Confirm
                                                     participation and
                                                     institutional
                                                     interest
  -----------------------------------------------------------------------

------------------------------------------------------------------------

# Exponential Moving Average (EMA)

## Purpose

EMA smooths price movement while giving greater importance to recent
candles.

Implemented EMAs:

-   EMA 9
-   EMA 20
-   EMA 50
-   EMA 200

### Usage

-   Identify trend direction
-   Detect crossovers
-   Measure pullbacks
-   Confirm trend continuation

Example interpretation:

-   Price \> EMA20 \> EMA50 \> EMA200 → Strong bullish trend
-   Price \< EMA20 \< EMA50 \< EMA200 → Strong bearish trend

------------------------------------------------------------------------

# Relative Strength Index (RSI)

## Purpose

RSI measures the speed and magnitude of recent price changes.

Typical interpretation:

-   Above 70 → Overbought
-   Below 30 → Oversold
-   Around 50 → Neutral

### Scanner Usage

RSI is used as a confirmation tool rather than a standalone trading
signal.

Examples:

-   Bullish setup with RSI strengthening
-   Bearish setup with RSI weakening

------------------------------------------------------------------------

# MACD

## Purpose

MACD measures trend momentum by comparing fast and slow EMAs.

Components:

-   MACD Line
-   Signal Line
-   Histogram

### Scanner Usage

-   Bullish crossover
-   Bearish crossover
-   Momentum confirmation
-   Divergence awareness (future enhancement)

------------------------------------------------------------------------

# ADX (Average Directional Index)

## Purpose

ADX measures trend strength regardless of direction.

Typical interpretation:

-   Below 20 → Weak trend
-   20--25 → Trend developing
-   Above 25 → Strong trend
-   Above 40 → Very strong trend

### Scanner Usage

Signals in stronger trends receive greater confidence.

------------------------------------------------------------------------

# ATR (Average True Range)

## Purpose

ATR measures market volatility.

High ATR:

-   Larger price movement
-   Higher opportunity
-   Increased risk

Low ATR:

-   Quiet market
-   Lower momentum

### Scanner Usage

ATR influences confidence scoring and trade quality.

------------------------------------------------------------------------

# VWAP (Volume Weighted Average Price)

## Purpose

VWAP represents the average traded price weighted by volume.

Institutional traders commonly monitor VWAP.

### Scanner Usage

-   Price above VWAP supports bullish setups.
-   Price below VWAP supports bearish setups.
-   Helps filter false breakouts.

------------------------------------------------------------------------

# Relative Volume (RVOL)

## Purpose

Relative Volume compares current trading activity with normal volume.

Interpretation:

-   RVOL \> 1 → Higher-than-normal participation
-   RVOL \< 1 → Lower-than-normal participation

### Scanner Usage

Higher RVOL increases confidence because price movement is supported by
stronger participation.

------------------------------------------------------------------------

# Indicator Execution Flow

``` text
Completed Candle
        │
        ▼
Read Historical Candles
        │
        ▼
Calculate EMA
        │
        ▼
Calculate RSI
        │
        ▼
Calculate MACD
        │
        ▼
Calculate ADX
        │
        ▼
Calculate ATR
        │
        ▼
Calculate VWAP
        │
        ▼
Calculate RVOL
        │
        ▼
Persist Indicators
        │
        ▼
Update MarketDataStore
        │
        ▼
Trigger Strategy Engine
```

------------------------------------------------------------------------

# Design Principles

-   Indicators are calculated only from completed candles.
-   Calculations are isolated from strategy logic.
-   Indicator values are persisted for historical analysis.
-   Downstream modules consume indicator data without recalculating it.

------------------------------------------------------------------------

# Summary

The Indicator Engine converts raw market data into structured analytical
information. By separating indicator computation from strategy
evaluation, the architecture remains modular, testable, and easy to
extend with future indicators.

------------------------------------------------------------------------

# Next Document

The next document explains the Strategy Engine, including how individual
trading strategies consume indicator data to generate BUY and SELL
candidates.
