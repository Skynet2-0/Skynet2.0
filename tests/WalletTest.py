"""
Created on April 20, 2016.

@author: stefanboodt
"""

import unittest
from src.main.Wallet import *
from bitcoinrpc.config import read_config_file


class Test(unittest.TestCase):
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
        self.SUT = Wallet(address, remote_conn)
        assert(self.remote_conn.getinfo().testnet) #prevent testing on production networks.

    def tearDown(self):
        """Does some clean up."""
        super().tearDown()
        pass

    def testAddress(self):
        """Tests if the address is as expected."""
        self.assertEquals(SUT.getAddress(), self.address)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
