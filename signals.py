import pandas as pd
from loguru import logger

def generate_signal(df, sentiment_score=0):
    if df is None or len(df) < 20:
        return "Not enough data", "⚪", "gray"

    latest_close = df["Close"].iloc[-1]
    ma20  = df["MA20"].iloc[-1]  if "MA20"  in df.columns else None
    ma50  = df["MA50"].iloc[-1]  if "MA50"  in df.columns else None

    score = 0

    if ma20 and latest_close > ma20:
        score += 1
    elif ma20 and latest_close < ma20:
        score -= 1

    if ma50 and latest_close > ma50:
        score += 1
    elif ma50 and latest_close < ma50:
        score -= 1

    prev_close = df["Close"].iloc[-2]
    if latest_close > prev_close:
        score += 1
    else:
        score -= 1

    if sentiment_score > 0.05:
        score += 1
    elif sentiment_score < -0.05:
        score -= 1

    logger.info(f"Signal score: {score}")

    if score >= 2:
        return "BUY",  "🟢", "green"
    elif score <= -2:
        return "SELL", "🔴", "red"
    else:
        return "HOLD", "🟡", "orange"

def get_price_change_summary(df):
    if df is None or len(df) < 2:
        return {}
    latest = df["Close"].iloc[-1]
    return {
        "1D":  round(((latest - df["Close"].iloc[-2])  / df["Close"].iloc[-2])  * 100, 2),
        "1W":  round(((latest - df["Close"].iloc[-5])  / df["Close"].iloc[-5])  * 100, 2) if len(df) >= 5  else 0,
        "1M":  round(((latest - df["Close"].iloc[-22]) / df["Close"].iloc[-22]) * 100, 2) if len(df) >= 22 else 0,
        "3M":  round(((latest - df["Close"].iloc[-66]) / df["Close"].iloc[-66]) * 100, 2) if len(df) >= 66 else 0,
    }