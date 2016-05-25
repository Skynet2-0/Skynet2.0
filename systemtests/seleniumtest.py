from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from agent.BogusFormBuilder import BogusFormBuilder

from agent.VPSBuyer import VPSBuyer

import selenium.webdriver.support.ui as ui


class abc(object):
    def __init__(self):
        self.driver = webdriver.Remote(
        command_executor='http://127.0.0.1:4444/wd/hub',
        desired_capabilities=DesiredCapabilities.FIREFOX)
        pass


    def somefunction(self):
        self.driver.get("http://3dsplaza.com/selenium.html")

        print("huh")

        wait = ui.WebDriverWait(self.driver,20)

        wait.until(lambda driver: driver.find_element_by_css_selector('.payment--paid'))

        print("yeah")

        self.driver.close()

        self.driver.get("http://google.com")

    def somefunction2(self):
        self.driver.get("http://3dsplaza.com/selenium2.html")

        a = self.driver.find_elements_by_xpath("//*[contains(text(), 'IP Address:')]").pop()
        rawtext = a.find_elements_by_xpath("..").pop().text
        text1 = rawtext.split('IP Address:\n', 1)
        text2 = text1[1].split('\n', 1)
        ip = text2[0]
        print(ip)

a = abc()
a.somefunction2()
