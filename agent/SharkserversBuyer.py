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

from CountryGetter import CountryGetter


class SharkserversBuyer(VPSBuyer):
    '''
    This class orders a VPS from sharkservers.co.uk
    '''
    def __init__(self, email = "", password = "", SSHPassword = ""):
        super(SharkserversBuyer, self).__init__()
        self.email = email
        if self.email == "":
            self.email = self.generator.getEmail()
            

        if self.password != password or self.password == "":
            self.password = self.generator.getRAString(32) + "!"
            
        if self.SSHPassword != SSHPassword or self.SSHPassword == "":
            self.SSHPassword = self.generator.getRAString(32) # Generate new password
            
        self.SSHUsername = "root"
        pass



    def buy(self):
        '''
        Walks through the entire process of buying a VPS from Sharkservers. Returns True if it succeeded, returns False otherwise
        '''
        succeeded = self.placeOrder() # places the order
        if succeeded == False:
            return False

        time.sleep(30) # Wait for half a minute so Sharkservers can process the payment

        succeeded = self.getSSHInfo()
        if succeeded == False:
            return False
        return True



    def placeOrder(self):
        '''
        Places an order on Sharkservers for a new VPS
        '''
        try:
            self.spawnBrowser()
            self.driver.get("https://www.sharkservers.co.uk/clients/cart.php?a=add&pid=11")
            
            self.fillInElement('hostname', self.generator.getRAString(randint(8, 15)))
            self.fillInElement('rootpw', self.SSHPassword)
            
            self.chooseSelectElement("customfield[203]", "ubuntu-14.04-x86_64-minimal")
            
            
            self.driver.find_element_by_id('btnCompleteProductConfig').click()

            time.sleep(5)
            #Click the pay by bitcoin button
            self.driver.find_element_by_css_selector("input[type='radio'][value='bitpay']").click()

            
            #driver.find_element_by_css_selector("input[name='firstname']").send_keys(getFormValue('firstname'))

            self.fillInElement('firstname', self.generator.getFirstName())
            self.fillInElement('lastname', self.generator.getSurname())
            self.fillInElement('email', self.email)
            self.fillInElement('address1', self.generator.getRAString(randint(8, 15)) + ' ' + self.generator.getRNString(randint(1, 2)))
            self.fillInElement('city', self.generator.getCity())
            self.fillInElement('postcode', self.generator.getZipcode())

            # Select the country that the machine is currently in in the list of countries to seem more legible, because apparently the country you selected sometimes gets compared to your IP address
            country_found = self.clickSelectElement('country', CountryGetter.get_country())
            if(country_found != True):
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
            self.driver.find_element_by_id('inputNewPassword1').send_keys(self.password)
            self.fillInElement('password2', self.password)

            
            self.driver.find_element_by_id('btnCompleteOrder').click() # Submit the form

            try:
            	self.driver.find_element_by_css_selector("input[type='submit'][value='Pay Now']").click()
            except Exception as e:
				print("Warning: Pay now button not found")

            self.driver.implicitly_wait(10)

            bitcoinAmount = self.driver.find_element_by_css_selector(".ng-binding.payment__details__instruction__btc-amount").text
            toWallet = self.driver.find_element_by_css_selector(".payment__details__instruction__btc-address.ng-binding").text

            print("Bitcoin amount to transfer: " + bitcoinAmount)

            print("To wallet: " + toWallet)

            print("Username:" + self.email)
            print("Password:" + self.password)


            wallet = Wallet()
            paymentSucceeded = wallet.payToAutomatically(toWallet, bitcoinAmount)
            if paymentSucceeded == False:
                print "payment failed"
                return False

            # Wait for the transaction to be accepted
            wait = ui.WebDriverWait(self.driver, 666)
            wait.until(lambda driver: driver.find_element_by_css_selector('.payment--paid'))
            self.closeBrowser()
            
            return True #payment succeeded

        except Exception as e:
            print("Could not complete the transaction because an error occurred:")
            print(e)
            self.closeBrowser()
            return False
            #raise # Raise the exception that brought you here

        return True


    def getSSHInfo(self):
        '''
        Obtains the bought VPS' IP Address from Sharkservers
        '''
        try:
            self.spawnBrowser()
            self.driver.get("https://www.sharkservers.co.uk/clients/clientarea.php")

            #Click the to cart button for the cheapest VPS
            self.driver.find_element_by_id('inputEmail').send_keys(self.email)
            self.driver.find_element_by_id('inputPassword').send_keys(self.password)

            self.driver.find_elements_by_name('rememberme').pop().click()
            return

            self.driver.find_element_by_id('login').click()

            self.driver.get("https://www.sharkservers.co.uk/clients/clientarea.php?action=services")
            self.driver.find_element_by_css_selector('.label.status.status-active').click()

            # GET THE IP ADDRESS
            cols = self.driver.find_elements_by_css_selector('.col-sm-7.text-left')
            self.IP = cols[1].text
            # END OF GET IP ADDRESS

            self.closeBrowser()

        except Exception as e:
            print("Could not complete the transaction because an error occurred:")
            print(e)
            #raise # Raise the exception that brought you here
            self.closeBrowser()
            return False

        return True
