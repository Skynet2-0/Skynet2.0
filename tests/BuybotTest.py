"""
Created June 7, 2016

@author: Stefan
"""

from market.market import Market
from market.buybot import AutoBuyBot
from Tribler.community.market.core.order import *
from Tribler.community.market.core.price import Price
from Tribler.community.market.core.quantity import Quantity
import unittest
from mock import *

class AutoBuyBotTest(unittest.TestCase):
    """Tests the market class."""

    def setUp(self):
        """Does some set up."""
        self.mockmarket = create_autospec(Market)
        self.mockwallet = create_autospec(Wallet)
        self.bot = AutoBuyBot(mockmarket, mockwallet)

    def tearDown(self):
        """Does some clean up."""
        pass

    def testRun(self):
        self.mockwallet.balance.return_value = 0.02
        self.assertTrue(self._run(0.01))

    def testRunIsCalledNever(self):
        self.mockwallet.balance.return_value = 0.00
        self._run(0.01)
        self.assertEquals(0, self.mockmarket.buy.call_count)

    def testRunIsCalledOnce(self):
        self.mockwallet.balance.return_value = 0.01
        self._run(0.01)
        self.assertEquals(1, self.mockmarket.buy.call_count)

    def testRunIsCalledTwice(self):
        self.mockwallet.balance.return_value = 0.02
        self._run(0.01)
        self.assertEquals(2, self.mockmarket.buy.call_count)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
