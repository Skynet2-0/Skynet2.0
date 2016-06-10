"""
The API for the market that is wrapped by market.py.

Created June 7, 2016.

@author Stefan
"""
from abc import *

class MarketAPI(object):
    """Abstract class documenting the API of the market that is wrapped around."""
    __metaclass__ = ABCMeta

    def _init_(self):
        pass

    @abstractmethod
    def create_ask(self, price, quantity, timeout):
        """
        Creates a sell order.

        price -- (float) bitcoin price in btc (precision to 1/10000) roughly 3 cents
        quantity -- (float) multichain bytes in MB 10^6 (precision to 1/10000) roughly 100 bytes
        timeout -- (float) time from builtin python time format when the order must expire
        returns -- Order object that includes all the information
        """
        pass

    @abstractmethod
    def create_bid(self, price, quantity, timeout):
        """
        Creates a buy order.

        price -- (float) bitcoin price in btc (precision to 1/10000) roughly 3 cents
        quantity -- (float) multichain bytes in MB 10^6 (precision to 1/10000) roughly 100 bytes
        timeout -- (float) time from builtin python time format when the order must expire
        returns -- Order object that includes all the information
        """
        pass

    @abstractmethod
    def get_multichain_balance(self):
        """
        returns -- (Quantity object) the current amount of multichain in ~MB
        (10^6 byte) and bytes both contained in the object.
        """
        pass

class OrderBookAPI(object):
    """Abstract class registering the behaviour of the orderbook."""
    __metaclass__ = ABCMeta

    @abstractmethod
    def bid_price(self):
        """
        Return the price an ask needs to have to make a trade.

        :rtype: Price
        """
        pass

    @abstractmethod
    def ask_price(self):
        """
        Return the price a bid needs to have to make a trade.

        :rtype: Price
        """
        pass

    @abstractmethod
    def bid_side_depth_profile(self):
        """
        Returns the list of bids in the format provided.

        format: [(price (Price object), depth (Quantity object)), (price, depth), ...]
        """
        pass

    @abstractmethod
    def ask_side_depth_profile(self):
        """
        Returns the list of asks in the format provided

        format: [(price (Price object), depth (Quantity object)), (price, depth), ...]
        """
        pass


try :
    from Tribler.community.market.community import MarketCommunity
    MarketAPI.register(MarketCommunity) # MarketCommunity extends MarketAPI
except:
    print("MarketCommunity not registered as MarketAPI.")
try:
    from Tribler.community.market.core.orderbook import Orderbook
    OrderBookAPI.register(Orderbook) # Orderbook extends OrderbookAPI
except:
    print("Orderbook is not registered as OrderBookAPI")
