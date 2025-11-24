import time, requests, pandas as pd
import requests
import datetime as dte
import os

COINGECKO_API = "https://api.coingecko.com/api/v3"

def get_top_coins(limit=50):
    r = requests.get(f"{COINGECKO_API}/coins/markets", params={
        "vs_currency":"usd",
        "order":"market_cap_desc",
        "per_page":limit,
        "page":1,
        "sparkline":False,
        "price_change_percentage":"24h,7d"
    })
    r.raise_for_status()
    return pd.DataFrame(r.json())

if __name__ == "__main__":
    df = get_top_coins(30)
    # keep only relevant columns:
    df = df[["id","symbol","name","current_price","market_cap","total_volume",
             "price_change_percentage_24h_in_currency","price_change_percentage_7d_in_currency",
             "market_cap_change_percentage_24h"]]
    df.to_csv("top_coins_snapshot.csv", index=False)
    print(df.head())
