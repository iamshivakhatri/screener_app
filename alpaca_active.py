import requests
from load_dotenv import load_dotenv
import json
import os
import pandas as pd

load_dotenv()

# url = "https://data.alpaca.markets/v1beta1/screener/stocks/most-actives"

headers = {
    "accept": "application/json",
    "APCA-API-KEY-ID": os.environ.get("API_KEY"),
    "APCA-API-SECRET-KEY": os.environ.get("API_SECRET")
}
# params = {
#     'by': 'volume',
#     'top': 100
# }

# response = requests.get(url, headers=headers, params=params)

# print(json.dumps(response.json(), indent=2))

# with open("alpaca_active.json", "w") as f:
#     f.write(json.dumps(response.json(), indent=2))

# print(json.dumps(response.json(), indent=2))

# price_url = "https://data.alpaca.markets/v2/stocks/quotes/latest"



with open("alpaca_active.json", "r") as f:
    data = json.load(f)


# print(data["most_actives"])
df_stocks = pd.DataFrame(data["most_actives"])
print(df_stocks)

symbol_list = df_stocks['symbol'].tolist()
# print(symbol_list)

# price_params = {
#     'symbols': ",".join(symbol_list), 
#     'feed': 'iex'
# }

# response = requests.get(price_url, headers=headers, params=price_params)

# print(json.dumps(response.json(), indent=2))

# with open("alpaca_active_price.json", "w") as f:
#     f.write(json.dumps(response.json(), indent=2))


with open("alpaca_active_price.json", "r") as f:
    data = json.load(f)

# print(data["quotes"])
df_price = pd.DataFrame(data["quotes"])
df_price = df_price.transpose()
df_price.reset_index(inplace=True)



df_price.to_csv('test_transpose.csv', index=False)

print(df_price)

merged_df = pd.merge(df_stocks, df_price, left_on='symbol', right_on='index')
print(merged_df)

print(merged_df.columns)

merged_df = merged_df[['symbol', 'volume', 'ap',  'bp',
      't']]
print(merged_df)

merged_df = merged_df.rename(columns={'ap': 'ask_price', 'bp': 'bid_price', 't': 'timestamp'})
merged_df['timestamp'] = pd.to_datetime(merged_df['timestamp'])

filtered_df = merged_df[(merged_df['ask_price'] > 1) & (merged_df['ask_price'] < 20)]
filtered_df = filtered_df.reset_index(drop=True)
filtered_df.sort_values(by='volume', ascending=False, inplace=True)


print(filtered_df)