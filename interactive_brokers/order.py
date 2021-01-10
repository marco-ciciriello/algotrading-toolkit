from ib_insync import *

ib = IB()
# Use port 7497 for TWS, port 4002 for IB Gateway
ib.connect('127.0.0.1', 7497, clientId=1)

stock = Stock('AMD', 'SMART', 'USD')
order = LimitOrder('BUY', 5, 91.33)

trade = ib.placeOrder(stock, order)
print(trade)


def orderFilled(trade, fill)
    """Handle how filled orders are processed."""
    print('Order filled')
    print(order)
    print(fill)


trade.filledEvent += orderFilled

ib.run()
