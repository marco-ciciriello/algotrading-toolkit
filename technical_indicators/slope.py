import datetime as dt
import numpy as np
import yfinance as yf
import statsmodels.api as sm

ticker = 'AAPL'
ohlcv = yf.download(ticker, dt.date.today() - dt.timedelta(1825), dt.datetime.today())


def slope(series, n):
    """
    Calculate the slope of regression line for n consecutive
    points on a plot.

    Parameters
    ---------
    series : DataFrame
        Column(s) we want to find the slope for
    n : int
        Number of consecutive points to find the slope for

    Returns
    -------
    np.array
        Slope of the regression line for the previous n points
    """
    ser = (series-series.min()) / (series.max()-series.min())
    x = np.array(range(len(ser)))
    x = (x-x.min()) / (x.max()-x.min())
    # Initialise slopes to be 0
    slopes = [i * 0 for i in range(n-1)]

    for i in range(n, (len(ser)+1)):
        # Standardise x and y scales
        y_scaled = ser[i-n:i]
        x_scaled = x[i-n:i]
        # Ensure slope is taken of line y = mx + c instead of y = mx
        x_scaled = sm.add_constant(x_scaled)
        # Perform linear regression
        model = sm.OLS(y_scaled, x_scaled)
        results = model.fit()
        slopes.append(results.params[-1])

    slope_angle = (np.rad2deg(np.arctan(np.array(slopes))))
    return np.array(slope_angle)


ohlcv['close_slope'] = slope(ohlcv['Adj Close'], 5)
