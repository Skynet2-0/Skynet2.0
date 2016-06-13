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
            self.fillInElement("configoption[2]", "Ubuntu 14.04")

            self.driver.find_element_by_css_selector('.checkout').click()
            self.driver.implicitly_wait(10)
            self._fill_in_form()
            self.driver.find_element_by_css_selector('.ordernow').click()
            #self.fillInElement("hostname", self.generator.getRAString(10))
            #self.fillInElement("ns1prefix", "ns1")
            #self.fillInElement("ns2prefix", "ns2")
            #self.fillInElement("rootpw", self.SSHPassword)
            print("Email used: " + self.email)
            print("password used: " + self.password)
            #self.driver.find_element_by_id('btnCompleteOrder').click()


            self.driver.find_element_by_name('paynow').click()
            paymentSucceeded = self._pay()
            if paymentSucceeded == False:
                return False
            self._wait_for_transaction(self._still_on_paypage, 60 * 15)
            return not self._still_on_paypage()
            # If they are the same the payment failed.
            #self.closeBrowser()
        except Exception as e:
            print("Could not complete the transaction because an error occurred:")
            print(e)
            #self.closeBrowser()
            return False
            #raise # Raise the exception that brought you here

    def _fill_in_form(self):
        """Fills the form with values."""
        self.fillInElement('firstname', self.generator.getFirstName())
        self.fillInElement('lastname', self.generator.getSurname())
        self.fillInElement('email', self.email)

    def _fill_in_country(self):
        """Fill in the country on the form."""
        self.clickRandomSelectElement('country')
        select = Select(self.driver.find_element_by_id('country'))
        selected_text = select.first_selected_option.text;
        if (selected_text == 'United States' or selected_text == 'Spain' or selected_text == 'Australia'
                or selected_text == 'Brazil' or selected_text == 'Canada' or selected_text == 'France' or selected_text == 'Germany'
                or selected_text == 'India' or selected_text == 'Italy' or selected_text == 'Netherlands'
                or selected_text == 'New Zealand' or selected_text == 'United Kingdom'):
            # For US, Brazil, Canada, France, Germany, India, Italia, Netherlands, New Zealand and United Kingdom select state option in a select
            self.clickRandomSelectElement('stateselect')
        else:
            # For all other countries, fill in string
            self.fillInElement('state', self.generator.getRAString(randint(6, 12)))

    def _still_on_paypage(self):
        return self.driver.current_url == self.pay_page_url

    def _pay(self):
        self.driver.switch_to_frame(self.driver.find_element_by_tag_name("iframe"))
        text = self.driver.find_element_by_tag_name('body').text
        lines = text.split('\n')
        firstlinesplit = lines[0].split(' ')
        bitcoinAmount = firstlinesplit[2]
        toWallet = lines[2]
        self.pay_page_url = self.driver.current_url
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
            self.driver.get("https://my.yourserver.se/clientarea.php")
            self._login()
            self.driver.get("https://my.yourserver.se/clientarea.php?action=services")
            pending = self._wait_for_transaction(self._server_ready, 60 * 24, 60) # Try for 24 hours.
            if pending:
                return False # The VPS is still pending!
            self.driver.get("https://my.yourserver.se/clientarea.php?action=emails")
            onclick = self.driver.find_elements_by_css_selector(".btn.btn-info.btn-sm").pop().get_attribute('onclick')
            explode = onclick.split('\'')
            url = explode[1]
            print(url)
            self.driver.get("https://my.yourserver.se/" + url)
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
        self.driver.find_element_by_id('inputEmail').send_keys(self.email)
        self.driver.find_element_by_id('inputPassword').send_keys(self.password)
        self.driver.find_elements_by_name('rememberme').pop().click()
        self.driver.find_element_by_id('login').click()

    def _extract_information(self):
        """
        Extract the IP address and SSH Password.
        The values can then be found in self.SSHPassword and self.IP.
        """
        email = self.driver.find_element_by_css_selector(".bodyContent").text
        lines = email.split('\n')
        ipsplit = lines[7].split(',')
        ipsplit2 = ipsplit[0].split(' ')
        self.IP = ipsplit2[2]
        self.SSHPassword = lines[8].split(' ')[2]

    def _server_ready(self):
        # Check if the server is ready.
        try:
            # The block dissappears when done loading.
            self.driver.find_element_by_css_selector(".label.status.status-pending")
            self.driver.get("https://my.yourserver.se/clientarea.php?action=services")
            return False
        except Exception as e:
            return True

    def _wait_for_transaction(self, wait_test, number_of_tries, sleeptime=1, log=True, arg=None):
        """
        Waits for the transaction to be accepted.
        wait_test -- The test to perform to check whether to keep waiting. The
        footprint of the test is that it accepts only self and returns a boolean.
        It should return False if we still need to wait.
        number_of_tries -- The number of times to try if the connection
        is already working.
        sleeptime -- The time in seconds to wait between two tries. (Default is 1)
        log -- Whether to print the number of tries left to the screen. (Default is True)
        arg -- Optional argument for the wait_test function. (Default is None)
        returns True if stopped because the wait ended and False on timeout.
        """
        tries_left = number_of_tries
        done = False
        while(not done and tries_left > 0):
            tries_left = tries_left - 1
            if arg is None:
                done = wait_test()
            else:
                done = wait_test(arg)
            if not done:
                if log:
                    print("Tries left: %i" % tries_left)
                time.sleep(sleeptime)
        return done;