import time
from bs4 import BeautifulSoup
import json
from wod import Wod


class WebPageParser:
    def __init__(self, url, driver):
        self.url = url
        self.chrome_driver = driver
        self.parsed_wod_list = []
        self.last_recorded_workout_date = self._get_last_recored_workout()

    def parse_web_page(self):
        self.chrome_driver.get(self.url)
        time.sleep(2)
        soup = BeautifulSoup(self.chrome_driver.page_source, features="html.parser")

        self.parsed_wod_list = soup.find_all('ul', {'class': 'btwb-wod-list'})
        return self._get_current_wod()

    def _get_current_wod(self):
        for wod_list_item in self.parsed_wod_list:
            wod = self._get_workout_details(wod_list_item)
            if wod:
                if self._is_wod_latest(wod):
                    return wod
        return None

    def _is_wod_latest(self, wod):
        month, day, year = self._convert_date_string_to_mmddyy(wod.date)
        month_recorded, day_recorded, year_recorded = self._convert_date_string_to_mmddyy(self.last_recorded_workout_date)
        if year > year_recorded:
            print("##############")
            return True
        if year == year_recorded:
            days = int(month)*31 + int(day)
            days_recorded = int(month_recorded)*31 + int(day_recorded)
            return days > days_recorded
        return False

    def _convert_date_string_to_mmddyy(self, date_string):
        date_string = date_string.replace(",", "")
        date_parameters = date_string.split(" ")
        month = self._month_to_num(date_parameters[0])
        day = date_parameters[1]
        year = date_parameters[2]
        return month, day, year

    def _get_workout_details(self, test):
        if test.find('h5') and test.find('small') and test.find('p'):
            title = test.find('h6').text
            date_start_index = test.find('small').text.find('-') + 2
            date = test.find('small').text[date_start_index:]
            description = test.find('p').text
            wod = Wod(date, title, description)
            return wod
        return None

    def _get_last_recored_workout(self):
        with open('config.json') as json_file:
            data = json.load(json_file)
            return data["date"]

    def _convert_to_date_object(self, date_string):
        date_string = date_string.replace(",", "")
        date_parameters = date_string.split(" ")
        return self._month_to_num(date_parameters[0])

    def _month_to_num(self, short_month):
        return{
                'Jan': 1,
                'Feb': 2,
                'Mar': 3,
                'Apr': 4,
                'May': 5,
                'Jun': 6,
                'Jul': 7,
                'Aug': 8,
                'Sep': 9,
                'Oct': 10,
                'Nov': 11,
                'Dec': 12
        }[short_month]

    def update_last_recorded_entry_in_config_file(self, date):
        with open('config.json', 'r+') as json_file:
            data = json.load(json_file)
            data["date"] = date
            json_file.seek(0)
            json.dump(data, json_file)
            json_file.truncate()

