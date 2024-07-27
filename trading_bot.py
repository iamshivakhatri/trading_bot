from lumibot.brokers import Alpaca
from lumibot.backtesting import YahooDataBacktesting
from lumibot.strategies.strategy import Strategy
from lumibot.traders import Trader
from datetime import datetime
import os
from types import SimpleNamespace
from dotenv import load_dotenv
from alpaca_trade_api import REST
from timedelta import Timedelta
from finbert_utils import estimate_sentiment

load_dotenv(override=True)

API_KEY = os.environ.get("API_KEY")
API_SECRET = os.environ.get("API_SECRET")
BASE_URL = os.environ.get("BASE_URL")

# Create a dictionary for Alpaca credentials
ALPACA_CONFIG = {
    "API_KEY":API_KEY, 
    "API_SECRET": API_SECRET, 
    "PAPER": True
}
print(ALPACA_CONFIG)



class MLTrader(Strategy):
    def initialize(self, symbol:str="SPY", cash_at_risk:float=0.5):
        self.symbol = symbol
        self.sleeptime = "24H"
        self.last_trade = None
        self.cash_at_risk = cash_at_risk
        self.api = REST(base_url=BASE_URL, key_id=API_KEY, secret_key=API_SECRET)
        self.count = 0

    def position_sizing(self):
        cash = self.get_cash()
        last_price = self.get_last_price(self.symbol)
        quantity = round(cash * self.cash_at_risk / last_price,0)
        return cash, last_price, quantity
    
    def get_dates(self):
        today = self.get_datetime()
        print(today)
        three_days_prior = today - Timedelta(days=3)
        print(three_days_prior)
        return today.strftime("%Y-%m-%d"), three_days_prior.strftime("%Y-%m-%d")



    def get_sentiment(self):
        today, three_days_prior = self.get_dates()
        news = self.api.get_news(symbol=self.symbol, start=three_days_prior , end=today)
        news = [ev. __dict__["_raw"]["headline"] for ev in news]
        probability, sentiment = estimate_sentiment(news)
        return probability, sentiment

    def on_trading_iteration(self):
        self.count = self.count + 1
        print(f"Trading iteration: {self.count}")
        cash, last_price, quantity = self.position_sizing()
        probability, sentiment = self.get_sentiment() 
        if cash > last_price:   
            if sentiment == "positive" and probability > 0.8:
                if self.last_trade == "sell":
                    self.sell_all()
                print(f"Probability: {probability}, Sentiment: {sentiment}")
                order = self.create_order(
                    self.symbol,
                    quantity,
                    "buy",
                    type="bracket",
                    take_profit_price=last_price * 1.20,
                    stop_loss_price=last_price * 0.95
                )
                self.submit_order(order)
                self.last_trade = "buy"
            elif sentiment == "negative" and probability > 0.8:
                if self.last_trade == "buy":
                    self.sell_all()
                print(f"Probability: {probability}, Sentiment: {sentiment}")
                order = self.create_order(
                    self.symbol,
                    quantity,
                    "sell",
                    type="bracket",
                    take_profit_price=last_price * 0.8,
                    stop_loss_price=last_price * 1.05
                )
                self.submit_order(order)
                self.last_trade = "sell"


            



start_date = datetime(2023,7,1)
# current_time = datetime.now()
end_date = datetime(2024,7,15)

broker = Alpaca(ALPACA_CONFIG)

strategy  = MLTrader(name='mistrat', broker=broker, parameters={
    "symbol":"SPY",
    "cash_at_risk":0.5
    
    }) 


strategy.backtest(
    YahooDataBacktesting,
    start_date,
    end_date,
    parameters={ }
)

