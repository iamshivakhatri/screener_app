import requests
import json
import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables from .env file
# load_dotenv()

# # Define the URL and parameters for the API request
# url = "https://yahoo-finance15.p.rapidapi.com/api/v1/markets/screener"
# querystring = {"list": "trending"}

# headers = {
#     "x-rapidapi-key": os.getenv("RAPID_API_KEY"),
#     "x-rapidapi-host": "yahoo-finance15.p.rapidapi.com"
# }

# # Make the API request
# response = requests.get(url, headers=headers, params=querystring)

# print(json.dumps(response.json(), indent=2))

# # Save the response data to a file
# with open("trending_tickers.json", "w") as f:
#     f.write(json.dumps(response.json(), indent=2))

# Load the response data from the file
with open("dataset/trending_tickers.json", "r") as f:
    data = json.load(f)

ticker_list = data["body"]

df = pd.DataFrame(ticker_list)

df.columns = ['Stock']
# df.to_csv('data/trending.csv', index=False)
print(df)
