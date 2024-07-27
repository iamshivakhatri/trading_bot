from lumibot.brokers import Alpaca
from lumibot.backtesting import YahooDataBacktesting
from lumibot.strategies.strategy import Strategy
from lumibot.traders import Trader
from datetime import datetime
import os
from types import SimpleNamespace
from dotenv import load_dotenv

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
    def initialize(self, symbol:str="SPY", cash_at_ristk:float=0.5):
        self.symbol = symbol
        self.sleeptime = "24H"
        self.last_trade = None
        self.cash_at_risk = cash_at_ristk

    def position_sizing(self):
        cash = self.get_cash()
        last_price = self.get_last_price(self.symbol)
        quantity = round(cash * self.cash_at_risk / last_price,0)
        return cash, last_price, quantity


    def on_trading_iteration(self):
        cash, last_price, quantity = self.position_sizing()

        
        
        if cash > last_price:
            if self.last_trade == None:
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



start_date = datetime(2023,1,1)
# current_time = datetime.now()
end_date = datetime(2024,1,30)

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

