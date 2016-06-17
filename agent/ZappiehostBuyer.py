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


class ZappiehostBuyer(VPSBuyer):
    """
    This class orders a VPS from zappiehost.com
    """
    def __init__(self, email="", password="", SSHPassword=""):
        """
        Creates a new ZappiehostBuyer.

        email -- The email address to use. (Default is '')
        password -- The password to use. (Default is '')
        SSHPassword -- The password to use for the ssh connection. (Default is '')
        """
        super(ZappiehostBuyer, self).__init__(email, password, "root", SSHPassword)

    def buy(self):
        """
        Walks through the entire process of buying a VPS from Zappiehost. 
        Returns True if it succeeded, returns False otherwise.
        """
        succeeded = self.placeOrder() # places the order
        if not succeeded:
            return False
        time.sleep(30) # Wait for half a minute so Zappiehost can process the payment
        succeeded = self.setSSHPassword(self.SSHPassword)
        return succeeded

    def placeOrder(self):
        """
        Places an order on Zappiehost for a new VPS.

        Return True if the order is succesfully handled.
        """
        try:
            self.spawnBrowser()
            self.driver.get("https://billing.zappiehost.com/cart.php?a=confproduct&i=0")
            #Click the to cart button for the cheapest VPS
            self.driver.find_element_by_css_selector('.cartbutton.ui-button.ui-widget.ui-state-default.ui-corner-all').click()
            #Click the continue button
            self.driver.find_element_by_css_selector('.cartbutton.green.ui-button.ui-widget.ui-state-default.ui-corner-all').click()
            succeeded = self._do_transaction()

            # Wait for the transaction to be accepted
            wait = ui.WebDriverWait(self.driver, 666)
            wait.until(lambda driver: driver.find_element_by_css_selector('.payment--paid'))
            self.closeBrowser()
            return succeeded
        except Exception as e:
            print("Could not complete the transaction because an error occurred:")
            print(e)
            self.closeBrowser()
            return False
            #raise # Raise the exception that brought you here

        return True

    def _do_transaction(self):
        """Does the transaction of bitcoins for the VPS."""
        #Click the pay by bitcoin button
        self.driver.find_element_by_css_selector("input[type='radio'][value='bitpay']").click()
        #driver.find_element_by_css_selector("input[name='firstname']").send_keys(getFormValue('firstname'))
        self._fill_in_form()
        paymentSucceeded = self._pay()
        if paymentSucceeded == False:
            print "payment failed"
            return False
        return True


    def _fill_in_form(self):
        """Fills in the form so """
        self.fillInElement('firstname', self.generator.getFirstName())
        self.fillInElement('lastname', self.generator.getSurname())
        self.fillInElement('email', self.email)
        self.fillInElement('address1', self.generator.getRAString(randint(8, 15)) + ' ' + self.generator.getRNString(randint(1, 2)))
        self.fillInElement('city', self.generator.getCity())
        self.fillInElement('postcode', self.generator.getZipcode())
        self.clickRandomSelectElement('country')
        self._fill_in_state()
        self.fillInElement('phonenumber', self.generator.getPhoneNum())
        # password =  # Generate a password
        self.fillInElement('password', self.password)
        self.fillInElement('password2', self.password)
        # Submit the form
        self.driver.find_element_by_css_selector("input[type='submit'][class='cartbutton green ui-button ui-widget ui-state-default ui-corner-all']").click()

    def _fill_in_state(self):
        """Fills in the state on the form."""
        select = Select(self.driver.find_element_by_id('country'))
        selected_text = select.first_selected_option.text;
        if (selected_text == 'United States' or selected_text == 'Spain' or selected_text == 'Australia' or selected_text == 'Brazil'
                or selected_text == 'Canada' or selected_text == 'France' or selected_text == 'Germany' or selected_text == 'India'
                or selected_text == 'Italy' or selected_text == 'Netherlands' or selected_text == 'New Zealand' or selected_text == 'United Kingdom'):
            # For US, Brazil, Canada, France, Germany, India, Italia, Netherlands, New Zealand and United Kingdom select state option in a select
            self.clickRandomSelectElement('stateselect')
        else:
            # For all other countries, fill in string
            self.fillInElement('state', self.generator.getRAString(randint(6, 12)))

    def _pay(self):
        self.driver.find_element_by_css_selector("input[type='submit'][value='Pay Now']").click()
        self.driver.implicitly_wait(10)
        bitcoinAmount = self.driver.find_element_by_css_selector(".ng-binding.payment__details__instruction__btc-amount").text
        toWallet = self.driver.find_element_by_css_selector(".payment__details__instruction__btc-address.ng-binding").text
        print("Bitcoin amount to transfer: " + bitcoinAmount)
        print("To wallet: " + toWallet)
        print("Username:" + self.email)
        print("Password:" + self.password)
        wallet = Wallet()
        return wallet.payToAutomatically(toWallet, bitcoinAmount)

    def setSSHPassword(self, SSHPassword=''):
        """
        Re-installs the VPS on Zappiehost with a new password. This is handy, so we don't have to fetch the password from an email.

        SSHPassword -- The password to log in over ssh. (Default is '')
        """
        if SSHPassword != '':
            self.SSHPassword = SSHPassword
        try:
            self.spawnBrowser()
            self.driver.get("https://billing.zappiehost.com/clientarea.php")
            #Click the to cart button for the cheapest VPS
            self._login()
            self.driver.get("https://billing.zappiehost.com/clientarea.php?action=products")
            self.driver.find_element_by_css_selector(".table.table-striped.table-framed").find_element_by_css_selector(".btn-group").find_element_by_css_selector(".btn").click()

            self.driver.implicitly_wait(10)
            self._get_ip_address()
            self.driver.find_element_by_css_selector(".icon-btn.icon-reinstall").click()

            self.driver.implicitly_wait(10)
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

    def _login(self):
        """Log in on Zappiehost."""
        self.fillInElement('username', self.email)
        self.fillInElement('password', self.password)
        self.driver.find_element_by_id('login').click()

    def _get_ip_address(self):
        """Find the ip address."""
        a = self.driver.find_elements_by_xpath("//*[contains(text(), 'IP Address:')]").pop()
        rawtext = a.find_elements_by_xpath("..").pop().text
        text1 = rawtext.split('IP Address:\n', 1)
        text2 = text1[1].split('\n', 1)
        self.IP = text2[0]
