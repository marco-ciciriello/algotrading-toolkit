import datetime as dt
import numpy as np
import yfinance as yf

ticker = 'AAPL'
snp = yf.download(ticker, dt.date.today() - dt.timedelta(1825), dt.datetime.today())


def cagr(df_original):
    """Calculate the Cumulative Annual Growth Rate of a strategy."""
    df = df_original.copy()
    df['daily_return'] = df_original['Adj Close'].pct_change()
    df['cumulative_return'] = (1 + df['daily_return']).cumprod()
    n = len(df) / 252  # Number of trading days in a year (UK)
    cagr = (df['cumulative_return'][-1])**(1/n) - 1
    return cagr
