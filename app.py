import requests
from selenium import webdriver
import time

from email_handler import MailHandler
from web_page_parser import WebPageParser

url = 'http://cf-erlangen.com/index.php/wod/'
chrome_driver_path = r'C:\\Users\\Sanjay.Jayaram\\Downloads\\chromedriver_win32\\chromedriver.exe'

page_response = requests.get(url, timeout=5)
driver = webdriver.Chrome(executable_path=chrome_driver_path)

web_parser = WebPageParser(url, driver)
wod = web_parser.parse_web_page()

if wod:
    print(wod.date)
    print(wod.workout_name)
    print(wod.workout_description)
    subject = "Workout description " + wod.date
    email_handler = MailHandler(subject, wod.workout_name + wod.workout_description)
    email_handler.send_email()
    web_parser.update_last_recorded_entry_in_config_file(wod.date)