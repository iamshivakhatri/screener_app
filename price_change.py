import requests
from load_dotenv import load_dotenv
import json
import os

load_dotenv()

url = "https://data.alpaca.markets/v1beta1/screener/stocks/movers"

headers = {
    "accept": "application/json",
    "APCA-API-KEY-ID": os.environ.get("API_KEY"),
    "APCA-API-SECRET-KEY": os.environ.get("API_SECRET")
}
params = {
    'top': 50
}

response = requests.get(url, headers=headers, params=params)

print(json.dumps(response.json(), indent=2))

with open("price_data.json", "w") as f:
    f.write(json.dumps(response.json(), indent=2))
