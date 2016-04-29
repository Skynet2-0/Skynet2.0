from random import randint
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from agent.BogusFormBuilder import BogusFormBuilder

from agent.VPSBuyer import VPSBuyer
from agent.ZappiehostBuyer import ZappiehostBuyer


#temporary, for testing:
#email = "ncb21992@hotmail.com"
#password = "2Rxub#21l8oR#$niEd#L08J9*MK3IiLP"

#generator = BogusFormBuilder()

#SSHPassword = generator.getRAString(32)

#zhb = ZappiehostBuyer('xKlupfS@XEF.org', 'qnrmHRNxCZWLskFtiDSUGkSyUoHJBSpj')
#zhb.placeOrder('abc', 'def')

#zhb.setSSHPassword()



# The code here will actually buy a VPS from Zappiehost
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
