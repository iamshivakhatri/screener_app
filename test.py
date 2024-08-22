import requests
from dotenv import load_dotenv
import os

# Load API credentials from .env file
load_dotenv()

API_KEY = os.environ.get("API_KEY")
API_SECRET = os.environ.get("API_SECRET")

print("API Key:", API_KEY)
print("API Secret:", API_SECRET)

# The base URL for the Alpaca data API
BASE_URL = 'https://data.alpaca.markets/v2/stocks'

# The stock symbol you want to fetch data for
SYMBOL = 'AAPL'

# The timeframe for the bars ('1Min', '5Min', '15Min', 'day')
TIMEFRAME = '1Min'

# The number of bars you want to retrieve
LIMIT = 10000

# The endpoint URL with the necessary parameters
url = f"{BASE_URL}/{SYMBOL}/bars?timeframe={TIMEFRAME}&limit={LIMIT}"

# The headers for authentication
headers = {
    'APCA-API-KEY-ID': API_KEY,
    'APCA-API-SECRET-KEY': API_SECRET
}

# Make the API request
response = requests.get(url, headers=headers)

print("This is response:", response)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()
    print(f"Data for {SYMBOL} ({TIMEFRAME} timeframe):")
    for bar in data['bars']:
        print(f"Time: {bar['t']}, Open: {bar['o']}, High: {bar['h']}, Low: {bar['l']}, Close: {bar['c']}, Volume: {bar['v']}")
else:
    print(f"Error: {response.status_code} - {response.text}")
