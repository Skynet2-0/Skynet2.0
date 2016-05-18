'''
This script buys a server automatically and then installs a copy of itself from github unto that server.
'''
from VPSBuyer import VPSBuyer
from ZappiehostBuyer import ZappiehostBuyer
from ssh.install import Installer
from ssh.starter import Starter

class Birthchamber(object):
    '''
    This class is responsible for creating children of the agent
    '''
    def __init__(self):
        pass

    def getChild(self):
        #do a startup message
        print("Starting up a child server")
        '''
        #buy a server
        zhb = ZappiehostBuyer()
        result = zhb.buy()

        if result == True:
            print("VPS BOUGHT! Details:")
            print("Zappiehost email: " + zhb.getEmail())
            print("Zappiehost password: " + zhb.getPassword())
            print("SSH IP: " + zhb.getIP())
            print("SSH Username: " + zhb.getSSHUsername())
            print("SSH Password: " + zhb.getSSHPassword())
        else:
            print("Failed to buy VPS from Zappiehost...")
            #maybe do an alternative vps?'''

        #run installation on vps
        print("starting the installation procedure")
        #Installer(zhb.getIP(),zhb.getSSHUsername(),zhb.getSSHPassword(), 21)
        i = Installer("103.208.86.62","root","HEzbhNeAfPBTyQbrzpzaMzyEEhEzNfVg", 22)
        i.install()

        #start the core program on child
        print("starting the agent node")
        #Starter(zhb.getIP(),zhb.getSSHUsername(),zhb.getSSHPassword(), 21)
        s = Starter("103.208.86.62","root","HEzbhNeAfPBTyQbrzpzaMzyEEhEzNfVg", 22)
        s.start()
