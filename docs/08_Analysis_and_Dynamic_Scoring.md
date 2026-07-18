# 08_Analysis_and_Dynamic_Scoring.md

# Analysis Engine and Dynamic Scoring

## Overview

The Analysis Engine acts as the quality control layer of the
application. While the Strategy Engine identifies potential BUY and SELL
opportunities, the Analysis Engine validates those opportunities using
multiple confirmations before assigning a confidence score.

Only signals that successfully pass the analysis stage proceed to the
Ranking Engine and Dashboard.

------------------------------------------------------------------------

# Responsibilities

The Analysis Engine is responsible for:

-   Validating candidate signals
-   Applying additional confirmation checks
-   Rejecting weak opportunities
-   Producing structured analysis facts
-   Assigning weighted confidence scores
-   Forwarding validated signals for ranking

------------------------------------------------------------------------

# Processing Pipeline

``` text
Strategy Engine
      │
      ▼
Candidate Signal
      │
      ▼
Analysis Engine
      │
      ▼
Validation Rules
      │
      ▼
Dynamic Scoring
      │
      ▼
Ranked Signal
      │
      ▼
Ranking Engine
```

------------------------------------------------------------------------

# Validation Stage

The engine evaluates whether the signal satisfies multiple technical
confirmations.

Typical confirmation groups include:

## Trend Confirmation

Examples:

-   EMA alignment
-   Price relative to moving averages
-   Trend direction

------------------------------------------------------------------------

## Momentum Confirmation

Examples:

-   RSI supports direction
-   MACD confirms momentum
-   Positive histogram (BUY)
-   Negative histogram (SELL)

------------------------------------------------------------------------

## Trend Strength

Measured primarily using ADX.

Weak trends reduce confidence.

Strong trends increase confidence.

------------------------------------------------------------------------

## Volume Confirmation

Checks include:

-   Relative Volume
-   VWAP relationship
-   Participation quality

Higher participation generally increases signal reliability.

------------------------------------------------------------------------

## Volatility Check

ATR helps determine whether price movement is meaningful.

Very low volatility can reduce confidence.

------------------------------------------------------------------------

# Analysis Facts

Every validated signal may include structured facts explaining why it
qualified.

Typical facts include:

-   Strong EMA alignment
-   Bullish MACD crossover
-   RSI above midpoint
-   ADX indicates strong trend
-   Price trading above VWAP
-   Relative Volume above average

These facts improve transparency and debugging.

------------------------------------------------------------------------

# Dynamic Scoring

Instead of assigning a fixed score, the application calculates
confidence dynamically.

Each confirmation contributes a weighted value.

Typical contributors:

  Factor            Effect
  ----------------- ----------
  EMA Alignment     High
  RSI               Medium
  MACD              High
  ADX               Medium
  ATR               Medium
  VWAP              Medium
  Relative Volume   High
  Strategy Bonus    Variable

The sum becomes the overall confidence score.

------------------------------------------------------------------------

# Confidence Levels

Although exact thresholds are implementation-specific, signals can
generally be interpreted as:

  Confidence   Interpretation
  ------------ ----------------------------
  Very High    Strong trading opportunity
  High         Good probability setup
  Medium       Acceptable with caution
  Low          Weak confirmation
  Very Low     Usually discarded

------------------------------------------------------------------------

# Interaction with Other Modules

## Input

-   Candidate signals
-   Latest indicators
-   MarketDataStore

## Output

-   Validated signals
-   Confidence score
-   Analysis facts
-   Score breakdown

------------------------------------------------------------------------

# Runtime Flow

``` text
Candidate Signal
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
Calculate Confidence
      │
      ▼
Validated Signal
```

------------------------------------------------------------------------

# Design Benefits

-   Reduces false positives
-   Separates detection from validation
-   Improves explainability
-   Produces consistent scoring
-   Supports future scoring enhancements

------------------------------------------------------------------------

# Next Document

The next document explains the BUY and SELL decision flow, showing how
validated signals are ranked and presented to the user.
