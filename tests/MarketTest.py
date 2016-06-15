"""
Created June 7, 2016

@author: Stefan
"""

from market.market import Market
from market.api import MarketAPI, OrderBookAPI
from Tribler.community.market.core.order import *
from Tribler.community.market.core.price import Price
from Tribler.community.market.core.quantity import Quantity
import unittest
from mock import *

class MarketTest(unittest.TestCase):
    """Tests the market class."""

    def setUp(self):
        """Does some set up."""
        self.mock = create_autospec(MarketAPI)
        self.mock.order_book = create_autospec(OrderBookAPI)
        self.market = Market(self.mock)

    def tearDown(self):
        """Does some clean up."""
        #del self.mock
        #del self.market
        pass

    def testBuy(self):
        amount = 20.0
        mocked_orderid = 732257
        mocked_order = Mock(Order)
        mocked_order.order_id.return_value = mocked_orderid
        self.mock.create_bid(ANY, amount, ANY).return_value = mocked_order
        order = self.market.buy(amount)
        # self.assertEquals(mocked_orderid, order.order_id) # Does not go well.
        self.assertIsNotNone(order)

    def testBuyCalled(self):
        amount = 3.0
        self.market.buy(amount)
        self.mock.create_bid.assert_called_once_with(ANY, amount, ANY)

    def testBuyCalledDefaultPresent(self):
        amount = 30.1
        price = 13.0
        timeout = 2.0
        self.mock.order_book.bid_price.return_value = Price.from_float(price)
        self.market.buy(amount, price, timeout)
        self.mock.create_bid.assert_called_once_with(price, amount, timeout)

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
        except KeyError as e:
            msg = e.args[0]
            if msg == errormsg:
                succes = True
            else:
                # Unexpected Exception so reraise
                print("\nexpected message:%s (%s)\nbut was:%s (%s)\nequal:%s" % (errormsg, str(type(errormsg)), msg, str(type(msg)), str(msg == errormsg)))
                raise
        self.assertTrue(succes, "Error was altered.")

    def testBuyInOrderBook(self):
        amount = 1.0
        price = 2.1
        expected = [ (2.1, 1.0) ]
        t = (Price.from_float(price), Quantity.from_float(amount))
        self.mock.order_book.bid_side_depth_profile.return_value = []
        def addOrder(*args, **kwargs):
            self.mock.order_book.bid_side_depth_profile.return_value = [ t ]
        self.mock.create_bid.side_effect = addOrder
        self.market.buy(amount, price)
        self.assertEquals(expected, self.market.get_buys())

    def testSell(self):
        amount = 3.0
        price = 3.3
        mocked_orderid = 732257
        mocked_order = Mock(Order)
        mocked_order.order_id.return_value = mocked_orderid
        self.mock.create_ask(price, amount, ANY).return_value = mocked_order
        order = self.market.sell(amount, price)
        # self.assertEquals(mocked_orderid, order.order_id) # Comparison states order is a mock.
        self.assertIsNotNone(order)

    def testSellCalled(self):
        amount = 30.1
        price = 13.0
        self.market.sell(amount, price)
        self.mock.create_ask.assert_called_once_with(price, amount, ANY)

    def testSellCalledDefaultPresent(self):
        amount = 30.1
        price = 13.0
        timeout = 2.0
        self.mock.order_book.ask_price.return_value = Price.from_float(price)
        self.market.sell(amount, price, timeout)
        self.mock.create_ask.assert_called_once_with(price, amount, timeout)

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
            errormsg = "'%s'" % errormsg
            if msg == errormsg:
                succes = True
            else:
                # Unexpected Exception so reraise
                raise
        self.assertTrue(succes, "Error was altered.")

    def testSellInOrderBook(self):
        amount = 1.0
        price = 2.1
        expected = [ (2.1, 1.0) ]
        t = (Price.from_float(price), Quantity.from_float(amount))
        self.mock.order_book.ask_side_depth_profile.return_value = []
        def addOrder(*args, **kwargs):
            self.mock.order_book.ask_side_depth_profile.return_value = [ t ]
        self.mock.create_ask.side_effect = addOrder
        self.market.sell(amount, price)
        self.assertEquals(expected, self.market.get_sells())

    def testGetMCBalance(self):
        quan = 2.4
        self.mock.get_multichain_balance.return_value = Quantity.from_float(quan)
        self.assertEquals(quan, self.market.get_multichain_balance())

    def testGetMCBalanceReturnType(self):
        quan = 2.4
        self.mock.get_multichain_balance.return_value = Quantity.from_float(quan)
        self.assertTrue(isinstance(self.market.get_multichain_balance(), float))

    def testSellPriceReturnType(self):
        sell_price = 1.0
        # self.mock.ask_price = Mock()
        self.mock.order_book.ask_price.return_value = Price.from_float(sell_price)
        self.assertIsInstance(self.market.sell_price(), float)

    def testSellPricePositive(self):
        sell_price = 1.0
        # self.mock.ask_price = Mock()
        self.mock.order_book.ask_price.return_value = Price.from_float(sell_price)
        self.assertTrue(self.market.sell_price() >= 0.0)

    def testSellPrice(self):
        sell_price = 1.0
        # self.mock.ask_price = Mock()
        self.mock.order_book.ask_price.return_value = Price.from_float(sell_price)
        self.assertEquals(sell_price, self.market.sell_price())

    def testBuyPriceReturnType(self):
        buy_price = 1.0
        # self.mock.bid_price = Mock()
        self.mock.order_book.bid_price.return_value = Price.from_float(buy_price)
        self.assertIsInstance(self.market.buy_price(), float)

    def testBuyPricePositive(self):
        buy_price = 1.0
        # self.mock.bid_price = Mock()
        self.mock.order_book.bid_price.return_value = Price.from_float(buy_price)
        self.assertTrue(self.market.buy_price() >= 0)

    def testBuyPrice(self):
        buy_price = 1.0
        self.mock.order_book.bid_price.return_value = Price.from_float(buy_price)
        self.assertEquals(buy_price, self.market.buy_price())

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
        self.assertEquals(history, self.market.get_sells())

    def testShowSells(self):
        price1 = Price.from_float(30.0)
        quantity1 = Quantity.from_float(2.2)
        price2 = Price.from_float(1.2)
        quantity2 = Quantity.from_float(4.0)
        t1 = (price1, quantity1)
        t2 = (price2, quantity2)
        history = [ t1, t2 ]
        expected = [ (30.0, 2.2), (1.2, 4.0) ]
        self.mock.order_book.ask_side_depth_profile.return_value = history
        self.assertEquals(expected, self.market.get_sells())

    def testShowSellsTypes(self):
        price1 = Price.from_float(30.0)
        quantity1 = Quantity.from_float(2.2)
        price2 = Price.from_float(1.2)
        quantity2 = Quantity.from_float(4.0)
        t1 = (price1, quantity1)
        t2 = (price2, quantity2)
        history = [ t1, t2 ]
        self.mock.order_book.ask_side_depth_profile.return_value = history
        result = self.market.get_sells()
        for (price, quantity) in result:
            self.assertIsInstance(price, float)
            self.assertIsInstance(quantity, float)

    def testShowBuysEmpty(self):
        history = []
        self.mock.order_book.bid_side_depth_profile.return_value = history
        self.assertEquals(history, self.market.get_buys())

    def testShowBuys(self):
        price1 = Price.from_float(30.0)
        quantity1 = Quantity.from_float(2.2)
        price2 = Price.from_float(1.2)
        quantity2 = Quantity.from_float(4.0)
        t1 = (price1, quantity1)
        t2 = (price2, quantity2)
        history = [ t1, t2 ]
        answer = [ (30.0, 2.2), (1.2, 4.0) ]
        self.mock.order_book.bid_side_depth_profile.return_value = history
        self.assertEquals(answer, self.market.get_buys())

    def testShowBuysTypes(self):
        price1 = Price.from_float(30.0)
        quantity1 = Quantity.from_float(2.2)
        t1 = (price1, quantity1)
        price2 = Price.from_float(1.2)
        quantity2 = Quantity.from_float(4.0)
        t2 = (price2, quantity2)
        history = [ t1, t2 ]
        self.mock.order_book.bid_side_depth_profile.return_value = history
        result = self.market.get_buys()
        for (price, quantity) in result:
            self.assertIsInstance(price, float)
            self.assertIsInstance(quantity, float)

    def testOrderBookExists(self):
        self.assertIsNotNone(self.market.order_book)

    def testOrderBookEquals(self):
        self.assertEquals(self.mock.order_book, self.market.order_book)

    def testOrderBookType(self):
        self.assertTrue(isinstance(self.market.order_book, OrderBookAPI))

    def testConvertPriceToFloat(self):
        price = Price.from_float(2.035)
        self.assertEquals(price, Price.from_float(self.market._convert_price_to_float(price)))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
