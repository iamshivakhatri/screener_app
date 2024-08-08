import requests
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('FINNHUB_API_KEY')
SYMBOL = 'AAPL'
URL = f'https://finnhub.io/api/v1/company-news'

now = datetime.now()
start_date = now.strftime('%Y-%m-%d')
end_date = now.strftime('%Y-%m-%d')

params = {
    'symbol': SYMBOL,
    'from': start_date,
    'to': end_date,
    'token': API_KEY,
}

response = requests.get(URL, params=params)
news = response.json()

for article in news:
    print(f"Headline: {article['headline']}")
    print(f"Source: {article['source']}")
    print(f"Summary: {article['summary']}")
    print(f"URL: {article['url']}\n")
