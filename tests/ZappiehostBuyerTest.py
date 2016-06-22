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

    def testWriteToFileBuyer(self):
        import os
        filename = "children.info"
        if os.path.isfile(filename):
            os.remove(filename)
        self.buyer.writeInfoToFile()
        read = None
        with open(filename) as f:
            read = f.read()
        self.assertTrue("ZappiehostBuyer" in read)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
