from random import randint
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from BogusFormBuilder import BogusFormBuilder


class VPSBuyer(object):
    """
    This is the standard class to buy a VPS host.

    By itself, it does nothing; this class is supposed to be extended by other
    classes, each for a specific VPS Provider.

    email -- The email address. (Default is '')
    password -- The password for the account on the site. (Default is '')
    SSHUsername -- The user for the SSH Connection. (Default is 'root')
    SSHPassword -- The password for ssh connections. (Default is '')
    """
    def __init__(self, email='', password='', SSHUsername='root', SSHPassword=''):
        self.generator = BogusFormBuilder()
        #password = generator.getPassword()
        if email == "":
            self.email = self.generator.getEmail()
        else:
            self.email = email
        if password == "":
            self.password = self.generator.getRAString(32)
        else:
            self.password = password
        self.SSHUsername = SSHUsername
        self.SSHPassword = SSHPassword
        self.IP = ""

    def getFormValue(self, name):
       "function_docstring"
       return "To be implemented: " + name

    def spawnBrowser(self):
        """Spawns the browser to use when internetting."""
        self.driver = webdriver.Remote(
            command_executor='http://127.0.0.1:4444/wd/hub',
            desired_capabilities=DesiredCapabilities.FIREFOX)


    def fillInElement(self, fieldname, value):
        """
        Automatically fills ina form element by executing a piece of javascript that sets the value attribute of the form element
        """
        #driver.find_element_by_css_selector("input[name='" + fieldname + "']").send_keys(value)

        # ^ send_keys has some issues, using javascript to set an attribute instead:
        self.driver.execute_script('arguments[0].setAttribute("value", "' + value + '")', self.driver.find_element_by_css_selector("input[name='" + fieldname + "']"))

    def clickRandomSelectElement(self, fieldId):
        """
        Chooses one of the elements in a select list randomly, except for the first element.
        """
        el = self.driver.find_element_by_id(fieldId)
        options = el.find_elements_by_tag_name('option')
        num = randint(1, len(options) - 1)
        option = options[num]
        option.click()

    def chooseSelectElement(self, fieldName, fieldText):
        """
        Chooses one of the elements in a select list, by its visible text
        """
        select = Select(self.driver.find_element_by_name(fieldName));
        #select.deselect_all()
        select.select_by_visible_text(fieldText)


    def getSSHUsername(self):
        """Returns the SSH Username to log in on the bought VPS."""
        return self.SSHUsername

    def getSSHPassword(self):
        """Returns the SSH Password to log in on the bought VPS."""
        return self.SSHPassword

    def getIP(self):
        """Returns the IP Address that the VPS is installed on."""
        return self.IP

    def getEmail(self):
        """Returns the email address to log in on the VPS provider."""
        return self.email

    def getPassword(self):
        """Returns the password to log in on the VPS provider."""
        return self.password

    def closeBrowser(self):
        """Closes the current browser instance of Selenium."""
        self.driver.quit()
