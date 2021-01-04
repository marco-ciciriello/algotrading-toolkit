import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf

tickers = ['MSFT', 'AMZN', 'AAPL', 'CSCO', 'IBM', 'FB']

close_prices = pd.DataFrame()
start_date = dt.datetime.today() - dt.timedelta(3650)
end_date = dt.datetime.today()

for ticker in tickers:
    close_prices[ticker] = yf.download(ticker, start_date, end_date)['Adj Close']

# Handle NaN values
close_prices.fillna(method='bfill', axis=0, inplace=True)
daily_return = close_prices.pct_change()

# Plot all stocks superimposed
close_prices.plot()

# Plot all stocks superimposed (standardised)
close_prices_standardised = (close_prices - close_prices.mean()) / close_prices.std()
close_prices_standardised.plot()

# Subplots of all stocks
close_prices.plot(subplots=True, layout=(3,2), title="Tech Stock Price Evolution", grid=True)

# Pyplot
fig, ax = plt.subplots()
plt.style.available
plt.style.use('ggplot')
ax.set(title="Daily return on tech stocks", xlabel="Tech Stocks", ylabel="Daily Returns")
plt.bar(daily_return.columns, daily_return.mean())
