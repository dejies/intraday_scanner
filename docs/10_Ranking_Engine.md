# 10_Ranking_Engine.md

# Ranking Engine

## Overview

The Ranking Engine is responsible for prioritizing validated BUY and
SELL signals before they are displayed to the user. Since multiple
strategies can generate signals simultaneously, the Ranking Engine
ensures that the highest-quality opportunities appear first.

The Ranking Engine does not create trading signals. It consumes
validated signals from the Analysis Engine and produces an ordered list
based on confidence and quality.

------------------------------------------------------------------------

# Responsibilities

The Ranking Engine performs the following tasks:

-   Receive validated BUY and SELL signals
-   Compare signal confidence
-   Apply ranking rules
-   Sort opportunities
-   Publish ranked results to the Dashboard
-   Supply ranked signals to the Alert Engine

------------------------------------------------------------------------

# Position in the Pipeline

``` text
Indicator Engine
        │
        ▼
Strategy Engine
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
        ├────────► Dashboard
        │
        └────────► Alert Engine
```

------------------------------------------------------------------------

# Ranking Inputs

Each validated signal typically contains:

-   Security ID
-   Signal Type (BUY / SELL)
-   Strategy Name
-   Signal Price
-   Current LTP
-   Confidence Score
-   Analysis Facts
-   Score Breakdown
-   Timestamp

------------------------------------------------------------------------

# Ranking Process

``` text
Validated Signals
        │
        ▼
Group BUY Signals
        │
        ▼
Group SELL Signals
        │
        ▼
Sort by Confidence
        │
        ▼
Resolve Equal Scores
        │
        ▼
Publish Ranked List
```

------------------------------------------------------------------------

# Primary Ranking Criteria

Signals are primarily ordered using:

1.  Confidence Score
2.  Overall Signal Quality
3.  Strategy Strength
4.  Timestamp (when applicable)

The exact implementation may vary, but confidence remains the dominant
ranking factor.

------------------------------------------------------------------------

# BUY and SELL Separation

BUY and SELL opportunities are ranked independently.

This allows:

-   Dedicated BUY table
-   Dedicated SELL table
-   Independent prioritization
-   Cleaner dashboard presentation

------------------------------------------------------------------------

# Dashboard Interaction

The Dashboard consumes only ranked signals.

Responsibilities include:

-   Display highest-ranked opportunities first
-   Refresh incrementally
-   Preserve user-selected sorting
-   Remove expired entries
-   Update confidence values as rankings change

------------------------------------------------------------------------

# Alert Interaction

The Alert Engine consumes ranked signals to determine which
opportunities warrant user notification.

Benefits include:

-   Alerting only meaningful opportunities
-   Reducing duplicate notifications
-   Highlighting the strongest setups first

------------------------------------------------------------------------

# Runtime Flow

``` text
Validated Signal
        │
        ▼
Confidence Available?
    ┌────┴────┐
    │         │
   No        Yes
    │         │
Discard   Rank Signal
               │
               ▼
      BUY / SELL Lists
               │
               ▼
 Dashboard & Alerts
```

------------------------------------------------------------------------

# Design Principles

-   Ranking is isolated from signal generation.
-   Signals remain immutable during ranking.
-   BUY and SELL lists are maintained separately.
-   Dashboard presentation is based entirely on ranked output.
-   Additional ranking rules can be introduced without changing
    strategies.

------------------------------------------------------------------------

# Benefits

-   Clear prioritization of opportunities
-   Consistent user experience
-   Separation of validation and presentation
-   Improved scalability for additional strategies

------------------------------------------------------------------------

# Next Document

The next document explains the Dashboard architecture, including live
updates, table management, signal presentation, and user interaction.
