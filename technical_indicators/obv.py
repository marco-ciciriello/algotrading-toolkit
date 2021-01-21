import datetime as dt
import numpy as np
import yfinance as yf

ticker = 'AAPL'
ohlcv = yf.download(ticker, dt.date.today() - dt.timedelta(1825), dt.datetime.today())


def obv(df_original):
    """Function to calculate On Balance Volume."""
    df = df_original.copy()
    # Calculate whether market had an up day or a down day
    df['daily_return] = df['Adj Close'].pct_change()
    df['direction'] = np.where(df['daily_return'] >= 0, 1, -1)
    # Set first row in direction column to 0 (no previous day)
    df['direction'][0] = 0
    # Calculate adjusted volume and cumulative sum
    df['adj_volume'] = df['Volume'] * df['direction']
    df['obv'] = df['adj_volume'].cumsum()
    return df['obv']
