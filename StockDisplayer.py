import matplotlib.pyplot as plt
import requests
from datetime import datetime, timedelta
import sys

symbol = input("Enter stock symbol: ")  


url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey='' "

#for getting data:
response = requests.get(url)
data = response.json()

if 'Error Message' in data:
    print("Stock not found ")
    sys.exit()

if 'Time Series (Daily)' not in data:
    print("No data available ")
    sys.exit()
print("Please check for graph")


#for procesing:
dates = list(data['Time Series (Daily)'].keys())
closing_prices = [float(data['Time Series (Daily)'][date]['4. close']) for date in dates]


dates = [datetime.strptime(date, '%Y-%m-%d') for date in dates]
end_date = max(dates)
start_date = end_date - timedelta(days=7)
filtered_dates, filtered_closing_prices = zip(*[
    (date, price) for date, price in zip(dates, closing_prices) if start_date <= date <= end_date
])
filtered_dates, filtered_closing_prices = zip(*sorted(zip(filtered_dates, filtered_closing_prices)))

#for plotting:
plt.figure(figsize=(10, 6))
plt.plot(filtered_dates, filtered_closing_prices, marker='o', linestyle='-', color='b')
plt.title(f'{symbol} Daily Closing Prices for the Last Week')
plt.xlabel('Date')
plt.ylabel('Closing Price')
plt.xticks(rotation=45)
plt.grid(True)
plt.show()
