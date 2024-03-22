from lumibot.brokers import Alpaca  # broker
from lumibot.backtesting import YahooDataBacktesting # backtesting framework
from lumibot.strategies.strategy import Strategy # automated trading
from lumibot.traders import Trader # deployement
from datetime import datetime as dt

API_KEY = "PKPRVPP06CANE9O63SN9"
API_SECRET = "6FfKbsWFlbFHd4JEbnMaB337RTSHoDWIgRYZLPj7"
API_ENDPOINT = "https://paper-api.alpaca.markets/v2"

ALPACA_CREDS = {
    "API_KEY": API_KEY,
    "API_SECRET": API_SECRET,
    "API_ENDPOINT": API_ENDPOINT
}

class MlTrader(Strategy):
    """All ML-based trading algorithm logic

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




