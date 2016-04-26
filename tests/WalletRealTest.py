"""
Created on April 26, 2016.

@author: stefanboodt
"""

import unittest
from src.main.Wallet import *
from bitcoinrpc.config import read_config_file
from bitcoinrpc.exceptions import InsufficientFunds


@unittest.skip("Does not work properly and keeps crashing because the socket fails.")
class WalletRealTest(unittest.TestCase):
    """This class tests the wallet class."""

    """Object under test."""
    SUT = Wallet("testaddress", config="tests/bitcoin-test-config.config")

    def setUp(self):
        """Does some set up."""
        super().setUp()

    def tearDown(self):
        """Does some clean up."""
        super().tearDown()

    def testAddress(self):
        """Tests if the address is as expected."""
        self.assertIsNotNone(WalletRealTest.SUT.getAddress())

    def testBalancePositive(self):
        """Tests if the balance is positive."""
        self.assertTrue(WalletRealTest.SUT.getSaldo() >= 0)

    def testTransferInsufficientFunds(self):
        """Tests the transfer method."""
        try:
            rediculous_amount = 10000000000
            address = WalletRealTest.SUT.getAddress()
            WalletRealTest.SUT.transfer(rediculous_amount, address)
            assert(0) # Fail the test.
        except InsufficientFunds:
            pass

    def testTransferInvalid(self):
        """Tests the transfer method to a non existing transfer."""
        self.assertFalse(WalletRealTest.SUT.transfer(0.0, "_super invalid_"))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
