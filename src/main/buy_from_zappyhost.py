from random import randint
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from main.BogusFormBuilder import BogusFormBuilder



def getFormValue(name):
   "function_docstring"
   return "To be implemented: " + name


def fillInElement(fieldname, value):
    #driver.find_element_by_css_selector("input[name='" + fieldname + "']").send_keys(value)
    
    # ^ send_keys has some issues, using javascript to set an attribute instead:
    driver.execute_script('arguments[0].setAttribute("value", "' + value + '")', driver.find_element_by_css_selector("input[name='" + fieldname + "']"))
    
def clickRandomSelectElement(fieldId):
    el = driver.find_element_by_id(fieldId)
    options = el.find_elements_by_tag_name('option')
    num = randint(1, len(options) - 1)
    option = options[num]
    option.click()
    
    
def placeOrder(email, password):
    try:
        
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
        fillInElement('email', email)
        fillInElement('address1', generator.getRAString(randint(8, 15)) + ' ' + generator.getRNString(randint(1, 2)))
        fillInElement('city', generator.getCity())
        fillInElement('postcode', generator.getZipcode())
        
        clickRandomSelectElement('country')
        
        select = Select(driver.find_element_by_id('country'))
        selected_text = select.first_selected_option.text;
        
        if selected_text == 'United States' or selected_text == 'Spain' or selected_text == 'Australia' or selected_text == 'Brazil' or selected_text == 'Canada' or selected_text == 'France' or selected_text == 'Germany' or selected_text == 'India' or selected_text == 'Italy' or selected_text == 'Netherlands' or selected_text == 'New Zealand' or selected_text == 'United Kingdom':
            # For US, Brazil, Canada, France, Germany, India, Italia, Netherlands, New Zealand and United Kingdom select state option in a select
            clickRandomSelectElement('stateselect')
        else:
            # For all other countries, fill in string
            fillInElement('state', generator.getRAString(randint(6, 12)))
            
        
        fillInElement('phonenumber', generator.getPhoneNum())
        
        # password =  # Generate a password
        fillInElement('password', password)
        fillInElement('password2', password)
        
        driver.find_element_by_css_selector("input[type='submit'][class='cartbutton green ui-button ui-widget ui-state-default ui-corner-all']").click() # Submit the form
        
        driver.find_element_by_css_selector("input[type='submit'][value='Pay Now']").click()
        
        
        driver.implicitly_wait(10)
        
        bitcoinAmount = driver.find_element_by_css_selector(".ng-binding.payment__details__instruction__btc-amount").text
        toWallet = driver.find_element_by_css_selector(".payment__details__instruction__btc-address.ng-binding").text
        
        print "Bitcoin amount to transfer: " + bitcoinAmount
        
        print "To wallet: " + toWallet
    
    except Exception as e:
        print "Could not complete the transaction because an error occurred:"
        print e
        #raise # Raise the exception that brought you here 

def setSSHPassword(email, password, SSHPassword):
    try:
        
        driver.get("https://billing.zappiehost.com/clientarea.php")
        
        #Click the to cart button for the cheapest VPS
        fillInElement('username', email)
        fillInElement('password', password)
        
        driver.find_element_by_id('login').click()
        
        driver.get("https://billing.zappiehost.com/clientarea.php?action=products")
        driver.find_element_by_css_selector(".table.table-striped.table-framed").find_element_by_css_selector(".btn-group").find_element_by_css_selector(".btn").click()
        
        driver.find_element_by_css_selector(".icon-btn.icon-reinstall").click()
        
        
        #driver.find_element_by_id('password')._execute(command, params)
        driver.find_element_by_id('password').send_keys(SSHPassword)
        #fillInElement("rebuild[password]", SSHPassword)
        
        driver.find_element_by_css_selector("input[value='local:vztmpl/ubuntu-14.04-64bit.tar.gz']").click()
        
        driver.find_element_by_css_selector(".form-actions").find_element_by_css_selector(".btn.btn-primary").click()
    
        print "New SSH Password: " + SSHPassword
        
    except Exception as e:
        print "Could not complete the transaction because an error occurred:"
        print e
        #raise # Raise the exception that brought you here 


driver = webdriver.Remote(
    command_executor='http://127.0.0.1:4444/wd/hub',
    desired_capabilities=DesiredCapabilities.FIREFOX)
generator = BogusFormBuilder()

email = generator.getEmail()
#password = generator.getPassword()
password = generator.getRAString(32)


#temporary, for testing:
email = "ncb21992@hotmail.com"
password = "2Rxub#21l8oR#$niEd#L08J9*MK3IiLP"

SSHPassword = generator.getRAString(32)

setSSHPassword(email, password, SSHPassword)
