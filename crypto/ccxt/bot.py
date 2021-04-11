import ccxt
import config
import pandas as pd 
import ta

from ta.volatility import AverageTrueRange, BollingerBands

exchange = ccxt.binance({
    'apiKey': config.BINANCE_API_KEY,
    'secret': config.BINANCE_API_SECRET
})

markets = exchange.load_markets()
bars = exchange.fetch_ohlcv('ETH/USDT', timeframe='15m', limit=30)

df = pd.DataFrame(bars[:-1], columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
df['datetime'] = pd.to_datetime(df['datetime'], unit='ms')


def bollinger_bands(df: pd.DataFrame):
    bb_indicator = BollingerBands(df['close'])
    df['upper_band'] = bb_indicator.bollinger_hband()
    df['lower_band'] = bb_indicator.bollinger_lband()
    df['moving_average'] = bb_indicator.bollinger_mavg()

    return df

def true_range(df: pd.DataFrame):
    df['prev_close'] = df['close'].shift(1)
    df['high-low'] = df['high'] - df['low']
    df['high-prev_close'] = abs(df['high'] - df['prev_close'])
    df['low-prev_close'] = abs(df['low'] - df['prev_close'])
    tr = df[['high-low', 'high-prev_close', 'low-prev_close']].max(axis=1)

    return tr


def average_true_range(df: pd.DataFrame, period: int = 14):
    df['true_range'] = true_range(df)
    atr = df['true_range'].rolling(period).mean()

    return atr


def supertrend(df: pd.DataFrame, period: int = 7, multiplier: float = 3.0):
    df['atr'] = average_true_range(df, period=period)
    df['basic_upper_band'] = ((df['high'] + df['low']) / 2) + (multiplier * df['atr'])
    df['basic_lower_band'] = ((df['high'] + df['low']) / 2) - (multiplier * df['atr'])

    return df
