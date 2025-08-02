from driver_manager import DriverManager as DM
from consts import BOUNDARIES_SCRIPT
import consts as c

import re

class BoundariesCapturer:
    def __init__(self):
        self.map_coords = [] # absolute coords from URL
        self.cursor_coords = [] # relative cursor coords

    def getPoints(self):
        new_driver = DM()
        new_driver.launchChromeWithSelenium(no_overlays=True)
        new_driver.injectScript(BOUNDARIES_SCRIPT)
        while new_driver.pollForVariables('selectionMode'):
            if new_driver.pollForVariables('newPointToStore'):
                self.map_coords.append(new_driver.driver.current_url)
                self.cursor_coords.append(new_driver.pollForVariables('boundaryPoint'))
                new_driver.injectScript('window.newPointToStore = false')
        new_driver.closeDriver()
        print(self.map_coords)
        print(self.cursor_coords)

    def getLatLongFromURL(self):
        for i, coord in enumerate(self.map_coords):
            _, lat, long = re.findall(c.XYZ_URL_REGEX, coord)
            self.map_coords[i] = (lat, long)



