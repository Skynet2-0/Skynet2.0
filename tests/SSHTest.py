'''
Created on Apr 29, 2016

@author: Stefan
'''
import unittest
from src.agent.SSH import *


class SSHTest(unittest.TestCase):

    def setUp(self):
        self.that = SSH('localhost', None, None)

    def tearDown(self):
        self.that.close_connection()

    def testNoError():
        (_, out, _) = self.that.run('ls')
        self.assertNotNone(out)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
