from alpha_vantage.timeseries import TimeSeries
import requests
import yfinance as yf

def fetch_stock_data(symbol):
    stock = yf.Ticker(symbol)
    data = stock.history(period='5d')  # Fetch last 2 days of data
    return data

def screen_by_volume_increase(tickers):
    volume_data = []
    for ticker in tickers:
        try:
            print(f"Fetching data for {ticker} ***")
            data = fetch_stock_data(ticker)
            current_volume = data['Volume'].iloc[-1]
            average_volume = data['Volume'].mean()
            relative_volume = current_volume / average_volume
            print(f"Downloaded data for {ticker}: {current_volume}, {average_volume}, {relative_volume}")
            volume_data.append((ticker, current_volume, relative_volume))
            
        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")
    sorted_volume_data = sorted(volume_data, key=lambda x: x[2], reverse=True)
    return sorted_volume_data[:10]

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

# Replace 'YOUR_API_KEY' with your actual Alpha Vantage API key
api_key = 'YOUR_API_KEY'
tickers = get_all_tickers(api_key)

# Print the first 10 tickers as an example
print(tickers[:100])
print(len(tickers))


volume_increase_stocks = screen_by_volume_increase(tickers)

# Print the top 10 stocks by volume increase
print("Top 10 Stocks by Volume Increase:")
for stock in volume_increase_stocks[:10]:
    print(stock)
