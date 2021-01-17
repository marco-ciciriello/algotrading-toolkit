import datetime as dt
import numpy as np
import yfinance as yf

ticker = 'AAPL'
ohlcv = yf.download(ticker, dt.date.today() - dt.timedelta(1825), dt.datetime.today())


def atr(df_original, period):
    """Function to calculate True Range and Average True Range."""
    df_atr = df_original.copy()
    df_atr['H-L'] = abs(df_atr['High'] - df_atr['Low'])
    # Take difference between daily high/low and previous day's close
    df_atr['H-PC'] = abs(df_atr['High'] - df_atr['Adj Close'].shift(1))
    df_atr['L-PC'] = abs(df_atr['Low'] - df_atr['Adj Close'].shift(1))
    # Take maximum value of these three to get the true range for that stock's movement across two days, then take rolling average to get ATR
    df_atr['TR'] = df_atr[['H-L', 'H-PC', 'L-PC']].max(axis=1, skipna=False)
    df_atr['ATR'] = df_atr['TR'].rolling(period).mean()
    df_atr = df_atr.drop(['H-L', 'H-PC', 'L-PC'], axis=1)
    return df_atr


def adx(df_original, period):
    """Function to calculate Average Directional Index."""
    df_adx = df_original.copy()
    df_adx['TR'] = atr(df_adx, period)['TR']
    # DM+ (upwards directional movement)
    df_adx['DMplus'] = np.where((df_adx['High'] - df_adx['High'].shift(1)) >
                             (df_adx['Low'].shift(1) - df_adx['Low']),
                             df_adx['High'] - df_adx['High'].shift(1), 0)
    df_adx['DMplus'] = np.where(df_adx['DMplus'] < 0, 0, df_adx['DMplus'])
    # DM- (downwards directional movement)
    df_adx['DMminus'] = np.where((df_adx['Low'].shift(1) - df_adx['Low']) >
                              (df_adx['High'] - df_adx['High'].shift(1)),
                              df_adx['Low'].shift(1) - df_adx['Low'], 0)
    df_adx['DMminus'] = np.where(df_adx['DMminus'] < 0, 0, df_adx['DMminus'])
    TRn = []
    DMplusN = []
    DMminusN = []

    TR = df_adx['TR'].tolist()
    DMplus = df_adx['DMplus'].tolist()
    DMminus = df_adx['DMminus'].tolist()

    for i in range(len(df_adx)):
        if i < period:
            TRn.append(np.NaN)
            DMplusN.append(np.NaN)
            DMminusN.append(np.NaN)
        elif i == period:
            TRn.append(df_adx['TR'].rolling(period).sum().tolist()[period])
            DMplusN.append(df_adx['DMplus'].rolling(period).sum().tolist()[period])
            DMminusN.append(df_adx['DMminus'].rolling(period).sum().tolist()[period])
        elif i > period:
            TRn.append(TRn[i-1] - (TRn[i-1] / period) + TR[i])
            DMplusN.append(DMplusN[i-1] - (DMplusN[i-1] / period) + DMplus[i])
            DMminusN.append(DMminusN[i-1] - (DMminusN[i-1] / period) + DMminus[i])

    df_adx['TRn'] = np.array(TRn)
    df_adx['DMplusN'] = np.array(DMplusN)
    df_adx['DMminusN'] = np.array(DMminusN)
    df_adx['DIplusN'] = 100 * (df_adx['DMplusN'] / df_adx['TRn'])
    df_adx['DIminusN'] = 100 * (df_adx['DMminusN'] / df_adx['TRn'])
    df_adx['DIdiff'] = abs(df_adx['DIplusN'] - df_adx['DIminusN'])
    df_adx['DIsum'] = df_adx['DIplusN'] + df_adx['DIminusN']
    # Create directional indicator column
    df_adx['DX'] = 100 * (df_adx['DIdiff'] / df_adx['DIsum'])
    DX = df_adx['DX'].tolist()
    ADX = []

    for j in range(len(df_adx)):
        if j < 2*period-1:
            ADX.append(np.NaN)
        elif j == 2*period-1:
            ADX.append(df_adx['DX'][j-period+1:j + 1].mean())
        elif j > 2*period-1:
            ADX.append(((period-1) * [j-1] + DX[j]) / period)

    df_adx['ADX'] = np.array(adx)
    return df_adx['ADX']

atr(ohlcv, 20)
adx(ohlcv, 20)
print(atr)
print(adx)
