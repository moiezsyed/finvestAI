from lumibot.brokers import Alpaca  # broker
from lumibot.backtesting import YahooDataBacktesting # backtesting framework
from lumibot.strategies.strategy import Strategy # automated trading
from lumibot.traders import Trader # deployement
from datetime import datetime as dt, timedelta as td

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

    def initialize(self, symbol:str="SPY"):
        """Runs everytime (once) when an object is instantiated

        Args:
            symbol (string): Represents a ticker to represent a particular stock on the exchange.
        """
        self.symbol = symbol
        # https://lumibot.lumiwealth.com/strategy_properties/strategies.strategy.Strategy.sleeptime.html
        self.sleeptime = "24H"
        self.last_trade = None

    def position_sizing(self):
        # available cash
        cash = self.get_cash()
        # last price after buying/selling stock
        last_price = self.get_last_price(self.symbol)


    def on_trading_iteration(self):
        """Runs everytime new data is retrieved from the data source (news, information, etc.)
        """
        if self.last_trade == None:
            order = self.create_order(
                self.symbol,
                10,
                "buy",
                type="market"
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
strategy = AITrader(name='aistrategy', broker=broker, parameters={"symbol":"SPY"})

# backtest the strategy
strategy.backtest(YahooDataBacktesting, start_date, end_date, parameters={"symbol":"SPY"})