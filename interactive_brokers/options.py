from ib_insync import *

ib = IB()
# Use port 7497 for TWS, port 4002 for IB Gateway
ib.connect('127.0.0.1', 7497, clientId=1)

stock = Stock('AMD', 'SMART', 'USD')
ib.qualifyContracts(stock)

chains = ib.reqSecDefOptParams(stock.symbol, '', stock.secType, stock.conId)
print(util.df(chains))
