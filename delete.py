import requests
import json
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
import yfinance as yf
from load_dotenv import load_dotenv

load_dotenv()
# url = "https://data.alpaca.markets/v1beta1/screener/stocks/most-actives"


# headers = {
#     "accept": "application/json",
#     "APCA-API-KEY-ID": os.environ.get("API_KEY"),
#     "APCA-API-SECRET-KEY": os.environ.get("API_SECRET")
# }


# response = requests.get(url, headers=headers, params={"by": "volume", "top": 100})

# df = pd.DataFrame(response.json())

# with open("data.json", "w") as f:
#     f.write(json.dumps(response.json(), indent=2))

with open("data.json", "r") as f:
    data = json.load(f)

def fetch_stock_data(symbol):
    stock = yf.Ticker(symbol)
    data = stock.history(period='5d')
    return data

def screen_by_price_percentage_increase(tickers):
    price_data = []

    def process_ticker(ticker):
        try:
            data = fetch_stock_data(ticker)
            if not data.empty:
                current_price = data['Close'].iloc[-1]
                if 2 <= current_price <= 20:  # Price range filter
                    previous_close = data['Close'].iloc[-2]
                    price_percentage_change = ((current_price - previous_close) / previous_close) * 100
                    return ticker, current_price, price_percentage_change
        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")
        return None

    with ThreadPoolExecutor(max_workers=10) as executor:
        results = executor.map(process_ticker, tickers)
    
    for result in results:
        if result:
            price_data.append(result)
    
    sorted_price_data = sorted(price_data, key=lambda x: x[2], reverse=True)
    return sorted_price_data

# print(json.dumps(data.json(), indent=2))
df = pd.DataFrame(data)


new_df = df["most_actives"].apply(pd.Series)
df = pd.concat([(df.drop(columns =["most_actives"])), new_df], axis=1)


tickers = df['symbol'].tolist()
print(tickers)
stocks = screen_by_price_percentage_increase(tickers)
print(stocks)
df_price = pd.DataFrame(stocks, columns=["symbol", "current_price", "price_percentage_change"])
# print(df_price)


