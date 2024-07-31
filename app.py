from flask import Flask, render_template, request, jsonify
import yfinance as yf
import pandas as pd
from alpha_vantage.timeseries import TimeSeries

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/screen', methods=['POST'])
def screen():
    criteria = request.json
    min_price = criteria.get('min_price', 1)
    max_price = criteria.get('max_price', 20)
    min_volume = criteria.get('min_volume', 1000000)
    min_rel_volume = criteria.get('min_rel_volume', 5)
    
    tickers = get_tickers()  # Implement a function to get all stock tickers
    screened_stocks = []
    
    for ticker in tickers:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1d")
        if hist.empty:
            continue
        
        close_price = hist['Close'].iloc[-1]
        volume = hist['Volume'].iloc[-1]
        avg_volume = stock.info['averageVolume']
        rel_volume = volume / avg_volume if avg_volume else 0
        
        if min_price <= close_price <= max_price and volume >= min_volume and rel_volume >= min_rel_volume:
            stock_info = {
                'ticker': ticker,
                'price': close_price,
                'volume': volume,
                'rel_volume': rel_volume,
                'news': get_news(ticker),  # Implement a function to get news
                'float': stock.info['floatShares'],
            }
            if stock_info['float'] <= 20000000:  # Check float criteria
                screened_stocks.append(stock_info)
    
    screened_stocks.sort(key=lambda x: x['rel_volume'], reverse=True)
    return jsonify(screened_stocks[:10])

# Use finnhub API to get all stock tickers
def get_tickers():
    api_key = 'YOUR_FINNHUB_API_KEY'
    url = f'https://finnhub.io/api/v1/stock/symbol?exchange=US&token={api_key}'
    response = requests.get(url)
    data = response.json()
    tickers = [item['symbol'] for item in data if 'symbol' in item]
    return tickers

def get_news(ticker):
    # Placeholder: replace with actual logic to fetch news
    return f"News for {ticker}"

def get_all_tickers(api_key):
    # Define the Alpha Vantage endpoint for the symbol search
    url = f"https://www.alphavantage.co/query?function=LISTING_STATUS&apikey={api_key}"
    
    # Make the request to the API
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code != 200:
        raise Exception("Error fetching data from Alpha Vantage API")
    
    # Parse the response content
    tickers = response.text.split('\n')
    ticker_list = [line.split(',')[0] for line in tickers[1:] if line]  # Skip header and empty lines
    
    return ticker_list 

if __name__ == '__main__':
    app.run(debug=True)
