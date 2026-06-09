# Binance Futures Trading CLI Bot
A professional, modular, and human-centric Command Line Interface (CLI) application built in Python to interact with the **Binance Futures Testnet (USDT-M) API**.

This application features robust input pre-flight validation, centralized thread-safe logging, automated runtime environment configuration, and support for dual operational modes: regular developer flags or an interactive step-by-step terminal wizard designed for non-technical users.

# 🌟 Features & Project Scope
### Core Requirements Fully Implemented

1. **Dual Market Order Execution**: Supports immediate execution for both BUY (Long) and SELL (Short) directions.
2. **Resting Limit Orders**: Supports placement of orders onto the digital order book at precise price targets.
3. **Pre-flight Constraints Verification**: Independent semantic validation layer confirming symbol structure, absolute price thresholds, and position size constraints before initiating network connections.
4. **Persistent Structural Logging**: Centralized engine recording outbound request payloads, successful inbound confirmation receipts, and raw API connection exceptions directly to a local tracking file.

### Extra Features(Bonus):

1. **STOP_LIMIT Order Type**:Advanced conditional orchestration introducing automated trigger activation thresholds (--stop-price) alongside traditional book execution prices (--price).
2. **Enhanced Interactive UX & Wizard Mode**: Gracefully switches to a beautiful step-by-step Q&A format using choices and confirmation modules if launched without command flags.
3. **Automated Onboarding Script (bot/config.py)**: Automatically checks for required API environment variables at startup and guides the user to set them up on the fly if missing.

---

# 📂 Project Architecture

The architecture relies strictly on the separation of concerns paradigm, isolating the representation layer from the transaction orchestration and the underlying networking protocols:

```text
trading_bot/
│
├── bot/
│   ├── client.py           # The Python scripts which checks the Client API configuration
│   ├── orders.py           # Orchestrates middleware logic and forwards arguments
│   ├── validators.py       # Checks User's arguments for any syntax error
│   ├── config.py           # Checks presence of .env for User's device
│   └── logging_config.py   # Logs User's interaction in a file name bot.log
│
├── cli.py                  # Entry point for the trading bot system
├── bot.log                 # Generated transaction receipts log file 
├── .gitignore              # Shields secret operational variables from version tracking
└── requirements.txt        # Isolated minimalist dependency production matrix
```

---

# 🚀 Setup & Installation Instructions

## 1. Clone Project

```
git clone https://github.com/DIPRO2000/Binance_trading_bot.git
cd Binance_trading_bot
```

## 2. Configure Environment

### Option 1: Using Conda

```
# Create Environment
conda create --name trading_bot python=3.10 -y

# Activate Environment
conda activate trading_bot
```

### Option 2: Using standard Python (venv)

```
cd Binance_trading_bot

# Create a virtual environment folder named 'trading_bot'
python -m venv trading_bot

# On Windows (Command Prompt):
trading_bot\Scripts\activate

# On macOS / Linux:
source trading_bot/bin/activate
```

## 3. Install Minimalist Dependencies

```
pip install -r requirements.txt
```

---

# 🔐 Environment Configuration (.env)

This application includes a zero-configuration onboarding mechanism. You do not need to manually create or manage a configuration file before your first launch.

### Automated Setup
When you execute `python cli.py` for the first time without flags, the core engine (`bot/config.py`) intercepts the execution path, detects the missing variables, and guides you through a secure terminal prompt to populate your keys. It then writes a local `.env` file automatically.

### Manual Setup Fallback
If you prefer to configure the environment file manually before launching the script, create a file named `.env` in the root directory and populate it with your Binance Futures Testnet credentials:

```env
BINANCE_API_KEY=your_actual_testnet_api_key_here
BINANCE_API_SECRET=your_actual_testnet_api_secret_here
```

---

# 💻 Operation & Usage Guide
The bot dynamically routes usage based on the arguments provided.

## Mode A: Non-Technical Interactive Wizard Mode
If you run the application with no arguments, it automatically triggers the guided setup wizard. It will check for your credentials, ask you to input them if missing, and then walk you through building your order.

```
python cli.py
```

## Mode B: Developer Command-Flag Mode
For high-speed automated testing, scripts, or advanced operators, pass structured flags directly into the entry execution script:

### 1. Immediate Market Buy Order

```
python cli.py --symbol BTCUSDT --side BUY --order-type MARKET --quantity 0.001
```

### 2. Resting Limit Sell Order

```
python cli.py --symbol BTCUSDT --side SELL --order-type LIMIT --quantity 0.001 --price 75000
```

### 3. Advanced Stop-Limit Buy Order (Bonus)

```
python cli.py --symbol BTCUSDT --side BUY --order-type STOP_LIMIT --quantity 0.001 --price 63000 --stop-price 65000
```

---

# 📊 Order Execution Output Formatting

When an order successfully goes through the network layer, a structured table summarizes the metadata returned from the Binance engine:

| *Key Metric Reference*               | *Exchange Value Output Description*                                          |
| :------------------------------------| :---------------------------------------------------------------------------:|
| **Order Identification Unique ID**   | The unchangeable receipt reference generated by Binance (e.g., 14508718653). |
| **Transaction Target Status**        | Current status state on the book (NEW, FILLED, PARTIALLY_FILLED).            |
| **Client Context Symbol Pair**       | The validated asset ticker matched on the exchange (BTCUSDT).                |
| **Executed Context Filled Qty**      | Exact volume filled immediately upon reception.                              |
| **Average Filled Processing Price**  | Execution weight price (Outputs N/A for resting limit books).                |

---

# 📝 Verification Logs & Exception Testing

All transaction states, payloads, and underlying failures are written down within *bot.log*.

## Successful Order Log Entry Sample

```
2026-06-09 11:45:12 - INFO - Orchestrating logic block for: MARKET BUY 0.001 BTCUSDT
2026-06-09 11:45:12 - INFO - Sending API request payload: {'symbol': 'BTCUSDT', 'side': 'BUY', 'type': 'MARKET', 'quantity': 0.001}
2026-06-09 11:45:13 - INFO - API Success Response received: {'orderId': 14507953910, 'status': 'NEW', 'symbol': 'BTCUSDT', 'executedQty': '0.0000', 'avgPrice': '0.00000'}
```

## Handled API Rejection Log Entry Sample
```
2026-06-09 11:50:04 - INFO - Sending API request payload: {'symbol': 'BTCUSDT', 'side': 'BUY', 'type': 'MARKET', 'quantity': 0.0001}
2026-06-09 11:50:04 - ERROR - Binance API Error: Status 400 - Filter failure: MIN_NOTIONAL
```

---

# 👤 Author

- **Name**: Diprajit Chakraborty
- **Role**: Full-Stack Web & Web3 Developer
