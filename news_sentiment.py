# news_sentiment.py
from newspaper import Article
from transformers import pipeline
import requests

sentiment = pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment",framework="pt")

def fetch_article_text(url):
    art = Article(url)
    art.download()
    art.parse()
    return art.text

def analyze_text(text):
    s = sentiment(text[:512])  # or chunk
    return s
print(s)

# crawl headlines from CoinDesk + Reuters RSS, run classify

