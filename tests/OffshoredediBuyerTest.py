"""
Created on May 27, 2016

@author: Stefan
"""
import unittest
from VPSBuyerTest import VPSBuyerTest
from agent.OffshoredediBuyer import OffshoredediBuyer


class OffshoredediBuyerTest(VPSBuyerTest):
    """
    Tests the vps buyer.

    Only non buying methods are tested.
    """

    def setUp(self):
        VPSBuyerTest.setUp(self)
        self.sshuser = "root"
        self.sshpassword = ""
        self.buyer = OffshoredediBuyer(self.email, self.password)

    def testSSHPassword(self):
        self.assertEqual(self.sshpassword, self.buyer.getSSHPassword())

    def testSSHName(self):
        self.assertEqual(self.sshuser, self.buyer.getSSHUsername())

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
