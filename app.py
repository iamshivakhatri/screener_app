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
time_series_data1 = {
    '1min': [],
    '5min': [],
    '1hour': [],
    '1day': []
}

time_series_data2 = {
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

ticker_list1 = []
ticker_list2 = []

def fetch_time_series_data(tickers, interval, api):


    global api_hit_counter

    

    
    # Increment the counter for the specific interval
    api_hit_counter[interval] += 1

    print(f"Fetching data for tickers: {tickers} with interval {interval}")
    print(f"API hits for interval '{interval}': {api_hit_counter[interval]}")
    

    # API endpoint
    url = 'https://api.twelvedata.com/time_series'

    

    # TODO: FIX THIS WHEN YOU HOST IT.
    if interval == '1h' or interval == '1day':
        api_key = os.getenv('twelve_api_1h')
    elif api == 'one':
        api_key = os.getenv('twelve_api_2')
    else:
        api_key = os.getenv('twelve_api')



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


def job(interval, ticker_list, api):
    global time_series_data1
    global time_series_data2
    data = fetch_time_series_data(ticker_list, interval, api)
    # print("This is data in the job", data)

    # if interval == '1h' or interval == '1day':

    if interval == '1h':
        with open("1h_data.txt", "w") as f:
            f.write(json.dumps(data, indent=4))
    elif interval == '1day':
        with open("1day_data.txt", "w") as f:
            f.write(json.dumps(data, indent=4))
    elif interval == '1min':
        with open("1min_data.txt", "w") as f:
            f.write(json.dumps(data, indent=4))

    if api == 'one':
        time_series_data1[interval] = data
        print(f"Fetched and stored data for {interval} with api {api}")
    else:
        time_series_data2[interval] = data
        print(f"Fetched and stored data for {interval} with api {api}")
    

def schedule_time_series_data_fetch(ticker_list1, ticker_list2):
    schedule.every(1).minutes.do(job, interval='1min', ticker_list=ticker_list1, api = 'one')
    # schedule.every(5).minutes.do(job, interval='5min', ticker_list=ticker_list1, api = 'one')
    schedule.every().hour.at(":00").do(job, interval='1h', ticker_list=ticker_list1,  api = 'one')
    schedule.every().day.at("00:02").do(job, interval='1day', ticker_list=ticker_list1, api = 'one')  # Fetch daily data at midnight

    # TODO: Uncomment the following lines to fetch data for the second list
    # schedule.every(1).minutes.do(job, interval='1min', ticker_list=ticker_list2, api = 'two')
    # schedule.every(5).minutes.do(job, interval='5min', ticker_list=ticker_list2, api = 'two')
    schedule.every().hour.at(":01").do(job, interval='1h', ticker_list=ticker_list2, api = 'two')
    schedule.every().day.at("00:03").do(job, interval='1day', ticker_list=ticker_list2,api = 'two')  # Fetch daily data at midnight

    print("Data fetching is scheduled.")

    while True:
        schedule.run_pending()
        time.sleep(1)  # Sleep to prevent busy-waiting

def start_threaded_schedule(ticker_list1, ticker_list2):
    t1 = threading.Thread(target=schedule_time_series_data_fetch, args=(ticker_list1, ticker_list2 ))
    t1.daemon = True  # Allows thread to exit when the main program exits
    t1.start()

def trigger_initial_api_hits(ticker_list1, ticker_list2):
    # Manually trigger the first run of each job with a delay to respect the rate limit
    # Trigger minute data fetch
    print("1 min job")
    job(interval='1min', ticker_list=ticker_list1, api='one')
    # job(interval='1min', ticker_list=ticker_list2, api='two')

    # Trigger daily data fetch
    print("1 day job")
    job(interval='1day', ticker_list=ticker_list1, api='one')
    time.sleep(60)  # Wait 1 minute

    print("1 day job")
    job(interval='1day', ticker_list=ticker_list2, api='two')
    time.sleep(60)  # Wait 1 minute


    # Trigger hourly data fetch
    print("1 hour job")
    job(interval='1h', ticker_list=ticker_list1, api='one')

    print("1 hour job")
    time.sleep(60)  # Wait 1 minute
    job(interval='1h', ticker_list=ticker_list2, api='two')




    
    # time.sleep(60)  # Wait 1 minute

    start_threaded_schedule(ticker_list1, ticker_list2)

    

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
    global ticker_list1
    global ticker_list2
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
    ticker_list1 = gainer_tickers_list[:7]
    ticker_list1.append('TSLA')
    ticker_list2 = active_ticker_list[:7]



    # ticker_list = combine_lists(gainer_tickers_list, active_ticker_list)
    global news_cache
    # news_cache = get_news(ticker_list)
    # print("This is news", news_cache)

    # Manually trigger the initial API hits
    trigger_initial_api_hits(ticker_list1, ticker_list2)
    

    return render_template('index.html', gainers=gainers_filtered.to_dict(orient='records'), active=active_filtered.to_dict(orient='records'))



@app.route('/try_page')
def try_page():
    return render_template('try.html')

@app.route('/get_ticker_data/<interval>/<ticker>', methods=['GET'])
def get_ticker_data(interval, ticker):
    print("This is interval", interval, "This is ticker", ticker)


    global time_series_data1
    global time_series_data2
    global ticker_list1
    global ticker_list2

    print("This is ticker list 1", ticker_list1)
    print("This is ticker list 2", ticker_list2)


    if ticker in ticker_list1:
        time_series_data = time_series_data1
    else:
        time_series_data = time_series_data2

    with open("time_series_data.txt", "w") as f:
        f.write(json.dumps(time_series_data, indent=4))

    # Get the list of data for the given interval
    interval_data = time_series_data.get(interval, [])
 
    print("This is interval data", len(interval_data))


    # If the interval data is empty, return an empty list
    if not interval_data:
        return jsonify([])
    


    for stock_data in interval_data:
        print("This is stock data", stock_data)
        if ticker == stock_data:
            return jsonify(interval_data[ticker]['values'])  # Return the data for the specified ticker

    # If ticker is not found, return an empty list
    return jsonify([])



if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)