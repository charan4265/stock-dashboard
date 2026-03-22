import yfinance as yf
import pandas as pd
from loguru import logger
import time

def get_stock_info(ticker):
    logger.info(f"Fetching stock info for {ticker}")
    for attempt in range(3):
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            return {
                "name":       info.get("longName", ticker),
                "price":      info.get("currentPrice") or info.get("regularMarketPrice", 0),
                "change":     info.get("regularMarketChangePercent", 0),
                "market_cap": info.get("marketCap", 0),
                "pe_ratio":   info.get("trailingPE", 0),
                "52w_high":   info.get("fiftyTwoWeekHigh", 0),
                "52w_low":    info.get("fiftyTwoWeekLow", 0),
                "volume":     info.get("regularMarketVolume", 0),
                "sector":     info.get("sector", "N/A"),
                "country":    info.get("country", "N/A"),
                "summary":    info.get("longBusinessSummary", "N/A"),
            }
        except Exception as e:
            logger.warning(f"Attempt {attempt+1} failed: {e}")
            time.sleep(2)
    logger.error("All attempts failed — returning default values")
    return {
        "name": ticker, "price": 0, "change": 0,
        "market_cap": 0, "pe_ratio": 0, "52w_high": 0,
        "52w_low": 0, "volume": 0, "sector": "N/A",
        "country": "N/A", "summary": "Data temporarily unavailable. Please try again in a few minutes."
    }

def get_historical_data(ticker, period="6mo"):
    logger.info(f"Fetching historical data for {ticker} — period: {period}")
    for attempt in range(3):
        try:
            stock = yf.Ticker(ticker)
            df = stock.history(period=period)
            if df.empty:
                raise ValueError("Empty dataframe returned")
            df.reset_index(inplace=True)
            df["Date"] = pd.to_datetime(df["Date"]).dt.tz_localize(None)
            return df
        except Exception as e:
            logger.warning(f"Attempt {attempt+1} failed: {e}")
            time.sleep(2)
    logger.error("Returning empty dataframe")
    return pd.DataFrame()

def get_moving_averages(df):
    if df.empty:
        return df
    df["MA20"]  = df["Close"].rolling(window=20).mean()
    df["MA50"]  = df["Close"].rolling(window=50).mean()
    df["MA200"] = df["Close"].rolling(window=200).mean()
    return df

if __name__ == "__main__":
    info = get_stock_info("TCS.NS")
    print(info)
    df = get_historical_data("TCS.NS")
    print(df.tail())