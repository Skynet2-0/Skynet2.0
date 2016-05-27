from random import randint
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from BogusFormBuilder import BogusFormBuilder

from VPSBuyer import VPSBuyer

from Wallet import Wallet

import selenium.webdriver.support.ui as ui

import time
    
    
class ThcserversBuyer(VPSBuyer):
    '''
    This class orders a VPS from Thcservers.com
    '''
    def __init__(self, email = "", password = "", SSHPassword = ""):
        super(ThcserversBuyer, self).__init__()
        self.email = email
        if self.email == "":
            self.email = self.generator.getEmail()
            
        self.password = password
        if self.password == "":
            self.password = self.generator.getRAString(32)
            
        self.SSHPassword = SSHPassword
        if self.SSHPassword == "":
            self.SSHPassword = self.generator.getRAString(32)
            
        self.SSHUsername = "root"
        pass
    
    
    '''
    Walks through the entire process of buying a VPS from Thcservers. Returns True if it succeeded, returns False otherwise
    '''
    def buy(self):
        succeeded = self.placeOrder() # places the order
        if succeeded == False:
            return False
        
        time.sleep(30) # Wait for half a minute so Thcservers can process the payment

	succeeded = self.getSSHInfo()
        if succeeded == False:
            return False
        return True
        
        
    '''
    Places an order on Zappiehost for a new VPS
    '''
    def placeOrder(self):
        try:
            self.spawnBrowser()
            self.driver.get("https://www.thcservers.com/vps-hosting")
            
            
            self.driver.find_element_by_class_name("vps_submit_form").click()
            
            
            
            
            self.fillInElement("hostname", self.generator.getRAString(10))
            self.fillInElement("ns1prefix", "ns1")
            self.fillInElement("ns2prefix", "ns2")
            self.fillInElement("rootpw", self.SSHPassword)
            
            # configoption[9]
            #self.chooseSelectElement("configoption[5]", "Ubuntu 14.04")
            
            
            self.driver.execute_script("var elements = document.getElementsByName('configoption[5]'); var element = elements[0]; element.value = '87'; recalctotals();")
            
            self.driver.implicitly_wait(2)
            
            self.driver.find_element_by_class_name("checkout").click()
            
            self.driver.implicitly_wait(10)
            
            
            self.fillInElement('firstname', self.generator.getFirstName())
            self.fillInElement('lastname', self.generator.getSurname())
            self.fillInElement('email', self.email)
            self.fillInElement('address1', self.generator.getRAString(randint(8, 15)) + ' ' + self.generator.getRNString(randint(1, 2)))
            self.fillInElement('city', self.generator.getCity())
            self.fillInElement('postcode', self.generator.getZipcode())
            
            # country
            self.driver.execute_script("var element = document.getElementById('country'); element.value = 'US';")
            
            self.driver.execute_script("document.getElementById('stateselect').value = 'Kansas';")
            
            self.fillInElement('phonenumber', self.generator.getPhoneNum())
            
            # password =  # Generate a password
            self.driver.find_element_by_id("newpw").send_keys(self.password)
            #self.fillInElement('password', self.password)
            self.fillInElement('password2', self.password)
            
            self.driver.find_element_by_id('pgbtnbitpay').click()
            
            self.driver.find_element_by_name('accepttos').click()
            
            print("Email used: " + self.email)
            print("password used: " + self.password)
            
            self.driver.find_element_by_css_selector('.btn.btn-success').click()
            
            try:
                self.driver.find_element_by_css_selector('input[value="Pay Now"]').click()
	    except Exception as e:
		print("Warning: Pay now button not found")

            bitcoinAmount = self.driver.find_element_by_css_selector(".ng-binding.payment__details__instruction__btc-amount").text
            toWallet = self.driver.find_element_by_css_selector(".payment__details__instruction__btc-address.ng-binding").text
            
            
            print("amount: " + bitcoinAmount)
            print("to wallet: " + toWallet)
            
            wallet = Wallet()
            paymentSucceeded = wallet.payToAutomatically(toWallet, bitcoinAmount)
            if paymentSucceeded == False:
                return False
            
            # Wait for the transaction to be accepted
            wait = ui.WebDriverWait(self.driver, 666)
            wait.until(lambda driver: driver.find_element_by_css_selector('.payment--paid'))
            
            
            self.closeBrowser()
        
        except Exception as e:
            print("Could not complete the transaction because an error occurred:")
            print(e)
            self.closeBrowser()
            return False
            #raise # Raise the exception that brought you here 
            
        return True


    def getSSHInfo(self):
        """Retrieves the SSH login information for our bought VPS."""
        try:
            self.spawnBrowser()
            self.driver.get("https://www.thcservers.com/portal/clientarea.php?action=products")

	    print(self.email)
            self.driver.find_element_by_id('username').send_keys(self.email)
            self.driver.find_element_by_id('password').send_keys(self.password)
            self.driver.find_elements_by_name('rememberme').pop().click()

	    self.driver.find_element_by_css_selector('.btn.btn-primary.btn-large').click()

            # Wait for the transaction to be accepted
            pending = True
            tries_left = 30 # Try for 30 minutes
            first = True
            while(pending == True and tries_left > 0):
                if first == False:
                    time.sleep(60)
                    self.driver.get("https://www.thcservers.com/portal/clientarea.php?action=products")
                first = False
                tries_left = tries_left - 1
                print("Tries left: ")
                print(tries_left)
		pending = False
                try:
                    self.driver.find_element_by_css_selector(".label.active")
                except Exception as e:
                    pending = True


            if pending == True:
                return False # The VPS is still pending!

	    self.driver.find_elements_by_xpath("//*[contains(text(), 'View Details')]").pop().click()
	    

	    text = self.driver.find_elements_by_css_selector(".col2half").pop(0).text

	    print(text)
            textsplit = text.split('\n')
	    self.IP = textsplit[1]

            self.closeBrowser()

        except Exception as e:
            print("Could not complete the transaction because an error occurred:")
            print(e)
            #raise # Raise the exception that brought you here
            self.closeBrowser()
            return False

        return True
