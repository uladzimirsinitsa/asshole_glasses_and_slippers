
import sys
import os
import pickle
import time

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from dotenv import load_dotenv


load_dotenv()

PATH_DRIVER = os.environ['PATH_DRIVER']
URL_BLOGABET = 'https://blogabet.com/'


service = Service(PATH_DRIVER)
driver = webdriver.Firefox(service=service)
driver.get(URL_BLOGABET)

print('Log in to the site.')
time.sleep(60)

pickle.dump(driver.get_cookies(), open('cookies_BLOGABET.pkl', 'wb'))

driver.quit()
sys.exit()