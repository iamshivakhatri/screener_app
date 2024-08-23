import requests
import matplotlib.pyplot as plt
import json
import os
from dotenv import load_dotenv

load_dotenv()

# Your API key here
api_key = os.getenv('twelve_api')

# API endpoint
url = 'https://api.twelvedata.com/time_series'

# Parameters for the API request
params = {
    'apikey': api_key,
    'interval': '1h',     # 1-minute interval
    'symbol': 'TSLA',
    'outputsize': 1000       # Number of data points to retrieve (up to 1000)
}

# Send GET request to the API
response = requests.get(url, params=params)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()
    print(json.dumps(data, indent=2))
    with open("1hour.json", "w") as f:
        f.write(json.dumps(data, indent=2))

#     # Check if data is available
#     if 'values' in data:
#         # Extracting data
#         dates = [item['datetime'] for item in data['values']]
#         closing_prices = [float(item['close']) for item in data['values']]

#         # Reverse the lists to ensure the data is in chronological order
#         dates.reverse()
#         closing_prices.reverse()

#         # Plotting the data
#         plt.figure(figsize=(10, 5))
#         plt.plot(dates, closing_prices, marker='o')
#         plt.title('TSLA 1-Minute Interval Closing Prices')
#         plt.xlabel('Date and Time')
#         plt.ylabel('Closing Price (USD)')
#         plt.xticks(rotation=45)
#         plt.grid(True)
#         plt.tight_layout()
#         plt.show()
#     else:
#         print("No data available.")
# else:
#     print(f"Error: {response.status_code} - {response.text}")
