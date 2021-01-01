# Code snippet for extracting historical close price data using YahooFinancials

import datetime as dt
import pandas as pd

from yahoofinancials import YahooFinancials

tickers = ['AAPL', 'MSFT', 'CSCO', 'AMZN', 'INTC']

closing_prices = pd.DataFrame()
end_date = (dt.date.today()).strftime('%Y-%m-%d')
start_date = (dt.date.today() - dt.timedelta(253)).strftime('%Y-%m-%d')  # One trading year = 253 days

# Extract historical close price for all stocks identified
for ticker in tickers:
    yahoofinancials = YahooFinancials(ticker)
    json_return = yahoofinancials.get_historical_price_data(start_date, end_date, 'daily')
    ohlcv = json_return[ticker]['prices']
    temp_df = pd.DataFrame(ohlcv)[['formatted_date', 'adjclose']]
    temp_df.set_index('formatted_date', inplace=True)
    temp_df.dropna(inplace=True)
    closing_prices[ticker] = temp_df['adjclose']

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)
print(closing_prices)
