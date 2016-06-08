"""
This file arranges the API for the market.

Created June 6, 2016.

@author Stefan
"""

from api import *

class Market(object):
    """
    The class handling the market.

    This class wraps the tribler market to make running it from our code
    easy and makes the code of the rest of the program more safe against
    changes by the developers of the other market.
    """

    def _init_(self, wrapped_market=None):
        """
        Initializes a market.

        wrapped_market -- The market to wrap. The type is api.MarketAPI
        (Default is None)
        """
        if wrapped_market is None:
            pass
        else:
            self.market = wrapped_market

    def sell(self, num_multicoins, price):
        """
        Sells num_multicoins multicoins for price bitcoins each.

        num_multicoins -- float of the number of multicoins to sell.
        price -- float of price in bitcoins.
        raises ValueError -- when num_multicoins or price is invalid.
        raises TypeError -- when num_multicoins or price is not a float.
        """
        pass

    def buy(self, num_multicoins):
        """
        Buys num_multicoins multicoins.

        num_multicoins -- The number of multicoins to buy as float.
        raises ValueError -- when num_multicoins is invalid.
        raises TypeError -- when num_multicoins is not a float.
        """
        pass

    def get_multichain_balance(self):
        """Requests the multichain balance."""
        pass

    def sell_price(self):
        """
        Get the current sell price on the market.

        returns the sell price as float.
        """
        pass

    def buy_price(self):
        """
        Get the current buy price on the market.

        returns the buy price as float.
        """
        pass

    def show_sells(self):
        """
        Show all sells in a list of tuples (price, quantity).

        returns -- a list of (price, quantity) in which both quantity and price
        are floats.
        """
        pass

    def show_buys(self):
        """
        Show all buys in a list of tuples (price, quantity).

        returns -- a list of (price, quantity) in which both quantity and price
        are floats.
        """
        pass

    @property
    def market(self):
        """The market used."""
        return self._market

    @market.setter
    def market(self, value):
        #assert isinstance(value, MarketAPI)
        self._market = value
