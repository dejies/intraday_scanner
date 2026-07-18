# 12_Alert_Engine.md

# Alert Engine

## Overview

The Alert Engine is responsible for notifying users whenever a new,
qualified BUY or SELL opportunity is detected. It consumes ranked
signals from the Ranking Engine, applies duplicate prevention rules,
formats the alert, stores it, and makes it available for presentation.

The Alert Engine is intentionally isolated from strategy evaluation and
scoring. Its only responsibility is managing alerts.

------------------------------------------------------------------------

# Responsibilities

The Alert Engine performs the following tasks:

-   Receive ranked BUY and SELL signals
-   Detect newly qualified opportunities
-   Prevent duplicate alerts
-   Format alert messages
-   Persist alert history
-   Publish alerts for presentation

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
        ▼
Alert Engine
        │
        ▼
Dashboard / Notification
```

------------------------------------------------------------------------

# Alert Lifecycle

Every alert follows the same lifecycle.

``` text
Ranked Signal
      │
      ▼
Duplicate Check
      │
 ┌────┴────┐
 │         │
Yes       No
 │         │
 ▼         ▼
Ignore  Create Alert
             │
             ▼
      Format Message
             │
             ▼
      Store in SQLite
             │
             ▼
     Publish to UI
```

------------------------------------------------------------------------

# Duplicate Prevention

One of the most important responsibilities of the Alert Engine is
avoiding repeated notifications.

Typical duplicate checks include:

-   Same security
-   Same signal type
-   Same strategy
-   Previously alerted state

If the signal has already been notified, it is ignored until a
meaningful change occurs.

------------------------------------------------------------------------

# Alert Structure

A typical alert contains:

-   Security ID
-   Symbol
-   BUY / SELL
-   Strategy
-   Signal Price
-   Current Price
-   Confidence
-   Timestamp
-   Human-readable message

Additional metadata may also be stored for historical review.

------------------------------------------------------------------------

# Alert Formatting

The formatter converts technical signal information into a readable
message.

Typical content includes:

-   Instrument
-   Signal direction
-   Strategy name
-   Confidence score
-   Current market price
-   Time generated

Keeping formatting separate from business logic allows future
notification channels (desktop, email, mobile) to reuse the same alert
information.

------------------------------------------------------------------------

# Persistence

Alerts are written to SQLite.

Benefits include:

-   Historical review
-   Duplicate detection
-   Auditing
-   Future analytics

------------------------------------------------------------------------

# Interaction with Other Modules

## Input

-   Ranked BUY signals
-   Ranked SELL signals

## Output

-   Alert Repository
-   Dashboard
-   Notification system

The Alert Engine never recalculates indicators or modifies signal
confidence.

------------------------------------------------------------------------

# Runtime Flow

``` text
Ranked Signal
      │
      ▼
Already Alerted?
 ┌────┴────┐
 │         │
Yes       No
 │         │
 ▼         ▼
Ignore  Format Alert
             │
             ▼
      Persist Alert
             │
             ▼
      Notify Dashboard
```

------------------------------------------------------------------------

# Design Principles

-   Single responsibility
-   Stateless processing where possible
-   Duplicate prevention
-   Reusable alert formatting
-   Persistent alert history

------------------------------------------------------------------------

# Benefits

-   Eliminates repeated notifications
-   Provides a clean notification pipeline
-   Enables future notification channels
-   Improves user experience
-   Maintains complete alert history

------------------------------------------------------------------------

# Next Document

The next document explains the database layer and domain models,
including repositories, SQLite schema, persistence flow, and how runtime
objects are stored and retrieved.
