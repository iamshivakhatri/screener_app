import requests
import yfinance as yf
import pandas as pd
from concurrent.futures import ThreadPoolExecutor

def get_all_tickers(api_key):
    url = f"https://www.alphavantage.co/query?function=LISTING_STATUS&apikey={api_key}"
    response = requests.get(url)
    
    if response.status_code != 200:
        raise Exception("Error fetching data from Alpha Vantage API")
    
    tickers = response.text.split('\n')
    ticker_list = [line.split(',')[0] for line in tickers[1:] if line]
    
    return ticker_list

def fetch_stock_data(symbol):
    stock = yf.Ticker(symbol)
    data = stock.history(period='5d')
    return data

def screen_by_volume_increase(tickers):
    volume_data = []
    
    def process_ticker(ticker):
        try:
            data = fetch_stock_data(ticker)
            if not data.empty:
                current_volume = data['Volume'].iloc[-1]
                average_volume = data['Volume'].mean()
                relative_volume = current_volume / average_volume
                return ticker, current_volume, relative_volume
        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")
        return None

    with ThreadPoolExecutor(max_workers=10) as executor:
        results = executor.map(process_ticker, tickers)
    
    for result in results:
        if result:
            volume_data.append(result)
    
    sorted_volume_data = sorted(volume_data, key=lambda x: x[2], reverse=True)
    return sorted_volume_data[:10]

def screen_by_price_percentage_increase(tickers):
    price_data = []

    def process_ticker(ticker):
        try:
            data = fetch_stock_data(ticker)
            if not data.empty:
                current_price = data['Close'].iloc[-1]
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
    return sorted_price_data[:10]

# Replace 'YOUR_API_KEY' with your actual Alpha Vantage API key
api_key = 'YOUR_API_KEY'
tickers = get_all_tickers(api_key)

print("Top 10 Stocks by Volume Increase:")
volume_increase_stocks = screen_by_volume_increase(tickers)
for stock in volume_increase_stocks:
    print(stock)

print("Top 10 Stocks by Price Percentage Increase:")
price_percentage_increase_stocks = screen_by_price_percentage_increase(tickers)
for stock in price_percentage_increase_stocks:
    print(stock)
