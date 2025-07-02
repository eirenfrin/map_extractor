from driver_manager import DriverManager as DM
from consts import BOUNDARIES_SCRIPT

class BoundariesCapturer:
    def __init__(self):
        self.map_coords = []
        self.cursor_coords = []

    def getPoints(self):
        new_driver = DM()
        new_driver.launchChromeWithSelenium(no_overlays=False)
        new_driver.injectScript(BOUNDARIES_SCRIPT)
        while new_driver.pollForVariables('selectionMode'):
            if new_driver.pollForVariables('newPointToStore'):
                self.map_coords.append(new_driver.driver.current_url)
                self.cursor_coords.append(new_driver.pollForVariables('boundaryPoint'))
                new_driver.injectScript('window.newPointToStore = false')
        new_driver.closeDriver()
        print(self.map_coords)
        print(self.cursor_coords)
    
    def formatPoints(self):
        pass