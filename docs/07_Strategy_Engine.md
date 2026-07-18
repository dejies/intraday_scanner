# 07_Strategy_Engine.md

# Strategy Engine

## Overview

The Strategy Engine is responsible for converting indicator values into
actionable BUY and SELL candidates. Each strategy operates
independently, evaluates the latest market state, and produces candidate
signals without considering ranking or presentation.

The engine does not decide whether a signal should be shown to the user.
It only detects potential trading opportunities. Validation is performed
later by the Analysis Engine.

------------------------------------------------------------------------

# Responsibilities

The Strategy Engine:

-   Reads the latest indicators from the MarketDataStore
-   Evaluates each enabled strategy independently
-   Generates BUY or SELL candidates
-   Records strategy-specific metadata
-   Passes candidate signals to the Analysis Engine

It does **not** calculate indicators, assign confidence scores, rank
signals, or update the dashboard.

------------------------------------------------------------------------

# Strategy Pipeline

``` text
Completed Indicators
        │
        ▼
Load Strategy
        │
        ▼
Evaluate Entry Conditions
        │
        ▼
Entry Conditions Met?
    ┌────┴────┐
    │         │
   No        Yes
    │         │
    ▼         ▼
 Ignore   Create Candidate Signal
               │
               ▼
        Analysis Engine
```

------------------------------------------------------------------------

# Strategy Inputs

Each strategy may consume one or more of the following:

-   Current OHLC candle
-   Previous candles
-   EMA 9
-   EMA 20
-   EMA 50
-   EMA 200
-   RSI
-   MACD
-   ADX
-   ATR
-   VWAP
-   Relative Volume

------------------------------------------------------------------------

# Typical Strategy Types

Although each strategy has unique rules, they generally fall into the
following categories.

## Trend Following

Objective:

-   Trade in the direction of the prevailing trend.

Typical confirmations:

-   EMA alignment
-   Strong ADX
-   Price above/below key moving averages

------------------------------------------------------------------------

## Pullback

Objective:

-   Enter after a temporary retracement within an existing trend.

Typical confirmations:

-   Trend remains intact
-   Price returns toward EMA
-   Momentum resumes

------------------------------------------------------------------------

## Breakout

Objective:

-   Capture strong moves beyond important price levels.

Typical confirmations:

-   Break above/below range
-   High Relative Volume
-   Momentum confirmation

------------------------------------------------------------------------

## Momentum Continuation

Objective:

-   Participate in an already accelerating move.

Typical confirmations:

-   MACD agreement
-   RSI strength
-   Strong trend

------------------------------------------------------------------------

# Candidate Signal

A generated signal typically contains:

-   Security ID
-   BUY or SELL type
-   Strategy name
-   Signal price
-   Current market price
-   Timestamp
-   Supporting analysis facts

At this stage, the signal is only a candidate and has not yet received a
confidence score.

------------------------------------------------------------------------

# Multiple Strategy Support

The architecture allows multiple strategies to evaluate the same
security.

Possible outcomes:

-   No strategy produces a signal.
-   One strategy produces a signal.
-   Multiple strategies produce independent signals.

The Analysis Engine determines which opportunities should continue.

------------------------------------------------------------------------

# Interaction with Other Modules

## Reads From

-   MarketDataStore
-   Indicator Repository

## Writes To

-   Candidate Signal Model

## Passes To

-   Analysis Engine

------------------------------------------------------------------------

# Design Principles

-   Strategies are independent.
-   Strategies do not communicate with each other.
-   Business rules remain isolated.
-   New strategies can be added without modifying existing ones.
-   Indicator calculations are never duplicated inside strategies.

------------------------------------------------------------------------

# Runtime Flow

``` text
Indicators
    │
    ▼
Strategy A
Strategy B
Strategy C
    │
    ▼
Candidate Signals
    │
    ▼
Analysis Engine
```

------------------------------------------------------------------------

# Benefits

-   Modular strategy implementation
-   Easy experimentation
-   Independent testing
-   Extensible architecture
-   Clean separation between detection and validation

------------------------------------------------------------------------

# Next Document

The next document explains the Analysis Engine and Dynamic Scoring
process, showing how candidate signals are validated, assigned
confidence scores, and prepared for ranking.
