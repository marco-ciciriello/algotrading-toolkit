import datetime as dt
import numpy as np
import yfinance as yf

ticker = 'AAPL'
snp = yf.download(ticker, dt.date.today() - dt.timedelta(1825), dt.datetime.today())


def volatility(df_original):
    """Function to calculate annualised volatility of a strategy."""
    df = df_original.copy()
    df['daily_ret'] = df_original['Adj Close'].pct_change()
    # Calculate daily volatility (252 trading days in year)
    vol = df['daily_ret'].std() * np.sqrt(252)
    return vol
