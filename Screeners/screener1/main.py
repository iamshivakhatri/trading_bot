import pandas_datareader as web
import pandas as pd
from yahoo_fin import stock_info as si
import datetime as dt


ticker = si.tickers_sp500()

print(ticker.head())