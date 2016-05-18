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
        
        succeeded = self.setSSHPassword(self.SSHPassword)
        if succeeded == False:
            return False
        return True
        
    '''
    Places an order on Offshorededi for a new VPS
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
            
            pay_page_url = self.driver.current_url()
            
            print("amount: " + bitcoinAmount)
            print("to wallet: " + toWallet)
            
            wallet = Wallet()
            paymentSucceeded = wallet.payToAutomatically(toWallet, bitcoinAmount)
            if paymentSucceeded == False:
                return False
            
            # Wait for the transaction to be accepted
            tries_left = 60 * 15
            while(self.driver.current_url() == pay_page_url and tries_left > 0):
                time.sleep(1)
                tries_left = tries_left - 1
                
            if self.driver.current_url() == pay_page_url:
                # Payment redirect failed
                return False
            
            return True #payment succeeded
            
            #self.closeBrowser()
        
        except Exception as e:
            print("Could not complete the transaction because an error occurred:")
            print(e)
            #self.closeBrowser()
            return False
            #raise # Raise the exception that brought you here 
            
        return True
    
    def setSSHPassword(self, SSHPassword = ''):
        '''
        Re-installs the VPS on Offshorededi with a new password. This is handy, so we don't have to fetch the password from an email
        '''
        if SSHPassword == '':
            SSHPassword = self.SSHPassword
        self.SSHPassword = SSHPassword
        try:
            self.spawnBrowser()
            self.driver.get("https://my.offshorededi.com/clientarea.php")
            
            #Click the to cart button for the cheapest VPS
            self.driver.find_element_by_id('inputEmail').send_keys(self.email)
            self.driver.find_element_by_id('inputPassword').send_keys(self.password)
            #self.fillInElement('username', self.email)
            #self.fillInElement('password', self.password)
            
            self.driver.find_element_by_id('login').click()
            
            self.driver.get("https://my.offshorededi.com/clientarea.php?action=services")
            
            
            # Wait for the transaction to be accepted
            pending = True
            tries_left = 60 * 24 # Try for 24 hours
            first = True
            while(pending == True and tries_left > 0):
                if first == False:
                    time.sleep(60)
                first = False
                tries_left = tries_left - 1
                print("Tries left: ")
                print(tries_left)
                try:
                    self.driver.find_element_by_css_selector(".label.status.status-pending")
                except Exception as e:
                    pending = False
                    
                
            if pending == True:
                return False # The VPS is still pending!
            
            self.driver.find_element_by_css_selector(".table.table-striped.table-framed").find_element_by_css_selector(".btn-group").find_element_by_css_selector(".btn").click()
            
            # GET THE IP ADDRESS
            a = self.driver.find_elements_by_xpath("//*[contains(text(), 'IP Address:')]").pop()
            rawtext = a.find_elements_by_xpath("..").pop().text
            text1 = rawtext.split('IP Address:\n', 1)
            text2 = text1[1].split('\n', 1)
            self.IP = text2[0]
            # END OF GET IP ADDRESS
            
            
            self.driver.find_element_by_css_selector(".icon-btn.icon-reinstall").click()
            
            
            #driver.find_element_by_id('password')._execute(command, params)
            self.driver.find_element_by_id('password').send_keys(self.SSHPassword)
            #fillInElement("rebuild[password]", SSHPassword)
            
            self.driver.find_element_by_css_selector("input[value='local:vztmpl/ubuntu-14.04-64bit.tar.gz']").click()
            
            self.driver.find_element_by_css_selector(".form-actions").find_element_by_css_selector(".btn.btn-primary").click()
        
            # print("New SSH Password: " + self.SSHPassword)
            self.closeBrowser()
            
        except Exception as e:
            print("Could not complete the transaction because an error occurred:")
            print(e)
            #raise # Raise the exception that brought you here 
            self.closeBrowser()
            return False
        
        return True