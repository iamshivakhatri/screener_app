import requests
import json
import pandas as pd
from load_dotenv import load_dotenv

load_dotenv()

# url = "https://yahoo-finance15.p.rapidapi.com/api/v1/markets/screener"

# querystring = {"list":"small_cap_gainers"}

# headers = {
# 	"x-rapidapi-key": os.environ.get("RAPID_API_KEY"),
# 	"x-rapidapi-host": "yahoo-finance15.p.rapidapi.com"
# }

# response = requests.get(url, headers=headers, params=querystring)

# print(json.dumps(response.json(), indent=2))

# with open("small_cap_gainers.json", "w") as f:
#     f.write(json.dumps(response.json(), indent=2))

with open("dataset/small_cap_gainers.json", "r") as f:
    data = json.load(f)

df_small_cap_gainers = pd.DataFrame(data["body"])
print(df_small_cap_gainers)
df_small_cap_gainers.to_csv('small_cap_gainers.csv', index=False)

# Select only the columns related to price
price_related_columns = ['symbol', 'regularMarketPrice', 'regularMarketPreviousClose',
                         'regularMarketDayHigh', 'regularMarketDayLow', 'regularMarketChangePercent']
df_price_data = df_small_cap_gainers[price_related_columns]
print(df_price_data)
# price_list = df_price_data['regularMarketPrice'].tolist()
# print(price_list)
print(df_price_data[(df_price_data['regularMarketPrice'] < 20) & (df_price_data['regularMarketPrice'] > 1)])

df_price_data = df_price_data[(df_price_data['regularMarketPrice'] < 20) & (df_price_data['regularMarketPrice'] > 1)]
df_price_data.sort_values(by='regularMarketChangePercent', ascending=False, inplace=True)
df_price_data.columns = ['symbol', 'Price', 'Previous Close',
                         'High', 'Low', 'Percent Change']
df_price_data.to_csv('data/small_cap_gainers.csv', index=False)
print(df_price_data)