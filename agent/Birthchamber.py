"""
This script buys a server automatically and then installs a copy of itself from
github unto that server.
"""
import json

from agent.DNA import DNA
from agent.DummyVPSBuyer import DummyVPSBuyer
from agent.VPSBuyer import VPSBuyer
from agent.ZappiehostBuyer import ZappiehostBuyer
from agent.Settings import Settings

from ssh.install import Installer
from ssh.starter import Starter
from ssh.FileCreator import FileCreator

class Birthchamber(object):
    """ This class is responsible for creating children of the agent. """

    def __init__(self):
        pass


    def get_child_using_test_server(self, otherBranch=None, otherCore=None):
        """
        Buys a child server.
        
        Do not use dna to find a child candidate and do not buy this candidate, use the vps candidate from settings.json instead 
        """
        s = Settings()
        v = DummyVPSBuyer(s.get_test_server_ip(), s.get_test_server_ssh_username(), s.get_test_server_ssh_password())
        
        self.vps = v
        
        self.printChildInfo()
        
        d = DNA()
        self.install_and_run_child(d,s.get_test_server_VPSBuyer(), otherBranch, otherCore)
        

    def getChild(self, otherBranch = None, otherCore = None):
        """
        Buys a child server.
         
        """
        
        print("fetching genetic code")
        d = DNA()
        
        #do a startup message
        print("Starting up a child server")
        
        #buy a server
        (vps, vpsname) = self.find_child_candidate(d)
        self.vps = vps
        result = self.vps.buy()

        if result == True:
            self.install_and_run_child(d, vpsname, otherBranch, otherCore)
        else:
            print("Failed to buy the VPS...")
            #maybe do an alternative vps?
            
    def install_and_run_child(self, dna, vpsname, otherBranch = None, otherCore = None):
        
        
        
        self.installChild(otherBranch)        
        self.giveChildGeneticCode(dna, vpsname)
        self.startChild(otherCore)
        
        self.printChildInfo()
            
    def printChildInfo(self):
        print("VPS Child Details:")
        print("vps email: " + self.vps.getEmail())
        print("vps password: " + self.vps.getPassword())
        print("SSH IP: " + self.vps.getIP())
        print("SSH Username: " + self.vps.getSSHUsername())
        print("SSH Password: " + self.vps.getSSHPassword())
        
    def getChildCost(self):
        #should return self.vps.price() or something similar
        """
        Returns the price of the child in bitcoin
        """
        return 0.02
        
    def find_child_candidate(self, dna):
        return dna.getVPSBuyer()
        
    def buy_child_candidate(self, vps):
        return vps.buy()

    def installChild(self, otherBranch = None):
        """ Installs the project on the child. """
        '''
        ToDo: add check whether ssh access is succesfull, and if not wait and retry
        '''
        #run installation on vps
        print("starting the installation procedure")
        i = Installer(self.vps.getIP(),self.vps.getSSHUsername(),self.vps.getSSHPassword(),22)
        i.install(otherBranch)
        
    def giveChildGeneticCode(self, dna, childvpsname):
        """
        creates the dna.json file on the child
        """        
        print("Sending genetic code to the child")
        text = json.dumps(dna.getMutation(childvpsname), indent=4, sort_keys=True)
        fc = FileCreator(self.vps.getIP(),self.vps.getSSHUsername(),self.vps.getSSHPassword(),22)
        fc.create("~/Skynet2.0/dna.json", text)

    def startChild(self, otherCore = None):
        """ Starts the program on the child. """
        #start the core program on child
        print("starting the agent node")
        s = Starter(self.vps.getIP(),self.vps.getSSHUsername(),self.vps.getSSHPassword(),22)
        s.start(otherCore)
        
    def start_child_other_version(self, otherVersion):
        """Starts the specified other program on the child
            e.g. start_child_other_version("agent/prototype2_agentCore -x True -t True") would enable prototype 2 to be run with exitnode and using the testserver        
        """
        s = Starter(self.vps.getIP(),self.vps.getSSHUsername(),self.vps.getSSHPassword(),22)
        s.start_other_requirements()
        s.start_agent(otherVersion)