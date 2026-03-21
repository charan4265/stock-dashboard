import requests
import os
from dotenv import load_dotenv
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from loguru import logger
from datetime import datetime

load_dotenv()
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

analyzer = SentimentIntensityAnalyzer()

def get_news(company_name, num_articles=10):
    logger.info(f"Fetching news for {company_name}")
    url = (
        f"https://newsapi.org/v2/everything?"
        f"q={company_name}&"
        f"language=en&"
        f"sortBy=publishedAt&"
        f"pageSize={num_articles}&"
        f"apiKey={NEWS_API_KEY}"
    )
    response = requests.get(url)
    if response.status_code != 200:
        logger.error(f"NewsAPI error: {response.status_code}")
        return []
    articles = response.json().get("articles", [])
    logger.success(f"Fetched {len(articles)} articles")
    return articles

def analyse_sentiment(text):
    scores = analyzer.polarity_scores(text)
    compound = scores["compound"]
    if compound >= 0.05:
        return "Positive", compound, "🟢"
    elif compound <= -0.05:
        return "Negative", compound, "🔴"
    else:
        return "Neutral", compound, "🟡"

def get_news_with_sentiment(company_name, num_articles=10):
    articles = get_news(company_name, num_articles)
    results = []
    for article in articles:
        title       = article.get("title", "") or ""
        description = article.get("description", "") or ""
        text        = title + " " + description
        sentiment, score, emoji = analyse_sentiment(text)
        results.append({
            "title":       title,
            "source":      article.get("source", {}).get("name", "Unknown"),
            "url":         article.get("url", ""),
            "published":   article.get("publishedAt", "")[:10],
            "sentiment":   sentiment,
            "score":       round(score, 3),
            "emoji":       emoji,
            "description": description,
        })
    return results

if __name__ == "__main__":
    results = get_news_with_sentiment("TCS India")
    for r in results[:3]:
        print(r["emoji"], r["sentiment"], f"({r['score']})", "|", r["title"][:60])
