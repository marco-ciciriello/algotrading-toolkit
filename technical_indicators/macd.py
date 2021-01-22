import datetime as dt
import matplotlib.pyplot as plt
import yfinance as yf

ticker = 'AAPL'
ohlcv = yf.download(ticker, dt.date.today() - dt.timedelta(1825), dt.datetime.today())


def macd(df_original, a, b, c):
    """Function to calculate MACD, typical values a = 12; b = 26, c = 9."""
    df = df_original.copy()
    # Fast and slow moving averages by taking exponential weighted mean
    df['MA_Fast'] = df['Adj Close'].ewm(span=a, min_periods=a).mean()
    df['MA_Slow'] = df['Adj Close'].ewm(span=b, min_periods=b).mean()
    # MACD line
    df['MACD'] = df['MA_Fast'] - df['MA_Slow']
    # Draw signal line
    df['Signal'] = df['MACD'].ewm(span=c, min_periods=c).mean()
    df.dropna(inplace=True)
    return df


# Visualisation - plotting MACD/signal along with close price and volume for last 100 data points
df = macd(ohlcv, 12, 26, 9)

plt.subplot(311)
plt.plot(df.iloc[-100:, 4])
plt.title(f'{ticker} Stock Price')
plt.xticks([])

plt.subplot(312)
plt.bar(df.iloc[-100:, 5].index, df.iloc[-100:, 5].values)
plt.title('Volume')
plt.xticks([])

plt.subplot(313)
plt.plot(df.iloc[-100:, [-2, -1]])
plt.title('MACD')
plt.legend(('MACD', 'Signal'), loc='lower right')

plt.show()

# Get the figure and the axes
fig, (ax0, ax1) = plt.subplots(nrows=2, ncols=1, sharex=True, sharey=False, figsize=(10, 6),
                               gridspec_kw={'height_ratios': [2.5, 1]})
df.iloc[-100:, 4].plot(ax=ax0)
ax0.set(ylabel='Adj Close')
df.iloc[-100:, [-2, -1]].plot(ax=ax1)
ax1.set(xlabel='Date', ylabel='MACD/Signal')
fig.suptitle('Stock Price with MACD', fontsize=14, fontweight='bold')
