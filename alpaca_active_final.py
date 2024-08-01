import requests
import json
import os
import pandas as pd
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Define Alpaca API headers
alpaca_headers = {
    "accept": "application/json",
    "APCA-API-KEY-ID": os.environ.get("API_KEY"),
    "APCA-API-SECRET-KEY": os.environ.get("API_SECRET")
}

# Step 1: Retrieve most active stocks from Alpaca
most_active_stocks_url = "https://data.alpaca.markets/v1beta1/screener/stocks/most-actives"
most_active_stocks_params = {
    'by': 'volume',
    'top': 100
}
most_active_response = requests.get(most_active_stocks_url, headers=alpaca_headers, params=most_active_stocks_params)
most_active_data = most_active_response.json()

# Step 2: Convert most active stocks data to DataFrame
most_active_df = pd.DataFrame(most_active_data["most_actives"])

# Step 3: Prepare list of symbols for price data retrieval
symbols_list = most_active_df['symbol'].tolist()

# Step 4: Retrieve latest stock quotes from Alpaca
latest_quotes_url = "https://data.alpaca.markets/v2/stocks/quotes/latest"
latest_quotes_params = {
    'symbols': ",".join(symbols_list), 
    'feed': 'iex'
}
latest_quotes_response = requests.get(latest_quotes_url, headers=alpaca_headers, params=latest_quotes_params)
latest_quotes_data = latest_quotes_response.json()

# Step 5: Convert price data to DataFrame
latest_quotes_df = pd.DataFrame(latest_quotes_data["quotes"]).transpose().reset_index()

# Step 6: Merge the two DataFrames on the 'symbol' column
merged_df = pd.merge(most_active_df, latest_quotes_df, left_on='symbol', right_on='index')

# Step 7: Select relevant columns and rename for clarity
merged_df = merged_df[['symbol', 'volume', 'ap', 'bp', 't']]
merged_df = merged_df.rename(columns={'ap': 'ask_price', 'bp': 'bid_price', 't': 'timestamp'})

# Step 8: Convert timestamp column to datetime
merged_df['timestamp'] = pd.to_datetime(merged_df['timestamp'])

# Step 9: Filter stocks based on ask price
filtered_stocks_df = merged_df[(merged_df['ask_price'] > 1) & (merged_df['ask_price'] < 20)]

# Step 10: Sort filtered DataFrame by volume and reset index
filtered_stocks_df.sort_values(by='volume', ascending=False, inplace=True)
filtered_stocks_df = filtered_stocks_df.reset_index(drop=True)

# Step 11: Display the final filtered DataFrame
print(filtered_stocks_df)
