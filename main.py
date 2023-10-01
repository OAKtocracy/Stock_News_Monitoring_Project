# STOCK TRADING NEWS ALERT
import requests
from twilio.rest import Client
import os

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"


STOCK_API_KEY = os.environ.get("Tesla_Stock_APIkey")

stock_parameters = {
    'function': 'TIME_SERIES_DAILY_ADJUSTED',
    'symbol': STOCK_NAME,
    'apikey': STOCK_API_KEY
                    }

# Use https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

# Get yesterday's closing stock price.
result = requests.get(STOCK_ENDPOINT, params=stock_parameters)
result.raise_for_status()
stock_data = result.json()

yesterday_closing_stock = float(stock_data['Time Series (Daily)']['2023-01-09']['4. close'])
print(yesterday_closing_stock)

# Get the day before yesterday's closing stock price
day_before_closing_stock = float(stock_data['Time Series (Daily)']['2023-01-06']['4. close'])
print(day_before_closing_stock)

# Find the positive difference between 1 and 2.
difference = yesterday_closing_stock - day_before_closing_stock
up_down = None
if difference > 0:
    up_down = '🔺'
else:
    up_down = '🔻'
    print(difference)

# Work out the percentage difference in price between closing price yesterday and closing price the day before yesterday
percent_diff = abs((difference*100)/yesterday_closing_stock)
print(percent_diff)

# If the above percentage is greater than 5 then print("Get News").

# https://newsapi.org/ :Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.

NEWS_API_KEY = os.environ.get("News_APIkey")
news_parameters = {'qInTitle': COMPANY_NAME,
                   'from': '2022-12-18',
                   'sortBy': 'publishedAt',
                   'apiKey': NEWS_API_KEY
                   }
global news_data, news_titles
if percent_diff >= 5:
    news_result = requests.get(NEWS_ENDPOINT, params=news_parameters)
    news_result.raise_for_status()
    news_data = news_result.json()
    news_titles = (news_data['articles'])

# Use Python slice operator to create a list that contains the first 3 articles.

    first_three_news = (news_titles[0: 3])
    print(first_three_news)

# Use twilio.com/docs/sm/quickstart/python to send a separate message to your phone number.

    three_titles = [f"Headline: {article['title']}. \nBrief: {article['description']}." for article in first_three_news]
    print(three_titles)

# Send each article as a separate message via Twilio.
    TWILIO_ACCOUNT_SID = os.environ.get("twilio_SID")

    TWILIO_AUTH_TOKEN = os.environ.get("twilio_token")

    from_number = os.environ.get("to")
    to_number = os.environ.get("from")

    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    for article in three_titles:
        message = client.messages.create(
            body=f" {STOCK_NAME}: {up_down}{percent_diff}% \n {article}",
            from_=from_number,
            to=to_number
        )
        print(message.status)
