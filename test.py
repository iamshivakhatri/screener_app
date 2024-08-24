import os
from dotenv import load_dotenv
import requests

load_dotenv()

def fetch_time_series_data(tickers, interval):

    print(f"Fetching data for tickers: {tickers} with interval {interval}")
    api_key = os.getenv('twelve_api')

    # API endpoint
    url = 'https://api.twelvedata.com/time_series'

    tickers = ','.join(tickers)

    # Parameters for the API request
    params = {
        'apikey': api_key,
        'interval': interval,    
        'symbol': tickers,
        'outputsize': 1000       # Number of data points to retrieve (up to 1000)
    }
    response = requests.get(url, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None
 

gainer_tickers_list = ['AAPL', 'TSLA']
active_ticker_list = ['MSFT', 'GOOGL']
tickers = gainer_tickers_list + active_ticker_list 

data = fetch_time_series_data(tickers, '1min')  # Replace 'AAPL' with your desired tickers
print(data )