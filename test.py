from alpha_vantage.timeseries import TimeSeries
import requests

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
print(tickers[:10])
