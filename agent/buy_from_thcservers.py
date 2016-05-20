from random import randint
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from agent.BogusFormBuilder import BogusFormBuilder

from agent.VPSBuyer import VPSBuyer
from agent.ThcserversBuyer import ThcserversBuyer


buyer = ThcserversBuyer()
result = buyer.placeOrder()


#if result == True:
#    print("VPS BOUGHT! Details:")
#    print("Zappiehost email: " + zhb.getEmail())
#    print("Zappiehost password: " + zhb.getPassword())
#    print("SSH IP: " + zhb.getIP())
#    print("SSH Username: " + zhb.getSSHUsername())
#    print("SSH Password: " + zhb.getSSHPassword())
#else:
#    print("Failed to buy VPS from Zappiehost...")
