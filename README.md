# Intraday Scanner

A lightweight, modular intraday stock market scanner built in Python for the Indian stock market using the DhanHQ API.

The project is designed for **personal use**, focusing on real-time market scanning rather than automated trading. It provides a clean architecture that is easy to understand, extend, and maintain.

---

## Features

### Market Data

* Live market data using Dhan WebSocket API
* Watchlist-based scanning
* Multi-stock monitoring
* Real-time candle generation
* Historical and live data support (planned)

### Technical Indicators

* Simple Moving Average (SMA)
* Exponential Moving Average (EMA)
* Relative Strength Index (RSI)
* Volume Weighted Average Price (VWAP)
* Highest High
* Lowest Low
* Average Volume

### Trading Strategies

* Trend Scanner
* Breakout Scanner
* Volume Scanner

### Signal Processing

* Signal generation
* Confidence scoring
* Signal ranking
* Duplicate signal filtering

### Dashboard

* Console dashboard
* Ranked trading signals
* Strategy information
* Confidence score
* Price information

---

# Project Structure

```text
intraday_scanner/
│
├── src/
│   ├── core/
│   │   ├── config.py
│   │   ├── constants.py
│   │   ├── exceptions.py
│   │   └── logger.py
│   │
│   ├── models/
│   │   ├── candle.py
│   │   ├── signal.py
│   │   └── stock.py
│   │
│   ├── services/
│   │   ├── base_service.py
│   │   ├── dhan_context.py
│   │   ├── market_data.py
│   │   ├── notifier.py
│   │   ├── watchlist.py
│   │   └── websocket_client.py
│   │
│   ├── scanners/
│   │   ├── breakout.py
│   │   ├── trend.py
│   │   └── volume.py
│   │
│   ├── dashboard.py
│   ├── indicators.py
│   ├── ranking.py
│   ├── scanner.py
│   └── main.py
│
├── config/
├── logs/
├── tests/
├── requirements.txt
├── README.md
└── .env
```

---

# Current Status

## Completed

* Project structure
* Configuration management
* Logging
* Watchlist management
* Market data management
* DhanHQ authentication
* WebSocket connectivity
* Technical indicators
* Trend scanner
* Breakout scanner
* Volume scanner
* Signal ranking
* Console dashboard

## In Progress

* Live tick processing
* Main application integration
* Telegram notifications

---

# Technology Stack

* Python 3.12+
* DhanHQ SDK v2
* Pandas
* WebSockets
* Thread-safe data structures
* Logging

---

# Installation

## Clone Repository

```bash
git clone https://github.com/<your-username>/intraday_scanner.git
cd intraday_scanner
```

## Create Virtual Environment

```bash
python3.12 -m venv venv
```

Linux/macOS

```bash
source venv/bin/activate
```

Windows

```bash
venv\Scripts\activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Configuration

Create a `.env` file.

```text
DHAN_CLIENT_ID=xxxxxxxx
DHAN_ACCESS_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxx
```

---

# Running

## Run Unit Tests

```bash
python3.12 test_indicators.py
python3.12 test_trend.py
python3.12 test_breakout.py
python3.12 test_volume.py
python3.12 test_ranking.py
python3.12 test_dashboard.py
```

## Test WebSocket

```bash
python3.12 test_websocket.py
```

---

# Scanner Workflow

```text
Watchlist
      │
      ▼
Dhan WebSocket
      │
      ▼
Market Data
      │
      ▼
Technical Indicators
      │
      ▼
Trend Scanner
Breakout Scanner
Volume Scanner
      │
      ▼
Signal Ranking
      │
      ▼
Dashboard
```

---

# Trading Strategies

## Trend Strategy

BUY

* EMA20 > EMA50
* Price > VWAP
* RSI > 55

SELL

* EMA20 < EMA50
* Price < VWAP
* RSI < 45

---

## Breakout Strategy

BUY

* Close above previous 20-candle high
* Volume greater than 1.5× average volume

SELL

* Close below previous 20-candle low
* Volume greater than 1.5× average volume

---

## Volume Strategy

BUY

* Bullish candle
* Volume greater than 2× average volume
* Close above previous candle

SELL

* Bearish candle
* Volume greater than 2× average volume
* Close below previous candle

---

# Future Enhancements

* Historical data loading
* Telegram notifications
* SQLite trade logging
* Strategy configuration
* Multi-timeframe analysis
* Additional technical indicators
* Performance analytics
* Backtesting framework

---

# Disclaimer

This project is intended for educational and personal use only.

It does **not** provide financial advice. Trading in financial markets involves risk, and users should evaluate any trading decisions independently.

---

# License

MIT License

---

# Author

**Dejies Deoder**

Built as a personal intraday stock market scanner for the Indian stock market using the DhanHQ API.
