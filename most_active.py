import requests
import json
import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables from .env file
# load_dotenv()

# # Define the URL and parameters for the API request
# url = "https://yahoo-finance15.p.rapidapi.com/api/v1/markets/screener"
# querystring = {"list": "most_actives"}

# headers = {
#     "x-rapidapi-key": os.getenv("RAPID_API_KEY"),
#     "x-rapidapi-host": "yahoo-finance15.p.rapidapi.com"
# }

# # Make the API request
# response = requests.get(url, headers=headers, params=querystring)

# print(json.dumps(response.json(), indent=2))

# # Save the response data to a file
# with open("most_actives.json", "w") as f:
#     f.write(json.dumps(response.json(), indent=2))

#Load the response data from the file
with open("dataset/most_actives.json", "r") as f:
    data = json.load(f)

# Convert to DataFrame
df_most_actives = pd.DataFrame(data["body"])

# Select only the columns related to price
price_related_columns = ['symbol', 'regularMarketPrice', 'regularMarketPreviousClose',
                         'regularMarketDayHigh', 'regularMarketDayLow', 'regularMarketChangePercent']
df_price_data = df_most_actives[price_related_columns]
df_price_data.to_csv("data/most_actives.csv", index=False)
print(df_price_data)
