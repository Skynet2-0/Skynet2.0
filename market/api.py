"""
The API for the market that is wrapped by market.py.

Created June 7, 2016.

@author Stefan
"""

class MarketAPI(object):
    """Abstract class documenting the API of the market that is wrapped around."""
    def _init_(self):
        pass

    def create_bid(btc, mc, timeout):
        """
        Creates a sell.

        btc -- float, amount in entire bitcoins
        mc -- float, amount in entire multichain
        timeout -- timeout in ??.
        returns -- orderId, the class that refers to a specific order
        """
        pass

    def create_ask(btc, mc, timeout):
        """
        Creates a buy.

        btc -- float, amount in entire bitcoins
        mc -- float, amount in entire multichain
        returns -- orderId, the class that refers to a specific order
        """
        pass
