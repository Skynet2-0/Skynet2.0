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
from tempmail import TempMail

from pprint import pprint


class YourserverBuyer(VPSBuyer):
    """
    This class orders a VPS from yourserver.se
    """
    def __init__(self, email="", password=""):
        """
        Initializes an YourserverBuyer with the given email and password.
        email -- The email address to use.
        password -- The password to use for creating an account.
        """
        self.tm = TempMail()
        if email == "":
            email = self.tm.get_email_address()
        super(YourserverBuyer, self).__init__(email, password, "root", BogusFormBuilder().getRNString(30))


    def buy(self):
        """
        Walks through the entire process of buying a VPS from Yourserver.
        Returns True if it succeeded, returns False otherwise.
        """
        succeeded = self.placeOrder() # places the order
        if not succeeded:
            return False
        time.sleep(30) # Wait for half a minute so Yourserver can process the payment
        succeeded = self.getSSHInfo(self.SSHPassword)
        return succeeded

    def placeOrder(self):
        """Places an order on Yourserver for a new VPS."""
        try:
            self.spawnBrowser()
            self.driver.get("https://www.yourserver.se/cart.php?a=confproduct&i=0")
            self.driver.find_element_by_css_selector('.ordernow').click()
            self.driver.implicitly_wait(5)
            self.chooseSelectElement("configoption[2]", "Ubuntu 14.04")

            self.driver.find_element_by_css_selector('.checkout').click()
            self.driver.implicitly_wait(10)
            time.sleep(5)
            self._fill_in_form()
            self.driver.find_element_by_css_selector('.ordernow').click()
            
            print("Email used: " + self.email)
            print("Password used: " + self.password)
            print("SSHPassword to be used: " + self.SSHPassword)
            print("SSHUsername to be used: " + self.SSHUsername)
            
            try:
                self.driver.find_element_by_css_selector('input[value="Pay Now"]').click()
            except Exception as e:
                print("Warning: Pay now button not found")

            paymentSucceeded = self._pay()
            if not paymentSucceeded:
                return False

            # Wait for the transaction to be accepted
            wait = ui.WebDriverWait(self.driver, 666)
            wait.until(lambda driver: driver.find_element_by_css_selector('.payment--paid'))

            time.sleep(60)

            emails = self.tm.get_mailbox(self.email)
            mails_html = emails[0][u'mail_html'] + emails[1][u'mail_html']
            #print(mails_html)

            verify_url = mails_html.split('clicking the link below:<br>\n<a href=\'')[1].split('\'')[0]
            print("verify URL: " +verify_url)

            password = mails_html.split('Password: ')[1].split('\n')[0]
            self.password = password[:-2] # Split off the last two characters of the password, those are empty characters that aren't part of the password
            print("password used: " + self.password)

            self.driver.get(verify_url)

            time.sleep(10)
            self.closeBrowser()


        except Exception as e:
            print("Could not complete the transaction because an error occurred:")
            print(e)
            self.closeBrowser()
            return False
            #raise # Raise the exception that brought you here

        return True


    def _fill_in_form(self):
        """Fills the form with values."""
        print(self.generator.getFirstName())
        self.fillInElement('firstname', self.generator.getFirstName())
        self.fillInElement('lastname', self.generator.getSurname())
        self.fillInElement('email', self.email)

    def _pay(self):
        bitcoinAmount = self.driver.find_element_by_css_selector(".ng-binding.payment__details__instruction__btc-amount").text
        toWallet = self.driver.find_element_by_css_selector(".payment__details__instruction__btc-address.ng-binding").text
        print("amount: " + bitcoinAmount)
        print("to wallet: " + toWallet)
        wallet = Wallet()
        return wallet.payToAutomatically(toWallet, bitcoinAmount)

    def getSSHInfo(self, SSHPassword=''):
        """
        Retrieves the SSH login information for our bought VPS.
        SSHPassword -- The password to use for sshconnections. (Default is '')
        """
        if SSHPassword != '':
            self.SSHPassword = SSHPassword
        try:
            self.spawnBrowser()
            self.driver.get("https://www.yourserver.se/portal/clientarea.php")
            self._login()
            self.driver.get("https://www.yourserver.se/portal/clientarea.php?action=emails")


            action = self.driver.find_element_by_css_selector('.btn.btn-info').get_attribute('onclick')
            email_url = "https://www.yourserver.se/portal/viewemail.php?id=" + action.split('?id=')[1].split('\'')[0]
            self.driver.get(email_url)

            self._extract_information()
            self.closeBrowser()
        except Exception as e:
            print("Could not complete the transaction because an error occurred:")
            print(e)
            #raise # Raise the exception that brought you here
            self.closeBrowser()
            return False
        return True

    def _login(self):
        """login on the website of Yourserver."""
        self.fillInElement('username', self.email)
        self.fillInElement('password', self.password)
        self.driver.find_elements_by_name('rememberme').pop().click()
        self.driver.find_element_by_id('login').click()

    def _extract_information(self):
        """
        Extract the IP address and SSH Password.
        The values can then be found in self.SSHPassword and self.IP.
        """
        email = self.driver.find_element_by_css_selector(".popupcontainer").text
        lines = email.split('\n')
        self.IP = lines[4].split(': ')[1]
        self.SSHPassword = lines[7].split(': ')[1]

