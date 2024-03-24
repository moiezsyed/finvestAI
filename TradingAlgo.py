from lumibot.brokers import Alpaca  # broker
from lumibot.backtesting import YahooDataBacktesting # backtesting framework
from lumibot.strategies.strategy import Strategy # automated trading
from lumibot.traders import Trader # deployement
from datetime import datetime as dt, timedelta as td
from alpaca_trade_api import REST

API_KEY = "PKPRVPP06CANE9O63SN9"
API_SECRET = "6FfKbsWFlbFHd4JEbnMaB337RTSHoDWIgRYZLPj7"
API_ENDPOINT = "https://paper-api.alpaca.markets/v2"

ALPACA_CREDS = {
    "API_KEY": API_KEY,
    "API_SECRET": API_SECRET,
    "PAPER": True
}

class AITrader(Strategy):
    """AI-based trading algorithm strategy class, based on the lifecycle method documented at: https://lumibot.lumiwealth.com/lifecycle_methods.html

    Args:
        Strategy (Class): Automated trading algorithm class provided by 'lumibot'
    """

    def initialize(self, symbol:str="SPY", cash_at_risk:float=0.5):
        """Runs everytime (once) when an object is instantiated

        Args:
            symbol (string): Represents a ticker to represent a particular stock on the exchange.
            cash_at_risk (float): Metric representing cash balance to be risked at every trade (0.5 -> 50%)
        """
        self.symbol = symbol
        # https://lumibot.lumiwealth.com/strategy_properties/strategies.strategy.Strategy.sleeptime.html
        self.sleeptime = "24H"
        self.last_trade = None
        self.cash_at_risk = cash_at_risk
        self.api = REST(key_id=API_KEY, secret_key=API_SECRET, base_url=API_ENDPOINT)

    def position_sizing(self):
        """Determined how much of an asset to buy or sell, directly impacting the potential profit or loss.

        Returns:
            cash (float): Available cash in the account (https://lumibot.lumiwealth.com/strategy_properties/strategies.strategy.Strategy.cash.html)
            last_price (float): Last known price of the stock/ticker (https://lumibot.lumiwealth.com/strategy_methods.data/lumibot.strategies.strategy.Strategy.get_last_price.html)
            quantity_per_trade (float): Cash we're risking per trade from the cash being risked
        """
        cash = self.get_cash()
        last_price = self.get_last_price(self.symbol)
        quantity_per_trade = round((cash * self.cash_at_risk) / last_price, 0)

        return cash, last_price, quantity_per_trade

    def get_dates_str(self):
        """Gets start and end dates for fetching the news to perform sentiment analysis on.
         This method emphasizes the most up-to-date (recent) news.
        """
        # today
        end_date = (self.get_datetime()).strftime('%Y-%m-%d')
        # 3 days prior (range to get the news from)
        start_date = (end_date - td(days=3)).strftime('%Y-%m-%d')
        
        # convert to string to send over the REST API
        return start_date, end_date

    def get_news(self):
        """Gets news for the relevant asset, using the REST API for Alpaca
        """
        # get date range in string for fetching the news
        start_date, end_date = self.get_dates_str()

        news = self.api.get_news(symbol=self.symbol, start=start_date ,end=end_date)

    def on_trading_iteration(self):
        """Runs everytime new data is retrieved from the data source (news, information, etc.)
        """
        # retrieve position sizing variables
        available_cash, last_price, quantity_per_trade = self.position_sizing()

        # logic to make sure cash is always greater than last known asset price before purchase
        if available_cash > last_price:
            if self.last_trade == None:
                order = self.create_order(
                    self.symbol,
                    quantity_per_trade,
                    "buy",
                    type="bracket",
                    take_profit_price=last_price*1.20,  # 120% of 'last_price' considered profit
                    stop_loss_price=last_price*0.95 # 95% of 'last_price' considered loss 
                )
                # executing order
                self.submit_order(order)
                self.last_trade = "buy"

# Running the Algorithm
# datetime objects
# end_date = dt.now() - td(days=1)    # yesterday
# start_date = end_date - td(days=30) # 1 month back from 'end_date'
start_date = dt(2023,12,15)
end_date = dt(2023,12,31) 

# broker for trading
broker = Alpaca(ALPACA_CREDS)

# initialize the strategy
strategy = AITrader(name='aistrategy', broker=broker, parameters={"symbol":"SPY", "cash_at_risk": 0.5})

# backtest the strategy
strategy.backtest(YahooDataBacktesting, start_date, end_date, parameters={"symbol":"SPY", "cash_at_risk": 0.5})