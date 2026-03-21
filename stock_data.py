import yfinance as yf
import pandas as pd
from loguru import logger

def get_stock_info(ticker):
    logger.info(f"Fetching stock info for {ticker}")
    stock = yf.Ticker(ticker)
    info = stock.info
    return {
        "name":          info.get("longName", ticker),
        "price":         info.get("currentPrice", 0),
        "change":        info.get("regularMarketChangePercent", 0),
        "market_cap":    info.get("marketCap", 0),
        "pe_ratio":      info.get("trailingPE", 0),
        "52w_high":      info.get("fiftyTwoWeekHigh", 0),
        "52w_low":       info.get("fiftyTwoWeekLow", 0),
        "volume":        info.get("regularMarketVolume", 0),
        "sector":        info.get("sector", "N/A"),
        "country":       info.get("country", "N/A"),
        "summary":       info.get("longBusinessSummary", "N/A"),
    }

def get_historical_data(ticker, period="6mo"):
    logger.info(f"Fetching historical data for {ticker} — period: {period}")
    stock = yf.Ticker(ticker)
    df = stock.history(period=period)
    df.reset_index(inplace=True)
    df["Date"] = pd.to_datetime(df["Date"]).dt.tz_localize(None)
    return df

def get_moving_averages(df):
    df["MA20"]  = df["Close"].rolling(window=20).mean()
    df["MA50"]  = df["Close"].rolling(window=50).mean()
    df["MA200"] = df["Close"].rolling(window=200).mean()
    return df

if __name__ == "__main__":
    info = get_stock_info("TCS.NS")
    print(info)
    df = get_historical_data("TCS.NS")
    print(df.tail())
