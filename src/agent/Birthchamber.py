'''
This class buys a server automatically
and then installs a copy of itself from github unto that server
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

    def getZHBChild(self):
        #do a startup message
        print("Starting up a child server")
        
        #buy a server
        self.zhb = ZappiehostBuyer()
        result = self.zhb.buy()

        if result == True:
            print("VPS BOUGHT! Details:")
            print("Zappiehost email: " + self.getEmail())
            print("Zappiehost password: " + self.getPassword())
            print("SSH IP: " + self.getIP())
            print("SSH Username: " + self.getSSHUsername())
            print("SSH Password: " + self.getSSHPassword())
        else:
            print("Failed to buy VPS from Zappiehost...")
            #maybe do an alternative vps?            
        
        self.installChild()
        self.startChild()
    
    def getEmail(self):
        if self.email is None:
            self.email = self.zhb.getEmail() 
        return self.email
    
    def getPassword(self):
        if self.password is None:
            self.password = self.zhb.getPassword()
        return self.password    
    
    def getIP(self):
        if self.ip is None:
            self.ip = self.zhb.getIP()
        return self.ip
        
    def getSSHUsername(self):
        if self.SSHUsername is None:
            self.SSHUsername = self.zhb.getSSHUsername(self)
        return self.SSHUsername
            
    def getSSHPassword(self):
        if self.SSHPassword is None:
            self.SSHPassword = self.zhb.getSSHPassword(self)
        return self.SSHPassword
        
    def installChild(self):
        #run installation on vps
        print("starting the installation procedure")
        #i = Installer(self.getIP(),self.getSSHUsername(),self.getSSHPassword(), 22)
        i = Installer("185.99.132.241","root","HEzbhNeAfPBTyQbrzpzaMzyEEhEzNfVg", 22)
        i.install()
        
    def startChild(self):
        #start the core program on child
        print("starting the agent node")
        #s = Starter(self.getIP(),self.getSSHUsername(),self.getSSHPassword(), 22)
        s = Starter("185.99.132.241","root","HEzbhNeAfPBTyQbrzpzaMzyEEhEzNfVg", 22)
        s.start()