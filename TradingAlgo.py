from lumibot.brokers import Alpaca  # broker
from lumibot.backtesting import YahooDataBacktesting # backtesting framework
from lumibot.strategies.strategy import Strategy # automated trading
from lumibot.traders import Trader # deployement
from datetime import datetime as dt, timedelta as td
from alpaca_trade_api import REST
from utils.finbert_NLP import sentiment_estimate

API_KEY = "YOUR-API-KEY"
API_SECRET = "YOUR-API-TOKEN"
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

    def get_news_dates_str(self):
        """Gets start and end dates for fetching the news to perform sentiment analysis on.
         This method emphasizes the most up-to-date (recent) news.

         Returns:
            start_date (string): The start date for fetching the relevant news from
            end_date (string): The end date for fetching the relevant news till
        """
        # today
        end_date = self.get_datetime()
        # 3 days prior (range to get the news from)
        start_date = end_date - td(days=3)
        
        # convert to string to send over the REST API
        return start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')

    def get_news(self):
        """Gets news for the relevant asset, using the REST API for Alpaca

        Returns:
            processed_news (list): Relevant news articles, processed in a readable format, to perform sentiment analysis on
        """
        # get date range in string for fetching the news
        start_date, end_date = self.get_news_dates_str()

        # fetch the news based on the asset ticket, start and end dates
        news = self.api.get_news(symbol=self.symbol, start=start_date ,end=end_date)

        # process the news in a readbale format
        processed_news = [event.__dict__["_raw"]["headline"] for event in news]
        
        return processed_news

    def get_sentiment(self):
        """Perform sentiment analysis on news articles, pertaining to a particular asset

        Returns:
            prob (float): Probability of the accumulative news articles
            sentiment (string): Sentiment based on the calculated probability
        """
        news = self.get_news()
        prob, sentiment = sentiment_estimate(news)

        return prob, sentiment

    def on_trading_iteration(self):
        """Runs everytime new data is retrieved from the data source (news, information, etc.)
        """
        # retrieve position sizing variables
        available_cash, last_price, quantity_per_trade = self.position_sizing()
        probability, sentiment = self.get_sentiment()

        # logic to make sure cash is always greater than last known asset price before purchase
        if available_cash > last_price:
            # 'buy' logic
            if sentiment == 'positive' and probability >.999:
                if self.last_trade == "sell": 
                    self.sell_all() 
                order = self.create_order(
                    self.symbol,
                    quantity_per_trade,
                    "buy",
                    type="bracket",
                    take_profit_price=last_price*1.20,  # 120% of 'last_price' considered profit
                    stop_loss_price=last_price*0.95 # 95% of 'last_price' considered loss in 'buy'
                )
                # executing order
                self.submit_order(order)
                self.last_trade = "buy"
            # 'sell' logic
            elif sentiment == 'negative' and probability > 0.999:
                if self.last_trade == "buy": 
                    self.sell_all() 
                order = self.create_order(
                    self.symbol, 
                    quantity_per_trade, 
                    "sell", 
                    type="bracket", 
                    take_profit_price=last_price*.8, # 80% of 'last_price' considered loss
                    stop_loss_price=last_price*1.05 # 105% of 'last_price' considered profit in 'sell'
                )
                self.submit_order(order) 
                self.last_trade = "sell"

# Running the Algorithm
# datetime objects
end_date = dt.now() - td(days=3)    # 3 days ago
start_date = end_date - td(days=365) # 1 year back from 'end_date' as our timeline start

# broker for trading
broker = Alpaca(ALPACA_CREDS)

# initialize the strategy
strategy = AITrader(name='aistrategy', broker=broker, parameters={"symbol":"SPY", "cash_at_risk": 0.5})

# backtest the strategy
strategy.backtest(YahooDataBacktesting, start_date, end_date, parameters={"symbol":"SPY", "cash_at_risk": 0.5})

# # Deplyoment logic
# trader = Trader()
# trader.add_strategy(strategy)
# trader.run_all()