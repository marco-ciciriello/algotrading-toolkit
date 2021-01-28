import copy
import talib

from alpha_vantage.timeseries import TimeSeries

talib.get_function_groups()  # Get list of TA-Lib functions by group

tickers = ['AAPL', 'AMZN', 'CSCO', 'FB', 'IBM', 'INTC', 'LYFT''MSFT', 'QCOM']
ohlcv = {}
key_path = 'YOUR_KEY_PATH_HERE'
ts = TimeSeries(key=open(key_path, 'r').read(), output_format='pandas')

attempt = 0
drop = []

while len(tickers) != 0 and attempt <= 100:
    tickers = [j for j in tickers if j not in drop]

    for i in range(len(tickers)):
        try:
            ohlcv[tickers[i]] = ts.get_daily(symbol=tickers[i], outputsize='full')[0]
            ohlcv[tickers[i]].columns = ['Open', 'High', 'Low', 'Adj Close', 'Volume']
            drop.append(tickers[i])
        except:
            print(tickers[i] + ': failed to fetch data...retrying')
            continue
    attempt += 1

# Redefine tickers variable after removing any tickers with corrupted data
tickers = ohlcv.keys()
ohlc_dict = copy.deepcopy(ohlcv)

# Apply ta_lib functions on each dataframe
for ticker in tickers:
    # Calculate momentum indicators (e.g. MACD, ADX, RSI etc.) using TA-Lib
    ohlc_dict[ticker]['ADX'] = talib.ADX(ohlc_dict[ticker]['High'],
                                         ohlc_dict[ticker]['Low'],
                                         ohlc_dict[ticker]['Adj Close'],
                                         timeperiod=14)
    # Identify chart patterns (e.g. two crows, three crows, three inside,
    # engulfing pattern, etc.)
    ohlc_dict[ticker]['3I'] = talib.CDL3WHITESOLDIERS(ohlc_dict[ticker]['Open'],
                                                      ohlc_dict[ticker]['High'],
                                                      ohlc_dict[ticker]['Low'],
                                                      ohlc_dict[ticker]['Adj Close'])

    # Statistical functions (beta, correlation, etc.)
    ohlc_dict[ticker]['Beta'] = talib.BETA(ohlc_dict[ticker]['High'],
                                           ohlc_dict[ticker]['Low'],
                                           timeperiod=14)
