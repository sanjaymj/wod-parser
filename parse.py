from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import time
import re

url = 'http://cf-erlangen.com/index.php/wod/'

page_response = requests.get(url, timeout=5)

path = r'C:\\Users\\Sanjay.Jayaram\\Downloads\\chromedriver_win32\\chromedriver.exe'
driver = webdriver.Chrome(executable_path = path)
driver.get(url)

time.sleep(2)
soup = BeautifulSoup(driver.page_source)

test = soup.find_all('ul',{'class':'btwb-wod-list'})
print(test[1].find('small').text)
print(test[1].find('h5').text)