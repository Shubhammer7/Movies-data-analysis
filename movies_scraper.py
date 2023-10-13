#Imports
import time
import requests
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

#Mozilla Webdriver
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5.2 Safari/605.1.15'
firefox_driver = "/opt/homebrew/bin/geckodriver"
firefox_service = Service(firefox_driver)
firefox_options = Options()
firefox_options.set_preference('general.useragent.override', user_agent)

#Url
url = 'https://www.imdb.com/title/tt1630029/?ref_=fn_al_tt_1'
response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
soup = BeautifulSoup(response.content, "html.parser")

#Lists for new columns

directors = []
top_ten_leads = []


#Launching the Webdriver
driver = webdriver.Firefox(options=firefox_options)
driver.get(url)
driver.maximize_window()
driver.implicitly_wait(10)


#Scraping


section = soup.find("section", class_ ="ipc-page-section ipc-page-section--baseAlt ipc-page-section--tp-none ipc-page-section--bp-xs sc-e226b0e3-2 fxgTov")

run_time = section.find("li", class_="ipc-inline-list__item").get_text()
print(run_time)

# search_win = driver.find_element(By.XPATH,'//*[@id="suggestion-search"]')
# time.sleep(3)
# search_win.send_keys("Avengers: Endgame")
# time.sleep(3)
# search_win.send_keys(Keys.RETURN)
# time.sleep(5)
# title = driver.find_element(By.XPATH, "/html/body/div[2]/main/div[2]/div[3]/section/div/div[1]/section[2]/div[2]/ul/li[1]/div[2]/div/a").click()
# time.sleep(5)
#
# director = soup.find('a',class_="ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link")
# print(director)

driver.quit()












