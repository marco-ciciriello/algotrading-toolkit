import ccxt
import config

exchange = ccxt.binance({
    'apiKey': config.BINANCE_API_KEY,
    'secret': config.BINANCE_API_SECRET,
    'timeout': 30000,
    'enableRateLimit': True,
})

balance = exchange.fetch_balance()

order = exchange.create_market_buy_order('ETH/USD', 0.01)
print(order)
