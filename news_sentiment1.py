import argparse
import os
import json
import requests
from newspaper import Article
from transformers import pipeline

sent = pipeline('sentiment-analysis')

COINGECKO_NEWS_RSS = 'https://www.coindesk.com/arc/outboundfeeds/rss/'

def fetch_coindesk_headlines(limit=10):
    r = requests.get('https://www.coindesk.com/arc/outboundfeeds/rss/')
    # For simplicity we'll fallback to static list in case of parsing difficulty
    return []

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--out', default='outputs/sentiment.json')
    args = p.parse_args()
    os.makedirs(os.path.dirname(args.out), exist_ok=True)

    # placeholder: read headlines from top_coins snapshot and analyze coin names
    headlines = [
        'Bitcoin dips as ETF flows slow',
        'Ethereum upgrade scheduled',
        'Major exploit hits altcoin project'
    ]
    results = []
    for h in headlines:
        r = sent(h)
        results.append({'headline':h, 'sentiment':r})
    with open(args.out,'w') as f:
        json.dump(results, f, indent=2)
    print('Saved sentiment to', args.out)

