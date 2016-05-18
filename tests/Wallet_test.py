import unittest
from src.agent.Wallet import Wallet

class WalletTest(unittest.TestCase):	
    def testOnlyConfirmedBalance(self):
    	w = Wallet()
    	balancesheet = """{
    	"confirmed": "0.02386436"
		}"""

    	self.assertEqual(w.calculateBalance(balancesheet), 0.02386436)
    	
    def testBothBalance(self):
    	w = Wallet()
    	balancesheet = """{
    	"confirmed": "0.02386436",
    	"unconfirmed": "0.02386436"
		}"""

    	self.assertEqual(w.calculateBalance(balancesheet), 0.04772872)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()