from random import randint
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from BogusFormBuilder import BogusFormBuilder

from VPSBuyer import VPSBuyer
from ThcserversBuyer import ThcserversBuyer


buyer = ThcserversBuyer()
result = buyer.placeOrder()


if result == True:
    print("VPS BOUGHT! Details:")
    print("THCServers email: " + buyer.getEmail())
    print("THCServers password: " + buyer.getPassword())
    print("SSH IP: " + buyer.getIP())
    print("SSH Username: " + buyer.getSSHUsername())
    print("SSH Password: " + buyer.getSSHPassword())
else:
    print("Failed to buy VPS from THCServers...")
