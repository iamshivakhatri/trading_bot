import yfinance as yf
import pandas as pd
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

# Use timezone-aware datetime objects
start = dt.datetime.now(timezone) - dt.timedelta(days=365)
end = dt.datetime.now(timezone)

# Use yfinance for S&P 500 data
sp500_df = yf.download('^GSPC', start=start, end=end)
sp500_df['Pct Change'] = sp500_df['Adj Close'].pct_change()
sp500_return = (sp500_df['Pct Change'] + 1).cumprod().iloc[-1]

return_list = []
final_df = pd.DataFrame(columns=[
    'Ticker', 'Latest_Price', 'Score', 'PE_Ratio', 'PEG_Ratio', '52_Week_Low', 
    '52_Week_High', 'SMA_150', 'SMA_200'
])


# Normalize tickers for file names
def normalize_ticker(ticker):
    return ticker.replace('.', '_')

for ticker in tickers:
    try:
        # df = yf.download(ticker, start=start, end=end)
        df = pd.read_csv(f"stock_data/{normalize_ticker(ticker)}.csv")
        if df.empty:
            print(f"No data for {ticker}, skipping.")
            continue

        # df.to_csv(f'stock_data/{normalized_ticker}.csv')
        df['Pct Change'] = df['Adj Close'].pct_change()
        stock_return = (df['Pct Change'] + 1).cumprod().iloc[-1]
        returns_compared = round((stock_return / sp500_return), 2)
        return_list.append(returns_compared)
    except Exception as e:
        print(f"Error processing {ticker}: {e}")

best_performers = pd.DataFrame(list(zip(tickers, return_list)), columns=['Ticker', 'Returns Compared'])
best_performers['Score'] = best_performers['Returns Compared'].rank(pct=True) * 100
best_performers = best_performers[best_performers['Score'] >= best_performers['Score'].quantile(.7)]

print(best_performers)

# for ticker in best_performers['Ticker']:
#     try:
#         normalized_ticker = normalize_ticker(ticker)
#         df = pd.read_csv(f'stock_data/{normalized_ticker}.csv', index_col=0)
#         moving_average = [150, 200]
#         for ma in moving_average:
#             df["SMA_" + str(ma)] = round(df['Adj Close'].rolling(window=ma).mean(), 2)

#         latest_price = df['Adj Close'].iloc[-1]
#         pe_ratio = float(si.get_quote_table(ticker)['PE Ratio (TTM)'])
#         peg_ratio = float(si.get_stats_valuation(ticker)[1][4])
#         moving_average_150 = df['SMA_150'].iloc[-1]
#         moving_average_200 = df['SMA_200'].iloc[-1]
#         low_52week = round(min(df['Low'].iloc[-260:]), 2)
#         high_52week = round(max(df['High'].iloc[-260:]), 2)
#         score = round(best_performers[best_performers['Ticker'] == ticker]['Score'].tolist()[0], 2)

#         condition_1 = latest_price > moving_average_150 > moving_average_200
#         condition_2 = latest_price >= (1.3 * low_52week)
#         condition_3 = latest_price >= (0.75 * high_52week)
#         condition_4 = pe_ratio < 40
#         condition_5 = peg_ratio < 2

#         if condition_1 and condition_2 and condition_3 and condition_4 and condition_5:
#             row = pd.DataFrame([{
#                 'Ticker': ticker,
#                 'Latest_Price': latest_price,
#                 'Score': score,
#                 'PE_Ratio': pe_ratio,
#                 'PEG_Ratio': peg_ratio,
#                 '52_Week_Low': low_52week,
#                 '52_Week_High': high_52week,
#                 'SMA_150': moving_average_150,
#                 'SMA_200': moving_average_200
#             }])
#             final_df = pd.concat([final_df, row], ignore_index=True)
#     except Exception as e:
#         print(f"Error processing {ticker}: {e}")

# final_df.sort_values('Score', ascending=False, inplace=True)
# pd.set_option("display.max_columns", 10)
# print(final_df)
# final_df.to_csv('final.csv')
