"""
Created on April 20, 2016.

@author: stefanboodt
"""

import unittest
from src.main.Wallet import *
from bitcoinrpc.config import read_config_file


class WalletTest(unittest.TestCase):
    """This class tests the wallet class."""

    def setUp(self):
        """Does some set up."""
        super().setUp()
        config = read_config_file("tests/bitcoin-test-config.config")
        port = int(config.get('rpcport', '18332' if config.get('testnet') else '8332'))
        self.remote_conn = bitcoinrpc.connect_to_remote(
                user=config['rpcuser'], password=config['rpcpassword'],
                host='localhost', port=port, use_https=False)
        self.address = self.remote_conn.getnewaddress()
        self.SUT = Wallet(self.address, self.remote_conn)
        assert(self.remote_conn.getinfo().testnet) #prevent testing on production networks.

    def tearDown(self):
        """Does some clean up."""
        super().tearDown()

    def testAddress(self):
        """Tests if the address is as expected."""
        self.assertEquals(self.SUT.getAddress(), self.address)

    def testBalancePositive(self):
        """Tests if the balance is positive."""
        self.assertTrue(self.SUT.getBalance() >= 0)

    def testTransfer():
        """Tests the transfer method."""
        #self.assertTrue(self.SUT.transfer("", 0.0))
        pass

    def testTransferInvalid():
        """Tests the transfer method to a non existing transfer."""
        self.assertFalse(self.SUT.transfer("_super invalid_", 0.0))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
