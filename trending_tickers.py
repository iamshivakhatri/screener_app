import requests
import json
import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

print(os.getenv("RAPID_API_KEY"))

# Define the URL and parameters for the API request
url = "https://yahoo-finance15.p.rapidapi.com/api/v1/markets/screener"
querystring = {"list": "trending"}

headers = {
    "x-rapidapi-key": os.getenv("RAPID_API_KEY"),
    "x-rapidapi-host": "yahoo-finance15.p.rapidapi.com"
}

# Make the API request
response = requests.get(url, headers=headers, params=querystring)

print(json.dumps(response.json(), indent=2))

# # Save the response data to a file
# with open("trending_tickers.json", "w") as f:
#     f.write(json.dumps(response.json(), indent=2))

# # Load the response data from the file
# with open("trending_tickers.json", "r") as f:
#     data = json.load(f)

# # Convert to DataFrame
# df_trending_tickers = pd.DataFrame(data["body"])

# # Select only the columns related to price
# price_related_columns = ['symbol', 'regularMarketPrice', 'regularMarketPreviousClose',
#                          'regularMarketDayHigh', 'regularMarketDayLow', 'regularMarketChangePercent']
# df_price_data = df_trending_tickers[price_related_columns]
# print(df_price_data)
