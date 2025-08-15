from driver_manager import DriverManager as DM
from consts import BOUNDARIES_SCRIPT
import consts as c

import re
import os
import json
from decimal import Decimal
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class BoundariesCapturer:
    def __init__(self):
        self.urls = [] # strings
        self.map_coords = [] # absolute coords from URL, tuples with Decimal types
        self.cursor_coords = [] # relative cursor coords

    def getPoints(self):
        new_driver = DM()
        new_driver.launchChromeWithSelenium(no_overlays=True)
        new_driver.injectScript(BOUNDARIES_SCRIPT)

        while new_driver.pollForVariables('selectionMode'):
            if new_driver.pollForVariables('newPointToStore'):
                current_url = new_driver.driver.current_url
                zoom, (lat, long) = self.getZoomLatLongFromURL(current_url)

                if zoom != c.ZOOM:
                    new_driver.injectScript(f"alert('Point was NOT stored. Adjust zoom to {c.ZOOM} and try again.');")
                    try:
                        WebDriverWait(new_driver.driver, 300).until_not(EC.alert_is_present())
                    except TimeoutException:
                        pass
                    new_driver.injectScript('window.newPointToStore = false')
                    continue

                self.urls.append(current_url)
                self.map_coords.append((lat, long))
                self.cursor_coords.append(new_driver.pollForVariables('boundaryPoint'))
                new_driver.injectScript('window.newPointToStore = false')

        new_driver.closeDriver()
        print(self.map_coords)
        print(self.cursor_coords)

    def getZoomLatLongFromURL(self, url):
        zoom, lat, long = re.findall(c.XYZ_URL_REGEX, url)
        return (int(zoom), (lat, long))
    
    def storePoints(self):
        with open(os.path.join(c.BOUNDARIES_OUTPUT_FOLDER, f"{c.MAP_TITLE}.json"), "w") as boundaries_storage:
            json.dump([list(coord) for coord in self.map_coords], boundaries_storage)





