import requests
import pandas as pd

API_KEY = "6F3XHUOHPBBJI7QJ6F3XHUOHPBBJI7QJ"          # ← put your real key here
SYMBOL   = "IBM"
INTERVAL = "5min"

url = (
    "https://www.alphavantage.co/query"
    f"?function=TIME_SERIES_INTRADAY&symbol={SYMBOL}"
    f"&interval={INTERVAL}&apikey={API_KEY}"
)

data = requests.get(url).json()

# --- Convert the nested dict to a DataFrame ---------------------------------
# 1. Pull the “Time Series …” block
# 2. Flip the timestamps into rows (orient='index')
# 3. Rename columns to plain English
# 4. Make numbers float instead of strings
df = (
    pd.DataFrame.from_dict(data[f"Time Series ({INTERVAL})"], orient="index")
      .rename(columns=lambda c: c.split(". ")[1].title())   # “1. open” → “Open”
      .astype(float)
      .sort_index(ascending=False)                          # most‑recent first
)

df.index = pd.to_datetime(df.index, utc=False)              # give the index a real dtype
df.index.name = "Timestamp"

# --- Show the first few rows nicely -----------------------------------------
#print(df.head(10).to_string(float_format="%.2f"))

print(df.to_string(float_format="%.2f"))  # prints the whole thing


# Optional extras:
# df.to_csv("ibm_intraday.csv")            # save to CSV
# print(df.describe())                     # quick stats
