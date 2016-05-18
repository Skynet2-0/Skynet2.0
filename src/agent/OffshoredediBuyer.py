from random import randint
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from src.agent.BogusFormBuilder import BogusFormBuilder

from src.agent.VPSBuyer import VPSBuyer

from src.agent.Wallet import Wallet

import selenium.webdriver.support.ui as ui

import time
    
    
class OffshoredediBuyer(VPSBuyer):
    '''
    This class orders a VPS from offshorededi.com
    '''
    def __init__(self, email = "", password = "", SSHPassword = ""):
        super(OffshoredediBuyer, self).__init__()
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
    Walks through the entire process of buying a VPS from Offshorededi. Returns True if it succeeded, returns False otherwise
    '''
    def buy(self):
        succeeded = self.placeOrder() # places the order
        if succeeded == False:
            return False
        
        time.sleep(30) # Wait for half a minute so Offshorededi can process the payment
        
        
    '''
    Places an order on Zappiehost for a new VPS
    '''
    def placeOrder(self):
        try:
            self.spawnBrowser()
            self.driver.get("http://my.offshorededi.com/cart.php?a=add&pid=5")
            
            self.fillInElement("hostname", self.generator.getRAString(10))
            self.fillInElement("ns1prefix", "ns1")
            self.fillInElement("ns2prefix", "ns2")
            self.fillInElement("rootpw", self.SSHPassword)
            
            # configoption[9]
            self.chooseSelectElement("configoption[9]", "Ubuntu 14.04")
            
            self.driver.find_element_by_id("btnCompleteProductConfig").click()
            
            self.driver.implicitly_wait(10)
            
            self.fillInElement('firstname', self.generator.getFirstName())
            self.fillInElement('lastname', self.generator.getSurname())
            self.fillInElement('email', self.email)
            self.fillInElement('address1', self.generator.getRAString(randint(8, 15)) + ' ' + self.generator.getRNString(randint(1, 2)))
            self.fillInElement('city', self.generator.getCity())
            self.fillInElement('postcode', self.generator.getZipcode())
            
            self.clickRandomSelectElement('country')
            
            select = Select(self.driver.find_element_by_id('country'))
            selected_text = select.first_selected_option.text;
            
            if selected_text == 'United States' or selected_text == 'Spain' or selected_text == 'Australia' or selected_text == 'Brazil' or selected_text == 'Canada' or selected_text == 'France' or selected_text == 'Germany' or selected_text == 'India' or selected_text == 'Italy' or selected_text == 'Netherlands' or selected_text == 'New Zealand' or selected_text == 'United Kingdom':
                # For US, Brazil, Canada, France, Germany, India, Italia, Netherlands, New Zealand and United Kingdom select state option in a select
                self.clickRandomSelectElement('stateselect')
            else:
                # For all other countries, fill in string
                self.fillInElement('state', self.generator.getRAString(randint(6, 12)))
                
            
            self.fillInElement('phonenumber', self.generator.getPhoneNum())
            
            # password =  # Generate a password
            self.driver.find_element_by_id("inputNewPassword1").send_keys(self.password)
            #self.fillInElement('password', self.password)
            self.fillInElement('password2', self.password)
            
            self.driver.find_element_by_id('pgbtnblockchainv2').click()
            
            self.driver.find_element_by_name('accepttos').click()
            
            print("Email used: " + self.email)
            print("password used: " + self.password)
            
            self.driver.find_element_by_id('btnCompleteOrder').click()
            
            
            self.driver.find_element_by_name('paynow').click()
            self.driver.switch_to_frame(self.driver.find_element_by_tag_name("iframe"))
            text = self.driver.find_element_by_tag_name('body').text
            lines = text.split('\n')
            firstlinesplit = lines[0].split(' ')
            bitcoinAmount = firstlinesplit[2]
            toWallet = lines[2]
            
            print("amount: " + bitcoinAmount)
            print("to wallet: " + toWallet)
            
            wallet = Wallet()
            paymentSucceeded = wallet.payToAutomatically(toWallet, bitcoinAmount)
            if paymentSucceeded == False:
                return False
            
            # Wait for the transaction to be accepted
            wait = ui.WebDriverWait(self.driver, 666)
            wait.until(lambda driver: driver.find_element_by_css_selector('.payment--paid'))
            
            
            #self.closeBrowser()
        
        except Exception as e:
            print("Could not complete the transaction because an error occurred:")
            print(e)
            #self.closeBrowser()
            return False
            #raise # Raise the exception that brought you here 
            
        return True