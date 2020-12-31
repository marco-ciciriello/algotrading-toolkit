# Code snippet for creating DataFrames for OHLCV and close price data using yfinance

import datetime as dt
import pandas as pd
import yfinance as yf

tickers = ['AMZN', 'MSFT', 'INTC', 'GOOG', 'INFY.NS', '3988.HK']

# Return data for 30 trading days before today
start = dt.datetime.today() - dt.timedelta(30)
end = dt.datetime.today()

# Create empty dictionary for OHLCV data. Key = ticker, value = DataFrame
ohlcv_data = {}

# Create empty DataFrame to take closing price data
closing_price_data = pd.DataFrame()

# Loop over tickers and create a DataFrame with all price data
for ticker in tickers:
    ohlcv_data[ticker] = yf.download(ticker, start, end)

# Loop over tickers and create a DataFrame with closing prices
for ticker in tickers:
    closing_price_data[ticker] = yf.download(ticker, start, end)['Adj Close']

# pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)
# pd.set_option('display.width', None)
# pd.set_option('display.max_colwidth', None)
# print(ohlcv_data)

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)
print(closing_price_data)
