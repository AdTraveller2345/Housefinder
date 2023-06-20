import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# pararius login details
ppassword = '*'
pemail = '*'
city_name = 'Eindhoven'

#costume message
message = '''
Hi
I am interested in the advertised apartman. Please let me know if its still available for rent! 

About me:
'''

# Create a new instance of the Chrome WebDriver
driver = webdriver.Chrome()
driver.maximize_window()

# opens pararius webpage
driver.get("https://www.pararius.com/login?_target_path=/english")
driver.implicitly_wait(10)

# filling out the login fields
email = driver.find_element(By.NAME, "email")
email.send_keys(pemail)
password = driver.find_element(By.NAME, "password")
password.send_keys(ppassword)

# clicking log in button
login = driver.find_element(By.CLASS_NAME,"form__submit-button").click()

#search for eindhoven
city = driver.find_element(By.CLASS_NAME, 'autocomplete__input')
city.send_keys(city_name)
searchbutton = driver.find_element(By.CLASS_NAME,"autocomplete__item").click()

#select advertisement
ad = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CLASS_NAME, "listing-search-item__link--title")))
ad.click()
#contact the estate agency
agency_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT,"Contact the estate agent")))
# Scroll the page to the element
driver.execute_script("arguments[0].scrollIntoView();", agency_button)
agency_button.click()

#send message
message_field = driver.find_element(By.NAME, "listing_contact_agent_form[message]")
message_field.send_keys(message)
time.sleep(3)

