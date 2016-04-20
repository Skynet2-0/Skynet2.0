'''
Created on Apr 20, 2016

@author: Niels
'''
import unittest
from main.BogusFormBuilder import BogusFormBuilder


class Test(unittest.TestCase):
        
    def setUp(self):
        self.that = BogusFormBuilder()

    def testPassword(self):
        pwd = self.that.getPassword()
        self.assertTrue(len(pwd)>=15, "an insecure password was created")
        self.assertEqual(pwd, self.that.getPassword(), "memoization of password failed")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()