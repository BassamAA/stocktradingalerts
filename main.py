import requests
from twilio.rest import Client



DAILY_FUNCTION = 'TIME_SERIES_INTRADAY'
SYMBOL = 'TSLA'
INTERVAL = '30min'
API_KEY = 'ROH2UM7WAQ8SZS7O'
STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

parameters = {
    'function' : 'TIME_SERIES_DAILY',
    'symbol' : 'TSLA',
    'apikey' : API_KEY,
}

response = requests.get(STOCK_ENDPOINT, params=parameters)
response.raise_for_status()
data = response.json()
imp = data['Time Series (Daily)']
arr = list(imp.items())
last_daily= arr[0][1]
last_close = float(last_daily['4. close'])
print(last_close)

before_last_daily = arr[1][1]
before_last_close = float(before_last_daily['4. close'])
print(before_last_close)

difference = float(last_close) - float(before_last_close)

if difference < 0:
    difference = difference * -1

print(difference)

percentage_dif = 100 - 100*before_last_close/last_close
print(percentage_dif)

if percentage_dif > 5:
    print("Get News")

NEWS_API_KEY = 'ce35b96c2c0d453191f8f5f6dc30d58a'
news_api_param = {
    'q':'tesla',
    # 'from':'2022-08-15',
    'sortBy':'publishedAt',
    'apikey':NEWS_API_KEY,
    'language' : 'en'
}

news_data = requests.get('https://newsapi.org/v2/everything',params=news_api_param).json()
news_data = news_data['articles']
news_data = list(news_data)


if percentage_dif > 5:
    print(news_data)

first_3articles = news_data[0:18]


smslist = [i['title'] and i['description'] for i in first_3articles]

for i in smslist:
    print(i)


account_sid = 'AC4683d84226f168e7f1f536343c76bd8c'
auth_token = '9062872c426e7a599dc6832c2e03e0e0'
client = Client(account_sid, auth_token)
if percentage_dif > 0:
    percentage_string = '🔺'+str(percentage_dif)+'%'
else:
    percentage_string = '🔻' + str(percentage_dif) + '%'
BODY = f'{SYMBOL}: {percentage_dif}'
for n in smslist:
    message = client.messages.create(
        from_='+16726480362',
        to='+14388664662',
        body= BODY + '\n' + n
    )


