"""
Created on May 27, 2016

@author: Stefan
"""
import unittest
from agent.VPSBuyer import VPSBuyer


class VPSBuyerTest(unittest.TestCase):
    """
    Tests the vps buyer.

    Only non buying methods are tested.
    """

    def setUp(self):
        self.email = "AViuhsHAOD"
        self.password = "Xhks.shfl0s"
        self.sshuser = "your mother"
        self.sshpassword = "Nxgski729sjos>S;s"
        self.buyer = VPSBuyer(self.email, self.password, self.sshuser,
            self.sshpassword)

    def testPassword(self):
        self.assertEqual(self.password, self.buyer.getPassword())

    def testSSHName(self):
        self.assertEqual(self.sshuser, self.buyer.getSSHUsername())

    def testEmail(self):
        self.assertEqual(self.email, self.buyer.getEmail())

    def testSSHPassword(self):
        self.assertEqual(self.sshpassword, self.buyer.getSSHPassword())

    def testWriteToFileBuyer(self):
        import os
        filename = "children.info"
        os.remove(filename)
        self.buyer.writeInfoToFile()
        read = None
        with open(filename) as f:
            read = f.read()
        self.assertTrue("VPSBuyer" in read)

    def testWriteToFileInformation(self):
        import os
        filename = "children.info"
        os.remove(filename)
        self.buyer.writeInfoToFile()
        read = None
        with open(filename) as f:
            read = f.read()
        self.assertTrue(self.email in read)
        self.assertTrue(self.password in read)
        self.assertTrue(self.sshuser in read)
        self.assertTrue(self.sshpassword in read)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
