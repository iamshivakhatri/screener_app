from flask import Flask, render_template
import pandas as pd
import json
import finnhub
from datetime import datetime
import os
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()

FINNHUB_API_KEY = os.getenv('FINNHUB_API_KEY')

finnhub_client = finnhub.Client(api_key=FINNHUB_API_KEY)

news_cache = {}

app = Flask(__name__)
CORS(app)

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
    combined_set = set(list1) | set(list2)  # Combine both lists into a set to remove duplicates
    combined_list = list(combined_set)      # Convert the set back to a list
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
    global news_cache
    # news_cache = get_news(ticker_list)
    # print("This is news", news_cache)

    return render_template('index.html', gainers=gainers_filtered.to_dict(orient='records'), active=active_filtered.to_dict(orient='records'))



# @app.route('/try_page')
# def try_page():
#     return render_template('try.html')



if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)