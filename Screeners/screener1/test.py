from yahoo_fin import stock_info as si
import datetime as dt
import pytz
from io import StringIO
import pandas as pd

# Set timezone
timezone = pytz.timezone('US/Eastern')

# Function to fetch S&P 500 tickers
def get_sp500_tickers():
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    tables = pd.read_html(url)
    df = tables[0]
    tickers = df['Symbol'].tolist()
    return tickers

# Fetch the tickers
tickers = get_sp500_tickers()
print(tickers)