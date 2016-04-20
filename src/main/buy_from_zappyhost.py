from random import randint
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.select import Select

import BogusFormBuilder



def getFormValue(name):
   "function_docstring"
   return "To be implemented: " + name


def fillInElement(fieldname, value):
    driver.find_element_by_css_selector("input[name='" + fieldname + "']").send_keys(value)
    
def clickRandomSelectElement(fieldId):
    el = driver.find_element_by_id(fieldId)
    options = el.find_elements_by_tag_name('option')
    num = randint(1, len(options) - 1)
    option = options[num]
    option.click()


driver = webdriver.Remote(
   command_executor='http://127.0.0.1:4444/wd/hub',
   desired_capabilities=DesiredCapabilities.CHROME)

driver.get("https://billing.zappiehost.com/cart.php?a=confproduct&i=0")

#Click the to cart button for the cheapest VPS
driver.find_element_by_css_selector('.cartbutton.ui-button.ui-widget.ui-state-default.ui-corner-all').click()

#Click the continue button
driver.find_element_by_css_selector('.cartbutton.green.ui-button.ui-widget.ui-state-default.ui-corner-all').click()


#Click the pay by bitcoin button
driver.find_element_by_css_selector("input[type='radio'][value='bitpay']").click()


#driver.find_element_by_css_selector("input[name='firstname']").send_keys(getFormValue('firstname'))

generator = BogusFormBuilder()


fillInElement('firstname', generator.getFirstName())
fillInElement('lastname', generator.getSurname())
fillInElement('email', generator.getEmail())
fillInElement('address1', generator.getRAString(randint(10, 20)) + generator.getRNString(randint(1, 2)))
fillInElement('city', generator.getCity())
fillInElement('postcode', generator.getZipCode())

clickRandomSelectElement('country')

print '-1'
select = Select(driver.find_element_by_id('country'))

print '0'
if select.first_selected_option.text == 'United States' or select.first_selected_option.text == 'Spain' or select.first_selected_option.text == 'Australia' or select.first_selected_option.text == 'Brazil' or select.first_selected_option.text == 'Canada' or select.first_selected_option.text == 'France' or select.first_selected_option.text == 'Germany' or select.first_selected_option.text == 'India' or select.first_selected_option.text == 'Italy' or select.first_selected_option.text == 'Netherlands' or select.first_selected_option.text == 'New Zealand' or select.first_selected_option.text == 'United Kingdom':
    # For US, Brazil, Canada, France, Germany, India, Italia, Netherlands, New Zealand and United Kingdom select state option in a select
    clickRandomSelectElement('stateselect')
    print 'a'
else:
    # For all other countries, fill in string
    fillInElement('state', getFormValue('state'))
    print 'b'
    
print 'c'

fillInElement('phonenumber', generator.getPhoneNum())

password = generator.getPassword() # Generate a password
fillInElement('password', password)
fillInElement('password2', password)

driver.find_element_by_css_selector("input[type='submit'][class='cartbutton green ui-button ui-widget ui-state-default ui-corner-all']").click() # Submit the form