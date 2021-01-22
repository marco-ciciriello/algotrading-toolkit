import datetime as dt
import yfinance as yf

from stocktrends import Renko

ticker = 'AAPL'
ohlcv = yf.download(ticker, dt.date.today() - dt.timedelta(1825), dt.datetime.today())


def atr(df_original, n):
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
    # In case of wanting to use exponential mean over simple mean - not
    # recommended for ATR
    # df['ATR'] = df['TR'].ewm(span=n, adjust=False, min_periods=n).mean()
    df2 = df.drop(['H-L', 'H-PC', 'L-PC'], axis=1)
    return df2


def renko_df(df_original):
    """Function to convert OHLCV data into Renko bricks."""
    df = df_original.copy()
    df.reset_index(inplace=True)
    df = df.iloc[:, [0, 1, 2, 3, 5, 6]]
    df.rename(columns={'Date': 'date',
                       'High': 'high',
                       'Low': 'low',
                       'Open': 'open',
                       'Adj Close': 'close',
                       'Volume': 'volume'},
                       inplace=True)
    df2 = Renko(df)
    # Use average true range to determine brick size
    df2.brick_size = round(atr(df_original, 120)['ATR'][-1], 0)
    renko_df = df2.get_ohlc_data()
    return renko_df


renko_data = renko_df(ohlcv)
