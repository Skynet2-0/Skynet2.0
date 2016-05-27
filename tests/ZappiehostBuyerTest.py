"""
Created on May 27, 2016

@author: Stefan
"""
import unittest
from VPSBuyerTest import VPSBuyerTest
from agent.ZappiehostBuyer import ZappiehostBuyer


class ZappiehostBuyerTest(VPSBuyerTest):
    """
    Tests the zappiehost buyer.

    Only non buying methods are tested.
    """

    def setUp(self):
        super(ZappiehostBuyerTest, self).setUp()
        self.sshuser = "root"
        self.buyer = ZappiehostBuyer(self.email, self.password, self.sshpassword)

    def testSSHName(self):
        self.assertEqual(self.sshuser, self.buyer.getSSHUsername())

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
