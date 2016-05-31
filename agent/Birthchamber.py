"""
This script buys a server automatically and then installs a copy of itself from
github unto that server.
"""
import json
from VPSBuyer import VPSBuyer
from ZappiehostBuyer import ZappiehostBuyer
from ssh.install import Installer
from ssh.starter import Starter
from ssh.CreateFile import CreateFile

class Birthchamber(object):
    """ This class is responsible for creating children of the agent. """

    def __init__(self):
        pass

    def getChild(self):
        """
        Buys a child server.

        VPSBuyer -- The VPSBuyer to use of type VPSBuyer.
        """
        
        print("fetching genetic code")
        d = DNA()
                
        
        
        #do a startup message
        print("Starting up a child server")

        #buy a server
        self.vps = d.getVPSBuyer()
        result = self.VPSBuyer.buy()

        if result == True:
            print("VPS BOUGHT! Details:")
            print("Zappiehost email: " + self.vps.getEmail())
            print("Zappiehost password: " + self.vps.getPassword())
            print("SSH IP: " + self.vps.getIP())
            print("SSH Username: " + self.vps.getSSHUsername())
            print("SSH Password: " + self.vps.getSSHPassword())
            
            self.giveChildGeneticCode()
            self.installChild()        
            self.startChild()
        else:
            print("Failed to buy the VPS...")
            #maybe do an alternative vps?
        
    def getChildCost(self):
        #should return self.vps.price() or something similar
        """
        Returns the price of the child in bitcoin
        """
        return self.vps.getprice()

    def installChild(self):
        """ Installs the project on the child. """
        '''
        ToDo: add check whether ssh access is succesfull, and if not wait and retry
        '''
        #run installation on vps
        print("starting the installation procedure")
        i = Installer(self.vps.getIP(),self.vps.getSSHUsername(),self.vps.getSSHPassword(),22)
        #i = Installer("185.99.132.241","root","HEzbhNeAfPBTyQbrzpzaMzyEEhEzNfVg",22)
        i.install()
        
    def giveChildGeneticCode(self, dna):
        """
        creates the dna.json file on the child
        """        
        text = json.dumps(dna.getMutation(), indent=4, sort_keys=True)
        cf = CreateFile("185.99.132.241","root","Koekje123",22)
        #cf = CreateFile(self.vps.getIP(),self.vps.getSSHUsername(),self.vps.getSSHPassword(),22)
        cf.create("~/Skynet2.0/dna.json", text)

    def startChild(self):
        """ Starts the program on the child. """
        #start the core program on child
        print("starting the agent node")
        s = Starter(self.vps.getIP(),self.vps.getSSHUsername(),self.vps.getSSHPassword(),22)
        #s = Starter("185.99.132.241","root","HEzbhNeAfPBTyQbrzpzaMzyEEhEzNfVg",22)
        s.start()
