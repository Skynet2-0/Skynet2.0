"""
This script buys a server automatically and then installs a copy of itself from
github unto that server.
"""
from VPSBuyer import VPSBuyer
from ZappiehostBuyer import ZappiehostBuyer
from ssh.install import Installer
from ssh.starter import Starter

class Birthchamber(object):
    """ This class is responsible for creating children of the agent. """

    def __init__(self):
        pass

    def getChild(self, VPSBuyer):
        """
        Buys a child server.

        VPSBuyer -- The VPSBuyer to use of type VPSBuyer.
        """
        #do a startup message
        print("Starting up a child server")

        #buy a server
        self.vps = VPSBuyer
        result = self.VPSBuyer.buy()

        if result == True:
            print("VPS BOUGHT! Details:")
            print("Zappiehost email: " + self.vps.getEmail())
            print("Zappiehost password: " + self.vps.getPassword())
            print("SSH IP: " + self.vps.getIP())
            print("SSH Username: " + self.vps.getSSHUsername())
            print("SSH Password: " + self.vps.getSSHPassword())
        else:
            print("Failed to buy VPS from Zappiehost...")
            #maybe do an alternative vps?

        self.installChild()
        self.startChild()

    def installChild(self):
        """ Installs the project on the child. """
        '''
        ToDo: addd check whether ssh access is succesfull, and if not wait and retry
        '''
        #run installation on vps
        print("starting the installation procedure")
        i = Installer(self.vps.getIP(),self.vps.getSSHUsername(),self.vps.getSSHPassword(),22)
        #i = Installer("185.99.132.241","root","HEzbhNeAfPBTyQbrzpzaMzyEEhEzNfVg",22)
        i.install()

    def startChild(self):
        """ Starts the program on the child. """
        #start the core program on child
        print("starting the agent node")
        s = Starter(self.vps.getIP(),self.vps.getSSHUsername(),self.vps.getSSHPassword(),22)
        #s = Starter("185.99.132.241","root","HEzbhNeAfPBTyQbrzpzaMzyEEhEzNfVg",22)
        s.start()
