from ib_insync import *

ib = IB()
# Use port 7497 for TWS, port 4002 for IB Gateway
ib.connect('127.0.0.1', 7497, clientId=1)

stock = Stock('AMD', 'SMART', 'USD')
bars = ib.reqHistoricalData(
    stock,
    endDateTime='',
    durationStr='30 D',
    barSizeSetting='1 hour',
    whatToShow='MIDPOINT',
    useRTH=True,
    )

# Convert to dataframe
df = util.df(bars)
print(df)

market_data = ib.reqMktData(stock, '', False, False)
print(market_data)


def onPendingTicker(ticker):
    """Handle how pending tickers are processed."""
    print('Pending ticker event received')
    print(ticker)


ib.pendingTickersEvent += onPendingTicker

ib.run()
