"""
Created June 7, 2016

@author Stefan
"""

from market.market import Market
from market.api import MarketAPI
from Tribler.community.market.core.order import *
from Tribler.community.market.core.price import Price
from Tribler.community.market.core.quantity import Quantity
import unittest
from unittest.mock import *

class MarketTest(unittest.TestCase):
    """Tests the market class."""

    def setUp(self):
        """Does some set up."""
        self.mock = create_autospec(MarketAPI)
        self.mock.order_book = create_autospec(OrderBookAPI)
        self.market = Market(mock)

    def tearDown(self):
        """Does some clean up."""
        #del self.mock
        #del self.market
        pass

    def testBuy(self):
        amount = 20.0
        mocked_orderid = 732257
        mocked_order = Mock(Order)
        mocked_order.orderId.return_value = mocked_orderid
        self.mock.create_bid(ANY, amount, ANY).return_value = mocked_order
        order = self.market.buy(amount)
        self.assertEquals(mocked_orderid, order.orderId)

    def testBuyCalled(self):
        amount = 3.0
        self.market.buy(amount)
        self.mock.create_bid.assert_called_once_with(ANY, amount, ANY)

    def testBuyInvalidAmount(self):
        amount = -4.0
        with self.assertRaises(ValueError):
            self.market.buy(amount)

    def testBuyAmountWrongType(self):
        amount = "I am not a float"
        with self.assertRaises(TypeError):
            self.market.buy(amount)

    def testBuyDoesNotAlterExceptions(self):
        amount = 2.0
        errormsg = "expected error"
        self.mock.create_bid.side_effect = KeyError(errormsg)
        succes = False
        try:
            self.market.buy(amount)
        except KeyError, msg:
            if msg == errormsg:
                succes = True
            else:
                # Unexpected Exception so reraise
                raise
        self.assertTrue(succes, "Error was altered.")

    def testSell(self):
        amount = 3.0
        price = 3.3
        mocked_orderid = 732257
        mocked_order = Mock(Order)
        mocked_order.orderId.return_value = mocked_orderid
        self.mock.create_ask(ANY, amount, ANY).return_value = mocked_order
        order = self.market.sell(amount, price)
        self.assertEquals(mocked_orderid, order.orderId)

    def testSellCalled(self):
        amount = 30.1
        price = 13.0
        self.market.sell(amount, price)
        self.mock.create_ask.assert_called_once_with(ANY, amount, ANY)

    def testSellInvalidPrice(self):
        amount = 30.0
        price = -10.0
        with self.assertRaises(ValueError):
            self.market.sell(amount, price)

    def testSellInvalidAmount(self):
        amount = -4.0
        price = 0.1
        with self.assertRaises(ValueError):
            self.market.sell(amount, price)

    def testSellPriceWrongType(self):
        amount = 2.0
        price = "I am not a float"
        with self.assertRaises(TypeError):
            self.market.sell(amount, price)

    def testSellAmountWrongType(self):
        amount = "I am not a float"
        price = 1.1
        with self.assertRaises(TypeError):
            self.market.sell(amount, price)

    def testSellDoesNotAlterExceptions(self):
        amount = 2.0
        price = 1.0
        errormsg = "expected error"
        self.mock.create_ask.side_effect = KeyError(errormsg)
        succes = False
        try:
            self.market.sell(amount, price)
        except KeyError, msg:
            if msg == errormsg:
                succes = True
            else:
                # Unexpected Exception so reraise
                raise
        self.assertTrue(succes, "Error was altered.")

    def testSellPriceReturnType(self):
        self.assertTrue(isinstance(self.market.sell_price, float))

    def testSellPricePositive(self):
        self.assertTrue(self.market.sell_price >= 0)

    def testSellPrice(self):
        sell_price = 1.0
        self.market.sell_price.return_value = Price.from_float(sell_price)
        self.assertEquals(sell_price, self.market.sell_price())

    def testBuyPriceReturnType(self):
        self.assertTrue(isinstance(self.market.buy_price, float))

    def testBuyPricePositive(self):
        self.assertTrue(self.market.buy_price >= 0)

    def testBuyPrice(self):
        buy_price = 1.0
        self.market.buy_price.return_value = Price.from_float(buy_price)
        self.assertEquals(buy_price, self.market.buy_price())

    def testOrderBookExists(self):
        self.assertIsNotNone(self.market.order_book)

    def testOrderBookEquals(self):
        self.assertEquals(self.mock.order_book, self.market.order_book)

    def testMarketSetting(self):
        """Tests whether the used market is the same as the set one."""
        self.assertEquals(self.mock, self.market.market)

    def testMarketSettingString(self):
        """Tests whether the used market is the same as the set one."""
        randomstr = "WHKScjhk@*O-sollDn>C SSTtsPALS"
        try:
            self.market.market = randomstr
            self.assertEquals(self.mock, self.market.market) # Test if set was done correctly.
        except TypeError as e:
            pass # Succes because a sting could not be set.

    def testMarketSettingTrivial(self):
        """
        Tests whether or not the market setting was trivial by
        checking against its own private value.
        """
        self.assertEquals(self.market.market, self.market._market)

    def testShowSellsEmpty(self):
        history = []
        self.mock.order_book.ask_side_depth_profile.return_value = history
        self.assertEquals(history, self.show_sells())

    def testShowSells(self):
        price1 = Price.from_float(30.0)
        quantity1 = Quantity.from_float(2.2)
        price2 = Price.from_float(1.2)
        quantity2 = Quantity.from_float(4.0)
        history = [ (price1, quantity1) (price2, quantity2) ]
        self.mock.order_book.ask_side_depth_profile.return_value = history
        self.assertEquals(history, self.show_sells())

    def testShowSellsTypes(self):
        price1 = Price.from_float(30.0)
        quantity1 = Quantity.from_float(2.2)
        price2 = Price.from_float(1.2)
        quantity2 = Quantity.from_float(4.0)
        history = [ (price1, quantity1) (price2, quantity2) ]
        self.mock.order_book.ask_side_depth_profile.return_value = history
        result = self.show_sells()
        for (price, quantity) in result:
            self.assertTrue(isinstance(price, float))
            self.assertTrue(isinstance(quantity, float))

    def testShowBuysEmpty(self):
        history = []
        self.mock.order_book.ask_side_depth_profile.return_value = history
        self.assertEquals(history, self.show_sells())

    def testShowBuys(self):
        price1 = Price.from_float(30.0)
        quantity1 = Quantity.from_float(2.2)
        price2 = Price.from_float(1.2)
        quantity2 = Quantity.from_float(4.0)
        history = [ (price1, quantity1) (price2, quantity2) ]
        self.mock.order_book.ask_side_depth_profile.return_value = history
        self.assertEquals(history, self.show_sells())

    def testShowBuysTypes(self):
        price1 = Price.from_float(30.0)
        quantity1 = Quantity.from_float(2.2)
        price2 = Price.from_float(1.2)
        quantity2 = Quantity.from_float(4.0)
        history = [ (price1, quantity1) (price2, quantity2) ]
        self.mock.order_book.ask_side_depth_profile.return_value = history
        result = self.show_sells()
        for (price, quantity) in result:
            self.assertTrue(isinstance(price, float))
            self.assertTrue(isinstance(quantity, float))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
