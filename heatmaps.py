# heatmaps.py
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# load historical price table (example: pivot of daily close with coins as columns)
prices = pd.read_parquet("prices_daily.parquet")  # index=Date

# compute returns for 24h and 7d
ret_1d = prices.pct_change(1).tail(1).T
ret_7d = prices.pct_change(7).tail(1).T

# Heatmap 24h
plt.figure(figsize=(8,6))
sns.heatmap(ret_1d, annot=True, fmt=".2%", cmap="RdYlGn", cbar=True)
plt.title("24h Return Heatmap")
plt.tight_layout()
plt.savefig("heatmap_24h.png")

# Correlation matrix (30-day rolling)
corr = prices.pct_change().rolling(30).corr().iloc[-len(prices.columns):]  # easier: compute full correlation
corr_mat = prices.pct_change().corr()
plt.figure(figsize=(10,8))
sns.heatmap(corr_mat, annot=False, cmap="coolwarm", vmin=-1, vmax=1)
plt.title("Correlation matrix (daily returns)")
plt.tight_layout()
plt.savefig("corr_matrix.png")

