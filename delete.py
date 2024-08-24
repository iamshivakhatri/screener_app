import threading
import schedule
import time
import requests
import os
from dotenv import load_dotenv

load_dotenv()
# Global dictionary to store data for each interval
time_series_data = {
    '1min': [],
    '5min': [],
    '1hour': [],
    '1day': []

}

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

# Send GET request to the API
    response = requests.get(url, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None


def job(interval, ticker_list):
    global time_series_data
    data = fetch_time_series_data(ticker_list, interval)
    time_series_data[interval].append(data)
    print(f"Fetched and stored data for {interval}: {data}")

def schedule_time_series_data_fetch(ticker_list):
    schedule.every(1).minutes.do(job, interval='1min', ticker_list=ticker_list)
    schedule.every(5).minutes.do(job, interval='5min', ticker_list=ticker_list)
    schedule.every().hour.do(job, interval='1h', ticker_list=ticker_list)
    schedule.every().day.at("00:00").do(job, interval='1day', ticker_list=ticker_list)  # Fetch daily data at midnight

    print("Data fetching is scheduled.")

    while True:
        schedule.run_pending()
        time.sleep(1)  # Sleep to prevent busy-waiting

def start_threaded_schedule(ticker_list):
    t1 = threading.Thread(target=schedule_time_series_data_fetch, args=(ticker_list,))
    t1.daemon = True  # Allows thread to exit when the main program exits
    t1.start()

if __name__ == "__main__":
    gainer_tickers_list = ['AAPL', 'TSLA']
    active_ticker_list = ['MSFT', 'GOOGL']
    ticker_list = gainer_tickers_list + active_ticker_list  # Combine the lists

    # Start the scheduling thread
    start_threaded_schedule(ticker_list)

    # Main thread doing its own work
    while True:
        print("Main thread is running simultaneously.")
        time.sleep(10)  # Simulate some ongoing work in the main thread
