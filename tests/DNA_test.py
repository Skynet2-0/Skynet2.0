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
        (instance, winner) = d.getVPSBuyer()
        self.assertTrue(isinstance(instance, VPSBuyer))
        self.assertTrue(isinstance(winner, basestring))
        
    def test_normalizing(self):
        dictionary = {'a': 2, 'b': 3, 'c': 4}
        d = DNA()
        (normalized, length) = d._normalize_as_vector(dictionary)
        self.assertEqual(length, 9)
        self.assertEqual(normalized['a'], 2.0/9)
        self.assertEqual(normalized['b'], 3.0/9)
        self.assertEqual(normalized['c'], 4.0/9)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()