'''
Created on April 20, 2016

@author: stefanboodt
'''
import unittest
from bitcoin.Wallet import *

class Test(unittest.TestCase):
    """This class tests the wallet class"""

    def setUp(self):
        """Does some set up."""
        self.SUT = Wallet()
        pass


    def tearDown(self):
        'Does some clean up'
        pass


    def testName(self):
        pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()