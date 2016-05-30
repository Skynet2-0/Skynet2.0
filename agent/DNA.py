import json

class DNA(object):
    """
    DNA is responsible for providing the data needed by birthchamber in a dynamic way.
    """
    def __init__(self):
        """
        Read the own DNA file, and if none exists create one
        """
        
        try:
            self.json =self._load() 
        except (IOError, TypeError, ValueError) as e:
            self._save(DNA.default())
            self.json = self._load()
        
        
    def mutate(self):
        """
        returns a mutated version of the own DNA
        """
        pass
        
    def getDNA(self):
        return self.json
    
    def _load(self, path = "dna.json"):
        """
        opens the json file containing the dna, and return it as a json
        """
        f = open("dna.json", "r")
        fc = f.read()
        return json.loads(fc)    
        
    def _save(self, djson, path = "dna.json"):
        """
        saves the dna json at path
        """
        print djson
        fw = open(path, "w")        
        fw.write(json.dumps(DNA.default(), indent=4, sort_keys=True))
        fw.close()
        
    @staticmethod
    def default():
        #return json.loads('{"vps buyers": {"zappiehost": 0.34, "offshorededi": 0.33, "vhs": 0.33}}')
        return {"vps buyers": {"zappiehost": 0.34, "offshorededi": 0.33, "vhs": 0.33}}