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
bars = exchange.fetch_ohlcv('ETH/USDT', limit=20)

df = pd.DataFrame(bars[:-1], columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])

bb_indicator = BollingerBands(df['close'])
df['upper_band'] = bb_indicator.bollinger_hband()
df['lower_band'] = bb_indicator.bollinger_lband()
df['moving_average'] = bb_indicator.bollinger_mavg()

atr_indicator = AverageTrueRange(df['high'], df['low'], df['close'])
df['atr'] = atr_indicator.average_true_range()

print(df)
