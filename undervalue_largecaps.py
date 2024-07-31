import requests
import json
import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables from .env file
# load_dotenv()

# # Define the URL and parameters for the API request
# url = "https://yahoo-finance15.p.rapidapi.com/api/v1/markets/screener"
# querystring = {"list": "undervalued_large_caps"}

# headers = {
#     "x-rapidapi-key": os.getenv("RAPID_API_KEY"),
#     "x-rapidapi-host": "yahoo-finance15.p.rapidapi.com"
# }

# # Make the API request
# response = requests.get(url, headers=headers, params=querystring)

# print(json.dumps(response.json(), indent=2))

# # Save the response data to a file
# with open("undervalued_large_caps.json", "w") as f:
#     f.write(json.dumps(response.json(), indent=2))

# Load the response data from the file
with open("dataset/undervalued_large_caps.json", "r") as f:
    data = json.load(f)

# Convert to DataFrame
df_undervalued_large_caps = pd.DataFrame(data["body"])

# Select only the columns related to price
# price_related_columns = ['symbol', 'regularMarketPrice', 'regularMarketPreviousClose',
#                          'regularMarketDayHigh', 'regularMarketDayLow', 'regularMarketChangePercent']
# df_price_data = df_undervalued_large_caps[price_related_columns]
df_undervalued_large_caps.to_csv('data/undervalued_large_caps.csv', index=False)
print(df_undervalued_large_caps)

