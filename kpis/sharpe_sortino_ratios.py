# Continues from CAGR and volatility calculations

import datetime as dt
import numpy as np
import yfinance as yf

ticker = 'AAPL'
snp = yf.download(ticker, dt.date.today() - dt.timedelta(1825), dt.datetime.today())


def sharpe_ratio(df_original, rf):
    """Function to calculate Sharpe ratio; rf is the risk free rate."""
    df = df_original.copy()
    sharpe = (cagr(df)-rf) / volatility(df)
    return sharpe_ratio


def sortino_ratio(df_original, rf):
    """Function to calculate Sortino ratio; rf is the risk free rate."""
    df = df_original.copy()
    df['daily_return'] = df_original['Adj Close'].pct_change()
    df['neg_return'] = np.where(df['daily_return'] < 0, df['daily_return'], 0)
    neg_vol = df['neg_return'].std() * np.sqrt(252)
    sortino = (cagr(df) - rf) / neg_vol
    return sortino_ratio
