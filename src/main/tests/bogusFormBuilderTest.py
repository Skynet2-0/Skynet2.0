'''
Created on Apr 20, 2016

@author: Niels
'''
import unittest
from main.bogusFormBuilder import bogusFormBuilder


class Test(unittest.TestCase):

    
        
    def setUp(self):
        self.that = bogusFormBuilder()

    def testPassword(self):
        pwd = self.that.getPassword()
        self.assertTrue(len(pwd)>=15, "an insecure password was created")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()