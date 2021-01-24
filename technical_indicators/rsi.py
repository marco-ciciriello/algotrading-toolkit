import datetime as dt
import numpy as np
import yfinance as yf

ticker = 'AAPL'
ohlcv = yf.download(ticker, dt.date.today() - dt.timedelta(1825), dt.datetime.today())


def rsi(df_original, n):
    """Function to calculate Relative Strength Index."""
    df = df_original.copy()
    # Find difference between today's and yesterday's close prices
    df['delta'] = df['Adj Close'] - df['Adj Close'].shift(1)
    # Update gain and loss columns daily
    df['gain'] = np.where(df['delta'] >= 0, df['delta'], 0)
    df['loss'] = np.where(df['delta'] < 0, abs(df['delta']), 0)
    avg_gain = []
    avg_loss = []
    gain = df['gain'].tolist()
    loss = df['loss'].tolist()

    # For each day of time period specified, populate avg_gain/loss lists
    for i in range(len(df)):
        if i < n:
            avg_gain.append(np.NaN)
            avg_loss.append(np.NaN)
        elif i == n:
            avg_gain.append(df['gain'].rolling(n).mean().tolist()[n])
            avg_loss.append(df['loss'].rolling(n).mean().tolist()[n])
        elif i > n:
            avg_gain.append(((n - 1) * avg_gain[i - 1] + gain[i]) / n)
            avg_loss.append(((n - 1) * avg_loss[i - 1] + loss[i]) / n)

    df['avg_gain'] = np.array(avg_gain)
    df['avg_loss'] = np.array(avg_loss)
    # Calculate relative strength
    df['RS'] = df['avg_gain'] / df['avg_loss']
    # Calculate relative strength index
    df['RSI'] = 100 - (100 / (1 + df['RS']))
    return df['RSI']


# # Calculating RSI without using loop
# def rsi(df_original, n):
#     """Function to calculate RSI."""
#     delta = df['Adj Close'].diff().dropna()
#     u = delta * 0
#     d = u.copy()
#     u[delta > 0] = delta[delta > 0]
#     d[delta < 0] = -delta[delta < 0]
#     # First value is average of gains
#     u[u.index[n - 1]] = np.mean(u[:n])
#     u = u.drop(u.index[:(n-1)])
#     # First value is average of losses
#     d[d.index[n - 1]] = np.mean(d[:n])
#     d = d.drop(d.index[:(n-1)])
#     rs = u.ewm(com=n, min_periods=n).mean() / d.ewm(com=n, min_periods=n).mean()
#     return 100 - (100 / (1 + rs))

rsi(ohlcv, 14)
