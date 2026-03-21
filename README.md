# 📈 Stock Market Intelligence Dashboard

A real-time stock market intelligence dashboard built with Python that provides live stock data, candlestick charts, news sentiment analysis, and AI-powered Buy/Hold/Sell signals.

## 🌐 Live Demo
👉 **[stock-dashboard-live.streamlit.app](https://stock-dashboard-live.streamlit.app)**

## 📸 Screenshots

### Stock Overview
![Stock Overview](screenshots/overview.png)

### Candlestick Chart
![Candlestick Chart](screenshots/candlestick.png)

### News & Sentiment
![News Sentiment](screenshots/sentiment.png)

### Buy / Sell Signal
![Signal](screenshots/signal.png)

## ✨ Features

- 📊 **Stock Overview** — Live price, day change, 52W high/low, market cap, P/E ratio
- 🕯️ **Candlestick Charts** — Professional OHLC charts with MA20 and MA50 indicators
- 📰 **News & Sentiment** — Live news articles with VADER NLP sentiment scoring
- 🤖 **Buy/Hold/Sell Signal** — AI signal based on moving averages + price trend + news sentiment
- 🔄 **Multi-Stock Comparison** — Compare any 2 stocks side by side with normalised chart
- 📉 **Price Returns** — 1D, 1W, 1M, 3M return analysis with color coded bar chart
- 🌙 **Dark Theme** — Professional dark trading terminal UI

## 🛠️ Tech Stack

| Library | Purpose |
|---|---|
| `yfinance` | Fetch live stock data from Yahoo Finance |
| `streamlit` | Build the interactive web dashboard |
| `plotly` | Candlestick charts, bar charts, comparison charts |
| `pandas` | Data manipulation and analysis |
| `numpy` | Moving average calculations |
| `vaderSentiment` | NLP sentiment analysis on news articles |
| `newsapi-python` | Fetch live financial news from 150,000+ sources |
| `python-dotenv` | Secure API key management |
| `loguru` | Pipeline logging and monitoring |

## 📁 Project Structure
```
stock_dashboard/
│
├── stock_data.py        # Fetch live stock data using yfinance
├── news_sentiment.py    # Fetch news + VADER sentiment analysis
├── signals.py           # Generate Buy/Hold/Sell signals
├── dashboard.py         # Main Streamlit multi-page dashboard
├── .env                 # API keys (not pushed to GitHub)
├── requirements.txt     # All library versions
└── README.md            # Project documentation
```

## 🚀 How to Run Locally

**Step 1 — Clone the repository**
```bash
git clone https://github.com/charan4265/stock-dashboard.git
cd stock-dashboard
```

**Step 2 — Create virtual environment**
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

**Step 3 — Install all libraries**
```bash
pip install -r requirements.txt
```

**Step 4 — Add your API key**

Create a `.env` file in the project folder:
```
NEWS_API_KEY=your_newsapi_key_here
```

Get your free NewsAPI key at [newsapi.org](https://newsapi.org)

**Step 5 — Run the dashboard**
```bash
streamlit run dashboard.py
```

Open your browser at `http://localhost:8501`

## 📊 Supported Stocks

### Indian Stocks (NSE)
| Company | Ticker |
|---|---|
| Tata Consultancy Services | TCS.NS |
| Infosys | INFY.NS |
| Reliance Industries | RELIANCE.NS |
| Wipro | WIPRO.NS |
| HDFC Bank | HDFCBANK.NS |

### US Stocks
| Company | Ticker |
|---|---|
| Apple | AAPL |
| Tesla | TSLA |
| Microsoft | MSFT |
| Google | GOOGL |
| Amazon | AMZN |

> You can also type any custom ticker in the sidebar — e.g. `ZOMATO.NS`, `NFLX`, `TATAMOTORS.NS`

## 🤖 How the Signal Works

The Buy/Hold/Sell signal is calculated using 4 factors:

| Factor | Bullish | Bearish |
|---|---|---|
| Price vs MA20 | Price above MA20 | Price below MA20 |
| Price vs MA50 | Price above MA50 | Price below MA50 |
| 1-Day Price Move | Price went up today | Price went down today |
| News Sentiment | Positive news score | Negative news score |

- Score ≥ 2 → 🟢 **BUY**
- Score ≤ -2 → 🔴 **SELL**
- Otherwise → 🟡 **HOLD**

> ⚠️ This is for educational purposes only. Not real financial advice.

## 🧠 What I Learned

- How to fetch real-time stock data using `yfinance`
- How to build professional candlestick charts with Plotly
- How to perform NLP sentiment analysis using VADER on financial news
- How to generate trading signals using technical indicators
- How to build a multi-page Streamlit dashboard with custom dark theme
- How to integrate multiple APIs (Yahoo Finance + NewsAPI) in one app
- How to deploy a Python app on Streamlit Cloud with secret management

## 🙋 Author

**Charan** — Python Developer  
GitHub: [@charan4265](https://github.com/charan4265)  
Live App: [stock-dashboard-live.streamlit.app](https://stock-dashboard-live.streamlit.app)

