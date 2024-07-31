import requests
from load_dotenv import load_dotenv
import json
import os
import pandas as pd

load_dotenv()

# url = "https://data.alpaca.markets/v1beta1/screener/stocks/movers"

# headers = {
#     "accept": "application/json",
#     "APCA-API-KEY-ID": os.environ.get("API_KEY"),
#     "APCA-API-SECRET-KEY": os.environ.get("API_SECRET")
# }
# params = {
#     'top': 50
# }

# response = requests.get(url, headers=headers, params=params)

# print(json.dumps(response.json(), indent=2))

# with open("price_data.json", "w") as f:
#     f.write(json.dumps(response.json(), indent=2))


with open("dataset/price_data.json", "r") as f:
    data = json.load(f)


print(data["gainers"])
df_price = pd.DataFrame(data["gainers"])

filtered_df = df_price[(df_price['price'] > 1) & (df_price['price'] < 20)]
print(filtered_df)