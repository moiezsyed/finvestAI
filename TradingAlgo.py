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
    "API_ENDPOINT": API_ENDPOINT
}

class AITrader(Strategy):
    """AI-based trading algorithm strategy class, based on the lifecycle method documented at: https://lumibot.lumiwealth.com/lifecycle_methods.html

    Args:
        Strategy (Class): Automated trading algorithm class provided by 'lumibot'
    """

    def initialize(self):
        """Runs everytime (once) when an object is instantiated
        """
        pass

    def on_trading_iteration(self):
        """Runs everytime new data is retrieved from the data source (news, information, etc.)
        """
        pass

# Running the Algorithm
# dates
end_date = dt.now().date()
start_date = dt.now() - td(days=30)

# broker for trading
broker = Alpaca(ALPACA_CREDS)

# initialize the strategy
strategy = AITrader(name='aistrategy', broker=broker, parameters={})

# backtest the strategy
strategy.backtest(YahooDataBacktesting, start_date, end_date, end_date, parameters={})




