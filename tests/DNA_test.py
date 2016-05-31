import unittest
import json
from agent.DNA import DNA
from agent.VPSBuyer import VPSBuyer

class DNATest(unittest.TestCase):
    def test_DNA_structure_VPS_buyer(self):
        d = DNA()
        djson = d.getDNA()
        
        vps_buyers = djson['vps buyers']
        
        #verify vps_buyers sums to 1
        sum = 0.0
        for key, val in vps_buyers.iteritems():
            sum+=val
        self.assertEqual(sum,1.0)
    
    def test_get_winner(self):
        d = DNA()
        dictionary = {"a": 1.0}
        self.assertEqual(d._select_winner(dictionary), "a")
        
    def test_returns_vpsBuyer(self):
        d = DNA()
        instance = d.getVPSBuyer()
        self.assertTrue(isinstance(instance, VPSBuyer))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()