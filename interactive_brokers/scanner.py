from ib_insync import *

ib = IB()
# Use port 7497 for TWS, port 4002 for IB Gateway
ib.connect('127.0.0.1', 7497, clientId=1)

subscription = ScannerSubscription(instrument='STK', locationCode='STK.US.MAJOR', scanCode='SCAN_currYrETFFYDividendYield_DESC')

scan_data = ib.reqScannerData(subscription)
for scan in scan_data:
    print(scan)
    print(scan.contractDetails.contract.symbol)
