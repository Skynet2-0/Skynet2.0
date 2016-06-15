"""
This file arranges the API for the market.

Created June 6, 2016.

@author: Stefan
"""

from api import *
from decimal import *
from Tribler.community.market.community import MarketCommunity
from typing.typecheck import *


class Market(object):
    """
    The class handling the market.

    This class wraps the tribler market to make running it from our code
    easy and makes the code of the rest of the program more safe against
    changes by the developers of the other market.
    """

    def __init__(self, wrapped_market):
        """
        Initializes a market.

        wrapped_market -- The market to wrap. The type is api.MarketAPI
        """
        self.market = wrapped_market
        self.default_timeout = 7200.0 # Two hours.

    def sell(self, num_multicoins, price=None, timeout=None):
        """
        Sells num_multicoins multicoins for price bitcoins each.

        num_multicoins -- float of the number of multicoins to sell.
        price -- float of price in bitcoins.
        timeout -- The timeout of the trade. (Default is None which will
        be mapped to default_timeout)
        raises ValueError -- when num_multicoins or price is invalid.
        raises TypeError -- when num_multicoins or price is not a float.
        returns -- The created order.
        """
        if timeout is None:
            timeout = self.default_timeout
        else:
            check_positive_float(timeout)
        check_positive_float(num_multicoins)
        if price is None:
            price = self.sell_price()
        else:
            check_positive_float(price)
        return self.market.create_ask(price, num_multicoins, timeout)

    def buy(self, num_multicoins, price=None, timeout=None):
        """
        Buys num_multicoins multicoins.

        num_multicoins -- The number of multicoins to buy as float.
        price -- The price that is being wanted to pay. (Default is None)
        timeout -- The timeout of the trade. (Default is None which will
        be mapped to default_timeout)
        raises ValueError -- when num_multicoins or timeout is invalid.
        raises TypeError -- when num_multicoins or timeout is not a float.
        returns -- The created order.
        """
        if timeout is None:
            timeout = self.default_timeout
        else:
            check_positive_float(timeout)
        check_positive_float(num_multicoins)
        if price is None:
            price = self.buy_price()
        else:
            check_positive_float(price)
        return self.market.create_bid(price, num_multicoins, timeout)

    def get_multichain_balance(self):
        """
        Requests the multichain balance.

        returns -- The balance as a float
        """
        quantity = self.market.get_multichain_balance()
        return self._convert_quantity_to_float(quantity)

    def sell_price(self):
        """
        Get the current sell price on the market.

        returns the sell price as float.
        """
        price = self.market.order_book.ask_price()
        return self._convert_price_to_float(price)

    def buy_price(self):
        """
        Get the current buy price on the market.

        returns the buy price as float.
        """
        price = self.market.order_book.bid_price()
        return self._convert_price_to_float(price)

    def _convert_price_to_float(self, price):
        """
        Returns the float value of the given price.

        price -- A price object of the price.
        returns -- A float of the price.
        """
        return float(price)

    def get_sells(self):
        """
        Get all sells in a list of tuples (price, quantity).

        returns -- a list of (price, quantity) in which both quantity and price
        are floats.
        """
        sells = self.market.order_book.ask_side_depth_profile()
        return self._convert_trade_list(sells)

    def get_buys(self):
        """
        Get all buys in a list of tuples (price, quantity).

        returns -- a list of (price, quantity) in which both quantity and price
        are floats.
        """
        buys = self.market.order_book.bid_side_depth_profile()
        return self._convert_trade_list(buys)

    def _convert_trade_list(self, trades):
        """
        Converts the trade list in trades in the format
        [(price, quantity) ... ] to a list in which price and
        quantity are floats.

        trades -- list of trades to convert.
        returns -- The list of converted trades.
        """
        converted = []
        for (p, q) in trades:
            price = self._convert_price_to_float(p)
            quantity = self._convert_quantity_to_float(q)
            t = (price, quantity)
            converted.append(t)
        return converted

    def _convert_quantity_to_float(self, quantity):
        """
        Converts quantity to float.

        It uses the str method to do so.

        quantity -- The quantity to convert.
        returns -- A float version of the quantity.
        """
        return float(str(quantity)) # Decimal(str(quantity))

    @property
    def market(self):
        """The market used."""
        return self._market

    @market.setter
    def market(self, value):
        check_type(value, MarketAPI)
        self._market = value

    @property
    def default_timeout(self):
        """
        A positive float indicating the timeout of the trade in
        default python format.
        """
        return self._default_timeout

    @default_timeout.setter
    def default_timeout(self, value):
        check_positive_float(value)
        self._default_timeout = value

    @property
    def order_book(self):
        """The order book used."""
        return self.market.order_book
