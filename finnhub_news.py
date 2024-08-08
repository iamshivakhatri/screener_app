import finnhub
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('FINNHUB_API_KEY')

now = datetime.now()
start_date = now.strftime('%Y-%m-%d')
end_date = now.strftime('%Y-%m-%d')

finnhub_client = finnhub.Client(api_key=API_KEY)

news = finnhub_client.company_news('AAPL' , _from=start_date, to=end_date)

for article in news:
    print(f"Headline: {article['headline']}")
    print(f"Source: {article['source']}")
    print(f"Summary: {article['summary']}")
    print(f"URL: {article['url']}\n")
    print(f"related: {article['related']}\n")
