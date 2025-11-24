#!/usr/bin/env python3
import requests
import pandas as pd
import datetime as dt
import time
import os

# -----------------------------------
# CONFIG
# -----------------------------------
OUTPUT_PARQUET = "prices_daily.parquet"
OUTPUT_CSV = "prices_daily.csv"
OUTPUT_JSON = "prices_daily.json"
TOP_N = 50  # number of cryptocurrencies
VS_CURRENCY = "usd"
COINGECKO_API = "https://api.coingecko.com/api/v3"

# -----------------------------------
# GET TOP COINS BY MARKET CAP
# -----------------------------------
def get_top_coins(n=TOP_N):
    url = f"{COINGECKO_API}/coins/markets"
    params = {
        "vs_currency": VS_CURRENCY,
        "order": "market_cap_desc",
        "per_page": n,
        "page": 1
    }
    r = requests.get(url, params=params)
    r.raise_for_status()
    coins = r.json()
    return [c["id"] for c in coins]

# -----------------------------------
# GET HISTORICAL PRICES FOR EACH COIN
# -----------------------------------
def get_historical_prices(coin_id, days=90):
    url = f"{COINGECKO_API}/coins/{coin_id}/market_chart"
    params = {"vs_currency": VS_CURRENCY, "days": days}
    r = requests.get(url, params=params)
    r.raise_for_status()
    data = r.json()
    prices = data.get("prices", [])

    rows = []
    for timestamp, price in prices:
        dt_obj = dt.datetime.utcfromtimestamp(timestamp / 1000).date()
        rows.append({"date": dt_obj, "coin": coin_id, "price": price})
    return rows

# -----------------------------------
# MAIN INGEST FUNCTION
# -----------------------------------
def generate_parquet():
    print("Fetching top coins...")
    coins = get_top_coins()
    print(f"Top {len(coins)} coins retrieved.")

    all_rows = []
    for coin in coins:
        print(f"Fetching history for: {coin} ...")
        try:
            coin_data = get_historical_prices(coin, days=90)
            all_rows.extend(coin_data)
        except Exception as e:
            print(f"Failed for {coin}: {e}")
        time.sleep(1)  # avoid API rate-limit

    print("Converting to DataFrame...")
    df = pd.DataFrame(all_rows)

    print("Pivoting to daily price matrix...")
    df_pivot = df.pivot_table(index="date", columns="coin", values="price")

    print("Saving to Parquet...")
    df_pivot.to_parquet(OUTPUT_PARQUET)

    print("Saving CSV copy...")
    df_pivot.to_csv(OUTPUT_CSV)

    print("Saving JSON copy...")
    df_pivot.to_json(OUTPUT_JSON, orient="index")

    print("\n----------------------------------------")
    print(f"Data ingestion complete!")
    print(f"Saved files:\n- {OUTPUT_PARQUET}\n- {OUTPUT_CSV}\n- {OUTPUT_JSON}")
    print("----------------------------------------")

# -----------------------------------
# RUN SCRIPT
# -----------------------------------
if __name__ == "__main__":
    generate_parquet()

