import json
import random
import importlib

class DNA(object):
    """
    DNA is responsible for providing the data needed by birthchamber in a dynamic way.
    """
    def __init__(self):
        """
        Read the own DNA file, and if none exists create one
        """
        
        self.filename = "dna.json"
        
        try:
            self.json =self._load() 
        except (IOError, TypeError, ValueError) as e:
            self._save(DNA.default())
            self.json = self._load()
        
    def getMutation(self, winner):
        """
        returns a mutated version of the own DNA
        """
        mutateRate = self.json["mutate rate"]
        
        
        #rebuild vps_buyers with enw values, keeping it's original length
        (normalized, length) = self._normalize_as_vector(self.json["vps buyers"])
        
        try:
            self.json["vps buyers"][winner] = self.json["vps buyers"][winner] + mutateRate 
        except:
            print("did not find winning vps in vps buyers, not mutating dna at getMutation in dna.py")
        
        self.json["vps buyers"] =  self._denormalize_as_vector(normalized, length)
                
        return self.json
        
    def _normalize_as_vector(self,dictionary):
        """
           uses the values in the dictionary as a vector and then normalizes this vector.
           returns the corrected dictionary
           returns -- the pair of the normalized dictionary and the original length (normalized, length)
        """
        
        normalized_d = {}
        length = 0.0
        for value in dictionary.values():
            length+=value
        
        for key, value in dictionary.iteritems():
            normalized_d[key] = value/length
        
        return (normalized_d, length)
        
    def _denormalize_as_vector(self, dictionary, length):
        """
            denormalizes a vector back length=length
            returns the denormalized dictionary
        """
        denormalized_d = {}
        for key, value in dictionary.iteritems():
            denormalized_d[key] = value*length
        
        return denormalized_d
                
    def getVPSBuyer(self):
        """
        Returns a random vps buyer class according to the odds described in the "vps buyers" entry of the dna
        Also returns the name of the picked instance in vps_buyers so dna can be mutated
        """
        
        vpsb = self.json["vps buyers"]
                
        key = self._select_winner(vpsb)
                
        #this part assumes module and class have the same name and are in the agent directory.
        #also that no init parameters are required
        module = importlib.import_module("agent."+key)
        class_ = getattr(module, key)
        
        #now mutate the dna        
        
        return (class_(), key)
        
    def _select_winner(self, dictionary):
        """
        given a dictionary with float values
        it will return a random key in the dictionary weighted by the float values
        """
        sum = 0.0
        for key, value in dictionary.iteritems():
            sum+=value
        
        r = random.uniform(0, sum)
        sum=0.0
        k = ""
        for key, value in dictionary.iteritems():
            sum+=value
            if sum >= r:
                return key
            
    def getDNA(self):
        return self.json
    
    def _load(self, path = "dna.json"):
        """
        opens the json file containing the dna, and return it as a json
        """
        f = open(path, "r")
        fc = f.read()
        return json.loads(fc)    
        
    def _save(self, djson, path = "dna.json"):
        """
        saves the dna json at path
        """
        fw = open(path, "w")        
        fw.write(json.dumps(DNA.default()))
        fw.close()
        
    @staticmethod
    def default():
        #return json.loads('{"vps buyers": {"zappiehost": 0.34, "offshorededi": 0.33, "vhs": 0.33}}')
        return {"vps buyers": {"ZappiehostBuyer": 0.34, "OffshoredediBuyer": 0.33, "ThcserversBuyer": 0.33},
                "mutateRate": 0.05}