"""
This file arranges the API for the market.

Created June 6, 2016.

@author Stefan
"""

class Market(object):
    """
    The class handling the market.

    This class wraps the tribler market to make running it from our code
    easy and makes the code of the rest of the program more safe against
    changes by the developers of the other market.
    """

    def _init_(self):
        """Initializes a market."""
        pass

    def sell(self, num_multicoins, price):
        """
        Sells num_multicoins multicoins for price bitcoins each.

        price -- float of price in bitcoins.
        """
        pass

    def buy(self, num_multicoins):
        """
        Buys num_multicoins multicoins.

        num_multicoins -- The number of multicoins to buy.
        """
        pass
