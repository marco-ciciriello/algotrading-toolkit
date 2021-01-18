import datetime as dt
import pandas as pd
import yfinance as yf

ticker = 'AAPL'
ohlcv = yf.download(ticker, dt.date.today() - dt.timedelta(1825), dt.datetime.today())


def average_true_range(df_original, n):
    """Function to calculate True Range and Average True Range."""
    df = df_original.copy()
    # Take difference between daily high and daily low values
    df['H-L'] = abs(df['High'] - df['Low'])
    # Take difference between daily high and previous close
    df['H-PC'] = abs(df['High'] - df['Adj Close'].shift(1))
    # Take difference between daily low and previous close
    df['L-PC'] = abs(df['Low'] - df['Adj Close'].shift(1))
    # Take maxiumum value of these three to get the true range for stock's movement across two days
    df['TR'] = df[['H-L', 'H-PC', 'L-PC']].max(axis=1, skipna=False)
    # Take the rolling average of the true range values to get average true range
    df['ATR'] = df['TR'].rolling(n).mean()
    # In case of wanting to use exponential mean over simple mean - not recommended for ATR
    # df['ATR'] = df['TR'].ewm(span=n, adjust=False, min_periods=n).mean()
    df2 = df.drop(['H-L', 'H-PC', 'L-PC'], axis=1)
    return df2


def bollinger_band(df_original, n):
    """Function to calculate Bollinger Band."""
    df = df_original.copy()
    # Take simple rolling average
    df['MA'] = df['Adj Close'].rolling(n).mean()
    # Calculate upper and lower Bollinger bands
    # ddof=0 is required since we want to take the standard deviation of the
    # population and not sample
    df['BB_up'] = df['MA'] + 2 * df['Adj Close'].rolling(n).std(ddof=0)
    df['BB_dn'] = df['MA'] - 2 * df['Adj Close'].rolling(n).std(ddof=0)
    df['BB_width'] = df['BB_up'] - df['BB_dn']
    df.dropna(inplace=True)
    return df


# Visualising Bollinger Band of the stocks for last 100 data points
bollinger_band(ohlcv, 20).iloc[-100:, [-4, -3, -2]].plot(title='Bollinger Band')
