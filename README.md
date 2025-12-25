# 🚀 TradeForge - Binance Futures Order Bot

> A production-ready, secure CLI trading bot for Binance USDT-M Futures with advanced algorithmic trading capabilities

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Security](https://img.shields.io/badge/security-HMAC%20SHA256-red.svg)](https://www.binance.com/en/support/faq/360002502072)

**Author:** Buvananand Vendotha  
**Date:** November 20, 2025

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Architecture](#-architecture)
- [Security](#-security)
- [Installation](#-installation)
- [Usage](#-usage)
- [Execution Examples](#-execution-examples)
- [Technical Implementation](#-technical-implementation)
- [Future Enhancements](#-future-enhancements)

---

## 🎯 Overview

This project implements a **command-line trading bot** for Binance USDT-M Futures, built from the ground up with enterprise-grade security and scalability in mind. Unlike wrapper-dependent solutions, this bot features a **custom API client** that provides full control over request signing, error handling, and execution flow.

The bot supports both **standard order types** (Market, Limit) and **advanced algorithmic strategies** (TWAP), making it suitable for both manual trading and automated execution systems.

---

## ✨ Key Features

### Core Functionality
- ✅ **Market Orders** - Instant execution at current market price
- ✅ **Limit Orders** - Precision entry/exit at specified price levels
- ✅ **TWAP Strategy** - Time-Weighted Average Price execution to minimize market impact

### Technical Highlights
- 🔐 **Custom Security Implementation** - HMAC SHA256 signature generation without third-party dependencies
- 🏗️ **Modular Architecture** - Separation of concerns enabling easy scalability
- 📊 **Centralized Logging** - Dual-output system (console + file) for real-time monitoring and auditing
- 🛡️ **Robust Error Handling** - Comprehensive validation and API error management
- 🔑 **Environment-Based Credentials** - Zero hardcoded secrets, production-safe configuration

---

## 🏛️ Architecture

The project follows a **modular design pattern** to ensure maintainability and extensibility:

```
binance-futures-bot/
├── src/
│   ├── client.py          # Custom API wrapper with HMAC signing
│   ├── logger.py          # Centralized logging system
│   ├── main.py            # CLI entry point with argparse routing
│   └── advanced/          # Advanced trading algorithms
│       └── twap.py        # Time-Weighted Average Price strategy
├── .env                   # API credentials (gitignored)
├── .gitignore
├── requirements.txt
└── README.md
```

### Design Principles

**Separation of Concerns:** Each module has a single, well-defined responsibility  
**Extensibility:** New strategies (Grid, OCO, DCA) can be added without modifying core logic  
**Zero Dependencies:** Custom API client eliminates reliance on potentially abandoned libraries  
**Auditability:** Every trade action is logged with timestamps and full context

---

## 🔒 Security

Security is the **cornerstone** of this implementation:

### 1. Credential Management
- API keys loaded from `.env` file using `python-dotenv`
- `.env` excluded from version control via `.gitignore`
- No secrets in code, logs, or commit history

### 2. Request Signing
- Custom **HMAC SHA256** implementation in `client.py`
- Ensures requests cannot be intercepted or tampered with
- Compliant with Binance API security requirements

### 3. Input Validation
- Strict type checking on all user inputs
- Symbol validation against Binance exchange info
- Quantity and price bounds verification

---

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- Binance Futures Testnet or Live API keys

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/vendotha/Buvananand-binance-bot.git
cd Buvananand-binance-bot
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure API credentials**
Create a `.env` file in the root directory:
```env
BINANCE_API_KEY=your_api_key_here
BINANCE_API_SECRET=your_api_secret_here
BINANCE_BASE_URL=https://testnet.binancefuture.com  # Use testnet for testing
```

4. **Verify installation**
```bash
python src/main.py --help
```

---

## 🎮 Usage

### Market Order
Execute immediate buy/sell at current market price:
```bash
python src/main.py market <SYMBOL> <SIDE> <QUANTITY>

# Example: Buy 0.01 BTC at market price
python src/main.py market BTCUSDT BUY 0.01
```

### Limit Order
Place order at specific price (Good Till Cancel):
```bash
python src/main.py limit <SYMBOL> <SIDE> <QUANTITY> <PRICE>

# Example: Buy 0.01 BTC at $45,000
python src/main.py limit BTCUSDT BUY 0.01 45000
```

### TWAP Strategy
Execute large order gradually to minimize market impact:
```bash
python src/main.py twap <SYMBOL> <SIDE> <TOTAL_QUANTITY> <DURATION_MINUTES> <SLICES>

# Example: Buy 0.05 BTC over 1 minute, split into 5 orders
python src/main.py twap BTCUSDT BUY 0.05 1 5
```

#### TWAP Algorithm Logic
```
Quantity per Slice = Total Quantity / Number of Slices
Delay (seconds) = (Duration in Minutes × 60) / Number of Slices

For each slice:
  1. Execute Market Order for calculated quantity
  2. Log execution details
  3. Sleep for calculated delay
  4. Repeat until all slices completed
```

---

## 📸 Execution Examples

### Market Order Execution
![Market Order](https://github.com/vendotha/Buvananand-binance-bot/blob/main/Market%20Order%20Execution.png)
*Successful market buy order execution on Binance Futures Testnet*

### Limit Order Execution
![Limit Order](https://github.com/vendotha/Buvananand-binance-bot/blob/main/Limit%20Order%20Execution.png)
*Limit order placed at $45,000 price level*

### TWAP Strategy Execution
![TWAP Strategy](https://github.com/vendotha/Buvananand-binance-bot/blob/main/TWAP%20Strategy%20Execution.png)
*TWAP algorithm executing 5 sequential slices over 1-minute duration*

---

## 🔧 Technical Implementation

### Custom API Client (`client.py`)
- Raw HTTP request handling using `requests` library
- Dynamic header construction with timestamp and signature
- HMAC SHA256 signature generation from scratch
- Generic `_request()` method supporting all API endpoints

### Logging System (`logger.py`)
- Dual handler setup: `StreamHandler` (console) + `FileHandler` (bot.log)
- ISO 8601 timestamp format for compliance
- Color-coded console output (INFO=green, ERROR=red)
- Rotation-ready for production deployment

### Error Handling Strategy
```python
try:
    response = self._request("POST", endpoint, params)
except requests.exceptions.HTTPError as e:
    logger.error(f"API Error: {e.response.json()}")
    # Specific handling for common errors:
    # - 400: Invalid parameters
    # - 401: Authentication failure
    # - 429: Rate limit exceeded
except Exception as e:
    logger.error(f"Unexpected error: {str(e)}")
```

### TWAP Implementation Highlights
- Stateful execution tracking across multiple iterations
- Graceful interruption handling (Ctrl+C)
- Real-time progress logging
- Atomic order execution with rollback capability

---

## 🚀 Future Enhancements

This architecture supports seamless integration of additional strategies:

- **Grid Trading** - Automated buy low/sell high within price range
- **OCO Orders** - One-Cancels-Other for stop-loss/take-profit
- **DCA Strategy** - Dollar-Cost Averaging for position building
- **Portfolio Rebalancing** - Multi-asset weight maintenance
- **WebSocket Integration** - Real-time price monitoring
- **Backtesting Engine** - Historical strategy validation

---

## 📊 Project Statistics

- **Lines of Code:** ~500 (core implementation)
- **Test Coverage:** Validated on Binance Futures Testnet
- **Dependencies:** Minimal (requests, python-dotenv, argparse)
- **API Endpoints Used:** `/fapi/v1/order`, `/fapi/v1/exchangeInfo`

---

## 🤝 Contributing

This project demonstrates professional-grade software engineering practices:
- Clean, documented code following PEP 8 standards
- Modular design enabling collaborative development
- Comprehensive error handling and logging
- Security-first approach with no hardcoded credentials

---

## 📄 License

This project is available under the MIT License. See `LICENSE` file for details.

---

## 👤 Contact

**Buvananand Vendotha**

For questions, collaboration opportunities, or technical discussions about algorithmic trading systems, feel free to reach out.

---

<div align="center">
  <b>Built with precision. Secured by design. Optimized for performance.</b>
</div>

