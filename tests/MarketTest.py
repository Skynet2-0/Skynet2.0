"""
Created June 7, 2016

@author Stefan
"""

from market.market import Market
from market.api import MarketAPI
from tribler.Tribler.community.market.core.order import *
import unittest
from unittest.mock import *

class MarketTest(unittest.TestCase):
    """Tests the market class."""

    def setUp(self):
        """Does some set up."""
        self.mock = create_autospec(MarketAPI)
        self.market = Market(mock)

    def tearDown(self):
        """Does some clean up."""
        del self.mock
        del self.market

    def testBuy(self):
        amount = 20
        mocked_orderid = 732257
        mocked_order = Mock(Order)
        mocked_order.orderId.return_value = mocked_orderid
        self.mock.create_bid(ANY, amount, ANY).return_value = mocked_order
        order = self.market.buy(amount)
        self.assertEquals(mocked_orderid, order.orderId)

    def testBuyCalled(self):
        amount = 30
        self.market.buy(amount)
        self.mock.create_bid.assert_called_once_with(ANY, amount, ANY)

    def testSell(self):
        amount = 30
        mocked_orderid = 732257
        mocked_order = Mock(Order)
        mocked_order.orderId.return_value = mocked_orderid
        self.mock.create_ask(ANY, amount, ANY).return_value = mocked_order
        order = self.market.sell(amount, price)
        self.assertEquals(mocked_orderid, order.orderId)

    def testSellCalled(self):
        amount = 30
        self.market.sell(amount)
        self.mock.create_ask.assert_called_once_with(ANY, amount, ANY)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
