from flask import Flask, render_template
import pandas as pd
import json
import finnhub
from datetime import datetime
import os
from dotenv import load_dotenv
from flask_cors import CORS
import requests
import threading
import time
import schedule
from flask import jsonify



load_dotenv()

FINNHUB_API_KEY = os.getenv('FINNHUB_API_KEY')

finnhub_client = finnhub.Client(api_key=FINNHUB_API_KEY)

news_cache = {}

app = Flask(__name__)
CORS(app)

# Global dictionary to store data for each interval
time_series_data = {
    '1min': [],
    '5min': [],
    '1hour': [],
    '1day': []

}

# Counter to keep track of API hits
api_hit_counter = {
    '1min': 0,
    '5min': 0,
    '1h': 0,
    '1day': 0
}

def fetch_time_series_data(tickers, interval):
    global api_hit_counter
    
    # Increment the counter for the specific interval
    api_hit_counter[interval] += 1

    print(f"Fetching data for tickers: {tickers} with interval {interval}")
    print(f"API hits for interval '{interval}': {api_hit_counter[interval]}")
    api_key = os.getenv('twelve_api_2')

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
    # print("This is data in the job", data)
    time_series_data[interval].append(data)
    print(f"Fetched and stored data for {interval}")

def schedule_time_series_data_fetch(ticker_list):
    schedule.every(1).minutes.do(job, interval='1min', ticker_list=ticker_list)
    # schedule.every(5).minutes.do(job, interval='5min', ticker_list=ticker_list)
    # schedule.every().hour.do(job, interval='1h', ticker_list=ticker_list)
    # schedule.every().day.at("00:00").do(job, interval='1day', ticker_list=ticker_list)  # Fetch daily data at midnight

    print("Data fetching is scheduled.")

    # Manually trigger the first run of each job
    job(interval='1min', ticker_list=ticker_list)
    # job(interval='5min', ticker_list=ticker_list)
    # job(interval='1h', ticker_list=ticker_list)
    # job(interval='1day', ticker_list=ticker_list)

    while True:
        schedule.run_pending()
        time.sleep(1)  # Sleep to prevent busy-waiting

def start_threaded_schedule(ticker_list):
    t1 = threading.Thread(target=schedule_time_series_data_fetch, args=(ticker_list,))
    t1.daemon = True  # Allows thread to exit when the main program exits
    t1.start()

# Load data
def load_data():
    # Replace with your actual data loading logic
    # For example:
    df_day_gainers = pd.read_csv('data/day_gainers.csv')

    df_small_cap_gainers = pd.read_csv('data/small_cap_gainers.csv')
    df_most_actives = pd.read_csv('data/most_actives.csv')
    df_trending = pd.read_csv('data/trending.csv')
    df_undervalued_large_caps = pd.read_csv('data/undervalued_large_caps.csv')
    
    return {
        'day_gainers': df_day_gainers,
        'most_actives': df_most_actives,
        'trending': df_trending,
        'undervalued_large_caps': df_undervalued_large_caps,
        'small_cap_gainers': df_small_cap_gainers
    }

@app.route('/news/<ticker>')
def get_news_for_ticker(ticker):
    global news_cache
    news = news_cache.get(ticker, [])
    return news

def get_news(ticker_list):
    news = {}
    now = datetime.now()
    start_date = now.strftime('%Y-%m-%d')
    end_date = now.strftime('%Y-%m-%d')

    for ticker in ticker_list:
        news[ticker] = []
        company_news = finnhub_client.company_news(ticker, _from=start_date, to=end_date)
        for article in company_news:
            # news[ticker].append(article['summary'])
            news[ticker].append({
                'title': article['headline'],
                'summary': article['summary'],
                'url': article['url']
            })
    
    return news

def combine_lists(list1, list2):
    # Explicitly add 'TSLA' to the first list
    # if 'TSLA' not in list1:
    #     list1.append('TSLA')
    
    # Combine both lists into a set to remove duplicates
    combined_set = set(list1) | set(list2)
    
    # Convert the set back to a list
    combined_list = list(combined_set)
    combined_list = combined_list[0:6]
    combined_list.append('TSLA')


    return combined_list



@app.route('/')
def index():
    # Load and process the first dataset
    with open("fmp_gainers.json", "r") as f:
        gainers_data = json.load(f)
    gainers_df = pd.DataFrame(gainers_data)
    gainers_filtered = gainers_df[(gainers_df['price'] > 1) & (gainers_df['price'] < 20)]
    gainers_filtered = gainers_filtered.reset_index(drop=True)
    gainers_filtered = gainers_filtered.head(10)
    gainer_tickers_list = gainers_filtered['symbol'].tolist()
    print(gainer_tickers_list)

    # Load and process the second dataset
    with open("fmp_active.json", "r") as f:
        active_data = json.load(f)
    active_df = pd.DataFrame(active_data)
    active_filtered = active_df[( active_df['price'] > 1) & ( active_df['price'] < 20) & ( active_df['changesPercentage'] > 0)]
    active_filtered = active_filtered.reset_index(drop=True)
    active_ticker_list = active_filtered['symbol'].tolist()
    print(active_ticker_list)
    ticker_list = combine_lists(gainer_tickers_list, active_ticker_list)
    print("This is the list", ticker_list)
    global news_cache
    # news_cache = get_news(ticker_list)
    # print("This is news", news_cache)
    start_threaded_schedule(ticker_list)

    return render_template('index.html', gainers=gainers_filtered.to_dict(orient='records'), active=active_filtered.to_dict(orient='records'))



@app.route('/try_page')
def try_page():
    return render_template('try.html')

@app.route('/get_ticker_data/<interval>/<ticker>', methods=['GET'])
def get_ticker_data(interval, ticker):
    print("This is interval", interval, "This is ticker", ticker)


    global time_series_data

    # Get the list of data for the given interval
    interval_data = time_series_data.get(interval, [])
    print("This is interval data", len(interval_data))

    # If the interval data is empty, return an empty list
    if not interval_data:
        return jsonify([])
    
    with open("newfile.txt", "w") as f:
        f.write(json.dumps(interval_data, indent=4))

    # Iterate through the list to find the ticker data
    whole_data = interval_data[0]
    for stock_data in whole_data:
        print("This is stock data", stock_data)
        if ticker == stock_data:
            print("This data in get_ticker_data",len(whole_data[ticker]))
            return jsonify(whole_data[ticker]['values'])  # Return the data for the specified ticker

    # If ticker is not found, return an empty list
    return jsonify([])



if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)