import unittest
from agent.DNA import DNA

class DNATest(unittest.testcase){
    def test_DNA_structure_VPS_buyer(self):
        d = DNA()
        djson = d.getDNA()
        
        vps_buyers = json.loads(djson['vps buyers'])
        
        #verify vps_buyers sums to 1
        sum = 0.0
        for val in vps_buyers:
            sum+=val
        self.assertEqual(sum,1.0)
        
    
        
}

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()