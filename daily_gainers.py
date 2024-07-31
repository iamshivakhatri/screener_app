import requests
import json
import pandas as pd
from load_dotenv import load_dotenv

load_dotenv()


# url = "https://yahoo-finance15.p.rapidapi.com/api/v1/markets/screener"

# querystring = {"list":"day_gainers"}

# headers = {
# 	"x-rapidapi-key": os.environ.get("RAPID_API_KEY"),
# 	"x-rapidapi-host": "yahoo-finance15.p.rapidapi.com"
# }

# response = requests.get(url, headers=headers, params=querystring)

# print(json.dumps(response.json(), indent=2))

# with open("daily_gainers.json", "w") as f:
#     f.write(json.dumps(response.json(), indent=2))

with open("daily_gainers.json", "r") as f:
    data = json.load(f)

df_daily_gainers = pd.DataFrame(data["body"])
# print(df_daily_gainers)
# Select only the columns related to price
price_related_columns = ['symbol', 'regularMarketPrice', 'regularMarketPreviousClose',
                         'regularMarketDayHigh', 'regularMarketDayLow', 'regularMarketChangePercent']
df_price_data = df_daily_gainers[price_related_columns]
print(df_price_data)