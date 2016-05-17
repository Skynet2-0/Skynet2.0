'''
This script buys a server automatically
and then installs a copy of itself from github unto that server
'''

#print("Hello World!")
#from Wallet import Wallet
from VPSBuyer import VPSBuyer
from ZappiehostBuyer import ZappiehostBuyer
from src.ssh.install import Installer
#wallet = Wallet()
#print(wallet.balance())
#wallet.payTo('16gFWwnDT3Fa56pYPZud74HXYEmhumoRMJ', '0.0002', '0.0002')

#do a startup message
print("Starting up a child server")

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
	#maybe do an alternative vps?
	

#run installation on vps
Installer(zhb.getIP(),zhb.getSSHUsername(),zhb.getSSHPassword(), 21)

