import datetime as dt
import numpy as np
import yfinance as yf

ticker = 'AAPL'
SnP = yf.download(ticker, dt.date.today() - dt.timedelta(1825), dt.datetime.today())


def max_dd(df_original):
    """Function to calculate maximum drawdown."""
    df = df_original.copy()
    df['daily_return'] = df_original['Adj Close'].pct_change()
    df['cumulative_return'] = (1 + df['daily_return']).cumprod()
    df['cumulative_roll_max'] = df['cumulative_return'].cummax()
    df['drawdown'] = df['cumulative_roll_max'] - df['cumulative_return']
    df['drawdown_pct'] = df['drawdown'] / df['cumulative_roll_max']
    max_dd = df['drawdown_pct'].max()
    return max_dd


def calmar(df_original):
    """Function to calculate Calmar ratio."""
    df = df_original.copy()
    calmar = cagr(df) / max_dd(df)
    return calmar
