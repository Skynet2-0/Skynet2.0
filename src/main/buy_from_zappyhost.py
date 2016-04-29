from random import randint
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from main.BogusFormBuilder import BogusFormBuilder

from main.VPSBuyer import VPSBuyer
from main.ZappiehostBuyer import ZappiehostBuyer


#temporary, for testing:
email = "ncb21992@hotmail.com"
password = "2Rxub#21l8oR#$niEd#L08J9*MK3IiLP"

generator = BogusFormBuilder()

SSHPassword = generator.getRAString(32)

zhb = ZappiehostBuyer(email, password)
#zhb.placeOrder('abc', 'def')

zhb.setSSHPassword()
