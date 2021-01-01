# Code snippet for extracting adjusted close price data using pandas-datareader
# and calculating some basic statistical functions on this

import datetime as dt
import pandas as pd
import pandas_datareader.data as pdr

tickers = ['MSFT', 'AMZN', 'AAPL', 'CSCO', 'IBM', 'FB']

close_prices = pd.DataFrame()
drop = []
attempt = 0
# Initialise list to store tickers whose close price was successfully extracted

while len(tickers) != 0 and attempt <= 5:
    tickers = [j for j in tickers if j not in drop]
    for i in range(len(tickers)):
        try:
            temp = pdr.get_data_yahoo(tickers[i], dt.date.today() - dt.timedelta(3650), dt.date.today())
            temp.dropna(inplace=True)
            close_prices[tickers[i]] = temp['Adj Close']
            drop.append(tickers[i])
        except:
            print(tickers[i], ' failed to fetch data...retrying')
            continue
    attempt += 1

# Handle NaN values
close_prices.fillna(method='bfill', axis=0, inplace=True)
close_prices.dropna()

# Mean, median, standard deviation, daily return
close_prices.mean()
close_prices.median()
close_prices.std()

daily_return = close_prices.pct_change()
daily_return.mean()
daily_return.std()

# Simple moving average and standard deviation
daily_return.rolling(window=20).mean()
daily_return.rolling(window=20).std()

# Exponential weighted mean and standard deviation
daily_return.ewm(span=20, min_periods=20).mean()
daily_return.ewm(span=20, min_periods=20).std()
