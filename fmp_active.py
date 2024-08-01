import requests
import json
import os
from dotenv import load_dotenv
import pandas as pd

# # Load environment variables
# load_dotenv()

# # Define FMP API key
# api_key = os.getenv("FMP_API_KEY")

# # Check if the API key is loaded correctly
# if not api_key:
#     print("API key is missing")
#     exit(1)

# # Define the endpoint for stock market gainers
# url = f'https://financialmodelingprep.com/api/v3/stock_market/gainers?apikey={api_key}'

# response = requests.get(url)

# # Check if the request was successful
# if response.status_code == 200:
#     data = response.json()
#     print(json.dumps(data, indent=2))

#     with open("fmp_active.json", "w") as f:
#         f.write(json.dumps(data, indent=2))
# else:
#     print(f"Error: {response.status_code} - {response.text}")

with open("fmp_active.json", "r") as f:
    data = json.load(f)

print(len(data))

df = pd.DataFrame(data)
print(df.head())
df_filtered = df[(df['price'] > 1) & (df['price'] < 20)]
print(df_filtered.head())