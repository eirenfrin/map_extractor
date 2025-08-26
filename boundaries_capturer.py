from driver_manager import DriverManager as DM
from consts import BOUNDARIES_SCRIPT
import consts as c

import re
import os
import json
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class BoundariesCapturer:
    """
    Captures and processes URLs of views that user marks by pressing 'b' on the keyboard.

     Attributes:
        urls (list): Contains strings, full URL address
        map_coords(list): Contains tuples with two strings, latitude and longitude extracted from each URL
    """
    
    def __init__(self):
        self.urls = [] 
        self.map_coords = []

    def get_points(self):
        new_driver = DM()
        new_driver.launch_chrome_with_selenium()
        new_driver.inject_script(BOUNDARIES_SCRIPT)

        while new_driver.poll_for_variables('selectionMode'):
            if not new_driver.poll_for_variables('newPointToStore'):
                continue
            
            current_url = new_driver.driver.current_url
            zoom, (lat, long) = self.get_zoom_lat_long_from_url(current_url)

            if zoom != c.zoom:
                new_driver.inject_script(f"alert('Point was NOT stored. Adjust zoom to {c.zoom} and try again.');")
                try:
                    WebDriverWait(new_driver.driver, 300).until_not(EC.alert_is_present())
                except TimeoutException:
                    pass
                new_driver.inject_script('window.newPointToStore = false')
                continue

            self.urls.append(current_url)
            self.map_coords.append((lat, long))
            new_driver.inject_script('window.newPointToStore = false')

        new_driver.close_driver()

    def get_zoom_lat_long_from_url(self, url):
        zoom, lat, long = re.findall(c.XYZ_URL_REGEX, url)
        return (int(zoom), (lat, long))
    
    def store_points(self):
        json_path = os.path.join(c.BOUNDARIES_OUTPUT_FOLDER, f"{c.map_title}.json")
        with open(json_path, "r") as boundaries_storage:
            json_data = json.load(boundaries_storage)
            json_data['data'] = [list(coord) for coord in self.map_coords]   

        with open(json_path, "w") as boundaries_storage:
            json.dump(json_data, boundaries_storage)




