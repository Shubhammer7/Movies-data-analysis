from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.safari.service import Service
from selenium.webdriver.common.by import By
from safari import options

options = options
safari_service = Service(service_args=["--verbose"])

# Example usage:

driver = webdriver.Safari(service=safari_service, options=options)
driver.get("https://www.imdb.com")
# Perform actions on the webpage (e.g., find elements, click, etc.)
# element = driver.find_element(By.NAME, "q")
# element.send_keys("Selenium")
# element.send_keys(Keys.RETURN)

# Close the browser when done
driver.quit()












