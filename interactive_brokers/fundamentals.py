from bs4 import BeautifulSoup as bs
from ib_insync import *

ib = IB()
# Use port 7497 for TWS, port 4002 for IB Gateway
ib.connect('127.0.0.1', 7497, clientId=1)

stock = Stock('AMD', 'SMART', 'USD')

fundamentals = ib.reqFundamentalData(stock, 'ReportSnapshot')
content = bs(fundamentals, 'xml')
print(content)

ratios = content.find_all('Ratio')
for ratio in ratios:
    print(ratio['FieldName'] + ': ' + ratio.text)
